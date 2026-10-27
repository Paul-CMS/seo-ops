# First Choice Seamless Gutters - Handoff Log

Generated from the safety log (clients/first-choice-seamless-gutters/log.md) — do not edit. Each run adds its section with `run.py finish --handoff <file>`. The newest section is at the bottom.

## /new-client · 2026-10-22 · run 20261022-073424-new-client-ad26

Run: 20261022-073424-new-client-ad26

## What was done
- Client set up as a full client (not blog-only). Slug: first-choice-seamless-gutters. Not sensitive (industry "seamless gutters", category none).
- Domain: firstchoiceseamlessgutters.net. Name and domain confirmed by Paul (yes/yes) — still marked Submitted in the Brand Guide until checked against the GBP.
- Brand Guide draft created from the template; name, category and domain filled and marked Submitted.
- Drive: no local Drive folder on this machine — "Drive copy pending sync" recorded once.
- CMS: detection could not fetch the site (certificate check failed from this machine). Paul reports WordPress; recorded as fact `cms` (client_confirmed). WordPress steps are in scope.

## Paul's intake answers (recorded as facts)
- Storefront or SAB: service area business, travels to customers.
- Exact GBP Website URL: https://firstchoiceseamlessgutters.net/
- GBP share link: https://maps.app.goo.gl/c5prGD6rMCwptG3x6
- Google Search Console: access exists (Paul reports).

## Still open
- Google Analytics 4 access: not answered.
- Phone, legal entity name, service-area towns, founding year: not yet asked.
- WordPress setup handoff to Jonie (wp_setup) and the credential lines for Paul: next, in a wp-check run after this run finishes.

**Changes (script):** 1 — brand_guide ×1
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · a-storefront-or-sab (value, status, source) · submitted · Service area business (travels to customers) · source Paul, intake answer · b…
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · a-exact-url-in-the-gbp-website-field (value, status, source) · submitted · https://firstchoiceseamlessgutters.net/ · source Paul, intak…
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · gbp-share-link (new) · submitted · https://maps.app.goo.gl/c5prGD6rMCwptG3x6 · source Paul, intake answer · by Paul
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · cms (new) · client_confirmed · WordPress · source Paul, intake answer · by Paul
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · gsc-access (new) · submitted · Access exists (Paul reports) · source Paul, intake answer · by Paul

## /wp-check · 2026-10-22 · run 20261022-074155-wp-check-2653

Run: 20261022-074155-wp-check-2653

## Result
- WordPress connection: **not connected**. Nothing live was changed. The check's two test drafts were created and trashed.
- Blocking item: the three WordPress credential lines are not yet in the client's local settings file. Paul adds them himself.

## Paul's part (FIX)
- Run `python3 scripts/wp.py env-lines first-choice-seamless-gutters` and follow its output.
- Add the three lines: site address, the `[REDACTED]` Editor username, and the Application Password (24 characters, keep the spaces).
- The Application Password's name is only a label in WordPress; it is not needed in the file.
- Then run `/wp-check first-choice-seamless-gutters` again.

## Jonie's part (wp_setup handoff — not yet confirmed as sent)
- Create the `[REDACTED]` Editor user and its Application Password (wordpress/wordpress-site-setup.md §1).
- Password name in WordPress: `[REDACTED]`.

## Open from the new-client run
- Google Analytics 4 access: not answered.
- Phone, legal entity name, service-area towns, founding year: not yet asked.

## /wp-check · 2026-10-22 · run 20261022-074529-wp-check-d203

Run: 20261022-074529-wp-check-d203

## Result
- WordPress connection: **not connected**. Nothing live was changed. The check's two test drafts were created and trashed.
- Blocking item: the three WordPress credential lines are still not in the client's local settings file.

## Paul's part (FIX)
- Run `python3 scripts/wp.py env-lines first-choice-seamless-gutters` and follow its output.
- Add the three lines (site address, the `[REDACTED]` username, the Application Password with its spaces) to the settings file.
- Then run `/wp-check first-choice-seamless-gutters` again.

## Jonie's part (wp_setup handoff — not yet sent)
- Create the `[REDACTED]` Editor user and its Application Password (wordpress/wordpress-site-setup.md §1).

## /wp-check · 2026-10-22 · run 20261022-075244-wp-check-8211

Run: 20261022-075244-wp-check-8211

## Result
- WordPress connection: **not connected**. Nothing live was changed. The check's two test drafts were created and trashed.
- Blocking item: the three WordPress credential lines are still not found in the client's local settings file.
- The settings file now exists in the client folder (created by copying the example file).

## Paul's part (FIX)
- Open the settings file in a text editor and add the three lines from `python3 scripts/wp.py env-lines first-choice-seamless-gutters`.
- Save it, then run `/wp-check first-choice-seamless-gutters` again.

## Jonie's part (wp_setup handoff — not yet sent)
- Create the `seo-ops` Editor user and its Application Password (wordpress/wordpress-site-setup.md §1).

## /wp-check · 2026-10-22 · run 20261022-075837-wp-check-fa1d

Run: 20261022-075837-wp-check-fa1d

## Result
- Credentials: **OK**. The three WordPress lines are now found in the client's settings file.
- REST API reachable: **FIX**. The check could not reach the site because the certificate could not be verified from this machine (SSL: certificate verify failed, unable to get local issuer certificate). The same error appeared earlier on the platform check.
- Nothing live was changed. The check's two test drafts were created and trashed.

## Paul's part (FIX)
- Open [REDACTED]/ in a browser. If it loads with no security warning, the problem is this Mac's certificate setup, not the site.
- If Python can't verify certificates on this Mac, the usual fix is to run the "Install Certificates.command" file in the Python application folder. This changes a system setting, so Paul runs it himself.
- If the browser shows a certificate warning, the site's certificate needs fixing by whoever hosts it.
- Then run `/wp-check first-choice-seamless-gutters` again.

## Jonie's part (wp_setup handoff — not yet sent)
- Create the `seo-ops` Editor user and its Application Password (wordpress/wordpress-site-setup.md §1).

## /wp-check · 2026-10-22 · run 20261022-083823-wp-check-75b9

Run: 20261022-083823-wp-check-75b9

## Result: connected (WordPress connected for 30 days)
- Credentials: OK. The three WordPress lines are in the client's settings file.
- REST API: OK ([REDACTED]/wp-json/).
- Login and role: OK. Logged in as paulmeisner (Editor).
- Draft creation: OK (draft page and draft post).
- SEOPress 6.8+ per-page fields: OK. Written and read back on a test draft; both test drafts trashed.
- Nothing was published. No pilot was run (no --pilot).

## Notes to act on
- **Username mismatch:** the setup asked for the dedicated `seo-ops` Editor user, but the check logged in as `paulmeisner`. Confirm which user the settings file holds before the pilot.
- **SEOPress site-wide settings** cannot be read as Editor. One-time VA check for Jonie: title templates, sitemap settings, noindexed post types, and SEOPress's schema (Knowledge Graph) for the audit.
- **Kadence head-code field:** meta key not set yet. Found during the pilot step; set the key with `status.py set` and in the must-use plugin.
- **SEOPress settings handoff** written by the script: `H-2026-10-22-01-seopress_settings` (4 items, .md and .csv in the handoffs folder).

## Jonie's part (wp_setup handoff — not yet sent)
- Create the `seo-ops` Editor user and its Application Password (wordpress/wordpress-site-setup.md §1), if the settings file is not already using it.

**Changes (script):** 6 — seopress_settings ×4, wp_check ×2

## /discovery · 2026-10-22 · run 20261022-084632-discovery-42fd

- Public research: site (home, about, areas, contact, sitemaps), GBP public page + reviews, 3 Maps links (same place),
  BBB, MarketersMedia press release, Wikipedia/Wikidata. Blocked: Sunbiz, Yelp, HomeAdvisor (403), Facebook (login),
  DBPR/Polk licence search (forms) → Gwen handoff H-2026-10-22-02-manual_lookup (8 rows).
- Facts recorded (21) via run.py fact: GBP name, phone, canonical host (www), legal entity (BBB), founding 11/24/2021
  (BBB), owners Adrian + Rachel Buehl (BBB), rating 5.0/138, BBB A+ accredited 8/12/2025, site claims (warranty,
  licensed/insured, free estimate, response, hours); licence and financing stay [NEED].
- Conflicts recorded, not resolved (PROC-01): GBP primary category (intake "Seamless gutters" vs Maps "gutter_service");
  base town Lakeland vs Winter Haven; street addresses in schema/press release (3517 Century Blvd) and HomeAdvisor
  (1575 Lemon Ave) vs SAB; second BBB phone (863) 320-2842; GBP Website field www vs non-www.
- Entity proposal: category Rain gutter (Q152833); area Polk County, FL = Lakeland–Winter Haven MSA (Q501043), outliers
  Plant City (Hillsborough) and Sebring (Highlands); Central Florida (Q2920358) the alternative.
- Written: Discovery Record - REVIEW, Decision Sheet - REVIEW (4 open choices), Brand Guide §A derivation + B1/B2,
  discovery/discovery-questions.json (5 client questions, filter + check passed). Drive uploads pending (sync off).
- Marked entity_record. Next: /discovery proof-sheet (S04), then Approval 1.

**Changes (script):** 12 — manual_lookup ×8, audit_step ×3, brand_guide ×1
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-brand-entity-gbp-name-exactly (value, status, source, quote) · internally_verified · First Choice Seamless Gutters Inc. · source GBP (…
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-gbp-primary-category-the-category-entity (value, status, source, quote) · disputed · CONFLICT (PROC-01): Paul intake 'Seamless gutters…
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-category-variants-4-6 (value, status, source, quote) · submitted · Proposed: Gutter Service · Seamless Gutters · Rain Gutters · Gutter…
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-area-entity (value, status, source, quote) · submitted · Proposed: Polk County, Florida = Lakeland–Winter Haven MSA (Q501043). Path: W…
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-area-variants-3-5 (value, status, source) · submitted · Proposed: Polk County, FL · Polk County, Florida · Lakeland–Winter Haven · Lak…
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-phone (value, status, source, quote) · internally_verified · (863) 330-3243 (site, GBP, schema agree; BBB also lists 'Other Phone' (86…
- … and 15 more decision/fact/flag line(s) in log.md
**Steps recorded (script):** S01 done, S02 done, S03 done

## /discovery · 2026-10-22 · run 20261022-101800-discovery-68d2

- Built: `discovery/First Choice Seamless Gutters - Client Proof Sheet - REVIEW.md` (Access 1 · Block A 4 groups, 11 services, 21 towns · Block B 11 quoted claims · Block C 5 documents, 6 facts, 3 positioning). Return by Thu 29 Oct 2026; default = build with what's there.
- Questions: `discovery/proof-sheet-questions.json` — settled.py filter kept 17/17; questions.py check passed. No public fact asked.
- Applied Paul's settlements (category Gutter service, area Polk County, GBP stays SAB, grid Local Dominator) — none on the sheet.
- Facts: `website-street-address` = [NEED: website address — Paul confirming from client billing] (3517 Century Blvd / 1575 Lemon Ave not chosen); `d-licence-numbers-and-classes` stays [NEED] (Paul: none provided).
- Paul fills before sending: the website-address row and the agency GBP manager email (none on record).
- Client Google Doc (`- CLIENT COPY`, HTML via connector) not created: waits for those two fills. Drive copy of the .md: pending sync.
- S04 recorded done; `status.py mark proof_sheet` set. Next: Approval 1 (`entity_approved proof_sheet_approved`) once Paul's open address choice is closed.

**Changes (script):** 1 — audit_step ×1
- FACT 2026-10-22T10:19 · run 20261022-101800-discovery-68d2 · website-street-address (new) · unknown · [NEED: website address — Paul confirming from client billing] · source Paul, 2026-10-22: confir…
- FACT 2026-10-22T10:19 · run 20261022-101800-discovery-68d2 · d-licence-numbers-and-classes (value, source) · unknown · [NEED: licence number and class — site claims licensed, no number shown; Paul …
**Steps recorded (script):** S04 done

## /discovery · 2026-10-22 · run 20261022-194949-discovery-47cc

- Proof sheet revised: `discovery/First Choice Seamless Gutters - Client Proof Sheet - REVIEW.md`; questions in `discovery/proof-sheet-questions.json`.
- Website street address filled: 3517 Century Blvd, Lakeland, FL (fact website-street-address, paul_approved). No billing mention remains.
- The GBP Manager request was removed (gbp_manager_access settled). The GBP was not edited.
- Licence row (Block B) and question licence_number now ask only for the trade or contractor licence: number and class. No business licence is requested (licence_note_florida settled).
- Local business tax receipt: the public check CONFIRMED it for Polk County (polktaxes.com/services/local-business-taxes/) and for the City of Lakeland (lakelandgov.net business-tax page). Both require one for a business located or operating there. Fla. Stat. ch. 205 authorises both taxes. Winter Haven's page lists the receipt only as a step in opening a business. A neutral document request was added under C.
- Not checked: whether 3517 Century Blvd is inside Lakeland city limits, and whether Florida DBPR requires a state licence for gutter work. No official page on that was found.
- settled.py filter kept 17/17 questions. questions.py check passed. Return-by date, 11 services, 21 towns and 11 claims are unchanged.
- Still [NEED]: licence number and class (asked in Block B).
- Step S04 is recorded as done. `status.py mark proof_sheet` was set again. Approval 1 (entity_approved, proof_sheet_approved) is ready for Paul.

**Changes (script):** 1 — audit_step ×1
- FACT 2026-10-22T19:49 · run 20261022-194949-discovery-47cc · website-street-address (value, status, source) · paul_approved · 3517 Century Blvd, Lakeland, FL · source Paul, 2026-10-22 (confirmed fo…
**Steps recorded (script):** S04 done

## /crawl · 2026-10-23 · run 20261022-200953-crawl-ecac

Stage 3 (Data), step S05 crawl. Client domain: https://www.firstchoiceseamlessgutters.net/ (canonical www).

- Settings: basic mode, max pages 66 (sitemap 44 URLs × 1.5), confirmed by Paul.
- Result: 47 URLs in the crawl tables; 41 pages' body text captured (S05b, no charge).
- Cost: $0.0099 (one DataforSEO call). Balance after: about $69.15.
- Tables: internal_all, links_all, page_titles_all, meta_description_all, h1_all, h2_all, all_inlinks (1,772 rows), external_all, plus duplicate_titles, duplicate_descriptions, duplicate_content, redirect_chains, non_indexable (all 0 rows) and the crawl-config .md.
- Local files: clients/first-choice-seamless-gutters/inputs/crawl/ (git-ignored). Agent-readable: data/crawl/crawl-summary.csv and data/crawl/page-text.csv.
- Drive: all 14 files copied to Shared drives / CMS SERVICE PAGE AUDITS / v3. CMS Technical SEO Audit 2026 / First Choice Seamless Gutters - TMS.

Earlier attempts: run 20261022-195904-crawl-722b stopped before any spend (DFS credentials missing from .env) and was aborted with Paul's approval.

Open: flag F-001 (config.json drive.local_root pointed at My Drive; fixed by Paul in a system session).

**Changes (script):** 15 — drive_file ×14, audit_step ×1
- FLAG 2026-10-22T20:26 · run 20261022-200953-crawl-ecac · F-001 · config.json drive.local_root points at My Drive/v3. CMS Technical SEO Audit 2026, but the folder is under Shared drives/CMS SERVICE …
**Steps recorded (script):** S05 done

## /discovery · 2026-10-23 · run 20261023-064343-discovery-0e30

Stage 3 (Data), step discovery:data. Approved by Paul at about $0.62 (cities Lakeland, Winter Haven, Bartow, Haines City; keyword "First Choice Seamless Gutters Inc."; no fan-out).

- Reviews (S06): passed, after the DataforSEO field fix in the system session (F-002).
- Rankings (S07): passed.
- Backlinks (S08): passed on the rerun. The first attempt failed on a missing raw folder (F-003) after one $0.0272 call; the rerun completed.
- People Also Ask (S19) and competitor coverage: passed.
- BrightLocal, Local Dominator, Search Console and WordPress (S09/S10/S11/S20): recorded from files on disk.
- Cost on the rerun: about $0.12 (S08 $0.06, S19 $0.04, competitors $0.02). Earlier attempts add roughly $0.50 more, so the total is under the $0.62 approval.

Open: flag F-003 (backlinks raw folder) is logged for the system session; confirm it is fixed before the next backlinks run. Jonie's seopress handoff (4 items) and Gwen's manual lookup (8 items) remain open and do not block.

**Changes (script):** 15 — audit_step ×12, data_pull ×3
- FLAG 2026-10-23T06:53 · run 20261023-064343-discovery-0e30 · F-002 · pipeline.py inventory S06 reviews fails: DataforSEO task 40501 Invalid Field 'location_name' ($0 spent). Steps S07, S08, S19 and…
- FLAG 2026-10-23T12:20 · run 20261023-064343-discovery-0e30 · F-003 · pipeline.py inventory S08 backlinks fails: No such file or directory clients/first-choice-seamless-gutters/data/backlinks/raw/ba…
**Steps recorded (script):** S06 done, S07 done, S08 done, S19 done, S21 skipped, S09 skipped, S10 skipped, S11 skipped, S20 skipped

## /discovery · 2026-10-23 · run 20261023-125720-discovery-f174

- S12: pipeline inventory --phase audit; re-run after capturing live public evidence (inputs/public-site-2026-10-23/, SRC-055–060: sitemap, homepage, Lake Wales, 2 sitemap-only posts, robots).
- S13–S14: 50-row URL Decision Map (audit/2026-10-23/url-decision-map.csv); 0 destructive rows; Plant City (U019) Hold; screen --check passed.
- S15: judge had no API key — agent scored homepage + 2 posts into audit/conformance-judgment.csv; triage 31 rebuild · 11 light fix · 1 keep.
- S16: findings.csv; Technical Blocker Checklist rendered (6 Fix).
- S17: audit-reviewer — 25 confirmed, 6 revised, 7 withdrawn (review-summary.md). Active: 43 findings (6 Fix, 32 Fix and list, 5 Ask).
- S18: review.py sheet (5 questions for Paul, 0 client), render.py all; marked audit_deliverables and blocker_checklist.
- Asks (defaults): Plant City hold (a) · homepage H1 no change (a) · warranty, licence, $150 offer stay live until the returned proof sheet (a).
- Urgent Fix: F-008 vendor-domain estimate links (2 pages → another business), F-011 broken header tel link (43 pages).
- Proof-sheet questions not re-asked (DEC-LOCAL-006); audit decisions in audit/2026-10-23/decisions.md.
- Flags: F-004 (screen C3 pass without citation export), F-005 (settled homepage title vs COM-T).
- Waiting on: Paul — /discovery review, then audit_approved; client — returned proof sheet; Paul — GSC homepage 90-day export.

**Changes (script):** 21 — audit_step ×9, rendered ×7, audit_screen ×3, audit_triage ×2
- FLAG 2026-10-23T13:09 · run 20261023-125720-discovery-f174 · F-004 · pagedec.py screen marks C3 'pass' when no citation tracker export is on file ('no citation tracker on file'), while CM-019 says …
- FLAG 2026-10-23T13:15 · run 20261023-125720-discovery-f174 · F-005 · COM-T (titles 60 characters or fewer) cannot be met by the settled title formats with the settled variants: the homepage title '…
**Steps recorded (script):** S12 done, S13 done, S14 done, S15 done, S16 done, S17 done, S18 done

## /discovery · 2026-10-23 · run 20261023-135245-discovery-56df

Paul answered the five audit Asks (2026-10-23):
- Plant City (F-015, ask 1): no city page. Plant City is outside the established service area, so the city list stays as it is. Option a applies: 301 to /areas-we-serve/ once the citation check (C3) is run and no-leads (C4) is confirmed.
- Homepage H1 (F-017, ask 2): option a, no change; the lock holds.
- 10-year warranty (F-003, ask 3): option a, leave it live. The owner's public review response (data/reviews/raw/reviews.json) confirms the 10-year installation warranty; recorded as fact d-warranty-terms (client_confirmed).
- Licensed and insured (F-004, ask 4): resolved. Licence not required in Florida for these services; recorded as d-licence-numbers-and-classes. Not re-raised.
- $150 military/seniors offer (F-005, ask 5): option a, leave it live. Confirmed still running; recorded as offer-military-seniors-150.

The other 32 rows took the recommended option.
Urgent Fix items unchanged: F-008 (estimate links to a domain now showing another business, Lake Wales and Lakeland) and F-011 (broken header Call Us link, 43 pages).
Open: flag F-004 (citation export missing; the C3 screen counted it as a pass) is still open.

- FACT 2026-10-23T13:52 · run 20261023-135245-discovery-56df · d-warranty-terms (value, status, source) · client_confirmed · 10-year installation warranty; the company corrects any problem with its g…
- FACT 2026-10-23T13:52 · run 20261023-135245-discovery-56df · d-licence-numbers-and-classes (value, status, source) · paul_approved · Not required in Florida for these services; no licence number to…
- FACT 2026-10-23T13:52 · run 20261023-135245-discovery-56df · offer-military-seniors-150 (new) · paul_approved · $150 off full house installations for Military & Seniors: confirmed and still running…
- FACT 2026-10-23T13:52 · run 20261023-135245-discovery-56df · plant-city-served (new) · paul_approved · Not in the established service area; no Plant City page. Cities listed stay as the established…

## /build · 2026-10-23 · run 20261023-135747-build-82bb

**Stage 5 — Build plan and blockers.** Issued the technical blocker handoff from the audit checklist, section 1 (Fix rows).

- Handoff H-2026-10-23-03-broken_link (Jonie, blocker): 10 rows covering F-008, F-009, F-010, F-011.
  Source: audit/2026-10-23/findings.csv; rendered checklist "Technical Blocker Checklist - REVIEW.md".
- Not issued in this run:
  - F-013 (homepage Wednesday hours in LocalBusiness schema): the schema kind needs entity_approved + brand_guide_approved. Not yet met.
  - F-048 (Lakeland post author "wittycow" in Article schema): no Jonie kind is open at audit_approved. Needs a decision on the owner and channel.
- "Blockers cleared" stays open until Jonie returns H-2026-10-23-03-broken_link done and /verify passes it.
- Not yet run: `/verify` (runs once the handoff is marked done).

**Changes (script):** 10 — broken_link ×10

## /build · 2026-10-23 · run 20261023-212602-build-55fa

**Stage 5 — Build plan and blockers.** Paul assigned the blockers to Jonie and Gwen (his VAs). He said the returned proof sheet will name the blog author, so F-048 waits for that.

- Issued H-2026-10-23-04-other to Gwen (blocker, 1 row): F-013, the homepage Wednesday opening time (00:00:00 to 07:00) in the existing local-business setting. Routed as kind `other` because the schema kind waits on entity and brand-guide approval. The full schema is rebuilt in Finish.
- Still open, not issued: F-048 (blog author "wittycow" on the Lakeland post). Waits for the proof sheet's blog author.
- Earlier: H-2026-10-23-03-broken_link to Jonie, 10 rows (F-008 to F-011).
- "Blockers cleared" stays open until both handoffs are marked done and `/verify` passes them.

**Changes (script):** 1 — other ×1

## /discovery · 2026-10-24 · run 20261024-195727-discovery-1534

- Returned sheet saved verbatim: discovery/First Choice Seamless Gutters - Client Proof Sheet - RETURNED.json (form export v1); marked proof_sheet_returned; Drive copy made.
- Facts: 27 recorded — 20 Client Confirmed (A rows, owners, insurance, warranty in writing, 24 h response, free inspection, award, base town Lakeland, family owned, hours, Sebring not served, 20 Polk towns, 10 services kept / Gutter Maintenance stop, listings, $150 offer), 1 Paul Approved (blog author Adrian Buehl, per settled blog_author), 1 Disputed (Plant City), 1 Submitted (question_6 text), 4 [NEED] (minimum charge, payment, financing, subcontracting "n/a").
- Reconciled: Brand Guide D2 (4 unsupported claims), D3 (4 content-risk rows), E (service area + towns note), G (positioning [NEED] + claims to substantiate); Discovery Record §10. Marked reconciled (brand-guide.md#A+D+E+G).
- Reopen logged: audit_plant_city — client says Plant City served; Paul's fact says not served.
- Open for Paul: Plant City; Gutter Maintenance page (client: stop); "licensed" on 8 live pages (no licence held, F-004); founding year (client "25+ years" vs BBB 2021 and review-named owners James/Randall/Will); question_6 and towns_excluded read as not client-written.
- Still blank: after-hours, payment, financing, minimum charge, staff roles, travel fee, job wanted most, customer misconception, all documents.
- Next: Paul reviews the Brand Guide → Approval 2b (brand_guide_approved). Build not started.

**Changes (script):** 3 — drive_file ×2, reconcile ×1
- FACT 2026-10-24T20:00 · run 20261024-195727-discovery-1534 · a-brand-entity-gbp-name-exactly (status, source, quote) · client_confirmed · First Choice Seamless Gutters Inc. · source Client proof sh…
- FACT 2026-10-24T20:00 · run 20261024-195727-discovery-1534 · a-legal-entity-name (status, source, quote) · client_confirmed · First Choice Seamless Gutters Inc. (BBB: Corporation, incorporated 11/2…
- FACT 2026-10-24T20:00 · run 20261024-195727-discovery-1534 · a-phone (status, source, quote) · client_confirmed · (863) 330-3243 (site, GBP, schema agree; BBB also lists 'Other Phone' (863) 320-284…
- FACT 2026-10-24T20:00 · run 20261024-195727-discovery-1534 · a-storefront-or-sab (status, source, quote) · client_confirmed · Service area business (travels to customers) · source Client proof shee…
- FACT 2026-10-24T20:00 · run 20261024-195727-discovery-1534 · d-legal-entity-dba (value, status, source, quote) · client_confirmed · First Choice Seamless Gutters Inc., a corporation (client confirm…
- FACT 2026-10-24T20:00 · run 20261024-195727-discovery-1534 · d-named-staff-for-on-page-use (value, status, source, quote) · client_confirmed · Owners: Adrian Buehl and Rachel Buehl (client confirme…
- … and 22 more decision/fact/flag line(s) in log.md

## /discovery · 2026-10-24 · run 20261024-201520-discovery-2ca6

Your two answers are applied to the Brand Guide and the reconciliation note (2026-10-24).

- Plant City: not served for now. Fact plant-city-served updated (Paul Approved 2026-10-24). The client's "Yes" is recorded but not applied.
  It is out of the area entity row (A5) and the derivation. Section E lists it under exclusions. D3 has a new row: /areas-we-serve/plant-city-fl/
  301s to /areas-we-serve/ under F-015, once the citation check and C4 (no leads) are confirmed. The page is never deleted.
- Gutter Maintenance: it is no longer a standalone service. A new fact row, gutter-maintenance-consolidated (Section D), says its scope moves
  into Gutter Repair and Gutter Cleaning. The D3 row now sends the old URL to a 301 handoff, pointing at the closer of the two pages. Section G
  says to position only the 10 kept services.
- The reconciliation note's two "needs a call" lines are replaced with your dated answers.
- Changes #152 and #153 are logged. Nothing is approved and run.py finish was not run.

Still open:
- The Brand Guide approval waits on you.
- Build has to choose the redirect target for /services/gutter-maintenance/ (Repair or Cleaning).
- decisions-settled.md still shows audit_plant_city as reopened until the records regenerate at finish.

**Changes (script):** 2 — local_file ×2
- FACT 2026-10-24T20:16 · run 20261024-201520-discovery-2ca6 · plant-city-served (value, source) · paul_approved · Not served for now: Plant City is listed nowhere (no Plant City page, not in towns s…
- FACT 2026-10-24T20:16 · run 20261024-201520-discovery-2ca6 · gutter-maintenance-consolidated (new) · paul_approved · Not a standalone service. Its maintenance scope is folded into the Gutter Repair…
- FACT 2026-10-24T20:16 · run 20261024-201520-discovery-2ca6 · a-area-entity (value, source) · submitted · Proposed: Polk County, Florida = Lakeland–Winter Haven MSA (Q501043). Path: Winter Haven → P…

## /build · 2026-10-24 · run 20261024-202120-build-2ab2

- Site plan registered (status.py plan): `build/First Choice Seamless Gutters - Site Plan - REVIEW.md` + `build/site-plan.json`.
- 30 pages: 10 service, 19 location, 1 About; no county hub (F-016); homepage stays on its light-fix route (H1 lock).
- Batches: pilot (Gutter Cleaning + Lakeland; pilot needed — new industry), services 9, locations-west 9, locations-east 9, about 1.
- URLs: all 29 service/location URLs move to root slugs (folders dropped, slugs kept); each lists its live URL in `replaces`
  so the 301s ship with publish. urlcheck passes.
- Gutter Maintenance → 301 to /gutter-cleaning/ (closer page; listed in that row's `replaces`). Plant City not in plan (F-015 hold).
- "The Best" (CM-020): yes on Gutter Cleaning and Gutter Guards; no elsewhere. 6 SERP calls, $0.012 (data/rankings/raw/best-serp/).
- PAA routing filled in data/paa/paa-routing.md: 46 service FAQ, 11 drop, 2 blog. No fan-out file exists.
- CM-013: 3 B2 area variants for 10 service pages (variant list exhausted — reuse is correct per CM-024).
- Evidence gate run --all: 29 BLOCK, About WARN (expected before the facts round).
- Viability: Lakeland and Winter Haven viable; 17 others marked "merge proposal" only because no place research exists yet.
  Plan keeps all 19; re-run viability after /build facts. Flag F-007 raised (ordering).
- Link wheel: 722 rows, wheel check 0 errors, 0 kind-1 Asks.
- Open choices for Paul (asked): plan_unincorporated_pages (recommend keep), plan_lakeland_highlands_page (recommend no page).
- Next: Paul reviews and approves `/approve first-choice-seamless-gutters site_plan`; then `/build facts`.

**Changes (script):** 3 — site_plan ×2, paa_routing ×1
- FLAG 2026-10-24T20:30 · run 20261024-202120-build-2ab2 · F-007 · Viability check (evidence_pack.py viability) runs in build:plan before the facts round's research, with no place store (methodology/…

## /build · 2026-10-24 · run 20261024-203609-build-ddb9

- Applied Paul's three settled site-plan choices; nothing else changed.
  - A (plan_unincorporated_pages): Highland City, Kathleen, Wahneta, Waverly location pages kept; no merge, no 301s.
  - B (plan_lakeland_highlands_page): no Lakeland Highlands page; named in Lakeland's local context only.
  - C (the_best_plan_pages): "The Best" in the H1 on Gutter Cleaning and Gutter Guards only.
- All three matched the first plan's recommendations, so page rows were already correct: counts unchanged.
  - 30 pages: 10 service, 19 location, 1 About. Batches: pilot 2, services 9, locations-west 9, locations-east 9, about 1.
- `build/site-plan.json`: added a `revised` block recording the run and the three settled keys. No page row changed.
- Review sheet: section 1 is now "Choices settled by Paul (closed)" with A, B, C closed; section 4 notes A and B;
  section 6 caveat now records Paul's confirmation; section 9 says the four unincorporated pages are not re-raised.
- Plan re-registered (`status.py plan`); change #191 logged.
- Checks re-run: urlcheck passes; wheel plan 722 rows on 29 pages; wheel check 0 errors; wheel asks 0 kind-1 Asks.
- Still open (unchanged by this run): viability re-check after `/build facts`; Jonie SEOPress handoff (4 items);
  Gwen manual lookup handoff (8 items); flag F-007 (viability ordering).
- Nothing approved. Next: Paul reviews and approves the site plan (`/approve first-choice-seamless-gutters site_plan`), then `/build facts`.

**Changes (script):** 1 — site_plan_revision ×1

## /interview · 2026-10-24 · run 20261024-204250-interview-bece

- Evidence gate blocked svc-gutter-cleaning and loc-lakeland (CM-041).
- Facts question pack written: clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Interview - pilot - 2026-10-24 - REVIEW.md
- 3 questions: service timeframe, service pricing, after-hours and emergency (loc-lakeland). Not sent; Paul reviews and sends.
- Public facts (certifications, city conditions, neighborhoods, places, permit office) go to the researcher, not the client.
- Waive option if Paul chooses: /approve first-choice-seamless-gutters evidence:svc-gutter-cleaning --reason "..." and evidence:loc-lakeland --reason "..."
- Next: when the owner's answers come back, run /interview first-choice-seamless-gutters facts-answers pilot.
- Still open (not blocking this run): broken-link blocker handoffs issued to VA (H-2026-10-23-03-broken_link-01 to -05, +6 more); /verify runs when they return.

## /interview · 2026-10-24 · run 20261024-204753-interview-c729

- Owner answers (relayed by Paul 2026-10-24) saved: clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Answers - pilot - 2026-10-24.md
- Settled under keys: fact:svc-gutter-cleaning:timeframe, fact:svc-gutter-cleaning:pricing, fact:d:emergency. Fact d-emergency-after-hours-reality recorded as client_confirmed.
- Q1 (timeframe) and Q2 (pricing): site statements confirmed true. No specific duration given.
- Q3 (after-hours): available 7 days, emergency after-hours available, GBP hours correct.
- Paul's note on maintenance wording (advertise cleaning instead): consistent with settled gutter-maintenance-consolidated. Wording change on the cleaning page is for Build; any change to the settled decision needs a revision.
- Evidence gate re-run (pilot): still BLOCK.
  - svc-gutter-cleaning: 2 required facts unknown: "What the service includes (scope)" and "How the service is delivered (steps, methods, equipment)". These were not in the answered pack; the owner still needs asking.
  - loc-lakeland: 3 required facts unverified or unknown: city served (site claim, not yet confirmed as a fact); city-specific conditions and neighborhoods (public research, not the client); permit office and named places (public research).
- Open: owner questions on service scope and delivery (not yet asked). Public research for loc-lakeland via the researcher.

- FACT 2026-10-24T20:48 · run 20261024-204753-interview-c729 · d-emergency-after-hours-reality (value, status, source) · client_confirmed · Available 7 days a week; emergency after-hours service avai…

## /interview · 2026-10-24 · run 20261024-205237-interview-c961

- Evidence gate still blocks svc-gutter-cleaning (service scope and service process unknown) and loc-lakeland (public research).
- Client research logged as partial: RL-Service scope-1 and RL-Service process-1. The site text describes scope (clearing outlets, checking elbows, flushing downspouts); no method or equipment found.
- evidence.py questions returned 0 questions after the partial log. The two gap questions were added by hand to the pack; the generator behaviour is flagged F-008 for the system review.
- Pack for Paul to send: clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Interview - pilot - 2026-10-24 - REVIEW.md (2 questions: scope confirm; process and equipment).
- Public research still open for loc-lakeland (researcher): 3-4 named places, permit office. Certifications for svc-gutter-cleaning also still open.
- Waive option if Paul chooses: /approve first-choice-seamless-gutters evidence:svc-gutter-cleaning --reason "..." and evidence:loc-lakeland --reason "..."
- Next: when the owner answers, run /interview first-choice-seamless-gutters facts-answers pilot.

- FLAG 2026-10-24T20:53 · run 20261024-205237-interview-c961 · F-008 · evidence.py questions returns 0 questions for svc-gutter-cleaning scope and process after research.py log records them as partia…

## /interview · 2026-10-24 · run 20261024-205937-interview-aca1

- Owner answers (relayed by Paul 2026-10-24) saved: clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Answers - pilot - Gutter Cleaning - 2026-10-24.md
- Settled under keys: fact:svc-gutter-cleaning:service_scope and fact:svc-gutter-cleaning:service_process.
- Scope: cleaning covers debris, outlets, elbows, downspout flush and water exit checks. Repairs are separate and not in the cleaning price. Underground drains are separate.
- Process: ladders; debris by hand or gutter scoop; hose rinse and downspout flush; blower for loose dry debris when appropriate. No indoor pressure washing; outside washing is a separate service.
- Evidence gate re-run: svc-gutter-cleaning PASS (known 11, unknown 1 which is certifications, public research).
- loc-lakeland still BLOCK: 3 required facts are not known. City served (site claim, unverified), city-specific conditions, and up to 12 neighborhoods are unverified. Named places and permit office are unknown. These are public research for the researcher agent, not owner questions.
- Waive option if Paul chooses: /approve first-choice-seamless-gutters evidence:loc-lakeland --reason "..."
- Open (not blocking this run): broken-link blocker handoffs issued to VA (H-2026-10-23-03-broken_link-01 to -05, +6 more); /verify runs when they return.

## /interview · 2026-10-24 · run 20261024-210035-interview-d9f2

- Researcher logged all five public gaps (summary: clients/first-choice-seamless-gutters/build/evidence/research-pilot.md):
  - Permit office for Lakeland: FOUND. City of Lakeland Building Inspection (inside city limits). https://www.lakelandgov.net/departments/community-economic-development/building-inspection/faqs/
  - Named places: FOUND. Lake Mirror Park, Dixieland Historic District, Florida Southern College, Lake Morton. https://en.wikipedia.org/wiki/Lakeland,_Florida
  - City-specific conditions: PARTIAL. NWS rainy season (May 25 to Oct 10) and hurricane season (Jun 1 to Nov 30). No source found for tree debris or housing age. https://www.weather.gov/tbw/RainySeason
  - Neighborhoods: PARTIAL. Nine named districts from Wikipedia (Beacon Hill-Alta Vista, Biltmore-Cumberland, Dixieland, East Lake Morton, Lake Hunter Terrace, Munn Park, South Lake Morton, Moorehead, Orangewood). City list pages returned 404.
  - Certifications (svc-gutter-cleaning): PARTIAL. BBB Accredited A+ since 8/12/2025. No DBPR licence number or manufacturer certification found. DBPR lookup is interactive and was not queried.
- Research log accepted all five entries. The places store (methodology/places/) is not in this worktree, so places were not checked against it.
- Evidence gate re-run: loc-lakeland still BLOCK (city served, city-specific conditions, neighborhoods unverified). svc-gutter-cleaning still PASS.
- The research findings did not move the gate. The gate reads the page evidence pack, which needs the place and public rows rebuilt by the build step before the gate sees them. Not hand-edited.
- Waive option if Paul chooses: /approve first-choice-seamless-gutters evidence:loc-lakeland --reason "..."
- Open: broken-link blocker handoffs with the VA (H-2026-10-23-03-broken_link-01 to -05, +6 more).

## /interview · 2026-10-24 · run 20261024-210357-interview-1566

- The earlier research log wrote to build/Serving, build/Local context and similar folders, but the pack reads build/pilot/research-log.csv. The four Lakeland findings were re-logged under section pilot (RL-pilot-1 to -4). The place and neighborhood findings are partial where noted.
- Rebuilt: build/pilot/packs/loc-lakeland.md and .json (evidence_pack.py build, page loc-lakeland). Public facts now list the four research results.
- Gaps still listed in the pack: place_entities and permit_office. Both were logged found, but the pack's gap matcher still shows them, so the log keys may not match. Not fixed here.
- Evidence gate re-run: loc-lakeland still BLOCK (known 5, unknown 2, unverified 3). The city-served, city-conditions and neighborhoods items are unverified. svc-gutter-cleaning still PASS.
- Waive option if Paul chooses: /approve first-choice-seamless-gutters evidence:loc-lakeland --reason "..."
- Open: broken-link blocker handoffs with the VA (H-2026-10-23-03-broken_link-01 to -05, +6 more).

## /interview · 2026-10-24 · run 20261024-210625-interview-355e

- Paul asked for the block to be resolved with what is on file. Three page facts for loc-lakeland settled as decisions, each with its source:
  - city_served: client proof sheet confirms all 20 Polk County places, including Lakeland (settled as Client via Paul).
  - local_context: NWS rainy and hurricane season dates; Lakeland rainfall (Wikipedia). Housing stock, tree debris and failure patterns are not sourced and are stated as not stated. Settled as Paul, public research.
  - neighborhoods: nine named Lakeland neighborhoods and historic districts (Wikipedia). Settled as Paul, public research.
- Evidence gate: svc-gutter-cleaning PASS; loc-lakeland PASS (known 8, unknown 2, unverified 0).
- Note: the local_context item settles a weather-only view. Paul should see it at Brand Guide or page review before publication.
- The "by" on the two public items records Paul as the decider because he directed the resolution; no client attribution was made.
- Open: broken-link blocker handoffs with the VA (H-2026-10-23-03-broken_link-01 to -05, +6 more).

## /build · 2026-10-24 · run 20261024-210703-build-c2ee

- First pass stopped before the outlines (client.route unset). Paul chose route A (status.py set); run resumed under the same RUN_ID.
- Evidence gate: svc-gutter-cleaning PASS (known 11 · unknown 1), loc-lakeland PASS (known 8 · unknown 2).
- Review meaning check (no API key → researcher, `reviews.py checked`): clean-up 4, explains 22, response_time 36,
  James 26, Adrian 8, Landon 5, Randall 3, Inc 0 (false staff name). Packs rebuilt (`evidence_pack.py build`).
- `outline.py faq` had no API key: writers used the plan's FAQ picks / the outline's candidates.
- Outlines: build/pilot/outlines/svc-gutter-cleaning.md, loc-lakeland.md (outline.py).
- Drafts (one fresh build subagent each, recorded with page-stage --agent): build/pilot/drafts/svc-gutter-cleaning.md
  (agent ac6baece3cb254cf5, 1 NEED) · build/pilot/drafts/loc-lakeland.md (agent a1830ac2b3155f813, 4 NEEDs).
- Review: build/pilot/drafts-review.csv/.md (copied to Drive) — 1 Ask (kind 2: permit-pull, loc-lakeland), 15 decided
  for you, 3 fixed silently (applied with the answers). Batch pilot → drafts_written.
- Flags: F-009 (service review topics can never be meaning-checked; staff "Inc"), F-010 (spec LOC-02 vs settled
  title_format.location; no placeholder form for the map embed).
- Not done here, by instruction: review.py apply, the write-back, any approval.
- Open: decision key client_route still shows as an open question in records although route A is set.
- Next: Paul answers the sheet — `/build first-choice-seamless-gutters review pilot drafts "<answer line>"`; then
  the write-back, then `/approve first-choice-seamless-gutters batch:pilot:drafts`, then pilot corrections.

**Changes (script):** 1 — drive_file ×1
- FLAG 2026-10-24T21:41 · run 20261024-210703-build-c2ee · F-009 · evidence_pack.py review_topics gives 'service: <name>' topics no facts.json R key, so a service review topic can never be checked by…
- FLAG 2026-10-24T21:48 · run 20261024-210703-build-c2ee · F-010 · Spec LOC-02 (location SEO title 'Brand - GB Category - City, Full State Name') conflicts with Paul's settled title_format.location (…

## /build · 2026-10-24 · run 20261024-215156-build-ae21

- Applied all 16 rows of build/pilot/drafts-apply.json (Paul: "accept all 1a"); none deferred or skipped.
- loc-lakeland: 1 permit-pull — permit NEED removed, page points to the City permit FAQ only (Paul, option a).
  4 FAQ 3 reworded to "How do Lakeland's summer storms affect gutters?", answer opens with the sourced
  wettest-months (June to September) / hurricane-season overlap. 5 HOA review sentence cut. 6 and 7 response-time
  and storm-scheduling NEEDs removed. 2, 3, 9 kept as drafted. 8 map-embed NEED kept as the open item for ship.
- svc-gutter-cleaning: 11 rainy-season NEED filled ("about late May", NWS May 25 to October 10) with the NWS
  RainySeason page as the page's one outbound authority link. 12 "Florida trees" clause cut. 13 "twice a year"
  number dropped, reworded to depend on the trees over the roof. 10, 14, 15, 16 kept.
- Both drafts re-recorded (status.py page-stage --stage draft); placeholders: loc-lakeland 1 (map embed), svc 0.
- Evidence gate re-run for batch pilot: svc-gutter-cleaning PASS, loc-lakeland PASS.
- Next: the pilot write-back (/build writeback pilot), then Paul's drafts approval line. Nothing approved here.

## /build · 2026-10-24 · run 20261024-215547-build-55dc

- Paul decided: the city-level Google Maps embed on the Lakeland page is replaced by the VA when the page is in draft. The [NEED] placeholder stays in build/pilot/drafts/loc-lakeland.md until then.
- Recorded as a settled decision (loc-lakeland:map-embed).
- Open for the VA worklist: replace the Lakeland map embed in the draft before ship. Ship is not run until it is done.
- No other change. Both pilot drafts still pass the evidence gate (svc-gutter-cleaning PASS, loc-lakeland PASS).

## /build · 2026-10-24 · run 20261024-215625-build-f067

- Route: A (system writes). Paul's answer recorded: decision `client_route` settled ("Route A: the system writes the pages.").
- The pilot section's ONE Brand Guide write-back (CM-061, outline route), from the reviewed drafts of run 20261024-215156-build-ae21, before the drafts approval.
- B3 (assignment log): 2 rows — /gutter-cleaning/ (title service name; H1 "Gutter and Downspout Cleaning" + Polk County, Florida; opening rain gutters + seamless gutter contractor + Lakeland–Winter Haven metropolitan area; FAQ H2 Gutter Contractor + Polk County) and /lakeland-fl/ (title Gutter Contractor; H1 Rain Gutters + Lakeland; first H2 Gutter Installation; opening seamless gutters + Polk County, Florida). Reserved homepage variants (Polk County, FL / Gutter Service) unused.
- C1: /gutter-cleaning/ — Gutter Cleaning — H1 "The Best Gutter and Downspout Cleaning in Polk County, Florida".
- C2: /lakeland-fl/ — Lakeland — not the GBP landing page (GBP Website field = homepage); map embed left for the VA (settled loc-lakeland:map-embed).
- C3: 18 rows — 10 H2s, 8 FAQ questions; no collision between the two pages.
- Brand Guide copied to Drive; records rendered; `status.py writeback` recorded (once per section).
- Not done here (by instruction): no approval, no ship. Next is Paul's drafts approval for the pilot.

**Changes (script):** 2 — brand_guide_writeback ×1, drive_file ×1

## /build · 2026-10-24 · run 20261024-220333-build-d450

- Read: decisions.md, approval-record.md, log.md approval entry (2026-10-24T22:01, "batch pilot drafts", SEM items to apply: none), build/pilot/drafts-review.csv, decisions-settled.md.
- Paul approved both pilot drafts (svc-gutter-cleaning, loc-lakeland) as drafted; the review sheet (rows 1-16, U1-U2) has no answer and no note from Paul.
- Wrote build/pilot-corrections.md: corrections none; nothing flagged for a global spec.
- Recorded `status.py pilot-corrections --none` (CM-061 §9 counter).
- No flags raised. No approval, ship, unlock or abort done.

## /interview · 2026-10-24 · run 20261024-220530-interview-f675

## What happened
- Evidence gate blocked 9 service pages in batch `services` (CM-041).
- Generated the facts pack: `clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Interview - services - 2026-10-24 - REVIEW.md` (15 questions, 9 pages).
- Nothing sent. Paul reviews and sends, or waives per page.

## Problems in the pack (not fixed by hand)
- Same question wording repeats for every page (duration and price each appear 6 times, quoting the same site text). Flagged as a script bug.
- Q1/Q3/Q5/Q8/Q10/Q12 quote a phone number and nav text as "what your website says". Paul should trim or reword before sending.
- Certifications, authorizations and training are researched, not asked (research-services.md).
- Scope and process questions for copper, commercial and the rest (Q7, Q14, Q15) are the real gaps; the rest are repeats.

## Next
- Paul: send the pack (or reword), or waive per page with `/approve first-choice-seamless-gutters evidence:<page> --reason "..."`.
- After answers: `/interview first-choice-seamless-gutters facts-answers services`.

- FLAG 2026-10-24T22:05 · run 20261024-220530-interview-f675 · F-011 · evidence.py questions (facts pack, batch services) repeats the same wording for every page: 'Typical job duration' and 'Price ra…

## /interview · 2026-10-24 · run 20261024-221346-interview-5ad3

## What happened
- Paul answered the pack: all site claims still true. He confirmed them himself, not the owner.
- Settled 3 keys: commercial service_scope, copper service_scope, copper service_process.
- Left open: timeframe and pricing (site line was the phone and nav text, no real value).
- Gate re-run: commercial and copper WARN; the other 7 services still BLOCK.

## Next
- Owner must give real timeframe and pricing, or Paul waives per page.

## /build · 2026-10-24 · run 20261024-221856-build-c8ed

- Route A, section `services` on the outline route. Evidence gate re-run: 7 pages BLOCK carried by Paul's valid waivers (grid sha unchanged; `status.py require evidence:<page>` met for all 9), commercial and copper WARN.
- `outline.py build` wrote 9 outlines (build/services/outlines/). FAQ picks fixed by the approved plan; `outline.py faq` not run (no API key route).
- `reviews.py meaning`: no API key. Researcher check skipped — service review topics cannot be marked checked (flag F-012); writers used them as attributed examples only.
- 9 fresh `build` page agents, one per page, all returned; every draft recorded with `status.py page-stage … --stage draft`.
- Drafts: build/services/drafts/<page>.md · results: build/services/results/<page>-draft.md (each lists Chosen values and Evidence gaps).
- Open [NEED] gaps are mostly service_process / service_scope (client facts, waived); no timeframe or price invented; no "licensed", no founding year.
- Review: one checker pass (fresh build agent) → build/services/drafts-findings.json (60 rows: 5 Fix, 55 Fix and list, 0 Ask).
- `review.py sheet` → build/services/drafts-review.csv / .md (0 questions, 55 decided, 5 fixed silently); copied to Drive 02 - Build.
- `status.py batch services --state drafts_written --review-sheet …` done.
- Flag F-013: plan-fixed H1s on 5 service pages use the "Lakeland–Winter Haven" area variant (city names in an H tag vs SVC-07/SVC-12); kept the approved plan.
- Not done (stops here for Paul): `review.py apply` (defaults not yet applied to the drafts), re-record, Brand Guide write-back, approval. No ship.
- Next: Paul answers the sheet with `/build first-choice-seamless-gutters review services drafts "accept all"` (or "accept all except N…"); that run applies, records, writes back, then prints the approval line.

**Changes (script):** 2 — drive_file ×2
- FLAG 2026-10-24T22:20 · run 20261024-221856-build-c8ed · F-012 · evidence_pack.review_topics gives 'service: <name>' topics an empty key list, so a researcher's reviews.py checked can never move th…
- FLAG 2026-10-24T22:37 · run 20261024-221856-build-c8ed · F-013 · Approved site plan fixes service-page H1 area variant 'Lakeland–Winter Haven' (B2 pool) on 5 service pages; it contains city names, …

## /build · 2026-10-25 · run 20261025-135749-build-dc55

- Paul's line: "accept all except 4b, 10b, 19b, 34b, 41b" (recorded in build/services/drafts-apply.json, 55 items).
- Applied 55 of 55 to the 9 services drafts in build/services/drafts/. Not one item was skipped.
  The no-change rows (Keep as drafted, Keep the NEEDs, Keep) changed nothing, as intended.
- H1s switched to Polk County, Florida (option b, Paul):
  svc-aluminum-gutters → "Aluminum Rain Gutters in Polk County, Florida"
  svc-commercial-gutters → "Commercial Gutter Systems in Polk County, Florida"
  svc-copper-gutters → "Copper Gutter Systems in Polk County, Florida"
  svc-gutter-guards → "The Best Gutter Protection Systems in Polk County, Florida"
  svc-gutter-installation → "Gutter Replacement in Polk County, Florida"
- PLAN vs DRAFTS: the approved site plan still has the old Lakeland–Winter Haven H1s for these 5 pages.
  The drafts and the plan no longer match. Paul should decide whether to update the plan.
- Follow-on edits I made (worth a look):
  #39 gutter-installation: cutting the materials H3 left the H2 intro saying "four kinds", so it now says
  "three kinds" and the material-change sentence is gone. The CTA's last two sentences were reworded.
  #50 seamless meta: the sheet's wording ran to 166 characters, so ", Florida" came out to reach 157 (limit 150–160).
  #54 seamless: the CTA's last two sentences were reworded. #16 copper: Half-Round and K-Style were merged into one H3.
- Seen but not changed (outside the 55): the 5 "fixed silently" form fixes in drafts-fixes.json (run c8ed) are
  not in the drafts, e.g. lowercase "galvalume" in the seamless materials H3, the Galvalume opening still saying
  "so it is stiffer", and FAQ first sentences still short on repair, downspouts and aluminum.
- Records: all 9 pages re-recorded (status.py page-stage), with change records #336–#344 (local; old copies in the run snapshot).
- Not done (separate steps): Brand Guide write-back, /approve batch:services:drafts, ship.

**Changes (script):** 9 — draft-review-apply ×9

## /build · 2026-10-25 · run 20261025-142019-build-47a3

## Fixes and revisions recorded
- seamless-gutter-installation: 'galvalume' → 'Galvalume' (materials H3 body); meta (158 chars, all entities) left as revised.
- gutter-repair: 5 FAQ first sentences now 38–45 words; page grade 7.8; E10 passes.
- gutter-downspouts: 5 FAQ first sentences now 36–39 words; page grade 7.0.
- galvalume-gutters: opening split — "…coating that fights rust. Because it is steel, it is stiffer than aluminum."
- aluminum-gutters: 2 FAQ first sentences now 41 and 35 words; page grade 7.1.
- CM-005: the four H3 links on gutter-installation are allowed (CM-022 names "table/H3 links"); not changed.
- Review sheet regenerated: 0 Asks, 0 listed, 55 not raised (decided earlier); review.py apply ran (0 rows).
- REFUSED: status.py page-stage — "a draft is recorded only by its own /build draft run, the batch's write run, or the review run". No page re-recorded; run NOT finished; stopped here.
- Pre-existing E10 paragraph overs left as-is (outside the fixes): aluminum cost FAQ, downspouts process H2, galvalume x2, seamless meta + highest-rated FAQ.

## /build · 2026-10-25 · run 20261025-142837-build-a824

## What happened
- Recorded the nine service drafts as drafted (draft stage) with status.py page-stage.
- Review answers: "accept all". The five H1 changes from Paul's earlier answer (4b, 10b, 19b, 34b, 41b: switch H1 to "Polk County, Florida") are already in the drafts; the regenerated sheet has no rows for them, so they could not be named in the answer.
- Earlier apply record (55 answers, including the H1 choices) is in commit 4a6e14c.

## Still open
- Approved site plan still lists the old Lakeland–Winter Haven H1s for the five pages; plan and drafts differ.
- Paragraphs still over grade 10: aluminum cost FAQ, downspouts process H2, two sections on the Galvalume page, seamless meta and "highest rated" FAQ.
- Brand Guide write-back and ship not run.

## /build · 2026-10-25 · run 20261025-143023-build-18ec

## What happened
- The services section's one Brand Guide write-back, from the nine reviewed drafts (review applied "accept all", run a824).
- B3: 9 rows added (category and area variant per position: title, H1, opening, first H2, FAQ H2), each pointing to its draft.
- C1: 9 service rows added with the drafts' H1s (all area "Polk County, Florida"; "The Best" only on Gutter Guards, settled).
- C2: no change (no location pages in this section).
- C3: 76 rows added (37 H2, 39 FAQ). Checked: no duplicates within the section or with the pilot's 18 rows.
- `status.py writeback` recorded (no refusal); change #363 logged; records rendered; brand-guide.md copied to Drive.
- Values come from the drafts, not the result files: five H1s switched to "Polk County, Florida" by Paul's earlier answer.

## Still open (not blocking this step)
- The approved site plan still lists Lakeland–Winter Haven H1s for five pages; the Brand Guide now holds the draft H1s.
- On those five pages (aluminum, commercial, copper, gutter guards, gutter installation) the opening paragraph also uses
  "Polk County, Florida", the same area variant as the H1. This is noted only; it was not raised as a finding.
- 27 [NEED] placeholders across the nine drafts (service process/scope mostly); the open timeframe and pricing questions.
- Technical blockers (H-2026-10-23-03 broken_link, 11 items) still issued; ship waits on them, not the approval.

## Next
- Paul: `/approve first-choice-seamless-gutters batch:services:drafts` (the write-back changed no approved value).
- Then `/build write locations-west`.

**Changes (script):** 3 — drive_file ×2, brand_guide_writeback ×1

## /discovery · 2026-10-25 · run 20261025-200645-discovery-96bd

- Paul 2026-10-25: service area state = Florida → settled `area_state`; Section A derivation tagged
  `[Paul Approved 2026-10-25]` (status tag only; entity_approved stays MET).
- Paul 2026-10-25: "no answers, mark them unknown" → all 15 open `[NEED: …]` markers in brand-guide.md now read
  "Unknown — not provided by client (Paul, 2026-10-25)". No figure, date or claim written (CM-016).
- Whole-row Unknown (run.py fact, status unknown): financing, minimum/trip charge, payment methods, subcontracting
  (client's 'n/a' kept in the source, not interpreted).
- Part-row Unknown (run.py fact, status kept Client Confirmed — the client did confirm the rest of the row):
  founding year (25+ years stays), certificate of insurance (insured stays), copy of the written warranty
  (10-year workmanship guarantee in writing stays), roles of April/Matt/Isaac/James (owners stay), travel fee
  (towns-served-client).
- Hand-edited free text (not generated rows): D2 rows "licensed and insured" and "Business Started 2021" (25+ years
  may now be written; exact year Unknown); Section E towns at the edges, travel fee; Section G own sentence,
  most-wanted job, common customer mistake.
- `status.py mark reconciled --file brand-guide.md#A+D+E+G` recorded. brand_guide_approved is VOID → Paul re-approves.
- No service draft uses an Unknown field: drafts state only "insured" and the 10-year written guarantee (both
  Client Confirmed). Evidence packs in build/*/packs/ still show the old `[NEED]` text until Build regenerates them.
- Nothing published; WordPress not touched; no draft pushed; no gate set.

- FACT 2026-10-25T20:08 · run 20261025-200645-discovery-96bd · d-financing-available-provider-terms (value, source) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 2026…
- FACT 2026-10-25T20:08 · run 20261025-200645-discovery-96bd · d-minimum-service-call-or-trip-charge (value, source) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 202…
- FACT 2026-10-25T20:08 · run 20261025-200645-discovery-96bd · d-payment-methods (value, source) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 2026-10-25: no answers,…
- FACT 2026-10-25T20:08 · run 20261025-200645-discovery-96bd · d-services-subcontracted-out (value, source) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 2026-10-25: …
- FACT 2026-10-25T20:08 · run 20261025-200645-discovery-96bd · d-founding-year-years-in-business (value, source) · client_confirmed · In business 'well over 25 plus years' (client). Client says BBB '…
- FACT 2026-10-25T20:08 · run 20261025-200645-discovery-96bd · d-insurance-bonded-status (value, source) · client_confirmed · Insured: client confirms the insurance part of 'fully licensed and insure…
- … and 3 more decision/fact/flag line(s) in log.md

## /discovery · 2026-10-25 · run 20261025-201113-discovery-816f

What was done (Paul's instruction, 2026-10-25: five rows fully Unknown, client returns answers later)
- Set fully Unknown (status unknown, value "Unknown — not provided by client (Paul, 2026-10-25)", quote cleared):
  d-founding-year-years-in-business, d-insurance-bonded-status, d-warranty-terms.
- New rows, Unknown: d-staff-roles (Roles of April, Matt, Isaac, James), d-travel-fee (Travel fee).
- Split, not wiped: d-named-staff-for-on-page-use keeps the client-confirmed owners (Adrian and Rachel Buehl,
  used by many packs); towns-served-client keeps the 20 confirmed towns. Their embedded "Unknown" sentences now
  point to the new rows.
- Hand-written Brand Guide text aligned: D2 row 1 (no "insured"), D2 row 4 (no founding year or years figure),
  D3 row 1 (adds "insured"), G (warranty no longer listed as confirmed). Changes #382-384.
- status.py mark reconciled --file brand-guide.md#A+D+E+G. brand_guide_approved is VOID, waiting on Paul.

Drafts that now consume an Unknown field (not edited; Build's call)
- "insured": svc-gutter-cleaning (pilot, approved), svc-aluminum, svc-commercial, svc-copper, svc-galvalume,
  svc-gutter-downspouts, svc-gutter-guards, svc-gutter-repair, svc-seamless-gutter-installation.
- 10-year written guarantee: svc-aluminum, svc-copper, svc-galvalume, svc-gutter-downspouts, svc-gutter-guards,
  svc-gutter-installation, svc-seamless-gutter-installation.
- Founding year, staff roles, travel fee: no draft uses them. loc-lakeland: none.

Flag
- F-014: discovery_signed_off shows MET while brand_guide_approved is VOID. Workaround: treat as not signed off.

Next
- Paul: /approve first-choice-seamless-gutters brand_guide_approved (2b) once happy; then Build corrects the drafts above.

**Changes (script):** 3 — brand_guide ×3
- FACT 2026-10-25T20:12 · run 20261025-201113-discovery-816f · d-founding-year-years-in-business (value, status, source, quote) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · sourc…
- FACT 2026-10-25T20:12 · run 20261025-201113-discovery-816f · d-insurance-bonded-status (value, status, source, quote) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, …
- FACT 2026-10-25T20:12 · run 20261025-201113-discovery-816f · d-warranty-terms (value, status, source, quote) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 2026-10-2…
- FACT 2026-10-25T20:12 · run 20261025-201113-discovery-816f · d-staff-roles (new) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 2026-10-25: set fully Unknown until t…
- FACT 2026-10-25T20:12 · run 20261025-201113-discovery-816f · d-named-staff-for-on-page-use (value, source) · client_confirmed · Owners: Adrian Buehl and Rachel Buehl (client confirmed). Other staff…
- FACT 2026-10-25T20:12 · run 20261025-201113-discovery-816f · d-travel-fee (new) · unknown · Unknown — not provided by client (Paul, 2026-10-25) · source Paul, 2026-10-25: set fully Unknown until th…
- … and 2 more decision/fact/flag line(s) in log.md

## /discovery · 2026-10-25 · run 20261025-202228-discovery-6767

- Paul confirmed both claims from a Google review (2026-10-25). Recorded with run.py fact:
  - d-insurance-bonded-status: Unknown → Client Confirmed — "Insured … Certificate of insurance: not on file."
  - d-warranty-terms: Unknown → Client Confirmed — "10-Year Workmanship Guarantee, in writing … Written copy: not on file."
  - Source on both: "Google review, confirmed by Paul 2026-10-25". Brand Guide D rows regenerated from facts.json.
- Hand edits to brand-guide.md (change #399): D2 row 1 now covers only the *licensed* part ("insured" may be
  written); D3 row 1 marks "insured" resolved; Section G warranty note (claim_4) states the confirmed guarantee.
  No Unknown wording remains for either claim. "Licensed" stays unsupported (no licence held).
- Approval effect: brand_guide_approved (brand-guide.md#A+D+E+G) now shows VOID on the status screen — the
  approved sections changed. Not re-approved; Paul decides.
- Drafts using the claims (copy not changed): "insured" in all 9 service drafts and the gutter-cleaning pilot
  draft; the 10-year written guarantee in aluminum, copper, galvalume, downspouts, gutter-guards,
  gutter-installation and seamless-gutter-installation. Both claims now read "confirmed" to the writer.
- Gaps kept as notes, not asked: certificate of insurance and written warranty copy are not on file.
- Nothing approved, published or sent to WordPress.

**Changes (script):** 1 — brand_guide ×1
- FACT 2026-10-25T20:23 · run 20261025-202228-discovery-6767 · d-insurance-bonded-status (value, status, source) · client_confirmed · Insured (confirmed by Paul from a Google review, 2026-10-25). Cer…
- FACT 2026-10-25T20:23 · run 20261025-202228-discovery-6767 · d-warranty-terms (value, status, source) · client_confirmed · 10-Year Workmanship Guarantee, in writing (confirmed by Paul from a Google…

## /build · 2026-10-26 · run 20261026-110346-build-402f

Paul edited the 9 service drafts by hand, outside a run (CM-067). This run records the edited versions again. No agent wrote copy. Nothing is approved and nothing went to WordPress.

## What Paul changed (per page, against the last recorded version)
- svc-aluminum-gutters: [NEED] placeholders for installation steps, scope and profiles replaced with text; two Q&A answers reworded.
- svc-commercial-gutters: steps and sizing filled in; service-scope line filled in.
- svc-copper-gutters: profile and downspout-style line filled in.
- svc-galvalume-gutters: intro and installation steps, scope and downspout pairing filled in.
- svc-gutter-downspouts: install method, sizes, add-ons, cost and grounding text filled in.
- svc-gutter-guards: pre-install cleaning, attachment and guard types filled in.
- svc-gutter-installation: installation steps filled in; new "What Gutter Materials Can You Choose?" section with links to the four material pages; $150 offer line added.
- svc-gutter-repair: repair steps and sealant filled in; several sentences rewritten.
- svc-seamless-gutter-installation: install steps and job scope filled in; meta description reworded.

## Check before approval
These new claims are Paul's words, not yet in facts.json or confirmed by the client. Confirm them, or take them out, before approval:
- "UV-resistant sealant" (repair), "metal-compatible hidden hangers" (Galvalume)
- "two common sizes" 2x3 and 3x4; "3x4 drains a 5-inch gutter faster" (downspouts)
- copper is "half-round and K-style"; drainage add-ons "splash blocks, flexible extensions, rain chains, underground drains"
- guards "attach under the first row of shingles or to the fascia board"; crew cleans gutters before guards go on
- Galvalume downspouts as "the standard pairing"

## Status
- 9 drafts recorded again (page-stage, draft). Change log #414–#422.
- Blockers still open (Jonie's broken-link handoffs). /verify waits; it does not block this step.

**Changes (script):** 9 — draft ×9
- FLAG 2026-10-26T11:04 · run 20261026-110346-build-402f · F-015 · next.py --continue crashed with AttributeError: module 'status' has no attribute 'drafts_drifted' (next.py -> records.py -> status_m…

## /build · 2026-10-26 · run 20261026-110943-build-66b7

- Step: ship, run through seq.py: `publish.py wheel` then `publish.py drafts --all`.
- Step 1 done: `publish.py wheel first-choice-seamless-gutters` rebuilt build/link-wheel.json (script output, no copy touched).
- Step 2 REFUSED (exit 4): "REFUSED — every service and location page ships together — still waiting for:
  locations-west (drafts not approved yet), locations-east (drafts not approved yet)".
- The sequence stopped there. Nothing was pushed to WordPress; no page is a WordPress draft from this run.
- Approved pages that would ship once the rule is met: 10 service pages (pilot svc-gutter-cleaning + services batch of 9)
  and loc-lakeland (pilot). about is planned, not approved.
- Not worked around (ship is all-or-nothing by design, CM-055/P9). Nothing approved, nothing published, no copy edited.
- Note: a first seq.py call was mistyped (`--step ship`) and crashed before running anything; no state was written by it.
- Next: `/build first-choice-seamless-gutters write locations-west`, then locations-east, their reviews, write-backs and
  approvals; then `/build first-choice-seamless-gutters ship`.
- Not blocking writing (P8): the technical blocker handoff H-2026-10-23-03 (11 items) is still issued; /verify when Jonie returns it.

## /interview · 2026-10-26 · run 20261026-111314-interview-9c3d

- Ran interview facts for batch locations-west (9 blocked pages: loc-winter-haven, loc-auburndale, loc-bartow, loc-polk-city, loc-kathleen, loc-highland-city, loc-mulberry, loc-eagle-lake, loc-wahneta).
- Question pack generated with 0 owner questions. Every gap is a public fact for the researcher (build/evidence/research-locations-west.md), or was already answered (plant-city-served).
- Nothing to send to the client from this batch. The pack file is kept as a record only.
- Next: the evidence gate still blocks these pages until the researcher facts are in or Paul waives them with an approve line for evidence of each page.

## /interview · 2026-10-26 · run 20261026-111511-interview-3edf

- Ran `evidence.py questions` for batch locations-east: 9 blocked pages (loc-davenport, loc-haines-city, loc-lake-alfred, loc-lake-hamilton, loc-dundee, loc-lake-wales, loc-waverly, loc-frostproof, loc-fort-meade).
- Result: 0 client questions. Every gap is either a public fact (researcher looks it up in build/evidence/research-locations-east.md) or already answered (plant-city-served, settled).
- Pack written to clients/first-choice-seamless-gutters/interviews/facts/ (locations-east REVIEW.md, 2026-10-26). Nothing to send to the owner.
- No facts changed, no decisions settled, no Brand Guide edits.
- Open: the blocked pages still need the researcher pass before the evidence gate can clear; facts-answers is not needed for this batch unless the research leaves a gap.

## /build · 2026-10-26 · run 20261026-113830-build-374a

- Grids: evidence.py run (9 pages BLOCK at start: local context, neighbourhoods, city served not Known).
- reviews.py extract: 18 topics, 12 with 3+ reviewers.
- Researcher (Sonnet) x3 in parallel, 36 research-log rows (RL-locations-west-1..36), facts files build/evidence/loc-*.facts.json:
  local context (NWS Tampa Bay rainy season, Wikipedia terrain/history), neighbourhoods, place entities (Wikidata Q-ids), permit office.
- City served: recorded from the returned proof sheet (all 20 places confirmed), status Client Confirmed — not asked.
- Grids after research: 6 PASS (winter-haven, auburndale, bartow, polk-city, kathleen, highland-city), 3 WARN
  (mulberry: neighbourhoods + permit page partial; eagle-lake: neighbourhoods partial; wahneta: neighbourhoods not found,
  2 place entities only). 0 BLOCK.
- evidence.py questions: "no page is blocked" (writes nothing). Owner-only facts written by hand as 4 client questions:
  build/locations-west/questions.json → settled.py filter kept 4/4 → questions.py check passed → REVIEW file
  interviews/facts/First Choice Seamless Gutters - Facts Interview - locations-west - 2026-10-26 - REVIEW.md (4 questions verified).
- Open questions logged (--ask): fact:locations-west:permit_handling, :hoa_approval, :historic_homes, :neighborhoods_worked.
- Flags: F-018 (research-log lost 7 rows under parallel writes; re-logged), F-019 (questions step writes no set without a
  block), F-020 (suggest a Florida/Polk source list).
- Caveats for the writer: some neighbourhoods are from listing sites only (polk-city, kathleen, highland-city, mulberry,
  eagle-lake); Mulberry and Polk City city sites returned 403 (address/phone from directories/search excerpts);
  Auburndale neighbourhoods seen in agenda snippets only; no Census median year built found anywhere.
- Next: Paul sends the 4 questions; pages may also be written now (no block) — /build first-choice-seamless-gutters write locations-west.

- FLAG 2026-10-26T11:38 · run 20261026-113830-build-374a · F-017 · Facts interview review files for locations-west and locations-east (interviews/facts/*REVIEW.md, 2026-10-26) contain no question tex…
- FLAG 2026-10-26T11:46 · run 20261026-113830-build-374a · F-018 · Parallel researchers writing research.py log at once lost 7 rows of build/locations-west/research-log.csv (mulberry/eagle-lake place…
- FLAG 2026-10-26T11:46 · run 20261026-113830-build-374a · F-019 · evidence.py questions writes nothing when no page blocks, so owner-only Serving-section facts (permit handling, HOA approval, neighb…
- FLAG 2026-10-26T11:46 · run 20261026-113830-build-374a · F-020 · No Florida area source list: suggest methodology/sources/fl-polk.md with Polk County Building Division https://www.polkfl.gov/servic…

## /answers · 2026-10-26 · run 20261026-115900-answers-8ab0

Paul forwarded the owner's answers to the locations-west facts questions (email, 2026-10-26).
Settled: HOA approval standard (yes); historic-home practice (yes, detailed); neighbourhoods broad (no names); permit: assists with permits, who pulls it not stated.
Open: permit responsibility per town; named HOA communities; named historic districts and neighbourhoods.

## /build · 2026-10-26 · run 20261026-120219-build-bc47

- Evidence gate: 6 PASS (Winter Haven, Auburndale, Bartow, Polk City, Kathleen, Highland City), 3 WARN (Mulberry, Eagle Lake, Wahneta), 0 blocked.
- Review meaning check (no API key → researcher, reviews.py checked): response_time 56, explains 41, clean-up 12, James 26, Adrian 8, Landon 5, Randall 3, Inc 0. Packs rebuilt (evidence_pack.py build). outline.py faq: no API key, writers used the plan's FAQ picks.
- Outlines: 9 by outline.py (build/locations-west/outlines/).
- Drafts: 9 fresh draft-writer agents (Opus), one per page, each recorded with page-stage --agent. Results in build/locations-west/results/.
- Review: one checker pass → drafts-review.csv/.md (copied to Drive "02 - Build" as "locations-west drafts-review.md"): 0 Ask, 26 decided for you, 86 fixed silently (82 of them similarity LOC-31 rewordings).
- Decided for you (defaults applied, review.py apply): writer values kept (9); "who pulls the permit" NEED cut on all 9 (settled answer: "we assist with building permits"); older-home sentence cut on Kathleen, Mulberry, Wahneta (swap test); public-gap NEEDs cut on Mulberry and Wahneta; Mulberry permit-page NEEDs cut; Kathleen Neighbourhoods H2 dropped (Fox Branch is only planned); Highland City FAQ 3 reworded without "oaks".
- Apply: 9 fresh agents, one per page; every page recorded again; batch locations-west → drafts_written.
- Placeholders left: 18 NEEDs — 9 city map embeds, travel/response time (Winter Haven, Auburndale, Kathleen, Mulberry, Wahneta, Polk City storm FAQ), Winter Haven lake-discharge rule, Auburndale Lakes District colour rule, Kathleen outbuilding gutters. Link tables stay wheel rows.
- Flags: F-021 (meaning checks lost from facts.json R rows), F-022 (pack truncates long page facts), F-023 (LOC-31 flags confirmed boilerplate).
- Not done here: the Brand Guide write-back (its own step, as for services), approval, ship.
- Next: /build first-choice-seamless-gutters writeback locations-west, then /approve first-choice-seamless-gutters batch:locations-west:drafts.

**Changes (script):** 1 — drive_file ×1
- FLAG 2026-10-26T12:15 · run 20261026-120219-build-bc47 · F-021 · Review meaning checks recorded at run c2ee (reviews.py checked → facts.json R rows meaning_checked) were gone by this run: every R r…
- FLAG 2026-10-26T12:15 · run 20261026-120219-build-bc47 · F-022 · evidence_pack.py cuts long page-fact values (local_context, neighborhoods, place_entities, permit_office) mid-sentence in packs/<pag…
- FLAG 2026-10-26T12:15 · run 20261026-120219-build-bc47 · F-023 · similarity.py (LOC-31) raised 82 silent sentence fixes across 9 location drafts, most of them the client's confirmed boilerplate (gu…

## /build · 2026-10-26 · run 20261026-121738-build-762d

## What happened
- The locations-west section's one Brand Guide write-back, from the nine reviewed drafts (review applied, 0 Ask rows, run bc47).
- B3: 9 location rows added (title, H1, first H2, opening category variant; city, opening area and sibling-section area
  variant), each pointing to its draft.
- C1: no change (no service pages in this section).
- C2: 9 location rows added (Winter Haven, Auburndale, Bartow, Polk City, Kathleen, Highland City, Mulberry, Eagle Lake,
  Wahneta); none is the GBP landing page (A11 — the GBP Website field is the homepage).
- C3: 75 rows added (48 H2, 27 FAQ). Checked: no exact duplicates within the section or with the 94 earlier rows.
- `status.py writeback` recorded (no refusal); change #476 logged; records rendered; brand-guide.md copied to Drive.
- brand_guide_approved still MET; no approved value changed (only B3 and C, the system's own sections).
- No facts added; no new [NEED]s from this step.

## Still open (not blocking this step)
- 18 [NEED] placeholders across the nine drafts (travel/response time, local permit and runoff rules, others).
- Every draft opening says "Seamless Gutters" only as part of the company name; the opening variants are recorded in B3.
- Technical blockers (H-2026-10-23-03 broken_link, 11 items) still issued; ship waits on them, not the approval.

## Next
- Paul: `/approve first-choice-seamless-gutters batch:locations-west:drafts` (the write-back changed no approved value).
- Then `/build write locations-east`.

**Changes (script):** 3 — drive_file ×2, brand_guide_writeback ×1

## /interview · 2026-10-26 · run 20261026-163013-interview-7173

- Facts interview, batch locations-east (9 blocked pages: loc-davenport, loc-haines-city, loc-lake-alfred, loc-lake-hamilton, loc-dundee, loc-lake-wales, loc-waverly, loc-frostproof, loc-fort-meade).
- evidence.py questions produced 0 client questions. The gaps are public facts (city conditions, neighborhoods, places, permit office) that the researcher looks up (build/evidence/research-locations-east.md), not Paul or the client. plant-city-served was already answered.
- The REVIEW pack has no questions, so there is nothing for Paul to send. Do not send it.
- Pack file: clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Interview - locations-east - 2026-10-26 - REVIEW.md
- Pack bug to fix in a system session: the "Public facts, not asked" note repeats the same items many times.
- Still open: a waiver or research path for the 9 blocked pages (evidence gate, CM-041); the 20 open client facts (facts-answers all).

## /answers · 2026-10-26 · run 20261026-164329-answers-12fd

- Paul confirmed the city-served fact for the nine locations-east pages: yes, served (all are in Polk County, which the business serves). Settled under fact:loc-<page>:city_served for davenport, haines-city, lake-alfred, lake-hamilton, dundee, lake-wales, waverly, frostproof, fort-meade.
- Two earlier settlements used a mangled key (fact:loc-<page>ity_served) because of a typo in my shell command. Nothing reads those keys. They are still in decisions-settled.md as stray entries and should be removed in a system session.
- evidence.py run --batch locations-east: each page now has 6 known, 2 unverified, 2 unknown. Still BLOCK (block at 2 required gaps).
- Remaining required gaps per page: local context (city-specific conditions) and neighborhoods. Both are public facts for the researcher (build/evidence/research-locations-east.md), not owner questions.
- Supporting gaps (named places, permit office) are also public-fact research items.

## /interview · 2026-10-27 · run 20261027-103205-interview-d789

- Evidence gate blocked 9 pages in batch locations-east (loc-davenport, loc-haines-city, loc-lake-alfred, loc-lake-hamilton, loc-dundee, loc-lake-wales, loc-waverly, loc-frostproof, loc-fort-meade).
- Each block is two required facts per page: City-specific conditions (local_context) and Up to 12 real neighborhoods (neighborhoods); supporting gaps are place_entities and permit_office.
- evidence.py questions wrote the pack with 0 client questions: every gap is a public fact listed in build/evidence/research-locations-east.md (P6, CM-057), so none goes to the owner.
- Pack written: clients/first-choice-seamless-gutters/interviews/facts/First Choice Seamless Gutters - Facts Interview - locations-east - 2026-10-27 - REVIEW.md — nothing for Paul to send.
- Gate re-run (evidence.py run): still 9 BLOCK. No page is cleared by this run.
- Next: the researcher must look up the public facts for these 9 pages (fact:<page>:local_context, :neighborhoods, :place_entities, :permit_office), then the gate re-runs. Waiver remains open to Paul via /approve evidence:<page> --reason.
- Open waits (not changed here): the facts-answers round for the owner (20 open facts) and the blocker handoff from Jonie (/verify).

## /build · 2026-10-27 · run 20261027-120406-build-cccb

Run 20261027-120406-build-cccb (build facts, batch locations-east), finished by the orchestrator.
Researcher checked public facts for the 9 blocked pages: 18 gaps logged (RL-locations-east-1 to 18), plus RL-locations-east-19 for loc-waverly neighborhoods (not found, minimum effort met).
Wrote build/evidence/<page>.facts.json for all 9 (Internally Verified = official or Wikipedia; Needs Review = partial or listing-site only).
Evidence gate re-run: 8 pages WARN (the brief lists their gaps); loc-waverly BLOCKS (2 required facts unknown). Paul decides: owner facts interview for loc-waverly, or /approve evidence:loc-waverly --reason.
Open: methodology/sources/fl-polk.md needs a system session (suggested by researcher; not flagged).

