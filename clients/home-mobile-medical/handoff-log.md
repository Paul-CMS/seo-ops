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

