---
description: Paul only — start a system session (changing seo-ops itself). Claude cannot invoke this.
argument-hint: [what this session is for]
disable-model-invocation: true
---

Paul typed: /system $ARGUMENTS

The UserPromptSubmit hook has just issued the system token for this session (rewrite 2 P3). Only this session may
now change the system files; every client session still cannot.

1. `python3 scripts/changereq.py session` — confirm it says "system session: yes". If it says no, tell Paul in plain
   words (the hooks may not be installed — `hooks-pending/INSTALL.md` — or this Mac has `can_change_system: false`)
   and stop.
2. A system session runs on **Opus** and does no client work. Start in the main folder (`~/Documents/seo-ops`, branch
   `main`), never in a client worktree.
3. Do what Paul asked ($ARGUMENTS). If he named nothing, offer `/system-review`.
4. After **every** change: `python3 tests/run_all.py`. Never commit a failing change; every new behaviour gets a new
   check. One commit per item, with the item or CR ID in the message; then `changereq.py done <CR-###> --sha <sha>`
   for a change request that was built.
