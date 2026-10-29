# Carolina Carpet Cleaning - Status

- **Stage 4 of 8 — Audit**
- **What is happening now:** Stage 3 (Data) is done in this session. Start a new session (new chat, model: Haiku) in the client folder (python3 scripts/worktree.py open carolina-carpet-cleaning) and type /next carolina-carpet-cleaning. Next there: /discovery carolina-carpet-cleaning audit (the audit: entity → architecture → page conformance → technical, then the fresh-context review)
- **Waiting on:** nobody
- **Next action:** `/next carolina-carpet-cleaning` once the wait above is over · model: Haiku chat

_Generated 2026-10-29T07:50 by the system — do not edit. Start every session in the client folder (`python3 scripts/worktree.py open <slug>`), one session per stage._

## Waiting on

| Who | What | Since | Reference |
|---|---|---|---|
| — | nothing | | |

## Waiting on (not blocking)

_Open, but the next action above goes ahead without them._

| Who | What | Since | Reference |
|---|---|---|---|
| Gwen | manual lookup handoff — 9 of 9 item(s) open | 2026-10-28 | H-2026-10-28-01-manual_lookup |

## Settled decisions — never re-raised

- 2026-10-14: page specs (global: location) — approved
- 2026-10-28: Discovery approved — the Decision Sheet (every identity and format decision) and the entity foundation (category, area, variants, reserved homepage variant) — approved
- 2026-10-28: Client facts approved — the proof sheet ready for Paul to send, or the client's answers taken directly — approved
- The site runs on wordpress
- Site connection: Novamira MCP, read-only until the handoff is approved; no Application Password setup
- GBP primary category = the category entity: **Carpet cleaning service** → Wikipedia "Carpet cleaning" (Q5045777) — provisional until Gwen reads the GBP primary category (H-2026-10-28-01); if GBP shows another category, that category stands and this row reopens (recommended default)
- Category variants (4–6): carpet cleaning · carpet cleaning service · carpet cleaners · carpet cleaning company · carpet cleaner (recommended default)
- Scope descriptor: **residential and commercial** (description only, never a category variant) (recommended default)
- Area entity: **Hilton Head Island metropolitan area** (official: Hilton Head Island–Bluffton–Port Royal, SC MSA; Q17020871). Alternative: **South Carolina Lowcountry** (Q3885311) if Yemassee must sit wholly inside (recommended default)
- Area variants (3–5): Hilton Head Island Metro Area · South Carolina Lowcountry · Hilton Head Island–Bluffton–Port Royal area · Lowcountry (recommended default)
- Area variant reserved for the homepage SEO title: **Hilton Head Island Metro Area** (exclusive; the live title already uses it) (recommended default)
- Area variant for the homepage H1: **South Carolina Lowcountry** (the live H1) (recommended default)
- SEO-title format — homepage: `Category Variant in Area - Brand` (recommended default)
- SEO-title format — service pages: `Service Name - Brand` (recommended default)
- SEO-title format — location pages: `Category Variant in City, ST - Brand` (recommended default)
- SEO-title format — about page: `About Brand - Category in Area` (recommended default)
- SEO-title format — blog posts: `Post Title - Brand` (recommended default)
- Brand written in full in every title: yes — "Carolina Carpet Cleaning" (recommended default)
- Services offered: Carpet Cleaning · Residential Carpet Cleaning · Commercial Carpet Cleaning · Low-Moisture Carpet Cleaning · Carpet Stain Removal · Pet Odor Removal · Upholstery Cleaning · Tile & Grout Cleaning · Hardwood Floor Cleaning · Oriental Rug Cleaning · Area Rug Cleaning · Boat & Auto Interior Cleaning (RV/camper per press release) — which become pages or fold together is the audit's URL decision (recommended default)
- Towns served: **The 6 live location towns only:** Hilton Head Island, Bluffton, Beaufort, Ridgeland, Hardeeville, Lady's Island. The other towns are not kept for now. (recommended default)
- Street address on GBP?: **No** (service-area business) (recommended default)
- Street address on the website?: **Yes** — 273 Club Gate, Bluffton, SC 29910 (pending the client's confirmation of the Birdeye Beaufort address conflict) (recommended default)
- "The Best" in H1s: per page, by CM-020 (recommended default)
- Blog author (a real person, CM-039): **Kevin Snow**, owner — once the returned facts confirm him (recommended default)
- Sensitive category: **No** (recommended default)
- WordPress access for the system: **N/A — settled**: Novamira MCP, read-only until the handoff is approved; no Application Password (recommended default)
- Citations data this audit: BrightLocal citation tracker (VA uploads the CSV) (recommended default)
- Local grid tool: BrightLocal (recommended default)
- Search Console / Analytics: **Search Console: use the exports already supplied** (coverage + per-page performance, 2026-10-28); **GA4: not used** (none) (recommended default)

## Open VA items

_Every VA item is in one living worklist: `handoffs/VA-WORKLIST.md` (Drive: "Carolina Carpet Cleaning - VA Worklist")._

- **H-2026-10-28-01-manual_lookup** (Gwen) — manual lookup: 9 of 9 open, issued 2026-10-28

## Data on file not used yet

_Inputs the data manifest (methodology/data-manifest.json) says a step must read, where that step has not finished for this client yet._

- **reviews** (1 file(s), e.g. `data/reviews/reviews.csv`) — read by build:evidence, build:facts
- **reviews-raw** (2 file(s), e.g. `data/reviews/raw/reviews.json`) — read by the step that reads reviews
- **review-mentions** (1 file(s), e.g. `data/reviews/mentions.csv`) — read by build:evidence, build:facts
- **review-facts** (1 file(s), e.g. `data/reviews/review-facts.json`) — read by build:evidence, build:facts
- **customer-language** (2 file(s), e.g. `data/reviews/customer-language.md`) — read by discovery:audit, build:brief, build:write
- **paa-questions** (2 file(s), e.g. `data/paa/paa-questions.csv`) — read by build:evidence, discovery:fanout
- **paa-raw** (20 file(s), e.g. `data/paa/raw/area-rug-cleaning-hilton-head-island.json`) — read by the step that reads paa-questions
- **paa-routing** (1 file(s), e.g. `data/paa/paa-routing.md`) — read by build:plan, blog:map, build:brief, build:write
- **rankings** (5 file(s), e.g. `data/rankings/best-variants.csv`) — read by build:plan, discovery:audit
- **rankings-raw** (2 file(s), e.g. `data/rankings/raw/best-variants.json`) — read by the step that reads rankings
- **competitors** (2 file(s), e.g. `data/competitors/coverage.json`) — read by build:plan
- **crawl-page-text** (2 file(s), e.g. `data/crawl/crawl-summary.csv`) — read by discovery:audit, build:evidence
- **crawl-raw** (36 file(s), e.g. `inputs/crawl/crawl-state-2026-10-28-10290009.json`) — read by the step that reads crawl-page-text
- **imported-exports** (32 file(s), e.g. `inputs/Carolina Carpet Cleaning - CMS - export-all-urls - 2026-10-28.csv`) — read by discovery:audit
- **cms-page-inventory** (1 file(s), e.g. `data/novamira-page-inventory-2026-10-28.md`) — read by discovery:audit
- **discovery-record** (2 file(s), e.g. `discovery/Carolina Carpet Cleaning - Discovery Record - REVIEW.md`) — read by build:evidence, build:facts
- **facts** (1 file(s), e.g. `facts.json`) — read by build:evidence, build:facts
- **settled** (1 file(s), e.g. `decisions-settled.md`) — read by build:evidence, build:facts, build:brief, build:draft, build:drafts, build:write, build:plan

## Flagged for Paul (system)

- **F-003** (open, not yet reviewed) 2026-10-28 · crawl: DataforSEO task 10290139 (carpetcleaningblufftonsc.com, basic, 132 pages) stays 'In Queue' (error 40602); resume returns exit 8 on every call. Earlier retries posted 34 paid tasks (about $0.67) because crawl.py run does not stop on exit 8 before reposting; see F-002. — workaround: Stopped after three free resume attempts. No new paid task posted. Run 20261028-204638-crawl-94cd left open for Paul's decision.

## Spend so far

- DataforSEO: $1.03 (of which failed tasks $0.01)
- Claude API (llm.py): $0.00 over 0 call(s)

## Spend by stage (model)

_Session = the chats and their agents; API = llm.py's direct calls._

| Stage | Runs | Tokens | Session USD | API USD |
|---|---|---|---|---|
| 1 · Setup | 1 | 1,944,639 | $0.80 | $0.00 |
| 2 · Discovery | 2 | 4,718,881 | $2.04 | $0.00 |
| 3 · Data | 3 | 4,864,287 | $0.30 | $0.00 |
| any stage | 3 | 816,224 | $0.13 | $0.00 |
| **total** | 9 | 12,344,031 | $3.27 | $0.00 |

## Spend by step (model)

| Step | Runs | Tokens | Session USD | API USD |
|---|---|---|---|---|
| discovery:discovery | 1 | 3,941,016 | $2.03 | $0.00 |
| new-client | 1 | 1,944,639 | $0.80 | $0.00 |
| discovery:data | 1 | 0 | $0.22 | $0.00 |
| answers | 3 | 816,224 | $0.13 | $0.00 |
| crawl | 2 | 4,864,287 | $0.08 | $0.00 |
| discovery:facts-direct | 1 | 777,865 | $0.01 | $0.00 |
| **total** | 9 | 12,344,031 | $3.27 | $0.00 |

Last run: /crawl 2026-10-29T07:50 — Crawled 92 pages of carpetcleaningblufftonsc.com (task 10290153, basic), $0.0198; 89 page texts captured; files uploaded to Drive
