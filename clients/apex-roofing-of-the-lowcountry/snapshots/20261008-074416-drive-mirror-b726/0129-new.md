# Apex Roofing of the Lowcountry - Discovery Record - REVIEW

**Client:** Apex Roofing of the Lowcountry · **Slug:** apex-roofing-of-the-lowcountry · **Site:** https://apexroofingtlc.com/
**Run:** 20261005-211303-discovery-aee7 · **Steps:** S01 intake facts · S02 public sources · S03 entity foundation
**Date checked:** 2026-10-05 · **Prepared by:** Agent 1 (Discovery and Audit) · **Status:** REVIEW — awaiting Paul (`entity_approved`)

> Discovery records observations and questions only. Nothing here is a finding, a severity, a priority or a
> recommendation — those belong to the audit (S12–S18). Conflicts are recorded with every candidate value and are
> **not resolved** here (PROC-01, GOV-06 §5). Missing facts are written `[NEED: …]` (CM-016).
> Rules are cited by ID (BB-105, BB-106, BB-107, BB-109, BB-110, CM-016, CM-024, PROC-01).

Confidence legend (client-intake `discovery.md`): `verified` = government record or authoritative third party ·
`found` = the business states it publicly (or a non-primary copy of a record) · `inferred` = reasoned, marked as such ·
`unknown` = checked, nothing found.

---

## 1 · S01 — Intake facts (status.json, recorded by Paul 2026-10-05)

| Fact | Value | Source |
|---|---|---|
| Client name | Apex Roofing of the Lowcountry | status.json |
| Industry / type | Roofing · full client · not sensitive | status.json |
| Site | https://apexroofingtlc.com/ | status.json |
| GBP link | https://maps.app.goo.gl/AWfz3YNkwvsrggFg7 | status.json |
| GBP type | Service-area business (SAB) | status.json (Paul) — consistent with the public listing showing no street address (§2.1) |
| GBP Website field | `http://www.apexroofingtlc.com/` | status.json (Paul) |
| Search Console / GA4 | No access | status.json |
| CMS | WordPress · Kadence theme · Kadence Blocks + Pro · WPForms · AccelerateWP | public homepage source |

Nothing was missing for S01.

---

## 2 · S02 — Public sources

### 2.1 Google Business Profile (public Maps view, limited — not signed in)

Resolved link: `https://maps.app.goo.gl/AWfz3YNkwvsrggFg7` → place ID `0x88fb8ecb91119aeb:0x75fdd2b798249104`,
Knowledge Graph ID `/g/11clmtnn2t`. The site's "Open in Maps" link (`https://maps.app.goo.gl/wEEeaFamtyAZLnnD9`)
resolves to the **same** place ID.

| Field | Observed (verbatim) | Confidence |
|---|---|---|
| Name | "Apex Roofing of the Lowcountry" | found (GBP) |
| Primary category (as displayed) | "Roofing contractor" | found (GBP) |
| Secondary categories | not shown in the limited public view — `[NEED: GBP secondary categories, from the GBP dashboard or the client]` | unknown |
| Rating / count | "5.0" · "67 reviews" (2026-10-05) | found (GBP) |
| Phone | "(843) 757-2739" | found (GBP) |
| Website (displayed) | "apexroofingtlc.com" (Paul recorded the field value as `http://www.apexroofingtlc.com/`) | found (GBP) |
| Address | none displayed (consistent with SAB) | inferred |
| Hours | Monday–Saturday "8 AM to 5 PM"; Sunday "Closed" | found (GBP) |
| Service areas | not shown in the limited view — `[NEED: GBP service-area list]` | unknown |
| Open date | not shown — `[NEED: GBP opening date]` | unknown |
| Photos | "12 Photos" | found (GBP) |
| Owner posts | active — latest "1 day ago" (2026-10-04); it says Apex "provides residential and commercial roof inspections throughout the Lowcountry" | found (GBP) |
| Review topics (Google's tags) | "answering questions" (12), "timely completion" (8), "efficient crew" (6), "underlayment" (5), "new roof installation" (4), "competitive pricing" (4), others | found (GBP) |
| Owner response to reviews | yes (observed on recent reviews) | found (GBP) |
| Names in reviews | recent reviews name "Ralph" as owner and "his son Pierce" (reviewer names not recorded) | found (reviews — never a verified fact, CM-027) |

**Duplicate-listing check (partial):** a Maps search for "Apex Roofing Bluffton SC" returned this single listing directly.
A full duplicate sweep (old addresses, former names, a listing made by a previous agency) was not possible in the limited view.

### 2.2 Live website (crawled pages come later — this is a public read of the pages in the sitemap)

**Hosts:** `http://www.apexroofingtlc.com/`, `https://www.apexroofingtlc.com/` and `http://apexroofingtlc.com/` each
**301 in one hop** to `https://apexroofingtlc.com/` (observation only). Canonical host form: `https://apexroofingtlc.com/`.

**Inventory from the XML sitemaps** (`/page-sitemap1.xml`, `/post-sitemap1.xml`): 29 page URLs and 34 post URLs
(incl. `/blog/`). Pages: home, 8 service pages, 12 location pages, about, contact, blog, terms + 4 policy pages.

| Type | URLs |
|---|---|
| Service (8) | `/roof-repair/` · `/roof-replacement/` · `/roof-installation/` · `/roof-inspections/` · `/emergency-roof-repair/` · `/metal-roofing-2/` · `/slate-roofing/` · `/skylights/` |
| Location (12) | `/bluffton/` · `/hilton-head-island/` · `/beaufort/` · `/okatie/` · `/hardeeville/` · `/ladys-island/` · `/port-royal/` · `/fripp-island/` · `/st-helena-island/` · `/pritchardville/` · `/levy/` · `/ridgeland/` |

**Current entity signals on the site (observations):**

| Element | Verbatim | URL |
|---|---|---|
| Homepage title | "Apex Roofing of the Lowcountry - Roofing Contractor - Hilton Head Island Metro Area" | https://apexroofingtlc.com/ |
| Homepage H1 | "The Best Residential Roofer in the South Carolina Lowcountry" | https://apexroofingtlc.com/ |
| Service titles | pattern "Apex Roofing of the Lowcountry - [Service] - Hilton Head Island Metro Area" (all 8) | service pages |
| Location titles | pattern "Apex Roofing of the Lowcountry - Roofing Contractor - [City], South Carolina" (all 12) | location pages |
| Area wording in body | "the surrounding communities of the Hilton Head Island-Bluffton, SC Metropolitan Statistical Area" | https://apexroofingtlc.com/ |
| Footer NAP | "Apex Roofing of the Lowcountry / Bluffton, SC 29910 / United States" · "(843) 757-2739" (no street) | all pages |
| Phone (all pages) | (843) 757-2739 — `tel:8437572739` (homepage also has `tel:%208437572739`) | site-wide |
| Email | none published | — |
| Schema | homepage: one `WebSite` node only; no JSON-LD found on the other 23 pages read | site-wide |
| Footer credit | "Powered By Tampa Bay SEO" (links to tampabayseoexperts.com) | site-wide |
| Social | Facebook only: https://www.facebook.com/ApexRoofingTLC/ | footer |
| Recognition badges (image file names only, empty alt) | HomeAdvisor 20 Reviews · HomeAdvisor 1 Year · Screened and Approved HomeAdvisor Roofer · Elite Service Provider · Top Rated Roofer · Best of 2018 Roofer (uploaded 2023/11) | https://apexroofingtlc.com/ |

**Public factual claims (self-reported — `found`):**

| # | Claim (verbatim) | URL |
|---|---|---|
| W1 | "Founded by Ralph and Pierce Brehany" | https://apexroofingtlc.com/ |
| W2 | "since the company was founded here over a decade ago" | https://apexroofingtlc.com/bluffton/ |
| W3 | "CertainTeed ShingleMaster certified. SC License #57706." | https://apexroofingtlc.com/ |
| W4 | "We hold South Carolina License #57706 and Town of Bluffton License #0620033323." | https://apexroofingtlc.com/ |
| W5 | "holds South Carolina State License #57706 issued by the SC Department of Labor, Licensing and Regulation, which is valid statewide" | https://apexroofingtlc.com/hardeeville/ |
| W6 | "a licensed residential roofing contractor" | https://apexroofingtlc.com/ |
| W7 | "providing top-tier roofing solutions for homes and businesses" | https://apexroofingtlc.com/about/ |
| W8 | "Serving the South Carolina Lowcountry & Coastal Georgia" | https://apexroofingtlc.com/ |
| W9 | "We have completed projects in Sun City, Sea Pines, Palmetto Dunes, Hilton Head Plantation, Palmetto Bluff, Colleton River Plantation, Moss Creek, and Belfair." | https://apexroofingtlc.com/ |
| W10 | "Every estimate is free. Every project is documented photographically from start to finish." | https://apexroofingtlc.com/ |
| W11 | "CertainTeed or GAF shingles, corrosion-resistant flashings, synthetic underlayment" | https://apexroofingtlc.com/ |
| W12 | "which allows us to offer the SureStart PLUS extended warranty covering both material and labor" | https://apexroofingtlc.com/roof-replacement/ |
| W13 | "All workmanship is separately guaranteed by Apex Roofing of the Lowcountry." (no term stated) | https://apexroofingtlc.com/roof-replacement/ |
| W14 | "Kynar 500 and Hylar 5000 coated panels that carry a 40-year warranty against chalking and fading" | https://apexroofingtlc.com/roof-replacement/ |
| W15 | "We carry full general liability and workers compensation insurance" | https://apexroofingtlc.com/roof-installation/ |
| W16 | "We work as a roofing subcontractor on new construction projects throughout Beaufort and Jasper County." | https://apexroofingtlc.com/roof-installation/ |
| W17 | "Pre-estimate inspections … are always free. Independent inspection reports … are priced separately." | https://apexroofingtlc.com/roof-inspections/ |
| W18 | "We install Velux and FAKRO units" | https://apexroofingtlc.com/skylights/ |
| W19 | Natural slate "typically ranges from $35,000 to $70,000 or more"; synthetic "$18,000 to $35,000" | https://apexroofingtlc.com/slate-roofing/ |
| W20 | Standing seam "expect $22,000 to $40,000 … versus $9,000 to $18,000 for shingles" | https://apexroofingtlc.com/metal-roofing-2/ |
| W21 | "Bluffton-area clients are typically our first response given our base of operations." | https://apexroofingtlc.com/emergency-roof-repair/ |
| W22 | "Many homeowners in rural Beaufort County … benefit from payment arrangements." | https://apexroofingtlc.com/levy/ |
| W23 | "we don't apply a premium rate in Ridgeland that we would charge on Hilton Head Island" | https://apexroofingtlc.com/ridgeland/ |
| W24 | "Our operations are handled by our in-house team" | https://apexroofingtlc.com/about/ |
| W25 | "Ralph or Pierce will schedule a site visit and get on your roof personally." | https://apexroofingtlc.com/ |
| W26 | "Levy and the broader Gardens Corner corridor sit in an area of Beaufort County" | https://apexroofingtlc.com/levy/ |
| W27 | "Okatie is a largely unincorporated community in Beaufort County" | https://apexroofingtlc.com/okatie/ |
| W28 | Cities in the closing CTA: "Bluffton, Hilton Head Island, Beaufort, Hardeeville, Okatie, Ladys Island, Port Royal, Fripp Island, St. Helena Island, Pritchardville, Levy, Palmetto Bluff, and Ridgeland" | all service pages, about |

### 2.3 Secretary of State (SC)

The SC Secretary of State Business Entities Online search (https://businessfilings.sc.gov/BusinessFiling/Entity/Search)
requires a CAPTCHA, which the system does not complete. **The primary record was not read.** A public copy of the
registry record was read on OpenCorporates (a secondary source — confidence `found`, not `verified`):

| Field | Value (verbatim) | Source |
|---|---|---|
| Legal name | "APEX ROOFING OF THE LOWCOUNTRY LLC" | https://opencorporates.com/companies/us_sc/493170 |
| Company number | "493170" (previous: "782709") | same |
| Status | "Good Standing" | same |
| Type | "Limited Liability Company" · "DOMESTIC LLC" filing "2 Dec 2015" | same |
| Registered agent | an individual is listed (name and address not copied here) | same |
| Incorporation date | hidden behind login on OpenCorporates; BBB states "incorporated on 12/2/2015" (§2.5) | — |

`[NEED: SC SOS primary record — Paul or Gwen to read it by hand (CAPTCHA) and confirm entity number 493170, formation date, status]`

### 2.4 Licence board (SC LLR)

The SC LLR licensee lookup (https://verify.llronline.com/LicLookup/LookupMain.aspx → Residential Builders) requires a
reCAPTCHA. **Not read.** The only public statement of licence detail is third-party:

| Field | Value | Source | Confidence |
|---|---|---|---|
| Licence number | 57706 | site (W3–W5); BBB (search-result text) | found |
| Issuer | "South Carolina Department of Labor-Licensing & Regulation" | BBB (search-result text) | found |
| Expiry | 6/30/2027 | BBB (search-result text) | found |
| Class / board | unknown — `[NEED: licence class (e.g. Residential Builders Commission specialty — roofing, or Contractor's Licensing Board), status and the name it is held under]` | — | unknown |
| Town of Bluffton business licence | #0620033323 (W4) | site | found |

### 2.5 Third-party profiles

| Source | What it says (verbatim where quoted) | URL |
|---|---|---|
| BBB | Name "Apex Roofing of the Lowcountry"; address "6 Sutton Ct, Bluffton, SC 29910-4112"; phone "(843) 757-2739"; "Business Started: 2015-11-11"; accredited since "2021-03-29", "A+"; management "Mr. Ralph Brehany" — "President", "Mr. Pierce Brehany" — "Owner"; service area "Beaufort,, Jasper and Savannah counties" | https://www.bbb.org/us/sc/bluffton/profile/roofing-contractors/apex-roofing-of-the-lowcountry-0403-236004004 |
| HomeAdvisor (city list page) | "Apex Roofing of the Lowcountry, LLC"; 4.8 / 53 reviews; "Since 2015"; "Free estimates", "Credit card accepted" (profile page itself returned 403) | https://www.homeadvisor.com/tloc/bluffton-SC/Metal-Roofing-Install-or-Replace · profile https://www.homeadvisor.com/rated.ApexRoofing.52819750.html |
| Facebook | Name "Apex Roofing of the LowCountry" (capital C); title "… \| Bluffton SC"; "352 followers"; "a residential roofing company specializing in all types of residential roofing solutions" | https://www.facebook.com/ApexRoofingTLC/ |
| Domain (RDAP, Verisign) | registered 2015-11-23; **expires 2026-11-23**; last changed 2025-11-16 | https://rdap.verisign.com/com/v1/domain/apexroofingtlc.com |
| GAF directory (search result only, not opened) | a separate business "Apex Roofing of Coastal Georgia", St. Simons Island GA — relationship to the client unknown | https://www.gaf.com/en-us/roofing-contractors/residential/usa/ga/st-simons-island/apex-roofing-of-coastal-georgia-1128156 |

Not found / not checked: Yelp, Angi profile page, Nextdoor, Instagram, LinkedIn, Apple Maps, Bing Places (§7).

---

## 3 · S03 — Entity foundation (proposal for Paul — BB-1xx)

### 3.1 Category entity (BB-106, BB-107)

| Item | Value |
|---|---|
| GBP primary category | **Roofing contractor** (as displayed on the public GBP, 2026-10-05) |
| Wikipedia verification | https://en.wikipedia.org/wiki/Roofer — opening sentence names "roofer, roof mechanic, or roofing contractor" as one trade (no separate "Roofing contractor" article exists) |
| Wikidata | **Q552378** (roofer) — https://www.wikidata.org/wiki/Q552378 |
| BB-107 (broadest primary) | cannot be checked — secondary categories not visible `[NEED]` |

**Category variants (BB-109 — real names only; 4–6 asked for, the real ones are fewer):**

| Variant | Real-name source | Note |
|---|---|---|
| Roofing Contractor | GBP primary category; Wikipedia "Roofer" lead | proposed **homepage category variant** |
| Roofer | Wikipedia article title; Wikidata label | |
| Roofers | Wikipedia redirect to "Roofer" | plural |
| Roof Mechanic | Wikipedia "Roofer" lead | real but rarely used — Paul's call whether to include |
| Residential Roofer / Residential Roofing Contractor | used on the site (homepage H1, W6) — not a Wikipedia name | candidate only; also depends on the residential-vs-commercial question (C4) |

### 3.2 Area entity — Russian Doll path (BB-105, BB-110)

SAB (status.json; no address on the GBP) → BB-110 says the containing metro / MSA.

```
City served:   Bluffton, SC — "a town in southern Beaufort County" (Wikipedia)
-> County:     Beaufort County, SC — "Beaufort County is part of the Hilton Head Island-Bluffton-Port Royal
               metropolitan statistical area" (Wikipedia)
-> Region:     Hilton Head Island metropolitan area — "officially the Hilton Head Island–Bluffton–Port Royal, SC
               Metropolitan Statistical Area … consisting of the two southernmost counties in the South Carolina
               Lowcountry" = Beaufort County + Jasper County (Wikipedia)
Contains all 12 cities served (the 12 location pages)?  YES — see table
Smallest true container:  Hilton Head Island–Bluffton–Port Royal, SC MSA (Hilton Head Island metropolitan area)
Next level up (not needed unless Georgia is in scope — conflict C1):  South Carolina Lowcountry
```

| City (location page) | County per Wikipedia | In MSA? | Wikipedia |
|---|---|---|---|
| Bluffton | Beaufort | yes | https://en.wikipedia.org/wiki/Bluffton,_South_Carolina |
| Hilton Head Island | Beaufort | yes | https://en.wikipedia.org/wiki/Hilton_Head_Island,_South_Carolina |
| Beaufort | Beaufort | yes | https://en.wikipedia.org/wiki/Beaufort,_South_Carolina |
| Okatie | Beaufort and Jasper | yes | https://en.wikipedia.org/wiki/Okatie,_South_Carolina |
| Hardeeville | Jasper and Beaufort | yes | https://en.wikipedia.org/wiki/Hardeeville,_South_Carolina |
| Lady's Island | Beaufort | yes | https://en.wikipedia.org/wiki/Lady%27s_Island_(South_Carolina) |
| Port Royal | Beaufort | yes | https://en.wikipedia.org/wiki/Port_Royal,_South_Carolina |
| Fripp Island | Beaufort (infobox) | yes | https://en.wikipedia.org/wiki/Fripp_Island,_South_Carolina |
| St. Helena Island | Beaufort | yes | https://en.wikipedia.org/wiki/Saint_Helena_Island_(South_Carolina) |
| Pritchardville | Beaufort | yes | https://en.wikipedia.org/wiki/Pritchardville,_South_Carolina |
| Levy | Jasper | yes | https://en.wikipedia.org/wiki/Levy,_South_Carolina |
| Ridgeland | Jasper (county seat) | yes | https://en.wikipedia.org/wiki/Ridgeland,_South_Carolina |

Also named on the site: Palmetto Bluff (W28) and the communities in W9 — all inside Beaufort County (inferred; Palmetto
Bluff has no Wikipedia article). **All 12 cities are in Beaufort or Jasper County → all inside the MSA.**
The one thing that would break this: Georgia (C1).

### 3.3 Area variants (BB-109 — every one a real name from Wikipedia / Wikidata)

| Variant | Source |
|---|---|
| Hilton Head Island Metropolitan Area | Wikipedia article title; Wikidata alias |
| Hilton Head Island–Bluffton–Port Royal, SC Metropolitan Statistical Area (MSA) | official name (Wikipedia lead; Wikidata label) |
| Hilton Head Island–Bluffton Metropolitan Area | Wikipedia redirect; Wikidata alias (the pre-2023 name) |
| South Carolina Lowcountry | Wikipedia region the MSA sits in ("two southernmost counties in the South Carolina Lowcountry") — a larger true container, as in the BB-105 GutterXperts example |
| Beaufort and Jasper Counties | the two counties that make up the MSA (Wikipedia) |

Observation: the site currently uses "Hilton Head Island Metro Area" in every title — "metro" is a shortening of the
Wikipedia title, not itself a Wikipedia/Wikidata name (Wikidata has "Hilton Head Island-Bluffton, SC Metro Area"). Whether
the shortening counts as real under BB-109 is Paul's call (question Q8).

### 3.4 Proposed reserved homepage variant (CM-024)

```
HOMEPAGE AREA VARIANT:      Hilton Head Island Metropolitan Area   [proposal — awaits entity_approved]
HOMEPAGE CATEGORY VARIANT:  Roofing Contractor                      [proposal — awaits entity_approved]
Rotation pool:  1. Hilton Head Island–Bluffton–Port Royal MSA  2. Hilton Head Island–Bluffton Metropolitan Area
                3. South Carolina Lowcountry  4. Beaufort and Jasper Counties
```

### 3.5 Wikidata URIs

| Entity | URI |
|---|---|
| Category — roofer / roofing contractor | http://www.wikidata.org/entity/Q552378 |
| Area — Hilton Head Island–Bluffton–Port Royal metropolitan area | http://www.wikidata.org/entity/Q17020871 |
| County — Beaufort County, SC | http://www.wikidata.org/entity/Q495682 |
| County (second) — Jasper County, SC | http://www.wikidata.org/entity/Q112957 |
| State — South Carolina | http://www.wikidata.org/entity/Q1456 |
| (region, if used) South Carolina Lowcountry | http://www.wikidata.org/entity/Q3885311 |

The MSA spans two counties; the Brand Guide has one county row — both are listed (Paul picks, or keeps both).

### 3.6 Paul's direction, 2026-10-05 — supersedes 3.2–3.5 where they differ

Paul reviewed the proposal above and directed these changes before approving (logged as decisions in this run):

| Item | Was proposed | Paul's direction | Now in the Brand Guide |
|---|---|---|---|
| Category entity | Roofing contractor | Roofing Contractor — agreed | Roofing Contractor (homepage category variant) |
| Category variants | Roofing Contractor · Roofer · Roofers · Roof Mechanic | All except Roof Mechanic | Roofing Contractor · Roofer · Roofers (Residential Roofer stays a candidate only — not approved) |
| Area entity | Hilton Head Island–Bluffton–Port Royal, SC MSA (Q17020871) | "Lowcountry or South Carolina Lowcountry" instead | **South Carolina Lowcountry** (Wikipedia article title; Wikidata Q3885311) |
| Reserved homepage variant | Hilton Head Island Metropolitan Area | "Lowcountry or South Carolina Lowcountry" | **South Carolina Lowcountry** — bare "Lowcountry" is in the brand name on every page, so it can't be exclusive to the homepage; it goes into the rotation pool |
| C1 — Georgia | open | "No coastal Georgia is being served currently" | Georgia out of scope; the homepage line "& Coastal Georgia" stays an observation for the audit |

Russian Doll with Paul's choice: Bluffton → Beaufort County → Hilton Head Island–Bluffton–Port Royal MSA (smallest
true container) → **South Carolina Lowcountry** (Wikipedia: "The area includes the Hilton Head Island-Bluffton-Beaufort,
SC Metropolitan Statistical Area"; most common definition Charleston, Dorchester, Beaufort, Georgetown, Colleton, Hampton,
Berkeley, Jasper and Williamsburg counties). Contains all 12 cities: yes. It is one level above the smallest container
BB-105 names — Paul's decision, logged; BB-105's own Beaufort + Jasper example lists "South Carolina Lowcountry" as a name
for this area, so it is a real name under BB-109.

Rotation pool now: Lowcountry · Hilton Head Island–Bluffton–Port Royal MSA · Hilton Head Island Metropolitan Area ·
Beaufort and Jasper Counties.

### 3.7 Paul's second direction, 2026-10-05 — supersedes the area part of 3.6

Paul: the brand name contains "Lowcountry" and the brand is in every SEO title, so the SEO title should carry the
Hilton Head Island–Bluffton–Port Royal metro area as the area entity instead.

| Item | 3.6 | Now |
|---|---|---|
| Area entity | South Carolina Lowcountry (Q3885311) | **Hilton Head Island–Bluffton–Port Royal, SC MSA** (Q17020871) — also the smallest true container (BB-105), so the 3.6 deviation no longer applies |
| Reserved homepage variant (homepage SEO title) | South Carolina Lowcountry | **Hilton Head Island–Bluffton–Port Royal Metropolitan Area** |
| Rotation pool | Lowcountry · MSA · HHI Metropolitan Area · Beaufort and Jasper Counties | South Carolina Lowcountry · Lowcountry · Hilton Head Island Metropolitan Area · Beaufort and Jasper Counties |
| SEO-title rule | — | "Lowcountry" variants never in an SEO title (the brand supplies it); they are used in H1, H2s and body |

Category entity, category variants (Roofing Contractor, Roofer, Roofers) and C1 (Georgia not served) are unchanged from 3.6.

Paul confirmed (same day): the reserved variant is written "…Metropolitan Area" (the Wikipedia form; Q8 answered — no
"Metro Area" shortening), and the brand is always written in full in every SEO title that carries it, since "Lowcountry"
is part of the official brand name — the "Lowcountry" variants are therefore not added on top in SEO titles, site-wide.

### 3.8 Paul's direction, 2026-10-08 — reserved homepage variant (supersedes that row of 3.7)

During the audit approval Paul ruled the homepage title/H1 split (audit conflict CF-LOCAL-002, HP-06 vs BB-304):

| Item | 3.7 | Now |
|---|---|---|
| Reserved homepage variant (homepage SEO title) | Hilton Head Island–Bluffton–Port Royal Metropolitan Area | **Hilton Head Island Metropolitan Area** (Wikipedia article title — §3.3; a real name, BB-109) |
| Homepage H1 | — | a familiar pool variant: **Lowcountry** or **South Carolina Lowcountry** ("folks are more familiar with that and it is still accurate") |
| Rotation pool | South Carolina Lowcountry · Lowcountry · Hilton Head Island Metropolitan Area · Beaufort and Jasper Counties | South Carolina Lowcountry · Lowcountry · **Hilton Head Island–Bluffton–Port Royal Metropolitan Area** · Beaufort and Jasper Counties |
| Service-page SEO titles | (metro/county variants) | `Service Name - Brand`, no area term (Gate B 1a, 2026-10-07) |

The area entity itself (the MSA, Q17020871) is unchanged.

---

## 4 · Conflicts — every candidate value, none resolved (PROC-01)

| # | Field | Candidate values (verbatim, with source) | Goes to |
|---|---|---|---|
| C1 | **Service area — does it include Georgia?** (affects the area entity) | (a) 12 SC cities, all in Beaufort/Jasper — location pages, menu; (b) "Serving the South Carolina Lowcountry & Coastal Georgia" — homepage (W8); (c) "Beaufort,, Jasper and Savannah counties" — BBB; (d) GBP service-area list — not visible | Proof sheet (client) + Paul (entity) — **Paul 2026-10-05: Georgia not served currently** (see 3.6) |
| C2 | Founding / start date | (a) "Business Started: 2015-11-11" — BBB; (b) DOMESTIC LLC filing "2 Dec 2015" — OpenCorporates copy of SOS; BBB "incorporated on 12/2/2015"; (c) domain registered 2015-11-23 — RDAP; (d) "founded here over a decade ago" — /bluffton/ (W2); (e) GBP open date — not visible | Proof sheet |
| C3 | Owner / roles | (a) "Founded by Ralph and Pierce Brehany" — homepage (W1); (b) BBB: Ralph Brehany "President", Pierce Brehany "Owner"; (c) reviews: "Ralph" as "The owner" and "his son Pierce" | Proof sheet |
| C4 | Residential only, or residential + commercial | (a) "a licensed residential roofing contractor" — homepage (W6); Facebook / footer "a residential roofing company"; (b) "top-tier roofing solutions for homes and businesses" — /about/ (W7); (c) "residential and commercial roof inspections" — GBP post 2026-10-04; (d) "roofing subcontractor on new construction projects" — /roof-installation/ (W16) | Proof sheet |
| C5 | Business name form | (a) "Apex Roofing of the Lowcountry" — GBP, site, BBB; (b) "APEX ROOFING OF THE LOWCOUNTRY LLC" — SOS copy; (c) "Apex Roofing of the Lowcountry, LLC" — HomeAdvisor; (d) "Apex Roofing of the LowCountry" — Facebook; (e) "Apex Roofing of The Lowcountry" — /about/ and /contact/ titles | Proof sheet (exact NAP) |
| C6 | Address shown publicly | (a) none — GBP (SAB) and site footer ("Bluffton, SC 29910"); (b) "6 Sutton Ct, Bluffton, SC 29910-4112" — BBB | Proof sheet (NAP) |
| C7 | County of Levy | (a) "an area of Beaufort County" — /levy/ (W26); (b) "southern portions of Jasper County" — Wikipedia | Paul (observation for the audit) |
| C8 | County of Okatie | (a) "in Beaufort County" — /okatie/ (W27); (b) "located in Beaufort and Jasper counties" — Wikipedia | Paul (observation for the audit) |
| C9 | Ratings across platforms | GBP 5.0 / 67 · HomeAdvisor 4.8 / 53 · search-result text "4.93 … 42 reviews" (Angi/HomeAdvisor, date unknown) · BBB 0 reviews | none — recorded only |
| C10 | MSA name on the site | (a) "Hilton Head Island-Bluffton, SC Metropolitan Statistical Area" — homepage; (b) "Hilton Head Island–Bluffton–Port Royal, SC Metropolitan Statistical Area" — Wikipedia (current official) | Paul (entity) |

None of these is a methodology-rule conflict, so no PROC-01 entry was opened in `methodology/rulings.md` /
`lessons.md`; they are fact conflicts for the proof sheet and Paul. (If Paul reads Q8 as a BB-109 interpretation
question, it would go to `lessons.md` as an inbox item.)

---

## 5 · Other observations (no severity — the audit decides)

- O1 — GBP Website field `http://www.apexroofingtlc.com/` 301s in one hop to `https://apexroofingtlc.com/` (Apache).
- O2 — Domain registration expires **2026-11-23** (RDAP).
- O3 — Only a `WebSite` JSON-LD node on the homepage; none found on the other pages read.
- O4 — Every service and location H1 opens "The Best …" (CM-020 applies at Build; a missing or present "The Best" is not judged here).
- O5 — Metal roofing lives at `/metal-roofing-2/` (the `-2` suffix).
- O6 — Six recognition badges on the homepage, empty alt text; one reads "Best of 2018 Roofer" (source of the award not stated).
- O7 — Price ranges are published on /slate-roofing/ and /metal-roofing-2/ (W19, W20) — need client confirmation before any writer reuses them (CM-016).
- O8 — Site credit "Powered By Tampa Bay SEO"; the site was evidently reworked recently in a Bradley-style pattern (titles, "Service Areas" H2s, FAQs) — the crawl and audit will read it properly.
- O9 — 33 blog posts in the post sitemap, several city-plus-service topics (e.g. `/roof-repair-in-ridgeland-sc-…/`, `/4-point-inspection-bluffton-sc/`) — for the Blog Decision Map later, not discovery.

---

## 6 · Questions (for the proof sheet unless marked Paul)

| # | Question | For |
|---|---|---|
| Q1 | Do you take jobs in Georgia (Savannah / Chatham County, coastal Georgia)? If so, which places? Is "Apex Roofing of Coastal Georgia" connected to you? | client (C1) |
| Q2 | Which date should we use for when the business started — Nov 2015, Dec 2015, or another? | client (C2) |
| Q3 | Who owns the company and what are Ralph's and Pierce's titles? Which names may appear on the site? | client (C3) |
| Q4 | Do you do commercial roofing, or residential only? | client (C4) |
| Q5 | Exact business name and address as they must appear (and should the Sutton Ct address stay hidden)? | client (C5, C6) |
| Q6 | Licence: class, board and the name it is held under for #57706; is the Town of Bluffton licence current? | client (+ manual LLR check) |
| Q7 | CertainTeed ShingleMaster: current? GAF status? Workmanship guarantee term? Insurance carriers? Financing / "payment arrangements"? | client |
| Q8 | Is "Hilton Head Island Metro Area" (the current title wording) acceptable as a real variant under BB-109, or should variants use only the Wikipedia/Wikidata names? | **Paul** |
| Q9 | The MSA spans Beaufort and Jasper: one county URI or both in schema later? | **Paul** |
| Q10 | GBP secondary categories, service-area list and opening date (GBP dashboard). | client or Gwen |

---

## 7 · Not checked / could not check

- **SC Secretary of State** primary record — CAPTCHA (read a public copy on OpenCorporates instead).
- **SC LLR licence lookup** — reCAPTCHA. Licence class, status and holder name unknown.
- **GBP** secondary categories, service areas, open date, Q&A, duplicates beyond one search — limited public view.
- HomeAdvisor profile page (403); Yelp, Angi profile, Nextdoor, Instagram, LinkedIn, Apple Maps, Bing Places — not checked.
- CertainTeed / GAF contractor directories — not checked (certification stays `found`).
- Older Apex folders in Drive outside v3 — **not read** on Paul's instruction.
- No DataforSEO or other paid call was made.

Evidence capture: `Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05.md`
(repo `clients/apex-roofing-of-the-lowcountry/discovery/`, Drive `01 - Discovery and Audit/Evidence/`).
