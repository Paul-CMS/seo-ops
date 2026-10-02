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
2. Files: for a gate, the approval names the exact file versions being approved — use the
   deliverables the agent named when it asked for this approval (show them). For `page:<id>`,
   the draft file. If you are unsure which files, ask Paul before running anything.
3. Sensitive client and `page:<id>`: ask Paul who reviewed the content if he didn't say
   (`--review`). Medical/chiropractic: ask for the licensed practitioner's name and licence
   (`--practitioner`). Never fill these in yourself.
4. Run exactly one:
   - `python3 scripts/approve.py <slug> <gate> --decision <d> [--conditions "..."] [--files f1,f2] [--note "..."]`
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
