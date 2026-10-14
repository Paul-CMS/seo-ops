# Pending hook — Paul installs it

Claude may not edit `.claude/hooks/` or `.claude/settings.json` (the guard blocks it). Hook changes are written here and
Paul installs them from his own terminal.

## What changes (rewrite 3, 2026-10-14)

| File | Change |
|---|---|
| `session_start.py` | The model reminder said system sessions run on Opus. It now says: client stage chats **Haiku**; a system session implementing a written spec **Sonnet**; a system session deciding design **Opus**, only when Paul says so. It also says client work runs only in the client's own folder, never in `~/Documents/seo-ops` (§00). Nothing else changes — the session recording, `CLAUDE_ENV_FILE` and the unknown-model warning are as before. |

`.claude/settings.json` does not change (SessionStart is already registered for `session_start.py`). No test depends on
the reminder's wording.

## Install — in `~/Documents/seo-ops`, from your own terminal

1. Look at what changes:

   ```bash
   cd ~/Documents/seo-ops && diff -u .claude/hooks/session_start.py hooks-pending/session_start.py
   ```

2. Copy it in:

   ```bash
   cp hooks-pending/session_start.py .claude/hooks/session_start.py
   ```

3. Check the suite still passes, then commit and push (the hook is tracked, so every client worktree gets it on its next `git pull`):

   ```bash
   python3 tests/run_all.py && git add .claude/hooks && git commit -m "Install the rewrite 3 session-start reminder (Sonnet for specs, Opus for design)" && git push
   ```

4. Quit and reopen every Claude chat (hooks load at session start). A new chat's first message should show the new reminder.
5. Remove this folder once installed: `git rm -r hooks-pending && git commit -m "Remove hooks-pending" && git push`.
