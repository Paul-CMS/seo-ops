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
technical findings. Steps S05–S11 and S19–S21 run **while the client has the proof sheet**.

| ID | Step | Phase | How | Outputs | Used by | Reusable |
|---|---|---|---|---|---|---|
| S01 | Intake facts: website, GBP link, storefront/SAB, exact GBP Website-field URL, GSC/GA4 access | Discovery | Paul, /new-client | status.json client fields | Entity, schema (LocalBusiness test) | no |
| S02 | Public discovery: live site, GBP, social, review profiles, Secretary of State, licence board | Discovery | discovery-audit agent, web | Discovery Record; Brand Guide D claims | Proof sheet, Brand Guide | yes |
| S03 | Entity research: category entity (Wikipedia), area entity (Russian Doll), variants, Wikidata URIs | Discovery | discovery-audit agent, Wikipedia/Wikidata | Brand Guide A, B, F | Entity approval; every spec | yes |
| S04 | Proof sheet built (Markdown + client Google Doc) | Discovery | discovery-audit agent | Client Proof Sheet | Proof sheet condition | no |
| S05 | Site crawl | Client has sheet | `/crawl` (DataforSEO OnPage, basic) | `DFS -` crawl tables + crawl-config | Architecture, conformance, technical; Evidence Manifest | yes |
| S06 | Reviews pull: Google rating, count, recent review text (no reviewer names) | Client has sheet | `scripts/reviews.py` (DataforSEO Business Data) | `data/reviews/reviews.csv`, `mentions.csv`, `customer-language.md`; rating + count in status.json evidence | Brand Guide I (customer language); rating/count = "The Best" proof (CM-020, CM-027). Never Section D unless client-confirmed (CM-027) | yes |
| S07 | Rankings + cannibalization: every ranked keyword per URL (top 100), conflict clusters, "best" variant volumes | Client has sheet | `scripts/rankings.py` (DataforSEO Labs + Google Ads volume) | `data/rankings/ranked-keywords.csv`, `url-rankings.csv`, `cannibalization.csv`, `best-variants.csv`, `rankings-summary.md` | URL Decision Map (CM-019), top-3 H1 lock and demand test (CM-020), cannibalization (RULE-005, CM-021) | yes |
| S08 | Backlinks pull: referring domains per URL | Client has sheet | DataforSEO Backlinks | `DFS - backlinks` | URL Decision Map (CM-019) | yes |
| S09 | Citations | Client has sheet | BrightLocal citation tracker (Gwen uploads) | `BL - citation-tracker` | Entity findings (NAP) | yes |
| S10 | Local grid | Client has sheet | BrightLocal grid, or **Local Dominator** scan reports (Paul, 2026-10-07) — DataforSEO alongside on the pilot client only. Only the measured results are used (average rank per keyword and view, grid size and spacing, competitors with their average rank); the report's own written advice is never used | `BL - local-grid` or `MANUAL - local-grid-<keyword>-<view>` (Local Dominator PDF) + `data/local-grid/local-grid-summary.md` | Entity findings | yes |
| S11 | Search Console / GA4 | Client has sheet | Client access, if any | `GSC -`, `GA4 -` | Severity, URL Decision Map | yes |
| S19 | People Also Ask: core services × primary city + top 3 cities, capped (default 20 queries) | Client has sheet | `scripts/paa.py` (DataforSEO SERP), then the discovery-audit agent routes each question | `data/paa/paa-questions.csv`, `queries.csv`, `paa-routing.md` (intent + route: service FAQ / location FAQ / blog topic / drop; C3 duplicates dropped) | Site plan FAQ topics, briefs, Blog topic list | yes |
| S20 | SEOPress site-wide settings (title templates, sitemap, noindexed post types, Knowledge Graph schema) — read-only | Client has sheet | `/wp-check` (saved if readable as Editor) or Jonie's one-time VA check; `skipped` if there is no WordPress access yet | `inputs/seopress-settings-*.json` or the returned check worksheet | Technical findings; schema readiness (duplicate schema, wordpress-site-setup.md §8) | yes |
| S21 | Query fan-out (CM-045): core services × primary city + top 3 cities, capped (default 10 seeds × 40 queries) — an LLM's brainstorm of likely searches, **not demand** (no volume) | Client has sheet | `scripts/fanout.py` (DataforSEO AI Optimization, LLM responses; ≤ ~$0.0072 per seed), then the discovery-audit agent routes each query | `data/fanout/fanout-queries.csv`, `seeds.csv`, `fanout-routing.md` (intent + route: service H2/FAQ / location FAQ / blog topic / drop; C3 and PAA duplicates pre-marked) | Site plan coverage check (every kept query answered by a page or a blog topic), Blog Decision Map and topic list — alongside PAA (S19). Never evidence for CM-019/020/021 | yes |
| S12 | Ingest + cross-checks | Audit | seo-technical-audit `ingest_evidence.py`, `crosscheck.py` | Evidence Manifest, 00-crosschecks | Every finding | no |
| S13 | Entity analysis: site vs Brand Guide (triple, NAP, brand search, supporting assets) | Audit | discovery-audit agent | Finding Register (entity) | Recommendations | no |
| S14 | Architecture: every page typed, keep/merge/redirect per CM-019 | Audit | discovery-audit agent | URL Decision Map | Site plan, Build | no |
| S15 | Page conformance: every page scored against its spec (check IDs HP/SVC/LOC/HUB/ABT/BLG) | Audit | discovery-audit agent + `methodology/specs/<type>.md` | Conformance scorecard (results placed in the nine categories, analysis-rules.md); Finding Register (failed check = Medium, CM-028) | Site plan, Build | no |
| S16 | Technical findings (Low batched into one handoff) | Audit | discovery-audit agent | Finding Register (technical) | Technical handoff | no |
| S17 | Fresh-context review of Finding Register + URL Decision Map | Audit | audit-reviewer agent | Revised registers; decisions.md exception | Audit approval | no |
| S18 | Render deliverables | Audit | discovery-audit agent | Recommendations, Evidence Manifest (with step outcomes) | Audit approval | no |

## Severity

One scale only: CM-028 in `methodology/rulings.md`, shown in `.claude/skills/seo-technical-audit/references/finding-standard.md`.

## Adding a step

Add a row (next free ID, in the right phase), say what it outputs and which deliverable uses
it, then run it. Until the row exists, the add-on's output is not evidence.
