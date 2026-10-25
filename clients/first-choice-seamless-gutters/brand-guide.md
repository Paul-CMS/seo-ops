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
| 1 | Brand entity (GBP name, exactly) | First Choice Seamless Gutters Inc. | Client Confirmed 2026-10-24 · was: Internally Verified |
| 2 | GBP primary category = the category entity | CONFLICT (PROC-01): Paul intake 'Seamless gutters' · Google Maps place data category id 'gutter_service' (display 'Gutter service') — dashboard check pending (Gwen manual_lookup) | Disputed 2026-10-22 · was: Submitted |
| 3 | Category variants (4–6) | Proposed: Gutter Service · Seamless Gutters · Rain Gutters · Gutter Contractor · Gutter Installation (Wikipedia entity: Rain gutter, Q152833) | Submitted 2026-10-22 · was: Unknown |
| 4 | Storefront or SAB | Service area business (travels to customers) | Client Confirmed 2026-10-24 · was: Submitted |
| 5 | Area entity | Proposed: Polk County, Florida = Lakeland–Winter Haven MSA (Q501043). Path: Winter Haven → Polk County → 'comprises the Lakeland–Winter Haven metropolitan statistical area'. Contains 19 of 20 site towns; outliers Plant City (Hillsborough) and Sebring (Highlands, GBP only) | Submitted 2026-10-22 · was: Unknown |
| 6 | Area variants (3–5) | Proposed: Polk County, FL · Polk County, Florida · Lakeland–Winter Haven · Lakeland–Winter Haven metropolitan area | Submitted 2026-10-22 · was: Unknown |
| 7 | Separator standard | ` - ` | |
| 8 | Phone | (863) 330-3243 (site, GBP, schema agree; BBB also lists 'Other Phone' (863) 320-2842) | Client Confirmed 2026-10-24 · was: Internally Verified |
| 9 | Primary domain (canonical host form) | https://www.firstchoiceseamlessgutters.net/ (non-www 301 → www; canonical tag www) | Internally Verified 2026-10-22 · was: Submitted |
| 10 | Legal entity name | First Choice Seamless Gutters Inc. (BBB: Corporation, incorporated 11/24/2021) — Sunbiz record not read (403), Gwen manual_lookup | Client Confirmed 2026-10-24 · was: Submitted |
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
| Founding year / years in business | In business 'well over 25 plus years' (client). Client says BBB 'Business Started: 11/24/2021' is not when they started trading (2021 is the BBB/incorporation date). Exact founding year: [NEED: founding year] | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_5 / claim_5_detail) — "we have been in business for well over 25 plus years" |
| Legal entity + DBA | First Choice Seamless Gutters Inc., a corporation (client confirmed); BBB primary name 'First Choice Seamless Gutters'; site also 'First Choice Seamless Gutter Inc' (typo, singular) | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Who_you_are_0/1) — "Yes, correct" |
| Licence numbers and classes | Not required in Florida for these services; no licence number to show. Settled: not an open question. | Paul Approved 2026-10-23 · was: Unknown | Paul, 2026-10-23 — "We’re fully licensed and insured" |
| Insurance / bonded status | Insured: client confirms the insurance part of 'fully licensed and insured'. Carrier and certificate: [NEED: certificate of insurance — not sent] | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_3) — "Yes, accurate" |
| Certifications, authorizations, factory training | | | |
| Association memberships | BBB Accredited Business since 8/12/2025, A+ rating | Internally Verified 2026-10-22 · was: Unknown | BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026-10-22 — "Date of BBB Accreditation: 8/12/2025" |
| Warranty terms | 10-Year Workmanship Guarantee, in writing (client). Owner's public review response: problems with its gutters corrected free of cost. Written terms not on file: [NEED: copy of the written warranty] | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_4); owner review response in data/reviews/raw/reviews.json — "Yes, and in writing" |
| Guarantees (response time, on-time, satisfaction) | Form enquiries answered within 24 hours (client confirmed). Client note: 'We pride ourselves on great customer communication and excellent customer care.' | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_7 / claim_7_detail) — "Yes, accurate" |
| Awards and rankings | 'Best Gutter Installer in Lakeland, Florida' by GutterPro HQ, 2025 — client says accurate; only public source is a company-distributed press release (MarketersMedia, Dec 2025) | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_10); markets.financialcontent.com MarketersMedia release 2025-12-03 — "Yes, accurate" |
| Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0) | 5 out of 5 (138 reviews), 2026-10-22 (site says '95+ 5 Star Google Reviews') | Internally Verified 2026-10-22 · was: Unknown | GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22 — "5 out of 5 (138 reviews)" |
| Team size / trucks / jobs completed | | | |
| Financing — available, provider, terms | [NEED: financing — none found on site, GBP or BBB; client wrote 'answers follow'] | Unknown 2026-10-24 | searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, question_3) |
| Free estimate — and what free means | Free on-site inspection and detailed estimate, free whether or not the customer books (client confirmed); site also says no-obligation, 'no hidden fees' | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_9) — "Yes, accurate" |
| Emergency / after-hours reality | Site: 'Available 7 Days a Week'; GBP hours 7 AM–8 PM Mon–Sun; no emergency claim found | Submitted 2026-10-22 · was: Unknown | GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22; firstchoiceseamlessgutters.net homepage, read 2026-10-22 — "Available 7 Days a Week" |
| Minimum service call or trip charge | [NEED: minimum or trip charge — client wrote 'answers follow'] | Unknown 2026-10-24 | searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, question_0) |
| Payment methods | [NEED: payment methods — client wrote 'answers follow'] | Unknown 2026-10-24 | searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, question_2) |
| Services subcontracted out | [NEED: subcontracting — client answered 'n/a'; confirm it means nothing is subcontracted] | Unknown 2026-10-24 | searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, question_4) — "n/a" |
| Named staff for on-page use | Owners: Adrian Buehl and Rachel Buehl (client confirmed). Roles of April, Matt, Isaac, James: [NEED: staff roles — client wrote 'answers follow'] | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Who_you_are_2; question_5) — "Yes, correct" |
| Licensed practitioner for health-claim sign-off *(medical / chiropractic)* | | | |
| Blog author — a real person (CM-039; from the Decision Sheet) | Adrian Buehl, owner | Paul Approved 2026-10-24 · was: Unknown | Settled blog_author (Paul, Approval 1, 2026-10-22: the owner named on the returned facts, candidate Adrian Buehl); owners confirmed on Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Who_you_are_2) |
| Google Business Profile link | https://maps.app.goo.gl/c5prGD6rMCwptG3x6 | Submitted 2026-10-22 · was: Unknown | Paul, intake answer |
| Content management system | WordPress | Client Confirmed 2026-10-22 · was: Unknown | Paul, intake answer |
| Google Search Console access | Access exists (Paul reports) | Submitted 2026-10-22 · was: Unknown | Paul, intake answer |
| Street address shown on the website | 3517 Century Blvd, Lakeland, FL | Paul Approved 2026-10-22 · was: Unknown | Paul, 2026-10-22 (confirmed for website display; billing address check) |
| Military and seniors offer | $150 off full house installations for Military & Seniors: confirmed and still running. | Client Confirmed 2026-10-24 · was: Paul Approved | Paul, 2026-10-23; Client proof sheet returned 2026-10-24 (RETURNED.json, claim_8) — "Yes, accurate" |
| Plant City served | Not in the established service area; no Plant City page. Cities listed stay as the established service area. | Paul Approved 2026-10-23 · was: Unknown | Paul, 2026-10-23 |
| Base town (where the business is based) | Lakeland, FL | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_0 / claim_0_detail) — "Lakeland, FL" |
| Family owned and operated | Yes — family owned and operated | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_6) — "Yes, accurate" |
| Opening hours | 7 AM – 8 PM, Monday to Sunday | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Contact_and_hours_2) — "Yes, correct" |
| Services (client keep/stop) | Keep (10): Seamless Gutter Installation, Gutter Installation, Gutter Repair, Commercial Gutters, Gutter Downspouts, Gutter Guards, Gutter Cleaning, Copper Gutters, Galvalume Gutters, Aluminum Gutters. Stop: Gutter Maintenance. None added; none marked 'want more' | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, service_0..10_keep, service_6_stop) — "service_6_stop: true" |

### D2 · Unsupported claims
Claims the site makes publicly that the client could not substantiate. Writers must not repeat
them; the content-risk list tracks where they are live.

| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|
| "fully licensed and insured" / "Licensed & Insured" — the *licensed* part | 8 pages (F-004) | "no license number needed in fl." (claim_2_detail, 2026-10-24); no licence held to cite | Do not write "licensed". "Insured" may be written (claim_3 confirmed); certificate still [NEED] |
| "Based in Winter Haven" | Homepage (F-001) | Based in Lakeland, FL (claim_0, 2026-10-24) | Do not repeat; base town = Lakeland |
| "Based in nearby Bartow" | Both blog posts (F-001, F-045) | Based in Lakeland, FL (claim_0, 2026-10-24) | Do not repeat; base town = Lakeland |
| "Business Started: 11/24/2021" (BBB, not the site) | BBB profile | Not when they started trading; "well over 25 plus years" (claim_5, 2026-10-24) | Write no founding year or "since 2021"; "25+ years" waits on the founding year [NEED] |

### D3 · Content-risk list
Every live page that still carries a D2 claim or an unconfirmed fact, until it is rebuilt or corrected.

| Page URL | Claim or fact | Source (D2 row / audit finding) | Fixed by (batch or handoff) |
|---|---|---|---|
| / · /areas-we-serve/fort-meade-fl/ · /areas-we-serve/polk-city-fl/ · /services/copper-gutters/ · /services/galvalume-gutters/ · /services/gutter-cleaning/ · /services/gutter-installation/ · /services/gutter-maintenance/ | "licensed" (no licence held) | D2 row 1 / F-004 (settled audit_licence_claim) | Build rebuild; live pages until then — Paul |
| / | "Based in Winter Haven" | D2 row 2 / F-001 | Build rebuild (homepage) |
| /gutter-guards-winter-haven-fl/ · /gutter-services-lakeland-fl/ | "Based in nearby Bartow" | D2 row 3 / F-001, F-045 | Blog (Block 5) |
| /services/gutter-maintenance/ | A service the client wants to stop getting calls for (service_6_stop) | services-client fact / F-014 | Paul — fold or redirect (open) |

## Section E — Service area truth
```
TOWNS AT THE EDGES (the furthest towns served, any direction): [NEED: not asked as edges] — all 20 Polk County places confirmed (towns-served-client, 2026-10-24)
CITIES CLAIMED ON SITE: Auburndale, Bartow, Davenport, Dundee, Eagle Lake, Haines City, Lake Alfred, Lake Wales, Lakeland, Polk City, Waverly, Winter Haven, Fort Meade, Frostproof, Highland City, Kathleen, Lake Hamilton, Mulberry, Wahneta (+ Lakeland Highlands on the GBP) — all confirmed by the client; Plant City: client says served — DISPUTED with Paul's fact plant-city-served (reopen logged, Paul decides)
EXPLICIT EXCLUSIONS: Sebring — not served (client, claim_1_sebring)
TRAVEL FEE BEYOND: [NEED: travel fee — not answered]
```
Note (client-written, towns_excluded, 2026-10-24 — a caution, not a fact change): all 20 places are inside Polk County, which
has the same boundaries as the Lakeland–Winter Haven MSA; Davenport and Haines City ZIP codes reach into Four Corners
(Osceola, Lake, Orange counties), so developments such as ChampionsGate or Four Corners would be outside the county;
Highland City, Kathleen, Wahneta, Waverly and Lakeland Highlands are unincorporated places — the note suggests listing
them in areas served rather than giving them their own location pages (a site-plan choice for Paul at Build). The text
is addressed to the agency, not written as the client's own answer.

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
WHAT WE DO THAT OTHERS HERE DO NOT: [NEED: the client's own sentence] — question_6 came back as ten third-person
  marketing bullets (fact positioning-client-text, Submitted), not the client's words
JOB WE MOST WANT MORE OF: [NEED: client wrote "answers follow"]
MOST COMMON THING CUSTOMERS GET WRONG ABOUT THIS TRADE: [NEED: client wrote "answers follow"]
```
New claims to substantiate before any page states them (question_6, 2026-10-24): beats competing regional quotes "by
shocking margins"; competitors offer "1- to 2-year warranties"; calls returned "often within an hour" (the confirmed
promise is within 24 hours); "eliminating unpredictable arrival windows"; HOA colour and metal samples at the door;
downspouts engineered by roof pitch; Galvalume "specialty" and storm claims. Already confirmed elsewhere: the 10-year
workmanship guarantee in writing (claim_4) and $150 off for military and seniors (claim_8). On-site seamless
fabrication fits the trade but is not yet confirmed as the client's own statement.

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
