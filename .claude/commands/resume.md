---
description: Where a client stands, what ran last, and what's next — in plain language
argument-hint: <slug>   (or no argument for every client)
---

Arguments: $ARGUMENTS

Read-only. No run is started.

For the client (or each folder in `clients/` if none given):
1. `python3 scripts/status.py show <slug>` and `python3 scripts/run.py check <slug>`.
2. Read the last two sections of `clients/<slug>/handoff-log.md` and the tail of `log.md`.
3. `python3 scripts/handoff.py list <slug> --open` and `python3 scripts/dfs.py ledger <slug>` (totals only).

Answer in plain language, short:
- **Where they stand:** the phase, which decisions are approved and which conditions are met (name them
  in plain words, e.g. "entity foundation approved 2 Oct", not IDs). Any decision marked VOID (its file
  changed) and any "upstream change" flag: say which file changed and that Paul decides whether the
  later approval still stands.
- **What ran last:** the command, when, what it changed, and its result.
- **Unfinished run:** if `run.py check` found one, say so first and list the choices (resume,
  /verify, /rollback, abort — Paul's call).
- **Waiting on:** Paul (which `/approve`), the client (what), a VA (which handoffs).
- **Next:** the exact next command.
- **Spend:** DataforSEO total so far.
