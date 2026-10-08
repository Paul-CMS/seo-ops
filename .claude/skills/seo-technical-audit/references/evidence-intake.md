# Evidence Intake and Phase 0 Readiness

## Load and pin

Before any analysis, locate and read:

1. **Methodology and guidelines file** — root drive resources folder
2. **Brand / truth file** — the client's Brand Guide (`clients/<slug>/brand-guide.md`)
3. **intake record (Client Control Record)** — the client's drive
4. **Evidence folder** — the exports

Then state which version of each was loaded, in `README.md`.

**If the methodology file cannot be found, stop.** Do not proceed on general SEO
knowledge. Half the value of this skill is that the client's rules override a model's
defaults; an audit run without them looks identical and is not.

## Recognised exports

`scripts/ingest_evidence.py` fingerprints by **header signature**, not filename —
filenames vary by client, VA and export date; column sets do not.

| Recognised as | Category |
|---|---|
| `screamingfrog.internal_all` / `external_all` / `links_all` / `javascript_all` | crawl |
| `screamingfrog.h1_all` / `h2_all` / `page_titles_all` / `meta_description_all` | crawl |
| `screamingfrog.all_inlinks` | crawl |
| `siteauditor.overview` / `pages` / `anchor_text` / `images` | crawl |
| `siteauditor.issues` / `ai_engines` / `internal_links` | tool_findings |
| `citationtracker.audit` | citations |
| `cms.wordpress_all_urls` | cms_inventory |
| `gsc.queries` / `pages` / `page_indexing` | measurement |
| `localserp.audit_sheet` | local_visibility |
| `dataforseo.duplicate_tags` / `duplicate_content` / `redirect_chains` / `non_indexable` | crawl |
| `dataforseo.crawl_config` (the `DFS - crawl-config` file) | crawl |
| `sitemap.urls` (any `*sitemap*.txt` / `.xml` / `.csv` — one URL per line or `<loc>`) | crawl |

### The client's other evidence — by folder, one manifest row per file

The data steps write their outputs under `clients/<slug>/data/`; `ingest_evidence.py` finds
the client folder from the evidence path (or `--client-dir`) and adds a row for every file
there and under `inputs/` outside the crawl folder. Each `raw/` folder is one row (file
count, total size). `--no-extra` reads the crawl folder only.

| Folder | Recognised as | Category |
|---|---|---|
| `data/reviews/` | `data.reviews (S06)` | reviews |
| `data/rankings/` | `data.rankings (S07)` | rankings |
| `data/backlinks/` | `data.backlinks (S08)` | backlinks |
| `data/citations/` | `data.citations (S09)` | citations |
| `data/local-grid/` | `data.local_grid (S10)` — `local-grid-summary.md` from `scripts/grid_pdf.py` | local_visibility |
| `data/gsc/` | `data.gsc (S11)` | measurement |
| `data/paa/` | `data.paa (S19)` | content_research |
| `data/fanout/` | `data.fanout (S21)` — never demand (CM-045) | content_research |
| `data/` (top level, e.g. `services.txt`) | `data.client_lists` | intake |
| `inputs/seopress-settings-*.json` | `wordpress.settings (S20)` | cms_settings |
| `inputs/local-grid/*.pdf` | `localdominator.grid_pdf (S10)` — read the summary, not the PDF | local_visibility |
| `inputs/live-pages/` | `manual.live_capture` | crawl_supplement |

A standard export dropped into `data/` (a GSC or citation CSV) keeps its fingerprinted
type. URLs in these files' `url` / `page` columns join the URL inventory. Two manifest
columns are added for them and for every crawl export: `size_bytes` and `file_date` (the
date in the file name, else the file's modified date).

Note the `tool_findings` category is deliberately separate from `crawl`. Those exports
contain a tool's conclusions, and the workflow treats them differently throughout —
see `reconciliation.md`.

Unrecognised files are listed in `00-unrecognised.md` and never silently dropped. If an
unrecognised type recurs, add its signature to the script.

## Manifest fields the script cannot fill

`ingest_evidence.py` writes `tool_settings`, `date_window`, `geography_device` and
`scope_limits` blank on purpose. They are not in the exports. They come from the person
who ran the tool, and they are exactly what determines whether a finding is safe.

Fill them before the readiness check. Where unknown, the correct value is `unknown` —
which then flows into the readiness check as a possible halt.

## Phase 0 readiness check

Runs automatically as part of Phase 0, not as a separate stop. It produces a coverage
table and halts only on genuinely fatal conditions.

### Halt on any of these

- Methodology or guidelines file not found
- Intake record missing, or business truth not confirmed
- Crawl scope unknown or clearly partial, **when architecture is in scope**
- Rendering mode unknown, **when the site is JS-dependent**

### Everything else becomes a limitation and the audit proceeds

Missing GSC, no backlink export, no grid runs, incomplete citation data, unknown date
windows on a non-critical source — all of these produce an `N/A` with rationale on the
affected category and a row in Assumptions & Limitations.

### Why conditional rather than a hard gate

An unconditional stop on every audit is friction that gets skipped by month three, and a
control that gets skipped is worse than one that never existed. Four fatal conditions
cost nothing on a clean evidence set and prevent the expensive failure: eighty findings
written against a crawl that ran without rendering.

### Coverage table

For each of the nine Analysis categories, record: evidence present, source IDs, and
whether the category can be assessed. Categories with no evidence are marked `N/A` with
rationale **here**, at the start — not discovered missing at the exit gate.

| Category | Evidence | Source IDs | Assessable |
|---|---|---|---|
| 1 Baseline & measurement | | | |
| 2 Technical & crawl | | | |
| 3 Brand & entity | | | |
| 4 GBP & local | | | |
| 5 Architecture | | | |
| 6 On-page | | | |
| 7 Blog & supporting | | | |
| 8 Citations & authority | | | |
| 9 Schema readiness | | | |
