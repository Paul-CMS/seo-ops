#!/usr/bin/env python3
"""paa.py — add-on 4b: People Also Ask questions for core services × cities. Discovery step,
before the site plan.

    paa.py estimate <slug> --services-file F --cities "Spring Hill,Franklin,..." --state Tennessee [--cap 20]
    paa.py run      <slug> --run R --services-file F --cities ... --state ... [--cap 20] [--confirmed]
                    [--registry c3.txt]

Queries are "<service> <city>" for each core service × the primary city plus the top 3
service-area cities (the order given in --cities; the first is the primary city). The run is
capped at --cap queries (default 20); expanding beyond the cap needs Paul's OK.
Outputs in clients/<slug>/data/paa/ (raw/ git-ignored):
  paa-questions.csv   question, source queries, times seen, closest C3 match + similarity
  queries.csv         every query run and how many PAA questions it returned
  paa-routing.md      the routing worksheet: Intent and Route columns are filled by the
                      discovery-audit agent (a judgment, not a script); C3 duplicates pre-marked drop
"""
import argparse
import csv
import json
import re
from difflib import SequenceMatcher

import dfs
import run as R
from lib import client_dir

SERP = "serp/google/organic/live/advanced"


def norm(q):
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()


def queries(services, cities):
    """Primary city first for every service, then the other cities — so a cap keeps full
    coverage of the primary city before spreading out."""
    return [f"{s} {c}" for c in cities for s in services]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("estimate", "run"):
        s = sub.add_parser(n); s.add_argument("slug"); s.add_argument("--services-file", required=True)
        s.add_argument("--cities", required=True); s.add_argument("--state", required=True)
        s.add_argument("--cap", type=int, default=20)
        if n == "run":
            s.add_argument("--run", required=True); s.add_argument("--confirmed", action="store_true")
            s.add_argument("--registry")
    a = ap.parse_args()
    services = [l.strip().lower() for l in open(a.services_file) if l.strip()]
    cities = [c.strip() for c in a.cities.split(",") if c.strip()][:4]
    qs = queries(services, cities)
    run_qs = qs[: a.cap]
    each = dfs.estimate(SERP, tasks=1, depth=10)

    if a.cmd == "estimate":
        print(f"{len(services)} services × {len(cities)} cities = {len(qs)} queries; capped at {a.cap} "
              f"→ {len(run_qs)} queries × ${each:.4f} = ${each * len(run_qs):.4f} "
              f"(all {len(qs)} would be ${each * len(qs):.4f}) · balance ${dfs.balance():.2f}")
        if len(qs) > a.cap:
            print(f"Not run: {len(qs) - a.cap} queries beyond the cap — expanding needs Paul's OK.")
        return

    R.open_run(a.slug, a.run)
    d = client_dir(a.slug) / "data" / "paa"
    (d / "raw").mkdir(parents=True, exist_ok=True)
    seen, qlog = {}, []
    for q in run_qs:
        city = next((c for c in cities if q.endswith(c.lower()) or q.endswith(c)), cities[0])
        resp = dfs.paid_post(a.slug, SERP, [{"keyword": q, "location_name": f"{city},{a.state},United States",
                                             "language_code": "en", "depth": 10, "device": "desktop"}],
                             f"PAA for '{q}'", each, a.confirmed)
        res = (dfs.task_result(resp).get("result") or [{}])[0]
        (d / "raw" / (re.sub(r"[^a-z0-9]+", "-", q.lower()) + ".json")).write_text(json.dumps(res))
        n = 0
        for it in res.get("items") or []:
            if it.get("type") != "people_also_ask":
                continue
            for el in it.get("items") or []:
                t = (el.get("title") or "").strip()
                if not t:
                    continue
                k = norm(t)
                seen.setdefault(k, {"question": t, "queries": [], "count": 0})
                seen[k]["queries"].append(q); seen[k]["count"] += 1; n += 1
        qlog.append([q, n])

    reg = [l.strip() for l in open(a.registry)] if a.registry else []
    with open(d / "paa-questions.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["question", "source_queries", "times_seen", "closest_existing_heading_or_faq", "similarity"])
        for v in sorted(seen.values(), key=lambda v: -v["count"]):
            best, score = "", 0.0
            for r in reg:
                sc = SequenceMatcher(None, norm(v["question"]), norm(r)).ratio()
                if sc > score:
                    best, score = r, sc
            w.writerow([v["question"], " | ".join(dict.fromkeys(v["queries"])), v["count"], best, f"{score:.2f}"])
    rows = []
    for v in sorted(seen.values(), key=lambda v: -v["count"]):
        best, score = "", 0.0
        for r in reg:
            sc = SequenceMatcher(None, norm(v["question"]), norm(r)).ratio()
            if sc > score:
                best, score = r, sc
        rows.append((v, best, score))
    md = ["# PAA routing — People Also Ask questions", "",
          f"{len(run_qs)} queries ({', '.join(cities)}) → {len(seen)} distinct questions (deduplicated). "
          "Written by scripts/paa.py; **the discovery-audit agent fills Intent and Route** for every row.", "",
          "Intent: informational · problem-aware · commercial investigation · comparison · transactional.  ",
          "Route: **service FAQ** (name the page) · **location FAQ** (name the city page) · **blog topic** · **drop** "
          "(off-topic, or already in the C3 registry — similarity ≥ 0.85 is pre-marked).", "",
          "| # | Question | Seen | Source queries | Closest C3 heading/FAQ | Similarity | Intent | Route | Note |",
          "|---|---|---|---|---|---|---|---|---|"]
    for i, (v, best, score) in enumerate(rows, 1):
        route = "drop (C3 duplicate)" if score >= 0.85 else ""
        md.append(f"| {i} | {v['question']} | {v['count']} | {' / '.join(dict.fromkeys(v['queries']))} | "
                  f"{best} | {score:.2f} | | {route} | |")
    (d / "paa-routing.md").write_text("\n".join(md) + "\n")
    with open(d / "queries.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["query", "paa_questions"]); w.writerows(qlog)
    R.log_change(a.slug, a.run, "data_pull", ",".join(cities), "PAA", "", f"{len(run_qs)} queries, {len(seen)} questions",
                 "DONE", channel="local")
    print(f"{len(run_qs)} queries → {len(seen)} distinct PAA questions "
          f"({sum(1 for v in seen.values() if v['count'] > 1)} seen on more than one query)")
    if len(qs) > a.cap:
        print(f"{len(qs) - a.cap} queries beyond the cap were not run — ask Paul before expanding.")


if __name__ == "__main__":
    main()
