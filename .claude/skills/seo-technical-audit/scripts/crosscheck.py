#!/usr/bin/env python3
"""
crosscheck.py — reconcile evidence sources against each other and flag tool output
that contradicts other evidence, BEFORE any finding is written.

    python3 crosscheck.py <evidence_dir> <audit_dir>

Writes <audit_dir>/00-crosschecks.md.

Why this runs first: an audit tool's own finding is evidence of what the tool
concluded, not evidence of the condition. Several of the checks below exist because
a tool asserted something its own companion export disproves. Writing findings from
unverified tool output is the fastest way to put a false claim in front of a client.

Every check emits one of:
  CONTRADICTED — another source disproves the tool's claim. Do not write the finding.
  UNVERIFIED   — nothing corroborates it. Corroborate or downgrade confidence.
  CONFIRMED    — corroborated by an independent source.
  LIMITATION   — evidence is insufficient to check; record in Assumptions.
"""

import csv, os, re, sys, glob

try:
    import openpyxl
except ImportError:
    openpyxl = None


def norm_url(u):
    if not u:
        return ""
    s = re.sub(r"^https?://", "", str(u).strip(), flags=re.I)
    s = re.sub(r"^www\.", "", s, flags=re.I)
    return s.split("#")[0].rstrip("/").lower()


def norm_header(h):
    return re.sub(r"\s+", " ", str(h or "").replace("\ufeff", "").strip().lower())


def load(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".tsv", ".txt"):
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            rows = list(csv.reader(fh, delimiter="\t" if ext == ".tsv" else ","))
    elif ext in (".xlsx", ".xlsm") and openpyxl:
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        return [], []
    if not rows:
        return [], []
    return [norm_header(h) for h in rows[0]], rows[1:]


def find_files(evidence_dir):
    """Map export kind -> (path, headers, rows), reusing the ingest fingerprints."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ingest_evidence import fingerprint  # noqa
    found = {}
    for root, _, files in os.walk(evidence_dir):
        for fn in sorted(files):
            if fn.startswith("~$") or fn.startswith("."):
                continue
            p = os.path.join(root, fn)
            if os.path.splitext(fn)[1].lower() not in (".csv", ".tsv", ".txt",
                                                       ".xlsx", ".xlsm"):
                continue
            h, r = load(p)
            kind, _ = fingerprint(h)
            if kind:
                found.setdefault(kind, []).append((p, h, r))
    return found


def col(headers, *names):
    for n in names:
        if n in headers:
            return headers.index(n)
    return None


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_orphans(found, out):
    """A tool's orphan flag vs. the link-level export it shipped alongside.

    The failure this catches: crawlers that index pages under one host form
    (www) and record link targets under another (apex) will report every page as
    an orphan. The orphan list and the anchor-text export then contradict each
    other inside the same tool's output.
    """
    orph_src = found.get("siteauditor.internal_links") or []
    link_src = (found.get("siteauditor.anchor_text") or
                found.get("screamingfrog.all_inlinks") or [])
    if not orph_src:
        return
    if not link_src:
        out.append(("LIMITATION", "Orphan claims",
                    "Tool reports orphans but no link-level export is present to "
                    "corroborate. A crawl alone cannot prove a URL has no inlinks."))
        return

    _, h, rows = orph_src[0]
    iu, it = col(h, "url"), col(h, "issue type")
    orphans = [r[iu] for r in rows
               if it is not None and str(r[it]).strip().lower() == "orphan"]

    inbound = {}
    for _, lh, lrows in link_src:
        ti = col(lh, "target url", "destination")
        if ti is None:
            continue
        for r in lrows:
            if ti < len(r) and r[ti]:
                k = norm_url(r[ti])
                inbound[k] = inbound.get(k, 0) + 1

    contra = [(u, inbound.get(norm_url(u), 0)) for u in orphans
              if inbound.get(norm_url(u), 0) > 0]

    if contra:
        contra.sort(key=lambda x: -x[1])
        lines = "\n".join(f"  - {n} inbound links → {u}" for u, n in contra[:10])
        more = f"\n  …and {len(contra)-10} more" if len(contra) > 10 else ""
        out.append(("CONTRADICTED", "Orphan claims",
                    f"{len(contra)} of {len(orphans)} pages flagged as orphans DO have "
                    f"inbound internal links in the link-level export from the same "
                    f"tool. Almost always a host-normalization defect (www vs apex).\n"
                    f"{lines}{more}\n"
                    f"  → Do not write an orphan finding. Record the tool defect as a "
                    f"limitation and re-derive orphan status from the link export."))
    elif orphans:
        out.append(("CONFIRMED", "Orphan claims",
                    f"{len(orphans)} orphan flags corroborated — none appear as link "
                    f"targets in the link-level export."))


def check_host_consistency(found, out):
    """Mixed www/apex across exports is both a finding and a confounder."""
    hosts = {}
    for kind, entries in found.items():
        for _, h, rows in entries:
            for name in ("url", "address", "source url", "target url"):
                i = col(h, name)
                if i is None:
                    continue
                for r in rows[:4000]:
                    if i < len(r) and r[i]:
                        m = re.match(r"^https?://([^/]+)", str(r[i]))
                        if m:
                            hosts.setdefault(m.group(1).lower(), set()).add(kind)
    apex = {h for h in hosts if not h.startswith("www.")}
    www = {h for h in hosts if h.startswith("www.")}
    if apex and www:
        pairs = [h for h in apex if f"www.{h}" in www]
        if pairs:
            out.append(("CONTRADICTED", "Host consistency",
                        f"Both apex and www forms appear across exports for: "
                        f"{', '.join(sorted(pairs))}. Every URL-keyed comparison in "
                        f"this audit must normalize host before matching, and the "
                        f"host split itself is a canonical/redirect finding to verify "
                        f"against live response codes."))


def check_crawl_coverage(found, out):
    """Overview page-count vs. the page inventory it claims to describe."""
    ov = found.get("siteauditor.overview")
    pg = found.get("siteauditor.pages")
    if not (ov and pg):
        return
    _, oh, orows = ov[0]
    ci = col(oh, "pages crawled")
    if ci is None or not orows:
        return
    claimed = orows[0][ci]
    actual = len(pg[0][2])
    if str(claimed).strip() and int(claimed) != actual:
        out.append(("UNVERIFIED", "Crawl coverage",
                    f"Overview reports {claimed} pages crawled; the page export "
                    f"contains {actual} rows. Reconcile before using either as a "
                    f"denominator for any percentage."))
    else:
        out.append(("CONFIRMED", "Crawl coverage",
                    f"Overview page count matches the page export ({actual})."))


def check_rendering(found, out):
    """JS-dependency evidence — governs whether raw-HTML findings are safe."""
    js = found.get("screamingfrog.javascript_all")
    if not js:
        out.append(("LIMITATION", "Rendering",
                    "No JS rendering export present. Per the Agency Profile our "
                    "standing crawler is the DataforSEO OnPage API in basic mode (no "
                    "JavaScript rendering; free Screaming Frog is the fallback), so this "
                    "is expected, not a gap. Any finding that would depend on what Google "
                    "renders is marked Needs Evidence. Do not recommend re-crawling with "
                    "rendering unless Paul asks (JavaScript mode costs 10x)."))
        return
    _, h, rows = js[0]
    wi = col(h, "js word count %")
    hi, ri = col(h, "html h1"), col(h, "rendered html h1")
    rwi = col(h, "rendered html word count")

    # First establish whether rendering was actually captured. If the rendered
    # columns are systematically empty, the crawl ran without rendering — the
    # correct conclusion is "unknown", not "content disappears on render".
    if ri is not None and rows:
        rendered_empty = sum(1 for r in rows
                             if ri >= len(r) or not str(r[ri] or "").strip())
        if rendered_empty / len(rows) > 0.9:
            out.append(("LIMITATION", "Rendering",
                        f"Rendered columns empty on {rendered_empty}/{len(rows)} rows. "
                        f"This is our standing configuration (DataforSEO OnPage, basic "
                        f"mode, no JavaScript rendering), NOT evidence that content "
                        f"disappears on render and NOT a defect to report.\n"
                        f"  Consequence: JS dependency is unknown. Any finding that "
                        f"would rest on what Google renders is marked Needs Evidence.\n"
                        f"  State this ONCE in Assumptions and Limitations. Never per "
                        f"finding. Do not recommend re-crawling with rendering."))
            return

    heavy = 0
    h1diff = 0
    for r in rows:
        try:
            if wi is not None and r[wi] not in (None, "") and float(
                    str(r[wi]).replace("%", "")) >= 30:
                heavy += 1
        except ValueError:
            pass
        if hi is not None and ri is not None and hi < len(r) and ri < len(r):
            if str(r[hi] or "").strip() != str(r[ri] or "").strip():
                h1diff += 1
    msg = (f"{heavy} pages derive ≥30% of word count from JS; {h1diff} pages have an "
           f"H1 that differs between raw and rendered HTML.")
    if heavy or h1diff:
        out.append(("CONTRADICTED", "Rendering",
                    msg + " Raw-HTML on-page findings are unsafe on these URLs — use "
                          "the rendered values."))
    else:
        out.append(("CONFIRMED", "Rendering",
                    "Raw and rendered HTML agree on the sampled fields; raw-HTML "
                    "on-page findings are safe."))


def check_crawl_truncation(found, out):
    """Our free licence caps the crawl at 500 URLs.

    A crawl that stopped at the cap is partial by definition, and a percentage
    computed against it is wrong in a way nobody notices. Detect it rather than
    letting the analyst assume full coverage.
    """
    crawl = (found.get("screamingfrog.internal_all") or
             found.get("siteauditor.pages") or [])
    if not crawl:
        return
    n = len(crawl[0][2])
    if n >= 495:
        out.append(("UNVERIFIED", "Crawl coverage vs licence cap",
                    f"The crawl returned {n} URLs against a 500-URL licence cap. It is "
                    f"very likely truncated, so the site is larger than this export "
                    f"shows.\n"
                    f"  Do not compute any percentage against {n} as a denominator, and "
                    f"do not treat absence from this export as evidence a URL does not "
                    f"exist — that is the orphan trap.\n"
                    f"  Reconcile against the sitemap and CMS export to size the gap, "
                    f"and record the cap as a limitation."))
    else:
        out.append(("CONFIRMED", "Crawl coverage vs licence cap",
                    f"{n} URLs crawled, below the 500 cap — coverage is not truncated "
                    f"by the licence."))


def check_tool_findings_are_not_findings(found, out):
    """Tool issue lists are inputs, not findings."""
    total = 0
    for kind in ("siteauditor.issues", "siteauditor.ai_engines",
                 "siteauditor.internal_links"):
        for _, _, rows in found.get(kind, []):
            total += len(rows)
    if total:
        out.append(("UNVERIFIED", "Tool issue lists",
                    f"{total} tool-generated issue rows are present. These are "
                    f"evidence of what a tool concluded, not of the condition. Each "
                    f"one that becomes a finding needs an independent corroborating "
                    f"source, and none may be promoted in bulk. A single tool score "
                    f"is never proof."))


def check_indexability_vs_inventory(found, out):
    """CMS inventory vs crawl — the real orphan-candidate reconciliation."""
    cms = found.get("cms.wordpress_all_urls")
    crawl = (found.get("screamingfrog.internal_all") or
             found.get("siteauditor.pages") or [])
    if not (cms and crawl):
        return
    _, ch, crows = cms[0]
    ci = col(ch, "url")
    cms_urls = {norm_url(r[ci]) for r in crows if ci is not None and ci < len(r) and r[ci]}
    _, kh, krows = crawl[0]
    ki = col(kh, "address", "url")
    crawl_urls = {norm_url(r[ki]) for r in krows if ki is not None and ki < len(r) and r[ki]}
    only_cms = cms_urls - crawl_urls
    only_crawl = crawl_urls - cms_urls
    if only_cms or only_crawl:
        out.append(("UNVERIFIED", "Inventory reconciliation",
                    f"{len(only_cms)} URLs exist in the CMS export but were not "
                    f"crawled; {len(only_crawl)} were crawled but are absent from the "
                    f"CMS export. These are orphan *candidates* only — resolve against "
                    f"sitemaps, Search Console, analytics, backlinks, GBP destinations "
                    f"and paid landing pages before any is called an orphan."))


def check_citation_nap(found, out):
    cit = found.get("citationtracker.audit")
    if not cit:
        return
    _, h, rows = cit[0]
    issues = {}
    for label in ("business name issue", "address issue", "zip/postcode issue",
                  "phone number issue"):
        i = col(h, label)
        if i is None:
            continue
        n = sum(1 for r in rows if i < len(r) and str(r[i] or "").strip()
                not in ("", "None", "-"))
        if n:
            issues[label] = n
    if issues:
        detail = ", ".join(f"{k}: {v}" for k, v in issues.items())
        out.append(("UNVERIFIED", "Citation NAP",
                    f"Citation tracker reports discrepancies ({detail}). Each is a "
                    f"discrepancy against the tracker's stored NAP, which is not "
                    f"automatically the verified NAP. Reconcile against the Intake "
                    f"Client Control Record before treating any as an error."))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    evidence_dir, audit_dir = sys.argv[1], sys.argv[2]
    found = find_files(evidence_dir)
    out = []
    for fn in (check_orphans, check_host_consistency, check_crawl_coverage,
               check_crawl_truncation,
               check_rendering, check_tool_findings_are_not_findings,
               check_indexability_vs_inventory, check_citation_nap):
        try:
            fn(found, out)
        except Exception as e:  # a failed check must not stop the rest
            out.append(("LIMITATION", fn.__name__,
                        f"Check could not complete: {e}"))

    os.makedirs(audit_dir, exist_ok=True)
    path = os.path.join(audit_dir, "00-crosschecks.md")
    order = {"CONTRADICTED": 0, "UNVERIFIED": 1, "LIMITATION": 2, "CONFIRMED": 3}
    out.sort(key=lambda x: order.get(x[0], 9))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# Evidence cross-checks\n\n")
        fh.write("Run before any finding is written. CONTRADICTED items block the "
                 "related finding outright.\n\n")
        fh.write(f"Sources recognised: {', '.join(sorted(found))}\n\n")
        for status, title, body in out:
            fh.write(f"## [{status}] {title}\n\n{body}\n\n")
    print(f"wrote {path}")
    for status, title, _ in out:
        print(f"  [{status}] {title}")
    blocked = sum(1 for s, _, _ in out if s == "CONTRADICTED")
    if blocked:
        print(f"\n{blocked} CONTRADICTED check(s) — do not write the related findings.")


if __name__ == "__main__":
    main()
