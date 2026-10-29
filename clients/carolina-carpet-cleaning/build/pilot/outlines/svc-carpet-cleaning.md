# Outline — Carpet Cleaning (service)

Page `svc-carpet-cleaning` · section `pilot` · run 20261029-142210-build-b1dd · derived 2026-10-29T14:26 by outline.py (Rewrite 4: no brief — nothing in this file is a decision; the plan, the spec and the pack are).
Final URL: /carpet-cleaning/
Spec: `methodology/specs/service.md` · Pack: `clients/carolina-carpet-cleaning/build/pilot/packs/svc-carpet-cleaning.md`
Evidence gate: warn — gaps: 1 required and 2 supporting gap(s), 1 conflict(s) — the brief must list them under 'Evidence gaps'

## Fixed by the approved site plan

| Field | Value |
|---|---|
| Keyword | carpet cleaning |
| H1 | Home Carpet Cleaning in the South Carolina Lowcountry |
| Service variant | home carpet cleaning |
| Area variant | South Carolina Lowcountry |
| FAQ picks | How much does it cost to have carpet professionally cleaned? — PAA #12; what changes the price, no figure (pricing not in Section D), How do I get brown stains out of my carpet? — PAA #2; stain removal is folded into this page (F-008), How long does carpet take to dry after cleaning? — settled fact_drying_time (under one hour, typical job); competitor coverage, Do you move furniture before cleaning the carpet? — competitor coverage; client practice is a facts-round question, Is the cleaning solution safe for children and pets? — Section D safety claims (F-006, Paul approved), How is low-moisture cleaning different from steam cleaning? — low-moisture is folded into this page (F-008) |

## Variants

- Reserved for the homepage — never on this page: HOMEPAGE AREA VARIANT:      Hilton Head Island Metro Area (title) · South Carolina Lowcountry (H1) [Submitted 2026-10-28, proposal] · HOMEPAGE CATEGORY VARIANT:  Carpet Cleaning [Submitted 2026-10-28, proposal]
- Area rotation pool (B2): 1. South Carolina Lowcountry · 2. Hilton Head Island–Bluffton–Port Royal area · 3. Lowcountry
- Category variants (A3): Proposed: carpet cleaning · carpet cleaning service · carpet cleaners · carpet cleaning company · carpet cleaner (search volume checked in the data step)
- No variant at two consecutive steps URL → title → H1 → first H2 (BB-108, CM-024).

## Page order (the spec, §3 — every row is a requirement)

| # | Element | Requirement |
|---|---|---|
| 1 | URL | Root-proximate (`/service-name/`), no city |
| 2 | SEO title | `Service Name - Brand`, site separator, Title Case, no "The Best", never truncated |
| 3 | Meta description | 150–160 chars, names the area and at least two services, soft CTA |
| 4 | H1 | One H1. `[Service Variant] in [Area Variant]`; area variant from B2, **never a city**; no brand; differs from title variants. Superlative only if BG-H2 says yes. |
| 5 | Opening paragraph | No H tag, 60–120 words, triple in a third variant set, phone and offer, a distinct buyer state, first sentence answers |
| 6 | H2 how the service is delivered | Process, materials, what the buyer gets; names entities |
| 7 | H2 service types / subtypes | H3 per type; sub-services live here, not on their own pages |
| 8 | H2 FAQ | Fresh variant pair; H3 per question in customer words; 4–6, each with its reason in the site plan (a routed PAA/fan-out question is a candidate, not an obligation); first sentence is the full answer (40–60 words); none in the C3 registry |
| 9 | H2 service areas | H3 links to **every** location page; table rows left as a placeholder for Finish; no city in the H2 text |
| 10 | CTA | No H tag; phone and offer |
| — | Every H tag | No city name anywhere |
| — | Every H2 section | Under 500 tokens (~375 words); readable alone; sayable as a question; no decorative headers |
| — | Specificity | At least 3 concrete, verifiable, page-specific facts; no stat dumps |
| — | Outbound authority link | 1–2 in-text, relevant, non-competing; or none with reason documented |
| — | Schema readiness | `WebPage` + `Service`; `provider` = ID page `@id`; never LocalBusiness, no NAP or address. Recommendation only. |
| — | Word ceiling | None set by any rule |

## FAQ candidates

- None tagged to this page in the pack: use the place research's local questions, then review language (location-faq.md order); list the source of each pick in the results file.

## Already owned by another page — never repeated (Brand Guide C3)

- none yet

## Links — the wheel (wheel.py, CM-064): write each table as its placeholder row; the rows are filled when the draft is generated. No cross-page link in prose

- `| [Link wheel: populate service-area links here] |`: Home Carpet Cleaning in Bluffton — Bluffton, SC (/bluffton/) · Home Carpet Cleaning in Hilton Head Island — Hilton Head Island, SC (/hilton-head/) · Home Carpet Cleaning in Beaufort — Beaufort, SC (/beaufort/) · Home Carpet Cleaning in Lady's Island — Lady's Island, SC (/ladys-island/) · Home Carpet Cleaning in Ridgeland — Ridgeland, SC (/ridgeland/) · Home Carpet Cleaning in Hardeeville — Hardeeville, SC (/hardeeville/)

## Claims

Every fact is in the pack's Facts section, in its state: 32 confirmed · 1 sourced public · 6 unknown — **confirmed** is a plain claim, **sourced public** a plain statement, **unknown** is never claimed.

### Unknown — never claimed: `[NEED: …]` where the page needs it, or leave it out

- `a-brand-entity-gbp-name-exactly` Brand entity (GBP name, exactly)
- `a-separator-standard` Separator standard
- `d-google-rating-and-review-count-exactly-as-google-shows-the` Google rating and review count — exactly as Google shows them on the day, with the date ("4.9 · 67 reviews, 2026-10-07"; never a rounded 5.0)
- `d-licensed-practitioner-for-health-claim-sign-off-medical-ch` Licensed practitioner for health-claim sign-off *(medical / chiropractic)*
- `g-positioning-owner-words` Section G positioning lines (owner's words)

Reviews (use only at the tier the pack gives): service: Carpet Cleaning (unchecked, 9 reviewer(s)) · service: home carpet cleaning (example, 1 reviewer(s)) · practice: communication (example, 2 reviewer(s)) · practice: speed (known, 14 reviewer(s)) · named staff: Kevin (known, 11 reviewer(s))

### Never reuse (Brand Guide D2)

- "$2 to $5 per square foot … $160 to $400" (rug-cleaning price range) → Do not repeat; remove (audit F-023, decided)
- "our personnel is highly-trained and insured" → Do not repeat "personnel"/"highly-trained"; remove (audit F-023, decided)
- "Call (843) 525-6288" (homepage hero button, tel:8435256288) → Never use 525-6288; fix (audit F-001)
- Any review count other than Google's figure on the day → No page states a count until Paul records the Google figure

## The writer reports (results file → the draft review sheet)

Keyword · SEO title · meta description · H1 · the variants used where · every H2 · each FAQ question with its category and source · the place entities named · every `[NEED: …]` and `[LINK → …]` left. Each choice the plan did not fix is a **Fix and list** row; a legal or money claim from the site is an Ask.
