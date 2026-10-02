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
| `category` | One of the nine Stage 1 categories. |
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
| `implementation_owner` | Placeholder only — Stage 4 assigns for real. |
| `decision_state` | Blank until Stage 3. Never set here. |
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
| **Client Constraint** | The client's business, legal or operational limit | Cite the Stage 0 record. |
| **Paul Exception** | Overrides the above for this engagement | Must exist in `decisions.md`. |

If a claim cannot be classified, it is a Working Hypothesis. That is not a failure —
unlabelled certainty is.

**Things that are Bradley Methodology, not Platform Requirement:** one H1 per page, the
100+ citation benchmark, semantic triplet construction, entity variant usage, GBP posting
cadence, internal anchor distribution targets. Each may be right; none is a platform
rule, and the deliverable must not imply Google enforces them.

## Severity

GOV-02 uses these levels without defining them. Proposed definitions below — **these
need Paul ratification into the RULE register before v1.0**, and until then every audit
using them records that in `decisions.md`.

| Severity | Definition |
|---|---|
| **Critical** | Blocks indexing, eligibility or conversion for a revenue page, or publishes a false/legally exposed claim. Evidence is unambiguous. |
| **High** | Materially suppresses visibility or conversion on a revenue page, or corrupts measurement such that other decisions are unsafe. |
| **Medium** | Degrades performance or consistency, with a plausible but unquantified revenue path. |
| **Low** | Correctness or hygiene issue with no demonstrated revenue path. |
| **Monitor** | Not actionable now; needs a defined trigger, owner and review date. |

Two rules that matter more than the table: severity is assigned from **business
consequence**, never from a tool's own severity label; and a finding on a page with no
traffic, no conversions, no backlinks and no paid or GBP dependency is not Critical no
matter how broken it is.

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
- Any finding asserting cannibalization on entity or keyword overlap alone, without
  unstable ranking URLs, split impressions/clicks, or query-level conflict
- Any merge, redirect, delete, noindex or canonical recommendation without a completed
  `value_dependency_check` and a `safer_alternative`
- Any indexation-rate calculation derived from a `site:` result count
- Any finding whose only evidence is a tool score
