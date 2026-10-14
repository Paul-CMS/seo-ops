# Home Mobile Medical — readiness for the services-section test run (rewrite 3 §10)

Prepared 2026-10-14 in a system session, from a read-only copy of HMM's files (nothing was written to
`clients/home-mobile-medical/`). Each line: **ready** or **missing**, and the exact fix.

| # | Item | State | What is true | Fix |
|---|---|---|---|---|
| 1 | Site plan | **missing — approval voided** | The plan (`Home Mobile Medical - Site Plan - REVISED.md`) was approved 2026-10-09, then edited (file sha `99199b5f08eb`, approved `acd2d040d2df`), so `/next` asks for approval again. Content is in shape: 33 pages, root-proximate URLs pass `urlcheck` (no problems), 2 hubs (`hilton-head-bluffton-metro`, `charleston-metro`), 30 pages carry their old URL under `replaces` (the 301s). | Paul reads the plan, then types `/approve home-mobile-medical site_plan --files "clients/home-mobile-medical/build/Home Mobile Medical - Site Plan - REVISED.md"` |
| 2 | Places | **missing — all 24** | `places.py status` lists 24 planned towns with no place or niche research. The place store is new, so nothing is reusable yet (Apex's town research lives in `methodology/sources/` lists, not in the store). The niche is taken from HMM's Brand Guide: **mobility equipment supplier** (primary category *Mobility equipment supplier*; services from the plan: Stair Lifts, Curved Stair Lifts, Porch Lifts / Vertical Platform Lifts, Wheelchair Lifts, Stair Lift and Lift Repair and Maintenance). Once these 24 are researched, Apex gets the **place layer** for any shared town (Beaufort, Bluffton, Hilton Head Island, Okatie, Port Royal, Hardeeville, Ridgeland, Lady's Island, Levy) free; only a roofing niche layer would be new for Apex. | In HMM's folder: `python3 scripts/places.py status home-mobile-medical`, then per town `python3 scripts/places.py prompt home-mobile-medical "Beaufort, SC"` (all 24 prompts render; the prompt for each town is `build/places/prompts/<town>-mobility-equipment-supplier.md`) → Gemini Deep Research → save as `clients/home-mobile-medical/inputs/places/<town>-mobility-equipment-supplier.md` → `places.py ingest` → `places.py verify`. Towns: Beaufort, Bluffton, Charleston, Daufuskie Island, Edisto Island, Folly Island, Goose Creek, Hanahan, Hardeeville, Hilton Head Island, Hollywood, Kiawah Island, Lady's Island, Laurel Bay, Levy, Moncks Corner, Mount Pleasant, North Charleston, Okatie, Port Royal, Ridgeland, Summerville, Walterboro, Yemassee. |
| 3 | Evidence packs | **missing** | No pack exists yet (`evidence.py run` builds them with the evidence gate, after the plan is approved). **Data on file not used yet** (12 input types, none read by a finished step): reviews (+ raw), review mentions, PAA (+ 20 raw), fan-out (+ 10 raw), blog inventory, entity profile, facts, settled decisions. | After item 1: `/next home-mobile-medical` runs `build:facts` (evidence gate and one pack per services-section page); `python3 scripts/manifest.py unused home-mobile-medical` lists what is still unread. |
| 4 | Facts | **ready** | `facts.json` has 39 rows. The de-duplication test on HMM's settled answers passes: all 3 settled/answered keys fed back as questions are dropped; there are no open questions, and `settled.py reconcile` would close nothing. | none |
| 5 | Homepage keyword / Search Console | **missing (both)** | Homepage keyword is not recorded — Paul picks it in an HMM session after the keyword research. No `* GSC * queries-homepage-90d *` file in `inputs/` (CR-024; the Document Checklist now lists it). | Paul picks the keyword in an HMM session. Export Search Console → Performance → Queries, Page = homepage, last 90 days, and save it as `inputs/Home Mobile Medical - GSC - queries-homepage-90d - 2026-10-14.csv`. |
| 6 | WordPress | **cannot verify here** | The system records `wordpress_connected` as met. A live test needs the `.env` credentials (never read here) and the network. | In HMM's folder: `/wp-check home-mobile-medical` — it must pass with the Editor-role user. |
| 7 | Models | **ready (as `gates.json` requires)** | Session (stage 5/6): **Haiku** chat. Services section: `build:facts` — clerk (Haiku) + researcher (Sonnet); `build:write` — briefs: brief-writer (**Sonnet**), drafts: build (**Opus** until Paul decides the side-by-side test; then draft-writer on Sonnet), batch review: build (Opus); `build:plan` — build (Opus); place research ingest/meaning check: researcher (Sonnet). `run.py start` refuses a stage on the wrong model when the session hook can see it. | none |
| 8 | First command | — | — | `python3 scripts/worktree.py open home-mobile-medical`, then a new **Haiku** chat in that folder, then `/next home-mobile-medical` |

## Also blocking HMM today

- **`page_specs_approved`:** `methodology/specs/location.md` is the new CM-062 structure and is a draft until Paul types
  **`/approve global specs:location`**. HMM has no drafted location page, so it needs the new spec; Apex keeps its
  structure (it already drafted location pages) and is not blocked.
- **Technical blockers:** the blocker handoff Jonie owns (`H-2026-10-09-03 … -04 …`, 14 rows) is still `issued`; it does
  not stop writing, but `/verify` has to clear it before ship.

## VA Worklist check on HMM (`worklist.py check`)

0 errors, 5 warnings — the five redirect targets have no WordPress draft yet (expected before drafting; they become
errors at the handover).
