# Stage 4 — Audit

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: discovery-audit (Opus), audit-reviewer (Opus) — the mechanical steps are scripts.

| Step | Command | Ends at |
|---|---|---|
| Audit (page specs approved once, globally): entity → architecture → page conformance → technical, then the fresh-context review (S12–S18) | `/discovery audit` | — |
| The client's facts recorded and reconciled into the Brand Guide | `/discovery sheet-returned`, `reconcile` | **Approval 2**: `/approve <slug> audit_approved brand_guide_approved` → **discovery_signed_off** |

- **S12 is a script:** `python3 scripts/pipeline.py <slug> inventory --run <RUN_ID> --phase audit` (ingest, cross-checks,
  conformance, outcome, Evidence Manifest). **Every Markdown deliverable is rendered, never typed:** `python3 scripts/render.py
  all <slug> --run <RUN_ID>` (Evidence Manifest, URL Decision Map, Finding Register, audit review sheet, blocker checklist,
  site plan; STATUS.md via `render.py status`). A file an approval covers is never rendered over.
- Mechanical checks first: `python3 scripts/conformance.py <slug>` scores every check with no judgment
  (`methodology/specs/check-kinds.json`), run by `pipeline.py` or the stage chat; the Opus agent fills only the judgment columns.
- S15, once the URL Decision Map exists: `python3 scripts/conformance.py judge <slug> --run <RUN_ID>` scores the
  judgment checks of every **kept** page on the Claude API (Sonnet) → `audit/conformance-judgment.csv`; the agent
  reads it instead of scoring those pages. No API key yet (or the API answers 401): the script says "no API key — ran on the agent route" and the agent does it as before.
- Gate B questions: kinds and `searched:` lines, `settled.py filter`, `questions.py check` (P6).
- The audit-reviewer sees only the registers and decisions, never the analysis conversation (CM-018; CM-026 standing).
- Conflicts are recorded per PROC-01, never resolved inside the work.
