#!/usr/bin/env python3
"""
ingest_evidence.py — fingerprint every export in an evidence folder, normalize what
can be normalized, and write the evidence manifest plus the URL inventory.

    python3 ingest_evidence.py <evidence_dir> <audit_dir> [--client-dir DIR] [--no-extra]

Identifies exports by header signature rather than filename, because filenames vary
by client, VA and export date while the tool's column set does not.

Also takes the client's other evidence into the same manifest, one row per file: the
data-step outputs under `clients/<slug>/data/` (reviews, rankings, backlinks, local grid,
PAA, fan-out, citations, GSC — whatever exists) and the files under `clients/<slug>/inputs/`
outside the crawl folder (SEOPress / WordPress settings evidence, Local Dominator PDFs,
sitemap URL lists, live-page captures). The client folder is found from <evidence_dir>
(…/clients/<slug>/…) or given with --client-dir; --no-extra reads the crawl folder only.
Those files are recognised by the folder they sit in (our own scripts wrote them), so
they never go to 00-unrecognised.md. A `raw/` folder is one row (file count, total size).

Writes:
    <audit_dir>/00-manifest.csv        one row per export / evidence file, with recognised type
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

    # --- DataforSEO OnPage (scripts/crawl.py) — tables Screaming Frog has no equivalent for ---
    (["duplicated value", "pages sharing it", "address", "status code"],
     "dataforseo.duplicate_tags", "crawl"),
    (["address", "similar address", "similarity (0-10)"],
     "dataforseo.duplicate_content", "crawl"),
    (["chain id", "hop", "from url", "to url", "redirect loop"],
     "dataforseo.redirect_chains", "crawl"),
    (["address", "non-indexable reason"],
     "dataforseo.non_indexable", "crawl"),

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

TABULAR = (".csv", ".tsv", ".txt", ".xlsx", ".xlsm")

# clients/<slug>/data/<folder>/ -> (recognised_as, category). Written by our own scripts
# (reviews.py, rankings.py, dfs backlinks, grid_pdf.py, paa.py, fanout.py …).
DATA_FOLDERS = {
    "reviews":   ("data.reviews (S06)", "reviews"),
    "rankings":  ("data.rankings (S07)", "rankings"),
    "backlinks": ("data.backlinks (S08)", "backlinks"),
    "citations": ("data.citations (S09)", "citations"),
    "local-grid": ("data.local_grid (S10)", "local_visibility"),
    "gsc":       ("data.gsc (S11)", "measurement"),
    "paa":       ("data.paa (S19)", "content_research"),
    "fanout":    ("data.fanout (S21)", "content_research"),
}
# clients/<slug>/inputs/<folder>/ (outside the crawl folder) -> (recognised_as, category)
INPUT_FOLDERS = {
    "local-grid": ("localdominator.grid_pdf (S10)", "local_visibility"),
    "live-pages": ("manual.live_capture", "crawl_supplement"),
    "gsc":        ("gsc.export (S11)", "measurement"),
    "citations":  ("citations.export (S09)", "citations"),
}


def is_sitemap(path):
    """A sitemap URL list: the file name says sitemap (txt / xml / csv)."""
    fn = os.path.basename(path).lower()
    return "sitemap" in fn and os.path.splitext(fn)[1] in (".txt", ".xml", ".csv")


def sitemap_urls(path):
    """URLs listed in a sitemap file: <loc> values in XML, else every line that starts
    with http (first token). Child-sitemap entries (*.xml) are dropped."""
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        text = fh.read()
    if "<loc>" in text.lower():
        urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text, flags=re.I)
    else:
        urls = [re.split(r"[\s,]", ln.strip())[0] for ln in text.splitlines()
                if ln.strip().lower().startswith("http")]
    return [u for u in urls if not u.lower().split("?")[0].endswith(".xml")]


def client_dir_for(evidence_dir):
    """clients/<slug>/ from a path inside it, else None."""
    parts = os.path.abspath(evidence_dir).split(os.sep)
    if "clients" in parts:
        i = len(parts) - 1 - parts[::-1].index("clients")
        if i + 1 < len(parts):
            return os.sep.join(parts[:i + 2])
    return None


def extra_files(client_dir, evidence_dir):
    """Evidence outside the crawl folder: data/** and inputs/** (minus the crawl folder).
    Yields (path, kind, category, raw_dir_or_None). raw/ folders are yielded once."""
    if not client_dir:
        return
    ev = os.path.abspath(evidence_dir)
    for top, table in (("data", DATA_FOLDERS), ("inputs", INPUT_FOLDERS)):
        base = os.path.join(client_dir, top)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            ar = os.path.abspath(root)
            if ar == ev or ar.startswith(ev + os.sep):
                dirs[:] = []
                continue
            dirs.sort()
            rel = os.path.relpath(root, base)
            folder = "" if rel == "." else rel.split(os.sep)[0]
            kind, cat = table.get(folder, (f"{top}.{folder or 'root'}", "other"))
            if folder == "" and top == "data":
                kind, cat = "data.client_lists", "intake"
            if "raw" in dirs:
                dirs.remove("raw")
                yield os.path.join(root, "raw"), kind + " raw", cat, True
            for fn in sorted(files):
                if fn.startswith((".", "~$")):
                    continue
                p = os.path.join(root, fn)
                k, c = kind, cat
                if is_sitemap(p):
                    k, c = "sitemap.urls", "crawl"
                elif top == "inputs" and re.search(r"seopress|wordpress|wp-settings", fn, re.I):
                    k, c = "wordpress.settings (S20)", "cms_settings"
                yield p, k, c, False


def file_date(path):
    m = re.search(r"(20\d\d-\d\d-\d\d)", os.path.basename(path))
    if m:
        return m.group(1)
    return datetime.date.fromtimestamp(os.stat(path).st_mtime).isoformat()


def count_records(path):
    """(rows, columns) for a non-crawl evidence file; '' where it has no rows."""
    ext = os.path.splitext(path)[1].lower()
    if is_sitemap(path):
        return len(sitemap_urls(path)), ""
    if ext in (".csv", ".tsv", ".xlsx", ".xlsm"):
        h, r = read_headers_and_rows(path)
        return len(r), len(h)
    if ext == ".json":
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (ValueError, OSError):
            return "", ""
        return (len(d) if isinstance(d, (list, dict)) else 1), ""
    if ext in (".jsonl", ".txt"):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for ln in fh if ln.strip()), ""
    return "", ""


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


def manifest_row(path, shown, kind, category, rows, columns, digest=None, size=None, date=None):
    stat = os.stat(path)
    return {
        "source_id": "",
        "file": shown,
        "recognised_as": kind or "UNRECOGNISED",
        "category": category or "",
        "rows": rows,
        "columns": columns,
        "sha256_12": sha(path) if digest is None else digest,
        "file_modified": datetime.datetime.fromtimestamp(
            stat.st_mtime).isoformat(timespec="seconds"),
        "tool_settings": "",     # analyst fills: UA, rendering, scope
        "date_window": "",       # analyst fills
        "geography_device": "",  # analyst fills
        "scope_limits": "",      # analyst fills
        "size_bytes": stat.st_size if size is None else size,
        "file_date": date or file_date(path),
    }


def add_urls(all_urls, headers, rows, kind):
    for key, raw, col, k in harvest_urls(headers, rows, kind):
        if not key:
            continue
        rec = all_urls.setdefault(key, {"url_key": key, "example_raw": raw,
                                        "seen_in": set(), "hosts": set()})
        rec["seen_in"].add(k)
        m = re.match(r"^https?://([^/]+)", raw)
        if m:
            rec["hosts"].add(m.group(1).lower())


def main():
    args = sys.argv[1:]
    no_extra = "--no-extra" in args
    client_dir = None
    if "--client-dir" in args:
        i = args.index("--client-dir")
        client_dir = args[i + 1]
        del args[i:i + 2]
    args = [a for a in args if a != "--no-extra"]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    evidence_dir, audit_dir = args[0], args[1]
    if not no_extra and not client_dir:
        client_dir = client_dir_for(evidence_dir)
    os.makedirs(os.path.join(audit_dir, "inventories"), exist_ok=True)

    manifest, unknown, all_urls = [], [], {}

    for root, dirs, files in os.walk(evidence_dir):
        dirs.sort()
        for fn in sorted(files):
            if fn.startswith("~$") or fn.startswith("."):
                continue
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            shown = os.path.relpath(path, evidence_dir)
            if is_sitemap(path):
                urls = sitemap_urls(path)
                row = manifest_row(path, shown, "sitemap.urls", "crawl", len(urls), "")
                row["_group"] = 0
                manifest.append(row)
                add_urls(all_urls, ["url"], [[u] for u in urls], "sitemap.urls")
                continue
            if "crawl-config" in fn.lower():
                row = manifest_row(path, shown, "dataforseo.crawl_config", "crawl", "", "")
                row["_group"] = 0
                manifest.append(row)
                continue
            if ext not in TABULAR:
                continue
            headers, rows = read_headers_and_rows(path)
            kind, category = fingerprint(headers)
            row = manifest_row(path, shown, kind, category, len(rows), len(headers))
            row["_group"] = 0
            manifest.append(row)
            if not kind:
                unknown.append((row["file"], [norm_header(h) for h in headers][:15]))
                continue
            add_urls(all_urls, headers, rows, kind)

    extra = 0
    if not no_extra:
        for path, kind, category, is_raw in extra_files(client_dir, evidence_dir):
            shown = os.path.relpath(path, client_dir)
            if is_raw:
                fs = [os.path.join(r, f) for r, _, fl in os.walk(path) for f in fl
                      if not f.startswith(".")]
                if not fs:
                    continue
                newest = max(fs, key=lambda f: os.stat(f).st_mtime)
                row = manifest_row(newest, f"{shown}/ ({len(fs)} files)", kind, category,
                                   len(fs), "", digest="",
                                   size=sum(os.stat(f).st_size for f in fs),
                                   date=file_date(newest))
            else:
                rows, columns = count_records(path)
                row = manifest_row(path, shown, kind, category, rows, columns)
                if kind == "sitemap.urls":
                    urls = sitemap_urls(path)
                    add_urls(all_urls, ["url"], [[u] for u in urls], "sitemap.urls")
                elif os.path.splitext(path)[1].lower() in (".csv", ".tsv", ".xlsx", ".xlsm"):
                    h, r = read_headers_and_rows(path)
                    fp, fc = fingerprint(h)
                    if fp:   # a standard export dropped into data/ — keep its real type
                        row["recognised_as"], row["category"] = fp, fc
                    add_urls(all_urls, h, r, row["recognised_as"])
            row["_group"] = 1
            manifest.append(row)
            extra += 1

    manifest.sort(key=lambda r: (r.pop("_group"), r["file"]))
    for i, row in enumerate(manifest, 1):
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
    if not no_extra:
        print(f"other evidence: {extra} file(s) from "
              f"{os.path.join(client_dir, 'data') if client_dir else '(no client folder found)'}"
              f" and inputs/")
    print(f"urls:       {inv_path}  ({len(all_urls)} unique)")
    if unknown:
        print(f"unrecognised: {len(unknown)} — see 00-unrecognised.md")
    print("\nManifest columns tool_settings / date_window / geography_device / "
          "scope_limits are blank by design — fill them before the Phase 0 readiness check.")


if __name__ == "__main__":
    main()
