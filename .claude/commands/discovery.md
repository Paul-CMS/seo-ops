---
description: Agent 1 — discovery, entity foundation, proof sheet, audit, reconciliation, Block 1
argument-hint: <slug> [discovery|proof-sheet|audit|reconcile|block1]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. If no step is given, pick the next one from `status.py show <slug>`:
entity not approved → `discovery`; entity approved, sheet not ready → `proof-sheet`;
audit not approved → `audit` (allowed while the client has the sheet); sheet returned →
`reconcile`; all five Block 1 gates met → `block1`. Say which step you picked and why.

| Step | Gates to pass to run.py start |
|---|---|
| discovery | *(none)* |
| proof-sheet | b1_entity |
| audit | b1_entity |
| reconcile | b1_proof_sheet_returned |
| block1 | b1_entity,b1_proof_sheet_ready,b1_proof_sheet_returned,b1_brand_guide,b1_audit |

1. `python3 scripts/run.py start <slug> discovery --gates <gates>` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse in
   plain language (which gate, what it unlocks). Exit 3 → stop and ask Paul.
2. Use the **discovery-audit** subagent for the step, giving it the slug, `<RUN_ID>` and the step.
3. For `audit`: when the subagent finishes Stage 1, use the **audit-reviewer** subagent (a
   fresh context) for Stage 2. Never let the agent that wrote the findings review them.
4. Show Paul the result and the exact `/approve` line he can type. Never type it yourself.
5. Append the Handoff Log section; `run.py finish <slug> <RUN_ID> --summary ... --phase ... --next ... [--waiting ...]`.
   Client view examples: phase "Confirming your business details", waiting "Your answers on the
   fact sheet we sent".
