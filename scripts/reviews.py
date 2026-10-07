#!/usr/bin/env python3
"""reviews.py — add-on 3: Google reviews → customer language. Discovery step (client has the sheet).

    reviews.py estimate <slug> [--depth 200]
    reviews.py run      <slug> --run R --keyword "Business Name" --location "City,State,United States"
                        [--depth 200] [--confirmed] [--max-wait 540]

Pulls the newest reviews (up to --depth, max 200 here) through DataforSEO Business Data.
Saves raw data (with reviewer names) to clients/<slug>/data/reviews/raw/ — git-ignored and
never used in a deliverable. Writes reviews.csv WITHOUT reviewer names, plus mentions.csv
(services, cities and questions spotted in each review) for the agent that writes
customer-language.md. Records rating + count for the "The Best" proof condition (CM-020).
Fewer than 5 reviews → the step is skipped with a reason.
Reviews are NOT verified facts: nothing from them enters Brand Guide Section D unless the
client confirms it on the proof sheet.
"""
import argparse
import csv
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


def write_customer_language(d, slug, items, rating, count, services, cities):
    """customer-language.md — the customers' own words, no reviewer names. Never verified facts
    (CM-027): nothing here enters Brand Guide Section D unless the client confirms it."""
    st = S.load(slug)
    texts = [(it.get("review_text") or "").strip() for it in items if (it.get("review_text") or "").strip()]
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
    a = ap.parse_args()
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

    items = review_items(res)
    rating = (res.get("rating") or {}).get("value")
    count = res.get("reviews_count")
    st = S.load(a.slug)
    st.setdefault("evidence", {})["google_rating"] = {"rating": rating, "reviews_count": count,
                                                       "checked": now()[:10], "source": "DataforSEO Business Data"}
    S.save(a.slug, st)

    services = [l.strip().lower() for l in open(a.services_file)] if a.services_file else []
    cities = [c.strip() for c in a.cities.split(",") if c.strip()]
    with open(d / "reviews.csv", "w", newline="") as fh, open(d / "mentions.csv", "w", newline="") as mh:
        w = csv.writer(fh); w.writerow(["review_id", "date", "rating", "text", "owner_replied"])
        m = csv.writer(mh); m.writerow(["review_id", "date", "services_mentioned", "places_mentioned", "questions"])
        for it in items:
            text = (it.get("review_text") or "").strip()
            rid, date = it.get("review_id"), (it.get("timestamp") or "")[:10]
            w.writerow([rid, date, (it.get("rating") or {}).get("value"), text, bool(it.get("owner_answer"))])
            low = text.lower()
            m.writerow([rid, date,
                        "; ".join(s_ for s_ in services if s_ and s_ in low),
                        "; ".join(c for c in cities if c.lower() in low),
                        " | ".join(q.strip() for q in re.findall(r"[^.!?]*\?", text))])
    write_customer_language(d, a.slug, items, rating, count, services, cities)
    summary = (f"rating {rating} from {count} Google reviews · pulled {len(items)} (newest first) · "
               f"no reviewer names in reviews.csv / mentions.csv")
    print(summary)
    if (count or 0) < 5:
        print("SKIP — fewer than 5 reviews; record S06 as skipped with this reason.")


if __name__ == "__main__":
    main()
