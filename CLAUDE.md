# seo-ops — the Coastal Marketing SOP (core)

**Paul decides. The system prepares, checks, logs and stops.** This core is loaded in every session; the procedure
lives in `docs/` — `docs/stage-<n>-*.md` for the stage you are in (`run.py start` prints it), `docs/reference.md`
for gates, Drive, money, files and talking to Paul, `docs/system.md` for changing seo-ops. Every term (client/public
fact, evidence pack, usage tier, finding, Fix · Fix and list · Ask, section, review sheet …) is defined once, in
`methodology/definitions.md` (CM-061 — evidence first, decide by default).

## Safety
- Never read, print, search or commit `.env`. Credentials are typed by Paul; scripts load them.
- Nothing goes to a client automatically — Paul sends. The system never publishes; WordPress gets drafts only.
- DataforSEO only through `scripts/dfs.py`/`crawl.py`: estimate the whole run first; over $2 → ask Paul.
- Never delete; always redirect (redirects are VA handoffs). Check the live value before every change.
- status.json, log.md, changes.jsonl, flags.jsonl and the generated records change only through scripts.

## Every session
- Client work runs in the client's own folder (`python3 scripts/worktree.py open <slug>`), one chat per client,
  one session per stage, on the stage's model (stage chats: Haiku). System work runs in `~/Documents/seo-ops`: Sonnet to build a written spec, Opus only when Paul says it is design work
  (one models table: `gates.json` → `models`).
- Start with `python3 scripts/records.py top <slug>` and `clients/<slug>/decisions-settled.md`; never re-raise
  anything settled. Read only the step's read list (`run.py start` prints it); rules by ID with
  `python3 scripts/rulings.py CM-…` — never `rulings.md` whole. The read list never limits web research for
  public facts.

## The run protocol
1. `python3 scripts/run.py start <slug> <command> [--step S] [--batch B|--page P|--pages all]`.
   Exit 4 → refuse and say what is missing; exit 3 → stop and ask Paul (resume, /verify, /rollback, abort).
   `--dry` is the free dry run: no agent is spawned until it passes. `run.py`/`publish.py` refuse client work in the
   main folder (§00).
   A refusal or failure in a multi-step command stops it and is reported (`scripts/seq.py`); no later step runs and no
   approval runs after a failure.
2. Log every change as it happens (`run.py change`; the scripts log their own). Files reach Drive only via `drive.py`.
3. Decisions: `run.py decision … --text` · settle once `--settle <key>` · ask once `--ask <key>`.
4. `python3 scripts/run.py finish <slug> <RUN_ID> --summary "…" --handoff clients/<slug>/handoffs/run-<RUN_ID>.md
   [--tokens N --cost USD]` — records, Drive copy and the run's one commit of this client's folder.

## Facts — answered once
Every fact goes in one way: `run.py fact <slug> <RUN_ID> --id … --value … --status … --source …`, the moment Paul or
the client answers (`facts.py get <slug> --ids …` to read). Brand Guide fact rows are generated. Before a question
set reaches Paul: `settled.py filter` (drops what is answered) and `questions.py check` (a public fact is looked up,
never asked; a client question carries its `searched:` line). Never invent a fact — write `[NEED: …]` (CM-016).

## Decisions are Paul's
Gates are set only by Paul typing `/approve` (a hook issues the token). At a decision: open choices first; print the
`/approve` line only when nothing is open. Changes sent with an `/approve` line are a revision, not an approval.

## Never change the workflow in a client session
Scripts, gates, methodology, specs, CLAUDE.md, docs, agents, commands, skills, templates, tests and config change
only in a system session (Paul types `/system`). Otherwise flag it and carry on:
`python3 scripts/run.py flag <slug> <RUN_ID> --text "…" --workaround "…"`. After every system change:
`python3 tests/run_all.py` (fast, under a minute); before every system commit `--full`; never commit a failing change.
