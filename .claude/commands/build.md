---
description: Agent 2 — technical blockers, site plan, pilot, then service/location batches (briefs, drafts, semantic review, write-back)
argument-hint: <slug> [blockers|plan|batch <id> [drafts|apply-sem]|pilot-corrections|writeback <id>] [--route A|B]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §5. If no step is given, use `python3 scripts/next.py <slug>`.

| Step | Gates for run.py start |
|---|---|
| blockers | discovery_signed_off |
| plan | discovery_signed_off |
| batch <id> (briefs) | discovery_signed_off,batch:<id>:briefs_ready |
| batch <id> drafts | discovery_signed_off,batch:<id>:drafts_ready |
| batch <id> apply-sem | discovery_signed_off,batch:<id>:sem |
| pilot-corrections | discovery_signed_off,batch:pilot:briefs |
| writeback <id> | discovery_signed_off,batch:<id>:drafts |

1. `python3 scripts/run.py start <slug> build --gates <gates>` → note the RUN_ID and pass it
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

Drafts reach WordPress only through `/implement <slug> batch <id>` — drafts by default.
