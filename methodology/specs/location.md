# Spec — Location page
**Status:** APPROVED — 2026-10-14, Paul
**Governs:** location page (one per city) · **Rule sources:** BB-108, BB-201–206, BB-208, BB-301–312, BB-315–318, BB-402, BB-604 (v1.0), BB-605/606 (v1.1), CM-003, CM-005, CM-010, CM-011, CM-014–016, CM-020, CM-022–025, CM-027, CM-060, CM-061, CM-062, WC-C2–C8
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections
**Earlier structure:** pages drafted before CM-062 (Apex) keep `methodology/specs/legacy/location-2026-10-08.md`.

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| One city: lean, conversion-focused (BB-201, BB-202) | Service descriptions: link to service pages, never explain them (BB-315, BB-914) |
| This city's genuinely unique conditions and named places (BB-317) | Any service in the URL (BB-208); service+city pages (BB-203) |
| How the client works in this city (Serving section) | Brand-level or service-level questions |
| City-specific questions (FAQ, three, one per category) | A static star rating or review count (CM-027) |

**Ownership inside the page (no overlap):** rules asked as questions belong in the **FAQ**. The **Serving** section says
only how the client handles those rules. **Local context** never describes the client. The **opening** never covers
conditions or logistics.

## 2. Required inputs

| Input | Source |
|---|---|
| Brand, GB category, category variants, separator, phone, **hours** | BG-A1, A2, A3, A7, A8, F |
| City, state, GBP landing page yes/no | BG-C2, A11 |
| Assigned category variant | BG-B3, brief |
| Service page list (services table); sibling city list | BG-C1, C2 |
| Heading and FAQ registry | BG-C3 |
| Verified facts and offer; NAP | BG-D, F |
| Service area truth (city is actually served) | BG-E |
| Superlative decision for this page | BG-H2 |
| The page's **evidence pack**: place and place × niche facts (place store), review excerpts, PAA and fan-out questions, client facts | `build/<section>/packs/<page>.md` (CM-061) |

## 3. Element-by-element structure (in page order — CM-023, CM-062)

| # | Element | Requirement | Rule ID | Source |
|---|---|---|---|---|
| 1 | URL | City slug only, no service | BB-208 | BG-C2 |
| 2 | SEO title | `Brand - GB Category - City, Full State Name`; one city; Title Case; no "The Best"; never truncated | BB-301, BB-302, BB-303, CM-014 | BG-A1, A2, A7, C2 |
| 3 | Meta description | 150–160 chars, names the area and at least two services, soft CTA | WC-C2 | BG-C1, C2 |
| 4 | H1 | One H1. `[Service Variant] in [City]`, **no state**, no brand, differs from title variants. Superlative only if BG-H2 says yes. | BB-304, BB-305, BB-315, CM-020 | BG-A3, C2, H2 |
| 5 | Opening paragraph | No H tag, 60–120 words, unique to this city, triple in a third variant set, phone and offer, first sentence answers. Never covers conditions or logistics. | BB-312, CM-003, WC-C5 | BG-A8, D |
| 6 | H2 services table | H3 links to **all** service pages; **no service descriptions**; rows left as placeholder for Finish | BB-205, BB-315, CM-005 | BG-C1 |
| 7 | H2 Local context | The place: climate, housing stock, terrain, exposure, why the work fails here. **Up to two short paragraphs**, with **3–4 named, verifiable place entities woven in** (from the pack; also the schema `about` entries). Never describes the client. Appears on no other page; no links. | BB-315, BB-317, CM-005, CM-016, CM-062 | Pack: place facts |
| 8 | H2 Serving [City] | How the client operates here: response and travel time, which office issues permits, HOA/ARB experience in named communities, access, storm-season scheduling, hours. **One informational outbound link** to the official town or county page (CM-011). No service explanations; says only how the client handles the rules the FAQ asks about. | CM-011, CM-016, CM-062 | Pack: client facts + place × niche facts |
| 9 | FAQ | H2 wrapper + H3 per question; **three questions, one per category** (location-faq.md): 1 local cost or decision · 2 logistics here · 3 trust here. First sentence answers (CM-060, 40–60 words); none in C3; none on another page. | BB-315, BB-316, CM-060, WC-C7 | Pack: PAA and fan-out first, then place research angle 8, then review language; BG-C3 |
| 10 | H2 Neighbourhoods | **Up to 12**, as many as can be verified. Fewer than 3 verified → drop the section and name them in Local context. | BB-315, BB-317, CM-016 | Pack: place facts |
| 11 | H2 Recent work in [City] | **Optional.** A 3–4 sentence story from a review that names the city, at its usage tier (attributed customer example; "Customers mention…" at 3+ mentions), no reviewer name. **Dropped silently** if no such review exists. | CM-057, CM-027, CM-062 | Pack: reviews |
| 12 | City map | City-level map embed, no H tag; the GBP map only if this is a verified GBP landing page | BB-315 | BG-C2, F |
| 13 | H2 sibling cities | Links to every other location page; rows left as placeholder for Finish | BB-205, BB-315, CM-005 | BG-C2 |
| 14 | CTA | No H tag; **name, phone and hours** matching the GBP exactly; the address **only** on the GBP landing page | BB-315, BB-504 | BG-F |
| — | Every H2 section | Under 500 tokens; readable alone; names its entities; no decorative headers (CM-023) | BB-308, BB-309, BB-310, CM-023 | — |
| — | Specificity and the swap test | At least 3 concrete, verifiable, city-specific facts. **Swap test, per paragraph:** swap the city name for a neighbouring city — if it is still true, rewrite it (a Fix). | CM-015, CM-062 | Pack |
| — | Ratings | **No static star rating or review count**, and no rating schema | CM-027, CM-062 | — |
| — | Word ceiling | Under 1,000 words, unless the excess is genuine city substance (passes) rather than service description (fails) | BB-315, CM-010 | — |
| — | Schema readiness | Non-GBP page: `WebPage` + `ItemList` of service `@id`s, `mainEntity` = ID page; never LocalBusiness. `about` = the ID page, the city, and the 3–4 place entities as `Thing`s with the **Wikidata URI as `@id`** and `sameAs` (Wikipedia, Wikidata, grokipedia) (BB-606). Place entities are **not** put in `mentions` (it is the service catalog). GBP landing page only: LocalBusiness subtype per the GBP test. Recommendation only. | BB-604 (v1.0), BB-605/606 (v1.1), CM-062 | BG-C2, F |

Section minimums are **targets** (CM-061): an optional section that cannot be sourced is shortened or dropped as "Fix and
list"; no page is held for one.

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| LOC-01 | Page covers one city; not a service+city combination; no service in the URL | BB-202, BB-203, BB-208 | §5 Architecture | High |
| LOC-02 | Title follows `Brand - GB Category - City, Full State Name` in that order | BB-301, BB-302 | §6 On-page | High |
| LOC-03 | Title: full state name, one city, Title Case, no "The Best", site separator consistent, no entity term dropped | BB-302, BB-303, CM-014 | §6 On-page | Medium |
| LOC-04 | Exactly one H1 | BB-307 | §6 On-page | High |
| LOC-05 | H1 contains no brand name | BB-305 | §6 On-page | High |
| LOC-06 | H1 names the city with no state, and uses a different variant of every title entity — tested mechanically by COM-11 (CM-046) | BB-304, BB-305, CM-046 | §6 On-page | Medium |
| LOC-07 | H1 superlative matches the BG-H2 decision for this page. A missing "The Best" is never a failed check by itself (CM-020). | CM-020 | §6 On-page | Medium |
| LOC-08 | (Recommendation check) No recommendation changes the H1 of a page in the top 3 for its main keyword | CM-020 | §6 On-page | High |
| LOC-09 | No variant repeats at consecutive elements URL → title → H1 → first H2 | BB-108, CM-024 | §3 Brand, entity | Medium |
| LOC-10 | Opening paragraph: no H tag, phone and offer, first sentence answers, unique to this city, no conditions or logistics | BB-312, CM-003, CM-062 | §6 On-page | Medium |
| LOC-11 | Services table present with H3 links to all service pages | BB-205, BB-315 | §5 Architecture | High |
| LOC-12 | No service descriptions on the page (link, don't explain) | BB-315, BB-914 | §5 Architecture | Medium |
| LOC-13 | Local context: up to two short paragraphs, 3–4 named verifiable place entities woven in, genuinely this city, appears on no other page, no links, never describes the client | BB-317, CM-005, CM-015, CM-062 | §6 On-page | Medium |
| LOC-14 | FAQ: H2 + H3, **three questions, one per category** (local cost or decision · logistics here · trust here), first sentence answers, no question on another page | BB-315, BB-316, CM-060, CM-062 | §6 On-page | Medium |
| LOC-15 | Neighbourhoods: up to 12, all real and verifiable; fewer than 3 → section dropped and named in local context | BB-315, BB-317, CM-016, CM-062 | §3 Brand, entity | Medium |
| LOC-16 | City map present; GBP map used only on a verified GBP landing page | BB-315 | §4 GBP and local | Medium |
| LOC-17 | No Things to Do or Top Sites section (CM-062); the named place entities appear in the text and every one is real and verifiable | BB-317, CM-016, CM-062 | §6 On-page | Medium |
| LOC-18 | Sibling cities section present and links to every other location page (city mesh) | BB-205, BB-315 | §5 Architecture | High |
| LOC-19 | CTA carries name, phone and **hours** matching the GBP exactly; the address appears only on the GBP landing page | BB-315, BB-504, CM-062 | §3 Brand, entity | Medium |
| LOC-20 | Sections present in the CM-062 order (list missing or out of order) | CM-023, CM-062 | §5 Architecture | Medium |
| LOC-21 | No cross-page link in prose, FAQ answers or local context (CM-022 approved exceptions excepted); the Serving section's one official outbound link is the exception (CM-011) | BB-206, CM-005, CM-011, CM-022 | §6 On-page | Medium |
| LOC-22 | Over 1,000 words fails only if the excess is service description or padding; genuine city substance passes | BB-315, CM-010 | §6 On-page | Medium |
| LOC-23 | No decorative headers; every H2 under ~375 words and readable alone | BB-308, BB-309, BB-310 | §6 On-page | Medium |
| LOC-24 | At least 3 city-specific verifiable facts; passes the portability and swap tests; no copied content | CM-015, BB-318, CM-062 | §6 On-page | Medium |
| LOC-25 | Every claim traces to Section D or verified source facts; none from D2 | CM-016, CM-027 | §3 Brand, entity | Medium |
| LOC-26 | Schema readiness: LocalBusiness only if this exact URL is a verified GBP's website; otherwise WebPage + ItemList, no NAP; `about` carries the place entities with Wikidata `@id` | BB-604 (v1.0), BB-605/606 (v1.1) | §9 Schema readiness | High |
| LOC-27 | Sensitive industry: no claim beyond Section D; health claims flagged | CM-025 | §3 Brand, entity | High |
| LOC-28 | Serving [City]: how the client operates here (response and travel time, permit office, HOA/ARB experience, access, storm season, hours), one informational outbound link to the official town or county page, no service explanations, nothing the FAQ owns | CM-011, CM-016, CM-062 | §6 On-page | Medium |
| LOC-29 | Recent work in [City] (when present): 3–4 sentences from a review naming the city, at its usage tier, no reviewer name; absent when no such review exists (never a finding) | CM-057, CM-027, CM-062 | §6 On-page | Medium |
| LOC-30 | Ownership: no rule asked as a FAQ is explained in Local context; Serving does not restate FAQ answers; Local context does not describe the client; the opening carries no conditions or logistics | CM-062 | §6 On-page | Medium |
| LOC-31 | No sentence is still true when the city is swapped for a neighbouring one; no sentence across the section's location pages is too similar (`scripts/similarity.py`, run by `review.py`; rewritten as a Fix) | CM-015, CM-062 | §6 On-page | Medium |
| LOC-32 | No static star rating or review count, no rating schema | CM-027, CM-062 | §3 Brand, entity | Medium |

## 5. Variants and collisions

- Vertical only (CM-024): no variant at two consecutive elements on this page (BB-108).
- Location pages sharing a category variant is correct. Never the homepage's reserved B1 variants.
- More pages than variants: one "variant list exhausted" finding (CM-013).

## 6. Links

- Services table (H3 links to every service page) and sibling-cities table (every other location page): BB-205, BB-206. Never in prose, FAQ answers or local context (CM-005).
- Leave rows as placeholders for Finish: `| [Link wheel: populate service links here] |`, `| [Link wheel: populate sibling-city links here] |` (WC-C8).
- The Serving section carries **one informational outbound link** to the official town or county page (CM-011). Other outbound authority links and one proposed contextual link (CM-022) are exceptions only via Finish, with a stated reason, logged, Paul approves.

## 7. Sensitive-industry additions

- No health, legal, financial or insurance claim beyond Section D (CM-025, WC-A).
- Medical and chiropractic health claims carry `[PRACTITIONER REVIEW]`.
- No superlative in the H1 unless Paul approves (CM-020 condition 4).
- Do not manufacture uniqueness between cities (analysis-rules §4): missing local facts are `[NEED: …]`, never invented.

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
| 2026-10-14 | All elements | New order: Things to Do and Top Sites removed (place entities woven into Local context and the schema), Serving [City] added, FAQ three per category, neighbourhoods up to 12, optional Recent work, CTA with hours, ownership and swap rules, no ratings | CM-062 (Paul, rewrite 3 §0) |
