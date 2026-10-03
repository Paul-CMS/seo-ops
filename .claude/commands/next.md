---
description: Do whatever comes next for a client, and stop at the next decision
argument-hint: <slug>
---

Arguments: $ARGUMENTS

1. `python3 scripts/next.py <slug>` — it prints `{"kind", "command", "why"}`.
2. **kind = run:** say in one line what you are about to run and why, then carry out that
   command exactly as its own file in `.claude/commands/` describes (all its gates, logging and
   stops apply). When it finishes, go back to step 1.
3. **kind = decision:** stop. Tell Paul in plain language what is ready, then print the `command`
   exactly as given — it is the `/approve` line to type, with the files it covers. If it ends in
   `--sem <…>`, say he lists the SEM items to apply from the table (e.g. `1,3,4`) or `none`; if it has `<who reviewed it>` /
   `<name, licence>`, say he fills those in. Never type it yourself.
4. **kind = wait:** stop. Say who or what it is waiting on (client, VA handoff, unfinished run).
5. Also stop whenever the command you are running stops for Paul (cost confirmation, outline
   check, a STOP from a script). Never run more than one paid step without Paul seeing the cost.

The specific commands (`/discovery`, `/crawl`, `/build`, …) stay available for manual use.
