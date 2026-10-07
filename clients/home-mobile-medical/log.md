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
