---
description: Agent 2 — technical blockers, site plan, pilot, then service/location batches (briefs, drafts, semantic review, write-back)
argument-hint: <slug> [blockers|plan|batch <id> [drafts|apply-sem]|pilot-corrections|ship <id>] [--route A|B]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §5. If no step is given, use `python3 scripts/next.py <slug>`.

Steps: `blockers` · `plan` · `batch` (briefs; `--batch <id>`) · `drafts` (`--batch <id>`) · `apply-sem` (`--batch <id>`, only when Paul picked SEM items) · `pilot-corrections` · `ship` (`--batch <id>`).
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps build` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> build --step <step> [--batch <id>|--page <id>]` → note the RUN_ID and pass it
   literally to every later step. Exit 4 → refuse and explain; exit 3 → stop and ask Paul.
2. Route: `--route`, else status.json `client.route`, else ask Paul (A = the system writes,
   B = Paul provides finished content).
3. Use the **build** subagent with slug, RUN_ID, the step and the route.
4. Stop at each decision and give Paul the exact line from `python3 scripts/next.py <slug>`:
   site plan · briefs · SEM IDs (`batch:<id>:sem --ids …`) · drafts (+ `--review` for sensitive
   clients, `--practitioner` for health) · technical blockers cleared (`blockers_cleared`). When every
   batch is written back, the `pages_built` condition is met by the system — no approval.
5. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> ...` with a plain client view
   (e.g. phase "Writing your service pages", done "First 5 service pages approved").

Drafts reach WordPress only through `/build <slug> ship <id>` — always as WordPress drafts.
