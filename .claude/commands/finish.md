---
description: Agent 3 — link wheel, schema, QA and release (plus outbound links and voice FAQs)
argument-hint: <slug> [wheel|schema|qa]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. If no part is given, use `python3 scripts/next.py <slug>`: wheel (block2 met, block3 not) →
schema (block3 met, not marked schema_built) → qa.

| Part | Gates |
|---|---|
| wheel | block2 |
| schema | block3 |
| qa | block3 |

1. `python3 scripts/run.py start <slug> finish --gates <gates>` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   explain; exit 3 → stop and ask Paul.
2. Use the **finish** subagent with slug, `<RUN_ID>` and the part.
3. Linking exceptions (one contextual link, outbound authority links — CM-022) are listed
   separately for Paul to approve; never applied without his yes.
4. Give Paul the exact line from `next.py`: `block3` after the wheel verifies; `block5` after QA clears.
5. Handoff Log section; `run.py finish ...` (client view e.g. "Final checks before launch").
