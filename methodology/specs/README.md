# Page specs

**Status:** DRAFT — awaiting Paul's review (build and audit treat a DRAFT spec as advisory; Paul marks it APPROVED)

## What a spec is

A spec is a list of what one page type must have, in page order, with the rule ID behind each
item. It does not repeat the rule text: look up the ID in the source.

| Spec | Page type |
|---|---|
| `homepage.md` | Homepage: the 17 parts of BB-313 |
| `service.md` | One page per primary service (BB-314) |
| `location.md` | One page per city (BB-315, CM-023) |
| `county-hub.md` | County hub page (mostly Coastal defaults, needs Paul's rulings) |
| `about.md` | About page (mostly Coastal defaults, needs Paul's rulings) |
| `blog-post.md` | Informational blog post (BB-704, CM-038, CM-039) |

**Where the rule IDs live**
- `BB-1xx`–`BB-9xx`: `sop-source/BB-Standard-v1.0.md`. Schema rules marked `(v1.1)` mean
  `sop-source/BB-Standard-Schema-Section-v1.1.md`, which replaces BB-601–608 of v1.0.
  BB-601–608 mean different things in the two versions, so always write the `(v1.1)` tag.
- `CM-001`–`CM-018`: `sop-source/Coastal-Delta-v1.0.md`. `CM-019`–`CM-024`:
  `methodology/rulings.md` (formerly the addendum). `CM-038`, `CM-039` and later: `methodology/rulings.md`.
  These are being merged into `methodology/rulings.md` under the same IDs, plus CM-025
  (sensitive industries), CM-026 (self-review exception), CM-027 (reviews are never verified
  facts), CM-028 (severity scale).
- `WC-Cn` = a Coastal house standard that was rule Cn of the commercial writing standard until
  2026-10-03; it now lives only in these specs (the writing standard keeps process and voice).
  `WB-Cn` = `methodology/writing-blog.md` rule Cn.
- `BG-X` = Brand Guide section X (`templates/brand-guide.md`), e.g. `BG-A2` = Section A field 2.

**Precedence:** rulings (CM-xxx) > Bradley Standard (BB-xxx) > writing standards. Where a
writing standard line conflicts with a ruling, the spec follows the ruling and says so.

**"Coastal default — needs Paul's ruling"** marks an element that no BB or CM rule requires.
It is our best default, built from what the Standard and the Delta do say. Treat it as
advisory until Paul rules; an audit may report it but never above Low until then.

## How specs are used

| Who | How |
|---|---|
| **Build — briefs** | Each brief lists the spec's section 3 elements for that page and fills the inputs in section 2. A missing input becomes `[NEED: …]` (CM-016). |
| **Build — drafts** | The draft follows section 3 in order. The writer's self-critique (WC-D / WB-D) runs the section 4 checks before handing over. |
| **Audit (S15 conformance scorecard)** | The auditor runs section 4 against each live page: pass / fail / N/A per check. A failed check becomes a finding at the severity in "Fails as". One finding per check, listing every affected URL. |
| **Finish QA** | Runs section 4 on the final draft plus the link placeholders (section 6) once Finish fills them. |
| **Pilot corrections** | Paul's corrections to pilot pages are written into section 8 of the spec they change. The next batch cannot start until they are recorded (`status.py pilot-corrections`). |

## The approved page file

Each approved page (SD/LD/LDCH/HD/AD, and PD for blog posts) starts with a header block —
`page_id`, `url`, `seo_title`, `meta_description`, optional `replaces` — then `# H1` and the body
(`methodology/writing-commercial.md` → Output). The WordPress draft is generated from it one-way;
`/verify` checks the live page against it.

## Common to every commercial page (homepage, service, location, county hub, about)

These apply on top of each spec's own elements and checks. Audit category §6 On-page; Medium unless noted.

| Check ID | Check | Rule ID |
|---|---|---|
| COM-01 | Every header names an entity — no "Our Process", "Why Choose Us", "Get Started" | BB-306/307 |
| COM-02 | Every H2 is sayable as a question a real customer would ask out loud | BB-308 |
| COM-03 | No skipped heading levels (H2 → H3 → H4, never H2 → H4) | BB-306 |
| COM-04 | No H tags in navigation or footer; H tags are never used for styling | BB-306 |
| COM-05 | Every H2 section is under ~375 words (500 tokens) | BB-309 |
| COM-06 | Every section reads correctly alone and names its own entities (no pronoun leaning on an earlier section) | BB-310, BB-311 |
| COM-07 | First sentence under every header answers that header | CM-003 |
| COM-08 | No variant at two consecutive elements (URL → title → H1 → first H2); the homepage's reserved variant appears nowhere else | CM-024 |
| COM-09 | No cross-page link in body prose, an FAQ answer or local context — links live only in their tables (High if a table is missing) | BB-206, CM-005 |
| COM-10 | Tables only for real comparisons, lists only for real steps | WC voice |
| COM-11 | **H1 restate test** (pages whose title names a service or category: homepage, service, location, county hub): strip the brand and the area entity / area variant / city from the SEO title and the H1 — and "The Best" when Brand Guide H2 approves it for this page. If what is left of the H1 is the title's service or category term unchanged, or that term plus one filler word (service, services, company, experts, pros, specialists, solutions, near me, for, local), it fails: rewrite with a different service variant (BB-304). BB-302/BB-305 formats are unchanged | CM-046, BB-304 |
| COM-12 | **FAQ answers:** sentence one answers the question in plain English and stands alone (BB-316). An optional second sentence gives the company and the next step — never identical on two pages, never a link, left off purely informational answers. A phone number, "call us", "contact us for a quote" or "we offer this service" is never the answer. Fact Unknown → teach the general point and invite a look at their case, no number or promise. A cost question names what drives the cost | CM-048, BB-316, CM-005, CM-015 |
| COM-13 | **Reading level:** visitor-facing copy (opening, body, FAQ answers, meta description, CTA) at grade 7–8 — `scripts/readability.py` page average ≤ 8.9, no paragraph over 10; the SEO title is excluded. Low | CM-047 |
| COM-14 | **A keyword is still a claim:** no keyword, variant, PAA question or fan-out query brings an Unknown or Unverified fact into the copy ("24-hour…", "emergency…", "certified…" need that fact Known in the evidence grid) | CM-049, CM-016 |

## Check IDs

`HP-` homepage · `SVC-` service · `LOC-` location · `HUB-` county hub · `ABT-` about ·
`BLG-` blog post, numbered `-01` upward. IDs are permanent: a retired check keeps its number
and is marked RETIRED; new checks take the next free number. Findings and pilot corrections
cite the check ID.

## Severity (CM-028)

The scale is defined only in CM-028 (`methodology/rulings.md`). For specs: a failed check is Medium by
default; it is High when it breaks the entity model or page structure (wrong page type, missing or
duplicate H1, brand in the H1, wrong title entity order, missing city-mesh table); Low for hygiene.

Two standing rules apply to every spec:
- A missing "The Best" is never a failed check by itself (CM-020). The check is whether the
  H1 matches the Brand Guide H2 decision for that page.
- Never recommend changing the H1 of a page already in the top 3 for its main keyword
  (CM-020). This is a check on the **recommendation**, not on the page.

## Status line rule

Every spec's second line is its status: `DRAFT — awaiting Paul's review` or
`APPROVED — <date>, Paul`. Only Paul changes a spec to APPROVED. A DRAFT spec is advisory:
build follows it, audit reports against it, but a failed check against a DRAFT spec is a
recommendation, not a gate. Any change to an APPROVED spec other than a logged pilot
correction returns it to DRAFT.
