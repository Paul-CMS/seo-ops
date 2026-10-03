#!/usr/bin/env python3
"""rankings.py — add-on 4a: every keyword the domain ranks for (top 100), cannibalization,
and "best" search volumes for the "The Best" test (CM-020). Audit step: Pass 1 inventory.

    rankings.py estimate <slug> --services-file F [--cities "Spring Hill,Franklin"] [--state Tennessee]
    rankings.py run      <slug> --run R --services-file F [--cities ...] [--state ...]
                         [--max-keywords 3000] [--confirmed]

services-file: one core service per line (e.g. "roof repair").
Outputs in clients/<slug>/data/rankings/ (raw/ is git-ignored):
  ranked-keywords.csv   keyword, volume, url, position, type
  url-rankings.csv      per URL: keywords in top 100, best position, total volume   (CM-019 evidence)
  cannibalization.csv   one row per conflict cluster: query, volume, every URL + position
  best-variants.csv     "best [service] [city]" and "best [service] near me" volumes (CM-020)
  rankings-summary.md   counts, top clusters, top keywords, cost
DataforSEO Labs is country-level only, so rankings are for the United States market.
"""
import argparse
import csv
import json
from collections import defaultdict

import dfs
import run as R
import status as S
from lib import client_dir, die, now, write_json

LABS = "dataforseo_labs/google/ranked_keywords/live"
VOL = "keywords_data/google_ads/search_volume/live"


US_STATES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}


def state_name_abbr(state):
    """('South Carolina', 'SC') from a full name or abbreviation, any case. ('', '') if blank."""
    if not state:
        return "", ""
    s_ = state.strip()
    for name, ab in US_STATES.items():
        if s_.lower() in (name.lower(), ab.lower()):
            return name, ab
    die(f"Unknown US state '{state}'. Use the full name or the two-letter code.")


def out_dir(slug):
    d = client_dir(slug) / "data" / "rankings"
    (d / "raw").mkdir(parents=True, exist_ok=True)
    return d


def best_keywords(services, cities, state_abbr):
    kws = []
    for s in services:
        kws.append(f"best {s} near me")
        for c in cities:
            kws.append(f"best {s} {c.lower()} {state_abbr.lower()}".strip())
    return [k for k in dict.fromkeys(kws) if len(k) <= 80 and len(k.split()) <= 10]


def plan(st, services, cities, state, max_kw):
    domain = st["client"]["domain"].replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
    pages = max(1, -(-max_kw // 1000))
    est_labs = dfs.estimate(LABS, tasks=pages, items=max_kw)
    _, abbr = state_name_abbr(state)
    kws = best_keywords(services, cities, abbr)
    est_vol = dfs.estimate(VOL, tasks=max(1, -(-len(kws) // 1000)))
    return domain, pages, est_labs, kws, est_vol


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("estimate", "run"):
        s = sub.add_parser(n); s.add_argument("slug"); s.add_argument("--services-file", required=True)
        s.add_argument("--cities", default=""); s.add_argument("--state", default="")
        s.add_argument("--max-keywords", type=int, default=3000)
        if n == "run":
            s.add_argument("--run", required=True); s.add_argument("--confirmed", action="store_true")
    a = ap.parse_args()
    st = S.load(a.slug)
    services = [l.strip().lower() for l in open(a.services_file) if l.strip()]
    cities = [c.strip() for c in a.cities.split(",") if c.strip()]
    domain, pages, est_labs, kws, est_vol = plan(st, services, cities, a.state, a.max_keywords)

    if a.cmd == "estimate":
        _, labs_ok = dfs.price(LABS)
        print(f"Ranked keywords for {domain} (United States): up to {pages} call(s), "
              f"up to {a.max_keywords} rows → at most ${est_labs:.4f}"
              + ("" if labs_ok else "  [price NOT confirmed — needs Paul's OK]"))
        print(f"'best' variants: {len(kws)} keywords in {max(1, -(-len(kws) // 1000))} task(s), "
              f"location {a.state or 'United States'} → ${est_vol:.4f}")
        print(f"Total at most ${est_labs + est_vol:.4f} · balance ${dfs.balance():.2f}")
        return

    R.open_run(a.slug, a.run)
    dfs.run_guard(a.slug, est_labs + (est_vol if kws else 0), a.confirmed, "the rankings pull")
    d = out_dir(a.slug)
    rows, offset = [], 0
    for i in range(pages):
        resp = dfs.paid_post(a.slug, LABS, [{
            "target": domain, "location_name": "United States", "language_code": "en",
            "limit": 1000, "offset": offset, "load_rank_absolute": True,
            "item_types": ["organic", "local_pack", "featured_snippet"],
            "order_by": ["keyword_data.keyword_info.search_volume,desc"]}],
            f"ranked keywords {domain} page {i + 1}", dfs.estimate(LABS, 1, 1000), a.confirmed)
        res = (dfs.task_result(resp).get("result") or [{}])[0]
        (d / "raw" / f"ranked-{i + 1}.json").write_text(json.dumps(res))
        items = res.get("items") or []
        for it in items:
            kd = it.get("keyword_data") or {}
            se = ((it.get("ranked_serp_element") or {}).get("serp_item")) or {}
            rows.append({"keyword": kd.get("keyword"),
                         "volume": (kd.get("keyword_info") or {}).get("search_volume") or 0,
                         "url": se.get("url"), "position": se.get("rank_group") or it.get("rank_group"),
                         "type": se.get("type")})
        offset += len(items)
        total = res.get("total_count") or 0
        if len(items) < 1000 or offset >= total:
            break
    with open(d / "ranked-keywords.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["keyword", "volume", "url", "position", "type"])
        w.writeheader(); w.writerows(rows)

    per_url = defaultdict(lambda: {"keywords": 0, "best": 999, "volume": 0})
    by_kw = defaultdict(list)
    for r in rows:
        u = per_url[r["url"]]
        u["keywords"] += 1; u["volume"] += r["volume"] or 0
        u["best"] = min(u["best"], r["position"] or 999)
        by_kw[r["keyword"]].append(r)
    with open(d / "url-rankings.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["url", "keywords_top100", "best_position", "total_volume"])
        for url, v in sorted(per_url.items(), key=lambda x: -x[1]["volume"]):
            w.writerow([url, v["keywords"], v["best"], v["volume"]])

    clusters = [(k, rs) for k, rs in by_kw.items() if len({r["url"] for r in rs}) >= 2]
    clusters.sort(key=lambda x: -(x[1][0]["volume"] or 0))
    with open(d / "cannibalization.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["cluster_id", "query", "volume", "urls_and_positions"])
        for i, (k, rs) in enumerate(clusters, 1):
            w.writerow([f"CAN-{i:03d}", k, rs[0]["volume"],
                        " | ".join(f"{r['url']} (#{r['position']})" for r in sorted(rs, key=lambda r: r["position"] or 999))])

    vol_rows = []
    if kws:
        loc = f"{state_name_abbr(a.state)[0]},United States" if a.state else "United States"
        resp = dfs.paid_post(a.slug, VOL, [{"keywords": kws, "location_name": loc, "language_code": "en"}],
                             f"'best' variant volumes ({len(kws)} keywords, {loc})", est_vol, a.confirmed)
        res = dfs.task_result(resp).get("result") or []
        (d / "raw" / "best-variants.json").write_text(json.dumps(res))
        for it in res:
            vol_rows.append([it.get("keyword"), it.get("search_volume"), it.get("competition")])
        with open(d / "best-variants.csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["keyword", "search_volume", "competition"]); w.writerows(vol_rows)

    summary = [f"# Rankings — {st['client']['name']} — {now()[:10]}", "",
               f"- Domain: {domain} · market: United States (DataforSEO Labs is country-level)",
               f"- Keyword/URL rows in the top 100: **{len(rows)}** · distinct keywords {len(by_kw)} · "
               f"ranking URLs {len(per_url)}",
               f"- Cannibalization clusters (2+ URLs on one query): **{len(clusters)}**",
               f"- 'best' variants checked: {len(vol_rows)} · with measurable volume: "
               f"{sum(1 for v in vol_rows if (v[1] or 0) > 0)}", "",
               "## Top 10 cannibalization clusters (by volume)", "",
               "| Cluster | Query | Volume | URLs (position) |", "|---|---|---|---|"]
    for i, (k, rs) in enumerate(clusters[:10], 1):
        summary.append(f"| CAN-{i:03d} | {k} | {rs[0]['volume']} | "
                       + "<br>".join(f"{r['url']} (#{r['position']})" for r in rs) + " |")
    summary += ["", "## Top 15 keywords by volume", "", "| Keyword | Volume | URL | Position |", "|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: -(r["volume"] or 0))[:15]:
        summary.append(f"| {r['keyword']} | {r['volume']} | {r['url']} | {r['position']} |")
    summary += ["", "## 'best' variants with volume", "", "| Keyword | Volume |", "|---|---|"]
    for v in sorted(vol_rows, key=lambda v: -(v[1] or 0)):
        if (v[1] or 0) > 0:
            summary.append(f"| {v[0]} | {v[1]} |")
    (d / "rankings-summary.md").write_text("\n".join(summary) + "\n")
    R.log_change(a.slug, a.run, "data_pull", domain, "rankings", "", f"{len(rows)} rows, {len(clusters)} clusters",
                 "DONE", channel="local")
    print("\n".join(summary[:8]))


if __name__ == "__main__":
    main()
