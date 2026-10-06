# Spec — County hub page
**Status:** DRAFT — awaiting Paul's review (build and audit treat a DRAFT spec as advisory; Paul marks it APPROVED)
**Governs:** county hub page · **Rule sources:** BB-207, BB-208, BB-301–304, BB-306–312, BB-316–318, BB-604 (v1.0), CM-003, CM-005, CM-014–016, CM-024, CM-025, CM-027, WC-C2, WC-C4, WC-C5, WC-C7, WC-C8
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections

> The Standard gives a county hub only a title format (BB-302) and forbids empty hubs (BB-207).
> It gives no section structure. Every element marked **Coastal default — needs Paul's ruling**
> is our proposal, built from BB-315's location pattern and the general on-page rules. Audit
> reports those elements at Low at most until Paul rules.

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| One county: which served cities it contains and what is true county-wide | Any single city's content (location pages own that) |
| A navigation and association role between the county and its location pages | Service descriptions (service pages, BB-201) |
| — | Being an empty `/service-area/`-style hub (BB-207) |

**When a county hub exists at all:** decided per site on verified geography, operations, intent, query evidence, link usability and maintenance capacity (analysis-rules §5). Coastal default — needs Paul's ruling on the trigger (e.g. a minimum number of served cities in the county).

## 2. Required inputs

| Input | Source |
|---|---|
| Brand, GB category, category variants, separator, phone | BG-A1, A2, A3, A7, A8 |
| County name and state (verified, Wikipedia form); BB-105 derivation path | BG-A area derivation |
| Served cities in this county, with their location page URLs | BG-C2, E |
| Service page list | BG-C1 |
| Heading and FAQ registry | BG-C3 |
| Verified facts, offer, NAP | BG-D, F |
| County-level source facts (verified) | Brief |

## 3. Element-by-element structure (in page order)

| # | Element | Requirement | Rule ID | Brand Guide source |
|---|---|---|---|---|
| 1 | URL | Root-proximate county slug, no service | BB-208 | BG-A derivation |
| 2 | SEO title | `Brand - GB Category - County, Full State Name`; Title Case; no "The Best"; never truncated | BB-301, BB-302, BB-303, CM-014 | BG-A1, A2, A7 |
| 3 | Meta description | 150–160 chars, names the county and at least two services, soft CTA | WC-C2 | BG-C1 |
| 4 | H1 | One H1, no brand, different variant of every title entity (BB-304). Format `[Service Variant] in [County]`, no state, superlative per BG-H2 | BB-304, BB-307; format: Coastal default — needs Paul's ruling | BG-A3, H2 |
| 5 | Opening paragraph | No H tag, 60–120 words, triple in a third variant set, phone and offer, first sentence answers | BB-312, CM-003, WC-C5 | BG-A8, D |
| 6 | H2 cities served in this county | H3 link to each location page in the county; rows left as placeholder for Finish | Coastal default — needs Paul's ruling | BG-C2 |
| 7 | H2 county context | 3–5 sentences of genuinely county-wide conditions, not repeated from any city page; no links | Coastal default — needs Paul's ruling (uniqueness per BB-317, BB-318, CM-015) | Brief source facts |
| 8 | H2 services table | H3 links to all service pages, no descriptions; placeholder for Finish | Coastal default — needs Paul's ruling | BG-C1 |
| 9 | FAQ | H2 + H3 per question; first sentence answers; no question on another page (BB-316). Count 3–4, county-level | BB-316; count: Coastal default — needs Paul's ruling | BG-C3 |
| 10 | Map | County-level map embed, no H tag; not the GBP map unless a verified GBP lands here | Coastal default — needs Paul's ruling | BG-F |
| 11 | CTA with NAP | No H tag; NAP matches BG-F | BB-504; placement: Coastal default — needs Paul's ruling | BG-F |
| — | Every H2 section | Under 500 tokens; names its entities; readable alone; no decorative headers | BB-308, BB-309, BB-310 | — |
| — | Real content | Not an empty hub: carries county substance, not just a link list | BB-207 | — |
| — | Word ceiling | Under 1,000 words, matching location pages | Coastal default — needs Paul's ruling | — |
| — | Wheel position | Whether location pages link up to their hub and service pages link to hubs | Coastal default — needs Paul's ruling | — |
| — | Schema readiness | Never LocalBusiness unless this exact URL is a verified GBP's website; otherwise WebPage | BB-604 (v1.0); node set: Coastal default — needs Paul's ruling | BG-F |

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| HUB-01 | Hub has real county content and a purpose; not an empty link-only hub | BB-207 | §5 Architecture | High |
| HUB-02 | Title follows `Brand - GB Category - County, Full State Name` in that order | BB-302 | §6 On-page | High |
| HUB-03 | Title: full state name, Title Case, no "The Best", separator consistent, no entity term dropped | BB-302, BB-303, CM-014 | §6 On-page | Medium |
| HUB-04 | URL root-proximate, no service in slug | BB-208 | §5 Architecture | Medium |
| HUB-05 | Exactly one H1, no brand | BB-305, BB-307 | §6 On-page | High |
| HUB-06 | H1 uses a different variant of every title entity — tested mechanically by COM-11 (CM-046) | BB-304, CM-046 | §6 On-page | Medium |
| HUB-07 | H1 superlative matches the BG-H2 decision for this page. A missing "The Best" is never a failed check by itself (CM-020) — the check is whether the H1 matches the Brand Guide H2 decision for this page. | CM-020 | §6 On-page | Medium |
| HUB-08 | (Recommendation check) No recommendation changes the H1 of a page in the top 3 for its main keyword | CM-020 | §6 On-page | High |
| HUB-09 | No variant repeats at consecutive elements; not the homepage's reserved B1 variant | BB-108, CM-024 | §3 Brand, entity | Medium |
| HUB-10 | Opening paragraph: no H tag, phone and offer, first sentence answers | BB-312, CM-003 | §6 On-page | Medium |
| HUB-11 | Links to every location page in the county (Coastal default) | Coastal default | §5 Architecture | Low |
| HUB-12 | County context is county-wide and appears on no city page | BB-317, BB-318, CM-015 | §6 On-page | Medium |
| HUB-13 | FAQ format: H2 + H3, first sentence answers, no question on another page | BB-316 | §6 On-page | Medium |
| HUB-14 | No cross-page link in prose, FAQ answers or county context | BB-206, CM-005 | §6 On-page | Medium |
| HUB-15 | No decorative headers; every H2 under ~375 words | BB-308, BB-309 | §6 On-page | Medium |
| HUB-16 | Every claim traces to Section D or verified source facts; county and cities real | CM-016, CM-027 | §3 Brand, entity | Medium |
| HUB-17 | Schema readiness: no LocalBusiness unless the GBP test passes | BB-604 (v1.0) | §9 Schema readiness | High |
| HUB-18 | Sensitive industry: no claim beyond Section D; health claims flagged | CM-025 | §3 Brand, entity | High |

## 5. Variants and collisions

- Vertical only (CM-024): no variant at two consecutive elements (BB-108). Never the reserved B1 variant.
- The county itself is a real area name (BB-109); a county used as a homepage area variant belongs to the homepage only.

## 6. Links

- City and service links live in tables/H3 only, never in prose (BB-206, CM-005); rows left as Finish placeholders (WC-C8).
- Exceptions via CM-022 only, with Paul's approval in Finish.

## 7. Sensitive-industry additions

- No claim beyond Section D (CM-025); medical and chiropractic health claims carry `[PRACTITIONER REVIEW]`; no H1 superlative without Paul (CM-020).

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
