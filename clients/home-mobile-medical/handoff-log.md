# Home Mobile Medical - Handoff Log

Generated from the safety log (clients/home-mobile-medical/log.md) — do not edit. Each run adds its section with `run.py finish --handoff <file>`. The newest section is at the bottom.

## /new-client · 2026-10-07 · run 20261006-112201-new-client-fb9a

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

## /wp-check · 2026-10-07 · run 20261007-172152-wp-check-12e0

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

