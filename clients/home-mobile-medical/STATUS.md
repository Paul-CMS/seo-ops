# Home Mobile Medical - Status

- **Stage 6 of 8 — Pilot, services, locations, ship (one session each) (batch pilot)**
- **What is happening now:** Paul is reviewing what the last step produced; /next continues
- **Waiting on:** Paul — build:facts finished (run 20261014-100458-build-2be7) and that stage is in review mode — l; Client (via Paul) — How the service is delivered (steps, methods, equipment) — what should we say? If it depen; Client (via Paul) — Any emergency or after-hours help for a stopped lift? (facts round 2026-10-14, Q2)
- **Next action:** `/next home-mobile-medical` once the wait above is over · model: Haiku chat

_Generated 2026-10-14T10:21 by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), one session per stage._

## Waiting on

| Who | What | Since | Reference |
|---|---|---|---|
| Paul | build:facts finished (run 20261014-100458-build-2be7) and that stage is in review mode — look at what it produced, then type /next to go on. Next would be: /build home-mobile-medical write pilot (batch pilot in one run: every brief, then one draft per page (each from its own fresh sub-agent, CM-043), then the batch review side by side) | 2026-10-14 | /next home-mobile-medical |
| Client (via Paul) | How the service is delivered (steps, methods, equipment) — what should we say? If it depends, on what? | 2026-10-14 | fact:svc-repair-maintenance:service_process |
| Client (via Paul) | Any emergency or after-hours help for a stopped lift? (facts round 2026-10-14, Q2) | 2026-10-14 | fact:d:emergency |
| Client (via Paul) | Order-to-install and install times for curved, porch and wheelchair lifts; who handles pad and permit (facts round 2026-10-14, Q3) | 2026-10-14 | fact:svc-curved-stair-lifts:install_time |

## Waiting on (not blocking)

_Open, but the next action above goes ahead without them._

| Who | What | Since | Reference |
|---|---|---|---|
| Client (via Paul) | waiting for the answers to the facts round (clients/home-mobile-medical/interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md; 3 fact(s) open) — when they arrive, each is recorded once (run.py fact / --settle) and the grids re-run | 2026-10-14 | /interview home-mobile-medical facts-answers all |
| Jonie | blockers not cleared: H-2026-10-09-03-redirect-01 is issued; H-2026-10-09-03-redirect-02 is issued; H-2026-10-09-03-redirect-03 is issued; H-2026-10-09-04-broken_link-01 is issued; H-2026-10-09-04-broken_link-02 is issued (+9 more). When Jonie returns the blocker handoff, /verify checks every item; the blockers count as cleared when all are done and verified — no approval | 2026-10-14 | /verify home-mobile-medical |
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
- 2026-10-14: page specs (global: location) — approved
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

- **paa-questions** (2 file(s), e.g. `data/paa/paa-questions.csv`) — read by build:evidence, discovery:fanout
- **paa-raw** (20 file(s), e.g. `data/paa/raw/curved-stair-lifts-beaufort.json`) — read by the step that reads paa-questions
- **fanout-queries** (2 file(s), e.g. `data/fanout/fanout-queries.csv`) — read by build:evidence
- **fanout-raw** (10 file(s), e.g. `data/fanout/raw/curved-stair-lifts-beaufort.json`) — read by the step that reads fanout-queries
- **blog-inventory** (1 file(s), e.g. `inputs/Home Mobile Medical - CMS - blog-inventory - 2026-09-18.csv`) — read by blog:map
- **entity-profile** (1 file(s), e.g. `inputs/Home Mobile Medical - MANUAL - entity-profile - 2026-09-18.md`) — read by discovery:discovery
- **interviews** (2 file(s), e.g. `interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md`) — read by build:evidence, interview:facts-answers

## Flagged for Paul (system)

- **F-001** (open, not yet reviewed) 2026-10-14 · build:facts: methodology/sources/sc-lowcountry.md: no rows for Charleston County, Berkeley/Dorchester/Colleton/Hampton counties or their towns (researchers found official permit pages: charleston-sc.gov/856/Permit-Center, charlestoncounty.gov/departments/building-inspection-services, northcharleston.org Building-and-Permit-Inspections, tompsc.com/151/Permit, kiawahisland.gov/building_services.php, cityoffollybeach.com building_planning, goosecreeksc.gov building-permits, cityofhanahan.com/node/86, summervillesc.gov/289/Permitting); HHI permit URL listed returns 404 to fetch (hiltonheadislandsc.gov/permits works); Bluffton Neighborhoods PDF row has no URL; Census QuickFacts returns 403 to the fetch tool and the Census API needs a key, so 65+ shares come via Wikipedia (2020 census). — workaround: Researchers cited the official pages directly and Wikipedia for census figures; Paul adds the rows at /system-review.

## Spend so far

- DataforSEO: $0.27

## Spend by step (model)

_Nothing recorded yet (run.py finish --tokens --cost)._

Last run: /build 2026-10-14T10:21 — Facts round: 100 public facts looked up, grids 28 pass/5 warn/0 block, 3-question set for Paul
