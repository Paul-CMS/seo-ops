#!/usr/bin/env python3
"""qa.py — the mechanical QA, by script (Rewrite 4 Phase 5, CM-064). No agent, no spend (explain: a few cents).

    qa.py check   <slug> [--stage ship|live] [--pages a,b] [--out DIR]   every approved page → finish/qa/qa-<stage>.csv
                                                                         + .md (the punch list); exit 1 on any error
    qa.py explain <slug> --run R [--stage ship|live] [--confirmed]       the explanations job on llm.py (Haiku): a plain
                                                                         explanation, the fix and who acts, per row
    qa.py sample  <slug>                                                 the pages finish-qa (Opus) reads: every page for
                                                                         a sensitive client (CM-025), else a sample

Checks, per page (its approved file as it ships — link markers resolved, CM-064):
    placeholders  P11: open items (ship: listed — each becomes a notice and a worklist row; live: an error), markers
    links         the wheel's rows resolve to planned URLs and have a table to sit in; every Markdown link is a planned
                  page, an https URL, never '#' or empty; a cross-page link in prose (CM-005) is flagged
    title / h1    the spec's formats (§3): service "Service - Brand"; location "Brand - Category - City, Full State";
                  hub "Brand - Category - …, Full State"; homepage "Brand - Category - Area"; one H1; no brand in the H1;
                  location H1 ends "in [City]" with no state; a service H1 names no city; no "The Best" without H2's yes
    meta          150–160 characters (WC-C2)
    reading       Flesch-Kincaid page average ≤ 8.9 (CM-047) — entity terms excluded
    schema        the page's built schema is valid (schema.py validate); ship: missing = built at the handoff; live: an error
    live          (live stage) the live page matches its approved file (verify.py's comparison) and carries its schema
Levels: error (blocks the handoff / release) · warn (listed for Paul) · note. The handoff (`publish.py handoff`) runs
`check --stage ship` and refuses on any error; finish:qa runs `check --stage live` on the published pages.
Explain without a key (or a 401): "no API key — ran on the agent route" — each row keeps the script's own detail and a
fixed hint, which is enough for Jonie; nothing fails.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

from lib import ROOT, client_dir, config, die, now, today, write_json

COLS = ["page", "url", "check", "level", "rule", "detail", "explain", "fix", "who"]
HINT = {"placeholders": ("an open item is still on the page", "resolve it (or the notice stays and the page is not published)", "Paul"),
        "links": ("a link would be missing or broken on the live page", "correct the site plan or the approved file", "writer"),
        "title": ("the SEO title is not in the spec's format", "rewrite the title in the approved file", "writer"),
        "h1": ("the H1 is not in the spec's format", "rewrite the H1 in the approved file", "writer"),
        "meta": ("the meta description length is outside 150–160 characters", "adjust it in the approved file", "writer"),
        "reading": ("the page reads above grade 8", "split long sentences in the approved file", "writer"),
        "schema": ("the page's structured data is missing or invalid", "fix the Brand Guide input and rebuild (schema.py build)", "Paul"),
        "live": ("the live page differs from its approved file", "make the live page match the approved file", "Jonie")}


def qa_dir(slug):
    return client_dir(slug) / "finish" / "qa"


def _bg_bits(slug):
    import outline
    import schema
    bg = outline.brand_guide(slug)
    ent = outline.bg_entity(bg) if bg else {"category": "", "reserved_area": "", "pool": [], "variants": [], "c1": {}}
    a = schema._a(bg) if bg else {}
    brand = schema._clean(a.get("1")) or ""
    area = schema._clean(a.get("5")) or ""
    nap = schema.nap(schema._row(schema._f(bg), r"Confirmed NAP")) if bg else None
    state = schema.STATES.get((nap or {}).get("addressRegion", ""), "")
    h2 = (outline.md_section(bg, r"H2\b") if bg else "") or ""
    return {"brand": brand, "category": ent.get("category", ""), "area": area, "state": state,
            "abbr": (nap or {}).get("addressRegion", ""), "reserved": ent.get("reserved_area", ""),
            "best_ok": bool(re.search(r"\byes\b", h2, re.I)), "ent": ent}


def _title_case(s):
    import outline
    return outline.title_case(s or "")


def title_checks(p, m, bits, cities):
    out = []
    t, title, h1 = p.get("type"), m["seo_title"], m["h1"]
    brand, cat, state = bits["brand"], _title_case(bits["category"]), bits["state"]
    sep = " - "
    if t == "service":
        ok = title.endswith(f"{sep}{brand}") and title.count(sep) == 1
        want = "Service Name - Brand"
    elif t == "location":
        import wheel
        ok = title == f"{brand}{sep}{cat}{sep}{wheel.city_of(p)}, {state}"
        want = f"{brand} - {cat} - {wheel.city_of(p)}, {state}"
    elif t == "county":
        ok = title.startswith(f"{brand}{sep}{cat}{sep}") and title.endswith(f", {state}")
        want = f"{brand} - {cat} - [County], {state}"
    elif t == "homepage":
        ok = title == f"{brand}{sep}{cat}{sep}{bits['area']}"
        want = f"{brand} - {cat} - {bits['area']}"
    elif t == "about":
        ok = title.startswith(f"About {brand}{sep}")
        want = f"About {brand} - [Area Category]"
    else:
        ok, want = True, ""
    if brand and cat and not ok:
        out.append(("title", "error", "BB-302", f"SEO title {title!r} is not the {t} format {want!r}"))
    if len(title) > 65 and t in ("service", "about"):   # the location, hub and homepage formats fix their length
        out.append(("title", "warn", "BB-303", f"SEO title is {len(title)} characters — it may be truncated in search"))
    if re.search(r"\bthe best\b", title, re.I):
        out.append(("title", "error", "CM-020", "\"The Best\" is never in an SEO title"))
    # H1
    body_h1 = re.findall(r"^# ", m["body"], re.M)
    if body_h1:
        out.append(("h1", "error", "BB-307", f"{len(body_h1) + 1} H1s — exactly one"))
    if brand and brand.lower() in h1.lower() and t != "about":
        out.append(("h1", "error", "BB-305", f"H1 {h1!r} names the brand"))
    if t == "location":
        import wheel
        city = wheel.city_of(p)
        if not h1.endswith(f" in {city}"):
            out.append(("h1", "error", "location §3.4", f"H1 {h1!r} is not '[Service Variant] in {city}'"))
        if state and (state in h1 or re.search(rf",\s*{bits['abbr']}\b", h1)):
            out.append(("h1", "error", "location §3.4", f"H1 {h1!r} carries the state — no state"))
    if t == "service":
        hit = [c for c in cities if re.search(rf"\b{re.escape(c)}\b", h1)]
        if hit:
            out.append(("h1", "error", "BB-314", f"service H1 {h1!r} names a city ({hit[0]}) — never a city"))
        if bits["reserved"] and bits["reserved"].lower() in h1.lower():
            out.append(("h1", "error", "CM-024", f"service H1 uses the homepage's reserved variant {bits['reserved']!r}"))
    if re.search(r"\bthe best\b", h1, re.I) and not bits["best_ok"]:
        out.append(("h1", "error", "CM-020", "\"The Best\" in the H1 without Brand Guide H2's yes"))
    n = len(m["meta_description"])
    if t in ("service", "location", "county", "homepage", "about") and not 150 <= n <= 160:
        out.append(("meta", "warn", "WC-C2", f"meta description is {n} characters (150–160)"))
    return out


def link_checks(slug, st, pid, m, wheel_rows, wheel_issues, planned_urls, domain):
    import placeholders
    import wheel as W
    out = [("links", lvl if lvl == "error" else "warn", "CM-064", t) for lvl, p_, t in wheel_issues if p_ == pid]
    in_table = False
    for ln in m["body"].split("\n"):
        s = ln.strip()
        in_table = s.startswith("|")
        for text, href in re.findall(r"\[([^\]]+)\]\(([^)\s]*)\)", ln):
            if not href or href.startswith("#") or href.lower() in ("tbd", "todo", "url", "link"):
                out.append(("links", "error", "CM-016", f"link {text!r} has no real target ({href!r})"))
            elif href.startswith("/") or any(hst in href for hst in domain):
                u = href if href.startswith("http") else f"https://x{href}"
                if W.path_of(u) not in planned_urls:
                    out.append(("links", "error", "CM-064", f"internal link {href} is not a planned page"))
                elif not in_table:
                    out.append(("links", "warn", "CM-005", f"cross-page link {href} in prose — only in the link tables "
                                                            "(or an approved CM-022 exception)"))
            elif not href.startswith("https://"):
                out.append(("links", "warn", "CM-011", f"outbound link {href} is not https"))
    for x in m.get("marker_actions") or []:
        out.append(("links", "note", "CM-064", f"{x['marker'][:70]} → {x['action']}" + (f" ({x.get('why')})" if x.get("why") else "")))
    return out


def reading_checks(f, bits, st):
    import readability
    terms = [bits["category"], bits["area"], bits["brand"]] + [p.get("name") or "" for p in st["pages"].values()]
    terms = sorted({t for t in terms if t}, key=len, reverse=True)
    rows = [(sec, t, *readability.grade(t)) for sec, t in readability.units((ROOT / f).read_text(encoding="utf-8"), terms)]
    rows = [r for r in rows if r[2] is not None]
    if not rows:
        return []
    total = sum(r[3] for r in rows)
    avg = sum(r[2] * r[3] for r in rows) / total
    if avg > readability.PAGE_MAX:
        return [("reading", "warn", "CM-047", f"page average grade {avg:.1f} (target ≤ {readability.PAGE_MAX})")]
    return []


def schema_checks(slug, pid, stage):
    import schema
    d = schema.out_dir(slug)
    idx = d / "index.json"
    if not idx.exists():
        return [("schema", "error" if stage == "live" else "note", "CM-064",
                 "no schema built yet" + ("" if stage == "live" else " — built at the handoff (schema.py build)"))]
    index = json.loads(idx.read_text())
    e = index["pages"].get(pid)
    if not e:
        return []
    cfg = json.loads((d / "config.json").read_text()) if (d / "config.json").exists() else None
    try:
        g = json.loads((d / e["file"].replace(".script.html", ".jsonld")).read_text())
    except (OSError, ValueError) as ex:
        return [("schema", "error", "BB-6xx", f"schema file unreadable ({ex})")]
    probs = schema.validate(pid, e["url"], e["kind"], g, schema.known_ids(cfg) if cfg else set(),
                            (cfg or {}).get("gbp_landing_page", ""))
    return [("schema", "error", "BB-6xx", p) for p in probs]


def live_checks(slug, st, pid):
    import schema
    import verify
    meta, diffs, _, body = verify.page_diffs(slug, st, pid)
    out = [("live", "error", "verify", d) for d in diffs]
    idx = schema.out_dir(slug) / "index.json"
    e = json.loads(idx.read_text())["pages"].get(pid) if idx.exists() else None
    if e and body:
        want = json.loads((schema.out_dir(slug) / e["file"].replace(".script.html", ".jsonld")).read_text())
        found = []
        for blob in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body, re.S | re.I):
            try:
                found.append(json.loads(blob))
            except ValueError:
                out.append(("live", "error", "BB-6xx", "a JSON-LD block on the live page is not valid JSON"))
        if want not in found:
            out.append(("live", "error", "BB-6xx", "the live page does not carry its built schema (head-code field)"))
    return out


def run_checks(slug, stage="ship", only=None):
    import publish
    import status as S
    import wheel as W
    st = S.load(slug)
    bits = _bg_bits(slug)
    wheel_rows, wheel_issues = W.plan(st, slug)
    pages = W.pages_of(st)
    planned = {W.path_of(p["url"]) for p in pages.values() if p.get("url")}
    domain = {urllib.parse.urlparse(p["url"]).netloc for p in pages.values() if p.get("url")} or {st["client"].get("domain") or "-"}
    cities = [W.city_of(p) for p in pages.values() if p.get("type") == "location"]
    rows = []
    for pid, p in pages.items():
        if only and pid not in only:
            continue
        if stage == "live" and p.get("state") not in ("published", "verified", "written_back"):
            continue
        f = W.approved_file(st, pid)
        if not f:
            rows.append({"page": pid, "url": p.get("url", ""), "check": "placeholders", "level": "error",
                         "rule": "CM-055", "detail": "no approved page file — every page ships together"})
            continue
        m = publish.shipped(slug, st, pid, publish.parse(f))
        found = []
        import placeholders
        for i in placeholders.scan_text(publish.shipped_text(slug, st, pid, f)):
            found.append(("placeholders", "error" if stage == "live" else "warn", "P11",
                          f"line {i['line']}: {i['text'][:90]} — " + ("must be resolved before release" if stage == "live"
                                                                     else "becomes an 'Open items' notice and a worklist row")))
        found += link_checks(slug, st, pid, m, wheel_rows, wheel_issues, planned, domain)
        found += title_checks(p, m, bits, cities)
        found += reading_checks(f, bits, st)
        if p.get("type") in ("service", "location", "county", "homepage"):
            found += schema_checks(slug, pid, stage)
        if stage == "live":
            found += live_checks(slug, st, pid)
        rows += [{"page": pid, "url": m["url"], "check": c, "level": lvl, "rule": r, "detail": d} for c, lvl, r, d in found]
    return rows


def write(slug, stage, rows, out=None):
    d = Path(out) if out else qa_dir(slug)
    d.mkdir(parents=True, exist_ok=True)
    with open(d / f"qa-{stage}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in COLS} for r in rows)
    errs = [r for r in rows if r["level"] == "error"]
    warns = [r for r in rows if r["level"] == "warn"]
    lines = [f"# QA Punch-List — {stage} — {today()}", "",
             f"_By `qa.py check --stage {stage}` (no agent). {len(errs)} error(s) block "
             f"{'the handoff' if stage == 'ship' else 'release'}; {len(warns)} warning(s) are listed for Paul._", ""]
    for level, title in (("error", "Errors — fix before going on"), ("warn", "Warnings"), ("note", "Notes")):
        sel = [r for r in rows if r["level"] == level]
        if not sel:
            continue
        lines += [f"## {title}", "", "| Page | Check | Rule | Detail | Fix | Who |", "|---|---|---|---|---|---|"]
        for r in sel:
            lines.append(f"| {r['page']} | {r['check']} | {r['rule']} | {r['detail'].replace('|', '/')} | "
                         f"{(r.get('fix') or '').replace('|', '/')} | {r.get('who', '')} |")
        lines.append("")
    (d / f"qa-{stage}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return d / f"qa-{stage}.csv", len(errs), len(warns)


def explain(slug, run_id, stage, confirmed=False):
    import llm
    p = qa_dir(slug) / f"qa-{stage}.csv"
    if not p.exists():
        die(f"no QA file yet — run qa.py check {slug} --stage {stage} first")
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    ask = [r for r in rows if r["level"] in ("error", "warn")]
    items = [{"id": str(i), "page": r["page"], "url": r["url"], "check": r["check"], "rule": r["rule"], "detail": r["detail"]}
             for i, r in enumerate(ask)]
    got = llm.attempt(slug, run_id, "qa-explain", {"stage": stage}, items, f"QA explanations ({stage})",
                      "each row keeps the script's detail and a fixed hint", confirmed) if items else {}
    for i, r in enumerate(ask):
        a = (got or {}).get(str(i))
        h = HINT.get(r["check"], ("", "", ""))
        r["explain"], r["fix"], r["who"] = (a["explain"], a["fix"], a["who"]) if a else (h[0], h[1], h[2])
    _, e, w = write(slug, stage, rows)
    print(f"{len(ask)} row(s) explained " + ("on the Claude API" if got else "by the fixed hints") +
          f" → {(qa_dir(slug) / f'qa-{stage}.md').relative_to(ROOT)}")


def sample(slug):
    """finish-qa reads every page for a sensitive client (CM-025), else a fixed sample (config qa_sample_share)."""
    import status as S
    import wheel as W
    st = S.load(slug)
    pages = sorted(W.pages_of(st))
    if st["client"].get("sensitive"):
        return pages, f"sensitive client ({st['client'].get('sensitive_category') or 'CM-025'}): every page"
    share = float(config().get("qa_sample_share", 0.2))
    n = min(len(pages), max(int(config().get("qa_sample_min", 2)), round(len(pages) * share)))
    by_type = {}
    for pid in pages:
        by_type.setdefault(W.pages_of(st)[pid]["type"], []).append(pid)
    pick = [sorted(v, key=lambda x: hashlib.sha256(f"{slug}:{x}".encode()).hexdigest())[0] for v in by_type.values()]
    rest = sorted((p for p in pages if p not in pick), key=lambda x: hashlib.sha256(f"{slug}:{x}".encode()).hexdigest())
    pick = (pick + rest)[:max(n, len(by_type))]
    return sorted(pick), f"a sample of {len(pick)} of {len(pages)} page(s) (every page type, then by a fixed hash)"


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("check"); s.add_argument("slug"); s.add_argument("--stage", choices=["ship", "live"], default="ship")
    s.add_argument("--pages"); s.add_argument("--out")
    s = sub.add_parser("explain"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--stage", choices=["ship", "live"], default="ship"); s.add_argument("--confirmed", action="store_true")
    s = sub.add_parser("sample"); s.add_argument("slug")
    a = ap.parse_args()
    if a.cmd == "check":
        rows = run_checks(a.slug, a.stage, set(a.pages.split(",")) if a.pages else None)
        p, e, w = write(a.slug, a.stage, rows, a.out)
        print(f"QA ({a.stage}): {e} error(s), {w} warning(s) on {len({r['page'] for r in rows})} page(s) → "
              f"{p.with_suffix('.md').relative_to(ROOT) if p.is_relative_to(ROOT) else p.with_suffix('.md')}")
        for r in [r for r in rows if r["level"] == "error"][:6]:
            print(f"  ERROR {r['page']} · {r['check']}: {r['detail'][:110]}")
        sys.exit(1 if e else 0)
    if a.cmd == "explain":
        return explain(a.slug, a.run, a.stage, a.confirmed)
    pages, why = sample(a.slug)
    p = qa_dir(a.slug) / "finish-qa-pages.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(pages) + "\n")
    print(f"finish-qa (Opus) reads {why}: {', '.join(pages)}")


if __name__ == "__main__":
    main()
