# Apex Roofing of the Lowcountry - Document Checklist

Generated 2026-10-08T11:13 from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · `[!]` failed · `[ ]` not yet.

## Evidence and data steps (methodology/audit-steps.md)

| | Step | Outcome | Reason / output |
|---|---|---|---|
| [x] | S01 Intake facts: website, GBP link, storefront/SAB, exact GBP Website-fie | done | Intake facts complete from the client record (GBP link, SAB, GBP Website field, no GSC/GA4, WordPress/Kadence); nothing missing |
| [x] | S02 Public discovery: live site, GBP, social, review profiles, Secretary o | done | Live site (sitemap pages), public GBP view, BBB, HomeAdvisor list page, Facebook, RDAP, OpenCorporates copy of SC SOS read. Not read: SC SOS primary and SC LLR (both CAPTCHA), GBP secondary categories/service areas/open date (limited view), HomeAdvisor profile (403), Yelp/Angi/Nextdoor/Apple/Bing |
| [x] | S03 Entity research: category entity (Wikipedia), area entity (Russian Dol | done | Category entity Roofing contractor (Wikipedia Roofer, Q552378); area entity Hilton Head Island-Bluffton-Port Royal SC MSA (Q17020871) by Russian Doll from Bluffton, contains all 12 location-page cities; variants, reserved homepage variant and Wikidata URIs proposed. Open: Georgia service-area conflict (C1) |
| [x] | S04 Proof sheet built (Markdown + client Google Doc) | done | Proof sheet built from the approved Discovery Record and Brand Guide A; .md and CLIENT COPY Google Doc in Drive Deliverables; return by 2026-10-20 |
| [x] | S05 Site crawl | done | DataforSEO basic crawl, 72 URLs, $0.15. 12 of 14 files in Drive Evidence; h2_all and all_inlinks local only (connector paste limits) |
| [x] | S06 Reviews pull: Google rating, count, recent review text (no reviewer na | done | 67 reviews (rating 5.0; 66 five-star, 1 two-star); themes, symptom words and review-only claims added to customer-language.md; nothing to Brand Guide D (CM-027) |
| [x] | S07 Rankings + cannibalization: every ranked keyword per URL (top 100), co | done | DataforSEO Labs ranked keywords (US): 41 keywords on 7 URLs; 2 'cannibalization' clusters are the homepage under http://www and https (host duplicate); 3 of 104 'best' variants with volume; $0.107 |
| [x] | S08 Backlinks pull: referring domains per URL | done | DataforSEO backlinks one_per_domain: 711 referring domains (694 to the homepage), 6 target URLs incl. 2 old URLs; $0.05 |
| [-] | S09 Citations | skipped | Paul 2026-10-07: skip citations for this audit (no BrightLocal citation tracker export) |
| [x] | S10 Local grid | done | Local Dominator scans 2026-10-07: roof repair bluffton (local pack 6.99, maps 20+), roofing contractor near me (local pack 19.29, maps 20+); 176 pins, 3 mi. Results only; report advice not used |
| [-] | S11 Search Console / GA4 | skipped | No Search Console or GA4 access (intake 2026-10-05); Paul 2026-10-06: not needed, we use our own SEO data |
| [x] | S19 People Also Ask: core services × primary city + top 3 cities, capped ( | done | PAA: 96 queries (8 services x 12 towns), 140 distinct questions routed - 76 service FAQ, 2 location FAQ (Lady's Island, Fripp Island), 28 blog topic, 34 drop; first 50 routes carried over unchanged |
| [x] | S20 SEOPress site-wide settings (title templates, sitemap, noindexed post  | done | Readable during /wp-check 2026-10-05 (Administrator login); saved as evidence |
| [x] | S21 Query fan-out (CM-045): core services × primary city + top 3 cities, c | done | 10 seeds, 379 queries routed: 269 service H2/FAQ (about 75 head terms), 35 location FAQ, 55 blog topic, 20 drop; 2 PAA repeats route with PAA; no volumes (CM-012) |
| [x] | S12 Ingest + cross-checks | done | Ingest + cross-checks: 13/13 crawl exports recognised, manifest SRC-001-027; crosscheck: rendering LIMITATION (standing config), coverage CONFIRMED; nothing CONTRADICTED |
| [x] | S13 Entity analysis: site vs Brand Guide (triple, NAP, brand search, suppo | done | Entity: site vs Brand Guide (triple, NAP, brand forms, GBP field, schema readiness) - findings F-001 to F-008 |
| [x] | S14 Architecture: every page typed, keep/merge/redirect per CM-019 | done | URL Decision Map: 83 rows (72 crawled + 2 sitemap-only + 1 backlink-only + 2 host variants + 6 noindexed archives); no CM-019 candidate (conditions 3-4 unmet everywhere); 1 Needs Evidence slug change, 1 redirect fix |
| [x] | S15 Page conformance: every page scored against its spec (check IDs HP/SVC | done | Conformance scorecards for 46 spec'd pages (homepage, 8 service, 12 location, about, 24 posts); all specs DRAFT (advisory); utility pages have no spec |
| [x] | S16 Technical findings (Low batched into one handoff) | done | Technical findings F-009, F-027, F-029, F-030, F-031, F-033 (Low, one batch) - redirect to 404, internal links to redirects, sitemap redirects, separators, meta descriptions, alt text |
| [x] | S17 Fresh-context review of Finding Register + URL Decision Map | done | Fresh-context review: 21 confirmed, 9 revised, 3 withdrawn; High 3 / Medium 17 / Low 10; map 3 rows corrected |
| [x] | S18 Render deliverables | done | Rendered Finding Register, URL Decision Map, Recommendations, Evidence Manifest (REVIEW) from the latest revision of each finding (30 active: High 3, Medium 17, Low 10; 3 withdrawn listed). Recommendations and Evidence Manifest uploaded to Drive Deliverables; Finding Register (87 KB) and URL Decision Map (40 KB) kept local - too large to paste reliably |

## Conditions

- [x] Client set up (/new-client finished)
- [x] The client returned the proof sheet (the returned sheet is recorded)
- [x] Every registered audit step has an outcome (Done / Skipped / Failed)
- [ ] Every page in the site plan is built, verified and written back — no site plan yet
- [x] WordPress connected (/wp-check passed in the last 30 days)

## Decisions (Paul)

- [x] Entity foundation approved (category entity, area entity, variant list, reserved homepage variant)
- [x] Client proof sheet approved by Paul, ready for him to send
- [x] Audit deliverables approved (Finding Register, URL Decision Map, Recommendations, Evidence Manifest)
- [x] Brand Guide approved: the client's returned proof sheet reconciled (verified facts separated from unsupported claims)
- [x] Discovery and audit signed off — Build may start
- [ ] Technical blocker checklist cleared and tracking stable
- [ ] Link wheel built and verified — schema may start
- [ ] Schema built and QA cleared — release
- [ ] Blog Decision Map approved — redirects and blog briefs may start
- [ ] WordPress pilot passed for this site — the system may write titles, keyword, social, robots, canonical and schema directly
