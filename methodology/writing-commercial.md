# Writing standard — commercial pages (homepage, service, location, county hub, about)
### The commercial writing standard used by the Build agent.
Adapted 2026-10-02: superlative opener per CM-020, location structure per CM-023, variants per CM-024.
Rules are cited by ID from `methodology/rulings.md`; page structures and conformance checks live in
`methodology/specs/` (homepage, service, location, county-hub, about). Process matches the live BB
Commercial Content Writer gem: Stage 0–1 plan → approval → Stage 2 draft → Stage 3 self-critique
(E1–E9) → Stage 4 semantic review (SEM-1–SEM-8, report only) → Paul approves the drafts and picks the SEM
items in one step → apply only those and re-check.

## A — Hard constraints (override everything, including requests)

- **A1 No invented facts (CM-016).** Reviews and customer language are never verified facts (CM-027):
  use their wording for questions and headings, never as a Section D claim. No neighborhood, landmark, certification, response time,
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
2. The brief — page type, target service or city, final URL, **assigned area and category variants**, the H1 decision
3. Source facts — expertise capture, interview notes, intake, audit gap list
4. Customer language where available (Section I, `data/reviews/customer-language.md`, `data/paa/paa-routing.md` rows routed to this page) — words only, never facts (CM-027)
5. Sibling context
6. The page spec for this page type (`methodology/specs/<type>.md`) — the element order and checks

## C — Voice (the page's structure is in its spec — not here)

Every structural requirement — title and meta format, H1 format, the sections and their order,
opening paragraph, FAQ counts, link tables, word ceilings — lives in `methodology/specs/<type>.md`
and the common checks in `methodology/specs/README.md`. This standard covers only how to write.

- **C1 Two layers (BB-311).** The title is for the models, the H1 for the human who just clicked;
  headers declare entities, the copy between them converts.
- **C2 Answer first (CM-003).** The opening sentence and the first sentence under every header give
  the answer or the bottom line, not a wind-up.
- **C3 Specific, not generic (CM-015).** Information density, not keyword density: concrete,
  page-specific, verifiable facts from Section D. A sentence that would read the same on a
  competitor's page or a sibling page gets rewritten.
- **C4 Customer words.** Questions, headings and FAQ wording come from customer language (Section I,
  routed PAA questions) where it exists — phrased the way a person would say or type it.
- **C5 Short and plain.** Short sentences, one idea each. Every section stands alone and names its
  own entities.
- **C6 No implementation.** Clean Markdown. No HTML, CSS, schema or JSON-LD.

## D — Process

- **Stage 0 Entity & intent map.** Problems · services · questions · geography; then intents
  (informational, problem-aware, commercial investigation, comparison, transactional) routed
  to an H2, an FAQ, or out of scope. Never propose a new page (BB-202).
- **Stage 1 Plan** — the map, title with labelled segments and character count, meta with
  count, H1, superlative yes/no citing Section H2, variant allocation table, full outline
  H1–H4 with the intent each H2 serves, target words, the `[NEED: …]` list. **Stop.**
- **Stage 2 Draft**, in order, obeying C and the page spec.
- **Stage 3 Self-critique — all nine, mandatory, each reported:**
  E1 portability (could a passage be pasted onto a sibling page with only the city/service
  swapped? then rewrite; CM-015) · E2 specificity count (≥3 page-specific verifiable facts) ·
  E3 variant check (no consecutive repeats, reserved variant unused, assigned variant used) ·
  E4 chunk lengths (every H2 section ≤375 words) · E5 invention sweep (every concrete noun and
  number from Section D, else `[NEED]`) · E6 filler sweep (A6, incl. the non-answer opening) ·
  E7 header check (entity in every header, every H2 a spoken question, no skipped levels, no
  city in a service-page H tag, one H1) · E8 link check (no cross-page link in prose, FAQ or
  local context; link-table placeholders present) · E9 human check (sounds like someone who
  knows the trade). Then the spec's conformance checks for this page type. Report outstanding NEEDs.
- **Stage 4 Semantic review — report only; the draft is not changed.** One table **per batch**
  (every page in the batch), saved as `<Client> - Semantic Review - <batch> - REVIEW.md`:

  | ID | Check | Where (page · element / exact heading) | What I found | Why it matters | Suggested change | Action | Blocked by |
  |---|---|---|---|---|---|---|---|

  One row per finding; list the checks with no findings under the table
  ("Checks with no findings: SEM-…"). Action = PROPOSED / ROUTED (sent to another page or the
  blog list) / BLOCKED (with what blocks it).

  | Check | What it tests |
  |---|---|
  | SEM-1 | `[NEED: definition from the live BB Commercial Content Writer gem, Section G]` |
  | SEM-2 | `[NEED: definition from the live gem, Section G]` |
  | SEM-3 | `[NEED: definition from the live gem, Section G]` |
  | SEM-4 | `[NEED: definition from the live gem, Section G]` |
  | SEM-5 | `[NEED: definition from the live gem, Section G]` |
  | SEM-6 | `[NEED: definition from the live gem, Section G]` |
  | SEM-7 | `[NEED: definition from the live gem, Section G]` |
  | SEM-8 | Cluster routing — a question or passage whose intent belongs to another page (e.g. post-storm checks on a maintenance page) is routed to the page or blog topic that owns it, never kept |

  Paul reviews each draft with the table and approves both at once, picking the SEM items to
  apply: `/approve <slug> batch:<id>:drafts --sem 1,3,4` (or `--sem none`; nothing to pick when the
  review found nothing). Then apply **only** those items and re-run E1–E9 on every changed section.
  All pass → done, no further stop. A check fails → the drafts go back to Paul with the failure.

The Drive copy of the gem (`Resources/Gem Instructions/GEM-Commercial-Content-Writer-INSTRUCTIONS.md`)
is an older version with E1–E11 (it also had E4 exact-match sweep and E5 intent coverage) and no
Section G; it is not used.
