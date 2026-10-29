# Carolina Carpet Cleaning - Brand Guide
### The single business-truth record. Every agent reads it; the Build agent writes back to it.
Repo working copy: `clients/<slug>/brand-guide.md` · mirrored to `Carolina Carpet Cleaning - TMS/Carolina Carpet Cleaning - Brand Guide.md`

## Field status values

`Submitted` · `Internally Verified` · `Client Confirmed` · `Disputed` · `Unknown` · `Paul Approved`

**A field at `Unknown` or `Disputed` blocks whatever consumes it.** Writers write
`[NEED: ...]` instead of inventing (CM-016). `Submitted` may appear in a draft but blocks
publication.

---

## Section A — Entity foundation  *(Paul approves: gate entity_approved)*

| # | Field | Value | Status |
|---|---|---|---|
| 1 | Brand entity (GBP name, exactly) | Carolina Carpet Cleaning | Submitted 2026-10-28 · was: Unknown |
| 2 | GBP primary category = the category entity | Carpet cleaning service | Client Confirmed 2026-10-28 · was: Submitted |
| 3 | Category variants (4–6) | Proposed: carpet cleaning · carpet cleaning service · carpet cleaners · carpet cleaning company · carpet cleaner (search volume checked in the data step) | Submitted 2026-10-28 · was: Unknown |
| 4 | Storefront or SAB | SAB; address on website only (273 Club Gate, Bluffton, SC 29910) matches GBP | Paul Approved 2026-10-28 · was: Unknown |
| 5 | Area entity | Hilton Head Island metropolitan area | Paul Approved 2026-10-28 · was: Submitted |
| 6 | Area variants (3–5) | SEO titles: Hilton Head Island Metro Area · user-facing titles and homepage H1: South Carolina Lowcountry | Paul Approved 2026-10-28 · was: Submitted |
| 7 | Separator standard | ' - ' | Submitted 2026-10-28 · was: Unknown |
| 8 | Phone | (843) 575-6286 | Paul Approved 2026-10-28 · was: Disputed |
| 9 | Primary domain (canonical host form) | https://carpetcleaningblufftonsc.com/ (http and www 301 to it; rel=canonical matches) | Internally Verified 2026-10-28 · was: Unknown |
| 10 | Legal entity name | Carolina Floor Cleaning Pros | Client Confirmed 2026-10-28 · was: Unknown |
| 11 | Exact URL in the GBP Website field | https://carpetcleaningblufftonsc.com/ | Paul Approved 2026-10-28 · was: Unknown |
| | Facebook page (Beaufort) | https://www.facebook.com/carpetcleaningbeaufortsc | Paul Approved 2026-10-28 · was: Unknown |
| | Travel fee beyond the six towns | None — no travel fee | Paul Approved 2026-10-29 · was: Unknown |

**Area entity derivation** (BB-105) — record the path, not just the answer:

```
City served: Bluffton, SC (Q3243593) — "Bluffton is a town in southern Beaufort County"
-> County: Beaufort County, SC (Q495682); also served: Jasper County, SC (Q112957); Yemassee touches Hampton County (Q497880)
-> Region: Hilton Head Island metropolitan area (Q17020871) — "officially the Hilton Head Island–Bluffton–Port Royal, SC
   Metropolitan Statistical Area ... the two southernmost counties in the South Carolina Lowcountry" (Beaufort + Jasper)
Contains all 18 towns served? 17 of 18 wholly; Yemassee only in its Beaufort County part ("a town in Hampton and Beaufort counties")
Next level up: South Carolina Lowcountry (Q3885311) — contains Beaufort, Jasper and Hampton
Smallest true container: PROPOSED Hilton Head Island metropolitan area (Paul decides: MSA, or the Lowcountry if Yemassee
   must sit wholly inside) — Decision Sheet row area_entity
State: South Carolina (Q1456)
```

**Paul approved this section on:** ____________

## Section B — Variant ownership  *(CM-024: collisions are vertical, not horizontal)*

### B1 · Reserved for the homepage
```
HOMEPAGE AREA VARIANT:      Hilton Head Island Metro Area (title) · South Carolina Lowcountry (H1) [Submitted 2026-10-28, proposal]
HOMEPAGE CATEGORY VARIANT:  Carpet Cleaning [Submitted 2026-10-28, proposal]
```
No other page may claim the reserved area variant. This is the only cross-page variant rule.

### B2 · Rotation pool
Every area variant except the reserved one. Reuse across service pages is correct.
```
1. South Carolina Lowcountry
2. Hilton Head Island–Bluffton–Port Royal area
3. Lowcountry
```
_"Hilton Head Island metropolitan area" is left out of the pool: it is the reserved title variant in its full form._
_Proposed 2026-10-28 (discovery); settled at Approval 1._

### B3 · Assignment log — the write-back target
| Page URL | Page type | Category variant | Area variant | Content file (SD/LD) | Shipped |
|---|---|---|---|---|---|
| / | homepage | | *(reserved)* | | |
| /carpet-cleaning/ | service | home carpet cleaning (H1) · carpet cleaners (first H2) · carpet cleaning service (FAQ H2) | South Carolina Lowcountry (H1, site plan; sheet row 1 = a) · Lowcountry (FAQ H2) | build/pilot/drafts/svc-carpet-cleaning.md | |
| /bluffton/ | location | carpet cleaners (H1) · carpet cleaning (title) | Bluffton (city) | build/pilot/drafts/loc-bluffton.md | |

## Section C — Page inventory

### C0 · Page order (from the URL Decision Map)
| Order | Plan no. | Page | Type | Final URL |
|---|---|---|---|---|

### C1 · Service pages
| URL | Service name | H1 service variant | Status |
|---|---|---|---|
| /carpet-cleaning/ | Carpet Cleaning | home carpet cleaning | draft reviewed (pilot), awaiting drafts approval |

### C2 · Location pages
| URL | City | GBP landing page? | Status |
|---|---|---|---|
| /bluffton/ | Bluffton | No (the GBP landing page is the homepage) | draft reviewed (pilot), awaiting drafts approval |

Only a verified GBP's actual landing URL gets LocalBusiness-type schema (BB-604).

### C3 · Heading and FAQ registry
Every FAQ question and H2 live on the site, with the page that owns it. No question on two pages (BB-316).

| Question or H2 | Page that owns it |
|---|---|
| H2: How Do Professional Carpet Cleaners Clean a Carpet? | /carpet-cleaning/ |
| H2: Which Carpet Cleaning Services Does Carolina Carpet Cleaning Offer? | /carpet-cleaning/ |
| H2: What Do Lowcountry Homeowners Ask About a Carpet Cleaning Service? | /carpet-cleaning/ |
| H2: Which Towns Does Carolina Carpet Cleaning Serve? | /carpet-cleaning/ |
| FAQ: How much does it cost to have carpet professionally cleaned? | /carpet-cleaning/ |
| FAQ: How do I get brown stains out of my carpet? | /carpet-cleaning/ |
| FAQ: How long does carpet take to dry after cleaning? | /carpet-cleaning/ |
| FAQ: Is the cleaning solution safe for children and pets? | /carpet-cleaning/ |
| FAQ: How is low-moisture cleaning different from steam cleaning? | /carpet-cleaning/ |
| H2: What floor and fabric cleaning services are available in Bluffton? | /bluffton/ |
| H2: Why is carpet hard to keep fresh in Bluffton? | /bluffton/ |
| H2: How does Carolina Carpet Cleaning work in Bluffton? | /bluffton/ |
| H2: What do Bluffton homeowners ask about carpet cleaning? | /bluffton/ |
| H2: Which Bluffton neighborhoods does Carolina Carpet Cleaning serve? | /bluffton/ |
| H2: Which other South Carolina Lowcountry towns does Carolina Carpet Cleaning serve? | /bluffton/ |
| FAQ: Do HOA or gated-community rules in Bluffton change how a carpet cleaning visit is booked? | /bluffton/ |
| FAQ: How soon can a carpet cleaning be scheduled in Bluffton? | /bluffton/ |
| FAQ: Why do carpets in Bluffton homes smell musty in summer? | /bluffton/ |

## Section D — Verified facts
Everything a writer may state. **Not here = does not exist.**

| Fact | Value | Status | Source |
|---|---|---|---|
| Founding year / years in business | 1993 - operated locally as a family-owned business since 1993 | Client Confirmed 2026-10-28 · was: Submitted | Owner note, passed on by Paul 2026-10-28 — "'In Business Since 1993' (home); 'has served the South Carolina Lowcountry since 1993' (about); 'Founded in 1993' (press release). Domain registered 2019-11-12; SOS date not yet read." |
| Legal entity + DBA | Carolina Carpet Cleaning (DBA / trade name) | Client Confirmed 2026-10-28 · was: Unknown | Owner note, passed on by Paul 2026-10-28 |
| Licence numbers and classes | No current licence number provided | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Insurance / bonded status | General workmanship insurance | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Certifications, authorizations, factory training | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Association memberships | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Warranty terms | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Guarantees (response time, on-time, satisfaction) | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Awards and rankings | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0) | Disputed: client stated 6 Google reviews, all 5 stars (2026-10-28); the DataforSEO Google reviews pull shows rating 5 from 29 reviews (2022-04-18 to 2026-06-01), Birdeye also 29. [NEED: the figure exactly as Google shows it on the day, with the date — Paul records it (audit F-002)] | Disputed 2026-10-29 · was: Client Confirmed | Owner note 2026-10-28 vs DataforSEO reviews pull (data/reviews); audit F-002 |
| Team size / trucks / jobs completed | Kevin is the team; one truck; thousands of jobs completed | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Financing — available, provider, terms | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Free estimate — and what free means | Free estimate; no deposit to schedule | Client Confirmed 2026-10-28 · was: Submitted | Owner note, 2026-10-28 — "No deposit is required to schedule an appointment" |
| Emergency / after-hours reality | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Minimum service call or trip charge | N/A | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Payment methods | Normal payment methods | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Services subcontracted out | Not subcontracted out | Client Confirmed 2026-10-28 · was: Unknown | Owner note, 2026-10-28 |
| Named staff for on-page use | Kevin Snow (owner) | Client Confirmed 2026-10-28 · was: Submitted | Owner note, 2026-10-28 — "Contact Info: Name: Kevin Snow; 'you're getting the owner on every job'" |
| Licensed practitioner for health-claim sign-off *(medical / chiropractic)* | | | |
| Blog author — a real person (CM-039; from the Decision Sheet) | Kevin Snow (owner) | Paul Approved 2026-10-28 · was: Unknown | Paul, chat 2026-10-28: Kevin Snow confirmed as author |
| GBP link | https://maps.app.goo.gl/vvsrqH6TxL815KWB6 | Paul Approved 2026-10-28 · was: Unknown | Paul, chat 2026-10-28 |
| GA4 access | none | Paul Approved 2026-10-28 · was: Unknown | Paul, chat 2026-10-28 |
| Drying time | Carpets dry in under one hour on a typical job | Paul Approved 2026-10-29 · was: Unknown | Paul, audit review 2026-10-29 (F-005, decision fact_drying_time) |
| Cleaning solution — safety claims | pH-neutral, biodegradable, non-toxic; safe for pets and children (owner's claims; product names not recorded) | Paul Approved 2026-10-29 · was: Unknown | Paul, audit review 2026-10-29 (F-006, decision fact_cleaning_solution_product) |
| Quality commitment (not a guarantee) | The owner commits to quality cleaning at a reasonable price; no refund, warranty or satisfaction guarantee is offered | Paul Approved 2026-10-29 · was: Unknown | Paul, audit review 2026-10-29 (F-004, decision audit-f004-keep-quality-sentence) |
| Section G positioning lines (owner's words) | Skipped — Paul chose to leave question 25 unanswered; no owner words recorded | Unknown 2026-10-29 | Paul, chat 2026-10-29 (answer 3) |

### D2 · Unsupported claims
Claims the site makes publicly that the client could not substantiate. Writers must not repeat
them; the content-risk list tracks where they are live.

| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|
| "$2 to $5 per square foot … $160 to $400" (rug-cleaning price range) | /3-reasons-why-you-should-try-a-professional-carbonated-cleaning-service-for-your-oriental-rug/ | No price given; pricing not in Section D | Do not repeat; remove (audit F-023, decided) |
| "our personnel is highly-trained and insured" | /if-you-dont-hire-a-carpet-cleaning-company-now-youll-regret-it-later/ | Team = Kevin alone; insurance = general workmanship; no certifications or training (N/A) | Do not repeat "personnel"/"highly-trained"; remove (audit F-023, decided) |
| "Call (843) 525-6288" (homepage hero button, tel:8435256288) | / | Approved phone is (843) 575-6286 | Never use 525-6288; fix (audit F-001) |
| Any review count other than Google's figure on the day | homepage testimonials (F-029) | Client said 6; Google data shows 29 (F-002) | No page states a count until Paul records the Google figure |

### D3 · Content-risk list
Every live page that still carries a D2 claim or an unconfirmed fact, until it is rebuilt or corrected.

| Page URL | Claim or fact | Source (D2 row / audit finding) | Fixed by (batch or handoff) |
|---|---|---|---|
| https://carpetcleaningblufftonsc.com/ | Hero button calls (843) 525-6288; second tel: link malformed | D2 row 3 / F-001 | H-2026-10-29-02-broken_link (issued) |
| https://carpetcleaningblufftonsc.com/3-reasons-why-you-should-try-a-professional-carbonated-cleaning-service-for-your-oriental-rug/ | Rug-cleaning price range | D2 row 1 / F-023 | [NEED: VA content-edit handoff — not issued yet] |
| https://carpetcleaningblufftonsc.com/if-you-dont-hire-a-carpet-cleaning-company-now-youll-regret-it-later/ | "personnel is highly-trained and insured" | D2 row 2 / F-023 | [NEED: VA content-edit handoff — not issued yet] |
| https://carpetcleaningblufftonsc.com/about/ | "carolina carpet cleaning of the midlands" brand confusion (another company) | F-003 | Build — About and homepage rebuild |

## Section E — Service area truth
```
TOWNS AT THE EDGES (the furthest towns served, any direction): Beaufort and Lady's Island (north/east) · Ridgeland (north-west) · Hardeeville (south-west) · Hilton Head Island (south-east). Six towns served: Hilton Head Island, Bluffton, Beaufort, Ridgeland, Hardeeville, Lady's Island (Paul Approved 2026-10-28, towns_served; client answer 2026-10-28). Address 273 Club Gate, Bluffton, SC 29910 (website only; SAB).
CITIES CLAIMED ON SITE: the 6 published location pages above. Live page text also names Okatie, Port Royal, Daufuskie, Sun City and Savannah, GA (Savannah = the 3 "Know the Area" posts, F-009, Blog Decision Map); the homepage once named 18 towns — the other 12 are not kept for now (settled towns_served).
EXPLICIT EXCLUSIONS: none stated by the client. Towns outside the six are not written as served (settled); Savannah, GA is outside the settled area.
TRAVEL FEE BEYOND: [NEED: whether a travel fee applies outside the six towns, and from where — client did not say; "Minimum service call or trip charge" = N/A]
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
| **Wikidata URI — category entity** | https://www.wikidata.org/wiki/Q5045777 (carpet cleaning) — proposed, pending the GBP primary category | Submitted 2026-10-28 |
| **Wikidata URI — area entity** | https://www.wikidata.org/wiki/Q17020871 (Hilton Head Island metropolitan area) — proposed; alternative Q3885311 (South Carolina Lowcountry) | Submitted 2026-10-28 |
| **Wikidata URI — county** (one per county the area entity covers) | https://www.wikidata.org/wiki/Q495682 (Beaufort County) · https://www.wikidata.org/wiki/Q112957 (Jasper County) · [Q497880 Hampton County only if the area entity is the Lowcountry] | Submitted 2026-10-28 |
| **Wikidata URI — state** | https://www.wikidata.org/wiki/Q1456 (South Carolina) | Submitted 2026-10-28 |

## Section G — Positioning (client's own words)
```
WHAT WE DO THAT OTHERS HERE DO NOT: [NEED: the owner's own words — not on the returned answers (question 25 blank). Section D supports: owner-operated (Kevin is the team, one truck), family-owned since 1993, carpets dry in under one hour on a typical job]
JOB WE MOST WANT MORE OF: [NEED: the owner's own words — not on the returned answers]
MOST COMMON THING CUSTOMERS GET WRONG ABOUT THIS TRADE: [NEED: the owner's own words — not on the returned answers]
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

## Updates since approval
*Changes Paul made after approving this guide (CM-066). A line here overrides any earlier text in the guide on the same point; his approval stands.*

- Updated 2026-10-29 · Drying time — was new → now Paul Approved: Carpets dry in under one hour on a typical job (source: Paul, audit review 2026-10-29 (F-005, decision fact_drying_time); by discovery agent)
- Updated 2026-10-29 · Cleaning solution — safety claims — was new → now Paul Approved: pH-neutral, biodegradable, non-toxic; safe for pets and children (owner's claims; product names not recorded) (source: Paul, audit review 2026-10-29 (F-006, decision fact_cleaning_solution_product); by discovery agent)
- Updated 2026-10-29 · Quality commitment (not a guarantee) — was new → now Paul Approved: The owner commits to quality cleaning at a reasonable price; no refund, warranty or satisfaction guarantee is offered (source: Paul, audit review 2026-10-29 (F-004, decision audit-f004-keep-quality-sentence); by discovery agent)
- Updated 2026-10-29 · Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0) — was Client Confirmed: 6 Google reviews, all 5 stars (as of 2026-10-28; client-stated, re-check on Goog → now Disputed: Disputed: client stated 6 Google reviews, all 5 stars (2026-10-28); the DataforSEO Google reviews pull shows rating 5 from 29 reviews (2022-04-18 to 2026-06-01) (source: Owner note 2026-10-28 vs DataforSEO reviews pull (data/reviews); audit F-002; by discovery agent)
- Updated 2026-10-29 · Travel fee beyond the six towns — was new → now Paul Approved: None — no travel fee (source: Paul, chat 2026-10-29 (answer 2); by Paul)
- Updated 2026-10-29 · Section G positioning lines (owner's words) — was new → now Unknown: Skipped — Paul chose to leave question 25 unanswered; no owner words recorded (source: Paul, chat 2026-10-29 (answer 3); by Paul)

## Maintenance

| When | Action |
|---|---|
| Page content approved (SD/LD) | Add its row to B3 and C1/C2, its FAQ questions and H2s to C3 |
| New citation built | Add to Section F and sameAs |
| GBP primary category changes | Rebuild Sections A and B — entity gate re-opens |
| Any field moves status | Update in place. Never keep two versions |
