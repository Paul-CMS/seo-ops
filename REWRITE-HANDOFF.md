# seo-ops rewrite — cut cost, approve less, decide once

**For:** a clean Claude Code session in `~/Documents/seo-ops`, started on **Opus** (this is system design work).
**From:** the Apex Roofing of the Lowcountry run, 2026-10-05 → 2026-10-08. **Owner:** Paul.
**Read first:** this file, then `CLAUDE.md`. Do the work in the order of §6. `python3 tests/run_all.py` after every
change; never commit a failing change; every new behaviour gets a new check. Hooks (`.claude/hooks/guard.py`,
`approve_token.py`) are off limits unless Paul says in that session, in words, that you may edit them for a named item.

---

## 1 · Why — what the Apex run actually cost

Paul's bill for intake → discovery sign-off on one client: **about $111.** Of that:

| Where it went | Share | ≈ $ |
|---|---|---|
| Main chat re-reading its whole history every turn (370 turns, context grew to ~670k tokens) | 35% | 39 |
| Main chat storing new content into that history (incl. 6 full re-stores after long pauses) | 17% | 19 |
| Audit analysis helper | 18% | 20 |
| Claude's standing instructions, re-read every turn | 8% | 9 |
| Drive "uploads" — the model retyping files into the connector (Handoff Log 65 KB, ×4) | 7% | 8 |
| Other helpers (discovery, proof sheet, reviewer, routing, reconcile, sign-off) | 11% | 12 |
| Claude's written replies | 4% | 4 |
| **Paid data (DataforSEO: crawl, reviews, rankings, backlinks, PAA, fan-out)** | **<1%** | **0.60** |

Also costly: decisions revisited (entity approved 3×, proof sheet 3 versions, audit re-rendered twice) and one-time
system repairs during the run. A simulation of the same run split into one session per stage cuts the main-chat
cost by ~35–55%. **Target after this rewrite: $15–30 for a client like Apex.**

## 2 · Paul's requirements (2026-10-08) — all mandatory

| # | Requirement (Paul's words, tightened) |
|---|---|
| R1 | **Models are preset — Haiku and Opus only** (no Sonnet, no Fable). Never switch a session's model mid-session (it re-stores the whole conversation). Note for Paul: Haiku is the cheapest model; Opus is the most capable and the most expensive — so Opus is used only where judgment is needed. |
| R2 | **A new session is mandatory at each stage start.** The system must enforce it, not suggest it. |
| R3 | **Approve less.** |
| R4 | **Drive uploads happen by themselves** — never by Claude retyping a file. |
| R5 | Use the **cheapest file types** for Claude to read. |
| R6 | **A decision is made once and done.** If a decision gets revisited three times because of later decisions, it was asked at the wrong time — fix the order, not the decision. |
| R7 | **VA-clear status:** at any moment a VA can see what stage the client is in, what is happening, who is waiting on what, and the next action. Settled things are never re-raised (e.g. "the Finding Register isn't in Drive" is one decision, recorded once). |
| R8 | **Drive scope = the v3 folder only.** A new client: check whether `<Client> - TMS` exists in v3 and go from there. Never search or scan other Drive folders for prior work on a client. |
| R9 | **Every earlier workflow note is implemented** (inventory in §5). |
| R10 | Keep what works: gates, the safety log, runs, tests, "Paul decides; the system prepares, checks, logs and stops". |

## 3 · Design — what to build, per requirement

### R1 · Preset models
- `.claude/agents/*.md` frontmatter gets `model:`. **opus:** `discovery-audit`, `audit-reviewer`, `build`, `finish`,
  `blog` (judgment and writing). **haiku:** a new **`clerk`** agent for all mechanical work — running scripts and
  recording step outcomes, data pulls after Paul's cost yes, `/crawl`, `/wp-check`, safe-fix runs from an approved list,
  record mirrors, handoff-file writing, status reports. Opus agents hand mechanical sub-tasks to `clerk` instead of doing
  them.
- **Main session = Haiku** for every stage (it orchestrates `/next`, relays agent reports, prints `/approve` lines).
  Judgment lives in the Opus agents, which write their own plain-language summary file for the main session to relay.
  Exception: system/design sessions like this one run on Opus.
- `next.py` prints, for the step it proposes, the **session model** and the agents/models it will use, so Paul starts
  the session right. A `SessionStart` hook prints the same reminder. Subagent models are fixed by frontmatter, so they
  never cause a mid-session switch.

### R2 · Mandatory new session per stage
- A hook records the session id at session start (`.claude/state/session.json`, git-ignored). `run.py start` stores the
  session id on every run. **`run.py start` refuses a run of a new stage in a session that already finished a different
  stage** (bookkeeping runs inside the same stage are allowed). Message: *"Stage <x> is done. Start a new session
  (new chat, model: <m>) and type /next <slug>."*
- Stage boundaries = the approval points in R3. Each stage session begins with `/next <slug>` — which already loads only
  `status.py show` + the step's read list. Handoff Log sections carry everything the next session needs.
- Long Paul pauses inside a session (cache expiry → full re-store) become rare because sessions are short.

### R3 · Approve less — target 2 approvals for discovery + audit (Apex needed 7)
| Today | Proposed |
|---|---|
| entity_approved, then proof_sheet_approved | **One "Discovery" approval:** the Decision Sheet (R6) + entity + proof sheet in one line. If the facts were answered directly and no sheet is sent, a **"facts answered directly"** path: Paul confirms the answers file, which meets both `proof_sheet_approved` and `proof_sheet_returned` — no approving a sheet nobody receives. |
| audit_approved, brand_guide_approved, discovery_signed_off | **One "Audit + facts" approval** line. `discovery_signed_off` becomes a **derived condition** (met when entity, audit and Brand Guide are approved and the returned facts are recorded) — no separate summary to approve. |
| Page specs DRAFT, per client | Paul approves the **page specs once, globally**, before any audit scores against them (they are methodology, not client work). Never re-approved per client unless a spec changes. |
| blockers_cleared (Paul) | **Condition**: Jonie's blocker handoff returned `done` + `/verify` passed. |
| per-batch briefs + drafts approvals | Keep through the pilot; after the pilot Paul may switch stages to auto (CM-044 already supports it) and approve **drafts only** per batch. |
| Re-approvals caused by status-label edits (entity voided by reconcile) | Section A/B row **statuses move out of the hashed sections** (a status table approve.py stamps, or the Approval Record is the only status). A reconcile with no entity-relevant correction must not void `entity_approved`. |
Change `gates.json`, `approve.py`, `next.py`, `status.py`, the commands and agents together; migrate existing clients' status.json (Apex, Gettysburg, home-mobile-medical) without losing recorded approvals.

### R4 · Drive uploads by themselves — Google Drive for desktop
- **Paul installs Google Drive for desktop** (not installed on this Mac as of 2026-10-08) and signs in as
  paul@coastalmarketingstrategies.com, **streaming** mode. The v3 folder then exists as a local path under
  `~/Library/CloudStorage/GoogleDrive-…/` (My Drive or Shared drives — confirm with Paul). Store it in `config.json`
  `drive.local_root`.
- `drive.py` writes to that local path: upload = **file copy** (byte-exact, any size — crawl CSVs, the 87 KB Finding
  Register), archive-and-replace = local rename + move into `_Archive/`; Drive syncs. **Zero tokens, nothing retyped.**
  `/new-client` copies `_CLIENT FOLDER TEMPLATE - copy per client` as a real folder copy (fixes the template-drift note).
- **Records mirror automatically inside `run.py finish`** (regenerated Handoff Log, Approval Record, Document Checklist,
  Brand Guide, STATUS.md) — no separate `drive-mirror` run, no agent. Every copy logged as a `drive_file` change by the
  script.
- The Drive connector stays only for the single native Google Doc (proof sheet `- CLIENT COPY`), uploaded as **HTML**
  (Markdown inside tables showed literal asterisks). Everything else via the local path.
- Until Paul installs it: no connector retyping of large files — record "Drive copy pending sync" once (R7) and move on.

### R5 · Cheapest file types for Claude to read
- Cost is **size in tokens**, not the format's name — but formats differ: **CSV** (tables) and **Markdown** (documents)
  are the cheapest per fact. **JSON** repeats every key on every row (several times a CSV). **HTML** carries markup.
  **PDFs and images** are the most expensive (pages can be read as images) — and need a renderer.
- Rule: agents read **script-made summaries**, never raw exports. Add compact summary outputs: crawl → one row per page
  with only the audited columns; reviews → themes + counts; backlinks → per-URL counts; Local Dominator PDFs → a script
  extracts the text once (macOS PDFKit works without poppler) into `data/local-grid/local-grid-summary.md`.
  Each step's read list names the summary, not the raw file.
- Read only what a step needs (the read lists already do this — keep them tight; add line/section targeting where a file
  is large).

### R6 · Decide once — fix the order
What went wrong at Apex (every one is a decision asked before the information that shapes it existed):
- Area entity and reserved homepage variant were approved **before** the title format per page type was known → entity
  re-approved twice (Lowcountry vs metro; reserved variant swapped after the audit).
- The audit scored pages against **DRAFT** specs → Gate B and approval-time rulings (service title format, HP-06 vs
  BB-304, About page format) arrived late.
- Street address display was decided at the proof sheet, then the client reversed it, then reconcile asked again.

Build this:
- **One Decision Sheet at the discovery stage** — every identity/format decision together, each with a recommended
  default, answered once: category + variants · area entity · reserved homepage **title** variant · homepage **H1**
  variant · **SEO-title format per page type** (homepage, service, location, about, blog) · brand written in full in
  titles · residential/commercial scope · service list · towns served · address display (GBP / website) · "The Best"
  policy · blog author · sensitive category · tools available (citations? grid tool?). The audit and Build then *apply*
  these; they never re-ask.
- **Settled-decisions register** `clients/<slug>/decisions-settled.md`, generated from the log (records.py). Every agent
  reads it; an agent may not re-raise a settled decision. New contradicting evidence → **one** "reopen request" with the
  reason, logged with the flag `reopened`; `records.py` counts reopenings per client as process defects in the test-run
  notes.
- Missing-data decisions (citations skipped, a grid tool, files too big for Drive, Admin vs Editor login…) are recorded
  **once**, appear under "Settled" in STATUS.md, and are never repeated in later summaries.

### R7 · VA-clear status
- `records.py` generates **`clients/<slug>/STATUS.md`** (one page, plain language, mirrored to the Drive client folder):
  **Stage n of N — name** · **What is happening now** · **Waiting on** (who, what, since, handoff id) · **Next action**
  (the exact command and session model) · **Settled decisions** (one line each, never re-raised) · **Open VA items**
  (Jonie / Gwen handoffs with status) · **Spend so far** (DataforSEO from the ledger).
- `/resume` and `/next` print STATUS.md's top four lines instead of re-explaining history.

### R8 · Drive scope = v3 only
- Remove every Drive-wide search from commands and agents. `/new-client` checks only `<v3>/<Client> - TMS`. With R4 the
  tooling never sees anything outside `drive.local_root`.
- Guard rule (Paul to authorise the hook edit): block the Drive connector's `search_files` unless the query is scoped to
  a folder under v3 (`parentId = '<id under v3>'`). At Apex the setup searched all of Drive and surfaced three unrelated
  Apex folders — exactly what R8 forbids.

## 4 · Stage map (target)

| Stage | Session model | Agents | Paul at the end |
|---|---|---|---|
| 1 Setup (`/new-client`, WordPress setup handoff, Decision Sheet questions sent) | Haiku | clerk | — (condition) |
| 2 Discovery (public research, entity, Decision Sheet, proof sheet or direct facts) | Haiku | discovery-audit (Opus) | **Approval 1** — Decision Sheet + entity + proof sheet / facts |
| 3 Data (crawl + paid pulls after one cost yes; routing) | Haiku | clerk (scripts), discovery-audit (routing) | one cost "yes" for the whole step |
| 4 Audit (analysis → fresh review → render; facts reconciled into the Brand Guide) | Haiku | discovery-audit, audit-reviewer (Opus) | **Approval 2** — audit + Brand Guide (sign-off derived) |
| 5 Build plan + blockers (site plan; blocker handoff to Jonie) | Haiku | build (Opus), clerk | site plan |
| 6 Pilot, then batches | Haiku | build (Opus), clerk | per batch (drafts only after the pilot) |
| 7 Finish, 8 Blog | Haiku | finish / blog (Opus), clerk | as today |

## 5 · Every workflow note — status and what to do

**Done already** (commits on `main`): approval vs open-choices separation + env-lines credentials helper (73a99c0) ·
SEOPress 10.x reads, section-scoped approvals, `wp_setup`/`manual_lookup` handoff kinds, no doubled Handoff Log headings,
one county URI per county, /wp-check wording (e0cdf3b) · Local Dominator registered for S10 (d0c6425) · reviews.py reads
`google_reviews_search` (a5c57eb) · PAA resume + one retry (6487a4c) · balance rate-limit + fan-out resume (990b381) ·
PAA `--max-cities`/`--search-from` (b98efbc) · Gettysburg: branch merged, logged Drive mirror, health-adjacent category
(CM-040), safe-fix cap.

**To do in this rewrite** (beyond R1–R8):
| # | Note (date, source) | Do |
|---|---|---|
| 1 | Access block asks who has GBP/domain/hosting/Facebook + GSC/GA4 (Paul 10-06) | `templates/proof-sheet.md` Access = one row: "please add us as a Manager on your Google Business Profile". No GSC/GA4 ask. |
| 2 | FAQ/PAA used "just because" (Paul 10-07) | Rule in `writing-commercial.md` + build agent + specs: a routed question is a candidate, not an obligation; a location FAQ must be about that town or the service there; cite in the site plan why each FAQ applies. |
| 3 | Residential roofer (Paul 10-06, decided 10-07) | Decision Sheet item "scope descriptor" — used as description in H1/body, never as a category variant unless Wikipedia-real. |
| 4 | Content sooner (Paul 10-08) | R2/R3/R6 + run the site plan in parallel with blockers (already allowed) and start the plan as soon as Approval 2 lands. |
| 5 | Phone placeholder on the proof sheet; Paul: no phone line | Remove the phone-offer line from the template. |
| 6 | Proof sheet never sent; answers arrived informally | "facts answered directly" path (R3) + an "informal client answers" capture saved verbatim as MANUAL evidence immediately. |
| 7 | `RETURNED` and `CLIENT COPY` names rejected by naming.py | Add both to `naming.py`; add an internal-notes pattern (Paul's answers file). |
| 8 | `run.py finish` refuses an answers-only proof-sheet run | Let a run record facts without re-marking an unchanged sheet. |
| 9 | Brand Guide template lacks author (CM-039) and D3 content-risk list; Section E N/S/E/W unmeasurable | Add author row + `### D3` to the template; drop N/S/E/W or define it as "towns at the edges". |
| 10 | APPROVED Drive copies still say "REVIEW" inside | Drive copy gets a stamped header (approved by Paul, date, sha); repo file unchanged. |
| 11 | Live page text capture (body text the basic crawl lacks) not registered | Register a free S05b "page text capture" in `crawl.py` + audit-steps.md. |
| 12 | `ingest_evidence.py` only reads the crawl; `crosscheck.py` runs 2 checks | Ingest `data/` outputs and settings into the manifest; add host-consistency, orphan and sitemap checks. |
| 13 | Scorecards: one per page type | Update the audit procedure and reviewer to expect one file per type. |
| 14 | Reviewer's signed name inside a review text | `reviews.py` strips a trailing sign-off line / flags texts ending in a capitalised name. |
| 15 | Rating "5.0" is rounded (66×5 + 1×2) | CM-020 proof quotes rating + count as Google shows on the day. |
| 16 | Fan-out seeds all on 2 cities; no group column | Spread seeds across services × cities; script writes a `group` column. |
| 17 | `paa.py` re-run wipes routing | Keep Intent/Route/Note by question text on re-run. |
| 18 | Crawl billed the 1,000-page cap for 72 URLs | `--max-pages` defaults to sitemap size × 1.5. |
| 19 | DataforSEO bills failed tasks (PAA cost +$0.05) | Cap retries per query at 1 (done) and report failed-task spend in the cost line. |
| 20 | Guard: blocks harmless text (record names in arguments, `cd &&`, credentials-file name in commit messages); read-only chains | Paul authorises: allow read-only chains and names inside quoted arguments; keep all write protections. |
| 21 | CAPTCHA registries, directory sites that block reads, GBP dashboard | One `manual_lookup` handoff to Gwen per client (done); now that Apex gave GBP manager access, add "read the GBP dashboard" to Gwen's standing list. |
| 22 | Admin login instead of a dedicated Editor (Apex) | Settled-decision slot: Paul keeps Admin or Jonie switches — asked once. |
| 23 | Non-WordPress site (Gettysburg = Astro) | `/new-client` detects the CMS; WordPress steps become N/A when not WordPress. |
| 24 | Document Checklist timestamp newer than its Drive copy | Moot with R4 (mirror inside finish). |
| 25 | Session opened in `~/CMS` (Gettysburg) | STATUS/`/next` say "start sessions in ~/Documents/seo-ops". |

## 6 · Order of work for the rewrite session
1. **Paul first:** install Google Drive for desktop and tell the session the v3 local path; say whether hooks may be
   edited for items R2, R8 and #20.
2. R1 models (agent frontmatter, `clerk` agent, next.py model line) → tests.
3. R4 Drive via local path + mirror inside finish → tests (fake local Drive folder in the sandbox).
4. R7 STATUS.md + R6 settled register and reopen flag → tests.
5. R6 Decision Sheet (template + discovery agent + next.py) and R3 gate consolidation + migration of the three existing
   clients → tests.
6. R2 session-per-stage enforcement → tests.
7. R5 summaries + read lists; §5 items 1–25 → tests.
8. Update CLAUDE.md (it is the SOP) to match; run `tests/run_all.py`; commit and push.
9. Apex resumes **in its own new session** at Build (§7).

## 7 · Apex Roofing of the Lowcountry — where it stands (2026-10-08)
See `clients/apex-roofing-of-the-lowcountry/STATUS.md` (written by hand for the VA handoff until R7 generates it).
In one line: **Discovery and audit are approved and signed off; next is Build — site plan + technical-blocker handoff to
Jonie; page specs still need Paul's approval before any page is written.**
