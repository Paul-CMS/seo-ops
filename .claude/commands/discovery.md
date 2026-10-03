---
description: Agent 1 — discovery, entity foundation, proof sheet, audit, reconciliation, Block 1
argument-hint: <slug> [discovery|proof-sheet|sheet-returned|data|audit|reconcile|signoff]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. If no step is given, use `python3 scripts/next.py <slug>` and say which step and why.
Order: discovery → entity decision → proof sheet → (client has the sheet) `/crawl`, `data`,
`audit` → audit decision → client returns sheet (`sheet-returned`) → `reconcile` → `signoff`.

| Step | Gates to pass to run.py start |
|---|---|
| discovery | *(none)* |
| proof-sheet | entity_approved |
| sheet-returned | proof_sheet_approved |
| data | proof_sheet_approved |
| audit | entity_approved |
| reconcile | proof_sheet_returned |
| signoff | entity_approved,proof_sheet_approved,proof_sheet_returned,brand_guide_approved,audit_approved |

1. `python3 scripts/run.py start <slug> discovery --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse in
   plain language (which gate, what it unlocks). Exit 3 → stop and ask Paul.
2. Use the **discovery-audit** subagent for the step, giving it the slug, `<RUN_ID>` and the step.
3. For `audit`: when the subagent has the Finding Register and URL Decision Map, use the
   **audit-reviewer** subagent (a fresh context) on those two registers (step S17). Never let
   the agent that wrote the findings review them. Then the discovery-audit subagent renders
   the deliverables (S18).
4. Show Paul the result and the exact `/approve` line from `python3 scripts/next.py <slug>` (it names
   the files the approval covers). Never type it yourself.
5. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary ... --phase ... --next ... [--waiting ...]`.
   Client view examples: phase "Confirming your business details", waiting "Your answers on the
   fact sheet we sent".
