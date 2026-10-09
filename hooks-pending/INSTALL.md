# Pending hooks — Paul installs them

Claude may not edit `.claude/hooks/` or `.claude/settings.json` (the guard blocks it). Hook changes are written
here, `tests/run_all.py` runs the suite against these files, and Paul installs them by copying them in from his own
terminal, in `~/Documents/seo-ops`:

```bash
cp hooks-pending/*.py .claude/hooks/ && { [ ! -f hooks-pending/settings.json ] || cp hooks-pending/settings.json .claude/settings.json; }
```

Then restart the chat (hooks load at session start). After installing, this folder may be emptied in a system
session; the tests use `.claude/hooks/` when it is empty.

## Rewrite 2 (2026-10-09)

- **P3** `guard.py`: system files (scripts, methodology, CLAUDE.md, agents, commands, skills, templates, tests,
  docs, hooks-pending, config.json) change only in a session where Paul typed `/system`. `change-requests.md` and
  `clients/*/flags.jsonl` are append-only, scripts only.
- **P3** `approve_token.py`: `/system` writes the one-time system token for that session (refused on a VA Mac,
  `machine.json can_change_system: false`).
