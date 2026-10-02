#!/usr/bin/env python3
"""
ingest_evidence.py — fingerprint every export in an evidence folder, normalize what
can be normalized, and write the evidence manifest plus the URL inventory.

    python3 ingest_evidence.py <evidence_dir> <audit_dir>

Identifies exports by header signature rather than filename, because filenames vary
by client, VA and export date while the tool's column set does not.

Writes:
    <audit_dir>/00-manifest.csv        one row per export, with recognised type
    <audit_dir>/00-unrecognised.md     anything it could not fingerprint
    <audit_dir>/inventories/urls.csv   normalized URL inventory across all sources

Never discards a file it cannot identify — unknown exports are listed for the analyst.
"""

import csv, json, os, re, sys, hashlib, datetime

try:
    import openpyxl
except ImportError:
    openpyxl = None

# --------------------------------------------------------------------------
# Fingerprints: (required column subset) -> export type.
# Matching is on normalized lowercase headers; a signature matches when every
# column in it is present. Longest signature wins, so specific beats generic.
# --------------------------------------------------------------------------
SIGNATURES = [
    # --- Screaming Frog ---
    (["address", "content type", "status code", "indexability", "title 1",
      "canonical link element 1", "word count", "crawl depth"],
     "screamingfrog.internal_all", "crawl"),
    (["address", "content type", "status code", "status", "crawl depth", "inlinks"],
     "screamingfrog.external_all", "crawl"),
    (["address", "indexability", "crawl depth", "link score", "inlinks",
      "unique inlinks", "outlinks"],
     "screamingfrog.links_all", "crawl"),
    (["address", "status code", "html word count", "rendered html word count",
      "js word count %"],
     "screamingfrog.javascript_all", "crawl"),
    (["address", "occurrences", "h1-1", "h1-1 length", "indexability"],
     "screamingfrog.h1_all", "crawl"),
    (["address", "occurrences", "h2-1", "h2-1 length", "indexability"],
     "screamingfrog.h2_all", "crawl"),
    (["address", "occurrences", "title 1", "title 1 length", "indexability"],
     "screamingfrog.page_titles_all", "crawl"),
    (["address", "occurrences", "meta description 1", "meta description 1 length"],
     "screamingfrog.meta_description_all", "crawl"),
    (["source", "destination", "anchor text", "status code"],
     "screamingfrog.all_inlinks", "crawl"),

    # --- site auditor (overview / pages / issues / links / anchors / images / ai) ---
    (["domain", "audit date", "pages crawled", "issues count", "seo score"],
     "siteauditor.overview", "crawl"),
    (["url", "title", "status", "depth", "type", "indexable", "dom parity"],
     "siteauditor.pages", "crawl"),
    (["issue", "description", "layer", "severity", "category", "urls count",
      "affected urls"],
     "siteauditor.issues", "tool_findings"),
    (["issue", "description", "severity", "category", "affected urls"],
     "siteauditor.ai_engines", "tool_findings"),
    (["url", "title", "depth", "inlinks", "status code", "issue type",
      "issue reason"],
     "siteauditor.internal_links", "tool_findings"),
    (["source url", "target url", "anchor text", "is image link"],
     "siteauditor.anchor_text", "crawl"),
    (["image url", "alt text", "has alt", "external", "lazy loaded"],
     "siteauditor.images", "crawl"),

    # --- citations ---
    (["domain", "status", "domain authority", "key citation", "business name",
      "business name issue", "address issue", "phone number issue"],
     "citationtracker.audit", "citations"),

    # --- CMS ---
    (["post id", "title", "url", "status", "categories", "slug", "post type"],
     "cms.wordpress_all_urls", "cms_inventory"),

    # --- search console / analytics ---
    (["query", "clicks", "impressions", "ctr", "position"],
     "gsc.queries", "measurement"),
    (["page", "clicks", "impressions", "ctr", "position"],
     "gsc.pages", "measurement"),
    (["url", "coverage state", "last crawl"],
     "gsc.page_indexing", "measurement"),
]

URL_COLS = ["address", "url", "page", "target url", "source url", "image url", "domain"]


def norm_header(h):
    return re.sub(r"\s+", " ", str(h or "").replace("\ufeff", "").strip().lower())


def norm_url(u):
    """Host- and slash-insensitive URL key. This is not cosmetic — see crosscheck.py."""
    if not u:
        return ""
    s = str(u).strip()
    s = re.sub(r"^https?://", "", s, flags=re.I)
    s = re.sub(r"^www\.", "", s, flags=re.I)
    s = s.split("#")[0]
    return s.rstrip("/").lower()


def read_headers_and_rows(path, limit=None):
    """Return (headers, rows) for csv/xlsx. rows are lists."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".tsv", ".txt"):
        delim = "\t" if ext == ".tsv" else ","
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            r = csv.reader(fh, delimiter=delim)
            rows = []
            for i, row in enumerate(r):
                rows.append(row)
                if limit and i > limit:
                    break
        if not rows:
            return [], []
        return rows[0], rows[1:]
    if ext in (".xlsx", ".xlsm") and openpyxl:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        if not rows:
            return [], []
        return rows[0], rows[1:]
    return [], []


def fingerprint(headers):
    hs = {norm_header(h) for h in headers if h is not None}
    # Freeform sheets whose first cell is the label rather than a column set.
    first = norm_header(headers[0]) if headers else ""
    if first == "search terms":
        return "localserp.audit_sheet", "local_visibility"
    best = None
    for cols, kind, category in SIGNATURES:
        if all(c in hs for c in cols):
            if best is None or len(cols) > best[0]:
                best = (len(cols), kind, category)
    return (best[1], best[2]) if best else (None, None)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def harvest_urls(headers, rows, kind):
    """Pull URLs out of whichever column holds them, with a source tag."""
    hs = [norm_header(h) for h in headers]
    idxs = [i for i, h in enumerate(hs) if h in URL_COLS]
    out = []
    for row in rows:
        for i in idxs:
            if i < len(row) and row[i]:
                v = str(row[i])
                if v.startswith("http") or hs[i] == "domain":
                    out.append((norm_url(v), v, hs[i], kind))
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    evidence_dir, audit_dir = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(audit_dir, "inventories"), exist_ok=True)

    manifest, unknown, all_urls = [], [], {}

    for root, _, files in os.walk(evidence_dir):
        for fn in sorted(files):
            if fn.startswith("~$") or fn.startswith("."):
                continue
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (".csv", ".tsv", ".txt", ".xlsx", ".xlsm"):
                continue
            headers, rows = read_headers_and_rows(path)
            kind, category = fingerprint(headers)
            stat = os.stat(path)
            row = {
                "source_id": "",
                "file": os.path.relpath(path, evidence_dir),
                "recognised_as": kind or "UNRECOGNISED",
                "category": category or "",
                "rows": len(rows),
                "columns": len(headers),
                "sha256_12": sha(path),
                "file_modified": datetime.datetime.fromtimestamp(
                    stat.st_mtime).isoformat(timespec="seconds"),
                "tool_settings": "",     # analyst fills: UA, rendering, scope
                "date_window": "",       # analyst fills
                "geography_device": "",  # analyst fills
                "scope_limits": "",      # analyst fills
            }
            manifest.append(row)
            if not kind:
                unknown.append((row["file"], [norm_header(h) for h in headers][:15]))
                continue
            for key, raw, col, k in harvest_urls(headers, rows, kind):
                if not key:
                    continue
                rec = all_urls.setdefault(key, {"url_key": key, "example_raw": raw,
                                                "seen_in": set(), "hosts": set()})
                rec["seen_in"].add(k)
                m = re.match(r"^https?://([^/]+)", raw)
                if m:
                    rec["hosts"].add(m.group(1).lower())

    for i, row in enumerate(sorted(manifest, key=lambda r: r["file"]), 1):
        row["source_id"] = f"SRC-{i:03d}"

    man_path = os.path.join(audit_dir, "00-manifest.csv")
    with open(man_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(manifest[0].keys()) if manifest else
                           ["source_id", "file", "recognised_as"])
        w.writeheader()
        for row in sorted(manifest, key=lambda r: r["source_id"]):
            w.writerow(row)

    inv_path = os.path.join(audit_dir, "inventories", "urls.csv")
    with open(inv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["url_key", "example_raw", "source_count", "seen_in", "hosts",
                    "host_variants"])
        for key in sorted(all_urls):
            r = all_urls[key]
            w.writerow([r["url_key"], r["example_raw"], len(r["seen_in"]),
                        ";".join(sorted(r["seen_in"])), ";".join(sorted(r["hosts"])),
                        len(r["hosts"])])

    if unknown:
        with open(os.path.join(audit_dir, "00-unrecognised.md"), "w",
                  encoding="utf-8") as fh:
            fh.write("# Unrecognised exports\n\n")
            fh.write("These were not fingerprinted. Identify them manually and add a "
                     "signature to `ingest_evidence.py` if they recur.\n\n")
            for f, hs in unknown:
                fh.write(f"## {f}\nFirst headers: `{', '.join(hs)}`\n\n")

    recognised = sum(1 for m in manifest if m["recognised_as"] != "UNRECOGNISED")
    print(f"manifest:   {man_path}  ({recognised}/{len(manifest)} recognised)")
    print(f"urls:       {inv_path}  ({len(all_urls)} unique)")
    if unknown:
        print(f"unrecognised: {len(unknown)} — see 00-unrecognised.md")
    print("\nManifest columns tool_settings / date_window / geography_device / "
          "scope_limits are blank by design — fill them before the Phase 0 readiness check.")


if __name__ == "__main__":
    main()
