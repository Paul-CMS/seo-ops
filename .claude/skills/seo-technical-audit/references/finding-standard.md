# Finding Standard (CM-063)

## The record

One row per finding in `findings.csv`, in the workbook's column order (columns prefixed `ext_` are this skill's).
Blank means nobody decided; `N/A` is a valid value.

| Column | Rule |
|---|---|
| `Finding ID`, `ext_revision` | `F-001`, stable forever; `1` on creation, +1 on each superseding row (append-only) |
| `Category` | One of the nine analysis categories (`analysis-rules.md`) |
| `Affected URL / Entity` | Every affected URL. "Site-wide" only when every URL is affected |
| `Observation` | What was observed — no cause, no recommendation |
| `Evidence / Locator` | `SRC-NNN` + file, row range or screenshot. **No locator, no finding** |
| `Classification` | Platform Requirement · Bradley Methodology Rule · Project Evidence · Working Hypothesis · Client Constraint · Paul Exception (RULE-001) |
| `Confidence` | Corroborated (two independent sources) · Single-source · Contested · Assumed |
| `Alternative Explanation` | At least one other explanation of the same evidence |
| `Recommendation` | Scoped and reversible; for Fix and list this is the default that will be applied |
| `Risk if Acted`, `Risk if Deferred` | Both |
| `Priority` | **The severity: `Fix` · `Fix and list` · `Ask`** (below) |
| `Owner`, `Status` | Owner placeholder (VA, Build, Paul); `draft` / `reviewed` / `superseded` / `withdrawn` |
| Ask only: `ext_ask_kind`, `ext_options`, `ext_default`, `ext_plain_why`, `ext_decision_key` | kind 1–4; options `a) … · b) …` (at least two); the recommended letter; one plain sentence on why it matters; a stable key |
| Client fact only: `ext_searched` | the `searched:` line — facts.json → decisions-settled.md → reviews → site text → GBP → proof sheet |

Observation, inference and recommendation never share a column. Methodology (one H1, citation counts, triples,
variants) is a Bradley Methodology Rule, never a Platform Requirement.

## Severity — CM-061 (definitions: `methodology/definitions.md`)

| Severity | Audit meaning | Where it goes |
|---|---|---|
| **Fix** | Technical hygiene with no content decision: broken links, redirect chains, alt text, sitemap, robots, canonicals, duplicate meta, speed | The Technical Blocker Checklist (§1) → one VA handoff after the audit approval |
| **Fix and list** | A change made by default: a spec failure Build's rebuild fixes, a title or H1 the rebuild resets, a light fix on a kept page, a menu change | "Decided for you" in the review sheet — Paul can override any |
| **Ask** | Only the four kinds | "Questions for Paul" (kinds 1, 2, 4) or the client list (kind 3) |

The four Ask kinds: **1** page or URL decision (most audit Asks: every destructive URL row becomes one automatically
— do not write a finding for it) · **2** a legal or money claim on the live site (guarantees, warranties, licences,
prices) · **3** a client-only fact not found after the search order — it goes to the client list · **4** a real
conflict between two sources of equal standing (two `SRC-` ids). Anything else with a sensible default is Fix and list.
Severity never comes from a tool's own label. A missing "The Best" is never a finding (CM-020).

## Findings that must not be written

- Any finding whose cross-check came back `CONTRADICTED`
- A tool's issue list, or a tool score, as the only evidence
- An orphan claim on crawl evidence alone; cannibalization without RULE-005 / RULE-015 / CM-021 evidence
- Any merge, redirect, noindex or canonical change on a URL the screen fails (CM-019) — the URL stays live
- An indexation rate from a `site:` count (CM-008)
- Missing JavaScript-rendered data
