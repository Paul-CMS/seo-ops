#!/usr/bin/env python3
"""evidence.py — the evidence gate (CM-041). Runs before any brief; a blocked page gets no brief.

    evidence.py run <slug> --run R (--batch B | --page P)     build, score and record each page's grid
    evidence.py show <slug> <page_id>                         print a page's grid and result
    evidence.py questions <slug> --run R --batch B            the facts interview pack for the batch's
                                                              blocked pages (CM-042) — Paul sends it

Each page's grid lists the facts its spec needs (methodology/evidence-requirements.json → types),
each marked Known / Unknown / Unverified / Conflict from Brand Guide Sections A and D and the page's
own facts file (clients/<slug>/build/evidence/<page_id>.facts.json, written by the Build agent from
the proof sheet, Discovery Record and research — value, status, source per fact). The script does
the marking and the scoring; nobody types a result.

Result: pass · warn (the brief must carry an "Evidence gaps" section) · block (no brief until the
facts interview fills the gaps and the gate re-runs, or Paul waives it with
`/approve <slug> evidence:<page_id> --reason "..."`). Thresholds: evidence-requirements.json.
The grid is written to clients/<slug>/build/evidence/<page_id>.grid.md; its sha is recorded, so a
waiver stops counting the moment the grid changes.
"""
import argparse
import json
import re
import sys

import run as R
import status as S
from lib import ROOT, append, client_dir, die, now, read_json, sha12, today

REQ = ROOT / "methodology" / "evidence-requirements.json"
KNOWN_STATES = {"client confirmed", "paul approved", "internally verified"}


def requirements():
    return read_json(REQ)


# ------------------------------------------------------------------ Brand Guide
def _section_rows(text, letter):
    """Table rows (cells) of Brand Guide Section <letter>, stopping at the next ## heading.
    Only the section's main table — subsections (### D2 …) are not facts a writer may state."""
    m = re.search(rf"^## Section {letter}\b.*$", text, re.M)
    if not m:
        return []
    rows = []
    for line in text[m.end():].splitlines():
        if line.startswith("## ") or line.startswith("### "):
            break
        if line.startswith("|") and not re.match(r"^\|[\s\-|:]+\|\s*$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:] if rows else []   # drop the header row


def brand_facts(slug):
    """{'A:<field>': {...}, 'D:<fact>': {...}} with value, status, source."""
    p = client_dir(slug) / "brand-guide.md"
    text = p.read_text() if p.exists() else ""
    out = {}
    for cells in _section_rows(text, "A"):
        if len(cells) >= 4:
            out["A:" + cells[1]] = {"value": cells[2], "status": cells[3], "source": "Brand Guide A"}
    for cells in _section_rows(text, "D"):
        if len(cells) >= 4:
            out["D:" + cells[0]] = {"value": cells[1], "status": cells[2], "source": cells[3]}
    return out


def page_facts(slug, pid):
    p = client_dir(slug) / "build" / "evidence" / f"{pid}.facts.json"
    return (read_json(p) or {}).get("facts", {}), p


def lookup(src, bf, pf):
    kind, _, key = src.partition(":")
    if kind == "page":
        return pf.get(key)
    want = key.lower()
    for k, v in bf.items():
        if k.startswith(kind + ":") and k[2:].lower().startswith(want):
            return v
    return None


def mark(rec):
    """Known / Unknown / Unverified / Conflict, from the Brand Guide status vocabulary."""
    if not rec:
        return "Unknown"
    value = str(rec.get("value") or "").strip()
    status = str(rec.get("status") or "").strip().lower()
    source = str(rec.get("source") or "").strip()
    if status == "disputed":
        return "Conflict"
    if not value or status == "unknown" or value.startswith("[NEED"):
        return "Unknown"
    if status in KNOWN_STATES and source:
        return "Known"
    return "Unverified"   # Submitted, no status, or no source


# ------------------------------------------------------------------ scoring
def score(rows, th):
    gap = lambda r: r["mark"] != "Known"
    req_gaps = [r for r in rows if r["need"] == "required" and gap(r)]
    sup_gaps = [r for r in rows if r["need"] != "required" and gap(r)]
    conflicts = [r for r in rows if r["mark"] == "Conflict"]
    known = [r for r in rows if r["mark"] == "Known"]
    why = []
    if th.get("block_if_any_required_conflict") and any(r["need"] == "required" for r in conflicts):
        why.append("a required fact is in conflict: " + ", ".join(r["label"] for r in conflicts if r["need"] == "required"))
    if len(req_gaps) >= th["block_if_required_gaps_at_least"]:
        why.append(f"{len(req_gaps)} required facts are not known (block at {th['block_if_required_gaps_at_least']})")
    if len(known) < th["block_if_known_below"]:
        why.append(f"only {len(known)} known fact(s) — fewer than {th['block_if_known_below']} (CM-015)")
    if why:
        result = "block"
    elif not req_gaps and not conflicts and len(sup_gaps) <= th["pass_max_supporting_gaps"]:
        result = "pass"
    else:
        result = "warn"
        why.append(f"{len(req_gaps)} required and {len(sup_gaps)} supporting gap(s), {len(conflicts)} conflict(s) — "
                   "the brief must list them under 'Evidence gaps'")
    counts = {m: sum(r["mark"] == m for r in rows) for m in ("Known", "Unknown", "Unverified", "Conflict")}
    return result, counts, why


def grid(slug, st, pid):
    page = st["pages"].get(pid) or die(f"page {pid} is not in the site plan")
    reqs = requirements()
    items = reqs["types"].get(page.get("type"))
    if items is None:
        die(f"no evidence requirements for page type {page.get('type')!r} (methodology/evidence-requirements.json)")
    bf = brand_facts(slug)
    pf, pf_path = page_facts(slug, pid)
    # CM-049: a keyword or variant the site plan flagged as carrying a claim makes that fact required
    items = items + [{"key": f"claim:{c.get('phrase', i)}", "label": f"Claim in '{c.get('phrase')}': {c.get('label')}",
                      "need": "required", "from": c["from"]} for i, c in enumerate(page.get("claims") or [])]
    rows = []
    for it in items:
        rec = lookup(it["from"], bf, pf)
        rows.append({**it, "mark": mark(rec), "value": (rec or {}).get("value", ""),
                     "source": (rec or {}).get("source", ""), "status": (rec or {}).get("status", "")})
    result, counts, why = score(rows, reqs["thresholds"])
    return rows, result, counts, why


def render(st, pid, rows, result, counts, why):
    p = st["pages"][pid]
    out = [f"# Evidence grid — {p.get('name') or pid} ({p.get('type')})", "",
           f"**Result: {result.upper()}** · Known {counts['Known']} · Unknown {counts['Unknown']} · "
           f"Unverified {counts['Unverified']} · Conflict {counts['Conflict']} (CM-041)", "",
           "_The grid holds only the facts, so its fingerprint changes only when a fact changes (a waiver is tied to it)._", ""]
    out += [f"- {w}" for w in why] + ([""] if why else [])
    out += ["| Fact | Need | Mark | Value | Source |", "|---|---|---|---|---|"]
    for r in rows:
        v = str(r["value"]).replace("|", "/")[:120]
        out.append(f"| {r['label']} | {r['need']} | **{r['mark']}** | {v} | {str(r['source']).replace('|', '/')} |")
    return "\n".join(out) + "\n"


def record(slug, run_id, pid):
    st = S.load(slug)
    rows, result, counts, why = grid(slug, st, pid)
    d = client_dir(slug) / "build" / "evidence"
    d.mkdir(parents=True, exist_ok=True)
    gp = d / f"{pid}.grid.md"
    gp.write_text(render(st, pid, rows, result, counts, why))
    rel = str(gp.relative_to(ROOT))
    st = S.load(slug)
    prev = (st["pages"][pid].get("evidence") or {})
    st["pages"][pid]["evidence"] = {"result": result, "counts": counts, "why": why, "grid": rel,
                                    "sha": sha12(gp), "at": now(), "run": run_id,
                                    "gaps": [r["key"] for r in rows if r["mark"] != "Known"],
                                    **({"waiver": prev["waiver"]} if prev.get("waiver") else {})}
    S.save(slug, st)
    append(client_dir(slug) / "log.md", f"- EVIDENCE {now()[:16]} · run {run_id} · {pid}: {result.upper()} "
           f"(known {counts['Known']}, unknown {counts['Unknown']}, unverified {counts['Unverified']}, "
           f"conflict {counts['Conflict']})\n")
    return result, counts, why, rel


# ------------------------------------------------------------------ facts interview pack (CM-042)
def question(r):
    if r["mark"] == "Conflict":
        return (f"We found different versions of **{r['label']}**: \"{r['value']}\" ({r['source'] or 'no source'}). "
                "Which is right?", "Verify")
    if r["mark"] == "Unverified":
        return (f"We have **{r['label']}** as \"{r['value']}\" (from {r['source'] or 'an unconfirmed source'}). "
                "Is that right? yes / partly — correction / no", "Verify")
    return (f"**{r['label']}** — what should we say? If it depends, on what?", "Describe")


def facts_pack(slug, run_id, bid):
    st = S.load(slug)
    b = S.batch(st, bid) or die(f"no batch {bid}")
    blocked = [p for p in b["pages"] if S.evidence_state(st, p)[0] == "block"]
    if not blocked:
        die(f"batch {bid}: no page is blocked by the evidence gate — the facts interview runs only on a block (CM-042).")
    seen, qs = {}, []
    for pid in blocked:
        rows, *_ = grid(slug, st, pid)
        for r in sorted(rows, key=lambda r: (r["need"] != "required", r["mark"] != "Conflict")):
            if r["mark"] == "Known":
                continue
            k = r["from"] if not r["from"].startswith("page:") else f"{pid}:{r['from']}"
            if k in seen:
                seen[k]["pages"].append(pid)
                continue
            text, kind = question(r)
            seen[k] = {"text": text, "kind": kind, "need": r["need"], "pages": [pid], "from": r["from"]}
            qs.append(seen[k])
    cap = 15
    qs = qs[:cap]
    name = st["client"]["name"]
    d = client_dir(slug) / "interviews" / "facts"
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"{name} - Facts Interview - {bid} - {today()} - REVIEW.md"
    lines = [f"# {name} — a few facts we need before we write", "",
             "Quick ones — answer by reply, voice memo or a five-minute call. \"I don't know\" is a fine answer.", ""]
    for i, q in enumerate(qs, 1):
        lines.append(f"{i}. {q['text']}")
        if q["kind"] == "Describe":
            lines.append("   *Can we say this on your website?* yes / only in general terms / no")
    lines += ["", "<!-- System notes (removed before sending):",
              f"- Facts interview (CM-042) for blocked page(s): {', '.join(blocked)} · evidence gate CM-041",
              "- Each question → the fact it fills:"]
    lines += [f"  - Q{i}: {q['from']} ({q['need']}) → pages {', '.join(q['pages'])} · {q['kind']}" for i, q in enumerate(qs, 1)]
    lines += ["- Answers go into Brand Guide Section D (status Client Confirmed, source 'Facts interview <date>') or the",
              "  page facts file; then /interview <slug> facts-answers <batch> re-runs the gate.",
              "- Paul sends it. Nothing goes to the client automatically. -->", ""]
    f.write_text("\n".join(lines))
    rel = str(f.relative_to(ROOT))
    st = S.load(slug)
    S.batch(st, bid)["facts_interview"] = {"file": rel, "at": now(), "run": run_id, "pages": blocked,
                                           "questions": len(qs)}
    S.save(slug, st)
    append(client_dir(slug) / "log.md", f"- FACTS INTERVIEW {now()[:16]} · run {run_id} · batch {bid} · "
           f"{len(qs)} question(s) for {', '.join(blocked)} · {rel}\n")
    return rel, len(qs), blocked


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("run"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--batch"); s.add_argument("--page")
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("page")
    s = sub.add_parser("questions"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--batch", required=True)
    a = ap.parse_args()
    if a.cmd == "show":
        st = S.load(a.slug)
        rows, result, counts, why = grid(a.slug, st, a.page)
        print(render(st, a.page, rows, result, counts, why), end="")
        ok, why2 = S.evidence_ok(st, a.page)
        print(f"\nGate: {'open' if ok else 'closed — ' + why2}")
        return
    R.open_run(a.slug, a.run)
    if a.cmd == "questions":
        rel, n, blocked = facts_pack(a.slug, a.run, a.batch)
        print(f"facts interview: {n} question(s) for {', '.join(blocked)} → {rel}\nPaul reviews and sends it.")
        return
    st = S.load(a.slug)
    if a.batch:
        b = S.batch(st, a.batch) or die(f"no batch {a.batch}")
        pids = b["pages"]
    elif a.page:
        pids = [a.page]
    else:
        die("give --batch or --page")
    blocked = 0
    for pid in pids:
        result, counts, why, rel = record(a.slug, a.run, pid)
        blocked += result == "block"
        print(f"{pid:28} {result.upper():5}  known {counts['Known']} · unknown {counts['Unknown']} · "
              f"unverified {counts['Unverified']} · conflict {counts['Conflict']}  ({rel})")
        for w in why:
            print(f"{'':28}   - {w}")
    if blocked:
        print(f"\n{blocked} page(s) blocked: no brief for them until the facts interview fills the gaps "
              "(/interview <slug> facts <batch>) or Paul waives (/approve <slug> evidence:<page_id> --reason \"...\").")
    sys.exit(0)


if __name__ == "__main__":
    main()
