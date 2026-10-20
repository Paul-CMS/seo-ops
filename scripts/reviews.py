#!/usr/bin/env python3
"""reviews.py — add-on 3: Google reviews → customer language. Discovery step (client has the sheet).

    reviews.py estimate <slug> [--depth 200]
    reviews.py run      <slug> --run R --keyword "Business Name" --location "City,State,United States"
                        [--depth 200] [--confirmed] [--max-wait 540] [--services-file F] [--cities "a,b"]
    reviews.py summarize <slug> [--services-file F] [--cities "a,b"]
                        rebuild every output from the saved raw/reviews.json (no DataforSEO call)
    reviews.py extract  <slug> --run R
                        CM-057 (rewrite 2 P5): for every fact the evidence gate needs, and for staff, places,
                        materials, practices, prices, timelines and warranties, the review sentences that say it and the
                        number of DIFFERENT reviewers — written to data/reviews/review-facts.json, the "Facts customers
                        report" table in customer-language.md, and facts.json as customer_reported candidates
                        (section R: never a Brand Guide row, so no approval changes). A keyword match never counts as
                        Known: the researcher reads each by meaning and records it —
    reviews.py meaning  <slug> --run R [--confirmed]   every match read by meaning on the Claude API (llm.py
                        review-meaning, Sonnet — Rewrite 4 Phase 2); with no API key the researcher does it instead:
    reviews.py checked  <slug> --run R --key fact:<key> --count N   (N different reviewers left; Known at 3+)

Pulls the newest reviews (up to --depth, max 200 here) through DataforSEO Business Data.
Saves raw data (with reviewer names) to clients/<slug>/data/reviews/raw/ — git-ignored and
never used in a deliverable. Writes reviews.csv WITHOUT reviewer names, plus mentions.csv
(services, cities and questions spotted in each review) for the agent that writes
customer-language.md, and reviews-summary.md — the compact summary agents read (themes with counts,
rating distribution, review count; no reviewer names, no quotes). Records rating + count for the
"The Best" proof condition (CM-020).
A reviewer's sign-off at the end of a text ("- John D.", "Thanks, Mary", a last line that is only a
capitalised name) is stripped before any output; texts that still end in a capitalised name are
counted and listed by review_id so the agent can check them.
Fewer than 5 reviews → the step is skipped with a reason.
Reviews (CM-057, which amends CM-027's first bullet): a fact 3+ different reviewers report, with nothing conflicting,
is customer_reported — Known for the evidence gate, stated only as customers describe it, never as the company's own
claim; prices, timelines and warranty terms only as a cited customer example. Reviewer names never appear: reviews.csv
carries a one-way reviewer_key (a hash), only so the same reviewer is never counted twice. Owner replies never count.
The pull is checked against Google's displayed count; a gap is flagged.
"""
import argparse
import csv
import hashlib
import json
import re
import time

import dfs
import run as R
import status as S
from lib import client_dir, die, now, read_json, write_json

POST = "business_data/google/reviews/task_post"


def out_dir(slug):
    d = client_dir(slug) / "data" / "reviews"
    (d / "raw").mkdir(parents=True, exist_ok=True)
    return d


def review_items(res):
    """The review items in a task result. DataforSEO labels them "google_review" or (seen 2026-10)
    "google_reviews_search"; anything carrying a review_id is a review."""
    return [i for i in (res.get("items") or [])
            if str(i.get("type", "google_review")).startswith("google_review") or "review_id" in i]


NAME_TOKEN = r"(?:[A-Z][a-z'’\-]+|[A-Z]\.?)"
NAME = rf"{NAME_TOKEN}(?:\s+{NAME_TOKEN}){{0,2}}"
THANKS = r"(?:thanks|thank you|many thanks|thanks again|cheers|regards|best|best regards|kind regards|" \
         r"warm regards|sincerely|respectfully|thx|god bless|blessings)"
# capitalised words that end a review without being a name
NOT_NAMES = {"highly", "recommended", "recommend", "great", "thanks", "thank", "you", "excellent", "awesome",
             "amazing", "five", "stars", "star", "best", "service", "services", "work", "job", "company", "team",
             "again", "very", "happy", "satisfied", "customer", "customers", "perfect", "outstanding", "wonderful",
             "fantastic", "good", "nice", "a", "i", "we", "the", "and", "definitely", "will", "use", "hire",
             "roof", "roofing", "plumbing", "hvac", "google", "facebook", "yelp", "bbb", "usa", "ok", "okay",
             "love", "loved", "it", "them", "him", "her", "us", "god", "bless", "lord", "jesus", "christmas",
             "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "january", "february",
             "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
             "thanksgiving", "easter"}


def _is_name(txt, extra=()):
    toks = re.findall(r"[A-Za-z'’\-]+\.?", txt)
    stop = NOT_NAMES | {w.lower() for e in extra for w in re.findall(r"[A-Za-z]+", e)}
    return bool(toks) and re.fullmatch(NAME, txt.strip().rstrip(".!")) is not None \
        and not any(t.rstrip(".").lower() in stop for t in toks)


def strip_signoff(text, cities=()):
    """(text without a trailing sign-off, stripped?, still ends in a capitalised name?).
    Strips: a last line that is "- Name" / "Thanks, Name" / only a capitalised name (1-3 words); or the same
    after the final sentence of a one-line text ("Great job! - John D.", "... done. Thanks, Mary")."""
    t = (text or "").strip()
    stripped = False
    lines = [l for l in t.splitlines()]
    while len([l for l in lines if l.strip()]) > 1:
        last = lines[-1].strip()
        if not last:
            lines.pop(); continue
        m = re.fullmatch(rf"(?:[-–—~]+\s*|(?i:{THANKS})[,!.]?\s*(?:[-–—]\s*)?)?({NAME})\.?", last)
        if m and _is_name(m.group(1), cities):
            lines.pop(); stripped = True
            continue
        break
    t = "\n".join(lines).strip()
    m = re.search(rf"(?<=[.!?)])\s*(?:[-–—~]+\s*|(?i:{THANKS})[,!.]?\s+(?:[-–—]\s*)?)({NAME})\.?\s*$", t)
    if m and _is_name(m.group(1), cities):
        t, stripped = t[: m.start()].strip(), True
    m = re.search(r"\s[-–—~]+\s*(" + NAME + r")\.?\s*$", t)   # "great work - John" with no full stop
    if m and _is_name(m.group(1), cities):
        t, stripped = t[: m.start()].strip(), True
    tail = re.search(rf"(?<![.!?]\s)(?<=\s)({NAME})[.!]?\s*$", t)
    flagged = bool(tail and _is_name(tail.group(1), cities))
    return t, stripped, flagged


def clean_items(items, cities=()):
    """[(item, cleaned text)], number stripped, review_ids flagged."""
    out, n_stripped, flagged = [], 0, []
    for it in items:
        txt, st_, fl = strip_signoff(it.get("review_text") or "", cities)
        n_stripped += st_
        if fl:
            flagged.append(it.get("review_id"))
        out.append((it, txt))
    return out, n_stripped, flagged


THEMES = {
    "responsive / on time": ["quick", "fast", "prompt", "responsive", "on time", "same day", "next day",
                             "right away", "promptly", "showed up", "timely"],
    "price / value / estimate": ["price", "affordable", "fair", "cost", "quote", "estimate", "reasonable",
                                 "value", "budget", "cheaper", "expensive"],
    "communication": ["communicat", "explained", "kept us informed", "kept me informed", "answered",
                      "updates", "responsive to", "followed up", "follow up"],
    "professional / courteous": ["professional", "courteous", "respectful", "polite", "friendly", "kind"],
    "clean-up": ["clean", "mess", "tidy", "debris", "nails"],
    "quality of work": ["quality", "workmanship", "great job", "excellent work", "beautiful", "looks great",
                        "attention to detail", "thorough"],
    "honest / trustworthy": ["honest", "trust", "integrity", "upfront", "transparent"],
    "recommend": ["recommend"],
    "insurance / claims": ["insurance", "claim", "adjuster"],
    "storm / leak / emergency": ["storm", "emergency", "leak", "hail", "wind", "tree fell", "water damage"],
    "warranty / guarantee": ["warranty", "guarantee"],
    "complaint words": ["never", "late", "rude", "disappointed", "worst", "terrible", "unprofessional",
                        "still waiting", "no show", "didn't", "did not", "wouldn't"],
}


def write_summary(d, slug, cleaned, rating, count, services, cities, n_stripped, flagged):
    """reviews-summary.md — what agents read instead of the raw export: counts only, no names, no quotes."""
    st = S.load(slug)
    texts = [t for _, t in cleaned if t]
    low = [t.lower() for t in texts]
    stars = {}
    for it, _ in cleaned:
        v = (it.get("rating") or {}).get("value")
        stars[v] = stars.get(v, 0) + 1
    dates = sorted((it.get("timestamp") or "")[:10] for it, _ in cleaned if it.get("timestamp"))
    replied = sum(1 for it, _ in cleaned if it.get("owner_answer"))
    themes = {k: sum(1 for t in low if any(w in t for w in ws)) for k, ws in THEMES.items()}
    lines = [f"# {st['client']['name']} - Reviews summary", "",
             f"Made by scripts/reviews.py from the saved Google reviews ({now()[:10]}). No reviewer names, no "
             "quotes — counts only. Reviews are not verified facts (CM-027). The customers' wording is in "
             "customer-language.md.", "",
             f"- Google rating: {rating} from {count} reviews (DataforSEO Business Data)",
             f"- Reviews pulled: {len(cleaned)} (newest first), {len(texts)} with text"
             + (f", dated {dates[0]} to {dates[-1]}" if dates else ""),
             f"- Owner replied to: {replied}",
             f"- Reviewer sign-offs removed from the text: {n_stripped}; texts still ending in a capitalised name "
             f"(check them): {len(flagged)}", "",
             "## Rating distribution", "", "| Stars | Reviews |", "|---|---|"]
    for k in sorted(stars, key=lambda x: -(x or 0)):
        lines.append(f"| {k if k is not None else 'no rating'} | {stars[k]} |")
    lines += ["", "## Themes (reviews mentioning each)", "", "| Theme | Reviews |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(themes.items(), key=lambda x: -x[1]) if v] or ["| (none) | 0 |"]
    lines += ["", "## Services mentioned", "", "| Service | Reviews |", "|---|---|"]
    svc = {s_: sum(1 for t in low if s_ in t) for s_ in services if s_}
    lines += [f"| {k} | {v} |" for k, v in sorted(svc.items(), key=lambda x: -x[1]) if v] or ["| (none) | 0 |"]
    lines += ["", "## Places mentioned", "", "| Place | Reviews |", "|---|---|"]
    plc = {c: sum(1 for t in low if c.lower() in t) for c in cities}
    lines += [f"| {k} | {v} |" for k, v in sorted(plc.items(), key=lambda x: -x[1]) if v] or ["| (none) | 0 |"]
    qn = sum(1 for t in texts if re.search(r"[^.!?]*\?", t))
    lines += ["", f"Reviews containing a question: {qn}.", ""]
    (d / "reviews-summary.md").write_text("\n".join(lines))


def write_customer_language(d, slug, items, rating, count, services, cities):
    """customer-language.md — the customers' own words, no reviewer names. Never verified facts
    (CM-027): nothing here enters Brand Guide Section D unless the client confirms it."""
    st = S.load(slug)
    texts = [t for _, t in items if t]   # items: [(item, text with the sign-off stripped)]
    questions = [q.strip() for t in texts for q in re.findall(r"[^.!?]*\?", t) if len(q.split()) > 2]
    svc = {s_: sum(1 for t in texts if s_ in t.lower()) for s_ in services}
    plc = {c: sum(1 for t in texts if c.lower() in t.lower()) for c in cities}
    openers = []
    for t in texts:
        first = re.split(r"(?<=[.!?])\s", t)[0].strip()
        if 4 <= len(first.split()) <= 30:
            openers.append(first)
    lines = [f"# {st['client']['name']} - Customer Language", "",
             f"From {len(texts)} Google review texts (newest first) · rating {rating} from {count} reviews · "
             f"pulled {now()[:10]} by scripts/reviews.py.", "",
             "**Rules (CM-027):** reviewer names are removed and never used in a deliverable. These are the "
             "customers' words, not verified facts — nothing here enters Brand Guide Section D unless the "
             "client confirms it on the proof sheet. Use for headings, FAQ wording and Section I.", "",
             "## Questions customers asked", ""]
    lines += [f"- \"{q}\"" for q in dict.fromkeys(questions)] or ["- (none in the review text)"]
    lines += ["", "## Services mentioned (reviews mentioning each)", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(svc.items(), key=lambda x: -x[1]) if v] or ["- (no services file given, or none mentioned)"]
    lines += ["", "## Places mentioned", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(plc.items(), key=lambda x: -x[1]) if v] or ["- (no cities given, or none mentioned)"]
    lines += ["", "## How customers describe the work (first sentence of each review)", ""]
    lines += [f"- \"{o}\"" for o in openers[:60]] or ["- (none)"]
    lines += ["", "## Agent notes", "", "The discovery-audit agent adds themes and the words customers use for "
              "problems and symptoms here — quoted, never attributed to a person.", ""]
    (d / "customer-language.md").write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("estimate"); s.add_argument("slug"); s.add_argument("--depth", type=int, default=200)
    s = sub.add_parser("run"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--keyword", required=True); s.add_argument("--location", required=True)
    s.add_argument("--depth", type=int, default=200); s.add_argument("--confirmed", action="store_true")
    s.add_argument("--max-wait", type=int, default=540)
    s.add_argument("--services-file"); s.add_argument("--cities", default="")
    s = sub.add_parser("summarize"); s.add_argument("slug")
    s.add_argument("--services-file"); s.add_argument("--cities", default="")
    s = sub.add_parser("extract"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s = sub.add_parser("meaning"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--confirmed", action="store_true")
    s = sub.add_parser("checked"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--key", required=True, help="the candidate's key, e.g. fact:service_scope or practice:photos")
    s.add_argument("--count", type=int, required=True, help="different reviewers left after dropping false matches")
    s.add_argument("--note", default="")
    a = ap.parse_args()
    if a.cmd == "meaning":
        R.open_run(a.slug, a.run)
        meaning(a.slug, a.run, a.confirmed)
        return
    if a.cmd == "checked":   # the researcher has read the matches by meaning (Paul 2026-10-09)
        R.open_run(a.slug, a.run)
        mark_checked(a.slug, a.run, a.key, a.count, a.note, "researcher")
        print(f"{a.key}: checked by meaning — {a.count} reviewer(s)"
              + (" → counts as Known (CM-057)" if a.count >= 3 else " → below 3, stays a yes/no line"))
        return
    if a.cmd == "extract":
        R.open_run(a.slug, a.run)
        found, strong, need = extract(a.slug, a.run)
        print(f"{len(found)} fact(s)/topic(s) found in the reviews · {strong} reported by {need}+ different reviewers "
              "(customer_reported) · customer-language.md 'Facts customers report' and facts.json section R updated")
        return
    if a.cmd == "summarize":
        raw = out_dir(a.slug) / "raw" / "reviews.json"
        if not raw.exists():
            die(f"No saved reviews for {a.slug} (clients/{a.slug}/data/reviews/raw/reviews.json). "
                "Run 'reviews.py run' first.", 4)
        process(a.slug, json.loads(raw.read_text()), a.services_file, a.cities)
        return
    depth = max(10, min(a.depth, 200))
    est = dfs.estimate(POST, tasks=1, depth=depth)

    if a.cmd == "estimate":
        print(f"Google reviews, newest first, up to {depth}: at most ${est:.4f} "
              f"(billed per 10 reviews actually returned) · balance ${dfs.balance():.2f}")
        return

    R.open_run(a.slug, a.run)
    d = out_dir(a.slug)
    state_f = d / "raw" / "task.json"
    task = read_json(state_f, {})
    if not task.get("id"):
        resp = dfs.paid_post(a.slug, POST, [{"keyword": a.keyword, "location_name": a.location,
                                             "language_code": "en", "depth": depth, "sort_by": "newest"}],
                             f"Google reviews for '{a.keyword}' ({a.location}), newest {depth}", est, a.confirmed)
        t = dfs.task_result(resp)
        task = {"id": t["id"], "posted": now(), "keyword": a.keyword, "location": a.location}
        write_json(state_f, task)
        R.log_change(a.slug, a.run, "data_pull", a.keyword, "reviews task", "", t["id"], "POSTED", channel="local")

    start, res = time.time(), None
    while time.time() - start < a.max_wait:
        try:
            r = dfs.request(f"business_data/google/reviews/task_get/{task['id']}", method="GET")
            t = (r.get("tasks") or [{}])[0]
            if t.get("status_code") == 20000 and t.get("result"):
                res = t["result"][0]
                break
        except dfs.DfsError:
            pass
        time.sleep(20)
    if res is None:
        print("STILL QUEUED — run the same command again (the task is saved; no new charge).")
        raise SystemExit(10)
    (d / "raw" / "reviews.json").write_text(json.dumps(res))
    process(a.slug, res, a.services_file, a.cities)


def process(slug, res, services_file=None, cities_arg=""):
    """Every output from one saved reviews result: reviews.csv, mentions.csv, customer-language.md,
    reviews-summary.md (all without reviewer names or sign-offs) and the rating evidence."""
    d = out_dir(slug)
    items = review_items(res)
    rating = (res.get("rating") or {}).get("value")
    count = res.get("reviews_count")
    st = S.load(slug)
    st.setdefault("evidence", {})["google_rating"] = {"rating": rating, "reviews_count": count,
                                                       "checked": now()[:10], "source": "DataforSEO Business Data"}
    S.save(slug, st)

    services = [l.strip().lower() for l in open(services_file) if l.strip()] if services_file else []
    cities = [c.strip() for c in (cities_arg or "").split(",") if c.strip()]
    cleaned, n_stripped, flagged = clean_items(items, cities)
    with open(d / "reviews.csv", "w", newline="") as fh, open(d / "mentions.csv", "w", newline="") as mh:
        w = csv.writer(fh); w.writerow(["review_id", "date", "rating", "text", "owner_replied", "reviewer_key"])
        m = csv.writer(mh); m.writerow(["review_id", "date", "services_mentioned", "places_mentioned", "questions"])
        for it, text in cleaned:
            rid, date = it.get("review_id"), (it.get("timestamp") or "")[:10]
            who = str(it.get("profile_url") or it.get("profile_name") or rid)
            w.writerow([rid, date, (it.get("rating") or {}).get("value"), text, bool(it.get("owner_answer")),
                        hashlib.sha256(who.encode()).hexdigest()[:10]])   # a hash, never the name
            low = text.lower()
            m.writerow([rid, date,
                        "; ".join(s_ for s_ in services if s_ and s_ in low),
                        "; ".join(c for c in cities if c.lower() in low),
                        " | ".join(q.strip() for q in re.findall(r"[^.!?]*\?", text))])
    write_customer_language(d, slug, cleaned, rating, count, services, cities)
    write_summary(d, slug, cleaned, rating, count, services, cities, n_stripped, flagged)
    summary = (f"rating {rating} from {count} Google reviews · pulled {len(items)} (newest first) · "
               f"no reviewer names in reviews.csv / mentions.csv · {n_stripped} reviewer sign-off(s) stripped · "
               f"{len(flagged)} text(s) still end in a capitalised name"
               + (f" (check: {', '.join(str(x) for x in flagged[:10])}{' …' if len(flagged) > 10 else ''})"
                  if flagged else "")
               + " · agents read reviews-summary.md")
    gap = (count or 0) - len(items)
    if gap > 0:   # P5: the pull is checked against the count Google shows
        print(f"PULL INCOMPLETE — Google shows {count} reviews, {len(items)} were pulled ({gap} missing"
              + (", the 200-review cap" if len(items) >= 200 else "") + "). Facts in the missing reviews are not seen.")
    st = S.load(slug)
    st["evidence"]["google_rating"]["pulled"] = len(items)
    S.save(slug, st)
    print(summary)
    if (count or 0) < 5:
        print("SKIP — fewer than 5 reviews; record S06 as skipped with this reason.")


# ------------------------------------------------------------------ CM-057: facts customers report
TOPICS = {
    "practice:photos": [r"\bphotos?\b|\bpictures?\b"],
    "practice:clean-up": [r"\bclean(ed|ing)?[- ]?up\b|\bclean\b|\btidy\b|\bmagnet\b|\bdebris\b"],
    "practice:permits": [r"\bpermits?\b"],
    "practice:explains": [r"\bexplain(ed|s)?\b|\bwalked (us|me) through\b"],
    "prices ($ amounts)": [r"\$\s?\d[\d,]*(\.\d\d)?\s?(k\b)?"],
    "materials": [r"\bshingles?\b|\bmetal\b|\bslate\b|\bunderlayment\b|\bflashing\b|\bgutters?\b|\bskylights?\b|\btile\b"],
}


def _rows(slug):
    p = out_dir(slug) / "reviews.csv"
    if not p.exists():
        die(f"no reviews.csv for {slug} — pull the reviews first (reviews.py run / summarize)", 4)
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def extract(slug, run_id, write=True):
    """{fact or topic: {count, quotes[{date, quote, row}]}} — counted by different reviewers (CM-057).
    write=False: only the matches (each with every hit, `_hits`), nothing written — for the meaning check."""
    import facts
    import sources
    reqs = read_json(sources.REQ) or {}
    need = int(reqs.get("review_min_independent") or 3)
    rows = _rows(slug)
    docs = [{"kind": "review", "text": r.get("text") or "", "date": r.get("date", ""),
             "reviewer": r.get("reviewer_key") or r.get("review_id") or f"row{i}", "label": f"reviews.csv row {i}"}
            for i, r in enumerate(rows, 2)]
    st = S.load(slug)
    found = {}

    def add(key, label, hits):
        people = {h["reviewer"] for h in hits}
        if people:
            found[key] = {"label": label, "count": len(people),
                          "quotes": [{"date": h["date"], "quote": h["quote"], "row": h["label"]} for h in hits[:8]],
                          "_hits": hits}

    for key in (reqs.get("find") or {}):
        res = sources.search(slug, key, {}, docs, limit=None)
        add(f"fact:{key}", key.replace("_", " "), res["hits"])
    for key, pats in TOPICS.items():
        rx = [re.compile(x, re.I) for x in pats]
        hits = []
        for d_ in docs:
            for sent in sources.SENT.split(d_["text"]):
                if any(r.search(sent) for r in rx):
                    hits.append({"reviewer": d_["reviewer"], "date": d_["date"], "label": d_["label"],
                                 "quote": sent.strip()[:220]})
                    break
        add(key, key.split(":")[-1].replace("-", " ") if ":" in key else key, hits)
    cities = sorted({p.get("city") for p in st["pages"].values() if p.get("city")})
    for c in cities:
        hits = [{"reviewer": d_["reviewer"], "date": d_["date"], "label": d_["label"],
                 "quote": next(x for x in sources.SENT.split(d_["text"]) if c.lower() in x.lower()).strip()[:220]}
                for d_ in docs if c.lower() in d_["text"].lower()]
        add(f"place:{c}", c, hits)
    # people: a capitalised first name in 3+ different reviews that is not a place, a brand word or a sentence start
    names = {}
    skip = {c.lower() for c in cities} | NOT_NAMES | {w.lower() for w in str(st["client"].get("name", "")).split()}
    skip |= {w for d_ in docs for w in re.findall(r"\b[a-z][a-z]{2,}\b", d_["text"])}   # also in lower case: not a name
    brand = re.sub(r"[^a-z]", "", str(st["client"].get("name", "")).lower())
    skip |= {w.lower() for d_ in docs for w in re.findall(r"\b[A-Z][a-z]{2,}\b", d_["text"]) if w.lower() in brand}
    for d_ in docs:
        for m in re.finditer(r"\b([A-Z][a-z]{2,})\b", d_["text"]):
            w = m.group(1)
            if w.lower() not in skip:
                names.setdefault(w, {})[d_["reviewer"]] = d_
    for w, by in names.items():
        if len(by) >= need:
            add(f"staff:{w}", f"person named {w}", [{"reviewer": r, "date": d_["date"], "label": d_["label"],
                 "quote": next((x for x in sources.SENT.split(d_["text"]) if w in x), "").strip()[:220]}
                for r, d_ in by.items()])
    if not write:
        return found, need
    for f in found.values():
        f.pop("_hits", None)
    d = out_dir(slug)
    write_json(d / "review-facts.json", {"made": now(), "min_reviewers": need, "facts": found})
    # customer-language.md: the "Facts customers report" table (replaced each time)
    cl = d / "customer-language.md"
    text = cl.read_text() if cl.exists() else f"# {st['client']['name']} - Customer Language\n"
    text = re.sub(r"\n## Facts customers report.*?(?=\n## |\Z)", "", text, flags=re.S)
    tbl = ["", "## Facts customers report (CM-057)", "",
           f"Counted by different reviewers. {need}+ = customer_reported: Known for the evidence gate, stated only as "
           "customers describe it (\"customers mention…\"). Prices, timelines and warranty terms only as a cited customer "
           "example, never as the company's. No reviewer names.", "",
           "| Fact | Reviewers | Example (date) |", "|---|---|---|"]
    for key, f in sorted(found.items(), key=lambda kv: -kv[1]["count"]):
        q = f["quotes"][0]
        tbl.append(f"| {f['label']} | {f['count']}{' ✓' if f['count'] >= need else ''} | \"{q['quote'].replace('|', '/')}\" "
                   f"({q['date']}) |")
    cl.write_text(text.rstrip("\n") + "\n" + "\n".join(tbl) + "\n")
    # facts.json: customer_reported candidates in section R (never a Brand Guide row, so no approval changes)
    data = facts.load(slug)
    rows_ = [r for r in data["facts"] if r.get("section") != "R"]
    for key, f in found.items():
        rows_.append({"id": "r-" + re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-"), "section": "R", "key": key,
                      "label": f["label"], "value": "; ".join(f"\"{q['quote']}\" ({q['date']})" for q in f["quotes"][:3]),
                      "status": "customer_reported", "status_text": None, "source": f"Google reviews ({f['count']} "
                      "different reviewers; data/reviews/review-facts.json)", "quote": f["quotes"][0]["quote"],
                      "date": now()[:10], "who": "reviews.py extract", "count": f["count"]})
    facts.save(slug, rows_)
    strong = sum(1 for f in found.values() if f["count"] >= need)
    from lib import append
    append(client_dir(slug) / "log.md", f"- REVIEW FACTS {now()[:16]} · run {run_id} · {len(found)} fact(s)/topic(s) found "
           f"in reviews, {strong} with {need}+ different reviewers (customer_reported, CM-057) · data/reviews/review-facts.json\n")
    return found, strong, need


# ------------------------------------------------------------------ CM-057 by meaning, on the Claude API (Phase 2)
def mark_checked(slug, run_id, key, count, note, who):
    """The same record `reviews.py checked` writes: the candidate read by meaning, N different reviewers left."""
    import facts
    from lib import append
    data = facts.load(slug)
    row = next((r for r in data["facts"] if r.get("section") == "R" and r.get("key") == key), None)
    if not row:   # a page-level fact (its terms name the page's service or city)
        row = {"id": "r-" + re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-"), "section": "R", "key": key,
               "label": key.split(":", 1)[-1].replace("_", " "), "value": note, "status": "customer_reported",
               "status_text": None, "source": "Google reviews (read by meaning; data/reviews/reviews.csv)",
               "quote": "", "date": now()[:10], "who": who, "count": count}
        data["facts"].append(row)
    row.update({"meaning_checked": True, "count": count, "checked_at": now(), "checked_note": note, "who": who})
    facts.save(slug, data["facts"])
    append(client_dir(slug) / "log.md", f"- REVIEW FACT CHECKED {now()[:16]} · run {run_id} · {key}: "
           f"{count} different reviewer(s) after reading by meaning ({who})" + (f" · {note}" if note else "") + "\n")


def meaning(slug, run_id, confirmed=False):
    """Every keyword match read by meaning in one llm.py review-meaning job (Sonnet): the sentences that state the
    fact are kept, the reviewers behind them counted (3+ = Known, CM-057). No key: the researcher reads them
    (`reviews.py checked`), as before."""
    import llm
    found, need = extract(slug, run_id, write=False)
    sid, items = {}, []
    for key, f in sorted(found.items()):
        sents = []
        for n, h in enumerate(f["_hits"], 1):
            i = f"{len(sid) + 1}"
            sid[i] = (key, h["reviewer"])
            sents.append({"sentence_id": i, "text": h["quote"]})
        items.append({"id": key, "label": f["label"], "sentences": sents})
    if not items:
        print("no review matches to read by meaning")
        return
    ans = llm.attempt(slug, run_id, "review-meaning", {"rule": "CM-057: 3+ different reviewers = customer_reported"},
                      items, f"review facts by meaning ({len(items)} fact(s))",
                      "the researcher reads each match by meaning (reviews.py checked)", confirmed)
    if ans is None:
        return
    who = f"llm.py review-meaning ({llm.JOBS['review-meaning']['model']})"
    strong = 0
    for key, a in sorted(ans.items()):
        people = {sid[x][1] for x in a.get("stating") or [] if x in sid and sid[x][0] == key}
        mark_checked(slug, run_id, key, len(people), (a.get("note") or "")[:200], who)
        strong += len(people) >= need
    left = len(items) - len(ans)
    R.log_change(slug, run_id, "llm_judgment", "data/reviews", "review facts by meaning", "",
                 f"{len(ans)} read, {strong} with {need}+ reviewers", "DONE", channel="local")
    print(f"{len(ans)} review fact(s) read by meaning on the Claude API · {strong} reported by {need}+ different "
          "reviewers (customer_reported)" + (f" · {left} not answered — the researcher reads them" if left else ""))


if __name__ == "__main__":
    main()
