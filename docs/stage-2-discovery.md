# Stage 2 — Discovery

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: discovery-audit (Opus), clerk.

| Step | Command | Ends at |
|---|---|---|
| Discovery + entity research (S02–S03), public sources, **Decision Sheet** | `/discovery` | — |
| Proof sheet (S04) — Markdown + the client Google Doc (HTML) — or the client's direct answers | `/discovery proof-sheet` \| `facts-direct` | **Approval 1**: `/approve <slug> entity_approved proof_sheet_approved` |

- Approval 1 settles every Decision Sheet answer for good. Paul sends the sheet; nothing goes to a client automatically.
- Every fact found goes into `facts.json` with its source (`run.py fact`); public facts are looked up, never asked (P6).
- Discovery is not the audit: no severity, priorities or recommendations yet.
