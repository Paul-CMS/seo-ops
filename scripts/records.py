#!/usr/bin/env python3
"""records.py — the human-readable records, generated one-way from status.json and log.md.

    records.py render <slug>
    records.py top <slug>     STATUS.md's top four lines (stage, what is happening, waiting on, next action)

Writes (overwrites) in clients/<slug>/:
  handoff-log.md        every run's handoff section (run.py finish --handoff <file>), oldest first
  decisions.md          decisions summary: Paul's approvals, logged decisions (run.py decision),
                        conditions met, aborted runs
  document-checklist.md what is in, skipped or missing — from the audit-step outcomes, conditions
                        and decisions
  approval-record.md    the Drive Approval Record (status.py approval-record)
  decisions-settled.md  every settled decision, one line each — agents never re-raise them (R6)
  STATUS.md             one page a VA can read at any moment (R7): stage, now, waiting on, next, settled, VA items, spend

These files are never edited by hand (the guard hook blocks it): change the source — run a
command, record a decision, approve — and they are regenerated. run.py finish/abort and
approve.py call render automatically.
"""
import re
import sys

import status as S
import steps
from lib import client_dir, now

HANDOFF = re.compile(r"^### HANDOFF · (.+?)\n(.*?)^### END HANDOFF", re.M | re.S)


def _log(slug):
    p = client_dir(slug) / "log.md"
    return p.read_text() if p.exists() else ""


def handoff_log(st, log):
    name = st["client"]["name"]
    out = [f"# {name} - Handoff Log", "",
           "Generated from the safety log (clients/{}/log.md) — do not edit. Each run adds its section "
           "with `run.py finish --handoff <file>`. The newest section is at the bottom.".format(st["client"]["slug"]), ""]
    found = HANDOFF.findall(log)
    if not found:
        out.append("_No handoff sections yet._")
    for head, body in found:
        out += [f"## {head.strip()}", "", body.strip(), ""]
    return "\n".join(out) + "\n"


def decisions(st, log):
    name = st["client"]["name"]
    out = [f"# {name} - Decisions", "",
           "Generated from status.json and the safety log — do not edit. Record a decision with "
           "`run.py decision <slug> <RUN_ID> --text \"...\" [--ids F-001,...]` (Paul Exceptions, applied "
           "defaults, N/A rationales, deviations, Gate B outcome). Standing exception for audits: CM-026.", "",
           "## Paul's approvals", "", "| When | What | Decision |", "|---|---|---|"]
    for m in re.finditer(r"^## APPROVAL · (\S+) · (.+?) · (\w+) · by Paul$", log, re.M):
        out.append(f"| {m.group(1)[:16]} | {m.group(2)} | {m.group(3)} |")
    for m in re.finditer(r"^## APPROVAL · (\S+) · import confirmed by Paul$", log, re.M):
        out.append(f"| {m.group(1)[:16]} | import from Drive | confirmed |")
    out += ["", "## Decisions logged during runs", ""]
    ds = re.findall(r"^- DECISION (.+)$", log, re.M)
    out += [f"- {d}" for d in ds] or ["_None yet._"]
    out += ["", "## Conditions met (system-verified)", ""]
    cs = re.findall(r"^## CONDITION · (\S+) · (.+)$", log, re.M)
    out += [f"- {c[0][:16]} — {c[1]}" for c in cs] or ["_None yet._"]
    ab = re.findall(r"^## RUN (\S+) · ABORTED · (\S+)\nReason \(Paul\): (.+)$", log, re.M)
    if ab:
        out += ["", "## Runs aborted (Paul's call)", ""] + [f"- {r[1][:16]} {r[0]} — {r[2]}" for r in ab]
    return "\n".join(out) + "\n"


def checklist(st):
    name = st["client"]["name"]
    out = [f"# {name} - Document Checklist", "",
           f"Generated {now()[:16]} from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · "
           "`[!]` failed · `[ ]` not yet.", ""]
    if st["client"]["type"] != "blog-only":
        out += ["## Evidence and data steps (methodology/audit-steps.md)", "",
                "| | Step | Outcome | Reason / output |", "|---|---|---|---|"]
        have = st.get("audit_steps") or {}
        for r in steps.registry():
            h = have.get(r["id"])
            box = {"done": "[x]", "skipped": "[-]", "failed": "[!]"}.get((h or {}).get("outcome"), "[ ]")
            detail = (h or {}).get("reason") or ", ".join((h or {}).get("outputs") or [])
            out.append(f"| {box} | {r['id']} {r['step'][:70]} | {(h or {}).get('outcome', '—')} | {detail} |")
        out.append("")
    out += ["## Conditions", ""]
    for c in S.GATES["conditions"]:
        if st["client"]["type"] == "blog-only" and c != "client_setup":
            continue
        ok, why = S.condition_met(st, c)
        out.append(f"- {'[x]' if ok else '[ ]'} {S.label(c)}" + ("" if ok else f" — {why}"))
    out += ["", "## Decisions (Paul)", ""]
    for g in S.visible_gates(st):
        ok, _ = S.gate_met(st, g)
        out.append(f"- {'[x]' if ok else '[ ]'} {S.label(g)}")
    if st["client"].get("practitioner_signoff"):
        named = any((p.get("approval") or {}).get("practitioner") for p in st["pages"].values()) or \
            any(((b.get("drafts") or {}).get("practitioner")) for b in S.batches(st))
        out += ["", "## Health content (CM-025)", "",
                f"- {'[x]' if named else '[ ]'} Licensed practitioner named on an approval"]
    return "\n".join(out) + "\n"


def settled_register(slug):
    """decisions-settled.md (R6): every settled decision, one line each. Agents read it and never re-raise them."""
    import settled
    st = S.load(slug)
    ents = settled.entries(slug)
    out = [f"# {st['client']['name']} - Settled decisions", "",
           "Generated from the safety log — do not edit. **Settled means settled: no agent asks these again.** New "
           "contradicting evidence → one `run.py decision <slug> <RUN_ID> --reopen <key> --text \"<evidence>\"`.", "",
           "## Paul's approvals", ""]
    aps = settled.approvals(slug)
    out += [f"- {when} — {what}: {dec}" for when, what, dec in aps] or ["_None yet._"]
    out += ["", "## Settled", ""]
    rows = [(k, e) for k, e in ents.items() if e.get("state") == "settled"]
    out += [f"- **{k}** ({e['at'][:10]}, {e.get('by') or '—'}): {e['text']}" for k, e in rows] or ["_None yet._"]
    opn = [(k, e) for k, e in ents.items() if e.get("state") == "open"]
    if opn:
        out += ["", "## Open questions — asked once, waiting for an answer", ""]
        out += [f"- **{k}** (asked {e.get('asked_at', '')[:10]}, waiting on {e.get('who')}): {e.get('question')}"
                for k, e in opn]
    ans = [(k, e) for k, e in ents.items() if e.get("state") == "answered"]
    if ans:
        out += ["", "## Answered — never asked again", ""]
        out += [f"- **{k}** (asked {e.get('asked_at', '')[:10]}): {e.get('question')} — answered by **{e.get('answered_by')}** "
                f"({e.get('answered_at', '')[:10]})" for k, e in ans]
    reo = [(k, e) for k, e in ents.items() if e.get("state") == "reopened"]
    if reo:
        out += ["", "## Reopened — waiting for Paul", ""]
        out += [f"- **{k}** (reopened {e.get('reopened_at', '')[:10]}): {e.get('reason')} — was: {e.get('text')}"
                for k, e in reo]
    n = settled.defects(slug)
    out += ["", f"Process defects (reopenings): **{n}**" + (" — a decision asked before the information that shapes it "
                                                            "existed; fix the order, not the decision." if n else "")]
    return "\n".join(out) + "\n"


DEFECTS = re.compile(r"<!-- reopenings:start -->.*?<!-- reopenings:end -->\n?", re.S)


def test_run_notes(slug):
    """R6: the reopening count goes into the client's test-run notes as a generated block."""
    import settled
    p = client_dir(slug) / "test-run-notes.md"
    ents = settled.entries(slug)
    lines = [f"- {k}: reopened {e['reopened']}×" for k, e in ents.items() if e.get("reopened")]
    block = ("<!-- reopenings:start -->\n## Process defects — decisions reopened (generated by records.py)\n\n"
             + (f"{settled.defects(slug)} reopening(s):\n" + "\n".join(lines) if lines else "None.") + "\n<!-- reopenings:end -->\n")
    text = p.read_text() if p.exists() else f"# {S.load(slug)['client']['name']} - test-run notes\n\n"
    if not lines and not DEFECTS.search(text):
        return
    new =DEFECTS.sub(block, text) if DEFECTS.search(text) else text.rstrip("\n") + "\n\n" + block
    if new != text:
        p.write_text(new)


def _open_handoffs(slug):
    """[(id, owner, kind, issued, open, total)] for every handoff with rows not done/verified."""
    import csv
    d = client_dir(slug) / "handoffs"
    out = []
    for f in sorted(d.glob("H-*.csv")) if d.exists() else []:
        m = re.match(r"^(H-(\d{4}-\d{2}-\d{2})-\d+-([a-z_]+))\.csv$", f.name)
        if not m:
            continue
        with open(f, newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))
        left = [r for r in rows if r.get("status") not in ("done", "verified")]
        if not left:
            continue
        md = f.with_suffix(".md")
        who = re.search(r"\*\*For:\*\* (\w+)", md.read_text()) if md.exists() else None
        owner = who.group(1) if who else (S.GATES["change_kinds"].get(m.group(3)) or {}).get("owner", "Gwen")
        out.append((m.group(1), owner, m.group(3).replace("_", " "), m.group(2), len(left), len(rows)))
    return out


def _spend(slug):
    import json
    p = client_dir(slug) / "dfs-costs.jsonl"
    rows = [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []
    return sum(float(r.get("actual_usd") or 0) for r in rows), sum(float(r.get("failed_usd") or 0) for r in rows)


def status_md(slug):
    """STATUS.md (R7): one page a VA can read at any moment — stage, what is happening, who waits on what, the next
    action, settled decisions (never re-raised), open VA items, spend. Plain language; mirrored to Drive."""
    import next as N
    import run as R
    import settled
    st = S.load(slug)
    c = st["client"]
    nx = N.compute(slug)
    left = R.unfinished(slug)
    stage = nx.get("stage") or "—"
    if left:
        info = (st.get("open_runs") or {}).get(left[0]) or {}
        now_line = f"run {left[0]} ({info.get('step', '?')}) started {info.get('started', '')[:16]} and has not finished"
    elif nx["kind"] == "run":
        now_line = f"ready to start: {nx['why']}"
    elif nx["kind"] == "decision":
        now_line = f"waiting for Paul's approval — {nx['why']}"
    elif nx["kind"] == "review":
        now_line = "Paul is reviewing what the last step produced; /next continues"
    else:
        now_line = nx["why"]
    lr = st.get("last_run") or {}
    since = (lr.get("finished") or st.get("updated") or "")[:10]
    waits = []
    if left:
        waits.append(("Paul", "decide what to do with the unfinished run (resume, /verify, /rollback or abort)", since, left[0]))
    if nx["kind"] in ("decision", "review"):
        waits.append(("Paul", nx["why"], since, nx["command"].split(" --")[0]))
    elif nx["kind"] == "wait" and not left:
        who = "Client (via Paul)" if re.search(r"client|owner", nx["why"]) else (
            "Jonie" if "Jonie" in nx["why"] else "Paul")
        waits.append((who, nx["why"], since, nx["command"]))
    for k, e in settled.entries(slug).items():
        if e.get("state") == "reopened":
            waits.append(("Paul", f"reopened decision '{k}': {e.get('reason')}", e.get("reopened_at", "")[:10], k))
        elif e.get("state") == "open":
            waits.append((e.get("who") or "Paul", e.get("question"), e.get("asked_at", "")[:10], k))
    hs = _open_handoffs(slug)
    # P8: while the system can run or Paul can decide, the VA's work and other waits do not block — listed apart
    side = []
    for w in nx.get("waits") or []:
        who = "Client (via Paul)" if re.search(r"client|owner", w["why"]) else ("Jonie" if "Jonie" in w["why"] else "Paul")
        side.append((who, w["why"], since, w["command"]))
    for hid, owner, kind, issued, n_open, n in hs:
        (waits if nx["kind"] == "wait" else side).append((owner, f"{kind} handoff — {n_open} of {n} item(s) open", issued, hid))
    if nx["kind"] == "run":
        nxt = (f"`{nx['command']}` — Paul opens a **new session on {nx.get('session_model', 'haiku').title()}** in "
               f"the client folder (`python3 scripts/worktree.py open {slug}`) and types `/next {slug}`" + (f" (agents: {nx['agents']})" if nx.get("agents") else ""))
    elif nx["kind"] == "decision":
        nxt = f"Paul types `{nx['command']}` (or asks for changes first)"
    else:
        nxt = f"`{nx['command']}` once the wait above is over"
    who_waits = "; ".join(f"{w[0]} — {w[1][:90]}" for w in waits[:3]) or "nobody"
    total, failed = _spend(slug)
    out = [f"# {c['name']} - Status", "",
           f"- **Stage {stage.replace(' of ', ' of ', 1)}**",
           f"- **What is happening now:** {now_line}",
           f"- **Waiting on:** {who_waits}",
           f"- **Next action:** {nxt}", "",
           f"_Generated {S.now()[:16]} by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), "
           "one session per stage._", "",
           "## Waiting on", "", "| Who | What | Since | Reference |", "|---|---|---|---|"]
    out += [f"| {w} | {t} | {s} | {r} |" for w, t, s, r in waits] or ["| — | nothing | | |"]
    out += ["", "## Waiting on (not blocking)", "", "_Open, but the next action above goes ahead without them._", "",
            "| Who | What | Since | Reference |", "|---|---|---|---|"]
    out += [f"| {w} | {t} | {s} | {r} |" for w, t, s, r in side] or ["| — | nothing | | |"]
    out += ["", "## Settled decisions — never re-raised", ""]
    aps = settled.approvals(slug)
    out += [f"- {when}: {S.label(what) if what in S.GATES['gates'] else what} — {dec}" for when, what, dec in aps]
    out += [f"- {e['text']}" for k, e in settled.entries(slug).items() if e.get("state") == "settled"]
    if not aps and not settled.entries(slug):
        out.append("_None yet._")
    out += ["", "## Open VA items", "", "_Every VA item is in one living worklist: `handoffs/VA-WORKLIST.md` "
            "(Drive: \"" + c["name"] + " - VA Worklist\")._", ""]
    out += ([f"- **{hid}** ({owner}) — {kind}: {n_open} of {n} open, issued {issued}" for hid, owner, kind, issued, n_open, n in hs]
            or ["_None._"])
    import manifest   # CM-061 §3.1: inputs on file that no finished step has read
    un = manifest.unused(slug)
    out += ["", "## Data on file not used yet", "",
            "_Inputs the data manifest (methodology/data-manifest.json) says a step must read, where that step has not "
            "finished for this client yet._", ""]
    out += ([f"- **{e['id']}** ({len(fs)} file(s), e.g. `{fs[0]}`) — read by "
             f"{', '.join(e.get('read_by') or ['the step that reads ' + e.get('raw_of', '?')])}" for e, fs in un]
            or ["_None — every input on file has been read._"])
    import changereq   # P3: workflow issues flagged in this client's sessions, for Paul's next system session
    fl = changereq.open_flags(slug)
    out += ["", "## Flagged for Paul (system)", ""]
    out += ([f"- **{r['id']}**{' → ' + cid if cid else ''} ({state.lower()}{', not yet reviewed' if not cid else ''}) "
             f"{r['at'][:10]} · {r.get('step') or '—'}: {r['text']}"
             + (f" — workaround: {r['workaround']}" if r.get("workaround") else "") for r, cid, state in fl]
            or ["_None._"])
    out += ["", "## Spend so far", "", f"- DataforSEO: ${total:.2f}" + (f" (of which failed tasks ${failed:.2f})" if failed else "")]
    ms = st.get("model_spend") or []   # P12: model cost per step (run.py finish --tokens/--cost)
    by = {}
    for r in ms:
        k = r.get("step") or "?"
        t = by.setdefault(k, [0, 0, 0.0])
        t[0] += 1; t[1] += int(r.get("tokens") or 0); t[2] += float(r.get("usd") or 0)
    out += ["", "## Spend by step (model)", ""]
    out += (["| Step | Runs | Tokens | USD |", "|---|---|---|---|"]
            + [f"| {k} | {n} | {tok:,} | ${usd:.2f} |" for k, (n, tok, usd) in sorted(by.items(), key=lambda kv: -kv[1][2])]
            + [f"| **total** | {sum(v[0] for v in by.values())} | {sum(v[1] for v in by.values()):,} | "
               f"${sum(v[2] for v in by.values()):.2f} |"]) if by else ["_Nothing recorded yet (run.py finish --tokens --cost)._"]
    if lr:
        out += ["", f"Last run: /{lr.get('command')} {lr.get('finished', '')[:16]} — {lr.get('result')}"]
    return "\n".join(out) + "\n"


def top(slug):
    """The four lines /next and /where print instead of re-explaining history."""
    lines = [x for x in status_md(slug).splitlines() if x.startswith("- **")]
    return "\n".join(lines[:4])


def render(slug):
    import facts
    import worklist
    facts.render(slug)   # P4: the Brand Guide's fact rows come from facts.json
    worklist.build(slug)   # P9: one living VA Worklist
    st = S.load(slug)
    d = client_dir(slug)
    log = _log(slug)
    (d / "handoff-log.md").write_text(handoff_log(st, log))
    (d / "decisions.md").write_text(decisions(st, log))
    (d / "document-checklist.md").write_text(checklist(st))
    (d / "approval-record.md").write_text(S.render_approval_record(st))
    (d / "decisions-settled.md").write_text(settled_register(slug))
    (d / "STATUS.md").write_text(status_md(slug))
    test_run_notes(slug)


def brand(slug, sections):
    """P12: only the named Brand Guide sections (A, D, B2, C3 …), never the whole 36 KB file."""
    from lib import _md_section
    text = (client_dir(slug) / "brand-guide.md").read_text(encoding="utf-8")
    out, missing = [], []
    for sid in sections:
        sec = _md_section(text, sid)
        (out.append(sec) if sec else missing.append(sid))
    return "\n\n".join(out), missing


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "top":
        print(top(sys.argv[2]))
        sys.exit(0)
    if len(sys.argv) == 5 and sys.argv[1] == "brand" and sys.argv[3] == "--sections":
        text, missing = brand(sys.argv[2], [x.strip() for x in sys.argv[4].split(",") if x.strip()])
        print(text)
        if missing:
            print("not found: " + ", ".join(missing), file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    if len(sys.argv) != 3 or sys.argv[1] != "render":
        sys.exit(__doc__)
    render(sys.argv[2])
    print(f"rendered handoff-log.md, decisions.md, document-checklist.md, approval-record.md for {sys.argv[2]}")
