# seo-ops — the Coastal Marketing SOP

This file **is** the SOP. Claude Code is the only tool: four subagents plus a reviewer,
thirteen commands (`/next` runs whatever comes next), one status file per client, and an
append-only safety log. status.json and log.md are the only records written; everything a
person reads (Handoff Log, decisions summary, Document Checklist, Approval Record) is generated
from them one-way by `scripts/records.py`. The methodology (the rules) lives in `sop-source/` and `methodology/`;
this file is the procedure (who does what, in what order, behind which gate).

**Paul decides. The system prepares, checks, logs and stops.**

---

## 1 · Step zero — every command, every session

1. Read `methodology/agency-profile.md`. Never re-ask anything it answers (crawler, JS
   rendering, tools, who decides what).
2. `python3 scripts/status.py show <slug>` — where the client stands, which gates are met.
3. Read the client's Handoff Log (`clients/<slug>/handoff-log.md`, generated, mirrored to Drive) —
   the last section says what the next step needs.
4. Rules come from `methodology/rulings.md` (cite IDs; never restate). `methodology/lessons.md` is
   an inbox of proposals — nothing in it is in force.

## 2 · The run protocol — no exceptions

Every command that does work:

1. **Start:** `python3 scripts/run.py start <slug> <command> --gates <g1,g2,...>`
   - exit **4** → something it needs is missing. **Refuse.** Tell Paul in plain language what is
     missing (the script's message says it) and what to do first. Never work around it.
   - exit **3** → an unfinished earlier run exists. **Stop and ask Paul**: resume it, verify
     it (`/verify`), roll it back (`/rollback`), or abort it (Paul's call only).
2. **Act.** Log every change *as it happens*:
   `python3 scripts/run.py change <slug> <RUN_ID> --kind K --url U --field F --old V --new V --result R`
   (wp.py, handoff.py, verify.py and crawl.py log for you). A file written to Drive is a
   change too (`--kind drive_file --channel drive`, URL = the Drive link).
3. **Decisions and hand-off:** a decision during the run (Paul Exception, applied default, N/A,
   deviation, Gate B outcome) → `run.py decision <slug> <RUN_ID> --text "..." [--ids F-001]`.
   Write this run's Handoff Log section (template `templates/handoff-log.md`) to
   `clients/<slug>/handoffs/run-<RUN_ID>.md` and pass it to finish. Never edit handoff-log.md,
   decisions.md, document-checklist.md or approval-record.md — they are generated.
4. **Finish:** `python3 scripts/run.py finish <slug> <RUN_ID> --summary "..." --handoff clients/<slug>/handoffs/run-<RUN_ID>.md --phase "..." --next "..." [--done "..."] [--waiting "..."]`
   This writes FINISHED, logs any condition newly met, regenerates the records, updates
   `client_view`, and makes the run's **one git commit (and push)**. Mirror the regenerated
   Handoff Log and Approval Record to Drive.

A run that stops early stays STARTED in the log on purpose — that is how the next command
knows to stop and ask.

## 3 · Decisions and conditions

`scripts/gates.json` names every gate by what it means. Two kinds:

- **Decisions** — Paul's, set **only by `/approve`** typed by Paul (a hook issues a one-time token
  only for a real `/approve` prompt; a guard hook blocks direct edits). **Every approval names the
  exact files it covers** — the producing step records them with `status.py mark <slug> <artifact>
  --file …`; approve.py refuses an approval with no files. If one of those files changes, **only
  that decision** stops counting; later ones stay open and `/resume` flags them "upstream change —
  check whether it affects this". Paul decides. One `/approve` line may approve several decisions
  at once (`/approve <slug> a b c`), each with the files its step recorded. Decision values:
  `approved` · `approved_with_conditions` (each condition becomes a blocker in the next agent's
  sequence) · `revise` · `deferred` · `rejected` · `blocked`.
- **Conditions** — facts the scripts check from evidence, never approved, logged in log.md the
  first time they are met: `client_setup` (/new-client finished), `proof_sheet_returned` (the
  returned sheet is recorded), `audit_steps_complete` (every audit step has an outcome),
  `pages_built` (every batch built and written back).

`/next` passes every condition automatically when its evidence exists and stops at every
decision, printing the exact `/approve` line with its files. Refusals are in plain language.

### Full client — the order

| # | Step | Command | Needs | Ends at decision (Paul) |
|---|---|---|---|---|
| 1 | Intake, Drive folder, document checklist (S01) | `/new-client` | — | condition **client_setup** |
| 2 | Discovery + entity research (S02–S03), public sources | `/discovery` | — | **entity_approved** |
| 3 | Proof sheet (S04), Markdown + client Google Doc | `/discovery proof-sheet` | entity_approved | **proof_sheet_approved** — Paul sends it |
| 4 | *While the client has the sheet:* crawl (S05), reviews → customer language, rankings + cannibalization, backlinks, citations, grid, GSC, People Also Ask (S06–S11, S19) | `/crawl`, `/discovery data` | crawl: client set up · data: proof_sheet_approved | — |
| 5 | Audit: entity → architecture → page conformance → technical, then fresh-context review (S12–S18) | `/discovery audit` | condition **audit_steps_complete** | **audit_approved** → safe fixes |
| 6 | Client returns sheet → record it, reconcile into the Brand Guide | `/discovery sheet-returned`, `/discovery reconcile` | proof_sheet_approved / condition **proof_sheet_returned** | **brand_guide_approved** → structural changes |
| 7 | Discovery sign-off (Agent 1 never starts Agent 2) | `/discovery signoff` | all of the above | **discovery_signed_off** |
| 8 | Technical blockers (Low items as one handoff) | `/build blockers` + `/implement` | discovery_signed_off | **blockers_cleared** |
| 9 | **Site plan** — every service and location page in one pass | `/build plan` | discovery_signed_off | **site_plan** |
| 10 | **Pilot** — 1 service + 1 location brief; corrections go into the specs | `/build batch pilot` | site_plan | **batch:pilot:briefs** |
| 11 | **Batches of ~5** — service by cluster, location by county (hub + cities); briefs → drafts + self-critique + **semantic review table** → apply approved SEM IDs → `/implement`, `/verify`, write-back | `/build batch <id>` [`drafts`\|`apply-sem`] … | pilot corrections applied | **batch:<id>:briefs**, **batch:<id>:sem** (SEM IDs), **batch:<id>:drafts** |
| 12 | All pages built and written back | — | every batch written back | condition **pages_built** (no approval) |
| 13 | Link wheel → verify | `/finish wheel` | pages_built | **link_wheel_approved** |
| 14 | Schema → QA crawl → punch-list → acceptance | `/finish schema`, `/finish qa` | link_wheel_approved | **release_approved** (release) |
| 15 | Blog Decision Map → redirects (handoff) → posts | `/blog` | release_approved | **blog_map_approved**, then **page:<id>** per post |

Every step's data is saved once per client and reused (re-run if older than 60 days).
An imported client (`/new-client --import`) gets its live pages as an approved baseline and a
generated site plan; `/next` resumes at its real stage.
`/next <slug>` reads status.json and runs whatever comes next, stopping at the next decision.

### Blog-only client (Blog Authority Builder)

Short intake → entity foundation (**entity_approved**) → topic list checked against the service and
location page FAQs (**blog_topics_approved**) → one optimized post at a time (**page:<id>** each). No
proof sheet, no site audit, no rebuild. Inputs: services list, city list, voice guidance,
customer language.

## 4 · Implementation — what can change, behind which gate

| Gate | Unlocks | Channel |
|---|---|---|
| **safe_fixes_allowed** = audit_approved | Client-independent fixes: broken links, alt text, image URLs, sitemap, robots.txt, **meta description** duplicates, speed | Alt text via wp.py; the rest as VA handoffs |
| **structural_changes_allowed** = entity_approved + brand_guide_approved | Redirects, URL/slug changes, consolidations, **SEO titles and H1s** | Always VA handoffs (titles via wp.py only after the pilot) |
| **batch:<id>:drafts** | That batch's approved content (`page:<id>` for blog posts) | WordPress **draft** |
| pages_built / link_wheel_approved | Link tables / schema | Draft / Kadence head field after the pilot (must-use plugin `wordpress/mu-plugins/seo-ops-head-meta.php`, key set at the pilot) |

Rules enforced in the scripts as well as here:

- **Check the current value before every change; skip what is already done; stop if the live
  value is not what the audit recorded.**
- **Drafts by default.** A published page changes only with `--live` *and* Paul's
  confirmation of a fresh ManageWP backup, recorded in the log.
- **Handoffs go to the owner of the work** (gates.json `owner`): WordPress, technical, redirect and
  title/meta work → Jonie; citations, GBP, content review and everything else → Gwen. Redirect rows
  get `301` filled in and always use full URLs, never bare slugs.
- **Redirects are never implemented by the system.** Every redirect is a VA handoff (from URL,
  to URL, 301, reason, URL Decision Map ref). A slug change is a URL change: it waits for gate
  2 and always comes with its redirect handoff. `/verify` checks each after the VA marks it done.
- **Until the WordPress pilot is done** (`config.json` `wp_pilot_done`), SEO titles, meta
  descriptions, slugs and schema go out as VA handoffs (Jonie). SEOPress exposes titles and
  descriptions at `PUT /wp-json/seopress/v1/posts/{id}/title-description-metas`; the Kadence
  per-page head-code meta key is read on the pilot site.
- Destructive candidates follow CM-019 (§6). Never delete; always redirect.

## 5 · Routes for page content (Build)

- **Route A (normal):** brief → content → Paul's approval → Brand Guide write-back.
- **Route B (Paul writes):** Paul provides finished content → the Build agent sanity-checks it
  against the rules (it lists issues; it never rewrites Paul's copy) → Paul's approval →
  Brand Guide write-back → handoff to the VA.

Every page type has a spec in `methodology/specs/` (homepage, service, location, county hub,
about, blog post): element order and numbered conformance checks. Build and the audit read them;
a spec marked DRAFT stops building that page type until Paul approves it; pilot corrections are
logged in the spec. Writers follow `methodology/writing-commercial.md` (E1–E9, then the Stage 4
semantic review, one table per batch, report only; Paul approves SEM IDs once per batch) and
`methodology/writing-blog.md` (E1–E8, CM-038 link caps, CM-039 author).

Build works in batches: one **site plan** for every service and location page (keyword, area
variant, H1 decision with the "The Best" test, FAQ topics, link targets; checked across the
site for duplicates, variant conflicts and FAQ overlap) → a **1+1 pilot** → batches of about
5. Service batches are written back to the Brand Guide before any location batch; homepage
and about last. Plan and batches live in status.json → `build`.

**Sensitive clients (CM-025)** — matched by category at `/new-client` (health, legal, insurance,
financial; term lists in `config.json`); when unsure, `/new-client` asks Paul. Content needs
Paul's `/approve` with the human review recorded; for health categories the client's licensed
practitioner signs off on health claims and the approval records who. Nothing goes live without it.

## 6 · Methodology — what governs

**`methodology/rulings.md` > the Bradley Standard (`sop-source/BB-Standard-v1.0.md`, APPROVED, with
BB-601–608 replaced by `BB-Standard-Schema-Section-v1.1.md`; woodlawntrees.com is the schema
reference, schema only) > everything else.** Platform requirements and legal/truth limits bind
every rule. rulings.md holds every Coastal ruling (CM-###), the Rule Register (RULE-###), the
GOV-06 procedure for new conflicts (PROC-01) and the resolved Conflicts Register. Skills, agents
and writer standards cite IDs; never restate a rule as if it were new. New proposals go to
`methodology/lessons.md` (inbox) until Paul moves them into rulings.md.

The rulings that most change daily work:

- **"The Best" (CM-020)** — not a default. Only when demand, opportunity, proof and
  not-sensitive all pass; never touch the H1 of a page already top 3 for its main keyword;
  log the evidence in the URL Decision Map and Brand Guide Section H. A missing "The Best" is
  never a finding by itself.
- **Linking (CM-022)** — Bradley/Delta govern service and location pages: full city mesh,
  table/H3 links, never in prose. `updated-link-strategy` governs blog posts and link QA, and
  may *propose* one high-value contextual link or outbound authority link per page as a
  logged exception for Paul's approval in Finish.
- **Destructive without GSC (CM-019)** — candidate only if DataforSEO shows no top-100
  rankings and no referring domains, not a GBP/citation destination, and the client confirms
  no leads. Otherwise `Needs Evidence`. No research support → no recommendation.
- **Blog redirects (CM-021)** — need GSC or DataforSEO showing both URLs ranking for the same
  query. Test B (protected posts, CM-007) runs first.
- **Location pages (CM-023)** follow BB-315's sections; **variants (CM-024)** are a shared
  pool, only the homepage's reserved variant is exclusive.
- **No invented facts (CM-016)** — write `[NEED: …]`. Unknown/Disputed Brand Guide fields block.
- **Discovery is not the audit.** No severity, priorities or recommendations before the audit
  step. Conflicts are recorded in `methodology/conflicts-register.csv`, never resolved inside
  the work (GOV-06 §5).

A proposed methodology correction goes in `methodology/lessons.md` (inbox) with its reason; it is
in force only once Paul moves it into rulings.md with an ID.

## 7 · Independence

Auditing and writing never share a context (CM-017, CM-018, RULE-011). The audit self-check
runs in the **audit-reviewer** subagent, which sees only the registers, inventories, manifest,
cross-checks and decisions — never the analysis conversation. Content QA in Finish runs in
the Finish subagent, never the Build subagent that wrote the copy. Claude doing both analysis
and review is one standing exception (CM-026); the audit cites CM-026 in `decisions.md` rather
than re-logging an exception each time.

## 8 · Drive

- One folder per client: `[Client Name] - TMS` at the root of `v3. CMS Technical SEO Audit 2026`,
  copied from `_CLIENT FOLDER TEMPLATE - copy per client`. Audits reference only that folder.
- Every file follows `methodology/naming-convention.md` (check with `scripts/naming.py`).
  Content: `[CODE] - [Service or Location] - [Client]`. Deliverables:
  `[Client] - [Artifact] - [STATUS].md`. Evidence:
  `[Client] - [SF|LNKD|BL|GSC|GA4|CMS|DFS|MANUAL] - [export] - [date].ext`.
- Write real `.md` files (no Google Docs conversion). The only Google Doc the system creates
  is the proof sheet's client copy, named `- CLIENT COPY`.
- Never rename or delete existing Drive files. Renames go on a rename list for Paul.
- Never use the pre-Claude-Code instruction files (old agent and writer instructions in Drive
  `Resources/` — Gem Instructions, Agent Instructions). They are not part of this system. They are
  archived only through `/archive-old-instructions`: it lists them, **asks Paul file by file**, and
  moves only the ones he says yes to into `Resources/_Archive/` (logged). Nothing else touches them.

| Artifact | Drive location |
|---|---|
| Evidence (crawl tables, BL, GSC) | `01 - Discovery and Audit/Evidence/` |
| Discovery Record, Proof Sheet, Finding Register, URL Decision Map, Recommendations, Evidence Manifest | `01 - Discovery and Audit/Deliverables/` |
| SB/LB/HB/AB briefs, SD/LD/HD/AD approved drafts, Technical Blocker Checklist, build handoffs | `02 - Build/` |
| Link Wheel Tables, schema, QA Punch-List, acceptance sheets | `03 - Finish/` |
| Blog Decision Map, PB/PD, refresh schedule | `04 - Blog/` |
| Brand Guide, Approval Record (mirrored from status.json), Document Checklist, Handoff Log | client folder root |

## 9 · Money, credentials, contact

- **DataforSEO:** every call through `scripts/dfs.py` / `scripts/crawl.py` (the connector is
  blocked). Estimate the **whole run** first (multi-call scripts check the run total before the
  first call; every call also counts what the run already spent). Over **$2** → ask Paul and wait. More than the remaining balance →
  **stop and tell Paul; do not start.** Every call's actual cost is logged.
- **Credentials:** `.env` only, typed by Paul. Never read, print, paste or commit it. Scripts
  load it themselves.
- **Nothing goes to a client automatically.** The system prepares; Paul sends.
- Any other spend (citations, links, press releases) needs Paul's explicit approval with
  provider, cost and renewal (RULE-014). Off-page work runs outside this system.

## 10 · Per-client files (repo)

```
clients/<slug>/
  status.json        gates, pages, client_view   (scripts only)
  log.md             safety log, append-only      (scripts only)
  changes.jsonl      machine copy for /rollback   (scripts only)
  snapshots/         old/new content for rollback (scripts only)
  decisions.md       decisions summary         (generated by records.py)
  handoff-log.md     Handoff Log               (generated; mirrored to Drive)
  document-checklist.md                        (generated)
  approval-record.md Approval Record           (generated; mirrored to Drive)
  brand-guide.md     working copy of the Drive Brand Guide
  discovery/ audit/ build/ finish/ blog/ handoffs/
  inputs/            raw evidence and crawl (git-ignored)
  dfs-costs.jsonl    DataforSEO spend
```

`status.json` → `client_view` is the **only** client-facing part (phase, done, waiting on
client, next — plain language, no jargon, no rule IDs, no internal names). Nothing else in
status.json or the repo is ever shown to a client.

## 11 · Talking to Paul

Plain language. Say what was done, what is waiting on whom, and what the next command is.
When refusing, say which gate is missing and what it would unlock. Never claim a check passed
if it was skipped.
