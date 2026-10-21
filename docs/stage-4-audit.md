# Stage 4 — Audit

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md. The slim audit: CM-063 (Rewrite 4 Phase 3)._

Session model: Haiku · agents: discovery-audit (Opus), audit-reviewer (Opus) — the mechanical steps are scripts.

| Step | Command | Ends at |
|---|---|---|
| Audit (page specs approved once, globally): screen → entity → URL decisions → triage → technical → fresh-context review → the one review sheet (S12–S18) | `/discovery audit` | — |
| Paul answers the audit review sheet | `/discovery review "accept all"` | **Approval 2a**: `/approve <slug> audit_approved` — safe fixes and the blocker handoff start (D3) |
| The client's facts recorded and reconciled into the Brand Guide | `/discovery sheet-returned`, `reconcile` | **Approval 2b**: `/approve <slug> brand_guide_approved` → **discovery_signed_off** |

- **S12 is a script:** `python3 scripts/pipeline.py <slug> inventory --run <RUN_ID> --phase audit` (ingest, cross-checks,
  auto conformance, the **redirect screen** `pagedec.py screen`, the Evidence Manifest).
- **The screen decides CM-019 C1–C3** for every URL (rankings, backlinks, GSC/GA4, GBP website, citations): pass / fail /
  needs evidence. The agent decides only the `needs evidence` rows and entity mismatches; `pagedec.py screen <slug>
  --check` refuses a destructive row on a failing URL.
- **S15 is triage:** `conformance.py judge` (the API scores pages Build will not rewrite), then `conformance.py triage`
  writes rebuild / light fix / keep into the URL Decision Map. No scorecard files.
- **Severity is CM-061's:** Fix (→ the Technical Blocker Checklist, rendered at the audit by `render.py blockers`) ·
  Fix and list · Ask (four kinds; URL decisions become kind-1 Asks by themselves).
- **S17:** `review.py scope <slug> audit` lists the reviewer's rows (every destructive URL row, every Ask, a sample); the
  reviewer reads the registers only (CM-018; CM-026 standing).
- **S18:** `review.py sheet <slug> audit --run <RUN_ID>` → `audit-review.csv` + `client-questions.csv` (the only thing the
  client ever sees; Paul sends it), then `render.py all <slug> --run <RUN_ID>`. Deliverables: the registers (CSV), the
  audit review sheet and the Evidence Manifest — no Recommendations document, no Markdown Finding Register.
- `/discovery review` applies Paul's answer line (`review.py apply <slug> audit`); `audit_approved` is refused until it is
  applied. Audits approved before CM-063 (Home Mobile Medical, Apex) keep their documents and approvals.
- Conflicts are recorded per PROC-01 (`conflicts.csv`) and become kind-4 Asks, never resolved inside the work.
