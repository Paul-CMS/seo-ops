# THE COASTAL DELTA

**Consolidated into methodology/rulings.md on 2026-10-02 — rulings.md governs; this file is the historical source.**
### Every place Coastal Marketing adds to, extends, overrides or exempts itself from the Bradley Standard
**Coastal Marketing Strategies · v1.0 DRAFT · Companion to BB-Standard-v1.0**

---

## What this file is for

The Bradley Standard holds his methodology. This holds ours.

Nothing in here is Bradley. Some of it extends him, some overrides him, some fills gaps he
never addressed. All of it is legitimate — but a VA needs to know which is which when a
client asks "why?", and an AI needs to know which rules can bend and which cannot.

**The test:** if you cannot point to a `BB-###` rule, it belongs here.

### Entry types

| Type | Meaning |
|---|---|
| **ADD** | Bradley is silent. We have a rule; he has none. |
| **EXTEND** | His rule stands; we make it more specific or operational. |
| **OVERRIDE** | His rule is scoped, conditioned or replaced. Always needs Paul's approval. |
| **EXEMPT** | His rule stands generally; named cases are excused. |
| **OPEN** | Unresolved. Neither confirmed nor rejected. Do not treat as settled. |

### Status

`APPROVED` governs · `PILOT` in limited use with enhanced QA · `DRAFT` not in force ·
`OPEN` awaiting evidence

---

## CM-001 · Destructive vs constructive asymmetry · OVERRIDE
**Scopes:** BB-202, BB-203, BB-204, BB-207, BB-210, BB-701, BB-702
**Status:** APPROVED · **Approved by:** Paul · **Refs:** GOV-06 §1, RULE-005/007/015

**Bradley says** redundant pages, sub-service pages, combination pages, empty hubs and
competing blog posts get consolidated and redirected.

**Coastal says** the methodology governs **how things are built** and produces a
**candidate** — never a decision — for **destroying** them. Construction follows the
Standard with no evidence required. Destruction requires evidence.

**Why** His architecture rules were derived from what works when building. They were not
derived from, and say nothing about, what a specific existing page currently earns. Those
are different questions and the methodology only answers the first.

**Operational** Any conversion, lead or attributable job in 12 months → keep, improve in
place. Backlinks, GBP/citation dependency or paid traffic → keep the URL. Traffic with no
conversion data → Needs Evidence, do not act. No traffic, no conversions, no dependencies
over 12 months → consolidation candidate. **Never delete; always redirect.** Full
value/dependency check recorded in the URL Decision Map.

---

## CM-002 · "The Best" is untested · OPEN
**Scopes:** BB-305
**Status:** OPEN · **Resolves:** BB_Test_The_Best_Cohort, day 42

**Bradley says** "The Best" opens every service and location H1 — a confirmed AI search
trigger word for recommendation queries.

**The problem** "Confirmed" appears in a derived document with no source cited. It is the
only grade-C claim carrying portfolio-wide weight. It was last confirmed in the
GutterXperts-era work, and every model behind every AI surface has been replaced at least
once since.

**Ruling until the test resolves** Keep it. It costs nothing measurable and a
portfolio-wide change on an untested hunch is the larger risk. **Do not flag its absence
above Low severity.** Do not add it to a page currently performing well — that page is a
free variant slot in the cohort and changing it destroys the baseline.

---

## CM-003 · BLUF openings · ADD
**Extends:** BB-310, BB-312 · **Status:** PILOT

**Bradley is silent** on where the answer sits inside an opening paragraph.

**Coastal says** the first sentence or two states who/what/where before any scene-setting
or brand-story preamble.

**Why** Compatible with his passage-level retrieval model and his H3 question + paragraph
answer FAQ format, but he never states it as a rule for the opening paragraph. Blog
rewrites are exactly where old posts bury the answer under a long intro.

---

## CM-004 · E-E-A-T verifiable experience layer · ADD
**Status:** PILOT · **Source:** newsletter research, not Bradley

**Coastal says** cosmetic trust badges and author bios move nothing on their own. What is
evaluated is whether claimed experience is corroborated across the entity's whole
footprint: real project photos, named technicians tied to the service area, specific
checkable numbers, and a cross-check that those numbers and names match the GBP, citations
and press releases.

**Why** It operationalizes his consistency principle (BB-103) on the trust layer, but the
E-E-A-T framing and the corroboration check are ours.

---

## CM-005 · Content/links separation · EXTEND
**Extends:** BB-205, BB-206 · **Status:** PILOT

**Bradley says** cross-page links live in the service-areas and sibling-cities tables.

**Coastal says** protect that separation deliberately. Write and finalize all narrative
content first. Build the table with its heading and structure but leave rows as a labeled
placeholder. Never embed a cross-page link in body prose, an FAQ answer or the
local-context section.

**Why** So a link-wheel update edits one table block per page and never reopens approved
narrative copy — no re-approval cycle with the client. His rule is architectural; this
operational discipline is ours.

**Exception** Outbound authority links (CM-011) are exempt — they are not part of the
internal wheel and will not need mass updates.

---

## CM-006 · Benchmarks are planning targets · EXTEND
**Extends:** BB-502, BB-512, BB-804 · **Status:** APPROVED · **Refs:** RULE-004

**Coastal says** the 100/65/200 citation benchmarks, the competitor-average link ceiling
and the 16-of-20 supporting asset threshold are **planning benchmarks, not thresholds**.
Never present any of them to a client as a Google requirement. Recommend quantity only
after accuracy, relevance, competition, cost and maintenance.

**Where a client already exceeds the link average** Do not recommend removal. Stop adding,
correct the anchor ratio and topical relevance, and let the average catch up.

**Any citation or link spend** needs explicit approval with provider, cost, renewal,
prerequisites and duplicate plan (RULE-014).

---

## CM-007 · AI Search Gap protected posts · OVERRIDE
**Overrides:** BB-701, BB-702 · **Status:** PILOT · **Refs:** GOV-06 T3

**Bradley says** a post targeting the same entity + location as a service or location page
is competing. Redirect it.

**Coastal says** run the gap test **before** executing his redirect. A post qualifies as
protected if it meets the mandatory criterion — it answers a specific real question that
**no** service or location page covers — plus at least one supporting signal: meaningful
impressions with low CTR (a post losing the click to an AI summary), an AI-assistant-shaped
question (cost, troubleshooting, "is it worth it"), or no better-covering competitor page.

**Protected posts are never deleted or redirected.** They are optimized in place.

**Why** The entity match is not what makes a post competing — covering the same *question*
is. A post answering something no page answers is filling a gap, not splitting a signal.

**Re-test on refresh** A service page built since may now cover the ground, which moves the
post back to his test. Review every 6 months.

**Attribution** This is ours, classified PILOT. Never present it to a client as
methodology.

---

## CM-008 · `site:` is not an index-count source · OVERRIDE
**Overrides:** BB-806, BB-210 measurement method · **Status:** APPROVED · **Refs:** RULE-012

**Bradley says** compare the sitemap URL count against the `site:` operator's reported
count.

**Coastal says** keep the diagnostic — indexation shortfall is a real and useful finding —
and change the measurement source to GSC Page Indexing and URL Inspection, corroborated
with crawl, sitemaps, logs and performance data. `site:` is directional discovery only.

**Note** All three registered audit examples use the `site:` count. They are applied
examples showing the technique was used, not evidence it is currently valid.

---

## CM-009 · Site quality multiplier cannot authorize destruction · OVERRIDE
**Scopes:** BB-209 · **Status:** APPROVED · **Refs:** GOV-06 T9, publication gate

**Bradley says** a site-level quality score multiplies every page's performance, so
redundancy anywhere hurts everywhere.

**Coastal says** this is a **Working Hypothesis**, not documented platform behaviour. It is
legitimate explanatory framing and it drives the right behaviour. Under the publication
gate it **may not independently authorize** deletion, consolidation, URL change, GBP
change, citation spend, migration or automation.

**Why this one matters most** It is the stated reason behind the consolidation argument in
CM-001, it is genuinely persuasive, and it is the claim most likely to slip past a review.
A consolidation whose only support is "it lowers site quality score" fails the gate and is
withdrawn.

---

## CM-010 · Location page ceilings measure the wrong thing · EXEMPT
**Exempts:** BB-315 word and H2 ceilings · **Status:** APPROVED · **Refs:** GOV-06 T4

**Bradley says** location pages under 1,000 words, 2–3 H2s.

**Coastal says** check what the excess words *are*. Duplicated service description → the
finding stands, cut it. Genuine city-specific substance — local conditions, named
neighborhoods, real failure patterns → **the page passes.**

**Why** The ceiling is a proxy for the real rule, which is BB-315's actual content rule:
do not restate the service on every city page. A page over the ceiling with unique local
substance is at most a Low note.

---

## CM-011 · Outbound authority links · ADD
**Status:** PILOT · **Source:** Stage 9 — explicitly not Bradley

**Coastal says** add 1–2 outbound links per service and location page to genuinely
authoritative, topically relevant, non-competing external sources — a manufacturer's
install spec, a licensing body, an industry association, a government code page tied to
this exact service or city.

**Priority** Relevance first · genuine recognized authority second · a DR floor as a sanity
check only, never the deciding factor. This carries BB-513's relevance-over-metrics stance
into a new context.

**Placement** Natural in-text citation. Never in the link-wheel tables. Never to a
competitor or a page that could divert a conversion. Exempt from CM-005.

**When nothing qualifies** Leave the page without one and document why. Do not force a
weak link to hit a target.

---

## CM-012 · Voice query routing · ADD
**Extends:** BB-316 · **Status:** PILOT

**Coastal says** conversational long-tail queries are routed to an **existing** page's FAQ
or flagged as a blog gap candidate. **Never a new standalone page**, per BB-202.

**Why** His H3-question-plus-paragraph-answer format is already voice-optimized. The real
job is finding genuine question gaps the existing FAQs miss, not rebuilding anything.

**Adaptation made** The source prompt asked for a search-volume column on queries that have
no measurable volume, inviting a fabricated number. Replaced with a Query Signal column:
cite real GSC impressions, or mark plainly as "long-tail / not independently measurable."
Never invent a number.

---

## CM-013 · Variant exhaustion is one finding, not many · ADD
**Extends:** BB-108 · **Status:** APPROVED · **Refs:** GOV-06 T7

**Coastal says** when the page count of a type exceeds the approved variant list,
collisions are inevitable and are a **symptom**. The finding is "variant list exhausted,"
not twelve separate collision findings. The remedy is variant research, not page edits.

**Why** Twelve location pages against five approved area variants will collide no matter
how carefully each page is written. Recommending rewrites cannot fix a shortage.

---

## CM-014 · Separator standard · OPEN
**Extends:** BB-302 · **Status:** OPEN

**Bradley** specifies a separator is used identically site-wide but does not settle which
glyph.

**House default** hyphen. Pipe only where an entity contains an internal hyphen.

**Ruling** **Consistency is the finding, not the glyph.** Mixed separators within a site
are a real defect and get flagged. A site consistently using the non-default glyph is
**not a finding** — do not recommend a site-wide retitle to change a character nobody has
evidence about.

---

## CM-015 · Portability test · ADD
**Extends:** BB-317, BB-318 · **Status:** PILOT

**Coastal says** take the opening paragraph, every body section and every FAQ answer in
turn and ask: could this be pasted onto a sibling page with only the city or service name
swapped and still read correctly? If yes, it is functionally duplicate content and must be
rewritten with page-specific substance.

**Why** It makes BB-317's "genuinely unique" requirement testable instead of aspirational.
On a compliant site the structure is identical by design, so the human layer is the only
differentiator — and this is the only check that catches a failure there.

**Threshold** Minimum three concrete, page-specific, verifiable facts per service or
location page. Below three, the page is generic.

---

## CM-016 · No invented facts · ADD
**Status:** APPROVED

**Coastal says** never invent a neighborhood, landmark, certification, response time, brand
serviced, statistic, founding year, warranty term or price. Where a fact is missing, write
`[NEED: <exactly what is required>]` inline and continue.

**Why** A draft full of NEED markers is a correct draft. A draft with invented specifics is
a failure that reaches a client's website. Bradley requires local context to be real
(BB-317); the marker convention and the hard prohibition are ours.

**Related** Never fabricate license numbers, project counts or years in business — these
are exactly the claims E-E-A-T requires to be verifiable, and an invented number is worse
than an acknowledged gap.

---

## CM-017 · Session discipline · ADD
**Status:** APPROVED

**Coastal says** one chat per client, not per page — cross-page collision detection depends
on the model remembering siblings. Auditing and writing go in **separate sessions**; a
model that just wrote the copy will not honestly audit it. Never audit from a bare URL —
always capture first. Never publish an AI rewrite without Paul's sign-off.

**Why** Operational discipline for running the methodology through an AI. Bradley's
methodology says nothing about this because he was not running it this way.

---

## CM-018 · Independent review · OVERRIDE
**Status:** PILOT · **Refs:** RULE-011

**The rule says** every audit gets an analyst self-check **and** an independent review
before release.

**Coastal's exception** Where Claude performs both, record it as an explicit Paul Exception
on every audit. Mitigation: run the review in a **fresh session**, loading only the finding
register, inventories, evidence manifest and decision log — never the analysis
conversation or any narrative explaining the reasoning.

**Why the mitigation matters** A summary explaining *why* a finding was written re-imports
exactly the reasoning the review is meant to challenge. It is a mitigation, not an
equivalent.

---

## Quick index

| ID | Type | Scopes | Status |
|---|---|---|---|
| CM-001 | OVERRIDE | BB-202/203/204/207/210/701/702 | APPROVED |
| CM-002 | OPEN | BB-305 | OPEN |
| CM-003 | ADD | BB-310/312 | PILOT |
| CM-004 | ADD | — | PILOT |
| CM-005 | EXTEND | BB-205/206 | PILOT |
| CM-006 | EXTEND | BB-502/512/804 | APPROVED |
| CM-007 | OVERRIDE | BB-701/702 | PILOT |
| CM-008 | OVERRIDE | BB-806/210 | APPROVED |
| CM-009 | OVERRIDE | BB-209 | APPROVED |
| CM-010 | EXEMPT | BB-315 | APPROVED |
| CM-011 | ADD | — | PILOT |
| CM-012 | ADD | BB-316 | PILOT |
| CM-013 | ADD | BB-108 | APPROVED |
| CM-014 | OPEN | BB-302 | OPEN |
| CM-015 | ADD | BB-317/318 | PILOT |
| CM-016 | ADD | — | APPROVED |
| CM-017 | ADD | — | APPROVED |
| CM-018 | OVERRIDE | — | PILOT |

**Rules with no delta are followed as written.** That is most of the Standard — 18 entries
against 82 rules.
