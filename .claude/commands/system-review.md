---
description: Paul only, in a system session — go through every open change request and flag, one by one
argument-hint: (none)
disable-model-invocation: true
---

Paul typed: /system-review $ARGUMENTS

Rewrite 2 P3: the one place the workflow changes. Client sessions only flag (`run.py flag`); this lists what they
flagged and every proposal still open, and Paul answers each.

1. `python3 scripts/changereq.py session` — must say "system session: yes". If not, stop: Paul types `/system` first.
2. `python3 scripts/changereq.py collect` — every new client flag gets its CR-### entry.
3. `python3 scripts/changereq.py list --open` — then, for each OPEN item, show Paul its text (read only that entry in
   `methodology/change-requests.md`) in plain words: what happens now, what is proposed, the evidence, the workaround
   used. Ask **one item at a time**: accept, reject, or edit (Paul's own wording). Never decide for him.
4. Record each answer as he gives it: `python3 scripts/changereq.py decide <CR-###> accept|reject|edit --text "…"`.
5. Accepted items are this session's work list. For each: make the change → `python3 tests/run_all.py` (a new check
   for the new behaviour) → commit with the CR ID in the message → `python3 scripts/changereq.py done <CR-###> --sha <sha>`.
   A change to a ruling becomes a numbered entry in `methodology/rulings.md` (PROC-01), never a silent edit.
6. End with what was accepted, built, rejected, and anything accepted but not yet built.
