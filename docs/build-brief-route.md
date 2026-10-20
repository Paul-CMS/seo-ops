# The brief route — only for sections whose briefs were approved before Rewrite 4

_Reference for `.claude/agents/build.md`. A section is on this route only when `status.py show` lists it with
`route briefs` (Rewrite 4, D5: its briefs were approved or under way when the outline route arrived — e.g. HMM's
pilot and services). Every other section is on the outline route (build.md → "Step: write")._

## Step: brief <id> — every cleared page's brief (Route A) or sanity check (Route B)
After the evidence gate (build.md → "The evidence gate"), one file per page from the approved site plan; skip blocked
pages. The brief (`SB/LB/LBCH/HB/AB - <subject> - <Client>`): assigned variants, page type, target, final URL, sibling
context (C1/C2/C3, the briefs already written in this batch, every page approved in earlier batches), facts from the
pack (nothing Unknown/Disputed), customer language (I — words only, CM-027), the H1 decision, the audit findings and
failed spec checks for this page, the spec's element order, the PAA and fan-out questions routed to it. **If the gate
warned, the brief has an `## Evidence gaps` section**; `status.py page-stage` refuses the brief without it.
`status.py page-stage <slug> <page> --stage brief --file <brief> --run <RUN_ID>` for each page; the last one collects
the batch's briefs for Paul's one approval.
**Route B:** Paul's finished content is checked against `writing-commercial.md` and the Brand Guide — list issues per
page, never rewrite his copy.

## The pilot on this route
One line approves its briefs and drafts and switches later briefs to auto:
`/approve <slug> batch:pilot:briefs batch:pilot:drafts mode:build:brief=auto`; then pilot corrections. If Paul keeps
briefs in review after the pilot, a batch falls back to `brief` (one run) → his briefs approval → `draft` per page.

## Step: draft <id> <page>
As build.md → "Writing one page", from the approved brief instead of the outline.

## Step: batch <id> drafts — a batch under way with a semantic review table (before CM-061)
Read every draft in the batch. Check it against itself and earlier batches (portability E1, opening-angle reuse,
FAQ/heading collisions). Stage 4 semantic review — one table for the batch, report only:
`<Client> - Semantic Review - <batch> - REVIEW.md` in `clients/<slug>/build/`. `status.py batch <slug> <id> --state
drafts_written --sem-table <table> --sem-findings <rows>`. Paul approves both at once: `/approve <slug>
batch:<id>:drafts --sem 1,3,4` (or `--sem none`; none at all when nothing was found).

## Step: batch <id> apply-sem   (only when Paul picked SEM items)
Apply only the picked items (status.json → the batch's `drafts.sem_ids`); re-run E1–E10 and the spec checks on every
changed section. All pass → `status.py batch <slug> <id> --state sem_applied --files <drafts> --checks-passed`. Any
fails → `--state sem_check_failed --files <drafts> --note "<check, page>"` (back to Paul).

## Step: writeback <id>   (once per section, at the brief approval — CM-061 §6)
After the briefs are approved (or accepted, briefs on auto): each page's row in B3, the variants its brief assigns in
C1/C2, every H2 and FAQ in C3, the fact rows regenerated (`records.py render`), the Drive copy (`drive.py upload`),
then `status.py writeback <slug> <id> --run <RUN_ID>`.
