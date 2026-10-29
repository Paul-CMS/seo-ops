# Carolina Carpet Cleaning - Status

- **Stage 2 of 8 — Discovery**
- **What is happening now:** waiting for Paul's approval — Discovery is ready for your approval in one line — the Decision Sheet and the entity foundation: Carolina Carpet Cleaning - Decision Sheet - REVIEW.md, Carolina Carpet Cleaning - Discovery Record - REVIEW.md, brand-guide.md#A+B1+B2; the client proof sheet (or the client's direct answers): Carolina Carpet Cleaning - MANUAL - client-answers - 2026-10-28.md. Once approved, every Decision Sheet answer is settled for good and the data pulls can start
- **Waiting on:** Paul — Discovery is ready for your approval in one line — the Decision Sheet and the entity found
- **Next action:** Paul types `/approve carolina-carpet-cleaning entity_approved proof_sheet_approved` (or asks for changes first) · model: Haiku chat

_Generated 2026-10-28T19:04 by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), one session per stage._

## Waiting on

| Who | What | Since | Reference |
|---|---|---|---|
| Paul | Discovery is ready for your approval in one line — the Decision Sheet and the entity foundation: Carolina Carpet Cleaning - Decision Sheet - REVIEW.md, Carolina Carpet Cleaning - Discovery Record - REVIEW.md, brand-guide.md#A+B1+B2; the client proof sheet (or the client's direct answers): Carolina Carpet Cleaning - MANUAL - client-answers - 2026-10-28.md. Once approved, every Decision Sheet answer is settled for good and the data pulls can start | 2026-10-28 | /approve carolina-carpet-cleaning entity_approved proof_sheet_approved |

## Waiting on (not blocking)

_Open, but the next action above goes ahead without them._

| Who | What | Since | Reference |
|---|---|---|---|
| Gwen | manual lookup handoff — 9 of 9 item(s) open | 2026-10-28 | H-2026-10-28-01-manual_lookup |

## Settled decisions — never re-raised

- 2026-10-14: page specs (global: location) — approved
- The site runs on wordpress
- Site connection: Novamira MCP, read-only until the handoff is approved; no Application Password setup

## Open VA items

_Every VA item is in one living worklist: `handoffs/VA-WORKLIST.md` (Drive: "Carolina Carpet Cleaning - VA Worklist")._

- **H-2026-10-28-01-manual_lookup** (Gwen) — manual lookup: 9 of 9 open, issued 2026-10-28

## Data on file not used yet

_Inputs the data manifest (methodology/data-manifest.json) says a step must read, where that step has not finished for this client yet._

- **imported-exports** (18 file(s), e.g. `inputs/Carolina Carpet Cleaning - CMS - export-all-urls - 2026-10-28.csv`) — read by discovery:audit
- **discovery-record** (2 file(s), e.g. `discovery/Carolina Carpet Cleaning - Discovery Record - REVIEW.md`) — read by build:evidence, build:facts
- **facts** (1 file(s), e.g. `facts.json`) — read by build:evidence, build:facts
- **settled** (1 file(s), e.g. `decisions-settled.md`) — read by build:evidence, build:facts, build:brief, build:draft, build:drafts, build:write, build:plan

## Flagged for Paul (system)

_None._

## Spend so far

- DataforSEO: $0.00
- Claude API (llm.py): $0.00 over 0 call(s)

## Spend by stage (model)

_Session = the chats and their agents; API = llm.py's direct calls._

| Stage | Runs | Tokens | Session USD | API USD |
|---|---|---|---|---|
| 1 · Setup | 1 | 1,944,639 | $0.80 | $0.00 |
| 2 · Discovery | 2 | 4,718,881 | $2.04 | $0.00 |
| any stage | 3 | 816,224 | $0.13 | $0.00 |
| **total** | 6 | 7,479,744 | $2.98 | $0.00 |

## Spend by step (model)

| Step | Runs | Tokens | Session USD | API USD |
|---|---|---|---|---|
| discovery:discovery | 1 | 3,941,016 | $2.03 | $0.00 |
| new-client | 1 | 1,944,639 | $0.80 | $0.00 |
| answers | 3 | 816,224 | $0.13 | $0.00 |
| discovery:facts-direct | 1 | 777,865 | $0.01 | $0.00 |
| **total** | 6 | 7,479,744 | $2.98 | $0.00 |

Last run: /discovery 2026-10-28T19:04 — facts-direct: owner's answers saved verbatim and marked as facts_direct and proof_sheet
