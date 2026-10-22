# First Choice Seamless Gutters - Discovery Record - REVIEW

Run `20261022-084632-discovery-42fd` · 2026-10-22 · steps S01–S03 · public sources only (no crawl yet).
Observations and questions only — no severity, priorities or recommendations (those belong to the audit).
Confidence: `verified` (government / authoritative third party) · `found` (the business states it) · `inferred` ·
`unknown` (checked, nothing found). Every fact is in `facts.json` (`facts.py get first-choice-seamless-gutters --ids …`).

## 1 · Sources read

| # | Source | URL | Read | Result |
|---|---|---|---|---|
| 1 | Website (home, about, areas, contact, sitemaps) | https://www.firstchoiceseamlessgutters.net/ | 2026-10-22 | read |
| 2 | Google Business Profile (public business page + reviews) | https://business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_ | 2026-10-22 | read (10 newest reviews visible) |
| 3 | Google Maps place links (intake link + 2 site footer links) | maps.app.goo.gl/c5prGD6rMCwptG3x6 · /ccL5rnpD3uyDpunG9 · /snPL4u1dYc5QaWL99 | 2026-10-22 | all resolve to the same place (CID 0xcb9c83deacccb627) |
| 4 | BBB | https://www.bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573 | 2026-10-22 | read |
| 5 | Press release (MarketersMedia via FinancialContent) | https://markets.financialcontent.com/chroniclejournal/article/marketersmedia-2025-12-3-first-choice-seamless-gutters-named-best-gutter-installer-in-lakeland-florida | 2026-10-22 | read |
| 6 | Florida Sunbiz (Division of Corporations) | https://search.sunbiz.org/ | 2026-10-22 | **blocked (HTTP 403)** → Gwen manual_lookup |
| 7 | Yelp | https://www.yelp.com/biz/first-choice-seamless-gutters-winter-haven | 2026-10-22 | **blocked (403)** → Gwen |
| 8 | Facebook | https://www.facebook.com/people/First-Choice-Seamless-Gutters-INC/100077007987844/ | 2026-10-22 | name only (login wall) → Gwen |
| 9 | HomeAdvisor | homeadvisor.com (search snippet only) | 2026-10-22 | **blocked (403)**; snippet shows "1575 Lemon Ave", "4 years of experience" → Gwen |
| 10 | Licence: FL DBPR / Polk County contractor licensing | myfloridalicense.com · polkfl.gov | 2026-10-22 | not determined (form-based search) → Gwen |
| 11 | Wikipedia / Wikidata | Rain gutter (Q152833) · Polk County, Florida (Q501043) · Central Florida (Q2920358) · Florida (Q812) | 2026-10-22 | read |

## 2 · Identity (NAP)

| Field | Candidate values (verbatim) | Source | Confidence |
|---|---|---|---|
| Name | "First Choice Seamless Gutters Inc." | GBP; site schema `name` | found (GBP = what Google shows) |
| Name | "First Choice Seamless Gutters" (alt: "First Choice Seamless Gutters Inc.") | BBB | found |
| Name | "First Choice Seamless Gutter Inc provides the ultimate in home protection…" (singular "Gutter") | site homepage body | found |
| Entity | "Type of Entity: Corporation" · "Business Incorporated: 11/24/2021" · "Business Started: 11/24/2021" | BBB | found (Sunbiz not read) |
| Owners | "Adrian Buehl, Owner" · "Rachel Buehl, Owner" | BBB | found |
| Phone | "(863) 330-3243" | site header/footer, GBP, schema `+1 863-330-3243` | found, consistent |
| Phone | "(863) 320-2842" — listed as "Other Phone" | BBB | found — **conflict / second number** |
| Base town | "Based in Lakeland, FL" (hero) | site homepage | found |
| Base town | "Based in Winter Haven, our gutter company…" | site homepage (2nd section) | found — **conflict** |
| Base town | "Winter Haven, FL 33881" | BBB; Yelp slug `winter-haven` | found |
| Street address | schema `"streetAddress":"3517 Century Blvd","addressLocality":"Lakeland","postalCode":"33811"`, geo 28.0319, -81.9376 | site LocalBusiness JSON-LD | found (not displayed on page) |
| Street address | "3517 Cuntury Blvd., Lakeland, FL 33811" (as printed) | press release contact block | found |
| Street address | "1575 Lemon Ave" | HomeAdvisor search snippet | found (unconfirmed — page blocked) |
| Street address | none shown; GBP lists a service area | GBP; Paul intake: SAB | found |
| GBP pin | 27.8138615, -81.800041 (south-central Polk, Bartow area) | Maps place data | inferred |
| Hours | "7 AM–8 PM" Mon–Sun | GBP | found |
| Hours | schema 07:00–20:00 daily, except Wednesday `"opens":"00:00:00"` | site JSON-LD | found (observation) |
| Hours | "Available 7 Days a Week" | site | found |
| Domain | https://www.firstchoiceseamlessgutters.net/ — non-www 301 → www; canonical www | live HTTP check | verified (technical) |
| GBP Website field | Paul intake: `https://firstchoiceseamlessgutters.net/` (non-www); GBP posts link `https://www.firstchoiceseamlessgutters.net/` | intake; GBP | **unconfirmed** → Gwen |

## 3 · Category and services

- GBP primary category: Maps place data carries category id `gutter_service` (public display "Gutter service"); Paul's intake
  says "Seamless gutters". **Conflict, recorded not resolved (PROC-01).** Secondary categories not visible publicly → Gwen.
- BBB categories: "Gutter Contractors, Gutters, Gutter Cleaning, Gutter Guards, Gutter Installation".
- GBP services visible: "Seamless Gutter Installation", "Gutter Guard Installation".
- Site service pages (11): Seamless Gutter Installation · Gutter Installation · Gutter Repair · Commercial Gutters · Gutter
  Downspouts · Gutter Guards · Gutter Maintenance · Gutter Cleaning · Copper Gutters · Galvalume Gutters · Aluminum Gutters
  (all under `/services/`). Site: "We work only with gutters".
- Blog: post sitemap lists 2 posts — `/gutter-guards-winter-haven-fl/`, `/gutter-services-lakeland-fl/`.
- Wikipedia category entity: **Rain gutter** (Q152833) — "A rain gutter, eavestrough, eaves-shoot or surface water collection
  channel…"; the article describes seamless gutters ("produced on site with a portable roll forming machine") and gutter guards.

## 4 · Service area

| Source | Towns |
|---|---|
| Site `/areas-we-serve/` (20, each with a page `/areas-we-serve/<town>-fl/`) | Auburndale, Bartow, Eagle Lake, Fort Meade, Highland City, Kathleen, Lake Wales, Lakeland, Polk City, Wahneta, Davenport, Dundee, Frostproof, Haines City, Lake Alfred, Lake Hamilton, Mulberry, Plant City, Waverly, Winter Haven |
| GBP "Location" block (15) | Bartow, Dundee, Sebring, Waverly, Lakeland, Davenport, Auburndale, Eagle Lake, Lake Wales, Plant City, Haines City, Lake Alfred, Winter Haven, Polk City, Lakeland Highlands |
| GBP About | "We service all of Polk County!" |
| Site footer | "Proudly Serving Polk County, Florida" |

- On GBP, not on site: Sebring (Highlands County), Lakeland Highlands (Polk CDP).
- On site, not on GBP: Fort Meade, Highland City, Kathleen, Wahneta, Frostproof, Lake Hamilton, Mulberry.
- Outside Polk County: Plant City (Hillsborough — site and GBP), Sebring (Highlands — GBP only).
- Reviews read (10 visible on GBP) name no towns.

## 5 · Entity foundation (S03) — proposals for Paul

Category entity: GBP primary category (pending the conflict above) ↔ Wikipedia **Rain gutter** (Q152833).
Area entity (BB-105, BB-110 — SAB → the containing metro): Winter Haven → **Polk County, Florida** (Q501043) → "Polk County
comprises the Lakeland–Winter Haven metropolitan statistical area (MSA)." The MSA is the county itself. It contains 19 of
the 20 site towns; Plant City and Sebring are outside it. Next container up: **Central Florida** (Q2920358) — its "usual"
13-county definition includes Polk and Hillsborough, not Highlands; Wikipedia notes the name is increasingly used for the
Orlando area. State: Florida (Q812). The full path is in Brand Guide §A; the choices are on the Decision Sheet.

## 6 · Claims on the site (for Brand Guide D / the proof sheet)

| Claim (verbatim) | Where | Third-party support found |
|---|---|---|
| "backed by a 10-Year Workmanship Guarantee" / "10-Year Workmanship Warranty" | home | none (terms not published) |
| "We’re fully licensed and insured" | home | none — no licence number anywhere; BBB "Licensing: not listed" |
| "Family Owned & Operated" / "As a family owned and operated company" | home, about | BBB lists two owners sharing a surname (inference only) |
| "BBB A+ Accredited" / "We are an accredited business with the Better Business Bureau." | home | BBB: A+, accredited 8/12/2025 — supported |
| "95+ 5 Star Google Reviews" | home | GBP shows "5 out of 5 (138 reviews)" on 2026-10-22 — figure on site is out of date |
| "Fast Response Times" · "we’ll contact you within 24 hours" | home, contact | none |
| "$150 off full house installations for Military & Seniors" | home | none |
| "free, no-obligation estimate" · "Free On-Site Inspection & Estimate" | home, contact | GBP About: "free estimate" |
| "named the Best Gutter Installer in Lakeland, Florida by GutterPro HQ for 2025" | press release (not on site) | company-distributed release only |
| "bbc accredited" (heading typo for BBB) | home | observation |

## 7 · Reviews (GBP, 10 visible of 138)

Staff named: Adrian (×2, plus 2 on the site), April, Matt, Isaac, James. Services named: new gutters, downspouts, leaf
guards (site testimonial), HOA coordination/approval (×2). One negative review (Kerry Gregory, edited ~4 months ago):
"Dont drain properly, wasn't installed correctly." Owner responses not visible. Full review export comes with the data step.

## 8 · Questions this record raises (client-only; go to the proof sheet, not asked here)

Set: `discovery/discovery-questions.json` (settled.py filter + questions.py check passed; the phone question was dropped
as answered — (863) 330-3243 agrees across site, GBP and schema; the BBB "Other Phone" stays an observation for the audit).

1. (dropped — answered)
2. Base town: Lakeland or Winter Haven? Is 3517 Century Blvd, Lakeland 33811 (schema, press release) or 1575 Lemon Ave
   (HomeAdvisor) a real business address, a home, or a mail drop?
3. Plant City and Sebring — served regularly? (both outside Polk County)
4. Licence: which licence (state or Polk County competency card) and its number; insurance carrier.
5. 10-year workmanship warranty terms; family-owned (who); response-time claim; Military & Seniors discount still running.
6. Founding date: is 11/24/2021 (BBB) the start of trading?

## 9 · Manual lookups (Gwen, one handoff)

Sunbiz entity record · FL DBPR licence search · Polk County contractor licence · GBP dashboard (primary + secondary
categories, service areas, open date, Website field) · Yelp · Facebook About · HomeAdvisor profile. See the run's
`manual_lookup` handoff. Until returned, these fields keep their public-copy confidence (never verified).
