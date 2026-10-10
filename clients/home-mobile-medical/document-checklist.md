# Home Mobile Medical - Document Checklist

Generated 2026-10-09T22:27 from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · `[!]` failed · `[ ]` not yet.

## Evidence and data steps (methodology/audit-steps.md)

| | Step | Outcome | Reason / output |
|---|---|---|---|
| [x] | S01 Intake facts: website, GBP link, storefront/SAB, exact GBP Website-fie | done | Intake 2026-09-28 (Document Checklist) |
| [x] | S02 Public discovery: live site, GBP, social, review profiles, Secretary o | done | Discovery Record 2026-09-28 |
| [x] | S03 Entity research: category entity (Wikipedia), area entity (Russian Dol | done | Entity foundation approved 2026-10-02 |
| [x] | S04 Proof sheet built (Markdown + client Google Doc) | done | Client Gap Sheet + claims proof list 2026-10-07 |
| [x] | S05 Site crawl (max pages = sitemap size × 1.5, min 20, max 1000; 1000 whe | done | Screaming Frog crawl 2026-09-18 (118 HTML URLs; internal, external, titles, meta, H1, H2, links, javascript) in v3 Evidence; no new crawl (Paul) |
| [ ] | S05b Page text capture: the body text of every crawled HTML page (the basic | — |  |
| [x] | S06 Reviews pull: Google rating, count, recent review text (no reviewer na | done | DataforSEO Google reviews, 19 reviews, rating 2.9; listing matched GBP address; reviews 2017-2023 describe the former retail/rental store, none mention lift services; $0.0150 |
| [x] | S07 Rankings + cannibalization: every ranked keyword per URL (top 100), co | done | DataforSEO Labs ranked keywords (US, whole domain): 115 rows, 110 keywords, 15 ranking URLs, 0 cannibalization clusters; 25 'best' variants (SC) all without measurable volume; $0.1158 |
| [x] | S08 Backlinks pull: referring domains per URL | done | DataforSEO Backlinks (whole domain, live): 722 backlinks / 709 referring domains; 5 target URLs, homepage holds 708 RDs; $0.0740 |
| [x] | S09 Citations | done | BrightLocal citation tracker 2026-09-28 in v3 Evidence |
| [x] | S10 Local grid | done | Six Local Dominator grid reports 2026-09-18 in v3 Evidence (12x12, 2-mile spacing; device unknown) |
| [-] | S11 Search Console / GA4 | skipped | GSC and GA4 unavailable (client); DataforSEO replaces them for CM-019 (Paul 2026-10-06) |
| [x] | S19 People Also Ask: core services × primary city + top 3 cities, capped ( | done | 20 PAA queries (5 services x Beaufort, Charleston, Hilton Head Island, Bluffton) -> 35 questions, all routed; 24 SERP calls incl. 4 billed retries after DataforSEO 40101 errors; $0.0480 |
| [-] | S20 SEOPress site-wide settings (title templates, sitemap, noindexed post  | skipped | SEOPress site-wide settings not readable as Editor (/wp-check 20261007-172720-wp-check-bb94); one-time VA check issued to Jonie as handoff H-2026-10-07-02-seopress_settings. Re-record S20 done when her returned worksheet is saved. No Administrator access attempted (wordpress-site-setup.md section 5). |
| [x] | S21 Query fan-out (CM-045): core services × primary city + top 3 cities, c | done | Query fan-out, 10 seeds (5 services x Beaufort, Charleston; cap 10 per Paul) -> 354 queries, all routed; Hilton Head Island and Bluffton seeds not run; not demand (CM-045, CM-012); $0.0122 |
| [x] | S12 Ingest + cross-checks | done | Ingest (8/8 SF exports recognised) + crosscheck (host CONTRADICTED = third-party domains only; rendering LIMITATION; coverage OK) + manual addendum (H1 corroborated; LNKD canonical issue contradicted; orphan candidates reconciled; CM-019 C3 method); manifest SRC-001..027 incl. BL, CMS, sitemap, LNKD, 6 grid PDFs, old map, DFS data |
| [x] | S13 Entity analysis: site vs Brand Guide (triple, NAP, brand search, suppo | done | Entity analysis: 12 findings (F-001..F-012): category entity in homepage title, Georgia on SC site, discontinued services/DME, second NAP, safety claims, unsupported claims, Folly naming, Yemassee heading, GBP reviews 2.9/19 old store, citation NAP/coverage, backlink baseline |
| [x] | S14 Architecture: every page typed, keep/merge/redirect per CM-019 | done | URL Decision Map 159 rows (all 118 crawled + 40 uncrawled + 1 Create), CM-019 C1-C4 per destructive candidate: 36 pass C1-C3 awaiting C4, 10 fail (Needs Evidence), 18 Georgia Hold-microsite; findings F-013..F-021 |
| [x] | S15 Page conformance: every page scored against its spec (check IDs HP/SVC | done | Conformance scorecard vs methodology/specs (all DRAFT - advisory): homepage, 5 service, 24 SC location (+9 GA held), 3 hubs (Low cap), about, 21 posts; findings F-022..F-032; checks needing body/full headings marked NE |
| [x] | S16 Technical findings (Low batched into one handoff) | done | Technical findings F-033..F-040 (all Low) + other Low items batched into one list (13 items) for Build handoff; schema readiness N/A (no structured-data export, S20 pending) |
| [x] | S17 Fresh-context review of Finding Register + URL Decision Map | done | clients/home-mobile-medical/audit/2026-10-07/ |
| [x] | S18 Render deliverables | done | Rendered from the registers after S17 review and the five reviewer fixes: Finding Register, URL Decision Map, Recommendations, Evidence Manifest (REVIEW) in audit/2026-10-07/deliverables/ |

## Conditions

- [x] Client set up (/new-client finished)
- [x] The client's facts are in — the returned proof sheet is recorded, or Paul approved the client's direct answers
- [x] Every registered audit step has an outcome (Done / Skipped / Failed)
- [ ] Every page in the site plan is a WordPress draft — ready for the one living publish handoff (CM-055) — batches not yet in WordPress as drafts: pilot, services, loc-hhi, loc-charleston
- [ ] Every page in the site plan is built, verified and written back — batches not yet built and written back: pilot, services, loc-hhi, loc-charleston, final
- [x] WordPress connected (/wp-check passed in the last 30 days)
- [x] Discovery and audit signed off — Build may start (met when the Decision Sheet, entity, client facts, audit and Brand Guide are approved and the client's facts are recorded)
- [ ] Technical blockers cleared — every blocker handoff returned done and /verify passed it — blockers not cleared: H-2026-10-09-03-redirect-01 is issued; H-2026-10-09-03-redirect-02 is issued; H-2026-10-09-03-redirect-03 is issued; H-2026-10-09-04-broken_link-01 is issued; H-2026-10-09-04-broken_link-02 is issued (+9 more)
- [x] Page specs approved by Paul once, globally (methodology/specs) and unchanged since

## Decisions (Paul)

- [x] Discovery approved — the Decision Sheet (every identity and format decision) and the entity foundation (category, area, variants, reserved homepage variant)
- [x] Client facts approved — the proof sheet ready for Paul to send, or the client's answers taken directly
- [x] Audit deliverables approved (Finding Register, URL Decision Map, Recommendations, Evidence Manifest)
- [x] Brand Guide approved: the client's returned proof sheet reconciled (verified facts separated from unsupported claims)
- [ ] Link wheel built and verified — schema may start
- [ ] Schema built and QA cleared — release
- [ ] Blog Decision Map approved — redirects and blog briefs may start
- [ ] WordPress pilot passed for this site — the system may write titles, keyword, social, robots, canonical and schema directly
