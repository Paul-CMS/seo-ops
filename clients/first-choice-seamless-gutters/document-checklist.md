# First Choice Seamless Gutters - Document Checklist

Generated 2026-10-24T22:01 from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · `[!]` failed · `[ ]` not yet.

## Evidence and data steps (methodology/audit-steps.md)

| | Step | Outcome | Reason / output |
|---|---|---|---|
| [x] | S01 Intake facts: website, GBP link, storefront/SAB, exact GBP Website-fie | done | intake facts present in status.json/facts.json (SAB, GBP link, Website-field URL, GSC access, CMS); nothing missing for discovery |
| [x] | S02 Public discovery: live site, GBP, social, review profiles, Secretary o | done | site, GBP, BBB, press release read; Sunbiz/Yelp/HomeAdvisor blocked (403), Facebook login wall, licence boards form-only -> manual_lookup H-2026-10-22-02 |
| [x] | S03 Entity research: category entity (Wikipedia), area entity (Russian Dol | done | category entity Rain gutter Q152833 (GBP primary disputed), area entity proposal Polk County/Lakeland-Winter Haven MSA Q501043, variants, Wikidata URIs |
| [x] | S04 Proof sheet built (Markdown + client Google Doc) | done | Proof sheet revised: website address filled (3517 Century Blvd, Lakeland), GBP Manager request removed, licence row trade/contractor only, local business tax receipt request added after Polk County/Lakeland official check; 17/17 questions kept, check passed |
| [x] | S05 Site crawl (max pages = sitemap size × 1.5, min 20, max 1000; 1000 whe | done | clients/first-choice-seamless-gutters/inputs/crawl/ |
| [ ] | S05b Page text capture: the body text of every crawled HTML page (the basic | — |  |
| [x] | S06 Reviews pull: Google rating, count, recent review text (no reviewer na | done | data/reviews/reviews-summary.md |
| [x] | S07 Rankings + cannibalization: every ranked keyword per URL (top 100), co | done | data/rankings/rankings-summary.md |
| [x] | S08 Backlinks pull: referring domains per URL | done | data/backlinks/backlinks-per-url.csv |
| [-] | S09 Citations | skipped | no citation tracker upload on file yet |
| [-] | S10 Local grid | skipped | no local-grid report on file yet |
| [-] | S11 Search Console / GA4 | skipped | no Search Console / GA4 access on file |
| [x] | S19 People Also Ask: core services × primary city + top 3 cities, capped ( | done | data/paa/paa-routing.md |
| [-] | S20 SEOPress site-wide settings (title templates, sitemap, noindexed post  | skipped | no SEOPress settings check on file (not WordPress, or no access yet) |
| [-] | S21 Query fan-out (CM-045): core services × primary city + top 3 cities, c | skipped | query fan-out is off by default (D6) — pipeline.py … --fanout runs it |
| [x] | S12 Ingest + cross-checks + redirect pre-screen | done | pipeline inventory --phase audit (re-run after capturing sitemap + live pages, SRC-055..060) |
| [x] | S13 Entity analysis: site vs Brand Guide (triple, NAP, brand search, suppo | done | entity: base town x3, brand string x3, warranty/licence/offer claims (kind-2 Asks), GBP host, citations |
| [x] | S14 Architecture: every page typed; the screen decides CM-019 C1–C3, the a | done | 50 URL rows; 0 destructive; Plant City held (kind-1 Ask); screen --check passed |
| [x] | S15 Page conformance triage (CM-063): rebuild / light fix / keep; only pag | done | judge: no API key, agent scored 3 pages into conformance-judgment.csv; triage 31 rebuild, 11 light fix, 1 keep |
| [x] | S16 Technical findings (Fix rows → the Technical Blocker Checklist, writte | done | 6 Fix rows rendered to the Technical Blocker Checklist |
| [x] | S17 Fresh-context review: every destructive URL row, every Ask, a sample o | done | clients/first-choice-seamless-gutters/audit/2026-10-23 |
| [x] | S18 The audit review sheet + render | done | review sheet (5 Asks for Paul, 0 client) + render all; deliverables marked |

## Intake documents

- [ ] Search Console homepage queries, last 90 days — ask for it: Search Console → Performance → Queries, filter Page = the homepage, last 90 days, export; name it '<Client> - GSC - queries-homepage-90d - <date>.csv' and put it in inputs/ (scripts/h1lock.py --gsc reads it; without it CM-059 condition (c) cannot be checked)

## Conditions

- [x] The client's facts are in — the returned proof sheet is recorded, or Paul approved the client's direct answers
- [ ] Every page in the site plan is a WordPress draft — ready for the one living publish handoff (CM-055) — batches not yet in WordPress as drafts: pilot, services, locations-west, locations-east
- [ ] Every page in the site plan is built, verified and written back — batches not yet built and written back: pilot, services, locations-west, locations-east, about
- [x] WordPress connected (/wp-check passed in the last 30 days)
- [x] Discovery and audit signed off — Build may start (met when the Decision Sheet, entity, client facts, audit and Brand Guide are approved and the client's facts are recorded)
- [ ] Technical blockers cleared — every blocker handoff returned done and /verify passed it — blockers not cleared: H-2026-10-23-03-broken_link-01 is issued; H-2026-10-23-03-broken_link-02 is issued; H-2026-10-23-03-broken_link-03 is issued; H-2026-10-23-03-broken_link-04 is issued; H-2026-10-23-03-broken_link-05 is issued (+6 more)
- [x] Page specs approved by Paul once, globally (methodology/specs) and unchanged since

## Decisions (Paul)

- [x] Discovery approved — the Decision Sheet (every identity and format decision) and the entity foundation (category, area, variants, reserved homepage variant)
- [x] Client facts approved — the proof sheet ready for Paul to send, or the client's answers taken directly
- [x] Audit approved — its one review sheet answered (URL decisions), the registers and the Evidence Manifest (D3: on its own, as soon as the audit is done; safe fixes and the blocker handoff unlock here)
- [x] Brand Guide approved: the client's returned proof sheet reconciled (verified facts separated from unsupported claims)
- [ ] Release — the published pages pass QA (schema built at the handoff)
- [ ] Blog Decision Map approved — redirects and blog briefs may start
- [ ] WordPress pilot passed for this site — the system may write titles, keyword, social, robots, canonical and schema directly
