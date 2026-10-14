# Spec — Location page
**Status:** APPROVED — 2026-10-08, Paul
**Governs:** location page (one per city) · **Rule sources:** BB-108, BB-201–206, BB-208, BB-301–312, BB-315–318, BB-402, BB-604 (v1.0), BB-605/606 (v1.1), CM-003, CM-005, CM-010, CM-011, CM-014–016, CM-020, CM-022–025, CM-027, WC-C2–C8
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| One city: lean, conversion-focused (BB-201, BB-202) | Service descriptions: link to service pages, never explain them (BB-315, BB-914) |
| This city's genuinely unique conditions, neighborhoods, sites (BB-317) | Any service in the URL (BB-208); service+city pages (BB-203) |
| City-specific questions (FAQ 3–4) | Brand-level or service-level questions |

## 2. Required inputs

| Input | Source |
|---|---|
| Brand, GB category, category variants, separator, phone | BG-A1, A2, A3, A7, A8 |
| City, state, GBP landing page yes/no | BG-C2, A11 |
| Assigned category variant | BG-B3, brief |
| Service page list (services table); sibling city list | BG-C1, C2 |
| Heading and FAQ registry | BG-C3 |
| Verified facts and offer; NAP | BG-D, F |
| Service area truth (city is actually served) | BG-E |
| Superlative decision for this page | BG-H2 |
| Source facts: real local conditions, neighborhoods, things to do, top sites (verified, never invented) | Brief, intake, research |

## 3. Element-by-element structure (in page order — CM-023)

| # | Element | Requirement | Rule ID | Brand Guide source |
|---|---|---|---|---|
| 1 | URL | City slug only, no service | BB-208 | BG-C2 |
| 2 | SEO title | `Brand - GB Category - City, Full State Name`; one city; Title Case; no "The Best"; never truncated | BB-301, BB-302, BB-303, CM-014 | BG-A1, A2, A7, C2 |
| 3 | Meta description | 150–160 chars, names the area and at least two services, soft CTA | WC-C2 | BG-C1, C2 |
| 4 | H1 | One H1. `[Service Variant] in [City]`, **no state**, no brand, differs from title variants. Superlative only if BG-H2 says yes. | BB-304, BB-305, BB-315, CM-020 | BG-A3, C2, H2 |
| 5 | Opening paragraph | No H tag, 60–120 words, unique to this city, triple in a third variant set, phone and offer, first sentence answers | BB-312, CM-003, WC-C5 | BG-A8, D |
| 6 | H2 services table | H3 links to **all** service pages; **no service descriptions**; rows left as placeholder for Finish | BB-205, BB-315, CM-005 | BG-C1 |
| 7 | H2 local context | 3–5 sentences on this city's genuinely unique conditions (housing stock, terrain, weather, failure patterns); appears on no other page; no links | BB-315, BB-317, CM-005, CM-016 | Brief source facts |
| 8 | FAQ | H2 wrapper + H3 per question; 3–4 questions unique to this city — each about this town or the service here, with its reason in the site plan (a routed PAA/fan-out question is a candidate, not an obligation); first sentence answers (40–60 words); none in C3 | BB-315, BB-316, WC-C7 | BG-C3 |
| 9 | H2 neighborhoods | 6–12 real, verifiable neighborhoods | BB-315, BB-317, CM-016 | Brief source facts |
| 10 | City map | City-level map embed, no H tag; the GBP map only if this is a verified GBP landing page | BB-315 | BG-C2, F |
| 11 | H2 Things to Do | Real, verifiable | BB-315, BB-317 | Brief source facts |
| 12 | H2 Top Sites | Real, verifiable | BB-315, BB-317 | Brief source facts |
| 13 | H2 sibling cities | Links to every other location page; rows left as placeholder for Finish | BB-205, BB-315, CM-005 | BG-C2 |
| 14 | CTA with NAP | No H tag; NAP matches BG-F exactly | BB-315, BB-504 | BG-F |
| — | Every H2 section | Under 500 tokens; readable alone; names its entities; no decorative headers. No "2–3 H2s" limit (CM-023). | BB-308, BB-309, BB-310, CM-023 | — |
| — | Specificity | At least 3 concrete, verifiable, city-specific facts | CM-015 | Brief source facts |
| — | Word ceiling | Under 1,000 words, unless the excess is genuine city substance (passes) rather than service description (fails) | BB-315, CM-010 | — |
| — | Outbound authority link | 1–2 in-text (e.g. city code page), or none with reason documented | CM-011 | — |
| — | Schema readiness | Non-GBP page: `WebPage` + `ItemList` of service `@id`s, `mainEntity` = ID page; never LocalBusiness. GBP landing page only: LocalBusiness subtype per the GBP test. Recommendation only. | BB-604 (v1.0), BB-605 (v1.1) | BG-C2, F |

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| LOC-01 | Page covers one city; not a service+city combination; no service in the URL | BB-202, BB-203, BB-208 | §5 Architecture | High |
| LOC-02 | Title follows `Brand - GB Category - City, Full State Name` in that order | BB-301, BB-302 | §6 On-page | High |
| LOC-03 | Title: full state name, one city, Title Case, no "The Best", site separator consistent, no entity term dropped | BB-302, BB-303, CM-014 | §6 On-page | Medium |
| LOC-04 | Exactly one H1 | BB-307 | §6 On-page | High |
| LOC-05 | H1 contains no brand name | BB-305 | §6 On-page | High |
| LOC-06 | H1 names the city with no state, and uses a different variant of every title entity — tested mechanically by COM-11 (CM-046) | BB-304, BB-305, CM-046 | §6 On-page | Medium |
| LOC-07 | H1 superlative matches the BG-H2 decision for this page. A missing "The Best" is never a failed check by itself (CM-020) — the check is whether the H1 matches the Brand Guide H2 decision for this page. | CM-020 | §6 On-page | Medium |
| LOC-08 | (Recommendation check) No recommendation changes the H1 of a page in the top 3 for its main keyword | CM-020 | §6 On-page | High |
| LOC-09 | No variant repeats at consecutive elements URL → title → H1 → first H2 | BB-108, CM-024 | §3 Brand, entity | Medium |
| LOC-10 | Opening paragraph: no H tag, phone and offer, first sentence answers, unique to this city | BB-312, CM-003 | §6 On-page | Medium |
| LOC-11 | Services table present with H3 links to all service pages | BB-205, BB-315 | §5 Architecture | High |
| LOC-12 | No service descriptions on the page (link, don't explain) | BB-315, BB-914 | §5 Architecture | Medium |
| LOC-13 | Local context: 3–5 sentences, genuinely this city, appears on no other page, no links | BB-317, CM-005, CM-015 | §6 On-page | Medium |
| LOC-14 | FAQ: H2 + H3, 3–4 questions unique to this city, first sentence answers, no question on another page | BB-315, BB-316 | §6 On-page | Medium |
| LOC-15 | Neighborhoods: 6–12, all real and verifiable | BB-315, BB-317, CM-016 | §3 Brand, entity | Medium |
| LOC-16 | City map present; GBP map used only on a verified GBP landing page | BB-315 | §4 GBP and local | Medium |
| LOC-17 | Things to Do and Top Sites present; every item real and verifiable | BB-315, BB-317, CM-016 | §6 On-page | Medium |
| LOC-18 | Sibling cities section present and links to every other location page (city mesh) | BB-205, BB-315 | §5 Architecture | High |
| LOC-19 | CTA carries NAP matching BG-F exactly | BB-315, BB-504 | §3 Brand, entity | Medium |
| LOC-20 | BB-315 sections present in CM-023 order (list missing or out of order) | BB-315, CM-023 | §5 Architecture | Medium |
| LOC-21 | No cross-page link in prose, FAQ answers or local context (CM-022 approved exceptions excepted) | BB-206, CM-005, CM-022 | §6 On-page | Medium |
| LOC-22 | Over 1,000 words fails only if the excess is service description or padding; genuine city substance passes | BB-315, CM-010 | §6 On-page | Medium |
| LOC-23 | No decorative headers; every H2 under ~375 words and readable alone | BB-308, BB-309, BB-310 | §6 On-page | Medium |
| LOC-24 | At least 3 city-specific verifiable facts; passes the portability test; no copied content | CM-015, BB-318 | §6 On-page | Medium |
| LOC-25 | Every claim traces to Section D or verified source facts; none from D2 | CM-016, CM-027 | §3 Brand, entity | Medium |
| LOC-26 | Schema readiness: LocalBusiness only if this exact URL is a verified GBP's website; otherwise WebPage + ItemList, no NAP | BB-604 (v1.0), BB-605 (v1.1) | §9 Schema readiness | High |
| LOC-27 | Sensitive industry: no claim beyond Section D; health claims flagged | CM-025 | §3 Brand, entity | High |

## 5. Variants and collisions

- Vertical only (CM-024): no variant at two consecutive elements on this page (BB-108).
- Location pages sharing a category variant is correct. Never the homepage's reserved B1 variants.
- More pages than variants: one "variant list exhausted" finding (CM-013).

## 6. Links

- Services table (H3 links to every service page) and sibling-cities table (every other location page): BB-205, BB-206. Never in prose, FAQ answers or local context (CM-005).
- Leave rows as placeholders for Finish: `| [Link wheel: populate service links here] |`, `| [Link wheel: populate sibling-city links here] |` (WC-C8).
- Outbound authority links (CM-011) and one proposed contextual link (CM-022) are exceptions only via Finish, with a stated reason, logged, Paul approves.

## 7. Sensitive-industry additions

- No health, legal, financial or insurance claim beyond Section D (CM-025, WC-A).
- Medical and chiropractic health claims carry `[PRACTITIONER REVIEW]`.
- No superlative in the H1 unless Paul approves (CM-020 condition 4).
- Do not manufacture uniqueness between cities (analysis-rules §4): missing local facts are `[NEED: …]`, never invented.

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
