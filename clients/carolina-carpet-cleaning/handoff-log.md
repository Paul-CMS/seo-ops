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

