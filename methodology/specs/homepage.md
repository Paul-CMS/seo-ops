# Spec — Homepage
**Status:** DRAFT — awaiting Paul's review (build and audit treat a DRAFT spec as advisory; Paul marks it APPROVED)
**Governs:** homepage (`/`) · **Rule sources:** BB-105, BB-108, BB-110, BB-201, BB-301–313, BB-316, BB-318, BB-402, BB-601–603/607/608 (v1.1), CM-003, CM-004, CM-014–016, CM-020, CM-024, CM-025, CM-027, WC-C2–C8
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| The brand hub: who the business is, what it does (GB category), where (area entity) (BB-201, BB-301) | Describing any single service (service pages own that, BB-201) |
| The area entity that contains every city served (BB-105, BB-908) | Any single city (location pages) |
| Brand-level questions: who, trust, how it works, coverage (BB-316) | Service- or city-specific FAQs |
| Usually the GBP landing page (BB-402) | — |

## 2. Required inputs

| Input | Source |
|---|---|
| Brand entity, GB category, area entity, separator, phone, domain, GBP website URL | BG-A1, A2, A5, A7, A8, A9, A11 |
| Reserved homepage area + category variants | BG-B1 |
| Service list (for the H3 links) and city list (for the areas grid) | BG-C1, C2, E |
| Heading and FAQ registry (no reuse) | BG-C3 |
| Verified facts: rating and review count, awards, licences, guarantees, offer | BG-D |
| Superlative decision for this page | BG-H2 |
| NAP exactly as published | BG-F "Confirmed NAP" |
| Positioning and customer language | BG-G, BG-I |
| Brief: final URL, assigned variants per element | Brief |

## 3. Element-by-element structure (in page order)

| # | Element | Requirement | Rule ID | Brand Guide source |
|---|---|---|---|---|
| 0a | URL | Root domain, canonical host form | BB-208 | BG-A9 |
| 0b | SEO title | `Brand - GB Category - Area Entity`, site separator, Title Case, full state names, no "The Best", never truncated | BB-301, BB-302, BB-303, CM-014 | BG-A1, A2, A5, A7 |
| 0c | Meta description | 150–160 chars, names the area and at least two services, soft CTA | WC-C2 | BG-A5, C1 |
| 1 | Review bar (above nav) | Rating and count from Section D; no H tag | BB-313 §1, CM-027 | BG-D rating row |
| 2 | Navigation | Top-level pages only; no H tags | BB-313 §2, BB-307 | — |
| 3 | H1 | One H1. `[Category Variant] in [Area Variant]` from the reserved B1 variants, a different variant of every title entity, no brand. Superlative only if BG-H2 says yes. Never changed once live. | BB-304, BB-305, BB-313 §3, CM-020, CM-024 | BG-B1, H2 |
| 4 | Opening paragraph | No H tag, 60–120 words, triple in a third variant set, phone and offer, first sentence answers who/what/where | BB-312, CM-003, WC-C5 | BG-A, A8, D (offer) |
| 5 | H2 "[GB Category variant] Services" | The only H2 that introduces services | BB-313 §5 | BG-A3 |
| 6 | H3 service links | One H3 anchor-text link per service page, no descriptions, max 5–6 | BB-201, BB-313 §6 | BG-C1 |
| 7 | Trust / About | H2; sub-items are styled cards, **not H3**; claims only from Section D | BB-313 §7, CM-004, CM-016 | BG-D, G |
| 8 | How It Works | 3 steps, styled bold, no H tags | BB-313 §8 | BG-G |
| 9 | Social proof bar | No H tag; rating/count from Section D | BB-313 §9, CM-027 | BG-D |
| 10 | Gallery | H2; alt text `[service type] in [city], [State] — [Brand]`, vary cities; real project photos | BB-313 §10, CM-004 | BG-C1, C2 |
| 11 | Testimonials | H2; real reviews, chosen to mention services and cities; never used as verified facts | BB-313 §11, CM-027 | BG-I |
| 12 | FAQ | H2 with fresh variant pair + H3 per question; 4–6 brand-level questions; first sentence is the full answer (40–60 words); none in the C3 registry | BB-313 §12, BB-316, WC-C7 | BG-C3 |
| 13 | Service areas grid | H2; cities listed, **not** H-tagged per city | BB-313 §13 | BG-C2, E |
| 14 | Google Maps embed | GBP iframe, no H tag | BB-313 §14 | BG-F Maps share link |
| 15 | Featured blog posts | H2; build only after blog redirects are live | BB-313 §15 | — |
| 16 | Final CTA | H2 naming an entity (not "Get Started") | BB-313 §16, BB-308 | BG-A8 |
| 17 | Footer | NAP exact match; **zero H tags** | BB-313 §17, BB-307, BB-504 | BG-F NAP |
| — | Every H2 section | Under 500 tokens (~375 words); names its own entities; sayable as a question | BB-308, BB-309, BB-310 | — |
| — | Specificity | At least 3 concrete, verifiable, homepage-specific facts | CM-015, WC-C6 | BG-D |
| — | Schema readiness | Two-node graph (Corporation + HomeAndConstructionBusiness subtype), location `@id` = ID page URL, identical full `sameAs` on both, `hasMap` = share link, `WebSite` node defined. Recommendation only. | BB-601, 602, 603, 607, 608 (v1.1) | BG-F |
| — | Word ceiling | None set by any rule | Coastal default — needs Paul's ruling | — |

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| HP-01 | Title follows `Brand - GB Category - Area Entity` in that order | BB-301, BB-302 | §6 On-page | High |
| HP-02 | Title uses the GBP primary category (or Wikipedia-verified variant) and the approved area entity — not one city when many are served | BB-105, BB-106, BB-908 | §3 Brand, entity | High |
| HP-03 | Title: full state name, Title Case, no "The Best", site separator used consistently, no entity term dropped for length | BB-302, BB-303, CM-014 | §6 On-page | Medium |
| HP-04 | Exactly one H1 | BB-307 | §6 On-page | High |
| HP-05 | H1 contains no brand name | BB-305 | §6 On-page | High |
| HP-06 | H1 uses a different variant of every title entity, and uses the reserved B1 variants | BB-304, CM-024 | §3 Brand, entity | Medium |
| HP-07 | H1 superlative matches the BG-H2 decision for this page. A missing "The Best" is never a failed check by itself (CM-020) — the check is whether the H1 matches the Brand Guide H2 decision for this page. | CM-020 | §6 On-page | Medium |
| HP-08 | (Recommendation check) No recommendation changes the homepage H1 once live, or the H1 of any page in the top 3 for its main keyword | BB-313 §3, CM-020 | §6 On-page | High |
| HP-09 | No variant repeats at consecutive elements URL → title → H1 → first H2 | BB-108, CM-024 | §3 Brand, entity | Medium |
| HP-10 | Opening paragraph: no H tag, contains phone and offer, first sentence states who/what/where | BB-312, CM-003 | §6 On-page | Medium |
| HP-11 | Exactly one H2 introduces services; services appear as H3 links with no descriptions, max 5–6 | BB-201, BB-313 §5–6 | §5 Architecture | Medium |
| HP-12 | Trust sub-items are cards, not H3s; How It Works steps carry no H tags | BB-313 §7–8, BB-306 | §6 On-page | Medium |
| HP-13 | Review bar, social proof bar and Maps embed carry no H tags; review figures match Section D | BB-313 §1, 9, 14, CM-027 | §6 On-page | Medium |
| HP-14 | Gallery alt text follows `[service type] in [city], [State] — [Brand]` and varies cities | BB-313 §10 | §6 On-page | Low |
| HP-15 | FAQ: H2 wrapper + H3 questions, 4–6, brand-level only, first sentence answers, no question used on another page | BB-313 §12, BB-316 | §6 On-page | Medium |
| HP-16 | Service areas grid present; cities are not individually H-tagged | BB-313 §13, BB-307 | §6 On-page | Medium |
| HP-17 | Featured blog section absent or built after blog redirects are live | BB-313 §15 | §7 Blog | Low |
| HP-18 | Footer and nav contain zero H tags; footer NAP matches BG-F exactly | BB-307, BB-313 §17, BB-504 | §3 Brand, entity | Medium |
| HP-19 | No decorative headers ("Why Choose Us", "Our Process", "Get Started") | BB-308 | §6 On-page | Medium |
| HP-20 | Every H2 section under ~375 words and readable alone | BB-309, BB-310 | §6 On-page | Medium |
| HP-21 | Every claim (years, licences, awards, guarantees) traces to Section D; none from D2 | CM-016, CM-027 | §3 Brand, entity | Medium |
| HP-22 | At least 3 concrete, verifiable, page-specific facts; passes the portability test | CM-015, BB-318 | §6 On-page | Medium |
| HP-23 | All 17 BB-313 parts present in order (list missing parts) | BB-313 | §5 Architecture | Medium |
| HP-24 | Schema readiness: business entity defined once here, two-node graph, ID page `@id`, full identical `sameAs`, `hasMap` share link, `WebSite` node present | BB-601–603, 607, 608 (v1.1) | §9 Schema readiness | Medium |
| HP-25 | Sensitive industry: no claim beyond Section D; health claims flagged | CM-025 | §3 Brand, entity | High |

## 5. Variants and collisions

- Collisions are vertical, not horizontal (CM-024): no variant at two consecutive elements on this page (BB-108).
- The homepage owns the reserved B1 area and category variants. No other page may use them; the homepage uses nothing from the B2 pool at H1.
- Too few variants for the page count is one finding, "variant list exhausted" (CM-013), not page edits.

## 6. Links

- Services: H3 anchor-text links in part 6 only (BB-201, BB-313 §6). Cities: the areas grid, part 13.
- No cross-page links in prose or FAQ answers (CM-005, WC-C8). Leave link rows as placeholders for Finish: `| [Stage 8: populate service links here] |`.
- Outbound authority link or one contextual link: exception only, proposed with a reason, logged, Paul approves in Finish (CM-022).

## 7. Sensitive-industry additions

- No health, legal, financial or insurance claim beyond Section D (CM-025, WC-A).
- Medical and chiropractic health claims carry `[PRACTITIONER REVIEW]` for the licensed practitioner named in BG-D.
- No superlative in the H1 unless Paul approves (CM-020 condition 4).
- Reviews may be shown as testimonials but never restated as facts (CM-027).

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
