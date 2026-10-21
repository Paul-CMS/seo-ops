#!/usr/bin/env python3
"""conformance.py — score every spec check that needs no judgment (rewrite 2 P12: mechanical checks off Opus).

    conformance.py <slug> [--crawl-date YYYY-MM-DD]
    conformance.py judge <slug> --run R [--confirmed]   the judgment checks for the pages Build will NOT rewrite, on
                                                         the Claude API (llm.py conformance-judge, Sonnet — Phase 2)
    conformance.py triage <slug> [--run R]              S15 triage (Rewrite 4 Phase 3): one column in the URL Decision
                                                         Map, "Conformance Triage" = rebuild / light fix / keep

S15 is triage, not a scorecard (Rewrite 4 Phase 3). A page Build rewrites (service, location, county hub and about pages
the map improves or creates) is `rebuild` and is never spec-scored. Only the pages Build will not rewrite are scored in
full — blog posts, kept utility pages (auto checks only: they have no spec), Route B pages and the homepage under the H1
lock (HP-08) — and become `light fix` (a failed check) or `keep`. Redirected and held URLs get no triage. There are no
per-type scorecard files.

Reads the crawl tables (inputs/crawl/*internal_all*, *h1_all*, *h2_all*), the page-text capture
(data/crawl/page-text.csv, if any), the site plan / page register (status.json pages) and facts.json (brand name,
phone). Which checks are auto is listed in methodology/specs/check-kinds.json; every other check is judgment and is
left for the audit agent. Writes clients/<slug>/audit/conformance.csv (page, type, check, result PASS|FAIL|N/A,
detail) and conformance.md (a summary per page type). Free, offline, deterministic.

`judge` (S15, after the URL Decision Map exists): every page in the scoring set (triage 'score', see above) whose type
has a spec is scored on the spec's judgment checks — every check the spec lists that is not auto — from the
crawl's title, meta, H1, H2s and the page-text capture, in one llm.py job. Writes audit/conformance-judgment.csv (page,
url, type, check, result PASS|FAIL|NE|N/A, detail, who) and adds "## Judgment checks (kept pages)" to conformance.md.
The audit agent reads the file instead of scoring those pages itself. No API key: nothing is written; the agent scores
them as before.
"""
import csv
import json
import re
import sys
import urllib.parse

import status as S
import urlcheck
from lib import ROOT, client_dir, die, now, read_json

KINDS = ROOT / "methodology" / "specs" / "check-kinds.json"


def table(slug, name, tools=("DFS",)):
    d = client_dir(slug) / "inputs" / "crawl"
    hits = sorted(h for t in tools for h in d.glob(f"* - {t} - {name} - *.csv")) if d.exists() else []
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


# ------------------------------------------------------------------ judgment checks for kept pages (Phase 2)
SPEC_FILE = [(r"^homepage", "homepage.md"), (r"^service\b(?!\s*\+)", "service.md"), (r"^location\b", "location.md"),
             (r"^county hub", "county-hub.md"), (r"^blog post", "blog-post.md"), (r"^about", "about.md")]


def spec_for(page_type):
    t = (page_type or "").strip().lower()
    return next((f for rx, f in SPEC_FILE if re.search(rx, t)), None)


def judgment_checks(spec):
    """[(id, requirement)] — the spec's checks that are not auto (methodology/specs/check-kinds.json)."""
    auto = (read_json(KINDS) or {}).get("auto", {})
    text = (ROOT / "methodology" / "specs" / spec).read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"^\|\s*([A-Z]{2,4}-\d+)\s*\|\s*([^|]+)\|", text, re.M):
        if m.group(1) not in auto and m.group(1) not in dict(out):
            out.append((m.group(1), m.group(2).strip()))
    return out


# ------------------------------------------------------------------ S15 triage (Rewrite 4 Phase 3)
TRIAGE_COL = "Conformance Triage"
REBUILT = ("service.md", "location.md", "county-hub.md", "about.md")


def _map_file(slug):
    maps = sorted((client_dir(slug) / "audit").glob("*/url-decision-map.csv"))
    return maps[-1] if maps else None


def _route_b(st):
    return {norm_url(p.get("url")) for p in st["pages"].values()
            if p.get("url") and str(p.get("route") or "").strip().upper() in ("B", "ROUTE B")}


def triage_class(row, st, route_b=frozenset()):
    """(class, why) for one URL Decision Map row: 'rebuild' (Build rewrites it — never spec-scored), 'score' (Build will
    not rewrite it: blog posts, kept utility pages, Route B pages, the homepage under the H1 lock HP-08 — scored in
    full, then light fix or keep), or None (the URL is going or held: a 301, a merge, an existing 301, a held URL)."""
    import pagedec
    act = re.sub(r"\s+", " ", (row.get("Proposed Action") or "").strip().lower())
    spec = spec_for(row.get("Page Type"))
    if not row.get("Current URL") or pagedec.destructive(act) or re.match(r"^(keep (existing )?301|hold)\b", act) \
            or "301" in (row.get("Page Type") or ""):
        return None, "the URL is redirected or held — not scored"
    if norm_url(row["Current URL"]) in route_b or "route b" in act:
        return "score", "Route B — Paul writes it; Build lists issues only"
    if spec == "homepage.md":
        return ("rebuild", "the H1 lock was lifted (CM-059)") if st["client"].get("h1_lock_lifted") else \
            ("score", "homepage under the H1 lock (HP-08) — kept, scored in full")
    if spec in REBUILT and re.match(r"^(improve|rebuild|create)\b", act):
        return "rebuild", "Build rewrites it to its spec"
    if spec == "blog-post.md":
        return "score", "blog post — Build does not rewrite it"
    return "score", ("kept " + ("page with a spec" if spec else "utility page (auto checks only)"))


def scoring_set(slug):
    """[(url, page_type, spec)] — the pages scored in full (triage 'score' with a spec); None before the map exists."""
    f = _map_file(slug)
    if not f:
        return None
    import pagedec
    st = S.load(slug)
    rb = _route_b(st)
    out, seen = [], set()
    for r in pagedec.map_rows(slug):
        cls, _ = triage_class(r, st, rb)
        spec = spec_for(r.get("Page Type"))
        if cls == "score" and spec and norm_url(r["Current URL"]) not in seen:
            seen.add(norm_url(r["Current URL"]))
            out.append((r["Current URL"], r.get("Page Type"), spec))
    return out


kept_pages = scoring_set   # Phase 2 name


def _fails(path):
    out = {}
    if path.is_file():
        with open(path, newline="", encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                if r.get("result") == "FAIL":
                    out.setdefault(norm_url(r.get("url") or r.get("page")), []).append(r["check"])
    return out


def triage(slug, run_id=None):
    """S15 triage: one column in the URL Decision Map — rebuild / light fix / keep — written by this script alone.
    A scored page with any failed check (auto: conformance.csv; judgment: conformance-judgment.csv) is 'light fix',
    else 'keep'. Also writes audit/conformance-triage.csv (url, action, type, triage, why, failed checks)."""
    f = _map_file(slug) or die(f"no URL Decision Map for {slug} yet — triage runs after S14 writes it", 4)
    st = S.load(slug)
    import render
    if str(f.relative_to(ROOT)) in render.approved_paths(st):
        die(f"{f.relative_to(ROOT)} is covered by an approval — the triage column is not added to an approved map", 4)
    rb = _route_b(st)
    d = client_dir(slug) / "audit"
    fails = _fails(d / "conformance.csv")
    for k, v in _fails(d / "conformance-judgment.csv").items():
        fails.setdefault(k, []).extend(v)
    with open(f, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        cols, rows = list(rd.fieldnames), list(rd)
    if TRIAGE_COL not in cols:
        cols.insert(cols.index("Proposed Action") + 1 if "Proposed Action" in cols else len(cols), TRIAGE_COL)
    out, n = [], {}
    for r in rows:
        cls, why = triage_class(r, st, rb)
        bad = sorted(set(fails.get(norm_url(r.get("Current URL")), []))) if cls == "score" else []
        val = "" if cls is None else "rebuild" if cls == "rebuild" else ("light fix" if bad else "keep")
        r[TRIAGE_COL] = val
        n[val or "—"] = n.get(val or "—", 0) + 1
        out.append({"url_id": r.get("URL ID", ""), "url": r.get("Current URL", ""), "action": r.get("Proposed Action", ""),
                    "type": r.get("Page Type", ""), "triage": val, "why": why, "failed_checks": " ".join(bad)})
    with open(f, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(d / "conformance-triage.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]) if out else ["url_id"])
        w.writeheader()
        w.writerows(out)
    if run_id:
        import run as R
        R.log_change(slug, run_id, "audit_triage", str(f.relative_to(ROOT)), TRIAGE_COL, "",
                     ", ".join(f"{v} {k}" for k, v in sorted(n.items())), "DONE", channel="local")
    return n


def judge(slug, run_id, confirmed=False):
    import llm
    import run as R
    R.open_run(slug, run_id)
    pages = kept_pages(slug)
    if pages is None:
        die(f"no URL Decision Map for {slug} yet (audit/<date>/url-decision-map.csv) — judge runs after it", 4)
    tools = ("DFS", "SF")
    internal, h1s, h2s = table(slug, "internal_all", tools), table(slug, "h1_all", tools), table(slug, "h2_all", tools)
    pt = client_dir(slug) / "data" / "crawl" / "page-text.csv"
    text = {}
    if pt.exists():
        with open(pt, newline="", encoding="utf-8-sig") as fh:
            text = {norm_url(r["url"]): r.get("text", "") for r in csv.DictReader(fh)}
    by_norm = {norm_url(u): r for u, r in internal.items()}
    h1n = {norm_url(u): r for u, r in h1s.items()}
    h2n = {norm_url(u): r for u, r in h2s.items()}
    items, asked, meta = [], {}, {}
    for url, ptype, spec in pages:
        k = norm_url(url)
        r = by_norm.get(k, {})
        checks = judgment_checks(spec)
        h2 = [v for kk, v in (h2n.get(k) or {}).items() if re.match(r"^H2-\d+$", kk) and v]
        body = text.get(k)
        pid = f"p{len(items) + 1}"
        asked[pid] = {c for c, _ in checks}
        meta[pid] = (url, ptype)
        items.append({"id": pid, "url": url, "type": ptype, "title": r.get("Title 1", ""),
                      "meta_description": r.get("Meta Description 1", ""),
                      "h1": (h1n.get(k) or {}).get("H1-1") or r.get("H1-1", ""), "h2s": h2,
                      "h2s_complete": bool(body),   # the crawl exports only the first H2s; the page text has all
                      "word_count": r.get("Word Count", ""),
                      "page_text": (body or "")[:12000] if body else "(not captured — body checks are NE)",
                      "checks": [{"check": c, "requirement": q} for c, q in checks]})
    if not items:
        print("the URL Decision Map keeps no page with a spec — nothing to judge")
        return
    st = S.load(slug)
    import facts
    fx = {r["id"]: r for r in facts.load(slug)["facts"]}
    brand = (fx.get("a-brand-entity-gbp-name-exactly") or {}).get("value", "").split(" — ")[0].strip() \
        or st["client"].get("name", "")
    cities = sorted({p.get("city") for p in st["pages"].values() if p.get("type") == "location" and p.get("city")})
    ans = llm.attempt(slug, run_id, "conformance-judge", {"brand": brand, "planned_cities": cities}, items,
                      f"conformance judgment for {len(items)} kept page(s)",
                      "the audit agent scores the kept pages' judgment checks (S15)", confirmed)
    if ans is None:
        return
    who = f"llm.py conformance-judge ({llm.JOBS['conformance-judge']['model']})"
    rows = []
    for pid, a in ans.items():
        url, ptype = meta[pid]
        got = {c["check"]: c for c in a.get("checks") or [] if c.get("check") in asked[pid]}
        for c in sorted(asked[pid]):
            g = got.get(c) or {"result": "NE", "detail": "not answered on the API — the audit agent scores it"}
            rows.append({"page": url, "url": url, "type": ptype, "check": c, "result": g["result"],
                         "detail": g["detail"], "who": who if c in got else "open"})
    d = client_dir(slug) / "audit"
    with open(d / "conformance-judgment.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["page", "url", "type", "check", "result", "detail", "who"])
        w.writeheader(); w.writerows(rows)
    md = d / "conformance.md"
    old = md.read_text() if md.exists() else f"# {st['client']['name']} - Conformance\n"
    old = re.sub(r"\n## Judgment checks \(kept pages\).*\Z", "", old, flags=re.S).rstrip("\n")
    fails = [r for r in rows if r["result"] == "FAIL"]
    add = ["", "## Judgment checks (kept pages)", "",
           f"Scored {now()[:10]} by {who} for {len(ans)} kept page(s) (audit/conformance-judgment.csv): "
           + " · ".join(f"{sum(r['result'] == x for r in rows)} {x}" for x in ("PASS", "FAIL", "NE", "N/A")), ""]
    add += [f"- {r['url']} ({r['type']}) {r['check']}: {r['detail']}" for r in fails] or ["- no failures"]
    md.write_text(old + "\n" + "\n".join(add) + "\n")
    R.log_change(slug, run_id, "llm_judgment", "audit/conformance-judgment.csv", "judgment checks (kept pages)", "",
                 f"{len(rows)} check(s) on {len(ans)} page(s), {len(fails)} FAIL", "DONE", channel="local")
    print(f"{len(ans)} kept page(s) scored on the Claude API · {len(rows)} judgment check(s), {len(fails)} FAIL · "
          f"clients/{slug}/audit/conformance-judgment.csv")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "judge":
        import argparse
        ap = argparse.ArgumentParser(prog="conformance.py judge")
        ap.add_argument("slug"); ap.add_argument("--run", required=True); ap.add_argument("--confirmed", action="store_true")
        a = ap.parse_args(sys.argv[2:])
        judge(a.slug, a.run, a.confirmed)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "triage":
        import argparse
        ap = argparse.ArgumentParser(prog="conformance.py triage")
        ap.add_argument("slug"); ap.add_argument("--run")
        a = ap.parse_args(sys.argv[2:])
        if a.run:
            import run as R
            R.open_run(a.slug, a.run)
        n = triage(a.slug, a.run)
        print("S15 triage written to the URL Decision Map (Conformance Triage): "
              + " · ".join(f"{v} {k}" for k, v in sorted(n.items())) + f" · clients/{a.slug}/audit/conformance-triage.csv")
        return
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = run(sys.argv[1])
    f = sum(r["result"] == "FAIL" for r in rows)
    print(f"{len(rows)} auto check(s) scored · {f} fail · clients/{sys.argv[1]}/audit/conformance.md")


if __name__ == "__main__":
    main()
