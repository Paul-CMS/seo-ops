# CMS SEO System — Bradley rules + Novamira execution (v1)

| Folder | What it is |
|---|---|
| `rules/` | The ruled master rulebook split by stage. `rules/README.md` = which step loads which file |
| `handoff/` | Handoff spec + template folder (handoff.json + content/*.md) |
| `skills/novamira-executor/` | Skill + `build_bundle.py` (validate, convert) + `cms-executor.php` (runs on the site) |
| `skills/implementation-qa/` | Skill + `verify_live.py` (checks the live site, no model tokens) |
| `CONFLICT-PATCHES.md` | Lines in your existing skills to change so there's one rulebook |
| `runbook/TEST-RUN.md` | Step-by-step first run with copy-paste messages |

Flow: Agent 2 writes handoff → build_bundle.py validates → Paul approves → backup → upload with curl
→ preflight → stage (drafts) → VA review → apply → verify → verify_live.py → Paul.
