# Stage 5 — Build plan, blockers and the facts round

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: build (Opus), researcher (Sonnet), clerk.

| Step | Command | Ends at |
|---|---|---|
| Technical blockers — one handoff to Jonie (worklist section 2); never holds up writing, gates release only | `/build blockers` + `/verify` | condition **blockers_cleared** |
| **Site plan** — every service, location and hub page in one pass; URL check (P7), competitor coverage | `/build plan` | **site_plan** |
| **One facts round** for every page (P10): grids, the researcher clears public facts, reviews attached, one question set grouped by fact | `/build facts` | answers recorded once (`run.py fact`) |

- URLs: one root slug per service, location and hub page — no folder, no city in a service slug, no service in a
  location slug, no `-2`; hubs are county or metro slugs (CM-058). `status.py plan` refuses anything else.
- Batches: one per kind (all services; all locations and hubs; home and about) — split only above 15 pages.
- The facts round's question set goes to Paul once; `/interview <slug> facts-answers all` records the answers.
