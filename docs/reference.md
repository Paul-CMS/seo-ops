# seo-ops reference — gates, implementation, methodology, Drive, money, files, talking to Paul

Read the part you need. The stage files (`docs/stage-<n>-*.md`) say what each stage does.

## Decisions and conditions (`scripts/gates.json`)
- **Decisions** — Paul's, set **only by `/approve`** typed by Paul (a hook issues a one-time token; the guard blocks
  direct edits). **Every approval names the exact files it covers** (the producing step records them with `status.py
  mark`); approve.py refuses an approval with no files. If one of those files changes, **only that decision** stops
  counting; `/where` flags later ones "upstream change". Brand Guide sections are fingerprinted on their values only
  (P4): a confirmation, a new source or a date never voids an approval; a changed value does. One `/approve` line may
  approve several decisions (`/approve <slug> a b c`); a decision named in the same line counts for the others'
  prerequisites. Values: `approved` · `approved_with_conditions` · `revise` · `deferred` · `rejected` · `blocked`.
- **Conditions** — facts the scripts check from evidence, never approved, logged the first time they are met:
  `client_setup`, `proof_sheet_returned`, `audit_steps_complete`, `discovery_signed_off`, `blockers_cleared`,
  `page_specs_approved` (global, `/approve global specs`), `pages_drafted` (every service and location page is a
  WordPress draft), `pages_built`, `wordpress_connected`.
- **Review or auto, per stage (CM-044).** Every producing stage is in review (the `/next` loop stops after it) or auto.
  Default review; auto only after the stage passed the pilot, only by Paul (`/approve <slug>|global mode:<stage>=auto`).
  Decisions can never be auto. The pilot's approval line switches `build:brief` to auto (P10).
- **Models (§4, Q12).** `gates.json → models` names the agent and model for each job; `stages.py list` prints them;
  Paul changes one only with `/approve global model:<job>=<model>` (e.g. `model:build:draft=sonnet`, the Sonnet
  drafting test; `build/compare/` holds the side-by-side pages).
- **Global approvals** (`/approve global …`: specs, mode, model) are typed in the main folder only; a client folder
  refuses them and says so. All checks run first, then the system files (spec stamp, `config.json`, the token) are
  written together or not at all. They never write a client's records: each client records the approval on its own
  next `/next`, in its own folder (`config.json → global_approvals`; the client's `global_seen` counter).

## Implementation — what can change, and how
Each change kind's gate, channel and owner are in `gates.json → change_kinds`. Safe fixes after the audit approval;
structural changes (redirects, slugs, titles, H1s) after the entity and Brand Guide approvals, always as handoffs;
page content only as WordPress drafts from approved files; link tables and schema in Finish.
- **The system never publishes.** Every service and location page is made a WordPress **draft** in one ship run (P9):
  exact slug, SEOPress title/meta/keyword/social, content as blocks, link tables complete. A draft with an open
  placeholder carries a visible "Open items on this page" notice and a worklist row (P11).
- **One VA Worklist per client (P9)** — `handoffs/VA-WORKLIST.md` / `.csv` (Drive: "<Client> - VA Worklist"):
  1 Setup · 2 Blockers · 3 Redirects · 4 Publish · 5 After publish · 6 Manual lookups. Sections 1, 2 and 6 go to the VA
  at any time; 3–5 are handed over once, when every service and location page is a draft. The VA returns the CSV;
  `handoff.py ingest <slug> --run R --returned <csv>`; `/verify` checks every done row.
- **WordPress: one spec — `wordpress/wordpress-site-setup.md`** (code `scripts/wp.py`; `/wp-check` first). Any change to
  a published page needs `--live` and Paul's ManageWP backup confirmation.
- **Handoffs go to the owner of the work**: WordPress, technical, redirect, title/meta → Jonie; citations, GBP, content
  review and everything else → Gwen. Redirect rows are `301`, full URLs, never bare slugs. A slug change always comes
  with its redirect; a changed planned URL lists its old URL under `replaces` (P7).
- Destructive candidates follow CM-019. Never delete; always redirect.

## Methodology — what governs
**`methodology/rulings.md` > the Bradley Standard (`sop-source/BB-Standard-v1.0.md`, BB-601–608 replaced by
`BB-Standard-Schema-Section-v1.1.md`) > everything else.** Read rulings by ID (`scripts/rulings.py CM-020 …`);
cite IDs, never restate. Most-used: CM-016 (no invented facts), CM-020 ("The Best" is tested), CM-022 (links in
tables, never prose), CM-024 (variants are a shared pool), CM-041 (evidence gate), CM-043 (one page per context),
CM-057 (reviews as customer-reported facts), CM-058 (metro hubs). URLs: one root slug (BB-207/208, `urlcheck.py`).
Discovery is not the audit. A new conflict is recorded per PROC-01 and flagged.

## Place research (CM-061; `scripts/places.py`)
Research for a town and a niche is done once and reused across clients: `methodology/places/<state>/<place>/place.json`
(niche-free) and `<niche>.json` (place × niche). The first stop for a public fact. The VA runs it: `places.py status
<slug>` lists planned places with no research → `places.py prompt <slug> <place>` → paste into Gemini Deep Research →
save the report to `clients/<slug>/inputs/places/<place>-<niche>.md` → `places.py ingest` → `places.py verify <state>
<place> <niche>` (URLs must load; quotes must be on the page) → the rest are checked by meaning on the Claude API
(`places.py judge-all <state> <place> <niche> --slug <slug> --run <RUN_ID>`, Sonnet); with no API key, or for a fact the
API calls unclear, the researcher (Sonnet) reads it (`places.py judge`). Failed facts are dropped, never asked. Packs use only verified, current (under 3 years) facts.

## Independence
Auditing and writing never share a context (CM-017, CM-018, RULE-011): the audit-reviewer sees only registers and
decisions; content QA in Finish runs in finish-qa, never the build context that wrote the copy. CM-026 is the standing
self-review exception.

## Drive (R8)
One folder per client, `[Client Name] - TMS`, at the root of `v3. CMS Technical SEO Audit 2026` (`drive.py where`).
Never search other Drive folders. Files reach Drive only by `drive.py` (archive-and-replace, logged; nothing deleted).
The only Google Doc the system creates is the proof sheet's client copy (HTML). Names follow
`methodology/naming-convention.md`. Never use the pre-Claude-Code instruction files (`/archive-old-instructions`).

| Artifact | Drive location |
|---|---|
| Evidence | `01 - Discovery and Audit/Evidence/` |
| Discovery Record, Proof Sheet, Finding Register, URL Decision Map, Recommendations, Evidence Manifest | `01 - Discovery and Audit/Deliverables/` |
| Briefs, approved drafts, Technical Blocker Checklist | `02 - Build/` |
| Link Wheel Tables, schema, QA Punch-List | `03 - Finish/` |
| Blog Decision Map, posts, refresh schedule | `04 - Blog/` |
| Brand Guide, Approval Record, Document Checklist, Handoff Log, Status, VA Worklist | client folder root |

## Money and credentials
DataforSEO: whole-run estimate first, over $2 → Paul, more than the balance → stop. Other spend needs Paul's approval
with provider, cost and renewal (RULE-014). Model spend per run: `run.py finish` measures it itself from Claude Code's
transcripts (`scripts/usage.py run|client <slug>`, prices in `scripts/model_prices.json`; `--tokens/--cost` only to override) → STATUS.md "Spend by
stage" and "Spend by step". Credentials: never ask in chat — show `python3 scripts/wp.py env-lines <slug>` and link `[.env](.env)`.

## Per-client files
`status.json` (gates, pages, build) · `log.md` (safety log) · `changes.jsonl` · `snapshots/` · `facts.json` (every fact)
· `flags.jsonl` (workflow flags) · `brand-guide.md` · generated records (see `docs/system.md`) · `discovery/ audit/
build/ finish/ blog/ handoffs/ interviews/` · `data/` (summaries agents read) · `inputs/` (raw, git-ignored).
`status.json → client_view` is the only client-facing part, generated from `methodology/client-phrases.json`.

## Scripts do the clerical work (Rewrite 4 Phase 1)
No clerk agent: the stage chat runs scripts itself. `pipeline.py <slug> inventory` (crawl → pulls → S12; one combined
estimate, `--confirmed`, `--dry`), `render.py` (every Markdown deliverable and STATUS.md from its CSV/JSON; never typed,
never rendered over an approved file), `outline.py` (a keyword, H1 or variant the plan row leaves empty is assigned by
formula). Logs: scripts write the CHANGE/DECISION/FACT/step lines; `run.py finish` adds them to the handoff and refuses an
agent-written handoff over 25 lines (`config.json → handoff_max_lines`).

## VA Worklist (`scripts/worklist.py`; rewrite 3 §7a)
One worklist per client; every row has `id · section · task · where · how · values · depends_on · done_check · owner ·
source · status`. **`worklist.py check <slug>` runs before any handover** (`publish.py handoff` runs it and refuses on an
error; the Drive copy waits for a passing check): publish rows match a real draft and the approved URL, no page missing
or twice; redirects resolve, target a planned page with a draft, no chains, loops or duplicates, and depend on their
target's publish row; open-item notices and rows match; a stale row is marked `worklist.py supersede`, never left open.
**Page decisions** (`pagedec.py`: drop, hold, stale drafts, a reworded open item) live in `clients/<slug>/page-decisions.json`
and the Worklist follows them: a dropped page loses its publish and open-item rows and gains a "trash draft" Setup row and a
301; a held page just loses its rows. A kind-1 Ask finding carries `page_actions` (option letter → the decision), so
`review.py apply` records the page decision Paul picked in the sheet. Open items split by who resolves them: Jonie only for a VA
task (a map embed); cited sources are the researcher's (`handoffs/researcher-list.md`); real client questions go in one
pre-filled list grouped by page (`handoffs/client-questions.md`, ready for Paul to send). `/verify` reopens a done row whose `done_check` fails. `worklist_title_max_chars` and `worklist_meta_chars` are in
`config.json`.

## Talking to Paul
Plain language: what was done, what waits on whom, the next command — start from `records.py top <slug>`; never
re-explain history. When refusing, say which gate is missing and what it would unlock. Never claim a check passed if
it was skipped. At a decision stop, end with: "Answer and approve in one sitting; if you step away for more than a few
minutes, end this chat and start a new one with /next — STATUS.md carries everything."
