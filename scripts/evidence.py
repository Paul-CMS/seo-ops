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

Decide once and research before asking (Paul, 2026-10-09; CM-057). A fact that is not Known there is then looked up:
  1. an answer already settled under its facts key (`fact:<d|a>:<fact>` or `fact:<page>:<key>`, decisions-settled.md)
     — never asked again;
  2. every source on disk (scripts/sources.py: reviews, the client's site text, a GBP export, grid, rankings), each hit
     cited (file, row, date, quote) and marked per evidence-requirements.json → found_marks.
Each remaining gap says "searched, not found" with the sources listed. Only those become facts questions; a fact found
only on the client's own site is a one-line yes/no. Every question is asked once (run.py --ask under its facts key).

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
import settled
import sources
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
    """{'A:<field>': {...}, 'D:<fact>': {...}} with value, status, source — from facts.json, the one facts store (P4).
    A client not migrated yet is read from its Brand Guide rows (facts.load bootstraps them)."""
    import facts
    out = {}
    for r in facts.load(slug)["facts"]:
        out[f"{r['section']}:{r['label']}"] = {
            "value": r.get("value", ""), "status": r.get("status_text") or r.get("status", ""),
            "source": r.get("source") or (f"Brand Guide {r['section']}" if r["section"] == "A" else ""),
            "count": r.get("count"), "fact_id": r["id"]}
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
    status = re.sub(r"[\s_-]+", " ", str(rec.get("status") or "")).strip().lower()   # "paul_approved" = "Paul Approved"
    source = str(rec.get("source") or "").strip()
    # a status cell may carry a date or a note after the word ("Paul Approved 2026-10-06 · was: Submitted"): the
    # leading status word is what counts (P1)
    lead = next((k for k in KNOWN_STATES | {"disputed", "unknown", "submitted"} if status.startswith(k)), status)
    status = lead
    if status == "disputed":
        return "Conflict"
    if status.startswith("found — "):   # research before asking: the mark comes from found_marks (CM-057)
        return "Known" if status.endswith("known") and source else "Unverified"
    if not value or status == "unknown" or value.startswith("[NEED"):
        return "Unknown"
    if status in KNOWN_STATES and source:
        return "Known"
    if status.startswith("customer reported") and source and int(rec.get("count") or 0) >= int(
            requirements().get("review_min_independent") or 3):
        return "Known"   # CM-057: 3+ different reviewers; stated only as customers describe it
    return "Unverified"   # Submitted, no status, or no source


# ------------------------------------------------------------------ decide once + research before asking
def fact_key(pid, src):
    """The one key a fact is asked and answered under: shared Brand Guide facts once per client, page facts per page."""
    kind, _, key = src.partition(":")
    base = f"fact:{pid}:{key}" if kind == "page" else f"fact:{kind.lower()}:{key}"
    return re.sub(r"[^a-z0-9_.:-]+", "_", base.lower()).strip("_")[:60]


def settled_answer(ents, fk):
    e = ents.get(fk) or {}
    if e.get("state") != "settled":
        return None
    by = (e.get("by") or "").lower()
    return {"value": e["text"], "status": "Client Confirmed" if "client" in by else "Paul Approved",
            "source": f"answer {e['at'][:10]} ({e.get('by')}; decisions-settled.md {fk})", "via": "settled"}


def research(slug, it, page, docs):
    """(rec or None, searched) — a sourced value from the files on disk, or what was searched."""
    res = sources.search(slug, it["key"], page, docs, limit=None)
    if not res["hits"]:
        return None, res
    reqs = requirements()
    marks = reqs.get("found_marks") or {}
    need = int(reqs.get("review_min_independent") or 3)
    revs = [h for h in res["hits"] if h["kind"] == "review"]
    people = {h.get("reviewer") or h["label"] for h in revs}
    if len(people) >= need:   # CM-057: 3+ different reviewers, nothing conflicting → Known, stated as customers say it
        h = revs[0]
        return {"value": f"\"{h['quote']}\" (+{len(revs) - 1} more)", "status": "Found — " + marks.get("review", "Known"),
                "source": f"customer_reported: {len(people)} different reviewers, e.g. {h['label']} · state it only as "
                          "customers describe it ('customers mention…'); prices, timelines and warranty terms only as a "
                          "cited customer example (CM-057)", "via": "review", "count": len(people)}, res
    h = next((x for x in res["hits"] if x["kind"] != "review"), res["hits"][0])
    if h["kind"] == "review":
        return {"value": f"\"{h['quote']}\"", "status": "Found — Unverified",
                "source": f"customer_reported: only {len(people)} reviewer(s) — CM-057 needs {need} · {h['label']}",
                "via": "review", "count": len(people)}, res
    more = f" (+{len(res['hits']) - 1} more)" if len(res["hits"]) > 1 else ""
    return {"value": f"\"{h['quote']}\"{more}", "status": "Found — " + marks.get(h["kind"], "Unverified"),
            "source": h["label"], "via": h["kind"]}, res


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
    ents = settled.entries(slug)
    docs = None
    # CM-049: a keyword or variant the site plan flagged as carrying a claim makes that fact required
    items = items + [{"key": f"claim:{c.get('phrase', i)}", "label": f"Claim in '{c.get('phrase')}': {c.get('label')}",
                      "need": "required", "from": c["from"]} for i, c in enumerate(page.get("claims") or [])]
    rows = []
    for it in items:
        rec = lookup(it["from"], bf, pf)
        fk = fact_key(pid, it["from"])
        searched = None
        if mark(rec) not in ("Known", "Conflict"):
            ans = settled_answer(ents, fk)
            if ans:
                rec = ans
            elif mark(rec) == "Unknown":
                docs = sources.documents(slug) if docs is None else docs
                found, searched = research(slug, it, page, docs)
                rec = found or rec
        rows.append({**it, "mark": mark(rec), "value": (rec or {}).get("value", ""), "fact_key": fk,
                     "fact_id": (rec or {}).get("fact_id"),
                     "source": (rec or {}).get("source", ""), "status": (rec or {}).get("status", ""),
                     "via": (rec or {}).get("via", ""), "searched": searched})
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
    searched, missing = set(), set()
    for r in rows:
        v = str(r["value"]).replace("|", "/")[:240]
        src = str(r["source"]).replace("|", "/")
        sr = r.get("searched")
        if sr and sr.get("terms"):
            searched |= set(sr["searched"]); missing |= set(sr["missing"])
            if r["mark"] == "Unknown":
                src = f"searched, not found ({len(sr['searched'])} source(s) on disk)"
        elif sr is not None and not sr.get("terms") and r["mark"] == "Unknown":
            src = "not searchable on disk — ask"
        out.append(f"| {r['label']} | {r['need']} | **{r['mark']}** | {v} | {src} |")
    if searched or missing:
        out += ["", "**Sources searched before asking (CM-057):** " + (", ".join(sorted(searched)) or "none on disk"),
                "", "**Not on disk:** " + (", ".join(sorted(missing)) or "—")]
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
    if r.get("via") in ("site", "gbp"):   # CM-057: the client's own site or GBP — one yes/no line
        return (f"Your website says this about **{r['label']}**: {r['value']} ({r['source']}). Still true? yes / no — "
                "correction", "Verify")
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
    seen, qs, waiting = {}, [], {}
    ents = settled.entries(slug)
    for pid in blocked:
        rows, *_ = grid(slug, st, pid)
        for r in sorted(rows, key=lambda r: (r["need"] != "required", r["mark"] != "Conflict")):
            if r["mark"] == "Known":
                continue
            k = r["fact_key"]
            if (ents.get(k) or {}).get("state") in ("open", "answered"):   # asked once already — never again
                waiting.setdefault(k, ents[k])
                continue
            if k in seen:
                seen[k]["pages"].append(pid)
                continue
            text, kind = question(r)
            seen[k] = {"text": text, "kind": kind, "need": r["need"], "pages": [pid], "from": r["from"], "key": k,
                       "fact_id": r.get("fact_id"), "searched": r.get("searched")}
            qs.append(seen[k])
    qs, _dropped, answered = settled.filter_questions(slug, qs)   # P4: never ask what is already answered
    cap = 15
    qs = qs[:cap]
    for q in qs:   # asked once: the key is what the answer settles (run.py decision --settle <key>)
        settled.ask(slug, run_id, q["key"], "Client (via Paul)", re.sub(r"\*\*", "", q["text"])[:300])
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
    lines += [f"  - Q{i}: {q['from']} ({q['need']}) → pages {', '.join(q['pages'])} · {q['kind']} · key {q['key']}"
              + (f" · searched first: {', '.join(q['searched']['searched']) or 'nothing on disk'}" if q.get("searched") else "")
              for i, q in enumerate(qs, 1)]
    if answered:
        lines += [f"- {answered[0].upper()}{answered[1:]} (not asked again)"]
    if waiting:
        lines += ["- Already asked, not repeated here: " + ", ".join(f"{k} ({e.get('asked_at', '')[:10]})" for k, e in waiting.items())]
    lines += ["- Each answer is recorded once under its key: run.py decision <slug> <RUN_ID> --settle <key> --by",
              "  \"Client (via Paul)\" --text \"<answer>\" (and into Brand Guide Section D or the page facts file); then",
              "  /interview <slug> facts-answers <batch> re-runs the gate, which reads the settled answers.",
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
