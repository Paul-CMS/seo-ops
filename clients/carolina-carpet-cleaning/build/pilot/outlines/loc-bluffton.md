# Outline — Bluffton, SC (location)

Page `loc-bluffton` · section `pilot` · run 20261029-142210-build-b1dd · derived 2026-10-29T14:26 by outline.py (Rewrite 4: no brief — nothing in this file is a decision; the plan, the spec and the pack are).
Final URL: /bluffton/
Spec: `methodology/specs/location.md` · Pack: `clients/carolina-carpet-cleaning/build/pilot/packs/loc-bluffton.md` · FAQ recipe: `methodology/location-faq.md`
Evidence gate: warn — gaps: 1 required and 1 supporting gap(s), 1 conflict(s) — the brief must list them under 'Evidence gaps'

## Fixed by the approved site plan

| Field | Value |
|---|---|
| Keyword | carpet cleaning bluffton sc |
| H1 | Carpet Cleaners in Bluffton |
| City | Bluffton |
| FAQ picks | 1 · Local cost or decision: do HOA or gated-community rules in Bluffton change how a cleaning visit is booked — many Bluffton homes sit in gated communities, 2 · Logistics: how soon can a cleaning be scheduled in Bluffton — the business is based in Bluffton (273 Club Gate), 3 · Trust: why carpets in Bluffton homes smell musty in summer — marsh-side humidity; review language at its tier |

## Assigned by formula (outline.py — the site-plan row left these empty; use them as given)

| Field | Value | Formula and source |
|---|---|---|
| Category variant | Proposed: carpet cleaning | the same A3 variant (the H1 slot) |

## Variants

- Reserved for the homepage — never on this page: HOMEPAGE AREA VARIANT:      Hilton Head Island Metro Area (title) · South Carolina Lowcountry (H1) [Submitted 2026-10-28, proposal] · HOMEPAGE CATEGORY VARIANT:  Carpet Cleaning [Submitted 2026-10-28, proposal]
- Area rotation pool (B2): 1. South Carolina Lowcountry · 2. Hilton Head Island–Bluffton–Port Royal area · 3. Lowcountry
- Category variants (A3): Proposed: carpet cleaning · carpet cleaning service · carpet cleaners · carpet cleaning company · carpet cleaner (search volume checked in the data step)
- No variant at two consecutive steps URL → title → H1 → first H2 (BB-108, CM-024).
- Assigned to this page by formula: category variant Proposed: carpet cleaning

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

- none yet

## Links — the wheel (wheel.py, CM-064): write each table as its placeholder row; the rows are filled when the draft is generated. No cross-page link in prose

- `| [Link wheel: populate service links here] |`: Home Carpet Cleaning — Carpet Cleaning (/carpet-cleaning/) · Business Carpet Cleaning — Commercial Carpet Cleaning (/commercial-carpet-cleaning/) · Area and Oriental Rug Cleaning — Rug Cleaning (/rug-cleaning/) · Furniture Upholstery Cleaning — Upholstery Cleaning (/upholstery-cleaning/) · Tile Floor and Grout Cleaning — Tile & Grout Cleaning (/tile-grout-cleaning/) · Wood Floor Cleaning — Hardwood Floor Cleaning (/hardwood-floor-cleaning/) · Pet Urine Odor Removal — Pet Odor Removal (/pet-odor-removal/) · Boat and Car Interior Cleaning — Boat & Auto Interior Cleaning (/boat-and-auto-interior-cleaning/)
- `| [Link wheel: populate sibling-city links here] |` (its hub first, then every other location): Carpet Cleaners in Hilton Head Island — Hilton Head Island, SC (/hilton-head/) · Carpet Cleaners in Beaufort — Beaufort, SC (/beaufort/) · Carpet Cleaners in Lady's Island — Lady's Island, SC (/ladys-island/) · Carpet Cleaners in Ridgeland — Ridgeland, SC (/ridgeland/) · Carpet Cleaners in Hardeeville — Hardeeville, SC (/hardeeville/)

## Claims

Every fact is in the pack's Facts section, in its state: 32 confirmed · 5 sourced public · 6 unknown — **confirmed** is a plain claim, **sourced public** a plain statement, **unknown** is never claimed.

### Unknown — never claimed: `[NEED: …]` where the page needs it, or leave it out

- `a-brand-entity-gbp-name-exactly` Brand entity (GBP name, exactly)
- `a-separator-standard` Separator standard
- `d-google-rating-and-review-count-exactly-as-google-shows-the` Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0)
- `d-licensed-practitioner-for-health-claim-sign-off-medical-ch` Licensed practitioner for health-claim sign-off *(medical / chiropractic)*
- `g-positioning-owner-words` Section G positioning lines (owner's words)

Reviews (use only at the tier the pack gives): practice: communication (example, 2 reviewer(s)) · practice: speed (known, 14 reviewer(s)) · named staff: Kevin (known, 11 reviewer(s))

### Never reuse (Brand Guide D2)

- "$2 to $5 per square foot … $160 to $400" (rug-cleaning price range) → Do not repeat; remove (audit F-023, decided)
- "our personnel is highly-trained and insured" → Do not repeat "personnel"/"highly-trained"; remove (audit F-023, decided)
- "Call (843) 525-6288" (homepage hero button, tel:8435256288) → Never use 525-6288; fix (audit F-001)
- Any review count other than Google's figure on the day → No page states a count until Paul records the Google figure

## The writer reports (results file → the draft review sheet)

Keyword · SEO title · meta description · H1 · the variants used where · every H2 · each FAQ question with its category and source · the place entities named · every `[NEED: …]` and `[LINK → …]` left. Each choice the plan did not fix is a **Fix and list** row; a legal or money claim from the site is an Ask.
