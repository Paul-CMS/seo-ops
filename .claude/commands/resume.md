---
description: Where a client stands, what ran last, and what's next — in plain language
argument-hint: <slug>   (or no argument for every client)
---

Arguments: $ARGUMENTS

Read-only. No run is started. Cheap on purpose: read the generated status, never the history.

For the client (or each folder in `clients/` if none given):
1. `python3 scripts/records.py top <slug>` — print its four lines as they are (stage, what is happening now,
   waiting on, next action). They come from `clients/<slug>/STATUS.md` (generated; the VA reads the same page).
2. `python3 scripts/run.py check <slug>` — if an unfinished run exists, say so first and list the choices
   (resume, /verify, /rollback, abort — Paul's call).
3. Only if Paul asks for more: `clients/<slug>/STATUS.md` (waiting on, settled decisions, open VA items, spend)
   and `python3 scripts/status.py show <slug>` for any decision marked VOID or flagged "upstream change" — say
   which file changed and that Paul decides whether the later approval still stands.

Never re-explain history and never re-raise anything under "Settled decisions".
