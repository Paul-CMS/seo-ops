# Gettysburg Mold Remediation Pros - Brand Guide
### The single business-truth record. Every agent reads it; the Build agent writes back to it.
Repo working copy: `clients/gettysburg-mold-remediation-pros/brand-guide.md` · mirrored to `Gettysburg Mold Remediation Pros - TMS/Gettysburg Mold Remediation Pros - Brand Guide.md`

## Field status values

`Submitted` · `Internally Verified` · `Client Confirmed` · `Disputed` · `Unknown` · `Paul Approved`

**A field at `Unknown` or `Disputed` blocks whatever consumes it.** Writers write
`[NEED: ...]` instead of inventing (CM-016). `Submitted` may appear in a draft but blocks
publication.

---

## Section A — Entity foundation  *(Paul approves: gate entity_approved)*

| # | Field | Value | Status |
|---|---|---|---|
*Proposals from the Discovery Record (run 20261003-160508-discovery-552a, 2026-10-03). Nothing here is approved until Paul's `/approve … entity_approved`.*

| # | Field | Value | Status |
|---|---|---|---|
| 1 | Brand entity (GBP name, exactly) | Gettysburg Mold Remediation Pros — **no GBP exists**; name as used on the site and at intake | Submitted |
| 2 | GBP primary category = the category entity | **No GBP (OPEN, Q-01).** Proposed: **Mold remediation** (Wikipedia "Mold remediation" → Indoor mold, Remediation section; Wikidata Q97609893). Alternatives: Water damage restoration (→ Water damage, Q19289049); Indoor air quality (Q905504) | Unknown — Paul decides |
| 3 | Category variants (4–6) | Mold remediation · Mold growth, assessment, and remediation · Indoor mold remediation `[NEED: Paul — BB-109]` · Mold removal `[NEED: Paul — no Wikipedia title]` | Submitted |
| 4 | Storefront or SAB | SAB (Paul intake) — **Disputed by the site's presentation**: "Our own building, in the borough. Not a call center." (/contact/) (C-01) | Disputed |
| 5 | Area entity | Proposed: **South Central Pennsylvania** (Q7566771) — contains 5 of 6 cities (not Taneytown, MD). Strict BB-105 result: Mid-Atlantic (United States) (Q632014) (Q-02) | Unknown — Paul decides |
| 6 | Area variants (3–5) | South Central Pennsylvania · Harrisburg–York–Lebanon combined statistical area · Adams County, Pennsylvania · Gettysburg, PA Metropolitan Statistical Area · Gettysburg | Submitted |
| 7 | Separator standard | ` - ` | |
| 8 | Phone | (267) 828-9088 (site, every page) — `[NEED: client confirms it is the permanent business number]` | Submitted |
| 9 | Primary domain (canonical host form) | https://gettysburgpamoldremediationpros.com/ (canonical on homepage; http and www forms not verified here) | Submitted |
| 10 | Legal entity name | `[NEED: PA Department of State search — portal blocked automated access]` | Unknown |
| 11 | Exact URL in the GBP Website field | n/a — no GBP | Unknown |

**Area entity derivation** (BB-105) — record the path, not just the answer:

```
City served:  Gettysburg, Pennsylvania (Q694550) — borough, county seat of Adams County
-> County:    Adams County, Pennsylvania (Q351865) = Gettysburg, PA MSA (Q123332714) — contains Hanover/Taneytown? NO
-> Region:    South Central Pennsylvania (Q7566771) / Harrisburg–York–Lebanon CSA (Q18153388) — Adams + York
              — contains Taneytown (Carroll County, MD, Q501323)? NO
-> Region:    Mid-Atlantic (United States) (Q632014) — contains all? YES
Contains all 6 cities served? South Central PA: no (5 of 6) · Mid-Atlantic: yes
Smallest true container: Mid-Atlantic (strict BB-105). Proposed for Paul: South Central Pennsylvania, conditional on
Taneytown, MD being outside the homepage area statement (open question Q-02).
Cities: Gettysburg, Littlestown, New Oxford, Carroll Valley (Adams PA) · Hanover (York PA) · Taneytown (Carroll MD)
```

**Paul approved this section on:** ____________

## Section B — Variant ownership  *(CM-024: collisions are vertical, not horizontal)*

### B1 · Reserved for the homepage
```
HOMEPAGE AREA VARIANT:      South Central Pennsylvania [Submitted — proposal, depends on Q-02]
HOMEPAGE CATEGORY VARIANT:  Mold Remediation [Submitted — proposal, depends on Q-01]
```
No other page may claim the reserved area variant. This is the only cross-page variant rule.

### B2 · Rotation pool
Every area variant except the reserved one. Reuse across service pages is correct.
```
1. Harrisburg–York–Lebanon combined statistical area   [Submitted]
2. Adams County, Pennsylvania                           [Submitted]
3. Gettysburg, PA Metropolitan Statistical Area         [Submitted]
4. Gettysburg                                           [Submitted]
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
| **Wikidata URI — category entity** | https://www.wikidata.org/wiki/Q97609893 (mold remediation) — proposal; alt Q6895739 (enwiki "Indoor mold") | Submitted |
| **Wikidata URI — area entity** | https://www.wikidata.org/wiki/Q7566771 (South Central Pennsylvania) — proposal; strict BB-105 alt Q632014 (Mid-Atlantic) | Submitted |
| **Wikidata URI — county** | https://www.wikidata.org/wiki/Q351865 (Adams County, PA); also served: Q490914 (York County, PA), Q501323 (Carroll County, MD) | Submitted |
| **Wikidata URI — state** | https://www.wikidata.org/wiki/Q1400 (Pennsylvania); Taneytown: Q1391 (Maryland) | Submitted |

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
