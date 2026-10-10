---
description: Agent 1 — discovery, entity foundation, proof sheet, audit, reconciliation, Block 1
argument-hint: <slug> [discovery|proof-sheet|facts-direct|sheet-returned|data|audit|reconcile]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md and the stage file for the step (`docs/stage-2-discovery.md`, `stage-3-data.md`, `stage-4-audit.md`). If no step is given, use `python3 scripts/next.py <slug>` and say which step and why.
Order (R3 — two approvals): `discovery` (entity + **Decision Sheet**) → `proof-sheet` (or `facts-direct` when
the client already answered) → **Approval 1** (`/approve <slug> entity_approved proof_sheet_approved`) → new session:
`/crawl`, `data` (one cost yes for the whole step) → new session: `audit` (page specs approved once, globally) →
`sheet-returned` → `reconcile` → **Approval 2** (`/approve <slug> audit_approved brand_guide_approved`). The discovery
sign-off is then a condition — nothing to approve.

Steps: `discovery` · `proof-sheet` · `facts-direct` · `sheet-returned` · `data` · `audit` · `reconcile`.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps discovery` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> discovery --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse in
   plain language (which gate, what it unlocks). Exit 3 → stop and ask Paul.
2. Use the **discovery-audit** subagent for the step, giving it the slug, `<RUN_ID>` and the step.
3. For `audit`: when the subagent has the Finding Register and URL Decision Map, use the
   **audit-reviewer** subagent (a fresh context) on those two registers (step S17). Never let
   the agent that wrote the findings review them. Then the discovery-audit subagent renders
   the deliverables (S18).
4. Show Paul the result and the exact `/approve` line from `python3 scripts/next.py <slug>` (it names
   the files the approval covers). Never type it yourself.
5. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary ...`.
