# Finding Standard

## The record

Every finding is one row in `findings.csv`. All columns are required; `N/A` is a valid
value but blank is not. A blank cell means nobody decided, which is the state this
register exists to prevent.

| Column | Rule |
|---|---|
| `finding_id` | `F-001`, stable forever. Never reused, never renumbered. |
| `revision` | `1` on creation, incremented on each superseding row. |
| `supersedes` | The `finding_id.revision` this row replaces. Append-only: never edit a prior row. |
| `date`, `analyst`, `stage` | When, who, which stage produced it. |
| `category` | One of the nine Analysis categories. |
| `affected_entities`, `affected_urls` | Specific. "Site-wide" is not an answer unless every URL is genuinely affected. |
| `observed_condition` | **What was observed.** No interpretation, no cause, no recommendation. |
| `evidence_source_id` | `SRC-NNN` from the manifest. |
| `evidence_locator` | Where exactly — file, sheet, row range, or screenshot path. A finding without a locator is not written. |
| `rule_classification` | See below. |
| `expected_impact` | What changes if addressed, in business terms. |
| `severity` | See below. |
| `confidence` | See below. |
| `plausible_alternatives` | At least one other explanation of the same evidence. |
| `alternative_tested` | What you did to rule it out, or `not tested`. |
| `recommendation` | Scoped, reversible where practical, within audit scope. |
| `risk_if_acted`, `risk_if_deferred` | Both. A recommendation with no risk of acting has not been thought about. |
| `dependencies` | Other findings, access, client confirmation, platform checks. |
| `client_confirmation_required`, `paul_approval_required` | Yes/No. |
| `implementation_owner` | Placeholder only — Implementation assigns for real. |
| `decision_state` | Blank until Client confirmation. Never set here. |
| `status` | `draft` / `self-checked` / `reviewed` / `superseded` / `withdrawn`. |

## Observation vs. inference vs. recommendation

These occupy three different columns and must not bleed.

- **Observed:** "38 of 47 crawled URLs return a `Meta Robots` value of `noindex`."
- **Inferred:** "The template is likely applying noindex to all archive pages."
- **Recommended:** "Verify the template rule, then remove noindex from the 12 service URLs."

Writing causation where the evidence supports only correlation is the single most common
audit defect. If the evidence shows two things co-occurring, say so, and put the causal
story in `plausible_alternatives` where it belongs until it is tested.

## Rule classification

Every material claim carries one. This is what stops methodology from being presented
as platform law.

| Classification | Means | Test |
|---|---|---|
| **Platform Requirement** | Google/Bing/schema.org documentation states it | Can you cite current official guidance? If not, it is not this. |
| **Bradley Methodology Rule** | From the Semantic Links framework | Cite the methodology file section. |
| **Project Evidence** | Observed in this project's data | Cite the evidence locator. |
| **Working Hypothesis** | Plausible, untested | Must be labelled as such in the deliverable. |
| **Client Constraint** | The client's business, legal or operational limit | Cite the Intake record. |
| **Paul Exception** | Overrides the above for this engagement | Must exist in `decisions.md`. |

If a claim cannot be classified, it is a Working Hypothesis. That is not a failure —
unlabelled certainty is.

**Things that are Bradley Methodology, not Platform Requirement:** one H1 per page
(RULE-002), the 100+ citation benchmark (RULE-004, CM-006), semantic triplet construction, entity variant usage, GBP posting
cadence, internal anchor distribution targets. Each may be right; none is a platform
rule, and the deliverable must not imply Google enforces them.

## Severity

Use the one scale in **CM-028** (`methodology/rulings.md`) — it is defined there and nowhere else.
Medium means a failed check in the page's spec (`methodology/specs/`). Severity never comes from a
tool's own label. The workbook's `Priority` column carries the same value.

## Confidence

| Level | Means |
|---|---|
| **Corroborated** | Two independent sources agree. |
| **Single-source** | One source, no contradiction found. |
| **Contested** | Sources disagree; the disagreement is recorded and unresolved. |
| **Assumed** | Rests on an unanswered question's default. Must appear in Assumptions & Limitations. |

A tool's output and that same tool's second export are **not** independent sources.

## Findings that must not be written

- Any finding whose supporting cross-check came back `CONTRADICTED`
- Any finding derived solely from a tool's issue list without corroboration
- Any finding asserting a URL is an orphan on crawl evidence alone
- Any finding asserting cannibalization without the observed evidence RULE-005 / RULE-015
  / CM-021 require
- Any merge, redirect, delete, noindex or canonical recommendation that does not meet
  CM-019 (else `Needs Evidence`), or lacks a completed `value_dependency_check` and a
  `safer_alternative`
- Any indexation-rate calculation derived from a `site:` result count (CM-008)
- Any finding that a page lacks "The Best" (CM-020)
- Any finding whose only evidence is a tool score
