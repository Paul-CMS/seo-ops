# Audit steps — the registered list
### Every data step /discovery runs, in order. `scripts/steps.py` reads the table below.

**The rule (Paul, 2026-10-02):** every run records an outcome for every step — **Done**,
**Skipped** (with a reason) or **Failed** (with what went wrong) — in status.json, and the
Evidence Manifest shows them. The audit-deliverables condition cannot be met while any step
has no outcome. **A new add-on (tool, export, script) is unfinished until it has a row here.**

**Reuse:** discovery data is saved once per client (`clients/<slug>/inputs/`) and reused by
later stages. A step marked *Reusable* is re-run only if its last Done is older than 60 days
(`steps.py fresh`), or Paul asks.

**Order (Paul, 2026-10-02):** entity → architecture (URL Decision Map) → page conformance →
technical findings. Steps S05–S09 run **while the client has the proof sheet**.

| ID | Step | Phase | How | Outputs | Used by | Reusable |
|---|---|---|---|---|---|---|
| S01 | Intake facts: website, GBP link, storefront/SAB, exact GBP Website-field URL, GSC/GA4 access | Discovery | Paul, /new-client | status.json client fields | Entity, schema (LocalBusiness test) | no |
| S02 | Public discovery: live site, GBP, social, review profiles, Secretary of State, licence board | Discovery | discovery-audit agent, web | Discovery Record; Brand Guide D claims | Proof sheet, Brand Guide | yes |
| S03 | Entity research: category entity (Wikipedia), area entity (Russian Doll), variants, Wikidata URIs | Discovery | discovery-audit agent, Wikipedia/Wikidata | Brand Guide A, B, F | Entity approval; every spec | yes |
| S04 | Proof sheet built (Markdown + client Google Doc) | Discovery | discovery-audit agent | Client Proof Sheet | Proof sheet condition | no |
| S05 | Site crawl | Client has sheet | `/crawl` (DataforSEO OnPage, basic) | `DFS -` crawl tables + crawl-config | Architecture, conformance, technical; Evidence Manifest | yes |
| S06 | Reviews pull: Google rating, count, recent review text | Client has sheet | DataforSEO business_data (or manual) | `DFS - reviews` | Brand Guide D (rating = "The Best" proof), I (customer language) | yes |
| S07 | Rankings pull: ranked keywords per URL (top 100) | Client has sheet | DataforSEO Labs ranked_keywords | `DFS - ranked-keywords` | URL Decision Map (CM-019), top-3 H1 lock (CM-020) | yes |
| S08 | Backlinks pull: referring domains per URL | Client has sheet | DataforSEO Backlinks | `DFS - backlinks` | URL Decision Map (CM-019) | yes |
| S09 | Citations | Client has sheet | BrightLocal citation tracker (Gwen uploads) | `BL - citation-tracker` | Entity findings (NAP) | yes |
| S10 | Local grid | Client has sheet | BrightLocal grid (DataforSEO alongside on the pilot client only) | `BL - local-grid` | Entity findings | yes |
| S11 | Search Console / GA4 | Client has sheet | Client access, if any | `GSC -`, `GA4 -` | Severity, URL Decision Map | yes |
| S12 | Ingest + cross-checks | Audit | seo-technical-audit `ingest_evidence.py`, `crosscheck.py` | Evidence Manifest, 00-crosschecks | Every finding | no |
| S13 | Entity analysis: site vs Brand Guide (triple, NAP, brand search, supporting assets) | Audit | discovery-audit agent | Finding Register (entity) | Recommendations | no |
| S14 | Architecture: every page typed, keep/merge/redirect per CM-019 | Audit | discovery-audit agent | URL Decision Map | Site plan, Build | no |
| S15 | Page conformance: every page scored against its spec | Audit | discovery-audit agent + `methodology/specs/` | Conformance scorecard; Finding Register (page) | Site plan, Build | no |
| S16 | Technical findings (Low batched into one handoff) | Audit | discovery-audit agent | Finding Register (technical) | Technical handoff | no |
| S17 | Fresh-context review of Finding Register + URL Decision Map | Audit | audit-reviewer agent | Revised registers; decisions.md exception | Audit approval | no |
| S18 | Render deliverables | Audit | discovery-audit agent | Recommendations, Evidence Manifest (with step outcomes) | Audit approval | no |

## Severity (Paul, 2026-10-02 — by Bradley impact)

| Severity | Means |
|---|---|
| **High** | Breaks the entity model or page structure, or blocks indexing |
| **Medium** | Weakens a page against its spec |
| **Low** | Technical hygiene — batched into one handoff |

**One finding per issue, with all affected URLs** — never one finding per URL.

## Adding a step

Add a row (next free ID, in the right phase), say what it outputs and which deliverable uses
it, then run it. Until the row exists, the add-on's output is not evidence.
