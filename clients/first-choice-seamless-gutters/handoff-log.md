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

