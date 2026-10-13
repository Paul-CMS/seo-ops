# Location FAQ recipe (CM-061 part 5; rewrite 3 §7)

Governs every location page from 2026-10-12 (adapted from Bradley's local FAQ prompt). The wording in
`methodology/specs/location.md` is updated later, with CR-023; where they differ, this file governs. Answer form:
CM-060 (sentence one answers alone in short plain words; the first answer paragraph is 40–60 words).

## Three FAQs, one per category

| Category | What it answers | Answer source |
|---|---|---|
| **1 · Local cost or decision** | What changes the job or the price **here**: HOA/ARB, historic district, flood rules, wind code | Public facts + client practice. No prices unless client-confirmed (usage tiers, writing-commercial.md). |
| **2 · Logistics in this area** | Permits and who issues them, gate access, travel and response time, storm season | Public facts + client facts |
| **3 · Trust in this area** | Local pain points (salt air, hurricanes, humidity, older homes) and the client's local experience | Client facts + review evidence at its usage tier |

## Where the questions come from, in order
1. **PAA and fan-out questions already in the page's evidence pack** (`build/<section>/packs/<page>.md` → Questions).
   Use these first; no new lookup is needed when the pack has them.
2. Local conditions from the area source lists (`methodology/sources/`).
3. Review language for that place (the pack's Reviews → `place:` topic).

- A generic question is reframed with the place or a local term — "What is the 25% rule for roofing?" becomes "Does the
  25% re-roof rule apply to homes on Fripp Island?" — or discarded.
- **Fallback:** a category that cannot be sourced locally uses the **brand-level local fallback**, answered from client
  facts only ("How fast can Apex reach Okatie after a storm?"). That is a "Fix and list" row in the review sheet, never
  an Ask.
- **New PAA lookups** only for places with no tagged questions in the pack, and through the usual DataforSEO cost check
  (`dfs.py`, estimate first; over $2 → ask Paul).

## Minimums are targets (§8)
The minimums in `location.md` (neighbourhoods, things to do, top sites …) are **targets**. An optional section that
cannot be sourced — its public facts logged `not_found` at the minimum (`research.py log`) — is shortened or dropped
as "Fix and list". **No page is held for an optional section**: a researched public gap never blocks the evidence gate.

## Viability check — before the site plan reaches Paul
After the site plan is registered (`status.py plan`), the evidence gate builds every page's pack (`evidence.py run
<slug> --run <RUN_ID> --all`); then `python3 scripts/evidence_pack.py viability <slug> --all` scores each planned
location from its pack: neighbourhoods, places and things to do, local conditions, and the three FAQ categories. A place
where most cannot be filled arrives in the site plan as a **merge proposal** into the nearest planned city page (a 301
if a URL exists) — an Ask (kind 1, a page decision) with the merge as the recommended option.
