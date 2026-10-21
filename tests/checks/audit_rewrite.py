"""Audit rewrite (#12, #13, R5): ingest takes the data/ outputs into the manifest, the three new
crawl cross-checks (host form, orphan candidates, sitemap), S15 as triage (CM-063, no scorecards) in
the audit procedure, and scripts/grid_pdf.py (Local Dominator PDFs read once into a summary).

Run alone: python3 tests/run_all.py -k audit_rewrite
"""
import csv
import os
import time

INGEST = "python3 .claude/skills/seo-technical-audit/scripts/ingest_evidence.py"
CROSS = "python3 .claude/skills/seo-technical-audit/scripts/crosscheck.py"

IA_HEAD = ("Address,Content Type,Status Code,Status,Indexability,Indexability Status,Title 1,"
           "Meta Description 1,H1-1,Canonical Link Element 1,Word Count,Crawl Depth,Inlinks,Redirect URL")


def ia_row(url, status="200", canonical=None, depth="1", redirect=""):
    idx = "Indexable" if status == "200" else "Non-Indexable"
    can = url if canonical is None else canonical
    return f"{url},text/html; charset=UTF-8,{status},OK,{idx},,T,M,H,{can},300,{depth},1,{redirect}"


def link(src, dst, kind="Hyperlink"):
    return f"{kind},{src},{dst},anchor,,True,200,,"


LINK_HEAD = "Type,Source,Destination,Anchor Text,Alt Text,Follow,Status Code,Link Path,Link Position"


def new_client(h, slug):
    code, out = h.sh(f'python3 scripts/status.py init {slug} --name "Audit Test {slug}" --domain test.example '
                     f'--type full --industry roofing')
    h.check(f"client {slug} created", code == 0, out)
    return h.Agent(slug)


def crawl_fixture(ag, base="https://test.example", messy=True):
    """Home, /a/ (linked), /b/ (no inlinks), /c/ (canonical on another host form when messy), /old/ (301)."""
    rows = [ia_row(f"{base}/", depth="0"), ia_row(f"{base}/a/"), ia_row(f"{base}/b/"),
            ia_row(f"{base}/c/", canonical=("http://www.test.example/c/" if messy else None)),
            ia_row(f"{base}/old/", status="301", redirect=f"{base}/a/")]
    ag.w("inputs/crawl/T - DFS - internal_all - 2026-10-07.csv", IA_HEAD + "\n" + "\n".join(rows) + "\n")
    links = [link(f"{base}/", f"{base}/a/"), link(f"{base}/a/", f"{base}/"),
             link(f"{base}/", ("http://www.test.example/c/" if messy else f"{base}/c/")),
             link(f"{base}/", f"{base}/b/", "Canonical"),     # not a hyperlink — must not count
             link(f"{base}/b/", f"{base}/b/"),                 # self-link — must not count
             link(f"{base}/", f"{base}/old/")]
    if not messy:
        links.append(link(f"{base}/a/", f"{base}/b/"))
    ag.w("inputs/crawl/T - DFS - all_inlinks - 2026-10-07.csv", LINK_HEAD + "\n" + "\n".join(links) + "\n")


def data_fixture(ag):
    ag.w("data/reviews/reviews.csv", "review_id,date,rating,text,owner_replied\nr1,2026-09-01,5,Great,yes\n"
                                     "r2,2026-09-02,4,Good,no\n")
    ag.w("data/reviews/customer-language.md", "# Customer language\n")
    ag.w("data/reviews/raw/reviews.json", "[]")
    ag.w("data/reviews/raw/task.json", "{}")
    ag.w("data/rankings/url-rankings.csv", "url,keywords_top100,best_position,total_volume\n"
                                           "https://test.example/a/,3,4,100\nhttp://www.test.example/,9,1,500\n")
    ag.w("data/backlinks/referring-domains-per-url.csv", "url,referring_domains,domains\nhttps://test.example/,2,a.com; b.com\n")
    ag.w("data/paa/paa-questions.csv", "question,source_queries,times_seen,closest_existing_heading_or_faq,similarity\n"
                                       "How long does a roof last?,roof repair,3,,0.00\n")
    ag.w("data/fanout/fanout-queries.csv", "query,seeds,times_seen\nsigns you need roof repair,roof repair,3\n")
    ag.w("data/local-grid/local-grid-summary.md", "# grid\n")
    ag.w("data/services.txt", "roof repair\nroof replacement\n")
    ag.w("inputs/seopress-settings-2026-10-05.json", '{"titles-settings": {}, "sitemaps-settings": {}}')
    ag.w("inputs/live-pages/T - MANUAL - sitemap-urls - 2026-10-07.txt",
         "https://test.example/sitemap_index.xml\nhttps://test.example/\nhttps://test.example/a/\n"
         "https://test.example/old/\nhttps://test.example/ghost/\n")


def read_manifest(h, slug, audit):
    with open(h.SB / "clients" / slug / audit / "00-manifest.csv", newline="") as fh:
        return list(csv.DictReader(fh))


# ------------------------------------------------------------------ #12 ingest
def t_ingest_data(h):
    slug = "audit-ingest"
    ag = new_client(h, slug)
    crawl_fixture(ag)
    data_fixture(ag)
    code, out = h.sh(f"{INGEST} clients/{slug}/inputs/crawl clients/{slug}/audit/t1")
    h.check("ingest runs with the data folder", code == 0, out)
    rows = read_manifest(h, slug, "audit/t1")
    by = {r["file"]: r for r in rows}
    h.check("manifest keeps the crawl exports first and recognised",
            rows[0]["recognised_as"] == "screamingfrog.all_inlinks" and
            by.get("T - DFS - internal_all - 2026-10-07.csv", {}).get("recognised_as") == "screamingfrog.internal_all",
            [r["file"] for r in rows[:3]])
    want = {"data/reviews/reviews.csv": ("data.reviews (S06)", "2"),
            "data/rankings/url-rankings.csv": ("data.rankings (S07)", "2"),
            "data/backlinks/referring-domains-per-url.csv": ("data.backlinks (S08)", "1"),
            "data/paa/paa-questions.csv": ("data.paa (S19)", "1"),
            "data/fanout/fanout-queries.csv": ("data.fanout (S21)", "1"),
            "data/local-grid/local-grid-summary.md": ("data.local_grid (S10)", ""),
            "data/services.txt": ("data.client_lists", "2"),
            "inputs/seopress-settings-2026-10-05.json": ("wordpress.settings (S20)", "2"),
            "inputs/live-pages/T - MANUAL - sitemap-urls - 2026-10-07.txt": ("sitemap.urls", "4")}
    bad = {f: (by.get(f, {}).get("recognised_as"), by.get(f, {}).get("rows")) for f, v in want.items()
           if (by.get(f, {}).get("recognised_as"), by.get(f, {}).get("rows")) != v}
    h.check("one manifest row per data / inputs file, with source and row count", not bad, bad)
    raw = [r for r in rows if r["file"].startswith("data/reviews/raw/")]
    h.check("a raw/ folder is one row (file count)", len(raw) == 1 and raw[0]["file"].endswith("(2 files)")
            and raw[0]["rows"] == "2", raw)
    h.check("every row has a size and a date; source ids run SRC-001…",
            all(r["size_bytes"] and r["file_date"] for r in rows)
            and [r["source_id"] for r in rows] == [f"SRC-{i:03d}" for i in range(1, len(rows) + 1)]
            and by["inputs/seopress-settings-2026-10-05.json"]["file_date"] == "2026-10-05")
    h.check("nothing from data/ lands in 00-unrecognised.md",
            not (h.SB / "clients" / slug / "audit/t1/00-unrecognised.md").exists())
    urls = (h.SB / "clients" / slug / "audit/t1/inventories/urls.csv").read_text()
    h.check("sitemap-only and rankings URLs join the URL inventory",
            "test.example/ghost" in urls and "data.rankings (S07)" in urls and "sitemap_index" not in urls, urls[:600])
    code, out = h.sh(f"{INGEST} clients/{slug}/inputs/crawl clients/{slug}/audit/t2 --no-extra")
    rows2 = read_manifest(h, slug, "audit/t2")
    h.check("--no-extra reads the crawl folder only", code == 0 and len(rows2) == 2, [r["file"] for r in rows2])


# ------------------------------------------------------------------ #12 cross-checks
def section(md, title):
    i = md.find(f"] {title}")
    return md[i:md.find("\n## ", i + 1) if md.find("\n## ", i + 1) > 0 else len(md)] if i >= 0 else ""


def t_crosschecks(h):
    slug = "audit-cross"
    ag = new_client(h, slug)
    crawl_fixture(ag, messy=True)
    data_fixture(ag)
    code, out = h.sh(f"{CROSS} clients/{slug}/inputs/crawl clients/{slug}/audit/t1")
    md = (h.SB / "clients" / slug / "audit/t1/00-crosschecks.md").read_text() if code == 0 else ""
    h.check("crosscheck runs and finds the sitemap in inputs/", code == 0 and "sitemap.urls" in md, out)
    host = section(md, "Host consistency (crawl, canonicals, links)")
    h.check("host form: a canonical and a link on http://www. are flagged UNVERIFIED",
            "[UNVERIFIED] Host" in md and "http://www.test.example" in host and "canonicals: 1" in host
            and "internal link targets: 1" in host, host)
    orph = section(md, "Orphan candidates (zero internal inlinks)")
    h.check("orphans: /b/ (canonical row and self-link don't count) and sitemap-only /ghost/ are candidates; "
            "/a/, /c/ (linked under another host form), the homepage and the 301 are not",
            "test.example/b/ (crawl)" in orph and "ghost/ (sitemap only)" in orph and "/a/" not in orph
            and "/c/" not in orph and "/old/" not in orph and "[UNVERIFIED] Orphan" in md, orph)
    sm = section(md, "Sitemap")
    h.check("sitemap: /ghost/ not crawled, /old/ non-200, /b/ and /c/ missing from the sitemap",
            "did not find" in sm and "ghost/" in sm and "old/ → 301" in sm and "missing from the sitemap" in sm
            and "test.example/b/" in sm and "sitemap_index" not in sm, sm)

    clean = "audit-clean"
    ag2 = new_client(h, clean)
    crawl_fixture(ag2, messy=False)
    ag2.w("inputs/T - MANUAL - sitemap - 2026-10-07.xml",
          "<?xml version='1.0'?><urlset>" + "".join(f"<url><loc>https://test.example/{p}</loc></url>"
                                                    for p in ("", "a/", "b/", "c/")) + "</urlset>")
    code, out = h.sh(f"{CROSS} clients/{clean}/inputs/crawl clients/{clean}/audit/t1")
    md2 = (h.SB / "clients" / clean / "audit/t1/00-crosschecks.md").read_text() if code == 0 else ""
    h.check("clean site: the three new checks are CONFIRMED (XML sitemap read)",
            all(f"[CONFIRMED] {t}" in md2 for t in ("Host consistency (crawl, canonicals, links)",
                                                    "Orphan candidates (zero internal inlinks)", "Sitemap")), md2)

    bare = "audit-nositemap"
    ag3 = new_client(h, bare)
    crawl_fixture(ag3, messy=False)
    code, out = h.sh(f"{CROSS} clients/{bare}/inputs/crawl clients/{bare}/audit/t1")
    md3 = (h.SB / "clients" / bare / "audit/t1/00-crosschecks.md").read_text() if code == 0 else ""
    h.check("no sitemap list → Sitemap is a LIMITATION, never a pass", "[LIMITATION] Sitemap" in md3, md3[-800:])
    code, out = h.sh(f"{CROSS} clients/{bare}/inputs/crawl clients/{bare}/audit/t2 "
                     f"--sitemap clients/{clean}/inputs/'T - MANUAL - sitemap - 2026-10-07.xml'")
    md4 = (h.SB / "clients" / bare / "audit/t2/00-crosschecks.md").read_text() if code == 0 else ""
    h.check("--sitemap FILE is used when the client has none", "[CONFIRMED] Sitemap" in md4, out + md4[-500:])


# ------------------------------------------------------------------ #13 scorecards → CM-063 triage
def t_scorecards_per_type(h):
    sk = h.SB / ".claude/skills/seo-technical-audit"
    texts = {"SKILL.md": (sk / "SKILL.md").read_text(),
             "analysis-rules.md": (sk / "references/analysis-rules.md").read_text(),
             "review-selfcheck.md": (sk / "references/review-selfcheck.md").read_text(),
             "audit-reviewer.md": (h.SB / ".claude/agents/audit-reviewer.md").read_text(),
             "discovery-audit.md": (h.SB / ".claude/agents/discovery-audit.md").read_text()}
    h.check("CM-063: S15 is triage — no audit doc asks for a scorecard file (per type or combined)",
            not any(x in v for v in texts.values() for x in ("scorecard-<type>.csv", "scorecard-homepage.csv",
                                                                "conformance-scorecard.csv", "scorecard.csv`")),
            {k: "scorecard-" in v for k, v in texts.items()})
    h.check("CM-063: the procedure names the triage and the screen, the reviewer its scope script",
            "conformance.py triage" in texts["SKILL.md"] and "pagedec.py screen" in texts["SKILL.md"]
            and "review.py scope" in texts["audit-reviewer.md"] and "review.py scope" in texts["review-selfcheck.md"]
            and not (sk / "references/gate-b-questions.md").exists())


# ------------------------------------------------------------------ R5 grid_pdf.py
def make_pdf(path, lines):
    """A one-page PDF with real text (Helvetica), one line per entry."""
    esc = lambda s: s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    body = "BT /F1 11 Tf 14 TL 50 780 Td " + " ".join(f"({esc(ln)}) Tj T*" for ln in lines) + " ET"
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 4 0 R >> >> "
            "/Contents 5 0 R >>",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            f"<< /Length {len(body)} >>\nstream\n{body}\nendstream"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n".encode("latin-1")
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{o:010d} 00000 n \n" for o in offs).encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n".encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out)


GRID_LINES = ["Test Roofing Co", "Beaufort, United States of America", "Scan date: Oct 7, 2026 4:20 PM",
              "Scan Analysis Report local pack", "Primary keyword", "Avg. Rank", "roof repair bluffton", "6.99",
              "Local Visibility Summary", "In the next 30 days prioritise review drives.",
              "9 Pins | 3 with 1 mi spacing", "1 2 3", "4 5 20+", "7 8 9", "Top Competitors",
              "Business Name Avg. Rank", "Rival Roofing", "4.9 (76)", "1 Strong presence in top spots.",
              "Competition Overview", "Adopt top strategies: frequent photo updates."]


def t_grid_pdf(h):
    slug = "audit-grid"
    new_client(h, slug)
    c = h.SB / "clients" / slug
    pdf = c / "inputs/local-grid/T - MANUAL - local-grid-roof-repair-bluffton-local-pack - 2026-10-07.pdf"
    make_pdf(pdf, GRID_LINES)
    summ = c / "data/local-grid/local-grid-summary.md"
    code, out = h.sh(f"SEO_OPS_GRID_PDF_BACKEND=none python3 scripts/grid_pdf.py {slug}")
    h.check("no extraction backend → exit 2 with a plain message, nothing written",
            code == 2 and "no macOS PDFKit backend" in out and not summ.exists(), out)
    code, out = h.sh(f"python3 scripts/grid_pdf.py {slug}")
    if code == 2:   # not a Mac (or osascript unavailable): the clear-message path is all we can check
        h.check("grid_pdf: no PDFKit here — clear message instead of a summary", "PDFKit" in out, out)
        return
    s = summ.read_text() if summ.exists() else ""
    h.check("grid_pdf finds the PDF in inputs/local-grid and writes data/local-grid/local-grid-summary.md",
            code == 0 and summ.exists(), out)
    h.check("summary: keyword, view, average rank, grid size, scan date",
            "roof repair bluffton" in s and "Local pack" in s and "**6.99**" in s
            and "9 pins, 3 × 3, 1 mi spacing" in s and "Oct 7, 2026 4:20 PM" in s, s)
    h.check("summary: the rank grid as a small table and the competitor row",
            "| 4 | 5 | 20+ |" in s and "| Rival Roofing | 4.9 (76) | 1 |" in s, s)
    h.check("summary: the report's written advice is not copied",
            "prioritise review drives" not in s and "photo updates" not in s and "Strong presence" not in s, s)
    code, out = h.sh(f"python3 scripts/grid_pdf.py {slug}")
    h.check("re-run with nothing newer → up to date, nothing extracted", code == 0 and "up to date" in out, out)
    t = time.time()
    os.utime(summ, (t - 100, t - 100))
    os.utime(pdf, (t, t))
    code, out = h.sh(f"python3 scripts/grid_pdf.py {slug}")
    h.check("a newer PDF → the generated summary is rewritten", code == 0 and "wrote" in out, out)
    summ.write_text("# hand-written grid notes\n")
    os.utime(summ, (t - 100, t - 100))
    code, out = h.sh(f"python3 scripts/grid_pdf.py {slug}")
    h.check("a hand-written summary is never overwritten without --force",
            code == 1 and "by hand" in out and summ.read_text() == "# hand-written grid notes\n", out)
    code, out = h.sh(f"python3 scripts/grid_pdf.py {slug} --force")
    h.check("--force rewrites it", code == 0 and "roof repair bluffton" in summ.read_text(), out)


SCENARIOS = [t_ingest_data, t_crosschecks, t_scorecards_per_type, t_grid_pdf]
