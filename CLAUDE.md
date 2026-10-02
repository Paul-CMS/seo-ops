# seo-ops — the Coastal Marketing SOP

This file **is** the SOP. Claude Code is the only tool: four subagents plus a reviewer,
twelve commands (`/next` runs whatever comes next), one gate file per client, and an
append-only safety log. The methodology (the rules) lives in `sop-source/` and `methodology/`;
this file is the procedure (who does what, in what order, behind which gate).

**Paul decides. The system prepares, checks, logs and stops.**

---

## 1 · Step zero — every command, every session

1. Read `methodology/agency-profile.md`. Never re-ask anything it answers (crawler, JS
   rendering, tools, who decides what).
2. `python3 scripts/status.py show <slug>` — where the client stands, which gates are met.
3. Read the client's Handoff Log (`clients/<slug>/handoff-log.md`, mirrored to Drive) — the
   last section says what the next step needs.
4. Skim `methodology/lessons.md` for corrections since you last ran.

## 2 · The run protocol — no exceptions

Every command that does work:

1. **Start:** `python3 scripts/run.py start <slug> <command> --gates <g1,g2,...>`
   - exit **4** → a gate is not met. **Refuse.** Tell Paul in plain language which gate and
     what it unlocks. Never work around it.
   - exit **3** → an unfinished earlier run exists. **Stop and ask Paul**: resume it, verify
     it (`/verify`), roll it back (`/rollback`), or abort it (Paul's call only).
2. **Act.** Log every change *as it happens*:
   `python3 scripts/run.py change <slug> <RUN_ID> --kind K --url U --field F --old V --new V --result R`
   (wp.py, handoff.py, verify.py and crawl.py log for you). A file written to Drive is a
   change too (`--kind drive_file --channel drive`, URL = the Drive link).
3. **Hand off:** append this run's section to `clients/<slug>/handoff-log.md` (template in
   `templates/handoff-log.md`) and mirror it to the Drive Handoff Log.
4. **Finish:** `python3 scripts/run.py finish <slug> <RUN_ID> --summary "..." --phase "..." --next "..." [--done "..."] [--waiting "..."]`
   This writes FINISHED, updates `client_view`, and **commits to git (and pushes)**.

A run that stops early stays STARTED in the log on purpose — that is how the next command
knows to stop and ask.

## 3 · Gates — status.json, set only by Paul with /approve

`clients/<slug>/status.json` holds every gate. **Only `/approve`, typed by Paul, sets one**
(a hook issues a one-time token only for a real `/approve` prompt; a guard hook blocks
direct edits). An approval names the exact file versions it approves; if a file changes
afterwards, the gate stops counting as met until Paul re-approves. Decisions: `approved` ·
`approved_with_conditions` (each condition becomes a blocker in the next agent's sequence) ·
`revise` · `deferred` · `rejected` · `blocked`.

### Full client — the order

| # | Step | Command | Needs | Ends at decision (Paul) |
|---|---|---|---|---|
| 1 | Intake, Drive folder, document checklist (S01) | `/new-client` | — | — |
| 2 | Discovery + entity research (S02–S03), public sources | `/discovery` | — | **b1_entity** |
| 3 | Proof sheet (S04), Markdown + client Google Doc | `/discovery proof-sheet` | b1_entity | **b1_proof_sheet_ready** — Paul sends it |
| 4 | *While the client has the sheet:* crawl (S05), reviews, rankings, backlinks, citations, grid, GSC (S06–S11) | `/crawl`, `/discovery data` | b1_proof_sheet_ready | — |
| 5 | Audit: entity → architecture → page conformance → technical, then fresh-context review (S12–S18) | `/discovery audit` | every step has an outcome | **b1_audit** → implementation gate 1 |
| 6 | Client returns sheet → reconcile into the Brand Guide | `/discovery reconcile` | b1_proof_sheet_returned | **b1_brand_guide** → implementation gate 2 |
| 7 | Block 1 (Agent 1 never starts Agent 2) | `/discovery block1` | 1.1–1.5 | **block1** |
| 8 | Technical blockers (Low items as one handoff) | `/build blockers` + `/implement` | block1 | **b2_blockers** |
| 9 | **Site plan** — every service and location page in one pass | `/build plan` | block1 | **site_plan** |
| 10 | **Pilot** — 1 service + 1 location brief; corrections go into the specs | `/build batch pilot` | site_plan | **batch:pilot:briefs** |
| 11 | **Batches of ~5** — service by cluster, location by county (hub + cities); briefs, then drafts, then `/implement`, `/verify`, write-back | `/build batch <id>` … | pilot corrections applied | **batch:<id>:briefs**, **batch:<id>:drafts** |
| 12 | All pages live and written back | `/build block2` | every batch written back | **block2** |
| 13 | Link wheel → verify | `/finish wheel` | block2 | **block3** |
| 14 | Schema → QA crawl → punch-list → acceptance | `/finish schema`, `/finish qa` | block3 | **block5** (release) |
| 15 | Blog Decision Map → redirects (handoff) → posts | `/blog` | block5 | **block4**, then **page:<id>** per post |

Every step's data is saved once per client and reused (re-run if older than 60 days).
`/next <slug>` reads status.json and runs whatever comes next, stopping at the next decision.

### Blog-only client (Blog Authority Builder)

Short intake → entity foundation (**b1_entity**) → topic list checked against the service and
location page FAQs (**bab_topics**) → one optimized post at a time (**page:<id>** each). No
proof sheet, no site audit, no rebuild. Inputs: services list, city list, voice guidance,
customer language.

## 4 · Implementation — what can change, behind which gate

| Gate | Unlocks | Channel |
|---|---|---|
| **Gate 1 · impl_safe** = b1_audit | Client-independent fixes: broken links, alt text, image URLs, sitemap, robots.txt, **meta description** duplicates, speed | Alt text via wp.py; the rest as VA handoffs |
| **Gate 2 · impl_structural** = b1_entity + b1_brand_guide | Redirects, URL/slug changes, consolidations, **SEO titles and H1s** | Always VA handoffs (titles via wp.py only after the pilot) |
| **batch:<id>:drafts** | That batch's approved content (`page:<id>` for blog posts) | WordPress **draft** |
| block2 / block3 | Link tables / schema | Draft / Kadence head field after the pilot |

Rules enforced in the scripts as well as here:

- **Check the current value before every change; skip what is already done; stop if the live
  value is not what the audit recorded.**
- **Drafts by default.** A published page changes only with `--live` *and* Paul's
  confirmation of a fresh ManageWP backup, recorded in the log.
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

Build works in batches: one **site plan** for every service and location page (keyword, area
variant, H1 decision with the "The Best" test, FAQ topics, link targets; checked across the
site for duplicates, variant conflicts and FAQ overlap) → a **1+1 pilot** → batches of about
5. Service batches are written back to the Brand Guide before any location batch; homepage
and about last. Plan and batches live in status.json → `build`.

**Sensitive clients** (chiropractic, medical, insurance, legal, financial — flagged at
`/new-client`): content needs Paul's `/approve` with the human review recorded; for medical
and chiropractic, the client's licensed practitioner signs off on health claims and the
approval records who. Nothing goes live without it.

## 6 · Methodology — what governs

Authority, highest first: platform requirement → legal/truth → Paul's rulings
(`methodology/coastal-delta-addendum.md`, CM-019+) → the Coastal Delta
(`sop-source/Coastal-Delta-v1.0.md`, each entry's own status) → the Bradley Standard
(`sop-source/BB-Standard-v1.0.md`, with BB-601–608 **replaced** by
`BB-Standard-Schema-Section-v1.1.md`; woodlawntrees.com is the schema reference, schema only)
→ GOV-06 (procedure for new conflicts). Treat the Standard and the Delta as in force despite
their DRAFT labels. Cite rule IDs; never restate a rule as if it were new.

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

A methodology correction goes in `methodology/lessons.md` with its reason, and (if it is a
ruling) in the addendum.

## 7 · Independence

Auditing and writing never share a context (CM-017, CM-018, RULE-011). The audit self-check
runs in the **audit-reviewer** subagent, which sees only the registers, inventories, manifest,
cross-checks and decisions — never the analysis conversation. Content QA in Finish runs in
the Finish subagent, never the Build subagent that wrote the copy. Log "Claude performed both
analysis and review — Paul Exception, mitigated by fresh-context reviewer" in
`clients/<slug>/decisions.md` on every audit.

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
  `Resources/`). They are not part of this system. Do not edit, move or mark them without Paul.

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
  blocked). Estimate first. Over **$2** → ask Paul and wait. More than the remaining balance →
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
  decisions.md       exceptions, defaults, N/As (append)
  handoff-log.md     mirror of the Drive Handoff Log
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
