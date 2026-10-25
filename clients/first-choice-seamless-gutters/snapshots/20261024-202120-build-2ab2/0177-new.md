# First Choice Seamless Gutters - Site Plan - REVIEW

Run 20261024-202120-build-2ab2 · 2026-10-24 · Build, step `plan` · data file: `build/site-plan.json`

**30 pages, written in 5 batches:** 10 service pages, 19 location pages, 1 About page. No county hub (F-016).
The homepage is not in the plan: it keeps its light-fix route and its H1 lock (F-017, F-020, F-033).

| Batch | Pages | What |
|---|---|---|
| pilot | 2 | Gutter Cleaning + Lakeland. A pilot is needed because this is the first seamless-gutters client (CM-061 §9) |
| services | 9 | The other service pages |
| locations-west | 9 | West and north Polk: Winter Haven, Auburndale, Bartow, Polk City, Kathleen, Highland City, Mulberry, Eagle Lake, Wahneta |
| locations-east | 9 | East Ridge and south Polk: Davenport, Haines City, Lake Alfred, Lake Hamilton, Dundee, Lake Wales, Waverly, Frostproof, Fort Meade |
| about | 1 | About page, written last |

There are 18 location pages after the pilot. That is more than the 15-page cap, so they are split into two batches by area (P10).

## 1. Open choices for Paul

| # | Choice | Options | Recommended |
|---|---|---|---|
| A | **Unincorporated places.** Highland City, Kathleen, Wahneta and Waverly are not incorporated towns. The client's note on the proof sheet suggests listing them under areas served instead of giving each its own page (Brand Guide Section E). | **a)** Keep all four pages. The approved URL Decision Map says to rebuild them, and Highland City already ranks #16 for "gutters highland". **b)** Merge each one into the nearest planned city page, with a 301: Highland City and Kathleen → Lakeland, Wahneta → Winter Haven, Waverly → Lake Wales. | **a)**, unless the viability check below shows a page cannot be sourced |
| B | **Lakeland Highlands.** It is on the GBP location list but has no page today. | **a)** No page. It is named in Lakeland's local context and on the service-area index. **b)** A new location page. | **a)** |

The viability check results are in section 9. Any location that check proposes to merge appears there as a kind-1 Ask.

## 2. URL changes (P7, CM-058). Every rebuilt page moves to one root slug

The URL rule does not allow a folder in a service or location URL. So all 29 service and location URLs drop
`/services/` or `/areas-we-serve/`. The old slug is kept, so for example `/services/gutter-repair/` becomes `/gutter-repair/` and
`/areas-we-serve/lakeland-fl/` becomes `/lakeland-fl/`. Each row lists its live URL under `replaces`, so its 301 is
created next to its publish row (publish.py). Nothing is deleted. `urlcheck.py`: **every planned URL follows the URL rule.**

- **Gutter Maintenance** (settled audit_gutter_maintenance): `/services/gutter-maintenance/` → 301 to **`/gutter-cleaning/`**.
  The live page mostly describes debris clearing, flushing, clog prevention and checks, which is closer to cleaning than to repair. Its
  hanger, resealing and slope-check scope goes into the Gutter Repair FAQ. The redirect is listed under the Gutter Cleaning row's `replaces`.
- **Plant City** (settled audit_plant_city): not in the plan. Its live page stays held. The 301 to `/areas-we-serve/` waits for the
  citation check (C3) and the client's no-leads answer (C4), as F-015 requires. That redirect is separate and is not part of this plan.
- `/areas-we-serve/` and `/services/` stay as index pages (VA light fixes). The link wheel and the VA's menu update point
  them at the new URLs.

## 3. Service pages (10)

Title format (settled): `Service Name - First Choice Seamless Gutters`. H1 format: `[Service variant] in [B2 area variant]`. The H1 never names a city
and never uses the reserved "Polk County, FL". Area variants rotate through the B2 pool; reuse across pages is correct (CM-024).

| Page | URL | Keyword | H1 | Group |
|---|---|---|---|---|
| Seamless Gutter Installation | /seamless-gutter-installation/ | seamless gutter installation | Continuous Rain Gutters in Polk County, Florida | Installation |
| Gutter Installation | /gutter-installation/ | gutter installation | Gutter Replacement in Lakeland–Winter Haven | Installation |
| Gutter Repair | /gutter-repair/ | gutter repair | Leaking and Sagging Gutter Repair in Polk County, Florida | Repair and upkeep |
| Commercial Gutters | /commercial-gutters/ | commercial gutters | Commercial Gutter Systems in Lakeland–Winter Haven metropolitan area | Specialty |
| Gutter Downspouts | /gutter-downspouts/ | gutter downspouts | Downspout Installation and Drainage in Polk County, Florida | Repair and upkeep |
| Gutter Guards | /gutter-guards/ | gutter guards | **The Best** Gutter Protection Systems in Lakeland–Winter Haven | Repair and upkeep |
| Gutter Cleaning (pilot) | /gutter-cleaning/ | gutter cleaning | **The Best** Gutter and Downspout Cleaning in Polk County, Florida | Repair and upkeep |
| Copper Gutters | /copper-gutters/ | copper gutters | Copper Gutter Systems in Lakeland–Winter Haven | Materials |
| Galvalume Gutters | /galvalume-gutters/ | galvalume gutters | Galvalume Steel Gutters in Polk County, Florida | Materials |
| Aluminum Gutters | /aluminum-gutters/ | aluminum gutters | Aluminum Rain Gutters in Lakeland–Winter Haven | Materials |

**Distinct intent for the overlapping pages** (F-014):
- **Seamless Gutter Installation** is about the seamless product itself: one continuous run.
- **Gutter Installation** is about replacing old gutters or adding gutters to a house that has none.
- **Gutter Cleaning** now absorbs the maintenance scope.
- The three material pages each answer their own material question.

COM-11 restate test: every H1, with the area variant and "The Best" removed, is a different service variant from the title term. All pass.
Commercial is written as a service; the site describes the business as residential (settled scope_descriptor).

## 4. Location pages (19)

- Title format (settled title_format.location): `Category Variant in City, ST - Brand`, using "Gutter Contractor".
- H1 format: `[Category variant] in [City]`, with no state. It alternates between "Rain Gutters" and "Seamless Gutters", so H1 and title never share a term (COM-11).
- Lakeland uses "Rain Gutters" because the locked homepage H1 already reads "Seamless Gutters in Lakeland, FL…".
- Keyword: `gutters <city> fl`. This follows the ranked queries "gutters lakeland" (390), "gutters winter haven" (50), "gutters davenport" (30), "gutters highland" (30) and "gutters hamilton" (30).
- No location is a GBP landing page: the GBP is a service-area business and its website field is the homepage. So no page gets LocalBusiness schema and no page shows an address.

| City | URL | Batch | Keyword | H1 |
|---|---|---|---|---|
| Lakeland | /lakeland-fl/ | pilot | gutters lakeland fl | Rain Gutters in Lakeland |
| Winter Haven | /winter-haven-fl/ | west | gutters winter haven fl | Seamless Gutters in Winter Haven |
| Auburndale | /auburndale-fl/ | west | gutters auburndale fl | Rain Gutters in Auburndale |
| Bartow | /bartow-fl/ | west | gutters bartow fl | Seamless Gutters in Bartow |
| Polk City | /polk-city-fl/ | west | gutters polk city fl | Rain Gutters in Polk City |
| Kathleen | /kathleen-fl/ | west | gutters kathleen fl | Seamless Gutters in Kathleen |
| Highland City | /highland-city-fl/ | west | gutters highland city fl | Rain Gutters in Highland City |
| Mulberry | /mulberry-fl/ | west | gutters mulberry fl | Seamless Gutters in Mulberry |
| Eagle Lake | /eagle-lake-fl/ | west | gutters eagle lake fl | Rain Gutters in Eagle Lake |
| Wahneta | /wahneta-fl/ | west | gutters wahneta fl | Seamless Gutters in Wahneta |
| Davenport | /davenport-fl/ | east | gutters davenport fl | Rain Gutters in Davenport |
| Haines City | /haines-city-fl/ | east | gutters haines city fl | Seamless Gutters in Haines City |
| Lake Alfred | /lake-alfred-fl/ | east | gutters lake alfred fl | Rain Gutters in Lake Alfred |
| Lake Hamilton | /lake-hamilton-fl/ | east | gutters lake hamilton fl | Seamless Gutters in Lake Hamilton |
| Dundee | /dundee-fl/ | east | gutters dundee fl | Rain Gutters in Dundee |
| Lake Wales | /lake-wales-fl/ | east | gutters lake wales fl | Seamless Gutters in Lake Wales |
| Waverly | /waverly-fl/ | east | gutters waverly fl | Rain Gutters in Waverly |
| Frostproof | /frostproof-fl/ | east | gutters frostproof fl | Seamless Gutters in Frostproof |
| Fort Meade | /fort-meade-fl/ | east | gutters fort meade fl | Rain Gutters in Fort Meade |

Note: with the full brand name (settled brand_in_titles), the location titles run 63–69 characters, so the COM-T check (60 or fewer) will
fail on them. The format is settled, so this is a note, not a question.

## 5. About page (1)

- URL: `/about/` (unchanged).
- Title: `About First Choice Seamless Gutters - Gutter Service in Lakeland–Winter Haven`.
- H1: `About [Category variant] in [Area variant]`, using "Gutter Contractor" and "Lakeland–Winter Haven". The about spec format is a Coastal default, so the writer reports the H1 it chooses.
- Content comes from Section D only:
  - Owners Adrian and Rachel Buehl; family owned; base town Lakeland.
  - Insured, with the certificate still [NEED].
  - BBB A+ rating, accredited since 2025.
  - 10-year workmanship guarantee in writing.
  - "Well over 25 years" in business, with the founding year still [NEED].
- Never on this page: "licensed" or "since 2021" (D2).

## 6. "The Best" decisions (CM-020). These go to Brand Guide Section H2 at write-back

- Proof for every page: Google rating 5.0 from 138 reviews, recorded 2026-10-22 (Section D, Internally Verified), which is 4.5+ with 25+ reviews.
- Sensitive industry: no (settled).
- Top-3 lock: no service or location page is in the top 3 for its main keyword. The best is Gutter Cleaning at #15.
- SERPs were pulled 2026-10-24 for Lakeland, FL, 6 calls, $0.012 (`data/rankings/raw/best-serp/`).

| Page | 1 Demand | 2 Opportunity | Decision |
|---|---|---|---|
| Gutter Cleaning | "best gutter cleaning near me" 30/mo | 5 of the top 9 use "best"; our page is not in the top 10 | **Yes** |
| Gutter Guards | "best gutter guards near me" 10/mo | 4 of the top 9 use "best"; our page is not in the top 10 | **Yes** |
| Gutter Installation | "best gutter installation near me" 30/mo | Only 2 of 9 use "best" (Yelp, EcoWatch); not "very competitive", and we do not rank 4–20 | No |
| Gutter Repair | "best gutter repair near me" 10/mo | 2 of 9 use "best"; same as installation | No |
| Other 6 services | No volume for any "best" query | — | No |
| All 19 locations | No volume for "best … <city> fl" | "best gutter installation lakeland fl": 0 of 8 use "best"; Winter Haven: 1 of 9 | No |

Caveat: the "near me" SERPs for cleaning and guards came back with mostly out-of-area results (Jacksonville, SC). They are
national listicle pages, which is why so many titles use "best". Paul may override to No.

## 7. FAQ plan

**Service pages:** 4–6 questions each, all distinct. Each row in the JSON (`faq`) gives the question, its source and why it fits:

| Page | FAQ topics (source) |
|---|---|
| Seamless Gutter Installation | telling if gutters are seamless (PAA #40) · downsides of seamless gutters (#10) · how seamless gutters are made (#38) · highest-rated gutter system (#2) |
| Gutter Installation | when to replace gutters (#41) · cost of new gutters in Florida (#1; #15/#33/#47/#59 merged) · houses without gutters (#39) · DIY install (#12) · how the estimate works (#11) |
| Gutter Repair | repair cost (#13) · most common gutter problem (#24) · handyman or contractor (#14) · repair or replace (coverage) · what routine maintenance includes (folded maintenance scope) |
| Commercial Gutters | commercial-grade gutters (#16) · box versus K-style (coverage) · sizing for large roofs · installation timeline [NEED: client practice] |
| Gutter Downspouts | downspout rule of thumb (#46) · 3x4 downspout on a 5-inch gutter (#17) · alternatives to downspouts (#6) · replacement cost (#18/#45) · where downspouts drain on sandy lots |
| Gutter Guards | downsides (#7) · cost (#21/#49) · leaf guard versus gutter guard (#50) · what roofers say (#53) |
| Gutter Cleaning | cost (#9/#51/#55) · best time of year in Florida (#27/#52/#54) · how often in Polk County (coverage) · signs gutters need cleaning (coverage) · telescopic cleaners (#25) |
| Copper Gutters | lifespan (#30) · worth the cost (#57; #28/#56/#58 merged) · mixing with aluminum (#29) · soldering (#31) |
| Galvalume Gutters | best material for Florida (#32) · versus aluminum or galvanized (#34) · what Galvalume is · rust in humidity |
| Aluminum Gutters | are aluminum gutters good (#35) · .027 versus .032 (#36) · do they rust (coverage) · cost for a home (#37) |

**Location pages:** three questions each, one per category (location-faq.md):
- **1 · Local cost or decision:** HOA, ARB or historic-district limits; lakefront discharge; rural lots.
- **2 · Logistics here:** who issues permits at that address (the city or town building office, or the Polk County Building Division for Kathleen, Highland City, Wahneta and Waverly), and whether gutter work needs a permit at all.
- **3 · Trust here:** local storm, tree and lake conditions, and the client's reach from its Lakeland base.

Every topic marked "verify" or "client facts only" is checked in the facts round. A category that cannot be sourced falls back to
the brand-level local question (Fix and list, never an Ask). The final question wording comes from each page's evidence pack.

**PAA coverage** (`data/paa/paa-routing.md`, 59 questions): 46 are routed to a service FAQ (merged where they are duplicates), 11 are dropped and 2 go to the blog.
- Dropped as off-topic or a competitor brand: #3 and #26 (Lowe's), #20 (Lowe's downspouts), #5 (Home Depot repairs), #19 and #42 (where to buy), #4 (cons of living in Lakeland), #23 (Lakeland phone number).
- Dropped as not Florida: #43 and #48 (ice dams).
- Dropped as contractor-side: #44.
- Blog topics: #8 (worst gutter guards) and #22 (best guard brand).
- No PAA question named a city, so location FAQs come from place research (angle 8).
- The routes are written into the Route column of paa-routing.md, so outline.py offers them as candidates.

**Fan-out:** no `data/fanout/fanout-routing.md` exists for this client, so there is no fan-out coverage to report.

## 8. Plan checks

- **Duplicates:** none. There is one page per service (10, with Maintenance folded) and one per Polk town served (19, with Plant City and Sebring not served).
- **Variant conflicts:**
  - The reserved "Polk County, FL" is not used on any page.
  - **CM-013:** the B2 pool has 3 area variants for 10 service pages. "Variant list exhausted" is recorded as one finding; per CM-024, reuse across pages is correct.
- **Claims in keywords and variants (CM-049):** none. No keyword or variant implies an unconfirmed fact; "licensed", "emergency", "24-hour" and "certified" are absent.
- **FAQ overlap (BB-316, C3):** no question appears on two pages. The C3 registry is empty, since no page is approved yet.
- **Links (CM-064):** the link wheel is built by `wheel.py` and never listed by hand. No CM-022 exceptions are proposed in this plan.
- **Schema:** not part of this step.

## 9. Viability check (location pages)

Ran 2026-10-24: `evidence.py run --all`, then `evidence_pack.py viability --all`.

- **Viable:** Lakeland 5/7 and Winter Haven 5/7.
- **Below the bar:** the other 17 locations scored 2–3/7, so the script marks each one as a merge proposal.

**Recommendation: keep all 19. Do not merge any yet.** These scores do not show that the places cannot be sourced. They show that nobody
has researched them yet:
- The place store (`methodology/places/`) does not exist.
- There is no Florida area source list in `methodology/sources/`.
- No public fact for these towns is logged `not_found` in `research.py`.

Every place is missing the same items: named place entities, the Serving facts, and FAQ categories 1 and 2. All of these are public facts,
and the researcher looks them up in the facts round.

location-faq.md §8 only allows a merge when the public facts are logged `not_found` at the minimum, so a merge would be premature. The check is
re-run after the facts round. Any place still below the bar then comes back to Paul as a kind-1 Ask (merge, with a 301). This is flagged as an ordering
issue: the check ran before the research it depends on.

Evidence gate (for information, not a decision): 29 pages are blocked and About is a warn. This is expected before the facts round. The gaps
are Section D [NEED]s and place facts. The `/build facts` step clears the public facts and sends Paul one question set.

**Link wheel:** `wheel.py plan` wrote 722 rows across 29 pages. `wheel.py check` found 0 errors. `wheel.py asks` produced 0 kind-1 Asks.
