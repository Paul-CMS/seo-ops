# Pending hooks — Paul installs them

Claude may not edit `.claude/hooks/` or `.claude/settings.json` (the guard blocks it). Hook changes are written
here; `tests/run_all.py` runs the suite against these files; Paul installs them from his own terminal.

## What changes (rewrite 2, 2026-10-09)

| File | Change |
|---|---|
| `guard.py` | **P3** system files change only in a session where Paul typed `/system` (refused on a VA Mac); `change-requests.md` and `clients/*/flags.jsonl` are append-only, scripts only. **P2** Claude cannot clear a client lock (`run.py unlock`, `seo-ops-locks/`). **P12** in a client session: no whole read of `methodology/rulings.md`, no read of `clients/*/log.md` or `handoff-log.md`. |
| `approve_token.py` | **P3** `/system` writes the system token for that session. **P2** one state file per session (`.claude/state/sessions/<id>.json`). |
| `session_start.py` | **P2** one state file per session; `CLAUDE_SEO_OPS_SESSION=<id>` written to the session's `CLAUDE_ENV_FILE`; Sonnet allowed in the model reminder (Q12). |

**`.claude/settings.json` does not change.** `/system` is a user prompt, so it goes through the UserPromptSubmit
hook that is already registered (`approve_token.py`, the same one as `/approve`); SessionStart and PreToolUse are
already registered for `session_start.py` and `guard.py`; `CLAUDE_ENV_FILE` is given to SessionStart hooks by Claude
Code itself. There is no `settings.json` in this folder on purpose.

## Install — in `~/Documents/seo-ops`, from your own terminal

1. Look at what changes:

   ```bash
   cd ~/Documents/seo-ops && for f in guard.py approve_token.py session_start.py; do diff -u .claude/hooks/$f hooks-pending/$f; done | less
   ```

2. Copy the three hooks in:

   ```bash
   cp hooks-pending/guard.py hooks-pending/approve_token.py hooks-pending/session_start.py .claude/hooks/
   ```

3. Commit them (the hooks are tracked, so every client worktree gets them on its next `git pull`):

   ```bash
   git add .claude/hooks && git commit -m "Install rewrite 2 hooks (P2, P3, P12)" && git push
   ```

4. Quit and reopen every Claude chat (hooks load at session start).
5. In the main folder, start a chat on Opus and type `/system` — it should answer "system session ready".

To undo: `git checkout HEAD~1 -- .claude/hooks && git commit -m "Revert rewrite 2 hooks"`.
