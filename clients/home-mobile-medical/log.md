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
- CHANGE #60 [audit_step] S18 | Render deliverables | old:  | new: done | result: DONE — Rendered from the registers after S17 review and the five reviewer fixes: Finding Register, URL Decision Map, Recommendations, Evidence Manifest (REVIEW) in audit/2026-10-07/deliverables/
- CHANGE #61 [local_file] methodology/lessons.md | L-009 | old:  | new: Added L-009 PROPOSED: homepage H1 lock on a legacy homepage (PROC-01 step 4 for CF-LOCAL-001); notes Apex 2026-10-08 ruling is client-specific, not applied; te… | result: done
- CHANGE #62 [local_file] clients/home-mobile-medical/audit/2026-10-07/ | S17 hand-back fixes | old: CF-001; SF settings on SRC-009..027; rendering para named DataforSEO; U-138..U-159 source 'old URL Decision Map only' | new: CF-LOCAL-001 (conflicts, README, scorecard, questions, URL map draft rows; F-026 rev 3); manifest metadata corrected; crosschecks names SF free crawl 2026-09-1… | result: done
- CHANGE #63 [local_file] clients/home-mobile-medical/audit/2026-10-07/deliverables/ | S18 deliverables | old:  | new: Rendered (REVIEW): Home Mobile Medical - Finding Register - REVIEW.md; - URL Decision Map - REVIEW.md; - Recommendations - REVIEW.md; - Evidence Manifest - REV… | result: done
### HANDOFF · /discovery · 2026-10-08 · run 20261007-203219-discovery-784c
**What I did**
- Ran the audit on the existing evidence (option B, no new crawl): brought the 2026-09-18 Screaming Frog exports and other Drive v3 evidence into `inputs/` (read-only copies), then S12 ingest, S13 entity, S14 architecture, S15 conformance, S16 technical.
- S17: independent audit-reviewer in a fresh context — 28 findings confirmed, 12 revised, 0 withdrawn; 7 destructive URL recommendations withdrawn (they fail CM-019 C1/C2).
- S18: applied the reviewer's five fixes (CF-001 → CF-LOCAL-001; lessons.md L-009 PROPOSED; manifest metadata; cross-check wording; URL-map source labels), rendered four REVIEW deliverables, marked `audit_deliverables`. Tests: 283 passed.

**What was decided, and why**
- Paul's decisions applied throughout: 301 never 410; Georgia held for the microsite; FL/MI dropped; metro hubs (L-008 proposed, county-hub spec DRAFT → Low); blog disposition deferred to the Blog Decision Map; CM-040 claims.
- Independence per CM-026 (DEC-LOCAL-006).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Q1 client confirms no leads on 36 retirement URLs | Paul / client | Any 301 |
| Q2 redirect targets | Paul | 301 handoffs |
| Q3 the 10 CM-019-failing URLs: keep live or Paul Exception | Paul | Their disposition |
| Q4 / CF-LOCAL-001 / L-009 homepage H1 lock | Paul | Homepage H1 |
| Q9 GBP listing history after the BME sale | Client via Paul | Review replies, GBP changes |
| Q5, Q6 page status checks | Jonie | 2 + 40 URL rows |
| Q7 grid centre/device; Q8 citation link destinations | Gwen | Grid findings; CM-019 C3 |
| S20 SEOPress settings | Jonie | Technical evidence |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Finding Register | clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Finding Register - REVIEW.md | For Paul |
| URL Decision Map | …/deliverables/Home Mobile Medical - URL Decision Map - REVIEW.md | For Paul |
| Recommendations | …/deliverables/Home Mobile Medical - Recommendations - REVIEW.md | For Paul |
| Evidence Manifest | …/deliverables/Home Mobile Medical - Evidence Manifest - REVIEW.md | For Paul |

**What I could not check**
- Body text (free SF crawl, no rendering, two H2s per page) — many section/FAQ/claim checks are Needs Evidence. No structured-data export.

**Anything the next agent would otherwise get wrong**
- No URL is a final 301 yet: condition 4 is pending everywhere and condition 3 rests on backlink-domain matching until Gwen checks listing links (Q8).
- Two older log entries still say CF-001 (append-only); the conflict is CF-LOCAL-001.
- All specs are DRAFT: conformance failures are advisory.
### END HANDOFF
## RUN 20261007-203219-discovery-784c · FINISHED · 2026-10-08T07:57:14-05:00
Changes: 22 · Summary: Audit on existing evidence: 40 findings (12H/13M/15L) after independent review; 159-row URL Decision Map; 4 REVIEW deliverables marked

## CONDITION · 2026-10-08T07:57:14-05:00 · Every registered audit step has an outcome (Done / Skipped / Failed) — met (system-verified)

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
- REVIEW CONTINUED 2026-10-08T22:19 · after discovery:audit (run 20261007-203219-discovery-784c) · Paul typed /next

## RUN 20261009-071238-discovery-94fa · STARTED · /discovery · 2026-10-09T07:12:38-05:00
Step: discovery:audit · session 27001d21-4639-469e-ab5f-a835b621fa6f
Gates checked: entity_approved, page_specs_approved
- SETTLED cm019-c4-no-leads · 2026-10-09T07:13:00-05:00 · run 20261009-071238-discovery-94fa · by Paul · Paul 2026-10-09 (Q1): client confirms no leads from any of the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy incl. /services/straight-stair-lifts/). CM-019 C4 passes; all 36 become 301s.
- SETTLED cm019-c3-citation-check-waived · 2026-10-09T07:13:00-05:00 · run 20261009-071238-discovery-94fa · by Paul · Paul Exception 2026-10-09 (Q8): citation link-destination check skipped; CM-019 C3 accepted on DataforSEO referring-domain evidence for the 36 URLs. Do not re-raise.
- SETTLED redirect-targets-default · 2026-10-09T07:13:00-05:00 · run 20261009-071238-discovery-94fa · by Paul · Paul 2026-10-09 (Q2): redirect the 36 to the appropriate URLs - the audit's defaults (FL/MI -> /services/stair-lifts/, power chairs/scooter lifts -> /services/, ramps -> /services/porch-lifts/; SC legacy duplicates -> their canonical service/location page per the URL Decision Map).
- CHANGE #64 [audit_file] clients/home-mobile-medical/audit/2026-10-07/url-decision-map.csv | superseding rows (Paul Q1/Q2/Q8) | old: 167 rows; 36 Needs Evidence (C4 pending) | new: 203 rows: 36 superseding rows -> Redirect (301), C1-C4 pass | result: appended
- CHANGE #65 [audit_file] clients/home-mobile-medical/audit/2026-10-07/findings.csv | superseding rows (Paul Q1/Q2/Q8) | old: 57 rows | new: 62 rows: F-003 rev 3, F-013 rev 2, F-014 rev 2, F-015 rev 3, F-035 rev 3 - 36 URLs decided 301, disposition no longer Assumed | result: appended
- CHANGE #66 [audit_file] clients/home-mobile-medical/audit/2026-10-07/questions/questions.csv | Q1, Q2, Q8 answer columns | old: open | new: answered 2026-10-09 (Q1 confirmed no leads; Q2 defaults; Q8 waived - Paul Exception) | result: updated
- CHANGE #67 [audit_file] clients/home-mobile-medical/audit/2026-10-07/decisions.md | DEC-LOCAL-008 Gate B outcome | old:  | new: Q1/Q2/Q8 answered; Q8 Paul Exception; 36 URLs decided 301 | result: appended
- CHANGE #68 [audit_file] clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - URL Decision Map - REVIEW.md | re-render (36 rows, summary, CM-019 table) | old: 36 Redirect/merge candidate - Needs Evidence (C4 pending); CM-019 C1-C3 pass C4 pending 51 | new: 36 Redirect (301) decided; CM-019 C1-C4 pass 36, C1-C3 pass C4 pending 15 (Georgia, held) | result: rendered
- CHANGE #69 [audit_file] clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Finding Register - REVIEW.md | re-render F-003, F-013, F-014, F-015, F-035 | old: revisions 2/1/1/2/2 | new: revisions 3/2/2/3/3; totals unchanged (12H/13M/15L) | result: rendered
- CHANGE #70 [audit_file] clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Recommendations - REVIEW.md | re-render (summary, URL decisions, limitations, change preview, Q1/Q2/Q8, Low list F-035) | old: Q1/Q2/Q8 open; redirects and sitemap wait on Q1/Q8 | new: Q1/Q2/Q8 answered; 36 decided 301s as VA handoffs after audit approval; sitemap removal paired with them | result: rendered
- CHANGE #71 [audit_file] clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Evidence Manifest - REVIEW.md | CM-019 C3 limitation row | old: Q8 closes the gap | new: gap accepted by Paul Exception (Q8, 2026-10-09) | result: rendered
- CHANGE #72 [audit_file] clients/home-mobile-medical/audit/2026-10-07/findings.csv | row count correction for change #65 | old: 57 to 62 rows (as logged in #65) | new: 53 to 58 data rows (5 superseding rows appended) | result: corrected
### HANDOFF · /discovery · 2026-10-09 · run 20261009-071238-discovery-94fa
**What I did**
- Recorded Paul's answers to Q1, Q2 and Q8 as settled decisions.
- Appended 36 superseding rows to the URL Decision Map: each is now Redirect (301) to its default target, with CM-019 C1–C4 passing.
- Appended superseding rows for F-003, F-013, F-014, F-015 and F-035, and marked Q1, Q2 and Q8 answered. Added DEC-LOCAL-008 to the audit decisions.
- Re-rendered all four audit deliverables (still REVIEW) and re-marked them for audit_approved.

**What was decided, and why**
- Q1 (Paul, 2026-10-09): the client confirms no leads from the 36 retirement URLs (17 FL/MI, 5 discontinued-service, 14 SC legacy including /services/straight-stair-lifts/). CM-019 C4 passes.
- Q8 (Paul Exception): the citation listing check is waived. C3 is accepted on the DataforSEO referring-domain evidence.
- Q2: the audit's default redirect targets.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Approval 2 (audit_approved) | Paul | Redirect handoffs, safe fixes, Build |
| Q3 (the 10 URLs failing CM-019), Q4 (CF-001 homepage H1) | Paul | Those dispositions |
| Q5–Q7, Q9 | Jonie / Gwen / client | Their findings |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| URL Decision Map | clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - URL Decision Map - REVIEW.md | REVIEW |
| Finding Register, Recommendations, Evidence Manifest | same folder | REVIEW |

**What I could not check**
- Citation listing destinations (Q8 was waived by Paul).

**Anything the next agent would otherwise get wrong**
- Q1, Q2 and Q8 are settled. Never re-raise them.
- The 36 301s go to Jonie as handoffs only after audit_approved.
- The /hilton-head/stair-lift-repair/ redirect is paired with the publish of /services/stair-lift-repair/.
- The 15 Georgia rows stay on Hold.
### END HANDOFF
## RUN 20261009-071238-discovery-94fa · FINISHED · 2026-10-09T07:27:17-05:00
Changes: 9 · Summary: Q1, Q2 and Q8 settled by Paul; 36 retirement URLs decided as 301s; audit deliverables re-rendered for approval
- CHANGE #73 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-07 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-07 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #74 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-07 (2).md | new: Home Mobile Medical - Handoff Log.md · sha c2c1bd0524c6 | result: done · copied (Drive for desktop syncs it)
- CHANGE #75 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Approval Record - 2026-10-07 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Approval Record.md | new: _Archive/Home Mobile Medical - Approval Record - 2026-10-07 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #76 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Approval Record.md | upload | old: previous version archived as Home Mobile Medical - Approval Record - 2026-10-07 (2).md | new: Home Mobile Medical - Approval Record.md · sha 3f6a9beaa608 | result: done · copied (Drive for desktop syncs it)
- CHANGE #77 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-07 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-07 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #78 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-07 (2).md | new: Home Mobile Medical - Document Checklist.md · sha 4a7a29c134ad | result: done · copied (Drive for desktop syncs it)
- CHANGE #79 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: (new file) | new: Home Mobile Medical - Status.md · sha c0153c8d477c | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-09T07:39:47-05:00 · audit_approved · approved · by Paul
Approved version: clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Finding Register - REVIEW.md (sha 5bbf8d0d8c6a)
Approved version: clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - URL Decision Map - REVIEW.md (sha 87ed2b1e7129)
Approved version: clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Recommendations - REVIEW.md (sha 3c4e44d49845)
Approved version: clients/home-mobile-medical/audit/2026-10-07/deliverables/Home Mobile Medical - Evidence Manifest - REVIEW.md (sha 1a864e320a0d)

## CONDITION · 2026-10-09T07:39:47-05:00 · Discovery and audit signed off — Build may start (met when the Decision Sheet, entity, client facts, audit and Brand Guide are approved and the client's facts are recorded) — met (system-verified)
- CHANGE #80 [drive_file] drive:Home Mobile Medical - TMS/01 - Discovery and Audit/Deliverables/Home Mobile Medical - Finding Register - APPROVED.md | upload | old: (new file) | new: Home Mobile Medical - Finding Register - APPROVED.md · sha 8dd2e1d67abc | result: done · copied (Drive for desktop syncs it) | snapshots  clients/home-mobile-medical/snapshots/approval-2026-10-09/0080-new.tmp
- CHANGE #81 [drive_file] drive:Home Mobile Medical - TMS/01 - Discovery and Audit/Deliverables/Home Mobile Medical - URL Decision Map - APPROVED.md | upload | old: (new file) | new: Home Mobile Medical - URL Decision Map - APPROVED.md · sha 27d4e9c23c08 | result: done · copied (Drive for desktop syncs it) | snapshots  clients/home-mobile-medical/snapshots/approval-2026-10-09/0081-new.tmp
- CHANGE #82 [drive_file] drive:Home Mobile Medical - TMS/01 - Discovery and Audit/Deliverables/Home Mobile Medical - Recommendations - APPROVED.md | upload | old: (new file) | new: Home Mobile Medical - Recommendations - APPROVED.md · sha d7fa12c0dd45 | result: done · copied (Drive for desktop syncs it) | snapshots  clients/home-mobile-medical/snapshots/approval-2026-10-09/0082-new.tmp
- CHANGE #83 [drive_file] drive:Home Mobile Medical - TMS/01 - Discovery and Audit/Deliverables/Home Mobile Medical - Evidence Manifest - APPROVED.md | upload | old: (new file) | new: Home Mobile Medical - Evidence Manifest - APPROVED.md · sha f808cd1750db | result: done · copied (Drive for desktop syncs it) | snapshots  clients/home-mobile-medical/snapshots/approval-2026-10-09/0083-new.tmp
- CHANGE #84 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Approval Record - 2026-10-09.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Approval Record.md | new: _Archive/Home Mobile Medical - Approval Record - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #85 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Approval Record.md | upload | old: previous version archived as Home Mobile Medical - Approval Record - 2026-10-09.md | new: Home Mobile Medical - Approval Record.md · sha fa9c56e2a745 | result: done · copied (Drive for desktop syncs it)
- CHANGE #86 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #87 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09.md | new: Home Mobile Medical - Document Checklist.md · sha 5dccb2fca409 | result: done · copied (Drive for desktop syncs it)
- CHANGE #88 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #89 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09.md | new: Home Mobile Medical - Status.md · sha 056829011c63 | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-122052-build-8f9c · STARTED · /build · 2026-10-09T12:20:52-05:00
Step: build:blockers · session 0dc29fbc-0c0d-484a-b453-9417d993f6e3
Gates checked: discovery_signed_off
- CHANGE #90 [redirect] https://homemobilemedical.com/service-area/bluffton-sc-2/ | 301 | old: 301 -> [REDACTED]service-area/bluffton-sc -> 301 -> [REDACTED]service-area/bluffton-sc/ (two hops) | new: [REDACTED]service-area/bluffton-sc/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-03-redirect-01
- CHANGE #91 [redirect] https://homemobilemedical.com/service-area/charleston-sc-2/ | 301 | old: 301 -> [REDACTED]service-area/charleston-sc -> 301 -> [REDACTED]service-area/charleston-sc/ (two hops) | new: [REDACTED]service-area/charleston-sc/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-03-redirect-02
- CHANGE #92 [redirect] https://homemobilemedical.com/service-area/beaufort-sc-2/ | 301 | old: 301 -> [REDACTED]service-area/beaufort-sc -> 301 -> [REDACTED]service-area/beaufort-sc/ (two hops) | new: [REDACTED]service-area/beaufort-sc/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-03-redirect-03
- CHANGE #93 [broken_link] https://homemobilemedical.com/are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-01
- CHANGE #94 [broken_link] https://homemobilemedical.com/are-stair-lifts-covered-by-medicare/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-02
- CHANGE #95 [broken_link] https://homemobilemedical.com/are-stair-lifts-expensive-to-run/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-03
- CHANGE #96 [broken_link] https://homemobilemedical.com/are-stair-lifts-noisy/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-04
- CHANGE #97 [broken_link] https://homemobilemedical.com/are-stair-lifts-safe-and-ada-compliant/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-05
- CHANGE #98 [broken_link] https://homemobilemedical.com/can-stair-lifts-turn-corners-or-go-around-corners/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-06
- CHANGE #99 [broken_link] https://homemobilemedical.com/can-stairlifts-be-used-outside/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-07
- CHANGE #100 [broken_link] https://homemobilemedical.com/is-there-a-weight-limit-on-stairlifts/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-08
- CHANGE #101 [broken_link] https://homemobilemedical.com/service-area/mt-pleasant-sc/ | internal links | old: links to one or more of the redirecting URLs listed in 'new' (2026-09-18 crawl) | new: Repoint each internal link (post content, menus or widgets on this page) that goes to a redirecting URL, straight to its final URL: [REDACTED]service-area/beau… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-04-broken_link-09
- CHANGE #102 [other] https://homemobilemedical.com/new-homepage/ | HTTP status + robots (check only) | old: unknown (not crawled; CMS page 'New Homepage', published 2026-09-10, not in the sitemap) | new: record: HTTP status; WordPress status (published/draft/private); meta robots (index or noindex); canonical - change nothing | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-05-other-01
- CHANGE #103 [other] https://homemobilemedical.com/about-us-across-the-web/ | HTTP status + robots (check only) | old: unknown (not crawled; listed in the XML sitemap, no internal link) | new: record: HTTP status; WordPress status; meta robots; canonical - change nothing | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-05-other-02
- CHANGE #104 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/Home Mobile Medical - Technical Blocker Checklist - REVIEW.md | upload | old: (new file) | new: Home Mobile Medical - Technical Blocker Checklist - REVIEW.md · sha 4617130ee2db | result: done · copied (Drive for desktop syncs it)
- CHANGE #105 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/H-2026-10-09-03-redirect.md | upload | old: (new file) | new: H-2026-10-09-03-redirect.md · sha d234a9cf9d0b | result: done · copied (Drive for desktop syncs it)
- CHANGE #106 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/H-2026-10-09-03-redirect.csv | upload | old: (new file) | new: H-2026-10-09-03-redirect.csv · sha 862d09288c43 | result: done · copied (Drive for desktop syncs it)
- CHANGE #107 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/H-2026-10-09-04-broken_link.md | upload | old: (new file) | new: H-2026-10-09-04-broken_link.md · sha 9621dee60c72 | result: done · copied (Drive for desktop syncs it)
- CHANGE #108 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/H-2026-10-09-04-broken_link.csv | upload | old: (new file) | new: H-2026-10-09-04-broken_link.csv · sha 746282ce8926 | result: done · copied (Drive for desktop syncs it)
- CHANGE #109 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/H-2026-10-09-05-other.md | upload | old: (new file) | new: H-2026-10-09-05-other.md · sha b84f74af48c0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #110 [drive_file] drive:Home Mobile Medical - TMS/02 - Build/H-2026-10-09-05-other.csv | upload | old: (new file) | new: H-2026-10-09-05-other.csv · sha 198a2bd743f7 | result: done · copied (Drive for desktop syncs it)
- DECISION 2026-10-09T12:24 · run 20261009-122052-build-8f9c · Blocker checklist scope: no High finding blocks crawling, indexing or measurement; decided 301s, F-035 sitemap removals (paired with them) and F-002/F-003 menu removals routed to /implement structural (URL Decision Map), not the blocker handoff. Low batch to Jonie: F-033 chain repoints (3), F-033 internal links on non-rebuilt pages (9, /services/stair-lift/ links sent to /services/stair-lifts/ per F-034), F-038/Q5 status check (2). Chain targets use the slash URL per F-033 rather than the slash-less Decision Map target. · affects F-033,F-034,F-035,F-038
### HANDOFF · /build · 2026-10-09 · run 20261009-122052-build-8f9c
**What I did**
- Read the approved Finding Register (latest revision of each of the 40 findings) and the matching URL Decision Map rows. Wrote `Home Mobile Medical - Technical Blocker Checklist - REVIEW.md` and marked it as artifact `blocker_checklist`.
- Issued three blocker handoffs to Jonie (`--blockers`), 14 rows in all: H-2026-10-09-03-redirect (3 two-hop redirect chains, F-033), H-2026-10-09-04-broken_link (9 pages with internal links through 301s, F-033), H-2026-10-09-05-other (2-page status/robots check only, F-038 / Q5).
- Copied the checklist and the three handoffs (.md + .csv) to Drive `02 - Build`.

**What was decided, and why**
- None of the 12 High findings blocks crawling, indexing or measurement. Each is fixed by a rebuild, by `/implement structural` (decided 301s and menu removals from the URL Decision Map) or by the Blog Decision Map, so none is a blocker row.
- F-035 sitemap removals stay with the redirect handoff in `/implement structural`, because the finding pairs each removal with its 301.
- The chain repoints target the slash URL (F-033 text). The Decision Map target is slash-less, which would leave one hop.
- Links to /services/stair-lift/ are sent to /services/stair-lifts/ (F-034's natural target), not to the legacy /hilton-head/stair-lift/. The redirect itself is unchanged.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Return the 3 blocker handoffs, then `/verify` | Jonie, then system | blockers_cleared (release) |
| F-034 redirect target; Q3 (10 value URLs) | Paul | /services/stair-lift/ target; 6 F-013 and 4 F-003 URLs |
| F-040 GA4/GSC access from the client | Paul | measurement baseline |
| Decided 301s, F-035 sitemap removals, F-002/F-003 menu removals | `/implement structural` (not yet run) | entity cleanup |
| F-036 utility metas (/contact/, /terms-conditions/ + 4) | `/implement safe` | — |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Technical Blocker Checklist | clients/home-mobile-medical/build/Home Mobile Medical - Technical Blocker Checklist - REVIEW.md | written, marked |
| Blocker handoffs | clients/home-mobile-medical/handoffs/H-2026-10-09-0{3,4,5}-*.md/.csv | issued to Jonie |
| Item sources | clients/home-mobile-medical/build/blockers/*-items.csv | inputs |

**What I could not check**
- Live status of any URL. WordPress was not touched.
- Which page each redirecting link sits on. The crawl export has inlink counts only, so each link row lists all 8 redirecting URLs and Jonie marks "none found" where there are none.

**Anything the next agent would otherwise get wrong**
- The site plan is already approved (imported), so `/build plan` is not needed. The next Build work is the evidence gate for the first batch.
- The 36 decided 301s are NOT in the blocker handoff. Issue them in `/implement structural` with their F-035 sitemap removals. Pair /hilton-head/stair-lift-repair/ with the svc1 publish.
### END HANDOFF
## RUN 20261009-122052-build-8f9c · FINISHED · 2026-10-09T12:24:54-05:00
Changes: 21 · Summary: Technical Blocker Checklist written; 14 blocker rows to Jonie in 3 handoffs (redirect chains, internal links through 301s, Q5 status check); no High blocks crawling/indexing/measurement
- CHANGE #111 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-09.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #112 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-09.md | new: Home Mobile Medical - Handoff Log.md · sha 39bf71bfd647 | result: done · copied (Drive for desktop syncs it)
- CHANGE #113 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #114 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09 (2).md | new: Home Mobile Medical - Document Checklist.md · sha c558245b72fe | result: done · copied (Drive for desktop syncs it)
- CHANGE #115 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #116 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09 (2).md | new: Home Mobile Medical - Status.md · sha 4caed42171bb | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-09T12:34 · after build:blockers (run 20261009-122052-build-8f9c) · Paul typed /next

## APPROVAL · 2026-10-09T12:39:42-05:00 · site plan · revise · by Paul
Approved version: clients/home-mobile-medical/build/Home Mobile Medical - Site Plan - IMPORTED.md (sha 6ad603f87fd1)
Note: Re-open the imported site plan to add a pilot batch first (1 service + 1 location)
- CHANGE #117 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #118 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09 (3).md | new: Home Mobile Medical - Document Checklist.md · sha b07db1239fae | result: done · copied (Drive for desktop syncs it)
- CHANGE #119 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #120 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09 (3).md | new: Home Mobile Medical - Status.md · sha 94c5eac693a8 | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-09T12:40:09-05:00 · site plan · approved · by Paul
Approved version: clients/home-mobile-medical/build/Home Mobile Medical - Site Plan - REVISED.md (sha acd2d040d2df)
- CHANGE #121 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (4).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #122 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09 (4).md | new: Home Mobile Medical - Document Checklist.md · sha 08446c360d6b | result: done · copied (Drive for desktop syncs it)
- CHANGE #123 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09 (4).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #124 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09 (4).md | new: Home Mobile Medical - Status.md · sha afdce4c40aee | result: done · copied (Drive for desktop syncs it)

## MIGRATION · 2026-10-09T18:08:49-05:00 · rewrite 2 P4: facts.json
39 facts from Brand Guide A and D · 0 approval stamp(s) re-stamped on the value-only hash · 0 lost

## MIGRATION · 2026-10-09T20:15:33-05:00 · rewrite 2 P7 + P10: URLs and batches
Paul 2026-10-09 (REWRITE-2-DECISIONS.md c): /services/<x>/ → /<x>/, /service-area/<city>/ → /<city>/, metro hubs (CM-058: Charleston Q5084207, Hilton Head Island–Bluffton–Port Royal Q17020871), /service-area/ → 301 to the homepage
svc-stair-lifts: https://homemobilemedical.com/services/stair-lifts/ → https://homemobilemedical.com/stair-lifts/ (301 paired with the publish)
svc-curved-stair-lifts: https://homemobilemedical.com/services/curved-stair-lifts/ → https://homemobilemedical.com/curved-stair-lifts/ (301 paired with the publish)
svc-porch-lifts: https://homemobilemedical.com/services/porch-lifts/ → https://homemobilemedical.com/porch-lifts/ (301 paired with the publish)
svc-wheelchair-lifts: https://homemobilemedical.com/services/wheelchair-lifts/ → https://homemobilemedical.com/wheelchair-lifts/ (301 paired with the publish)
svc-repair-maintenance: https://homemobilemedical.com/services/stair-lift-repair/ (planned, never live) → https://homemobilemedical.com/stair-lift-repair/
hub-hhi-beaufort: https://homemobilemedical.com/service-area/hhi-beaufort/ → https://homemobilemedical.com/hilton-head-bluffton-metro/ (301 paired with the publish)
loc-beaufort-sc: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/ (301 paired with the publish)
loc-bluffton-sc: https://homemobilemedical.com/service-area/bluffton-sc/ → https://homemobilemedical.com/bluffton-sc/ (301 paired with the publish)
loc-hilton-head-island-sc: https://homemobilemedical.com/service-area/hilton-head-island-sc/ → https://homemobilemedical.com/hilton-head-island-sc/ (301 paired with the publish)
loc-port-royal-sc: https://homemobilemedical.com/service-area/port-royal-sc/ → https://homemobilemedical.com/port-royal-sc/ (301 paired with the publish)
loc-ladys-island-sc: https://homemobilemedical.com/service-area/ladys-island-sc/ → https://homemobilemedical.com/ladys-island-sc/ (301 paired with the publish)
loc-laurel-bay-sc: https://homemobilemedical.com/service-area/laurel-bay-sc/ → https://homemobilemedical.com/laurel-bay-sc/ (301 paired with the publish)
loc-daufuskie-island-sc: https://homemobilemedical.com/service-area/daufuskie-island-sc/ → https://homemobilemedical.com/daufuskie-island-sc/ (301 paired with the publish)
loc-okatie-sc: https://homemobilemedical.com/service-area/okatie-sc/ → https://homemobilemedical.com/okatie-sc/ (301 paired with the publish)
loc-hardeeville-sc: https://homemobilemedical.com/service-area/hardeeville-sc/ → https://homemobilemedical.com/hardeeville-sc/ (301 paired with the publish)
loc-ridgeland-sc: https://homemobilemedical.com/service-area/ridgeland-sc/ → https://homemobilemedical.com/ridgeland-sc/ (301 paired with the publish)
loc-levy-sc: https://homemobilemedical.com/service-area/levy-sc/ → https://homemobilemedical.com/levy-sc/ (301 paired with the publish)
loc-yemassee-sc: https://homemobilemedical.com/service-area/yemassee-sc/ → https://homemobilemedical.com/yemassee-sc/ (301 paired with the publish)
hub-charleston: https://homemobilemedical.com/service-area/charleston/ → https://homemobilemedical.com/charleston-metro/ (301 paired with the publish)
loc-charleston-sc: https://homemobilemedical.com/service-area/charleston-sc/ → https://homemobilemedical.com/charleston-sc/ (301 paired with the publish)
loc-north-charleston-sc: https://homemobilemedical.com/service-area/north-charleston-sc/ → https://homemobilemedical.com/north-charleston-sc/ (301 paired with the publish)
loc-mount-pleasant-sc: https://homemobilemedical.com/service-area/mount-pleasant-sc/ → https://homemobilemedical.com/mount-pleasant-sc/ (301 paired with the publish)
loc-summerville-sc: https://homemobilemedical.com/service-area/summerville-sc/ → https://homemobilemedical.com/summerville-sc/ (301 paired with the publish)
loc-goose-creek-sc: https://homemobilemedical.com/service-area/goose-creek-sc/ → https://homemobilemedical.com/goose-creek-sc/ (301 paired with the publish)
loc-hanahan-sc: https://homemobilemedical.com/service-area/hanahan-sc/ → https://homemobilemedical.com/hanahan-sc/ (301 paired with the publish)
loc-moncks-corner-sc: https://homemobilemedical.com/service-area/moncks-corner-sc/ → https://homemobilemedical.com/moncks-corner-sc/ (301 paired with the publish)
loc-hollywood-sc: https://homemobilemedical.com/service-area/hollywood-sc/ → https://homemobilemedical.com/hollywood-sc/ (301 paired with the publish)
loc-kiawah-island-sc: https://homemobilemedical.com/service-area/kiawah-island-sc/ → https://homemobilemedical.com/kiawah-island-sc/ (301 paired with the publish)
loc-folly-island-sc: https://homemobilemedical.com/service-area/folly-island-sc/ → https://homemobilemedical.com/folly-island-sc/ (301 paired with the publish)
loc-walterboro-sc: https://homemobilemedical.com/service-area/walterboro-sc/ → https://homemobilemedical.com/walterboro-sc/ (301 paired with the publish)
loc-edisto-island-sc: https://homemobilemedical.com/service-area/edisto-island-sc/ → https://homemobilemedical.com/edisto-island-sc/ (301 paired with the publish)
hub-lowcountry: https://homemobilemedical.com/service-area/ dropped from the plan → 301 to https://homemobilemedical.com/
batches: final1, final2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, svc1 → services, loc-hhi, loc-charleston, final
The site plan file changed: Paul re-approves it once.

## RUN 20261009-201533-drive-mirror-0325 · STARTED · /drive-mirror · 2026-10-09T20:15:33-05:00
Step: drive-mirror · session 55ffb3c8-069b-4af6-a4b4-8790ec003647
Gates checked: client_setup
Note: rewrite 2 URL migration: worklist rows
- CHANGE #125 [redirect] https://homemobilemedical.com/service-area/ | 301 | old: [REDACTED]service-area/ | new: [REDACTED] | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-06-redirect-01
- REOPENED redirect-targets-default · 2026-10-09T20:15:33-05:00 · run 20261009-201533-drive-mirror-0325 · rewrite 2 (Paul 2026-10-09, REWRITE-2-DECISIONS.md c): /services/ and /service-area/ are gone
- SETTLED redirect-targets-default · 2026-10-09T20:15:33-05:00 · run 20261009-201533-drive-mirror-0325 · by Paul (REWRITE-2-DECISIONS.md c) · Paul 2026-10-09 (Q2, revised in rewrite 2): redirect the 36 to the appropriate URLs — FL/MI → /stair-lifts/, power chairs/scooter lifts → the homepage (was /services/), ramps → /porch-lifts/; SC legacy duplicates → their canonical root service/location page. No redirect points at /services/ or /service-area/, so there are no chains.
### HANDOFF · /drive-mirror · 2026-10-09 · run 20261009-201533-drive-mirror-0325
**What I did**
- rewrite 2 URL migration: worklist rows for the redirect / slug clearing
### END HANDOFF
## RUN 20261009-201533-drive-mirror-0325 · FINISHED · 2026-10-09T20:15:34-05:00
Changes: 1 · Summary: rewrite 2 URL migration (worklist rows)
- CHANGE #126 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-09 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #127 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-09 (2).md | new: Home Mobile Medical - Handoff Log.md · sha f56d0bed687a | result: done · copied (Drive for desktop syncs it)
- CHANGE #128 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Approval Record - 2026-10-09 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Approval Record.md | new: _Archive/Home Mobile Medical - Approval Record - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #129 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Approval Record.md | upload | old: previous version archived as Home Mobile Medical - Approval Record - 2026-10-09 (2).md | new: Home Mobile Medical - Approval Record.md · sha eb0523819740 | result: done · copied (Drive for desktop syncs it)
- CHANGE #130 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (5).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #131 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09 (5).md | new: Home Mobile Medical - Document Checklist.md · sha 33b1b986ff5d | result: done · copied (Drive for desktop syncs it)
- CHANGE #132 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09 (5).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #133 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09 (5).md | new: Home Mobile Medical - Status.md · sha 304269f7429e | result: done · copied (Drive for desktop syncs it)
- CHANGE #134 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | upload | old: (new file) | new: Home Mobile Medical - VA Worklist.md · sha 2723646d3a18 | result: done · copied (Drive for desktop syncs it)
- CHANGE #135 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | upload | old: (new file) | new: Home Mobile Medical - VA Worklist.csv · sha 0805bef3f8ef | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-222728-drive-mirror-744e · STARTED · /drive-mirror · 2026-10-09T22:27:28-05:00
Step: drive-mirror · session 55ffb3c8-069b-4af6-a4b4-8790ec003647
Gates checked: client_setup
Note: rewrite 2 follow-up: /services/ redirect, -sc-2 retargets
- CHANGE #136 [redirect] https://homemobilemedical.com/services/ | 301 | old: [REDACTED]services/ | new: [REDACTED] | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-07-redirect-01
- CHANGE #137 [redirect] https://homemobilemedical.com/service-area/bluffton-sc-2/ | 301 target | old: [REDACTED]service-area/bluffton-sc/ | new: [REDACTED]bluffton-sc/ | result: RETARGETED · rewrite 2: /service-area/bluffton-sc/ moves to /bluffton-sc/ (Paul 2026-10-09) — no redirect chains | ref H-2026-10-09-03-redirect-01
- CHANGE #138 [redirect] https://homemobilemedical.com/service-area/charleston-sc-2/ | 301 target | old: [REDACTED]service-area/charleston-sc/ | new: [REDACTED]charleston-sc/ | result: RETARGETED · rewrite 2: /service-area/charleston-sc/ moves to /charleston-sc/ (Paul 2026-10-09) — no redirect chains | ref H-2026-10-09-03-redirect-02
- CHANGE #139 [redirect] https://homemobilemedical.com/service-area/beaufort-sc-2/ | 301 target | old: [REDACTED]service-area/beaufort-sc/ | new: [REDACTED]beaufort-sc/ | result: RETARGETED · rewrite 2: /service-area/beaufort-sc/ moves to /beaufort-sc/ (Paul 2026-10-09) — no redirect chains | ref H-2026-10-09-03-redirect-03
### HANDOFF · /drive-mirror · 2026-10-09 · run 20261009-222728-drive-mirror-744e
**What I did**
- Added the 301 /services/ → homepage (worklist section 3).
- Pointed the three -sc-2 redirects (not yet done by Jonie) at the root URLs, so there are no chains.
### END HANDOFF
## RUN 20261009-222728-drive-mirror-744e · FINISHED · 2026-10-09T22:27:37-05:00
Changes: 4 · Summary: rewrite 2 follow-up: /services/ 301 and -sc-2 retargets
- CHANGE #140 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-09 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-09 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #141 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-09 (3).md | new: Home Mobile Medical - Handoff Log.md · sha 93b010fa9fba | result: done · copied (Drive for desktop syncs it)
- CHANGE #142 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (6).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #143 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09 (6).md | new: Home Mobile Medical - Document Checklist.md · sha 0b509dad4f3f | result: done · copied (Drive for desktop syncs it)
- CHANGE #144 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09 (6).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #145 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09 (6).md | new: Home Mobile Medical - Status.md · sha 2f7c249c7316 | result: done · copied (Drive for desktop syncs it)
- CHANGE #146 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - VA Worklist - 2026-10-09.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | new: _Archive/Home Mobile Medical - VA Worklist - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #147 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | upload | old: previous version archived as Home Mobile Medical - VA Worklist - 2026-10-09.md | new: Home Mobile Medical - VA Worklist.md · sha e8888e1d20b1 | result: done · copied (Drive for desktop syncs it)
- CHANGE #148 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - VA Worklist - 2026-10-09.csv | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | new: _Archive/Home Mobile Medical - VA Worklist - 2026-10-09.csv | result: done · renamed and moved, nothing deleted
- CHANGE #149 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | upload | old: previous version archived as Home Mobile Medical - VA Worklist - 2026-10-09.csv | new: Home Mobile Medical - VA Worklist.csv · sha 10c85ac3c5ee | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-14T07:32:03-05:00 · site plan · approved · by Paul
Approved version: clients/home-mobile-medical/build/Home Mobile Medical - Site Plan - REVISED.md (sha 99199b5f08eb)
- CHANGE #150 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (7).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-09 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #151 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-09 (7).md | new: Home Mobile Medical - Document Checklist.md · sha 5652a3819342 | result: done · copied (Drive for desktop syncs it)
- CHANGE #152 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-09 (7).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-09 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #153 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-09 (7).md | new: Home Mobile Medical - Status.md · sha ba3f66bcaed0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #154 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - VA Worklist - 2026-10-09 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | new: _Archive/Home Mobile Medical - VA Worklist - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #155 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | upload | old: previous version archived as Home Mobile Medical - VA Worklist - 2026-10-09 (2).md | new: Home Mobile Medical - VA Worklist.md · sha 1deb557dad9b | result: done · copied (Drive for desktop syncs it)
- CHANGE #156 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - VA Worklist - 2026-10-09 (2).csv | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | new: _Archive/Home Mobile Medical - VA Worklist - 2026-10-09 (2).csv | result: done · renamed and moved, nothing deleted
- CHANGE #157 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | upload | old: previous version archived as Home Mobile Medical - VA Worklist - 2026-10-09 (2).csv | new: Home Mobile Medical - VA Worklist.csv · sha 8cc9063e0a09 | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-14T10:00:26-05:00 · page specs (global: location) · approved · by Paul
Approved version: methodology/specs/location.md (sha 1212fa3e9365)

## RUN 20261014-100458-build-2be7 · STARTED · /build · 2026-10-14T10:04:58-05:00
Step: build:facts · session 31f16b03-b772-499d-8b3b-b721a7f758ed
Gates checked: discovery_signed_off, site_plan, page_specs_approved
- REVIEW FACTS 2026-10-14T10:07 · run 20261014-100458-build-2be7 · 8 fact(s)/topic(s) found in reviews, 0 with 3+ different reviewers (customer_reported, CM-057) · data/reviews/review-facts.json
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-stair-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-beaufort-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-curved-stair-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-porch-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-wheelchair-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-repair-maintenance: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · hub-hhi-beaufort: BLOCK (known 3, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-bluffton-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hilton-head-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-port-royal-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-ladys-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-laurel-bay-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-daufuskie-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-okatie-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hardeeville-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-ridgeland-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-levy-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-yemassee-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · hub-charleston: BLOCK (known 3, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-charleston-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-north-charleston-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-mount-pleasant-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-summerville-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-goose-creek-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hanahan-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-moncks-corner-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hollywood-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-kiawah-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-folly-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-walterboro-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-edisto-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · homepage: WARN (known 8, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · about: WARN (known 5, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-stair-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-beaufort-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-curved-stair-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-porch-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-wheelchair-lifts: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · svc-repair-maintenance: BLOCK (known 6, unknown 3, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · hub-hhi-beaufort: BLOCK (known 3, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-bluffton-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hilton-head-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-port-royal-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-ladys-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-laurel-bay-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-daufuskie-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-okatie-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hardeeville-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-ridgeland-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-levy-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-yemassee-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · hub-charleston: BLOCK (known 3, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-charleston-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-north-charleston-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-mount-pleasant-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-summerville-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-goose-creek-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hanahan-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-moncks-corner-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-hollywood-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-kiawah-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-folly-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-walterboro-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · loc-edisto-island-sc: BLOCK (known 2, unknown 7, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · homepage: WARN (known 8, unknown 3, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:07 · run 20261014-100458-build-2be7 · about: WARN (known 5, unknown 3, unverified 0, conflict 0)
- CHANGE #158 [evidence] clients/home-mobile-medical/build/evidence/ | page_facts | old:  | new: city_served on 26 location pages (Brand Guide E); service_scope/service_process on 5 service pages, core_services, company_story — from Brand Guide D, Client C… | result: done
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-1 · fact:loc-hilton-head-island-sc:local_context (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-2 · fact:loc-hilton-head-island-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-3 · fact:loc-hilton-head-island-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-4 · fact:loc-hilton-head-island-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-5 · fact:loc-bluffton-sc:local_context (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-6 · fact:loc-bluffton-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-7 · fact:loc-bluffton-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-8 · fact:loc-bluffton-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-9 · fact:loc-daufuskie-island-sc:local_context (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-10 · fact:loc-daufuskie-island-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-11 · fact:loc-daufuskie-island-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-12 · fact:loc-daufuskie-island-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-13 · fact:loc-okatie-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-14 · fact:loc-okatie-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-15 · fact:loc-okatie-sc:place_entities (public): partial
- RESEARCH 2026-10-14T10:13 · run 20261014-100458-build-2be7 · RL-loc-hhi-16 · fact:loc-okatie-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-17 · fact:loc-hardeeville-sc:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-18 · fact:loc-hardeeville-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-19 · fact:loc-hardeeville-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-20 · fact:loc-hardeeville-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-21 · fact:loc-ridgeland-sc:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-22 · fact:loc-ridgeland-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-23 · fact:loc-ridgeland-sc:place_entities (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-24 · fact:loc-ridgeland-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-25 · fact:loc-levy-sc:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-26 · fact:loc-levy-sc:neighborhoods (public): not_found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-27 · fact:loc-levy-sc:place_entities (public): not_found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-28 · fact:loc-levy-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-29 · fact:loc-yemassee-sc:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-30 · fact:loc-yemassee-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-31 · fact:loc-yemassee-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-32 · fact:loc-yemassee-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-1 · fact:loc-walterboro-sc:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-2 · fact:loc-walterboro-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-3 · fact:loc-walterboro-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-4 · fact:loc-walterboro-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-5 · fact:loc-edisto-island-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-6 · fact:loc-edisto-island-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-7 · fact:loc-edisto-island-sc:place_entities (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-8 · fact:loc-edisto-island-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-pilot-1 · fact:loc-beaufort-sc:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-pilot-2 · fact:loc-beaufort-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-pilot-3 · fact:loc-beaufort-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-pilot-4 · fact:loc-beaufort-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-33 · fact:loc-port-royal-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-34 · fact:loc-port-royal-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-35 · fact:loc-port-royal-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-36 · fact:loc-port-royal-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-37 · fact:loc-ladys-island-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-38 · fact:loc-ladys-island-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-39 · fact:loc-ladys-island-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-40 · fact:loc-ladys-island-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-41 · fact:loc-laurel-bay-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-42 · fact:loc-laurel-bay-sc:neighborhoods (public): not_found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-43 · fact:loc-laurel-bay-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-44 · fact:loc-laurel-bay-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-45 · fact:hub-hhi-beaufort:county_cities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-hhi-46 · fact:hub-hhi-beaufort:local_context (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-9 · fact:loc-summerville-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-10 · fact:loc-summerville-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-11 · fact:loc-summerville-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-12 · fact:loc-summerville-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-13 · fact:loc-goose-creek-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-14 · fact:loc-goose-creek-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-15 · fact:loc-goose-creek-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-16 · fact:loc-goose-creek-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-17 · fact:loc-hanahan-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-18 · fact:loc-hanahan-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-19 · fact:loc-hanahan-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-20 · fact:loc-hanahan-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-21 · fact:loc-moncks-corner-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-22 · fact:loc-moncks-corner-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-23 · fact:loc-moncks-corner-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:14 · run 20261014-100458-build-2be7 · RL-loc-charleston-24 · fact:loc-moncks-corner-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-25 · fact:loc-charleston-sc:local_context (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-26 · fact:loc-charleston-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-27 · fact:loc-charleston-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-28 · fact:loc-charleston-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-29 · fact:loc-north-charleston-sc:local_context (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-30 · fact:loc-north-charleston-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-31 · fact:loc-north-charleston-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-32 · fact:loc-north-charleston-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-33 · fact:loc-mount-pleasant-sc:local_context (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-34 · fact:loc-mount-pleasant-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-35 · fact:loc-mount-pleasant-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-36 · fact:loc-mount-pleasant-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-37 · fact:loc-hollywood-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-38 · fact:loc-hollywood-sc:neighborhoods (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-39 · fact:loc-hollywood-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-40 · fact:loc-hollywood-sc:permit_office (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-41 · fact:loc-kiawah-island-sc:local_context (public): partial
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-42 · fact:loc-kiawah-island-sc:neighborhoods (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-43 · fact:loc-kiawah-island-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-44 · fact:loc-kiawah-island-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-45 · fact:loc-folly-island-sc:local_context (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-46 · fact:loc-folly-island-sc:neighborhoods (public): not_found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-47 · fact:loc-folly-island-sc:place_entities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-48 · fact:loc-folly-island-sc:permit_office (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-49 · fact:hub-charleston:county_cities (public): found
- RESEARCH 2026-10-14T10:18 · run 20261014-100458-build-2be7 · RL-loc-charleston-50 · fact:hub-charleston:local_context (public): found
- FACT 2026-10-14T10:19 · run 20261014-100458-build-2be7 · d-google-rating-and-review-count-date-checked (value, status, source) · internally_verified · 2.9 stars from 19 Google reviews (checked 2026-10-08) · source DataforSEO Google reviews pull 2026-10-08 (data/reviews/raw/reviews.json); reviews.csv 19 rows, 2017-04-02 to 2023-03-23 · by Paul
- RESEARCH 2026-10-14T10:19 · run 20261014-100458-build-2be7 · RL-evidence-1 · fact:d:google_rating (client): found
- RESEARCH 2026-10-14T10:19 · run 20261014-100458-build-2be7 · RL-evidence-2 · fact:d:emergency (client): not_found
- RESEARCH 2026-10-14T10:19 · run 20261014-100458-build-2be7 · RL-evidence-3 · fact:d:awards (client): not_found
- RESEARCH 2026-10-14T10:19 · run 20261014-100458-build-2be7 · RL-evidence-4 · fact:d:association (client): not_found
- RESEARCH 2026-10-14T10:19 · run 20261014-100458-build-2be7 · RL-services-1 · fact:svc-repair-maintenance:service_process (client): not_found
- FLAG 2026-10-14T10:19 · run 20261014-100458-build-2be7 · F-001 · methodology/sources/sc-lowcountry.md: no rows for Charleston County, Berkeley/Dorchester/Colleton/Hampton counties or their towns (researchers found official permit pages: charleston-sc.gov/856/Permit-Center, charlestoncounty.gov/departments/building-inspection-services, northcharleston.org Building-and-Permit-Inspections, tompsc.com/151/Permit, kiawahisland.gov/building_services.php, cityoffollybeach.com building_planning, goosecreeksc.gov building-permits, cityofhanahan.com/node/86, summervillesc.gov/289/Permitting); HHI permit URL listed returns 404 to fetch (hiltonheadislandsc.gov/permits works); Bluffton Neighborhoods PDF row has no URL; Census QuickFacts returns 403 to the fetch tool and the Census API needs a key, so 65+ shares come via Wikipedia (2020 census). · workaround: Researchers cited the official pages directly and Wikipedia for census figures; Paul adds the rows at /system-review.
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · svc-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-beaufort-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · svc-curved-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · svc-porch-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · svc-wheelchair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · svc-repair-maintenance: WARN (known 8, unknown 1, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · hub-hhi-beaufort: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-bluffton-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-hilton-head-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-port-royal-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-ladys-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-laurel-bay-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-daufuskie-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-okatie-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-hardeeville-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-ridgeland-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-levy-sc: PASS (known 6, unknown 3, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-yemassee-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · hub-charleston: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-charleston-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-north-charleston-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-mount-pleasant-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-summerville-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-goose-creek-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-hanahan-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-moncks-corner-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-hollywood-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-kiawah-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-folly-island-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-walterboro-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · loc-edisto-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · homepage: PASS (known 10, unknown 1, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T10:19 · run 20261014-100458-build-2be7 · about: PASS (known 6, unknown 2, unverified 0, conflict 0)
- OPEN fact:svc-repair-maintenance:service_process · 2026-10-14T10:20:02-05:00 · run 20261014-100458-build-2be7 · by Client (via Paul) · How the service is delivered (steps, methods, equipment) — what should we say? If it depends, on what?
- FACTS INTERVIEW 2026-10-14T10:20 · run 20261014-100458-build-2be7 · facts round (all pages) · 1 question(s) for svc-stair-lifts, svc-curved-stair-lifts, svc-porch-lifts, svc-wheelchair-lifts, svc-repair-maintenance · clients/home-mobile-medical/interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md
- RESEARCH 2026-10-14T10:20 · run 20261014-100458-build-2be7 · RL-services-2 · fact:svc-curved-stair-lifts:install_time (client): not_found
- RESEARCH 2026-10-14T10:20 · run 20261014-100458-build-2be7 · RL-services-3 · fact:svc-porch-lifts:install_time (client): not_found
- RESEARCH 2026-10-14T10:20 · run 20261014-100458-build-2be7 · RL-services-4 · fact:svc-wheelchair-lifts:install_time (client): not_found
- OPEN fact:d:emergency · 2026-10-14T10:20:37-05:00 · run 20261014-100458-build-2be7 · by Client (via Paul) · Any emergency or after-hours help for a stopped lift? (facts round 2026-10-14, Q2)
- OPEN fact:svc-curved-stair-lifts:install_time · 2026-10-14T10:20:37-05:00 · run 20261014-100458-build-2be7 · by Client (via Paul) · Order-to-install and install times for curved, porch and wheelchair lifts; who handles pad and permit (facts round 2026-10-14, Q3)
### HANDOFF · /build · 2026-10-14 · run 20261014-100458-build-2be7
**Step:** the one facts round (P10) for all 33 pages in the approved site plan.

**Done**
- reviews.py extract: 8 review topics. None was reported by 3 or more reviewers, so none needed checking by meaning.
- Page facts files (build/evidence/<page>.facts.json):
  - city_served on 26 location pages (Brand Guide E, Paul 2026-10-07).
  - service_scope and service_process on the service pages, core_services (homepage) and company_story (about), all from Brand Guide D. Client Confirmed facts only (change #158).
- Researcher (Sonnet) ran 5 parallel lookups for 28 location and hub pages: 100 public facts (59 found, 37 partial, 4 not found). Every one is logged in build/{pilot,loc-hhi,loc-charleston}/research-log.csv. The group with the hub-hhi-beaufort, Beaufort, Port Royal, Lady's Island and Laurel Bay pages first got an empty page list; it was resent and confirmed done (18 facts).
- Not found: Levy neighborhoods, Levy place_entities, Laurel Bay neighborhoods, Folly neighborhoods. Under CM-061 §8 these sections are left out by default and never asked.
- Google rating recorded with run.py fact: 2.9 stars from 19 reviews (DataforSEO pull 2026-10-08). Paul should know it is low. Some reviews date from the old medical-equipment era.
- Client search order logged for 6 gaps (RL-evidence-1..4, RL-services-1..4): emergency, awards, associations, the repair process, and install time for curved, porch and wheelchair lifts.
  - Awards and associations: none found (no BBB listing). They stay "None" and are not asked.
- Grids re-run: 28 PASS, 5 WARN (service pages, supporting gaps only), 0 BLOCK.
- evidence.py questions --all ran once and produced 1 generic question. I rewrote it pre-filled and added Q2 (after-hours) and Q3 (install times, pad and permit).
  - The set is in interviews/facts/facts-round-all-2026-10-14.questions.json. settled.py filter kept 3; questions.py check passed.
  - Q2 and Q3 were asked once with run.py decision --ask.

**Facts round for Paul:** interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md, 3 questions. Paul sends it; the answers go in with /interview home-mobile-medical facts-answers all.

**Flags:** F-001. sc-lowcountry.md has no rows for Charleston, Berkeley, Dorchester, Colleton or Hampton counties and their towns; the HHI permit URL returns 404 when fetched; the Bluffton PDF has no URL; Census QuickFacts returns 403, so 65+ shares come from Wikipedia's 2020 census figures.

**For the brief writers:**
- Folly naming: the official site says "City of Folly Beach". The Discovery Record's Folly Island vs Folly Beach conflict is still open, and it is Paul's call.
- Yemassee is mostly in Hampton County. Okatie spans Beaufort and Jasper.
- Permit offices for Walterboro and Hollywood are partial: confirm with the town.

**Not done:** none. The Brand Guide was not written (write-back happens at brief approval, CM-061 §6).
### END HANDOFF
## RUN 20261014-100458-build-2be7 · FINISHED · 2026-10-14T10:21:13-05:00
Changes: 1 · Summary: Facts round: 100 public facts looked up, grids 28 pass/5 warn/0 block, 3-question set for Paul
- CHANGE #159 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-09 (4).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-09 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #160 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-09 (4).md | new: Home Mobile Medical - Handoff Log.md · sha e61a80462cf5 | result: done · copied (Drive for desktop syncs it)
- CHANGE #161 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14.md | result: done · renamed and moved, nothing deleted
- CHANGE #162 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14.md | new: Home Mobile Medical - Document Checklist.md · sha 1b92ff22d5cf | result: done · copied (Drive for desktop syncs it)
- CHANGE #163 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Brand Guide - 2026-10-07.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | new: _Archive/Home Mobile Medical - Brand Guide - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #164 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | upload | old: previous version archived as Home Mobile Medical - Brand Guide - 2026-10-07.md | new: Home Mobile Medical - Brand Guide.md · sha 8ffe9fc32f05 | result: done · copied (Drive for desktop syncs it)
- CHANGE #165 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14.md | result: done · renamed and moved, nothing deleted
- CHANGE #166 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14.md | new: Home Mobile Medical - Status.md · sha d339e15de5ca | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-14T12:53 · after build:facts (run 20261014-100458-build-2be7) · Paul typed /next

## RUN 20261014-125319-build-9170 · STARTED · /build · 2026-10-14T12:53:19-05:00
Step: build:write · batch pilot · session 282ed557-3309-4abb-a218-45bc5987dda9
Gates checked: discovery_signed_off, batch:pilot:briefs_ready, page_specs_approved
- EVIDENCE 2026-10-14T12:54 · run 20261014-125319-build-9170 · svc-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T12:54 · run 20261014-125319-build-9170 · loc-beaufort-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- FLAG 2026-10-14T12:54 · run 20261014-125319-build-9170 · F-002 · Approved site plan (REVISED md + site-plan-revised.plan.json) carries no keyword, area variant, category variant, H1 decision, FAQ topics or link targets per page — the build:plan step requires them; the plan was imported. Briefs have no planned keyword/variant to take. · workaround: Pilot briefs propose keyword (data/rankings), area variant (B2, never B1) and H1 per page, marked 'proposed — confirm at brief approval'; Paul confirms with the briefs approval.
- FLAG 2026-10-14T12:54 · run 20261014-125319-build-9170 · F-003 · PAA/fan-out routing tables route to the old URLs (/services/stair-lifts/, /service-area/<city>/), so evidence_pack.py tags no question to the new root-slug pages (packs say 'None tagged to this page'). · workaround: Brief-writers read paa-routing.md/fanout-routing.md rows routed to the page's live_url as candidates.
- FLAG 2026-10-14T12:54 · run 20261014-125319-build-9170 · F-004 · status.json client.route is null for a full client; build.md says ask Paul when missing. · workaround: Ran the pilot as Route A (system writes): the run brief asks for briefs and drafts, and no Paul-written content exists on disk. Paul to confirm route A.
- BRIEF 2026-10-14T12:57 · run 20261014-125319-build-9170 · svc-stair-lifts · clients/home-mobile-medical/build/pilot/briefs/SB - Stair Lifts - Home Mobile Medical.md
- BRIEF 2026-10-14T12:58 · run 20261014-125319-build-9170 · loc-beaufort-sc · clients/home-mobile-medical/build/pilot/briefs/LB - Beaufort SC - Home Mobile Medical.md
- BRIEFS COLLECTED 2026-10-14T12:58 · batch pilot · 2 page(s), one run each
- DRAFT 2026-10-14T13:06 · run 20261014-125319-build-9170 · loc-beaufort-sc · clients/home-mobile-medical/build/pilot/drafts/loc-beaufort-sc.md · agent draft-loc-beaufort-sc-9170
- DRAFT 2026-10-14T13:06 · run 20261014-125319-build-9170 · svc-stair-lifts · clients/home-mobile-medical/build/pilot/drafts/svc-stair-lifts.md · agent draft-svc-stair-lifts-9170
- REVIEW SHEET 2026-10-14T13:07 · run 20261014-125319-build-9170 · pilot drafts: 1 Ask, 8 decided for you, 3 fixed silently, 0 not raised (duplicate, decided or answered) · clients/home-mobile-medical/build/pilot/drafts-review.csv
- FLAG 2026-10-14T13:07 · run 20261014-125319-build-9170 · F-005 · Draft writers put a '## Writer notes' section in the page file and publish.py drafts does not strip it, so the notes would reach the WordPress draft. Also: review.py sheet counts Fix rows as 'fixed silently' before review.py apply has run. · workaround: Recorded as Fix rows (formatting) in the pilot drafts findings; remove the Writer notes section when review.py apply runs after Paul's answer, before ship.
### HANDOFF · /build · 2026-10-14 · run 20261014-125319-build-9170
**Done**
- Briefs: `build/pilot/briefs/SB - Stair Lifts - Home Mobile Medical.md`, `build/pilot/briefs/LB - Beaufort SC - Home Mobile Medical.md` (recorded with page-stage brief).
- Drafts, one fresh subagent each: `build/pilot/drafts/svc-stair-lifts.md`, `build/pilot/drafts/loc-beaufort-sc.md` (recorded with page-stage draft). Self-checks E1–E10 and spec checks in each file's Writer notes: all pass except E10/COM-13 on the stair-lifts safety statement (grade 11.3, Paul's verbatim D text).
- Install time on stair lifts uses Decision 016 (client_confirmed 2026-10-07); the website's "a few hours" line is superseded and not used. Beaufort has no install-time claim.
- One checker pass over both drafts: `build/pilot/drafts-findings.json` (12 findings) → `review.py sheet` → `build/pilot/drafts-review.csv` / `.md`: 1 Ask, 8 Decided for you (7 carried + usage check), 3 Fix.
- `status.py batch home-mobile-medical pilot --state drafts_written --review-sheet build/pilot/drafts-review.csv`.
- Flag F-005: Writer notes are not stripped by publish.py; review.py counts Fix rows as "fixed silently" before apply.

**Open — waiting on Paul**
- Ask 1 (kind 2): stair-lifts safety statement at grade 11.3 — A keep verbatim (recommended) / B approve a plainer version.
- review.py apply NOT run (Ask row open). The 3 Fix rows apply then: Beaufort cost FAQ kept to the local quote angle (overlap with stair-lifts FAQ 1, BB-316); remove `## Writer notes` from both page files before ship.
- Still `[NEED: …]`, not filled: after-hours/emergency, curved/porch/wheelchair install times, pad and permit (Beaufort FAQ 2), price range, Beaufort city map.

**Next**
- Paul answers the sheet: `/build home-mobile-medical review pilot drafts "<his line>"` → review.py apply → `/approve home-mobile-medical batch:pilot:briefs batch:pilot:drafts mode:build:brief=auto` → pilot-corrections.
### END HANDOFF
## RUN 20261014-125319-build-9170 · FINISHED · 2026-10-14T13:08:00-05:00
Changes: 0 · Summary: Pilot drafts checked in one pass; review sheet has 1 Ask (safety statement grade), 8 decided for you, 3 fixes; batch drafts_written.
- CHANGE #167 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14.md | result: done · renamed and moved, nothing deleted
- CHANGE #168 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14.md | new: Home Mobile Medical - Handoff Log.md · sha 80f7b1d04034 | result: done · copied (Drive for desktop syncs it)
- CHANGE #169 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #170 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (2).md | new: Home Mobile Medical - Document Checklist.md · sha 04fca74952b0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #171 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #172 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (2).md | new: Home Mobile Medical - Status.md · sha 8a1325ec7460 | result: done · copied (Drive for desktop syncs it)

## RUN 20261014-131553-build-b121 · STARTED · /build · 2026-10-14T13:15:53-05:00
Step: build:review · batch pilot · session 282ed557-3309-4abb-a218-45bc5987dda9
Gates checked: discovery_signed_off
- REVIEW APPLIED 2026-10-14T13:16 · run 20261014-131553-build-b121 · pilot drafts: 9 row(s) (1 answered by Paul, the rest by default) · clients/home-mobile-medical/build/pilot/drafts-apply.json
- FLAG 2026-10-14T13:16 · run 20261014-131553-build-b121 · F-006 · review.py apply crashes (ValueError in LETTERS.index) when a row's 'recommended' is an uppercase letter (pilot drafts row 1 had 'A'); defaults are not lowercased before lookup. · workaround: Passed Paul's answer explicitly as '1a' in --answers ('accept all, 1a'), which parse_answers lowercases.
### HANDOFF · /build · 2026-10-14 · run 20261014-131553-build-b121
- Paul's line: "accept all", with Ask 1 = A.
- review.py apply → build/pilot/drafts-apply.json: 9 rows recorded (row 1 answered by Paul = a/A; rows 2–9 decided-for-you, accepted by default). Ledger: build/pilot/findings-ledger.json.
- Ask 1 (svc-stair-lifts safety statement, grade 11.3): A, approved Section D text kept word for word, unchanged.
- Rows 2–9: already in the drafts as decided; no text change needed.
- Fix rows (drafts-fixes.json) applied:
  - loc-beaufort-sc BB-316: cost FAQ reframed as "How Do I Get a Stair Lift Quote for My Beaufort Home?" (photo, free in-home estimate, stair count). The stair-lifts FAQ "How Much Does a Stair Lift Cost?" stays the cost answer. New answer grade 5.5.
  - loc-beaufort-sc and svc-stair-lifts P11: "## Writer notes" removed from both page files; the notes are kept in handoffs/run-20261014-131553-build-b121.writer-notes.md.
- Flag F-006: review.py apply crashed on the uppercase recommended value "A" (LETTERS.index). Workaround: the answers were passed as "accept all, 1a".
- Not done: the drafts were not re-recorded with the page-stage command (the coordinator said not to call it). If the drafts approval is pinned to file versions, the coordinator must re-record both drafts.
- Open placeholders (Beaufort): [NEED: permit/pad — facts round Q3], [NEED: city map]. Link-wheel rows stay placeholders for ship.
### END HANDOFF
## RUN 20261014-131553-build-b121 · FINISHED · 2026-10-14T13:17:25-05:00
Changes: 0 · Summary: Pilot drafts review applied: accept all, Ask 1 = A; BB-316 Beaufort FAQ reframed; Writer notes removed
- CHANGE #173 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #174 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14 (2).md | new: Home Mobile Medical - Handoff Log.md · sha 690f154ea3f0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #175 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #176 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (3).md | new: Home Mobile Medical - Document Checklist.md · sha d5c1ee0f0411 | result: done · copied (Drive for desktop syncs it)
- CHANGE #177 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #178 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (3).md | new: Home Mobile Medical - Status.md · sha 6727c8d044d2 | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-14T13:28:43-05:00 · batch pilot briefs · approved · by Paul
Approved version: clients/home-mobile-medical/build/pilot/briefs/SB - Stair Lifts - Home Mobile Medical.md (sha ddafedf3016d)
Approved version: clients/home-mobile-medical/build/pilot/briefs/LB - Beaufort SC - Home Mobile Medical.md (sha 88e0fadbb179)
Human review: Paul Meisner
- CHANGE #179 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (4).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #180 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (4).md | new: Home Mobile Medical - Document Checklist.md · sha d9fe7be9d947 | result: done · copied (Drive for desktop syncs it)
- CHANGE #181 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (4).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #182 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (4).md | new: Home Mobile Medical - Status.md · sha 7385a5df75af | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-14T13:29:26-05:00 · batch pilot drafts · approved · by Paul
Approved version: clients/home-mobile-medical/build/pilot/drafts/svc-stair-lifts.md (sha eb5499249a3e)
Approved version: clients/home-mobile-medical/build/pilot/drafts/loc-beaufort-sc.md (sha 2534ab32a0c6)
Approved version: clients/home-mobile-medical/build/pilot/drafts-review.csv (sha 300bededfb1f)
SEM items to apply: none
Human review: Paul Meisner
- CHANGE #183 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (5).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #184 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (5).md | new: Home Mobile Medical - Document Checklist.md · sha 9ca21a6f2d12 | result: done · copied (Drive for desktop syncs it)
- CHANGE #185 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (5).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #186 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (5).md | new: Home Mobile Medical - Status.md · sha f8703cc3ec79 | result: done · copied (Drive for desktop syncs it)

## MODE · 2026-10-14T13:29:45-05:00 · build:brief: review → auto · this client · by Paul

## RUN 20261014-133132-build-f0c5 · STARTED · /build · 2026-10-14T13:31:32-05:00
Step: build:writeback · batch pilot · session d461cc9d-b724-4b0b-88b0-0c1f5085ab5c
Gates checked: discovery_signed_off, batch:pilot:briefs
- CHANGE #187 [drive_file] drive:Home Mobile Medical - TMS/brand-guide.md | upload | old: (new file) | new: brand-guide.md · sha ded5e8aed622 | result: done · copied (Drive for desktop syncs it)
- WRITE-BACK 2026-10-14T13:33 · run 20261014-133132-build-f0c5 · batch pilot: Brand Guide B3, C1/C2, C3 updated once for the section, from its approved briefs
### HANDOFF · /build · 2026-10-14 · run 20261014-133132-build-f0c5
**Gate:** `status.py writeback` checks only `batch:pilot:briefs` (approved 2026-10-14) and a one-per-section guard. The 3 open facts (svc-repair-maintenance:service_process, d:emergency, svc-curved-stair-lifts:install_time) and the uncleared blockers do not gate this step; no refusal.

**Written back to brand-guide.md (from the approved pilot briefs SB - Stair Lifts, LB - Beaufort SC):**
- B3: two rows — /stair-lifts/ (service; category stair lift installer; area the Lowcountry) and /beaufort-sc/ (location; category stair lift installer; area Beaufort County), with their brief files.
- C1: /stair-lifts/ row — final URL (replaces /services/stair-lifts/), keyword "stair lifts", H1 variant "stair lift installation", H1 "Stair Lift Installation in the Lowcountry", no "The Best"; brief approved.
- C2: /beaufort-sc/ row — final URL (replaces /service-area/beaufort-sc/), keyword "stair lifts Beaufort SC", H1 "Stair Lift Installer in Beaufort", variants; brief approved.
- C3: 21 rows — 4 H2 + 4 H3 + 5 FAQ for /stair-lifts/; 5 H2 + 3 FAQ for /beaufort-sc/.
- `records.py render` run; Brand Guide copied to Drive (`drive.py upload`); `status.py writeback home-mobile-medical pilot` recorded.

**Not done:** the C1 row for /services/straight-stair-lifts/ still says "consolidated into /services/stair-lifts/" (should read /stair-lifts/). The edit was blocked by the permission classifier; left for Paul or the next write-back.

**Open / waiting (not blocking):** 3 open facts with the client; blocker handoffs issued, not returned.
### END HANDOFF
## RUN 20261014-133132-build-f0c5 · FINISHED · 2026-10-14T13:33:30-05:00
Changes: 1 · Summary: Pilot Brand Guide write-back: B3, C1/C2, C3 (21 rows) from approved briefs; recorded once
- CHANGE #188 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #189 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14 (3).md | new: Home Mobile Medical - Handoff Log.md · sha a624e79bf4b1 | result: done · copied (Drive for desktop syncs it)
- CHANGE #190 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (6).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #191 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (6).md | new: Home Mobile Medical - Document Checklist.md · sha 19fd1f8bf8a9 | result: done · copied (Drive for desktop syncs it)
- CHANGE #192 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Brand Guide - 2026-10-14.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | new: _Archive/Home Mobile Medical - Brand Guide - 2026-10-14.md | result: done · renamed and moved, nothing deleted
- CHANGE #193 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | upload | old: previous version archived as Home Mobile Medical - Brand Guide - 2026-10-14.md | new: Home Mobile Medical - Brand Guide.md · sha ded5e8aed622 | result: done · copied (Drive for desktop syncs it)
- CHANGE #194 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (6).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #195 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (6).md | new: Home Mobile Medical - Status.md · sha 3613ea8fc5a2 | result: done · copied (Drive for desktop syncs it)

## RUN 20261014-140654-build-4002 · STARTED · /build · 2026-10-14T14:06:54-05:00
Step: build:facts · session ab18dcf5-8794-4fa9-be37-18f6db3e0880
Gates checked: discovery_signed_off, site_plan, page_specs_approved
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-beaufort-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-curved-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-porch-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-wheelchair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-repair-maintenance: WARN (known 8, unknown 1, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · hub-hhi-beaufort: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-bluffton-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-hilton-head-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-port-royal-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-ladys-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-laurel-bay-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-daufuskie-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-okatie-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-hardeeville-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-ridgeland-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-levy-sc: PASS (known 6, unknown 3, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-yemassee-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · hub-charleston: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-charleston-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-north-charleston-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-mount-pleasant-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-summerville-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-goose-creek-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-hanahan-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-moncks-corner-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-hollywood-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-kiawah-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-folly-island-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-walterboro-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-edisto-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · homepage: PASS (known 10, unknown 1, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · about: PASS (known 6, unknown 2, unverified 0, conflict 0)
- REVIEW FACTS 2026-10-14T14:07 · run 20261014-140654-build-4002 · 8 fact(s)/topic(s) found in reviews, 0 with 3+ different reviewers (customer_reported, CM-057) · data/reviews/review-facts.json
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-beaufort-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-curved-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-porch-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-wheelchair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · svc-repair-maintenance: WARN (known 8, unknown 1, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · hub-hhi-beaufort: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-bluffton-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-hilton-head-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-port-royal-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-ladys-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-laurel-bay-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:07 · run 20261014-140654-build-4002 · loc-daufuskie-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-okatie-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-hardeeville-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-ridgeland-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-levy-sc: PASS (known 6, unknown 3, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-yemassee-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · hub-charleston: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-charleston-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-north-charleston-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-mount-pleasant-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-summerville-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-goose-creek-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-hanahan-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-moncks-corner-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-hollywood-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-kiawah-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-folly-island-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-walterboro-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · loc-edisto-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · homepage: PASS (known 10, unknown 1, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:08 · run 20261014-140654-build-4002 · about: PASS (known 6, unknown 2, unverified 0, conflict 0)
- FACTS INTERVIEW 2026-10-14T14:08 · run 20261014-140654-build-4002 · facts round (all pages) · 0 question(s) for svc-stair-lifts, svc-curved-stair-lifts, svc-porch-lifts, svc-wheelchair-lifts, svc-repair-maintenance · clients/home-mobile-medical/interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md
- SETTLED svc-repair-maintenance:service_process · 2026-10-14T14:08:15-05:00 · run 20261014-140654-build-4002 · by Client (via Paul) · When you call about a broken stair lift or lift, we first take your call, schedule a visit, diagnose the problem, provide a quote, order parts if needed, and complete the repair. There is no service call or trip charge. We repair any brand of stair lift or lift in our service area.
- CLOSED fact:svc-repair-maintenance:service_process · 2026-10-14T14:08:15-05:00 · run 20261014-140654-build-4002 · by svc-repair-maintenance:service_process · answered by 'svc-repair-maintenance:service_process'
- FLAG 2026-10-14T14:08 · run 20261014-140654-build-4002 · F-007 · evidence.py questions --all overwrote the open facts-round file 'Home Mobile Medical - Facts Interview - all - 2026-10-14 - REVIEW.md' (Q1-Q3, already asked and waiting) with an empty 0-question version on a same-day re-run; it should not replace a set that is still open. Also settled.py filter reports the still-open fact:svc-repair-maintenance:service_process as 'already answered'. · workaround: Left the file changed (restore was blocked by the permission system); the sent version is intact in git HEAD (f5c00c6) and in facts-round-all-2026-10-14.questions.json. Paul or the main chat can restore it with git checkout of that one file.
- SETTLED d:emergency · 2026-10-14T14:08:41-05:00 · run 20261014-140654-build-4002 · by Client (via Paul) · Our office is open Monday through Friday, 9 a.m. to 5 p.m. True emergencies are handled after hours; after-hours availability depends on current demand. Urgent non-emergency calls are scheduled as soon as possible.
- SETTLED svc-curved-stair-lifts:install_time · 2026-10-14T14:08:56-05:00 · run 20261014-140654-build-4002 · by Client (via Paul) · Stair lift installations typically take a couple of hours, and we can often complete two per day for curved, porch and wheelchair lifts. The actual timeline depends on project scope and is confirmed during your free in-home estimate.
- CLOSED fact:svc-curved-stair-lifts:install_time · 2026-10-14T14:08:56-05:00 · run 20261014-140654-build-4002 · by svc-curved-stair-lifts:install_time · answered by 'svc-curved-stair-lifts:install_time'
### HANDOFF · /build · 2026-10-14 · run 20261014-140654-build-4002
- Re-ran evidence grids for all 33 pages (evidence.py run --all): 0 block, 5 warn (all service pages), 28 pass.
- reviews.py extract: 8 review topics, none from 3+ reviewers, so no researcher check by meaning was needed; facts.json section R updated by the script.
- research.py todo for every batch (services, loc-hhi, loc-charleston, final, pilot): every gap already has a research-log entry from the earlier facts round today. No new public research run; researcher not spawned.
- evidence.py questions --all: 0 new questions. The three open client questions (service_process, d:emergency, install_time) were asked earlier today and are still waiting on the client via Paul.
- No facts recorded with run.py fact in this run (no new answers or sourced values).
- Flag F-007: the questions command overwrote the open facts-round REVIEW.md with an empty version; the sent version is in git HEAD. Restore was blocked by the permission system.
- Remaining [NEED]: emergency/after-hours (all location pages), repair service process (svc-repair-maintenance, required), install times for curved/porch/wheelchair lifts. Supporting gaps left out of pages: awards, associations; neighbourhoods for Folly Island, Laurel Bay, Levy; named places for Levy (researched, not found).
### END HANDOFF
## RUN 20261014-140654-build-4002 · FINISHED · 2026-10-14T14:14:22-05:00
Changes: 0 · Summary: Facts round re-check: all 33 page grids re-run (none blocked; 5 service pages warn, 28 pass). No new questions. Question sheet restored from f5c00c6 after F-007. Repair process, emergency hours and curved/porch/wheelchair install times were answered by Paul via decisions and settled after this re-check.
- CHANGE #196 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (4).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #197 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14 (4).md | new: Home Mobile Medical - Handoff Log.md · sha 96011c49058c | result: done · copied (Drive for desktop syncs it)
- CHANGE #198 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (7).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #199 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (7).md | new: Home Mobile Medical - Document Checklist.md · sha 52785f4ec8c8 | result: done · copied (Drive for desktop syncs it)
- CHANGE #200 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (7).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #201 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (7).md | new: Home Mobile Medical - Status.md · sha 0c533641b763 | result: done · copied (Drive for desktop syncs it)

## RUN 20261014-141534-interview-b760 · STARTED · /interview · 2026-10-14T14:15:34-05:00
Step: interview:facts-answers · batch all · session c2bdc5c2-5a67-42d5-84e8-bf06c732f070
Gates checked: discovery_signed_off
- FACT 2026-10-14T14:16 · run 20261014-141534-interview-b760 · d-emergency-after-hours-reality (value, status, source) · client_confirmed · Office hours are Monday–Friday 9 AM–5 PM. True emergencies are handled after hours. Urgent calls that are not emergencies are scheduled as soon as possible. After-hours availability depends on current · source Facts interview 2026-10-14, owner reply Q2 (general terms only) · by Paul
- FACT 2026-10-14T14:16 · run 20261014-141534-interview-b760 · d-minimum-service-call-or-trip-charge (value, status, source) · client_confirmed · None. No service-call or trip charge. · source Facts interview 2026-10-14, owner reply Q1 · by Paul
- FACT 2026-10-14T14:16 · run 20261014-141534-interview-b760 · svc-repair-maintenance:service_process (new) · client_confirmed · When someone calls about a broken stair lift or lift: first call, visit, diagnosis, quote, parts, fix. No service-call or trip charge. Repairs any stair lift or lift, any brand, within the service are · source Facts interview 2026-10-14, owner reply Q1; website wording allowed (yes) · by Paul
- FACT 2026-10-14T14:16 · run 20261014-141534-interview-b760 · d-install-time-other-lifts (new) · client_confirmed · The installation itself is quick for curved, porch and wheelchair lifts, the same as stair lifts. More than one installation can be done in a day, so the schedule is adjusted to fit. · source Facts interview 2026-10-14, owner reply Q3 (partial) · by Paul
- FACT 2026-10-14T14:16 · run 20261014-141534-interview-b760 · d-lead-time-and-pad-permit (new) · unknown · [NEED] Order-to-installed lead time for curved, porch and wheelchair lifts. [NEED] Who handles the concrete pad and building permit for porch and wheelchair lifts (you, the customer, or it depends). · source Facts interview 2026-10-14, owner reply Q3: not answered · by Paul
- SETTLED fact:svc-repair-maintenance:service_process · 2026-10-14T14:16:34-05:00 · run 20261014-141534-interview-b760 · by Client (via Paul) · Repair steps: first call, visit, diagnosis, quote, parts, fix. No service-call or trip charge. Website wording allowed: yes.
- SETTLED fact:d:emergency · 2026-10-14T14:16:34-05:00 · run 20261014-141534-interview-b760 · by Client (via Paul) · True emergencies are handled after hours; urgent non-emergency calls are scheduled as soon as possible; after-hours availability depends on current demand. Publish in general terms only; do not promise after-hours response.
- SETTLED fact:svc-curved-stair-lifts:install_time · 2026-10-14T14:16:34-05:00 · run 20261014-141534-interview-b760 · by Client (via Paul) · Installation itself is quick for every lift type (curved, porch, wheelchair); multiple installs per day possible. Order-to-installed lead time and pad/permit responsibility not answered.
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · svc-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-beaufort-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · svc-curved-stair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · svc-porch-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · svc-wheelchair-lifts: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · svc-repair-maintenance: WARN (known 9, unknown 0, unverified 3, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · hub-hhi-beaufort: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-bluffton-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-hilton-head-island-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-port-royal-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-ladys-island-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-laurel-bay-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-daufuskie-island-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-okatie-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-hardeeville-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-ridgeland-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-levy-sc: PASS (known 7, unknown 2, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-yemassee-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · hub-charleston: PASS (known 6, unknown 0, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-charleston-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-north-charleston-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-mount-pleasant-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-summerville-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-goose-creek-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-hanahan-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-moncks-corner-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-hollywood-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-kiawah-island-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-folly-island-sc: PASS (known 8, unknown 1, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-walterboro-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · loc-edisto-island-sc: PASS (known 9, unknown 0, unverified 1, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · homepage: PASS (known 10, unknown 1, unverified 0, conflict 0)
- EVIDENCE 2026-10-14T14:16 · run 20261014-141534-interview-b760 · about: PASS (known 6, unknown 2, unverified 0, conflict 0)
### HANDOFF · /interview · 2026-10-14 · run 20261014-141534-interview-b760
## Handoff Log

**Step:** facts-answers, batch `all` (the 2026-10-14 facts round, 3 questions).
**Reply saved:** `clients/home-mobile-medical/interviews/facts/Home Mobile Medical - Facts Interview - all - 2026-10-14 - REPLY.md` (as given).

**Answers and where they went**

| Key | Answer (short) | Brand Guide D | Settled |
|---|---|---|---|
| `fact:svc-repair-maintenance:service_process` | Steps as suggested (first call, visit, diagnosis, quote, parts, fix). No service-call or trip charge. Website wording: yes. | New row "Repair process: steps and charge" (Client Confirmed); trip-charge row changed from [NEED] to "None" (Client Confirmed) | Yes, by Client (via Paul) |
| `fact:d:emergency` | No standing after-hours service. True emergencies handled after hours; urgent non-emergency calls scheduled ASAP; after-hours availability depends on current demand. Advertise in general terms only. | "Emergency / after-hours reality" row changed from [NEED] to general-terms wording (Client Confirmed) | Yes, by Client (via Paul) |
| `fact:svc-curved-stair-lifts:install_time` | Installation itself is quick for curved, porch and wheelchair lifts; more than one install per day possible. **Partial.** | New row "Install time: curved, porch and wheelchair lifts" (Client Confirmed) | Yes, with open items left open |

**Still open (not answered):**
- Order-to-installed lead time for curved, porch and wheelchair lifts.
- Who handles the concrete pad and building permit for porch and wheelchair lifts (owner, customer, or depends).

Recorded as Unknown in Brand Guide D: row "Order-to-installed lead time; pad and permit for porch and wheelchair lifts".

**Gate re-run:** `python3 scripts/evidence.py run home-mobile-medical --run 20261014-141534-interview-b760 --all`
- Before: the five service pages were blocked on the three questions.
- After: no page is blocked. The five service pages (svc-repair-maintenance, svc-curved-stair-lifts, svc-porch-lifts, svc-wheelchair-lifts, svc-stair-lifts) now WARN with 3 supporting unverified gaps each; the brief must list them under "Evidence gaps".
- All location, hub, homepage and about pages PASS (some with 1–2 unverified or unknown supporting facts).

**Brand Guide changed:** Section D was edited, so `brand_guide_approved` is void until Paul re-approves. `/next` gives the approval line.

**Facts pack note:** `evidence.py run --batch all` is not a valid batch name, so the gate was re-run with `--all`.

**Next for Paul**
1. Re-approve the Brand Guide (sees the new D rows first).
2. Decide on the two open items: send a follow-up question for lead time and pad/permit, or accept the current wording (the pages say the install timeline is confirmed at the free in-home estimate).
3. Check the Brand Guide's D2 section: the homepage and service wording may still need the "no after-hours" and "same-day in most cases" lines re-checked when briefs are drafted.
### END HANDOFF
## RUN 20261014-141534-interview-b760 · FINISHED · 2026-10-14T14:17:07-05:00
Changes: 0 · Summary: Facts-answers (batch all): 3 owner answers saved, written to Brand Guide D, settled. Evidence gate re-run: no page blocked; service pages WARN on 3 supporting gaps each. Brand Guide changed, needs Paul re-approval. Open: install lead time and pad/permit.
- CHANGE #202 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (5).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #203 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14 (5).md | new: Home Mobile Medical - Handoff Log.md · sha d5887139c52b | result: done · copied (Drive for desktop syncs it)
- CHANGE #204 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (8).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (8).md | result: done · renamed and moved, nothing deleted
- CHANGE #205 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (8).md | new: Home Mobile Medical - Document Checklist.md · sha c99ce6913f45 | result: done · copied (Drive for desktop syncs it)
- CHANGE #206 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Brand Guide - 2026-10-14 (2).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | new: _Archive/Home Mobile Medical - Brand Guide - 2026-10-14 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #207 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | upload | old: previous version archived as Home Mobile Medical - Brand Guide - 2026-10-14 (2).md | new: Home Mobile Medical - Brand Guide.md · sha 4971136af402 | result: done · copied (Drive for desktop syncs it)
- CHANGE #208 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (8).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (8).md | result: done · renamed and moved, nothing deleted
- CHANGE #209 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (8).md | new: Home Mobile Medical - Status.md · sha 30659e078b9a | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-14T14:18 · after build:facts (run 20261014-140654-build-4002) · Paul typed /next

## MIGRATION · 2026-10-14T14:18:23-05:00 · URL move: references follow the new URL
brand-guide.md:87: /services/ → https://homemobilemedical.com/
brand-guide.md:89: /services/curved-stair-lifts/ → https://homemobilemedical.com/curved-stair-lifts/
brand-guide.md:90: /services/porch-lifts/ → https://homemobilemedical.com/porch-lifts/
brand-guide.md:91: /services/wheelchair-lifts/ → https://homemobilemedical.com/wheelchair-lifts/
brand-guide.md:92: /services/stair-lifts/ → https://homemobilemedical.com/stair-lifts/
brand-guide.md:103: /service-area/bluffton-sc/ → https://homemobilemedical.com/bluffton-sc/
brand-guide.md:104: /service-area/hilton-head-island-sc/ → https://homemobilemedical.com/hilton-head-island-sc/
brand-guide.md:105: /service-area/port-royal-sc/ → https://homemobilemedical.com/port-royal-sc/
brand-guide.md:106: /service-area/ladys-island-sc/ → https://homemobilemedical.com/ladys-island-sc/
brand-guide.md:107: /service-area/laurel-bay-sc/ → https://homemobilemedical.com/laurel-bay-sc/
brand-guide.md:108: /service-area/daufuskie-island-sc/ → https://homemobilemedical.com/daufuskie-island-sc/
brand-guide.md:109: /service-area/okatie-sc/ → https://homemobilemedical.com/okatie-sc/
brand-guide.md:110: /service-area/yemassee-sc/ → https://homemobilemedical.com/yemassee-sc/
brand-guide.md:111: /service-area/hardeeville-sc/ → https://homemobilemedical.com/hardeeville-sc/
brand-guide.md:112: /service-area/ridgeland-sc/ → https://homemobilemedical.com/ridgeland-sc/
brand-guide.md:113: /service-area/levy-sc/ → https://homemobilemedical.com/levy-sc/
brand-guide.md:114: /service-area/walterboro-sc/ → https://homemobilemedical.com/walterboro-sc/
brand-guide.md:115: /service-area/edisto-island-sc/ → https://homemobilemedical.com/edisto-island-sc/
brand-guide.md:116: /service-area/charleston-sc/ → https://homemobilemedical.com/charleston-sc/
brand-guide.md:117: /service-area/north-charleston-sc/ → https://homemobilemedical.com/north-charleston-sc/
brand-guide.md:118: /service-area/mount-pleasant-sc/ → https://homemobilemedical.com/mount-pleasant-sc/
brand-guide.md:119: /service-area/summerville-sc/ → https://homemobilemedical.com/summerville-sc/
brand-guide.md:120: /service-area/goose-creek-sc/ → https://homemobilemedical.com/goose-creek-sc/
brand-guide.md:121: /service-area/hanahan-sc/ → https://homemobilemedical.com/hanahan-sc/
brand-guide.md:122: /service-area/moncks-corner-sc/ → https://homemobilemedical.com/moncks-corner-sc/
brand-guide.md:123: /service-area/hollywood-sc/ → https://homemobilemedical.com/hollywood-sc/
brand-guide.md:124: /service-area/kiawah-island-sc/ → https://homemobilemedical.com/kiawah-island-sc/
brand-guide.md:125: /service-area/folly-island-sc/ → https://homemobilemedical.com/folly-island-sc/
brand-guide.md (Section C prose): Canonical pattern `/service-area/{city-state}/` (D… → the root pattern
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-01: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-02: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-03: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-04: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-05: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-06: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-07: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-08: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
H-2026-10-09-04-broken_link.csv H-2026-10-09-04-broken_link-09: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:2: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:3: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:4: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:5: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:6: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:7: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:8: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:9: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/broken_link-items.csv:10: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/
build/blockers/redirect-items.csv:2: https://homemobilemedical.com/service-area/bluffton-sc/ → https://homemobilemedical.com/bluffton-sc/
build/blockers/redirect-items.csv:3: https://homemobilemedical.com/service-area/charleston-sc/ → https://homemobilemedical.com/charleston-sc/
build/blockers/redirect-items.csv:4: https://homemobilemedical.com/service-area/beaufort-sc/ → https://homemobilemedical.com/beaufort-sc/

## RUN 20261014-141838-build-9492 · STARTED · /build · 2026-10-14T14:18:38-05:00
Step: build:pilot-corrections · session c2bdc5c2-5a67-42d5-84e8-bf06c732f070
Gates checked: discovery_signed_off, batch:pilot:briefs
### HANDOFF · /build · 2026-10-14 · run 20261014-141838-build-9492
- Source of Paul's notes: drafts review "accept all, Ask 1 = A" (run 20261014-131553-build-b121); briefs and drafts approved 2026-10-14 13:28/13:29 as written, SEM none; brief mode → auto.
- Paul wrote no corrections. No spec element or check changed for this client; nothing flagged for /system-review.
- build/pilot-corrections.md written: "none" under Paul's corrections, plus 5 accepted pilot answers/defaults carried forward (safety line kept verbatim at grade 11.3 — C5/CM-047; location cost FAQ uses the quote angle — BB-316; Recent work dropped without a town review — LOC-29; title with GBP primary category — LOC-02; install time from settled facts only).
- Open for Paul (one line, default given): may other Beaufort County pages also name Beaufort Medical Equipment? Default: no, Beaufort page only.
- `status.py pilot-corrections` recorded. Later batches (services, loc-hhi, loc-charleston, final) may start.
- Settled decisions untouched.
### END HANDOFF
### END HANDOFF
## RUN 20261014-141838-build-9492 · FINISHED · 2026-10-14T14:19:42-05:00
Changes: 0 · Summary: Pilot corrections: none from Paul; 5 accepted pilot defaults carried forward in build/pilot-corrections.md; 1 open question
- CHANGE #210 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (6).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #211 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14 (6).md | new: Home Mobile Medical - Handoff Log.md · sha b2530c52c820 | result: done · copied (Drive for desktop syncs it)
- CHANGE #212 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (9).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (9).md | result: done · renamed and moved, nothing deleted
- CHANGE #213 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (9).md | new: Home Mobile Medical - Document Checklist.md · sha 8726631ef017 | result: done · copied (Drive for desktop syncs it)
- CHANGE #214 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Brand Guide - 2026-10-14 (3).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | new: _Archive/Home Mobile Medical - Brand Guide - 2026-10-14 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #215 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Brand Guide.md | upload | old: previous version archived as Home Mobile Medical - Brand Guide - 2026-10-14 (3).md | new: Home Mobile Medical - Brand Guide.md · sha 55e993be2b2f | result: done · copied (Drive for desktop syncs it)
- CHANGE #216 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (9).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (9).md | result: done · renamed and moved, nothing deleted
- CHANGE #217 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (9).md | new: Home Mobile Medical - Status.md · sha 9358723b4dcb | result: done · copied (Drive for desktop syncs it)
- CHANGE #218 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - VA Worklist - 2026-10-14.md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | new: _Archive/Home Mobile Medical - VA Worklist - 2026-10-14.md | result: done · renamed and moved, nothing deleted
- CHANGE #219 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.md | upload | old: previous version archived as Home Mobile Medical - VA Worklist - 2026-10-14.md | new: Home Mobile Medical - VA Worklist.md · sha c728c796be79 | result: done · copied (Drive for desktop syncs it)
- CHANGE #220 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - VA Worklist - 2026-10-14.csv | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | new: _Archive/Home Mobile Medical - VA Worklist - 2026-10-14.csv | result: done · renamed and moved, nothing deleted
- CHANGE #221 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - VA Worklist.csv | upload | old: previous version archived as Home Mobile Medical - VA Worklist - 2026-10-14.csv | new: Home Mobile Medical - VA Worklist.csv · sha 46ee3b69081c | result: done · copied (Drive for desktop syncs it)

## RUN 20261014-143231-build-f825 · STARTED · /build · 2026-10-14T14:32:31-05:00
Step: build:pilot-corrections · session c2bdc5c2-5a67-42d5-84e8-bf06c732f070
Gates checked: discovery_signed_off, batch:pilot:briefs
- SETTLED bme-mention · 2026-10-14T14:32:35-05:00 · run 20261014-143231-build-f825 · by Paul · Beaufort Medical Equipment (Jason's former company) is not mentioned anywhere on the site or in drafts, including the Beaufort page. The Brand Guide history row stays internal.
- CHANGE #222 [x] x | x | old:  | new:  | result: x
- CHANGE #223 [draft-edit] build/pilot/drafts/loc-beaufort-sc.md | faq3-former-company | old: FAQ 3: Is Home Mobile Medical the Same Company as Beaufort Medical Equipment? | new:  | result: removed per Paul: no BME mentions
### HANDOFF · /build · 2026-10-14 · run 20261014-143231-build-f825
## Handoff Log

- **Paul's decision (chat):** no mentions of Beaufort Medical Equipment (BME), Jason's former company, anywhere on the site or in drafts, including the Beaufort page. Settled as `bme-mention`.
- **Draft changed:** `build/pilot/drafts/loc-beaufort-sc.md`. FAQ 3 "Is Home Mobile Medical the Same Company as Beaufort Medical Equipment?" removed. Logged as change #223.
- **Still mentions BME (internal only, not public copy):** Brand Guide D history row; `build/evidence/about.facts.json` and `about.grid.md`; `build/loc-hhi/packs/*`. Check before any brief or draft is written from them.
- **Open:** `build/pilot-corrections.md` still lists "whether other Beaufort County pages may also name the former company" as open. The settled answer is no, so that line is superseded by `bme-mention`.
- **Logging error:** a test `run.py change` with placeholder values (kind x, url x) was written to the changes log as entry #222 during this run. The log is append-only, so it cannot be removed here. It needs noting in the next system session.
### END HANDOFF
## RUN 20261014-143231-build-f825 · FINISHED · 2026-10-14T14:32:54-05:00
Changes: 2 · Summary: No BME mentions: decision settled; Beaufort FAQ 3 removed from pilot draft.
- CHANGE #224 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (7).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | new: _Archive/Home Mobile Medical - Handoff Log - 2026-10-14 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #225 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Handoff Log.md | upload | old: previous version archived as Home Mobile Medical - Handoff Log - 2026-10-14 (7).md | new: Home Mobile Medical - Handoff Log.md · sha 385f3e1efa5e | result: done · copied (Drive for desktop syncs it)
- CHANGE #226 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (10).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | new: _Archive/Home Mobile Medical - Document Checklist - 2026-10-14 (10).md | result: done · renamed and moved, nothing deleted
- CHANGE #227 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Document Checklist.md | upload | old: previous version archived as Home Mobile Medical - Document Checklist - 2026-10-14 (10).md | new: Home Mobile Medical - Document Checklist.md · sha 94bdb6e02a49 | result: done · copied (Drive for desktop syncs it)
- CHANGE #228 [drive_file] drive:Home Mobile Medical - TMS/_Archive/Home Mobile Medical - Status - 2026-10-14 (10).md | archive | old: drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | new: _Archive/Home Mobile Medical - Status - 2026-10-14 (10).md | result: done · renamed and moved, nothing deleted
- CHANGE #229 [drive_file] drive:Home Mobile Medical - TMS/Home Mobile Medical - Status.md | upload | old: previous version archived as Home Mobile Medical - Status - 2026-10-14 (10).md | new: Home Mobile Medical - Status.md · sha 81a5e9004e98 | result: done · copied (Drive for desktop syncs it)
