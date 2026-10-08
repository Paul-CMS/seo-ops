#!/usr/bin/env python3
"""settled.py — decide once (R6, R7; Paul 2026-10-08). A decision is made once and is done.

Settled decisions live in the safety log (append-only), one line each:
    - SETTLED <key> · <when> · run <RUN_ID> · by <who> · <text>
    - REOPENED <key> · <when> · run <RUN_ID> · <reason>          (one reopen request, with its reason)
    - OPEN <key> · <when> · run <RUN_ID> · by <who it waits on> · <question>   (asked once; settling the key closes it)
Paul's approvals (## APPROVAL lines) are settled too. records.py generates clients/<slug>/decisions-settled.md
from these; every agent reads it and never re-raises what it lists.

Record with run.py:
    run.py decision <slug> <RUN_ID> --settle <key> --text "..."     settle once (refused if already settled)
    run.py decision <slug> <RUN_ID> --reopen <key> --text "<new evidence / reason>"
    run.py decision <slug> <RUN_ID> --ask <key> --who "Client (via Paul)" --text "<the question>"   ask once
A key may be reopened only while it is settled, only with a reason, and every reopening is counted as a
process defect (a decision asked at the wrong time — fix the order, not the decision).

    settled.py show <slug>          the register as the agents see it
"""
import re
import sys

from lib import append, client_dir, die, now, redact

KEY = re.compile(r"^[a-z0-9][a-z0-9_.:-]{1,60}$")
LINE = re.compile(r"^- (SETTLED|REOPENED|OPEN) (\S+) · (\S+) · run (\S+) · (?:by (.+?) · )?(.*)$", re.M)
APPROVAL = re.compile(r"^## APPROVAL · (\S+) · (.+?) · (\w+) · by Paul$", re.M)


def _log(slug):
    p = client_dir(slug) / "log.md"
    return p.read_text() if p.exists() else ""


def entries(slug):
    """{key: {'state': settled|reopened, 'text', 'at', 'by', 'run', 'reopened': n, 'reason'}} in log order."""
    out = {}
    for m in LINE.finditer(_log(slug)):
        kind, key, at, run, by, text = m.groups()
        e = out.setdefault(key, {"reopened": 0})
        if kind == "SETTLED":
            e.update(state="settled", text=text, at=at, by=by or "", run=run)
        elif kind == "OPEN":
            if e.get("state") != "settled":
                e.update(state="open", question=text, asked_at=at, who=by or "Paul")
        else:
            e.update(state="reopened", reason=text, reopened_at=at)
            e["reopened"] += 1
    return out


def approvals(slug):
    """Paul's approvals as settled items: [(when, what, decision)] — the latest per target."""
    seen = {}
    for m in APPROVAL.finditer(_log(slug)):
        seen[m.group(2)] = (m.group(1)[:10], m.group(2), m.group(3))
    return list(seen.values())


def settle(slug, run_id, key, text, by="Paul", closed_ok=False):
    if not KEY.match(key or ""):
        die(f"'{key}' is not a settled-decision key (lowercase letters, digits, _ . : -).")
    if not closed_ok:
        import run as R
        R.open_run(slug, run_id)
    e = entries(slug).get(key)
    if e and e.get("state") == "settled":
        die(f"REFUSED — '{key}' is already settled ({e['at'][:10]}, {e['by']}): {e['text']}\n"
            f"A settled decision is not asked again. Only new contradicting evidence reopens it: "
            f"run.py decision <slug> <RUN_ID> --reopen {key} --text \"<the new evidence>\".", 4)
    append(client_dir(slug) / "log.md",
           f"- SETTLED {key} · {now()} · run {run_id} · by {by} · {redact(text).replace(chr(10), ' ')}\n")


def ask(slug, run_id, key, who, question, closed_ok=False):
    """An open question, asked once: it waits on <who> until the key is settled."""
    if not KEY.match(key or ""):
        die(f"'{key}' is not a key (lowercase letters, digits, _ . : -).")
    if not closed_ok:
        import run as R
        R.open_run(slug, run_id)
    e = entries(slug).get(key)
    if e and e.get("state") == "settled":
        die(f"REFUSED — '{key}' is already settled: {e['text']}. It is not asked again.", 4)
    if e and e.get("state") == "open":
        die(f"REFUSED — '{key}' is already asked ({e['asked_at'][:10]}, waiting on {e['who']}): {e['question']}", 4)
    append(client_dir(slug) / "log.md",
           f"- OPEN {key} · {now()} · run {run_id} · by {who} · {redact(question).replace(chr(10), ' ')}\n")


def reopen(slug, run_id, key, reason):
    import run as R
    R.open_run(slug, run_id)
    e = entries(slug).get(key)
    if not e or e.get("state") == "open":
        die(f"'{key}' is not settled — there is nothing to reopen. Settle it with --settle.")
    if e.get("state") == "reopened":
        die(f"REFUSED — '{key}' is already reopened ({e.get('reopened_at', '')[:10]}: {e.get('reason')}). "
            "One reopen request; settle it again once Paul has decided.", 4)
    if not (reason or "").strip():
        die("A reopen request needs the reason (the new contradicting evidence).")
    append(client_dir(slug) / "log.md",
           f"- REOPENED {key} · {now()} · run {run_id} · {redact(reason).replace(chr(10), ' ')}\n")


def defects(slug):
    """Reopenings = process defects (R6)."""
    return sum(e.get("reopened", 0) for e in entries(slug).values())


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "show":
        import records
        print(records.settled_register(sys.argv[2]), end="")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
