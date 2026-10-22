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
