---
description: Agent 2 — technical blocker checklist, then page content one page at a time (Route A or B), write-back, Block 2
argument-hint: <slug> [blockers|next|page <page_id>|block2] [--route A|B]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §5. Every step needs **block1**.

1. `python3 scripts/run.py start <slug> build --gates block1` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands) (add `,page:<prev_id>` when
   starting the next service page — the previous one must be approved first). Exit 4 → refuse
   and explain; exit 3 → stop and ask Paul.
2. Route: `--route`, else status.json `client.route`, else ask Paul (A = the system writes,
   B = Paul provides finished content).
3. Use the **build** subagent with slug, `<RUN_ID>`, the step and the route. If no step is given,
   it takes the next page in the state machine (service → write-back batch → location →
   write-back → homepage).
4. Stop at every approval point: outline OK, content approval (`/approve <slug> page:<id> --file ...`,
   plus `--review` for sensitive clients and `--practitioner` for medical/chiropractic), b2_blockers, block2.
5. Handoff Log section; `run.py finish <slug> <RUN_ID> ...` with a plain client view
   (e.g. phase "Writing your service pages", done "Roof Repair page approved").

Content changes reach WordPress only through `/implement` — drafts by default.
