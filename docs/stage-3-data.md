# Stage 3 — Data (while the client has the sheet)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: researcher (Sonnet), discovery-audit (Opus).

| Step | Command | Ends at |
|---|---|---|
| Crawl (S05) and page text (S05b) | `/crawl` | — |
| Reviews → customer language and review facts (CM-057), rankings, backlinks, citations, grid, GSC, People Also Ask, query fan-out (S06–S11, S19–S21), competitor coverage (P6) — one cost yes | `/discovery data` | — |

- **`python3 scripts/pipeline.py <slug> inventory --run <RUN_ID> …`** runs the whole inventory with no agent (Rewrite 4
  Phase 1): one combined estimate (exit 5 until Paul says yes), then `--confirmed` runs crawl → page text → reviews →
  rankings → backlinks → PAA → competitor coverage (S21 only with `--fanout`) and records every outcome; the first
  failure stops it. `--dry` is free and writes nothing in the client's folder.
- Every paid script: whole-run estimate first; over $2 → ask Paul.
- Reviews: `reviews.py run` (the pull is checked against Google's count), then `reviews.py extract` — a fact 3+
  different reviewers report is a `customer_reported` candidate (CM-057). A keyword match never counts: every match
  is read by meaning — `reviews.py meaning` (on the Claude API, Rewrite 4 Phase 2; `pipeline.py` runs it after S06),
  or, with no API key, the researcher (`reviews.py checked`); until then it is a yes/no line for Paul.
- PAA and fan-out routing: `paa.py route` / `fanout.py route` fill Intent and Route on the Claude API (Haiku;
  `pipeline.py` runs them after S19/S21). A filled row is never overwritten. No API key yet (or the API answers 401): the script says "no API key — ran on the agent route" and the agent does it as before.
- Direct API calls (`scripts/llm.py`): every call is logged to `llm-costs.jsonl`; a job over the per-run cap
  (`config.json llm_run_cap_usd`) stops with CONFIRM — ask Paul, then re-run with `--confirmed`.
- Competitor coverage (`crawl.py competitors`): the top 3 pages' H2s and FAQ topics per service — ideas only, never
  client claims (CM-016).
- Data is saved once per client and reused (re-run if older than 60 days). Agents read the summaries, never raw exports.
