# Authority, Classification and the Publication Gate

Implements the `01 - Authority and Conflict Rules` document. This governs what any claim
in a finding is allowed to assert, and what happens when sources disagree.

## Authority hierarchy

| Level | Source | Notes |
|---|---|---|
| **1** | Current approved SOPs | Production rules and required gates |
| **2** | Approved decision log (DEC-###) | Amends or clarifies SOPs until the SOP text is updated |
| **3** | Bradley / Semantic Links transcripts and teaching | Primary methodology |
| **4** | Applied client audit examples | Evidence of applied judgment for one campaign |
| **5** | Raw research, third-party commentary, drafts, prompts, notes | Supporting only |

**Platform rules** — current official Google or other platform documentation controls
platform eligibility, compliance and technical behaviour where directly applicable,
regardless of level.

### Document status check

Per the naming and document-control rules, **only documents with status `APPROVED` or
`PILOT` may be used as operational instruction.** Before citing any document in a
finding, check its status header. `DRAFT`, `IN REVIEW`, `SUPERSEDED`, `DEPRECATED` and
`SOURCE` documents may inform reasoning but may not be cited as the rule.

The Governance area is currently flagged **NEEDS REVIEW / NON-OPERATIVE** in its
entirety. Its registers are advisory. This matters in practice: the Rule Register is the
clearest statement of many rules, and it is advisory until promoted. Cite the governing
SOP for the rule and the register entry as supporting reference.

## Interpretation rules

These prevent a transcript, an audit example or an old note from quietly becoming a
universal rule:

- A repeated statement is not automatically a universal rule
- A client audit is an applied example, not a blanket requirement
- Recommendations tied to a market, site, budget or business model stay conditional
- Newer information does not automatically replace approved policy — it creates a
  review item
- Descriptive claims about what Google does require evidence, or explicit labelling as
  practitioner observation
- Entity overlap alone does not prove cannibalization
- Crawl verification begins with Googlebot Smartphone unless evidence requires otherwise

## Classification

Every material instruction, conclusion, benchmark or causal claim is classified before
it becomes operational. This is the `Classification` column of the Finding Register.

| Classification | Means |
|---|---|
| **Bradley Methodology Rule** | Taught by Bradley/Semantic Links, deliberately adopted as primary analytical method |
| **Platform Requirement** | Current first-party rule governing eligibility, compliance, technical behaviour or supported implementation |
| **Project Evidence** | Supported by this client's crawl, GBP, GSC, analytics, revenue, lead or verified business data |
| **Working Hypothesis** | Plausible explanation or tactic requiring validation; must not be stated as proven causation |
| **Client Constraint** | Operational, legal, service, geographic, revenue or brand fact confirmed by the client |
| **Paul Exception** | Approved departure, with scope, reason, risk, review trigger and exit condition |

**Methodology fidelity:** classification does not dilute Bradley's methodology. It is
the primary reasoning framework. Classification exists so that a practitioner
observation, campaign example, benchmark or hypothesis is not mislabelled as a platform
requirement.

## The publication gate

**A Working Hypothesis may appear in an audit only when labelled and paired with a
validation method. It may not independently authorize deletion, consolidation, URL
change, GBP change, citation spend, migration or automation.**

This is a hard constraint, and the most consequential rule in this file. Check it on
every destructive or spend recommendation: if the only thing supporting it is classified
Working Hypothesis, the recommendation cannot stand on that alone. Find independent
Project Evidence or withdraw it.

The `ext_publication_gate` column records the check: `passed`, `blocked`, or `n/a`.

**Known live case:** Bradley's site-quality-score multiplier (the basis of much of the
site-efficiency argument) is a Working Hypothesis, not documented platform behaviour. It
is legitimate explanatory framing and it drives the right behaviour, but a consolidation
or deletion recommendation resting on it alone fails this gate.

## Evidence quality

**Prefer:** direct documents, first-party records, reproducible crawl or SERP
observations, verified client facts, current official platform guidance.

**Supporting only:** anecdotes, single audit examples, generated summaries, unverified
claims.

An audit example demonstrating a technique is Level 4 evidence that the technique was
used — not evidence that it is correct or currently valid.

## Conflict records

When a real conflict is found, write a row in `conflicts.csv` rather than resolving it
silently or averaging the two positions. Averaging is explicitly prohibited.

Procedure:

1. Record both claims verbatim or as faithful summaries
2. Identify each source, date, authority level and scope
3. Determine whether the conflict is real, or caused by different conditions
4. Check current official guidance where platform behaviour is involved
5. Test against client evidence where the question is campaign-specific
6. Write a proposed ruling with conditions, risks and affected SOPs
7. Paul approves where the ruling changes production behaviour
8. Add the approved ruling to the decision log
9. Update affected SOPs; move replaced versions to Superseded

A conflict found during an audit does not get resolved inside the audit. It gets
recorded, the current production rule is followed, and the proposed ruling goes to Paul.

## Client-specific exceptions

A client exception identifies client, reason, duration, approver, affected stage and
**exit condition**. It does not change the global SOP unless separately approved. Record
it in `decisions.md` and reference it from every finding it touches.

## Rules currently in force

From the Rule Register. Advisory status noted above; these are the operative rulings
the audit works to.

| Rule | Ruling |
|---|---|
| RULE-001 | Bradley methodology is the central analytical lens; label the authority of each claim |
| RULE-002 | One H1 per visible page unless Paul approves a documented exception |
| RULE-003 | Homepage and location pages lead with the brand, semantic entity-association structure |
| RULE-004 | 100+ citations is a planning benchmark, not a Google threshold |
| RULE-005 | **Rejected:** entity overlap alone proves cannibalization. Require overlapping intent plus observed evidence |
| RULE-006 | Official platform guidance controls GBP eligibility and representation |
| RULE-007 | **Rejected:** a page may be deleted or merged solely for failing an entity test. Verify demand and 12-month job/lead value |
| RULE-008 | Geographic subdomain default — NEEDS WORK / DEFERRED. Do not recommend |
| RULE-009 | Stages 0–3 produce recommendations only; no edits, publishing, purchases, submissions or GBP/schema/citation/link changes |
| RULE-010 | Client confirms facts; Paul approves action, priority, risk and spend. Distinct gates |
| RULE-011 | Every audit gets an analyst self-check **and** an independent review before release, or a recorded exception |
| RULE-012 | The `site:` operator is directional evidence, not an index-count source |
| RULE-014 | First citation order only after website and GBP identity/location facts are reconciled |
| RULE-015 | Blog cannibalization requires overlapping intent plus observed search conflict |

**RULE-013 is absent from the register** while GOV-02 cites RULE-001–013 as controlling.
Flag this as a gap; do not infer what it said.

**RULE-011 is the basis for the Stage 2 exception.** Claude performing both the
self-check and the review is a departure from RULE-011 and must be recorded as an
explicit exception on every audit, per the rule's own escape clause.
