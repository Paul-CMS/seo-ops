# Outline — Auburndale (location)

Page `loc-auburndale` · section `locations-west` · run 20261026-120219-build-bc47 · derived 2026-10-26T12:04 by outline.py (Rewrite 4: no brief — nothing in this file is a decision; the plan, the spec and the pack are).
Final URL: https://www.firstchoiceseamlessgutters.net/auburndale-fl/ · replaces https://www.firstchoiceseamlessgutters.net/areas-we-serve/auburndale-fl/ (301 — a VA handoff) · group West and north Polk
Spec: `methodology/specs/location.md` · Pack: `clients/first-choice-seamless-gutters/build/locations-west/packs/loc-auburndale.md` · Pilot corrections: `clients/first-choice-seamless-gutters/build/pilot-corrections.md` · FAQ recipe: `methodology/location-faq.md`
Evidence gate: pass

## Fixed by the approved site plan

| Field | Value |
|---|---|
| Keyword | gutters auburndale fl |
| H1 | Rain Gutters in Auburndale |
| City | Auburndale |
| Category variant | Rain Gutters |
| FAQ picks | 1 · Local cost or decision: Do Auburndale HOA subdivisions need approval for new gutter colours?, 2 · Logistics here: Who issues permits for gutter work at a Auburndale address — City of Auburndale? (and whether gutter work needs one), 3 · Trust here: What wears out gutters and fascia on older Auburndale block homes? |

## Variants

- Reserved for the homepage — never on this page: HOMEPAGE AREA VARIANT:      Polk County, FL          [Submitted 2026-10-22 — proposal, Decision Sheet homepage_title_variant] · HOMEPAGE CATEGORY VARIANT:  Gutter Service           [Submitted 2026-10-22 — proposal; waits on the GBP primary category conflict]
- Area rotation pool (B2): 1. Polk County, Florida                         [Submitted 2026-10-22 — proposal] · 2. Lakeland–Winter Haven                        [Submitted 2026-10-22 — proposal] · 3. Lakeland–Winter Haven metropolitan area      [Submitted 2026-10-22 — proposal] · 4.
- Category variants (A3): Proposed: Gutter Service · Seamless Gutters · Rain Gutters · Gutter Contractor · Gutter Installation (Wikipedia entity: Rain gutter, Q152833)
- No variant at two consecutive steps URL → title → H1 → first H2 (BB-108, CM-024).

## Page order (the spec, §3 — every row is a requirement)

| # | Element | Requirement |
|---|---|---|
| 1 | URL | City slug only, no service |
| 2 | SEO title | `Brand - GB Category - City, Full State Name`; one city; Title Case; no "The Best"; never truncated |
| 3 | Meta description | 150–160 chars, names the area and at least two services, soft CTA |
| 4 | H1 | One H1. `[Service Variant] in [City]`, **no state**, no brand, differs from title variants. Superlative only if BG-H2 says yes. |
| 5 | Opening paragraph | No H tag, 60–120 words, unique to this city, triple in a third variant set, phone and offer, first sentence answers. Never covers conditions or logistics. |
| 6 | H2 services table | H3 links to **all** service pages; **no service descriptions**; rows left as placeholder for Finish |
| 7 | H2 Local context | The place: climate, housing stock, terrain, exposure, why the work fails here. **Up to two short paragraphs**, with **3–4 named, verifiable place entities woven in** (from the pack; also the schema `about` entries). Never describes the client. Appears on no other page; no links. |
| 8 | H2 Serving [City] | How the client operates here: response and travel time, which office issues permits, HOA/ARB experience in named communities, access, storm-season scheduling, hours. **One informational outbound link** to the official town or county page (CM-011). No service explanations; says only how the client handles the rules the FAQ asks about. |
| 9 | FAQ | H2 wrapper + H3 per question; **three questions, one per category** (location-faq.md): 1 local cost or decision · 2 logistics here · 3 trust here. First sentence answers (CM-060, 40–60 words); none in C3; none on another page. |
| 10 | H2 Neighbourhoods | **Up to 12**, as many as can be verified. Fewer than 3 verified → drop the section and name them in Local context. |
| 11 | H2 Recent work in [City] | **Optional.** A 3–4 sentence story from a review that names the city, at its usage tier (attributed customer example; "Customers mention…" at 3+ mentions), no reviewer name. **Dropped silently** if no such review exists. |
| 12 | City map | City-level map embed, no H tag; the GBP map only if this is a verified GBP landing page |
| 13 | H2 sibling cities | Links to every other location page; rows left as placeholder for Finish |
| 14 | CTA | No H tag; **name, phone and hours** matching the GBP exactly; the address **only** on the GBP landing page |
| — | Every H2 section | Under 500 tokens; readable alone; names its entities; no decorative headers (CM-023) |
| — | Specificity and the swap test | At least 3 concrete, verifiable, city-specific facts. **Swap test, per paragraph:** swap the city name for a neighbouring city — if it is still true, rewrite it (a Fix). |
| — | Ratings | **No static star rating or review count**, and no rating schema |
| — | Word ceiling | Under 1,000 words, unless the excess is genuine city substance (passes) rather than service description (fails) |
| — | Schema readiness | Non-GBP page: `WebPage` + `ItemList` of service `@id`s, `mainEntity` = ID page; never LocalBusiness. `about` = the ID page, the city, and the 3–4 place entities as `Thing`s with the **Wikidata URI as `@id`** and `sameAs` (Wikipedia, Wikidata, grokipedia) (BB-606). Place entities are **not** put in `mentions` (it is the service catalog). GBP landing page only: LocalBusiness subtype per the GBP test. Recommendation only. |

## FAQ candidates

Three questions, one per category (none already owned below):

- **1 · Local cost or decision** — what changes the job or the price here (HOA/ARB, historic district, flood rules, wind code); no prices unless confirmed
- **2 · Logistics in this area** — permits and who issues them, access, travel and response time, season
- **3 · Trust in this area** — local pain points and the client's local experience; reviews at their tier

- None tagged to this page in the pack: use the place research's local questions, then review language (location-faq.md order); list the source of each pick in the results file.

## Already owned by another page — never repeated (Brand Guide C3)

- /gutter-cleaning/: H2: How Does First Choice Seamless Gutters Clean Rain Gutters? · H2: What Does a Gutter Cleaning Include, and What Is Separate? · H2: What Do Polk County Homeowners Ask a Gutter Contractor About Cleaning? · H2: Where Does First Choice Seamless Gutters Offer Gutter Cleaning? · FAQ: How much does gutter cleaning cost? · FAQ: When is the best time of year to clean gutters in Florida? · FAQ: How often should gutters be cleaned in Polk County? · FAQ: What are the signs my gutters need cleaning? · FAQ: Do telescopic gutter cleaners work?
- /lakeland-fl/: H2: Gutter Installation, Repair and Cleaning in Lakeland · H2: What Makes Lakeland Hard on Gutters? · H2: How Does First Choice Serve Lakeland Homeowners? · H2: Lakeland Gutter Questions · H2: Which Lakeland Neighborhoods Does First Choice Serve? · H2: Which Other Cities Near Lakeland Does First Choice Serve? · FAQ: Does a Lakeland historic district or HOA limit gutter colour or profile? · FAQ: Who issues permits for gutter work at a Lakeland address — City of Lakeland? · FAQ: How do Lakeland's summer storms affect gutters?
- /seamless-gutter-installation/: H2: How Does a Seamless Gutter Installation Work, From Estimate to Clean-Up? · H2: What Kinds of Seamless Gutter Jobs Does First Choice Seamless Gutters Take On? · H2: What Should Polk County Homeowners Know Before Buying Seamless Gutters? · H2: Which Polk County Towns Get Seamless Gutter Installation From First Choice? · FAQ: How can you tell if gutters are seamless? · FAQ: What are the downsides of seamless gutters? · FAQ: How are seamless gutters made? · FAQ: What is the highest rated gutter system for a home?
- /gutter-installation/: H2: How Does First Choice Seamless Gutters Install New Rain Gutters? · H2: What Kinds of Gutter Replacement and New Gutter Jobs Are There? · H2: What Gutter Materials Can You Choose? · H2: What Do Homeowners in Polk County, Florida Ask About New Rain Gutters? · H2: Where Does First Choice Seamless Gutters Install and Replace Gutters? · FAQ: When should house gutters be replaced? · FAQ: What do new rain gutters cost in Florida? · FAQ: Is it common for a house not to have gutters? · FAQ: Can I install my own gutters? · FAQ: How is a gutter installation estimate worked out?
- /gutter-repair/: H2: What Happens During a Seamless Gutter Repair Visit? · H2: Which Gutter Problems Can Be Repaired Instead of Replaced? · H2: What Should Polk County Homeowners Know Before Paying for Rain Gutter Repair? · H2: Which Polk County Towns Can Book a Gutter Repair Visit? · FAQ: How much does it cost to fix gutters? · FAQ: What is the most common problem with gutters? · FAQ: Can a handyman fix a gutter? · FAQ: Should a damaged gutter be repaired or replaced? · FAQ: What does routine gutter maintenance include?
- /commercial-gutters/: H2: How Does First Choice Seamless Gutters Install Commercial Rain Gutters? · H2: What Kinds of Commercial Gutter Work Does First Choice Handle? · H2: What Do Polk County Business Owners Ask About Commercial Gutter Installation? · H2: Where Does First Choice Seamless Gutters Install Commercial Gutters? · FAQ: What are commercial-grade gutters? · FAQ: What is the difference between box gutters and K-style gutters on a commercial roof? · FAQ: What size gutters does a large commercial roof need? · FAQ: How long does a commercial gutter installation take?
- /gutter-downspouts/: H2: How Does First Choice Seamless Gutters Fit Downspouts to Rain Gutters? · H2: Which Downspout Sizes, Materials and Drainage Add-Ons Suit a Gutter Installation? · H2: Which Downspout Questions Come Up Most With Seamless Gutters in Polk County? · H2: Which Polk County Towns Does First Choice Serve for Downspout Work? · FAQ: What is the rule of thumb for how many downspouts a gutter needs? · FAQ: Can you put a 3x4 downspout on a 5-inch gutter? · FAQ: What can I use instead of a downspout? · FAQ: How much does it cost to replace a downspout? · FAQ: Where should downspouts drain on a Florida lot?
- /gutter-guards/: H2: How Does First Choice Seamless Gutters Add Gutter Guards to Rain Gutters? · H2: Which Kinds of Gutter Guards Work on Rain Gutters? · H2: Are Gutter Guards Worth It on Seamless Gutters in Polk County, Florida? · H2: Which Polk County Towns Can Get Gutter Guards From First Choice? · FAQ: What are the downsides of gutter guards? · FAQ: How much should I expect to pay for gutter guards? · FAQ: What is the difference between a leaf guard and a gutter guard? · FAQ: What do roofers say about gutter guards?
- /copper-gutters/: H2: How Does First Choice Seamless Gutters Plan and Install Copper Gutters? · H2: What Kinds of Copper Gutters and Downspouts Can You Choose From? · H2: What Do Polk County Homeowners Ask About Copper Rain Gutters? · H2: Which Polk County Towns Can Get Copper Gutters From First Choice Seamless Gutters? · FAQ: How long do copper gutters last? · FAQ: Are copper gutters worth the cost? · FAQ: Can copper and aluminum gutters be mixed? · FAQ: Should copper gutters be soldered?
- /galvalume-gutters/: H2: How Does a Galvalume Gutter Job Work With First Choice Seamless Gutters? · H2: Which Parts of a Galvalume Gutter System Can First Choice Seamless Gutters Handle? · H2: What Do Florida Homeowners Ask About Galvalume Rain Gutters? · H2: Where Does First Choice Seamless Gutters Install Galvalume Gutters? · FAQ: What is Galvalume steel? · FAQ: Are Galvalume gutters better than aluminum or galvanized gutters? · FAQ: What is the best gutter material for Florida homes? · FAQ: Do Galvalume gutters rust in Florida humidity?
- /aluminum-gutters/: H2: What Happens When First Choice Seamless Gutters Installs an Aluminum Gutter System? · H2: Which Kinds of Aluminum Gutters Can a Home Have? · H2: What Should Polk County, Florida Homeowners Ask About Aluminum Gutter Installation? · H2: Where Does First Choice Seamless Gutters Install Aluminum Gutters? · FAQ: Are aluminum gutters good? · FAQ: What is the difference between .027 and .032 aluminum gutters? · FAQ: Do aluminum gutters rust? · FAQ: What do aluminum gutters cost for a home?

## Links — the wheel (wheel.py, CM-064): write each table as its placeholder row; the rows are filled when the draft is generated. No cross-page link in prose

- `| [Link wheel: populate service links here] |`: Continuous Rain Gutters — Seamless Gutter Installation (https://www.firstchoiceseamlessgutters.net/seamless-gutter-installation/) · Gutter Replacement — Gutter Installation (https://www.firstchoiceseamlessgutters.net/gutter-installation/) · Leaking and Sagging Gutter Repair — Gutter Repair (https://www.firstchoiceseamlessgutters.net/gutter-repair/) · Commercial Gutter Systems — Commercial Gutters (https://www.firstchoiceseamlessgutters.net/commercial-gutters/) · Downspout Installation and Drainage — Gutter Downspouts (https://www.firstchoiceseamlessgutters.net/gutter-downspouts/) · Gutter Protection Systems — Gutter Guards (https://www.firstchoiceseamlessgutters.net/gutter-guards/) · Gutter and Downspout Cleaning — Gutter Cleaning (https://www.firstchoiceseamlessgutters.net/gutter-cleaning/) · Copper Gutter Systems — Copper Gutters (https://www.firstchoiceseamlessgutters.net/copper-gutters/) · Galvalume Steel Gutters — Galvalume Gutters (https://www.firstchoiceseamlessgutters.net/galvalume-gutters/) · Aluminum Rain Gutters — Aluminum Gutters (https://www.firstchoiceseamlessgutters.net/aluminum-gutters/)
- `| [Link wheel: populate sibling-city links here] |` (its hub first, then every other location): Rain Gutters in Lakeland — Lakeland (https://www.firstchoiceseamlessgutters.net/lakeland-fl/) · Seamless Gutters in Winter Haven — Winter Haven (https://www.firstchoiceseamlessgutters.net/winter-haven-fl/) · Seamless Gutters in Bartow — Bartow (https://www.firstchoiceseamlessgutters.net/bartow-fl/) · Rain Gutters in Polk City — Polk City (https://www.firstchoiceseamlessgutters.net/polk-city-fl/) · Seamless Gutters in Kathleen — Kathleen (https://www.firstchoiceseamlessgutters.net/kathleen-fl/) · Rain Gutters in Highland City — Highland City (https://www.firstchoiceseamlessgutters.net/highland-city-fl/) · Seamless Gutters in Mulberry — Mulberry (https://www.firstchoiceseamlessgutters.net/mulberry-fl/) · Rain Gutters in Eagle Lake — Eagle Lake (https://www.firstchoiceseamlessgutters.net/eagle-lake-fl/) · Seamless Gutters in Wahneta — Wahneta (https://www.firstchoiceseamlessgutters.net/wahneta-fl/) · Rain Gutters in Davenport — Davenport (https://www.firstchoiceseamlessgutters.net/davenport-fl/) · Seamless Gutters in Haines City — Haines City (https://www.firstchoiceseamlessgutters.net/haines-city-fl/) · Rain Gutters in Lake Alfred — Lake Alfred (https://www.firstchoiceseamlessgutters.net/lake-alfred-fl/) · Seamless Gutters in Lake Hamilton — Lake Hamilton (https://www.firstchoiceseamlessgutters.net/lake-hamilton-fl/) · Rain Gutters in Dundee — Dundee (https://www.firstchoiceseamlessgutters.net/dundee-fl/) · Seamless Gutters in Lake Wales — Lake Wales (https://www.firstchoiceseamlessgutters.net/lake-wales-fl/) · Rain Gutters in Waverly — Waverly (https://www.firstchoiceseamlessgutters.net/waverly-fl/) · Seamless Gutters in Frostproof — Frostproof (https://www.firstchoiceseamlessgutters.net/frostproof-fl/) · Rain Gutters in Fort Meade — Fort Meade (https://www.firstchoiceseamlessgutters.net/fort-meade-fl/)

## Claims

Every fact is in the pack's Facts section, in its state: 25 confirmed · 7 sourced public · 18 unknown — **confirmed** is a plain claim, **sourced public** a plain statement, **unknown** is never claimed.

### Unknown — never claimed: `[NEED: …]` where the page needs it, or leave it out

- `a-gbp-primary-category-the-category-entity` GBP primary category = the category entity
- `a-area-entity` Area entity
- `a-separator-standard` Separator standard
- `a-exact-url-in-the-gbp-website-field` Exact URL in the GBP Website field
- `d-founding-year-years-in-business` Founding year / years in business
- `d-certifications-authorizations-factory-training` Certifications, authorizations, factory training
- `d-team-size-trucks-jobs-completed` Team size / trucks / jobs completed
- `d-financing-available-provider-terms` Financing — available, provider, terms
- `d-minimum-service-call-or-trip-charge` Minimum service call or trip charge
- `d-payment-methods` Payment methods
- `d-services-subcontracted-out` Services subcontracted out
- `d-licensed-practitioner-for-health-claim-sign-off-medical-ch` Licensed practitioner for health-claim sign-off *(medical / chiropractic)*
- `gbp-share-link` Google Business Profile link
- `gsc-access` Google Search Console access
- `d-staff-roles` Roles of April, Matt, Isaac, James
- `d-travel-fee` Travel fee

Reviews (use only at the tier the pack gives): practice: photos (example, 1 reviewer(s)) · practice: clean-up (known, 5 reviewer(s)) · practice: communication (known, 23 reviewer(s)) · practice: speed (known, 40 reviewer(s)) · named staff: Adrian (known, 8 reviewer(s)) · named staff: Inc (example, 4 reviewer(s)) · named staff: James (known, 26 reviewer(s)) · named staff: Landon (known, 5 reviewer(s)) · named staff: Randall (known, 3 reviewer(s))

### Never reuse (Brand Guide D2)

- "fully licensed and insured" / "Licensed & Insured" — the *licensed* part only → Do not write "licensed"; "insured" may be written
- "Based in Winter Haven" → Do not repeat; base town = Lakeland
- "Based in nearby Bartow" → Do not repeat; base town = Lakeland
- "Business Started: 11/24/2021" (BBB, not the site) → Write no founding year, no years-in-business figure and no "since 2021"

## The writer reports (results file → the draft review sheet)

Keyword · SEO title · meta description · H1 · the variants used where · every H2 · each FAQ question with its category and source · the place entities named · every `[NEED: …]` and `[LINK → …]` left. Each choice the plan did not fix is a **Fix and list** row; a legal or money claim from the site is an Ask.
