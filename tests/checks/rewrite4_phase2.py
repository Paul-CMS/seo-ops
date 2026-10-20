"""Rewrite 4 Phase 2 — direct Claude API calls for narrow judgment (scripts/llm.py, D1). One call = model + short fixed
prompt + JSON schema + input; the fixed part cached; every call logged to llm-costs.jsonl; a per-run cap; a fake mode.
The jobs moved onto it — PAA and fan-out routing (Haiku), review meaning (Sonnet), places judge (Sonnet), FAQ fit picks
(Sonnet), conformance judgment for kept pages (Sonnet) — each with a regression check on HMM's saved data
(tests/fixtures/hmm, copied read-only from the main folder) and the no-key fallback: nothing fails, the job says once
"no API key — ran on the agent route" and leaves the work to its agent."""
import csv
import http.server
import json
import re
import shutil
import threading

FALLBACK = "no API key — ran on the agent route"


def _client(h, slug, name="Hmm Co"):
    h.sh(f'python3 scripts/status.py init {slug} --name "{name}" --domain homemobilemedical.com --type full '
         f"--industry \"stair lifts\" --category none")
    ag = h.Agent(slug)
    ag.fin(ag.start("new-client"), "set up")
    return ag


def _pages(h, slug, pages, batches=None):
    p = h.SB / "clients" / slug / "status.json"
    st = json.loads(p.read_text())
    st["pages"].update(pages)
    if batches is not None:
        st["build"] = st.get("build") or {}
        st["build"]["batches"] = batches
    p.write_text(json.dumps(st))


def _fx(h, name):
    return h.SB / "tests" / "fixtures" / "hmm" / name


def _rows(text, n):
    """{row number: cells} of the routing table (n columns)."""
    out = {}
    for l in text.splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if l.startswith("|") and len(c) == n and c[0].isdigit():
            out[c[0]] = c
    return out


def _blank(text, n):
    """The worksheet with every Intent / Route / Note cell emptied — as paa.py / fanout.py write it."""
    lines = []
    for l in text.splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if l.startswith("|") and len(c) == n and c[0].isdigit():
            c[-3:] = ["", "", ""]
            l = "| " + " | ".join(c) + " |"
        lines.append(l)
    return "\n".join(lines) + "\n"


def _answers(rows):
    """The agent's routing as llm.py answers: {id: {intent, route, page, note}}."""
    out = {}
    for n, c in rows.items():
        intent, route, note = c[-3:]
        kind, _, page = route.partition(" — ")
        out[n] = {"intent": intent, "page": page,
                  "route": "service" if kind.startswith("service") else "location" if kind.startswith("location") else kind,
                  "note": note}
    return out


def _env(h, fake, log=None):
    f = h.SB / "tests" / ".state" / "llm-fake.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(fake))
    return f"SEO_OPS_LLM_FAKE={f}" + (f" SEO_OPS_LLM_FAKE_LOG={log}" if log else "")


def _costs(h, slug):
    p = h.SB / "clients" / slug / "llm-costs.jsonl"
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


# ------------------------------------------------------------------ the routing jobs on HMM's worksheets
def t_hmm_routing(h):
    S = "p2-route"
    ag = _client(h, S)
    paa, fan = _fx(h, "paa-routing.md").read_text(), _fx(h, "fanout-routing.md").read_text()
    prow, frow = _rows(paa, 9), _rows(fan, 11)
    urls = sorted({c[-2].split(" — ", 1)[1] for c in list(prow.values()) + list(frow.values()) if " — /" in c[-2]})
    _pages(h, S, {f"p{i}": {"type": "location" if "service-area" in u else "service", "name": u,
                             "url": f"https://homemobilemedical.com{u}"} for i, u in enumerate(urls)})
    ag.w("data/paa/paa-routing.md", _blank(paa, 9))
    ag.w("data/fanout/fanout-routing.md", _blank(fan, 11))
    rid = ag.start("crawl")
    pa = _answers(prow)
    env = _env(h, {"route-questions": {"items": {**pa}}})
    code, out = h.sh(f"{env} python3 scripts/paa.py route {S} --run {rid}")
    got = _rows((ag.c / "data/paa/paa-routing.md").read_text(), 9)
    h.check("phase2 HMM: paa.py route fills all 35 PAA rows on the API and reproduces the agent's Intent, Route and Note",
            code == 0 and "35 of 35 row(s) routed" in out and got == prow, (out, [k for k in prow if got.get(k) != prow[k]][:5]))
    fa = _answers(frow)
    fa["7"] = {**fa["7"], "route": "service", "page": "/not-a-planned-page/"}
    # a row filled by hand before the run is never overwritten
    lines = _blank(fan, 11).splitlines()
    i12 = next(i for i, l in enumerate(lines) if l.startswith("| 12 |"))
    c12 = [x.strip() for x in lines[i12].strip().strip("|").split("|")]
    c12[-3:] = ["informational", "blog topic", "Paul's own call"]
    lines[i12] = "| " + " | ".join(c12) + " |"
    ag.w("data/fanout/fanout-routing.md", "\n".join(lines) + "\n")
    log = h.SB / "tests" / ".state" / "llm-requests.jsonl"
    log.unlink(missing_ok=True)
    env = _env(h, {"route-questions": {"items": fa}}, log)
    code, out = h.sh(f"{env} python3 scripts/fanout.py route {S} --run {rid}")
    got = _rows((ag.c / "data/fanout/fanout-routing.md").read_text(), 11)
    same = [k for k in frow if k not in ("7", "12") and got.get(k) == frow[k]]
    h.check("phase2 HMM: fanout.py route reproduces the agent's routing for all 352 other fan-out rows (354 in HMM)",
            code == 0 and len(same) == 352, (out, len(same)))
    h.check("phase2: a route naming a page that is not planned is left empty for the agent",
            got["7"][-2] == "" and "1 named a page that is not planned" in out, (got["7"], out))
    h.check("phase2: a row filled by hand before the run is never overwritten", got["12"][-3:] == c12[-3:], got["12"])
    reqs = [json.loads(x) for x in log.read_text().splitlines()]
    h.check("phase2: 353 fan-out rows are asked in chunks of 60 (6 calls), the hand-filled row not asked",
            len(reqs) == 6 and sum(len(json.loads(r["body"]["messages"][0]["content"])["items"]) for r in reqs) == 353, len(reqs))
    b = reqs[0]["body"]
    h.check("phase2: one call = the job's model + fixed prompt + context (cached) + JSON schema + the items",
            b["model"] == "claude-haiku-5-5" and b["system"][-1].get("cache_control") == {"type": "ephemeral"}
            and b["output_config"]["format"]["type"] == "json_schema" and "Context:" in b["system"][-1]["text"]
            and len({json.dumps(r["body"]["system"]) for r in reqs}) == 1, b.get("system"))
    costs = _costs(h, S)
    h.check("phase2: every call is logged to llm-costs.jsonl — run, job, model, tokens, estimate and actual cost",
            len(costs) == 1 + 6 and all(c["run_id"] == rid and c["job"] == "route-questions" and c["model"] == "claude-haiku-5-5"
                                        and c["actual_usd"] > 0 and c["tokens"]["output_tokens"] > 0 for c in costs)
            and costs[2]["tokens"]["cache_read_input_tokens"] > 0, costs[:2])
    st = h.status(S)
    h.check("phase2: the API spend is added to status.json spend.llm_usd",
            abs(st["spend"].get("llm_usd", 0) - sum(c["actual_usd"] for c in costs)) < 1e-5, st["spend"])
    code, out = h.sh(f"{env} python3 scripts/paa.py route {S} --run {rid}")
    h.check("phase2: a re-run asks nothing when every row is routed", code == 0 and "nothing to route" in out
            and len(_costs(h, S)) == 7, out)
    code, out = h.sh(f"python3 scripts/llm.py ledger {S}")
    h.check("phase2: llm.py ledger lists every call with its tokens and the total", code == 0 and "over 7 call(s)" in out
            and "cache-read" in out, out[-300:])
    ag.fin(rid, "routed")
    code, out = h.sh(f"python3 scripts/usage.py client {S}")
    h.check("phase2: usage.py shows the API spend beside the session spend", code == 0 and "API (llm.py) $" in out, out)
    h.sh(f"python3 scripts/render.py status {S}")
    md = (ag.c / "STATUS.md").read_text()
    h.check("phase2: STATUS.md shows Claude API (llm.py) spend, and an API column in the stage and step tables",
            "- Claude API (llm.py): $" in md and "| Session USD | API USD |" in md, md[-900:])


# ------------------------------------------------------------------ the cap and the key
def t_cap_and_key(h):
    S = "p2-cap"
    ag = _client(h, S)
    paa = _fx(h, "paa-routing.md").read_text()
    ag.w("data/paa/paa-routing.md", _blank(paa, 9))
    rid = ag.start("crawl")
    cfg = h.SB / "config.json"
    orig = cfg.read_text()
    c = json.loads(orig)
    c["llm_run_cap_usd"] = 0.00001
    cfg.write_text(json.dumps(c))
    env = _env(h, {"route-questions": {"items": _answers(_rows(paa, 9))}})
    code, out = h.sh(f"{env} python3 scripts/paa.py route {S} --run {rid}")
    h.check("phase2 cap: a job over the per-run cap is refused without Paul's yes (exit 5, CONFIRM), nothing called",
            code == 5 and "CONFIRM" in out and "llm_run_cap_usd" in out and not _costs(h, S), out)
    code, out = h.sh(f"{env} python3 scripts/paa.py route {S} --run {rid} --confirmed")
    h.check("phase2 cap: with --confirmed (after Paul's yes) it runs", code == 0 and "35 of 35" in out, out)
    cfg.write_text(orig)
    # the real HTTP path, against a local server: the key goes in the header only, never printed; 401 → agent route
    seen = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            seen["key"] = self.headers.get("x-api-key")
            seen["version"] = self.headers.get("anthropic-version")
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen["body"] = body
            if seen.get("deny"):
                self.send_response(401); self.end_headers(); self.wfile.write(b'{"type":"error"}'); return
            items = json.loads(body["messages"][0]["content"])["items"]
            ans = {"items": [{"id": it["id"], "intent": "informational", "route": "blog topic", "page": "", "note": ""}
                             for it in items]}
            resp = {"content": [{"type": "text", "text": json.dumps(ans)}], "stop_reason": "end_turn",
                    "usage": {"input_tokens": 900, "output_tokens": 400, "cache_creation_input_tokens": 700,
                              "cache_read_input_tokens": 0}}
            data = json.dumps(resp).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

        def log_message(self, *a):
            pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    secret = "sk-ant-api03-TESTSECRET-0123456789"
    env_file = h.SB / ".env"
    env_file.write_text(f"ANTHROPIC_API_KEY={secret}\n")
    try:
        ag.w("data/paa/paa-routing.md", _blank(paa, 9))
        api = f"SEO_OPS_LLM_API=http://127.0.0.1:{srv.server_port}/v1/messages"
        code, out = h.sh(f"{api} python3 scripts/paa.py route {S} --run {rid} --confirmed")
        h.check("phase2 key: the key from .env is sent in the x-api-key header and never printed",
                code == 0 and seen.get("key") == secret and secret not in out and seen.get("version") == "2023-06-01"
                and "35 of 35" in out, out)
        last = _costs(h, S)[-1]
        # haiku 5.5: 900*0.10 + 700*0.125 + 400*0.50 per 1e6
        h.check("phase2 key: the real answer's usage is priced from model_prices.json",
                abs(last["actual_usd"] - (900 * 0.10 + 700 * 0.125 + 400 * 0.50) / 1e6) < 1e-6, last)
        h.check("phase2 key: no secret in llm-costs.jsonl or the log",
                secret not in (ag.c / "llm-costs.jsonl").read_text() and secret not in (ag.c / "log.md").read_text())
        seen["deny"] = True
        ag.w("data/paa/paa-routing.md", _blank(paa, 9))
        code, out = h.sh(f"{api} python3 scripts/paa.py route {S} --run {rid} --confirmed")
        h.check("phase2 key: the API answers 401 → the run does not fail; it says once it ran on the agent route",
                code == 0 and out.count(FALLBACK) == 1 and secret not in out
                and _rows((ag.c / "data/paa/paa-routing.md").read_text(), 9)["1"][-2] == "", out)
        h.check("phase2 key: SEO_OPS_LLM_API can only point at localhost (the key is never sent elsewhere)",
                "127.0.0.1" in h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import os; "
                                    "os.environ['SEO_OPS_LLM_API']='http://127.0.0.1:9/x'; import llm; print(llm.endpoint())\"")[1]
                and "api.anthropic.com" in h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import os; "
                                                "os.environ['SEO_OPS_LLM_API']='https://evil.example/x'; import llm; "
                                                "print(llm.endpoint())\"")[1])
    finally:
        env_file.unlink(missing_ok=True)
        srv.shutdown()


# ------------------------------------------------------------------ the fallback, for every moved job
def t_fallback(h):
    """No ANTHROPIC_API_KEY (the sandbox has no .env), and a 401: each moved job ends 0, writes nothing, and says once,
    in plain words, that it ran on the agent route."""
    S = "p2-fall"
    ag = _client(h, S)
    paa, fan = _fx(h, "paa-routing.md").read_text(), _fx(h, "fanout-routing.md").read_text()
    ag.w("data/paa/paa-routing.md", _blank(paa, 9))
    ag.w("data/fanout/fanout-routing.md", _blank(fan, 11))
    (ag.c / "data/reviews").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_fx(h, "reviews.csv"), ag.c / "data/reviews/reviews.csv")
    (ag.c / "audit/2026-10-07").mkdir(parents=True)
    shutil.copyfile(_fx(h, "url-decision-map.csv"), ag.c / "audit/2026-10-07/url-decision-map.csv")
    shutil.copytree(_fx(h, "crawl"), ag.c / "inputs/crawl", dirs_exist_ok=True)
    _pages(h, S, {"loc-beaufort": {"type": "location", "name": "Beaufort, SC", "city": "Beaufort",
                                   "url": "https://homemobilemedical.com/beaufort-sc/"}},
           [{"id": "locs", "kind": "location", "label": "Locations", "pages": ["loc-beaufort"], "route": "outline"}])
    _place(h, "SC", "Fallville")
    rid = ag.start("crawl")
    before = {p: p.read_text() for p in (ag.c / "data").rglob("*.md")}
    cmds = {"PAA routing": f"python3 scripts/paa.py route {S} --run {rid}",
            "fan-out routing": f"python3 scripts/fanout.py route {S} --run {rid}",
            "review meaning": f"python3 scripts/reviews.py meaning {S} --run {rid}",
            "places judge": f"python3 tests/fakes.py places judge-all SC Fallville stair-lifts --slug {S} --run {rid}",
            "FAQ picks": f"python3 scripts/outline.py faq {S} locs --run {rid}",
            "conformance judgment": f"python3 scripts/conformance.py judge {S} --run {rid}"}
    for label, cmd in cmds.items():
        if label == "FAQ picks":   # candidates come from routed rows: give it HMM's routed fan-out sheet
            ag.w("data/fanout/fanout-routing.md", fan)
            before = {p: p.read_text() for p in (ag.c / "data").rglob("*.md")}
        code, out = h.sh(cmd)
        h.check(f"phase2 fallback: no API key — {label} does not fail and says once it ran on the agent route",
                code == 0 and out.count(FALLBACK) == 1, out)
        code, out = h.sh(f"{_env(h, {k: {'error': 401} for k in ('route-questions', 'review-meaning', 'place-judge', 'faq-picks', 'conformance-judge')})} {cmd}")
        h.check(f"phase2 fallback: the API answers 401 — {label} does the same", code == 0 and out.count(FALLBACK) == 1, out)
    after = {p: p.read_text() for p in (ag.c / "data").rglob("*.md")}
    layer = json.loads((h.SB / "methodology/places/sc/fallville/stair-lifts.json").read_text())
    h.check("phase2 fallback: nothing was written — worksheets, review facts, place facts, FAQ picks, judgment file",
            before == after and not _costs(h, S) and not (ag.c / "build/locs/faq-picks.json").exists()
            and not (ag.c / "audit/conformance-judgment.csv").exists()
            and not any(f.get("meaning_checked") for f in (json.loads((ag.c / "facts.json").read_text()).get("facts", [])
                                                            if (ag.c / "facts.json").exists() else []))
            and all(f["verified"] == "check" for f in layer["facts"] if f["id"] != "n-4"))


# ------------------------------------------------------------------ review meaning on HMM's reviews
TRUTH = {   # Paul's rule CM-057, read by hand on HMM's 24 reviews: the sentence must say the fact, not share a word
    "fact:timeframe": ["got me the chair the same day"], "fact:response_time": ["got me the chair the same day"],
    "fact:guarantees": [], "fact:pricing": [], "fact:insurance": [], "practice:clean-up": [],
    "practice:explains": ["explains the process"], "prices ($ amounts)": []}


def t_hmm_review_meaning(h):
    S = "p2-rev"
    ag = _client(h, S)
    (ag.c / "data/reviews").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_fx(h, "reviews.csv"), ag.c / "data/reviews/reviews.csv")
    rid = ag.start("crawl")
    code, out = h.sh(f"python3 scripts/reviews.py extract {S} --run {rid}")
    found = json.loads((ag.c / "data/reviews/review-facts.json").read_text())["facts"]
    h.check("phase2 HMM: reviews.py extract finds the 8 keyword candidates the audit found (explains: 2 reviewers)",
            code == 0 and set(found) == set(TRUTH) and found["practice:explains"]["count"] == 2, (out, sorted(found)))
    log = h.SB / "tests" / ".state" / "llm-requests.jsonl"
    log.unlink(missing_ok=True)
    code, out = h.sh(f"{_env(h, {'review-meaning': {'items': {}}}, log)} python3 scripts/reviews.py meaning {S} --run {rid}")
    items = json.loads(json.loads(log.read_text().splitlines()[0])["body"]["messages"][0]["content"])["items"]
    h.check("phase2 HMM: every candidate is sent with its sentences, no reviewer name or key",
            {i["id"] for i in items} == set(TRUTH) and all("reviewer" not in json.dumps(i) for i in items), items[:2])
    ans = {i["id"]: {"stating": [s["sentence_id"] for s in i["sentences"]
                                 if any(t in s["text"] for t in TRUTH[i["id"]])], "note": "read"} for i in items}
    code, out = h.sh(f"{_env(h, {'review-meaning': {'items': ans}})} python3 scripts/reviews.py meaning {S} --run {rid}")
    rows = {r["key"]: r for r in json.loads((ag.c / "facts.json").read_text())["facts"] if r.get("section") == "R"}
    h.check("phase2 HMM: the meaning check counts only the reviewers whose sentence states the fact — 'wouldn't even "
            "explain' drops (explains 2 → 1), 'same day' is not a guarantee (0), none reaches 3",
            code == 0 and rows["practice:explains"]["count"] == 1 and rows["fact:guarantees"]["count"] == 0
            and rows["fact:timeframe"]["count"] == 1 and all(r.get("meaning_checked") for r in rows.values())
            and "llm.py review-meaning" in rows["fact:pricing"]["who"] and "0 reported by 3+" in out, (out, rows))
    h.check("phase2: the meaning check is logged as a REVIEW FACT CHECKED line", "REVIEW FACT CHECKED" in
            (ag.c / "log.md").read_text())
    code, out = h.sh(f"python3 scripts/reviews.py checked {S} --run {rid} --key practice:explains --count 3 --note x")
    h.check("phase2: reviews.py checked (the researcher's route) still works", code == 0 and "counts as Known" in out, out)


# ------------------------------------------------------------------ places judge (no HMM place research is stored yet)
def _place(h, state, place):
    d = h.SB / "methodology" / "places" / state.lower() / place.lower()
    d.mkdir(parents=True, exist_ok=True)
    f = lambda i, fact, url, quote: {"id": i, "fact": fact, "applies_to": f"all of {place}", "source_url": url,
                                     "publisher": "Town", "source_type": "official", "date": "2025-01-01", "quote": quote,
                                     "verified": "check", "added": "2026-10-20"}
    (d / "stair-lifts.json").write_text(json.dumps({
        "state": state, "place": place, "niche": "stair-lifts", "dropped": [], "not_found": [], "questions": [],
        "identity": {}, "facts": [
            f("n-1", "The Oak Park HOA must approve roof colours before work starts.", "https://springfield.example.gov/hoa",
              "HOA approval of colours is required"),
            f("n-2", "The design wind speed is 160 mph.", "https://springfield.example.gov/wind", "wind speed 160 mph"),
            f("n-3", "Permits are issued by the county.", "https://springfield.example.gov/wind", "county issues permits"),
            f("n-4", "A page that no longer loads.", "https://springfield.example.gov/gone", "gone")]}))


def t_places_judge(h):
    S = "p2-place"
    ag = _client(h, S)
    _place(h, "SC", "Judgeton")
    rid = ag.start("crawl")
    log = h.SB / "tests" / ".state" / "llm-requests.jsonl"
    log.unlink(missing_ok=True)
    fake = {"place-judge": {"items": {"n-1": {"verdict": "supported", "reason": "'requires approval of roof colours'"},
                                      "n-2": {"verdict": "not_supported", "reason": "the page says 150 mph"},
                                      "n-3": {"verdict": "unclear", "reason": "the passage does not mention permits"}}}}
    code, out = h.sh(f"{_env(h, fake, log)} python3 tests/fakes.py places judge-all SC Judgeton stair-lifts --slug {S} "
                     f"--run {rid}")
    layer = json.loads((h.SB / "methodology/places/sc/judgeton/stair-lifts.json").read_text())
    by = {f["id"]: f for f in layer["facts"]}
    h.check("phase2 places: supported → verified, not supported → dropped (never asked), unclear → left for the "
            "researcher, a page that no longer loads is not sent",
            code == 0 and by["n-1"]["verified"] is True and "llm.py place-judge" in by["n-1"]["verified_how"]
            and "n-2" not in by and layer["dropped"][0]["id"] == "n-2" and "150 mph" in layer["dropped"][0]["reason"]
            and by["n-3"]["verified"] == "check" and by["n-4"]["verified"] == "check"
            and "1 verified · 1 dropped · 1 unclear" in out, (out, by))
    items = json.loads(json.loads(log.read_text().splitlines()[0])["body"]["messages"][0]["content"])["items"]
    h.check("phase2 places: each fact goes with the passage of its own source page (Sonnet)",
            {i["id"] for i in items} == {"n-1", "n-2", "n-3"} and "150 mph" in next(i for i in items if i["id"] == "n-2")["passage"]
            and json.loads(log.read_text().splitlines()[0])["body"]["model"] == "claude-sonnet-5-5", items)
    h.check("phase2 places: the client's run pays — the call is in its llm-costs.jsonl",
            [c["job"] for c in _costs(h, S)] == ["place-judge"])
    code, out = h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import places; "
                     "b = 'filler ' * 3000 + 'The design wind speed in Judgeton is 150 mph. ' + 'filler ' * 3000; "
                     "print('150 mph' in places.passage(places._plain(b), 'wind speed 160 mph', 'design wind speed'))\"")
    h.check("phase2 places: the passage is the stretch of a long page that holds the quote's words", out.strip() == "True", out)


# ------------------------------------------------------------------ FAQ picks from HMM's routed questions
def t_hmm_faq_picks(h):
    S = "p2-faq"
    ag = _client(h, S)
    ag.w("data/fanout/fanout-routing.md", _fx(h, "fanout-routing.md").read_text())
    ag.w("data/paa/paa-routing.md", _fx(h, "paa-routing.md").read_text())
    _pages(h, S, {"loc-beaufort": {"type": "location", "name": "Beaufort, SC", "city": "Beaufort",
                                   "url": "https://homemobilemedical.com/beaufort-sc/"},
                  "loc-charleston": {"type": "location", "name": "Charleston, SC", "city": "Charleston",
                                     "url": "https://homemobilemedical.com/charleston-sc/"},
                  "loc-nowhere": {"type": "location", "name": "Nowhere, SC", "city": "Nowhere",
                                  "url": "https://homemobilemedical.com/nowhere-sc/"}},
           [{"id": "locs", "kind": "location", "label": "Locations", "pages": ["loc-beaufort", "loc-charleston", "loc-nowhere"],
             "route": "outline"}])
    fan = _rows(_fx(h, "fanout-routing.md").read_text(), 11)
    want = {c: sum(1 for r in fan.values() if r[-2].startswith("location FAQ") and f"/{c}-sc/" in r[-2])
            for c in ("beaufort", "charleston")}
    rid = ag.start("crawl")
    log = h.SB / "tests" / ".state" / "llm-requests.jsonl"
    log.unlink(missing_ok=True)
    h.sh(f"{_env(h, {'faq-picks': {'items': {}}}, log)} python3 scripts/outline.py faq {S} locs --run {rid}")
    items = {i["id"]: i for i in json.loads(json.loads(log.read_text().splitlines()[0])["body"]["messages"][0]["content"])["items"]}
    h.check("phase2 HMM: each location page's candidates are HMM's fan-out rows routed to its city (older /service-area/ "
            "URLs included), a page with none is not sent",
            set(items) == {"loc-beaufort", "loc-charleston"}
            and len(items["loc-beaufort"]["candidates"]) == min(40, want["beaufort"]) > 0
            and len(items["loc-charleston"]["candidates"]) == min(40, want["charleston"])
            and all("location FAQ" in c["source"] for c in items["loc-beaufort"]["candidates"]),
            {k: len(v["candidates"]) for k, v in items.items()})
    cb = items["loc-beaufort"]["candidates"]
    ans = {"loc-beaufort": {"picks": [{"candidate": cb[0]["id"], "category": "1", "why": "local cost"},
                                      {"candidate": cb[1]["id"], "category": "1", "why": "second cat-1: refused"},
                                      {"candidate": "q999", "category": "2", "why": "not a candidate: refused"},
                                      {"candidate": cb[2]["id"], "category": "3", "why": "local trust"}]},
           "loc-charleston": {"picks": []}}
    code, out = h.sh(f"{_env(h, {'faq-picks': {'items': ans}})} python3 scripts/outline.py faq {S} locs --run {rid}")
    picks = json.loads((ag.c / "build/locs/faq-picks.json").read_text())["pages"]
    h.check("phase2: FAQ picks keep only listed candidates, one per location category",
            code == 0 and [p["question"] for p in picks["loc-beaufort"]] == [cb[0]["question"], cb[2]["question"]]
            and [p["category"] for p in picks["loc-beaufort"]] == ["1", "3"] and picks["loc-charleston"] == [], (out, picks))
    code, out = h.sh(f"python3 -c \"import sys; sys.path.insert(0,'scripts'); import outline; "
                     f"print(len(outline.faq_picks('{S}', 'locs', 'loc-beaufort')))\"")
    h.check("phase2: the outline reads the picks (faq_picks) for the page", out.strip() == "2", out)
    h.check("phase2: the outline shows the picks above the candidates", "## FAQ picks (outline.py faq on the Claude API"
            in (h.SB / "scripts/outline.py").read_text())


# ------------------------------------------------------------------ conformance judgment on HMM's kept pages
def _scorecard(h):
    """{url: {check: result}} from the audit agent's conformance-scorecard.csv (ranges like BLG-06..15 expanded)."""
    out = {}
    with open(_fx(h, "conformance-scorecard.csv"), newline="", encoding="utf-8-sig") as fh:
        for r in csv.reader(fh):
            if len(r) < 5 or not r[0].startswith("http"):
                continue
            d = {}
            for part in r[4].split(";"):
                m = re.match(r"\s*([A-Z]+)-(\d+)(?:\.\.(\d+))?=(\S+)", part)
                if not m:
                    continue
                for n in range(int(m.group(2)), int(m.group(3) or m.group(2)) + 1):
                    v = m.group(4).upper().rstrip(",")
                    d[f"{m.group(1)}-{n:02d}"] = "PASS" if v == "PASS" else "FAIL" if v.startswith("FAIL") else \
                        "N/A" if v.startswith("N/A") else "NE"
            out[r[0]] = d
    return out


def t_hmm_conformance(h):
    S = "p2-conf"
    ag = _client(h, S)
    (ag.c / "audit/2026-10-07").mkdir(parents=True)
    shutil.copyfile(_fx(h, "url-decision-map.csv"), ag.c / "audit/2026-10-07/url-decision-map.csv")
    shutil.copytree(_fx(h, "crawl"), ag.c / "inputs/crawl", dirs_exist_ok=True)
    rid = ag.start("crawl")
    log = h.SB / "tests" / ".state" / "llm-requests.jsonl"
    log.unlink(missing_ok=True)
    h.sh(f"{_env(h, {'conformance-judge': {'items': {}}}, log)} python3 scripts/conformance.py judge {S} --run {rid}")
    items = [i for l in log.read_text().splitlines() for i in json.loads(json.loads(l)["body"]["messages"][0]["content"])["items"]]
    card = _scorecard(h)
    blog = {u for u, d in card.items() if any(k.startswith("BLG") for k in d)}
    h.check("phase2 HMM: the kept pages with a spec are judged — HMM's 21 blog posts; legal pages (no spec), 301 rows "
            "and pages Build rebuilds are not",
            {i["url"] for i in items} == blog and len(items) == 21, (len(items), sorted({i["type"] for i in items})))
    med = next(i for i in items if "are-stair-lifts-covered-by-medicare" in i["url"])
    h.check("phase2 HMM: each page goes with its crawl title, H1 and H2s and every BLG judgment check (no page text → NE)",
            med["title"] and med["h1"] and len(med["checks"]) == 22 and "not captured" in med["page_text"], med)
    ans = {i["id"]: {"checks": [{"check": c["check"], "result": card[i["url"]].get(c["check"], "NE"), "detail": "as audited"}
                                for c in i["checks"]]} for i in items}
    ans[items[0]["id"]]["checks"] = ans[items[0]["id"]]["checks"][1:] + [{"check": "SVC-01", "result": "PASS", "detail": "x"}]
    code, out = h.sh(f"{_env(h, {'conformance-judge': {'items': ans}})} python3 scripts/conformance.py judge {S} --run {rid}")
    with open(ag.c / "audit/conformance-judgment.csv", newline="") as fh:
        rows = list(csv.DictReader(fh))
    agree = [r for r in rows if r["who"].startswith("llm.py") and card[r["url"]].get(r["check"], "NE") == r["result"]]
    first = [r for r in rows if r["url"] == items[0]["url"]]
    h.check("phase2 HMM: conformance.py judge writes the agent's S15 scorecard back exactly for the 21 kept blog posts "
            "(461 of 462 checks; the one not answered stays open as NE)",
            code == 0 and len(rows) == 462 and len(agree) == 461
            and not any(r["check"] == "SVC-01" for r in rows)
            and [r for r in first if r["who"] == "open"][0]["result"] == "NE", (out, len(rows), len(agree)))
    md = (ag.c / "audit/conformance.md").read_text()
    h.check("phase2: conformance.md gains the judgment section with the failures listed",
            "## Judgment checks (kept pages)" in md and "BLG-03" in md, md[-400:])


SCENARIOS = [t_hmm_routing, t_cap_and_key, t_fallback, t_hmm_review_meaning, t_places_judge, t_hmm_faq_picks,
             t_hmm_conformance]
