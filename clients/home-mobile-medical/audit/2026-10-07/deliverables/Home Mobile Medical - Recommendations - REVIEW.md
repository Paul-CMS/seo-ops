# Home Mobile Medical - Recommendations - REVIEW

**Status:** REVIEW - awaiting Paul (gate audit_approved). Rendered 2026-10-08 from the audit registers in `clients/home-mobile-medical/audit/2026-10-07/` (run 20261007-203219-discovery-784c); re-rendered 2026-10-09 after Paul's answers to Q1, Q2 and Q8 (run 20261009-071238-discovery-94fa). Rendered, never edited: to change anything, change the register row and re-render.

The audit recommendation package (seo-technical-audit Review): executive summary, prioritized register, URL decisions, measurement plan, assumptions and limitations, change preview, questions and client-confirmation list. Recommendations only - nothing here is implemented, and nothing could be pasted into the CMS as it stands.

## 1 · Executive summary

**Where the site stands.** homemobilemedical.com still presents the business it used to be - a walk-in home-medical-equipment and rental store serving South Carolina and Georgia (and, in published but unlinked pages, Florida and Michigan) - rather than the business it is now: a family-owned, service-area stair-lift and accessibility-lift installer for the South Carolina Lowcountry (Brand Guide A). The homepage title names "Home Medical Equipment"; every page's navigation links to discontinued services and to a Georgia hub; and the Google listing's 19 reviews (2.9 stars) all describe the former store.

**Verified strengths.**
- The GBP primary category is already Mobility equipment supplier, and name and phone are consistent on all 9 active citations.
- All 24 confirmed South Carolina towns have a page at the canonical /service-area/<city>-sc/ pattern, each with a city map embed and local attraction links; every location page links to every existing service page.
- The four core service pages exist at clean, city-free URLs.
- Every crawled page returns 200 or a working 301, is indexable and self-canonical; DataforSEO finds no cannibalization (no two URLs ranking for one query).
- The homepage holds 708 referring domains, and the Medicare coverage post ranks #2 for "will medicare pay for a stairlift".

**Primary constraints.** No Search Console, analytics or lead data (DataforSEO stands in for CM-019); the crawl is a 2026-09-18 Screaming Frog free crawl without body text; all page specs are still DRAFT; the client has not yet confirmed "no leads" for any URL, so no redirect is ready to go to Paul.

**Overall confidence.** Entity and architecture findings are corroborated by two independent sources in most cases (crawl + link export, crawl + CMS). Claim findings rest partly on the approved Brand Guide's quotes of the crawl. Rankings are US-level only.

**Highest-leverage recommendations.**
1. Take the discontinued services and the Georgia hub out of the site navigation, and Georgia links out of the service pages (non-destructive menu/link handoffs - F-002, F-003).
2. Rebuild the homepage title around the GBP category entity and the Lowcountry area entity (F-001), and give every rebuilt page one H1 and a brand-led title (F-022, F-023).
3. Create the repair & maintenance service page (F-014) and build the full city mesh and service-areas tables in the rebuilds (F-016, F-017).
4. Remove unsupported safety, regulatory and service claims and the second address (F-004, F-005, F-006).
5. Retire the 36 out-of-area, discontinued and duplicate URLs as decided 301s (client confirmed no leads, Paul 2026-10-09 - F-003, F-013, F-015), and get the client's answer on the GBP history (Q9) so the review plan can move.

## 2 · Prioritized register

Severity per CM-028. Full rows: Finding Register - REVIEW.

### High - breaks the entity model or page structure (12)

| ID | Issue | Affected | Depends on | Owner |
|---|---|---|---|---|
| F-001 | Homepage SEO title is "Home Mobile Medical — Home Medical Equipment — South Carolina Lowcountry"; the category slot reads "Home Medical Equipment". The GBP primary category entity is "Mobility equipment supplier" (Brand Guide A2). The homepage meta description... | 1 | Build homepage batch (final1); title change is a VA handoff (CLAUDE.md section 4) | Jonie (handoff) after Build |
| F-002 | The site-wide navigation/footer on all 102 pages in the link-level export links to the Georgia hub /service-area/savannah/ (SF Unique Inlinks = 96 on that URL). Every service page links to /service-area/savannah-ga/, /service-area/pooler-ga/ and /service-area/... | 15 | Microsite project (separate /new-client); menu handoff to Jonie | Jonie (menu handoff) |
| F-003 | Live, indexable pages describe services the business does not offer (Brand Guide D "Not offered": broad DME, rentals, power chairs, scooters/scooter lifts, mobility ramps): (a) the site-wide navigation links to /services/power-chairs/, /services/scooter-lifts/... | 17 | Q3 for the four C1-fail URLs; Build batches; menu handoff; redirect handoff (Jonie) after audit_approved | Jonie (menu/redirect handoffs) after Paul |
| F-005 | Safety claims without a named authoritative source appear on commercial pages of a health-adjacent client: homepage "Safety is our top priority, and we adhere to the highest standards and regulations."; Beaufort page "...installation meets the highest standard... | 2 | Paul review recorded (CM-025) | Build writer -> Paul -> Jonie |
| F-013 | 20 SC URLs duplicate the intent of a canonical service or location page through legacy patterns: service+city combinations (/charleston-sc/stair-lifts/, /charleston-sc/wheelchair-lifts/, /hilton-head/stair-lift/, /hilton-head/wheelchair-lift/, /hilton-head/sta... | 20 | Q3 for the 6 value URLs; F-014 (repair page) for the repair redirect and /bluffton-sc/wheelchair-lift-repair/; redirect handoff (Jonie) after audit_approved | Paul decides; Jonie (redirect handoffs) |
| F-014 | Repair and maintenance of any stair lift or lift is a confirmed service (Brand Guide D Services; Paul 2026-10-07) with no service page. Repair intent is served only by two service+city pages: /bluffton-sc/wheelchair-lift-repair/ (7 keywords in the top 100, bes... | 3 | Build svc1; repair redirect paired with the publish; Q3 for the Bluffton URL | Build |
| F-015 | 17 Florida and Michigan pages (6 FL, 11 MI) are published in the CMS (status Publish) and listed in the XML page-sitemap, but no internal link points to them (not reached by the crawl). DataforSEO shows 0 ranking keywords and 0 referring domains for every one;... | 17 | Q6 (live status, checked within the redirect handoff); redirect handoff (Jonie) after audit_approved | Jonie (sitemap + redirect handoffs) after Paul |
| F-016 | Each service page links to only 4 of the 24 SC location pages (/service-area/hardeeville-sc/, /service-area/ladys-island-sc/, /service-area/ridgeland-sc/, /service-area/walterboro-sc/), plus Georgia pages (/service-area/savannah-ga/, /pooler-ga/, /rincon-ga/),... | 5 | Build svc1; Finish link wheel | Build / Finish |
| F-017 | Each SC location page links to 9-10 of its 23 sibling location pages - only the cities of its own metro cluster (e.g. /service-area/beaufort-sc/ links Beaufort-area cities; /service-area/charleston-sc/ links Charleston-area cities); /service-area/ladys-island-... | 24 | Build location batches; Finish link wheel | Build / Finish |
| F-022 | 54 of the 96 crawled 200 pages have no H1: all 5 service pages, all 24 SC location pages, the 3 hubs, /services/, /terms-conditions/, and 20 Georgia/legacy pages. On the location pages the first H2 repeats the SEO title string including the brand (e.g. "Stair ... | 54 | Build batches | Build |
| F-023 | All 24 SC location titles lead with a service phrase: 22 read "Stair Lift Installation in <City>, SC \| Home Mobile Medical" (brand last); /service-area/folly-island-sc/ uses that pattern but names Folly Beach (F-007); /service-area/ladys-island-sc/ reads "Medi... | 24 | Build location batches | Build -> Jonie |
| F-032 | Posts make coverage, tax, legal, health and product-spec claims with no named authoritative source recorded: Medicare/Medicaid/insurance coverage of stair lifts (two posts; the larger ranks #2 for "will medicare pay for a stairlift"), tax deductibility, ADA co... | 10 | Blog Decision Map; Paul review | Blog agent -> Paul |

### Medium - fails a page-spec check (DRAFT specs: advisory) (13)

| ID | Issue | Affected | Depends on | Owner |
|---|---|---|---|---|
| F-004 | The site publishes a second address, "106 Arrow Road, Hilton Head, SC 29928": (a) an outbound Google Maps directions link (SRC-001 row 12: 1 inlink, crawl depth 2, so it sits on one page at crawl depth 1 - not the homepage, which is depth 0, and not the site-w... | 2 | VA locates the source page; audit_approved (content fix) or Build rebuild of /service-area/beaufort-sc/ | Jonie (handoff) |
| F-006 | Claims not supported by Brand Guide Section D appear on live pages: homepage "Our experienced technicians..."/"skilled professionals" (Section D: Jason plus one helper) and three placeholder testimonials (Paul: placeholders, remove); Beaufort page "Every lift ... | 5 | Build batches | Build writer -> Paul |
| F-007 | The Folly Island page names two different places: title "Stair Lift Installation in Folly Beach, SC \| Home Mobile Medical", meta "...stair lift installation in Folly Beach, SC...", city map embed q=Folly Beach, SC, while the H2-1 reads "Stair Lift Installation... | 1 | Build Charleston-metro location batch | Build |
| F-008 | The Yemassee page's first H2 reads "Stair Lift Installation in Port Royal, SC \| Home Mobile Medical" (the CMS excerpt opens with the same Port Royal heading) while its title, meta, slug and second H2 name Yemassee. | 1 | Build HHI-metro location batch or a content fix | Build / Jonie |
| F-009 | The Google listing shows 2.9 stars from 19 reviews (pulled 2026-10-07). All reviews date 2017 to 2023-03; they describe a walk-in medical-supply/rental store (wheelchair and lift-chair rentals, a breathing machine, mastectomy products, compression socks); none... | 1 | Client confirmation of the GBP history (new question, routed by Paul); then client action; GBP is outside the site (Gwen) | Gwen (GBP) / client |
| F-018 | The homepage links to 2 of the 4 core service pages (/services/stair-lifts/, /services/wheelchair-lifts/ - both via the site-wide navigation); it does not link to /services/curved-stair-lifts/ or /services/porch-lifts/, and it links to three discontinued servi... | 1 | Build final1 | Build |
| F-019 | The homepage links to none of the 24 location pages (only the three hub pages and the Georgia hub via navigation). | 1 | Build final1 | Build |
| F-024 | Title separators are mixed across the site: 46 titles use a pipe, 1 an em dash, 21 a hyphen, 3 an en dash, and three older service titles use the word "From" ("Stair Lifts From Home Mobile Medical", "Wheelchair Lifts From Home Mobile Medical", "Power Chairs Fr... | 31 | S20 (SEOPress settings worksheet) | Build / Jonie |
| F-025 | 16 of the 24 SC location pages open with the same sentence frame "Stay safe and independent with professional (or expert) stair lift installation from Home Mobile Medical, your trusted mobility experts serving <City> ..." - portable across siblings with only t... | 16 | Build location batches; facts interview if the evidence gate blocks (CM-041/042) | Build |
| F-026 | Homepage H1 "Enhance Your Independence And Mobility With Our Stair Lift Solutions" uses neither reserved homepage variant (B1: "Mobility equipment supplier", "South Carolina Lowcountry") and names no area. HP-08 / BB-313 section 3 say the homepage H1 is never ... | 1 | Q4 / conflict CF-LOCAL-001; lessons.md L-009 (PROPOSED) | Paul |
| F-029 | All 21 blog posts are authored by the WordPress user "wittycow"; the blog author must be the owner (Jason Workens, Brand Guide D named staff) unless the client states otherwise. | 21 | Blog Decision Map | Blog agent |
| F-030 | 20 of 21 post titles do not follow "Post Title - Brand": 18 omit the brand; 2 lead with it ("Introducing Home Mobile Medical - Revolutionizing Mobility Solutions", "Home Mobile Medical: Our Evolution from Beaufort Medical Equipment"). Only /costs-and-financing... | 20 | Blog Decision Map; S20 | Blog agent |
| F-031 | Four posts sit outside the entity: telemedicine history, long-term care, semaglutide side effects, and mobility-scooter repair (a discontinued service). DataforSEO shows 0 ranking keywords and 0 referring domains for all four. | 4 | Blog Decision Map | Blog agent |

### Low - hygiene, batched into one handoff (15)

| ID | Issue | Affected | Depends on | Owner |
|---|---|---|---|---|
| F-010 | Of 9 active citations in the BrightLocal tracker, names and phone match the confirmed NAP; address format varies: Yelp "2127 Boundary St, Beaufort, SC" (suite #5 missing); Hotfrog ZIP "Not found"; marketersmedia.com and locable.com have no NAP fields recorded;... | 1 | None | Gwen (citations) |
| F-011 | The tracker lists 9 active citations and 30 "Potential" sites not found, including Apple Maps, BBB, MapQuest, Yellow Pages and Manta; it also lists google.com as "Potential" although the GBP exists (tracker matching defect - not a finding). Brand Guide F recor... | 1 | RULE-014 approval | Gwen / Paul |
| F-012 | DataforSEO shows 708 referring domains (717 backlinks, 694 dofollow) to the homepage; only 8 referring domains have a spam score of 30 or below; median backlink spam score 55. Four other URLs each have 1 referring domain (storeboard.com -> http homepage; news.... | 1 | None | Paul (monitor) |
| F-020 | Hub pages: /service-area/charleston/ (161 words) and /service-area/hhi-beaufort/ (175 words) carry little more than a link list; /service-area/ has 795 words. None has an H1. Titles: "Service Area", "Charleston Service Area - Home Mobile Medical", "Hilton Head... | 3 | L-008 ruling; county-hub spec approval | Build |
| F-021 | /services/ is a services hub (title "Mobility Devices \| Home Mobile Medical", 980 words, no H1). No page spec in methodology/specs covers a services hub; Brand Guide C1 lists it as "Services hub - Planned (rewrite)". | 1 | Paul (spec decision) | Paul |
| F-027 | About page title "About Us - Home Mobile Medical" lacks the area/category part of the spec format "About Brand - Area Category". | 1 | Build final2 | Build |
| F-028 | About page H1 is "About us" - no category or area variant. | 1 | Build final2 | Build |
| F-033 | Internal links point at redirecting URLs: /equipment-rentals/ (from 3 pages); /service-area/beaufort-sc-2/ (from 10 pages); /service-area/bluffton-sc-2/ (from 10 pages); /service-area/charleston-sc-2/ (from 10 pages); /service-area/hardeeville-sc-2/ (from 18 p... | 36 | Batched Low handoff | Jonie |
| F-034 | /services/stair-lift/ (a service-pattern URL) 301-redirects to the legacy city page /hilton-head/stair-lift/, which is itself Needs Evidence (CM-019 C2/C3 fail). | 1 | Disposition of /hilton-head/stair-lift/ | Jonie |
| F-035 | The XML page-sitemap lists 37 URLs that no crawled page links to (orphan candidates): Florida/Michigan pages, /stair-lift-installer/*, Georgia /savannah-ga/* pages, /hilton-head/*, /charleston-sc/, /beaufort-sc/, /power-chairs/, /about-us-across-the-web/ and /... | 37 | S20 (SEOPress sitemap settings); audit_approved; paired with the redirect handoffs | Jonie |
| F-036 | Meta descriptions: 12 pages have none (blog index, category and pagination archives); 20 exceed 160 characters (legal pages, /contact/ 288, /about/ 328, /service-area/charleston/ 327, costs post 321 - several are truncated body text); the service pages /servic... | 35 | audit_approved (safe fix) | Jonie |
| F-037 | Outbound links return errors: https://summervilledream.org/farmers-market/ (404, SRC-001 row 119); https://parks.chathamcountyga.gov/CommunityParks/TomTriplett (404, SRC-001 row 130); https://parks.chathamcountyga.gov/BoatRampsAndFishingPiers/TybeeIslandFishin... | 1 | audit_approved | Jonie |
| F-038 | Two published CMS pages of unclear purpose are not linked internally: /new-homepage/ (CMS page "New Homepage", published 2026-09-10, not in the sitemap) and /about-us-across-the-web/ (in the sitemap; a list of directory names). Live status and robots directive... | 2 | Q5 | Jonie (check) / Paul |
| F-039 | 11 category and pagination archives are indexable ("index, follow"), have no meta description and 38-282 words; categories include off-entity topics (Telemedicine, Long Term Care, Health). | 11 | Blog Decision Map | Blog agent |
| F-040 | A GA4 tag (gtag.js?id=G-5GX2RP9PYX) and WordPress.com stats are loaded, but no GA4, GSC, call-tracking or form-delivery access exists for this audit; the conversion path (phone, form, upcoming photo-quote upload) is unvalidated. | 1 | Client access | Paul |

## 3 · URL decisions (summary)

| Decision | Rows |
|---|---|
| Keep | 38 |
| Redirect (301) - decided (Paul 2026-10-09; CM-019 C1-C4 pass) | 36 |
| Improve (keep URL, rebuild) | 35 |
| Keep existing 301 | 22 |
| Hold - Georgia microsite (Paul) | 18 |
| Needs Evidence - fails CM-019 (keep live) | 7 |
| Needs Evidence (status check) | 2 |
| Create | 1 |

36 URLs pass CM-019 conditions 1 to 3 (17 Florida/Michigan, 5 discontinued-service pages, 13 South Carolina legacy duplicates, and /services/straight-stair-lifts/ which Paul wants consolidated) and, with the client's "no leads" confirmation (Q1) and Paul's exception on the citation check (Q8), now pass all four conditions: they are decided 301s to the default targets (Q2; Paul 2026-10-09), issued as VA redirect handoffs to Jonie after audit approval. /hilton-head/stair-lift-repair/ waits for its target /services/stair-lift-repair/ to be published. 10 URLs fail CM-019 and stay live. 18 Georgia URLs are held for the microsite. Detail: URL Decision Map - REVIEW.

## 4 · Measurement plan

| What | Baseline (source, date) | Success indicator | Comparison window | Confounders | Reassess |
|---|---|---|---|---|---|
| Entity rankings | 115 ranked keyword rows, 15 URLs; no lift or Lowcountry keyword in the top 3 (DataforSEO Labs US, 2026-10-07) | Lift/area keywords ranking for the rebuilt service and location pages | re-pull 60 days after each batch ships | US-level data only; off-entity DME rankings will fall by design | after each Build batch |
| Local grid | Stair Lift Solutions Lowcountry: average 16.38 (map) / 18.53 (local pack); Bluffton keywords 20+ (Local Dominator, 2026-09-18, 12x12, 2 mi) | Lower average rank on the same keywords | same keywords, same grid | grid centre and device not recorded (Q7) - not comparable until fixed | after the GBP review plan and the rebuild |
| Reviews | 2.9 stars, 19 reviews, newest 2023-03 (DataforSEO, 2026-10-07) | New lift-customer reviews | quarterly | GBP history unknown (Q9) | quarterly |
| Leads / conversions | **Not measurable** - GA4 tag present (G-5GX2RP9PYX) but no access; no call tracking (F-040) | Form and phone enquiries | from access onward | none yet | when access is granted |
| Backlinks | 708 referring domains to the homepage, median spam score 55 (DataforSEO, 2026-10-07) | stable; no new low-quality links | 6 months | none | Finish |

## 5 · Assumptions and limitations

- **Evidence base.** Crawl: Screaming Frog free licence, 2026-09-18 - no JavaScript rendering, no body text, only the first two H2s per page. Linkdominator (2026-09-28, rendered DOM, DOM parity "Yes" on all pages) was used to rule out JavaScript-only headings and links. Many section, FAQ and claim checks are therefore "needs evidence" in the conformance scorecard. Claims are quoted from the approved Brand Guide (D2) and the CMS excerpts.
- **No GSC / GA4 / CRM.** DataforSEO replaces Search Console for CM-019 (Paul 2026-10-06). Rankings are US-level. Unknown metrics stay unknown.
- **Uncrawled URLs.** 40 URLs (CMS, sitemap or backlink data only) were not status-checked (Q6). Their dispositions assume they are live.
- **CM-019 condition 3** is a negative check through DataforSEO referring domains; it can miss a listing DataforSEO has not indexed. Paul accepted that limitation for the 36 decided 301s and waived the listing check (Paul Exception, Q8, 2026-10-09).
- **Specs.** All page specs are DRAFT - every failed check is a recommendation, not a gate. Hub conformance is capped at Low (county-hub spec DRAFT; metro-hub rule L-008 PROPOSED). About-page title/H1 formats are Coastal defaults (Low until Paul rules).
- **Schema readiness:** not assessable (no structured-data export; SEOPress site-wide settings pending with Jonie, S20).
- **Local grid:** six scans recorded as measured observations only; centre and device not stated, so no grid finding (Q7).
- **Tool issue lists** (Linkdominator heading gaps, alt text, thin content) not promoted without corroboration; its canonical warning is contradicted by the crawl.
- **Gate B defaults in force until answered:** every disposition that waits on Q3-Q7 or Q9 stays Needs Evidence; affected findings carry confidence Assumed for that part. Q1, Q2 and Q8 are answered (Paul 2026-10-09, DEC-LOCAL-008).
- **Paul's decisions applied, not re-litigated:** Georgia to a separate microsite (hold, no redirect to SC pages); Florida and Michigan dropped; 301 only, never 410; three hubs kept; five services; blog posts kept as they are until the Blog Decision Map; Folly Island; 24 SC towns confirmed.
- **Independent review:** Claude did both analysis and review under the standing exception CM-026; the review ran in a fresh-context reviewer (DEC-LOCAL-006).

## 6 · Change preview (what Build and implementation would consider - not instructions)

- **Navigation (Jonie, menu handoff):** remove links to /services/power-chairs/, /services/scooter-lifts/, /services/mobility-ramps/ and /service-area/savannah/.
- **Content fixes after audit approval (safe fixes):** remove the 106 Arrow Road directions link and closing-copy address; correct the Yemassee heading; fix dead outbound links; meta descriptions on kept utility and blog pages.
- **Rebuilds in Build (site plan already approved):** homepage, about, /services/ (spec decision first), four service pages + the new repair page, 24 location pages, three hubs - each with one H1, brand-led titles in the house format, the full city mesh and service-areas tables, only Section D claims, and the approved safety statement.
- **Sitemap (Jonie, after audit approval):** remove the 29 sitemap-listed decided 301s from the XML sitemap, paired with their redirect handoffs (no noindex; Georgia rows untouched).
- **Redirects (Jonie, after audit approval):** 301 handoffs for the 36 decided rows (full from/to URLs, 301, reason, URL ID; /hilton-head/stair-lift-repair/ paired with the repair page's publish); repoint the three two-hop redirects; revisit /services/stair-lift/'s target.
- **GBP and citations (Gwen, after Q9 and RULE-014 where spend):** citation NAP fixes; any review plan within Google policy.
- **Blog (Blog Decision Map):** author, titles, sourced rewrites of coverage/health claims, off-entity posts and archives.

## 7 · Questions for Paul and the client-confirmation list

- **Q1 (Paul) - answered 2026-10-09 by Paul (Q1: client, via Paul)** - Will the client confirm (CM-019 condition 4) that these URLs brought no leads: the 17 FL/MI pages, the discontinued-service pages (/services/power-chairs/, /services/scooter-lifts/, /services/mobility-ramps/, /charleston-sc/power-chairs/, /power-chairs/), /services/straight-stair-lifts/ and the 13 SC legacy duplicates that pass C1–C3 (list: URL Decision Map, ext_cm019_result = "C1–C3 pass")? *Answer:* Client confirms no leads from any of the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy incl. /services/straight-stair-lifts/). CM-019 C4 passes; all 36 become 301s. Settled: cm019-c4-no-leads. *Status:* answered - [x] confirmed no leads. *Was blocking:* F-003, F-013, F-015 (now revised by superseding row).
- **Q2 (Paul) - answered 2026-10-09 by Paul** - Redirect targets when Q1 clears: FL/MI (17) → /services/stair-lifts/? power chairs and scooter lifts → /services/? mobility ramps → /services/porch-lifts/? (old map said never blanket to an unrelated page). *Answer:* Defaults: FL/MI -> /services/stair-lifts/; power chairs and scooter lifts -> /services/; mobility ramps -> /services/porch-lifts/; SC legacy duplicates -> their canonical service/location page per the URL Decision Map. Settled: redirect-targets-default. *Status:* answered - [x] defaults. *Was blocking:* F-003, F-015 (now revised by superseding row).
- **Q3 (Paul)** - The 10 URLs that fail CM-019 (rank or have links): /savannah-ga/, /service-area/savannah-ga/, /savannah/stair-lift/ (Georgia — already Hold), /charleston-sc/mobility-ramps/, /service-area/mt-pleasant-sc/, /bluffton-sc/, /bluffton-sc/wheelchair-lift-repair/, /bluffton-sc/stair-lift-installer/, /charleston/stair-lift/, /hilton-head/stair-lift/. Keep them live (rewrite/de-link, no redirect), or grant a Paul Exception to CM-019 for any of them (most rankings are off-entity DME/rental queries at positions 34–86)? *Why:* CM-019 forbids a destructive recommendation; only a Paul Exception (PROC-02 rung 5) can move them. *Default:* Keep live, strip discontinued/DME claims, no redirect (Needs Evidence). *If defaulted:* Duplicate/legacy pages persist alongside the rebuilt canonical pages. *Blocks:* F-003, F-013, F-002
- **Q4 (Paul)** - Conflict CF-LOCAL-001: may the live homepage H1 be changed to the reserved B1 variants (HP-06), given HP-08/BB-313 §3 "never changed once live"? *Why:* Decides whether F-026 becomes a rebuild instruction or stays report-only. *Default:* Follow the current rule: no homepage H1 change. *If defaulted:* Homepage H1 keeps omitting the entity; F-026 stays advisory. *Blocks:* F-026
- **Q5 (VA (Jonie))** - Is /new-homepage/ live (HTTP 200, indexable) or draft/private? Same check for /about-us-across-the-web/. *Why:* If live and indexable, a duplicate homepage exists (severity rises; a destructive option comes into play). *Default:* Treated as unknown — Needs Evidence. *If defaulted:* F-038 stays Low/Needs Evidence. *Blocks:* F-038
- **Q6 (VA (Jonie))** - HTTP status of the 40 uncrawled URLs (CMS/sitemap/backlink-only; list = URL Decision Map rows with ext_crawl_status "not crawled") — list-mode check. *Why:* A redirect handoff for a URL that already 404s/410s is wrong; a 200 confirms the candidate. *Default:* Assume live 200 (CMS "Publish" + sitemap). *If defaulted:* Redirect rows carry an unverified premise until checked. *Blocks:* F-013, F-015, F-035
- **Q7 (VA (Gwen))** - Grid centre point and device for the six Local Dominator scans (2026-09-18). *Why:* Without them the grids are not reproducible (analysis-rules §4) and support no finding. *Default:* No grid finding; results kept as measured observations (inventories/local-grid.csv). *If defaulted:* GBP map visibility is unassessed as a finding. *Blocks:* none written — would enable a §4 grid finding
- **Q8 (VA (Gwen)) - answered 2026-10-09 by Paul** - Open each active tracked citation (facebook, bing, yelp, storeboard, chamberofcommerce, hotfrog, marketersmedia, tupalo, locable) and record the website URL it links to. *Answer:* Paul Exception: the citation link-destination check is skipped; CM-019 C3 accepted on DataforSEO referring-domain evidence for the 36 URLs. Settled: cm019-c3-citation-check-waived. *Status:* answered - waived (Paul Exception). *Was blocking:* F-013, F-015, F-003 (all C1-C3-pass rows in the URL Decision Map) (now revised by superseding row).
- **Q9 (Paul (cannot answer - client option))** - GBP history: was this Google listing the Beaufort Medical Equipment listing, renamed? Who owns and manages it since the sale? (Two reviews name "Beaufort Medical" and Jason; the live post /embracing-a-new-era-from-beaufort-medical-equipment-to-home-mobile-medical/ presents HMM as its continuation, while Brand Guide D History says HMM is not a rebrand.) *Why:* The answer either corrects Brand Guide D History or explains the reviews; it decides what the listing may keep (RULE-006) and whether any review plan or GBP change is safe. *Default:* No review plan and no GBP change until the client answers; Brand Guide D History stays as approved. *If defaulted:* F-009 recommendations wait; the GBP keeps presenting the former store. *Blocks:* F-009

**Client-confirmation list** (Paul sends; the system never contacts the client): Q1 answered 2026-10-09 (client confirms no leads from the 36), Q9 (GBP history and ownership), and every on-page claim the rebuilds must not carry without proof - "experienced technicians"/"skilled professionals", "custom-fit", "all ... battery backup", "guarantee" wording, "safety ... regulations", same-day without "in most cases", rentals, the Medicare/Medicaid/tax/ADA/product-spec statements and the stair-lift price ranges in the blog.

## 8 · Open conflict

- **CF-LOCAL-001 (OPEN)** - Homepage H1 on a legacy (pre-Standard) homepage. Claim A: "H1 ... Never changed once live." / HP-08: no recommendation changes the homepage H1 once live (methodology/specs/homepage.md §3 row 3 and HP-08 (BB-313 §3)). Claim B: HP-06: H1 must use the reserved B1 variants and a different variant of every title entity (methodology/specs/homepage.md HP-06 (BB-304, CM-024, CM-046)). Current rule followed: Follow the lock: no H1 change recommended (PROC-01 step 1). Proposed ruling (filed as methodology/lessons.md L-009, PROPOSED, 2026-10-08): BB-313 §3's lock applies to H1s built to the Standard or ranking top 3 for the main keyword (CM-020); a legacy homepage H1 that fails HP-06 and holds no top-3 entity ranking may be rebuilt once, with the change logged.

## 9 · Low items - one batched handoff list

| Finding | Owner | Gate | What |
|---|---|---|---|
| F-010 | Gwen (citations) | none | Gwen corrects the Yelp suite, Hotfrog ZIP and Chamber category to the Brand Guide F NAP/category and confirms the marketersmedia/locable NAP. |
| F-011 | Gwen / Paul | RULE-014 approval | No citation order during the audit (RULE-009). Paul decides any citation build per RULE-014 (provider, cost, renewal, duplicate plan) after NAP/GBP facts are reconciled; Apple Maps is the first gap (also a Finish schema input). |
| F-012 | Paul (monitor) | none (monitor) | No removal or disavow recommendation (CM-006: where a client exceeds the link average, stop adding and correct relevance; a disavow would rest on a Working Hypothesis - publication gate). Monitor; Paul may review in Finish. |
| F-020 | Build | L-008 ruling | Rebuild each hub in its location batch once Paul rules L-008 and approves the county-hub spec; give each real area substance (BB-207). |
| F-021 | Paul | Paul spec decision | Paul decides whether /services/ gets a spec (or follows the homepage services-section pattern) before it is rebuilt; content scope per F-003. |
| F-027 | Build | Paul rules about-title format; Build final2 | Retitle in the about rebuild (final2) once Paul confirms the "Area Category" meaning. |
| F-028 | Build | Paul rules about-H1 format; Build final2 | Use a B2-pool variant H1 in the about rebuild once Paul rules the about H1 format. |
| F-033 | Jonie | audit_approved (redirect repoint = structural, Paul) | Point internal links at the final URLs; repoint the three "-2" redirects straight to the canonical slash URL (one hop). Most links disappear with the Build rebuilds; the redirect repoint is a VA handoff. |
| F-034 | Jonie | Paul | Revisit the target when /hilton-head/stair-lift/ is decided; /services/stair-lifts/ is the natural target. Changing a redirect target is a structural handoff (Paul). |
| F-035 | Jonie | audit_approved; paired with the redirect handoffs (301s decided, Paul 2026-10-09) | Remove from the XML sitemap (VA handoff - SEOPress settings are handoffs) the 29 URLs that are decided 301s (Paul 2026-10-09, URL Decision Map): the 17 FL/MI URLs (F-015), /stair-lift-installer/ and /stair-lift-installer/{walterboro, ladys-island, mt-pleasant, hardeeville, ridgeland}/, /beaufort-sc/, /charleston-sc/, /hilton-head/, /hilton-head/wheelchair-lift/, /hilton-head/stair-lift-repair/ and /power-chairs/. Pair each removal with that URL's redirect handoff; the exclusion must not set noindex (the 301 is the disposition). Leave unchanged: the 6 Georgia URLs (/savannah-ga/ and its 3 children, /stair-lift-installer/pooler/, /stair-lift-installer/rincon/ - Hold, no action on this site now, Paul), /bluffton-sc/stair-lift-installer/ (fails CM-019 C1 - Q3) and /about-us-across-the-web/ (Q6 and the Finish ID-page decision). Removing from the sitemap does not delete pages. URL dispositions per the URL Decision Map. |
| F-036 | Jonie | audit_approved (safe fix) | Rebuilt pages get spec meta descriptions; for kept utility/blog pages, fix in the batched Low handoff (meta descriptions are a safe fix after audit_approved). |
| F-037 | Jonie | audit_approved (safe fix) | VA re-checks and replaces/removes dead outbound links on SC pages (safe fix: broken links) - or the rebuilds drop them; ignore Georgia pages (held). |
| F-038 | Jonie (check) / Paul | Q5 | VA checks HTTP status and robots for both (Q5). If /new-homepage/ is live and indexable, it is a duplicate homepage carrying unapproved claims: Paul decides, and any noindex/redirect is destructive (CM-019); severity is re-set after Q5. /about-us-across-the-web/ is reviewed in Finish as a possible sameAs/ID-page input. |
| F-039 | Blog agent | Blog Decision Map | Handle with the blog in the Blog Decision Map (taxonomy cleanup; any noindex is destructive -> CM-019). No change now. |
| F-040 | Paul | client access | Paul asks the client for GA4/GSC read access (or a VA check that forms deliver) before Build launches; measurement plan in the S18 package. |
