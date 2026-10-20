# Rewrite 4 — smaller, cheaper, entity-first (implementation plan)

**Status:** APPROVED by Paul, 2026-10-20, with all six §1 defaults (D1–D6). Phase 0 built (4ae11e3). Phase 4 system
side built 2026-10-20 (cost split 20fbba5; brief-free route, D5 routes, pilot rule, three fact states, build.md 28 → 12 KB);
left for Paul: run HMM locations in its client session (one review sheet, one approval line) and the Sonnet drafting
test there. Phase 1 built 2026-10-20 (render.py, pipeline.py inventory, clerk retired, script-written handoff lines
capped at 25, outline.py formula). Phase 2 built 2026-10-20 (llm.py; five jobs on the API with the agent route as
the no-key fallback); left for Paul: type `ANTHROPIC_API_KEY` into `.env`. Next: Phase 3. Each
phase runs in its own `/system` session, in order, starting with Phase 0. Phases marked **design** run on Opus; the rest on Sonnet, from
this file as the written spec (CLAUDE.md → models).

**Goal.** Make every money page (home, service, location, hub) a correct Bradley entity node — brand + GBP category +
area entity, one page per service entity and per place entity, the link wheel and the schema — at a fraction of
today's tokens. Mechanical work moves into scripts (zero tokens), narrow judgment into direct API calls (small
tokens), and agents keep only exploration, URL decisions, the independent reviewer and the writing.

**Unchanged (the safety core):** Paul decides and sends; nothing goes to a client automatically; WordPress gets
drafts only; never delete, always redirect through the VA; check the live value before every change; never invent a
fact (`[NEED: …]`); DataforSEO estimate first, over $2 asks; a fresh-context reviewer on anything destructive;
writing and checking never share a context (CM-018). The client only ever sees the questions they need to confirm.

---

## 1 · Paul's choices (settled 2026-10-20: all defaults)

| # | Choice | Default (recommended) |
|---|---|---|
| D1 | Direct API calls from scripts (Phase 2) need `ANTHROPIC_API_KEY` in `.env` — you type it | **Yes** |
| D2 | Remove the brief step for new sections (Phase 4); the outline moves into the site-plan row | **Yes** |
| D3 | Approval 2 stays one line (audit + Brand Guide), or the URL decisions and blocker handoff are approved as soon as the audit is done | **Split**: the URL/blocker approval no longer waits for the client's sheet |
| D4 | Place research depth: core GBP city at full depth, every other planned town at "lite" depth | **Yes** |
| D5 | In-flight clients: HMM services finish on the old route (briefs already approved); HMM locations and every later section use the new route | **Yes** |
| D6 | Query fan-out (S21) off by default, on by `--fanout` | **Yes** |

---

## 2 · Phases

Each phase: build → `python3 tests/run_all.py` → new checks for each new behaviour → `--full` before the commit →
one commit. A phase that changes a stage's commands updates `docs/stage-*.md`, the agent file and `gates.json` in the
same commit. No phase edits client records by hand; migrations go through `scripts/migrate*.py`.

### Phase 0 — Measure (Sonnet, small)
The log already records each run's session id; Claude Code keeps every session's token usage (and its subagents')
in `~/.claude/projects/<project>/<session>.jsonl` and `<session>/subagents/*.jsonl`.
- New `scripts/usage.py run <slug> <RUN_ID>` and `usage.py client <slug>`: sum input, cache-write, cache-read and
  output tokens per run and per model, and price them (`dfs_prices.json` pattern → `model_prices.json`).
- `run.py finish` fills `--tokens/--cost` itself from `usage.py`; STATUS.md shows cost per stage.
- Back-fill the baseline: HMM and Apex, every run so far → `REWRITE-4-BASELINE.md` (cost per stage, top 10 runs).
- **Done when:** HMM's audit and services-brief runs have a real token and dollar figure. Every later phase is judged
  against this baseline.

### Phase 1 — Scripts take the clerical work (Sonnet)
- `scripts/render.py`: every Markdown deliverable and summary is rendered from its CSV/JSON by template — the audit
  review sheet, Evidence Manifest, URL Decision Map view, Technical Blocker Checklist, site plan MD, STATUS.md
  sections. Agents never type a rendered file again.
- `scripts/pipeline.py <slug> inventory`: crawl (S05) → page text (S05b) → one combined DataforSEO estimate → one
  `--confirmed` run of S06–S08, S19 (+S21 with `--fanout`) and competitor coverage → `ingest_evidence.py` →
  `crosscheck.py` → `conformance.py` → step outcomes recorded → render. Prints ≤10 lines. Paul can run it from the
  Terminal panel, or the stage chat runs it directly — no agent.
- **Retire the clerk agent for anything a script can run.** The stage chat calls scripts itself; the clerk is
  removed from agent files' "Cost discipline" sections.
- Logs and handoffs: scripts write the CHANGE/DECISION lines; agent-written handoff sections capped at 25 lines.
- **Added by Paul, 2026-10-20 — `outline.py` assigns keyword, H1 and variants by formula.** When the site-plan row leaves
  them empty (HMM's locations rows have none), `outline.py` assigns them from the Brand Guide and the page spec, so the
  writer never chooses them. Rules (each shown beside its value in the outline's `## Assigned by formula`, and recorded in
  the page's `assigned`):
  - *Location:* keyword = core service keyword (Brand Guide C1 `keyword "…"`, first service row) + city + state
    abbreviation; H1 = `[category variant] in [City]`, no state, where the variant is the first A3 category variant that
    is neither the GBP primary category (the title slot) nor the homepage's reserved B1 variant (BB-304, CM-024);
    area variant (opening) = the B2 pool entry that names the page's own hub, else left open — never a rotation, which
    could put a city in the wrong county.
  - *Service:* keyword = C1 `keyword` for the URL, else the service name; H1 = `[service variant] in [first B2 area
    variant]` (variant from C1, else the plan's `service_variant`, else the name; never a city, never B1's reserved one).
  - *Never assigned:* county hubs (the same-named city's H1 would repeat; the format still waits on Paul's ruling), the
    homepage (H1 lock, HP-08) and about. A value the approved plan fixes is never overridden; one the Brand Guide cannot
    support stays open for the writer and the review sheet. Check against HMM: Bluffton → keyword "stair lifts Bluffton
    SC", H1 "Stair Lift Installer in Bluffton" — the Beaufort pilot's approved pattern.
- **Built 2026-10-20.** `scripts/render.py` (manifest · urlmap · findings · auditsheet · blockers · siteplan · status ·
  all · check; `--out`; refuses to render over a file an approval covers); `scripts/pipeline.py <slug> inventory`
  (`--phase data|audit|all`, `--confirmed`, `--dry`, `--fanout`; one combined estimate → exit 5; first failure stops;
  outcomes recorded by the script; exit 10 = crawl still running); the clerk agent removed (agent file, stage and model
  rows, docs); `run.py finish` refuses an agent handoff over 25 lines and adds the script-written record (changes by
  kind, decisions/facts/flags, step outcomes); tests in `tests/checks/rewrite4_phase1.py`.
- **Done when:** a dry run of `pipeline.py inventory` on HMM's saved data reproduces the S12 outputs with no agent.
  **Result:** `pipeline.py home-mobile-medical inventory --dry` runs with no agent and writes nothing in HMM's folder. It
  reproduces what the scripts derive from the files on disk. It cannot
  reproduce the audit's hand-edited manifest rows (Local Dominator PDFs read in Drive, typed MANUAL exports) or the
  files that were added after the audit on 2026-10-07 (fan-out, later pulls): 10 of the audit's 27 manifest files match
  exactly (all 8 crawl exports, the citation tracker, the blog inventory) and 3 of 8 cross-check lines. A script re-run of a **live** audit keeps the manifest's setting columns and the
  recognised type of an unchanged file, so a re-run does not lose that hand work. Not reproduced here: the S13–S18
  judgment, which Phase 3 slims.

### Phase 2 — Direct API calls for narrow judgment (Sonnet; needs D1)
- `scripts/llm.py`: one call = model + a short fixed prompt + a JSON schema + the input file; prompt caching on the
  fixed part; every call logged to `clients/<slug>/llm-costs.jsonl` (same shape as `dfs-costs.jsonl`); refuses
  above a per-run cap from `config.json` without Paul's yes.
- Move these jobs onto `llm.py` (Haiku unless noted):
  - PAA and fan-out routing (S19, S21)
  - review-mention meaning checks (CM-057; Sonnet)
  - `places.py judge` meaning checks (Sonnet)
  - FAQ fit picks in the site plan (Sonnet)
  - conformance judgment columns for kept pages (Sonnet)
  - mechanical QA explanations
- **Done when:** these jobs run without an agent session and each has a regression check on HMM data.
- **Built 2026-10-20.** `scripts/llm.py` (stdlib urllib; structured output via `output_config.format` JSON schema;
  the fixed prompt + the job's context cached; `ANTHROPIC_API_KEY` from `.env`, sent only in the header; every call →
  `clients/<slug>/llm-costs.jsonl` + `status.json spend.llm_usd`; `config.json llm_run_cap_usd` = $1.00 per run, exit
  5 CONFIRM above it until `--confirmed`; fake mode `SEO_OPS_LLM_FAKE`). Jobs: `paa.py route` / `fanout.py route`
  (Haiku; run by `pipeline.py` after S19/S21), `reviews.py meaning` (after S06), `places.py judge-all`, `outline.py faq`
  (→ `build/<section>/faq-picks.json`, shown in each outline), `conformance.py judge` (kept pages →
  `audit/conformance-judgment.csv`). **Until a real key is in `.env` (missing, or a 401) nothing fails**: each job says
  once "no API key — ran on the agent route" and its agent does the work as before. `usage.py` and STATUS.md show the
  API spend beside the session spend. Tests: `tests/checks/rewrite4_phase2.py` on HMM's saved data
  (`tests/fixtures/hmm`, copied read-only): PAA 35/35 and fan-out 352/352 rows reproduce the agent's routing; HMM's 8
  review candidates read by meaning (explains 2 → 1 reviewer, "same day" is not a guarantee); FAQ candidates for
  Beaufort and Charleston from HMM's 124 location-routed fan-out rows; the 21 kept blog posts judged on all 22 BLG
  checks, the agent's S15 scorecard written back exactly.
  **Not done here:** mechanical QA explanations (they belong with `qa.py`, Phase 5); `places.py judge` has no HMM data
  to regress on (HMM's place research was never ingested), so its check uses a test place until Phase 6 stores Beaufort.
  The regression checks prove the plumbing on HMM's real rows; the model's own agreement with the agent is measured on
  the first live run once Paul types the key.

### Phase 3 — Slim audit (design, Opus)
- **Redirect pre-screen script** (`pagedec.py screen`): CM-019 conditions 1–3 computed from rankings, backlinks,
  GSC/GA4 and internal links → `pass / fail / needs evidence` per URL. The agent decides only the rows the script
  cannot settle, plus entity mismatches.
- **S15 becomes triage**: `conformance.py` alone writes one column in the URL map — `rebuild / light fix / keep`.
  Full spec scoring only for pages Build will not rewrite: blog posts, kept utility pages, Route B pages, the
  homepage under the H1 lock (HP-08). The per-type scorecard files and the reviewer's scorecard checks go.
- **S16 writes the Technical Blocker Checklist directly**; Build's blockers step only issues the handoff.
- **Audit onto CM-061**: severity becomes Fix · Fix and list · Ask; Gate B becomes the audit's one review sheet
  (`review.py sheet <slug> audit`). Most Asks are kind 1 (URL decisions).
- **Deliverables**: registers (CSV) + audit review sheet + Evidence Manifest, all rendered. The Recommendations
  document and the Markdown Finding Register are removed (internal only; the client sees only confirm questions).
- **Reviewer (S17)** scope: every destructive URL row and every Ask row, plus a sample of the rest; reads the
  registers only (CM-026 unchanged).
- D3: `audit_approved` no longer rides with `brand_guide_approved`; safe fixes and blockers unlock at the audit.
- Trim `seo-technical-audit` references to what the remaining steps need; target the audit read list under 25 KB
  (today about 66 KB).
- **Done when:** the audit re-run on HMM's saved data reproduces its 36 decided 301s and the reviewer's 7
  withdrawals, at a measured fraction of the Phase 0 baseline.

### Phase 4 — Slim build (design, Opus; needs D2, D5) — runs SECOND, right after Phase 0 (Paul, 2026-10-20)
- **Per-agent cost split first** (Phase 0 follow-up): `usage.py run|client --by-agent` splits each run's cost by
  the main chat and each subagent transcript (`<session>/subagents/*.jsonl`, named by agent type where the transcript
  says so), and the baseline gains a "cost by agent" table. It decides whether the Sonnet test or a cheaper
  coordinator saves more. **Built 2026-10-20 — result:** the `build` subagent (Opus) is $105.56 of Apex's $122.00
  and $22.55 of HMM's $29.28; the main chat is $7.39 and $1.28. The writer's model and context are where the money
  is — the Sonnet drafting test and the brief-free route come first; a cheaper coordinator saves at most ~$9.
- **No brief step.** The outline (element order from the spec, H2s, FAQ picks, links, the claims list) is
  **derived by a script at draft time** from the approved site-plan row + the spec — the approved plan file does not
  change, so HMM's approved site plan stays valid (no re-approval). The draft is written from that outline + evidence
  pack + spec + pilot corrections, one fresh subagent per page (CM-043 holds). Steps become: drafts → draft review →
  ship. One review sheet and one approval per section; the Brand Guide write-back moves to the draft approval.
- **In flight (D5):** a section whose briefs are already approved (HMM services) finishes on the old route; every
  section with no approved briefs (HMM locations and later) takes the new route. `migrate` marks which is which.
- **Pilot rule** (CM-061 §9): add "no pilot once the specs and writing rules are unchanged across the last 3
  clients' pilots with no corrections" (HMM's pilot: no corrections).
- **Sonnet drafting test**: run the existing `model:build:draft=sonnet` test on HMM's locations section; Paul compares
  it with the Opus pilot. Sonnet becomes the default writer only on his yes.
- **Writer-facing fact states**: the pack shows three states — confirmed · sourced public · unknown (→ `[NEED]`).
  The eight statuses stay inside `facts.json`; usage tiers are applied by `evidence_pack.py`, not by the writer.
- Trim `build.md` (28 KB) to the remaining steps; target under 12 KB.
- **Done when:** the tests run an HMM locations dry run from the approved plan to the draft review sheet with no
  brief step; then Paul runs HMM locations in its client session, ending in one review sheet and one approval line,
  and `usage.py` shows its cost per page against the Apex brief + draft baseline ($77.41 for its services and
  locations).

### Phase 5 — Finish folds into the plan (design, Opus)
- `scripts/wheel.py`: the Bradley link wheel from the site plan (service ↔ every location, hub ↔ its cities,
  homepage → hubs and services, CM-022 counts and placement) → link rows embedded in each page at draft time.
  CM-022 exceptions stay kind-1 Asks in the site plan. `[LINK → …]` placeholders only for pages not yet planned.
- `scripts/schema.py`: BB-6xx node sets from the Brand Guide + plan (the `bb-schema-builder` skill becomes the
  script's spec); asset gate kept; LocalBusiness never on a service page or a non-GBP location page; validator.
- `scripts/qa.py`: the mechanical QA (placeholders, links resolve, title/H1 formats, reading grade, schema valid,
  live value matches the approved file). `finish-qa` (Opus) only for sensitive clients (CM-025) and a sample.
- Ship: all pages drafted → links + schema in place → one VA worklist → publish together (Paul's memory: publish only
  after all drafts). `link_wheel_approved` is removed; `release_approved` stays.
- **Done when:** a dry ship on HMM's pilot pages produces the wheel rows and valid schema with no agent.

### Phase 6 — Shared research layers (Sonnet; needs D4) — see §3
- `methodology/niches/<niche>/`: `entities.json` (service entities) and `angles.md` (the niche module for the
  place prompt). One per niche, reused by every client in it.
- `places.py`: fill `place.json` identity from the Wikidata API (free, no LLM); the Deep Research prompt is built
  from the niche's `angles.md` instead of the roofing-shaped angles hard-coded today; `--depth full|lite` (D4).
- `places.py status` orders the work: core GBP city first, then towns by planned-page priority.
- Brand footprint prompt (optional) → sameAs candidates for schema and citation checks.
- **Done when:** Beaufort SC × stair lifts and Charleston SC × roofing exist in the store, verified, and HMM's
  location packs draw from them.

### Phase 7 — Prune the governance (design, Opus)
- Every ruling a script now enforces is reduced to one line naming the script; agent files point to IDs, never
  restate them.
- Review the 22 gates: keep the decisions Paul makes; any condition that is never false in practice becomes a check
  inside its script.
- Target: each agent file under 12 KB; each step's read list under 30 KB. Measured with `usage.py` against Phase 0.

Order and dependencies (reordered by Paul, 2026-10-20, from the Phase 0 baseline): **0 ✓ → 4 → 1 → 2 → 3 → 5**
(6 can run any time after 1; 7 last). Why: briefs + drafts were $77.41 of Apex's $122.00 measured, and HMM's
locations section is next; the audit is a small share of measured spend (its discovery and audit runs predate the
transcripts on this Mac, so its true cost is measured on the next client). Phase 4 should not start mid-section for
a live client.

---

## 3 · Research: what to research, at which level

Research by **entity**, at the level where a fact is true, once, and reuse it. Never research a service × city
combination: that is the page itself, composed from the layers below.

| Layer | Key | Done | Feeds | Tool |
|---|---|---|---|---|
| **Niche** | GBP primary category (the niche) | Once per niche, all clients | Service pages (entity, attributes, H2s, FAQs), category variants, state licensing | Deep Research (prompt A) → `niches/<niche>/entities.json` |
| **Place** | Town / county / region | Once per place, all niches | Location identity, Russian Doll chain, neighbourhoods, landmarks | Wikidata API script + Deep Research angles 6–7 |
| **Place × niche** | Town × niche | Once per pair, all clients in that niche | Location page local sections and the three FAQ categories | Deep Research (prompt B, existing `places.py prompt`, niche module) |
| **Brand** | The client | Once per client | Entity sheet, sameAs, NAP, claims | Discovery (S02) + optional prompt C |

**Core first:** the GBP primary category and the GBP city get full depth before anything else — they anchor the
homepage, the primary service page and the area entity. Other towns get the lite prompt (identity, neighbourhoods,
landmarks, the three FAQ categories); a town where even the lite prompt comes back thin becomes a merge proposal
(viability check, CM-061 §8).

**Industry-specific: yes, through the niche module.** The angles differ by niche. Roofing: wind, permits, HOAs,
insurance. Stair lifts: accessibility and lift codes, Medicare/Medicaid/VA programmes, home types with stairs.
Mold: humidity, flooding, disclosure, remediation licensing. Prompt B stays one frame; `angles.md` supplies the
niche's angles.

All three prompts run in Gemini Deep Research by the VA (no Claude tokens). `places.py ingest` → `verify`
(scripts) → Sonnet meaning check on what the script cannot confirm.

### Prompt A — Niche and service entities (once per niche)

```
You are mapping the {NICHE} industry as entities, for local businesses whose Google Business
Profile primary category is "{GBP_CATEGORY}", in the United States, current as of {YEAR}.
Say nothing about any specific company.

1. Category entity: the Wikipedia article and Wikidata ID that best match "{GBP_CATEGORY}";
   broader and narrower entities; real name variants people and Wikipedia use (no invented ones).
2. Service entities: for each of {SERVICES} (and any core service of this category missing from
   the list): Wikipedia article, Wikidata ID, common names/variants, parent/child services
   (a type of / part of), and whether it is a distinct entity or a sub-type.
3. For each service: its attributes — types and components, how the work is done (steps),
   what decides the cost (factors, not prices), lifespan/maintenance, safety standards and
   codes (e.g. ASME, ICC, NFPA) with the issuing body, federal rules, major manufacturers
   and their certification programmes.
4. State layer for {STATE}: the licence type required for this work, the licensing board's
   lookup page, the state building/accessibility code edition in force, state programmes
   or funding that pay for this work.
5. Questions customers commonly ask about each service, found in official, manufacturer or
   programme FAQs (not other contractors' blogs), each with its source.

Rules: every fact has its own source URL, publisher, source type (official / code body /
manufacturer / encyclopedia / news) and date; government > code bodies and manufacturers >
encyclopedias > news; never a contractor's website for a rule or code; "not found" with what
was searched rather than a guess.
Output: one table per section: id | entity or service | fact (one sentence) | source_url |
publisher | source_type | date | quote (max 25 words). Then "Not found": section | searched.
```

### Prompt B — Place × niche (existing `places.py prompt`, made niche-driven)
Keep today's frame and rules (official limits, unincorporated split, source priority, dated facts, import tables).
Replace angles 1–5 with the niche's `angles.md`; keep 6 (places and entities), 7 (identity) and 8 (local
questions). Lite depth (D4) asks only angles 6–8 plus one niche angle per FAQ category (local cost or decision ·
logistics in this area · trust in this area).

### Prompt C — Brand footprint (optional, once per client)

```
Find every public profile and mention of "{BRAND}" at {ADDRESS_OR_AREA}, phone {PHONE},
website {WEBSITE}, current as of {YEAR}: Google Business Profile, social profiles, directory
and citation listings, Secretary of State registration, licence board record, manufacturer
dealer/installer listings, BBB, local news and press, awards. For each: URL, the name,
address and phone exactly as shown, the date seen, and whether it matches the details above.
List former names, former addresses and former lines of business you find. Never infer;
list "not found" with what was searched.
Output: url | platform | name shown | address shown | phone shown | matches (yes/no/partly) |
date | note.
```
Feeds: sameAs candidates (schema), the citation/NAP check, and the Decision Sheet's history rows.

---

## 4 · The workflow after Rewrite 4

| # | Stage | Who | Paul sees |
|---|---|---|---|
| 1 | Entity sheet — discovery, entity research, Decision Sheet + client confirm list (niche and place layers reused) | Agent (Sonnet) + researcher; Deep Research by the VA | **Approval 1**; the client gets only the confirm list |
| 2 | Inventory — `pipeline.py inventory` (one cost yes) | Scripts | A cost line and a 10-line summary |
| 3 | URL + entity decisions — pre-screen, agent on the rest, reviewer, one audit review sheet | Opus (small input) + reviewer | **Approval 2** (URL Asks); blockers go to the VA |
| 4 | Site plan — pages, URLs, formulas, outline, FAQ picks, wheel, schema nodes, viability; one facts round | Scripts + `llm.py` + researcher | **Approval 3** + one client facts list |
| 5 | Write + ship — drafts per section, script checks, one review sheet, WordPress drafts with links and schema, VA publishes all together, `/verify` | Writers (Sonnet after the test) + scripts | **Approval 4** per section, one line |

Blog (Stage 8) is unchanged in this rewrite.
