# Build — the agent's procedure for the write run and after

_Phase 7 (2026-10-21): moved here from `.claude/agents/build.md`; read only by the steps that run it (build:evidence, write, review, writeback, ship, handoff, published — gates.json read lists), never by a page writer. Stage overview: `docs/stage-6-build.md`._

**The evidence gate** (inside every write run, CM-041) — each page's facts go to `build/evidence/<page>.facts.json` (only
from the returned proof sheet, the Discovery Record, Brand Guide E and cited public research; never upgrade a status).
`evidence.py run <slug> --run <RUN_ID> --batch <id>` scores each page and rebuilds its evidence pack
(`build/<section>/packs/<page>.md`). The **researcher** checks by meaning every review topic marked "keyword match only"
with 3+ reviewers (`reviews.py meaning`, else `reviews.py checked …`), and writes the **industry standard** for every
page whose service scope or process is a client gap (researcher job 5, CM-068 — then `evidence.py run` again: a filled
gap is not a hold, so no waiver is needed for it), then `evidence_pack.py build <slug> <id> --run <RUN_ID>`; FAQ picks:
`outline.py faq <slug> <id> --run <RUN_ID>`. A blocked page is not written. Each page that used a standard fill is
listed in `clients/<slug>/later-rewrites.md` (the client's answer replaces it, CM-066 Updated line).

**write <id>** — the whole section in ONE run, ONE stop (outline route):
1. The evidence gate.
2. `outline.py build <slug> <id> --run <RUN_ID>` — one outline per cleared page, by script. Never edit an outline; if it is
   wrong, flag it.
3. **One fresh subagent per page**, all in one message (CM-043): always `draft-writer` (CM-065: four tools, a small
   context — never `build`), started with the Agent tool's `model` set to the drafts model in the run's models line
   (Opus; Sonnet after Paul's `model:build:draft=sonnet`). Each writes one page ("Writing one page" in build.md), then is recorded:
   `status.py page-stage <slug> <page> --stage draft --file <f> --run <RUN_ID> --agent <its id>`.
4. **The review** (below) in the same run → `status.py batch <slug> <id> --state drafts_written --review-sheet
   build/<id>/drafts-review.csv`.
5. No Ask rows → `review.py apply`, record every page again, the write-back, stop at the approval line. Ask rows → stop;
   Paul answers, `/build <slug> review <id> drafts "<his line>"` applies and records, the write-back follows.

**The review** — one checker pass for the section (CM-061): E1–E10, the spec's checks, portability and the swap test across
siblings (`similarity.py` in `review.py`), heading/FAQ collisions with C3 and each other, Stage 4 semantics, the usage
tiers, and every industry-standard fill (CM-068): it reads as trade practice, matches its cited statement, and claims
nothing for the client — else a Fix. One JSON finding per page + rule + item, severity per `methodology/review-severities.json` and definitions.md;
every value a writer chose that neither the plan nor `outline.py`'s formula fixed is one Fix and list row per page.
`review.py sheet <slug> <id> drafts --findings <findings.json> --run <RUN_ID>` writes the one sheet (`drive.py upload` it).
Overdue Asks: `review.py overdue <slug> --run <RUN_ID> --apply`. The approval: `/approve <slug> batch:<id>:drafts`
(`--review` / `--practitioner` per CM-025).

**writeback <id>** — once per section, before the drafts approval: from the reviewed drafts each page's row in B3, the
variants in C1/C2, every H2 and FAQ in C3, fact rows regenerated (`records.py render`), the Drive copy; then
`status.py writeback <slug> <id> --run <RUN_ID>` (it refuses before the review is applied, and a second time).
Drafts, the draft review and ship never write the Brand Guide — only this step.

**ship** — `publish.py wheel <slug>`; `publish.py drafts <slug> --run <RUN_ID> --all` — every approved page as a WordPress
**draft** from its approved file. Menu changes: `handoff.py create … --kind navigation`. No Brand Guide write-back here. Never edit a generated draft —
change the approved file (Paul re-approves) and regenerate.

**handoff** — `publish.py handoff <slug> --run <RUN_ID>`: `qa.py` (an error refuses: fix the plan or the approved file),
`schema.py` (an unmet asset gate refuses and lists Section F's gaps; Wikipedia down → CM-053), then one living publish
handoff to Jonie (never change wording; 301s and the schema under each row); `drive.py upload … --to "02 - Build"`.

**published <id>** — `handoff.py ingest … --returned <csv>`; `verify.py <slug> --run <RUN_ID> --batch <id>` — every
difference goes to Paul (a corrections handoff, `--state corrections_requested`). All match → alt text (`wp.py set-alt …
--live --backup-confirmed "…"` after Paul's fresh backup yes); `--state published`, `verified`, `written_back`;
`publish.py pending`.
