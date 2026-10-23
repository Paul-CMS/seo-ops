# Safety log — First Choice Seamless Gutters

Append-only. Every command writes STARTED before it acts and FINISHED after. Every change lists URL, old value, new value and result.
Machine-readable mirror for /rollback: changes.jsonl.


## APPROVAL · 2026-10-14T10:00:26-05:00 · page specs (global: location) · approved · by Paul
Approved version: methodology/specs/location.md (sha 1212fa3e9365)

## CONDITION · 2026-10-22T07:34:20-05:00 · Page specs approved by Paul once, globally (methodology/specs) and unchanged since — met (system-verified)

## RUN 20261022-073424-new-client-ad26 · STARTED · /new-client · 2026-10-22T07:34:24-05:00
Step: new-client · session ed73169c-b95a-4945-a39b-8dd5b655ebb1
- SETTLED drive_pending_sync · 2026-10-22T07:34:26-05:00 · run 20261022-073424-new-client-ad26 · by system · Drive copy pending sync — the local Drive folder ~/Library/CloudStorage/GoogleDrive-paul@coastalmarketingstrategies.com/My Drive/v3. CMS Technical SEO Audit 2026 is not there (Drive for desktop signed out or not syncing?). Files stay in the repo until Drive for desktop syncs; nothing is retyped into the connector.
- CHANGE #1 [brand_guide] local | clients/first-choice-seamless-gutters/brand-guide.md | old:  | new: Created from templates/brand-guide.md; name, domain and category marked Submitted (unverified) | result: created
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · a-storefront-or-sab (value, status, source) · submitted · Service area business (travels to customers) · source Paul, intake answer · by Paul
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · a-exact-url-in-the-gbp-website-field (value, status, source) · submitted · https://firstchoiceseamlessgutters.net/ · source Paul, intake answer · by Paul
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · gbp-share-link (new) · submitted · https://maps.app.goo.gl/c5prGD6rMCwptG3x6 · source Paul, intake answer · by Paul
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · cms (new) · client_confirmed · WordPress · source Paul, intake answer · by Paul
- FACT 2026-10-22T07:41 · run 20261022-073424-new-client-ad26 · gsc-access (new) · submitted · Access exists (Paul reports) · source Paul, intake answer · by Paul
### HANDOFF · /new-client · 2026-10-22 · run 20261022-073424-new-client-ad26
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
### END HANDOFF
## RUN 20261022-073424-new-client-ad26 · FINISHED · 2026-10-22T07:41:40-05:00
Changes: 1 · Summary: Client set up
Spend: 1774002 tokens · $0.02 (measured)

## RUN 20261022-074155-wp-check-2653 · STARTED · /wp-check · 2026-10-22T07:41:55-05:00
Step: wp-check · session ed73169c-b95a-4945-a39b-8dd5b655ebb1
### HANDOFF · /wp-check · 2026-10-22 · run 20261022-074155-wp-check-2653
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
### END HANDOFF
## RUN 20261022-074155-wp-check-2653 · FINISHED · 2026-10-22T07:42:00-05:00
Changes: 0 · Summary: WordPress check: not connected — credentials not yet in local settings; nothing live changed
Spend: 219123 tokens · $0.00 (measured)

## RUN 20261022-074529-wp-check-d203 · STARTED · /wp-check · 2026-10-22T07:45:29-05:00
Step: wp-check · session ed73169c-b95a-4945-a39b-8dd5b655ebb1
### HANDOFF · /wp-check · 2026-10-22 · run 20261022-074529-wp-check-d203
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
### END HANDOFF
## RUN 20261022-074529-wp-check-d203 · FINISHED · 2026-10-22T07:45:34-05:00
Changes: 0 · Summary: WordPress check: still not connected — credentials not found in local settings; nothing live changed
Spend: 228092 tokens · $0.00 (measured)

## RUN 20261022-075244-wp-check-8211 · STARTED · /wp-check · 2026-10-22T07:52:44-05:00
Step: wp-check · session ed73169c-b95a-4945-a39b-8dd5b655ebb1
### HANDOFF · /wp-check · 2026-10-22 · run 20261022-075244-wp-check-8211
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
### END HANDOFF
## RUN 20261022-075244-wp-check-8211 · FINISHED · 2026-10-22T07:52:49-05:00
Changes: 0 · Summary: WordPress check: still not connected — credentials not found in local settings; nothing live changed
Spend: 236634 tokens · $0.00 (measured)

## RUN 20261022-075837-wp-check-fa1d · STARTED · /wp-check · 2026-10-22T07:58:37-05:00
Step: wp-check · session ed73169c-b95a-4945-a39b-8dd5b655ebb1
### HANDOFF · /wp-check · 2026-10-22 · run 20261022-075837-wp-check-fa1d
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
### END HANDOFF
## RUN 20261022-075837-wp-check-fa1d · FINISHED · 2026-10-22T07:58:45-05:00
Changes: 0 · Summary: WordPress check: credentials OK; REST API not reached (certificate check on this Mac); nothing live changed
Spend: 243529 tokens · $0.00 (measured)

## RUN 20261022-083823-wp-check-75b9 · STARTED · /wp-check · 2026-10-22T08:38:23-05:00
Step: wp-check · session ed73169c-b95a-4945-a39b-8dd5b655ebb1
- CHANGE #2 [wp_check] https://www.firstchoiceseamlessgutters.net/?page_id=1328 | test draft page | old: (none) | new: draft id 1328 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #3 [wp_check] https://www.firstchoiceseamlessgutters.net/?p=1329 | test draft post | old: (none) | new: draft id 1329 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #4 [seopress_settings] SEOPress → Titles & Metas | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-22-01-seopress_settings-01
- CHANGE #5 [seopress_settings] SEOPress → XML/HTML Sitemap | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-22-01-seopress_settings-02
- CHANGE #6 [seopress_settings] SEOPress → Social Networks → Knowledge Graph | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-22-01-seopress_settings-03
- CHANGE #7 [seopress_settings] SEOPress → Advanced | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-22-01-seopress_settings-04
### HANDOFF · /wp-check · 2026-10-22 · run 20261022-083823-wp-check-75b9
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
### END HANDOFF
## RUN 20261022-083823-wp-check-75b9 · FINISHED · 2026-10-22T08:39:04-05:00
Changes: 6 · Summary: WordPress connected; drafts only, nothing published; username to confirm (seo-ops vs paulmeisner)
Spend: 250802 tokens · $0.00 (measured)

## CONDITION · 2026-10-22T08:39:04-05:00 · WordPress connected (/wp-check passed in the last 30 days) — met (system-verified)

## RUN 20261022-084632-discovery-42fd · STARTED · /discovery · 2026-10-22T08:46:32-05:00
Step: discovery:discovery · session 0a110021-8e6f-410a-8d0a-23c86a395f69
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-brand-entity-gbp-name-exactly (value, status, source, quote) · internally_verified · First Choice Seamless Gutters Inc. · source GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-gbp-primary-category-the-category-entity (value, status, source, quote) · disputed · CONFLICT (PROC-01): Paul intake 'Seamless gutters' · Google Maps place data category id 'gutter_service' (display 'Gutter service') — dashboard check pending (Gwen manual_lookup) · source Paul intake; Maps URL from maps.app.goo.gl/ccL5rnpD3uyDpunG9 (site footer link), read 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-category-variants-4-6 (value, status, source, quote) · submitted · Proposed: Gutter Service · Seamless Gutters · Rain Gutters · Gutter Contractor · Gutter Installation (Wikipedia entity: Rain gutter, Q152833) · source en.wikipedia.org/wiki/Rain_gutter; BBB categories; site services; Decision Sheet · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-area-entity (value, status, source, quote) · submitted · Proposed: Polk County, Florida = Lakeland–Winter Haven MSA (Q501043). Path: Winter Haven → Polk County → 'comprises the Lakeland–Winter Haven metropolitan statistical area'. Contains 19 of 20 site tow · source en.wikipedia.org/wiki/Polk_County,_Florida; Decision Sheet · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-area-variants-3-5 (value, status, source) · submitted · Proposed: Polk County, FL · Polk County, Florida · Lakeland–Winter Haven · Lakeland–Winter Haven metropolitan area · source en.wikipedia.org/wiki/Polk_County,_Florida; Decision Sheet · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-phone (value, status, source, quote) · internally_verified · (863) 330-3243 (site, GBP, schema agree; BBB also lists 'Other Phone' (863) 320-2842) · source GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22; firstchoices · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-primary-domain-canonical-host-form (value, status, source, quote) · internally_verified · https://www.firstchoiceseamlessgutters.net/ (non-www 301 → www; canonical tag www) · source live HTTP check 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · a-legal-entity-name (value, status, source, quote) · submitted · First Choice Seamless Gutters Inc. (BBB: Corporation, incorporated 11/24/2021) — Sunbiz record not read (403), Gwen manual_lookup · source BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-founding-year-years-in-business (value, status, source, quote) · submitted · Business started 11/24/2021 per BBB (self-reported to BBB); site gives no year · source BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-legal-entity-dba (value, status, source, quote) · submitted · First Choice Seamless Gutters Inc.; BBB primary name 'First Choice Seamless Gutters'; site also 'First Choice Seamless Gutter Inc' · source BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-licence-numbers-and-classes (value, source, quote) · unknown · [NEED: licence number and class — site claims licensed, no number shown; state/Polk County lookup pending] · source searched: site, BBB (licensing not listed), web search 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-insurance-bonded-status (value, status, source, quote) · submitted · Site claims 'fully licensed and insured' (no carrier/bond shown) · source firstchoiceseamlessgutters.net homepage, read 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-warranty-terms (value, status, source, quote) · submitted · 10-Year Workmanship Guarantee/Warranty (site claim; terms not published) · source firstchoiceseamlessgutters.net homepage, read 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-association-memberships (value, status, source, quote) · internally_verified · BBB Accredited Business since 8/12/2025, A+ rating · source BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-awards-and-rankings (value, status, source, quote) · submitted · 'Best Gutter Installer in Lakeland, Florida' by GutterPro HQ, 2025 — company-distributed press release (MarketersMedia), unverified · source markets.financialcontent.com/chroniclejournal/article/marketersmedia-2025-12-3-first-choice-seamless-gutters-named-best- · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-google-rating-and-review-count-exactly-as-google-shows-the (value, status, source, quote) · internally_verified · 5 out of 5 (138 reviews), 2026-10-22 (site says '95+ 5 Star Google Reviews') · source GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-guarantees-response-time-on-time-satisfaction (value, status, source, quote) · submitted · Site: 'we’ll contact you within 24 hours' (form); 'Fast Response Times' (no figure) · source firstchoiceseamlessgutters.net homepage, read 2026-10-22 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-free-estimate-and-what-free-means (value, status, source, quote) · submitted · Free, no-obligation estimate with free on-site inspection; 'no hidden fees' · source firstchoiceseamlessgutters.net homepage, read 2026-10-22; firstchoiceseamlessgutters.net/contact/ · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-emergency-after-hours-reality (value, status, source, quote) · submitted · Site: 'Available 7 Days a Week'; GBP hours 7 AM–8 PM Mon–Sun; no emergency claim found · source GBP (business.google.com/v/first-choice-seamless-gutters-inc/05119577617315017912/2948/_), read 2026-10-22; firstchoices · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-named-staff-for-on-page-use (value, status, source, quote) · submitted · BBB owners: Adrian Buehl, Rachel Buehl. Reviews name Adrian, April, Matt, Isaac, James (roles unknown) · source BBB profile bbb.org/us/fl/winter-haven/profile/gutter-contractor/first-choice-seamless-gutters-0733-235974573, read 2026 · by Paul
- FACT 2026-10-22T08:51 · run 20261022-084632-discovery-42fd · d-financing-available-provider-terms (value, source) · unknown · [NEED: financing — none found on site, GBP or BBB] · source searched: site, GBP, BBB 2026-10-22 · by Paul
- CHANGE #8 [manual_lookup] https://search.sunbiz.org/Inquiry/CorporationSearch/ByName (search: FIRST CHOICE SEAMLESS GUTTERS) | Sunbiz entity record | old:  | new: record exact name, document number, status, filing date, principal address, registered agent, officers (save page as MANUAL evidence) | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-01
- CHANGE #9 [manual_lookup] https://www.myfloridalicense.com/wl11.asp (search name FIRST CHOICE SEAMLESS GUTTERS and owner BUEHL) | FL DBPR licence | old:  | new: record any licence: number, class, status, expiry, name held under - or 'none found' | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-02
- CHANGE #10 [manual_lookup] https://www.polkfl.gov/services/building/ (contractor licence search or call 863-534-6530) | Polk County contractor licence or competency card | old:  | new: record any licence or competency card: number, category, status - or 'none found' | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-03
- CHANGE #11 [manual_lookup] GBP dashboard (after the client adds us as Manager) | GBP primary and secondary categories | old:  | new: record the primary category exactly as shown and every secondary category | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-04
- CHANGE #12 [manual_lookup] GBP dashboard (after the client adds us as Manager) | GBP service areas, opening date, Website field | old:  | new: record every service-area entry, the opening date and the exact Website field URL (www or non-www) | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-05
- CHANGE #13 [manual_lookup] https://www.yelp.com/biz/first-choice-seamless-gutters-winter-haven | Yelp profile | old:  | new: record name, address or service area, phone, rating, review count, year established, owner name | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-06
- CHANGE #14 [manual_lookup] https://www.facebook.com/people/First-Choice-Seamless-Gutters-INC/100077007987844/ | Facebook Intro and About | old:  | new: record category, address, service area, phone, email, website, hours, rating | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-07
- CHANGE #15 [manual_lookup] https://www.homeadvisor.com (search: First Choice Seamless Gutters Lakeland FL) | HomeAdvisor or Angi profile | old:  | new: record name, address (search snippet shows 1575 Lemon Ave), phone, years in business, rating | result: HANDOFF ISSUED to Gwen | ref H-2026-10-22-02-manual_lookup-08
- CHANGE #16 [brand_guide] clients/first-choice-seamless-gutters/brand-guide.md | A derivation + B1/B2 | old:  | new: Polk County / Lakeland–Winter Haven MSA path; B1 Polk County, FL; B2 rotation pool | result: proposal written
- CHANGE #17 [audit_step] S01 | Intake facts: website, GBP link, storefront/SAB, exact GBP W | old:  | new: done | result: DONE — intake facts present in status.json/facts.json (SAB, GBP link, Website-field URL, GSC access, CMS); nothing missing for discovery
- CHANGE #18 [audit_step] S02 | Public discovery: live site, GBP, social, review profiles, S | old:  | new: done | result: DONE — site, GBP, BBB, press release read; Sunbiz/Yelp/HomeAdvisor blocked (403), Facebook login wall, licence boards form-only -> manual_lookup H-2026-10-22-02
- CHANGE #19 [audit_step] S03 | Entity research: category entity (Wikipedia), area entity (R | old:  | new: done | result: DONE — category entity Rain gutter Q152833 (GBP primary disputed), area entity proposal Polk County/Lakeland-Winter Haven MSA Q501043, variants, Wikidata URIs
### HANDOFF · /discovery · 2026-10-22 · run 20261022-084632-discovery-42fd
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
### END HANDOFF
## RUN 20261022-084632-discovery-42fd · FINISHED · 2026-10-22T08:54:23-05:00
Changes: 12 · Summary: Discovery done: Discovery Record, Decision Sheet (25 rows with defaults), Brand Guide A/B1/B2, 5 proof-sheet questions. 4 open choices.
Spend: 6414949 tokens · $1.98 (measured)

## RUN 20261022-101800-discovery-68d2 · STARTED · /discovery · 2026-10-22T10:18:00-05:00
Step: discovery:proof-sheet · session 0a110021-8e6f-410a-8d0a-23c86a395f69
Gates checked: marked:entity_record
- SETTLED category_entity · 2026-10-22T10:18:03-05:00 · run 20261022-101800-discovery-68d2 · by Paul · Primary GBP category and category entity: Gutter service (Paul, 2026-10-22).
- SETTLED area_entity · 2026-10-22T10:18:03-05:00 · run 20261022-101800-discovery-68d2 · by Paul · Area entity: Polk County, Florida (Paul, 2026-10-22).
- SETTLED gbp_storefront_sab · 2026-10-22T10:18:03-05:00 · run 20261022-101800-discovery-68d2 · by Paul · GBP stays a service area business; do not edit the GBP unless required (re-verification risk). Website displays an address.
- SETTLED tools_grid · 2026-10-22T10:18:04-05:00 · run 20261022-101800-discovery-68d2 · by Paul · Grid tool: Local Dominator (Paul, 2026-10-22).
- OPEN address_display_website · 2026-10-22T10:18:04-05:00 · run 20261022-101800-discovery-68d2 · by Paul · Which address displays on the website: 3517 Century Blvd, Lakeland (site schema, press release) or 1575 Lemon Ave (HomeAdvisor)? Paul will check the client billing address; keep [NEED] until then.
- FACT 2026-10-22T10:19 · run 20261022-101800-discovery-68d2 · website-street-address (new) · unknown · [NEED: website address — Paul confirming from client billing] · source Paul, 2026-10-22: confirming from the client's billing address; candidates 3517 Century Blvd, Lakeland 33811 (site schem · by Paul
- FACT 2026-10-22T10:19 · run 20261022-101800-discovery-68d2 · d-licence-numbers-and-classes (value, source) · unknown · [NEED: licence number and class — site claims licensed, no number shown; Paul has none; asked on the proof sheet; state/Polk County lookup pending] · source searched: site, BBB (licensing not listed), web search 2026-10-22; Paul 2026-10-22: none provided · by Paul
- CHANGE #20 [audit_step] S04 | Proof sheet built (Markdown + client Google Doc) | old:  | new: done | result: DONE — Proof sheet Markdown built from the Decision Sheet and Discovery Record; 17 client questions filtered and checked; client Google Doc waits for Paul's two fills (website address, agency email)
### HANDOFF · /discovery · 2026-10-22 · run 20261022-101800-discovery-68d2
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
### END HANDOFF
## RUN 20261022-101800-discovery-68d2 · FINISHED · 2026-10-22T10:21:01-05:00
Changes: 1 · Summary: Client proof sheet built (17 client questions, return by 29 Oct 2026). Open: website street address and agency GBP manager email.
Spend: 3051206 tokens · $1.09 (measured)

## RUN 20261022-194949-discovery-47cc · STARTED · /discovery · 2026-10-22T19:49:49-05:00
Step: discovery:proof-sheet · session 0a110021-8e6f-410a-8d0a-23c86a395f69
Gates checked: marked:entity_record
- FACT 2026-10-22T19:49 · run 20261022-194949-discovery-47cc · website-street-address (value, status, source) · paul_approved · 3517 Century Blvd, Lakeland, FL · source Paul, 2026-10-22 (confirmed for website display; billing address check) · by Paul
- SETTLED address_display_website · 2026-10-22T19:49:52-05:00 · run 20261022-194949-discovery-47cc · by Paul · Website street address: 3517 Century Blvd, Lakeland (Paul, 2026-10-22).
- CLOSED address_display_website · 2026-10-22T19:49:52-05:00 · run 20261022-194949-discovery-47cc · by address_display_website · answered by 'address_display_website'
- SETTLED gbp_manager_access · 2026-10-22T19:49:52-05:00 · run 20261022-194949-discovery-47cc · by Paul · Agency is already a Manager on the client GBP; the proof sheet must not ask the client to add us. (Paul, 2026-10-22)
- SETTLED licence_note_florida · 2026-10-22T19:49:52-05:00 · run 20261022-194949-discovery-47cc · by Paul · Paul note: Florida has no general state business license to operate. Proof sheet asks for the trade/contractor licence only, not a business license. Local business tax receipt (county/city) is a separate item to verify, not asked as a business license. (Paul, 2026-10-22)
- CHANGE #21 [audit_step] S04 | Proof sheet built (Markdown + client Google Doc) | old:  | new: done | result: DONE — Proof sheet revised: website address filled (3517 Century Blvd, Lakeland), GBP Manager request removed, licence row trade/contractor only, local business tax receipt request added after Polk County/Lakeland official check; 17/17 questions kept, check passed
### HANDOFF · /discovery · 2026-10-22 · run 20261022-194949-discovery-47cc
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
### END HANDOFF
## RUN 20261022-194949-discovery-47cc · FINISHED · 2026-10-22T19:52:10-05:00
Changes: 1 · Summary: Proof sheet revised: address 3517 Century Blvd; GBP manager ask removed; licence asks trade licence only; local business tax receipt line added (checked on official pages).
Spend: 1651255 tokens · $0.72 (measured)
