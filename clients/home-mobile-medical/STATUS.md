# Home Mobile Medical - Status

- **Stage 6 of 8 — Pilot, then batches (batch pilot)**
- **What is happening now:** ready to start: briefs for batch pilot in one run: the evidence gate per page (sources on disk searched first), then a brief for every page it clears
- **Waiting on:** nobody
- **Next action:** `/build home-mobile-medical brief pilot` — Paul opens a **new session on Haiku** in the client folder (`python3 scripts/worktree.py open home-mobile-medical`) and types `/next home-mobile-medical` (agents: build (opus), clerk (haiku))

_Generated 2026-10-09T18:08 by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), one session per stage._

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

## Settled decisions — never re-raised

- 2026-10-08: page specs (global) — approved
- 2026-10-09: Audit deliverables approved (Finding Register, URL Decision Map, Recommendations, Evidence Manifest) — approved
- 2026-10-09: site plan — approved
- Paul 2026-10-09 (Q1): client confirms no leads from any of the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy incl. /services/straight-stair-lifts/). CM-019 C4 passes; all 36 become 301s.
- Paul Exception 2026-10-09 (Q8): citation link-destination check skipped; CM-019 C3 accepted on DataforSEO referring-domain evidence for the 36 URLs. Do not re-raise.
- Paul 2026-10-09 (Q2): redirect the 36 to the appropriate URLs - the audit's defaults (FL/MI -> /services/stair-lifts/, power chairs/scooter lifts -> /services/, ramps -> /services/porch-lifts/; SC legacy duplicates -> their canonical service/location page per the URL Decision Map).

## Open VA items

- **H-2026-10-07-01-wp_setup** (Jonie) — wp setup: 3 of 3 open, issued 2026-10-07
- **H-2026-10-07-02-seopress_settings** (Jonie) — seopress settings: 4 of 4 open, issued 2026-10-07
- **H-2026-10-09-03-redirect** (Jonie) — redirect: 3 of 3 open, issued 2026-10-09
- **H-2026-10-09-04-broken_link** (Jonie) — broken link: 9 of 9 open, issued 2026-10-09
- **H-2026-10-09-05-other** (Jonie) — other: 2 of 2 open, issued 2026-10-09

## Flagged for Paul (system)

_None._

## Spend so far

- DataforSEO: $0.27

Last run: /build 2026-10-09T12:24 — Technical Blocker Checklist written; 14 blocker rows to Jonie in 3 handoffs (redirect chains, internal links through 301s, Q5 status check); no High blocks crawling/indexing/measurement
