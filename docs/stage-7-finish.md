# Stage 7 — Finish

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: finish (Sonnet), finish-qa (Opus), clerk.

| Step | Command | Ends at |
|---|---|---|
| Link wheel → verify; `[LINK → …]` markers resolved (CM-022 exceptions) | `/finish wheel` | **link_wheel_approved** |
| Schema → QA crawl → content QA → punch-list → acceptance | `/finish schema`, `/finish qa` | **release_approved** (needs blockers cleared) |

- Content QA runs in finish-qa, never the context that wrote the copy (CM-018). The QA crawl covers published pages only.
