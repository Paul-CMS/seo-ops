#!/usr/bin/env python3
"""conformance.py — score every spec check that needs no judgment (rewrite 2 P12: mechanical checks off Opus).

    conformance.py <slug> [--crawl-date YYYY-MM-DD]

Reads the crawl tables (inputs/crawl/*internal_all*, *h1_all*, *h2_all*), the page-text capture
(data/crawl/page-text.csv, if any), the site plan / page register (status.json pages) and facts.json (brand name,
phone). Which checks are auto is listed in methodology/specs/check-kinds.json; every other check is judgment and is
left for the audit agent. Writes clients/<slug>/audit/conformance.csv (page, type, check, result PASS|FAIL|N/A,
detail) and conformance.md (a summary per page type). Free, offline, deterministic.
"""
import csv
import json
import re
import sys
import urllib.parse

import status as S
import urlcheck
from lib import ROOT, client_dir, now, read_json

KINDS = ROOT / "methodology" / "specs" / "check-kinds.json"


def table(slug, name):
    d = client_dir(slug) / "inputs" / "crawl"
    hits = sorted(d.glob(f"* - DFS - {name} - *.csv")) if d.exists() else []
    if not hits:
        return {}
    with open(hits[-1], newline="", encoding="utf-8-sig") as fh:
        return {r["Address"]: r for r in csv.DictReader(fh)}


def norm_url(u):
    p = urllib.parse.urlparse(u or "")
    return (p.netloc.replace("www.", "") + "/" + p.path.strip("/")).rstrip("/").lower()


def run(slug):
    import facts
    st = S.load(slug)
    fx = {r["id"]: r for r in facts.load(slug)["facts"]}
    brand = (fx.get("a-brand-entity-gbp-name-exactly") or {}).get("value", "").split(" — ")[0].strip() \
        or st["client"].get("name", "")
    phone = re.sub(r"\D", "", (fx.get("a-phone") or {}).get("value", ""))[:10]
    pages = {norm_url(p.get("url")): (pid, p) for pid, p in st["pages"].items() if p.get("url")}
    cities = [p.get("city") for p in st["pages"].values() if p.get("type") == "location" and p.get("city")]
    internal, h1s, h2s = table(slug, "internal_all"), table(slug, "h1_all"), table(slug, "h2_all")
    text = {}
    pt = client_dir(slug) / "data" / "crawl" / "page-text.csv"
    if pt.exists():
        with open(pt, newline="", encoding="utf-8-sig") as fh:
            text = {norm_url(r["url"]): r.get("text", "") for r in csv.DictReader(fh)}
    rows = []
    for url, r in internal.items():
        if r.get("Status Code") != "200" or "html" not in (r.get("Content Type") or ""):
            continue
        pid, p = pages.get(norm_url(url), (None, {}))
        t = p.get("type") or "unknown"
        prefix = {"service": "SVC", "location": "LOC", "county": "HUB", "homepage": "HP"}.get(t)

        def add(check, ok, detail=""):
            rows.append({"page": pid or url, "url": url, "type": t, "check": check,
                         "result": "N/A" if ok is None else ("PASS" if ok else "FAIL"), "detail": detail})
        title, meta = r.get("Title 1", ""), r.get("Meta Description 1", "")
        add("COM-T", len(title) <= 60, f"{len(title)} characters")
        add("COM-M", 120 <= len(meta) <= 160, f"{len(meta)} characters")
        add("COM-W", None, f"{r.get('Word Count')} words")
        h1n = int((h1s.get(url) or {}).get("Occurrences") or (1 if r.get("H1-1") else 0))
        h1 = r.get("H1-1", "")
        h2 = [v for k, v in (h2s.get(url) or {}).items() if re.match(r"^H2-\d+$", k) and v]
        if prefix:
            add(f"{prefix}-05" if prefix in ("SVC", "LOC", "HP") else "HUB-05", h1n == 1, f"{h1n} H1(s)")
        if t in ("service", "location", "county"):
            bad = urlcheck.problems([{"id": pid, "type": t, "url": url}])
            add({"service": "SVC-02", "location": "LOC-01", "county": "HUB-04"}[t], not bad, "; ".join(bad))
        if t == "service":
            add("SVC-03", bool(brand) and title.endswith(f" - {brand}"), title)
            add("SVC-06", not (brand and brand.lower() in h1.lower()), h1)
            hit = [c for c in cities if any(re.search(rf"\b{re.escape(c)}\b", x, re.I) for x in [h1] + h2)]
            add("SVC-12", not hit, ", ".join(hit))
        if t == "county":
            add("HUB-05", h1n == 1 and not (brand and brand.lower() in h1.lower()), h1)
        body = text.get(norm_url(url))
        add("COM-N", None if body is None or not phone else phone in re.sub(r"\D", "", body),
            "no page-text capture" if body is None else "")
    d = client_dir(slug) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "conformance.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["page", "url", "type", "check", "result", "detail"])
        w.writeheader(); w.writerows(rows)
    kinds = (read_json(KINDS) or {}).get("auto", {})
    lines = [f"# {st['client']['name']} - Conformance (auto checks)", "",
             f"Made by scripts/conformance.py ({now()[:10]}) from the crawl. Only the checks with no judgment "
             "(methodology/specs/check-kinds.json); every other check is the audit agent's.", "",
             "| Check | What | Pass | Fail | N/A |", "|---|---|---|---|---|"]
    for c in sorted({r["check"] for r in rows}):
        rs = [r for r in rows if r["check"] == c]
        lines.append(f"| {c} | {kinds.get(c, '')} | {sum(r['result'] == 'PASS' for r in rs)} | "
                     f"{sum(r['result'] == 'FAIL' for r in rs)} | {sum(r['result'] == 'N/A' for r in rs)} |")
    fails = [r for r in rows if r["result"] == "FAIL"]
    lines += ["", "## Failures", ""] + ([f"- {r['page']} ({r['type']}) {r['check']}: {r['detail']}" for r in fails] or ["- none"])
    (d / "conformance.md").write_text("\n".join(lines) + "\n")
    return rows


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = run(sys.argv[1])
    f = sum(r["result"] == "FAIL" for r in rows)
    print(f"{len(rows)} auto check(s) scored · {f} fail · clients/{sys.argv[1]}/audit/conformance.md")


if __name__ == "__main__":
    main()
