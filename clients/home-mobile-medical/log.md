# Safety log — Home Mobile Medical

Append-only. Every command writes STARTED before it acts and FINISHED after. Every change lists URL, old value, new value and result.
Machine-readable mirror for /rollback: changes.jsonl.


## RUN 20261006-112201-new-client-fb9a · STARTED · /new-client · 2026-10-06T11:22:01-05:00
Step: new-client
- CHANGE #1 [local_file] clients/home-mobile-medical/test-run-notes.md | file | old:  | new: created | result: done
- CHANGE #2 [local_file] clients/home-mobile-medical/rename-list.md | file | old:  | new: created | result: done
- CHANGE #3 [local_file] clients/home-mobile-medical/brand-guide.md | file | old:  | new: created | result: done
- DECISION 2026-10-06T11:23 · run 20261006-112201-new-client-fb9a · Sensitivity set by Paul: health_adjacent (classifier said health). No practitioner sign-off; health/safety claims need a named authoritative source, otherwise removed; Paul approves those pages (CM-040).
- CHANGE #4 [local_file] clients/home-mobile-medical/import-proposal.json | file | old:  | new: draft created | result: done
- DECISION 2026-10-06T11:35 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: no Georgia location pages. Decision 037 (Drive Client Decision Log, 2026-10-02) stands for location pages; Savannah GA and Pooler GA leave the location set and are treated like other out-of-area legacy pages.
- DECISION 2026-10-06T11:35 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: the GBP address (2127 Boundary St #5, Beaufort, SC 29902) stays in the site footer so the website and GBP cross-reference. It is not a storefront; the business remains a service-area business and the site must not present a walk-in location.
- DECISION 2026-10-06T11:35 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: Search Console is unavailable; DataforSEO replaces it as the evidence for every removal/redirect/410 candidate (CM-019: no top-100 rankings, no referring domains, not a GBP/citation destination, client confirms no leads).
- DECISION 2026-10-06T11:35 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: no gate is signed at import. Paul signs off once every claim has been proofed and everything has been recorded. Import gates stay pending until then.
- CHANGE #5 [local_file] clients/home-mobile-medical/out-of-area-pages.md | file | old:  | new: created | result: done
- DECISION 2026-10-06T11:43 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: the pre-seo-ops build files (homepage build sheet, service page drafts, location page drafts) are believed lost. None are in Drive. Unless they turn up, those pages are imported as planned, not written; live pages are checked against the site before anything is called a baseline.
- DECISION 2026-10-06T11:46 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: drop Florida and Michigan — all 17 FL/MI pages (6 FL, 11 MI) leave the site architecture.
- DECISION 2026-10-06T11:46 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: out-of-area and retired pages get 301s, not 410s. Replaces 'out-of-area legacy pages get 410s' from the import brief; matches CM-019/CM-001 (never delete; always redirect). Each still needs the CM-019 DataforSEO check before it becomes a candidate; every redirect is a handoff to Jonie.
- DECISION 2026-10-06T12:01 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: Georgia comes off homemobilemedical.com entirely (Savannah hub and all 17 Georgia pages) and becomes its own subdomain or microsite, keeping the main site's area entity clean (South Carolina Lowcountry). Open: client confirmation that Georgia is served (Decision 037 says it is not); subdomain vs separate domain; the microsite is a separate project, not part of this import. Georgia URLs 301 to their equivalent microsite pages once those exist; until then they stay as they are (no redirect to an unrelated SC page).
- DECISION 2026-10-06T12:05 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: DataforSEO evidence (CM-019) runs after the remaining gates are approved, in the normal /discovery data step — no pull inside the import. The 301 list is finished after that pull.
- DECISION 2026-10-06T12:05 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: the client does take jobs in Georgia (supersedes the 'Georgia not served' part of Decision 037 as a business fact). Georgia is served from a separate microsite (own project, own /new-client); homemobilemedical.com stays South Carolina Lowcountry only.
- DECISION 2026-10-06T12:05 · run 20261006-112201-new-client-fb9a · Paul 2026-10-06: a hub may be a metro area if it is a legitimate, verifiable geographic category; otherwise hub by county. Proposed for the hubs: /service-area/charleston/ = Charleston-North Charleston metro area; /service-area/hhi-beaufort/ = Hilton Head Island-Bluffton metro area (or Beaufort County). Names and Wikidata entries to be verified in Build; county-hub spec is still DRAFT. Logged as lessons.md L-008.
- CHANGE #6 [local_file] clients/home-mobile-medical/discovery/claims-proof-list.md | file | old:  | new: created | result: done
- DECISION 2026-10-07T16:51 · run 20261006-112201-new-client-fb9a · Client answers via Paul 2026-10-07: HMM does repairs and maintenance as well as installation (C6-C8 confirmed; scope by brand still open). Team is Jason plus one helper (wording: Jason and his helper, not 'technicians'). Free in-home estimates confirmed; he can also quote from a photo because price is based on stair count. Install is usually one day, 3-4 hours (same-day wording stays 'in most cases'). Brands: Paul checking.
- DECISION 2026-10-07T16:51 · run 20261006-112201-new-client-fb9a · Paul 2026-10-07: keep Stannah as the main dealer reference only if dealer evidence exists. Status: the old Brand Guide calls Stannah 'verified external' but records no link; a web search on 2026-10-07 found no Stannah dealer listing for HMM. Stannah stays unverified until the stannah.com dealer-locator entry or a client document is attached.
- DECISION 2026-10-07T16:51 · run 20261006-112201-new-client-fb9a · Client feature request via Paul 2026-10-07: let visitors upload a photo of their stairs so Jason can quote by phone. Goes into Build as a site-feature handoff to Jonie (form with image upload); privacy wording on the form needed.
- DECISION 2026-10-07T16:51 · run 20261006-112201-new-client-fb9a · A9 legal entity: web search 2026-10-07 found no South Carolina Secretary of State record for Home Mobile Medical (results were North Carolina only). Needs the client's legal name/DBA, or a direct search of businessfilings.sc.gov.
- DECISION 2026-10-07T17:01 · run 20261006-112201-new-client-fb9a · Client/Paul 2026-10-07: outdoor access = porch lifts (raised entrances and decks), existing site copy confirmed. No separate outdoor stair-lift service page or claim unless confirmed. Warranty: manufacturer's warranty only, no HMM warranty. No licence number found: no licence claim published. Homepage reviews (Debbie S, Laura B, Sher D) are placeholders: remove (F1). Legal name: Home Mobile Medical (Paul; no SC SOS record located). D4 wording: 'fitted to your staircase'.
- DECISION 2026-10-07T17:01 · run 20261006-112201-new-client-fb9a · Paul 2026-10-07 (E1/E3): keep a safety-standards statement as a true commitment, not a regulatory-compliance claim. Proposed wording drops 'and regulations' and names the standard actually followed: the manufacturer's installation instructions (health-adjacent rule CM-040).
- DECISION 2026-10-07T17:01 · run 20261006-112201-new-client-fb9a · Paul 2026-10-07 (A8): primary GBP category Mobility equipment supplier; secondary Medical equipment supplier. Flagged to Paul: the stated rationale names power chairs and ramps (discontinued, Decisions 007-008), and the secondary category signals broad DME, which the entity cleanup removes. Awaiting confirmation whether this is the live GBP setting or a proposal.
- DECISION 2026-10-07T17:09 · run 20261006-112201-new-client-fb9a · Paul 2026-10-07: GBP uses the primary category only (Mobility equipment supplier); 'Medical equipment supplier' is not used as a secondary category. Medicare/tax/ADA/product blog posts are kept as they are until the Blog Decision Map decides. Safety line approved: 'Safety comes first. Jason holds every installation to the highest industry standards and the manufacturer's installation instructions.' All 24 SC towns on the site confirmed served.
- DECISION 2026-10-07T17:09 · run 20261006-112201-new-client-fb9a · Paul 2026-10-07: repair scope is general: any stair lift or any lift type within the service coverage, any brand, not only HMM installs. Site gets a general brand claim ('we install and repair leading brands such as Stannah, ...') with no authorized-dealer wording; the brand names are only those Jason confirms he actually installs or repairs (CM-016).
- CHANGE #7 [local_file] clients/home-mobile-medical/brand-guide.md | file | old: imported Drive copy | new: reconciled to templates/brand-guide.md | result: done
- DECISION 2026-10-07T17:18 · run 20261006-112201-new-client-fb9a · Paul 2026-10-07: brand line confirmed: 'We install and repair stair lifts from leading brands such as Stannah, Bruno and Harmar.' No authorized-dealer wording. Location name: Folly Island. Schema assets (logo, owner photo, ID page, Apple Maps) deferred to Finish: placeholders now, asked again when schema is built. Payment methods: general wording only, no specific list. Audit: option B, the system runs the audit step on the evidence already in Drive (no new crawl, no discovery).
- CHANGE #8 [local_file] clients/home-mobile-medical/import-proposal.json | file | old: draft | new: final proposal (3 gates, 34 planned pages, 8 steps) | result: done

## APPROVAL · 2026-10-07T17:21:12-05:00 · import confirmed by Paul
Gates set from clients/home-mobile-medical/import-proposal.json: entity_approved, proof_sheet_approved, brand_guide_approved
Baseline pages (already live): 0 · remaining pages planned: 34
Site plan generated: clients/home-mobile-medical/build/Home Mobile Medical - Site Plan - IMPORTED.md

## CONDITION · 2026-10-07T17:21:12-05:00 · The client returned the proof sheet (the returned sheet is recorded) — met (system-verified)
### HANDOFF · /new-client · 2026-10-07 · run 20261006-112201-new-client-fb9a
**What I did**
- Imported Home Mobile Medical (mid-stream, old ChatGPT workflow) from the v3 folder `Home Mobile Medical - TMS` (Drive 1Hlfhaelu3mvsAItJgg0Zpi7T2_ccrNRp). Read every file there plus the reference package in the older TMS folder (URL Decision Map, Client Decision Log, Client Gap Sheet). Nothing in Drive was changed.
- Found the old Approval Record entirely unsigned, no Finding Register / Recommendations / Evidence Manifest, and no build files anywhere (Paul: lost). Brief said "stages 0-5 complete"; the records did not support it, so nothing was signed on Drive evidence alone.
- Built the claims proof list (`discovery/claims-proof-list.md`); Paul and the client answered it over two days. Reconciled the Brand Guide into the standard template (`brand-guide.md`). Wrote the out-of-area page list, the rename list and the import proposal.
- Paul approved the import 2026-10-07: entity_approved, proof_sheet_approved, brand_guide_approved (+ proof_sheet_returned condition). 34 pages planned; S01-S05, S09, S10 done, S11 skipped.

**What was decided, and why**
- Sensitivity health_adjacent (Paul; classifier said health). No practitioner sign-off.
- Area entity South Carolina Lowcountry; Georgia is served but only from a separate microsite (own project). Florida and Michigan dropped.
- Destructive URL actions are 301s, never 410s, each after the CM-019 DataforSEO check; DataforSEO replaces Search Console. The pull runs in the normal data step, not inside the import.
- Hubs: /service-area/ (Lowcountry), /service-area/charleston/ (Charleston metro), /service-area/hhi-beaufort/ (Hilton Head Island-Bluffton-Port Royal metro). Rule proposed as lessons.md L-008.
- GBP: primary category only (Mobility equipment supplier). Beaufort GBP address stays in the footer for GBP cross-reference; still an SAB.
- Claims: brand line "Stannah, Bruno and Harmar", no dealer wording; Jason plus one helper; one-day installs of 3-4 hours, "in most cases"; general repairs any brand; manufacturer warranty only; no licence claim; placeholder reviews removed; safety line approved.
- Audit route: option B (system runs the audit on the existing evidence; no new crawl).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| WordPress Editor user + Application Password | Jonie (handoff next), then Paul (.env) | All WordPress work |
| After-hours service, trip charge, positioning answers | Client via Paul | Only the copy that uses them |
| Logo, owner photo, ID page, Apple Maps, 6 county Wikidata IDs | Paul / Finish | Schema |
| Stannah dealer evidence | Paul | Nothing (brand line no longer claims dealer status) |
| Old URL Decision Map rows superseded by Paul's decisions | Audit step | 301 list |
| L-008 metro hubs; county-hub spec DRAFT | Paul | Hub pages in Build |
| Georgia microsite | Paul (new /new-client) | — |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide | clients/home-mobile-medical/brand-guide.md | Approved (import) |
| Claims proof list | clients/home-mobile-medical/discovery/claims-proof-list.md | Marked by Paul |
| Out-of-area pages | clients/home-mobile-medical/out-of-area-pages.md | GA/FL/MI list for the 301 plan |
| Old URL Decision Map | Drive 1xsYWtpEDDiW8Szv545h2zJBZGzRSzZ-M-W2bgaNN370 (older TMS folder) | Input to the audit, partly superseded |
| Crawl and evidence | v3 `01 - Discovery and Audit/Evidence/` | SF 2026-09-18, BL, LNKD, Local Dominator |
| Rename list | clients/home-mobile-medical/rename-list.md | For Paul; nothing renamed |

**What I could not check**
- The live site: the browser pane refused homemobilemedical.com and fetches failed a certificate check. All site quotes are from the 2026-09-18 crawl.
- GBP fields directly; SC Secretary of State record (none found).

**Anything the next agent would otherwise get wrong**
- Nothing was ever built: all 34 pages are planned, not written. The "IMPORTED" site plan is only a page list — re-run the full site plan after the audit.
- The old URL Decision Map predates Paul's decisions: its Georgia KEEP rows, its 410s and the hhi-beaufort split are all superseded. Georgia URLs wait for the microsite; FL/MI and retired pages are 301s after DataforSEO.
- Do not use the old Stannah "verified dealer" line or the homepage testimonials.
### END HANDOFF
## RUN 20261006-112201-new-client-fb9a · FINISHED · 2026-10-07T17:21:45-05:00
Changes: 8 · Summary: Client imported from the v3 TMS folder; claims proofed with Paul and the client; Brand Guide reconciled; import approved by Paul (entity, proof sheet, Brand Guide); audit runs next (option B)

## CONDITION · 2026-10-07T17:21:45-05:00 · Client set up (/new-client finished) — met (system-verified)

## RUN 20261007-172152-wp-check-12e0 · STARTED · /wp-check · 2026-10-07T17:21:52-05:00
Step: wp-check
Gates checked: client_setup
- CHANGE #9 [wp_setup] https://homemobilemedical.com/wp-admin/user-new.php | WordPress user | old: none | new: Create user: username [REDACTED], role Editor (never Administrator) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-01-wp_setup-01
- CHANGE #10 [wp_setup] https://homemobilemedical.com/wp-admin/users.php | Application Password | old: none | new: Users → [REDACTED] → Application Passwords → name it [REDACTED] → Add → copy the 24-character password once. Send it to Paul privately (password manager share … | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-01-wp_setup-02
- CHANGE #11 [wp_setup] https://homemobilemedical.com/wp-admin/plugins.php | SEOPress version | old: unknown | new: Report the installed SEOPress version (needs 6.8 or later; free is enough). Do not update anything without asking Paul | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-01-wp_setup-03
### HANDOFF · /wp-check · 2026-10-07 · run 20261007-172152-wp-check-12e0
**What I did**
- Issued handoff H-2026-10-07-01-wp_setup to Jonie: create the `[REDACTED]` Editor user, its Application Password (sent to Paul privately), and report the SEOPress version.
- Gave Paul the exact credential-file lines (`wp.py env-lines home-mobile-medical`).

**What was decided, and why**
- WordPress setup goes to Jonie (gates.json owner for wp_setup). No WordPress connection was attempted: there are no credentials yet.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| [REDACTED] user + Application Password | Jonie | All WordPress work |
| Three credential lines | Paul | /wp-check home-mobile-medical |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Setup worksheet | clients/home-mobile-medical/handoffs/H-2026-10-07-01-wp_setup.md / .csv | Sent to Jonie |

**What I could not check**
- Whether WordPress, SEOPress or Application Passwords are enabled on the site (site unreachable from this session).

**Anything the next agent would otherwise get wrong**
- The connection test is `/wp-check home-mobile-medical`, only after Paul has added the credential lines.
### END HANDOFF
## RUN 20261007-172152-wp-check-12e0 · FINISHED · 2026-10-07T17:22:18-05:00
Changes: 3 · Summary: WordPress setup handoff to Jonie (H-2026-10-07-01-wp_setup)

## RUN 20261007-172720-wp-check-bb94 · STARTED · /wp-check · 2026-10-07T17:27:20-05:00
Step: wp-check
Gates checked: client_setup
- CHANGE #12 [wp_check] https://homemobilemedical.com/?page_id=4166 | test draft page | old: (none) | new: draft id 4166 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #13 [wp_check] https://homemobilemedical.com/?p=4167 | test draft post | old: (none) | new: draft id 4167 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #14 [seopress_settings] SEOPress → Titles & Metas | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-02-seopress_settings-01
- CHANGE #15 [seopress_settings] SEOPress → XML/HTML Sitemap | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-02-seopress_settings-02
- CHANGE #16 [seopress_settings] SEOPress → Social Networks → Knowledge Graph | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-02-seopress_settings-03
- CHANGE #17 [seopress_settings] SEOPress → Advanced | screenshot or note | old:  | new: (record what is set — change nothing) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-07-02-seopress_settings-04
### HANDOFF · /wp-check · 2026-10-07 · run 20261007-172720-wp-check-bb94
**What I did**
- Ran `wp.py check`: credentials present, REST API reachable, logged in as [REDACTED] (Editor), draft page and post created, every SEOPress 6.8+ per-page field written and read back on a test draft. Test drafts trashed; nothing published.
- `wp.py` issued H-2026-10-07-02-seopress_settings to Jonie (4 items) because SEOPress site-wide settings need an Administrator to read.

**What was decided, and why**
- Result: connected. The condition "WordPress connected" is met for 30 days. The account stays Editor (setup §1).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| SEOPress site-wide settings check | Jonie | Audit step S20 evidence |
| Kadence head-code meta key | Found during the WordPress pilot | Schema in Finish |
| WordPress pilot (`--pilot`) | Paul, later | Direct structural writes (titles, robots, canonical, schema) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| SEOPress settings worksheet | clients/home-mobile-medical/handoffs/H-2026-10-07-02-seopress_settings.md / .csv | Sent to Jonie |

**What I could not check**
- SEOPress site-wide settings (Administrator only).

**Anything the next agent would otherwise get wrong**
- H-2026-10-07-01-wp_setup (user + Application Password) is in effect done: the check logged in as [REDACTED]. Ingest Jonie's returned worksheet to close it.
### END HANDOFF
## RUN 20261007-172720-wp-check-bb94 · FINISHED · 2026-10-07T17:28:07-05:00
Changes: 6 · Summary: WordPress connected ([REDACTED] Editor, SEOPress 6.8+ fields OK); SEOPress settings handoff to Jonie

## CONDITION · 2026-10-07T17:28:07-05:00 · WordPress connected (/wp-check passed in the last 30 days) — met (system-verified)

## RUN 20261007-172819-drive-mirror-bbb0 · STARTED · /drive-mirror · 2026-10-07T17:28:19-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #18 [drive_file] https://drive.google.com/file/d/1K8ikedB7cC2kbJVWVmmoMha374zk9b_3/view | archive | old: Home Mobile Medical - Approval Record.md | new: _Archive/Home Mobile Medical - Approval Record - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #19 [drive_file] https://drive.google.com/file/d/1107LvaCe5maXeRjGNt_gJ1xrWgpI2Qe5/view | upload | old: previous version archived as Home Mobile Medical - Approval Record - 2026-10-07.md | new: Home Mobile Medical - Approval Record.md · sha 9bbbed6e689a | result: done | snapshots  clients/home-mobile-medical/snapshots/20261007-172819-drive-mirror-bbb0/0019-new.md
- CHANGE #20 [drive_file] https://drive.google.com/file/d/1Vy-jQRS6kX-osokX99hLfkuByprL3B2M/view | archive | old: Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #21 [drive_file] https://drive.google.com/file/d/12CU6SFMw_P6bj4f_5R1Gt1zCQBZb5tFJ/view | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-07.md | new: Home Mobile Medical - Handoff Log.md · sha ed2a76248a37 | result: done | snapshots  clients/home-mobile-medical/snapshots/20261007-172819-drive-mirror-bbb0/0021-new.md
- CHANGE #22 [drive_file] https://drive.google.com/file/d/1_Fytn9V6t6VgXdyuteVKPBMK5tHw-vUa/view | archive | old: Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #23 [drive_file] https://drive.google.com/file/d/1t0JO6mUr8SFrOedo4BT9qRXXOsHBVBu7/view | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-07.md | new: Home Mobile Medical - Document Checklist.md · sha b116d2db39c3 | result: done | snapshots  clients/home-mobile-medical/snapshots/20261007-172819-drive-mirror-bbb0/0023-new.md
- CHANGE #24 [drive_file] https://docs.google.com/document/d/1lBvQBUQtOul5ti7FGqv1Wfw1O7hsp70ZH_qCX3FHr-E/edit | archive | old: Home Mobile Medical - Brand Guide.md | new: _Archive/Home Mobile Medical - Brand Guide - 2026-10-07 | result: done · renamed and moved, nothing deleted
- CHANGE #25 [drive_file] https://drive.google.com/file/d/1VO6CC1r9Ni-SrVs-8Y5gC6oIr541Q9g7/view | upload | old: previous version archived as Home Mobile Medical - Brand Guide - 2026-10-07 | new: Home Mobile Medical - Brand Guide.md · sha d8df329226ad | result: done | snapshots  clients/home-mobile-medical/snapshots/20261007-172819-drive-mirror-bbb0/0025-new.md
- DECISION 2026-10-07T17:31 · run 20261007-172819-drive-mirror-bbb0 · Paul 2026-10-07 approved archiving the ChatGPT-era Drive records (Handoff Log, Approval Record, Document Checklist, Google Doc Brand Guide): renamed with the date and moved to _Archive; nothing deleted. READ FIRST doc and SUPERSEDED proof sheet left in place (rename list).
### HANDOFF · /drive-mirror · 2026-10-07 · run 20261007-172819-drive-mirror-bbb0
**What I did**
- Archived the four ChatGPT-era records in the v3 folder (dated names, moved to `_Archive`) and uploaded the system's Approval Record, Handoff Log, Document Checklist and Brand Guide as real `.md` files at the client-folder root.

**What was decided, and why**
- Paul approved archiving files the system did not originally upload (CLAUDE.md §8 otherwise allows it only for system uploads). Nothing deleted.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| READ FIRST doc, SUPERSEDED proof sheet, LD→LNKD rename | Paul (rename list) | Nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Drive records | v3 `Home Mobile Medical - TMS/` root | Current as of this run |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- The "00 - … READ FIRST" Google Doc in Deliverables still describes the old ChatGPT audit; the system records at the folder root govern.
### END HANDOFF
## RUN 20261007-172819-drive-mirror-bbb0 · FINISHED · 2026-10-07T17:31:21-05:00
Changes: 8 · Summary: Drive records mirrored (4 archived, 4 uploaded)

## RUN 20261007-173133-discovery-dce1 · STARTED · /discovery · 2026-10-07T17:31:33-05:00
Step: discovery:data
Gates checked: proof_sheet_approved
- CHANGE #26 [audit_step] S20 | SEOPress site-wide settings (title templates, sitemap, noind | old:  | new: skipped | result: SKIPPED — SEOPress site-wide settings not readable as Editor (/wp-check 20261007-172720-wp-check-bb94); one-time VA check issued to Jonie as handoff H-2026-10-07-02-seopress_settings. Re-record S20 done when her returned worksheet is saved. No Administrator access attempted (wordpress-site-setup.md section 5).
- CHANGE #27 [data_prep] clients/home-mobile-medical/data/services.txt | file | old:  | new: seed file: 5 core services for S07/S19/S21 (stair lifts, curved stair lifts, porch lifts, wheelchair lifts, stair lift repair) | result: DONE
- CHANGE #28 [data_prep] clients/home-mobile-medical/data/backlinks/ | file | old:  | new: S08 DataforSEO payloads prepared, not sent: payload-summary.json (backlinks/summary/live), payload-backlinks-p1.json (backlinks/backlinks/live, domain target, … | result: DONE
- CHANGE #29 [data_pull] Home Mobile Medical | reviews task | old:  | new: 10080044-1266-0298-0000-7c408b378ad6 | result: POSTED
- CHANGE #30 [data_pull] homemobilemedical.com | rankings | old:  | new: 115 rows, 0 clusters | result: DONE
- CHANGE #31 [data_pull] Beaufort,Charleston,Hilton Head Island,Bluffton | PAA | old:  | new: 20 queries, 35 questions | result: DONE
- CHANGE #32 [data_pull] Beaufort,Charleston,Hilton Head Island,Bluffton | fan-out | old:  | new: 10 seeds, 354 queries | result: DONE
- CHANGE #33 [data_pull] clients/home-mobile-medical/data/reviews/ | reviews.csv, mentions.csv, customer-language.md | old:  | new: 19 reviews, rating 2.9; listing matched GBP (2127 Boundary St #5, Beaufort, SC 29902; place_id ChIJF8pA_TgM_IgRjCK0oAHmLKg); reviewer self-name redacted from o… | result: DONE
- CHANGE #34 [data_pull] clients/home-mobile-medical/data/backlinks/Home Mobile Medical - DFS - backlinks - 2026-10-07.csv | S08 referring domains per URL | old:  | new: summary: 722 live backlinks, 709 referring domains; 721 rows pulled (1 page); 5 target URLs; raw/summary.json + raw/backlinks-p1.json (git-ignored) | result: DONE
- CHANGE #35 [data_routing] clients/home-mobile-medical/data/paa/paa-routing.md | Intent + Route | old: unrouted | new: 35 routed: 15 service FAQ, 0 location FAQ, 6 blog topic, 14 drop; summary appended | result: DONE
- CHANGE #36 [data_routing] clients/home-mobile-medical/data/fanout/fanout-routing.md | Intent + Route | old: unrouted | new: 354 routed: 138 service H2/FAQ, 124 location FAQ (Charleston 89, Beaufort 35), 47 blog topic, 45 drop; summary appended | result: DONE
- CHANGE #37 [audit_step] S06 | Reviews pull: Google rating, count, recent review text (no r | old:  | new: done | result: DONE — DataforSEO Google reviews, 19 reviews, rating 2.9; listing matched GBP address; reviews 2017-2023 describe the former retail/rental store, none mention lift services; $0.0150
- CHANGE #38 [audit_step] S07 | Rankings + cannibalization: every ranked keyword per URL (to | old:  | new: done | result: DONE — DataforSEO Labs ranked keywords (US, whole domain): 115 rows, 110 keywords, 15 ranking URLs, 0 cannibalization clusters; 25 'best' variants (SC) all without measurable volume; $0.1158
- CHANGE #39 [audit_step] S08 | Backlinks pull: referring domains per URL | old:  | new: done | result: DONE — DataforSEO Backlinks (whole domain, live): 722 backlinks / 709 referring domains; 5 target URLs, homepage holds 708 RDs; $0.0740
- CHANGE #40 [audit_step] S19 | People Also Ask: core services × primary city + top 3 cities | old:  | new: done | result: DONE — 20 PAA queries (5 services x Beaufort, Charleston, Hilton Head Island, Bluffton) -> 35 questions, all routed; 24 SERP calls incl. 4 billed retries after DataforSEO 40101 errors; $0.0480
- CHANGE #41 [audit_step] S21 | Query fan-out (CM-045): core services × primary city + top 3 | old:  | new: done | result: DONE — Query fan-out, 10 seeds (5 services x Beaufort, Charleston; cap 10 per Paul) -> 354 queries, all routed; Hilton Head Island and Bluffton seeds not run; not demand (CM-045, CM-012); $0.0122
### HANDOFF · /discovery · 2026-10-07 · run 20261007-173133-discovery-dce1
**What I did**
- Ran the data step on Paul's approval (~$0.70 estimate, fan-out cap 10): reviews (S06), domain rankings + "best" volumes (S07), backlinks (S08), People Also Ask (S19), query fan-out (S21). 39 DataforSEO calls, **$0.265 actual**. S20 recorded skipped (SEOPress settings need Administrator; Jonie's handoff H-2026-10-07-02).
- Routed 35 PAA questions and 354 fan-out queries; wrote customer-language themes (no reviewer names); aggregated backlinks per URL.

**What was decided, and why**
- Rankings and backlinks pulled for the whole domain so every URL (incl. GA/FL/MI and retired) is covered for CM-019.
- Fan-out kept to 10 seeds (Beaufort, Charleston); Paul did not approve 20.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| S05 crawl tables not yet in `inputs/crawl/` (Drive v3 Evidence) | Audit step | S12 join to all 118 URLs |
| SEOPress settings worksheet | Jonie | S20 → done |
| CM-019 conditions 3–4 for FL/MI (GBP/citation destination; client confirms no leads) | Audit / Paul | Final 301 list |
| Fan-out for Hilton Head Island and Bluffton (+$0.07) | Paul | Optional |
| Confirm ranked_keywords price in dfs_prices.json ($0.012 + $0.00012/row) | Paul | Future --confirmed prompts |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Reviews | clients/home-mobile-medical/data/reviews/ | Done |
| Rankings | clients/home-mobile-medical/data/rankings/ | Done |
| Backlinks | clients/home-mobile-medical/data/backlinks/Home Mobile Medical - DFS - backlinks - 2026-10-07.csv | Done |
| PAA + fan-out routing | clients/home-mobile-medical/data/paa/, data/fanout/ | Done |

**What I could not check**
- Rankings are US-level only (DataforSEO Labs limit).

**Anything the next agent would otherwise get wrong**
- GBP shows 2.9 stars from 19 reviews, all 2017–2023 and about the old walk-in medical-supply/rental store; none mentions lifts. Not CM-020 proof and almost no lift customer language.
- No /services/ page ranks; the homepage (56 keywords) and the Medicare post (17) carry the domain. "Best" variants have no SC volume.
- CM-019 exceptions (rank or have links → Needs Evidence): /savannah-ga/, /service-area/savannah-ga/, /savannah/stair-lift/, /charleston-sc/mobility-ramps/, /service-area/mt-pleasant-sc/, /bluffton-sc/, /bluffton-sc/wheelchair-lift-repair/, /bluffton-sc/stair-lift-installer/, /charleston/stair-lift/, /hilton-head/stair-lift/. No FL/MI URL ranks or has links.
### END HANDOFF
## RUN 20261007-173133-discovery-dce1 · FINISHED · 2026-10-07T19:58:53-05:00
Changes: 16 · Summary: Data step: reviews, rankings, backlinks, PAA, fan-out (/bin/zsh.265); S20 skipped pending Jonie
- REVIEW CONTINUED 2026-10-07T20:32 · after discovery:data (run 20261007-173133-discovery-dce1) · Paul typed /next

## RUN 20261007-203219-discovery-784c · STARTED · /discovery · 2026-10-07T20:32:19-05:00
Step: discovery:audit
Gates checked: entity_approved
- CHANGE #42 [local_file] clients/home-mobile-medical/inputs/crawl/ | files | old:  | new: 8 SF exports 2026-09-18 downloaded read-only from Drive v3 Evidence (internal_all, external_all, page_titles_all, meta_description_all, h1_all, h2_all, links_a… | result: done
- CHANGE #43 [local_file] clients/home-mobile-medical/inputs/ | files | old:  | new: 7 evidence files downloaded read-only from Drive: BL citation-tracker 2026-09-28, CMS blog-inventory 2026-09-18, MANUAL sitemap-and-local-serp, MANUAL local-gr… | result: done
- CHANGE #44 [local_file] clients/home-mobile-medical/audit/2026-10-07/findings.csv | file | old:  | new: Finding Register: 40 findings (13 High, 14 Medium, 13 Low), status draft | result: done
- CHANGE #45 [local_file] clients/home-mobile-medical/audit/2026-10-07/url-decision-map.csv | file | old:  | new: URL Decision Map: 159 rows (118 crawled + 40 uncrawled CMS/sitemap/backlink URLs + 1 Create) with CM-019 C1-C4 columns | result: done
- CHANGE #46 [local_file] clients/home-mobile-medical/audit/2026-10-07/conformance-scorecard.csv | file | old:  | new: S15 conformance scorecard: 159 rows, check IDs HP/SVC/LOC/HUB/ABT/BLG (DRAFT specs, advisory) | result: done
- CHANGE #47 [local_file] clients/home-mobile-medical/audit/2026-10-07/ | S12 working files | old:  | new: scaffold (init_audit.py) + README.md, 00-manifest.csv (SRC-001..027), 00-crosschecks.md (+ manual addendum), audit decision log DEC-LOCAL-001..005, conflicts.c… | result: done
- CHANGE #48 [local_file] clients/home-mobile-medical/audit/2026-10-07/inventories/ | files | old:  | new: urls.csv (ingest), url-inventory.csv, services.csv, locations.csv, citations.csv, backlinks.csv, local-grid.csv (6 Local Dominator measured results), conversio… | result: done
- CHANGE #49 [local_file] clients/home-mobile-medical/audit/2026-10-07/low-items-handoff-list.csv | file | old:  | new: S16 Low items batched into one handoff list (13 items; not issued - Build issues handoffs) | result: done
- DECISION 2026-10-08T07:37 · run 20261007-203219-discovery-784c · Gate B (audit): 7 questions raised. Paul: Q1 CM-019 C4 client confirms no leads for 36 URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy/straight); Q2 redirect targets (defaults: FL/MI -> /services/stair-lifts/, power chairs/scooter lifts -> /services/, ramps -> /services/porch-lifts/); Q3 10 URLs failing CM-019 C1/C2/C3 - keep live (default) or Paul Exception; Q4 OPEN conflict CF-001 homepage H1 lock (BB-313 s3/HP-08) vs HP-06 (default: no H1 change). VA: Q5 /new-homepage/ and /about-us-across-the-web/ status; Q6 live status of 40 uncrawled URLs; Q7 Local Dominator grid centre/device. Until answered, dispositions stay Needs Evidence. Standing exception CM-026 cited for analysis+review. · affects F-003,F-013,F-015,F-026,F-035,F-038
- CHANGE #50 [audit_step] S12 | Ingest + cross-checks | old:  | new: done | result: DONE — Ingest (8/8 SF exports recognised) + crosscheck (host CONTRADICTED = third-party domains only; rendering LIMITATION; coverage OK) + manual addendum (H1 corroborated; LNKD canonical issue contradicted; orphan candidates reconciled; CM-019 C3 method); manifest SRC-001..027 incl. BL, CMS, sitemap, LNKD, 6 grid PDFs, old map, DFS data
- CHANGE #51 [audit_step] S13 | Entity analysis: site vs Brand Guide (triple, NAP, brand sea | old:  | new: done | result: DONE — Entity analysis: 12 findings (F-001..F-012): category entity in homepage title, Georgia on SC site, discontinued services/DME, second NAP, safety claims, unsupported claims, Folly naming, Yemassee heading, GBP reviews 2.9/19 old store, citation NAP/coverage, backlink baseline
- CHANGE #52 [audit_step] S14 | Architecture: every page typed, keep/merge/redirect per CM-0 | old:  | new: done | result: DONE — URL Decision Map 159 rows (all 118 crawled + 40 uncrawled + 1 Create), CM-019 C1-C4 per destructive candidate: 36 pass C1-C3 awaiting C4, 10 fail (Needs Evidence), 18 Georgia Hold-microsite; findings F-013..F-021
- CHANGE #53 [audit_step] S15 | Page conformance: every page scored against its spec (check  | old:  | new: done | result: DONE — Conformance scorecard vs methodology/specs (all DRAFT - advisory): homepage, 5 service, 24 SC location (+9 GA held), 3 hubs (Low cap), about, 21 posts; findings F-022..F-032; checks needing body/full headings marked NE
- CHANGE #54 [audit_step] S16 | Technical findings (Low batched into one handoff) | old:  | new: done | result: DONE — Technical findings F-033..F-040 (all Low) + other Low items batched into one list (13 items) for Build handoff; schema readiness N/A (no structured-data export, S20 pending)
- CHANGE #55 [audit_file] clients/home-mobile-medical/audit/2026-10-07/findings.csv | superseding rows (S17 review) | old: 40 rows, rev 1 | new: 52 rows: 12 rev-2 superseding rows (F-003, F-004, F-009, F-015, F-023, F-026, F-027, F-028, F-030, F-033, F-035, F-038) | result: appended
- CHANGE #56 [audit_file] clients/home-mobile-medical/audit/2026-10-07/url-decision-map.csv | superseding rows (S17 review) | old: 159 rows | new: 167 rows: 8 superseding rows (U-080, U-088, U-090-U-094 redirect candidate withdrawn - fail CM-019 C1/C2; U-089 reference fix) | result: appended
- CHANGE #57 [audit_file] clients/home-mobile-medical/audit/2026-10-07/review-s17.csv | review record (S17) | old:  | new: per-row outcomes: 40 findings + URL map rows | result: created
- CHANGE #58 [audit_file] clients/home-mobile-medical/audit/2026-10-07/ audit-local decision log | DEC-LOCAL-006 (S17 independent review) | old:  | new: Independent review per CM-026 (fresh-context reviewer): 28 confirmed, 12 revised, 0 withdrawn; map 7 destructive recs withdrawn, 1 revised | result: appended
- CHANGE #59 [audit_step] S17 | Fresh-context review of Finding Register + URL Decision Map | old:  | new: done | result: DONE
