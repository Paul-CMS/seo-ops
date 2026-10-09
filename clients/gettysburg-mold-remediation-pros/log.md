# Safety log — Gettysburg Mold Remediation Pros

Append-only. Every command writes STARTED before it acts and FINISHED after. Every change lists URL, old value, new value and result.
Machine-readable mirror for /rollback: changes.jsonl.


## RUN 20261003-153557-new-client-6698 · STARTED · /new-client · 2026-10-03T15:35:57-05:00
Step: new-client
- CHANGE #1 [drive_file] https://drive.google.com/drive/folders/1OsVC_nP_7Bx232B5HrG9cSduqwx6D7qn | folder | old:  | new: Gettysburg Mold Remediation Pros - TMS (01/Evidence, 01/Deliverables, 02, 03, 04, _Archive) | result: done
### HANDOFF · /new-client · 2026-10-03 · run 20261003-153557-new-client-6698
## Setup · 2026-10-03 · run 20261003-153557-new-client-6698

**What I did**
- Created the client record: Gettysburg Mold Remediation Pros, gettysburgpamoldremediationpros.com, full client, industry mold remediation.
- Built the Drive folder `Gettysburg Mold Remediation Pros - TMS` in v3 with the template's folders (01 - Discovery and Audit/Evidence and Deliverables, 02 - Build, 03 - Finish, 04 - Blog, _Archive).
- Created the Brand Guide working copy from the template (every field still blank).
- Started `test-run-notes.md` for this first real run.

**What was decided, and why**
- Not a sensitive client: the category check returned "no" for mold remediation (CM-025). See test-run-notes for the health-claims question.
- The connector can't copy folders, so the template folder tree was rebuilt by hand.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Intake answers: GBP link, storefront or SAB, exact GBP Website URL, GSC/GA4 access | Paul | Discovery |
| WordPress `seo-ops` Editor user + Application Password | Jonie | /wp-check |
| `WP_GETTYSBURG_MOLD_REMEDIATION_PROS_*` lines in .env | Paul | /wp-check |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide | clients/gettysburg-mold-remediation-pros/brand-guide.md | Blank template |
| Drive folder | https://drive.google.com/drive/folders/1OsVC_nP_7Bx232B5HrG9cSduqwx6D7qn | Created |

**What I could not check**
- The GBP listing and the WordPress connection (not set up yet).

**Anything the next agent would otherwise get wrong**
- This is the first real run, so safe fixes are capped at 5 alt texts and 2 broken links until Paul has checked them live (test-run-notes.md).
### END HANDOFF
## RUN 20261003-153557-new-client-6698 · FINISHED · 2026-10-03T15:37:04-05:00
Changes: 1 · Summary: Client set up

## CONDITION · 2026-10-03T15:37:04-05:00 · Client set up (/new-client finished) — met (system-verified)

## RUN 20261003-153748-wp-check-16f1 · STARTED · /wp-check · 2026-10-03T15:37:48-05:00
Step: wp-check
Gates checked: client_setup
### HANDOFF · /wp-check · 2026-10-03 · run 20261003-153748-wp-check-16f1
## WordPress check · 2026-10-03 · run 20261003-153748-wp-check-16f1

**What I did**
- Ran /wp-check. It stopped at the first check because the site's three WordPress lines are not in .env yet. Nothing on the site was touched.

**What was decided, and why**
- Nothing. The check fails safely, so WordPress stays "not connected".

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Create the `seo-ops` Editor user and an Application Password on gettysburgpamoldremediationpros.com (wordpress-site-setup.md §1) | Jonie | /wp-check |
| Add WP_GETTYSBURG_MOLD_REMEDIATION_PROS_URL / _USER / _APP_PASSWORD to .env | Paul | /wp-check |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Setup spec | wordpress/wordpress-site-setup.md | — |

**What I could not check**
- Whether the REST API, the Application Password and SEOPress fields work on this site.

**Anything the next agent would otherwise get wrong**
- WordPress isn't needed until safe fixes after audit approval, so discovery can go ahead without it. Re-run /wp-check once the .env lines are in.
### END HANDOFF
## RUN 20261003-153748-wp-check-16f1 · FINISHED · 2026-10-03T15:38:00-05:00
Changes: 0 · Summary: WordPress check: not connected — credentials not in .env yet

## RUN 20261003-160508-discovery-552a · STARTED · /discovery · 2026-10-03T16:05:08-05:00
Step: discovery:discovery
Gates checked: client_setup
- DECISION 2026-10-03T16:05 · run 20261003-160508-discovery-552a · Paul: sensitivity set to health_adjacent, practitioner sign-off no (CM-025, CM-040)
- DECISION 2026-10-03T16:05 · run 20261003-160508-discovery-552a · Paul: safe-fix cap for alt_text set to 5
- DECISION 2026-10-03T16:05 · run 20261003-160508-discovery-552a · Paul: safe-fix cap for broken_link set to 2
- DECISION 2026-10-03T16:05 · run 20261003-160508-discovery-552a · Intake answers from Paul: no GBP profile, service-area business, confirmed address 498 Wye Alley, Gettysburg, PA 17325, no GSC/GA4 access (CM-019/CM-021: DataforSEO is the only ranking evidence).
- CHANGE #2 [drive_file] https://drive.google.com/file/d/1zA3idZhM3s26SCojoqYOFtMnJ_CAngDs/view?usp=drivesdk | upload | old: (new file) | new: Gettysburg Mold Remediation Pros - Discovery Record - REVIEW.md · sha 09910d98db9c | result: done | snapshots  clients/gettysburg-mold-remediation-pros/snapshots/20261003-160508-discovery-552a/0002-new.md
- CHANGE #3 [audit_step] S01 | Intake facts: website, GBP link, storefront/SAB, exact GBP W | old:  | new: done | result: DONE — Intake facts from Paul as recorded at /new-client (no GBP, SAB, confirmed address, no GSC/GA4, health_adjacent); nothing missing for S02/S03
- CHANGE #4 [audit_step] S02 | Public discovery: live site, GBP, social, review profiles, S | old:  | new: done | result: DONE — Live site (24 sitemap URLs) and web search for name, address, phone, owner, profiles; no third-party profiles found. PA DOS (bot check), PA AG HIC and IICRC directory could not be checked - listed as NEED
- CHANGE #5 [audit_step] S03 | Entity research: category entity (Wikipedia), area entity (R | old:  | new: done | result: DONE — Category candidates verified on Wikipedia/Wikidata (no GBP - open question); area by Russian Doll with path (two-state area; strict result Mid-Atlantic; proposed South Central PA, 5 of 6 cities); variants; reserved homepage variant; Wikidata URIs
- DECISION 2026-10-03T16:16 · run 20261003-160508-discovery-552a · No GBP exists, so BB-106 (GBP primary category = category entity) cannot be applied; recorded as open question Q-01 with three Wikipedia-verified candidates (Mold remediation proposed). Two-state service area (Taneytown MD): strict BB-105 result is Mid-Atlantic; South Central Pennsylvania proposed conditionally (5 of 6 cities). Neither resolved - Paul decides at entity_approved (PROC-01).
- DECISION 2026-10-03T16:16 · run 20261003-160508-discovery-552a · entity_record covers the Discovery Record only; the Brand Guide working copy (Sections A, B, F filled as proposals) is not attached so later Brand Guide edits at reconcile do not reopen entity_approved. Brand Guide not mirrored to Drive yet (per instructions).
### HANDOFF · /discovery · 2026-10-03 · run 20261003-160508-discovery-552a
**What I did**
- S01: took the intake facts as Paul gave them (no GBP, SAB, 498 Wye Alley, no GSC/GA4, health_adjacent).
- S02: read all 24 sitemap pages of the live site and searched the web for the business name, address, phone, owner and review/social profiles. Found no third-party profile of any kind. The PA Department of State search (blocked by a bot check), the PA Attorney General HIC registry and the IICRC directory could not be checked.
- S03: checked category candidates and the area hierarchy on Wikipedia/Wikidata, recorded the Russian Doll path, listed variants, proposed a reserved homepage variant, and collected Wikidata URIs.
- Wrote the Discovery Record (observations, conflicts C-01 to C-10, health claims H-01 to H-17, open questions Q-01 to Q-06) and filled Brand Guide Sections A, B and the Section F Wikidata rows as proposals.
- Uploaded the Discovery Record to Drive `01 - Discovery and Audit/Deliverables/` as a real .md and logged it. Saved a snapshot of the public site to the git-ignored `inputs/public-site-2026-10-03/`.
- Recorded S01–S03 as done. Marked `entity_record` with the Discovery Record.

**What was decided, and why**
- Nothing about the entity was decided. Both entity questions are recorded as open for Paul (PROC-01): there is no GBP for BB-106, and the service area covers two states.
- Proposals for Paul: category **Mold remediation** (Wikidata Q97609893); area **South Central Pennsylvania** (Q7566771), which covers 5 of the 6 cities and leaves out Taneytown, MD. A strict BB-105 reading gives Mid-Atlantic (Q632014). Reserved homepage variant: South Central Pennsylvania / Mold Remediation.
- `entity_record` covers only the Discovery Record, so editing the Brand Guide at reconcile does not reopen entity_approved (logged as a decision).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Q-01 Category entity when there is no GBP (and whether to create a GBP) | Paul | entity_approved |
| Q-02 Area entity: is Taneytown, MD inside the homepage area statement | Paul | entity_approved |
| Q-03 Storefront or SAB (the site presents "Our own building") | Paul / client | entity_approved, later schema |
| Q-04 Category variants "Indoor mold remediation" and "Mold removal": real under BB-109? | Paul | entity_approved |
| Q-05 No public record of "Wye Alley" / 498 Wye Alley was found | Paul | Brand Guide NAP |
| Q-06 The live site is Astro on Vercel with no WordPress markers | Paul | every WordPress-channel step, /wp-check |
| Manual PA DOS, PA AG HIC and IICRC lookups | Gwen | Brand Guide D (legal entity, HIC, certifications) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record | clients/gettysburg-mold-remediation-pros/discovery/Gettysburg Mold Remediation Pros - Discovery Record - REVIEW.md · Drive https://drive.google.com/file/d/1zA3idZhM3s26SCojoqYOFtMnJ_CAngDs/view | REVIEW |
| Brand Guide (A, B, F proposals) | clients/gettysburg-mold-remediation-pros/brand-guide.md | working copy, not mirrored |
| Public site snapshot | clients/gettysburg-mold-remediation-pros/inputs/public-site-2026-10-03/ | git-ignored evidence |

**What I could not check**
- PA Department of State business registry: the portal showed a bot-detection page, and I did not try to get around it.
- PA Attorney General HIC registry and the IICRC directory: both are JavaScript apps, so I did not query them.
- No GBP, Maps or reviews exist to check. No DataforSEO was used.
- The office network intercepts TLS for this domain (issuer `usg_flex_500`). I fetched pages read-only with certificate verification off. This comes from the network, not the client's site.

**Anything the next agent would otherwise get wrong**
- Taneytown is in **Maryland**. The site says it holds no MHIC licence and does no repair work there, so no single MSA/CSA covers the whole service area.
- The site's schema `additionalType` points to a Wikipedia title that now redirects to "Indoor mold".
- The site makes many health claims with no source named (CM-040). They are listed verbatim as observations only: no severity until the audit.
- The live site does not look like WordPress. Settle Q-06 before planning any wp.py work.
### END HANDOFF
## RUN 20261003-160508-discovery-552a · FINISHED · 2026-10-03T16:17:07-05:00
Changes: 4 · Summary: Discovery S01-S03: entity foundation proposed (category and area open for Paul), Discovery Record uploaded

## RUN 20261003-161750-drive-mirror-414c · STARTED · /drive-mirror · 2026-10-03T16:17:50-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #6 [drive_file] https://drive.google.com/file/d/1Hb6UpX6iUP0mzWLRCxWQilBStTRBUbDq/view | archive | old: Gettysburg Mold Remediation Pros - Handoff Log.md | new: _Archive/Gettysburg Mold Remediation Pros - Handoff Log - 2026-10-03.md | result: done · renamed and moved, nothing deleted
- CHANGE #7 [drive_file] https://drive.google.com/file/d/1rqAhs_2qdxC0G92eKRLY_5o4JfsVPtA9/view | upload | old: previous version archived as Gettysburg Mold Remediation Pros - Handoff Log - 2026-10-03.md | new: Gettysburg Mold Remediation Pros - Handoff Log.md · sha 5a6b6e6e55ff | result: done | snapshots  clients/gettysburg-mold-remediation-pros/snapshots/20261003-161750-drive-mirror-414c/0007-new.md
- CHANGE #8 [drive_file] https://drive.google.com/file/d/1beH3Mqk_kZjMXc9oPnr1xGKHVdztup7b/view | archive | old: Gettysburg Mold Remediation Pros - Document Checklist.md | new: _Archive/Gettysburg Mold Remediation Pros - Document Checklist - 2026-10-03.md | result: done · renamed and moved, nothing deleted
- CHANGE #9 [drive_file] https://drive.google.com/file/d/1lQA2pZJUN4z4uckkjVIz9M3JaSBucu4N/view | upload | old: previous version archived as Gettysburg Mold Remediation Pros - Document Checklist - 2026-10-03.md | new: Gettysburg Mold Remediation Pros - Document Checklist.md · sha e04acd9c61d4 | result: done | snapshots  clients/gettysburg-mold-remediation-pros/snapshots/20261003-161750-drive-mirror-414c/0009-new.md
## RUN 20261003-161750-drive-mirror-414c · FINISHED · 2026-10-03T16:19:11-05:00
Changes: 4 · Summary: Drive records mirrored: Handoff Log, Document Checklist (old copies archived with their date)

## MIGRATION · 2026-10-08T12:21:53-05:00 · schema 4 (rewrite 2026-10-08)
Section approvals re-stamped (status columns no longer hashed): 0 · void approvals left void: 0 · now conditions: discovery_signed_off, blockers_cleared

## APPROVAL · 2026-10-08T13:15:46-05:00 · page specs (global) · approved · by Paul
Approved version: methodology/specs/README.md (sha 13bde3165a59)
Approved version: methodology/specs/about.md (sha 633163a215ae)
Approved version: methodology/specs/blog-post.md (sha bb60f76bddb0)
Approved version: methodology/specs/county-hub.md (sha 4ed0d3bfb1d8)
Approved version: methodology/specs/homepage.md (sha 645431d1fd4c)
Approved version: methodology/specs/location.md (sha bf5b163f4357)
Approved version: methodology/specs/service.md (sha 0d679dadad45)

## CONDITION · 2026-10-08T13:15:46-05:00 · Page specs approved by Paul once, globally (methodology/specs) and unchanged since — met (system-verified)

## MIGRATION · 2026-10-09T18:08:52-05:00 · rewrite 2 P4: facts.json
31 facts from Brand Guide A and D · 0 approval stamp(s) re-stamped on the value-only hash · 0 lost
