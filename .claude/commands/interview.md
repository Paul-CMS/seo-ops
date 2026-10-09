---
description: Client interviews (CM-042) — facts (on an evidence-gate block), stories (on a schedule, into the story bank), voice (Voice DNA for the blog author)
argument-hint: <slug> facts <batch>|facts-answers <batch>|stories|stories-answers|voice
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. Use the **expert-interview** skill; it holds the method for all three tracks.

1. `python3 scripts/run.py start <slug> interview --step <facts|facts-answers|stories|stories-answers|voice> [--batch <id>]`
   → note the RUN_ID. Exit 4 → refuse and explain; exit 3 → stop and ask Paul.
2. Do the step:
   - **facts <batch>** — only when the evidence gate blocked a page (CM-041). `python3 scripts/evidence.py questions <slug> --run <RUN_ID> --batch <id>`
     writes the pack from the gaps; edit the wording for the person, never add a question that is not a gap.
     Tell Paul it is ready for him to send — and that he may waive instead (`/approve <slug> evidence:<page> --reason "..."`).
   - **facts-answers <batch>** — save the owner's reply as given in `clients/<slug>/interviews/facts/`, write each
     answer into Brand Guide Section D or the page's facts file, settle each answer once under the key the pack names
     for it (`run.py decision <slug> <RUN_ID> --settle fact:… --by "Client (via Paul)" --text "<answer>"` — the gate
     reads settled answers, so it is never asked again, P4), then `python3 scripts/evidence.py run <slug> --run <RUN_ID> --batch <id>`.
     Tell Paul the Brand Guide changed, so he re-approves it (`/next` gives the line).
   - **stories** — `python3 scripts/interview.py due <slug>` first; one round of 3–5 questions; `status.py mark <slug> story_round --file <round>`.
   - **stories-answers** — transcript → story bank entries; `interview.py check <slug> bank`; `status.py mark <slug> story_bank --file clients/<slug>/interviews/story-bank.md`.
   - **voice** — transcript → `voice-dna-<author>.md`; `interview.py check <slug> voice`; `status.py mark <slug> voice_dna --file <it>`.
3. Nothing goes to the client automatically — Paul sends every question set.
4. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary "..."`.
