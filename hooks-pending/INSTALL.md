# Hooks waiting for Paul to install

Paul authorised these hook changes on 2026-10-08 (items R2, R8 and #20 of REWRITE-HANDOFF.md). The guard stops Claude
from writing `.claude/hooks/` or `.claude/settings.json` at all, so the new versions wait here. `tests/run_all.py`
already runs against these files, so the suite checks exactly what gets installed.

| File | What changes |
|---|---|
| `guard.py` | #20: read-only chains (`cd x && cat log.md \| grep …`) and record names / `.env` inside quoted arguments of a commit message, echo or script `--text` are allowed; every write protection stays. R8: the Drive connector's `search_files` must be scoped to a folder in v3 (`parentId = '<id>'`). |
| `approve_token.py` | R2: also records the session id on every prompt (`.claude/state/session.json`). |
| `session_start.py` (new) | R1/R2: records the session id at session start and prints the model reminder (Haiku for stage sessions, Opus for system sessions; warns on any other model). |
| `settings.json` | adds the SessionStart hook. |

**Until they are installed, `run.py start` refuses every stage run** ("the seo-ops session hook is not installed"):
the one-session-per-stage rule is enforced through them.

## Install (Paul, in a terminal — Claude can't run this)

```bash
cd ~/Documents/seo-ops && cp hooks-pending/guard.py hooks-pending/approve_token.py hooks-pending/session_start.py .claude/hooks/ && cp hooks-pending/settings.json .claude/settings.json && git rm -rq hooks-pending && python3 tests/run_all.py
```

Then start a new Claude Code session (the SessionStart hook runs only at the start of a session).
