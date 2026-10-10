# Stage 3 — Data (while the client has the sheet)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: clerk, researcher (Sonnet), discovery-audit (Opus).

| Step | Command | Ends at |
|---|---|---|
| Crawl (S05) and page text (S05b) | `/crawl` | — |
| Reviews → customer language and review facts (CM-057), rankings, backlinks, citations, grid, GSC, People Also Ask, query fan-out (S06–S11, S19–S21), competitor coverage (P6) — one cost yes | `/discovery data` | — |

- Every paid script: whole-run estimate first; over $2 → ask Paul.
- Reviews: `reviews.py run` (the pull is checked against Google's count), then `reviews.py extract` — a fact 3+
  different reviewers report is a `customer_reported` candidate (CM-057). A keyword match never counts: the
  researcher reads each by meaning and records it (`reviews.py checked`); until then it is a yes/no line for Paul.
- Competitor coverage (`crawl.py competitors`): the top 3 pages' H2s and FAQ topics per service — ideas only, never
  client claims (CM-016).
- Data is saved once per client and reused (re-run if older than 60 days). Agents read the summaries, never raw exports.
