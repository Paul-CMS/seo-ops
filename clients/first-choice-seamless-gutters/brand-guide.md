# First Choice Seamless Gutters - Brand Guide
### The single business-truth record. Every agent reads it; the Build agent writes back to it.
Repo working copy: `clients/<slug>/brand-guide.md` · mirrored to `[Client Name] - TMS/[Client Name] - Brand Guide.md`

## Field status values

`Submitted` · `Internally Verified` · `Client Confirmed` · `Disputed` · `Unknown` · `Paul Approved`

**A field at `Unknown` or `Disputed` blocks whatever consumes it.** Writers write
`[NEED: ...]` instead of inventing (CM-016). `Submitted` may appear in a draft but blocks
publication.

---

## Section A — Entity foundation  *(Paul approves: gate entity_approved)*

| # | Field | Value | Status |
|---|---|---|---|
| 1 | Brand entity (GBP name, exactly) | First Choice Seamless Gutters Inc. | Internally Verified 2026-10-22 · was: Submitted |
| 2 | GBP primary category = the category entity | CONFLICT (PROC-01): Paul intake 'Seamless gutters' · Google Maps place data category id 'gutter_service' (display 'Gutter service') — dashboard check pending (Gwen manual_lookup) | Disputed 2026-10-22 · was: Submitted |
| 3 | Category variants (4–6) | Proposed: Gutter Service · Seamless Gutters · Rain Gutters · Gutter Contractor · Gutter Installation (Wikipedia entity: Rain gutter, Q152833) | Submitted 2026-10-22 · was: Unknown |
| 4 | Storefront or SAB | Service area business (travels to customers) | Submitted 2026-10-22 · was: Unknown |
| 5 | Area entity | Proposed: Polk County, Florida = Lakeland–Winter Haven MSA (Q501043). Path: Winter Haven → Polk County → 'comprises the Lakeland–Winter Haven metropolitan statistical area'. Contains 19 of 20 site towns; outliers Plant City (Hillsborough) and Sebring (Highlands, GBP only) | Submitted 2026-10-22 · was: Unknown |
| 6 | Area variants (3–5) | Proposed: Polk County, FL · Polk County, Florida · Lakeland–Winter Haven · Lakeland–Winter Haven metropolitan area | Submitted 2026-10-22 · was: Unknown |
| 7 | Separator standard | ` - ` | |
| 8 | Phone | (863) 330-3243 (site, GBP, schema agree; BBB also lists 'Other Phone' (863) 320-2842) | Internally Verified 2026-10-22 · was: Unknown |
| 9 | Primary domain (canonical host form) | https://www.firstchoiceseamlessgutters.net/ (non-www 301 → www; canonical tag www) | Internally Verified 2026-10-22 · was: Submitted |
| 10 | Legal entity name | First Choice Seamless Gutters Inc. (BBB: Corporation, incorporated 11/24/2021) — Sunbiz record not read (403), Gwen manual_lookup | Submitted 2026-10-22 · was: Unknown |
| 11 | Exact URL in the GBP Website field | https://firstchoiceseamlessgutters.net/ | Submitted 2026-10-22 · was: Unknown |

**Area entity derivation** (BB-105) — record the path, not just the answer:

```
City served: Winter Haven, FL (Q1778769) — "Based in Winter Haven" (site); BBB Winter Haven, FL 33881
-> County: Polk County, Florida (Q501043) — "Polk County comprises the Lakeland–Winter Haven metropolitan statistical area (MSA)." (Wikipedia)
-> Region: Lakeland–Winter Haven MSA (= Polk County exactly; Wikipedia redirects the MSA to the county);
   next level up: Central Florida (Q2920358), the "usual" 13-county definition incl. Polk and Hillsborough, not Highlands
Contains all N cities served? Site lists 20 towns: 19 in Polk; Plant City is in Hillsborough County (Tampa Bay area).
   GBP "Location" list (15) adds Sebring (Highlands County) and Lakeland Highlands (Polk). -> no, 2 outliers
Smallest true container: Polk County / Lakeland–Winter Haven MSA for every Polk town (PROPOSED — Decision Sheet
   area_entity; Plant City and Sebring go to the client as towns_served questions). Central Florida would contain
   Plant City but not Sebring. State: Florida (Q812). PROPOSAL — Paul decides (agency profile §4).
```

**Paul approved this section on:** ____________

## Section B — Variant ownership  *(CM-024: collisions are vertical, not horizontal)*

### B1 · Reserved for the homepage
```
HOMEPAGE AREA VARIANT:      Polk County, FL          [Submitted 2026-10-22 — proposal, Decision Sheet homepage_title_variant]
HOMEPAGE CATEGORY VARIANT:  Gutter Service           [Submitted 2026-10-22 — proposal; waits on the GBP primary category conflict]
```
Homepage H1 area variant (proposal, Decision Sheet homepage_h1_variant): Lakeland–Winter Haven.
No other page may claim the reserved area variant. This is the only cross-page variant rule.

### B2 · Rotation pool
Every area variant except the reserved one. Reuse across service pages is correct.
```
1. Polk County, Florida                         [Submitted 2026-10-22 — proposal]
2. Lakeland–Winter Haven                        [Submitted 2026-10-22 — proposal]
3. Lakeland–Winter Haven metropolitan area      [Submitted 2026-10-22 — proposal]
4.
```

### B3 · Assignment log — the write-back target
| Page URL | Page type | Category variant | Area variant | Content file (SD/LD) | Shipped |
|---|---|---|---|---|---|
| / | homepage | | *(reserved)* | | |

## Section C — Page inventory

### C0 · Page order (from the URL Decision Map)
| Order | Plan no. | Page | Type | Final URL |
|---|---|---|---|---|

### C1 · Service pages
| URL | Service name | H1 service variant | Status |
|---|---|---|---|

### C2 · Location pages
| URL | City | GBP landing page? | Status |
|---|---|---|---|

Only a verified GBP's actual landing URL gets LocalBusiness-type schema (BB-604).

### C3 · Heading and FAQ registry
Every FAQ question and H2 live on the site, with the page that owns it. No question on two pages (BB-316).

| Question or H2 | Page that owns it |
|---|---|

## Section D — Verified facts
Everything a writer may state. **Not here = does not exist.**

| Fact | Value | Status | Source |
|---|---|---|---|
| Founding year / years in business | Business started 11/24/2021 per BBB (self-reported to BBB); site gives no year | Submitted 2026-10-22 · was: Unknown | BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026-10-22 — "Business Started: 11/24/2021" |
| Legal entity + DBA | First Choice Seamless Gutters Inc.; BBB primary name 'First Choice Seamless Gutters'; site also 'First Choice Seamless Gutter Inc' | Submitted 2026-10-22 · was: Unknown | BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026-10-22; firstchoiceseamlessgutters.net homepage, read 2026-10-22 — "First Choice Seamless Gutter Inc provides the ultimate in home protection" |
| Licence numbers and classes | [NEED: licence number and class — site claims licensed, no number shown; Paul has none; asked on the proof sheet; state/Polk County lookup pending] | Unknown 2026-10-22 | searched: site, BBB (licensing not listed), web search 2026-10-22; Paul 2026-10-22: none provided — "We’re fully licensed and insured" |
| Insurance / bonded status | Site claims 'fully licensed and insured' (no carrier/bond shown) | Submitted 2026-10-22 · was: Unknown | firstchoiceseamlessgutters.net homepage, read 2026-10-22 — "We’re fully licensed and insured, ensuring our clients’ protection on every project." |
| Certifications, authorizations, factory training | | | |
| Association memberships | BBB Accredited Business since 8/12/2025, A+ rating | Internally Verified 2026-10-22 · was: Unknown | BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026-10-22 — "Date of BBB Accreditation: 8/12/2025" |
| Warranty terms | 10-Year Workmanship Guarantee/Warranty (site claim; terms not published) | Submitted 2026-10-22 · was: Unknown | firstchoiceseamlessgutters.net homepage, read 2026-10-22 — "backed by a 10-Year Workmanship Guarantee" |
| Guarantees (response time, on-time, satisfaction) | Site: 'we’ll contact you within 24 hours' (form); 'Fast Response Times' (no figure) | Submitted 2026-10-22 · was: Unknown | firstchoiceseamlessgutters.net homepage, read 2026-10-22 — "Fill out the form below and we’ll contact you within 24 hours" |
| Awards and rankings | 'Best Gutter Installer in Lakeland, Florida' by GutterPro HQ, 2025 — company-distributed press release (MarketersMedia), unverified | Submitted 2026-10-22 · was: Unknown | markets.financialcontent.com/chroniclejournal/article/marketersmedia-2025-12-3-first-choice-seamless-gutters-named-best-gutter-installer-in-lakeland-florida — "officially named the Best Gutter Installer in Lakeland, Florida by GutterPro HQ for 2025" |
| Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0) | 5 out of 5 (138 reviews), 2026-10-22 (site says '95+ 5 Star Google Reviews') | Internally Verified 2026-10-22 · was: Unknown | GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22 — "5 out of 5 (138 reviews)" |
| Team size / trucks / jobs completed | | | |
| Financing — available, provider, terms | [NEED: financing — none found on site, GBP or BBB] | Unknown 2026-10-22 | searched: site, GBP, BBB 2026-10-22 |
| Free estimate — and what free means | Free, no-obligation estimate with free on-site inspection; 'no hidden fees' | Submitted 2026-10-22 · was: Unknown | firstchoiceseamlessgutters.net homepage, read 2026-10-22; firstchoiceseamlessgutters.net/contact/ — "Every project starts with a free on-site inspection and a detailed estimate." |
| Emergency / after-hours reality | Site: 'Available 7 Days a Week'; GBP hours 7 AM–8 PM Mon–Sun; no emergency claim found | Submitted 2026-10-22 · was: Unknown | GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22; firstchoiceseamlessgutters.net homepage, read 2026-10-22 — "Available 7 Days a Week" |
| Minimum service call or trip charge | | | |
| Payment methods | | | |
| Services subcontracted out | | | |
| Named staff for on-page use | BBB owners: Adrian Buehl, Rachel Buehl. Reviews name Adrian, April, Matt, Isaac, James (roles unknown) | Submitted 2026-10-22 · was: Unknown | BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026-10-22; GBP reviews read 2026-10-22 — "Adrian Buehl, Owner" |
| Licensed practitioner for health-claim sign-off *(medical / chiropractic)* | | | |
| Blog author — a real person (CM-039; from the Decision Sheet) | | | |
| Google Business Profile link | https://maps.app.goo.gl/c5prGD6rMCwptG3x6 | Submitted 2026-10-22 · was: Unknown | Paul, intake answer |
| Content management system | WordPress | Client Confirmed 2026-10-22 · was: Unknown | Paul, intake answer |
| Google Search Console access | Access exists (Paul reports) | Submitted 2026-10-22 · was: Unknown | Paul, intake answer |
| Street address shown on the website | 3517 Century Blvd, Lakeland, FL | Paul Approved 2026-10-22 · was: Unknown | Paul, 2026-10-22 (confirmed for website display; billing address check) |

### D2 · Unsupported claims
Claims the site makes publicly that the client could not substantiate. Writers must not repeat
them; the content-risk list tracks where they are live.

| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|

### D3 · Content-risk list
Every live page that still carries a D2 claim or an unconfirmed fact, until it is rebuilt or corrected.

| Page URL | Claim or fact | Source (D2 row / audit finding) | Fixed by (batch or handoff) |
|---|---|---|---|

## Section E — Service area truth
```
TOWNS AT THE EDGES (the furthest towns served, any direction):
CITIES CLAIMED ON SITE:
EXPLICIT EXCLUSIONS:
TRAVEL FEE BEYOND:
```

## Section F — Schema inputs  *(Block 3 cannot open without these)*

| Asset | Value | Status |
|---|---|---|
| ID page URL (becomes the business entity @id) | | |
| Full citation list → sameAs | | |
| Social profile list | | |
| Google Maps share link → hasMap | | |
| Apple Maps link → sameAs | | |
| Confirmed NAP exactly as it must appear | | |
| Confirmed GBP category → schema subtype | | |
| Logo files with pixel dimensions | | |
| Owner name + photo | | |
| **Wikidata URI — category entity** | | |
| **Wikidata URI — area entity** | | |
| **Wikidata URI — county** (one per county the area entity covers) | | |
| **Wikidata URI — state** | | |

## Section G — Positioning (client's own words)
```
WHAT WE DO THAT OTHERS HERE DO NOT:
JOB WE MOST WANT MORE OF:
MOST COMMON THING CUSTOMERS GET WRONG ABOUT THIS TRADE:
```

## Section H — Constraints, exceptions and the superlative opener

| Type | Detail | Approved by | Exit condition |
|---|---|---|---|
| Client constraint | | | |
| Paul Exception | | | |

### H2 · "The Best" decisions (CM-020) — conditional, never a default
| Page | Main keyword & current rank | 1 Demand | 2 Opportunity | 3 Proof (Section D fact) | 4 Not sensitive / Paul OK | Top-3 lock? | Decision | Evidence locator |
|---|---|---|---|---|---|---|---|---|

## Section I — Customer language
| Source | Location | Captured |
|---|---|---|

## Maintenance

| When | Action |
|---|---|
| Page content approved (SD/LD) | Add its row to B3 and C1/C2, its FAQ questions and H2s to C3 |
| New citation built | Add to Section F and sameAs |
| GBP primary category changes | Rebuild Sections A and B — entity gate re-opens |
| Any field moves status | Update in place. Never keep two versions |
