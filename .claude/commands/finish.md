---
description: Agent 3 — release QA of the published pages (the link wheel and schema ship with the drafts, CM-064)
argument-hint: <slug> [qa]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md and `docs/stage-7-finish.md`. The only step is `qa` (pages_built met, release_approved not). The link
wheel and the schema are no longer Finish steps: they are built by script and ship with the drafts (`/build ship`,
`/build handoff`, CM-064).

Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps finish` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> finish --step qa` → note the RUN_ID it prints and pass it literally to every
   later step (shell variables do not persist between commands). Exit 4 → refuse and explain; exit 3 → stop and ask Paul.
2. Run the scripts yourself (no agent): `python3 scripts/qa.py check <slug> --stage live`, then
   `python3 scripts/qa.py explain <slug> --run <RUN_ID> --stage live`, then `python3 scripts/qa.py sample <slug>`.
3. Use the **finish-qa** subagent with slug, `<RUN_ID>` and the pages `qa.py sample` listed (every page for a sensitive
   client) for the content QA; use the **finish** subagent only for what the scripts cannot do (the QA crawl of the
   published pages, the punch-list and acceptance sheets).
4. Give Paul the exact line from `next.py`: `release_approved` after QA clears.
5. Write the Handoff Log section (25 lines at most; the scripts add the change, decision and step lines) to
   `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> ...`.
