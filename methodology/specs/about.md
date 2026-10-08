# Spec — About page
**Status:** APPROVED — 2026-10-08, Paul
**Governs:** about page · **Rule sources:** BB-201, BB-302–304, BB-306–310, BB-312, BB-316, BB-318, BB-504, BB-603 (v1.0), CM-003, CM-004, CM-014–016, CM-024, CM-025, CM-027, CM-039, WC-C2, WC-C4, WC-C5, WC-C7
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections

> The Standard gives the about page a title format (BB-302) and a v1.0 schema rule (BB-603,
> which v1.1 marks unverified). It gives no section structure. Elements marked **Coastal
> default — needs Paul's ruling** are our proposal, built from CM-004 (verifiable experience)
> and the general on-page rules. Audit reports those at Low at most until Paul rules.

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| Who the business is: owner, team, history, credentials, all verifiable (BB-104 brand level, CM-004) | Service descriptions (service pages) or city content (location pages) |
| The owner as a real, checkable person (also the default blog author, CM-039) | Brand-level FAQs already on the homepage (BB-316 no duplicates) |

## 2. Required inputs

| Input | Source |
|---|---|
| Brand entity, legal entity name, separator, phone, area entity | BG-A1, A5, A7, A8, A10 |
| Owner name and photo | BG-F "Owner name + photo", proof sheet |
| Founding year, licences, certifications, associations, awards, named staff | BG-D |
| Positioning in the client's own words | BG-G |
| Heading and FAQ registry | BG-C3 |
| NAP | BG-F |

## 3. Element-by-element structure (in page order)

| # | Element | Requirement | Rule ID | Brand Guide source |
|---|---|---|---|---|
| 1 | URL | Short, root-proximate (e.g. `/about/`) | BB-208 | — |
| 2 | SEO title | `About Brand - Area Category`, site separator, Title Case, no "The Best" | BB-302, CM-014; meaning of "Area Category": Coastal default — needs Paul's ruling | BG-A1, A2/A5, A7 |
| 3 | Meta description | 150–160 chars, names the area and at least two services, soft CTA | WC-C2 | BG-A5, C1 |
| 4 | H1 | One H1, no brand (BB-305), differs from title (BB-304). Format, e.g. `About [Category Variant] in [Area Variant]` from B2 | BB-304, BB-307; format: Coastal default — needs Paul's ruling | BG-B2 |
| 5 | Opening paragraph | No H tag, 60–120 words, who/what/where in the first sentence, phone | BB-312, CM-003, WC-C5 | BG-A, A8 |
| 6 | H2 owner / founder | Named owner, real photo, verifiable background | CM-004, CM-039; section: Coastal default — needs Paul's ruling | BG-F owner, D |
| 7 | H2 credentials | Licences, insurance, certifications, associations, awards — Section D only, as cards or a list | CM-004, CM-016; section: Coastal default — needs Paul's ruling | BG-D |
| 8 | H2 team | Named staff tied to the service area, only those approved for on-page use | CM-004; section: Coastal default — needs Paul's ruling | BG-D named staff |
| 9 | H2 history / story | Founding year and milestones from Section D only; no founding-year padding | CM-016, WC-A6; section: Coastal default — needs Paul's ruling | BG-D, G |
| 10 | H2 service area | Area entity stated; no per-city H tags | BB-307; section: Coastal default — needs Paul's ruling | BG-A5, E |
| 11 | FAQ | Optional. If present: H2 + H3, first sentence answers, no question used on another page | BB-316; inclusion and count: Coastal default — needs Paul's ruling | BG-C3 |
| 12 | CTA with NAP | No H tag; NAP matches BG-F | BB-504; placement: Coastal default — needs Paul's ruling | BG-F |
| — | Every H2 section | Under 500 tokens; names its entities; no decorative headers ("Our Story" alone fails; name the entity) | BB-308, BB-309, BB-310 | — |
| — | Corroboration | Names, numbers and credentials match the GBP, citations and press releases | CM-004, BB-504 | BG-D, F |
| — | Word ceiling | None set by any rule | Coastal default — needs Paul's ruling | — |
| — | Schema readiness | `Person` for the owner + `Organization` for the brand, referencing the ID page `@id`; v1.0 rule, unverified in v1.1 | BB-603 (v1.0), BB-607 (v1.1) | BG-F |

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| ABT-01 | Title follows `About Brand - Area Category` in that order | BB-302 | §6 On-page | High |
| ABT-02 | Title: Title Case, no "The Best", separator consistent, no entity term dropped | BB-302, BB-303, CM-014 | §6 On-page | Medium |
| ABT-03 | Exactly one H1, no brand | BB-305, BB-307 | §6 On-page | High |
| ABT-04 | H1 uses a different variant of every title entity; not the reserved B1 variant | BB-304, CM-024 | §6 On-page | Medium |
| ABT-05 | (Recommendation check) No recommendation changes the H1 of a page in the top 3 for its main keyword | CM-020 | §6 On-page | High |
| ABT-06 | Opening paragraph: no H tag, first sentence states who/what/where | BB-312, CM-003 | §6 On-page | Medium |
| ABT-07 | Owner named, with a real photo; not "the team" or the company name only | CM-004, CM-039 | §3 Brand, entity | Medium |
| ABT-08 | Every credential, year, count and award traces to Section D; none from D2 | CM-016, CM-027 | §3 Brand, entity | Medium |
| ABT-09 | Names and numbers match the GBP and citations (no conflicting statements) | BB-103, BB-504, CM-004 | §3 Brand, entity | High |
| ABT-10 | No service descriptions or city content duplicated from other pages | BB-201, BB-318 | §5 Architecture | Medium |
| ABT-11 | No decorative headers; every H2 under ~375 words | BB-308, BB-309 | §6 On-page | Medium |
| ABT-12 | No H tags in nav/footer; no per-city H tags | BB-307 | §6 On-page | Medium |
| ABT-13 | FAQ, if present: correct format, no question used on another page | BB-316 | §6 On-page | Medium |
| ABT-14 | NAP matches BG-F exactly | BB-504 | §3 Brand, entity | Medium |
| ABT-15 | Schema readiness: owner `Person` + brand `Organization` tied to the ID page; no conflicting second business entity | BB-603 (v1.0), BB-607 (v1.1) | §9 Schema readiness | Medium |
| ABT-16 | Sensitive industry: no claim beyond Section D; practitioner credentials verified | CM-025 | §3 Brand, entity | High |

## 5. Variants and collisions

- Vertical only (CM-024): no variant at two consecutive elements (BB-108). Never the homepage's reserved B1 variant.

## 6. Links

- No link table is required by any rule. Links to service pages, if any, follow CM-005 (no cross-page links in prose) — Coastal default — needs Paul's ruling on whether the about page carries a services list.
- Outbound links to licensing bodies or associations that verify a Section D credential: allowed as CM-011-style authority links, proposed via Finish (CM-022).

## 7. Sensitive-industry additions

- No health, legal, financial or insurance claim beyond Section D (CM-025).
- Practitioner credentials shown exactly as verified; medical and chiropractic health claims carry `[PRACTITIONER REVIEW]`.

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
