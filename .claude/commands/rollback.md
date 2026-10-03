---
description: Restore old values from the safety log for a run (or chosen changes), after Paul approves the plan
argument-hint: <slug> --of RUN_ID [--change N ...]
---

Arguments: $ARGUMENTS

1. `python3 scripts/rollback.py plan <slug> --of <run> [--change N ...]` and show Paul the plan:
   what can be restored automatically, and what needs a reverse VA handoff (redirects, slugs,
   anything a person did). **Wait for Paul's yes.**
2. The system rolls back only what it applied itself (alt text, SEO fields after the pilot, drafts it created).
   Anything on a live page that Jonie did is a reverse handoff to Jonie.
3. `python3 scripts/run.py start <slug> rollback` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands) — if the run being rolled back is
   still unfinished, Paul must first say to abort it (`run.py abort <slug> <run> --reason "..."`).
4. For each automatic item, newest first: `python3 scripts/wp.py restore <slug> --run <RUN_ID> --change N`.
   It checks the live value still equals what we set; if someone changed it since, it stops.
5. Reverse handoffs: `handoff.py create <slug> --run <RUN_ID> --kind <k> --items <csv>` (owner set by the kind)
   (e.g. remove the redirect, restore the old slug).
6. `run.py finish <slug> <RUN_ID> --summary "rolled back n, reverse handoffs n, stopped n"`, then `/verify`.
