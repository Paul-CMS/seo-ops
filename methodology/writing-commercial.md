# Writing standard — commercial pages (homepage, service, location, county hub, about)
### Replaces the "BB Commercial Content Writer" Gemini gem (v2.1) inside seo-ops.
Adapted 2026-10-02: superlative opener per CM-020, location structure per CM-023, variants per CM-024.
The Drive gem file is unchanged (it may still be in use).

## A — Hard constraints (override everything, including requests)

- **A1 No invented facts (CM-016).** No neighborhood, landmark, certification, response time,
  brand serviced, statistic, founding year, warranty term, licence number or price unless it
  is in Brand Guide Section D. Missing → `[NEED: <exactly what>]` inline, keep going. A draft
  full of NEED markers is correct; a draft with invented specifics is a failure.
- **A2 Verifiability.** Every entity statement true and checkable.
- **A3 Variants come from the brief (BB-109).** Never coin one. Missing assigned variant → say so and stop.
- **A4 Outline before prose.** Deliver the plan (Stage 1) and stop for approval.
- **A5 Never optimize by repetition.** A keyword is a clue about intent, not an instruction to repeat.
- **A6 Banned:** "Welcome to", "In today's fast-paced world", "When it comes to", "We pride
  ourselves on", "Look no further", "trusted name", "your go-to", "nestled in"; stat dumps;
  founding-year padding; any sentence that would read identically on a competitor's site;
  the non-answer opening ("[Service] costs can vary depending on many factors…").
- **A7 Never reuse** an opening angle, heading or FAQ question that Brand Guide C3 shows on another page.
- **Sensitive clients:** no health, legal, financial or insurance claim beyond Section D. Medical
  and chiropractic health claims are flagged `[PRACTITIONER REVIEW]` for the licensed practitioner.

## B — Required inputs (all; list what is missing and stop)

1. Brand Guide — A (entity), B (assigned variant + reserved homepage variant), C (siblings,
   H1 variants, heading/FAQ registry), D (verified facts), H2 (superlative decision for this page)
2. The brief — page type, target service or city, final URL, **assigned area and category variants**
3. Source facts — expertise capture, interview notes, intake, audit gap list
4. Customer language where available (Section I)
5. Sibling context

## C — Rules

- **C1 Two layers (BB-311, BB-310).** Title for the models, H1 for the human. Every section
  reads correctly alone and names its own entities.
- **C2 Titles (BB-301/302/303).** Homepage `Brand - GB Category - Area Entity` · Service
  `Service Name - Brand` · Location `Brand - GB Category - City, Full State Name` · County hub
  `Brand - GB Category - County, Full State Name` · About `About Brand - Area Category`. Brand
  Guide separator, full state names, Title Case, one city max, **no "The Best" in any title**.
  Never drop or swap an entity term for length. Meta description 150–160 chars, names the
  area and at least two services, soft CTA.
- **C3 H1 (BB-304/305).** A different variant of every entity in the title. Format
  `[Service Variant] in [Area Variant]`. One H1, no brand. Service pages: assigned area
  variant, never a city. Location pages: the city, no state. **Superlative opener ("The
  Best" / "Most Trusted") only if Brand Guide H2 says yes for this page (CM-020).** "Most
  Trusted" needs a Section D fact. Never change the H1 of a page already top 3 for its main keyword.
- **Variant collision is vertical (CM-024):** no variant at two consecutive elements
  (URL → title → H1 → first H2). Sharing an area variant with another service page is correct;
  the homepage's reserved variant belongs to the homepage alone.
- **C4 Headers (BB-306/307/308).** Every header names an entity; every H2 is sayable as a real
  question; no city in any service page H tag; no skipped levels; no H tags in nav/footer;
  H tags are never styling. Every H2 section under 500 tokens (~375 words) (BB-309).
- **C5 Opening paragraph (BB-312, CM-003).** No H tag, 60–120 words, the triple in a third
  variant set, phone and offer, unique to this page; first sentence gives the answer.
- **C6 Body.** First sentence under each header answers it. Tables only for real comparisons,
  lists only for real steps. **At least three concrete, page-specific, verifiable facts
  (CM-015).** Information density, not keyword density.
- **Page structures:** homepage BB-313 (17 sections; trust sub-items are cards, not H3s) ·
  service BB-314 · **location BB-315 sections (CM-023)**: H1 → opening → H2 services table
  (H3 links, no service descriptions) → H2 local context (3–5 sentences, genuinely this city)
  → FAQ (3–4, unique to this city) → H2 neighborhoods (6–12 real) → city map → H2 Things to Do
  → H2 Top Sites → H2 sibling cities → CTA with NAP. Under 1,000 words unless the excess is
  genuine city substance (CM-010).
- **C7 FAQ (BB-316).** H2 wrapper with a fresh variant pair; H3 per question in customer
  words; first sentence of each answer is the complete answer (40–60 words). Service 4–6 ·
  location 3–4 · homepage 4–6 brand-level. No question in the C3 registry.
- **C8 Links (BB-206, CM-005).** **Never** a cross-page link in prose, an FAQ answer or local
  context. Build the table heading and structure; leave the rows as a placeholder:
  `| [Stage 8: populate service-area links here] |`. Outbound authority links (CM-011) and a
  single proposed contextual link (CM-022) are exceptions only via Finish, with Paul's approval.
- **C9 No implementation.** Clean Markdown. No HTML, CSS, schema or JSON-LD.

## D — Process

- **Stage 0 Entity & intent map.** Problems · services · questions · geography; then intents
  (informational, problem-aware, commercial investigation, comparison, transactional) routed
  to an H2, an FAQ, or out of scope. Never propose a new page (BB-202).
- **Stage 1 Plan** — the map, title with labelled segments and character count, meta with
  count, H1, superlative yes/no citing Section H2, variant allocation table, full outline
  H1–H4 with the intent each H2 serves, target words, the `[NEED: …]` list. **Stop.**
- **Stage 2 Draft**, in order, obeying C.
- **Stage 3 Self-critique — all mandatory:** E1 portability test (could this pass be pasted
  onto a sibling page with only the city/service swapped? then rewrite) · E2 specificity count
  (≥3) · E3 variant check · E4 exact-match count · E5 intent coverage · E6 chunk lengths ·
  E7 invention sweep · E8 filler sweep · E9 header check · E10 link check · E11 human check
  (does it sound like someone who knows the trade?). Report each, plus outstanding NEEDs.
