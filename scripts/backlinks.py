#!/usr/bin/env python3
"""backlinks.py — S08 backlinks: a compact per-URL summary of the saved raw DataforSEO backlinks exports.
Agents read the summary, never the raw export (R5).

    backlinks.py summary <slug> [--input F.json ...]

The pull itself is a paid call through dfs.py, saved into the client's git-ignored raw folder:
    dfs.py call <slug> backlinks/backlinks/live --payload p.json --purpose "S08 backlinks" \
        --out clients/<slug>/data/backlinks/raw/backlinks-<date>.json
Without --input every *.json in clients/<slug>/data/backlinks/raw/ is read. Understood shapes (the full
response, or just its result): backlinks/backlinks (one row per link: url_to, domain_from),
backlinks/domain_pages (page + page_summary), bulk_pages_summary (url + counts) and
backlinks/referring_domains (the target's referring domains). Where a source gives counts and a link list
for the same URL, the larger figure is kept.

Writes clients/<slug>/data/backlinks/backlinks-per-url.csv:
    url, referring_domains, backlinks, top_referring_domains (up to 3, most links first, "; "-separated)
Standard library only; no DataforSEO call, no cost.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

from lib import client_dir, die


def results(doc):
    """The result objects in a saved response (or a bare result / list of results)."""
    if isinstance(doc, list):
        for x in doc:
            yield from results(x)
    elif isinstance(doc, dict):
        if "tasks" in doc:
            for t in doc.get("tasks") or []:
                yield from results(t.get("result") or [])
        else:
            yield doc


def summarize(docs):
    """{url: {"rd": set(domains), "bl": int, "dom": {domain: links}, "rd_n": int, "bl_n": int}}"""
    urls = {}

    def u(url):
        return urls.setdefault(url, {"rd": set(), "bl": 0, "dom": {}, "rd_n": 0, "bl_n": 0})

    for doc in docs:
        for res in results(doc):
            target = res.get("target") or ""
            for it in res.get("items") or []:
                if not isinstance(it, dict):
                    continue
                if it.get("url_to") and it.get("domain_from"):           # backlinks/backlinks: one row per link
                    r = u(it["url_to"]); dom = it["domain_from"]
                    r["rd"].add(dom); r["bl"] += 1; r["dom"][dom] = r["dom"].get(dom, 0) + 1
                elif it.get("page") and isinstance(it.get("page_summary"), dict):   # domain_pages
                    ps, r = it["page_summary"], u(it["page"])
                    r["rd_n"] = max(r["rd_n"], int(ps.get("referring_domains") or 0))
                    r["bl_n"] = max(r["bl_n"], int(ps.get("backlinks") or 0))
                elif it.get("url") and ("referring_domains" in it or "backlinks" in it):   # bulk_pages_summary
                    r = u(it["url"])
                    r["rd_n"] = max(r["rd_n"], int(it.get("referring_domains") or 0))
                    r["bl_n"] = max(r["bl_n"], int(it.get("backlinks") or 0))
                elif it.get("domain") and target:                      # referring_domains of the target
                    r = u(target); dom = it["domain"]; n = int(it.get("backlinks") or 1)
                    r["rd"].add(dom); r["dom"][dom] = max(r["dom"].get(dom, 0), n)
                    r["bl_n"] = max(r["bl_n"], sum(r["dom"].values()))
    return urls


def rows(urls):
    out = []
    for url, r in urls.items():
        top = sorted(r["dom"].items(), key=lambda x: (-x[1], x[0]))[:3]
        out.append([url, max(len(r["rd"]), r["rd_n"]), max(r["bl"], r["bl_n"]), "; ".join(d for d, _ in top)])
    return sorted(out, key=lambda x: (-x[1], -x[2], x[0]))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("summary"); s.add_argument("slug"); s.add_argument("--input", nargs="*")
    a = ap.parse_args()
    d = client_dir(a.slug) / "data" / "backlinks"
    files = [Path(f) for f in a.input] if a.input else sorted((d / "raw").glob("*.json"))
    if not files:
        die(f"No saved backlinks export for {a.slug}. Pull it with dfs.py call ... --out "
            f"clients/{a.slug}/data/backlinks/raw/backlinks-<date>.json, then run this again.", 4)
    docs = []
    for f in files:
        try:
            docs.append(json.loads(f.read_text()))
        except (OSError, ValueError) as e:
            die(f"Could not read {f}: {e}")
    table = rows(summarize(docs))
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "backlinks-per-url.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["url", "referring_domains", "backlinks", "top_referring_domains"])
        w.writerows(table)
    print(f"{len(files)} saved export(s) → {len(table)} URL(s) with backlinks · "
          f"clients/{a.slug}/data/backlinks/backlinks-per-url.csv (agents read this, not the raw export)")


if __name__ == "__main__":
    sys.exit(main())
