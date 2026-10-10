---
description: Agent 3 — link wheel, schema, QA and release (plus outbound links and voice FAQs)
argument-hint: <slug> [wheel|schema|qa]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md and `docs/stage-7-finish.md`. If no part is given, use `python3 scripts/next.py <slug>`: wheel (pages_built met, link_wheel_approved not) →
schema (link_wheel_approved met, not marked schema_built) → qa.

Steps: `wheel` · `schema` · `qa`.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps finish` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> finish --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   explain; exit 3 → stop and ask Paul.
2. Use the **finish** subagent with slug, `<RUN_ID>` and the part.
3. Linking exceptions (one contextual link, outbound authority links — CM-022) are listed
   separately for Paul to approve; never applied without his yes.
4. Give Paul the exact line from `next.py`: `link_wheel_approved` after the wheel verifies; `release_approved` after QA clears.
5. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> ...`.
