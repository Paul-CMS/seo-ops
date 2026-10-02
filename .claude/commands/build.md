---
description: Agent 2 — technical blockers, site plan, pilot, then service/location batches (briefs, drafts, write-back)
argument-hint: <slug> [blockers|plan|batch <id> [drafts]|pilot-corrections|writeback <id>|block2] [--route A|B]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §5. If no step is given, use `python3 scripts/next.py <slug>`.

| Step | Gates for run.py start |
|---|---|
| blockers | block1 |
| plan | block1 |
| batch <id> (briefs) | block1,batch:<id>:briefs_ready |
| batch <id> drafts | block1,batch:<id>:drafts_ready |
| pilot-corrections | block1,batch:pilot:briefs |
| writeback <id> | block1,batch:<id>:drafts |
| block2 | block1 |

1. `python3 scripts/run.py start <slug> build --gates <gates>` → note the RUN_ID and pass it
   literally to every later step. Exit 4 → refuse and explain; exit 3 → stop and ask Paul.
2. Route: `--route`, else status.json `client.route`, else ask Paul (A = the system writes,
   B = Paul provides finished content).
3. Use the **build** subagent with slug, RUN_ID, the step and the route.
4. Stop at each decision and give Paul the line:
   - site plan → `/approve <slug> site_plan`
   - briefs → `/approve <slug> batch:<id>:briefs --files <one brief per page>`
   - drafts → `/approve <slug> batch:<id>:drafts --files <one draft per page>` (+ `--review` for
     sensitive clients, `--practitioner` for medical/chiropractic)
   - technical blockers cleared → `/approve <slug> b2_blockers`; all pages live → `/approve <slug> block2`
5. Handoff Log section; `run.py finish <slug> <RUN_ID> ...` with a plain client view
   (e.g. phase "Writing your service pages", done "First 5 service pages approved").

Drafts reach WordPress only through `/implement <slug> batch <id>` — drafts by default.
