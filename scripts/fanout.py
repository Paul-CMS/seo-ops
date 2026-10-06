#!/usr/bin/env python3
"""fanout.py — S21 query fan-out (CM-045). Discovery step, while the client has the proof sheet,
alongside People Also Ask (S19). Feeds the site plan's coverage check and the Blog Decision Map.

    fanout.py estimate <slug> --services-file F --cities "Gettysburg,Hanover,..." [--per-seed 40] [--cap 10]
    fanout.py run      <slug> --run R --services-file F --cities ... [--per-seed 40] [--cap 10] [--confirmed]
                       [--registry c3.txt] [--paa clients/<slug>/data/paa/paa-questions.csv]

What it is: for each seed ("<service> <city>", primary city first, capped at --cap seeds) one
DataforSEO AI Optimization call (ai_optimization/chat_gpt/llm_responses/live) asks an LLM for the
--per-seed searches a local customer might type around that seed — informational, cost, how-to,
comparison and local. The answers are deduplicated across seeds and checked against the PAA
questions and the C3 heading/FAQ registry.

What it is NOT: search demand. The queries are an LLM's brainstorm, not observed searches; they have
no volume and never count as evidence for CM-019/CM-020/CM-021. They are candidates for coverage:
a question a page or a post should answer. Never cite a volume for one (CM-012).

Outputs in clients/<slug>/data/fanout/ (raw/ git-ignored):
  fanout-queries.csv   query, seeds, times seen, also in PAA?, closest C3 match + similarity
  fanout-routing.md    the routing worksheet: Intent and Route filled by the discovery-audit agent
                       (service H2/FAQ · location FAQ · blog topic · drop); C3 and PAA duplicates pre-marked
Cost: whole-run estimate first (dfs.run_guard: balance, $2 threshold). Price (dfs_prices.json, checked
2026-10-05): $0.0006 per task + gpt-4.1-mini tokens — at most ~$0.0072 a call, ~$0.07 for the default
10 seeds. 180 s timeout, no retry (a retry after a timeout could bill twice).
"""
import argparse
import csv
import json
import re
from difflib import SequenceMatcher

import dfs
import run as R
from lib import client_dir

LLM = "ai_optimization/chat_gpt/llm_responses/live"
MODEL = "gpt-4.1-mini"
SYSTEM = ("You list the searches real local customers type into Google. Reply with only a JSON array of "
          "lowercase search queries, no commentary.")


def norm(q):
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()


def seeds(services, cities):
    return [f"{s} {c}" for c in cities for s in services]


def prompt(seed, n):
    p = (f"List {n} different Google searches a homeowner near the place in '{seed}' might type before or while "
         "hiring for it: questions, costs, how-to, comparisons, signs and causes, local. Mostly under 8 words.")
    return p[:500]   # the endpoint caps the prompt at 500 characters


def texts(node):
    """Every string under a 'text' key, anywhere in the response."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "text" and isinstance(v, str):
                yield v
            else:
                yield from texts(v)
    elif isinstance(node, list):
        for v in node:
            yield from texts(v)


def parse(res):
    """Queries from the model's answer: a JSON array if there is one, else one per line."""
    out = []
    for t in texts(res):
        m = re.search(r"\[.*\]", t, re.S)
        try:
            arr = json.loads(m.group(0)) if m else None
        except ValueError:
            arr = None
        if isinstance(arr, list):
            out += [str(x) for x in arr if isinstance(x, (str, int))]
        else:
            out += [re.sub(r"^[\s\-*\d.)\"]+|[\",]+$", "", l) for l in t.splitlines()]
    return [q.strip().lower() for q in out if 2 <= len(q.strip().split()) <= 14]


def best_match(q, pool):
    best, score = "", 0.0
    for r in pool:
        sc = SequenceMatcher(None, norm(q), norm(r)).ratio()
        if sc > score:
            best, score = r, sc
    return best, score


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("estimate", "run"):
        s = sub.add_parser(n); s.add_argument("slug"); s.add_argument("--services-file", required=True)
        s.add_argument("--cities", required=True); s.add_argument("--per-seed", type=int, default=40)
        s.add_argument("--cap", type=int, default=10)
        if n == "run":
            s.add_argument("--run", required=True); s.add_argument("--confirmed", action="store_true")
            s.add_argument("--registry"); s.add_argument("--paa")
    a = ap.parse_args()
    services = [l.strip().lower() for l in open(a.services_file) if l.strip()]
    cities = [c.strip() for c in a.cities.split(",") if c.strip()][:4]
    all_seeds = seeds(services, cities)
    run_seeds = all_seeds[: a.cap]
    each = dfs.estimate(LLM, tasks=1)

    if a.cmd == "estimate":
        print(f"{len(all_seeds)} seeds; capped at {a.cap} → {len(run_seeds)} calls × ${each:.4f} (upper bound) "
              f"= ${each * len(run_seeds):.4f} · balance ${dfs.balance():.2f}")
        if len(all_seeds) > a.cap:
            print(f"Not run: {len(all_seeds) - a.cap} seeds beyond the cap — expanding needs Paul's OK.")
        return

    R.open_run(a.slug, a.run)
    dfs.run_guard(a.slug, each * len(run_seeds), a.confirmed, f"query fan-out ({len(run_seeds)} seeds)")
    d = client_dir(a.slug) / "data" / "fanout"
    (d / "raw").mkdir(parents=True, exist_ok=True)
    seen, qlog = {}, []
    for seed in run_seeds:
        payload = [{"user_prompt": prompt(seed, a.per_seed), "model_name": MODEL, "system_message": SYSTEM,
                    "max_output_tokens": 4096, "temperature": 0.9, "web_search": False}]
        resp = dfs.paid_post(a.slug, LLM, payload, f"query fan-out for '{seed}'", each, a.confirmed,
                             timeout=180, retries=1)
        res = (dfs.task_result(resp).get("result") or [{}])[0]
        (d / "raw" / (re.sub(r"[^a-z0-9]+", "-", seed.lower()) + ".json")).write_text(json.dumps(res))
        qs = list(dict.fromkeys(parse(res)))
        for q in qs:
            seen.setdefault(norm(q), {"query": q, "seeds": [], "count": 0})
            seen[norm(q)]["seeds"].append(seed); seen[norm(q)]["count"] += 1
        qlog.append([seed, len(qs)])

    reg = [l.strip() for l in open(a.registry)] if a.registry else []
    paa = [r["question"] for r in csv.DictReader(open(a.paa))] if a.paa else []
    rows = []
    for v in sorted(seen.values(), key=lambda v: (-v["count"], v["query"])):
        c3, c3s = best_match(v["query"], reg)
        pq, pqs = best_match(v["query"], paa)
        rows.append((v, c3, c3s, pq, pqs))
    with open(d / "fanout-queries.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["query", "seeds", "times_seen", "closest_paa_question", "paa_similarity",
                    "closest_existing_heading_or_faq", "c3_similarity"])
        for v, c3, c3s, pq, pqs in rows:
            w.writerow([v["query"], " | ".join(dict.fromkeys(v["seeds"])), v["count"], pq, f"{pqs:.2f}", c3, f"{c3s:.2f}"])
    md = ["# Fan-out routing — LLM query fan-out (S21)", "",
          f"{len(run_seeds)} seeds → {len(seen)} distinct queries. Written by scripts/fanout.py; **the discovery-audit "
          "agent fills Intent and Route** for every row.", "",
          "**These are an LLM's brainstorm of likely searches, not observed demand.** No volume, never evidence for a "
          "destructive or superlative decision (CM-019, CM-020, CM-021), never cited with a number (CM-012). Use them "
          "to check coverage: every kept row is answered by a page (H2 or FAQ) or a blog topic.", "",
          "Intent: informational · problem-aware · commercial investigation · comparison · transactional.  ",
          "Route: **service H2/FAQ** (name the page) · **location FAQ** (name the city page) · **blog topic** · **drop** "
          "(off-topic, or already covered — C3 or PAA similarity ≥ 0.85 is pre-marked).", "",
          "| # | Query | Seen | Seeds | Closest PAA question | PAA sim | Closest C3 | C3 sim | Intent | Route | Note |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, (v, c3, c3s, pq, pqs) in enumerate(rows, 1):
        route = "drop (C3 duplicate)" if c3s >= 0.85 else ("same as PAA — route with it" if pqs >= 0.85 else "")
        md.append(f"| {i} | {v['query']} | {v['count']} | {' / '.join(dict.fromkeys(v['seeds']))} | {pq} | {pqs:.2f} | "
                  f"{c3} | {c3s:.2f} | | {route} | |")
    (d / "fanout-routing.md").write_text("\n".join(md) + "\n")
    with open(d / "seeds.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["seed", "queries"]); w.writerows(qlog)
    R.log_change(a.slug, a.run, "data_pull", ",".join(cities), "fan-out", "",
                 f"{len(run_seeds)} seeds, {len(seen)} queries", "DONE", channel="local")
    print(f"{len(run_seeds)} seeds → {len(seen)} distinct fan-out queries "
          f"({sum(1 for r in rows if r[4] >= 0.85)} overlap PAA, {sum(1 for r in rows if r[2] >= 0.85)} already in C3)")
    if len(all_seeds) > a.cap:
        print(f"{len(all_seeds) - a.cap} seeds beyond the cap were not run — ask Paul before expanding.")


if __name__ == "__main__":
    main()
