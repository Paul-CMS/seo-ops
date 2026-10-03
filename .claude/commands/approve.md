---
description: Paul only — set a gate or approve a page. Claude cannot invoke this.
argument-hint: <slug> <gate|page:<id>|import> [decision] [conditions / note / reviewer]
disable-model-invocation: true
---

Paul typed: /approve $ARGUMENTS

This is Paul's decision, not yours. Do not add, soften or second-guess it.

1. Parse: client slug, target (a gate from `scripts/gates.json`, `page:<id>`, or `import`),
   decision (default `approved`; also approved_with_conditions, revise, deferred, rejected,
   blocked), conditions (`;`-separated), note.
2. Files: every approval names the exact file versions it covers. Use the `--files` Paul typed;
   if he typed none, approve.py uses the files the producing step recorded (`status.py mark`) and
   refuses if there are none. For `page:<id>`, the draft file. For `batch:<id>:drafts`, pass Paul's
   `--sem` (the SEM items he picked, e.g. `1,3,4`, or `none`). If you are unsure, ask Paul before running anything.
3. Sensitive client and `page:<id>`: ask Paul who reviewed the content if he didn't say
   (`--review`). Medical/chiropractic: ask for the licensed practitioner's name and licence
   (`--practitioner`). Never fill these in yourself.
4. Run exactly one:
   - `python3 scripts/approve.py <slug> <gate> --decision <d> [--conditions "..."] [--files f1,f2] [--note "..."]`
   - `python3 scripts/approve.py <slug> batch:<id>:briefs|drafts --decision <d> [--files ...] [--sem 1,3,4|none] [--review ...] [--practitioner ...]`
   - `python3 scripts/approve.py <slug> page:<id> --decision <d> --file <f> [--review "..."] [--practitioner "..."]`
   - `python3 scripts/approve.py <slug> import --proposal clients/<slug>/import-proposal.json`
   It refuses unless this /approve came from Paul in the last 20 minutes, and it refuses gates
   whose earlier gates are not met. If it refuses because the token expired or was used, ask
   Paul to type /approve again — never try to work around it.
5. Mirror the Approval Record to Drive: `python3 scripts/status.py approval-record <slug>` →
   update `[Client] - Approval Record.md` in the client folder. If a deliverable was approved,
   save the Drive copy with status `APPROVED` (a new file; the REVIEW file moves to `_Archive/`
   only if Paul agrees).
6. Tell Paul in one or two sentences what this unlocks and the next command.
