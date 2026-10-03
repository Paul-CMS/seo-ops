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

In seo-ops the rule source is `methodology/rulings.md` (precedence: rulings > Bradley
Standard > everything else). The Rule Register, the Coastal Delta and GOV-06 are
consolidated there and in force; cite their IDs (CM-###, RULE-###, PROC-##).

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
- Entity overlap alone does not prove cannibalization (RULE-005)
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

**Known live case:** Bradley's site-quality-score multiplier — CM-009.

## Evidence quality

**Prefer:** direct documents, first-party records, reproducible crawl or SERP
observations, verified client facts, current official platform guidance.

**Supporting only:** anecdotes, single audit examples, generated summaries, unverified
claims.

An audit example demonstrating a technique is Level 4 evidence that the technique was
used — not evidence that it is correct or currently valid.

## Conflict records

Procedure: **PROC-01** (`methodology/rulings.md`). Write a row in `conflicts.csv`; never
resolve inside the audit and never average. While recording it, also note whether the
conflict is real or caused by different conditions, and check current official guidance
where platform behaviour is involved or client evidence where the question is
campaign-specific.

## Client-specific exceptions

A client exception identifies client, reason, duration, approver, affected stage and
**exit condition**. It does not change the global SOP unless separately approved. Record
it in `decisions.md` and reference it from every finding it touches.

## Rules in force

The rulings the audit works to are in `methodology/rulings.md` — Rule Register entries in
section C (RULE-001–015; RULE-013 is MISSING — do not infer it), Coastal rulings in
sections A–B. Cite the ID; do not copy rule text into findings or this skill.

The Review review exception is the standing ruling **CM-026** (RULE-011's exception
clause); it is cited in `decisions.md`, not re-logged per audit.
