# Home Mobile Medical - Status

- **Stage 6 of 8 — Pilot, services, locations, ship (one session each) (batch pilot)**
- **What is happening now:** waiting for Paul's approval — the drafts for batch pilot are ready: review each with the semantic review table (nothing found) and approve them together. No placeholders in the drafts
- **Waiting on:** Paul — the drafts for batch pilot are ready: review each with the semantic review table (nothing 
- **Next action:** Paul types `/approve home-mobile-medical batch:pilot:drafts --review "<who reviewed it>"` (or asks for changes first) · model: Haiku chat

_Generated 2026-10-14T21:00 by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), one session per stage._

## Waiting on

| Who | What | Since | Reference |
|---|---|---|---|
| Paul | the drafts for batch pilot are ready: review each with the semantic review table (nothing found) and approve them together. No placeholders in the drafts | 2026-10-14 | /approve home-mobile-medical batch:pilot:drafts |

## Waiting on (not blocking)

_Open, but the next action above goes ahead without them._

| Who | What | Since | Reference |
|---|---|---|---|
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
- 2026-10-14: batch pilot briefs — approved
- 2026-10-14: batch pilot drafts — approved
- 2026-10-14: batch services briefs — approved
- Paul 2026-10-09 (Q1): client confirms no leads from any of the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy incl. /services/straight-stair-lifts/). CM-019 C4 passes; all 36 become 301s.
- Paul Exception 2026-10-09 (Q8): citation link-destination check skipped; CM-019 C3 accepted on DataforSEO referring-domain evidence for the 36 URLs. Do not re-raise.
- Paul 2026-10-09 (Q2, revised in rewrite 2): redirect the 36 to the appropriate URLs — FL/MI → /stair-lifts/, power chairs/scooter lifts → the homepage (was /services/), ramps → /porch-lifts/; SC legacy duplicates → their canonical root service/location page. No redirect points at /services/ or /service-area/, so there are no chains.
- Repair steps: first call, visit, diagnosis, quote, parts, fix. No service-call or trip charge. Website wording allowed: yes.
- True emergencies are handled after hours; urgent non-emergency calls are scheduled as soon as possible; after-hours availability depends on current demand. Publish in general terms only; do not promise after-hours response.
- Installation itself is quick for every lift type (curved, porch, wheelchair); multiple installs per day possible. Order-to-installed lead time and pad/permit responsibility not answered.
- When you call about a broken stair lift or lift, we first take your call, schedule a visit, diagnose the problem, provide a quote, order parts if needed, and complete the repair. There is no service call or trip charge. We repair any brand of stair lift or lift in our service area.
- Our office is open Monday through Friday, 9 a.m. to 5 p.m. True emergencies are handled after hours; after-hours availability depends on current demand. Urgent non-emergency calls are scheduled as soon as possible.
- Stair lift installations typically take a couple of hours, and we can often complete two per day for curved, porch and wheelchair lifts. The actual timeline depends on project scope and is confirmed during your free in-home estimate.
- Beaufort Medical Equipment (Jason's former company) is not mentioned anywhere on the site or in drafts, including the Beaufort page. The Brand Guide history row stays internal.
- Legacy repair URLs: /hilton-head/stair-lift-repair/ -> 301 to /stair-lift-repair/; /bluffton-sc/wheelchair-lift-repair/ -> 301 to /stair-lift-repair/ (the repair page covers any stair lift or lift, incl. porch and wheelchair lift repair, FAQ 4). Services brief review row 1, option a. 301s go with the publish handoff.

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

## Flagged for Paul (system)

- **F-001** (open, not yet reviewed) 2026-10-14 · build:facts: methodology/sources/sc-lowcountry.md: no rows for Charleston County, Berkeley/Dorchester/Colleton/Hampton counties or their towns (researchers found official permit pages: charleston-sc.gov/856/Permit-Center, charlestoncounty.gov/departments/building-inspection-services, northcharleston.org Building-and-Permit-Inspections, tompsc.com/151/Permit, kiawahisland.gov/building_services.php, cityoffollybeach.com building_planning, goosecreeksc.gov building-permits, cityofhanahan.com/node/86, summervillesc.gov/289/Permitting); HHI permit URL listed returns 404 to fetch (hiltonheadislandsc.gov/permits works); Bluffton Neighborhoods PDF row has no URL; Census QuickFacts returns 403 to the fetch tool and the Census API needs a key, so 65+ shares come via Wikipedia (2020 census). — workaround: Researchers cited the official pages directly and Wikipedia for census figures; Paul adds the rows at /system-review.
- **F-002** (open, not yet reviewed) 2026-10-14 · build:write: Approved site plan (REVISED md + site-plan-revised.plan.json) carries no keyword, area variant, category variant, H1 decision, FAQ topics or link targets per page — the build:plan step requires them; the plan was imported. Briefs have no planned keyword/variant to take. — workaround: Pilot briefs propose keyword (data/rankings), area variant (B2, never B1) and H1 per page, marked 'proposed — confirm at brief approval'; Paul confirms with the briefs approval.
- **F-003** (open, not yet reviewed) 2026-10-14 · build:write: PAA/fan-out routing tables route to the old URLs (/services/stair-lifts/, /service-area/<city>/), so evidence_pack.py tags no question to the new root-slug pages (packs say 'None tagged to this page'). — workaround: Brief-writers read paa-routing.md/fanout-routing.md rows routed to the page's live_url as candidates.
- **F-004** (open, not yet reviewed) 2026-10-14 · build:write: status.json client.route is null for a full client; build.md says ask Paul when missing. — workaround: Ran the pilot as Route A (system writes): the run brief asks for briefs and drafts, and no Paul-written content exists on disk. Paul to confirm route A.
- **F-005** (open, not yet reviewed) 2026-10-14 · build:write: Draft writers put a '## Writer notes' section in the page file and publish.py drafts does not strip it, so the notes would reach the WordPress draft. Also: review.py sheet counts Fix rows as 'fixed silently' before review.py apply has run. — workaround: Recorded as Fix rows (formatting) in the pilot drafts findings; remove the Writer notes section when review.py apply runs after Paul's answer, before ship.
- **F-006** (open, not yet reviewed) 2026-10-14 · build:review: review.py apply crashes (ValueError in LETTERS.index) when a row's 'recommended' is an uppercase letter (pilot drafts row 1 had 'A'); defaults are not lowercased before lookup. — workaround: Passed Paul's answer explicitly as '1a' in --answers ('accept all, 1a'), which parse_answers lowercases.
- **F-007** (open, not yet reviewed) 2026-10-14 · build:facts: evidence.py questions --all overwrote the open facts-round file 'Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md' (Q1-Q3, already asked and waiting) with an empty 0-question version on a same-day re-run; it should not replace a set that is still open. Also settled.py filter reports the still-open fact:svc-repair-maintenance:service_process as 'already answered'. — workaround: Left the file changed (restore was blocked by the permission system); the sent version is intact in git HEAD (f5c00c6) and in facts-round-all-2026-10-14.questions.json. Paul or the main chat can restore it with git checkout of that one file.
- **F-008** (open, not yet reviewed) 2026-10-14 · build:write: Build agent started per-page brief agents in the background and stopped before they finished, leaving the run unrecorded (briefs on disk, none recorded, no review, run not finished). — workaround: Resume the write step in a fresh build agent that records the briefs first; do not start new background brief agents without waiting for their results.
- **F-009** (open, not yet reviewed) 2026-10-14 · build:write: Main chat relayed the same interim status about eight times (subagent hand-backs repeated). — workaround: Relay each agent hand-back once; report only changes in state.
- **F-010** (open, not yet reviewed) 2026-10-14 · build:write: Main chat could not see the child agents' results (brief-writer reports arrived only as hand-backs to the build agent). — workaround: Have the build agent write each child result to a file and report the file path to the main chat.
- **F-011** (open, not yet reviewed) 2026-10-14 · build:write: After the batch briefs revise decision was committed, status.py page-stage still refuses the other three briefs with 'batch services briefs are already approved'. Only the curved brief recorded; batch shows briefs_written. — workaround: Stop; do not record the other briefs or start drafts until the revise state is fixed in the system session.
- **F-012** (open, not yet reviewed) 2026-10-14 · build:drafts: review.py usage check (§3.4) recommends using 'the strongest excerpt' even when every pack excerpt is off-service (general wheelchairs, lift chairs, rentals — not offered) or a negative review; evidence_pack keyword matching put the same 4 off-topic excerpts on all four service packs. — workaround: Pre-empted the auto usage rows with page+usage+review-evidence findings decided 'leave as written' (drafts-findings.json); review.py dropped its own rows as duplicates.

## Spend so far

- DataforSEO: $0.27

## Spend by step (model)

_Nothing recorded yet (run.py finish --tokens --cost)._

Last run: /build 2026-10-14T21:00 — Accepted services drafts review (accept all) applied to curved (1), porch (3), wheelchair (4); all four drafts recorded again; repair unchanged.
