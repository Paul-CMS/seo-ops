# Changing seo-ops — the system session

**Only Paul changes the workflow (Q2).** The system files — `scripts/**` (incl. `gates.json`), `methodology/**`,
`CLAUDE.md`, `docs/**`, `.claude/agents|commands|skills/**`, `templates/**`, `tests/**`,
`config.json` — change only in a **system session**: Paul types `/system` (a hook issues a one-time system token for
that session; the guard blocks every other session; a VA Mac, `machine.json can_change_system: false`, never gets
one). A system session runs on **Opus**, in the main folder (`~/Documents/seo-ops`, branch `main`), and does no
client work. `/system` begins with `changereq.py start`: it refuses on uncommitted changes, then syncs main with GitHub (fast-forward; push unpushed commits; auto-rebase only when this Mac's commits are system-only and GitHub's are `clients/`-only, fast tier passed — otherwise it stops and shows both sides).

## The inbox
In a client session nobody changes the workflow — they flag it: `python3 scripts/run.py flag <slug> <RUN_ID> --text
"…" [--workaround "…"]`. The run continues on the current rules; the flag shows in the client's STATUS.md under
"Flagged for Paul (system)". **`/system-review`** collects every flag into `methodology/change-requests.md` (CR-###,
the one inbox, append-only, `scripts/changereq.py`) and lists every OPEN item; Paul answers each: accept, reject or
edit. Accepted items are built in that session → tests → commit (CR ID in the message) → `changereq.py push` (at once; exit 5 = the push failed: say so and stop) → `changereq.py done <CR> --sha`.
A ruling becomes a numbered entry in `methodology/rulings.md` (PROC-01), never a silent edit.

## Test first
After **every** change: `python3 tests/run_all.py` (the fast tier, under a minute). **Before every system commit:** `python3 tests/run_all.py --full` (every scenario incl. the end-to-end walkthroughs, 10–15 minutes — run it in the background; fake WordPress, fake DataforSEO, fake web, a
throwaway copy of the repo — no network, no cost, no client data; run it in the background). **Never commit a change
that fails it.** A new behaviour gets a new check (`tests/run_all.py` or `tests/checks/*.py`). One commit per item.

## Hooks
The guard keeps Claude out of `.claude/hooks/` and `.claude/settings.json`; the tests run the installed hooks (the
sandbox copies `.claude/`). A hook change is Paul's: Claude writes the proposed change in the chat (or a scratch file
outside the repo); Paul applies it to `.claude/hooks/` from his own terminal, commits it, and reopens every chat.

## Client migrations
A change that touches client records ships with a migration (`scripts/migrate2.py`): a dry run first that lists every
approval before and after; it refuses if one would be lost; one MIGRATION line per client in its log.md.

## What is generated (never edit by hand)
`decisions.md`, `decisions-settled.md`, `STATUS.md`, `handoff-log.md`, `document-checklist.md`, `approval-record.md`,
the Brand Guide's Section A/D fact rows (from `facts.json`), `handoffs/VA-WORKLIST.*` — all by `scripts/records.py`.
