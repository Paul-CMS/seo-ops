# GOV-06 — Methodology Override Decisions

**Document ID:** GOV-06 - Methodology Override Decisions
**Status:** DRAFT — pilot only, not approved
**Owner:** Paul
**Version:** 0.9
**Authority Level:** 1 (governing) once approved
**Consumed by:** Stages 1–6, and by the technical audit skill before any destructive or
spend recommendation

---

## Why this document exists as a document

The lean model caps governing documents at eight and prohibits a new one where a section
inside an existing document would do. Run against that test:

| Requirement | Met? |
|---|---|
| Distinct trigger | Yes — a methodology rule would recommend an action that site evidence contradicts |
| Accountable owner | Paul |
| Execution procedure | The override ladder and the per-tension evidence thresholds below |
| Approval gate | Paul rules on every override; the audit only records |
| Failure path | Absence-of-evidence defaults in §3 |
| Handoff | Conflicts register → decision log → Rule Register |

It passes. The alternative — a section inside GOV-01 — was considered and rejected
because this fires during Stages 1–6 rather than at the router level, and burying it in
the Master Operating Standard puts it outside the reading path of the people who hit the
tension.

---

## 1. The governing principle

**Bradley's methodology governs how things are built. Evidence governs whether things
are destroyed.**

That asymmetry is the whole document. It follows from what the methodology is: a set of
rules for constructing entity associations efficiently. It was derived from what works
when building, and it is authoritative there. It was not derived from, and says nothing
about, what a specific page is currently earning.

So:

**Constructive actions** — how to structure a new page, which schema type, which variant
goes at which element, how to write an H1, where internal links live, what an FAQ looks
like. **Methodology governs. Evidence is not required to follow it.** An analyst who
wants to deviate needs a reason; an analyst who follows it does not.

**Destructive actions** — merge, delete, redirect, noindex, canonical change, GBP
identity change, migration, and any spend. **Methodology produces a candidate, never a
decision.** Evidence decides, and where evidence is absent the default is to not act.

This resolves the consolidation question directly. Bradley's architecture rule is right
about what the site *should* look like. It is silent on what happens to a page that is
currently generating leads. Those are different questions and the methodology only
answers the first one.

---

## 2. The override ladder

What can beat a Bradley Methodology Rule, in order:

| # | Override | Applies to | Who decides |
|---|---|---|---|
| 1 | **Platform requirement** | Everything. Always wins. | Nobody — it is not a judgment |
| 2 | **Legal, licensing or truth constraint** | Everything. Always wins. | Nobody |
| 3 | **Client constraint** | Confirmed operational, service, geographic or brand fact | Client confirms, Paul approves the consequence |
| 4 | **Verified revenue evidence** | Destructive actions only | Paul, against the §4 thresholds |
| 5 | **Paul Exception** | Anything, with scope, reason, risk, review trigger and exit condition | Paul |

What can **never** override a methodology rule:

- An analyst's or an AI's reasoning about what seems better
- A client's preference unsupported by data
- A tool's score or severity label
- Aesthetic or stylistic judgment
- "The page looks fine"
- Another Working Hypothesis

**Absence of evidence is not evidence.** Being unable to retrieve GSC data does not
license a consolidation; it blocks it. See §3.

---

## 3. Defaults when evidence is unavailable

The most common real situation. Write the default into the finding rather than treating
the gap as a reason to proceed either way.

| Situation | Default | Why |
|---|---|---|
| No GSC, no analytics, destructive action proposed | **Do not act.** Downgrade to `Needs Evidence` in the URL Decision Map | Irreversible action on unknown value |
| No GSC, constructive action proposed | **Follow the methodology** | Nothing is lost if it is wrong; the page is being built either way |
| Partial evidence — traffic known, conversions unknown | **Do not act** on a page with any traffic. Traffic without conversion data is unresolved, not zero | A lead-generating page often shows trivial traffic |
| Client cannot confirm a fact a rule depends on | Rule is suspended for that page; record as `client_confirmation_required` | Stage 3 handles it |
| Evidence exists but contradicts itself | Conflicts register. Do not average | Averaging two sources is explicitly prohibited |

---

## 4. Named tension points

Each is a place where following the methodology literally would produce a wrong or
unsafe recommendation on some real site. Add a new one whenever an audit finds one — this
list is expected to grow.

---

### T1 — Consolidation vs. proven demand

**Methodology says:** one page per primary service, one page per city, no service+city
combination pages, no sub-service pages unless the sub-service has an independent
Wikipedia entity and distinct buyer intent. Redundant pages get consolidated and
redirected.
*Source: BB-P1-002; BB-P5-002 steps 8 and 11.*

**Where it breaks:** the methodology's page-count logic is about efficiency, and it
cannot see revenue. A site with 45 service×city pages built under old tactics may have
six of them producing the majority of inbound calls. Consolidating those is a net loss
regardless of how much cleaner the architecture becomes.

**Evidence required before any consolidation:**

- 12 months of organic traffic and query data for the page
- Conversions or leads attributable to it — form, call tracking, or CRM
- The client's own job history for that page's service and city
- Backlinks pointing at it
- Whether any paid campaign lands on it
- Whether a GBP or a citation points at it

**Thresholds:**

| Evidence | Ruling |
|---|---|
| Any conversion, lead or attributable job in 12 months | **Keep.** Improve in place. Consolidation is off the table until the traffic moves |
| Backlinks, GBP or citation dependency, or paid traffic | **Keep** the URL. If consolidating content, 301 and preserve the URL's equity |
| Traffic but no conversion data available | **Needs Evidence.** Do not act |
| No traffic, no conversions, no dependencies, 12 months | **Consolidation candidate.** 301 to the strongest sibling |
| Any of the above uncertain | **Needs Evidence** |

**Never delete. Always redirect.** Even a dead page's accumulated equity is worth
capturing, and a redirect is reversible where a deletion is not.

**Rules in force:** RULE-005, RULE-007, RULE-015. RULE-007 is explicit — a page may not
be deleted or merged solely for failing an entity test.

**Recording:** the full value/dependency check goes in the URL Decision Map. A
consolidation recommendation without a completed check is withdrawn, not downgraded.

---

### T2 — "The Best" in the H1

**Methodology says:** every service and location H1 opens with "The Best."
*Source: BB-P2-003; BB-P5-007 gate 3.*

**Status:** untested since the original GutterXperts-era confirmation. Every model behind
every AI surface has been replaced at least once since. It occupies the most valuable
slot on every page in the portfolio.

**Ruling until the cohort test resolves:** keep it. It costs nothing measurable and
changing it portfolio-wide on an untested hunch is the larger risk. **Do not flag its
absence as a finding above Low severity**, and do not recommend adding it to a page that
is currently performing well — that page would be a free variant slot in the test, and
changing it destroys the baseline.

**Resolves when:** BB-P5-008 reports at day 42.

---

### T3 — Blog competition vs. AI Search Gap protection

**Methodology says:** a blog post targeting the same entity + location as a service or
location page is competing. Redirect it.
*Source: BB-P1-002; Stage 6 Test A.*

**The extension says:** a post answering a specific real question no service or location
page covers is protected, never deleted, optimized in place.
*Source: BB-P3-003 — Coastal, not Bradley.*

**These genuinely conflict**, and the extension wins, deliberately. Test B runs before
Test A's redirect is executed. A post that passes Test B is protected even if it shares
an entity with a service page, because the entity match is not what makes it competing —
covering the same *question* is.

**But:** Test B is a Coastal extension classified PILOT, not a Bradley rule. It must be
attributed as such in any client deliverable. Do not present it as methodology.

**Re-test on refresh:** a service page built since may now cover the ground. That moves
the post back to Test A.

---

### T4 — Location page word and H2 ceilings

**Methodology says:** location pages under 1,000 words, 2–3 H2s, no service descriptions.
*Source: BB-P1-002; Stage 4-5 s4.*

**Where it breaks:** a location page that exceeds the ceiling and is the site's best
performer. The ceiling exists to prevent service descriptions duplicating across cities —
it is a proxy for the real rule, which is "do not restate the service on every city page."

**Ruling:** check what the excess words *are*. Duplicated service description → the
finding stands, cut it. Genuine city-specific substance — local conditions, named
neighborhoods, real failure patterns — → **the page passes.** The ceiling is not the
rule; non-duplication is.

**Severity:** a page over the ceiling with unique local substance is at most a Low note,
not a finding.

---

### T5 — Schema type on location pages

**Methodology says:** only a verified GBP's actual landing URL gets a LocalBusiness-type
schema. Every other location page gets Article or WebPage. "There is no exception to
this."
*Source: Stage 7 Part 1.*

**Ruling: no override exists.** This is a Platform Requirement, ladder level 1 —
misrepresenting a non-GBP page as a local business entity is a representation problem,
not an optimization choice. Client preference does not override it and neither does
current ranking.

Listed here because it is the most commonly violated rule in the system and analysts
reach for an exception. There isn't one.

---

### T6 — Citation and link quantity benchmarks

**Methodology says:** 100+ citations for a published-address business; build links at or
below the top-five competitor average.
*Source: BB-P1-004; RULE-004.*

**Ruling:** both are planning benchmarks, not thresholds. Recommend quantity only after
accuracy, relevance, competition, cost and maintenance. Never present either number to a
client as a Google requirement.

**Where a client already exceeds the link average:** do not recommend removal. Stop
adding, correct the anchor ratio and topical relevance, and let the average catch up.

**Any citation or link spend** is ladder-independent — it requires explicit approval with
provider, cost, renewal, prerequisites and duplicate plan, per RULE-014.

---

### T7 — Variant exhaustion

**Methodology says:** no two pages of the same type claim the same variant at the same
level.
*Source: BB-P5-002 step 5.*

**Where it breaks:** when the page count exceeds the approved variant list, collisions are
inevitable and are a symptom, not a defect. Twelve location pages against five approved
area variants will collide no matter how carefully each page is written.

**Ruling:** when collisions exceed available variants, the finding is **"variant list
exhausted,"** not twelve separate collision findings. The remedy is variant research,
not page edits. Do not recommend rewriting pages to resolve a shortage that rewriting
cannot resolve.

---

### T8 — `site:` as an index-count source

**Methodology says:** compare sitemap URL count against the `site:` reported count.
*Source: BB-P1-001; all three audit examples.*

**Ruling: RULE-012 overrides.** Keep the diagnostic — indexation shortfall is a real and
useful finding. Change the measurement source to GSC Page Indexing and URL Inspection,
corroborated with crawl, sitemaps, logs and performance data.

The audit examples are Level 4 and demonstrate that the technique was used, not that it
is currently valid.

---

### T9 — Site quality score as justification

**Methodology says:** a site-level quality score multiplies every page's performance, so
redundancy anywhere hurts everywhere.
*Source: BB-P1-002.*

**Status:** Working Hypothesis. Not documented platform behaviour.

**Ruling:** usable as explanatory framing and it drives the right behaviour. **Per the
publication gate it may not independently authorize deletion, consolidation, URL change,
GBP change, citation spend, migration or automation.** A consolidation recommendation
whose only support is "it lowers site quality score" fails the gate and is withdrawn.

This is the one most likely to slip through, because it is genuinely persuasive and it
is the stated reason behind T1.

---

### T10 — Separator standard

**Methodology says:** hyphen is the house default; pipe only where an entity contains an
internal hyphen.
*Source: BB-P2-003 §2.2.*

**Status:** open. Bradley has not tested it; neither has Coastal.

**Ruling:** consistency is the finding, not the glyph. Mixed separators within a site are
a real defect and get flagged. A site consistently using the non-default glyph is **not a
finding** — do not recommend a site-wide retitle to change a character nobody has
evidence about.

---

## 5. Procedure when a new tension is found

1. **Do not resolve it inside the audit.** Follow the current production rule.
2. Write a row in the conflicts register: both claims verbatim, sources, dates, authority
   levels, affected stages, current production rule, proposed ruling, evidence, risk.
3. Flag the affected findings `client_confirmation_required` or `paul_approval_required`
   as appropriate, with confidence `Assumed`.
4. Draft a proposed tension entry in this document's format.
5. Paul rules. The ruling goes to the decision log and the Rule Register, and this
   document is versioned.

A tension that recurs across three clients is a candidate for promotion into the Rule
Register as a standing rule, not a per-audit judgment.

---

## 6. What this document does not do

- It does not weaken the methodology. Bradley's framework remains the primary reasoning
  lens; classification and override thresholds exist so that a practitioner observation
  is not mistaken for a platform requirement.
- It does not license analyst discretion. Every override is evidence-based and
  Paul-approved. "I judged it differently" is not on the ladder.
- It does not cover Stage 4 remediation. Nothing here authorizes an implementation.
