#!/usr/bin/env python3
"""records.py — the human-readable records, generated one-way from status.json and log.md.

    records.py render <slug>

Writes (overwrites) in clients/<slug>/:
  handoff-log.md        every run's handoff section (run.py finish --handoff <file>), oldest first
  decisions.md          decisions summary: Paul's approvals, logged decisions (run.py decision),
                        conditions met, aborted runs
  document-checklist.md what is in, skipped or missing — from the audit-step outcomes, conditions
                        and decisions
  approval-record.md    the Drive Approval Record (status.py approval-record)

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


def render(slug):
    st = S.load(slug)
    d = client_dir(slug)
    log = _log(slug)
    (d / "handoff-log.md").write_text(handoff_log(st, log))
    (d / "decisions.md").write_text(decisions(st, log))
    (d / "document-checklist.md").write_text(checklist(st))
    (d / "approval-record.md").write_text(S.render_approval_record(st))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "render":
        sys.exit(__doc__)
    render(sys.argv[2])
    print(f"rendered handoff-log.md, decisions.md, document-checklist.md, approval-record.md for {sys.argv[2]}")
