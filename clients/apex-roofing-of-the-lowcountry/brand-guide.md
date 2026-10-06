# Apex Roofing of the Lowcountry - Brand Guide
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
| 1 | Brand entity (GBP name, exactly) | Apex Roofing of the Lowcountry | Proposed (Discovery 2026-10-05) — awaits entity_approved · name forms differ across sources (Discovery Record C5) |
| 2 | GBP primary category = the category entity | Roofing contractor — Wikipedia: https://en.wikipedia.org/wiki/Roofer (lead names "roofing contractor") | Proposed (Discovery 2026-10-05) — awaits entity_approved · secondary categories Unknown `[NEED]` |
| 3 | Category variants (4–6) | Roofing Contractor · Roofer · Roofers (all Wikipedia). Excluded by Paul 2026-10-05: Roof Mechanic. Candidate only, not approved: Residential Roofer (site wording, not Wikipedia; see C4) | Revised per Paul 2026-10-05 — awaits entity_approved · 3 variants, below the template's 4–6 |
| 4 | Storefront or SAB | SAB (intake; no address on the public GBP) | Internally Verified |
| 5 | Area entity | Hilton Head Island–Bluffton–Port Royal, SC Metropolitan Statistical Area — Wikipedia: https://en.wikipedia.org/wiki/Hilton_Head_Island_metropolitan_area | Revised per Paul 2026-10-05 (2nd) — awaits entity_approved · the brand name already carries "Lowcountry" into every SEO title, so the SEO title takes the metro area · BB-105 smallest container · Georgia not served (Paul 2026-10-05, C1) |
| 6 | Area variants (3–5) | Hilton Head Island–Bluffton–Port Royal Metropolitan Area (reserved, homepage) · South Carolina Lowcountry · Lowcountry · Hilton Head Island Metropolitan Area · Beaufort and Jasper Counties | Revised per Paul 2026-10-05 (2nd) — awaits entity_approved · "Lowcountry" variants never in an SEO title (see B2) |
| 7 | Separator standard | ` - ` | Standard |
| 8 | Phone | (843) 757-2739 (GBP, site, BBB, HomeAdvisor) | Submitted — client to confirm it is not a tracking number |
| 9 | Primary domain (canonical host form) | https://apexroofingtlc.com/ (www and http forms 301 here in one hop) | Internally Verified |
| 10 | Legal entity name | APEX ROOFING OF THE LOWCOUNTRY LLC (SC no. 493170, Good Standing — OpenCorporates copy; SOS primary not read, CAPTCHA) | Submitted `[NEED: SOS primary check]` |
| 11 | Exact URL in the GBP Website field | http://www.apexroofingtlc.com/ (as recorded by Paul at intake) | Submitted |

**Area entity derivation** (BB-105) — record the path, not just the answer:

```
City served:  Bluffton, SC ("a town in southern Beaufort County")
-> County:    Beaufort County, SC ("part of the Hilton Head Island-Bluffton-Port Royal metropolitan statistical area")
-> Metro:     Hilton Head Island–Bluffton–Port Royal, SC MSA = Beaufort + Jasper counties
-> Region:    South Carolina Lowcountry ("The area includes the Hilton Head Island-Bluffton-Beaufort, SC
              Metropolitan Statistical Area"; most common definition: Charleston, Dorchester, Beaufort,
              Georgetown, Colleton, Hampton, Berkeley, Jasper and Williamsburg counties)
Contains all 12 cities served? yes — Bluffton, Hilton Head Island, Beaufort, Okatie, Hardeeville, Lady's Island,
              Port Royal, Fripp Island, St. Helena Island, Pritchardville, Levy, Ridgeland (all Beaufort/Jasper)
              — Georgia is not served (Paul, 2026-10-05; Discovery Record C1)
Smallest true container: Hilton Head Island–Bluffton–Port Royal, SC MSA
Area entity chosen:      Hilton Head Island–Bluffton–Port Royal, SC MSA (Paul, 2026-10-05, second revision —
                         replaces South Carolina Lowcountry: "Lowcountry" is already in the brand name, which is in
                         every SEO title). South Carolina Lowcountry stays a variant (the region the MSA sits in).
```
Source: `discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md` §3 and "Paul's direction, 2026-10-05".

**Paul approved this section on:** ____________

## Section B — Variant ownership  *(CM-024: collisions are vertical, not horizontal)*

### B1 · Reserved for the homepage
```
HOMEPAGE AREA VARIANT:      Hilton Head Island–Bluffton–Port Royal Metropolitan Area [Revised per Paul 2026-10-05 (2nd) — awaits entity_approved]
HOMEPAGE CATEGORY VARIANT:  Roofing Contractor                                       [Proposed — awaits entity_approved]
```
The homepage SEO title carries this variant. "Lowcountry" can't be reserved: the brand name
("Apex Roofing of the Lowcountry") already carries it onto every page.
No other page may claim the reserved area variant. This is the only cross-page variant rule.

### B2 · Rotation pool
Every area variant except the reserved one. Reuse across service pages is correct.
```
1. South Carolina Lowcountry                        [Revised per Paul 2026-10-05 (2nd)]
2. Lowcountry                                       [Revised per Paul 2026-10-05]
3. Hilton Head Island Metropolitan Area              [Proposed]
4. Beaufort and Jasper Counties                      [Proposed]
```
**SEO titles (Paul, 2026-10-05):** the brand is in every SEO title and already says "Lowcountry", so
variants 1 and 2 are never used in an SEO title — only in the H1, H2s and body. SEO titles take the
metro-area, Hilton Head Island Metropolitan Area or county variants.

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
| Founding year / years in business | | | |
| Legal entity + DBA | | | |
| Licence numbers and classes | | | |
| Insurance / bonded status | | | |
| Certifications, authorizations, factory training | | | |
| Association memberships | | | |
| Warranty terms | | | |
| Guarantees (response time, on-time, satisfaction) | | | |
| Awards and rankings | | | |
| Google rating and review count (date checked) | | | |
| Team size / trucks / jobs completed | | | |
| Financing — available, provider, terms | | | |
| Free estimate — and what free means | | | |
| Emergency / after-hours reality | | | |
| Minimum service call or trip charge | | | |
| Payment methods | | | |
| Services subcontracted out | | | |
| Named staff for on-page use | | | |
| Licensed practitioner for health-claim sign-off *(medical / chiropractic)* | | | |

### D2 · Unsupported claims
Claims the site makes publicly that the client could not substantiate. Writers must not repeat
them; the content-risk list tracks where they are live.

| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|

## Section E — Service area truth
```
FURTHEST NORTH:            FURTHEST SOUTH:
FURTHEST EAST:             FURTHEST WEST:
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
| **Wikidata URI — category entity** | http://www.wikidata.org/entity/Q552378 (roofer) | Proposed |
| **Wikidata URI — area entity** | http://www.wikidata.org/entity/Q17020871 (Hilton Head Island–Bluffton–Port Royal MSA) — region it sits in, if used: http://www.wikidata.org/entity/Q3885311 (South Carolina Lowcountry) | Proposed |
| **Wikidata URI — county** | http://www.wikidata.org/entity/Q495682 (Beaufort) · http://www.wikidata.org/entity/Q112957 (Jasper) — Paul picks one or both | Proposed |
| **Wikidata URI — state** | http://www.wikidata.org/entity/Q1456 | Proposed |

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
