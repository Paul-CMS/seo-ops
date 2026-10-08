# Home Mobile Medical - Document Checklist

Generated 2026-10-07T19:58 from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · `[!]` failed · `[ ]` not yet.

## Evidence and data steps (methodology/audit-steps.md)

| | Step | Outcome | Reason / output |
|---|---|---|---|
| [x] | S01 Intake facts: website, GBP link, storefront/SAB, exact GBP Website-fie | done | Intake 2026-09-28 (Document Checklist) |
| [x] | S02 Public discovery: live site, GBP, social, review profiles, Secretary o | done | Discovery Record 2026-09-28 |
| [x] | S03 Entity research: category entity (Wikipedia), area entity (Russian Dol | done | Entity foundation approved 2026-10-02 |
| [x] | S04 Proof sheet built (Markdown + client Google Doc) | done | Client Gap Sheet + claims proof list 2026-10-07 |
| [x] | S05 Site crawl | done | Screaming Frog crawl 2026-09-18 (118 HTML URLs; internal, external, titles, meta, H1, H2, links, javascript) in v3 Evidence; no new crawl (Paul) |
| [x] | S06 Reviews pull: Google rating, count, recent review text (no reviewer na | done | DataforSEO Google reviews, 19 reviews, rating 2.9; listing matched GBP address; reviews 2017-2023 describe the former retail/rental store, none mention lift services; $0.0150 |
| [x] | S07 Rankings + cannibalization: every ranked keyword per URL (top 100), co | done | DataforSEO Labs ranked keywords (US, whole domain): 115 rows, 110 keywords, 15 ranking URLs, 0 cannibalization clusters; 25 'best' variants (SC) all without measurable volume; $0.1158 |
| [x] | S08 Backlinks pull: referring domains per URL | done | DataforSEO Backlinks (whole domain, live): 722 backlinks / 709 referring domains; 5 target URLs, homepage holds 708 RDs; $0.0740 |
| [x] | S09 Citations | done | BrightLocal citation tracker 2026-09-28 in v3 Evidence |
| [x] | S10 Local grid | done | Six Local Dominator grid reports 2026-09-18 in v3 Evidence (12x12, 2-mile spacing; device unknown) |
| [-] | S11 Search Console / GA4 | skipped | GSC and GA4 unavailable (client); DataforSEO replaces them for CM-019 (Paul 2026-10-06) |
| [x] | S19 People Also Ask: core services × primary city + top 3 cities, capped ( | done | 20 PAA queries (5 services x Beaufort, Charleston, Hilton Head Island, Bluffton) -> 35 questions, all routed; 24 SERP calls incl. 4 billed retries after DataforSEO 40101 errors; $0.0480 |
| [-] | S20 SEOPress site-wide settings (title templates, sitemap, noindexed post  | skipped | SEOPress site-wide settings not readable as Editor (/wp-check 20261007-172720-wp-check-bb94); one-time VA check issued to Jonie as handoff H-2026-10-07-02-seopress_settings. Re-record S20 done when her returned worksheet is saved. No Administrator access attempted (wordpress-site-setup.md section 5). |
| [x] | S21 Query fan-out (CM-045): core services × primary city + top 3 cities, c | done | Query fan-out, 10 seeds (5 services x Beaufort, Charleston; cap 10 per Paul) -> 354 queries, all routed; Hilton Head Island and Bluffton seeds not run; not demand (CM-045, CM-012); $0.0122 |
| [ ] | S12 Ingest + cross-checks | — |  |
| [ ] | S13 Entity analysis: site vs Brand Guide (triple, NAP, brand search, suppo | — |  |
| [ ] | S14 Architecture: every page typed, keep/merge/redirect per CM-019 | — |  |
| [ ] | S15 Page conformance: every page scored against its spec (check IDs HP/SVC | — |  |
| [ ] | S16 Technical findings (Low batched into one handoff) | — |  |
| [ ] | S17 Fresh-context review of Finding Register + URL Decision Map | — |  |
| [ ] | S18 Render deliverables | — |  |

## Conditions

- [x] Client set up (/new-client finished)
- [x] The client returned the proof sheet (the returned sheet is recorded)
- [ ] Every registered audit step has an outcome (Done / Skipped / Failed) — audit steps with no outcome yet: S12, S13, S14, S15, S16, S17, S18
- [ ] Every page in the site plan is built, verified and written back — batches not yet built and written back: svc1, loc1, loc2, loc3, loc4, loc5, loc6, loc7, final1, final2
- [x] WordPress connected (/wp-check passed in the last 30 days)

## Decisions (Paul)

- [x] Entity foundation approved (category entity, area entity, variant list, reserved homepage variant)
- [x] Client proof sheet approved by Paul, ready for him to send
- [ ] Audit deliverables approved (Finding Register, URL Decision Map, Recommendations, Evidence Manifest)
- [x] Brand Guide approved: the client's returned proof sheet reconciled (verified facts separated from unsupported claims)
- [ ] Discovery and audit signed off — Build may start
- [ ] Technical blocker checklist cleared and tracking stable
- [ ] Link wheel built and verified — schema may start
- [ ] Schema built and QA cleared — release
- [ ] Blog Decision Map approved — redirects and blog briefs may start
- [ ] WordPress pilot passed for this site — the system may write titles, keyword, social, robots, canonical and schema directly
