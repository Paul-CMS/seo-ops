#!/usr/bin/env python3
"""paa.py — add-on 4b: People Also Ask questions for core services × cities. Discovery step,
before the site plan.

    paa.py estimate <slug> --services-file F --cities "Spring Hill,Franklin,..." --state Tennessee [--cap 20]
    paa.py run      <slug> --run R --services-file F --cities ... --state ... [--cap 20] [--confirmed]
                    [--registry c3.txt]
    paa.py route    <slug> --run R [--confirmed]   fill every empty Intent / Route / Note (llm.py route-questions)

Queries are "<service> <city>" for each core service × the primary city plus the top 3
service-area cities (the order given in --cities; the first is the primary city). The run is
capped at --cap queries (default 20); expanding beyond the cap needs Paul's OK.
Outputs in clients/<slug>/data/paa/ (raw/ git-ignored):
  paa-questions.csv   question, source queries, times seen, closest C3 match + similarity
  queries.csv         every query run and how many PAA questions it returned
  paa-routing.md      the routing worksheet: Intent and Route are filled by `paa.py route` (llm.py
                      route-questions, Haiku — Rewrite 4 Phase 2); with no API key the discovery-audit agent fills
                      them as before. C3 duplicates pre-marked drop.
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
from lib import client_dir, now

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


LLM_LINE = "Intent and Route filled by scripts/llm.py"


def planned_pages(slug):
    """[{name, type, url (path)}] for the service, location and hub pages on record — what a route may name."""
    import urllib.parse
    import status as S
    out = []
    for pid, p in S.load(slug)["pages"].items():
        if p.get("type") in ("service", "location", "county") and p.get("url"):
            path = urllib.parse.urlparse(p["url"]).path or "/"
            out.append({"name": p.get("name") or pid, "type": p["type"], "url": path})
    return out


def route_worksheet(slug, run_id, path, service_label, confirmed=False):
    """Fill the empty Intent / Route / Note cells of a routing worksheet (paa-routing.md, fanout-routing.md) with one
    llm.py route-questions job (Rewrite 4 Phase 2). A filled cell — the agent's, Paul's, a pre-marked drop — is never
    overwritten. No key: nothing is written and the agent fills them as before."""
    import llm
    from lib import die as _die
    if not path.exists():
        _die(f"no {path.name} for {slug} — run the pull first", 4)
    lines = path.read_text().splitlines()
    hi = next((i for i, l in enumerate(lines) if l.startswith("|") and "| Intent |" in l and "| Route |" in l), None)
    if hi is None:
        _die(f"{path.name} has no table with Intent and Route columns", 4)
    head = [c.strip() for c in lines[hi].strip().strip("|").split("|")]
    col = {h: i for i, h in enumerate(head)}
    qcol = "Question" if "Question" in col else "Query"
    rows = {}
    for i in range(hi + 2, len(lines)):
        if not lines[i].startswith("|"):
            break
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if len(cells) == len(head) and cells[0].isdigit():
            rows[cells[0]] = (i, cells)
    todo = [(n, c) for n, (i, c) in rows.items() if not c[col["Route"]] and not c[col["Intent"]]]
    pages = planned_pages(slug)
    def get(c, *names):
        return next((c[col[x]] for x in names if x in col), "")
    items = [{"id": n, "question": c[col[qcol]], "seen": get(c, "Seen"), "group": get(c, "Group"),
              "source": get(c, "Seeds", "Source queries"),
              "closest_existing": get(c, "Closest C3", "Closest C3 heading/FAQ")} for n, c in todo]
    import status as S
    context = {"business": S.load(slug)["client"].get("name", ""), "pages": pages,
               "page_rule": "page is one of these URLs" if pages else
               "no pages are planned yet: page is the service name or the city name the answer belongs to"}
    if not items:
        print(f"{path.name}: every row already has an Intent or Route — nothing to route")
        return 0
    ans = llm.attempt(slug, run_id, "route-questions", context, items, f"{path.name} routing ({len(items)} row(s))",
                      f"the discovery-audit agent fills Intent and Route in {path.name}", confirmed)
    if ans is None:
        return 0
    urls = {p["url"] for p in pages}
    filled = bad = 0
    for n, (i, c) in rows.items():
        a = ans.get(n)
        if not a or (c[col["Route"]] or c[col["Intent"]]):
            continue
        page = (a.get("page") or "").strip()
        if a["route"] in ("service", "location"):
            if urls and page not in urls:
                bad += 1
                continue
            route = f"{service_label if a['route'] == 'service' else 'location FAQ'} — {page}"
        else:
            route = a["route"]
        c[col["Intent"]], c[col["Route"]] = a["intent"], route
        if "Note" in col and not c[col["Note"]]:
            c[col["Note"]] = cell(a.get("note") or "")
        lines[i] = "| " + " | ".join(c) + " |"
        filled += 1
    stamp = (f"{LLM_LINE} (route-questions, {llm.JOBS['route-questions']['model']}) for {filled} row(s), {now()[:10]}; "
             "a filled row is never overwritten — edit any row by hand.")
    lines = [l for l in lines if not l.startswith(LLM_LINE)]
    lines[1:1] = ["", stamp, ""]
    path.write_text(re.sub(r"\n{3,}", "\n\n", "\n".join(lines)) + "\n")
    R.log_change(slug, run_id, "llm_judgment", path.name, "Intent/Route", "", f"{filled} row(s) routed", "DONE",
                 channel="local")
    print(f"{path.name}: {filled} of {len(items)} row(s) routed by llm.py"
          + (f" · {bad} named a page that is not planned — left for the agent" if bad else "")
          + (f" · {len(items) - filled - bad} not answered — left for the agent" if len(items) - filled - bad > 0 else ""))
    return filled


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
    s = sub.add_parser("route"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--confirmed", action="store_true")
    a = ap.parse_args()
    if a.cmd == "route":
        R.open_run(a.slug, a.run)
        route_worksheet(a.slug, a.run, client_dir(a.slug) / "data" / "paa" / "paa-routing.md", "service FAQ", a.confirmed)
        return
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
          "Written by scripts/paa.py; Intent and Route are filled by `paa.py route` (llm.py), or by the "
          "discovery-audit agent when there is no API key.", "",
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
