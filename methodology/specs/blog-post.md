# Spec — Blog post (informational)
**Status:** DRAFT — awaiting Paul's review (build and audit treat a DRAFT spec as advisory; Paul marks it APPROVED)
**Governs:** informational blog post · **Rule sources:** BB-201, BB-302, BB-307–310, BB-316, BB-318, BB-603 (v1.0), BB-701–704, BB-913, CM-003, CM-004, CM-007, CM-011, CM-012, CM-016, CM-021, CM-025, CM-027, CM-038, CM-039, WB-A–C
**Used by:** Build (briefs and drafts), Audit (conformance scorecard, S15), Finish QA, pilot corrections

> Conflicts resolved here: WB-C7 (one link block at the end) and BB-704's separated-link-block
> clause are superseded for blog posts by **CM-038**. WB-C9 (named author) is made specific by
> **CM-039**.

## 1. Purpose and intent this page owns / does not own

| Owns | Does not own |
|---|---|
| One real informational question, useful to someone who will never hire anyone (WB-C1) | The same entity + location as a service or location page (BB-701, BB-913) |
| What no commercial page answers: brand story, technical deep-dives, FAQ-style questions (BB-703) | A new standalone commercial page (CM-012, BB-202) |
| An AI Search Gap answer, if the post is protected (CM-007) | Service sales copy |

**Before writing (full clients):** the post passed the gap test (CM-007) and has no observed search conflict with a commercial page (CM-021). Otherwise it is a redirect candidate, not a post (BB-702). **Blog-only clients:** topic is on the approved topic list (WB-B4).

## 2. Required inputs

| Input | Source |
|---|---|
| Primary question; commercial parent page(s) to bridge to; required information gain | Brief |
| Source material: expertise capture, interview transcript, client knowledge. Missing → stop (WB-B3) | Brief |
| Brand name and separator | BG-A1, A7 |
| Author = owner from the returned proof sheet, unless the client states otherwise | Brand Guide author field, BG-F owner (CM-039) |
| Heading and FAQ registry (and, for blog-only clients, all page FAQs) | BG-C3 |
| Verified facts | BG-D |
| Gap-test result (CM-007) or approved-topic confirmation | Brief / Blog Decision Map |

## 3. Element-by-element structure (in page order)

| # | Element | Requirement | Rule ID | Brand Guide source |
|---|---|---|---|---|
| 1 | URL | Short, describes the question; no service+city combination | BB-208 (general), BB-913 | — |
| 2 | SEO title | `Post Title - Brand`, site separator; no links | BB-302, BB-704, CM-038 | BG-A1, A7 |
| 3 | Meta description | 150–160 chars | WB-C2 | — |
| 4 | H1 | One H1; no links. Format not set by any rule | BB-307, WB-C3, CM-038; format: Coastal default — needs Paul's ruling | — |
| 5 | Author byline | The company owner, unless the client states otherwise; never "Admin", "Staff" or the company name. Unconfirmed → `[NEED: author — owner name from the proof sheet]`, blocks approval | CM-039, CM-004 | Brand Guide author field |
| 6 | BLUF (first ~100 words) | Sentence one answers the question; says who it applies to, the caveat, what to do next; no links | CM-003, WB-C4, CM-038 | Source material |
| 7 | H2 body sections | Each under 500 tokens (~375 words), self-contained, names its entities; every header names an entity or states a real question | BB-308, BB-309, BB-310, WB-C5 | — |
| 8 | Information gain | At least 4 items from the source material: firsthand cases, honest tradeoffs, diagnostic cues, local conditions, failure modes, real numbers | WB-C6, CM-016 | Source material, BG-D |
| 9 | FAQ | H3 per question, 3–5, first sentence is the full answer (40–60 words); none in the C3 registry or (blog-only) any page FAQ | BB-316, WB-C8, WB-A4 | BG-C3 |
| 10 | Links | Body or end block, within the CM-038 caps (section 6) | CM-038 | Brief (parent pages) |
| 11 | Dates | Published and modified dates shown (Article schema inputs) | BB-704 | — |
| — | Tone | No sales pitch; no banned phrases; attribution honest | WB-A3, WB-A5 | — |
| — | Word ceiling | None set by any rule | Coastal default — needs Paul's ruling | — |
| — | Schema readiness | `Article` with author, datePublished, dateModified (v1.0 rule, unverified in v1.1). Recommendation only. | BB-603 (v1.0), BB-704 | BG-F owner |

## 4. Conformance checks (the audit scorecard)

| Check ID | Check | Rule ID | Audit category | Fails as |
|---|---|---|---|---|
| BLG-01 | Post does not target the same entity + location as a service or location page, or is a protected AI Search Gap post | BB-701, BB-913, CM-007 | §7 Blog | High |
| BLG-02 | (Recommendation check) No redirect is proposed without observed conflict (GSC or DataforSEO, both ranking for the same query), and never for a protected post | CM-007, CM-021 | §7 Blog | High |
| BLG-03 | Title follows `Post Title - Brand`, site separator | BB-302, BB-704 | §6 On-page | Medium |
| BLG-04 | Exactly one H1 | BB-307, WB-C3 | §6 On-page | High |
| BLG-05 | Author is the owner (or the client's stated author), named and checkable; not generic; no unresolved `[NEED]` at approval | CM-039, CM-004 | §3 Brand, entity | Medium |
| BLG-06 | BLUF: first sentence answers the question within the first ~100 words | CM-003, WB-C4 | §6 On-page | Medium |
| BLG-07 | No links in the title, H1 or BLUF | CM-038 | §7 Blog | Medium |
| BLG-08 | Max 1 internal link per H2 section | CM-038 | §7 Blog | Medium |
| BLG-09 | Max 1 internal link per ~300 words | CM-038 | §7 Blog | Medium |
| BLG-10 | Max 5 internal links per post, of which max 2 to service or location pages | CM-038 | §7 Blog | Medium |
| BLG-11 | Max 2 outbound authority links | CM-038, CM-011 | §8 Citations, authority | Medium |
| BLG-12 | Each URL linked once; descriptive anchors; no repeated exact-match anchors | CM-038 | §7 Blog | Medium |
| BLG-13 | Every H2 under ~375 words, readable alone; no decorative headers | BB-308, BB-309, BB-310 | §6 On-page | Medium |
| BLG-14 | At least 4 information-gain items, each traceable to the source material | WB-C6 | §7 Blog | Medium |
| BLG-15 | FAQ: 3–5, H3, first sentence answers; no question used elsewhere on the site | BB-316, WB-C8 | §6 On-page | Medium |
| BLG-16 | Every statistic, price, code reference or credential traces to the brief, Section D or source material | CM-016, CM-027 | §3 Brand, entity | Medium |
| BLG-17 | Informational, not a sales pitch; no copied content from another page | WB-C1, BB-318 | §7 Blog | Medium |
| BLG-18 | Schema readiness: `Article` with author, datePublished, dateModified | BB-603 (v1.0), BB-704 | §9 Schema readiness | Low |
| BLG-19 | Sensitive industry: no claim beyond Section D; health claims flagged | CM-025 | §3 Brand, entity | High |
| BLG-20 | Reading level grade 7–8 (`scripts/readability.py`: average ≤ 8.9, no paragraph over 10); SEO title excluded | CM-047 | §7 Blog | Low |
| BLG-21 | FAQ answers: first sentence answers in plain English; any company/next-step sentence optional, never repeated from another page, never a link; a phone number is never the answer | CM-048, BB-316 | §6 On-page | Medium |
| BLG-22 | No keyword, PAA question or fan-out query brings an Unknown or Unverified fact into the post | CM-049, CM-016 | §3 Brand, entity | Medium |

## 5. Variants and collisions

- Blog posts take no assigned area variant. They must not claim the entity + location of a commercial page (BB-701) or reuse a C3 heading or question (WB-A4).
- Conversational queries go to an existing page's FAQ or become a blog gap candidate; never a new standalone page (CM-012).

## 6. Links (CM-038 — caps exactly)

| Rule | Cap |
|---|---|
| Title, H1, BLUF | **No links** |
| Per H2 section | Max **1** internal |
| Density | Max **1** internal per ~300 words |
| Per post, internal | Max **5**, of which max **2** to commercial (service or location) pages |
| Outbound authority | Max **2** |
| Repeats | Each URL **once** per post; descriptive anchors; no repeated exact-match anchors |

Placement is otherwise free (body or end block). The writer's link check reports each number. These caps replace WB-C7 and BB-704's end-block clause for blog posts.

## 7. Sensitive-industry additions

- Health, legal, financial and insurance claims only from Section D (CM-025, WB-A).
- Medical and chiropractic health claims flagged `[PRACTITIONER REVIEW]` for the licensed practitioner in BG-D.
- Reviews are never cited as facts (CM-027).

## 8. Pilot corrections log

Corrections Paul makes during the pilot are applied here, each as a dated line: date · element/check ID · what changed · why. The build may not start the next batch until the corrections are recorded (status.py pilot-corrections).

| Date | Element / check ID | What changed | Why |
|---|---|---|---|
