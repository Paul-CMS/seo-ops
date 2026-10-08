# Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW

**Status:** REVIEW — awaiting Paul (`audit_approved`). Rendered from the registers in `clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/` (latest revision of each finding); never edited by hand.

## Audit step outcomes (`steps.py manifest`)

| Step | Outcome | Reason | Outputs | Date |
|---|---|---|---|---|
| S01 Intake facts: website, GBP link, storefront/SAB, exact GBP W | Done | Intake facts complete from the client record (GBP link, SAB, GBP Website field, no GSC/GA4, WordPress/Kadence); nothing missing | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | 2026-10-05 |
| S02 Public discovery: live site, GBP, social, review profiles, S | Done | Live site (sitemap pages), public GBP view, BBB, HomeAdvisor list page, Facebook, RDAP, OpenCorporates copy of SC SOS read. Not read: SC SOS primary and SC LLR (both CAPTCHA), GBP secondary categories/service areas/open date (limited view), HomeAdvisor profile (403), Yelp/Angi/Nextdoor/Apple/Bing | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05.md | 2026-10-05 |
| S03 Entity research: category entity (Wikipedia), area entity (R | Done | Category entity Roofing contractor (Wikipedia Roofer, Q552378); area entity Hilton Head Island-Bluffton-Port Royal SC MSA (Q17020871) by Russian Doll from Bluffton, contains all 12 location-page cities; variants, reserved homepage variant and Wikidata URIs proposed. Open: Georgia service-area conflict (C1) | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | 2026-10-05 |
| S04 Proof sheet built (Markdown + client Google Doc) | Done | Proof sheet built from the approved Discovery Record and Brand Guide A; .md and CLIENT COPY Google Doc in Drive Deliverables; return by 2026-10-20 | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md | 2026-10-06 |
| S05 Site crawl | Done | DataforSEO basic crawl, 72 URLs, $0.15. 12 of 14 files in Drive Evidence; h2_all and all_inlinks local only (connector paste limits) | clients/apex-roofing-of-the-lowcountry/inputs/crawl/ | 2026-10-07 |
| S06 Reviews pull: Google rating, count, recent review text (no r | Done | 67 reviews (rating 5.0; 66 five-star, 1 two-star); themes, symptom words and review-only claims added to customer-language.md; nothing to Brand Guide D (CM-027) | clients/apex-roofing-of-the-lowcountry/data/reviews/customer-language.md | 2026-10-07 |
| S07 Rankings + cannibalization: every ranked keyword per URL (to | Done | DataforSEO Labs ranked keywords (US): 41 keywords on 7 URLs; 2 'cannibalization' clusters are the homepage under http://www and https (host duplicate); 3 of 104 'best' variants with volume; $0.107 | clients/apex-roofing-of-the-lowcountry/data/rankings/ | 2026-10-07 |
| S08 Backlinks pull: referring domains per URL | Done | DataforSEO backlinks one_per_domain: 711 referring domains (694 to the homepage), 6 target URLs incl. 2 old URLs; $0.05 | clients/apex-roofing-of-the-lowcountry/data/backlinks/referring-domains-per-url.csv | 2026-10-07 |
| S09 Citations | Skipped | Paul 2026-10-07: skip citations for this audit (no BrightLocal citation tracker export) |  | 2026-10-07 |
| S10 Local grid | Done | Local Dominator scans 2026-10-07: roof repair bluffton (local pack 6.99, maps 20+), roofing contractor near me (local pack 19.29, maps 20+); 176 pins, 3 mi. Results only; report advice not used | clients/apex-roofing-of-the-lowcountry/data/local-grid/local-grid-summary.md | 2026-10-07 |
| S11 Search Console / GA4 | Skipped | No Search Console or GA4 access (intake 2026-10-05); Paul 2026-10-06: not needed, we use our own SEO data |  | 2026-10-07 |
| S19 People Also Ask: core services × primary city + top 3 cities | Done | PAA: 96 queries (8 services x 12 towns), 140 distinct questions routed - 76 service FAQ, 2 location FAQ (Lady's Island, Fripp Island), 28 blog topic, 34 drop; first 50 routes carried over unchanged | clients/apex-roofing-of-the-lowcountry/data/paa/paa-routing.md | 2026-10-07 |
| S20 SEOPress site-wide settings (title templates, sitemap, noind | Done | Readable during /wp-check 2026-10-05 (Administrator login); saved as evidence | clients/apex-roofing-of-the-lowcountry/inputs/seopress-settings-2026-10-05.json | 2026-10-07 |
| S21 Query fan-out (CM-045): core services × primary city + top 3 | Done | 10 seeds, 379 queries routed: 269 service H2/FAQ (about 75 head terms), 35 location FAQ, 55 blog topic, 20 drop; 2 PAA repeats route with PAA; no volumes (CM-012) | clients/apex-roofing-of-the-lowcountry/data/fanout/fanout-routing.md | 2026-10-07 |
| S12 Ingest + cross-checks | Done | Ingest + cross-checks: 13/13 crawl exports recognised, manifest SRC-001-027; crosscheck: rendering LIMITATION (standing config), coverage CONFIRMED; nothing CONTRADICTED | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/00-crosschecks.md | 2026-10-07 |
| S13 Entity analysis: site vs Brand Guide (triple, NAP, brand sea | Done | Entity: site vs Brand Guide (triple, NAP, brand forms, GBP field, schema readiness) - findings F-001 to F-008 | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/findings.csv | 2026-10-07 |
| S14 Architecture: every page typed, keep/merge/redirect per CM-0 | Done | URL Decision Map: 83 rows (72 crawled + 2 sitemap-only + 1 backlink-only + 2 host variants + 6 noindexed archives); no CM-019 candidate (conditions 3-4 unmet everywhere); 1 Needs Evidence slug change, 1 redirect fix | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/url-decision-map.csv | 2026-10-07 |
| S15 Page conformance: every page scored against its spec (check  | Done | Conformance scorecards for 46 spec'd pages (homepage, 8 service, 12 location, about, 24 posts); all specs DRAFT (advisory); utility pages have no spec | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/inventories/conformance-scorecard-service.csv | 2026-10-07 |
| S16 Technical findings (Low batched into one handoff) | Done | Technical findings F-009, F-027, F-029, F-030, F-031, F-033 (Low, one batch) - redirect to 404, internal links to redirects, sitemap redirects, separators, meta descriptions, alt text | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/findings.csv | 2026-10-07 |
| S17 Fresh-context review of Finding Register + URL Decision Map | Done | Fresh-context review: 21 confirmed, 9 revised, 3 withdrawn; High 3 / Medium 17 / Low 10; map 3 rows corrected | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/review-s17.csv | 2026-10-07 |
| S18 Render deliverables | Done | Rendered Finding Register, URL Decision Map, Recommendations, Evidence Manifest (REVIEW) from the latest revision of each finding (30 active: High 3, Medium 17, Low 10; 3 withdrawn listed). Recommendations and Evidence Manifest uploaded to Drive Deliverables; Finding Register (87 KB) and URL Decision Map (40 KB) kept local - too large to paste reliably | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Recommendations - REVIEW.md | 2026-10-07 |

## Crawl configuration (S05 — Agency Profile standing config)

- Tool: DataforSEO OnPage API, task `10072030-1266-0216-0000-dd125d58970b`
- Mode: basic (JavaScript off; missing JavaScript-rendered data is never a finding)
- Max pages: 1000 · crawled: 72 · stop reason: empty_queue
- Crawl delay: 2000 ms between hits · user agent: DataforSEO default
- Posted: 2026-10-07T15:30:34-05:00 · cost: $0.15
- Converted to Screaming Frog-shaped tables (internal_all, links_all, page_titles_all, meta_description_all, h1_all, h2_all, all_inlinks, external_all). Columns DataforSEO does not provide (Link Score, external status codes) are left blank — not findings.
- Unlike the free Screaming Frog licence: no 500-URL cap, full H2 lists available.

## Sources

| ID | File | Recognised as | Rows | Tool settings | Date window | Geography / device | Scope limits |
|---|---|---|---|---|---|---|---|
| SRC-001 | Apex Roofing of the Lowcountry - DFS - all_inlinks - 2026-10-07.csv | screamingfrog.all_inlinks | 2225 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-002 | Apex Roofing of the Lowcountry - DFS - duplicate_content - 2026-10-07.csv | dataforseo.duplicate_content | 0 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-003 | Apex Roofing of the Lowcountry - DFS - duplicate_descriptions - 2026-10-07.csv | dataforseo.duplicate_tags | 0 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-004 | Apex Roofing of the Lowcountry - DFS - duplicate_titles - 2026-10-07.csv | dataforseo.duplicate_tags | 0 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-005 | Apex Roofing of the Lowcountry - DFS - external_all - 2026-10-07.csv | screamingfrog.external_all | 10 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-006 | Apex Roofing of the Lowcountry - DFS - h1_all - 2026-10-07.csv | screamingfrog.h1_all | 72 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-007 | Apex Roofing of the Lowcountry - DFS - h2_all - 2026-10-07.csv | screamingfrog.h2_all | 72 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-008 | Apex Roofing of the Lowcountry - DFS - internal_all - 2026-10-07.csv | screamingfrog.internal_all | 72 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-009 | Apex Roofing of the Lowcountry - DFS - links_all - 2026-10-07.csv | screamingfrog.links_all | 72 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-010 | Apex Roofing of the Lowcountry - DFS - meta_description_all - 2026-10-07.csv | screamingfrog.meta_description_all | 72 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-011 | Apex Roofing of the Lowcountry - DFS - non_indexable - 2026-10-07.csv | dataforseo.non_indexable | 6 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-012 | Apex Roofing of the Lowcountry - DFS - page_titles_all - 2026-10-07.csv | screamingfrog.page_titles_all | 72 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-013 | Apex Roofing of the Lowcountry - DFS - redirect_chains - 2026-10-07.csv | dataforseo.redirect_chains | 0 | as crawl config above | 2026-10-07 | crawler | complete, no rendering |
| SRC-014 | data/rankings/ (ranked-keywords.csv, url-rankings.csv, cannibalization.csv, best-variants.csv, rankings-summary.md) | S07 rankings | n/a | DataforSEO Labs ranked keywords + Google Ads volume | 2026-10-07 (Labs snapshot) | United States, country-level | top 100; 7 URLs rank |
| SRC-015 | data/backlinks/referring-domains-per-url.csv | S08 backlinks | n/a | DataforSEO Backlinks referring domains per URL | 2026-10-07 | n/a | 711 domains; per-URL |
| SRC-016 | data/reviews/ (reviews.csv, customer-language.md) | S06 reviews | n/a | DataforSEO Business Data Google reviews | pulled 2026-10-07 | GBP | 67 reviews, 5.0 (66×5, 1×2) |
| SRC-017 | data/local-grid/local-grid-summary.md (+ 4 MANUAL Local Dominator PDFs in inputs/local-grid/) | S10 local grid | n/a | Local Dominator 15×15, 3-mile spacing, 176 pins | 2026-10-07 16:19–16:21 | grid centre not stated ('Beaufort' label) — unverified | 2 keywords × 2 views; ranks only, report advice not used |
| SRC-018 | data/paa/paa-routing.md | S19 People Also Ask | n/a | DataforSEO SERP PAA | 2026-10-07 | 12 towns | 140 questions routed |
| SRC-019 | data/fanout/fanout-routing.md | S21 query fan-out (not demand, CM-045) | n/a | DataforSEO AI Optimization LLM responses | 2026-10-07 | 10 seeds | 379 queries; no volume |
| SRC-020 | inputs/seopress-settings-2026-10-05.json | S20 SEOPress site-wide settings | n/a | /wp-check read as Editor | 2026-10-05 | n/a | read-only |
| SRC-021 | discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md | returned proof sheet (client's words) | n/a | client answers via Paul | 2026-10-07 | n/a | as given |
| SRC-022 | discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | Paul's answers incl. 2026-10-07 addendum | n/a | Paul | 2026-10-06/07 | n/a | — |
| SRC-023 | inputs/live-pages/Apex Roofing of the Lowcountry - MANUAL - live-page-<page> - 2026-10-07.txt (23 files) | live page text captures (served HTML, no JS) — confirmation reads | n/a | curl + HTML-to-text, Mozilla UA, no JS | 2026-10-07 | n/a | homepage, about, contact, 8 service, 12 location pages |
| SRC-024 | inputs/live-pages/ … MANUAL - sitemap-urls / redirect-checks - 2026-10-07.txt | sitemap URL list + live redirect checks (curl) | n/a | curl -L, Mozilla UA | 2026-10-07 | n/a | sitemaps.xml children + 10 URLs |
| SRC-025 | inputs/live-pages/ … MANUAL - blog-post-titles-authors - 2026-10-07.json | blog post titles + author slugs (served HTML) | n/a | curl, regex on served HTML | 2026-10-07 | n/a | 24 posts |
| SRC-026 | brand-guide.md (Sections A, B1, B2; entity_approved 2026-10-05) | Brand Guide | n/a | — | 2026-10-05 | n/a | A/B approved; C–I not reconciled |
| SRC-027 | discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | Discovery Record (W/C observations) | n/a | — | 2026-10-05 | n/a | — |

Paths are relative to `clients/apex-roofing-of-the-lowcountry/`. `inputs/` is git-ignored (raw evidence). MANUAL live-page captures (SRC-023–025) are free reads of the public pages (served HTML, no JavaScript), made to confirm crawl findings (DEC-LOCAL-006).

## Cross-checks (S12)

- Rendering: LIMITATION — standing configuration (no JavaScript rendering); anything JS-loaded is not asserted.
- Crawl coverage: CONFIRMED — 72 URLs, stop reason empty_queue (not truncated).
- Nothing CONTRADICTED. Host variants (http, www) 301 to https://apexroofingtlc.com/ in one hop (SRC-024). Sitemap vs crawl reconciled by hand (F-031).

## Not available

- S09 citations — skipped (Paul). S11 Search Console / GA4 — skipped (no access; not needed per Paul).
- Local grid (S10): ranks only; the Local Dominator reports' written advice is never used; grid centre unverified; competitor review counts unreliable.
- Fan-out (S21): not demand, no volume, never evidence for CM-019/020/021 (CM-045).