#!/usr/bin/env python3
"""settled.py — decide once (R6, R7; Paul 2026-10-08). A decision is made once and is done.

Settled decisions live in the safety log (append-only), one line each:
    - SETTLED <key> · <when> · run <RUN_ID> · by <who> · <text>
    - REOPENED <key> · <when> · run <RUN_ID> · <reason>          (one reopen request, with its reason)
    - OPEN <key> · <when> · run <RUN_ID> · by <who it waits on> · <question>   (asked once; settling the key closes it)
    - CLOSED <key> · <when> · run <RUN_ID> · by <settled key> · <note>   (an open question answered under another key)
Paul's approvals (## APPROVAL lines) are settled too. records.py generates clients/<slug>/decisions-settled.md
from these; every agent reads it and never re-raises what it lists.

Record with run.py:
    run.py decision <slug> <RUN_ID> --settle <key> --text "..."     settle once (refused if already settled)
             [--closes <open key>[,<open key>]]   the open question(s) this answers (Paul 2026-10-09)
             [--leaves-open "<why the related open question still stands>"]
    run.py decision <slug> <RUN_ID> --reopen <key> --text "<new evidence / reason>"
    run.py decision <slug> <RUN_ID> --ask <key> --who "Client (via Paul)" --text "<the question>"   ask once
Decide once means an answer lands where the question was asked (Paul, 2026-10-09). Keys are compared by their words:
a key that starts with another, or shares most of its words, is RELATED. Settling a key related to an open question is
refused unless the answer names it (--closes) or says why it stays open (--leaves-open); asking a question whose key is
related to a settled or open one is refused (the register already holds it) unless --distinct "<why it is a new
question>". So "synthetic_roofing" cannot be settled while "synthetic_roofing_offered" silently stays open.
A key may be reopened only while it is settled, only with a reason, and every reopening is counted as a
process defect (a decision asked at the wrong time — fix the order, not the decision).

    settled.py show <slug>          the register as the agents see it
"""
import re
import sys

from lib import append, client_dir, die, now, redact

KEY = re.compile(r"^[a-z0-9][a-z0-9_.:-]{1,60}$")
LINE = re.compile(r"^- (SETTLED|REOPENED|OPEN|CLOSED) (\S+) · (\S+) · run (\S+) · (?:by (.+?) · )?(.*)$", re.M)
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
        elif kind == "CLOSED":
            if e.get("state") == "open":
                e.update(state="answered", answered_by=by or "", answered_at=at, note=text)
        else:
            e.update(state="reopened", reason=text, reopened_at=at)
            e["reopened"] += 1
    return out


STOP = {"the", "a", "an", "of", "is", "and", "or", "to", "for", "on", "in", "it", "its", "your", "are", "be", "we",
        "do", "does", "q", "fact"}


def words(key):
    return [w for w in re.split(r"[_.:\-]+", key.lower()) if w and w not in STOP]


def related(a, b):
    """Two keys that name the same decision: equal, one starts with the other, or most words shared."""
    if a == b:
        return True
    if a.startswith("fact:") or b.startswith("fact:"):   # facts-interview keys name one fact exactly (evidence.py)
        return False
    if a.startswith(b + "_") or b.startswith(a + "_"):
        return True
    wa, wb = set(words(a)), set(words(b))
    shared = wa & wb
    return len(shared) >= 2 and len(shared) / max(1, min(len(wa), len(wb))) >= 0.67


def related_to(slug, key, states):
    return [(k, e) for k, e in entries(slug).items() if k != key and e.get("state") in states and related(k, key)]


def approvals(slug):
    """Paul's approvals as settled items: [(when, what, decision)] — the latest per target."""
    seen = {}
    for m in APPROVAL.finditer(_log(slug)):
        seen[m.group(2)] = (m.group(1)[:10], m.group(2), m.group(3))
    return list(seen.values())


def settle(slug, run_id, key, text, by="Paul", closed_ok=False, closes=(), leaves_open=None):
    if not KEY.match(key or ""):
        die(f"'{key}' is not a settled-decision key (lowercase letters, digits, _ . : -).")
    if not closed_ok:
        import run as R
        R.open_run(slug, run_id)
    ents = entries(slug)
    e = ents.get(key)
    if e and e.get("state") == "settled":
        die(f"REFUSED — '{key}' is already settled ({e['at'][:10]}, {e['by']}): {e['text']}\n"
            f"A settled decision is not asked again. Only new contradicting evidence reopens it: "
            f"run.py decision <slug> <RUN_ID> --reopen {key} --text \"<the new evidence>\".", 4)
    closes = [c for c in closes if c]
    for c in closes:
        if (ents.get(c) or {}).get("state") != "open":
            die(f"--closes {c}: there is no open question '{c}' (decisions-settled.md lists the open ones).")
    left = [k for k, _ in related_to(slug, key, ("open",)) if k not in closes]
    if left and not (leaves_open or "").strip():
        die(f"REFUSED — '{key}' looks like the answer to open question(s) " + ", ".join(
            f"'{k}' ({ents[k]['question'][:90]})" for k in left) + ". Name the question it answers "
            f"(--closes {','.join(left)}) or say why it stays open (--leaves-open \"<reason>\"), so the question is "
            "not asked again.", 4)
    append(client_dir(slug) / "log.md",
           f"- SETTLED {key} · {now()} · run {run_id} · by {by} · {redact(text).replace(chr(10), ' ')}"
           + (f" (still open on purpose: {', '.join(left)} — {redact(leaves_open)})" if left else "") + "\n")
    for c in closes:
        append(client_dir(slug) / "log.md", f"- CLOSED {c} · {now()} · run {run_id} · by {key} · answered by '{key}'\n")


def ask(slug, run_id, key, who, question, closed_ok=False, distinct=None):
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
    if e and e.get("state") == "answered":
        die(f"REFUSED — '{key}' was answered under '{e['answered_by']}' ({e['answered_at'][:10]}). It is not asked again.", 4)
    near = related_to(slug, key, ("settled", "open", "answered"))
    if near and not (distinct or "").strip():
        k, n = near[0]
        what = (f"settled {n['at'][:10]}: {n['text']}" if n["state"] == "settled" else
                f"already asked {n.get('asked_at', '')[:10]}: {n.get('question')}" if n["state"] == "open" else
                f"answered under '{n.get('answered_by')}'")
        die(f"REFUSED — '{key}' is the same decision as '{k}' ({what[:200]}). It is not asked again. If it is truly a "
            "new question, say why with --distinct \"<what is new>\"; if new evidence contradicts the settled answer, "
            f"--reopen {k}.", 4)
    append(client_dir(slug) / "log.md",
           f"- OPEN {key} · {now()} · run {run_id} · by {who} · {redact(question).replace(chr(10), ' ')}"
           + (f" (new, not '{near[0][0]}': {redact(distinct)})" if near else "") + "\n")


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
