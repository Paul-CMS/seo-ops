# Home Mobile Medical - Status

- **Stage 5 of 8 — Build plan and blockers**
- **What is happening now:** ready to start: one facts round for every page: the evidence grids, the researcher looks up every public fact, reviews attached (CM-057), then one pre-filled question set grouped by fact
- **Waiting on:** nobody
- **Next action:** `/build home-mobile-medical facts` — Paul opens a **new session on Haiku** in the client folder (`python3 scripts/worktree.py open home-mobile-medical`) and types `/next home-mobile-medical` (agents: build (opus), researcher (sonnet), clerk (haiku)) · model: Haiku chat

_Generated 2026-10-14T07:32 by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), one session per stage._

## Waiting on

| Who | What | Since | Reference |
|---|---|---|---|
| — | nothing | | |

## Waiting on (not blocking)

_Open, but the next action above goes ahead without them._

| Who | What | Since | Reference |
|---|---|---|---|
| Jonie | blockers not cleared: H-2026-10-09-03-redirect-01 is issued; H-2026-10-09-03-redirect-02 is issued; H-2026-10-09-03-redirect-03 is issued; H-2026-10-09-04-broken_link-01 is issued; H-2026-10-09-04-broken_link-02 is issued (+9 more). When Jonie returns the blocker handoff, /verify checks every item; the blockers count as cleared when all are done and verified — no approval | 2026-10-09 | /verify home-mobile-medical |
| Jonie | wp setup handoff — 3 of 3 item(s) open | 2026-10-07 | H-2026-10-07-01-wp_setup |
| Jonie | seopress settings handoff — 4 of 4 item(s) open | 2026-10-07 | H-2026-10-07-02-seopress_settings |
| Jonie | redirect handoff — 3 of 3 item(s) open | 2026-10-09 | H-2026-10-09-03-redirect |
| Jonie | broken link handoff — 9 of 9 item(s) open | 2026-10-09 | H-2026-10-09-04-broken_link |
| Jonie | other handoff — 2 of 2 item(s) open | 2026-10-09 | H-2026-10-09-05-other |
| Jonie | redirect handoff — 1 of 1 item(s) open | 2026-10-09 | H-2026-10-09-06-redirect |
| Jonie | redirect handoff — 1 of 1 item(s) open | 2026-10-09 | H-2026-10-09-07-redirect |

## Settled decisions — never re-raised

- 2026-10-08: page specs (global) — approved
- 2026-10-09: Audit deliverables approved (Finding Register, URL Decision Map, Recommendations, Evidence Manifest) — approved
- 2026-10-14: site plan — approved
- Paul 2026-10-09 (Q1): client confirms no leads from any of the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy incl. /services/straight-stair-lifts/). CM-019 C4 passes; all 36 become 301s.
- Paul Exception 2026-10-09 (Q8): citation link-destination check skipped; CM-019 C3 accepted on DataforSEO referring-domain evidence for the 36 URLs. Do not re-raise.
- Paul 2026-10-09 (Q2, revised in rewrite 2): redirect the 36 to the appropriate URLs — FL/MI → /stair-lifts/, power chairs/scooter lifts → the homepage (was /services/), ramps → /porch-lifts/; SC legacy duplicates → their canonical root service/location page. No redirect points at /services/ or /service-area/, so there are no chains.

## Open VA items

_Every VA item is in one living worklist: `handoffs/VA-WORKLIST.md` (Drive: "Home Mobile Medical - VA Worklist")._

- **H-2026-10-07-01-wp_setup** (Jonie) — wp setup: 3 of 3 open, issued 2026-10-07
- **H-2026-10-07-02-seopress_settings** (Jonie) — seopress settings: 4 of 4 open, issued 2026-10-07
- **H-2026-10-09-03-redirect** (Jonie) — redirect: 3 of 3 open, issued 2026-10-09
- **H-2026-10-09-04-broken_link** (Jonie) — broken link: 9 of 9 open, issued 2026-10-09
- **H-2026-10-09-05-other** (Jonie) — other: 2 of 2 open, issued 2026-10-09
- **H-2026-10-09-06-redirect** (Jonie) — redirect: 1 of 1 open, issued 2026-10-09
- **H-2026-10-09-07-redirect** (Jonie) — redirect: 1 of 1 open, issued 2026-10-09

## Data on file not used yet

_Inputs the data manifest (methodology/data-manifest.json) says a step must read, where that step has not finished for this client yet._

- **reviews** (1 file(s), e.g. `data/reviews/reviews.csv`) — read by build:evidence, build:facts
- **reviews-raw** (2 file(s), e.g. `data/reviews/raw/reviews.json`) — read by the step that reads reviews
- **review-mentions** (1 file(s), e.g. `data/reviews/mentions.csv`) — read by build:evidence, build:facts
- **paa-questions** (2 file(s), e.g. `data/paa/paa-questions.csv`) — read by build:evidence, discovery:fanout
- **paa-raw** (20 file(s), e.g. `data/paa/raw/curved-stair-lifts-beaufort.json`) — read by the step that reads paa-questions
- **fanout-queries** (2 file(s), e.g. `data/fanout/fanout-queries.csv`) — read by build:evidence
- **fanout-raw** (10 file(s), e.g. `data/fanout/raw/curved-stair-lifts-beaufort.json`) — read by the step that reads fanout-queries
- **blog-inventory** (1 file(s), e.g. `inputs/Home Mobile Medical - CMS - blog-inventory - 2026-09-18.csv`) — read by blog:map
- **entity-profile** (1 file(s), e.g. `inputs/Home Mobile Medical - MANUAL - entity-profile - 2026-09-18.md`) — read by discovery:discovery
- **facts** (1 file(s), e.g. `facts.json`) — read by build:evidence, build:facts
- **settled** (1 file(s), e.g. `decisions-settled.md`) — read by build:evidence, build:facts, build:brief, build:draft, build:drafts, build:write, build:plan

## Flagged for Paul (system)

_None._

## Spend so far

- DataforSEO: $0.27

## Spend by step (model)

_Nothing recorded yet (run.py finish --tokens --cost)._

Last run: /build 2026-10-09T12:24 — Technical Blocker Checklist written; 14 blocker rows to Jonie in 3 handoffs (redirect chains, internal links through 301s, Q5 status check); no High blocks crawling/indexing/measurement
