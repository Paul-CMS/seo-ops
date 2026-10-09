# seo-ops rewrite 2: parallel clients, decide once for real, research before asking, content faster, cost down

**For:** a clean Claude Code **system session** in `~/Documents/seo-ops`, started on **Opus**. No client work happens in
this session.
**From:** Paul, 2026-10-09. The findings come from a full review of the repo, the git history and the Apex, Home Mobile
Medical and Gettysburg logs.
**Read first:** this file, then `CLAUDE.md`, then `REWRITE-HANDOFF.md` (rewrite 1). Rewrite 1's R1–R10 stay in force,
except where this file changes them.

**Working rules for this session:**

- Do the work in the order of §5.
- Run `python3 tests/run_all.py` after every change. Never commit a failing change, and give every new behaviour a new
  check.
- **Hooks:** Paul authorises editing `.claude/hooks/` for items **P2 and P3 only**. Ask Paul to confirm that in words at
  the start of the session before touching any hook.
- Commit per item, with the item ID in the message.

---

## 1 · Paul's requirements (2026-10-09) — all mandatory

| # | Requirement |
|---|---|
| Q1 | **Two clients, and two chats, at the same time** without any mixing of records, commits or session ids. |
| Q2 | **No workflow changes inside a client session.** Issues are flagged and noted. Changes are applied later, in a system session. **Only Paul changes the workflow.** |
| Q3 | **A question answered once is never asked again**, in any later session. |
| Q4 | **Use the evidence we have.** Reviews, the live site, GBP and the proof sheet are searched before anyone is asked. |
| Q5 | **Research before asking.** Public facts about a place, a code or the trade are looked up, never asked. Client facts are asked only after a search, and pre-filled with what was found. |
| Q6 | **Slugs per Bradley:** no `/services/`, `/service/` or `/service-area/` prefixes. Services and cities are root-proximate. |
| Q7 | **VA handoffs never stop page writing.** |
| Q8 | **One ongoing VA handoff document per client.** It is handed over once the service and location drafts exist; services and locations ship **as a whole**, not one page or one batch at a time. |
| Q9 | **Content much sooner.** A day to get past one service brief is not acceptable. |
| Q10 | **No silent placeholders.** Any placeholder or placeholder link left in a final draft carries a visible note. |
| Q11 | **Cut the cost of a full client run drastically.** |
| Q12 | **Models:** Haiku, Sonnet and Opus are all allowed. Each step uses the model that fits the job (§4). This replaces rewrite 1's R1, "Haiku and Opus only". |

---

## 2 · What is wrong today (evidence)

### F1 · Clients and chats mix (Q1)

- **The commit grabs everything.** `scripts/lib.py` `git_commit()` runs `git add -A`, so one client's run commits the other
  client's open run. This has already happened:
  - `db12ce6` (Apex) and `d2bbe0d` (Apex) contain `home-mobile-medical/log.md` and `status.json`.
  - `36f07e2` (HMM) contains `apex-roofing-of-the-lowcountry/log.md` and `status.json`.
- **There is one session file for the whole folder.** Both `session_start.py` and `approve_token.py` write
  `.claude/state/session.json`, so the last chat to receive a prompt wins. `run.py start` then stamps that id on another
  chat's run, and `stages.session_conflict()` refuses or merges the wrong session.
- **Pushes race.** Two runs that finish close together end in "push failed" with no retry.

### F2 · The workflow can change mid-session (Q2)

- **Nothing protects the system files.** `guard.py` does not cover `scripts/`, `scripts/gates.json`, `methodology/`,
  `CLAUDE.md`, `.claude/agents/`, `.claude/commands/` or `.claude/skills/`.
- **It has happened.** System commits landed in the middle of client runs: `e0cdf3b` (10-05 22:31, mid-Apex discovery),
  and `a5c57eb`, `6487a4c`, `990b381`, `b98efbc`, `d0c6425` (10-07, between Apex data runs).
- **The proposals inbox is never processed.** `methodology/lessons.md` has had L-008 to L-011 marked PROPOSED since
  10-06/10-08, with no review step.

### F3 · Answers don't stick (Q3)

- **A parser bug marks confirmed facts as unconfirmed.** `scripts/evidence.py` `mark()` (≈line 95) counts a fact as
  Known only when the status cell is exactly `paul approved`, `client confirmed` or `internally verified`.
  - Real cells read "Paul Approved 2026-10-06 · was: Submitted", so phone, warranty, licences, insurance and
    certifications all come out **Unverified**.
  - Both Apex pilot pages were blocked by this and needed waivers.
  - The bug was diagnosed in run `20261008-143018-build-a144` and is still unfixed.
- **Updating a fact's status cancels approvals.** Approvals fingerprint whole Brand Guide sections, status cells
  included. So no agent will update a status, and answers pile up as free text in `decisions-settled.md`.
  - Example: the ShingleMaster entry says "D value … still read not confirmed".
  - Example: `residential_roofer_a3_write` is still open although Paul approved the variant (site plan choice 4a).
- **The evidence script never reads the settled answers.** `evidence.py` grades from Brand Guide A/D and the page facts
  file only, never from `decisions-settled.md`.

### F4 · Reviews are not used (Q4)

- **A ruling keeps them out.** CM-027 bars review content from the facts.
- **The evidence gate doesn't read reviews.**
- **The summary is too thin.** `customer-language.md` keeps only first sentences and per-service counts.
- **Apex example.** `data/reviews/reviews.csv` had "Pierce" in 18 reviews, "photo" in 6, "clean" in 12, "underlayment" in
  6, "permit" in 2, and Hampton Hall once. Paul was still asked on 10-09 who goes on the roof (W25), about photos (W10),
  clean-up, permits on replacements and a 6th Bluffton neighbourhood.
- **The pull may be incomplete.** Two of Paul's answers ($20–25k price, magnet sweep) were "not in the export". Check
  whether `reviews.py` misses reviews or truncates long texts.

### F5 · No research (Q5)

- **The agents read the read lists as a ban on research.** `.claude/agents/build.md` says "Only the files listed for your
  step". Apex brief runs logged "No competitor research was done (it is outside the read list)" and "no official source
  in the read list" for the Town of Bluffton permit rules.
- **Paul's instruction was narrowed.** His waiver said "industry standards + competitor research + local context"; the
  agent applied it "narrowly".
- **Nothing separates client facts from public facts**, so both kinds go to Paul as questions.

### F6 · Slug rule not enforced (Q6)

- **The rules are correct on paper:**
  - `sop-source/BB-Standard-v1.0.md` lines 188 and 194.
  - `methodology/specs/service.md` SVC-02.
  - `methodology/specs/location.md` URL row 1.
  - `methodology/specs/county-hub.md` HUB-04.
- **But the approved HMM site plan breaks them on every page.** `clients/home-mobile-medical/build/site-plan-revised.plan.json`
  puts all 5 services under `/services/…` and all 25 location and hub pages under `/service-area/…`.
- **How that happened:**
  1. The import baseline kept the live URLs.
  2. Paul's round-3 question about keeping `/service-area/` hubs was logged as L-008 (PROPOSED) and never decided.
  3. No script checks site-plan URLs against the specs.
- **Apex has one leftover:** it keeps `/metal-roofing-2/`.

### F7 · Handoffs block writing (Q7)

- **`/next` stops at the first wait.** `scripts/next.py` raises `Next` at the first output, so a batch in `handed_off`
  returns "wait" and stops the loop.
- **Location writing waits for service pages to go live.** `scripts/status.py` `batch_order_blocks()` blocks every
  location batch until every service batch is `written_back`, which only comes after Jonie publishes and `/verify` passes.
- **The pilot's ship step waits for publishing too.** In `gates.json` → `modes`, `build:ship` pilot =
  `batch_state:pilot:written_back`.
- **It is visible today.** HMM's STATUS.md says "Next action: /next … once the wait above is over".

### F8 · Many handoffs, published batch by batch (Q8)

- **Five or more handoff files per client:** separate H-…-01 to 05 files (wp_setup, seopress_settings, redirect,
  broken_link, other), plus one publish handoff per batch.
- **Link tables go out incomplete.** `publish.py` leaves out link-table rows that point at unpublished pages and hands
  them over later as `publish.py pending`, which means more handoffs.

### F9 · Slow content (Q9)

- **Apex pilot timeline:**
  - Site plan approved 10-08 14:28.
  - Evidence gate blocked both pages (the F3 bug); waived 15:05.
  - Roof Repair brief run open 15:05–22:21.
  - Bluffton brief 22:22–22:29.
  - Briefs approved 10-09 12:22.
  - Drafts approved twice (13:14 and 14:02).
- **That is about 24 hours and 14 runs for 2 pages.** The causes:
  - the F3 bug;
  - fact questions raised in the middle of the pipeline;
  - a brief approval stop per batch;
  - one run per page per stage, with a new session per batch;
  - a second draft approval round.

### F10 · Placeholders ship silently (Q10)

- **Only one placeholder type is replaced.** `publish.py` swaps out only table-row link-wheel lines.
- **An approved draft carries publishable placeholder text.** The Apex Roof Repair draft
  (`build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md`, line 76) has an inline
  `[Link placeholder: /emergency-roof-repair/ — CM-022 exception …]` inside an FAQ answer. It would publish as visible
  text.
- **Nothing scans for `[NEED: …]` before shipping.** `readability.py` even strips the markers.
- **Missing link targets disappear silently.** Rows pointing at unpublished pages are dropped with no note.

### F11 · Cost (Q11)

- **Apex cost about $111 to discovery sign-off.** About 60% of that was the main chat re-reading and re-storing its own
  history (see REWRITE-HANDOFF.md §1).
- **Each build run starts at roughly 40k tokens of fixed reading before any work:**

  | File | Size |
  |---|---|
  | `methodology/rulings.md` | 60 KB |
  | `brand-guide.md` | 36 KB |
  | `CLAUDE.md` | 28 KB |
  | `.claude/agents/build.md` | 14 KB |
  | Spec + `writing-commercial.md` | ~19 KB |

- **Revisions multiply that fixed reading:** entity approved 3×, proof sheet 3 versions, audit re-rendered 2×, pilot
  drafts approved 2×.
- **Mechanical checks run on Opus.** Most spec conformance checks are mechanical, yet they run in the Opus audit agent
  (18% of the Apex bill).

---

## 3 · Design — what to build

### P1 · Fix the evidence parser (F3) — first, alone

- `evidence.py mark()`: read the **leading status word** of the cell (case-insensitive) before any date or qualifier.
  "Unknown …" counts as Unknown and "Disputed …" as Conflict.
- Add tests for:
  - "Paul Approved 2026-10-06 · was: Submitted" → Known;
  - "Client Confirmed (sheet)" → Known;
  - "Submitted" → Unverified;
  - "Unknown — asked 10-08" → Unknown.
- Re-run the grid for Apex `svc-roof-repair` and `loc-bluffton` in the test sandbox. Expect WARN, not BLOCK.

### P2 · Parallel clients and chats (F1)

- **One git worktree per client.** Add `scripts/worktree.py open <slug>`. It creates or reuses
  `~/Documents/seo-ops-clients/<slug>/` on branch `client/<slug>`, tracking `main`, and prints the folder to open the chat
  in. `config.json` → `client_worktrees_root`.
  - Each worktree has its own `.claude/state/`, which removes the shared session file.
  - Each worktree has its own git index, which stops one client's commit picking up another's files.
- **Commit only this client.** `lib.git_commit(message, slug=None)`:
  - with a slug, `git add -- clients/<slug>/` only, never `-A`;
  - system commits (no slug) are allowed only in a system session (P3).
- **Merge back safely.** After the commit: `git pull --rebase` on `client/<slug>`, then merge to `main` (fast-forward) and
  push, with one retry on a race. A real conflict → stop and print the plain-language message. Never force.
- **Session file per session.** `.claude/state/sessions/<session_id>.json`, written by both hooks.
  - `stages.current_session()` takes the id from the newest file for the worktree's own state folder.
  - Belt and braces: the hooks also write `CLAUDE_SEO_OPS_SESSION` into the session's environment file if Claude Code
    exposes one. If it doesn't, the worktree split alone is enough.
- **Client lock.** `clients/<slug>/.lock` (git-ignored) holds the session id and host. `run.py start` refuses a second
  session on the same client while the lock is fresh: under 2 hours old, or the owning session is still the latest in
  that worktree.
  - `run.py unlock <slug>` is for Paul only. The guard blocks Claude from deleting the lock.
- **VA-SETUP.md** changes from "agree on who has which client" to "`python3 scripts/worktree.py open <slug>`, then open
  the chat in that folder".
- **Tests:**
  - two fake clients run in two worktrees, interleaved, give two clean commits with no cross files;
  - two sessions on one client → the second is refused;
  - the push race → one retry, then success.

### P3 · System changes only in a system session (F2)

- **New command `/system`, typed by Paul.** A `UserPromptSubmit` hook writes a one-time system token, the same mechanism
  as `/approve`. It is valid for the session that typed it.
- **Guard: block edits to system paths without that token.** Covered: `scripts/**`, `scripts/gates.json`,
  `methodology/**` (except `methodology/change-requests.md`, which is append-only via script), `CLAUDE.md`,
  `.claude/agents/**`, `.claude/commands/**`, `.claude/skills/**`, `templates/**`, `tests/**`, `config.json`.
  - The refusal message: *"Workflow changes happen in a system session. Flag it instead:
    `python3 scripts/run.py flag <slug> <RUN_ID> --text "…"`."*
- **`machine.json` → `can_change_system: false`** on a VA Mac. The `/system` token is refused there.
- **`run.py flag`** appends to `methodology/change-requests.md`. Each entry gets an ID (CR-###), date, client, step, run,
  who flagged it, the text, and the workaround used.
  - The run continues on the current rules.
  - `records.py` lists open flags in the client's STATUS.md under "Flagged for Paul (system)".
- **New command `/system-review`** (system session only) lists open CRs and every PROPOSED item in `lessons.md`. Paul
  answers each: accept, reject or edit.
  - Accepted items become work items for that session.
  - Then: tests, commit, CR marked DONE with the commit sha.
- **Merge `lessons.md` into `change-requests.md`** (L-008 to L-011 become CR-001 to CR-004). One inbox.
- **CLAUDE.md §0** is rewritten to say this.

### P4 · One facts store; answers stick (F3, Q3)

- **New `clients/<slug>/facts.json`, the single source for every fact about the client.** Each row holds: id, label,
  value, status (`client_confirmed` · `paul_approved` · `internally_verified` · `customer_reported` · `submitted` ·
  `unknown` · `disputed`), source, quote, date, and who.
  - Statuses are machine values; their display labels live in the Brand Guide.
- **One way in:** `run.py fact <slug> <RUN_ID> --id … --value … --status … --source … [--quote …]`. It is logged in
  `log.md`.
  - Every answer from Paul or the client goes in this way, wherever it came from (chat, proof sheet, interview, email).
  - The Haiku main session must call it the moment Paul answers; the `/next` command text says so.
- **Brand Guide fact rows are generated from `facts.json`** (`records.py`). Agents never edit fact rows by hand.
- **Approvals fingerprint values only, never statuses or dates.** Change `lib.ref_sha` for `brand-guide.md#…`
  references to hash a normalised "field = value" list. A confirmation therefore never cancels an approval. A changed
  value still does, and should.
- **`evidence.py` grades from `facts.json`** (plus the page facts file for page-only facts). It no longer reads Brand
  Guide cells.
- **Question de-duplication.** Every question set goes through a new `settled.filter_questions(slug, questions)` before
  Paul sees it. It drops anything answered in `facts.json` or `decisions-settled.md`, matching on fact id first and
  normalised text second.
  - Dropped questions are listed in one line: "already answered: W25 (10-09), …".
- **Migration** (in `migrate.py`) for Apex, HMM and Gettysburg:
  - build `facts.json` from the Brand Guide A/D rows, the settled entries and the returned proof-sheet answers;
  - Apex's 10-09 settled answers (W25, W10, W11, Bluffton neighbourhoods, ShingleMaster, synthetic roofing,
    Residential Roofer) become `paul_approved` rows;
  - existing approvals are re-fingerprinted on the value-only hash so none of them is lost;
  - log one MIGRATION line per client.
- **Tests:**
  - a status-only change keeps the approval; a value change voids it;
  - a question already answered is filtered out;
  - the migration keeps every recorded approval.

### P5 · Reviews as evidence (F4, Q4)

- **New ruling CM-054** (Paul approves the wording at the start of the session). It replaces CM-027's first bullet:
  - review content may enter `facts.json` as **`customer_reported`**, with the quote and the count of reviews that
    support it;
  - a customer-reported fact counts as **Known for the evidence gate** when 3 or more independent reviews support it
    and nothing conflicts;
  - the writer may state it only as customers describe it ("customers mention…") until Paul or the client confirms it.
    One confirmation turns it into a plain fact;
  - reviewer names stay out of deliverables (unchanged), and so do self-serving rating claims in schema (unchanged).
- **`reviews.py extract <slug>`** (script, plus the Sonnet `researcher` agent from §4 for matching meaning, not just
  keywords). For every fact in `methodology/evidence-requirements.json`, find the supporting review quotes and write
  `customer_reported` candidates with the quote and the count.
  - Also: people named (staff), neighbourhoods and towns, materials, practices (photos, clean-up, permits), prices,
    timelines and warranties mentioned.
- **Check the pull is complete.** `reviews.py` compares its count with GBP's displayed count and flags a gap. Add a test
  for long review texts not being truncated.
- **`customer-language.md`** gains a "Facts customers report" table: fact, quote, count.

### P6 · Research before asking (F5, Q5)

- **Every question is labelled by kind:**
  - **`public`** — about a place, a code, the trade or a manufacturer. It is **never asked**. The `researcher` agent
    looks it up in official sources, cites them, or records "not found" with the sources tried. Paul sees only
    "not found" items, as a decision: drop the element, or keep it general.
  - **`client`** — something only the client can know. It is asked **only after** the client-fact search order:
    `facts.json` → `decisions-settled.md` → reviews (P5) → live site page text → GBP data → proof sheet and Discovery
    Record. Each question carries a `searched:` line and a pre-filled best answer when one exists.
- **Code enforces it.** `evidence.py questions` and the audit's Gate B question writer refuse a question without a kind,
  or a `client` question without a `searched:` line.
- **Read lists mean "files to load", not "the limit of research".** Add one line to every agent: *"The read list limits
  which project files you load. It never limits web research for public facts. Follow Paul's instructions as written,
  never narrower."*
- **Source lists per area,** `methodology/sources/<state>-<area>.md` (e.g. `sc-lowcountry.md`, `tn-middle.md`): town and
  county permit and planning pages, state licence lookups, state building code adoption, Wikipedia/Wikidata for places.
  The researcher uses these first. They are built once and reused for every client in that area; the researcher appends
  new ones (via `run.py flag` when it suggests a new source; Paul adds them in `/system-review`).
- **Competitor pages, for coverage only.** In the data stage, `crawl.py competitors <slug>` saves the top-3 organic pages
  per main service keyword. A script summarises them: H2s, FAQ topics, word count. Used only as coverage ideas in the
  site plan, never as client claims (CM-016 unchanged).

### P7 · Slugs (F6, Q6)

- **New `scripts/urlcheck.py <slug> <plan.json>`**, run by `/build plan` before the plan can be recorded. It refuses:
  - `/services/`, `/service/`, `/service-area/`, `/service-areas/`, `/locations/` and `/areas/` prefixes;
  - a service slug with a city;
  - a location slug with a service;
  - `-2`, `-3` … suffixes;
  - more than one path segment for service and location pages.
  - Hubs: root-proximate county or metro slug (HUB-04).
  - The import baseline is **not** exempt.
- **Changed URLs become redirect rows automatically.** Every changed URL generates its 301 row (old full URL → new full
  URL) in the VA Worklist (P9), paired with the publish of the new page.
- **Decided by Paul at session start, then applied:**
  - **HMM:** move all `/services/<x>/` → `/<x>/` and `/service-area/<city>/` → `/<city>/`.
    - Hubs become root-proximate (`/charleston-metro/` or a county slug per L-008/CR-001).
    - `/service-area/` itself redirects to the homepage or the main hub.
    - Re-approve the site plan once, in one line.
  - **Apex:** `/metal-roofing-2/` → `/metal-roofing/`, with its redirect.
  - Record both as settled decisions.

### P8 · Writing never waits on a VA (F7, Q7)

- **`next.py`: waits are collected, not stopped on.**
  - A `wait` is recorded in a list and the loop continues to the next runnable step.
  - `/next` returns the first `run` or `decision` it finds, plus the list of open waits.
  - It returns `wait` only when nothing else can run.
- **`status.py batch_order_blocks()`:** services before locations now means **service drafts approved**, not
  `written_back`. The Brand Guide write-back of a batch runs right after its drafts approval (it is content, not
  publishing). Publishing is never a prerequisite for writing.
- **`gates.json` → `modes`:** `build:ship` and `build:published` pilot conditions move from
  `batch_state:pilot:written_back` to `batch:pilot:drafts`.
- **STATUS.md** "Next action" shows the next thing the system can do. Waits move to "Waiting on (not blocking)".
- **Tests:**
  - a client with an open blocker handoff and an open publish handoff still gets `/next` → the next brief or draft;
  - location writing starts once the service drafts are approved, with nothing published.

### P9 · One VA Worklist per client; ship everything at once (F8, Q8)

- **The worklist file.** `handoff.py` writes every item for a client into one living worklist:
  `clients/<slug>/handoffs/VA-WORKLIST.csv`, plus a generated `[Client] - VA Worklist.md` copied to Drive.
  - Sections, in this order: **1 Setup** (WordPress user, SEOPress settings) · **2 Blockers** · **3 Redirects** ·
    **4 Publish** · **5 After publish** (alt text check, menus, link-table updates) · **6 Manual lookups** (Gwen).
  - Columns as today, plus `section`, `owner`, `added`, `status`, `note`.
  - New items are appended. Nothing is overwritten.
  - `handoff.py ingest` reads Jonie's ticks from the same file. `/verify` checks done rows.
  - Existing H-… files are migrated into it; old files are kept and marked superseded.
- **When it goes out.** Section 1 and Section 6 rows can go to the VA at any time (they block nothing). The full
  worklist, with Publish and Redirects, is **handed over once**, when **all service and location drafts** are in
  WordPress.
- **Ship everything together.**
  - `build:ship` takes `--all` (default). It creates WordPress drafts for every approved service and location page in
    one run. Link tables are filled **completely**, because every target now exists as a draft with its final URL.
    Set `config.json wheel_link_unpublished: true`; the slugs are fixed.
  - Homepage and About ship in the same handover if approved, otherwise as a later worklist addition.
  - Redirects for replaced URLs sit next to their publish rows, so Jonie does both together.
- **`publish.py pending`** stays only for pages added after the handover.

### P10 · Content faster (F9, Q9)

New build sequence after Approval 2:

1. **Site plan.** All service, location and hub pages, plus URL check (P7) and competitor coverage (P6). **One
   approval.**
2. **One facts round for all pages**, not per batch.
   - Evidence grids for every page in one run.
   - Then the researcher (P6) clears every `public` gap, and review candidates (P5) are attached.
   - Then **one** pre-filled question set for Paul, mostly confirm/deny lines, grouped by fact, not by page: one answer
     can fill 20 location pages.
   - Paul answers once; `run.py fact` records the answers; the grids re-run.
   - Waivers are rarely needed.
3. **Pilot (1 service + 1 location).** Briefs and drafts in one run (two parallel agents, each with a fresh context, so
   CM-043 holds) → **one** pilot approval (briefs and drafts together) → pilot corrections into the specs.
4. **After the pilot, briefs switch to auto by default** for that client (`/approve <slug> mode:build:brief=auto` is
   printed as part of the pilot approval line, so Paul approves both in one line).
5. **All service pages in one run.** Briefs, then drafts as parallel agents, one per page, each with a fresh context;
   then the batch review (sibling check) in the same run → **one drafts approval** with SEM picks.
6. **All location and hub pages in one run**, as in step 5 → **one drafts approval**.
7. **Ship everything (P9).** Homepage and About last, or in parallel if Paul prefers.

Supporting changes:

- **Parallel drafting in one run.** `run.py` gets a `--pages all` mode for brief and draft steps. The run records each
  page's sub-agent separately, so CM-043's fresh context per page is kept and logged.
- **`R2` (one session per stage) is kept,** with the stage map changed so steps 3–7 are four sessions, not one per
  batch: pilot · services · locations · ship.
- **Batches remain for very large sites:** over 15 pages of one kind are split by cluster or county, still one run per
  batch.

### P11 · Placeholders (F10, Q10)

- **New `scripts/placeholders.py scan <file>`** finds: `[NEED:`, `[Link placeholder`, `[Link wheel` (unfilled after
  ship), `[PLACEHOLDER`, `[TBD`, `TODO`, `TBD`, `XXX`, `{{…}}`, `[PAUL'S …]`, and any `[…]` that is not a Markdown link.
- **At drafts approval,** the approval line lists every placeholder per page, so Paul approves knowingly.
- **At ship:**
  - each WordPress draft with an open placeholder gets a visible notice block at the top ("Open items on this page —
    remove before publishing: …");
  - a matching row goes into VA Worklist section 4 with the exact text and line;
  - Jonie never publishes a page with a notice block until the row is resolved;
  - `/verify` fails a live page that still contains a placeholder string.
- **Inline link placeholders must be marked.** The build writer may only use inline link placeholders in the form
  `[LINK → /slug/ · reason]`. The link-wheel step then turns them into real links once Paul approves the CM-022
  exception, or removes the bracket and keeps the text.
- **Fix the Apex Roof Repair draft line 76** to that form (no wording change), as a migration step.

### P12 · Cost (F11, Q11)

- **Rulings by ID.** New `scripts/rulings.py CM-020 CM-022 …` prints only those sections. Read lists cite IDs. Agents
  must use the script, never read `rulings.md` whole; the guard warns on a full read of `rulings.md` inside a client
  session.
- **Split CLAUDE.md.**
  - A core file of at most 4 KB: the safety rules, the run protocol, "Paul decides", the flag rule and the facts rule.
  - Plus `docs/stage-<n>.md`, one per stage, loaded only by that stage's agent and command.
  - The full procedure lives in those files; the core points to them.
- **Read sections, not whole files.**
  - `brand-guide.md` and `facts.json` by section or by id: `records.py brand <slug> --sections A,D`,
    `facts.py get <slug> --ids …`.
  - Agents never read `log.md` or `handoff-log.md` (the guard blocks it in client sessions; STATUS.md and
    `decisions-settled.md` replace them).
- **Mechanical audit checks move to a script.** New `scripts/conformance.py` scores every check that needs no judgment,
  from the crawl and the page-text capture: URL format, title and meta length, brand in the title, H1 count and
  keyword/variant, variant repetition (SVC-11), NAP present, FAQ count, link tables present, schema present.
  - The Opus audit agent fills only the judgment columns (claims, openings, FAQ fit, tone).
  - Mark each check in the specs as `auto` or `judgment`.
- **Fewer runs.** P10 cuts the run count for a full build by about two-thirds.
- **Keep sessions short and warm.** `/next` prints, at every decision stop: *"Answer and approve in one sitting; if you
  step away for more than a few minutes, end this chat and start a new one with /next — STATUS.md carries everything."*
- **Turn off unused connectors.** Paul runs `/context` in a seo-ops session. Any connector tools listed that seo-ops never
  uses get disabled for this project in the project settings. Record which ones in `config.json` → `mcp_allowed`; the
  SessionStart hook warns when others are loaded.
- **Measure.** `run.py finish` records the run's token use and cost (from Claude Code's usage data if available,
  otherwise as a field the session reports). `records.py` adds a "Spend by step" table to STATUS.md next to the
  DataforSEO spend. After one client this shows exactly where the money goes.
- **Later step, not this session — batch drafting through the API.** If Paul pays API rates, location drafts can run
  through the Message Batches API at about half price, overnight. Record it as CR-005 for a later system session.

---

## 4 · Models per step (Q12)

The rule: **Opus** where the judgment is hard to check (audit analysis, the independent review, commercial copy before
the pilot proves the specs). **Sonnet** where the work is structured assembly, research or extraction. **Haiku** for
orchestration and mechanics. No session switches model mid-session (rewrite 1 R1 stays).

| Step | Main session | Agent | Model |
|---|---|---|---|
| Every stage chat (`/next`, relay, `/approve` lines, `run.py fact` on Paul's answers) | Haiku | — | Haiku |
| Setup, data pulls, crawl, wp-check, records, ship, worklist | Haiku | `clerk` | Haiku |
| Discovery research and the entity proposal | Haiku | `discovery-audit` | Opus |
| Public-fact research, review extraction, competitor summaries, source lists | Haiku | **`researcher` (new)** | **Sonnet** |
| Audit judgment columns and findings | Haiku | `discovery-audit` | Opus |
| Fresh-context audit review | Haiku | `audit-reviewer` | Opus |
| Site plan | Haiku | `build` | Opus |
| Briefs | Haiku | **`brief-writer` (new)** | **Sonnet** |
| Pilot drafts | Haiku | `build` | Opus |
| Service and location drafts after the pilot | Haiku | `build` (default) or **`draft-writer`** | Opus by default; **Sonnet test** (below) |
| Batch review / sibling check | Haiku | `build` | Opus |
| Link wheel, schema (script-driven), QA crawl | Haiku | `finish` | **Sonnet** |
| Content QA in Finish | Haiku | `finish-qa` | Opus |
| Blog map | Haiku | `blog` | Sonnet |
| Blog posts | Haiku | `blog` | Opus |
| System sessions (like this one) | Opus | — | Opus |

**Sonnet drafting test:** on the next client after the pilot, write one service page with both Opus and Sonnet from the
same brief. Paul compares them side by side (`build/compare/`) and decides with `/approve global model:build:draft=sonnet`
or `=opus`. Record the decision in `gates.json` → `models` and log it. `next.py` and `stages.py list` print each step's
models from `gates.json`, so the frontmatter and the stage map can't drift: add a test that compares them.

---

## 5 · Order of work for this session

1. **Paul first:**
   - (a) confirm the hook authorisation for P2 and P3;
   - (b) approve CM-054's wording (P5);
   - (c) decide the HMM URL move and hub slugs, and Apex `/metal-roofing-2/` (P7);
   - (d) say whether HMM and Apex may be migrated now.
2. **P1** parser fix → tests → commit.
3. **P3** system guard, `/system`, `run.py flag`, `/system-review`, lessons merged into change-requests → tests.
4. **P2** worktrees, per-client commit, per-session file, client lock, push retry → tests.
5. **P8** writing never waits → tests.
6. **P11** placeholder scan → tests.
7. **P7** URL check and the decided URL changes → tests.
8. **P4** facts store, value-only approval hashes, question filter, migration → tests.
9. **P5** CM-054, review extraction, pull completeness → tests.
10. **P6** question kinds, researcher agent, source lists, competitor coverage → tests.
11. **P9** VA Worklist, ship-all → tests.
12. **P10** new build sequence, `--pages all`, stage map, auto briefs after the pilot → tests.
13. **P12** cost items, plus the models in §4 → tests.
14. Update `CLAUDE.md` (core and stage files), `VA-SETUP.md` and the stage map; run `tests/run_all.py`; commit and push.
15. Regenerate STATUS.md for Apex, HMM and Gettysburg. Each resumes **in its own worktree and its own new session**.

## 6 · Done means

- Two clients run at the same time in two chats give clean, separate commits, with no session refusals caused by the
  other chat.
- A client session can't edit any system file. A flagged issue shows up in `/system-review`.
- A question answered once never appears again, and the evidence gate passes facts Paul or the client confirmed.
- Every question shown to Paul has a kind and a `searched:` line, and public facts never reach him as questions.
- No planned URL has a `/services/` or `/service-area/` prefix or a `-2` suffix.
- `/next` always offers the next writing step while VA items are open.
- One VA Worklist per client. Service and location pages ship together with complete link tables.
- Site plan approval to all service drafts approved: **one working day** for a client the size of Apex (8 services).
- No WordPress draft carries a placeholder without a visible notice and a worklist row.
- STATUS.md shows spend by step. Target for a full Apex-size client, intake to all pages shipped: **under $30** in model
  cost.
