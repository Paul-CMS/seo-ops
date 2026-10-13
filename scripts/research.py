#!/usr/bin/env python3
"""research.py — the research log (CM-061 part 2; rewrite 3 §4.2). No lazy way out: "not found" is valid only with a
log entry showing the queries and sources tried, at or above the minimum effort.

    research.py log <slug> --run R --section S --gap KEY --kind public|client [--page P]
                    --queries "q1 || q2 || q3" --sources "s1 || s2" --result found|partial|not_found
                    [--excerpt "…" --url U]                       one entry per gap → build/<S>/research-log.csv
    research.py todo <slug> (--all | --batch B)                   gaps still needing research before they may be asked
    research.py check <slug>                                      every not_found entry meets the minimum (exit 4)
    research.py show <slug> <entry id>                            one entry

KEY is the gap's facts key (evidence.py fact_key: fact:d:<fact> or fact:<page>:<key>). Minimum before "not found"
(methodology/definitions.md, "Searched"):
  public  the area source list for the place (methodology/sources/…), at least 3 distinct web queries — one naming the
          official body (town, city, county, state, board, department …) — and the place's Wikipedia/Wikidata entry
  client  every source in the search order (facts.json, decisions-settled.md, the evidence pack, the proof sheet, the
          Discovery Record), plus the client's site search, plus the client's GBP Q&A and GBP posts
The scripts refuse what falls short: this one refuses to log it; evidence.py refuses a page facts file that says "not
found" without a valid entry; the facts round asks no client fact without one; review.py refuses an Ask (kind 3)
that does not link one.
"""
import argparse
import csv
import re
import sys

from lib import ROOT, append, client_dir, die, now, today

COLS = ["id", "page", "gap", "kind", "queries", "sources_tried", "result", "excerpt", "url", "date", "run"]
CLIENT_MIN = {"facts.json": "facts.json", "decisions-settled": "decisions-settled.md", "evidence pack": "the evidence pack",
              "proof sheet": "the proof sheet", "discovery record": "the Discovery Record", "site search": "the client's site search",
              "gbp q&a": "the GBP Q&A", "gbp posts": "the GBP posts"}
OFFICIAL = re.compile(r"\b(town|city|county|state|board|department|dept|council|commission|agency|bureau|office|"
                      r"llr|\.gov|government|official|code|permit office|building official)\b", re.I)
SPLIT = re.compile(r"\s*\|\|\s*")


def _split(v):
    return [x.strip() for x in SPLIT.split(v or "") if x.strip()]


def path(slug, section):
    return client_dir(slug) / "build" / section / "research-log.csv"


def entries(slug):
    """Every log row of every section."""
    out = []
    for p in sorted((client_dir(slug) / "build").glob("*/research-log.csv")):
        with open(p, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                r["_section"] = p.parent.name
                out.append(r)
    return out


def problems(row):
    """[why] — what keeps an entry from meeting the minimum (empty = valid)."""
    res, kind = row.get("result"), row.get("kind")
    qs, srcs = _split(row.get("queries")), _split(row.get("sources_tried"))
    low = " ".join(srcs).lower()
    why = []
    if kind not in ("public", "client"):
        why.append("kind must be public or client")
    if res not in ("found", "partial", "not_found"):
        why.append("result must be found, partial or not_found")
    if res in ("found", "partial"):
        if not (row.get("excerpt") or "").strip():
            why.append("a found/partial result quotes its excerpt")
        if kind == "public" and not (row.get("url") or "").strip():
            why.append("a public result names its URL")
        return why
    if kind == "public":
        if "methodology/sources/" not in low:
            why.append("the area source list (methodology/sources/<state>-<area>.md) was not tried")
        if len({q.lower() for q in qs}) < 3:
            why.append(f"{len(set(q.lower() for q in qs))} distinct web quer(ies) — at least 3")
        if not any(OFFICIAL.search(q) for q in qs):
            why.append("no query names the official body (town, city, county, state, board …)")
        if "wikipedia" not in low and "wikidata" not in low:
            why.append("the place's Wikipedia/Wikidata entry was not tried")
    elif kind == "client":
        miss = [label for tok, label in CLIENT_MIN.items() if tok not in low]
        if miss:
            why.append("not tried yet: " + ", ".join(miss))
    return why


def find(slug, gap, results=("not_found",)):
    """The newest valid entry for a gap with one of these results, or None."""
    rows = [r for r in entries(slug) if r.get("gap") == gap and r.get("result") in results and not problems(r)]
    return rows[-1] if rows else None


def log(slug, run_id, section, gap, kind, page, queries, sources, result, excerpt="", url=""):
    row = {"page": page or "*", "gap": gap, "kind": kind, "queries": " || ".join(_split(queries)),
           "sources_tried": " || ".join(_split(sources)), "result": result, "excerpt": (excerpt or "").strip(),
           "url": (url or "").strip(), "date": today(), "run": run_id}
    bad = problems(row)
    if bad:
        die(f"REFUSED — research-log entry for {gap} ({kind}, {result}) is below the minimum (CM-061):\n  - "
            + "\n  - ".join(bad), 4)
    p = path(slug, section)
    p.parent.mkdir(parents=True, exist_ok=True)
    new = not p.is_file()
    n = 0 if new else sum(1 for _ in open(p, encoding="utf-8")) - 1
    row["id"] = f"RL-{section}-{n + 1}"
    with open(p, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in COLS})
    append(client_dir(slug) / "log.md", f"- RESEARCH {now()[:16]} · run {run_id} · {row['id']} · {gap} ({kind}): {result}\n")
    return row["id"]


def todo(slug, pids):
    """[(page, fact_key, label, kind, what is missing)] — gaps (Unknown in the grid) that research must still cover
    before they may be asked (client) or left out (public)."""
    import evidence
    import status as S
    st = S.load(slug)
    reqs = evidence.requirements()
    public = set(reqs.get("public_facts") or []) | set((reqs.get("verify_by_lookup") or {}).keys())
    out, seen = [], set()
    for pid in pids:
        rows, *_ = evidence.grid(slug, st, pid)
        for r in rows:
            if r["mark"] != "Unknown" or r["fact_key"] in seen:
                continue
            seen.add(r["fact_key"])
            kind = "public" if r["from"] in public else "client"
            if find(slug, r["fact_key"], ("not_found", "found", "partial")):
                continue
            out.append((pid, r["fact_key"], r["label"], kind))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("log"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--section", required=True); s.add_argument("--gap", required=True)
    s.add_argument("--kind", required=True, choices=["public", "client"]); s.add_argument("--page")
    s.add_argument("--queries", default=""); s.add_argument("--sources", required=True)
    s.add_argument("--result", required=True, choices=["found", "partial", "not_found"])
    s.add_argument("--excerpt", default=""); s.add_argument("--url", default="")
    s = sub.add_parser("todo"); s.add_argument("slug")
    g = s.add_mutually_exclusive_group(required=True); g.add_argument("--all", action="store_true"); g.add_argument("--batch")
    s = sub.add_parser("check"); s.add_argument("slug")
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("id")
    a = ap.parse_args()
    if a.cmd == "log":
        import run as R
        R.open_run(a.slug, a.run)
        print(log(a.slug, a.run, a.section, a.gap, a.kind, a.page, a.queries, a.sources, a.result, a.excerpt, a.url))
    elif a.cmd == "todo":
        import status as S
        st = S.load(a.slug)
        pids = ([p for b in S.batches(st) for p in b["pages"]] if a.all else (S.batch(st, a.batch) or die(f"no batch {a.batch}"))["pages"])
        rows = todo(a.slug, pids)
        for pid, k, label, kind in rows:
            print(f"{kind:7} {k:45} {label}  ({pid})")
        print(f"{len(rows)} gap(s) still need research (research.py log) before they may be asked or left out" if rows
              else "every gap has a research-log entry")
    elif a.cmd == "check":
        bad = [(r["id"], problems(r)) for r in entries(a.slug) if r.get("result") == "not_found" and problems(r)]
        for i, w in bad:
            print(f"{i}: " + "; ".join(w))
        print("every not_found meets the minimum" if not bad else f"{len(bad)} entr(ies) below the minimum")
        sys.exit(4 if bad else 0)
    elif a.cmd == "show":
        r = next((r for r in entries(a.slug) if r.get("id") == a.id), None) or die(f"no entry {a.id}")
        for k in COLS:
            print(f"{k:14} {r.get(k, '')}")
        w = problems(r)
        print("valid" if not w else "BELOW THE MINIMUM: " + "; ".join(w))


if __name__ == "__main__":
    main()
