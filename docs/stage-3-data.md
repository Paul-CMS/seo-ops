# Stage 3 — Data (while the client has the sheet)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: researcher (Sonnet), discovery-audit (Opus).

| Step | Command | Ends at |
|---|---|---|
| Crawl (S05) and page text (S05b) | `/crawl` | — |
| Reviews → customer language and review facts (CM-057), rankings, backlinks, citations, grid, GSC, People Also Ask, query fan-out (S06–S11, S19–S21), competitor coverage (P6) — one cost yes | `/discovery data` | — |

- **`python3 scripts/pipeline.py <slug> inventory --run <RUN_ID> --state <ST> [--cities "A,B,C,D"] [--fanout]`** runs
  the whole inventory with no agent (Rewrite 4 Phase 1): one combined estimate (exit 5 until Paul says yes), then
  `--confirmed` runs crawl → page text → reviews → rankings → backlinks → PAA → competitor coverage (S21 only with
  `--fanout`, D6) and records every outcome; exit 10 = the crawl is still running (run it again); the first failure
  stops it. `--dry` is free and writes nothing in the client's folder.
- Every paid script: whole-run estimate first; over $2 (or an unconfirmed price) → ask Paul; `--confirmed` only after
  his yes. `steps.py fresh <slug> <S##>` first: data under 60 days old is reused. Agents read the summaries, never raw
  exports.
- Reviews: `reviews.py run` (checked against Google's count), then `reviews.py extract` — the CM-057 candidates. A
  keyword match never counts: `reviews.py meaning` (Claude API; `pipeline.py` runs it after S06), or with no API key the
  researcher (`reviews.py checked`); until then it is a yes/no line for Paul. Add themes to `customer-language.md`;
  quote, never attribute. The rating and count are saved exactly as Google shows them on the day, with the date (CM-027).
  Fewer than 5 reviews → S06 skipped.
- PAA and fan-out routing: `paa.py route` / `fanout.py route` fill Intent and Route on the Claude API (Haiku). A filled
  row is never overwritten; correct one by hand only when it is wrong. With "no API key — ran on the agent route" the
  agent routes every row: Intent (informational / problem-aware / commercial investigation / comparison /
  transactional) and Route (service FAQ — name the page · location FAQ — name the city page · blog topic · drop; drop
  anything already in C3). Fan-out queries are coverage, not demand (CM-045, CM-012). Past the PAA cap needs Paul's OK.
- Direct API calls (`scripts/llm.py`): every call is logged to `llm-costs.jsonl`; a job over the per-run cap
  (`config.json llm_run_cap_usd`) stops with CONFIRM — ask Paul, then re-run with `--confirmed`.
- Competitor coverage (`crawl.py competitors`): the top 3 pages' H2s and FAQ topics per service — ideas for the site plan
  only, never client claims (CM-016); the researcher groups them per service.

## One step run alone (the agent, when not on `pipeline.py`)
- **S06** `reviews.py estimate|run <slug> --run <RUN_ID> --keyword "<GBP name>" --location "<City>,<State>,United States"
  --services-file <services.txt> --cities "<c1>,<c2>"` → `data/reviews/` (read `reviews-summary.md` and
  `customer-language.md`), then `reviews.py extract`.
- **S07** `rankings.py estimate|run <slug> --run <RUN_ID> --services-file <services.txt> --cities "<c1>,..." --state "<ST>"`.
- **S08** `dfs.py call … --out clients/<slug>/data/backlinks/raw/backlinks-<date>.json`, then `backlinks.py summary
  <slug>`; read `backlinks-per-url.csv`.
- **S09 / S10** BrightLocal uploads from Gwen; Local Dominator PDFs: `grid_pdf.py <slug>` once, read
  `local-grid-summary.md`. Not there yet → `skipped` with the reason. **S11** GSC/GA4 only if access exists.
- **S19** `paa.py estimate|run <slug> --run <RUN_ID> --services-file <services.txt> --cities "<primary>,<c2>,<c3>,<c4>"
  --state "<ST>" [--cap 20] [--registry <C3 file>]`, then `paa.py route`.
- **S20** not WordPress → `skipped` "not WordPress"; credentials in place → `/wp-check <slug>` now; no access → `skipped`.
- **S21** (`--fanout` only) `fanout.py estimate|run <slug> --run <RUN_ID> --services-file <services.txt> --cities "…"
  [--cap 10] [--per-seed 40] [--registry <C3 file>] --paa clients/<slug>/data/paa/paa-questions.csv`, then `fanout.py route`.
- Competitor coverage: `crawl.py competitors estimate|run <slug> --run <RUN_ID> --location "<city>,<ST>,United States"
  --keywords-file <services.txt>` → `data/competitors/coverage.md`.
