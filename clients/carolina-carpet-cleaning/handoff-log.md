# Carolina Carpet Cleaning - Handoff Log

Generated from the safety log (clients/carolina-carpet-cleaning/log.md) — do not edit. Each run adds its section with `run.py finish --handoff <file>`. The newest section is at the bottom.

## /new-client · 2026-10-28 · run 20261028-151835-new-client-df5d

- Client created: full, carpet cleaning, not sensitive; domain carpetcleaningblufftonsc.com (Bluffton only).
- Worktree: ~/Documents/seo-ops-clients/carolina-carpet-cleaning (branch client/carolina-carpet-cleaning).
- Drive: existing `Carolina Carpet Cleaning - TMS` folder used. CMS: WordPress.
- Brand Guide started from the template.
- Evidence: 18 unnamed Drive files identified from their contents and copied to inputs/ under the
  naming convention (SF internal_all, CMS export-all-urls, 9 GSC coverage, 7 page-filtered GSC performance).
  Map in rename-list.md. Drive files not renamed.
- Gaps: no site-wide GSC performance export; no SF h1_all/h2_all; GA4 unknown.
- Open: intake questions to Paul (GBP link, SAB/storefront, GBP Website URL, GA4 access).
- Next: answers run → /discovery carolina-carpet-cleaning discovery.

**Changes (script):** 3 — file ×2, drive_folder ×1

## /answers · 2026-10-28 · run 20261028-153804-answers-90b6

- Facts: SAB (address stays on the site), GBP Website URL = homepage, GBP link, no GA4.
- Settled: site connection is Novamira MCP, read-only until handoff approval.
- Next: /discovery carolina-carpet-cleaning discovery.

- FACT 2026-10-28T15:38 · run 20261028-153804-answers-90b6 · a-storefront-or-sab (value, status, source, quote) · paul_approved · SAB (service-area business); the address still appears on the website…
- FACT 2026-10-28T15:38 · run 20261028-153804-answers-90b6 · a-exact-url-in-the-gbp-website-field (value, status, source) · paul_approved · https://carpetcleaningblufftonsc.com/ · source Paul, chat 2…
- FACT 2026-10-28T15:38 · run 20261028-153804-answers-90b6 · gbp-link (new) · paul_approved · https://maps.app.goo.gl/vvsrqH6TxL815KWB6 · source Paul, chat 2026-10-28 · by Paul
- FACT 2026-10-28T15:38 · run 20261028-153804-answers-90b6 · ga4-access (new) · paul_approved · none · source Paul, chat 2026-10-28 · by Paul

## /discovery · 2026-10-28 · run 20261028-154310-discovery-622b

- S01–S03 done from public sources: live site (home, about, contact, raw HTML/schema), press release 2026-04-30,
  Birdeye, Wikipedia/Wikidata, WHOIS, OSM reverse geocode.
- Written: discovery/Carolina Carpet Cleaning - Discovery Record - REVIEW.md; discovery/Carolina Carpet Cleaning -
  Decision Sheet - REVIEW.md (25 keys, each with a default). Both copied to Drive.
- Brand Guide: A fact rows via run.py fact; Russian Doll path, B1/B2 and F Wikidata rows as proposals.
- Entity proposal: category "Carpet cleaning service" (Q5045777, provisional until GBP read); area entity Hilton Head
  Island metropolitan area (Q17020871) with Yemassee (Hampton Co.) as the one exception; alternative SC Lowcountry.
  Reserved homepage title variant "Hilton Head Island Metro Area", H1 "South Carolina Lowcountry" (both live now).
- Conflicts kept (PROC-01): phone 575-6286 vs 525-6288; address 273 Club Gate Bluffton vs 5922 Pleasant Farm Dr
  Beaufort (Birdeye); schema geo vs GBP pin; two Facebook URLs (schema one named "Jack Blaine Beers Jr.").
- Gwen: one manual_lookup handoff H-2026-10-28-01 (9 rows: SOS, GBP view + dashboard, possible duplicate listing
  "Carolina Carpet, Hardwood, & Tile", Yelp, 2 Facebook, Yola site, Birdeye address).
- entity_record marked. Next: /discovery carolina-carpet-cleaning proof-sheet, then Approval 1.
- No gate set, no spend, no client contact.

**Changes (script):** 17 — manual_lookup ×9, audit_step ×3, record ×2, drive_file ×2, brand_guide ×1
- FACT 2026-10-28T15:47 · run 20261028-154310-discovery-622b · a-brand-entity-gbp-name-exactly (value, status, source, quote) · submitted · Carolina Carpet Cleaning · source GBP place URL (cid 399205…
- FACT 2026-10-28T15:47 · run 20261028-154310-discovery-622b · a-phone (value, status, source, quote) · disputed · CONFLICT: (843) 575-6286 [footer, header, contact page, schema, press release] vs (8…
- FACT 2026-10-28T15:47 · run 20261028-154310-discovery-622b · a-primary-domain-canonical-host-form (value, status, source) · internally_verified · https://carpetcleaningblufftonsc.com/ (http and www…
- FACT 2026-10-28T15:47 · run 20261028-154310-discovery-622b · d-founding-year-years-in-business (value, status, source, quote) · submitted · 1993 (claimed) · source https://carpetcleaningblufftonsc.…
- FACT 2026-10-28T15:47 · run 20261028-154310-discovery-622b · d-named-staff-for-on-page-use (value, status, source, quote) · submitted · Kevin Snow (owner, per press release contact; reviews name 'K…
- FACT 2026-10-28T15:47 · run 20261028-154310-discovery-622b · d-free-estimate-and-what-free-means (value, status, source, quote) · submitted · Free estimate before work begins; no deposit to schedul…
- … and 6 more decision/fact/flag line(s) in log.md
**Steps recorded (script):** S01 done, S02 done, S03 done

## /answers · 2026-10-28 · run 20261028-155947-answers-b36e

- Paul's answers recorded: phone (843) 575-6286; area entity Hilton Head Island metropolitan area; SEO titles "Hilton Head Island Metro Area", user-facing titles and H1 "South Carolina Lowcountry"; Beaufort Facebook page.
- Scope decision: only the 6 live location pages are kept for now (not 18 towns).
- Redirect plan: all three client URLs redirect to carpetcleaningblufftonsc.com; the Beaufort and Hilton Head Island GBPs redirect to their location pages on the Bluffton site.
- Still open: Birdeye/Bluffton address conflict (Paul did not answer); Gwen's lookup handoff H-2026-10-28-01; legal entity name and the d-* client facts.

- FACT 2026-10-28T15:59 · run 20261028-155947-answers-b36e · a-phone (value, status, source) · paul_approved · (843) 575-6286 · source Paul, chat 2026-10-28 · by Paul
- FACT 2026-10-28T15:59 · run 20261028-155947-answers-b36e · a-area-entity (value, status, source) · paul_approved · Hilton Head Island metropolitan area · source Paul, chat 2026-10-28 · by Paul
- FACT 2026-10-28T15:59 · run 20261028-155947-answers-b36e · a-area-variants-3-5 (value, status, source) · paul_approved · SEO titles: Hilton Head Island Metro Area · user-facing titles and homepage …
- DECISION 2026-10-28T15:59 · run 20261028-155947-answers-b36e · Paul 2026-10-28: only the 6 currently live location pages are kept for now (not 18 towns). Area naming: SEO titles use 'Hilton Head Is…
- FACT 2026-10-28T16:00 · run 20261028-155947-answers-b36e · a-facebook-beaufort (new) · paul_approved · https://www.facebook.com/carpetcleaningbeaufortsc · source Paul, chat 2026-10-28 · by Paul

## /answers · 2026-10-28 · run 20261028-190054-answers-2d3d

- Paul's answers to the open questions recorded: Kevin Snow as author; 273 Club Gate address kept; Beaufort Facebook is the main page; six towns; GBP category Carpet cleaning service; founded 1993.
- Owner note recorded: legal/registered name Carolina Floor Cleaning Pros; DBA/trade name Carolina Carpet Cleaning. Brand in titles stays Carolina Carpet Cleaning; Gwen still checks the legal name against the SC Secretary of State record.
- Client facts recorded from the owner note: general workmanship insurance; no current licence number; 6 Google reviews, all 5 stars; family-owned since 1993; no subcontracting; normal payment methods; services list as on the site.
- Open: question 25 (blank). Gwen's lookup handoff H-2026-10-28-01 still pending. Decision Sheet and Discovery Record review files still show the old 18-town and legal-name rows until a revision run.

- FACT 2026-10-28T19:00 · run 20261028-190054-answers-2d3d · a-legal-entity-name (value, status, source) · client_confirmed · Carolina Floor Cleaning Pros · source Owner note, passed on by Paul 2026-…
- FACT 2026-10-28T19:00 · run 20261028-190054-answers-2d3d · d-legal-entity-dba (value, status, source) · client_confirmed · Carolina Carpet Cleaning (DBA / trade name) · source Owner note, passed on…
- FACT 2026-10-28T19:00 · run 20261028-190054-answers-2d3d · d-founding-year-years-in-business (value, status, source) · client_confirmed · 1993 - operated locally as a family-owned business since 19…
- FACT 2026-10-28T19:00 · run 20261028-190054-answers-2d3d · d-licence-numbers-and-classes (value, status, source) · client_confirmed · No current licence number provided · source Owner note, 2026-10…
- FACT 2026-10-28T19:00 · run 20261028-190054-answers-2d3d · d-insurance-bonded-status (value, status, source) · client_confirmed · General workmanship insurance · source Owner note, 2026-10-28 · by …
- FACT 2026-10-28T19:00 · run 20261028-190054-answers-2d3d · d-certifications-authorizations-factory-training (value, status, source) · client_confirmed · N/A · source Owner note, 2026-10-28 · by Paul
- … and 18 more decision/fact/flag line(s) in log.md

## /discovery · 2026-10-28 · run 20261028-190432-discovery-30f8

- Paul chose facts-direct: no proof sheet to send; the owner's answers go straight into the record.
- Owner's answers saved verbatim to `clients/carolina-carpet-cleaning/discovery/Carolina Carpet Cleaning - MANUAL - client-answers - 2026-10-28.md` and copied to Drive; marked as facts_direct and proof_sheet.
- Approval 1 (`entity_approved proof_sheet_approved`) now covers the entity, the Decision Sheet and these client facts. Question 25 is still blank.

**Changes (script):** 2 — drive_file ×1, audit_step ×1
**Steps recorded (script):** S04 done

## /crawl · 2026-10-28 · run 20261028-190920-crawl-36cb

- Crawled carolinacarpetcleaning.com in basic mode, max 20 pages (confirmed by Paul). Cost about $0.003.
- DataforSEO returned "Task In Queue" (task 40602) three times, then completed on the fourth try. Nothing lost.
- Tables in clients/carolina-carpet-cleaning/inputs/crawl/ (git-ignored). Summary the agents read: data/crawl/crawl-summary.csv (8 rows). Page text: data/crawl/page-text.csv (4 of 4 pages).
- S05 and S05b recorded done.
- 14 DFS tables and the crawl-config copied to Drive, 01 - Discovery and Audit/Evidence/.
- Notes from the tables: 4 duplicate meta descriptions, 1 non-indexable URL, 3 external links, 0 duplicate titles, 0 duplicate content, 0 redirect chains.
- Next: the discovery-audit agent reads the crawl summary as part of the audit.

**Changes (script):** 16 — drive_file ×14, audit_step ×2
**Steps recorded (script):** S05 done, S05b done

## /discovery · 2026-10-28 · run 20261028-191341-discovery-ec47

- Paul approved the data pulls at about $0.57 (free estimates). Actual spend about $0.22.
- Rankings (Hilton Head Island, Bluffton, Beaufort, Ridgeland, Hardeeville, Lady's Island): 27 keyword rows, 0 cannibalization clusters. data/rankings/.
- PAA (4 cities, cap 20): 15 distinct questions. Two queries hit DataforSEO server errors; the retry worked. Rows routed by hand on the agent route (paa-routing.md): 8 service FAQs, 4 blog topics, 3 dropped, 0 location FAQs. Four cost questions need the client's own prices.
- Reviews: 29 pulled, rating 5. Meaning check done with reviews.py checked. Known themes: technician named Kevin (11), fast response (6), booking timing (4). Below threshold: explains the work (2), other surfaces (1). Guarantees, pricing and clean-up were false keyword matches (0).
- Competitor coverage: 36 pages across 12 services, data/competitors/coverage.md. One SERP hit a server error; the retry worked.
- Steps: S06, S07 and S19 recorded done. Competitor coverage has no numbered step.
- Watch: the "Facts customers report" table in customer-language.md still shows the old keyword counts. The checked counts are in facts.json section R. Review row 20 ends with a reviewer's first name; never quote it.
- Not run (outside the approval): backlinks (S08), citations, local grid (S09/S10), GSC (S11).
- Summary for Paul: clients/carolina-carpet-cleaning/handoffs/run-20261028-191341-discovery-ec47.summary.md

**Changes (script):** 12 — audit_step ×9, data_pull ×3
**Steps recorded (script):** S06 done, S07 done, S19 done, S08 skipped, S09 skipped, S10 skipped, S11 skipped, S20 skipped, S21 skipped

## /crawl · 2026-10-29 · run 20261028-204638-crawl-94cd

- Crawl of carpetcleaningblufftonsc.com finished: 92 pages crawled, stop reason empty_queue, DataforSEO task 10290153, basic mode, max 132 pages.
- Cost: $0.0198 for the one paid post this run (task 10290153). Earlier task 10290139 was stuck in queue (error 40602) and was never completed.
- Output domain confirmed: carpetcleaningblufftonsc.com (crawl-state and crawl-config match).
- Files in clients/carolina-carpet-cleaning/inputs/crawl/ (15) uploaded to Drive 01 - Discovery and Audit/Evidence/. Two were already unchanged on Drive.
- data/crawl/page-text.csv: 89 of 89 pages captured, 0 failed, 0 disallowed by robots.txt. No charge.
- Steps recorded: S05 done, S05b done.
- Not done: the audit. Nothing was started past the crawl.
- Open issue: DataforSEO queue delays (F-002, F-003). Retries of the same run may post new paid tasks until the script is fixed in a system session.

**Changes (script):** 27 — drive_file ×25, audit_step ×2
- FLAG 2026-10-28T20:50 · run 20261028-204638-crawl-94cd · F-003 · DataforSEO task 10290139 (carpetcleaningblufftonsc.com, basic, 132 pages) stays 'In Queue' (error 40602); resume returns exit 8 on e…
**Steps recorded (script):** S05 done, S05b done

