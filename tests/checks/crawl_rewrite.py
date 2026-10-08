"""crawl.py rewrite: #18 max pages from the sitemap, #11 S05b page text capture, R5 crawl summary.

The fake web in tests/fakes.py serves no robots.txt or sitemap, so the fallback path runs through
tests/fakes.py as-is; the sitemap path runs through a small wrapper (written into tests/.state/)
that installs the same fakes and then serves the sitemaps and pages this module defines.
"""
import csv
import json

SLUG = "cr-co"
BASE = "https://test.example"

WRAPPER = '''import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fakes
fakes.install()
import verify, crawl
WEB = json.loads((Path(__file__).parent / "crawl_web.json").read_text())
_orig = verify.fetch
def fetch(url, follow=True):
    if url in WEB:
        return 200, {}, WEB[url]
    return _orig(url, follow)
verify.fetch = fetch
crawl.WEB_PACE = 0
sys.argv = ["scripts/crawl.py", *sys.argv[1:]]
crawl.main()
'''


def _setup(h):
    st = h.SB / "tests" / ".state"
    st.mkdir(parents=True, exist_ok=True)
    (st / "crawl_web.py").write_text(WRAPPER)
    if not (h.SB / "clients" / SLUG / "status.json").exists():
        h.sh(f'python3 scripts/status.py init {SLUG} --name "Cr Co" --domain test.example --type full --industry roofing')
        ag = h.Agent(SLUG)
        ag.fin(ag.start("new-client"), "set up")
    return h.Agent(SLUG)


def _web(h, pages):
    (h.SB / "tests" / ".state" / "crawl_web.json").write_text(json.dumps(pages))


def _urlset(urls):
    return ('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>")


def t_max_pages_fallback(h):
    _setup(h)
    _web(h, {})
    code, out = h.sh(f"python3 tests/fakes.py crawl estimate {SLUG} --domain test.example")
    h.check("#18: no sitemap -> max pages falls back to 1000 and the estimate says why",
            code == 0 and "Max pages: 1000" in out and "no readable sitemap" in out and "fell back" in out
            and "--max-pages 1000" in out, out)
    code, out = h.sh(f"python3 tests/fakes.py crawl estimate {SLUG} --domain test.example --max-pages 300")
    h.check("#18: an explicit --max-pages wins and the estimate says so",
            code == 0 and "Max pages: 300 — set with --max-pages" in out, out)


def t_max_pages_sitemap(h):
    _setup(h)
    pages = [f"{BASE}/p{i}/" for i in range(30)]
    posts = [f"https://www.test.example/post-{i}/" for i in range(18)] + ["https://other.example/x/"]
    _web(h, {f"{BASE}/robots.txt": f"User-agent: *\nDisallow:\nSitemap: {BASE}/sitemap_index.xml\n",
             f"{BASE}/sitemap_index.xml": '<?xml version="1.0"?><sitemapindex>'
             f"<sitemap><loc>{BASE}/page-sitemap.xml</loc></sitemap>"
             f"<sitemap><loc>{BASE}/post-sitemap.xml</loc></sitemap></sitemapindex>",
             f"{BASE}/page-sitemap.xml": _urlset(pages),
             f"{BASE}/post-sitemap.xml": _urlset(posts + pages[:3])})
    code, out = h.sh(f"python3 tests/.state/crawl_web.py estimate {SLUG} --domain test.example")
    h.check("#18: robots.txt Sitemap: -> index followed, 48 same-site URLs (duplicates and other hosts "
            "dropped) x 1.5 = max 72 pages",
            code == 0 and "Max pages: 72" in out and "sitemap lists 48 URLs" in out and "--max-pages 72" in out, out)

    _web(h, {f"{BASE}/sitemap.xml": _urlset(pages[:5])})
    code, out = h.sh(f"python3 tests/.state/crawl_web.py estimate {SLUG} --domain test.example")
    h.check("#18: /sitemap.xml without robots.txt; a tiny site gets the minimum of 20",
            code == 0 and "Max pages: 20" in out and "sitemap lists 5 URLs" in out, out)

    _web(h, {f"{BASE}/sitemap_index.xml": _urlset([f"{BASE}/q{i}/" for i in range(900)])})
    code, out = h.sh(f"python3 tests/.state/crawl_web.py estimate {SLUG} --domain test.example")
    h.check("#18: /sitemap_index.xml as the last fallback; a big site is capped at 1000",
            code == 0 and "Max pages: 1000" in out and "sitemap lists 900 URLs" in out, out)

    # the paid run uses the same default and records why
    _web(h, {f"{BASE}/sitemap.xml": _urlset(pages + [p.replace("www.", "") for p in posts[:18]])})
    ag = h.Agent(SLUG)
    rid = ag.start("crawl")
    code, out = h.sh(f"python3 tests/.state/crawl_web.py run {SLUG} --run {rid} --domain test.example "
                     f"--confirmed --max-wait 0 --crawl-delay 1000")
    st = json.loads((h.SB / "clients" / SLUG / "inputs" / "crawl" / "crawl-state.json").read_text())
    h.check("#18: crawl run without --max-pages posts sitemap x 1.5 (72), not 1000, and stores the reason",
            code == 10 and st.get("max_pages") == 72 and "sitemap lists 48 URLs" in st.get("max_pages_reason", ""),
            (code, out, {k: st.get(k) for k in ("max_pages", "max_pages_reason")}))
    log = (h.SB / "clients" / SLUG / "log.md").read_text()
    h.check("#18: the log note for the posted task says why that max pages was used",
            "max 72 pages — sitemap lists 48 URLs" in log, log[-500:])
    ag.step(rid, "S05", "skipped", "fake crawl still running")
    ag.fin(rid, "crawl posted (fake)")


RAW = [
    {"url": f"{BASE}/", "resource_type": "html", "status_code": 200, "click_depth": 0,
     "meta": {"title": "Home | Cr Co", "description": "Roofing in Springfield.", "canonical": f"{BASE}/",
              "htags": {"h1": ["Cr Co Roofing"], "h2": ["Services"]}, "content": {"plain_text_word_count": 420},
              "inbound_links_count": 5, "internal_links_count": 9, "external_links_count": 1}},
    {"url": f"{BASE}/roof-repair/", "resource_type": "html", "status_code": 200, "click_depth": 1,
     "meta": {"title": "Roof Repair", "description": "", "htags": {"h1": ["Roof Repair", "Call us"]},
              "content": {"plain_text_word_count": 1200}, "inbound_links_count": 3}},
    {"url": f"{BASE}/private/", "resource_type": "html", "status_code": 200, "click_depth": 2,
     "meta": {"title": "Private", "htags": {"h1": ["Private"]}}},
    {"url": f"{BASE}/old/", "resource_type": "redirect", "status_code": 301, "location": f"{BASE}/roof-repair/",
     "click_depth": 1, "meta": {}},
]

HOME = ("<html><head><title>Home</title><script>var junk='do not keep';</script><style>.x{}</style></head><body>"
        "<header><nav><a href='/'>Menu item</a></nav></header><main><h1>Cr Co Roofing</h1>"
        "<p>We fix roofs &amp; gutters in Springfield.</p></main><footer>Footer words</footer></body></html>")
LONG = "<html><body><h1>Roof <em>Repair</em></h1><article>" + " ".join(f"w{i}" for i in range(1000)) + "</article></body></html>"


def t_summary_and_text(h):
    ag = _setup(h)
    cd = h.SB / "clients" / SLUG / "inputs" / "crawl"
    (cd / "raw").mkdir(parents=True, exist_ok=True)
    sp = cd / "crawl-state.json"
    st = json.loads(sp.read_text()) if sp.exists() else {
        "task_id": "fake-task", "domain": "test.example", "max_pages": 72, "mode": "basic",
        "crawl_delay_ms": 2000, "checkpoints": {}}
    import datetime
    st.update(phase="converting", posted_at=datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
              summary={"pages_crawled": 4, "stop_reason": "empty_queue"})
    sp.write_text(json.dumps(st))
    (cd / "raw" / "pages.jsonl").write_text("".join(json.dumps(p) + "\n" for p in RAW))
    _web(h, {})
    rid = ag.start("crawl")
    code, out = h.sh(f"python3 tests/.state/crawl_web.py run {SLUG} --run {rid} --domain test.example --confirmed")
    summ = h.SB / "clients" / SLUG / "data" / "crawl" / "crawl-summary.csv"
    ok = code == 0 and summ.exists()
    rows = list(csv.DictReader(summ.open())) if summ.exists() else []
    by = {r["url"]: r for r in rows}
    h.check("R5: a finished crawl writes data/crawl/crawl-summary.csv, one row per page",
            ok and len(rows) == 4 and "crawl-summary.csv" in out, (code, out[-400:], len(rows)))
    hdr = list(rows[0].keys()) if rows else []
    h.check("R5: the summary has only the audited columns (CSV, no JSON)",
            hdr[:4] == ["url", "status", "indexability", "indexability_status"]
            and {"title", "title_len", "meta_description", "meta_len", "h1", "h1_count", "word_count",
                 "canonical", "inlinks", "outlinks", "depth"} <= set(hdr) and len(hdr) <= 20
            and summ.exists() and "{" not in summ.read_text(), hdr)
    r = by.get(f"{BASE}/roof-repair/", {})
    h.check("R5: summary values come from the crawl (H1 count 2, word count, length, indexability)",
            r.get("h1_count") == "2" and r.get("word_count") == "1200" and r.get("title_len") == "11"
            and by.get(f"{BASE}/old/", {}).get("indexability_status") == "Redirected", rows)
    before = summ.read_text() if summ.exists() else None
    summ.unlink(missing_ok=True)
    code, out = h.sh(f"python3 scripts/crawl.py summary {SLUG}")
    h.check("R5: crawl.py summary rebuilds the same file from the existing crawl tables",
            code == 0 and summ.exists() and summ.read_text() == before, out)
    ag.step(rid, "S05"); ag.fin(rid, "crawl converted (fake)")
    h.check("the crawl runs finished cleanly", not ag.errors, ag.errors)

    # S05b: page text
    _web(h, {f"{BASE}/robots.txt": "User-agent: *\nDisallow: /private/\n",
             f"{BASE}/": HOME, f"{BASE}/roof-repair/": LONG})
    rid = ag.start("crawl")
    code, out = h.sh(f"python3 tests/.state/crawl_web.py text {SLUG} --run {rid} --delay 1")
    pt = h.SB / "clients" / SLUG / "data" / "crawl" / "page-text.csv"
    rows = list(csv.DictReader(pt.open())) if pt.exists() else []
    by = {r["url"]: r for r in rows}
    h.check("S05b: one page-text.csv row per crawled HTML 200 page (redirects not fetched)",
            code == 0 and len(rows) == 3 and f"{BASE}/old/" not in by, (code, out, rows))
    home = by.get(f"{BASE}/", {})
    h.check("S05b: body text only — no script, style, navigation or footer; entities decoded",
            home.get("h1") == "Cr Co Roofing" and "We fix roofs & gutters in Springfield." in home.get("text", "")
            and not any(x in home.get("text", "") for x in ("junk", "Menu item", "Footer words", ".x{")), home)
    rr = by.get(f"{BASE}/roof-repair/", {})
    h.check("S05b: long pages are cut to --max-words with the full word count kept",
            rr.get("word_count") == "1000" and rr.get("truncated") == "yes" and rr.get("h1") == "Roof Repair"
            and len(rr.get("text", "").split()) == 801, {k: v for k, v in rr.items() if k != "text"})
    h.check("S05b: robots.txt is respected (disallowed page listed, not fetched)",
            "disallowed by robots.txt" in by.get(f"{BASE}/private/", {}).get("text", ""), by.get(f"{BASE}/private/"))
    log = (h.SB / "clients" / SLUG / "log.md").read_text()
    h.check("S05b: the capture is noted in the safety log as free", "S05b page text: 2 of 3 pages captured" in log
            and "no charge" in log, log[-400:])
    code, out = h.sh(f"python3 tests/.state/crawl_web.py text {SLUG} --run {rid} --delay 0.2")
    h.check("S05b: a fetch delay under 1 second is refused", code != 0 and "not polite" in out, out)
    ag.step(rid, "S05", "done")   # S05b once steps.py registers it (see the module docstring)
    ag.fin(rid, "page text captured (fake)")
    reg = (h.SB / "methodology" / "audit-steps.md").read_text()
    h.check("S05b: registered in methodology/audit-steps.md", "| S05b |" in reg and "page-text.csv" in reg)


SCENARIOS = [t_max_pages_fallback, t_max_pages_sitemap, t_summary_and_text]
