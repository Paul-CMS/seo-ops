#!/usr/bin/env python3
"""outline.py — each page's outline, derived by script at draft time (Rewrite 4 Phase 4: no brief step).

    outline.py build <slug> <section> --run R [--page P]   write and record the outline of every page in the section
                                                          that cleared the evidence gate (or one page)
    outline.py show <slug> <page>                          print a page's outline path and whether it is current

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
Whatever the outline leaves open (keyword, H1 wording, variants, H2 wording, FAQ picks) the writer chooses and
reports in its results file; each choice is a "Fix and list" row on the section's one draft review sheet (CM-061).
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
    wanted = ("keyword", "h1", "service_variant") if ptype == "service" else ("keyword", "h1")
    open_ = [lab for k, lab in PLAN_FIELDS if k in wanted and not p.get(k)]
    if open_:
        out.append(f"| Open — the writer chooses, reports it, and it is listed on the review sheet | {', '.join(open_)} |")
    out += ["", "## Variants", ""]
    res = code_block(md_section(bg, r"B1\b"))
    pool = code_block(md_section(bg, r"B2\b"))
    cat = next((f["value"] for f in pack.get("facts", []) if f["id"].startswith("a-category-variants")), "")
    out += [f"- Reserved for the homepage — never on this page: {' · '.join(res) or 'none recorded'}" if ptype != "homepage"
            else f"- Reserved for this page: {' · '.join(res) or 'none recorded'}",
            f"- Area rotation pool (B2): {' · '.join(pool) or 'none recorded'}",
            f"- Category variants (A3): {cat or 'none recorded'}",
            "- No variant at two consecutive steps URL → title → H1 → first H2 (BB-108, CM-024).", ""]
    out += ["## Page order (the spec, §3 — every row is a requirement)", "", "| # | Element | Requirement |", "|---|---|---|"]
    out += [f"| {n} | {e} | {r} |" for n, e, r in elements] or ["| — | the spec has no element table | |"]
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
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.slug, a.section, a.run, a.page)
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
