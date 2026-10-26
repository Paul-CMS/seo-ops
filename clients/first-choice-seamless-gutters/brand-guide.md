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
| 5 | Area entity | Proposed: Polk County, Florida = Lakeland–Winter Haven MSA (Q501043). Path: Winter Haven → Polk County → 'comprises the Lakeland–Winter Haven metropolitan statistical area'. Contains all 20 places served. Not served: Plant City (Hillsborough; Paul, 2026-10-24) and Sebring (Highlands; client, 2026-10-24) | Submitted 2026-10-24 · was: Unknown |
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
   area_entity). Both outliers are out of the service area: Plant City not served for now (Paul, 2026-10-24,
   audit_plant_city — client's 'Yes' recorded, not applied); Sebring not served (client). So Polk County contains
   every place served. State: Florida (Q812). PROPOSAL — Paul decides (agency profile §4). [Paul Approved 2026-10-25 — Paul confirmed Florida; settled area_state]
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
| /gutter-cleaning/ | service | title: Gutter Cleaning (service name) · H1: Gutter and Downspout Cleaning · opening: rain gutters + seamless gutter contractor · first H2: Rain Gutters · FAQ H2: Gutter Contractor | H1: Polk County, Florida · opening: Lakeland–Winter Haven metropolitan area · FAQ H2: Polk County | build/pilot/drafts/svc-gutter-cleaning.md (SD, reviewed draft, write-back run 20261024-215625-build-f067) | no |
| /lakeland-fl/ | location | title: Gutter Contractor · H1: Rain Gutters · first H2: Gutter Installation · opening: seamless gutters | city: Lakeland (title "Lakeland, FL", H1) · opening: Polk County, Florida | build/pilot/drafts/loc-lakeland.md (LD, reviewed draft, write-back run 20261024-215625-build-f067) | no |
| /seamless-gutter-installation/ | service | title: Seamless Gutter Installation (service name) · H1: Continuous Rain Gutters · opening: seamless gutters + gutter contractor · first H2: Seamless Gutter Installation · FAQ H2: Seamless Gutters | H1: Polk County, Florida · opening: Lakeland–Winter Haven area · FAQ H2: Polk County | build/services/drafts/svc-seamless-gutter-installation.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /gutter-installation/ | service | title: Gutter Installation (service name) · H1: Gutter Replacement · opening: gutter contractor + gutter installation · first H2: Rain Gutters · FAQ H2: Rain Gutters | H1: Polk County, Florida · opening: Polk County, Florida · FAQ H2: Polk County, Florida | build/services/drafts/svc-gutter-installation.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /gutter-repair/ | service | title: Gutter Repair (service name) · H1: Leaking and Sagging Gutter Repair · opening: gutter contractor + gutter repair · first H2: Seamless Gutter · FAQ H2: Rain Gutter | H1: Polk County, Florida · opening: Lakeland–Winter Haven area · FAQ H2: Polk County | build/services/drafts/svc-gutter-repair.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /commercial-gutters/ | service | title: Commercial Gutters (service name) · H1: Commercial Gutter Systems · opening: rain gutters + gutter contractor · first H2: Commercial Rain Gutters · FAQ H2: Gutter Installation | H1: Polk County, Florida · opening: Polk County, Florida · FAQ H2: Polk County | build/services/drafts/svc-commercial-gutters.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /gutter-downspouts/ | service | title: Gutter Downspouts (service name) · H1: Downspout Installation and Drainage · opening: gutter contractor · first H2: Rain Gutters · types H2: Gutter Installation · FAQ H2: Seamless Gutters | H1: Polk County, Florida · opening: Lakeland–Winter Haven area · FAQ H2: Polk County | build/services/drafts/svc-gutter-downspouts.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /gutter-guards/ | service | title: Gutter Guards (service name) · H1: The Best Gutter Protection Systems · opening: gutter guards + gutter contractor · first H2: Gutter Guards + Rain Gutters · FAQ H2: Seamless Gutters | H1: Polk County, Florida · opening: Polk County, Florida · FAQ H2: Polk County, Florida · areas H2: Polk County | build/services/drafts/svc-gutter-guards.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /copper-gutters/ | service | title: Copper Gutters (service name) · H1: Copper Gutter Systems · opening: gutter contractor + copper gutter installation · first H2: Copper Gutters · FAQ H2: Rain Gutters | H1: Polk County, Florida · opening: Polk County, Florida · FAQ H2: Polk County | build/services/drafts/svc-copper-gutters.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /galvalume-gutters/ | service | title: Galvalume Gutters (service name) · H1: Galvalume Steel Gutters · opening: Galvalume gutters + gutter contractor · first H2: Galvalume Gutter Job · FAQ H2: Galvalume Rain Gutters | H1: Polk County, Florida · opening: Lakeland–Winter Haven area · FAQ H2: Florida | build/services/drafts/svc-galvalume-gutters.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |
| /aluminum-gutters/ | service | title: Aluminum Gutters (service name) · H1: Aluminum Rain Gutters · opening: aluminum gutter systems + gutter contractor · first H2: Aluminum Gutter System · FAQ H2: Aluminum Gutter Installation | H1: Polk County, Florida · opening: Polk County, Florida · FAQ H2: Polk County, Florida | build/services/drafts/svc-aluminum-gutters.md (SD, reviewed draft, write-back run 20261025-143023-build-18ec) | no |

## Section C — Page inventory

### C0 · Page order (from the URL Decision Map)
| Order | Plan no. | Page | Type | Final URL |
|---|---|---|---|---|

### C1 · Service pages
| URL | Service name | H1 service variant | Status |
|---|---|---|---|
| /gutter-cleaning/ | Gutter Cleaning | The Best Gutter and Downspout Cleaning in Polk County, Florida ("The Best" settled the_best_plan_pages) | Draft reviewed (pilot), not approved, not shipped — 2026-10-24 |
| /seamless-gutter-installation/ | Seamless Gutter Installation | Continuous Rain Gutters in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /gutter-installation/ | Gutter Installation | Gutter Replacement in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /gutter-repair/ | Gutter Repair | Leaking and Sagging Gutter Repair in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /commercial-gutters/ | Commercial Gutters | Commercial Gutter Systems in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /gutter-downspouts/ | Gutter Downspouts | Downspout Installation and Drainage in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /gutter-guards/ | Gutter Guards | The Best Gutter Protection Systems in Polk County, Florida ("The Best" settled the_best_plan_pages) | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /copper-gutters/ | Copper Gutters | Copper Gutter Systems in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /galvalume-gutters/ | Galvalume Gutters | Galvalume Steel Gutters in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |
| /aluminum-gutters/ | Aluminum Gutters | Aluminum Rain Gutters in Polk County, Florida | Draft reviewed (services), not approved, not shipped — 2026-10-25 |

### C2 · Location pages
| URL | City | GBP landing page? | Status |
|---|---|---|---|
| /lakeland-fl/ | Lakeland | No — the GBP Website field is the homepage (A11) | Draft reviewed (pilot), not approved, not shipped — 2026-10-24; map embed left for the VA (settled loc-lakeland:map-embed) |

Only a verified GBP's actual landing URL gets LocalBusiness-type schema (BB-604).

### C3 · Heading and FAQ registry
Every FAQ question and H2 live on the site, with the page that owns it. No question on two pages (BB-316).

| Question or H2 | Page that owns it |
|---|---|
| H2: How Does First Choice Seamless Gutters Clean Rain Gutters? | /gutter-cleaning/ |
| H2: What Does a Gutter Cleaning Include, and What Is Separate? | /gutter-cleaning/ |
| H2: What Do Polk County Homeowners Ask a Gutter Contractor About Cleaning? | /gutter-cleaning/ |
| H2: Where Does First Choice Seamless Gutters Offer Gutter Cleaning? | /gutter-cleaning/ |
| FAQ: How much does gutter cleaning cost? | /gutter-cleaning/ |
| FAQ: When is the best time of year to clean gutters in Florida? | /gutter-cleaning/ |
| FAQ: How often should gutters be cleaned in Polk County? | /gutter-cleaning/ |
| FAQ: What are the signs my gutters need cleaning? | /gutter-cleaning/ |
| FAQ: Do telescopic gutter cleaners work? | /gutter-cleaning/ |
| H2: Gutter Installation, Repair and Cleaning in Lakeland | /lakeland-fl/ |
| H2: What Makes Lakeland Hard on Gutters? | /lakeland-fl/ |
| H2: How Does First Choice Serve Lakeland Homeowners? | /lakeland-fl/ |
| H2: Lakeland Gutter Questions | /lakeland-fl/ |
| H2: Which Lakeland Neighborhoods Does First Choice Serve? | /lakeland-fl/ |
| H2: Which Other Cities Near Lakeland Does First Choice Serve? | /lakeland-fl/ |
| FAQ: Does a Lakeland historic district or HOA limit gutter colour or profile? | /lakeland-fl/ |
| FAQ: Who issues permits for gutter work at a Lakeland address — City of Lakeland? | /lakeland-fl/ |
| FAQ: How do Lakeland's summer storms affect gutters? | /lakeland-fl/ |
| H2: How Does a Seamless Gutter Installation Work, From Estimate to Clean-Up? | /seamless-gutter-installation/ |
| H2: What Kinds of Seamless Gutter Jobs Does First Choice Seamless Gutters Take On? | /seamless-gutter-installation/ |
| H2: What Should Polk County Homeowners Know Before Buying Seamless Gutters? | /seamless-gutter-installation/ |
| H2: Which Polk County Towns Get Seamless Gutter Installation From First Choice? | /seamless-gutter-installation/ |
| FAQ: How can you tell if gutters are seamless? | /seamless-gutter-installation/ |
| FAQ: What are the downsides of seamless gutters? | /seamless-gutter-installation/ |
| FAQ: How are seamless gutters made? | /seamless-gutter-installation/ |
| FAQ: What is the highest rated gutter system for a home? | /seamless-gutter-installation/ |
| H2: How Does First Choice Seamless Gutters Install New Rain Gutters? | /gutter-installation/ |
| H2: What Kinds of Gutter Replacement and New Gutter Jobs Are There? | /gutter-installation/ |
| H2: What Gutter Materials Can You Choose? | /gutter-installation/ |
| H2: What Do Homeowners in Polk County, Florida Ask About New Rain Gutters? | /gutter-installation/ |
| H2: Where Does First Choice Seamless Gutters Install and Replace Gutters? | /gutter-installation/ |
| FAQ: When should house gutters be replaced? | /gutter-installation/ |
| FAQ: What do new rain gutters cost in Florida? | /gutter-installation/ |
| FAQ: Is it common for a house not to have gutters? | /gutter-installation/ |
| FAQ: Can I install my own gutters? | /gutter-installation/ |
| FAQ: How is a gutter installation estimate worked out? | /gutter-installation/ |
| H2: What Happens During a Seamless Gutter Repair Visit? | /gutter-repair/ |
| H2: Which Gutter Problems Can Be Repaired Instead of Replaced? | /gutter-repair/ |
| H2: What Should Polk County Homeowners Know Before Paying for Rain Gutter Repair? | /gutter-repair/ |
| H2: Which Polk County Towns Can Book a Gutter Repair Visit? | /gutter-repair/ |
| FAQ: How much does it cost to fix gutters? | /gutter-repair/ |
| FAQ: What is the most common problem with gutters? | /gutter-repair/ |
| FAQ: Can a handyman fix a gutter? | /gutter-repair/ |
| FAQ: Should a damaged gutter be repaired or replaced? | /gutter-repair/ |
| FAQ: What does routine gutter maintenance include? | /gutter-repair/ |
| H2: How Does First Choice Seamless Gutters Install Commercial Rain Gutters? | /commercial-gutters/ |
| H2: What Kinds of Commercial Gutter Work Does First Choice Handle? | /commercial-gutters/ |
| H2: What Do Polk County Business Owners Ask About Commercial Gutter Installation? | /commercial-gutters/ |
| H2: Where Does First Choice Seamless Gutters Install Commercial Gutters? | /commercial-gutters/ |
| FAQ: What are commercial-grade gutters? | /commercial-gutters/ |
| FAQ: What is the difference between box gutters and K-style gutters on a commercial roof? | /commercial-gutters/ |
| FAQ: What size gutters does a large commercial roof need? | /commercial-gutters/ |
| FAQ: How long does a commercial gutter installation take? | /commercial-gutters/ |
| H2: How Does First Choice Seamless Gutters Fit Downspouts to Rain Gutters? | /gutter-downspouts/ |
| H2: Which Downspout Sizes, Materials and Drainage Add-Ons Suit a Gutter Installation? | /gutter-downspouts/ |
| H2: Which Downspout Questions Come Up Most With Seamless Gutters in Polk County? | /gutter-downspouts/ |
| H2: Which Polk County Towns Does First Choice Serve for Downspout Work? | /gutter-downspouts/ |
| FAQ: What is the rule of thumb for how many downspouts a gutter needs? | /gutter-downspouts/ |
| FAQ: Can you put a 3x4 downspout on a 5-inch gutter? | /gutter-downspouts/ |
| FAQ: What can I use instead of a downspout? | /gutter-downspouts/ |
| FAQ: How much does it cost to replace a downspout? | /gutter-downspouts/ |
| FAQ: Where should downspouts drain on a Florida lot? | /gutter-downspouts/ |
| H2: How Does First Choice Seamless Gutters Add Gutter Guards to Rain Gutters? | /gutter-guards/ |
| H2: Which Kinds of Gutter Guards Work on Rain Gutters? | /gutter-guards/ |
| H2: Are Gutter Guards Worth It on Seamless Gutters in Polk County, Florida? | /gutter-guards/ |
| H2: Which Polk County Towns Can Get Gutter Guards From First Choice? | /gutter-guards/ |
| FAQ: What are the downsides of gutter guards? | /gutter-guards/ |
| FAQ: How much should I expect to pay for gutter guards? | /gutter-guards/ |
| FAQ: What is the difference between a leaf guard and a gutter guard? | /gutter-guards/ |
| FAQ: What do roofers say about gutter guards? | /gutter-guards/ |
| H2: How Does First Choice Seamless Gutters Plan and Install Copper Gutters? | /copper-gutters/ |
| H2: What Kinds of Copper Gutters and Downspouts Can You Choose From? | /copper-gutters/ |
| H2: What Do Polk County Homeowners Ask About Copper Rain Gutters? | /copper-gutters/ |
| H2: Which Polk County Towns Can Get Copper Gutters From First Choice Seamless Gutters? | /copper-gutters/ |
| FAQ: How long do copper gutters last? | /copper-gutters/ |
| FAQ: Are copper gutters worth the cost? | /copper-gutters/ |
| FAQ: Can copper and aluminum gutters be mixed? | /copper-gutters/ |
| FAQ: Should copper gutters be soldered? | /copper-gutters/ |
| H2: How Does a Galvalume Gutter Job Work With First Choice Seamless Gutters? | /galvalume-gutters/ |
| H2: Which Parts of a Galvalume Gutter System Can First Choice Seamless Gutters Handle? | /galvalume-gutters/ |
| H2: What Do Florida Homeowners Ask About Galvalume Rain Gutters? | /galvalume-gutters/ |
| H2: Where Does First Choice Seamless Gutters Install Galvalume Gutters? | /galvalume-gutters/ |
| FAQ: What is Galvalume steel? | /galvalume-gutters/ |
| FAQ: Are Galvalume gutters better than aluminum or galvanized gutters? | /galvalume-gutters/ |
| FAQ: What is the best gutter material for Florida homes? | /galvalume-gutters/ |
| FAQ: Do Galvalume gutters rust in Florida humidity? | /galvalume-gutters/ |
| H2: What Happens When First Choice Seamless Gutters Installs an Aluminum Gutter System? | /aluminum-gutters/ |
| H2: Which Kinds of Aluminum Gutters Can a Home Have? | /aluminum-gutters/ |
| H2: What Should Polk County, Florida Homeowners Ask About Aluminum Gutter Installation? | /aluminum-gutters/ |
| H2: Where Does First Choice Seamless Gutters Install Aluminum Gutters? | /aluminum-gutters/ |
| FAQ: Are aluminum gutters good? | /aluminum-gutters/ |
| FAQ: What is the difference between .027 and .032 aluminum gutters? | /aluminum-gutters/ |
| FAQ: Do aluminum gutters rust? | /aluminum-gutters/ |
| FAQ: What do aluminum gutters cost for a home? | /aluminum-gutters/ |

## Section D — Verified facts
Everything a writer may state. **Not here = does not exist.**

| Fact | Value | Status | Source |
|---|---|---|---|
| Founding year / years in business | In business 'well over 25 plus years' (client). Client says BBB 'Business Started: 11/24/2021' is not when they started trading (2021 is the BBB/incorporation date). Exact founding year: Unknown — not provided by client (Paul, 2026-10-25) | Client Confirmed 2026-10-25 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_5 / claim_5_detail); founding year: Paul, 2026-10-25: no answers, mark unknown — "we have been in business for well over 25 plus years" |
| Legal entity + DBA | First Choice Seamless Gutters Inc., a corporation (client confirmed); BBB primary name 'First Choice Seamless Gutters'; site also 'First Choice Seamless Gutter Inc' (typo, singular) | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Who_you_are_0/1) — "Yes, correct" |
| Licence numbers and classes | Not required in Florida for these services; no licence number to show. Settled: not an open question. | Paul Approved 2026-10-23 · was: Unknown | Paul, 2026-10-23 — "We’re fully licensed and insured" |
| Insurance / bonded status | Insured: client confirms the insurance part of 'fully licensed and insured'. Carrier and certificate of insurance: Unknown — not provided by client (Paul, 2026-10-25) | Client Confirmed 2026-10-25 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_3); certificate: Paul, 2026-10-25: no answers, mark unknown — "Yes, accurate" |
| Certifications, authorizations, factory training | | | |
| Association memberships | BBB Accredited Business since 8/12/2025, A+ rating | Internally Verified 2026-10-22 · was: Unknown | BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026-10-22 — "Date of BBB Accreditation: 8/12/2025" |
| Warranty terms | 10-Year Workmanship Guarantee, in writing (client). Owner's public review response: problems with its gutters corrected free of cost. Copy of the written warranty terms: Unknown — not provided by client (Paul, 2026-10-25) | Client Confirmed 2026-10-25 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_4); owner review response in data/reviews/raw/reviews.json; written copy: Paul, 2026-10-25: no answers, mark unknown — "Yes, and in writing" |
| Guarantees (response time, on-time, satisfaction) | Form enquiries answered within 24 hours (client confirmed). Client note: 'We pride ourselves on great customer communication and excellent customer care.' | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_7 / claim_7_detail) — "Yes, accurate" |
| Awards and rankings | 'Best Gutter Installer in Lakeland, Florida' by GutterPro HQ, 2025 — client says accurate; only public source is a company-distributed press release (MarketersMedia, Dec 2025) | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_10); markets.financialcontent.com MarketersMedia release 2025-12-03 — "Yes, accurate" |
| Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0) | 5 out of 5 (138 reviews), 2026-10-22 (site says '95+ 5 Star Google Reviews') | Internally Verified 2026-10-22 · was: Unknown | GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22 — "5 out of 5 (138 reviews)" |
| Team size / trucks / jobs completed | | | |
| Financing — available, provider, terms | Unknown — not provided by client (Paul, 2026-10-25) | Unknown 2026-10-25 | Paul, 2026-10-25: no answers, mark unknown; searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (question_3: 'answers follow') |
| Free estimate — and what free means | Free on-site inspection and detailed estimate, free whether or not the customer books (client confirmed); site also says no-obligation, 'no hidden fees' | Client Confirmed 2026-10-24 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_9) — "Yes, accurate" |
| Emergency / after-hours reality | Available 7 days a week; emergency after-hours service available. GBP hours 7 AM to 8 PM Mon-Sun correct. | Client Confirmed 2026-10-24 · was: Submitted | Client answer via Paul 2026-10-24 (interviews/facts/First Choice Seamless Gutters - Facts Answers - pilot - 2026-10-24.md) — "Available 7 Days a Week" |
| Minimum service call or trip charge | Unknown — not provided by client (Paul, 2026-10-25) | Unknown 2026-10-25 | Paul, 2026-10-25: no answers, mark unknown; searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (question_0: 'answers follow') |
| Payment methods | Unknown — not provided by client (Paul, 2026-10-25) | Unknown 2026-10-25 | Paul, 2026-10-25: no answers, mark unknown; searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (question_2: 'answers follow') |
| Services subcontracted out | Unknown — not provided by client (Paul, 2026-10-25) | Unknown 2026-10-25 | Paul, 2026-10-25: no answers, mark unknown; searched: site, GBP, BBB 2026-10-22; Client proof sheet returned 2026-10-24 (question_4: client wrote 'n/a', not interpreted) — "n/a" |
| Named staff for on-page use | Owners: Adrian Buehl and Rachel Buehl (client confirmed). Roles of April, Matt, Isaac, James: Unknown — not provided by client (Paul, 2026-10-25) | Client Confirmed 2026-10-25 · was: Submitted | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Who_you_are_2; question_5); staff roles: Paul, 2026-10-25: no answers, mark unknown — "Yes, correct" |
| Licensed practitioner for health-claim sign-off *(medical / chiropractic)* | | | |
| Blog author — a real person (CM-039; from the Decision Sheet) | Adrian Buehl, owner | Paul Approved 2026-10-24 · was: Unknown | Settled blog_author (Paul, Approval 1, 2026-10-22: the owner named on the returned facts, candidate Adrian Buehl); owners confirmed on Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Who_you_are_2) |
| Google Business Profile link | https://maps.app.goo.gl/c5prGD6rMCwptG3x6 | Submitted 2026-10-22 · was: Unknown | Paul, intake answer |
| Content management system | WordPress | Client Confirmed 2026-10-22 · was: Unknown | Paul, intake answer |
| Google Search Console access | Access exists (Paul reports) | Submitted 2026-10-22 · was: Unknown | Paul, intake answer |
| Street address shown on the website | 3517 Century Blvd, Lakeland, FL | Paul Approved 2026-10-22 · was: Unknown | Paul, 2026-10-22 (confirmed for website display; billing address check) |
| Military and seniors offer | $150 off full house installations for Military & Seniors: confirmed and still running. | Client Confirmed 2026-10-24 · was: Paul Approved | Paul, 2026-10-23; Client proof sheet returned 2026-10-24 (RETURNED.json, claim_8) — "Yes, accurate" |
| Plant City served | Not served for now: Plant City is listed nowhere (no Plant City page, not in towns served, not in the service area). The client's 'Yes' (claim_1_plant, 2026-10-24) is recorded but not applied. | Paul Approved 2026-10-24 · was: Unknown | Paul, 2026-10-24 (settled audit_plant_city) |
| Base town (where the business is based) | Lakeland, FL | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_0 / claim_0_detail) — "Lakeland, FL" |
| Family owned and operated | Yes — family owned and operated | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, claim_6) — "Yes, accurate" |
| Opening hours | 7 AM – 8 PM, Monday to Sunday | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, confirm_Contact_and_hours_2) — "Yes, correct" |
| Services (client keep/stop) | Keep (10): Seamless Gutter Installation, Gutter Installation, Gutter Repair, Commercial Gutters, Gutter Downspouts, Gutter Guards, Gutter Cleaning, Copper Gutters, Galvalume Gutters, Aluminum Gutters. Stop: Gutter Maintenance. None added; none marked 'want more' | Client Confirmed 2026-10-24 · was: Unknown | Client proof sheet returned 2026-10-24 (discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json, service_0..10_keep, service_6_stop) — "service_6_stop: true" |
| Gutter Maintenance (standalone service) | Not a standalone service. Its maintenance scope is folded into the Gutter Repair and Gutter Cleaning pages; no /services/gutter-maintenance/ page. The old URL is redirected (never deleted) to the closer of the two. | Paul Approved 2026-10-24 · was: Unknown | Paul, 2026-10-24 (settled audit_gutter_maintenance, F-014) |

### D2 · Unsupported claims
Claims the site makes publicly that the client could not substantiate. Writers must not repeat
them; the content-risk list tracks where they are live.

| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|
| "fully licensed and insured" / "Licensed & Insured" — the *licensed* part | 8 pages (F-004) | "no license number needed in fl." (claim_2_detail, 2026-10-24); no licence held to cite | Do not write "licensed". "Insured" may be written (claim_3 confirmed); certificate of insurance: Unknown — not provided by client (Paul, 2026-10-25) |
| "Based in Winter Haven" | Homepage (F-001) | Based in Lakeland, FL (claim_0, 2026-10-24) | Do not repeat; base town = Lakeland |
| "Based in nearby Bartow" | Both blog posts (F-001, F-045) | Based in Lakeland, FL (claim_0, 2026-10-24) | Do not repeat; base town = Lakeland |
| "Business Started: 11/24/2021" (BBB, not the site) | BBB profile | Not when they started trading; "well over 25 plus years" (claim_5, 2026-10-24) | Write no founding year or "since 2021"; "25+ years" may be written (client confirmed); exact founding year: Unknown — not provided by client (Paul, 2026-10-25) |

### D3 · Content-risk list
Every live page that still carries a D2 claim or an unconfirmed fact, until it is rebuilt or corrected.

| Page URL | Claim or fact | Source (D2 row / audit finding) | Fixed by (batch or handoff) |
|---|---|---|---|
| / · /areas-we-serve/fort-meade-fl/ · /areas-we-serve/polk-city-fl/ · /services/copper-gutters/ · /services/galvalume-gutters/ · /services/gutter-cleaning/ · /services/gutter-installation/ · /services/gutter-maintenance/ | "licensed" (no licence held) | D2 row 1 / F-004 (settled audit_licence_claim) | Build rebuild; live pages until then — Paul |
| / | "Based in Winter Haven" | D2 row 2 / F-001 | Build rebuild (homepage) |
| /gutter-guards-winter-haven-fl/ · /gutter-services-lakeland-fl/ | "Based in nearby Bartow" | D2 row 3 / F-001, F-045 | Blog (Block 5) |
| /services/gutter-maintenance/ | A service the client wants to stop getting calls for (service_6_stop) | services-client fact / F-014 (settled audit_gutter_maintenance, 2026-10-24) | Build: maintenance scope folded into /services/gutter-repair/ and /services/gutter-cleaning/; old URL 301 to the closer of the two (VA redirect handoff, never deleted) |
| /areas-we-serve/plant-city-fl/ | Plant City presented as served (not served for now) | plant-city-served fact / F-015 (settled audit_plant_city, 2026-10-24) | Build: 301 to /areas-we-serve/ per F-015 once the citation check (C3) and C4 (no leads) are confirmed; never deleted |

## Section E — Service area truth
```
TOWNS AT THE EDGES (the furthest towns served, any direction): Unknown — not provided by client (Paul, 2026-10-25) — all 20 Polk County places confirmed (towns-served-client, 2026-10-24)
CITIES CLAIMED ON SITE: Auburndale, Bartow, Davenport, Dundee, Eagle Lake, Haines City, Lake Alfred, Lake Wales, Lakeland, Polk City, Waverly, Winter Haven, Fort Meade, Frostproof, Highland City, Kathleen, Lake Hamilton, Mulberry, Wahneta (+ Lakeland Highlands on the GBP) — all confirmed by the client
EXPLICIT EXCLUSIONS: Sebring — not served (client, claim_1_sebring); Plant City — not served for now, listed nowhere,
  no Plant City page (Paul, 2026-10-24, audit_plant_city; the client's 'Yes' on claim_1_plant is recorded, not applied)
TRAVEL FEE BEYOND: Unknown — not provided by client (Paul, 2026-10-25)
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
WHAT WE DO THAT OTHERS HERE DO NOT: Unknown — not provided by client (Paul, 2026-10-25) — question_6 came back as ten third-person
  marketing bullets (fact positioning-client-text, Submitted), not the client's words
JOB WE MOST WANT MORE OF: Unknown — not provided by client (Paul, 2026-10-25)
MOST COMMON THING CUSTOMERS GET WRONG ABOUT THIS TRADE: Unknown — not provided by client (Paul, 2026-10-25)
```
New claims to substantiate before any page states them (question_6, 2026-10-24): beats competing regional quotes "by
shocking margins"; competitors offer "1- to 2-year warranties"; calls returned "often within an hour" (the confirmed
promise is within 24 hours); "eliminating unpredictable arrival windows"; HOA colour and metal samples at the door;
downspouts engineered by roof pitch; Galvalume "specialty" and storm claims. Already confirmed elsewhere: the 10-year
workmanship guarantee in writing (claim_4) and $150 off for military and seniors (claim_8). On-site seamless
fabrication fits the trade but is not yet confirmed as the client's own statement.
Services to position (Paul, 2026-10-24, audit_gutter_maintenance): the 10 the client keeps. Gutter Maintenance is not
a standalone service — never position or promote it on its own; its maintenance scope is written into the Gutter
Repair and Gutter Cleaning pages. Plant City is never named as a place served (audit_plant_city).

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
