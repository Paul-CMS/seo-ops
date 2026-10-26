---
description: Agent 1 — discovery, entity foundation, proof sheet, audit, reconciliation, Block 1
argument-hint: <slug> [discovery|proof-sheet|facts-direct|sheet-returned|data|audit|review|reconcile]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md and the stage file for the step (`docs/stage-2-discovery.md`, `stage-3-data.md`, `stage-4-audit.md`). If no step is given, use `python3 scripts/next.py <slug>` and say which step and why.
Order (R3 — two approvals): `discovery` (entity + **Decision Sheet**) → `proof-sheet` (or `facts-direct` when
the client already answered) → **Approval 1** (`/approve <slug> entity_approved proof_sheet_approved`) → new session:
`/crawl`, `data` (one cost yes for the whole step) → new session: `audit` (page specs approved once, globally; the
slim audit, CM-063) → `review` (Paul's one answer line on the audit review sheet) → **Approval 2a**
(`/approve <slug> audit_approved` — on its own, D3: safe fixes and the blocker handoff start) → `sheet-returned` →
`reconcile` → **Approval 2b** (`/approve <slug> brand_guide_approved`). The discovery sign-off is then a condition —
nothing to approve.

Steps: `discovery` · `proof-sheet` · `facts-direct` · `sheet-returned` · `data` · `audit` · `review` · `reconcile`.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps discovery` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> discovery --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse in
   plain language (which gate, what it unlocks). Exit 3 → stop and ask Paul.
2. Use the **discovery-audit** subagent for the step, giving it the slug, `<RUN_ID>` and the step. Paul's answers alone
   (facts, unknowns, a settled choice) are not a step for an agent: record them yourself in an `answers` run (CM-065,
   `/next` → "Every answer is recorded …").
3. For `audit`: when the subagent has `findings.csv` and the URL Decision Map (screen `--check` passed, triage
   written), use the **audit-reviewer** subagent (a fresh context) on the registers, scoped by `review.py scope <slug>
   audit` (step S17). Never let the agent that wrote the findings review them. Then the discovery-audit subagent
   writes the one review sheet and renders the deliverables (S18).
   For `review`: no agent — run `python3 scripts/review.py apply <slug> audit --run <RUN_ID> --answers "<Paul's line>"`
   yourself; then show the `/approve <slug> audit_approved` line.
4. Show Paul the result and the exact `/approve` line from `python3 scripts/next.py <slug>` (it names
   the files the approval covers). Never type it yourself.
5. Write the Handoff Log section (25 lines at most; the scripts add the change, decision and step lines) to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary ...`.
