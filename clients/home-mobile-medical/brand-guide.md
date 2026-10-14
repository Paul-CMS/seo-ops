# Home Mobile Medical - Brand Guide
### The single business-truth record. Every agent reads it; the Build agent writes back to it.
Repo working copy: `clients/home-mobile-medical/brand-guide.md` · mirrored to `Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md`

> **Reconciled 2026-10-07 during the import** (run 20261006-112201-new-client-fb9a) from: the v3 Drive Brand Guide
> (Google Doc, 2026-10-02), Client Decision Log 001–038, Client Gap Sheet with owner confirmations, Discovery Record
> (2026-09-28), the claims proof list (`discovery/claims-proof-list.md`, marked by Paul 2026-10-07) and the client's
> answers relayed by Paul on 2026-10-07. Quotes of the live site are from the 2026-09-18 crawl. Approved by Paul
> 2026-10-07 through the import (gate brand_guide_approved).

## Field status values

`Submitted` · `Internally Verified` · `Client Confirmed` · `Disputed` · `Unknown` · `Paul Approved`

**A field at `Unknown` or `Disputed` blocks whatever consumes it.** Writers write
`[NEED: ...]` instead of inventing (CM-016). `Submitted` may appear in a draft but blocks
publication.

**Sensitivity:** health-adjacent (CM-040). Health, safety and coverage claims only with a named authoritative source,
otherwise removed. Paul approves those pages. No practitioner sign-off.

---

## Section A — Entity foundation  *(Paul approves: gate entity_approved)*

| # | Field | Value | Status |
|---|---|---|---|
| 1 | Brand entity (GBP name, exactly) | Home Mobile Medical | Client Confirmed |
| 2 | GBP primary category = the category entity | Mobility equipment supplier (supporting Wikimedia subject: Mobility aid, Q6887300). **Primary category only** — no "Medical equipment supplier" secondary (Paul 2026-10-07) | Paul Approved 2026-10-02 / 2026-10-07 |
| 3 | Category variants (4–6) | Mobility equipment supplier · stair lift installer · stair lift and accessibility lift company · home accessibility lifts · accessibility equipment (grid query language). Excluded: "medical equipment supplier" (broad-DME signal, Decisions 007/038) | Submitted — taken from the Discovery Record's observed variants; the Document Checklist records the variant list as approved 2026-10-02 but the old files never wrote it out |
| 4 | Storefront or SAB | Service-area business. Not customer-facing. The GBP address stays in the site footer only so the site and GBP cross-reference | Client Confirmed; Paul Approved 2026-10-06 |
| 5 | Area entity | South Carolina Lowcountry (Q3885311) | Paul Approved 2026-10-02 |
| 6 | Area variants (3–5) | South Carolina Lowcountry *(reserved)* · the Lowcountry · Beaufort County · Hilton Head Island–Bluffton–Port Royal area · Charleston area | Submitted (see A3 note) |
| 7 | Separator standard | ` - ` | Paul Approved (agency standard) |
| 8 | Phone | (843) 476-1329 | Client Confirmed |
| 9 | Primary domain (canonical host form) | https://homemobilemedical.com/ | Internally Verified (crawl 2026-09-18) |
| 10 | Legal entity name | Home Mobile Medical | Paul Approved 2026-10-07 (no SC Secretary of State record located) |
| 11 | Exact URL in the GBP Website field | https://homemobilemedical.com/ | Paul Approved 2026-09-28 |

**Area entity derivation** (BB-105):

```
City served:   24 South Carolina towns (Section E), anchors Charleston, Hilton Head Island, Beaufort, Hollywood, Walterboro
-> County:     Beaufort, Jasper, Charleston, Berkeley, Dorchester, Colleton, Hampton
-> Region:     South Carolina Lowcountry
Contains all 24 cities served? yes
Smallest true container: South Carolina Lowcountry
Georgia is served from a separate microsite (own project), so it is outside this site's area entity.
```

**Paul approved this section on:** 2026-10-02 (old workflow, Phase 4b) · category scope narrowed 2026-10-07 · gate signed at import: 2026-10-07 (Paul)

## Section B — Variant ownership  *(CM-024: collisions are vertical, not horizontal)*

### B1 · Reserved for the homepage
```
HOMEPAGE AREA VARIANT:      South Carolina Lowcountry [Paul Approved 2026-10-02]
HOMEPAGE CATEGORY VARIANT:  Mobility equipment supplier [Paul Approved 2026-10-02]
```
No other page may claim the reserved area variant. This is the only cross-page variant rule.

### B2 · Rotation pool
```
1. the Lowcountry
2. Beaufort County
3. Hilton Head Island–Bluffton–Port Royal area
4. Charleston area
```

### B3 · Assignment log — the write-back target
| Page URL | Page type | Category variant | Area variant | Content file (SD/LD) | Shipped |
|---|---|---|---|---|---|
| / | homepage | | *(reserved)* | | |
| /stair-lifts/ | service | stair lift installer (opening also: Beaufort County) | the Lowcountry (H1) | SB - Stair Lifts - Home Mobile Medical (build/pilot/briefs/) | |
| /beaufort-sc/ | location | stair lift installer (H1); opening also: stair lift and accessibility lift company, home accessibility lifts | Beaufort County (opening) | LB - Beaufort SC - Home Mobile Medical (build/pilot/briefs/) | |

Pilot rows written back 2026-10-14 (run 20261014-133132-build-f0c5) from the approved pilot briefs. The pre-seo-ops build files were lost (Paul 2026-10-06).

## Section C — Page inventory

### C0 · Page order (from the URL Decision Map)
Set by the site plan in Build. Source map: `Home Mobile Medical - URL Decision Map` (Google Sheet, older TMS folder), amended by Paul's 2026-10-06/07 decisions.

### C1 · Service pages
| URL | Service name | H1 service variant | Status |
|---|---|---|---|
| /services/ | Services hub | | Planned (rewrite) |
| /stair-lifts/ (replaces /services/stair-lifts/, 301) | Stair lifts — parent; straight stair lifts consolidated in · keyword "stair lifts" | stair lift installation (H1 "Stair Lift Installation in the Lowcountry"; no "The Best") | Brief approved 2026-10-14 (pilot) |
| /services/curved-stair-lifts/ | Curved stair lifts | | Planned (rewrite) |
| /services/porch-lifts/ | Porch lifts / vertical platform lifts (the outdoor offer) | | Planned (rewrite) |
| /services/wheelchair-lifts/ | Wheelchair lifts | | Planned (rewrite) |
| /services/straight-stair-lifts/ | → consolidated into /services/stair-lifts/ (301 after the CM-019 check) | | Planned |
| repair and maintenance | Stair-lift and lift repair and maintenance — page/URL decided in the site plan (existing: /hilton-head/stair-lift-repair/, /bluffton-sc/wheelchair-lift-repair/) | | Planned |

Parent/child service pages with real subtype demand keep their URLs (Paul). Service pages share one area entity.

### C2 · Location pages
Canonical pattern `/service-area/{city-state}/` (Decision 023). Hubs: `/service-area/` (Lowcountry) · `/service-area/charleston/` (Charleston metro area) · `/service-area/hhi-beaufort/` (Hilton Head Island–Bluffton–Port Royal metro area) — metro hubs pending L-008 and the county-hub spec. Merged location pages become mentions, not sections.

| URL | City | GBP landing page? | Status |
|---|---|---|---|
| /beaufort-sc/ (replaces /service-area/beaufort-sc/, 301) | Beaufort | No (GBP lands on the homepage) | Brief approved 2026-10-14 (pilot) · keyword "stair lifts Beaufort SC" · H1 "Stair Lift Installer in Beaufort" · area variant Beaufort County · category variant stair lift installer |
| /service-area/bluffton-sc/ | Bluffton | No | Planned |
| /service-area/hilton-head-island-sc/ | Hilton Head Island | No | Planned |
| /service-area/port-royal-sc/ | Port Royal | No | Planned |
| /service-area/ladys-island-sc/ | Lady's Island | No | Planned |
| /service-area/laurel-bay-sc/ | Laurel Bay | No | Planned |
| /service-area/daufuskie-island-sc/ | Daufuskie Island | No | Planned |
| /service-area/okatie-sc/ | Okatie | No | Planned |
| /service-area/yemassee-sc/ | Yemassee | No | Planned |
| /service-area/hardeeville-sc/ | Hardeeville | No | Planned |
| /service-area/ridgeland-sc/ | Ridgeland | No | Planned |
| /service-area/levy-sc/ | Levy | No | Planned |
| /service-area/walterboro-sc/ | Walterboro | No | Planned |
| /service-area/edisto-island-sc/ | Edisto Island | No | Planned |
| /service-area/charleston-sc/ | Charleston | No | Planned |
| /service-area/north-charleston-sc/ | North Charleston | No | Planned |
| /service-area/mount-pleasant-sc/ | Mount Pleasant | No | Planned |
| /service-area/summerville-sc/ | Summerville | No | Planned |
| /service-area/goose-creek-sc/ | Goose Creek | No | Planned |
| /service-area/hanahan-sc/ | Hanahan | No | Planned |
| /service-area/moncks-corner-sc/ | Moncks Corner | No | Planned |
| /service-area/hollywood-sc/ | Hollywood | No | Planned |
| /service-area/kiawah-island-sc/ | Kiawah Island | No | Planned |
| /service-area/folly-island-sc/ | Folly Island | No | Planned |

Only a verified GBP's actual landing URL gets LocalBusiness-type schema (BB-604).

### C3 · Heading and FAQ registry
Filled from the site plan and each approved page.

| Question or H2 | Page that owns it |
|---|---|
| H2: How Does a Stair Lift Go From Quote to Working Lift? | /stair-lifts/ |
| H2: What Types of Stair Lifts and Stair Lift Services Are Available? | /stair-lifts/ |
| H3: Straight Stair Lifts | /stair-lifts/ |
| H3: Curved Stair Lifts (summary; detail on the curved page) | /stair-lifts/ |
| H3: Stair Lift Maintenance and Repair (summary; detail on the repair page) | /stair-lifts/ |
| H3: Stair Lift Brands | /stair-lifts/ |
| H2: What Do People Ask About Stair Lifts? | /stair-lifts/ |
| FAQ: How Much Does a Stair Lift Cost? | /stair-lifts/ |
| FAQ: Who Makes Stair Lifts? | /stair-lifts/ |
| FAQ: How Long Does It Take to Install a Stair Lift? | /stair-lifts/ |
| FAQ: Can I Get a Stair Lift Quote From a Photo? | /stair-lifts/ |
| FAQ: What Is the Difference Between Straight and Curved Stair Lifts? | /stair-lifts/ |
| H2: Where Does Home Mobile Medical Install Stair Lifts? | /stair-lifts/ |
| H2: Accessibility Lift Services in Beaufort | /beaufort-sc/ |
| H2: Beaufort's Older Homes and Marshland Setting | /beaufort-sc/ |
| H2: Serving Beaufort | /beaufort-sc/ |
| H2: Beaufort Stair Lift Questions | /beaufort-sc/ |
| FAQ: How much does a stair lift cost in Beaufort? | /beaufort-sc/ |
| FAQ: Do I need a permit for a lift in Beaufort? | /beaufort-sc/ |
| FAQ: Is Home Mobile Medical the same company as Beaufort Medical Equipment? | /beaufort-sc/ |
| H2: Beaufort Neighborhoods | /beaufort-sc/ |

## Section D — Verified facts
Everything a writer may state. **Not here = does not exist.**

| Fact | Value | Status | Source |
|---|---|---|---|
| Founding year / years in business | 15+ years of **Jason Workens' experience** — never the brand's age (a directory says the business opened 2023) | Client Confirmed | Decision 013 |
| History | Jason's former company, Beaufort Medical Equipment, was sold; Home Mobile Medical is not a rebrand of it | Client Confirmed | Decision 003 |
| Ownership | Family-owned; locally owned and operated | Client Confirmed | Decision 014; Paul 2026-10-07 |
| Legal entity + DBA | Home Mobile Medical; no DBA known | Paul Approved | Paul 2026-10-07 |
| Licence numbers and classes | None to publish | Paul Approved | Paul 2026-10-07 (none found) |
| Insurance / bonded status | None to publish | Paul Approved | Paul 2026-10-07 |
| Certifications, authorizations, factory training | None. No authorized/certified-dealer wording for any brand | Paul Approved | Paul 2026-10-07 |
| Brands installed and repaired | "We install and repair stair lifts from leading brands such as Stannah, Bruno and Harmar." Independent; no authorized/certified-dealer wording | Paul Approved | Paul 2026-10-07 |
| Association memberships | None known | Unknown | |
| Warranty terms | Manufacturer's warranty only; no Home Mobile Medical warranty | Client Confirmed | Paul 2026-10-07 |
| Guarantees | None | Client Confirmed | |
| Awards and rankings | None | Unknown | |
| Google rating and review count (date checked) | 2.9 stars from 19 Google reviews (checked 2026-10-08) | Internally Verified 2026-10-14 · was: Unknown | DataforSEO Google reviews pull 2026-10-08 (data/reviews/raw/reviews.json); reviews.csv 19 rows, 2017-04-02 to 2023-03-23 |
| Team size / trucks / jobs completed | Jason plus one helper. Jason personally supervises every installation | Client Confirmed | Paul 2026-10-07; Decision 015 |
| Installation time | Usually one day, about 3–4 hours; same-day installation **in most cases** | Client Confirmed | Paul 2026-10-07; Decision 016 |
| Financing — available, provider, terms | Available. No provider, rates or terms published | Client Confirmed | Decision 017 |
| Free estimate — and what free means | Free in-home estimate. Can also quote from a photo of the stairs (priced by stair count) | Client Confirmed | Paul 2026-10-07 |
| Services | Straight stair lifts · curved stair lifts · porch lifts / vertical platform lifts (outdoor access for raised entrances and decks) · wheelchair lifts · professional installation · sourcing new lifts for customers · maintenance · repairs (any stair lift or lift within the service coverage, any brand) | Client Confirmed | Decision 005; Paul 2026-10-07 |
| Not offered | Broad DME, rentals, hospital beds, power chairs, scooters, scooter lifts, scooter repair, lift chairs, mobility ramps, general wheelchairs; HMM is not a manufacturer | Client Confirmed | Decisions 007, 008, 018 |
| Safety statement | "Safety comes first. Jason holds every installation to the highest industry standards and the manufacturer's installation instructions." | Paul Approved | Paul 2026-10-07 |
| Email | info@homemobilemedical.com | Client Confirmed | Paul 2026-10-07 |
| Hours | Monday–Friday 9:00 AM–5:00 PM; Saturday–Sunday closed | Client Confirmed | Paul 2026-10-07 |
| Emergency / after-hours reality | Office hours are Monday–Friday 9 AM–5 PM. True emergencies are handled after hours. Urgent calls that are not emergencies are scheduled as soon as possible. After-hours availability depends on current demand. Use general terms only; do not promise a specific after-hours response. | Client Confirmed | Facts interview 2026-10-14, owner reply Q2 (general terms only) |
| Minimum service call or trip charge | None. No service-call or trip charge. | Client Confirmed | Facts interview 2026-10-14, owner reply Q1 |
| Payment methods | General wording only ("we accept common payment methods"); no specific list | Paul Approved | Paul 2026-10-07 |
| Services subcontracted out | None known | Unknown | |
| Named staff for on-page use | Jason Workens, founder/owner | Client Confirmed | Paul 2026-10-07 |
| Licensed practitioner for health-claim sign-off | Not required (health-adjacent, CM-040) | Paul Approved | |
| Repair process: steps and charge | When someone calls about a broken stair lift or lift: first call, visit, diagnosis, quote, parts, fix. No service-call or trip charge. Repairs any stair lift or lift, any brand, within the service area. | Client Confirmed | Facts interview 2026-10-14, owner reply Q1; website wording allowed (yes) |
| Install time: curved, porch and wheelchair lifts | The installation itself is quick for curved, porch and wheelchair lifts, the same as stair lifts. More than one installation can be done in a day, so the schedule is adjusted to fit. | Client Confirmed | Facts interview 2026-10-14, owner reply Q3 (partial) |
| Order-to-installed lead time; pad and permit for porch and wheelchair lifts | [NEED] Order-to-installed lead time for curved, porch and wheelchair lifts. [NEED] Who handles the concrete pad and building permit for porch and wheelchair lifts (you, the customer, or it depends). | Unknown | Facts interview 2026-10-14, owner reply Q3: not answered |

### D2 · Unsupported claims
| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|
| "We rent and sell mobility equipment in the Lowcountry." | /service-area/beaufort-sc/ | False — rentals discontinued | Remove |
| "Safety is our top priority, and we adhere to the highest standards and regulations." | / | "Regulations" unsupported | Replace with the Section D safety statement |
| "…installation meets the highest standards of safety and care." | /service-area/beaufort-sc/ | As above | Replace with the Section D safety statement |
| "Every lift is custom-fit to your staircase…" | /service-area/beaufort-sc/ | Not true of every unit | "fitted to your staircase" |
| "All of our stair lifts come with battery backup systems…" | /service-area/beaufort-sc/ | Product spec, unproven | Remove "all" unless manufacturer spec sheets cover every model sold |
| "…ready for safe use the same day it is installed." | /service-area/beaufort-sc/ | Same day in most cases | Add "in most cases" |
| "Our experienced technicians…" / "skilled professionals" | / | Jason plus one helper | "Jason and his helper" |
| Homepage testimonials (Debbie S, Laura B, Sher D) | / | Placeholder reviews | Remove |
| 106 Arrow Road, Hilton Head, SC 29928 | Directions link; Beaufort page closing copy | Not the business address | Remove |
| Medicare / Medicaid / insurance, tax, ADA, product-spec statements | Blog posts | Kept until the Blog Decision Map | Rewrite only from Medicare.gov/CMS, IRS Pub 502, ADA.gov, manufacturer spec sheets |
| Stannah "verified dealer" | Old Brand Guide | No evidence on record | Use only in the general brand line, never as dealer status |

## Section E — Service area truth
```
FURTHEST NORTH:   Moncks Corner          FURTHEST SOUTH:  Daufuskie Island
FURTHEST EAST:    Mount Pleasant         FURTHEST WEST:   Yemassee
CITIES CLAIMED ON SITE: the 24 South Carolina towns in C2 — all confirmed served (Paul 2026-10-07)
EXPLICIT EXCLUSIONS: Florida, Michigan (not served; pages dropped, 301). Georgia is served only through a separate microsite, never on this site.
TRAVEL FEE BEYOND: [NEED]
```
(Bounds derived from the confirmed city list.)

## Section F — Schema inputs  *(Block 3 cannot open without these)*

| Asset | Value | Status |
|---|---|---|
| ID page URL (becomes the business entity @id) | [NEED: decide — About page or a new ID page] | Unknown — deferred to Finish (Paul 2026-10-07) |
| Full citation list → sameAs | Facebook, Bing, Yelp, Storeboard, Chamber of Commerce, Hotfrog, Tupalo (BrightLocal 2026-09-28) — URLs to collect; Beaufort Medical Equipment listings excluded | Internally Verified (list), URLs Unknown |
| Social profile list | https://www.facebook.com/homemobilemed · https://www.instagram.com/homemobilemedical/ | Internally Verified |
| Google Maps share link → hasMap | https://maps.app.goo.gl/6A4wAczgy3A7w9Lu7 | Paul Approved |
| Apple Maps link → sameAs | [NEED] | Unknown — deferred to Finish (Paul 2026-10-07) |
| Confirmed NAP exactly as it must appear | Home Mobile Medical · 2127 Boundary St #5, Beaufort, SC 29902 · (843) 476-1329 | Paul Approved 2026-10-06 |
| Confirmed GBP category → schema subtype | Mobility equipment supplier → subtype chosen in Finish (bb-schema-builder) | Paul Approved |
| Logo files with pixel dimensions | [NEED] | Unknown — deferred to Finish (Paul 2026-10-07) |
| Owner name + photo | Jason Workens; photo [NEED] | Name Client Confirmed |
| **Wikidata URI — category entity** | https://www.wikidata.org/wiki/Q6887300 (Mobility aid, supporting subject) | Internally Verified |
| **Wikidata URI — area entity** | https://www.wikidata.org/wiki/Q3885311 | Paul Approved |
| **Wikidata URI — county** (one per county the area entity covers) | Beaufort County https://www.wikidata.org/wiki/Q495682 · Jasper, Charleston, Berkeley, Dorchester, Colleton, Hampton [NEED: look up] | Partly verified |
| **Wikidata URI — state** | https://www.wikidata.org/wiki/Q1456 | Internally Verified |

## Section G — Positioning (client's own words)
```
WHAT WE DO THAT OTHERS HERE DO NOT: Jason installs every lift himself; most installs take one day, about 3–4 hours; quotes from a photo of your stairs. [Submitted — relayed by Paul, not yet in the client's own words]
JOB WE MOST WANT MORE OF: [NEED]
MOST COMMON THING CUSTOMERS GET WRONG ABOUT THIS TRADE: [NEED]
```

## Section H — Constraints, exceptions and the superlative opener

| Type | Detail | Approved by | Exit condition |
|---|---|---|---|
| Client constraint | Georgia lives on a separate microsite; nothing on this site targets Georgia | Paul 2026-10-06/07 | Paul reverses it |
| Client constraint | Destructive URL actions are 301s (never 410s), each after the CM-019 DataforSEO check; DataforSEO replaces Search Console | Paul 2026-10-06 | — |
| Client constraint | Medicare/tax/ADA/product blog posts stay as they are until the Blog Decision Map | Paul 2026-10-07 | Blog Decision Map approved |
| Client constraint | Site feature wanted: photo upload so Jason can quote by phone | Client via Paul 2026-10-07 | Built (Jonie handoff in Build) |
| Paul Exception | None | | |

### H2 · "The Best" decisions (CM-020) — conditional, never a default
| Page | Main keyword & current rank | 1 Demand | 2 Opportunity | 3 Proof (Section D fact) | 4 Not sensitive / Paul OK | Top-3 lock? | Decision | Evidence locator |
|---|---|---|---|---|---|---|---|---|

## Section I — Customer language
| Source | Location | Captured |
|---|---|---|
| None yet — the homepage reviews were placeholders | — | — |

## Maintenance

| When | Action |
|---|---|
| Page content approved (SD/LD) | Add its row to B3 and C1/C2, its FAQ questions and H2s to C3 |
| New citation built | Add to Section F and sameAs |
| GBP primary category changes | Rebuild Sections A and B — entity gate re-opens |
| Any field moves status | Update in place. Never keep two versions |
