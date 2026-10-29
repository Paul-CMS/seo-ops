# Carolina Carpet Cleaning - Document Checklist

Generated 2026-10-28T19:52 from status.json — do not edit. `[x]` done · `[-]` skipped (reason) · `[!]` failed · `[ ]` not yet.

## Evidence and data steps (methodology/audit-steps.md)

| | Step | Outcome | Reason / output |
|---|---|---|---|
| [x] | S01 Intake facts: website, GBP link, storefront/SAB, exact GBP Website-fie | done | intake facts read from facts.json/status; nothing missing for discovery |
| [x] | S02 Public discovery: live site, GBP, social, review profiles, Secretary o | done | site, press release, Birdeye, Wikipedia, WHOIS read; SOS, GBP, Yelp, Facebook, Yola go to Gwen (H-2026-10-28-01) |
| [x] | S03 Entity research: category entity (Wikipedia), area entity (Russian Dol | done | entity foundation proposed: category, MSA area entity via Russian Doll, variants, reserved homepage variant, Wikidata URIs |
| [x] | S04 Proof sheet built (Markdown + client Google Doc) | done |  |
| [!] | S05 Site crawl (max pages = sitemap size × 1.5, min 20, max 1000; 1000 whe | failed | Crawled the wrong domain (carolinacarpetcleaning.com, task 10290009-1266-0216-0000-9b27d219671b) instead of the settled primary domain carpetcleaningblufftonsc.com (Brand Guide A9). Re-crawl needed: estimate 132 pages, about $0.02. |
| [!] | S05b Page text capture: the body text of every crawled HTML page (the basic | failed | Page text is for the wrong site (carolinacarpetcleaning.com, 4 pages); re-capture after the S05 re-crawl of carpetcleaningblufftonsc.com. |
| [x] | S06 Reviews pull: Google rating, count, recent review text (no reviewer na | done | clients/carolina-carpet-cleaning/data/reviews/ |
| [x] | S07 Rankings + cannibalization: every ranked keyword per URL (top 100), co | done | clients/carolina-carpet-cleaning/data/rankings/ |
| [-] | S08 Backlinks pull: referring domains per URL | skipped | backlinks not in the approved data pulls; run in a later pass |
| [-] | S09 Citations | skipped | no BrightLocal or Local Dominator grid files on file yet |
| [-] | S10 Local grid | skipped | no Local Dominator grid PDFs on file yet |
| [-] | S11 Search Console / GA4 | skipped | GSC exports are on file; analysis is a later pass |
| [x] | S19 People Also Ask: core services × primary city + top 3 cities, capped ( | done | clients/carolina-carpet-cleaning/data/paa/ |
| [-] | S20 SEOPress site-wide settings (title templates, sitemap, noindexed post  | skipped | WordPress check (wp-check) not run in this pass |
| [-] | S21 Query fan-out (CM-045): core services × primary city + top 3 cities, c | skipped | query fan-out only with --fanout; not requested |
| [!] | S12 Ingest + cross-checks + redirect pre-screen | failed | The S05 crawl tables are for the wrong site: carolinacarpetcleaning.com (a different West Columbia SC business, (803) 606-0154, since 1997), not the client's carpetcleaningblufftonsc.com. Cross-checks, crawl-summary and page-text describe that other business; no audit can rest on them. Re-crawl the right domain, then re-run S12. |
| [ ] | S13 Entity analysis: site vs Brand Guide (triple, NAP, brand search, suppo | — |  |
| [ ] | S14 Architecture: every page typed; the screen decides CM-019 C1–C3, the a | — |  |
| [ ] | S15 Page conformance triage (CM-063): rebuild / light fix / keep; only pag | — |  |
| [ ] | S16 Technical findings (Fix rows → the Technical Blocker Checklist, writte | — |  |
| [ ] | S17 Fresh-context review: every destructive URL row, every Ask, a sample o | — |  |
| [ ] | S18 The audit review sheet + render | — |  |

## Intake documents

- [ ] Search Console homepage queries, last 90 days — ask for it: Search Console → Performance → Queries, filter Page = the homepage, last 90 days, export; name it '<Client> - GSC - queries-homepage-90d - <date>.csv' and put it in inputs/ (scripts/h1lock.py --gsc reads it; without it CM-059 condition (c) cannot be checked)

## Conditions

- [x] The client's facts are in — the returned proof sheet is recorded, or Paul approved the client's direct answers
- [ ] Every page in the site plan is a WordPress draft — ready for the one living publish handoff (CM-055) — no site plan yet
- [ ] Every page in the site plan is built, verified and written back — no site plan yet
- [ ] WordPress connected (/wp-check passed in the last 30 days) — WordPress is not connected yet — run /wp-check carolina-carpet-cleaning
- [ ] Discovery and audit signed off — Build may start (met when the Decision Sheet, entity, client facts, audit and Brand Guide are approved and the client's facts are recorded) — discovery is not signed off yet — still open: the audit (its review sheet, registers and Evidence Manifest), the reconciled Brand Guide
- [ ] Technical blockers cleared — every blocker handoff returned done and /verify passed it — the technical blocker checklist is not written yet
- [x] Page specs approved by Paul once, globally (methodology/specs) and unchanged since

## Decisions (Paul)

- [x] Discovery approved — the Decision Sheet (every identity and format decision) and the entity foundation (category, area, variants, reserved homepage variant)
- [x] Client facts approved — the proof sheet ready for Paul to send, or the client's answers taken directly
- [ ] Audit approved — its one review sheet answered (URL decisions), the registers and the Evidence Manifest (D3: on its own, as soon as the audit is done; safe fixes and the blocker handoff unlock here)
- [ ] Brand Guide approved: the client's returned proof sheet reconciled (verified facts separated from unsupported claims)
- [ ] Release — the published pages pass QA (schema built at the handoff)
- [ ] Blog Decision Map approved — redirects and blog briefs may start
- [ ] WordPress pilot passed for this site — the system may write titles, keyword, social, robots, canonical and schema directly
