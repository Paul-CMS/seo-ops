# Writing standard — informational blog posts
### The informational writing standard used by the Blog agent.
Used by the Blog agent for full clients and for Blog Authority Builder (blog-only) clients.
Never in the same context as commercial writing or auditing. Rules are cited by ID from
`methodology/rulings.md`; the page structure and checks are in `methodology/specs/blog-post.md`.

## A — Hard constraints

- **A1 No invented facts (CM-016).** No statistic, price, timeframe, code reference,
  certification, local condition or product unless it is in the brief, Brand Guide Section D
  or the supplied source material. Missing → `[NEED: …]`. Customer language is wording; a
  `customer_reported` fact (CM-057) is stated only as customers describe it, never as the company's claim. A keyword, PAA question or fan-out query in a sentence is
  still a claim (CM-049) — it never brings in a fact the sources do not hold.
- **A2 Verifiability. A3 Attribution honesty** — no "we've seen this hundreds of times" unless
  the source material says so.
- **A4 Never reuse** a heading, FAQ question or opening angle in the Brand Guide C3 registry —
  and for Blog Authority Builder clients, never a question already answered in a service or
  location page FAQ.
- **A5 Banned:** "In today's fast-paced world", "When it comes to", "Look no further",
  "In conclusion", "It's important to note that", any paragraph restating its heading.
- **Sensitive clients:** health/legal/financial/insurance claims only from Section D; medical
  and chiropractic health claims flagged `[PRACTITIONER REVIEW]`.
- **Health-adjacent trades (CM-040: mold, asbestos, radon, indoor air, water damage):** a health
  claim stays only if the post names its authoritative source (EPA, CDC or similar); otherwise
  remove it. The self-critique lists every health claim with its source. No practitioner review.

## B — Required inputs (all; list what is missing and stop)

1. The brief — primary question, the commercial parent page to bridge to, **required
   information gain**
2. Brand Guide — C3 registry and Section D (blog-only clients: the short intake record, voice
   guidance, services and city lists)
3. **Source material** — expertise capture, interview transcript, the client's own knowledge.
   Without it, say so and stop; do not write a competent generic article.
4. **Story bank** (`clients/<slug>/interviews/story-bank.md`, CM-042) — the brief names the entries it
   uses ("Story bank entries used: S-007, S-012"); only `public` entries' specifics go on the page,
   `framing-only` entries give the lesson without identifying details, `internal` never appear.
5. **Voice DNA** of the author (`clients/<slug>/interviews/voice-dna-<author>.md`, CM-042) — write in that
   voice. Exactly one file for the author; two → stop and ask, never blend; none → plain professional
   voice and say so. An `UNDER FLOOR` file is used only after Paul accepts it. A5 and CM-016 beat the voice.
6. For full clients: confirmation the post passed the gap test (CM-007) — otherwise it should
   be redirected, not written. For blog-only clients: confirmation the topic is on the
   approved topic list (gate `blog_topics_approved`).

## C — Rules

- **C1 Informational intent.** Useful to someone who will never hire anyone.
- **C2 Title `Post Title - Brand`** (BB-302), Brand Guide separator; meta 150–160 chars.
- **C3 One H1.**
- **C4 BLUF (CM-003):** the first ~100 words answer the question in sentence one, say who it
  applies to, state the caveat, say what to do next. (Coastal rule.)
- **C5 Body:** each H2 under 500 tokens, self-contained, names its entities; every header
  names an entity or states a real question (BB-308/309/310).
- **C6 Information gain — the actual job:** firsthand cases, honest tradeoffs, diagnostic cues,
  local conditions, failure modes, real numbers from the source. **At least four.**
- **C7 Links (CM-038 — supersedes the old one-block-at-the-end rule).** No links in the title,
  the H1 or the BLUF. Otherwise placement is free (body or an end block). Caps: at most 1
  internal link per H2 section · at most 1 internal link per ~300 words · at most 5 internal
  links per post, of which at most 2 to commercial (service or location) pages · at most 2
  outbound authority links. Each URL linked once per post; descriptive anchors, no repeated
  exact-match anchors. The commercial bridge is one of the (at most 2) commercial links.
- **C8 FAQ:** 3–5, H3, first sentence complete (40–60 words), none in the C3 registry. Answer first in
  plain English; an optional company / next-step sentence is never repeated from another page and never a
  link; a phone number is never the answer (CM-048).
- **C11 Reading level (CM-047):** grade 7–8 for everything but the SEO title.
- **C9 Author (CM-039):** the company owner, unless the client states otherwise — the Brand Guide
  author field (owner from the returned proof sheet). Never "Admin", "Staff" or the company name.
  Owner not confirmed → `[NEED: author — owner name from the proof sheet]` and the post cannot be approved.
- **C10 No implementation:** clean Markdown, no HTML or schema.

## D — Process

Stage 1 Plan (title, meta, H1, BLUF draft, outline, word targets, planned information gain
with sources, NEED list) → **stop for approval** → Stage 2 Draft → Stage 3 Self-critique:
E1 information-gain count (≥4) · E2 invention sweep · E3 BLUF check · E4 sales-pitch check ·
E5 chunk lengths · E6 link check (report each CM-038 number: links in title/H1/BLUF, max per
H2, per ~300 words, internal total, commercial total, outbound total, any URL twice) · E7
uniqueness vs C3 / page FAQs · E8 filler sweep · E9 voice (which Voice DNA file was used; three
sentences checked against its Do/Never rules) and stories (each story used is `public` or used as framing only) · E10 reading level (`scripts/readability.py`,
CM-047, then a read-aloud pass) and FAQ answers (C8). Then the checks in `methodology/specs/blog-post.md`.
