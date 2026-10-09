#!/usr/bin/env python3
"""competitors.py — what the top competitor pages cover, for coverage ideas only (rewrite 2 P6). Data stage.

    competitors.py estimate <slug> [--keywords-file F] [--top 3]
    competitors.py run      <slug> --run R --location "City,State,United States" [--keywords-file F] [--top 3]
                            [--confirmed]
    (also: crawl.py competitors …)

Keywords: one main keyword per service page (the site plan's `keyword`, else the service name), or --keywords-file.
For each keyword one Google SERP (DataforSEO, whole-run estimate first, over $2 → Paul), the top --top organic pages
that are not the client's own, each fetched once: its H2s, FAQ questions (headings ending in "?") and word count.
Writes clients/<slug>/data/competitors/coverage.md (and coverage.json). Used ONLY as coverage ideas in the site plan
— headings and FAQ topics a page might cover. Never a source of client claims (CM-016 unchanged); nothing on a
competitor page is a fact about the client.
"""
import argparse
import html
import json
import re
import urllib.parse

import dfs
import run as R
import status as S
from lib import client_dir, die, now, write_json

SERP = "serp/google/organic/live/advanced"


def keywords(st, file=None):
    if file:
        return [l.strip() for l in open(file) if l.strip()]
    out = []
    for p in st["pages"].values():
        if p.get("type") == "service":
            k = p.get("keyword") or p.get("service_variant") or p.get("name")
            if k and k not in out:
                out.append(k)
    return out


def summarise(body):
    def clean(t):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t or ""))).strip()
    b = re.sub(r"<(script|style|nav|footer|header)\b.*?</\1>", "", body or "", flags=re.S | re.I)
    h2 = [clean(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", b, re.S | re.I)]
    faqs = [clean(x) for x in re.findall(r"<h[2-4][^>]*>(.*?)</h[2-4]>", b, re.S | re.I) if clean(x).endswith("?")]
    words = len(clean(b).split())
    return {"h2": [x for x in h2 if x][:30], "faq": faqs[:30], "words": words}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("estimate", "run"):
        s = sub.add_parser(n); s.add_argument("slug"); s.add_argument("--keywords-file"); s.add_argument("--top", type=int, default=3)
        if n == "run":
            s.add_argument("--run", required=True); s.add_argument("--location", required=True)
            s.add_argument("--confirmed", action="store_true")
    a = ap.parse_args()
    st = S.load(a.slug)
    kws = keywords(st, a.keywords_file)
    if not kws:
        die("no service keywords — the site plan has no service pages yet (or pass --keywords-file)", 4)
    est = dfs.estimate(SERP, tasks=len(kws), depth=10)
    if a.cmd == "estimate":
        print(f"competitor coverage: {len(kws)} SERP(s) → at most ${est:.4f} · balance ${dfs.balance():.2f}")
        return
    R.open_run(a.slug, a.run)
    dfs.run_guard(a.slug, est, a.confirmed, "the competitor coverage pull")
    import crawl
    own = urllib.parse.urlparse("https://" + (st["client"].get("domain") or "").replace("https://", "")).netloc.replace("www.", "")
    rows = []
    for kw in kws:
        resp = dfs.paid_post(a.slug, SERP, [{"keyword": kw, "location_name": a.location, "language_code": "en",
                                             "depth": 10}], f"competitor SERP '{kw}'", dfs.estimate(SERP, 1, depth=10),
                             a.confirmed)
        res = (dfs.task_result(resp).get("result") or [{}])[0]
        urls = [i.get("url") for i in (res.get("items") or []) if i.get("type") == "organic" and i.get("url")
                and own not in (urllib.parse.urlparse(i["url"]).netloc or "")][:a.top]
        for u in urls:
            code, _, body = crawl.web_fetch(u)
            rows.append({"keyword": kw, "url": u, "status": code, **(summarise(body) if code == 200 else {"h2": [], "faq": [], "words": 0})})
    d = client_dir(a.slug) / "data" / "competitors"
    d.mkdir(parents=True, exist_ok=True)
    write_json(d / "coverage.json", {"made": now(), "location": a.location, "pages": rows})
    lines = [f"# {st['client']['name']} - Competitor coverage", "",
             f"Made by scripts/competitors.py ({now()[:10]}, {a.location}). **Coverage ideas only** — headings and FAQ "
             "topics a page might cover. Nothing here is a fact about the client (CM-016).", ""]
    for kw in kws:
        mine = [r for r in rows if r["keyword"] == kw]
        lines += [f"## {kw}", ""]
        for r in mine:
            lines += [f"- {r['url']} — {r['words']} words" + ("" if r["status"] == 200 else f" (answered {r['status']})")]
            if r["h2"]:
                lines.append("  - H2s: " + " · ".join(r["h2"][:12]))
            if r["faq"]:
                lines.append("  - FAQ topics: " + " · ".join(r["faq"][:12]))
        lines.append("" if mine else "- (no competitor pages found)\n")
    (d / "coverage.md").write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} competitor page(s) for {len(kws)} keyword(s) → clients/{a.slug}/data/competitors/coverage.md "
          "(coverage ideas only, never client claims)")


if __name__ == "__main__":
    main()
