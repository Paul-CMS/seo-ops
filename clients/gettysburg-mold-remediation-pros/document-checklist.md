# Gettysburg Mold Remediation Pros - Document Checklist

Generated 2026-10-22T07:08 from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · `[!]` failed · `[ ]` not yet.

## Evidence and data steps (methodology/audit-steps.md)

| | Step | Outcome | Reason / output |
|---|---|---|---|
| [x] | S01 Intake facts: website, GBP link, storefront/SAB, exact GBP Website-fie | done | Intake facts from Paul as recorded at /new-client (no GBP, SAB, confirmed address, no GSC/GA4, health_adjacent); nothing missing for S02/S03 |
| [x] | S02 Public discovery: live site, GBP, social, review profiles, Secretary o | done | Live site (24 sitemap URLs) and web search for name, address, phone, owner, profiles; no third-party profiles found. PA DOS (bot check), PA AG HIC and IICRC directory could not be checked - listed as NEED |
| [x] | S03 Entity research: category entity (Wikipedia), area entity (Russian Dol | done | Category candidates verified on Wikipedia/Wikidata (no GBP - open question); area by Russian Doll with path (two-state area; strict result Mid-Atlantic; proposed South Central PA, 5 of 6 cities); variants; reserved homepage variant; Wikidata URIs |
| [ ] | S04 Proof sheet built (Markdown + client Google Doc) | — |  |
| [ ] | S05 Site crawl (max pages = sitemap size × 1.5, min 20, max 1000; 1000 whe | — |  |
| [ ] | S05b Page text capture: the body text of every crawled HTML page (the basic | — |  |
| [ ] | S06 Reviews pull: Google rating, count, recent review text (no reviewer na | — |  |
| [ ] | S07 Rankings + cannibalization: every ranked keyword per URL (top 100), co | — |  |
| [ ] | S08 Backlinks pull: referring domains per URL | — |  |
| [ ] | S09 Citations | — |  |
| [ ] | S10 Local grid | — |  |
| [ ] | S11 Search Console / GA4 | — |  |
| [ ] | S19 People Also Ask: core services × primary city + top 3 cities, capped ( | — |  |
| [ ] | S20 SEOPress site-wide settings (title templates, sitemap, noindexed post  | — |  |
| [ ] | S21 Query fan-out (CM-045): core services × primary city + top 3 cities, c | — |  |
| [ ] | S12 Ingest + cross-checks + redirect pre-screen | — |  |
| [ ] | S13 Entity analysis: site vs Brand Guide (triple, NAP, brand search, suppo | — |  |
| [ ] | S14 Architecture: every page typed; the screen decides CM-019 C1–C3, the a | — |  |
| [ ] | S15 Page conformance triage (CM-063): rebuild / light fix / keep; only pag | — |  |
| [ ] | S16 Technical findings (Fix rows → the Technical Blocker Checklist, writte | — |  |
| [ ] | S17 Fresh-context review: every destructive URL row, every Ask, a sample o | — |  |
| [ ] | S18 The audit review sheet + render | — |  |

## Intake documents

- [ ] Search Console homepage queries, last 90 days — ask for it: Search Console → Performance → Queries, filter Page = the homepage, last 90 days, export; name it '<Client> - GSC - queries-homepage-90d - <date>.csv' and put it in inputs/ (scripts/h1lock.py --gsc reads it; without it CM-059 condition (c) cannot be checked)

## Conditions

- [ ] The client's facts are in — the returned proof sheet is recorded, or Paul approved the client's direct answers — the client has not returned the proof sheet yet (when it arrives: /discovery gettysburg-mold-remediation-pros sheet-returned)
- [ ] Every page in the site plan is a WordPress draft — ready for the one living publish handoff (CM-055) — no site plan yet
- [ ] Every page in the site plan is built, verified and written back — no site plan yet
- [ ] WordPress connected (/wp-check passed in the last 30 days) — the last /wp-check failed — fix what it reported (clients/gettysburg-mold-remediation-pros/wordpress/wp-check-2026-10-03.md) and run /wp-check gettysburg-mold-remediation-pros again
- [ ] Discovery and audit signed off — Build may start (met when the Decision Sheet, entity, client facts, audit and Brand Guide are approved and the client's facts are recorded) — discovery is not signed off yet — still open: the Decision Sheet and the entity foundation, the client proof sheet (or the client's direct answers), the client's returned proof sheet, the audit (its review sheet, registers and Evidence Manifest), the reconciled Brand Guide
- [ ] Technical blockers cleared — every blocker handoff returned done and /verify passed it — the technical blocker checklist is not written yet
- [x] Page specs approved by Paul once, globally (methodology/specs) and unchanged since

## Decisions (Paul)

- [ ] Discovery approved — the Decision Sheet (every identity and format decision) and the entity foundation (category, area, variants, reserved homepage variant)
- [ ] Client facts approved — the proof sheet ready for Paul to send, or the client's answers taken directly
- [ ] Audit approved — its one review sheet answered (URL decisions), the registers and the Evidence Manifest (D3: on its own, as soon as the audit is done; safe fixes and the blocker handoff unlock here)
- [ ] Brand Guide approved: the client's returned proof sheet reconciled (verified facts separated from unsupported claims)
- [ ] Release — the published pages pass QA (schema built at the handoff)
- [ ] Blog Decision Map approved — redirects and blog briefs may start
- [ ] WordPress pilot passed for this site — the system may write titles, keyword, social, robots, canonical and schema directly
