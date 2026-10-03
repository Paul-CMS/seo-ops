# Rulings
### The single rule source for seo-ops.

**Precedence:** `rulings.md` > the Bradley Standard (`sop-source/BB-Standard-v1.0.md`, with
BB-601–608 replaced by `sop-source/BB-Standard-Schema-Section-v1.1.md`) > everything else.
Platform requirements and legal/truth constraints still bound every rule (PROC-02).

**How this file is used**
- Skills, agents and writer standards **cite IDs from here and never restate rules.** If a
  skill needs a rule, it names the ID (e.g. "CM-019", "RULE-005", "BB-305").
- `methodology/lessons.md` is an **inbox**: proposals only, never in force until Paul moves
  an item here with an ID.
- Only Paul adds, changes or retires an entry. A change is a new entry (or a status change
  with a pointer) — never a silent edit of the rule text.
- Consolidated on 2026-10-02 from: the Coastal Delta v1.0 (CM-001–018), the Delta addendum
  (CM-019–024), the earlier `rulings.md` (CM-038, CM-039), GOV-06 (procedure and tensions
  T1–T10), the Rule Register (RULE-001–015) and the Conflicts Register (CF-001–009). Those
  source files are historical; this file governs. IDs CM-025–037 were reserved for this
  consolidation; unused reserved IDs stay unused.

**Entry format** — one line under each heading:
**ID** · **Status** (APPROVED / OPEN / PILOT / REJECTED / DEFERRED / NOTED / SUPERSEDED) ·
**Date** · **Reason** · **Supersedes** — then the rule text.

Status meanings: `APPROVED` governs · `PILOT` in limited use with enhanced QA · `OPEN`
unresolved, follow the current production rule and do not treat as settled · `REJECTED`
the stated position is not the rule · `DEFERRED` parked, do not recommend · `NOTED`
recorded, no rule · `SUPERSEDED` no longer governs; follow the pointer.

## Contents
- A. Coastal rulings (CM-001–024)
- B. Standing rulings from the consolidation and after (CM-025 onward, incl. CM-038, CM-039)
- C. Rule Register (RULE-001–015)
- D. GOV-06 — procedure and tensions (PROC-01, PROC-02, GOV-T1–T10)
- E. Resolved conflicts (CF-001–009)
- Quick index

---

# A. Coastal rulings

## CM-001 · Destructive vs constructive asymmetry
**ID** CM-001 · **Status** APPROVED — operational thresholds SUPERSEDED → CM-019 · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Bradley's architecture rules say how to build; they say nothing about what an existing page currently earns. · **Supersedes** — (scopes BB-202, BB-203, BB-204, BB-207, BB-210, BB-701, BB-702)

Type OVERRIDE. Bradley's consolidation and redirect rules (redundant pages, sub-service
pages, combination pages, empty hubs, competing blog posts) produce a **candidate**, never
a decision. Construction follows the Standard with no evidence required. Destruction
(merge, delete, redirect, noindex, canonical change) requires evidence. **Never delete;
always redirect.** The full value/dependency check is recorded in the URL Decision Map.

*Superseded part (historical):* the original operational thresholds (any conversion in
12 months → keep; backlinks/GBP/citation/paid dependency → keep URL; traffic without
conversion data → Needs Evidence; nothing over 12 months → candidate) are replaced by
CM-019. See CM-030 (OPEN) for how performance data is used when a client does supply it.

## CM-002 · "The Best" is untested
**ID** CM-002 · **Status** SUPERSEDED → CM-020 · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** "Confirmed AI trigger word" is a grade-C claim with no cited source carrying portfolio-wide weight. · **Supersedes** — (scoped BB-305)

*Historical:* keep "The Best" until the cohort test resolves; do not flag its absence above
Low; do not add it to a well-performing page (free variant slot in the cohort). Replaced by
CM-020, which makes it a tested opener and never a finding by its absence.

## CM-003 · BLUF openings
**ID** CM-003 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Fits Bradley's passage-level retrieval model; old posts bury the answer under long intros. · **Supersedes** —

Type ADD (extends BB-310, BB-312). The first sentence or two of an opening paragraph states
who/what/where before any scene-setting or brand-story preamble.

## CM-004 · E-E-A-T verifiable experience layer
**ID** CM-004 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Cosmetic trust badges and bios move nothing; corroborated experience does. Source: newsletter research, not Bradley. · **Supersedes** —

Type ADD. Claimed experience must be corroborated across the entity's whole footprint:
real project photos, named technicians tied to the service area, specific checkable
numbers, and a cross-check that those numbers and names match the GBP, citations and press
releases. Operationalizes BB-103 on the trust layer; the framing and check are Coastal's.

## CM-005 · Content/links separation
**ID** CM-005 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** A link-wheel update should edit one table block per page and never reopen approved copy. · **Supersedes** —

Type EXTEND (BB-205, BB-206). On service and location pages: write and finalize all
narrative content first; build the cross-page table with heading and structure, rows as a
labeled placeholder. Never embed a cross-page link in body prose, an FAQ answer or the
local-context section. Exempt: outbound authority links (CM-011) and approved exceptions
(CM-022). Blog posts are governed by CM-038, not this entry.

## CM-006 · Benchmarks are planning targets
**ID** CM-006 · **Status** APPROVED · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Bradley's numbers are planning aids, not Google requirements. · **Supersedes** — (refs RULE-004, RULE-014)

Type EXTEND (BB-502, BB-512, BB-804). The 100/65/200 citation benchmarks, the
competitor-average link ceiling and the 16-of-20 supporting-asset threshold are planning
benchmarks, not thresholds. Never present any of them to a client as a Google requirement.
Recommend quantity only after accuracy, relevance, competition, cost and maintenance.
Where a client already exceeds the link average: do not recommend removal — stop adding,
correct anchor ratio and topical relevance. Any citation or link spend needs RULE-014
approval.

## CM-007 · AI Search Gap protected posts
**ID** CM-007 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Covering the same question, not sharing an entity, is what makes a post competing. · **Supersedes** — (overrides BB-701, BB-702; resolves GOV-T3)

Type OVERRIDE. Run the gap test (bb-blog-analysis Test B) **before** executing a BB-701
redirect. A post is protected if it meets the mandatory criterion — answers a specific real
question that **no** service or location page covers — plus at least one supporting
signal: meaningful impressions with low CTR, an AI-assistant-shaped question (cost,
troubleshooting, "is it worth it"), or no better-covering competitor page. Protected posts
are never deleted or redirected; they are optimized in place. Re-test on refresh (every 6
months). This is Coastal PILOT — never present it to a client as methodology.

## CM-008 · `site:` is not an index-count source
**ID** CM-008 · **Status** APPROVED · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** The `site:` count is directional; the audit examples show the technique was used, not that it is valid. · **Supersedes** — (overrides BB-806 and BB-210 measurement method; same as RULE-012; resolves GOV-T8)

Type OVERRIDE. Keep the indexation-shortfall diagnostic; measure it with GSC Page Indexing
and URL Inspection, corroborated with crawl, sitemaps, logs and performance data. `site:`
is directional discovery only; never calculate an indexation rate from it.

## CM-009 · Site quality multiplier cannot authorize destruction
**ID** CM-009 · **Status** APPROVED · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** The most persuasive unproven claim, and the stated reason behind consolidation. · **Supersedes** — (scopes BB-209; resolves GOV-T9)

Type OVERRIDE. The site-level quality multiplier is a Working Hypothesis. Under the
publication gate it may not independently authorize deletion, consolidation, URL change,
GBP change, citation spend, migration or automation. A consolidation whose only support is
"it lowers site quality score" is withdrawn.

## CM-010 · Location page ceilings measure the wrong thing
**ID** CM-010 · **Status** APPROVED — H2-ceiling part SUPERSEDED → CM-023 · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** The ceiling is a proxy for BB-315's real rule: do not restate the service on every city page. · **Supersedes** — (exempts BB-315 word ceiling; resolves GOV-T4)

Type EXEMPT. For a location page over the word ceiling, check what the excess words are.
Duplicated service description → the finding stands, cut it. Genuine city-specific
substance (local conditions, named neighborhoods, real failure patterns) → the page passes;
at most a Low note. *(The "2–3 H2s" ceiling this entry also exempted is dropped by CM-023.)*

## CM-011 · Outbound authority links
**ID** CM-011 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Carries BB-513's relevance-over-metrics stance into outbound linking. Explicitly not Bradley. · **Supersedes** —

Type ADD. Add 1–2 outbound links per service and location page to genuinely
authoritative, topically relevant, non-competing sources (manufacturer install spec,
licensing body, industry association, government code page tied to this service or city).
Priority: relevance, then recognized authority; a DR floor is a sanity check only.
Placement: natural in-text citation; never in link-wheel tables; never to a competitor or a
page that could divert a conversion; exempt from CM-005. When nothing qualifies, leave the
page without one and document why. Blog posts: CM-038 caps apply. See CM-032 (OPEN).

## CM-012 · Voice query routing
**ID** CM-012 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** BB-316's H3-question format is already voice-ready; the job is finding real question gaps. · **Supersedes** —

Type ADD (extends BB-316). Conversational long-tail queries are routed to an existing
page's FAQ or flagged as a blog gap candidate — never a new standalone page (BB-202). Use a
Query Signal column: real GSC impressions, or "long-tail / not independently measurable".
Never invent a volume number.

## CM-013 · Variant exhaustion is one finding, not many
**ID** CM-013 · **Status** APPROVED — see CM-031 (OPEN) · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Rewrites cannot fix a shortage of approved variants. · **Supersedes** — (extends BB-108; was the remedy for GOV-T7)

Type ADD. When the page count of a type exceeds the approved variant list, collisions are a
symptom: the finding is "variant list exhausted", not one finding per collision; the remedy
is variant research, not page edits. *Note:* CM-024 has since ruled that pages sharing a B2
area variant is correct, which removes the premise GOV-T7 gave this entry. Whether CM-013
still applies to anything is CM-031.

## CM-014 · Separator standard
**ID** CM-014 · **Status** OPEN · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Bradley requires a consistent separator but does not settle the glyph; nobody has tested it. · **Supersedes** — (extends BB-302; resolves GOV-T10)

House default hyphen; pipe only where an entity contains an internal hyphen.
**Consistency is the finding, not the glyph.** Mixed separators within a site are a defect.
A site consistently using the non-default glyph is not a finding — do not recommend a
site-wide retitle to change it.

## CM-015 · Portability test
**ID** CM-015 · **Status** PILOT · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Makes BB-317's "genuinely unique" testable; on a compliant site the human layer is the only differentiator. · **Supersedes** —

Type ADD (extends BB-317, BB-318). Take the opening paragraph, every body section and every
FAQ answer in turn: could it be pasted onto a sibling page with only the city or service
swapped and still read correctly? If yes, it is functionally duplicate and must be
rewritten with page-specific substance. Minimum three concrete, page-specific, verifiable
facts per service or location page; below three the page is generic.

## CM-016 · No invented facts
**ID** CM-016 · **Status** APPROVED · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** A draft with NEED markers is correct; a draft with invented specifics reaches a client's site. · **Supersedes** —

Type ADD. Never invent a neighborhood, landmark, certification, response time, brand
serviced, statistic, founding year, warranty term, price, license number, project count or
years in business. Where a fact is missing, write `[NEED: <exactly what is required>]`
inline and continue.

## CM-017 · Session discipline
**ID** CM-017 · **Status** APPROVED · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Operational discipline for running the methodology through an AI. · **Supersedes** —

Type ADD. One working context per client, not per page (sibling collision detection depends
on it). Auditing and writing run in separate contexts — a model that just wrote the copy
will not honestly audit it. Never audit from a bare URL; capture first. Never publish an AI
rewrite without Paul's sign-off.

## CM-018 · Independent review
**ID** CM-018 · **Status** SUPERSEDED → CM-026 · **Date** pre-2026-10-02 (Delta v1.0) · **Reason** Claude performs both analysis and review, departing from RULE-011. · **Supersedes** —

*Historical:* record a Paul Exception on every audit; mitigate by running the review in a
fresh session loading only the finding register, inventories, evidence manifest and
decision log — never the analysis conversation or narrative. Replaced by the standing
exception CM-026, which keeps the mitigation and drops the per-audit logging.

## CM-019 · Destructive candidates without Search Console
**ID** CM-019 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** Most clients give no GSC, GA4 or backlink access, so the old "no data → nothing destructive" default blocked every cleanup; Paul ruled to rest it on our own local search research. · **Supersedes** CM-001 operational thresholds; GOV-06 §3 first default row; GOV-T1 thresholds; Agency Profile §3 default

Type OVERRIDE. A page is a removal / consolidation / redirect / noindex **candidate** only
when **all four** hold (thresholds in force):
1. DataforSEO shows **no ranking keywords in the top 100** for the URL.
2. DataforSEO shows **no referring domains** to the URL.
3. It is **not a GBP or citation destination**.
4. The **client confirms no leads** from it.

Any one missing → `Needs Evidence`. If the research cannot support a recommendation, make
none. Never delete; always redirect. A candidate goes to Paul; it is never a decision.
The check is recorded in the URL Decision Map.

## CM-020 · "The Best" in the H1 — a tested opener, not a default
**ID** CM-020 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** The "confirmed AI trigger" claim is grade C, occupies the most valuable slot on every page, and is a verifiable claim that needs proof. · **Supersedes** CM-002; GOV-T2; the BB-305 "The Best" default (BB-305's format otherwise stands)

Type OVERRIDE. Builds use the BB-305 H1 format (no brand), but "The Best" is not the
default. It goes in a service or location page H1 only if **all four** conditions pass
(thresholds in force; Paul tunes them here):
1. **Demand** — "best [service] [city]" or "best [service] near me" shows measurable search
   volume in DataforSEO, **or** at least **3 of the top 10** local results use "best" in
   the title or H1.
2. **Opportunity** — very competitive (top results use "best" and our page is not top 3),
   **or** low-hanging fruit: our page ranks **4–20** for the "best" query.
3. **Proof** — the client can back it up from **verified** Brand Guide Section D facts:
   Google rating **4.5+ with 25+ reviews** (recorded per CM-027), or a real award.
4. **Not a sensitive industry** (CM-025) unless Paul approves it.

Never change the H1 of a page already in the top 3 for its main keyword (the
highest-volume keyword the URL ranks for that matches its service/area entity).
Every decision and its evidence is written to the **URL Decision Map and Brand Guide
Section H (table H2)**. Audits never flag a missing "The Best" as a problem by itself.

## CM-021 · Observed conflict for blog redirects
**ID** CM-021 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** Same as CM-019: most clients give no GSC, so our own ranking research must count as observed evidence. · **Supersedes** — (extends BB-701, CM-007, RULE-005, RULE-015)

Type EXTEND. Observed search conflict = Search Console data **or** DataforSEO ranking data
showing the post and the commercial page **both ranking for the same query**. With neither:
no redirect proposal. Test B (CM-007) still runs first.

## CM-022 · Linking exceptions on any page
**ID** CM-022 · **Status** APPROVED — blog part SUPERSEDED → CM-038 · **Date** 2026-10-02 · **Reason** Resolves CF-002: Bradley's city mesh and the link skill's anchor-city model conflicted. · **Supersedes** — (extends BB-205, BB-206, CM-005, CM-011)

Type EXTEND. Bradley and the Delta govern service and location page structure: full city
mesh, table/H3 links (BB-205/206, CM-005). The `updated-link-strategy` skill governs the
link audit / QA workflow. It may also **propose**, as an exception on any page, a
high-value outbound authority link or **one** high-value contextual anchor-text link.
Exceptions are proposed **only in Finish**, each with a stated reason, logged, and each
needs Paul's approval before it is implemented. *(The clause giving the skill authority
over blog-post linking is superseded by CM-038.)*

## CM-023 · Location page structure
**ID** CM-023 · **Status** APPROVED (default accepted) · **Date** 2026-10-02 · **Reason** Resolves CF-005: the writer standard's "2–3 H2s" contradicted BB-315's section list. · **Supersedes** the former writing standard's "2–3 H2s" rule; the H2-ceiling part of CM-010

Type EXTEND (scopes BB-315). BB-315's section structure governs (services table, local
context, FAQ, neighborhoods, Things to Do, Top Sites, sibling cities). CM-010 still governs
the word ceiling.

## CM-024 · Area variants are shared across pages
**ID** CM-024 · **Status** APPROVED (default accepted) · **Date** 2026-10-02 · **Reason** Resolves CF-006: variant collision is vertical (within a page), not horizontal. · **Supersedes** GOV-T7's rule "no two pages of the same type claim the same variant"

Type EXTEND (scopes BB-108). No variant repeats at consecutive elements on one page. Service
pages sharing an area variant from the Brand Guide Section B2 pool is correct. Only the
homepage's reserved variant (B1) is exclusive.

---

# B. Standing rulings (consolidation and after)

## CM-025 · Sensitive industries
**ID** CM-025 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** Health, legal, insurance and financial claims carry legal and harm risk; a single named list stops each skill inventing its own. · **Supersedes** — (defines the list CM-020 condition 4 refers to)

Match by **category, not exact word**. The authoritative term list is `config.json`
`sensitive_categories`; the categories are:
- **Health** — chiropractic / chiropractor / chiro; physical therapy / physiotherapy;
  dental / dentist / orthodontics; medical / doctor / physician / clinic / healthcare;
  mental health / counseling / therapy; pharmacy; home health; med spa.
- **Legal** — legal, law firm, lawyer, attorney.
- **Insurance.**
- **Financial** — financial, finance, accounting / CPA, tax, mortgage, lending / loans,
  banking, wealth / investment.

Rules for a sensitive client:
1. Nothing goes live without Paul's `/approve`, with the human review recorded.
2. Health categories also need the client's **licensed practitioner sign-off** on health
   claims, recorded with who signed.
3. "The Best" is not allowed unless Paul approves (CM-020 condition 4).
4. When the category is unclear, `/new-client` asks Paul.

## CM-026 · Self-review exception (standing)
**ID** CM-026 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** Claude performs both audit analysis and review in every audit; one standing ruling replaces re-logging the same exception each time. · **Supersedes** CM-018; the per-audit exception-logging requirement in RULE-011

Claude performs both the audit analysis and its review. This is a standing exception to
RULE-011's independent-review requirement. Mitigation (required): the review is run by the
fresh-context `audit-reviewer` subagent, loading only the finding register, inventories,
evidence manifest, cross-checks and decision log — never the analysis conversation or any
narrative of its reasoning; and the content QA in Finish never shares context with the
writer. Each audit's `decisions.md` cites CM-026; it does not log a new exception.

## CM-027 · Reviews are never verified facts
**ID** CM-027 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** Customer language is unverified and reviewer names are personal data; only the client can confirm a fact. · **Supersedes** —

- Nothing from Google reviews (or any customer language) enters Brand Guide Section D
  unless the client confirms it on the proof sheet.
- Reviewer names never appear in deliverables.
- The Google rating and review count, with the date checked, are recorded as evidence for
  CM-020 condition 3 (proof).

## CM-028 · Severity scale
**ID** CM-028 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** One scale, set by Bradley impact rather than tool labels; resolves the unratified severity proposal in the audit skill. · **Supersedes** any other severity scale (incl. Critical / Monitor levels)

| Severity | Means |
|---|---|
| **High** | Breaks the entity model or page structure, or blocks indexing |
| **Medium** | Fails a check in its page spec (`methodology/specs/`) |
| **Low** | Technical hygiene — batched into one handoff |

One finding per issue, listing every affected URL. No other levels (no Critical, no
Monitor). Severity never comes from a tool's own label.

## CM-029 · (merged into CM-022)
**ID** CM-029 · **Status** NOTED · **Date** 2026-10-02 · **Reason** "Linking exceptions only in Finish, with Paul's approval" was already the substance of CM-022; CM-022's text now says it explicitly. · **Supersedes** —

No separate rule. Cite CM-022.

## CM-030 · Destructive candidates when performance data *is* supplied
**ID** CM-030 · **Status** OPEN · **Date** 2026-10-02 · **Reason** CM-019 replaced CM-001's thresholds and is framed around clients without GSC; it does not say whether the older performance tests also apply when a client does provide GSC/GA4/call data. · **Supersedes** —

Question for Paul: when GSC/GA4/CRM data exists, do the former CM-001 / GOV-T1 tests
(any conversion or lead in 12 months → keep and improve; traffic without conversion data
→ Needs Evidence) apply **in addition to** the four CM-019 conditions? Until ruled: apply
CM-019's four conditions, and record any performance data in the URL Decision Map without
using it to loosen CM-019.

## CM-031 · Does CM-013 still apply after CM-024?
**ID** CM-031 · **Status** OPEN · **Date** 2026-10-02 · **Reason** CM-013's premise was GOV-T7 (same-type pages may not share variants); CM-024 superseded that premise. · **Supersedes** —

Question for Paul: retire CM-013, or rescope it (e.g. to a page with more elements than
the variants available for vertical non-repetition)? Until ruled: do not raise
cross-page variant sharing as a finding (CM-024); if a single page cannot avoid consecutive
repeats with the approved variants, raise one "variant list exhausted" finding (CM-013).

## CM-032 · Outbound links on service/location pages: standing (CM-011) or exception (CM-022)?
**ID** CM-032 · **Status** OPEN · **Date** 2026-10-02 · **Reason** CM-011 (PILOT) tells writers to add 1–2 outbound authority links per service/location page; CM-022 treats a high-value outbound authority link on any page as an exception needing Paul's approval in Finish. · **Supersedes** —

Question for Paul: are CM-011 links standard writer output, with CM-022 covering only
additional links the link skill proposes? Until ruled: writers follow CM-011; any outbound
link the link skill proposes beyond that goes through CM-022.

## CM-038 · Blog links — placement and anti-stuffing caps
**ID** CM-038 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** Links were being forced into a single end block that readers skip, or stuffed into every section. Free placement with hard caps keeps links useful without turning posts into link farms. · **Supersedes** the blog writing standard's C7 ("one separated block at the end"); the `updated-link-strategy` skill's per-H2 link contract and link counts for blog posts; the blog part of CM-022; BB-704's separated-link-block clause (itself a Coastal addition, per CM-005) for blog posts

Decided by Paul.
- No links in the title, the H1, or the BLUF (the opening ~100-word answer block, CM-003).
- Links may sit in the body or in an end block; placement is otherwise free.
- Caps (starting values, tuned by Paul):
  - at most **1 internal link per H2 section**
  - at most **1 internal link per ~300 words**
  - at most **5 internal links per post**, of which at most **2 to commercial (service or
    location) pages**
  - at most **2 outbound authority links**
- Each URL is linked once per post. Descriptive anchors; no repeated exact-match anchors.
- The blog writer's link check (E6) tests the draft against these caps and reports each
  number.

## CM-039 · Blog author — the company owner by default
**ID** CM-039 · **Status** APPROVED · **Date** 2026-10-02 · **Reason** A real, checkable author is part of E-E-A-T (CM-004); the owner is the person the client's expertise belongs to. · **Supersedes** the blog writing standard's C9 ("real, named author from the Brand Guide") — now specific

Decided by Paul. The author of every blog post is the company owner, unless the client
states otherwise. The Brand Guide **author** field defaults to the owner named on the
returned proof sheet; the writer uses that field and never a generic byline ("Admin",
"Staff", the company name). If the owner is not yet confirmed, the author is
`[NEED: author — owner name from the proof sheet]` and the post cannot be approved.

---

# C. Rule Register

Formerly `methodology/rule-register.md` (from the Drive register). Now in force in seo-ops;
cite the RULE ID.

## RULE-001 · Bradley is the central lens
**ID** RULE-001 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Keeps methodology primary while stopping practitioner claims passing as platform law. · **Supersedes** —

Bradley methodology is the central analytical lens; label the authority (classification)
of each claim.

## RULE-002 · One H1 per page
**ID** RULE-002 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** House standard from the methodology. · **Supersedes** —

One H1 per visible page unless Paul approves a documented exception. It is a house
standard, not a platform requirement — say so in deliverables.

## RULE-003 · Brand-led homepage and location pages
**ID** RULE-003 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Semantic entity-association structure. · **Supersedes** —

Homepage and location pages lead with the brand, in the semantic entity-association
structure.

## RULE-004 · Citation benchmark
**ID** RULE-004 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** See CM-006. · **Supersedes** —

100+ citations is a planning benchmark, not a Google threshold.

## RULE-005 · Entity overlap alone does not prove cannibalization
**ID** RULE-005 · **Status** REJECTED (the claim "entity overlap alone proves cannibalization") · **Date** pre-2026-10-02 (Rule Register) · **Reason** Entity overlap is the most common false positive. · **Supersedes** —

Cannibalization requires overlapping intent **plus** observed evidence. CM-021 defines
observed evidence without GSC.

## RULE-006 · Platform guidance controls GBP
**ID** RULE-006 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Platform requirement (PROC-02 level 1). · **Supersedes** —

Official platform guidance controls GBP eligibility and representation.

## RULE-007 · No deletion for failing an entity test
**ID** RULE-007 · **Status** REJECTED (the claim "a page may be deleted or merged solely for failing an entity test") · **Date** pre-2026-10-02 (Rule Register) · **Reason** Entity tests describe construction, not value. · **Supersedes** —

Verify demand and value first. CM-019 defines how without GSC.

## RULE-008 · Geographic subdomains
**ID** RULE-008 · **Status** DEFERRED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Needs work. · **Supersedes** —

Geographic subdomain default — do not recommend.

## RULE-009 · Recommendations only before implementation gates
**ID** RULE-009 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Separates analysis from change. · **Supersedes** —

Discovery and audit produce recommendations only; nothing changes on a site (no edits,
publishing, purchases, submissions, or GBP/schema/citation/link changes) before the
implementation gates.

## RULE-010 · Two distinct gates
**ID** RULE-010 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Facts and decisions have different owners. · **Supersedes** —

The client confirms facts; Paul approves action, priority, risk and spend.

## RULE-011 · Self-check and independent review
**ID** RULE-011 · **Status** APPROVED — per-audit exception logging SUPERSEDED → CM-026 · **Date** pre-2026-10-02 (Rule Register) · **Reason** Review catches what the analyst cannot. · **Supersedes** —

Every audit gets a self-check **and** an independent review, or a recorded exception. In
seo-ops the exception is the standing ruling CM-026.

## RULE-012 · `site:` is directional
**ID** RULE-012 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** See CM-008. · **Supersedes** —

The `site:` operator is directional evidence, not an index-count source.

## RULE-013 · MISSING
**ID** RULE-013 · **Status** NOTED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Absent from the register while GOV-02 cites RULE-001–013. · **Supersedes** —

MISSING — do not infer its content.

## RULE-014 · Citation and link spend
**ID** RULE-014 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Spend is a Paul decision with a recurring cost. · **Supersedes** —

Any citation or link spend needs explicit approval with provider, cost, renewal,
prerequisites and duplicate plan. The first citation order happens only after website and
GBP identity/location facts are reconciled.

## RULE-015 · Blog cannibalization evidence
**ID** RULE-015 · **Status** APPROVED · **Date** pre-2026-10-02 (Rule Register) · **Reason** Same as RULE-005, for blog posts. · **Supersedes** —

Blog cannibalization requires overlapping intent plus observed search conflict (CM-021).

---

# D. GOV-06 — procedure and tensions

From `sop-source/GOV-06-Methodology-Override-Decisions.md` (v0.9). Its core principle is
CM-001: **methodology governs how things are built; evidence governs whether things are
destroyed.**

## PROC-01 · Procedure when a new conflict is found
**ID** PROC-01 · **Status** APPROVED · **Date** 2026-10-02 (consolidated from GOV-06 §5) · **Reason** Conflicts get recorded and ruled by Paul, never resolved inside an audit or averaged. · **Supersedes** — (GOV-06 §5's "ruling goes to the decision log and Rule Register" now means: ruling goes to this file)

1. Do not resolve it inside the audit. Follow the current production rule.
2. Record it in the audit's `conflicts.csv`: both claims verbatim, sources, dates,
   authority levels, affected steps, current production rule, proposed ruling, evidence,
   risk. Never average two positions.
3. Flag the affected findings `client_confirmation_required` or `paul_approval_required`,
   confidence `Assumed`.
4. Draft the proposed ruling in this file's entry format (as an inbox item in
   `lessons.md`).
5. Paul rules; the ruling becomes an entry here with an ID.

A tension that recurs across three clients is a candidate for a standing ruling here, not
a per-audit judgment.

## PROC-02 · Override ladder and evidence defaults
**ID** PROC-02 · **Status** APPROVED · **Date** 2026-10-02 (consolidated from GOV-06 §2–3) · **Reason** States what can and cannot beat a methodology rule, and the default when evidence is missing. · **Supersedes** — (GOV-06 §3 first row superseded by CM-019)

What can beat a Bradley rule, in order: (1) platform requirement — always wins;
(2) legal, licensing or truth constraint — always wins; (3) client constraint — client
confirms, Paul approves the consequence; (4) verified revenue evidence — destructive
actions only, Paul decides; (5) Paul Exception — with scope, reason, risk, review trigger
and exit condition. Never an override: analyst or AI reasoning about what seems better,
unsupported client preference, a tool's score or severity label, aesthetic judgment,
"the page looks fine", another Working Hypothesis.

Defaults: constructive action without GSC → follow the methodology. Destructive action →
CM-019. Client cannot confirm a fact a rule depends on → the rule is suspended for that
page, recorded `client_confirmation_required`. Evidence contradicts itself → conflicts
record (PROC-01); never average. Absence of evidence is not evidence.

## GOV-T1 · Consolidation vs proven demand
**ID** GOV-T1 · **Status** SUPERSEDED → CM-001 + CM-019 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Page-count logic cannot see revenue. · **Supersedes** —

Resolved by CM-001 (principle; never delete, always redirect; check recorded in the URL
Decision Map — a consolidation without a completed check is withdrawn) and CM-019
(thresholds). Open remainder: CM-030.

## GOV-T2 · "The Best" in the H1
**ID** GOV-T2 · **Status** SUPERSEDED → CM-020 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Untested claim in the most valuable slot. · **Supersedes** —

Resolved by CM-020.

## GOV-T3 · Blog competition vs AI Search Gap protection
**ID** GOV-T3 · **Status** SUPERSEDED → CM-007 + CM-021 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Test B deliberately beats Test A's redirect. · **Supersedes** —

Resolved by CM-007 (Test B first; PILOT, attribute as Coastal) and CM-021 (observed
conflict).

## GOV-T4 · Location page word and H2 ceilings
**ID** GOV-T4 · **Status** SUPERSEDED → CM-010 + CM-023 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** The ceiling is a proxy for non-duplication. · **Supersedes** —

Resolved by CM-010 (word ceiling) and CM-023 (H2 structure).

## GOV-T5 · Schema type on location pages
**ID** GOV-T5 · **Status** NOTED · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** The most commonly violated schema rule; analysts reach for an exception and there is none. · **Supersedes** —

No override exists. Only a verified GBP's actual landing URL gets a LocalBusiness-type
schema; every other location page does not. This is a platform/representation constraint
(PROC-02 level 1) and lives in BB-6xx v1.1 (`BB-Standard-Schema-Section-v1.1.md`).

## GOV-T6 · Citation and link quantity benchmarks
**ID** GOV-T6 · **Status** SUPERSEDED → CM-006 + RULE-004 + RULE-014 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Planning benchmarks, not thresholds. · **Supersedes** —

Resolved by CM-006, RULE-004, RULE-014.

## GOV-T7 · Variant exhaustion
**ID** GOV-T7 · **Status** SUPERSEDED → CM-024 (rule) and CM-013 (remedy; see CM-031) · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Collisions across same-type pages were treated as defects. · **Supersedes** —

The rule "no two pages of the same type claim the same variant" is superseded by CM-024.

## GOV-T8 · `site:` as an index-count source
**ID** GOV-T8 · **Status** SUPERSEDED → CM-008 + RULE-012 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Directional only. · **Supersedes** —

Resolved by CM-008 and RULE-012.

## GOV-T9 · Site quality score as justification
**ID** GOV-T9 · **Status** SUPERSEDED → CM-009 · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Working Hypothesis. · **Supersedes** —

Resolved by CM-009.

## GOV-T10 · Separator standard
**ID** GOV-T10 · **Status** SUPERSEDED → CM-014 (itself OPEN) · **Date** pre-2026-10-02 (GOV-06 v0.9) · **Reason** Untested glyph choice. · **Supersedes** —

Carried by CM-014.

---

# E. Resolved conflicts

Readable copy of `methodology/conflicts-register.csv` (the CSV stays for scripts; new
conflicts follow PROC-01 and are ruled here).

| ID | Topic | Resolved by | Status | Date |
|---|---|---|---|---|
| CF-001 | "The Best" in H1 | CM-020 | APPROVED | 2026-10-02 |
| CF-002 | City link mesh (Bradley mesh vs anchor cities) | CM-022 (blog part now CM-038) | APPROVED | 2026-10-02 |
| CF-003 | Destructive actions without GSC | CM-019 | APPROVED | 2026-10-02 |
| CF-004 | Blog redirect evidence | CM-021 | APPROVED | 2026-10-02 |
| CF-005 | Location page H2 count | CM-023 (BB-315 governs) | APPROVED | 2026-10-02 |
| CF-006 | Variant sharing across pages | CM-024 | APPROVED | 2026-10-02 |
| CF-007 | Schema homepage graph | BB-6xx v1.1 governs (observed implementation) | APPROVED | 2026-10-02 |
| CF-008 | Stage numbering | No numbers; named steps | APPROVED | 2026-10-02 |
| CF-009 | Rule count (83 vs 82) | No action | NOTED | 2026-10-02 |

---

# Quick index

| ID | Status |
|---|---|
| CM-001 | APPROVED (thresholds SUPERSEDED → CM-019) |
| CM-002 | SUPERSEDED → CM-020 |
| CM-003 | PILOT |
| CM-004 | PILOT |
| CM-005 | PILOT |
| CM-006 | APPROVED |
| CM-007 | PILOT |
| CM-008 | APPROVED |
| CM-009 | APPROVED |
| CM-010 | APPROVED (H2 part SUPERSEDED → CM-023) |
| CM-011 | PILOT |
| CM-012 | PILOT |
| CM-013 | APPROVED (see CM-031) |
| CM-014 | OPEN |
| CM-015 | PILOT |
| CM-016 | APPROVED |
| CM-017 | APPROVED |
| CM-018 | SUPERSEDED → CM-026 |
| CM-019 | APPROVED |
| CM-020 | APPROVED |
| CM-021 | APPROVED |
| CM-022 | APPROVED (blog part SUPERSEDED → CM-038) |
| CM-023 | APPROVED |
| CM-024 | APPROVED |
| CM-025 | APPROVED |
| CM-026 | APPROVED |
| CM-027 | APPROVED |
| CM-028 | APPROVED |
| CM-029 | NOTED (merged into CM-022) |
| CM-030 | OPEN |
| CM-031 | OPEN |
| CM-032 | OPEN |
| CM-033–037 | reserved, unused |
| CM-038 | APPROVED |
| CM-039 | APPROVED |
| RULE-001–004, 006, 009, 010, 012, 014, 015 | APPROVED |
| RULE-005, RULE-007 | REJECTED (the stated claim) |
| RULE-008 | DEFERRED |
| RULE-011 | APPROVED (logging SUPERSEDED → CM-026) |
| RULE-013 | NOTED — MISSING, do not infer |
| PROC-01, PROC-02 | APPROVED |
| GOV-T1–T4, T6–T10 | SUPERSEDED (see pointers) |
| GOV-T5 | NOTED |
| CF-001–008 | APPROVED · CF-009 NOTED |
