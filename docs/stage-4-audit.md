# Stage 4 — Audit

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: discovery-audit (Opus), audit-reviewer (Opus), clerk.

| Step | Command | Ends at |
|---|---|---|
| Audit (page specs approved once, globally): entity → architecture → page conformance → technical, then the fresh-context review (S12–S18) | `/discovery audit` | — |
| The client's facts recorded and reconciled into the Brand Guide | `/discovery sheet-returned`, `reconcile` | **Approval 2**: `/approve <slug> audit_approved brand_guide_approved` → **discovery_signed_off** |

- Mechanical checks first: `python3 scripts/conformance.py <slug>` scores every check with no judgment
  (`methodology/specs/check-kinds.json`) on the clerk; the Opus agent fills only the judgment columns.
- Gate B questions: kinds and `searched:` lines, `settled.py filter`, `questions.py check` (P6).
- The audit-reviewer sees only the registers and decisions, never the analysis conversation (CM-018; CM-026 standing).
- Conflicts are recorded per PROC-01, never resolved inside the work.
