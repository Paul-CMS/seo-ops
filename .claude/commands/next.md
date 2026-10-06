---
description: Do whatever comes next for a client, and stop at the next decision
argument-hint: <slug>
---

Arguments: $ARGUMENTS

0. **Only when Paul typed this `/next` himself** (not when you loop back in step 2): `python3 scripts/next.py <slug> --continue`
   — it clears a review pause and logs that Paul continued. Never pass `--continue` anywhere else.
1. `python3 scripts/next.py <slug>` — it prints `{"kind", "command", "why"}`.
2. **kind = run:** say in one line what you are about to run and why, then carry out that
   command exactly as its own file in `.claude/commands/` describes (all its gates, logging and
   stops apply). When it finishes, go back to step 1.
3. **kind = decision:** stop. Tell Paul in plain language what is ready, then print the `command`
   exactly as given — it is the `/approve` line to type, with the files it covers. If it ends in
   `--sem <…>`, say he lists the SEM items to apply from the table (e.g. `1,3,4`) or `none`; if it has `<who reviewed it>` /
   `<name, licence>`, say he fills those in. Never type it yourself.
4. **kind = review:** stop (CM-044). The stage that just finished is in review mode: tell Paul what it produced
   (the files, the result) and that `/next` continues. A stage Paul has switched to auto never pauses; a
   decision is never auto.
5. **kind = wait:** stop. Say who or what it is waiting on (client, VA handoff, unfinished run).
6. Also stop whenever the command you are running stops for Paul (cost confirmation, outline
   check, a STOP from a script). Never run more than one paid step without Paul seeing the cost.

The specific commands (`/discovery`, `/crawl`, `/build`, …) stay available for manual use.
