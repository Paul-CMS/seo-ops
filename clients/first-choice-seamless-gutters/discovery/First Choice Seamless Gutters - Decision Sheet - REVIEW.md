# First Choice Seamless Gutters - Decision Sheet - REVIEW

**Every identity and format decision for this client, together, once** (R6, Paul 2026-10-08). The discovery agent
filled the *Recommended default* and the *Evidence* from public research (run `20261022-084632-discovery-42fd`,
2026-10-22; sources in `First Choice Seamless Gutters - Discovery Record - REVIEW.md`). Paul answers only where he
disagrees — a blank *Answer* means the default stands. Approved with the entity foundation and the client facts in
**Approval 1** (`/approve first-choice-seamless-gutters entity_approved proof_sheet_approved`); approve.py then settles
every row. The audit and Build apply these and never ask again. New contradicting evidence → one reopen request.

**Open choices for Paul (rows marked ◆):** category_entity (conflict), area_entity (two out-of-county towns),
address_display.website, tools.grid.

| Key | Decision | Recommended default | Answer (Paul) | Evidence / why |
|---|---|---|---|---|
| category_entity ◆ | GBP primary category = the category entity (Wikipedia-verified, BB-106/107) | **Gutter service** (Wikipedia entity: *Rain gutter*, Q152833) — confirmed on the GBP dashboard by Gwen's lookup before Build | | Maps place data for the listing carries category id `gutter_service`; Paul's intake said "Seamless gutters" — conflict recorded (PROC-01), not resolved. "Gutter service" is the broad category (BB-107). Wikipedia "Rain gutter": "A rain gutter, eavestrough, eaves-shoot or surface water collection channel…" |
| category_variants | Category variants (4–6, real search terms, BB-109) | Gutter Service · Seamless Gutters · Rain Gutters · Gutter Contractor · Gutter Installation | | Rain gutter article (names "seamless gutters", "gutter guards"); BBB categories "Gutter Contractors, Gutters, Gutter Cleaning, Gutter Guards, Gutter Installation"; brand name. Search volume checked in the data step. |
| scope_descriptor | Scope descriptor (e.g. residential, commercial) | **residential** (description only; commercial stays a service page) | | Site/GBP speak to "homeowners" throughout; one page `/services/commercial-gutters/`. Neither is a category variant. |
| area_entity ◆ | Area entity (Russian Doll path recorded, BB-105/110) | **Polk County, Florida** (= Lakeland–Winter Haven MSA, Q501043); Plant City and Sebring asked on the proof sheet and, if served, listed without location pages | | SAB (Paul intake; GBP shows no address) → containing metro (BB-110). Winter Haven → Polk County: "Polk County comprises the Lakeland–Winter Haven metropolitan statistical area (MSA)." Contains 19 of 20 site towns; outliers Plant City (Hillsborough, site + GBP) and Sebring (Highlands, GBP only). Alternative: **Central Florida** (Q2920358) — contains Plant City but not Sebring, and Wikipedia notes it is now used mostly for the Orlando area. GBP: "We service all of Polk County!"; footer "Proudly Serving Polk County, Florida". |
| area_variants | Area variants (3–5) | Polk County, FL · Polk County, Florida · Lakeland–Winter Haven · Lakeland–Winter Haven metropolitan area | | Wikipedia (county title; MSA name, which redirects to the county). |
| homepage_title_variant | Area variant reserved for the homepage SEO title (exclusive, CM-024) | **Polk County, FL** | | The business's own framing ("Polk County" in GBP About, footer, areas page). Current title uses "Lakeland, FL" (observation). |
| homepage_h1_variant | Area variant for the homepage H1 | **Lakeland–Winter Haven** | | Familiar local name for the MSA; differs from the title variant (BB-108). |
| title_format.homepage | SEO-title format — homepage | `Category Variant in Area - Brand` | | template default |
| title_format.service | SEO-title format — service pages | `Service Name - Brand` | | template default |
| title_format.location | SEO-title format — location pages | `Category Variant in City, ST - Brand` | | template default; 20 location pages exist under `/areas-we-serve/<town>-fl/` |
| title_format.about | SEO-title format — about page | `About Brand - Category in Area` | | template default |
| title_format.blog | SEO-title format — blog posts | `Post Title - Brand` | | template default; 2 posts exist |
| brand_in_titles | Brand written in full in every title (no abbreviation) | yes — **First Choice Seamless Gutters** (legal suffix "Inc." left out of titles; kept in schema `legalName`) | | GBP name "First Choice Seamless Gutters Inc."; BBB primary name without "Inc."; site also prints "First Choice Seamless Gutter Inc" (singular). |
| service_list | Services offered | The 11 site services: Seamless Gutter Installation · Gutter Installation · Gutter Repair · Commercial Gutters · Gutter Downspouts · Gutter Guards · Gutter Maintenance · Gutter Cleaning · Copper Gutters · Galvalume Gutters · Aluminum Gutters — client confirms on the proof sheet; folding is the audit's call | | Site `/services/`; GBP services show Seamless Gutter Installation, Gutter Guard Installation; BBB adds Gutter Cleaning. |
| towns_served | Towns served | The 19 Polk towns on the site + Lakeland Highlands (GBP); Plant City and Sebring only if the client confirms | | Site areas list (20) vs GBP Location list (15) — differences in the Discovery Record §4. |
| address_display.gbp | Street address shown on the GBP? | **no** (SAB, as now) | | Paul intake: SAB; GBP shows a service area, no address. |
| address_display.website ◆ | Street address shown on the website? | **no** — matches GBP; the street address in the site's schema is an audit observation | | Site pages show no address; JSON-LD carries "3517 Century Blvd", Lakeland 33811 (press release prints the same); HomeAdvisor snippet "1575 Lemon Ave". Which, if any, is real goes to the proof sheet. |
| the_best_policy | "The Best" in H1s (CM-020) | per page, by CM-020 | | Proof leg: GBP 5.0 with 138 reviews (2026-10-22) meets 4.5+/25+; GutterPro HQ "award" is a company-distributed press release, not counted. |
| blog_author | Blog author (a real person, CM-039) | the owner named on the returned facts (candidate: Adrian Buehl) | | BBB: "Adrian Buehl, Owner"; "Rachel Buehl, Owner". Named in reviews as "Adrian". |
| sensitive_category | Sensitive category (CM-025, CM-040) | not sensitive | | `status.py classify "seamless gutters"` → sensitive: no |
| cms | The site's CMS | WordPress | | intake (client_confirmed); wp-check passed 2026-10-22 |
| wordpress_login | WordPress login for the system | dedicated Editor | | last wp-check: "username to confirm (seo-ops vs paulmeisner)" |
| tools.citations | Citations data this audit | BrightLocal | | agency standard (agency profile §1) |
| tools.grid ◆ | Local grid tool | BrightLocal | | agency profile §1: BrightLocal or Local Dominator — Paul's pick |
| tools.gsc_ga4 | Search Console / Analytics access | use Search Console (access exists); GA4 not used unless shared | | intake: "Access exists (Paul reports)" |
