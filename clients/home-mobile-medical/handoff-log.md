# Home Mobile Medical - Handoff Log

Generated from the safety log (clients/home-mobile-medical/log.md) — do not edit. Each run adds its section with `run.py finish --handoff <file>`. The newest section is at the bottom.

## /new-client · 2026-10-07 · run 20261006-112201-new-client-fb9a

**What I did**
- Imported Home Mobile Medical (mid-stream, old ChatGPT workflow) from the v3 folder `Home Mobile Medical - TMS` (Drive 1Hlfhaelu3mvsAItJgg0Zpi7T2_ccrNRp). Read every file there plus the reference package in the older TMS folder (URL Decision Map, Client Decision Log, Client Gap Sheet). Nothing in Drive was changed.
- Found the old Approval Record entirely unsigned, no Finding Register / Recommendations / Evidence Manifest, and no build files anywhere (Paul: lost). Brief said "stages 0-5 complete"; the records did not support it, so nothing was signed on Drive evidence alone.
- Built the claims proof list (`discovery/claims-proof-list.md`); Paul and the client answered it over two days. Reconciled the Brand Guide into the standard template (`brand-guide.md`). Wrote the out-of-area page list, the rename list and the import proposal.
- Paul approved the import 2026-10-07: entity_approved, proof_sheet_approved, brand_guide_approved (+ proof_sheet_returned condition). 34 pages planned; S01-S05, S09, S10 done, S11 skipped.

**What was decided, and why**
- Sensitivity health_adjacent (Paul; classifier said health). No practitioner sign-off.
- Area entity South Carolina Lowcountry; Georgia is served but only from a separate microsite (own project). Florida and Michigan dropped.
- Destructive URL actions are 301s, never 410s, each after the CM-019 DataforSEO check; DataforSEO replaces Search Console. The pull runs in the normal data step, not inside the import.
- Hubs: /service-area/ (Lowcountry), /service-area/charleston/ (Charleston metro), /service-area/hhi-beaufort/ (Hilton Head Island-Bluffton-Port Royal metro). Rule proposed as lessons.md L-008.
- GBP: primary category only (Mobility equipment supplier). Beaufort GBP address stays in the footer for GBP cross-reference; still an SAB.
- Claims: brand line "Stannah, Bruno and Harmar", no dealer wording; Jason plus one helper; one-day installs of 3-4 hours, "in most cases"; general repairs any brand; manufacturer warranty only; no licence claim; placeholder reviews removed; safety line approved.
- Audit route: option B (system runs the audit on the existing evidence; no new crawl).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| WordPress Editor user + Application Password | Jonie (handoff next), then Paul (.env) | All WordPress work |
| After-hours service, trip charge, positioning answers | Client via Paul | Only the copy that uses them |
| Logo, owner photo, ID page, Apple Maps, 6 county Wikidata IDs | Paul / Finish | Schema |
| Stannah dealer evidence | Paul | Nothing (brand line no longer claims dealer status) |
| Old URL Decision Map rows superseded by Paul's decisions | Audit step | 301 list |
| L-008 metro hubs; county-hub spec DRAFT | Paul | Hub pages in Build |
| Georgia microsite | Paul (new /new-client) | — |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide | clients/home-mobile-medical/brand-guide.md | Approved (import) |
| Claims proof list | clients/home-mobile-medical/discovery/claims-proof-list.md | Marked by Paul |
| Out-of-area pages | clients/home-mobile-medical/out-of-area-pages.md | GA/FL/MI list for the 301 plan |
| Old URL Decision Map | Drive 1xsYWtpEDDiW8Szv545h2zJBZGzRSzZ-M-W2bgaNN370 (older TMS folder) | Input to the audit, partly superseded |
| Crawl and evidence | v3 `01 - Discovery and Audit/Evidence/` | SF 2026-09-18, BL, LNKD, Local Dominator |
| Rename list | clients/home-mobile-medical/rename-list.md | For Paul; nothing renamed |

**What I could not check**
- The live site: the browser pane refused homemobilemedical.com and fetches failed a certificate check. All site quotes are from the 2026-09-18 crawl.
- GBP fields directly; SC Secretary of State record (none found).

**Anything the next agent would otherwise get wrong**
- Nothing was ever built: all 34 pages are planned, not written. The "IMPORTED" site plan is only a page list — re-run the full site plan after the audit.
- The old URL Decision Map predates Paul's decisions: its Georgia KEEP rows, its 410s and the hhi-beaufort split are all superseded. Georgia URLs wait for the microsite; FL/MI and retired pages are 301s after DataforSEO.
- Do not use the old Stannah "verified dealer" line or the homepage testimonials.

## /wp-check · 2026-10-07 · run 20261007-172152-wp-check-12e0

**What I did**
- Issued handoff H-2026-10-07-01-wp_setup to Jonie: create the `[REDACTED]` Editor user, its Application Password (sent to Paul privately), and report the SEOPress version.
- Gave Paul the exact credential-file lines (`wp.py env-lines home-mobile-medical`).

**What was decided, and why**
- WordPress setup goes to Jonie (gates.json owner for wp_setup). No WordPress connection was attempted: there are no credentials yet.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| [REDACTED] user + Application Password | Jonie | All WordPress work |
| Three credential lines | Paul | /wp-check home-mobile-medical |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Setup worksheet | clients/home-mobile-medical/handoffs/H-2026-10-07-01-wp_setup.md / .csv | Sent to Jonie |

**What I could not check**
- Whether WordPress, SEOPress or Application Passwords are enabled on the site (site unreachable from this session).

**Anything the next agent would otherwise get wrong**
- The connection test is `/wp-check home-mobile-medical`, only after Paul has added the credential lines.

## /wp-check · 2026-10-07 · run 20261007-172720-wp-check-bb94

**What I did**
- Ran `wp.py check`: credentials present, REST API reachable, logged in as [REDACTED] (Editor), draft page and post created, every SEOPress 6.8+ per-page field written and read back on a test draft. Test drafts trashed; nothing published.
- `wp.py` issued H-2026-10-07-02-seopress_settings to Jonie (4 items) because SEOPress site-wide settings need an Administrator to read.

**What was decided, and why**
- Result: connected. The condition "WordPress connected" is met for 30 days. The account stays Editor (setup §1).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| SEOPress site-wide settings check | Jonie | Audit step S20 evidence |
| Kadence head-code meta key | Found during the WordPress pilot | Schema in Finish |
| WordPress pilot (`--pilot`) | Paul, later | Direct structural writes (titles, robots, canonical, schema) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| SEOPress settings worksheet | clients/home-mobile-medical/handoffs/H-2026-10-07-02-seopress_settings.md / .csv | Sent to Jonie |

**What I could not check**
- SEOPress site-wide settings (Administrator only).

**Anything the next agent would otherwise get wrong**
- H-2026-10-07-01-wp_setup (user + Application Password) is in effect done: the check logged in as [REDACTED]. Ingest Jonie's returned worksheet to close it.

## /drive-mirror · 2026-10-07 · run 20261007-172819-drive-mirror-bbb0

**What I did**
- Archived the four ChatGPT-era records in the v3 folder (dated names, moved to `_Archive`) and uploaded the system's Approval Record, Handoff Log, Document Checklist and Brand Guide as real `.md` files at the client-folder root.

**What was decided, and why**
- Paul approved archiving files the system did not originally upload (CLAUDE.md §8 otherwise allows it only for system uploads). Nothing deleted.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| READ FIRST doc, SUPERSEDED proof sheet, LD→LNKD rename | Paul (rename list) | Nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Drive records | v3 `Home Mobile Medical - TMS/` root | Current as of this run |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- The "00 - … READ FIRST" Google Doc in Deliverables still describes the old ChatGPT audit; the system records at the folder root govern.

## /discovery · 2026-10-07 · run 20261007-173133-discovery-dce1

**What I did**
- Ran the data step on Paul's approval (~$0.70 estimate, fan-out cap 10): reviews (S06), domain rankings + "best" volumes (S07), backlinks (S08), People Also Ask (S19), query fan-out (S21). 39 DataforSEO calls, **$0.265 actual**. S20 recorded skipped (SEOPress settings need Administrator; Jonie's handoff H-2026-10-07-02).
- Routed 35 PAA questions and 354 fan-out queries; wrote customer-language themes (no reviewer names); aggregated backlinks per URL.

**What was decided, and why**
- Rankings and backlinks pulled for the whole domain so every URL (incl. GA/FL/MI and retired) is covered for CM-019.
- Fan-out kept to 10 seeds (Beaufort, Charleston); Paul did not approve 20.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| S05 crawl tables not yet in `inputs/crawl/` (Drive v3 Evidence) | Audit step | S12 join to all 118 URLs |
| SEOPress settings worksheet | Jonie | S20 → done |
| CM-019 conditions 3–4 for FL/MI (GBP/citation destination; client confirms no leads) | Audit / Paul | Final 301 list |
| Fan-out for Hilton Head Island and Bluffton (+$0.07) | Paul | Optional |
| Confirm ranked_keywords price in dfs_prices.json ($0.012 + $0.00012/row) | Paul | Future --confirmed prompts |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Reviews | clients/home-mobile-medical/data/reviews/ | Done |
| Rankings | clients/home-mobile-medical/data/rankings/ | Done |
| Backlinks | clients/home-mobile-medical/data/backlinks/Home Mobile Medical - DFS - backlinks - 2026-10-07.csv | Done |
| PAA + fan-out routing | clients/home-mobile-medical/data/paa/, data/fanout/ | Done |

**What I could not check**
- Rankings are US-level only (DataforSEO Labs limit).

**Anything the next agent would otherwise get wrong**
- GBP shows 2.9 stars from 19 reviews, all 2017–2023 and about the old walk-in medical-supply/rental store; none mentions lifts. Not CM-020 proof and almost no lift customer language.
- No /services/ page ranks; the homepage (56 keywords) and the Medicare post (17) carry the domain. "Best" variants have no SC volume.
- CM-019 exceptions (rank or have links → Needs Evidence): /savannah-ga/, /service-area/savannah-ga/, /savannah/stair-lift/, /charleston-sc/mobility-ramps/, /service-area/mt-pleasant-sc/, /bluffton-sc/, /bluffton-sc/wheelchair-lift-repair/, /bluffton-sc/stair-lift-installer/, /charleston/stair-lift/, /hilton-head/stair-lift/. No FL/MI URL ranks or has links.

## /discovery · 2026-10-08 · run 20261007-203219-discovery-784c

**What I did**
- Ran the audit on the existing evidence (option B, no new crawl): brought the 2026-09-18 Screaming Frog exports and other Drive v3 evidence into `inputs/` (read-only copies), then S12 ingest, S13 entity, S14 architecture, S15 conformance, S16 technical.
- S17: independent audit-reviewer in a fresh context — 28 findings confirmed, 12 revised, 0 withdrawn; 7 destructive URL recommendations withdrawn (they fail CM-019 C1/C2).
- S18: applied the reviewer's five fixes (CF-001 → CF-LOCAL-001; lessons.md L-009 PROPOSED; manifest metadata; cross-check wording; URL-map source labels), rendered four REVIEW deliverables, marked `audit_deliverables`. Tests: 283 passed.

**What was decided, and why**
- Paul's decisions applied throughout: 301 never 410; Georgia held for the microsite; FL/MI dropped; metro hubs (L-008 proposed, county-hub spec DRAFT → Low); blog disposition deferred to the Blog Decision Map; CM-040 claims.
- Independence per CM-026 (DEC-LOCAL-006).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Q1 client confirms no leads on 36 retirement URLs | Paul / client | Any 301 |
| Q2 redirect targets | Paul | 301 handoffs |
| Q3 the 10 CM-019-failing URLs: keep live or Paul Exception | Paul | Their disposition |
| Q4 / CF-LOCAL-001 / L-009 homepage H1 lock | Paul | Homepage H1 |
| Q9 GBP listing history after the BME sale | Client via Paul | Review replies, GBP changes |
| Q5, Q6 page status checks | Jonie | 2 + 40 URL rows |
| Q7 grid centre/device; Q8 citation link destinations | Gwen | Grid findings; CM-019 C3 |
| S20 SEOPress settings | Jonie | Technical evidence |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Finding Register | clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Finding Register - REVIEW.md | For Paul |
| URL Decision Map | …/deliverables/Home Mobile Medical - URL Decision Map - REVIEW.md | For Paul |
| Recommendations | …/deliverables/Home Mobile Medical - Recommendations - REVIEW.md | For Paul |
| Evidence Manifest | …/deliverables/Home Mobile Medical - Evidence Manifest - REVIEW.md | For Paul |

**What I could not check**
- Body text (free SF crawl, no rendering, two H2s per page) — many section/FAQ/claim checks are Needs Evidence. No structured-data export.

**Anything the next agent would otherwise get wrong**
- No URL is a final 301 yet: condition 4 is pending everywhere and condition 3 rests on backlink-domain matching until Gwen checks listing links (Q8).
- Two older log entries still say CF-001 (append-only); the conflict is CF-LOCAL-001.
- All specs are DRAFT: conformance failures are advisory.

## /discovery · 2026-10-09 · run 20261009-071238-discovery-94fa

**What I did**
- Recorded Paul's answers to Q1, Q2 and Q8 as settled decisions.
- Appended 36 superseding rows to the URL Decision Map: each is now Redirect (301) to its default target, with CM-019 C1–C4 passing.
- Appended superseding rows for F-003, F-013, F-014, F-015 and F-035, and marked Q1, Q2 and Q8 answered. Added DEC-LOCAL-008 to the audit decisions.
- Re-rendered all four audit deliverables (still REVIEW) and re-marked them for audit_approved.

**What was decided, and why**
- Q1 (Paul, 2026-10-09): the client confirms no leads from the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy including /services/straight-stair-lifts/). CM-019 C4 passes.
- Q8 (Paul Exception): the citation listing check is waived. C3 is accepted on the DataforSEO referring-domain evidence.
- Q2: the audit's default redirect targets.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Approval 2 (audit_approved) | Paul | Redirect handoffs, safe fixes, Build |
| Q3 (the 10 URLs failing CM-019), Q4 (CF-001 homepage H1) | Paul | Those dispositions |
| Q5–Q7, Q9 | Jonie / Gwen / client | Their findings |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| URL Decision Map | clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - URL Decision Map - REVIEW.md | REVIEW |
| Finding Register, Recommendations, Evidence Manifest | same folder | REVIEW |

**What I could not check**
- Citation listing destinations (Q8 was waived by Paul).

**Anything the next agent would otherwise get wrong**
- Q1, Q2 and Q8 are settled. Never re-raise them.
- The 36 301s go to Jonie as handoffs only after audit_approved.
- The /hilton-head/stair-lift-repair/ redirect is paired with the publish of /services/stair-lift-repair/.
- The 15 Georgia rows stay on Hold.

## /build · 2026-10-09 · run 20261009-122052-build-8f9c

**What I did**
- Read the approved Finding Register (latest revision of each of the 40 findings) and the matching URL Decision Map rows. Wrote `Home Mobile Medical - Technical Blocker Checklist - REVIEW.md` and marked it as artifact `blocker_checklist`.
- Issued three blocker handoffs to Jonie (`--blockers`), 14 rows in all: H-2026-10-09-03-redirect (3 two-hop redirect chains, F-033), H-2026-10-09-04-broken_link (9 pages with internal links through 301s, F-033), H-2026-10-09-05-other (2-page status/robots check only, F-038 / Q5).
- Copied the checklist and the three handoffs (.md + .csv) to Drive `02 - Build`.

**What was decided, and why**
- None of the 12 High findings blocks crawling, indexing or measurement. Each is fixed by a rebuild, by `/implement structural` (decided 301s and menu removals from the URL Decision Map) or by the Blog Decision Map, so none is a blocker row.
- F-035 sitemap removals stay with the redirect handoff in `/implement structural`, because the finding pairs each removal with its 301.
- The chain repoints target the slash URL (F-033 text). The Decision Map target is slash-less, which would leave one hop.
- Links to /services/stair-lift/ are sent to /services/stair-lifts/ (F-034's natural target), not to the legacy /hilton-head/stair-lift/. The redirect itself is unchanged.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Return the 3 blocker handoffs, then `/verify` | Jonie, then system | blockers_cleared (release) |
| F-034 redirect target; Q3 (10 value URLs) | Paul | /services/stair-lift/ target; 6 F-013 and 4 F-003 URLs |
| F-040 GA4/GSC access from the client | Paul | measurement baseline |
| Decided 301s, F-035 sitemap removals, F-002/F-003 menu removals | `/implement structural` (not yet run) | entity cleanup |
| F-036 utility metas (/contact/, /terms-conditions/ + 4) | `/implement safe` | — |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Technical Blocker Checklist | clients/home-mobile-medical/build/Home Mobile Medical - Technical Blocker Checklist - REVIEW.md | written, marked |
| Blocker handoffs | clients/home-mobile-medical/handoffs/H-2026-10-09-0{3,4,5}-*.md/.csv | issued to Jonie |
| Item sources | clients/home-mobile-medical/build/blockers/*-items.csv | inputs |

**What I could not check**
- Live status of any URL. WordPress was not touched.
- Which page each redirecting link sits on. The crawl export has inlink counts only, so each link row lists all 8 redirecting URLs and Jonie marks "none found" where there are none.

**Anything the next agent would otherwise get wrong**
- The site plan is already approved (imported), so `/build plan` is not needed. The next Build work is the evidence gate for the first batch.
- The 36 decided 301s are NOT in the blocker handoff. Issue them in `/implement structural` with their F-035 sitemap removals. Pair /hilton-head/stair-lift-repair/ with the svc1 publish.

## /drive-mirror · 2026-10-09 · run 20261009-201533-drive-mirror-0325

**What I did**
- rewrite 2 URL migration: worklist rows for the redirect / slug clearing

## /drive-mirror · 2026-10-09 · run 20261009-222728-drive-mirror-744e

**What I did**
- Added the 301 /services/ → homepage (worklist section 3).
- Pointed the three -sc-2 redirects (not yet done by Jonie) at the root URLs, so there are no chains.

## /build · 2026-10-14 · run 20261014-100458-build-2be7

**Step:** the one facts round (P10) for all 33 pages in the approved site plan.

**Done**
- reviews.py extract: 8 review topics. None was reported by 3 or more reviewers, so none needed checking by meaning.
- Page facts files (build/evidence/<page>.facts.json):
  - city_served on 26 location pages (Brand Guide E, Paul 2026-10-07).
  - service_scope and service_process on the service pages, core_services (homepage) and company_story (about), all from Brand Guide D. Client Confirmed facts only (change #158).
- Researcher (Sonnet) ran 5 parallel lookups for 28 location and hub pages: 100 public facts (59 found, 37 partial, 4 not found). Every one is logged in build/{pilot,loc-hhi,loc-charleston}/research-log.csv. The group with the hub-hhi-beaufort, Beaufort, Port Royal, Lady's Island and Laurel Bay pages first got an empty page list; it was resent and confirmed done (18 facts).
- Not found: Levy neighborhoods, Levy place_entities, Laurel Bay neighborhoods, Folly neighborhoods. Under CM-061 §8 these sections are left out by default and never asked.
- Google rating recorded with run.py fact: 2.9 stars from 19 reviews (DataforSEO pull 2026-10-08). Paul should know it is low. Some reviews date from the old medical-equipment era.
- Client search order logged for 6 gaps (RL-evidence-1..4, RL-services-1..4): emergency, awards, associations, the repair process, and install time for curved, porch and wheelchair lifts.
  - Awards and associations: none found (no BBB listing). They stay "None" and are not asked.
- Grids re-run: 28 PASS, 5 WARN (service pages, supporting gaps only), 0 BLOCK.
- evidence.py questions --all ran once and produced 1 generic question. I rewrote it pre-filled and added Q2 (after-hours) and Q3 (install times, pad and permit).
  - The set is in interviews/facts/facts-round-all-2026-10-14.questions.json. settled.py filter kept 3; questions.py check passed.
  - Q2 and Q3 were asked once with run.py decision --ask.

**Facts round for Paul:** interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md, 3 questions. Paul sends it; the answers go in with /interview home-mobile-medical facts-answers all.

**Flags:** F-001. sc-lowcountry.md has no rows for Charleston, Berkeley, Dorchester, Colleton or Hampton counties and their towns; the HHI permit URL returns 404 when fetched; the Bluffton PDF has no URL; Census QuickFacts returns 403, so 65+ shares come from Wikipedia's 2020 census figures.

**For the brief writers:**
- Folly naming: the official site says "City of Folly Beach". The Discovery Record's Folly Island vs Folly Beach conflict is still open, and it is Paul's call.
- Yemassee is mostly in Hampton County. Okatie spans Beaufort and Jasper.
- Permit offices for Walterboro and Hollywood are partial: confirm with the town.

**Not done:** none. The Brand Guide was not written (write-back happens at brief approval, CM-061 §6).

## /build · 2026-10-14 · run 20261014-125319-build-9170

**Done**
- Briefs: `build/pilot/briefs/SB - Stair Lifts - Home Mobile Medical.md`, `build/pilot/briefs/LB - Beaufort SC - Home Mobile Medical.md` (recorded with page-stage brief).
- Drafts, one fresh subagent each: `build/pilot/drafts/svc-stair-lifts.md`, `build/pilot/drafts/loc-beaufort-sc.md` (recorded with page-stage draft). Self-checks E1–E10 and spec checks in each file's Writer notes: all pass except E10/COM-13 on the stair-lifts safety statement (grade 11.3, Paul's verbatim D text).
- Install time on stair lifts uses Decision 016 (client_confirmed 2026-10-07); the website's "a few hours" line is superseded and not used. Beaufort has no install-time claim.
- One checker pass over both drafts: `build/pilot/drafts-findings.json` (12 findings) → `review.py sheet` → `build/pilot/drafts-review.csv` / `.md`: 1 Ask, 8 Decided for you (7 carried + usage check), 3 Fix.
- `status.py batch home-mobile-medical pilot --state drafts_written --review-sheet build/pilot/drafts-review.csv`.
- Flag F-005: Writer notes are not stripped by publish.py; review.py counts Fix rows as "fixed silently" before apply.

**Open — waiting on Paul**
- Ask 1 (kind 2): stair-lifts safety statement at grade 11.3 — A keep verbatim (recommended) / B approve a plainer version.
- review.py apply NOT run (Ask row open). The 3 Fix rows apply then: Beaufort cost FAQ kept to the local quote angle (overlap with stair-lifts FAQ 1, BB-316); remove `## Writer notes` from both page files before ship.
- Still `[NEED: …]`, not filled: after-hours/emergency, curved/porch/wheelchair install times, pad and permit (Beaufort FAQ 2), price range, Beaufort city map.

**Next**
- Paul answers the sheet: `/build home-mobile-medical review pilot drafts "<his line>"` → review.py apply → `/approve home-mobile-medical batch:pilot:briefs batch:pilot:drafts mode:build:brief=auto` → pilot-corrections.

## /build · 2026-10-14 · run 20261014-131553-build-b121

- Paul's line: "accept all", with Ask 1 = A.
- review.py apply → build/pilot/drafts-apply.json: 9 rows recorded (row 1 answered by Paul = a/A; rows 2–9 decided-for-you, accepted by default). Ledger: build/pilot/findings-ledger.json.
- Ask 1 (svc-stair-lifts safety statement, grade 11.3): A, approved Section D text kept word for word, unchanged.
- Rows 2–9: already in the drafts as decided; no text change needed.
- Fix rows (drafts-fixes.json) applied:
  - loc-beaufort-sc BB-316: cost FAQ reframed as "How Do I Get a Stair Lift Quote for My Beaufort Home?" (photo, free in-home estimate, stair count). The stair-lifts FAQ "How Much Does a Stair Lift Cost?" stays the cost answer. New answer grade 5.5.
  - loc-beaufort-sc and svc-stair-lifts P11: "## Writer notes" removed from both page files; the notes are kept in handoffs/run-20261014-131553-build-b121.writer-notes.md.
- Flag F-006: review.py apply crashed on the uppercase recommended value "A" (LETTERS.index). Workaround: the answers were passed as "accept all, 1a".
- Not done: the drafts were not re-recorded with the page-stage command (the coordinator said not to call it). If the drafts approval is pinned to file versions, the coordinator must re-record both drafts.
- Open placeholders (Beaufort): [NEED: permit/pad — facts round Q3], [NEED: city map]. Link-wheel rows stay placeholders for ship.

## /build · 2026-10-14 · run 20261014-133132-build-f0c5

**Gate:** `status.py writeback` checks only `batch:pilot:briefs` (approved 2026-10-14) and a one-per-section guard. The 3 open facts (svc-repair-maintenance:service_process, d:emergency, svc-curved-stair-lifts:install_time) and the uncleared blockers do not gate this step; no refusal.

**Written back to brand-guide.md (from the approved pilot briefs SB - Stair Lifts, LB - Beaufort SC):**
- B3: two rows — /stair-lifts/ (service; category stair lift installer; area the Lowcountry) and /beaufort-sc/ (location; category stair lift installer; area Beaufort County), with their brief files.
- C1: /stair-lifts/ row — final URL (replaces /services/stair-lifts/), keyword "stair lifts", H1 variant "stair lift installation", H1 "Stair Lift Installation in the Lowcountry", no "The Best"; brief approved.
- C2: /beaufort-sc/ row — final URL (replaces /service-area/beaufort-sc/), keyword "stair lifts Beaufort SC", H1 "Stair Lift Installer in Beaufort", variants; brief approved.
- C3: 21 rows — 4 H2 + 4 H3 + 5 FAQ for /stair-lifts/; 5 H2 + 3 FAQ for /beaufort-sc/.
- `records.py render` run; Brand Guide copied to Drive (`drive.py upload`); `status.py writeback home-mobile-medical pilot` recorded.

**Not done:** the C1 row for /services/straight-stair-lifts/ still says "consolidated into /services/stair-lifts/" (should read /stair-lifts/). The edit was blocked by the permission classifier; left for Paul or the next write-back.

**Open / waiting (not blocking):** 3 open facts with the client; blocker handoffs issued, not returned.

## /build · 2026-10-14 · run 20261014-140654-build-4002

- Re-ran evidence grids for all 33 pages (evidence.py run --all): 0 block, 5 warn (all service pages), 28 pass.
- reviews.py extract: 8 review topics, none from 3+ reviewers, so no researcher check by meaning was needed; facts.json section R updated by the script.
- research.py todo for every batch (services, loc-hhi, loc-charleston, final, pilot): every gap already has a research-log entry from the earlier facts round today. No new public research run; researcher not spawned.
- evidence.py questions --all: 0 new questions. The three open client questions (service_process, d:emergency, install_time) were asked earlier today and are still waiting on the client via Paul.
- No facts recorded with run.py fact in this run (no new answers or sourced values).
- Flag F-007: the questions command overwrote the open facts-round REVIEW.md with an empty version; the sent version is in git HEAD. Restore was blocked by the permission system.
- Remaining [NEED]: emergency/after-hours (all location pages), repair service process (svc-repair-maintenance, required), install times for curved/porch/wheelchair lifts. Supporting gaps left out of pages: awards, associations; neighbourhoods for Folly Island, Laurel Bay, Levy; named places for Levy (researched, not found).

## /interview · 2026-10-14 · run 20261014-141534-interview-b760

## Handoff Log

**Step:** facts-answers, batch `all` (the 2026-10-14 facts round, 3 questions).
**Reply saved:** `clients/home-mobile-medical/interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REPLY.md` (as given).

**Answers and where they went**

| Key | Answer (short) | Brand Guide D | Settled |
|---|---|---|---|
| `fact:svc-repair-maintenance:service_process` | Steps as suggested (first call, visit, diagnosis, quote, parts, fix). No service-call or trip charge. Website wording: yes. | New row "Repair process: steps and charge" (Client Confirmed); trip-charge row changed from [NEED] to "None" (Client Confirmed) | Yes, by Client (via Paul) |
| `fact:d:emergency` | No standing after-hours service. True emergencies handled after hours; urgent non-emergency calls scheduled ASAP; after-hours availability depends on current demand. Advertise in general terms only. | "Emergency / after-hours reality" row changed from [NEED] to general-terms wording (Client Confirmed) | Yes, by Client (via Paul) |
| `fact:svc-curved-stair-lifts:install_time` | Installation itself is quick for curved, porch and wheelchair lifts; more than one install per day possible. **Partial.** | New row "Install time: curved, porch and wheelchair lifts" (Client Confirmed) | Yes, with open items left open |

**Still open (not answered):**
- Order-to-installed lead time for curved, porch and wheelchair lifts.
- Who handles the concrete pad and building permit for porch and wheelchair lifts (owner, customer, or depends).

Recorded as Unknown in Brand Guide D: row "Order-to-installed lead time; pad and permit for porch and wheelchair lifts".

**Gate re-run:** `python3 scripts/evidence.py run home-mobile-medical --run 20261014-141534-interview-b760 --all`
- Before: the five service pages were blocked on the three questions.
- After: no page is blocked. The five service pages (svc-repair-maintenance, svc-curved-stair-lifts, svc-porch-lifts, svc-wheelchair-lifts, svc-stair-lifts) now WARN with 3 supporting unverified gaps each; the brief must list them under "Evidence gaps".
- All location, hub, homepage and about pages PASS (some with 1–2 unverified or unknown supporting facts).

**Brand Guide changed:** Section D was edited, so `brand_guide_approved` is void until Paul re-approves. `/next` gives the approval line.

**Facts pack note:** `evidence.py run --batch all` is not a valid batch name, so the gate was re-run with `--all`.

**Next for Paul**
1. Re-approve the Brand Guide (sees the new D rows first).
2. Decide on the two open items: send a follow-up question for lead time and pad/permit, or accept the current wording (the pages say the install timeline is confirmed at the free in-home estimate).
3. Check the Brand Guide's D2 section: the homepage and service wording may still need the "no after-hours" and "same-day in most cases" lines re-checked when briefs are drafted.

## /build · 2026-10-14 · run 20261014-141838-build-9492

- Source of Paul's notes: drafts review "accept all, Ask 1 = A" (run 20261014-131553-build-b121); briefs and drafts approved 2026-10-14 13:28/13:29 as written, SEM none; brief mode → auto.
- Paul wrote no corrections. No spec element or check changed for this client; nothing flagged for /system-review.
- build/pilot-corrections.md written: "none" under Paul's corrections, plus 5 accepted pilot answers/defaults carried forward (safety line kept verbatim at grade 11.3 — C5/CM-047; location cost FAQ uses the quote angle — BB-316; Recent work dropped without a town review — LOC-29; title with GBP primary category — LOC-02; install time from settled facts only).
- Open for Paul (one line, default given): may other Beaufort County pages also name Beaufort Medical Equipment? Default: no, Beaufort page only.
- `status.py pilot-corrections` recorded. Later batches (services, loc-hhi, loc-charleston, final) may start.
- Settled decisions untouched.

## /build · 2026-10-14 · run 20261014-143231-build-f825

## Handoff Log

- **Paul's decision (chat):** no mentions of Beaufort Medical Equipment (BME), Jason's former company, anywhere on the site or in drafts, including the Beaufort page. Settled as `bme-mention`.
- **Draft changed:** `build/pilot/drafts/loc-beaufort-sc.md`. FAQ 3 "Is Home Mobile Medical the Same Company as Beaufort Medical Equipment?" removed. Logged as change #223.
- **Still mentions BME (internal only, not public copy):** Brand Guide D history row; `build/evidence/about.facts.json` and `about.grid.md`; `build/loc-hhi/packs/*`. Check before any brief or draft is written from them.
- **Open:** `build/pilot-corrections.md` still lists "whether other Beaufort County pages may also name the former company" as open. The settled answer is no, so that line is superseded by `bme-mention`.
- **Logging error:** a test `run.py change` with placeholder values (kind x, url x) was written to the changes log as entry #222 during this run. The log is append-only, so it cannot be removed here. It needs noting in the next system session.

## /build · 2026-10-14 · run 20261014-144522-build-adbe

Step: build:drafts · batch: pilot · session: Haiku

## What changed
- `build/pilot/drafts/loc-beaufort-sc.md`
  1. Permit FAQ section ("Do I Need a Permit for a Lift in Beaufort?") and its NEED line removed. Paul: no permit mentions; cannot verify in time.
  2. Sentence in "Serving Beaufort" pointing to the City of Beaufort Building Codes Department (local building rules) removed as a permit pointer. Paul to confirm.
  3. City-level Google map NEED line removed. Paul: VA handles GBP maps.

## Paul's answers recorded
- No permit mentions on any page.
- Former company (Beaufort Medical Equipment): on the About page only, not on location pages. The About-page wording is a separate later step.
- Defaults in the drafts review (SEO title with GBP category, FAQ topics, H1, FAQ 1 fallback) approved as drafted.

## Open after this run
- The Beaufort draft's FAQ 3 (former company) is not in the file; the review sheet listed it as kept. Nothing to remove here.
- Removal of the building-codes sentence needs Paul's confirmation.
- About-page mention: separate step.

## /build · 2026-10-14 · run 20261014-163404-build-b049

**What I did**
- Drafted svc-curved-stair-lifts (Route A) from the approved brief and its evidence pack, in this run's own context (CM-043). One page only.
- Recorded it: `status.py page-stage home-mobile-medical svc-curved-stair-lifts --stage draft --agent build-svc-curved-stair-lifts` → "draft recorded".
- Ran readability.py (page grade 7.0; the only paragraph over 10 is the verbatim safety line, exempt per pilot-corrections) and placeholders.py (no placeholders).

**What was decided, and why**
- Kept every Paul constraint from the brief review: no ramps (no not-offered product list at all); settled install-time wording word for word (delivery H2 and FAQ 3); manufacturer's warranty only, no guarantee; no Beaufort Medical Equipment; no service-call/trip-charge wording (not needed on this page); cost FAQ worded around the curved staircase only, no sentence shared with the /stair-lifts/ cost answer.
- One H3 under the types H2 (the pack names one type); no second H3 invented.
- The free estimate is not attributed to Jason personally (the pack does not say who does it); Jason is named only as supervising every installation.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Order-to-installed lead time for a curved lift (unknown, left out) | Client via Paul | Nothing — page stands without it |
| Sibling collision check against the porch, wheelchair and repair drafts | Build agent, draft review (one checker pass) | The services draft review sheet |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Draft | clients/home-mobile-medical/build/services/drafts/svc-curved-stair-lifts.md | Recorded (draft), awaiting the section's draft review |
| Brief | clients/home-mobile-medical/build/services/briefs/SB - Curved Stair Lifts - Home Mobile Medical.md | Approved |

**What I could not check**
- The sibling drafts (porch, wheelchair, repair) were not on disk; I checked against their briefs only.

**Anything the next agent would otherwise get wrong**
- The settled install sentence repeats in the delivery H2 and FAQ 3 by design (brief: word for word in both); FAQ 3's second sentence is curved-only. The safety line's grade-14 reading is accepted, not a finding.

## /build · 2026-10-14 · run 20261014-163624-build-5523

**What I did**
- Wrote the svc-porch-lifts draft from its approved brief (SB - Porch Lifts) and evidence pack: clients/home-mobile-medical/build/services/drafts/svc-porch-lifts.md.
- Recorded it: `status.py page-stage home-mobile-medical svc-porch-lifts --stage draft --agent build-svc-porch-lifts` → "draft recorded".
- Self-checks: readability page grade 5.9 (731 words); placeholders scan clean (no [NEED] or [LINK] needed); sweep found no ramp, Beaufort Medical, guarantee, Medicare, insurance, licence, certification, "same day", "3–4 hours", health or "technician" wording.

**What was decided, and why**
- Followed the brief exactly: H1 "Vertical Platform Lift Installation in the Lowcountry"; opening uses "home accessibility lifts" + "Beaufort County"; 4 FAQs; boundary sentence about wheelchair lifts only inside the raised-entrance H3; warranty only in the delivery H2.
- Settled install-time wording (svc-curved-stair-lifts:install_time) used word for word in the delivery H2 and the install FAQ; it begins "Stair lift installations…" because it is verbatim.
- FAQ first sentences shortened below 40 words where needed to keep every paragraph under grade 10 (C5 over the 40–60 target).
- Used "15+ years of Jason Workens' experience" once (Decision 013 wording).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Safety line paragraph reads grade 14.1 — exempt (pilot-corrections, Ask 1 = A) | — | nothing |
| H3 "Servicing After Installation" names no entity (COM-01) — heading set by brief review row 7 | checker pass | draft review |
| FAQ 1 and 2 first sentences under 40 words (reading grade traded against SVC FAQ length) | checker pass | draft review |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Draft | clients/home-mobile-medical/build/services/drafts/svc-porch-lifts.md | recorded, awaiting the section's draft review |

**What I could not check**
- Sibling drafts other than curved (wheelchair, repair) were not in my read list; heading/FAQ collisions with them go to the checker pass.

**Anything the next agent would otherwise get wrong**
- The repeated settled install-time sentences across curved and porch are required verbatim, not an E1 portability failure.

## /build · 2026-10-14 · run 20261014-163836-build-20c8

**What I did**
- Wrote the svc-wheelchair-lifts draft from its approved brief (SB - Wheelchair Lifts) and evidence pack: clients/home-mobile-medical/build/services/drafts/svc-wheelchair-lifts.md.
- Recorded it: `status.py page-stage home-mobile-medical svc-wheelchair-lifts --stage draft --run 20261014-163836-build-20c8 --agent build-svc-wheelchair-lifts` → "draft recorded".
- Self-checks (E1–E10 + service spec): readability page grade 5.9 over 685 words, only paragraph over 10 is the verbatim safety line (exempt, pilot corrections); placeholders scan clean; sweep found no ramp, Beaufort Medical Equipment, guarantee, licence, certification, technician, "15+ years", "same day" or "3–4 hours" wording; meta 150 characters; one H1, no city in any H tag, no prose links; 4 FAQs.

**What was decided, and why**
- Followed the brief: H1 "Wheelchair Lift Installation in the Lowcountry"; opening uses "home accessibility lifts" + "Charleston area"; buyer state = a household that already uses a wheelchair.
- Settled install-time wording word for word in the delivery H2 and FAQ 2; FAQ 2's second sentence is page-specific (where the lift will stand in the home).
- "No trip charge" sits in FAQ 1 (and the delivery H2 and CTA); warranty FAQ here (manufacturer's only); porch-vs-wheelchair comparison owned here (H3 + FAQ 3).
- FAQ 3 and 4 first sentences kept under 40 words to hold every paragraph under grade 10 (same trade-off as the porch page).
- The optional `[LINK → /porch-lifts/ …]` was not placed; no in-prose links.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Safety line paragraph grade 14.1 — exempt (pilot corrections, Ask 1 = A) | — | nothing |
| FAQ 3 and 4 first sentences under the 40–60 word target (reading grade traded) | checker pass | draft review |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Draft | clients/home-mobile-medical/build/services/drafts/svc-wheelchair-lifts.md | recorded, awaiting the section's draft review |

**What I could not check**
- The repair page draft (svc-repair-maintenance) was not on disk / not in my read list; collisions with it go to the checker pass.

**Anything the next agent would otherwise get wrong**
- The settled install-time sentences repeat across curved, porch and wheelchair by design (verbatim), not an E1 failure.

## /build · 2026-10-14 · run 20261014-164054-build-4d84

**What I did**
- Wrote the draft for svc-repair-maintenance (/stair-lift-repair/) from its approved brief and evidence pack, in its own run (CM-043): H1 "Stair Lift and Lift Servicing in the Lowcountry", opening, delivery H2 (the six settled repair steps in order), types H2 (4 H3s), FAQ H2 (5 questions from the brief), service-areas H2 with the link-wheel placeholder row, CTA.
- Recorded it: `status.py page-stage … --stage draft --agent build-svc-repair-maintenance` → "draft recorded".
- Self-check: readability.py page grade 4.8, no paragraph over 10 (E10 passes); placeholders.py: none.

**What was decided, and why**
- Followed Paul's settled decisions: steps first call → visit → diagnosis → quote → parts → fix; no service-call or trip charge; any brand, any stair lift or lift incl. porch and wheelchair lifts (FAQ 4); after-hours in general terms only (no promise, no response time); hours Mon–Fri 9–5; no repair warranty or guarantee; no Beaufort Medical Equipment; no prices.
- FAQ answers: to keep each paragraph at or under grade 10, the 40–60-word answer runs over two short sentences on FAQs 3–5; sentence one still answers alone (C7). The checker pass may list this against the "first sentence 40–60 words" wording.
- Safety statement left out (it speaks of installations; brief recommendation). No reviews used (pack has none about repair; brief).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Legacy 301s /hilton-head/stair-lift-repair/ and /bluffton-sc/wheelchair-lift-repair/ → /stair-lift-repair/ (Paul, settled 2026-10-14). Not in page copy and not in the draft's `replaces:` field (the site plan JSON lists none for this page); the publish handoff must pair them | Build coordinator / ship | Nothing until ship |
| Draft review (one checker pass for the services section) | Build coordinator | batch:services:drafts approval |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Draft | clients/home-mobile-medical/build/services/drafts/svc-repair-maintenance.md | Recorded (draft) |
| Brief | clients/home-mobile-medical/build/services/briefs/SB - Stair Lift Repair - Home Mobile Medical.md | Approved |

**What I could not check**
- Sibling cross-checks beyond reading the three install drafts (no shared H2, H3 or FAQ found); the full collision check is the section's checker pass.

**Anything the next agent would otherwise get wrong**
- The two legacy repair URLs must get their 301s in the publish handoff even though the draft has no `replaces:` line — add them from decisions-settled.md (`svc-repair-maintenance:legacy-repair-redirects`).

## /build · 2026-10-14 · run 20261014-164325-build-3b84

**What I did**
- Ran the one checker pass over the four services drafts side by side (curved, porch, wheelchair, repair): sibling collisions, Paul's constraints, usage check, Stage 4 semantics, SVC-15 FAQ lengths.
- Wrote findings to `clients/home-mobile-medical/build/services/drafts-findings.json`; `review.py sheet` built `build/services/drafts-review.csv` (+ .md, .json, drafts-fixes.json): 0 Ask, 11 Fix and list, 11 Fix (silent), 3 not raised (the auto usage rows, superseded).
- `status.py batch home-mobile-medical services --state drafts_written --review-sheet …drafts-review.csv`.
- Flagged F-012 (usage check pushes off-service/negative review excerpts).
- No draft changed; nothing applied or approved.

**What was decided, and why**
- Paul's constraints hold in all four drafts: no ramps; no Beaufort Medical Equipment; manufacturer's warranty only, no guarantee; settled install-time wording word for word (curved, porch, wheelchair); repair page covers any stair lift or lift, any brand; emergency wording general only.
- Exception: wheelchair uses "no trip charge" three times, not the settled "no service-call or trip charge" → Fix and list (settled phrase in FAQ 1 and closing only).
- Settled install-time block appears twice on each install page and is the second sentence of the delivery paragraph and of the FAQ on all three → keep it once, in the FAQ, word for word, unsplit (Paul's word-for-word constraint outranks brief row 9's "no shared second sentence").
- Usage: every pack excerpt is off-service (wheelchair/lift chair/rental) or a 2020 complaint → "leave as written" on curved, porch, wheelchair.
- Other Fix and list: shared "Maybe…" openings (porch, wheelchair), wheelchair first sentence mirrors curved, porch repeats curved's supervise sentence, wheelchair FAQ 3 names no real difference.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Apply the sheet (`review.py apply … drafts`), apply 11 Fix-and-list + 11 Fix items, re-record every page | Build (next run) | `batch:services:drafts` approval |
| Lead time and pad/permit (d-lead-time-and-pad-permit) still unknown; drafts leave them out | Client via Paul | nothing |
| F-012 usage check flag | Paul, /system-review | nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Review sheet | clients/home-mobile-medical/build/services/drafts-review.csv (.md) | written, 0 Ask |
| Silent fixes | clients/home-mobile-medical/build/services/drafts-fixes.json | to apply |
| Findings | clients/home-mobile-medical/build/services/drafts-findings.json | input |

**What I could not check**
- Reading grade per page (not computed); pilot-corrections.md and Brand Guide C1–C3 were not opened (briefs' variant tables used).

**Anything the next agent would otherwise get wrong**
- Do not split or shorten the settled install-time sentences to satisfy the 40–60-word FAQ first-sentence rule or brief row 9; the safety line and the brands line are approved wording too.

## /build · 2026-10-14 · run 20261014-205855-build-59c9

**What I did**
- Applied the 11 accepted rows of the services drafts review sheet ("accept all") to the drafts and recorded all four pages again (`status.py page-stage … --stage draft`, agent `build-apply-<page>`).
- Curved stair lifts: item 2 (settled install-time wording now only in the FAQ; the delivery H2 has a curved-specific line). Item 1 needed no edit.
- Porch lifts: items 4 (settled install-time wording only in the FAQ), 5 (scenario without "Maybe"), 6 (supervision sentence in porch's own words). Item 3 needed no edit.
- Wheelchair lifts: items 8 (settled wording only in the FAQ), 9 (new first sentence and scenario without "Maybe"), 10 ("no service-call or trip charge" in FAQ 1 and the closing only; the delivery H2's extra line removed), 11 (FAQ 3 rewritten as the sheet says, with no indoor claim). Item 7 needed no edit.
- Stair lift repair: the sheet has no rows for it. Its draft is unchanged and was recorded again.

**What was decided, and why**
- Every edit follows the sheet's recommended option. No new facts were added: each new line restates a pack fact (estimate first, Jason supervises, lift sourced new).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Drafts approval for the services section | Paul | ship |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Drafts | clients/home-mobile-medical/build/services/drafts/ | Applied, recorded |
| Review sheet | clients/home-mobile-medical/build/services/drafts-review.md | Answered: accept all |

**What I could not check**
- Nothing published. The link-wheel table rows are still placeholders, as intended.

**Anything the next agent would otherwise get wrong**
- The settled install-time wording now appears once per page, in the FAQ. Do not add it back to the delivery H2s.

## /build · 2026-10-14 · run 20261014-211328-build-a865

**What I did**
- Wrote the services section's one Brand Guide write-back (CM-061) into `brand-guide.md` from the four approved service briefs: B3 +4 rows, C1 4 rows updated, C3 +44 rows. C2 was not changed.
- Logged the change (change #305), then recorded the write-back with `status.py writeback home-mobile-medical services`.

**What was decided, and why**
- B3 uses the pilot's format. Category variants are the brief's opening variants. Area variants are listed as "the Lowcountry (H1); opening: …".
- C1: the three install rows now show the replacing URL with its 301, the keyword, the H1 service variant and the H1, with status "Brief approved 2026-10-14 (services)". The repair placeholder row became `/stair-lift-repair/`, with the two legacy repair URLs noted as 301s (settled: svc-repair-maintenance:legacy-repair-redirects). The `/services/` and `/services/straight-stair-lifts/` rows were left as they were.
- C2: no change. Service pages have no location rows, and no brief assigns a C2 value.
- C3: every H2, H3 and FAQ question the briefs assign, in the same "H2:/H3:/FAQ:" format as the pilot rows. The pilot entries were not touched. I checked for duplicate rows and found none.
- Left out: the curved brief's optional second H3 "Straight Stairs" ("only if the writer needs it"). It is not an assigned heading. If the approved draft uses it, add it to C3.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Curved page: add "H3: Straight Stairs" to C3 if the approved draft uses it | next Build run | nothing |
| Drive copy of the Brand Guide (`drive.py upload`) was not made in this run | coordinator / run.py finish | nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide (B3, C1, C3 updated) | clients/home-mobile-medical/brand-guide.md | written back |
| Services briefs | clients/home-mobile-medical/build/services/briefs/ | approved, unchanged |

**What I could not check**
- The drafts, which this run's read list did not include. C3 records the headings the briefs assign, not what the drafts actually use.

**Anything the next agent would otherwise get wrong**
- Different service pages already share some variants, which is allowed (CM-024, horizontal): "home accessibility lifts" (porch, wheelchair), "Charleston area" in the openings (curved, wheelchair) and "the Lowcountry" in every service H1. The location section should pick its openings from the rest of the B2/A3 pool where it can.
- The pilot's C3 row "FAQ: Is Home Mobile Medical the same company as Beaufort Medical Equipment?" (/beaufort-sc/) conflicts with the settled decision bme-mention (Beaufort Medical Equipment is never mentioned). I was told not to touch the pilot rows, so it is left for Paul.

