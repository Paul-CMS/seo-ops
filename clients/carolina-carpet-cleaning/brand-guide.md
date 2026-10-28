# [Client Name] - Brand Guide
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
| 1 | Brand entity (GBP name, exactly) | Carolina Carpet Cleaning | Submitted 2026-10-28 · was: Unknown |
| 2 | GBP primary category = the category entity | Proposed: Carpet cleaning service → Wikipedia 'Carpet cleaning' (Q5045777). GBP primary category not yet read (dashboard/Maps not machine-readable; Gwen manual lookup) | Submitted 2026-10-28 · was: Unknown |
| 3 | Category variants (4–6) | Proposed: carpet cleaning · carpet cleaning service · carpet cleaners · carpet cleaning company · carpet cleaner (search volume checked in the data step) | Submitted 2026-10-28 · was: Unknown |
| 4 | Storefront or SAB | SAB (service-area business); the address still appears on the website (helps map rankings) | Paul Approved 2026-10-28 · was: Unknown |
| 5 | Area entity | Hilton Head Island metropolitan area | Paul Approved 2026-10-28 · was: Submitted |
| 6 | Area variants (3–5) | SEO titles: Hilton Head Island Metro Area · user-facing titles and homepage H1: South Carolina Lowcountry | Paul Approved 2026-10-28 · was: Submitted |
| 7 | Separator standard | ' - ' | Submitted 2026-10-28 · was: Unknown |
| 8 | Phone | (843) 575-6286 | Paul Approved 2026-10-28 · was: Disputed |
| 9 | Primary domain (canonical host form) | https://carpetcleaningblufftonsc.com/ (http and www 301 to it; rel=canonical matches) | Internally Verified 2026-10-28 · was: Unknown |
| 10 | Legal entity name | | |
| 11 | Exact URL in the GBP Website field | https://carpetcleaningblufftonsc.com/ | Paul Approved 2026-10-28 · was: Unknown |
| | Facebook page (Beaufort) | https://www.facebook.com/carpetcleaningbeaufortsc | Paul Approved 2026-10-28 · was: Unknown |

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
| Founding year / years in business | 1993 (claimed) | Submitted 2026-10-28 · was: Unknown | https://carpetcleaningblufftonsc.com/ ; https://carpetcleaningblufftonsc.com/about/ ; press release 2026-04-30 (marketersmedia) — "'In Business Since 1993' (home); 'has served the South Carolina Lowcountry since 1993' (about); 'Founded in 1993' (press release). Domain registered 2019-11-12; SOS date not yet read." |
| Legal entity + DBA | | | |
| Licence numbers and classes | | | |
| Insurance / bonded status | | | |
| Certifications, authorizations, factory training | | | |
| Association memberships | | | |
| Warranty terms | | | |
| Guarantees (response time, on-time, satisfaction) | | | |
| Awards and rankings | | | |
| Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0) | | | |
| Team size / trucks / jobs completed | | | |
| Financing — available, provider, terms | | | |
| Free estimate — and what free means | Free estimate before work begins; no deposit to schedule (what 'free' covers not stated) | Submitted 2026-10-28 · was: Unknown | https://carpetcleaningblufftonsc.com/ — "No deposit is required to schedule an appointment" |
| Emergency / after-hours reality | | | |
| Minimum service call or trip charge | | | |
| Payment methods | | | |
| Services subcontracted out | | | |
| Named staff for on-page use | Kevin Snow (owner, per press release contact; reviews name 'Kevin') | Submitted 2026-10-28 · was: Unknown | press release 2026-04-30 https://news.marketersmedia.com/carolina-carpet-cleaning-celebrates-32-years-of-professional-floor-and-carpet-cleaning-in-bluffton-and-the-lowcountry/89190379 ; About page image file Owner-Kevin-Snow — "Contact Info: Name: Kevin Snow; 'you're getting the owner on every job'" |
| Licensed practitioner for health-claim sign-off *(medical / chiropractic)* | | | |
| Blog author — a real person (CM-039; from the Decision Sheet) | | | |
| GBP link | https://maps.app.goo.gl/vvsrqH6TxL815KWB6 | Paul Approved 2026-10-28 · was: Unknown | Paul, chat 2026-10-28 |
| GA4 access | none | Paul Approved 2026-10-28 · was: Unknown | Paul, chat 2026-10-28 |

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
| **Wikidata URI — category entity** | https://www.wikidata.org/wiki/Q5045777 (carpet cleaning) — proposed, pending the GBP primary category | Submitted 2026-10-28 |
| **Wikidata URI — area entity** | https://www.wikidata.org/wiki/Q17020871 (Hilton Head Island metropolitan area) — proposed; alternative Q3885311 (South Carolina Lowcountry) | Submitted 2026-10-28 |
| **Wikidata URI — county** (one per county the area entity covers) | https://www.wikidata.org/wiki/Q495682 (Beaufort County) · https://www.wikidata.org/wiki/Q112957 (Jasper County) · [Q497880 Hampton County only if the area entity is the Lowcountry] | Submitted 2026-10-28 |
| **Wikidata URI — state** | https://www.wikidata.org/wiki/Q1456 (South Carolina) | Submitted 2026-10-28 |

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
