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
                      discovery-audit agent (a judgment, not a script); C3 duplicates pre-marked drop.
                      A re-run keeps the Intent / Route / Note already filled in, matched by question
                      text (lowercase, collapsed spaces, end punctuation ignored); routed questions that
                      no longer appear are listed at the bottom so nothing the agent wrote is lost.
"""
import argparse
import csv
import json
import re
import time
from difflib import SequenceMatcher

import dfs
import run as R
from lib import client_dir

SERP = "serp/google/organic/live/advanced"


def norm(q):
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()


def key(q):
    """Routing match key: lowercase, collapsed whitespace, punctuation at the end stripped."""
    return re.sub(r"\s+", " ", q.lower()).strip().rstrip("?.!,;:…\"' ").strip()


def cell(x):
    return str(x).replace("|", "/").replace("\n", " ").strip()


def old_routing(path):
    """{key(question): (question, intent, route, note)} from an earlier paa-routing.md — the table rows and
    the 'routed earlier, not seen in this run' list."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cells) == 9 and cells[0].isdigit():
            q, intent, route, note = cells[1], cells[6], cells[7], cells[8]
        else:
            m = re.match(r"^- (.+?) — Intent: (.*?) · Route: (.*?) · Note: (.*)$", line)
            if not m:
                continue
            q, intent, route, note = (g.strip() for g in m.groups())
        if intent or note or (route and route != "drop (C3 duplicate)"):
            out[key(q)] = (q, intent, route, note)
    return out


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
        # default: primary + top 3 cities (audit-steps S19); more only when Paul asks for them
        s.add_argument("--max-cities", type=int, default=4)
        # towns DataforSEO has no location for are searched from a nearby one: "Okatie=Bluffton;Levy=Beaufort"
        s.add_argument("--search-from", default="")
        if n == "run":
            s.add_argument("--run", required=True); s.add_argument("--confirmed", action="store_true")
            s.add_argument("--registry")
    a = ap.parse_args()
    services = [l.strip().lower() for l in open(a.services_file) if l.strip()]
    cities = [c.strip() for c in a.cities.split(",") if c.strip()][: a.max_cities]
    search_from = dict(p.split("=", 1) for p in a.search_from.split(";") if "=" in p)
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
    dfs.run_guard(a.slug, each * len(run_qs), a.confirmed, f"People Also Ask ({len(run_qs)} queries)")
    d = client_dir(a.slug) / "data" / "paa"
    (d / "raw").mkdir(parents=True, exist_ok=True)
    seen, qlog = {}, []
    for q in run_qs:
        city = next((c for c in cities if q.endswith(c.lower()) or q.endswith(c)), cities[0])
        raw = d / "raw" / (re.sub(r"[^a-z0-9]+", "-", q.lower()) + ".json")
        if raw.exists():                 # saved by an earlier, interrupted run: reuse, never pay twice
            res = json.loads(raw.read_text())
        else:
            res = None
            for attempt in (1, 2):       # one retry on DataforSEO's temporary errors (e.g. 40101)
                loc = search_from.get(city, city)
                resp = dfs.paid_post(a.slug, SERP, [{"keyword": q, "location_name": f"{loc},{a.state},United States",
                                                     "language_code": "en", "depth": 10, "device": "desktop"}],
                                     f"PAA for '{q}'", each, a.confirmed)
                try:
                    res = (dfs.task_result(resp).get("result") or [{}])[0]
                    break
                except dfs.DfsError as e:
                    if attempt == 2 or "Invalid Field" in str(e):
                        raise SystemExit(f"STOP — '{q}': {e}. Saved queries are reused on the next run.")
                    time.sleep(10)
            raw.write_text(json.dumps(res))
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
    prev = old_routing(d / "paa-routing.md")
    kept = 0
    for i, (v, best, score) in enumerate(rows, 1):
        route = "drop (C3 duplicate)" if score >= 0.85 else ""
        intent = note = ""
        old = prev.pop(key(v["question"]), None)
        if old:
            kept += 1
            intent, route, note = old[1], old[2] or route, old[3]
        md.append(f"| {i} | {cell(v['question'])} | {v['count']} | {' / '.join(dict.fromkeys(v['queries']))} | "
                  f"{cell(best)} | {score:.2f} | {intent} | {route} | {note} |")
    if prev:
        md += ["", "## Routed earlier, not seen in this run", "",
               "Kept so the routing is not lost; these questions did not come back from the queries above.", ""]
        md += [f"- {q} — Intent: {i_} · Route: {r_} · Note: {n_}" for q, i_, r_, n_ in prev.values()]
    (d / "paa-routing.md").write_text("\n".join(md) + "\n")
    with open(d / "queries.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["query", "paa_questions"]); w.writerows(qlog)
    R.log_change(a.slug, a.run, "data_pull", ",".join(cities), "PAA", "", f"{len(run_qs)} queries, {len(seen)} questions",
                 "DONE", channel="local")
    print(f"{len(run_qs)} queries → {len(seen)} distinct PAA questions "
          f"({sum(1 for v in seen.values() if v['count'] > 1)} seen on more than one query)"
          + (f" · routing kept for {kept} question(s) from the earlier worksheet" if kept else "")
          + (f" · {len(prev)} routed question(s) not seen this time, listed at the bottom" if prev else ""))
    if len(qs) > a.cap:
        print(f"{len(qs) - a.cap} queries beyond the cap were not run — ask Paul before expanding.")


if __name__ == "__main__":
    main()
