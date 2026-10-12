---
description: Paul only — start a system session (changing seo-ops itself). Claude cannot invoke this.
argument-hint: [what this session is for]
disable-model-invocation: true
---

Paul typed: /system $ARGUMENTS

The UserPromptSubmit hook has just issued the system token for this session (rewrite 2 P3). Only this session may
now change the system files; every client session still cannot.

1. `python3 scripts/changereq.py start` — it refuses unless this is a system session, in the main folder
   (`~/Documents/seo-ops`, branch `main`, never a client worktree), with **no uncommitted changes**; then it brings
   main in step with GitHub (fast-forward; push this Mac's unpushed commits; when both moved, rebase on its own only if
   this Mac's commits touch system files alone and GitHub's touch `clients/` alone, then the fast tier must pass and it
   pushes — anything else it shows you both sides). On a refusal, tell Paul in plain words what it said (the hooks may not be installed —
   `.claude/hooks/` and `.claude/settings.json` — this Mac may have `can_change_system: false`, or the folder has changes) and stop.
2. A system session runs on **Opus** and does no client work.
3. Do what Paul asked ($ARGUMENTS). If he named nothing, offer `/system-review`.
4. After **every** change: `python3 tests/run_all.py` (fast); before every commit `python3 tests/run_all.py --full`. Never commit a failing change; every new behaviour gets a new
   check. Commit only when the test output's last line says `0 failed`. One commit per item, with the item or CR ID in
   the message; **push it at once** with `python3 scripts/changereq.py push` — exit 5 means the push failed: tell Paul
   plainly that the commit is only on this Mac and stop. Then `changereq.py done <CR-###> --sha <sha>` for a change
   request that was built (it refuses a commit that is not on GitHub).
