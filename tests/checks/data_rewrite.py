"""Data-step rewrite checks: review sign-offs (#14), fan-out spread + group column (#16), PAA routing kept on
re-run (#17), failed-task spend reported apart (#19), compact summaries for agents (R5: reviews, backlinks).

A small wrapper (tests/dr_wrap.py, written into the sandbox) runs a script with the usual fakes plus the
DataforSEO answers these checks need: a reviews task, People Also Ask boxes, and failed (but billed) tasks.
"""
import csv
import json

WRAP = r'''
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fakes
fakes.install()
import dfs
_fake = dfs.request
MODE = HERE / ".state" / "dr_mode.json"


def req(endpoint, body=None, method=None, timeout=90, retries=3):
    m = json.loads(MODE.read_text()) if MODE.exists() else {}
    for pre in m.get("fail", []):
        if endpoint.startswith(pre):
            n = len(body or [1])
            tasks = [{"status_code": 40501, "status_message": "Invalid Field: location_name", "cost": 0.002}]
            tasks += [{"status_code": 20000, "id": f"ok-{i}", "cost": 0.003, "result": [{"items": []}]}
                      for i in range(n - 1)]
            return {"status_code": 20000, "cost": round(sum(t["cost"] for t in tasks), 4), "tasks": tasks}
    if endpoint == "business_data/google/reviews/task_post":
        return {"status_code": 20000, "cost": 0.015, "tasks": [{"status_code": 20100, "id": "rv-task", "cost": 0.015}]}
    if endpoint.startswith("business_data/google/reviews/task_get/"):
        res = json.loads((HERE / ".state" / "dr_reviews.json").read_text())
        return {"status_code": 20000, "cost": 0, "tasks": [{"status_code": 20000, "result": [res]}]}
    if endpoint.startswith("serp/") and m.get("paa"):
        _fake(endpoint, body, method, timeout, retries)   # keeps the fake's location log
        qs = m["paa"]
        return {"status_code": 20000, "cost": 0.002, "tasks": [{"status_code": 20000, "result": [{"items": [
            {"type": "people_also_ask", "items": [{"title": q} for q in qs]}]}]}]}
    return _fake(endpoint, body, method, timeout, retries)


dfs.request = req
name, args = sys.argv[1], sys.argv[2:]
mod = __import__(name)
sys.argv = [f"scripts/{name}.py", *args]
mod.main()
'''


def _setup(h, slug, mode=None, balance=10.0, cost=0.003):
    h.sh(f'python3 scripts/status.py init {slug} --name "{slug.title()}" --domain test.example --type full '
         f'--industry roofing')
    ag = h.Agent(slug)
    ag.fin(ag.start("new-client"), "set up")
    st = h.SB / "tests" / ".state"
    st.mkdir(parents=True, exist_ok=True)
    (h.SB / "tests" / "dr_wrap.py").write_text(WRAP)
    (st / "dfs.json").write_text(json.dumps({"balance": balance, "cost": cost}))
    (st / "dr_mode.json").write_text(json.dumps(mode or {}))
    return ag


def _done(h):
    for f in ("dfs.json", "dr_mode.json", "dr_reviews.json"):
        (h.SB / "tests" / ".state" / f).unlink(missing_ok=True)


REVIEWS = {"rating": {"value": 4.7}, "reviews_count": 6, "items": [
    {"type": "google_review", "review_id": "r1", "timestamp": "2026-09-01 10:00:00", "rating": {"value": 5},
     "profile_name": "John Doe", "review_text": "Great job on our roof repair, fast and fair price!\n- John D.",
     "owner_answer": "Thank you!"},
    {"type": "google_review", "review_id": "r2", "timestamp": "2026-08-20 10:00:00", "rating": {"value": 5},
     "profile_name": "Mary Smith", "review_text": "They fixed the leak in Springfield the same day. Thanks, Mary"},
    {"type": "google_review", "review_id": "r3", "timestamp": "2026-08-01 10:00:00", "rating": {"value": 4},
     "profile_name": "Sarah Miller", "review_text": "Very professional crew and they cleaned up.\nSarah Miller"},
    {"type": "google_review", "review_id": "r4", "timestamp": "2026-07-01 10:00:00", "rating": {"value": 5},
     "profile_name": "Pete Ross", "review_text": "Honest quote for gutter cleaning. We loved working with Tom"},
    {"type": "google_reviews_search", "review_id": "r5", "timestamp": "2026-06-01 10:00:00", "rating": {"value": 2},
     "profile_name": "Ann Lee", "review_text": "Late twice and disappointed. Would they come back?"},
    {"type": "google_review", "review_id": "r6", "timestamp": "2026-05-01 10:00:00", "rating": {"value": 5},
     "profile_name": "Bob Kane", "review_text": "Fantastic crew.\nHighly Recommended"},
]}


def t_reviews(h):
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    cases = {"Great job!\n- John D.": "Great job!", "Fixed it fast. Thanks, Mary": "Fixed it fast.",
             "Fantastic crew.\nSarah Miller": "Fantastic crew.", "Nice work - John": "Nice work",
             "Fantastic crew.\nHighly Recommended": "Fantastic crew.\nHighly Recommended",
             "Best roofer in Springfield.": "Best roofer in Springfield."}
    code, out = h.sh("python3 -c \"import sys, json; sys.path.insert(0, 'scripts'); import reviews; "
                     f"print(json.dumps([reviews.strip_signoff(t, ['Springfield'])[0] for t in {list(cases)!r}]))\"")
    got = json.loads(out.splitlines()[-1]) if code == 0 else []
    h.check("reviews: sign-offs ('- John D.', 'Thanks, Mary', a name-only last line) are stripped; other endings kept",
            got == list(cases.values()), out)

    ag = _setup(h, "rv-co")
    (h.SB / "tests" / ".state" / "dr_reviews.json").write_text(json.dumps(REVIEWS))
    svc = ag.w("tmp/services.txt", "roof repair\ngutter cleaning\n")
    rid = ag.start("verify")
    code, out = h.sh(f'python3 tests/dr_wrap.py reviews run rv-co --run {rid} --keyword "Rv Co" '
                     f'--location "Springfield,Missouri,United States" --services-file {svc} --cities Springfield '
                     f'--confirmed --max-wait 5')
    d = ag.c / "data" / "reviews"
    ment = (d / "mentions.csv").read_text() if (d / "mentions.csv").exists() else ""
    rcsv = (d / "reviews.csv").read_text() if (d / "reviews.csv").exists() else ""
    cl = (d / "customer-language.md").read_text() if (d / "customer-language.md").exists() else ""
    names = ("John D", "Mary", "Sarah Miller", "John Doe", "Mary Smith", "Pete Ross", "Ann Lee", "Bob Kane")
    h.check("reviews: no sign-off or reviewer name in reviews.csv, mentions.csv or customer-language.md",
            code == 0 and ment and cl and not [n for n in names if n in ment + rcsv + cl], out[-400:])
    h.check("reviews: the run counts stripped sign-offs and flags texts still ending in a name (by id)",
            "3 reviewer sign-off(s) stripped" in out and "1 text(s) still end in a capitalised name" in out
            and "r4" in out, out[-400:])
    sm = (d / "reviews-summary.md").read_text() if (d / "reviews-summary.md").exists() else ""
    h.check("reviews: reviews-summary.md has the review count, rating distribution and themes with counts",
            "4.7 from 6 reviews" in sm and "## Rating distribution" in sm and "| 5 | 4 |" in sm
            and "| 2 | 1 |" in sm and "## Themes" in sm and "| roof repair | 1 |" in sm, sm[:800])
    h.check("reviews: the summary carries no reviewer names and no quotes",
            sm and not [n for n in names + ("Tom",) if n in sm] and '"' not in sm, sm[:800])
    (d / "reviews-summary.md").unlink()
    code, out = h.sh(f"python3 scripts/reviews.py summarize rv-co --services-file {svc} --cities Springfield")
    costs = (ag.c / "dfs-costs.jsonl").read_text()
    h.check("reviews: summarize rebuilds every output from the saved raw export, with no new call",
            code == 0 and (d / "reviews-summary.md").exists() and costs.count("reviews/task_post") == 1, out)
    ag.fin(rid, "reviews")
    _done(h)


def t_fanout_spread(h):
    import sys
    code, out = h.sh("python3 -c \"import sys; sys.path.insert(0, 'scripts'); import fanout; "
                     "p = fanout.seed_pairs(['a', 'b', 'c'], ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']); "
                     "f = p[:6]; print(len({s for s, _ in f}), len({c for _, c in f}), len(p), len(set(p)))\"")
    h.check("fan-out: the first max(services, cities) seeds cover every service and every city (3 × 6)",
            out.strip().endswith("3 6 18 18"), out)
    code, out = h.sh("python3 -c \"import sys; sys.path.insert(0, 'scripts'); import fanout; "
                     "p = fanout.seed_pairs(['a', 'b', 'c', 'd', 'e', 'f', 'g'], ['C1', 'C2']); "
                     "f = p[:7]; print(len({s for s, _ in f}), len({c for _, c in f}), p[0])\"")
    h.check("fan-out: 7 services × 2 cities — every service within 7 seeds, primary city first",
            "7 2 ('a', 'C1')" in out, out)

    ag = _setup(h, "fs-co", cost=0.003)
    svc = ag.w("tmp/services.txt", "roof repair\nroof replacement\ngutters\nsiding\nskylights\n")
    rid = ag.start("verify")
    cities = "Springfield,Nixa,Ozark,Republic"
    code, out = h.sh(f"python3 tests/dr_wrap.py fanout run fs-co --run {rid} --services-file {svc} "
                     f"--cities {cities} --cap 5")
    d = ag.c / "data" / "fanout"
    seeds = list(csv.DictReader(open(d / "seeds.csv"))) if (d / "seeds.csv").exists() else []
    h.check("fan-out: with --cap 5, the seeds cover all 5 services and all 4 cities (not 2 cities)",
            code == 0 and len(seeds) == 5 and len({r["service"] for r in seeds}) == 5
            and len({r["city"] for r in seeds}) == 4, out[-300:] + str(seeds))
    rows = list(csv.DictReader(open(d / "fanout-queries.csv"))) if (d / "fanout-queries.csv").exists() else []
    md = (d / "fanout-routing.md").read_text() if (d / "fanout-routing.md").exists() else ""
    h.check("fan-out: a group column (the service) in fanout-queries.csv and the routing worksheet",
            rows and all(r.get("group") for r in rows) and "roof repair" in rows[0]["group"]
            and "| # | Group | Query |" in md, str(rows[:1]) + md[:300])
    h.check("fan-out: the cost line reports failed-task spend apart",
            "(of which failed tasks $0.0000)" in out, out[-300:])
    ag.fin(rid, "fanout")
    _done(h)


def _routing_rows(md):
    out = {}
    for line in md.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 9 and c[0].isdigit():
            out[c[1]] = (c[6], c[7], c[8])
    return out


def t_paa_routing(h):
    qs = ["How much does roof repair cost?", "Do I need a permit for roof repair?", "How long does a roof last?"]
    ag = _setup(h, "pa-co", mode={"paa": qs})
    svc = ag.w("tmp/services.txt", "roof repair\n")
    rid = ag.start("verify")
    cmd = (f"python3 tests/dr_wrap.py paa run pa-co --run {rid} --services-file {svc} --cities Springfield "
           f"--state Missouri --confirmed")
    code, out = h.sh(cmd)
    f = ag.c / "data" / "paa" / "paa-routing.md"
    md = f.read_text() if f.exists() else ""
    h.check("PAA: first run writes the worksheet with empty Intent/Route/Note", code == 0 and
            _routing_rows(md).get(qs[0]) == ("", "", ""), out[-300:] + md[-400:])
    # the agent routes two questions; one with different case/spacing/end punctuation in the cell
    lines = []
    for line in md.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 9 and c[0].isdigit():
            if c[1] == qs[0]:
                c[6:9] = ["commercial investigation", "service FAQ (roof repair)", "price range only"]
            elif c[1] == qs[1]:
                c[1], c[6:9] = "  do I need a PERMIT   for roof repair ", ["informational", "blog topic", ""]
            line = "| " + " | ".join(c) + " |"
        lines.append(line)
    lines.append("| 99 | Is a metal roof noisy? | 1 | x | | 0.00 | comparison | blog topic | keep |")
    f.write_text("\n".join(lines) + "\n")
    code, out = h.sh(cmd)
    md = f.read_text()
    r = _routing_rows(md)
    h.check("PAA: a re-run keeps Intent/Route/Note by question text (case, spaces, end punctuation ignored)",
            code == 0 and r.get(qs[0]) == ("commercial investigation", "service FAQ (roof repair)", "price range only")
            and r.get(qs[1]) == ("informational", "blog topic", "") and r.get(qs[2]) == ("", "", ""),
            out[-300:] + md[-600:])
    h.check("PAA: a routed question not seen this run is kept at the bottom, not lost",
            "Routed earlier, not seen in this run" in md and "Is a metal roof noisy? — Intent: comparison" in md
            and "routing kept for 2 question(s)" in out, md[-400:])
    code, out = h.sh(cmd)
    md = f.read_text()
    h.check("PAA: a third run still keeps both the table routing and the earlier list",
            _routing_rows(md).get(qs[0], ("",))[0] == "commercial investigation"
            and "Is a metal roof noisy? — Intent: comparison · Route: blog topic · Note: keep" in md, md[-400:])
    ag.fin(rid, "paa")
    _done(h)


def t_failed_costs(h):
    ag = _setup(h, "fc-co", mode={"fail": ["backlinks/backlinks/live", "serp/"]})
    rid = ag.start("verify")
    ag.w("data/backlinks/raw/.keep", "")
    p = ag.w("tmp/p.json", json.dumps([{"target": "test.example"}, {"target": "test.example/roof-repair/"}]))
    code, out = h.sh(f"python3 tests/dr_wrap.py dfs call fc-co backlinks/backlinks/live --payload {p} "
                     f"--purpose S08 --estimate 0.01 --confirmed --out clients/fc-co/data/backlinks/raw/x.json")
    rows = [json.loads(l) for l in (ag.c / "dfs-costs.jsonl").read_text().splitlines() if l.strip()]
    h.check("costs: a call with a failed task logs failed_usd for it in the ledger",
            code == 0 and rows and rows[-1].get("failed_usd") == 0.002 and rows[-1].get("actual_usd") == 0.005, rows)
    h.check("costs: the command's cost line shows the failed-task spend apart",
            "DataforSEO this command: $0.0050 over 1 call(s) (of which failed tasks $0.0020)" in out, out[-300:])
    svc = ag.w("tmp/services.txt", "roof repair\n")
    code, out = h.sh(f"python3 tests/dr_wrap.py paa run fc-co --run {rid} --services-file {svc} --cities Springfield "
                     f"--state Missouri --confirmed")
    h.check("costs: a paid script stopped by a failed task still prints its cost line with the failed spend",
            code != 0 and "STOP" in out and "(of which failed tasks $0.0020)" in out, out[-400:])
    code, out = h.sh("python3 scripts/dfs.py ledger fc-co")
    h.check("costs: dfs.py ledger totals show failed tasks apart",
            code == 0 and "(of which failed tasks $0.0040)" in out and "[failed tasks $0.0020]" in out, out)
    ag.fin(rid, "costs")
    _done(h)


BACKLINKS = {"status_code": 20000, "tasks": [{"status_code": 20000, "result": [{"target": "test.example", "items": [
    {"type": "backlink", "url_to": "https://test.example/", "domain_from": "a.com"},
    {"type": "backlink", "url_to": "https://test.example/", "domain_from": "a.com"},
    {"type": "backlink", "url_to": "https://test.example/", "domain_from": "b.org"},
    {"type": "backlink", "url_to": "https://test.example/", "domain_from": "c.net"},
    {"type": "backlink", "url_to": "https://test.example/", "domain_from": "d.io"},
    {"type": "backlink", "url_to": "https://test.example/roof-repair/", "domain_from": "b.org"}]}]}]}
PAGES = {"tasks": [{"status_code": 20000, "result": [{"items": [
    {"url": "https://test.example/gutters/", "referring_domains": 4, "backlinks": 9}]}]}]}


def t_backlinks(h):
    ag = _setup(h, "bl-co")
    code, out = h.sh("python3 scripts/backlinks.py summary bl-co")
    h.check("backlinks: no saved export → refused in plain language (exit 4)", code == 4 and "dfs.py call" in out, out)
    ag.w("data/backlinks/raw/backlinks-2026-10-08.json", json.dumps(BACKLINKS))
    ag.w("data/backlinks/raw/pages-2026-10-08.json", json.dumps(PAGES))
    code, out = h.sh("python3 scripts/backlinks.py summary bl-co")
    f = ag.c / "data" / "backlinks" / "backlinks-per-url.csv"
    rows = {r["url"]: r for r in csv.DictReader(open(f))} if f.exists() else {}
    home = rows.get("https://test.example/", {})
    h.check("backlinks: backlinks-per-url.csv has url, referring domains, backlinks, top 3 referring domains",
            code == 0 and home.get("referring_domains") == "4" and home.get("backlinks") == "5"
            and home.get("top_referring_domains") == "a.com; b.org; c.net"
            and rows.get("https://test.example/roof-repair/", {}).get("referring_domains") == "1"
            and rows.get("https://test.example/gutters/", {}).get("backlinks") == "9", out + str(rows))
    _done(h)


SCENARIOS = [t_reviews, t_fanout_spread, t_paa_routing, t_failed_costs, t_backlinks]
