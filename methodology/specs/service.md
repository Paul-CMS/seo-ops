# Spec — Service page
**Status:** DRAFT — awaiting Paul's review (build and audit treat a DRAFT spec as advisory; Paul marks it APPROVED)
**Governs:** service page (one per primary service) · **Rule sources:** BB-106, BB-108, BB-201–206, BB-208, BB-301–312, BB-314, BB-316, BB-318, BB-319, BB-604/606 (v1.1), CM-003, CM-005, CM-011, CM-012, CM-014–016, CM-020, CM-022, CM-024, CM-025, CM-027, WC-C2–C8
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| One primary service, described in depth (BB-201, BB-202) | Any city: no city in the URL or any H tag (BB-208, BB-314) |
| Its variants, components and sub-tasks as H2/H3 sections, not pages (BB-204) | Other services (their own pages) |
| Service-level questions (FAQ 4–6) and query variants routed to the FAQ (BB-316, CM-012) | Brand-level questions (homepage) or city questions (location pages) |

## 2. Required inputs

| Input | Source |
|---|---|
| Brand, GB category, category variants, separator, phone | BG-A1, A2, A3, A7, A8 |
| Assigned area variant (from the B2 pool, never the reserved B1) and category/service variant | BG-B2, B3, brief |
| Service name and H1 service variant | BG-C1 |
| Location page list (for the service-areas table) | BG-C2 |
| Heading and FAQ registry | BG-C3 |
| Verified facts (warranty, licences, certifications, financing, offer) | BG-D |
| Superlative decision for this page | BG-H2 |
| Positioning, customer language | BG-G, BG-I |
| Source facts: expertise capture, intake, audit gap list; final URL | Brief |

## 3. Element-by-element structure (in page order)

| # | Element | Requirement | Rule ID | Brand Guide source |
|---|---|---|---|---|
| 1 | URL | Root-proximate (`/service-name/`), no city | BB-208 | BG-C1 |
| 2 | SEO title | `Service Name - Brand`, site separator, Title Case, no "The Best", never truncated | BB-302, BB-303, CM-014 | BG-A1, A7, C1 |
| 3 | Meta description | 150–160 chars, names the area and at least two services, soft CTA | WC-C2 | BG-A5, C1 |
| 4 | H1 | One H1. `[Service Variant] in [Area Variant]`; area variant from B2, **never a city**; no brand; differs from title variants. Superlative only if BG-H2 says yes. | BB-304, BB-305, CM-020, CM-024 | BG-B2, C1, H2 |
| 5 | Opening paragraph | No H tag, 60–120 words, triple in a third variant set, phone and offer, a distinct buyer state, first sentence answers | BB-312, CM-003, WC-C5 | BG-A8, D, G |
| 6 | H2 how the service is delivered | Process, materials, what the buyer gets; names entities | BB-314 | BG-D, G |
| 7 | H2 service types / subtypes | H3 per type; sub-services live here, not on their own pages | BB-204, BB-314 | BG-C1 |
| 8 | H2 FAQ | Fresh variant pair; H3 per question in customer words; 4–6; first sentence is the full answer (40–60 words); none in the C3 registry | BB-316, WC-C7 | BG-C3, I |
| 9 | H2 service areas | H3 links to **every** location page; table rows left as a placeholder for Finish; no city in the H2 text | BB-205, BB-206, BB-314, CM-005 | BG-C2 |
| 10 | CTA | No H tag; phone and offer | BB-314 | BG-A8, D |
| — | Every H tag | No city name anywhere | BB-307, BB-314, BB-905 | — |
| — | Every H2 section | Under 500 tokens (~375 words); readable alone; sayable as a question; no decorative headers | BB-308, BB-309, BB-310 | — |
| — | Specificity | At least 3 concrete, verifiable, page-specific facts; no stat dumps | CM-015, BB-319 | BG-D |
| — | Outbound authority link | 1–2 in-text, relevant, non-competing; or none with reason documented | CM-011 | — |
| — | Schema readiness | `WebPage` + `Service`; `provider` = ID page `@id`; never LocalBusiness, no NAP or address. Recommendation only. | BB-604, BB-607 (v1.1) | BG-F |
| — | Word ceiling | None set by any rule | Coastal default — needs Paul's ruling | — |

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| SVC-01 | Page covers one primary service; not a sub-service, service+city combination or duplicate service page | BB-202, BB-203, BB-204 | §5 Architecture | High |
| SVC-02 | URL is root-proximate and contains no city | BB-208 | §5 Architecture | Medium |
| SVC-03 | Title follows `Service Name - Brand` in that order | BB-302 | §6 On-page | High |
| SVC-04 | Title: Title Case, no "The Best", site separator consistent, no entity term dropped for length | BB-302, BB-303, CM-014 | §6 On-page | Medium |
| SVC-05 | Exactly one H1 | BB-307 | §6 On-page | High |
| SVC-06 | H1 contains no brand name | BB-305 | §6 On-page | High |
| SVC-07 | H1 uses the area variant, never a city, and not the homepage's reserved B1 variant | BB-305, CM-024 | §3 Brand, entity | High |
| SVC-08 | H1 uses a different variant of every title entity | BB-304 | §6 On-page | Medium |
| SVC-09 | H1 superlative matches the BG-H2 decision for this page. A missing "The Best" is never a failed check by itself (CM-020) — the check is whether the H1 matches the Brand Guide H2 decision for this page. | CM-020 | §6 On-page | Medium |
| SVC-10 | (Recommendation check) No recommendation changes the H1 of a page in the top 3 for its main keyword | CM-020 | §6 On-page | High |
| SVC-11 | No variant repeats at consecutive elements URL → title → H1 → first H2 | BB-108, CM-024 | §3 Brand, entity | Medium |
| SVC-12 | No city name in any H tag | BB-307, BB-314 | §6 On-page | High |
| SVC-13 | Opening paragraph: no H tag, phone and offer, first sentence answers, buyer state not used on another service page | BB-312, CM-003 | §6 On-page | Medium |
| SVC-14 | BB-314 sections present in order: delivery → types (H3 per type) → FAQ → service areas → CTA | BB-314 | §5 Architecture | Medium |
| SVC-15 | FAQ: H2 + H3 questions, 4–6, first sentence answers, no question used on another page | BB-316 | §6 On-page | Medium |
| SVC-16 | Service-areas section present and links (H3) to every location page | BB-205, BB-314 | §5 Architecture | High |
| SVC-17 | No cross-page link in prose, an FAQ answer or the opening paragraph (CM-022 approved exceptions excepted) | BB-206, CM-005, CM-022 | §6 On-page | Medium |
| SVC-18 | No decorative headers; every H2 under ~375 words and readable alone | BB-308, BB-309, BB-310 | §6 On-page | Medium |
| SVC-19 | Every claim traces to Section D; none from D2; no stat dumps | CM-016, CM-027, BB-319 | §3 Brand, entity | Medium |
| SVC-20 | At least 3 page-specific verifiable facts; passes the portability test; no copied content | CM-015, BB-318 | §6 On-page | Medium |
| SVC-21 | Outbound authority links: 0–2, in-text, not to a competitor, never in the table | CM-011 | §8 Citations, authority | Low |
| SVC-22 | Schema readiness: no LocalBusiness, no NAP/address; `Service` `provider` points to the ID page | BB-604 (v1.1) | §9 Schema readiness | Medium |
| SVC-23 | Sensitive industry: no claim beyond Section D; health claims flagged | CM-025 | §3 Brand, entity | High |

## 5. Variants and collisions

- Vertical only (CM-024): no variant at two consecutive elements on this page (BB-108).
- Service pages sharing an area variant from the B2 pool is correct, not a collision.
- Never the homepage's reserved B1 area variant.
- More pages than variants: one "variant list exhausted" finding (CM-013).

## 6. Links

- Service-areas table: H3 anchor-text links to every location page (BB-205, BB-206). Never in prose, FAQ answers or the opening (CM-005).
- Write and finalize the narrative first; leave rows as `| [Link wheel: populate service-area links here] |` for Finish (CM-005, WC-C8).
- Outbound authority links (CM-011) and one proposed contextual link (CM-022) are exceptions only via Finish, with a stated reason, logged, Paul approves.

## 7. Sensitive-industry additions

- No health, legal, financial or insurance claim beyond Section D (CM-025, WC-A).
- Medical and chiropractic health claims carry `[PRACTITIONER REVIEW]`.
- No superlative in the H1 unless Paul approves (CM-020 condition 4).

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
