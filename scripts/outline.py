#!/usr/bin/env python3
"""outline.py — each page's outline, derived by script at draft time (Rewrite 4 Phase 4: no brief step).

    outline.py build <slug> <section> --run R [--page P]   write and record the outline of every page in the section
                                                          that cleared the evidence gate (or one page)
    outline.py show <slug> <page>                          print a page's outline path and whether it is current
    outline.py faq <slug> <section> --run R [--confirmed]  FAQ fit picks for every page of the section on the Claude API
                                                          (llm.py faq-picks, Sonnet — Rewrite 4 Phase 2) →
                                                          build/<section>/faq-picks.json, shown in each outline

A section on the outline route (status.py: batch "route" = "outline"; every section without approved briefs —
status.py assign_routes on /next, D5) has no brief. Inside its /build write run, after the evidence gate, this script writes
clients/<slug>/build/<section>/outlines/<page>.md from what is already approved — nothing is decided here:
  - the approved site-plan row (type, name, URL, group, replaces, and any planned keyword / H1 / variant / claims);
    the approved plan file itself never changes, so an approved site plan stays approved;
  - the page spec's element order (methodology/specs/<type>.md §3), quoted row by row;
  - the variant pools (Brand Guide B1 reserved, B2 rotation; the category variants from the pack);
  - FAQ candidates: the pack's PAA and fan-out questions (location pages: the three categories, location-faq.md);
  - headings and FAQs already owned by other pages (Brand Guide C3) — never repeated;
  - links: the table rows the page carries (services, locations, siblings, hub), left for Finish;
  - the claims list: the pack's facts in the writer's three states (confirmed · sourced public · unknown) and the
    Brand Guide's D2 claims never to reuse.
Phase 1: a keyword, H1, service/category variant or area variant the plan row leaves empty is assigned by formula
from the Brand Guide (A2/A3 categories, B1 reserved, B2 pool, C1 service rows) and the page spec's §3 formats —
`## Assigned by formula` in the outline, and recorded in the page's `assigned` — so the writer never chooses them
(HMM's location rows carry none). FAQ picks come from `outline.py faq` (Phase 2) when it has run; with no API key the
writer picks from the candidates as before. Whatever the Brand Guide cannot support (and H2 wording, FAQ picks not made
by `outline.py faq`) the writer chooses and reports in its results file; each choice is a "Fix and list" row on the section's one draft review sheet (CM-061).
Zero model tokens. The draft is written from the outline + pack + spec + pilot corrections, one fresh subagent per
page (CM-043).
"""
import argparse
import re
import time

import facts
import status as S
from lib import ROOT, append, client_dir, die, now, read_json, sha12

SPEC_OF = {v: k for k, v in S.SPEC_TYPE.items()}
VARIANT_ROWS = ("a-category-variants", "a-area-variants")
PLAN_FIELDS = (("keyword", "Keyword"), ("h1", "H1"), ("service_variant", "Service variant"), ("city", "City"),
               ("category_variant", "Category variant"), ("area_variant", "Area variant"), ("claims", "Claims"),
               ("faq", "FAQ picks"), ("h2s", "H2s"))
LOC_FAQ = (("1 · Local cost or decision", "what changes the job or the price here (HOA/ARB, historic district, "
            "flood rules, wind code); no prices unless confirmed"),
           ("2 · Logistics in this area", "permits and who issues them, access, travel and response time, season"),
           ("3 · Trust in this area", "local pain points and the client's local experience; reviews at their tier"))


def md_section(text, heading):
    """The body under the first heading matching `heading` (a regex), up to the next heading of the same or a
    higher level."""
    m = re.search(rf"^(#+)\s*{heading}.*$", text, re.M)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(rf"^#{{1,{level}}}\s", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def table_rows(text):
    """[[cell, …], …] for the body rows of the Markdown tables in `text` (header and rule rows skipped)."""
    rows, header = [], True
    for line in text.splitlines():
        if not line.startswith("|"):
            header = True
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            header = False
            continue
        if not header:
            rows.append(cells)
    return rows


def spec_elements(ptype):
    """[(n, element, requirement)] from the spec's §3 table, in page order."""
    spec = ROOT / "methodology" / "specs" / SPEC_OF.get(ptype, f"{ptype}.md")
    if not spec.is_file():
        return None, []
    sec = md_section(spec.read_text(encoding="utf-8"), r"3\.")
    return spec, [(r[0], r[1], r[2]) for r in table_rows(sec) if len(r) >= 3]


def brand_guide(slug):
    p = client_dir(slug) / "brand-guide.md"
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def code_block(text):
    m = re.search(r"```\n?(.*?)```", text, re.S)
    return [ln.strip() for ln in (m.group(1) if m else "").splitlines() if ln.strip()]


def used_elsewhere(bg, url):
    """Brand Guide C3 rows owned by another page: [(heading or question, owner)]."""
    path = (url or "").split("://")[-1].split("/", 1)[-1].strip("/")
    out = []
    for r in table_rows(md_section(bg, r"C3\b")):
        if len(r) >= 2 and r[0] and r[1].strip("/") != path:
            out.append((r[0], r[1]))
    return out


def never_reuse(bg):
    return [(r[0], r[3] if len(r) > 3 else "") for r in table_rows(md_section(bg, r"D2\b")) if r and r[0]]


def link_rows(st, pid):
    """{label: [(name, url)]} — the pages this page's tables link to (rows are filled at Finish)."""
    pages = st["pages"]
    me = pages[pid]
    def of(t, same_group=False):
        return [(p.get("name") or q, p.get("url", "")) for q, p in pages.items()
                if q != pid and p.get("type") == t and (not same_group or p.get("group") == me.get("group"))]
    t = me.get("type")
    if t == "location":
        return {"Services table (H3 links to every service page)": of("service"),
                "Sibling cities (every other location page)": of("location"),
                "Hub for this group (reached through the sibling table)": of("county", True)}
    if t == "service":
        return {"Service-areas table (every location page)": of("location") + of("county")}
    if t == "county":
        return {"Cities in this hub": of("location", True), "Services": of("service")}
    if t == "homepage":
        return {"Services (part 6)": of("service"), "Areas grid": of("county") + of("location")}
    return {}


SMALL = {"in", "of", "the", "and", "a", "an", "to", "for", "near"}


def title_case(s):
    words = s.split()
    return " ".join(w if (i and w.lower() in SMALL) else w[:1].upper() + w[1:] for i, w in enumerate(words))


def _clean(v):
    """A Brand Guide cell value without its status tag, parenthetical notes or template blanks."""
    v = re.sub(r"\[[^\]]*\]|\*\([^)]*\)\*|\([^)]*\)|\*\*|`", "", v or "")
    v = re.sub(r"_{3,}", "", v)
    return v.strip(" .;·—-")


def bg_entity(bg):
    """The entity values the formulas read, parsed from the Brand Guide: primary category (A2), category variants (A3),
    the homepage's reserved variants (B1), the area rotation pool (B2), and the service rows of C1."""
    a = {r[0]: r for r in table_rows(md_section(bg, r"Section A")) if len(r) >= 3}
    cat = _clean((a.get("2") or ["", "", ""])[2].split(" (")[0].split(" —")[0])
    raw3 = (a.get("3") or ["", "", ""])[2].split("Excluded")[0]
    variants = [v for v in (_clean(x) for x in raw3.split(" · ")) if v]
    res = {}
    for ln in code_block(md_section(bg, r"B1\b")):
        k, _, v = ln.partition(":")
        res[k.strip().upper()] = _clean(v)
    pool = [re.sub(r"^\d+\.\s*", "", x).strip() for x in code_block(md_section(bg, r"B2\b"))]
    c1 = {}
    for r in table_rows(md_section(bg, r"C1\b")):
        if len(r) >= 3 and r[0].startswith("/"):
            path = r[0].split()[0].strip("/")
            kw = re.search(r'keyword\s+"([^"]+)"', r[1])
            c1[path] = {"keyword": kw.group(1) if kw else "", "variant": _clean(r[2].split(" (H1")[0])}
    return {"category": cat, "variants": variants, "reserved_area": res.get("HOMEPAGE AREA VARIANT", ""),
            "reserved_cat": res.get("HOMEPAGE CATEGORY VARIANT", ""), "pool": [p for p in pool if p], "c1": c1}


def _path(url):
    return (url or "").split("://")[-1].split("/", 1)[-1].strip("/")


def _abbr(p):
    name = p.get("name") or ""
    m = re.search(r",\s*([A-Za-z]{2})\b", name) or re.search(r"-([a-z]{2})/?$", p.get("url", ""))
    return m.group(1).upper() if m else ""


def formula(st, pid, ent):
    """{field: (value, how)} for the plan values the site-plan row left empty — assigned by formula from the Brand Guide
    and the spec (Rewrite 4 Phase 1), so the writer never chooses them. A field the Brand Guide cannot support is left
    out: it stays open and the writer reports it as a Fix and list row."""
    pages = st["pages"]
    p = pages[pid]
    t = p.get("type")
    out = {}
    services = [q for q in pages.values() if q.get("type") == "service"]
    core = next((ent["c1"][_path(q["url"])]["keyword"] for q in services if ent["c1"].get(_path(q["url"]), {}).get("keyword")), "") \
        or next((q["keyword"] for q in services if q.get("keyword")), "") or (services[0].get("name", "").lower() if services else "")
    cat_h1 = next((v for v in ent["variants"] if v.lower() not in (ent["category"].lower(), ent["reserved_cat"].lower())), "")
    pool = [x for x in ent["pool"] if x.lower() != ent["reserved_area"].lower()]
    if t == "service":
        row = ent["c1"].get(_path(p.get("url")), {})
        kw = row.get("keyword") or (p.get("name") or "").lower()
        out["keyword"] = (kw, "BG C1 keyword for this URL, else the service name (service spec §3.4)" if row.get("keyword")
                          else "the service name, lower case (no BG C1 keyword for this URL)")
        sv = p.get("service_variant") or row.get("variant") or (p.get("name") or "").lower()
        if pool and sv:
            out["h1"] = (f"{title_case(sv)} in {pool[0]}", "service spec §3.4: [Service Variant] in [Area Variant]; "
                         "BG C1 service variant + the first B2 area variant (never a city, never the reserved one)")
            out["area_variant"] = (pool[0], "first B2 rotation entry (the H1 slot)")
        if sv:
            out["service_variant"] = (sv, "BG C1 H1 service variant, else the service name")
    elif t == "location":
        # A county hub is never assigned: its H1 would repeat the same-named city's (Charleston area hub vs Charleston),
        # and its format still waits on Paul's ruling (county-hub spec §3.4). It stays open for the writer and the sheet.
        city = p.get("city") or (p.get("name") or "").split(",")[0]
        if core and city:
            out["keyword"] = (" ".join(x for x in (core, city, _abbr(p)) if x), "location spec: core service keyword + city + "
                              "state abbreviation (the Beaufort pilot's pattern)")
        if cat_h1 and city:
            out["h1"] = (f"{title_case(cat_h1)} in {city}", "location spec §3.4: [Service Variant] in [City], no state; the first "
                         "A3 category variant that is neither the GBP category (title slot) nor the homepage's reserved one")
            out["category_variant"] = (cat_h1, "the same A3 variant (the H1 slot)")
        grp = p.get("group")
        hub = next((q for q in pages.values() if q.get("type") == "county" and q.get("group") == grp), None) if grp else None
        words = lambda v: set(re.findall(r"\w+", v.lower())) - SMALL - {"area", "hub", "county", "service"}
        hub_words = words(hub.get("name") or "") if hub else set()
        best = max(pool, key=lambda v: len(words(v) & hub_words), default="") if hub_words else ""
        if best and words(best) & hub_words:
            # only a pool entry that names this page's own hub: a rotation could put a city in the wrong county
            out["area_variant"] = (best, "the B2 entry that names this page's hub (opening slot)")
    return out


# ------------------------------------------------------------------ FAQ fit picks on the Claude API (Phase 2)
ROUTE_FILES = ("data/paa/paa-routing.md", "data/fanout/fanout-routing.md")


def routed(slug):
    """[(question, route, source)] from the routing worksheets' rows routed to a service or a location page."""
    out = []
    for rel in ROUTE_FILES:
        f = client_dir(slug) / rel
        if not f.is_file():
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        head = next((l for l in lines if l.startswith("|") and "| Route |" in l), None)
        if not head:
            continue
        cols = [c.strip() for c in head.strip().strip("|").split("|")]
        q = cols.index("Question") if "Question" in cols else cols.index("Query") if "Query" in cols else None
        r = cols.index("Route")
        for l in lines:
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if l.startswith("|") and len(c) == len(cols) and c[0].isdigit() and q is not None and " — /" in c[r]:
                out.append((c[q], c[r], ("PAA" if "paa" in rel else "fan-out") + f" #{c[0]}"))
    return out


def faq_candidates(slug, st, pid):
    """[{id, question, source, seen}] for one page: the pack's questions, then the worksheet rows routed to its URL (or,
    for a location page, to its city's page under an older URL)."""
    p = st["pages"][pid]
    pk = (p.get("pack") or {}).get("json")
    pack = read_json(ROOT / pk, {}) if pk else {}
    out, seen = [], set()

    def add(q, src, n=""):
        k = re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()
        if q and k not in seen:
            seen.add(k)
            out.append({"id": f"q{len(out) + 1}", "question": q, "source": src, "seen": str(n)})
    for x in (pack or {}).get("questions") or []:
        add(x.get("q") or "", f"pack {x.get('kind', '')}".strip(), x.get("seen", ""))
    mine = _path(p.get("url"))
    city = (p.get("city") or (p.get("name") or "").split(",")[0]).strip().lower()
    cslug = re.sub(r"[^a-z0-9]+", "-", city).strip("-")
    for q, route, src in routed(slug):
        target = route.split(" — ", 1)[1].strip().strip("/")
        if target == mine or (p.get("type") == "location" and cslug and target.split("/")[-1].startswith(cslug)):
            add(q, f"{src} ({route.split(' — ')[0]})")
    return out[:40]


def faq(slug, section, run_id, confirmed=False):
    """FAQ fit picks for every page of a section in one llm.py faq-picks job. Picks are candidates only — a question
    that is not in the list is never kept. No API key: nothing is written; the writer picks from the outline's
    candidates and reports each, as before."""
    import llm
    import run as R
    R.open_run(slug, run_id)
    st = S.load(slug)
    b = S.batch(st, section) or die(f"no section {section} in the site plan")
    bg = brand_guide(slug)
    items, cands = [], {}
    for pid in b["pages"]:
        p = st["pages"][pid]
        c = faq_candidates(slug, st, pid)
        if not c:
            continue
        cands[pid] = {x["id"]: x for x in c}
        items.append({"id": pid, "type": p.get("type", ""), "name": p.get("name") or pid, "url": p.get("url", ""),
                      "city": p.get("city") or "", "candidates": c,
                      **({"categories": [f"{n} = {c_}: {w}" for n, (c_, w) in enumerate(LOC_FAQ, 1)]}
                         if p.get("type") == "location" else {})})
    if not items:
        print(f"section {section}: no FAQ candidates for any page (no routed PAA or fan-out rows, no pack questions)")
        return
    owned = sorted({h for h, _ in used_elsewhere(bg, "")})[:200]
    ans = llm.attempt(slug, run_id, "faq-picks", {"business": st["client"].get("name", ""), "owned_elsewhere": owned},
                      items, f"FAQ picks for section {section} ({len(items)} page(s))",
                      "the writer picks the FAQs from the outline's candidates and reports each", confirmed)
    if ans is None:
        return
    out = {}
    for pid, a in ans.items():
        keep, cats = [], set()
        for k in a.get("picks") or []:
            c = cands.get(pid, {}).get(k.get("candidate"))
            if not c or (st["pages"][pid].get("type") == "location" and (k["category"] not in ("1", "2", "3")
                                                                         or k["category"] in cats)):
                continue
            cats.add(k["category"])
            keep.append({"question": c["question"], "category": k["category"], "source": c["source"],
                         "why": k.get("why", "")})
        out[pid] = keep
    d = client_dir(slug) / "build" / section
    d.mkdir(parents=True, exist_ok=True)
    from lib import write_json
    write_json(d / "faq-picks.json", {"made": now(), "run": run_id, "model": llm.JOBS["faq-picks"]["model"],
                                      "pages": out})
    R.log_change(slug, run_id, "llm_judgment", f"build/{section}/faq-picks.json", "FAQ picks", "",
                 f"{sum(len(v) for v in out.values())} pick(s) for {len(out)} page(s)", "DONE", channel="local")
    print(f"section {section}: FAQ picks for {len(out)} of {len(items)} page(s) on the Claude API → "
          f"build/{section}/faq-picks.json (each outline shows them)")


def faq_picks(slug, section, pid):
    f = client_dir(slug) / "build" / section / "faq-picks.json"
    return ((read_json(f, {}) or {}).get("pages") or {}).get(pid) if f.is_file() else None


def render(slug, st, b, pid, pack, run_id):
    p = st["pages"][pid]
    ptype = p.get("type", "")
    spec, elements = spec_elements(ptype)
    bg = brand_guide(slug)
    ev, ev_rec = S.evidence_state(st, pid)
    pc = client_dir(slug) / "build" / "pilot-corrections.md"
    out = [f"# Outline — {p.get('name') or pid} ({ptype})", "",
           f"Page `{pid}` · section `{b['id']}` · run {run_id} · derived {now()[:16]} by outline.py (Rewrite 4: no "
           "brief — nothing in this file is a decision; the plan, the spec and the pack are).",
           f"Final URL: {p.get('url', '')}"
           + (f" · replaces {', '.join(p['replaces'])} (301 — a VA handoff)" if p.get("replaces") else "")
           + (f" · group {p['group']}" if p.get("group") else ""),
           f"Spec: `{spec.relative_to(ROOT) if spec else 'none'}` · Pack: `{(p.get('pack') or {}).get('file', '')}`"
           + (f" · Pilot corrections: `{pc.relative_to(ROOT)}`" if pc.is_file() else "")
           + (" · FAQ recipe: `methodology/location-faq.md`" if ptype == "location" else ""),
           f"Evidence gate: {ev or 'not run'}" + (f" — gaps: {'; '.join(ev_rec.get('why') or [])}" if ev in ("warn", "block") else ""),
           "", "## Fixed by the approved site plan", "", "| Field | Value |", "|---|---|"]
    fixed = [(lab, p[k]) for k, lab in PLAN_FIELDS if p.get(k)]
    out += [f"| {lab} | {', '.join(v) if isinstance(v, list) else v} |" for lab, v in fixed]
    assigned = {k: va for k, va in formula(st, pid, bg_entity(bg)).items() if not p.get(k)}
    if assigned:
        out += ["", "## Assigned by formula (outline.py — the site-plan row left these empty; use them as given)", "",
                "| Field | Value | Formula and source |", "|---|---|---|"]
        out += [f"| {lab} | {assigned[k][0]} | {assigned[k][1]} |" for k, lab in PLAN_FIELDS if k in assigned]
    wanted = ("keyword", "h1", "service_variant") if ptype == "service" else ("keyword", "h1")
    open_ = [lab for k, lab in PLAN_FIELDS if k in wanted and not p.get(k) and k not in assigned]
    if open_:
        out += ["", f"Open — the Brand Guide gives no formula input, so the writer chooses, reports it, and it is listed on the "
                f"review sheet: {', '.join(open_)}"]
    out += ["", "## Variants", ""]
    res = code_block(md_section(bg, r"B1\b"))
    pool = code_block(md_section(bg, r"B2\b"))
    cat = next((f["value"] for f in pack.get("facts", []) if f["id"].startswith("a-category-variants")), "")
    out += [f"- Reserved for the homepage — never on this page: {' · '.join(res) or 'none recorded'}" if ptype != "homepage"
            else f"- Reserved for this page: {' · '.join(res) or 'none recorded'}",
            f"- Area rotation pool (B2): {' · '.join(pool) or 'none recorded'}",
            f"- Category variants (A3): {cat or 'none recorded'}",
            "- No variant at two consecutive steps URL → title → H1 → first H2 (BB-108, CM-024)."]
    mine = [f"{lab.lower()} {assigned[k][0]}" for k, lab in PLAN_FIELDS[4:6] if k in assigned]
    out += ([f"- Assigned to this page by formula: {' · '.join(mine)}"] if mine else []) + [""]
    out += ["## Page order (the spec, §3 — every row is a requirement)", "", "| # | Element | Requirement |", "|---|---|---|"]
    out += [f"| {n} | {e} | {r} |" for n, e, r in elements] or ["| — | the spec has no element table | |"]
    picks = faq_picks(slug, b["id"], pid)
    if picks:
        out += ["", "## FAQ picks (outline.py faq on the Claude API — use these, in this order; report each)", ""]
        out += [f"- {('cat ' + k['category'] + ' · ') if k.get('category') else ''}{k['question']} — {k['source']}"
                for k in picks]
    out += ["", "## FAQ candidates", ""]
    if ptype == "location":
        out += ["Three questions, one per category (none already owned below):", ""]
        out += [f"- **{c}** — {w}" for c, w in LOC_FAQ] + [""]
    qs = pack.get("questions") or []
    out += [f"- [{q.get('kind')}] {q.get('q')} — seen {q.get('seen')}×" for q in qs[:20]] or [
        "- None tagged to this page in the pack: use the place research's local questions, then review language "
        "(location-faq.md order); list the source of each pick in the results file."]
    used = used_elsewhere(bg, p.get("url"))
    out += ["", "## Already owned by another page — never repeated (Brand Guide C3)", ""]
    owners = {}
    for h_, o in used:
        owners.setdefault(o, []).append(h_)
    out += [f"- {o}: " + " · ".join(hs) for o, hs in owners.items()] or ["- none yet"]
    out += ["", "## Links — table rows only, left as placeholders for Finish (no cross-page link in prose)", ""]
    for label, rows in link_rows(st, pid).items():
        out.append(f"- {label}: " + (" · ".join(f"{n} ({u})" for n, u in rows) if rows else "none planned"))
    out += ["", "## Claims", ""]
    rows = {s: [f for f in pack.get("facts", []) if facts.writer_state(f.get("status")) == s] for s in facts.WRITER_STATES}
    out += ["Every fact is in the pack's Facts section, in its state: " + " · ".join(
        f"{len(rows[s])} {s}" for s in facts.WRITER_STATES) + " — **confirmed** is a plain claim, **sourced public** a "
        "plain statement, **unknown** is never claimed.", "",
        "### Unknown — never claimed: `[NEED: …]` where the page needs it, or leave it out", ""]
    out += [f"- `{f['id']}` {f['label']}" for f in rows["unknown"]
            if not f["id"].startswith(VARIANT_ROWS)] or ["- none"]   # variants are names, not claims (see Variants)
    out.append("")
    places = sorted({r.get("place", "") for r in pack.get("place", []) if r.get("place")})
    if places:
        out += [f"Place entities in the pack (name only what the pack states): {' · '.join(places)}", ""]
    reviews = pack.get("reviews") or {}
    if reviews:
        out += ["Reviews (use only at the tier the pack gives): "
                + " · ".join(f"{t} ({v.get('tier')}, {v.get('reviewers')} reviewer(s))" for t, v in reviews.items()), ""]
    d2 = never_reuse(bg)
    out += ["### Never reuse (Brand Guide D2)", ""]
    out += [f"- {c}" + (f" → {act}" if act else "") for c, act in d2] or ["- none recorded"]
    out += ["", "## The writer reports (results file → the draft review sheet)", "",
            "Keyword · SEO title · meta description · H1 · the variants used where · every H2 · each FAQ question with "
            "its category and source · the place entities named · every `[NEED: …]` and `[LINK → …]` left. Each "
            "choice the plan did not fix is a **Fix and list** row; a legal or money claim from the site is an Ask.", ""]
    return "\n".join(out)


def build(slug, section, run_id, page=None):
    st = S.load(slug)
    b = S.batch(st, section) or die(f"no section {section} in the site plan")
    if S.route(b) != "outline":
        die(f"section {section} is on the brief route (its briefs were approved before Rewrite 4) — it keeps briefs; "
            "outline.py is for sections on the outline route (migrate.py).", 4)
    info = (st.get("open_runs") or {}).get(run_id) or {}
    if info.get("step") != "build:write" or info.get("batch") not in (None, section):
        die(f"an outline is written only inside the section's /build write run (run {run_id} is "
            f"{info.get('step') or 'not open'}).", 4)
    if S.batch_stage_ok(st, section, "drafts", False)[0]:
        die(f"section {section} drafts are already approved; Paul re-opens them first (--decision revise).", 4)
    todo = [page] if page else list(b["pages"])
    done, skipped = [], []
    for pid in todo:
        if pid not in b["pages"]:
            die(f"{pid} is not in section {section}")
        ok, why = S.evidence_ok(st, pid)
        pk = (st["pages"][pid].get("pack") or {})
        if not ok or not pk.get("json") or not (ROOT / pk["json"]).is_file():
            skipped.append(f"{pid} ({why or 'no evidence pack — evidence.py run builds it'})")
            continue
        pack = read_json(ROOT / pk["json"], {}) or {}
        text = render(slug, st, b, pid, pack, run_id)
        st["pages"][pid]["assigned"] = {k: v for k, (v, _) in formula(st, pid, bg_entity(brand_guide(slug))).items()
                                        if not st["pages"][pid].get(k)}
        d = client_dir(slug) / "build" / section / "outlines"
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{pid}.md"
        f.write_text(text, encoding="utf-8")
        st["pages"][pid].setdefault("files", {})["outline"] = {
            "file": str(f.relative_to(ROOT)), "run": run_id, "at": now(), "sha": sha12(f), "ts": time.time(),
            "pack_sha": pk.get("sha")}
        done.append(pid)
    S.save(slug, st)
    if done:
        append(client_dir(slug) / "log.md", f"- OUTLINES {now()[:16]} · run {run_id} · section {section} · "
               f"{len(done)} page(s) by outline.py (no brief, Rewrite 4)\n")
    print(f"section {section}: {len(done)} outline(s) written by script"
          + (f"; no outline for {', '.join(skipped)}" if skipped else ""))
    return done, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("build"); s.add_argument("slug"); s.add_argument("section"); s.add_argument("--run", required=True)
    s.add_argument("--page")
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("page")
    s = sub.add_parser("faq"); s.add_argument("slug"); s.add_argument("section"); s.add_argument("--run", required=True)
    s.add_argument("--confirmed", action="store_true")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.slug, a.section, a.run, a.page)
        return
    if a.cmd == "faq":
        faq(a.slug, a.section, a.run, a.confirmed)
        return
    st = S.load(a.slug)
    rec = S.page_stage(st, a.page, "outline")
    if not rec:
        die(f"{a.page} has no outline (outline.py build {a.slug} <section> --run <RUN_ID>)")
    pk = (st["pages"][a.page].get("pack") or {})
    cur = (ROOT / rec["file"]).is_file() and sha12(ROOT / rec["file"]) == rec["sha"] and rec.get("pack_sha") == pk.get("sha")
    print(f"{rec['file']} · run {rec['run']} · {'current' if cur else 'STALE — the pack or the file changed; rebuild it'}")


if __name__ == "__main__":
    main()
