---
description: Do whatever comes next for a client, and stop at the next decision
argument-hint: <slug>
---

Arguments: $ARGUMENTS

0. **Only when Paul typed this `/next` himself** (not when you loop back in step 2): `python3 scripts/next.py <slug> --continue`
   — it clears a review pause and logs that Paul continued. Never pass `--continue` anywhere else.
1. `python3 scripts/next.py <slug>` — it prints `{"kind", "command", "why", "stage", "session_model", "agents"}`.
   Start every reply with the stage line, e.g. **Stage 5 of 8 — Build plan and blockers · session: Haiku · agents:
   build (Opus), clerk (Haiku)**. Judgment work goes to the named Opus agent; mechanical work to `clerk`. Relay an
   agent's `clients/<slug>/handoffs/run-<RUN_ID>.summary.md` as written — don't re-explain history.
2. **kind = run:** say in one line what you are about to run and why, then carry out that
   command exactly as its own file in `.claude/commands/` describes (all its gates, logging and
   stops apply). When it finishes, go back to step 1.
3. **kind = decision:** stop. Present it in two clearly separate parts:
   - **Open choices first.** List every choice still open in what Paul would approve (alternatives offered,
     questions marked Paul, a default you picked for him), each with the options. If there are any, end there:
     ask him to answer them, say the files will be revised first, and **do not print the `/approve` line yet**.
   - **Ready to approve** — only when nothing is open (or after his answers have been applied in a revision run).
     Say what he is approving and what changes once he does, then print the `command` exactly as given — it is
     the `/approve` line to type, with the files it covers. Say plainly: "If you want any change, tell me instead —
     don't type /approve with changes attached; I revise the files first and you approve the new version."
   If Paul sends changes together with an `/approve` line, it is not an approval: apply the changes in a revision
   run and come back to step 3. If it ends in
   `--sem <…>`, say he lists the SEM items to apply from the table (e.g. `1,3,4`) or `none`; if it has `<who reviewed it>` /
   `<name, licence>`, say he fills those in. Never type it yourself.
4. **kind = review:** stop (CM-044). The stage that just finished is in review mode: tell Paul what it produced
   (the files, the result) and that `/next` continues. A stage Paul has switched to auto never pauses; a
   decision is never auto.
5. **kind = wait:** stop. Say who or what it is waiting on (client, VA handoff, unfinished run).
6. Also stop whenever the command you are running stops for Paul (cost confirmation, outline
   check, a STOP from a script). Never run more than one paid step without Paul seeing the cost.

The specific commands (`/discovery`, `/crawl`, `/build`, …) stay available for manual use.
