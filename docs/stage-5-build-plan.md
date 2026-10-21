# Stage 5 — Build plan, blockers and the facts round

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: build (Opus), researcher (Sonnet).

| Step | Command | Ends at |
|---|---|---|
| Technical blockers — the audit wrote the checklist (S16); this issues one handoff to Jonie (worklist section 2) as soon as the audit is approved (D3); never holds up writing, gates release only | `/build blockers` + `/verify` | condition **blockers_cleared** |
| **Site plan** — every service, location and hub page in one pass; URL check (P7), competitor coverage | `/build plan` | **site_plan** |
| **One facts round** for every page (P10): grids, the researcher clears public facts, reviews attached, one question set grouped by fact | `/build facts` | answers recorded once (`run.py fact`) |

- URLs: one root slug per service, location and hub page — no folder, no city in a service slug, no service in a
  location slug, no `-2`; hubs are county or metro slugs (CM-058). `status.py plan` refuses anything else.
- **Pilot only when it is worth it** (CM-061 §9): `status.py pilot <slug>` — a client's first section, a new
  industry, or the first section after a spec or writing-rule change; otherwise all pages are drafted in one run.
- **Viability check** before the plan reaches Paul (`evidence_pack.py viability <slug> --all`): a location that
  cannot be sourced is proposed as a merge (kind-1 Ask). Location FAQs: `methodology/location-faq.md`.
- **FAQ fit picks** (Rewrite 4 Phase 2): `python3 scripts/outline.py faq <slug> <section> --run <RUN_ID>` picks each
  page's FAQs from its candidates on the Claude API (Sonnet) → `build/<section>/faq-picks.json`; each outline shows
  them. No API key yet (or the API answers 401): the script says "no API key — ran on the agent route" and the writer picks them as before.
- Batches: one per kind (all services; all locations and hubs; home and about) — split only above 15 pages.
- The facts round's question set goes to Paul once; `/interview <slug> facts-answers all` records the answers.

## The agent's procedure (Phase 7: moved here from `.claude/agents/build.md`)

**blockers** — runs as soon as the audit is approved (D3). The audit wrote the `Technical Blocker Checklist` (S16,
CM-063); this step only issues the handoff: section 1 (the Fix rows) → one handoff to Jonie, `handoff.py create <slug>
--run <RUN_ID> --kind <kind> --items <csv> --blockers` (one per change kind: `python3 scripts/handoff.py kinds`), or
`status.py blockers-none <slug> --run <RUN_ID>`. An audit approved before CM-063 has no marked checklist: render it first
(`render.py blockers <slug> --run <RUN_ID>`, `status.py mark <slug> blocker_checklist --file <it>`).

**plan** — the site plan, every page in one pass. Per page (from the URL Decision Map): id, type, final URL, keyword,
area variant (B2; never B1's reserved one), category variant, the H1 decision with the "The Best" test (CM-020;
`dfs.py`, estimate first), FAQ topics with a one-line *why it applies here* (location pages: `methodology/location-faq.md`),
link targets — in the plan JSON row (`keyword`, `h1`, `area_variant`, `category_variant`, `faq`, `claims`); `outline.py`
carries them to the writer as fixed. A keyword, H1 or variant left empty is assigned by `outline.py` by formula (a
county hub never); write a value only when the formula would be wrong (e.g. a "The Best" decision). URLs: one root slug
(CM-058); a changed URL carries `live_url` and `replaces`; `urlcheck.py` must pass. Report duplicates, variant conflicts
(CM-013), FAQ overlap (BB-316, C3), claims in keywords and variants (CM-049 → `"claims"`), coverage of routed PAA and
fan-out rows (CM-045). Register, then the viability check (`evidence.py run <slug> --run <RUN_ID> --all`,
`evidence_pack.py viability <slug> --all`). Write `<Client> - Site Plan - REVIEW.md` and the JSON in
`clients/<slug>/build/`, `status.py plan <slug> --file <md> --json <json>`. Links (CM-064): the wheel is `wheel.py`'s,
never listed by hand; `wheel.py check <slug>` must pass; a CM-022 exception goes in the row as `link_exceptions` and
`wheel.py asks <slug>` makes it a kind-1 Ask. Paul approves once: `/approve <slug> site_plan`.

**facts** — one facts round for every page (P10): `evidence.py run <slug> --run <RUN_ID> --all`; `reviews.py extract` if
reviews are on disk; hand `build/evidence/research-all.md` to the **researcher**; re-run the grids; `evidence.py questions
<slug> --run <RUN_ID> --all` — ONE pre-filled question set grouped by fact.
