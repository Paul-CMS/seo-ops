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


def _client(h, slug):
    h.sh(f'python3 scripts/status.py init {slug} --name "{slug}" --domain test.example --type full --industry roofing')
    ag = h.Agent(slug)
    ag.fin(ag.start("new-client"), "set up")
    return ag


def _posts(h, slug):
    p = h.SB / "clients" / slug / "dfs-costs.jsonl"
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
    return [r for r in rows if r.get("endpoint") == "on_page/task_post"]


def t_domain_check(h):
    S = "cd-co"
    ag = _client(h, S)
    code, out = h.sh(f"python3 tests/fakes.py crawl estimate {S} --domain other.example")
    h.check("CR-048: crawl estimate refuses (exit 4) a domain that is not the client's, naming both",
            code == 4 and "other.example is not this client's domain (test.example" in out, (code, out))
    code, out = h.sh(f"python3 tests/fakes.py crawl estimate {S} --domain https://www.test.example/")
    h.check("CR-048: the client's domain with www. and a scheme is accepted", code == 0 and "Estimate:" in out, out)
    code, out = h.sh(f"python3 tests/fakes.py crawl estimate {S} --domain other.example --other-domain")
    h.check("CR-048: --other-domain lets a deliberate second domain through", code == 0 and "Estimate:" in out, out)
    rid = ag.start("crawl")
    code, out = h.sh(f"python3 tests/fakes.py crawl run {S} --run {rid} --domain other.example --confirmed "
                     f"--max-pages 20 --max-wait 0")
    h.check("CR-048: crawl run on another domain is refused before any paid call",
            code == 4 and "not this client's domain" in out and not _posts(h, S), (code, out, _posts(h, S)))
    ag.step(rid, "S05", "skipped", "domain check test")
    ag.fin(rid, "domain check (fake)")


def t_queue_guard_cancel(h):
    S = "cq-co"
    ag = _client(h, S)
    st_dir = h.SB / "tests" / ".state"
    dj = st_dir / "dfs.json"
    dj.write_text(json.dumps({"balance": 10.0, "cost": 0.0198, "onpage_queued": True}))
    cd = h.SB / "clients" / S / "inputs" / "crawl"
    run = f"python3 tests/fakes.py crawl run {S} --domain test.example --confirmed --max-pages 20 --max-wait 0"
    try:
        rid = ag.start("crawl")
        code, out = h.sh(f"{run} --run {rid}")
        log = (ag.c / "log.md").read_text()
        h.check("CR-049: a task DataforSEO has not started (40602) is waited for — exit 10 QUEUED, not exit 8",
                code == 10 and "QUEUED" in out and "DataforSEO error" not in out and len(_posts(h, S)) == 1
                and "queued at DataforSEO (40602 Task In Queue.)" in log, (code, out, log[-300:]))
        code, out = h.sh(f"{run} --run {rid}")
        h.check("CR-049: running it again resumes the same task for free", code == 10 and len(_posts(h, S)) == 1, (code, out))
        code, out = h.sh(f"{run} --run {rid} --new-crawl")
        h.check("CR-049: --new-crawl on an unfinished task of the same site is refused (exit 4) and posts nothing",
                code == 4 and "is not finished" in out and "crawl.py cancel" in out and len(_posts(h, S)) == 1
                and not list(cd.glob("crawl-state-*.json")), (code, out, len(_posts(h, S))))

        code, out = h.sh(f"python3 tests/fakes.py crawl cancel {S} --run {rid}")
        st = json.loads((cd / "crawl-state.json").read_text())
        stops = (st_dir / "force_stop.txt").read_text().split() if (st_dir / "force_stop.txt").exists() else []
        h.check("CR-049: crawl.py cancel stops the task with the free on_page/force_stop and marks the state cancelled",
                code == 0 and "stopped  fake-task" in out and stops == ["fake-task"] and st.get("phase") == "cancelled"
                and "20000 Ok." in st.get("cancel_answer", "") and "no charge" in (ag.c / "log.md").read_text()
                and len(_posts(h, S)) == 1, (code, out, stops, st.get("phase")))
        code, out = h.sh(f"{run} --run {rid}")
        h.check("CR-049: a cancelled task is never resumed; a new crawl needs --new-crawl",
                code != 0 and "cancelled" in out and len(_posts(h, S)) == 1, (code, out))
        code, out = h.sh(f"{run} --run {rid} --new-crawl")
        h.check("CR-049: a run that already paid for a crawl task cannot post a second one (exit 4)",
                code == 4 and "already paid for 1 crawl task" in out and len(_posts(h, S)) == 1, (code, out))

        for tid, phase in (("old-1", "crawling"), ("old-2", "converted"), ("old-3", "crawling")):
            (cd / f"crawl-state-2026-10-28-{tid}.json").write_text(json.dumps(
                {"task_id": tid, "domain": "test.example", "phase": phase, "posted_at": "2026-10-28T19:00:00-05:00"}))
        dj.write_text(json.dumps({"balance": 10.0, "cost": 0.0198, "onpage_queued": True, "onpage_stop_fail": ["old-3"]}))
        (st_dir / "force_stop.txt").unlink(missing_ok=True)
        code, out = h.sh(f"python3 tests/fakes.py crawl cancel {S} --run {rid} --include-archived")
        ph = {t: json.loads((cd / f"crawl-state-2026-10-28-{t}.json").read_text())["phase"] for t in ("old-1", "old-2", "old-3")}
        stops = (st_dir / "force_stop.txt").read_text().split()
        h.check("CR-049: --include-archived stops the unfinished set-aside tasks only, and reports DataforSEO's answer "
                "for each (a refusal exits 8 and stays unfinished)",
                code == 8 and stops == ["old-1", "old-3"] and ph == {"old-1": "cancelled", "old-2": "converted",
                                                                       "old-3": "crawling"}
                and "NOT stopped  old-3" in out and "40400 Not Found." in out and "1 of 2 stopped" in out,
                (code, out, stops, ph))
        ag.step(rid, "S05", "skipped", "queued test")
        ag.fin(rid, "queued crawl cancelled (fake)")

        rid = ag.start("crawl")
        code, out = h.sh(f"{run} --run {rid} --new-crawl")
        h.check("CR-049: after a cancel, a new run may post a new crawl with --new-crawl",
                code == 10 and len(_posts(h, S)) == 2, (code, out))
        ag.step(rid, "S05", "skipped", "queued test")
        ag.fin(rid, "new crawl posted (fake)")
    finally:
        dj.unlink(missing_ok=True)
        (st_dir / "force_stop.txt").unlink(missing_ok=True)


SCENARIOS = [t_max_pages_fallback, t_max_pages_sitemap, t_summary_and_text, t_domain_check, t_queue_guard_cancel]
