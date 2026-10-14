---
description: Agent 2 — technical blockers, site plan, pilot, then service/location batches (briefs, drafts, semantic review, write-back)
argument-hint: <slug> [blockers|plan|brief <id>|draft <id> <page>|batch <id> [drafts|apply-sem]|pilot-corrections|ship <id>|handoff|published <id>] [--route A|B]
---

Arguments: $ARGUMENTS

Follow `docs/stage-5-build-plan.md` and `docs/stage-6-build.md`. If no step is given, use `python3 scripts/next.py <slug>`.

Steps: `blockers` · `plan` · `facts` (P10: ONE facts round for every page — grids, the researcher, reviews, one question set grouped by fact) · `write` (`--batch <id>`; P10: briefs, one fresh subagent per page for its draft (`--agent`), then the batch review — ONE run, ONE stop) · `brief` (`--batch <id>`; ONE run for the batch: the evidence gate per page, then every cleared page's brief, CM-054) · `draft` (`--batch <id> --page <id>`; one page per run, CM-043) · `drafts` (`--batch <id>`; a batch already under way: the batch review with the semantic review table) · `review` (`/build <slug> review <section> <briefs|drafts> "<Paul's answer line>"`; CM-061: `review.py apply` records his answers to the section's one review sheet — an empty answer takes the recommended option — and every item is applied to every page in this one run; then the approval line. With no answer line, for a section written before CM-061: the evidence packs are rebuilt (`evidence.py run`), the one checker pass runs over the section's briefs or drafts and `review.py sheet` writes the sheet — Paul sees only its Ask rows and the evidence-used lines) · `apply-sem` (`--batch <id>`, a batch already under way, only when Paul picked SEM items) · `pilot-corrections` · `writeback` (`--batch <id>`; CM-061: the section's ONE Brand Guide write-back, at its brief approval — drafts and ship never write it) · `ship` (no batch: every approved service and location page as a WordPress draft in ONE run, P9) · `handoff` (once every service and location page is drafted: the VA Worklist handover — sections 3 Redirects, 4 Publish, 5 After publish, P9) · `published` (`--batch <id>`; after Jonie returns the worksheet). `evidence` (`--batch <id>`) re-runs the gate alone.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps build` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> build --step <step> [--batch <id>|--page <id>]` → note the RUN_ID and pass it
   literally to every later step. Exit 4 → refuse and explain; exit 3 → stop and ask Paul. (§6.3: `run.py start … --dry`
   is the free dry run — it checks gates, model, session and folder and records nothing; no agent is spawned until
   `start` has passed. Scripts print at most about 10 lines; agents reply in at most 15.)
2. Route: `--route`, else status.json `client.route`, else ask Paul (A = the system writes,
   B = Paul provides finished content).
3. Use a **fresh build subagent** for every run, with slug, RUN_ID, the step, the route and (for `draft`) the one page.
   `brief` is one subagent for the whole batch (CM-054); `draft` never hands one subagent two pages (CM-043).
4. Stop at each decision and give Paul the exact line from `python3 scripts/next.py <slug>`:
   site plan · evidence block (facts interview or waiver) · briefs · drafts with SEM picks (+ `--review` for sensitive
   clients, `--practitioner` for health) · After the pilot, Paul may switch `build:brief` to auto (`/approve <slug> mode:build:brief=auto`): later batches
   then stop for the drafts only. "Blockers cleared" (Jonie's handoff done and verified) and `pages_built` (every
   batch written back) are conditions the system meets — no approval.
5. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary "..."`.

Drafts reach WordPress only through `/build <slug> ship` — one run for every approved service and location page,
always as WordPress drafts; nothing waits on Jonie or on the technical blockers (CM-055, P8). Every VA item is one
row of the client's **VA Worklist** (`handoffs/VA-WORKLIST.md` / `.csv`, copied to Drive): Setup, Blockers and
Manual lookups go to the VA at any time; Redirects, Publish and After publish are handed over once, by
`/build <slug> handoff`. Each `/build <slug> published <id>` ingests the returned worklist, verifies, and the
worklist shows the ticks.
