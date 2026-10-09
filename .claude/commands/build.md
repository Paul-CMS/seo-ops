---
description: Agent 2 — technical blockers, site plan, pilot, then service/location batches (briefs, drafts, semantic review, write-back)
argument-hint: <slug> [blockers|plan|brief <id>|draft <id> <page>|batch <id> [drafts|apply-sem]|pilot-corrections|ship <id>|handoff|published <id>] [--route A|B]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §5. If no step is given, use `python3 scripts/next.py <slug>`.

Steps: `blockers` · `plan` · `brief` (`--batch <id>`; ONE run for the batch: the evidence gate per page, then every cleared page's brief, CM-054) · `draft` (`--batch <id> --page <id>`; one page per run, CM-043) · `drafts` (`--batch <id>`; the batch review: every draft side by side + the semantic review table) · `apply-sem` (`--batch <id>`, only when Paul picked SEM items) · `pilot-corrections` · `ship` (`--batch <id>`; WordPress drafts only) · `handoff` (once every page is drafted: one living publish handoff, CM-055) · `published` (`--batch <id>`; after Jonie returns the worksheet). `evidence` (`--batch <id>`) re-runs the gate alone.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps build` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> build --step <step> [--batch <id>|--page <id>]` → note the RUN_ID and pass it
   literally to every later step. Exit 4 → refuse and explain; exit 3 → stop and ask Paul.
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

Drafts reach WordPress only through `/build <slug> ship <id>` — always as WordPress drafts, and the next batch goes
straight on: nothing waits on Jonie or on the technical blockers (CM-055). When every page is a draft,
`/build <slug> handoff` (`publish.py handoff <slug> --run <RUN_ID>`) writes the one living publish handoff; each
`/build <slug> published <id>` ingests her worksheet, verifies, and updates that same document.
