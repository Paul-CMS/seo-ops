#!/usr/bin/env python3
"""llm.py — direct Claude API calls for narrow judgment (Rewrite 4 Phase 2, D1). Standard library only.

    llm.py jobs                          every job: model, chunk size, the fixed prompt's sha
    llm.py ledger <slug>                 every call logged for a client, with the run totals
    llm.py estimate <slug> <job> --input F    what a job would cost on one input file (no call)

One call = a job's model + its short fixed prompt + its JSON schema + the input. The fixed prompt (and the job's
context, which is the same for every chunk of one job) are cached (`cache_control`); only the items change from chunk
to chunk. The jobs are called from the scripts that own the data, never by an agent:

    route-questions    Haiku   paa.py route · fanout.py route          Intent + Route for the S19/S21 worksheets
    review-meaning     Sonnet  reviews.py meaning                      which review sentences state each fact (CM-057)
    place-judge        Sonnet  places.py judge-all                     does the source passage support the fact?
    niche-judge        Sonnet  niches.py judge-all                     the same, for niche entity and state facts (Phase 6)
    faq-picks          Sonnet  outline.py faq                          FAQ fit picks per planned page
    conformance-judge  Sonnet  conformance.py judge                    the judgment checks for kept pages (S15)
    qa-explain         Haiku   qa.py explain                           plain explanation, fix and owner per QA row (Phase 5)

Key: ANTHROPIC_API_KEY in .env, typed by Paul (D1). It is loaded here, sent only in the request header, never
printed or logged. **No key yet, or the API answers 401:** nothing fails — the job falls back to its agent route and
the script says once, in plain words, "no API key — ran on the agent route".
Money: every call is logged to clients/<slug>/llm-costs.jsonl (the dfs-costs.jsonl shape, plus the model and the
tokens) and added to status.json spend.llm_usd. Before a job's first call its whole estimate plus what this run already
spent on llm.py is checked against config.json `llm_run_cap_usd`: above it → exit 5, "CONFIRM — …", and the job is
re-run with --confirmed only after Paul's yes.
Fake mode (tests): SEO_OPS_LLM_FAKE=<file.json> answers instead of the API — {"<job>": {"items": {"<id>": {answer}}}}
or {"<job>": {"error": 401}}. Usage is counted from the text length, so the cost log is exercised too;
SEO_OPS_LLM_FAKE_LOG=<file> records each request. SEO_OPS_LLM_API may point the real path at a localhost test server.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

from lib import append, client_dir, config, die, load_env, now, redact

API = "https://api.anthropic.com/v1/messages"
VERSION = "2023-06-01"
FALLBACK = "no API key — ran on the agent route"
DEFAULT_CAP = 1.00


class NoKey(Exception):
    """No ANTHROPIC_API_KEY in .env, or the API answered 401: the caller takes its agent route."""


class LlmError(Exception):
    """Any other failure (network, refusal, bad answer): the caller takes its agent route and says why."""


def _item(props, required=None):
    return {"type": "object", "properties": {"id": {"type": "string"}, **props},
            "required": ["id", *(required or list(props))], "additionalProperties": False}


S = {"type": "string"}
JOBS = {
    "route-questions": {
        "model": "claude-haiku-5-5", "effort": "low", "chunk": 60, "out_per_item": 70, "max_tokens": 8000,
        "item": _item({"intent": {"type": "string", "enum": ["informational", "problem-aware", "commercial investigation",
                                                            "comparison", "transactional"]},
                       "route": {"type": "string", "enum": ["service", "location", "blog topic", "drop"]},
                       "page": S, "note": S}),
        "prompt": """You route search questions for a local service business's website. Each item is one question or search
query that real customers ask (Google People Also Ask) or that an LLM brainstormed as a likely search (query fan-out).
The context lists the business, its planned service pages and location pages (each with its URL), and the headings and
FAQs other pages already own.

For every item return:
- intent: one of informational · problem-aware · commercial investigation · comparison · transactional.
- route: where the question is answered —
  "service": an H2 or FAQ on one service page. Use it when the question is about one service the business offers,
    wherever it is asked. Put that page's URL, exactly as given in the context, in "page".
  "location": a FAQ on one location page. Use it only when the answer really changes with the place (a local rule,
    local cost driver, local access or travel, a named local place). Put the city page's URL, exactly as given, in
    "page". A city name in the query is not enough on its own: "stair lift cost charleston" is a location question
    only if the local answer differs; otherwise it is the service page's question.
  "blog topic": a broad, educational or comparison question that no single money page should carry (alternatives,
    how-to, history, buying guides, paying for it in general).
  "drop": off-topic for this business, about another trade or a place outside its area, navigational (a brand or a
    company name), a duplicate of another item in the list or of a heading another page already owns, or unsafe to
    answer without facts the business has not given.
  For "blog topic" and "drop", "page" is "".
- note: at most 15 words, plain English. Say what the answer needs when it needs a fact only the client can give
  ("price answer needs client figures [NEED]"), which item a duplicate repeats ("duplicate of 12"), or why a row is
  dropped. "" when there is nothing to add.

Rules: never invent a page — "page" is one of the URLs in the context or "". Never route two items to the same answer
on the same page: route the clearest one and drop the rest as duplicates. A question about money, insurance, Medicare or
Medicaid, a programme or a legal rule is never answered with a number or a promise here — route it and note that the
answer needs a source. Return one result for every item id, in any order, and nothing else.""",
    },
    "review-meaning": {
        "model": "claude-sonnet-5-5", "effort": "low", "chunk": 12, "out_per_item": 120, "max_tokens": 8000,
        "item": _item({"stating": {"type": "array", "items": S}, "note": S}),
        "prompt": """You check customer reviews by meaning for a local service business (rule CM-057). A keyword search has
already matched review sentences to facts the business's pages may need — for example "response time", "warranty",
"cleans up", "takes photos", "explains the work", a named staff member, a place served. A keyword match is often wrong:
"same day" can match a guarantee search, "insurance" can appear in a complaint about something else.

Each item is one fact or topic: its key, its plain label, and the sentences the keyword search matched, each with a
sentence id. For every item return:
- stating: the ids of the sentences that, read by meaning, say the fact is true of this business as the customer
  experienced it. A sentence counts when a reasonable reader would agree it reports the fact; it does not count when
  it merely shares a word, is about another company, is a question, is sarcastic, reports the opposite, or is a
  complaint that the fact was missing. For a staff name, the sentence must be about a person of that name working for
  the business. For a place, the work must have been done in or for that place. For prices, the sentence must state an
  amount the customer paid or was quoted.
- note: at most 20 words: what the stating sentences say, in plain words, or why none count. Never a reviewer's name.

Rules: judge each sentence on its own words; do not infer from the star rating. Do not count the same sentence twice.
Return one result for every item id and nothing else.""",
    },
    "place-judge": {
        "model": "claude-sonnet-5-5", "effort": "low", "chunk": 10, "out_per_item": 80, "max_tokens": 6000,
        "item": _item({"verdict": {"type": "string", "enum": ["supported", "not_supported", "unclear"]}, "reason": S}),
        "prompt": """You verify place research for a local business's location pages. Each item is one fact found by a
research tool about a town or county, with the short quote the tool said supports it, and the passage of text taken
from the source page itself (the page loaded; the quote was not found word for word, so you read it by meaning).

For every item return:
- verdict:
  "supported" — the passage states the fact, in substance, for the place and the scope given (a town rule is a town
    rule; an unincorporated-county rule is not a town rule). Paraphrase is fine; small wording differences are fine.
  "not_supported" — the passage does not say it, says something different (another place, another year, another
    number, another scope), or contradicts it.
  "unclear" — the passage is too short, garbled, or about the topic but does not settle the specific claim.
- reason: at most 20 words, quoting the deciding words of the passage where you can.

Rules: use only the passage; never your own knowledge of the place. Numbers, dates, editions and names must match
exactly to be supported. A fact that is broader than the passage (all of the town, when the passage names one
neighbourhood) is not supported. Return one result for every item id and nothing else.""",
    },
    "niche-judge": {
        "model": "claude-sonnet-5-5", "effort": "low", "chunk": 10, "out_per_item": 80, "max_tokens": 6000,
        "item": _item({"verdict": {"type": "string", "enum": ["supported", "not_supported", "unclear"]}, "reason": S}),
        "prompt": """You verify industry research for a niche module that every local business in a trade reuses. Each
item is one fact found by a research tool about a service, its standards, its state licensing or its programmes, with the
short quote the tool said supports it, and the passage of text taken from the source page itself (the page loaded; the
quote was not found word for word, so you read it by meaning).

For every item return:
- verdict:
  "supported" — the passage states the fact, in substance, for the service and the scope given (a state rule is a
    state rule, a code edition is that edition). Paraphrase is fine; small wording differences are fine.
  "not_supported" — the passage does not say it, says something different (another service, state, edition, year or
    number), or contradicts it.
  "unclear" — the passage is too short, garbled, or about the topic but does not settle the specific claim.
- reason: at most 20 words, quoting the deciding words of the passage where you can.

Rules: use only the passage; never your own knowledge of the trade. Standard numbers, code editions, dates, board names
and programme names must match exactly to be supported. A fact that is broader than the passage (every state, when the
passage names one) is not supported. Return one result for every item id and nothing else.""",
    },
    "faq-picks": {
        "model": "claude-sonnet-5-5", "effort": "low", "chunk": 6, "out_per_item": 260, "max_tokens": 8000,
        "item": _item({"picks": {"type": "array", "items": {
            "type": "object", "properties": {"candidate": S, "category": S, "why": S},
            "required": ["candidate", "category", "why"], "additionalProperties": False}}}),
        "prompt": """You pick the FAQ questions for planned pages of a local service business's website. Each item is one
page: its type, name, URL, city where it has one, the candidate questions (each with an id, the question, where it came
from and how often it was seen) and, for location pages, the three FAQ categories. The context lists the headings and
FAQs other pages already own.

For every page return picks, each with:
- candidate: the id of the chosen candidate question, exactly as given. Never a question that is not in the list.
- category: for a location page, "1", "2" or "3" — the category the question answers; for any other page, "".
- why: at most 15 words: why this question fits this page.

How many and which:
- Location page: exactly three picks, one per category — 1 local cost or decision (what changes the job or the
  price here), 2 logistics in this area (permits, access, travel, timing), 3 trust in this area (local pain points,
  local experience). A question fits only when its answer is local to this city. If no candidate fits a category,
  leave that category out; never force a generic question in.
- Service page: four to six picks about this one service, most-seen first, covering different decisions (cost
  factors, types, how it works, upkeep, eligibility). Fewer when fewer fit.
- Any other page: up to four that fit the page's purpose.
Never pick a question another page already owns, a near-duplicate of another pick, a question about another service or
another city, or one whose answer needs a price, a programme rule or a legal claim nobody has sourced — unless the
candidate says the fact is on file. Return one result for every page id and nothing else.""",
    },
    "qa-explain": {
        "model": "claude-haiku-5-5", "effort": "low", "chunk": 40, "out_per_item": 90, "max_tokens": 8000,
        "item": _item({"explain": S, "fix": S, "who": {"type": "string", "enum": ["Jonie", "Paul", "writer", "system"]}}),
        "prompt": """You explain mechanical QA results for a local service business's new website pages, before they are
published, to the people who act on them: Jonie (the VA who builds and publishes pages in WordPress), Paul (the
account manager who decides) and the writer (who revises an approved page file). Each item is one failed or flagged
check: the page, its URL, the check's name and rule ID, and the script's own one-line detail.

For every item return:
- explain: at most 25 words, plain English: what is wrong and why it matters to a visitor or to search — no jargon,
  no rule IDs, never more than the detail says.
- fix: at most 25 words: the one concrete action, naming the exact text, URL or file from the detail.
- who: "Jonie" for a WordPress task (publishing, the head-code field, images, a link that did not render), "Paul" for
  a decision (a missing Brand Guide value, an exception, a waiver), "writer" for a change to the approved page file,
  "system" for a problem only a script change fixes.

Rules: never invent a value the detail does not give — say what is missing instead. Never soften an error into a
suggestion. Return one result for every item id and nothing else.""",
    },
    "conformance-judge": {
        "model": "claude-sonnet-5-5", "effort": "low", "chunk": 3, "out_per_item": 900, "max_tokens": 12000,
        "item": _item({"checks": {"type": "array", "items": {
            "type": "object", "properties": {"check": S, "result": {"type": "string", "enum": ["PASS", "FAIL", "NE", "N/A"]},
                                             "detail": S},
            "required": ["check", "result", "detail"], "additionalProperties": False}}}),
        "prompt": """You score existing web pages of a local service business against their page specification, during a
site audit. These pages are being kept (not rebuilt), so the score decides what is fixed on them. Each item is one page:
its URL and type, its SEO title, meta description, H1, H2s, word count, the page text where it was captured, and the
list of checks to score — each check has an id and its requirement from the spec. The context gives the brand name, the
planned cities and the homepage's reserved variant.

For every check on every page return:
- result: "PASS" when the page meets the requirement; "FAIL" when it does not; "NE" (needs evidence) when the
  requirement needs something the item does not contain — most often the page text, or headings beyond those given;
  "N/A" when the requirement does not apply to this page (for example an H1 rule when the page has no H1 — that is
  failed by the one-H1 check, not here).
- detail: at most 20 words: the deciding evidence (quote the title or heading) or what is missing.

Rules: judge only from the item; never assume what the rest of the page says. A requirement with several parts fails
when any part fails and is NE when no part fails but one cannot be seen. Do not score checks that were not asked.
"Recommendation checks" (about what the audit recommends, not the page) are N/A here. Return one result for every page
id, with every check it asked, and nothing else.""",
    },
}

_SAID = set()
_CACHED = set()   # fake mode: jobs whose cache was written in this process


def say_fallback(why_route):
    """Print the plain-words fallback line once per process."""
    if "nokey" not in _SAID:
        _SAID.add("nokey")
        print(f"{FALLBACK} — {why_route}")


def endpoint():
    """The Messages endpoint. SEO_OPS_LLM_API may point it at a local test server only (never another host: the key
    goes in the header)."""
    alt = os.environ.get("SEO_OPS_LLM_API", "")
    return alt if alt.startswith(("http://127.0.0.1:", "http://localhost:")) else API


def _fake():
    p = os.environ.get("SEO_OPS_LLM_FAKE")
    return json.loads(open(p).read()) if p else None


def api_key():
    k = (load_env().get("ANTHROPIC_API_KEY") or "").strip()
    if not k or k.startswith(("sk-ant-...", "<", "your")):
        raise NoKey("ANTHROPIC_API_KEY is not in .env")
    return k


def prices(model):
    import usage
    p = usage.price_for(model)
    if not p:
        raise LlmError(f"no price for {model} in scripts/model_prices.json")
    return p


def tokens_of(text):
    return max(1, len(text) // 3)   # a safe over-count for English and JSON


def estimate(job, context, items):
    """Upper-bound USD for the whole job: every chunk's input (first chunk writes the cache) + its output budget."""
    j = JOBS[job]
    p = prices(j["model"])
    fixed = tokens_of(j["prompt"]) + tokens_of(json.dumps(context, ensure_ascii=False))
    usd = 0.0
    for n, chunk in enumerate(chunks(items, j["chunk"])):
        inp = tokens_of(json.dumps({"items": chunk}, ensure_ascii=False))
        out = min(j["max_tokens"], 400 + j["out_per_item"] * len(chunk))
        usd += (fixed * (p["cache_write_5m"] if n == 0 else p["cache_read"]) + inp * p["input"] + out * p["output"]) / 1e6
    return round(usd, 4)


def chunks(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)] or []


def run_spent(slug, run_id):
    p = client_dir(slug) / "llm-costs.jsonl"
    if not run_id or not p.exists():
        return 0.0
    rows = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    return sum(float(r.get("actual_usd") or 0) for r in rows if r.get("run_id") == run_id)


def cap():
    return float(config().get("llm_run_cap_usd", DEFAULT_CAP))


def guard(slug, run_id, est, confirmed, what):
    spent = run_spent(slug, run_id)
    if not confirmed and est + spent > cap():
        print(f"CONFIRM — {what} is estimated at ${est:.4f} on the Claude API (run total ${est + spent:.4f}, over the "
              f"${cap():.2f} per-run cap in config.json llm_run_cap_usd). Ask Paul, then re-run with --confirmed.")
        sys.exit(5)


def log_cost(slug, run_id, job, model, purpose, est, usage_, actual):
    import status as St
    rec = {"at": now(), "run_id": run_id, "endpoint": f"anthropic/messages {model}", "job": job, "model": model,
           "purpose": purpose, "estimate_usd": est, "actual_usd": round(actual, 6),
           "tokens": {k: int(usage_.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                                           "cache_read_input_tokens", "output_tokens")}}
    append(client_dir(slug) / "llm-costs.jsonl", json.dumps(rec) + "\n")
    st = St.load(slug)
    st.setdefault("spend", {})["llm_usd"] = round(st["spend"].get("llm_usd", 0) + actual, 6)
    St.save(slug, st)


def cost_of(model, u):
    p = prices(model)
    return (int(u.get("input_tokens") or 0) * p["input"] + int(u.get("cache_creation_input_tokens") or 0)
            * p["cache_write_5m"] + int(u.get("cache_read_input_tokens") or 0) * p["cache_read"]
            + int(u.get("output_tokens") or 0) * p["output"]) / 1e6


def body(job, context, chunk):
    j = JOBS[job]
    schema = {"type": "object", "properties": {"items": {"type": "array", "items": j["item"]}}, "required": ["items"],
              "additionalProperties": False}
    return {"model": j["model"], "max_tokens": j["max_tokens"],
            "system": [{"type": "text", "text": j["prompt"]},
                       {"type": "text", "text": "Context:\n" + json.dumps(context, ensure_ascii=False, sort_keys=True),
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps({"items": chunk}, ensure_ascii=False)}],
            "output_config": {"effort": j["effort"], "format": {"type": "json_schema", "schema": schema}}}


def _post(payload, key):
    """(answer dict, usage). Retries 429/5xx and network errors twice; 401 → NoKey."""
    data = json.dumps(payload).encode()
    last = None
    for attempt in range(3):
        req = urllib.request.Request(endpoint(), data=data, method="POST", headers={
            "x-api-key": key, "anthropic-version": VERSION, "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                resp = json.loads(r.read().decode())
            break
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise NoKey("the API answered 401 (the key in .env is not accepted)")
            last = f"HTTP {e.code} {e.read()[:300].decode('utf-8', 'replace')}"
            if e.code not in (429, 500, 502, 503, 504, 529):
                raise LlmError(redact(last))
        except (urllib.error.URLError, TimeoutError) as e:
            last = f"network: {e}"
        time.sleep(5 * (attempt + 1))
    else:
        raise LlmError(redact(str(last)))
    if resp.get("stop_reason") in ("refusal", "max_tokens"):
        raise LlmError(f"the model stopped: {resp.get('stop_reason')}")
    text = "".join(b.get("text", "") for b in resp.get("content") or [] if b.get("type") == "text")
    try:
        return json.loads(text), resp.get("usage") or {}
    except ValueError:
        raise LlmError("the answer was not JSON")


def _fake_post(job, payload, fake):
    f = fake.get(job) or {}
    if f.get("error") == 401:
        raise NoKey("the API answered 401 (fake)")
    if f.get("error"):
        raise LlmError(f"fake error {f['error']}")
    asked = json.loads(payload["messages"][0]["content"])["items"]
    if os.environ.get("SEO_OPS_LLM_FAKE_LOG"):   # the tests read what was asked
        append(os.environ["SEO_OPS_LLM_FAKE_LOG"], json.dumps({"job": job, "body": payload}, ensure_ascii=False) + "\n")
    ans = {"items": [{**f["items"][it["id"]], "id": it["id"]} for it in asked if it["id"] in (f.get("items") or {})]}
    fixed = sum(tokens_of(b["text"]) for b in payload["system"])
    first = job not in _CACHED
    _CACHED.add(job)
    use = {"input_tokens": tokens_of(payload["messages"][0]["content"]), "output_tokens": tokens_of(json.dumps(ans)),
           "cache_creation_input_tokens": fixed if first else 0, "cache_read_input_tokens": 0 if first else fixed}
    return ans, use


def run_job(slug, run_id, job, context, items, purpose, confirmed=False):
    """{item id: answer} for every item the model answered. Raises NoKey (take the agent route) or LlmError.
    Exits 5 when the job is over the per-run cap without Paul's yes."""
    j = JOBS[job]
    fake = _fake()
    key = None if fake is not None else api_key()
    if not items:
        return {}
    est = estimate(job, context, items)
    guard(slug, run_id, est, confirmed, purpose)
    out = {}
    parts = chunks(items, j["chunk"])
    for n, chunk in enumerate(parts, 1):
        payload = body(job, context, chunk)
        ans, use = _fake_post(job, payload, fake) if fake is not None else _post(payload, key)
        ids = {it["id"] for it in chunk}
        got = [a for a in (ans.get("items") or []) if isinstance(a, dict) and a.get("id") in ids]
        log_cost(slug, run_id, job, j["model"], f"{purpose} ({n}/{len(parts)}, {len(chunk)} item(s))",
                 round(est / len(parts), 4), use, cost_of(j["model"], use))
        out.update({a["id"]: a for a in got})
    return out


def attempt(slug, run_id, job, context, items, purpose, route, confirmed=False):
    """run_job, or None after saying why the job ran on its agent route (no key / 401 → the plain FALLBACK line)."""
    try:
        return run_job(slug, run_id, job, context, items, purpose, confirmed)
    except NoKey:
        say_fallback(route)
    except LlmError as e:
        print(f"the Claude API call failed ({e}) — ran on the agent route — {route}")
    return None


def prompt_sha(job):
    return hashlib.sha256(JOBS[job]["prompt"].encode()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("jobs")
    s = sub.add_parser("ledger"); s.add_argument("slug")
    s = sub.add_parser("estimate"); s.add_argument("slug"); s.add_argument("job", choices=sorted(JOBS))
    s.add_argument("--input", required=True, help='a JSON file {"context": {…}, "items": [{"id": …}, …]}')
    a = ap.parse_args()
    if a.cmd == "jobs":
        for k, j in JOBS.items():
            print(f"{k:18} {j['model']:18} {j['chunk']:>3} item(s) a call · prompt {prompt_sha(k)}")
        print(f"per-run cap: ${cap():.2f} (config.json llm_run_cap_usd)")
        return
    if a.cmd == "estimate":
        client_dir(a.slug)
        d = json.loads(open(a.input).read())
        print(f"{a.job}: {len(d['items'])} item(s) → ${estimate(a.job, d.get('context', {}), d['items']):.4f} at most "
              f"on {JOBS[a.job]['model']} (per-run cap ${cap():.2f})")
        return
    p = client_dir(a.slug) / "llm-costs.jsonl"
    rows = [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []
    for r in rows:
        t = r.get("tokens") or {}
        print(f"{r['at'][:16]}  ${float(r.get('actual_usd') or 0):8.4f}  (est ${float(r.get('estimate_usd') or 0):.4f})  "
              f"{r.get('model')}  in {t.get('input_tokens', 0)} · cache-write {t.get('cache_creation_input_tokens', 0)} · "
              f"cache-read {t.get('cache_read_input_tokens', 0)} · out {t.get('output_tokens', 0)} — {r['purpose']}")
    print(f"total ${sum(float(r.get('actual_usd') or 0) for r in rows):.4f} over {len(rows)} call(s)")


if __name__ == "__main__":
    try:
        main()
    except (NoKey, LlmError) as e:
        die(str(e), 8)
