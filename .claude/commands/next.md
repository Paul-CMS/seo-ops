---
description: Do whatever comes next for a client, and stop at the next decision
argument-hint: <slug>
---

Arguments: $ARGUMENTS

0. **Only when Paul typed this `/next` himself** (not when you loop back in step 2): `python3 scripts/next.py <slug> --continue`
   — it clears a review pause and logs that Paul continued. Never pass `--continue` anywhere else.
1. `python3 scripts/records.py top <slug>` — print its four lines first (stage, what is happening now, waiting on,
   next action); never re-explain history. Then `python3 scripts/next.py <slug>` — it prints `{"kind", "command", "why", "stage", "session_model", "agents"}`.
   **`paul_said`** in that JSON (CM-067): what Paul asked in an earlier chat that it could not do. Do it first, as
   he said it — never ask it again — then `python3 scripts/next.py <slug> --carried`.
   Start every reply with the stage line, e.g. **Stage 5 of 8 — Build plan and blockers · session: Haiku · agents:
   build (Opus), researcher (Sonnet)**. Judgment work goes to the named agent; mechanical work is a script you run yourself (never an agent). Relay an
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
   End every decision stop with the record's `sitting` line, word for word (P12).
   If Paul sends changes together with an `/approve` line, it is not an approval: apply the changes in a revision
   run and come back to step 3. If it ends in
   `--sem <…>`, say he lists the SEM items to apply from the table (e.g. `1,3,4`) or `none`; if it has `<who reviewed it>` /
   `<name, licence>`, say he fills those in. Never type it yourself.
4. **kind = review:** stop (CM-044). The stage that just finished is in review mode: tell Paul what it produced
   (the files, the result) and that `/next` continues. A stage Paul has switched to auto never pauses; a
   decision is never auto.
5. **kind = new_session:** stop (R2). First, if Paul asked for something this chat cannot now do (an approval he
   gave in words, "push them to WordPress"), hand his words on: `python3 scripts/next.py <slug> --carry "<his words>"`
   (CM-067) — the next chat starts with them. Then say: "Stage <x> is done in this session. Open a new chat on <Model> in
   the client's folder (`python3 scripts/worktree.py open <slug>`) and type `/next <slug>`." Never try to run the step here — `run.py start` refuses it.
6. **kind = wait:** stop. Say who or what it is waiting on (client, VA handoff, unfinished run). This comes only
   when nothing else can run (P8).
   **`waits`** (any kind): open waits that do **not** block the next action. List them one line each under
   "Waiting on (not blocking)" and carry on. A VA handoff never stops writing.
**A draft changes only inside a run (CM-067).** When Paul asks for a change to drafts already recorded — fill a gap,
use his text, reword a line — open `python3 scripts/run.py start <slug> build --step revise --batch <id>` (any chat),
make the change, log it (`run.py change`), and record each changed page again: `status.py page-stage <slug> <page>
--stage draft --file <f> --run <RUN_ID>`. Never edit a draft with a one-off script outside a run: the approval then
refuses every page.
**Every answer is recorded the moment Paul gives it (P4, Q3) — by you, never an agent (CM-065).** When Paul's message is
answers only (facts, "mark them unknown", "confirmed from a Google review", a choice), open the any-stage `answers` run
yourself — `python3 scripts/run.py start <slug> answers` (allowed in any chat, even one whose stage is done) — record each
answer with the scripts below, write a 3-line handoff and `run.py finish`. No Opus agent for this. A fact — from Paul, the client, a returned sheet, an
interview or an email — goes in with `python3 scripts/run.py fact <slug> <RUN_ID> --id <fact id> --value "…" --status
paul_approved|client_confirmed|… --source "…"` (`facts.py list <slug>` shows the ids; a new fact adds `--label`). A
decision goes in with `run.py decision … --settle <key>`. Before any question set reaches Paul:
`python3 scripts/settled.py filter <slug> <questions.json>` — it drops what is already answered and names it in one line.
   **Quiet runs (§6.3):** never read command files, CLAUDE.md or agent files mid-run — they are loaded once; read
   STATUS.md and run summaries only. Relay an agent's reply (at most 15 lines) as it is.
   **Agents (F-008/F-009/F-010):** wait for an agent's one report (its summary file); never relay interim status or the
   same hand-back twice. A refusal or failure in a sequence of steps stops it: report the refusal as it is, run no
   later step, and run no approval after it.
7. Also stop whenever the command you are running stops for Paul (cost confirmation, outline
   check, a STOP from a script). Never run more than one paid step without Paul seeing the cost.

The specific commands (`/discovery`, `/crawl`, `/build`, …) stay available for manual use.
