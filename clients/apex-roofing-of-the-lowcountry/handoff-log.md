# Apex Roofing of the Lowcountry - Handoff Log

Generated from the safety log (clients/apex-roofing-of-the-lowcountry/log.md) — do not edit. Each run adds its section with `run.py finish --handoff <file>`. The newest section is at the bottom.

## /new-client · 2026-10-05 · run 20261005-210907-new-client-b5e9

**What I did**
- Created the client record: Apex Roofing of the Lowcountry, apexroofingtlc.com, full client, industry roofing.
- Recorded intake: GBP https://maps.app.goo.gl/AWfz3YNkwvsrggFg7 · service-area business · GBP Website field `http://www.apexroofingtlc.com/` · no Search Console or GA4 access.
- Set the safe-fix cap on Paul's word: 5 alt texts, 2 broken links, until he has checked them live.
- Built the Drive folder `Apex Roofing of the Lowcountry - TMS` in v3 with the template's folders (01 - Discovery and Audit/Evidence and Deliverables, 02 - Build, 03 - Finish, 04 - Blog, _Archive).
- Created the Brand Guide working copy from the template (every field still blank) and started `test-run-notes.md`.

**What was decided, and why**
- Not a sensitive client: the category check returned "no" for roofing (CM-025, CM-040).
- No GSC/GA4: rankings and destructive-candidate checks rely on DataforSEO only (CM-019, CM-021).
- The connector can't copy folders, so the template folder tree was rebuilt by hand (matches the template as of today).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| WordPress `seo-ops` Editor user + Application Password (handoff issued right after this run) | Jonie | /wp-check, any WordPress step |
| `WP_APEX_ROOFING_OF_THE_LOWCOUNTRY_URL / _USER / _APP_PASSWORD` in .env | Paul | /wp-check |
| Whether the older Apex folders elsewhere in Drive are source material | Paul | Nothing yet (discovery can use them if he says so) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Blank template |
| Drive folder | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Created |

**What I could not check**
- The GBP listing and the WordPress connection (not set up yet). Whether the http://www. GBP link and the https:// site resolve to the same place — discovery checks that.

**Anything the next agent would otherwise get wrong**
- No Search Console or GA4. And the GBP Website field (`http://www.`) differs from the site URL as given (`https://`, no www) — record what each resolves to; it is not a finding until the audit.

## /wp-check · 2026-10-05 · run 20261005-211116-wp-check-0f33

**What I did**
- Checked from the public site that apexroofingtlc.com runs WordPress: Kadence theme, Kadence Blocks + Pro, WPForms User Journey, AccelerateWP; Apache host. `http://www.apexroofingtlc.com/` (the GBP Website field) 301s in one hop to `https://apexroofingtlc.com/`.
- Issued handoff H-2026-10-05-01-other to Jonie: create the `seo-ops` Editor user and its Application Password (sent to Paul privately, never in the worksheet), and record the SEOPress version, permalink setting and any security plugin — record only, nothing changed.

**What was decided, and why**
- The connection test (`wp.py check`) was not run: there are no credentials yet, so it could only fail. It runs once Jonie is done and Paul has added the .env lines.
- Handoff sent to Jonie rather than the `other` default (Gwen): WordPress setup is WordPress work (CLAUDE.md §4).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| H-2026-10-05-01-other — seo-ops Editor user, Application Password, SEOPress/permalink/security record | Jonie | /wp-check |
| `WP_APEX_ROOFING_OF_THE_LOWCOUNTRY_URL / _USER / _APP_PASSWORD` in .env | Paul | /wp-check |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| WordPress setup handoff | clients/apex-roofing-of-the-lowcountry/handoffs/H-2026-10-05-01-other.md (+ .csv) | Issued to Jonie |

**What I could not check**
- The WordPress connection, SEOPress version, and whether the REST API is open — all need the seo-ops login.

**Anything the next agent would otherwise get wrong**
- Discovery does not need WordPress. It can run now; /wp-check is only needed before the first WordPress step (safe fixes after the audit approval).

## /drive-mirror · 2026-10-05 · run 20261005-211145-drive-mirror-3ea9

**What I did**
- First upload to the client Drive folder: Handoff Log, Approval Record and Document Checklist as real `.md` files under their standard names. Nothing to archive (no earlier copies).

**What was decided, and why**
- The Brand Guide is not mirrored yet: it is still the blank template. It goes up once discovery fills Section A.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Records in Drive | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Uploaded |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- Later mirrors are archive-and-replace (dated name → `_Archive`, upload new), never a second copy beside the first.

## /discovery · 2026-10-05 · run 20261005-211303-discovery-aee7

**What I did**
- Discovery from free public sources (S01–S03, all recorded done): live site, GBP public view, Facebook, BBB, HomeAdvisor, OpenCorporates copy of the SC record, WHOIS, Wikipedia/Wikidata. No paid calls.
- Proposed the entity foundation: category "Roofing contractor" (Wikipedia: Roofer, Q552378); area Hilton Head Island–Bluffton–Port Royal MSA (Q17020871) by Russian Doll Bluffton → Beaufort County → MSA, containing all 12 location-page cities; variants Roofing Contractor / Roofer / Roofers / Roof Mechanic; reserved homepage variant "Hilton Head Island Metropolitan Area".
- Wrote the Discovery Record (REVIEW) and the public-sources evidence capture; filled Brand Guide A, B and the Section F Wikidata rows as proposals.

**What was decided, and why**
- Nothing resolved: ten conflicts recorded with all candidate values (C1 Georgia service area, C2 start date, C3 owner roles, C4 residential vs commercial, C5 name form, C6 BBB street address on an SAB, C7 Levy county, C8 Okatie county, C9 ratings, C10 MSA name). None is a methodology conflict, so no PROC-01 entry.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Entity foundation | Paul (`entity_approved`) | Proof sheet |
| C1 — does Apex serve Coastal Georgia? (would change the area entity) | Paul / client via proof sheet | Area entity is final only once answered |
| Q8 "Hilton Head Island Metro Area" as a variant · Q9 one county URI or both | Paul | Schema later; entity approval now |
| SC SOS and SC LLR lookups (CAPTCHA) | Gwen or Paul, manual | Licence + legal entity stay "found", not verified |
| GBP secondary categories / service-area list (dashboard only) | Paul / client | BB-107 check |
| Domain apexroofingtlc.com expires 2026-11-23 (WHOIS) | Paul to mention to the client | Nothing in the system — but the site goes dark if it lapses |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md · Drive https://drive.google.com/file/d/1rwCwFByhKeO4g2NQbZeYuWharwMBGP1C/view | For Paul's review |
| Evidence capture | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05.md · Drive https://drive.google.com/file/d/1KRun10jn91aLeCsUkm-lmzq-NZj_jtmN/view | Uploaded |
| Brand Guide A/B/F | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Proposals; mirrored next |

**What I could not check**
- SC Secretary of State and SC LLR (CAPTCHA); GBP secondary categories, service areas, open date, Q&A; HomeAdvisor profile (403); Yelp, Angi, Nextdoor, Instagram, LinkedIn, Apple Maps, Bing Places, manufacturer directories.

**Anything the next agent would otherwise get wrong**
- "Apex Roofing of Coastal Georgia" (St. Simons Island, GAF directory) may be a different company — don't merge its facts. And every service/location H1 already starts "The Best…": that is an observation, not a finding, until the audit (CM-020).

## /drive-mirror · 2026-10-05 · run 20261005-212655-drive-mirror-c34f

**What I did**
- Archive-and-replace for the Handoff Log and Document Checklist: old copies renamed with `- 2026-10-05` and moved into `_Archive`; new versions uploaded under the standard names.
- First upload of the Brand Guide (Sections A, B and F proposals from discovery).

**What was decided, and why**
- The Approval Record was left as it is: its content has not changed since the first upload (every decision still pending).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Records + Brand Guide in Drive | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Current as of the discovery run |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- Two files called "… - 2026-10-05.md" now sit in `_Archive`; a second archive on the same day needs `drive.py archive-name --n 2`.

## /discovery · 2026-10-05 · run 20261005-215259-discovery-acd3

**What I did**
- Applied Paul's direction on the entity proposal to the Brand Guide (A, B, F) and the Discovery Record (new §3.6; C1 annotated). Nothing else changed.

**What was decided, and why**
- Area entity: **South Carolina Lowcountry** (Wikipedia title; Wikidata Q3885311), Paul's choice over the smaller Hilton Head Island–Bluffton–Port Royal MSA. This deviates from BB-105's "smallest true container" and is logged as Paul's decision. It contains all 12 cities, and BB-105's own Beaufort + Jasper example names it.
- Reserved homepage variant: **South Carolina Lowcountry**. Bare "Lowcountry" is in the brand name on every page, so it can't be homepage-only; it goes into the rotation pool.
- Category variants: Roofing Contractor, Roofer, Roofers. Roof Mechanic is excluded; Residential Roofer stays a candidate only.
- Georgia is not served currently (Paul). C1 is closed for the entity; the homepage "& Coastal Georgia" line stays an observation for the audit.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `entity_approved` on the revised files | Paul | Proof sheet |
| WordPress: dedicated `seo-ops` Editor + Application Password → `.env` (credentials were given in chat for a personal login) | Jonie (H-2026-10-05-01-other) / Paul | /wp-check |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | Revised, awaits approval |
| Brand Guide | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Revised, awaits approval |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- The Drive copy of the Discovery Record is still the version before Paul's changes. After approval the approved version goes up as `- APPROVED.md`. Use the repo file.

## /discovery · 2026-10-05 · run 20261005-221139-discovery-5ddf

**What I did**
- Applied Paul's second direction on the area entity to the Brand Guide (A5, A6, derivation, B1, B2, F) and the Discovery Record (new §3.7).

**What was decided, and why**
- Area entity: back to the **Hilton Head Island–Bluffton–Port Royal, SC MSA** (Q17020871). The brand name "Apex Roofing of the Lowcountry" is in every SEO title, so a Lowcountry area entity would repeat it. This is also BB-105's smallest container, so the earlier deviation is gone.
- Reserved homepage variant (homepage SEO title): **Hilton Head Island–Bluffton–Port Royal Metropolitan Area**.
- "South Carolina Lowcountry" and "Lowcountry" stay in the rotation pool but are never used in an SEO title — H1, H2s and body only.
- Category (Roofing Contractor; variants Roofing Contractor, Roofer, Roofers) and Georgia (not served) are unchanged.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Wording of the reserved variant: "…Metropolitan Area" (default) or "…Metro Area" (Q8) | Paul | entity_approved |
| Whether the Lowcountry-out-of-SEO-titles rule applies site-wide (default) or to the homepage only | Paul | entity_approved |
| `entity_approved` on the revised files | Paul | Proof sheet |
| WordPress `seo-ops` user + Application Password → credentials file | Jonie (H-2026-10-05-01-other) / Paul | /wp-check |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | Revised (§3.7) |
| Brand Guide | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Revised |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- §3.7 supersedes the area part of §3.6. The area entity is the MSA, not South Carolina Lowcountry.

## /wp-check · 2026-10-05 · run 20261005-221818-wp-check-1c23

**What I did**
- Ran /wp-check with the credentials Paul added. Credentials, REST API, login and draft creation all worked; two test drafts were created and trashed (logged). SEOPress site-wide settings were readable and saved as audit evidence (`inputs/seopress-settings-2026-10-05.json`).

**What was decided, and why**
- Result: **not connected**. SEOPress per-page fields were written to the test draft but couldn't be read back. A `wp.py get` on the live homepage (read-only) also reads every SEOPress field as empty, so `wp.py` doesn't understand how SEOPress 10.0.1 reports them. The check fails rather than guessing (setup §5).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `wp.py` SEOPress read for 10.x (map the response, add a test) | System fix round (Paul's go) | Every WordPress write and /verify — not the proof sheet, crawl or audit |
| Login is an Administrator, not the dedicated Editor | Paul (Jonie switches the role, or Paul allows it) | Nothing yet |
| Kadence head-code meta key | Found during the pilot | Schema (Finish) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Check report | clients/apex-roofing-of-the-lowcountry/wordpress/wp-check-2026-10-05.md | Not connected (1 FIX) |
| SEOPress site-wide settings | clients/apex-roofing-of-the-lowcountry/inputs/seopress-settings-2026-10-05.json | Audit evidence (S20) |

**What I could not check**
- Any SEOPress per-page value (reads come back empty on 10.0.1).

**Anything the next agent would otherwise get wrong**
- Empty SEOPress values from `wp.py get` on this site do NOT mean the pages have no SEO title or meta. It is a read problem. Use the crawl for live titles and meta until `wp.py` is fixed.

## /wp-check · 2026-10-05 · run 20261005-223142-wp-check-24f5

**What I did**
- Re-ran /wp-check after the SEOPress 10.x fix (commit e0cdf3b). Every SEOPress per-page field was written to a test draft and read back; both test drafts were trashed. Result: **connected** (valid 30 days).

**What was decided, and why**
- Nothing new. The login is still an Administrator (NOTE, not a failure) — Paul's call whether Jonie switches it to Editor.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Administrator login vs the dedicated Editor the spec asks for | Paul | Nothing |
| Kadence head-code meta key | Found during the pilot | Schema (Finish) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Check report | clients/apex-roofing-of-the-lowcountry/wordpress/wp-check-2026-10-05.md | Connected |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- This site runs SEOPress 10.0.1; `wp.py get` now reads its stored values. Use `wp.py raw-seo` if a field ever looks wrong.

## /discovery · 2026-10-05 · run 20261005-223335-discovery-40fe

**What I did**
- Wrote Paul's last two entity answers into the Brand Guide (B2) and the Discovery Record (§3.7): the reserved variant stays "Hilton Head Island–Bluffton–Port Royal Metropolitan Area", and the brand is always written in full in SEO titles.
- Re-recorded the entity decision's files with the Brand Guide by section (`brand-guide.md#A+B1+B2`), so later Brand Guide work doesn't cancel it.
- Issued H-2026-10-05-02-manual_lookup to Gwen: SC Secretary of State record, SC LLR licence, and the GBP dashboard (categories, service areas, opening date).

**What was decided, and why**
- "Apex Roofing of the Lowcountry" is never shortened in an SEO title, because "Lowcountry" is part of the official brand name. The Lowcountry area variants aren't added on top in SEO titles, site-wide (Paul).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `entity_approved` | Paul | Proof sheet |
| H-2026-10-05-02-manual_lookup (SOS, LLR, GBP dashboard) | Gwen | Verifying the licence and legal entity; BB-107 |
| Administrator login vs Editor | Paul | Nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | Ready for approval |
| Brand Guide A, B1, B2 | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Ready for approval |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- Discovery Record §3.7 is the final word on the area. Ignore the §3.6 Lowcountry area entity.

## /drive-mirror · 2026-10-05 · run 20261005-223638-drive-mirror-d324

**What I did**
- Archive-and-replace after Paul's `entity_approved`. Approval Record, Brand Guide, Handoff Log and Document Checklist: each old copy got a dated name and moved into `_Archive`, and the new version was uploaded under the standard name.
- Uploaded the approved Discovery Record as a new file, `Apex Roofing of the Lowcountry - Discovery Record - APPROVED.md`, in `01 - Discovery and Audit/Deliverables` (content identical to the approved version).

**What was decided, and why**
- The REVIEW copy of the Discovery Record stays where it is in Deliverables. It moves to `_Archive` only if Paul agrees (/approve step 5).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Move the Discovery Record REVIEW copy to `_Archive`? | Paul | Nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record (APPROVED) | https://drive.google.com/file/d/1gsWwLPrf9Wtfa5Ffc4GKOtqq315kpmpF/view | Uploaded |
| Records + Brand Guide | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Current as of the approval |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- The Brand Guide's A/B1/B2 rows still say "awaits entity_approved". Don't update them: that would cancel the approval. The Approval Record is the authority.

## /drive-mirror · 2026-10-06 · run 20261006-085120-drive-mirror-4406

**What I did**
- On Paul's yes, moved the pre-approval Discovery Record copy into `_Archive`, renamed with its date (`… - REVIEW - 2026-10-05.md`). Deliverables now holds only the APPROVED copy.

**What was decided, and why**
- Paul agreed to archive the REVIEW copy (/approve step 5).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Record (APPROVED) | https://drive.google.com/file/d/1gsWwLPrf9Wtfa5Ffc4GKOtqq315kpmpF/view | Current |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- —

## /discovery · 2026-10-06 · run 20261006-085141-discovery-bb0e

**What I did**
- Built the client proof sheet (S04, recorded done) from the approved Discovery Record and the Brand Guide.
  - Access asks, with no passwords anywhere.
  - Block A: 27 confirm rows, including "no Georgia" and that "Apex Roofing of Coastal Georgia" is a separate business.
  - Block B: 14 verify rows, each quoted word for word with where it appears.
  - Block C: documents and facts the client needs to send.
  - Return by Tue 20 Oct 2026.
- Saved the `.md` and the `- CLIENT COPY` Google Doc in `01 - Discovery and Audit/Deliverables`. The client was not contacted.

**What was decided, and why**
- Georgia isn't asked as an open question; it's a confirm row, per Paul.
- WordPress access is not asked. GA4/Search Console access is an optional ask.
- Gwen's manual lookups (SOS, LLR, GBP dashboard) are not asked of the client.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Paul's phone number — placeholder "[PAUL'S PHONE NUMBER]" in two places | Paul | Sending the sheet |
| Google Doc shows literal asterisks inside table cells (the Markdown didn't convert) | Paul: tidy by hand, or regenerate | Sending the sheet |
| Open choices: Georgia homepage line, claims left off, Block B length (14 vs 6–12), domain renewal note, block order, sharing | Paul | proof_sheet_approved |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Proof sheet | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md · https://drive.google.com/file/d/1InOV2XI8lZIA2iQsWbuja6pidepTX948/view | REVIEW |
| CLIENT COPY Google Doc | https://docs.google.com/document/d/11uhrPAeoOdQjw1x5ZolTDuL1FkntxL369dK3Rr7NfoU/edit | Needs the fixes above; not shared |

**What I could not check**
- How the Google Doc looks on a phone.

**Anything the next agent would otherwise get wrong**
- Any change to the sheet `.md` after Paul approves cancels the approval. Make Paul's changes first, then he approves.

## /discovery · 2026-10-06 · run 20261006-104753-discovery-44eb

**What I did**
- Recorded Paul's own answers to the proof sheet (2026-10-06) in `discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md` (internal, not sent to the client). One row per sheet item, each marked "Paul confirmed" or "to check".
- Cut the client sheet down to what only the client can answer:
  - **Access:** GBP manager access only.
  - **Confirm:** travel fee / places they won't go.
  - **Verify:** licences, CertainTeed, workmanship-guarantee length, Levy "payment arrangements".
  - **Needs:** licence class and holder name, email, after-hours, trip charge, payment methods, people/titles/certifications, the three questions.
- Re-marked `proof_sheet`.
- Checked public profiles (free search): Yelp, Angi 4.9/45, Nextdoor, Houzz, Manta, GAF directory ("GAF Certified", "RBS 57706"), and Ralph's LinkedIn. Added them as a dated addendum to the evidence capture.
- Drive: archive-and-replace for the sheet `.md`, the CLIENT COPY Google Doc (rebuilt from HTML) and the evidence capture.

**What was decided, and why**
- Paul confirmed:
  - SAB based in Bluffton, SC; the phone and hours as listed; all 8 services kept; all 12 towns.
  - Coastal GA is not theirs; start year 2015; founder statement as on the homepage.
  - Residential only for now; the Roof Installation page is accurate.
  - Public name "Apex Roofing of the Lowcountry"; show only "Bluffton, SC".
  - SureStart PLUS, insurance, free estimates and pricing are all accurate.
- Search Console/Analytics and the who-has-access questions are dropped (Paul).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Paul's phone number and the email the client adds as GBP manager | Paul | Sending the sheet |
| Where the documents Paul already has are stored | Paul | Reconcile |
| Keep "What job do you most want more of?" (on the sheet now) | Paul | proof_sheet_approved |
| "Residential" as a description vs a name variant | Paul | Build (not this sheet) |
| BBB street address (6 Sutton Ct) — to check down the road | Paul / later | Schema / NAP |
| New observations: GAF Certified vs CertainTeed claim · "RBS 57706" may be the licence class · Manta "Established in 2016" | Reconcile / audit | — |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Client proof sheet | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md · https://drive.google.com/file/d/11cC7ZXnisRSNK09Q3Tr1KKhFAkLXPIFB/view | REVIEW |
| CLIENT COPY | https://docs.google.com/document/d/1AU2GdOlZvpjAby3USOBzeQgOcvd5pXGYk0UoPsnO2N0/edit | Paul to check the layout |
| Paul's answers | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | Internal |

**What I could not check**
- Ratings on Yelp, Nextdoor and Apple Maps (blocked or not searchable from the web). Whether the Google Doc renders cleanly — Paul opens it.

**Anything the next agent would otherwise get wrong**
- At reconcile, read Paul's answers file together with the client's returned sheet. Paul's answers cover most of the facts.

## /discovery · 2026-10-07 · run 20261007-144926-discovery-20d6

**What I did**
- The client answered most of the sheet informally through Paul. I saved their words verbatim as evidence: `discovery/Apex Roofing of the Lowcountry - MANUAL - client-answers-informal - 2026-10-07.md`, also in Drive Evidence.
- Cut the client proof sheet to the 8 questions still open: licences current, licence class and holder, email, trip charge, payment methods, titles and certifications, what sets them apart, the job they want more of. Removed the Access block and the phone lines. Re-marked `proof_sheet`; archive-and-replace for the sheet `.md` and the CLIENT COPY in Drive.

**What was decided, and why**
- Paul: "residential" is a description in headings and page text, not a name variant (entity unchanged). No phone line on the sheet.
- The client's answers are not yet recorded as the returned sheet. That happens at sheet-returned, after Paul approves the sheet.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| proof_sheet_approved | Paul | Sending the follow-up; data pulls; recording the returned answers |
| 6 Sutton Ct on the GBP and website? (client wants it; Google's rules for service-area businesses; a storefront would change the area entity) | Paul | Reconcile (Brand Guide approval) |
| Check the CLIENT COPY layout | Paul | Sending |
| New client facts to reconcile: lifetime no-leak workmanship warranty (transferable) · 50-year manufacturer warranty (transferable) · Hearth financing · certified installers for both CertainTeed and GAF · Brays Island and Lobeco (both northern Beaufort County, inside the approved metro area) | Reconcile | — |
| We now have GBP access, so Gwen's dashboard lookups (H-2026-10-05-02 rows 3–5) can be done directly | Gwen | BB-107 |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Proof sheet | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md · https://drive.google.com/file/d/1MRVuiezDpyRafYHUoY3lKdA20kPaGvPe/view | REVIEW |
| CLIENT COPY | https://docs.google.com/document/d/17jqGB3i9Dfk791-_VCboakbX_Z5PM3BaFaR2mtZ8vTA/edit | Ready once Paul approves |
| Client answers (verbatim) | https://drive.google.com/file/d/1QUNMOJpa-7YXgRgWV7lFDAxW6yPZvhBW/view | Evidence |

**What I could not check**
- Brays Island has no Wikipedia article. It is a private community near Sheldon, northern Beaufort County — confirm at reconcile.

**Anything the next agent would otherwise get wrong**
- At sheet-returned, the returned file = the 2026-10-07 informal answers plus whatever the client sends for the 8 follow-up questions. At reconcile, read it together with Paul's answers file.

## /discovery · 2026-10-07 · run 20261007-151404-discovery-f9a6

**What I did**
- Recorded Paul's answers to the 8 follow-up questions in his answers file (Addendum 2026-10-07). The proof sheet itself was not changed and will not be sent.

**What was decided, and why**
- **Address:** option (a). 6 Sutton Ct stays hidden on the GBP (service-area business), and the approved metro area stays the area entity.
- **Licences:** use the evidence we have — #57706 per BBB/GAF ("RBS 57706"); Bluffton #0620033323 per the homepage. Both stay "found" until Gwen's LLR lookup.
- **No public email. No minimum call charge. "Standard" payment methods** (no list to publish).
- **Titles:** none published (sources conflict). The site keeps "Founded by Ralph and Pierce Brehany".
- **What sets them apart:** the client's own words — certified installers for both CertainTeed and GAF, plus the craftsmanship and flashing answer.
- **Job they want more of:** Paul's best guess, residential installation and repair (not confirmed by the client).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| proof_sheet_approved (the sheet is the record of what was asked; not sent) | Paul | Recording the returned answers; data pulls |
| LLR licence lookup + GBP dashboard (H-2026-10-05-02) | Gwen | Verifying licence facts; BB-107 |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Paul's answers | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | Complete |
| Client's answers (verbatim) | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - client-answers-informal - 2026-10-07.md | Complete |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- Nothing more is coming from the client. At sheet-returned, record the client's informal answers (with Paul's answers file alongside) as the returned sheet.

## /discovery · 2026-10-07 · run 20261007-151906-discovery-3a31

**What I did**
- Recorded Paul's confirmation that both licences are current — SC #57706 and Town of Bluffton #0620033323 — in his answers file. The proof sheet was not changed.

**What was decided, and why**
- Paul: "Both licenses are good. 57706 appears on more websites, but both legit."

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Licence class and holder name from the state lookup | Gwen (H-2026-10-05-02) | Schema / licence wording only |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Paul's answers | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | Updated |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- —

## /discovery · 2026-10-07 · run 20261007-152000-discovery-9b0e

**What I did**
- After Paul's `proof_sheet_approved`, saved the client's answers as the returned sheet, unchanged: `discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md` (the 2026-10-07 informal answers). This meets the condition proof_sheet_returned.

**What was decided, and why**
- The sheet was never sent: the client and Paul answered every question directly (2026-10-07). Paul's answers are kept separately in his MANUAL answers file. Both files feed reconcile.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Reconcile the answers into the Brand Guide | Next step (`/discovery reconcile`) | brand_guide_approved |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Returned sheet | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md | Recorded |
| Paul's answers | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | Read at reconcile |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- Reconcile must read Paul's answers file too. The returned sheet holds only the client's own words.

## /drive-mirror · 2026-10-07 · run 20261007-152058-drive-mirror-c605

**What I did**
- Archive-and-replace after Paul's `proof_sheet_approved`. Approval Record, Document Checklist and Handoff Log: each old copy got the `- 2026-10-07` name and moved into `_Archive`; the new version was uploaded under the standard name in the client folder.
- Uploaded the approved proof sheet as a new file, `Apex Roofing of the Lowcountry - Client Proof Sheet - APPROVED.md`, in `01 - Discovery and Audit/Deliverables` (content identical to the approved REVIEW version; size matches).
- Uploaded the returned sheet, `Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md`, in Deliverables. The first upload was one byte short (a trailing blank line was lost), so it was archived as `… - RETURNED - 2026-10-07.md` in `_Archive` and re-uploaded; the current copy matches the local file byte for byte.

**What was decided, and why**
- The Brand Guide was not mirrored: it has not changed since its last upload.
- The REVIEW copy of the proof sheet stays in Deliverables. It moves to `_Archive` only if Paul says so.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Move the proof sheet REVIEW copy to `_Archive`? | Paul | Nothing |
| Reconcile the returned sheet and Paul's answers into the Brand Guide | Next step (`/discovery reconcile`) | brand_guide_approved |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Proof sheet (APPROVED) | https://drive.google.com/file/d/11VXD7vHg63DetZkx8pwfo9JMnTUF91ew/view | Uploaded |
| Returned sheet | https://drive.google.com/file/d/1BgZFVGn5WQIe9Hin1jOn2OQ7P5jAnuN8/view | Uploaded |
| Records in Drive | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Current as of the proof sheet approval |

**What I could not check**
- Byte-for-byte size of the three uploaded records against the local files (not checked; content was pasted from the files unchanged, but a trailing newline may differ by one byte).

**Anything the next agent would otherwise get wrong**
- `_Archive` now holds a `… - RETURNED - 2026-10-07.md`: that is the one-byte-short first upload from this run, not an earlier version of the returned sheet. A second archive of these records today needs `drive.py archive-name --n 2`.

## /crawl · 2026-10-07 · run 20261007-152559-crawl-0206

**What I did**
- Crawled apexroofingtlc.com with DataforSEO OnPage, basic mode, max 1,000 pages, 2,000 ms between hits. Paul confirmed the $0.15 estimate; actual cost $0.15.
- Result: 72 URLs. No duplicate titles, descriptions or content; no redirect chains. 6 non-indexable pages, all by meta tag: two author archives, blog pages 2–4, one category page 2.
- Files in `inputs/crawl/` (git-ignored). Uploaded 12 of 14 to Drive Evidence: changes #72–#83. Recorded S05 done.

**What was decided, and why**
- Basic mode (no JavaScript rendering), per agency-profile. Missing rendered data is never a finding.
- `h2_all` was uploaded wrong (a paste error, 39 bytes off). It was archived as unfaithful (#84, #85) and not re-uploaded.
- `all_inlinks` (331 KB) is too large to paste through the connector, so it was not uploaded.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `h2_all` and `all_inlinks` exist only locally (not in Drive, not in git) | Paul — direct Drive upload needs Google credentials | Nothing for the audit; evidence completeness in Drive |
| Discovery Record REVIEW-style question: archive the proof sheet's REVIEW copy in Deliverables? | Paul | Nothing |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Crawl tables | clients/apex-roofing-of-the-lowcountry/inputs/crawl/ | Complete (local) |
| Crawl config | Drive Evidence: Apex Roofing of the Lowcountry - DFS - crawl-config - 2026-10-07.md | Uploaded |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- The audit reads the local crawl files, not the Drive copies. The Drive CSVs have LF line endings (the local files have CRLF); the content is the same.

## /discovery · 2026-10-07 · run 20261007-154441-discovery-64db

**What I did**
- **Paid pulls (Paul OK'd ≈ $0.68; actual $0.236).**
  - Reviews: 67 reviews, $0.015.
  - Rankings: 41 keywords on 7 URLs, $0.107.
  - Backlinks: 711 referring domains (694 to the homepage), including 2 old URLs, $0.050.
  - People Also Ask: 20 queries, $0.052.
  - Query fan-out: 10 seeds, $0.012.
  - The 4th city is Hardeeville, because DataforSEO has no location for Okatie or Lady's Island.
- **Free steps:**
  - S09 citations skipped (Paul).
  - S10 local grid done: Paul's Local Dominator scans, registered for S10 (commit d0c6425); results in `data/local-grid/local-grid-summary.md`; the reports' advice was not used.
  - S11 skipped (no GSC/GA4, Paul).
  - S20 done (SEOPress settings from /wp-check).
- **System fixes during the run (true blockers; each tested and pushed):**
  - `reviews.py` read 0 of 67 reviews (new DataforSEO label) — fixed (a5c57eb), re-read at no cost.
  - `paa.py` stopped on a temporary DataforSEO error and would have paid twice on a re-run — it now reuses saved queries and retries once (6487a4c).
  - `dfs.balance()` hit DataforSEO's 6-per-minute limit — it now reuses the balance for 60 s, and `fanout.py` reuses saved seeds (990b381).
- **Removed one reviewer's signed name** from `reviews.csv` before commit (review ChZDSUhNMG9n…, now "[reviewer's name removed]").
- **Routing and review themes (Discovery agent):**
  - S06 themes added to `customer-language.md`. 66 five-star and 1 two-star review, so the 5.0 is rounded.
  - S19: 50 PAA questions — 27 service FAQ, 10 blog, 13 drop.
  - S21: 379 fan-out queries — 269 service, 35 location FAQ (Bluffton and Hilton Head Island), 55 blog, 20 drop.
  - All recorded done.

**What was decided, and why**
- Rankings: the two "cannibalization" clusters are the homepage under its `http://www.` and `https://` hosts — a host issue, not two pages. Left for the audit.
- PAA: 6 queries were billed twice. DataforSEO bills failed tasks: 1 from the first stop, plus 5 retries on temporary errors. That added $0.012.
- Residential only: flat-roof and other commercial-leaning queries were dropped. Georgia and out-of-area queries were dropped.
- Review-only claims (10-year warranty, permits, free small fixes) stay out of Brand Guide D (CM-027).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Reviews: a signed name in review text isn't caught by the script (fixed by hand this time) | Next pause (script) | Nothing now |
| PAA / fan-out only used 4 / 2 cities — no city-specific questions for the other location pages | Paul | Site plan FAQ coverage (later) |
| Grid scan centre ("Beaufort") — check the heat-map image before citing any geographic pattern | Audit | Entity findings wording |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Reviews + customer language | clients/apex-roofing-of-the-lowcountry/data/reviews/ | Complete |
| Rankings | clients/apex-roofing-of-the-lowcountry/data/rankings/ | Complete |
| Backlinks | clients/apex-roofing-of-the-lowcountry/data/backlinks/referring-domains-per-url.csv | Complete |
| Local grid | clients/apex-roofing-of-the-lowcountry/data/local-grid/local-grid-summary.md | Complete |
| PAA / fan-out routing | clients/apex-roofing-of-the-lowcountry/data/paa/paa-routing.md · data/fanout/fanout-routing.md | Complete |

**What I could not check**
- The quality of the 711 referring domains (the audit judges it). Whether routed answers are true for Apex — every factual answer waits on Brand Guide D (reconcile).

**Anything the next agent would otherwise get wrong**
- Routing is planning input, not findings. Rows sharing a "merge: …" note are one H2/FAQ (BB-316).
- Head-term rows ("… near me") route to a page because it is their target, not to become FAQs.
- Old URLs with backlinks (/services/synthetic-roofing/, /service-area/hilton-head-island-sc/) matter for CM-019 / redirects.

## /discovery · 2026-10-07 · run 20261007-170552-discovery-4092

**What I did**
- At Paul's request, extended People Also Ask (S19) from 4 towns to all 12: 96 queries (8 services × 12 towns), 140 distinct questions. The 20 earlier queries were reused at no cost.
  - Okatie and Pritchardville were searched from Bluffton.
  - Lady's Island, Fripp Island and Levy were searched from Beaufort.
  - St. Helena Island was searched from "Saint Helena Island".
  - DataforSEO has no location for those five; a new `paa.py --search-from` option handles it (b98efbc, tested).
- Cost **$0.20** (100 calls). About $0.05 of it is failed searches that DataforSEO bills (temporary 40101 server errors; two stops, resumed without re-paying saved queries).
- The Discovery agent routed all 140: 76 service FAQ, 2 location FAQ, 28 blog, 34 drop. The 50 earlier routes were carried over unchanged (copy kept in `paa-routing-first-20-queries.md`). S19 recorded done.

**What was decided, and why**
- No town-specific roofing question came up for any of the 12 towns. The only town-named questions were tourism or trivia, so they were dropped as FAQs (the Hardeeville and St. Helena Island facts may go in page body text).
- Two coastal-material questions became location FAQs: Lady's Island (#109) and Fripp Island (#114). The site plan picks the final page for each.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Location pages get almost no FAQ material from PAA; the 35 fan-out location FAQs cover only Bluffton and Hilton Head Island | Site plan (Build) | Location-page FAQ coverage |
| Re-running `paa.py` wipes earlier routing (carried over by hand this time) | Next pause | Nothing now |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| PAA routing (all 12 towns) | clients/apex-roofing-of-the-lowcountry/data/paa/paa-routing.md | Complete |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- Routed answers about prices, financing, certification, code, tax and insurance need confirmed facts or a cited source before anyone writes them (CM-016).

## /discovery · 2026-10-07 · run 20261007-194242-discovery-9495

**What I did**
- **Audit analysis (S12–S16)**, using the evidence on hand: the S05 crawl (72 URLs), rankings, backlinks, reviews, the local grid, People Also Ask, fan-out and the SEOPress settings. No paid calls.
  - Read the public pages for free (served HTML, no JavaScript) to check text the crawl doesn't carry.
  - Saved those reads as MANUAL evidence in `inputs/live-pages/`.
- **Gate B:** 2 questions, both for Paul. He answered both on 2026-10-07:
  - Q1 = 1a: service titles are `Service Name - Brand` with no area term (DEC-LOCAL-011).
  - Q2 = 2a: the homepage shows all 8 services as H3 links, a Paul Exception (DEC-LOCAL-012).
  - F-014, F-004 and F-023 were superseded to match.
- **S17 fresh-context review:**
  - Of 33 findings: 21 confirmed, 9 revised, 3 withdrawn. F-005 merged into F-004, which is now Medium; F-006 withdrawn; F-013 merged into F-012.
  - Result: 30 active findings — High 3, Medium 17, Low 10.
  - 3 URL Decision Map rows corrected (DEC-LOCAL-013).
- **S18:** rendered the four REVIEW deliverables in `audit/2026-10-07/deliverables/`. All are built from the latest revision of each finding; withdrawn findings are listed as withdrawn.
  - Recommendations and the Evidence Manifest uploaded to Drive Deliverables (changes #112, #113). Byte sizes match.
  - Marked `audit_deliverables`.
- **Conflicts:** recorded the HP-06 wording conflict as CF-LOCAL-002 (PROC-01, not resolved).

**What was decided, and why**
- No URL is a CM-019 candidate: citations were skipped (S09) and the client has not been asked about leads. The Metal Roofing slug change is `Needs Evidence`; the only redirect work is repairing the synthetic-roofing 301 that lands on a 404.
- "The Best" is raised only because no CM-020 decision is recorded. The homepage H1 is locked (BB-313 §3).
- Paul's FAQ note (DEC-LOCAL-004) was applied to the live FAQs (F-021, F-001).
- Brand Guide B2's metro-area sentence is superseded for service pages by DEC-LOCAL-011. `brand-guide.md` was not edited, because B2 is under the entity approval.
- The Finding Register (87 KB) and URL Decision Map (40 KB) were **not** uploaded to Drive. They are too large to paste reliably through the connector; the local files are the record.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `audit_approved` | Paul | Safe fixes; the Low batch |
| HP-06 wording conflict (CF-LOCAL-002) — spec correction | Paul | Future homepage briefs |
| About-page Coastal defaults: "Area Category" meaning, H1 format, owner section | Paul | F-015 H1 part, F-016 severity |
| Client confirmations: Port Royal base housing; synthetic roofing; ShingleMaster; one price range; the other claims in F-002 | client via Paul | Brand Guide D/D2; F-009 target |
| GBP manager access | Paul | F-008 (Gwen) |
| Finding Register + URL Decision Map in Drive | Paul (direct-upload tool) | Drive completeness only |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Finding Register | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Finding Register - REVIEW.md | REVIEW (local only) |
| URL Decision Map | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - URL Decision Map - REVIEW.md | REVIEW (local only) |
| Recommendations | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Recommendations - REVIEW.md | REVIEW · Drive https://drive.google.com/file/d/1d6uL99jW-PCmFPjMDHd6UVFzpE_ZygDl/view |
| Evidence Manifest | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW.md | REVIEW · Drive https://drive.google.com/file/d/1brOXSWq2d-COpf0-HVrzNiJ0FT1HJh8p/view |
| Registers, scorecards, decisions, questions, review | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/ | complete |

**What I could not check**
- Anything JavaScript-loaded: review bar, Maps embeds, city maps, the contact form.
- No GSC, GA4 or call data, so there is no baseline.
- Citations (S09 skipped).
- Neighbourhood names, one by one.

**Anything the next agent would otherwise get wrong**
- Every spec is DRAFT, so the spec-based findings are advisory.
- `findings.csv` is append-only. Always read the latest revision of each finding: F-004 is at rev 3; F-005, F-006 and F-013 are withdrawn.
- Service titles carry no area term (DEC-LOCAL-011), even though Brand Guide B2 still reads otherwise.

## /discovery · 2026-10-08 · run 20261008-073331-discovery-a866

**What I did**
- Applied Paul's 2026-10-08 ruling on the homepage title/H1 to Brand Guide A6, B1 and B2 and the Discovery Record (§3.8). Re-recorded the entity_record files (Discovery Record + `brand-guide.md#A+B1+B2`).

**What was decided, and why**
- **Reserved homepage variant (SEO title):** "Hilton Head Island Metropolitan Area" — Wikipedia's article title, a real name. "Hilton Head Island–Bluffton–Port Royal Metropolitan Area" moves to the pool.
- **Homepage H1:** a familiar pool variant, "Lowcountry" or "South Carolina Lowcountry". Paul: people know it better and it's still accurate. This rules audit conflict CF-LOCAL-002 (HP-06 vs BB-304): reserved variant in the title, pool variant in the H1.
- **B2:** now states the SEO-title rule per page type — homepage takes the reserved variant; service pages `Service Name - Brand` (Gate B 1a); location pages follow the location spec.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Entity re-approval (B1 changed, so the 2026-10-05 approval no longer counts) | Paul | audit_approved, proof-sheet follow-ons |
| Audit deliverables updated to these rulings + the About rulings + 3a | Next run | audit_approved |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide A/B1/B2 | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Revised |
| Discovery Record §3.8 | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | Revised |

**What I could not check**
- —

**Anything the next agent would otherwise get wrong**
- The area entity itself (the MSA) is unchanged. Only which name is reserved for the homepage title changed.

## /discovery · 2026-10-08 · run 20261008-073627-discovery-2c41

**What I did**
- Applied Paul's 2026-10-08 audit-approval rulings to the existing findings. Each change is a superseding row; there are no new findings and no paid calls.
  - **F-004 rev 4:** the homepage title is now a one-word fix, "Metro" → "Metropolitan". The reserved variant is "Hilton Head Island Metropolitan Area". Stays Medium.
  - **F-015 rev 3:** the About page title and H1 follow Paul's ruling. Stays High.
  - **F-016 rev 3:** owners by name only, with a visible placeholder for their photo and job titles. Low → Medium.
- Marked CF-LOCAL-002 as ruled by Paul in `conflicts.csv`.
- Updated the "Paul Decision" cells on the homepage and About rows of the URL Decision Map. The map still has 83 rows.
- Recorded four entries in the audit's decision log:
  - DEC-LOCAL-014: CF-LOCAL-002 ruled, and the homepage H1 preference if it is ever rebuilt.
  - DEC-LOCAL-015: About page.
  - DEC-LOCAL-016: 3a — accepted as advisory while the specs are DRAFT.
  - DEC-LOCAL-017: B2 now aligned with 1a; no new review needed.
- Re-rendered the four REVIEW deliverables from the latest revision of each finding. Re-marked `audit_deliverables` with the four files.
- Archive-and-replace in Drive for the Recommendations (change #117) and the Evidence Manifest (change #119):
  - The old copies were renamed "… - REVIEW - 2026-10-08.md" and moved to `_Archive`.
  - The new copies were uploaded to Deliverables. Byte sizes match the local files.

**What was decided, and why**
- **F-004 stays Medium (CM-028):** the title still fails a spec check (HP-03, the B1 assignment) but does not break the entity model.
- **F-016 goes from Low to Medium:** Paul's ruling removed the "Coastal default — never above Low" condition.
- **Paul's About H1 carries the brand,** which ABT-03 would otherwise fail. His ruling governs for this client.
- **No fresh-context review is needed.** These are Paul's rulings applied to findings the S17 review already checked.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `audit_approved` | Paul | Safe fixes, the Low batch |
| Client confirmations (Port Royal base housing, synthetic roofing, ShingleMaster, one price range, other F-002 claims) | client via Paul | Brand Guide D/D2; F-009 target |
| Specs approved before Build; HP-06 wording correction | Paul | Build |
| Finding Register and URL Decision Map not in Drive (too large to paste) | Paul (direct-upload tool) | Drive completeness only |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Recommendations | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Recommendations - REVIEW.md | REVIEW · Drive https://drive.google.com/file/d/1dVCYpd3KlpBmAWDbHKJWmMgyzZHVzNlG/view |
| Evidence Manifest | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW.md | REVIEW · Drive https://drive.google.com/file/d/1-M0Pzd79LUGQ2wMIs6QFmf565IEnfr3y/view |
| Finding Register / URL Decision Map | same folder | REVIEW, local only |

**What I could not check**
- Nothing new this run. The limits of the 2026-10-07 audit still apply: JavaScript-loaded content, no GSC/GA4, no citations.

**Anything the next agent would otherwise get wrong**
- The reserved homepage variant is now "Hilton Head Island Metropolitan Area".
- "Hilton Head Island–Bluffton–Port Royal Metropolitan Area" is a pool variant; it is what the About title uses.
- The live homepage H1 stays locked.
- Read the latest revision of each finding: F-004 is at rev 4; F-015 and F-016 are at rev 3.

## /drive-mirror · 2026-10-08 · run 20261008-074416-drive-mirror-b726

**What I did**
- Archive-and-replace in the client folder after Paul's entity re-approval and `audit_approved` (2026-10-08). Approval Record, Document Checklist, Brand Guide and Handoff Log: each old copy renamed `… - 2026-10-08.md` and moved into `_Archive`; the current local file uploaded under the standard name.
- Uploaded the approved audit deliverables as new files in `01 - Discovery and Audit/Deliverables`: `Apex Roofing of the Lowcountry - Recommendations - APPROVED.md` and `Apex Roofing of the Lowcountry - Evidence Manifest - APPROVED.md` (content identical to the approved REVIEW files).
- Archive-and-replace for the Discovery Record APPROVED copy in Deliverables: the 2026-10-05 version went to `_Archive` as `… - Discovery Record - APPROVED - 2026-10-08.md`; the re-approved version (with §3.8) is uploaded under the standard name.

**What was decided, and why**
- The Finding Register (87 KB) and URL Decision Map (40 KB) were not uploaded: too large to paste reliably through the connector. The local files are the record.
- The REVIEW copies of the Recommendations and Evidence Manifest stay in Deliverables. They move to `_Archive` only if Paul says so.
- The Handoff Log (about 53 KB) was uploaded in one call rather than skipped; the Discovery Record (31 KB) had just gone up byte-exact.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Finding Register + URL Decision Map in Drive | Paul (direct-upload tool) | Drive completeness only |
| Move the Recommendations and Evidence Manifest REVIEW copies (and the proof sheet REVIEW copy) to `_Archive`? | Paul | Nothing |
| `brand_guide_approved` (reconcile the returned sheet and Paul's answers) | Next step (`/discovery reconcile`), then Paul | Structural changes, discovery sign-off |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Recommendations (APPROVED) | https://drive.google.com/file/d/1d3cHvGIIB9cWe5nkIyOQvbDzll5hdywi/view | Uploaded |
| Evidence Manifest (APPROVED) | https://drive.google.com/file/d/1UHMkUobIeLAI2p6DVfo-WM552kNLWZbK/view | Uploaded |
| Discovery Record (APPROVED, with §3.8) | https://drive.google.com/file/d/1Pmm-Ix7kfWE4MVfcT_vIj-i7cUIKrXoe/view | Uploaded |
| Records + Brand Guide | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Current as of the audit approval |

**What I could not check**
- Byte sizes of the three uploaded record files (Approval Record, Document Checklist, Handoff Log) against the local files — pasted unchanged from the Read output, but not compared (Drive sizes: 2,639 · 6,691 · 53,147). Brand Guide (10,957), Recommendations (14,827), Evidence Manifest (14,829) and Discovery Record (31,439) match the local files byte for byte.

**Anything the next agent would otherwise get wrong**
- The Drive copies of the APPROVED Recommendations and Evidence Manifest still carry "REVIEW" in their first line and status line: they are the approved files unchanged, as the Approval Record lists them. Don't edit them to say APPROVED — that would break the approval's file match.
- `_Archive` now holds one `… - 2026-10-08.md` of each of the four records and of the Discovery Record APPROVED copy; another archive of these today needs `drive.py archive-name --n 2`.

## /discovery · 2026-10-08 · run 20261008-075515-discovery-24a2

**What I did**
- Reconciled the returned proof sheet (client's words, 2026-10-07) and Paul's answers (2026-10-06 + 2026-10-07 addenda) into `clients/apex-roofing-of-the-lowcountry/brand-guide.md`: Section A statuses, Section D (filled, with an Author row), D2 unsupported claims (5), D3 content-risk list (R1–R8), Section E service-area truth, Section G positioning, Section H client constraints, Section I pointer to the customer-language file. Sections B1/B2, C and F not touched.
- Kept every `was:` value in Section A; Unknown / Submitted fields stay so with `[NEED: …]`.
- Marked `reconciled` → `brand-guide.md#A+D+E+G`; re-marked `entity_record` → Discovery Record + `brand-guide.md#A+B1+B2`. Logged change #132.

**What was decided, and why**
- Client's own words → `Client Confirmed 2026-10-07`; Paul's answers → `Paul Approved <date>` (he spoke for the client — not recorded as the client). Paul's "to check", "best guess" and "assume" answers are not confirmations.
- Author (CM-039) = Ralph Brehany, by Paul's direction ("assume father is the owner"), recorded as Paul Approved — the returned sheet names no owner.
- ShingleMaster stays Submitted and goes to D2: the client confirmed "certified factory installers of both CertainTeed and GAF", a different claim.
- Reviews used only for the rating/count (evidence for CM-020) and the Section I pointer (CM-027).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| entity_approved re-approval (Section A statuses changed) | Paul | structural changes, sign-off |
| Street address on the website — yes or no (client named 6 Sutton Ct for GBP + website; Paul chose hidden on the GBP) | Paul | NAP on the site, schema (Finish) |
| Client's "No" to "any travel fee or places you won't go?" — read as no travel fee? | Paul | any "no travel fee" claim |
| ShingleMaster current? (homepage W3) | Paul / client | R4 fix; any ShingleMaster claim |
| Job most wanted (Paul's guess: residential installation and repair) | client via Paul | site-plan priority |
| Licence class + holder name; SOS legal name; GBP secondary categories and Website field | Gwen (manual lookup H-2026-10-05-02) | licence-class claims; schema |
| Brays Island and Lobeco county check (inside the MSA?) | next discovery/build run | "contains all cities served" |
| Not-a-tracking-number confirmation for (843) 757-2739 | Paul / client | nothing now |
| Unconfirmed live claims: W9 communities, W10 photos, W11 rest, W14 40-year panel warranty, W17 paid reports, W18 Velux/FAKRO, W21, W23, W24, W25 | client via Paul | publication of those claims |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide (reconciled A, D, E, G) | clients/apex-roofing-of-the-lowcountry/brand-guide.md | REVIEW — awaits brand_guide_approved + entity_approved re-approval |
| Returned sheet | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md | recorded |
| Paul's answers | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | read |

**What I could not check**
- No paid calls and no live reads this run. Licence class, SOS record and GBP dashboard fields still wait on Gwen's lookup. Counties of Brays Island and Lobeco not checked.

**Anything the next agent would otherwise get wrong**
- "Paul Approved" in Section D is Paul speaking for the client, not the client — and the author (Ralph) is Paul's assumption. Never write "ShingleMaster", "commercial", "businesses", "Coastal Georgia" or "payment arrangements"; use "certified factory installers of both CertainTeed and GAF" and "financing through Hearth". The workmanship warranty now has a confirmed term (lifetime no-leak, transferable) that the live /roof-replacement/ page understates (R6).

## /discovery · 2026-10-08 · run 20261008-080806-discovery-b736

**What I did**
- Applied Paul's four reconcile choices to the Brand Guide (A4, D, D3 R4, E, H). No open-choice markers remain. Re-recorded `reconciled` (`#A+D+E+G`) and `entity_record` (Discovery Record + `#A+B1+B2`).

**What was decided, and why**
- **1a:** the website shows the full street address "6 Sutton Ct, Bluffton, SC 29910"; the GBP address stays hidden (service-area business).
- **2a:** no travel fee — the client's "No" is read as no travel fee.
- **3b:** ask the client whether CertainTeed ShingleMaster is current. It stays off the site until confirmed.
- **4a:** Ralph Brehany stays owner/author on Paul's direction (not client-confirmed).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Ask the client: "Is your CertainTeed ShingleMaster status current?" — one question; Paul sends it | Paul | Using "ShingleMaster" in any copy |
| brand_guide_approved + entity re-approval (Section A statuses changed) | Paul | Structural changes; discovery sign-off |
| Licence class / holder name; GBP secondary categories | Gwen (H-2026-10-05-02) | Licence wording; BB-107 |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Brand Guide (reconciled) | clients/apex-roofing-of-the-lowcountry/brand-guide.md | Ready for approval |

**What I could not check**
- Brays Island's county (no Wikipedia article; near Sheldon, Beaufort County). Lobeco is in Beaufort County per Wikipedia.

**Anything the next agent would otherwise get wrong**
- Website NAP = "Apex Roofing of the Lowcountry · 6 Sutton Ct, Bluffton, SC 29910 · (843) 757-2739"; the GBP shows no street address. That difference is deliberate (SAB), not a NAP inconsistency.

## /discovery · 2026-10-08 · run 20261008-104054-discovery-3010

**What I did**
- Wrote the one-page Discovery Summary and client-confirmation list from decisions.md, the Document Checklist and the approved audit deliverables. No new research and no paid calls.
- Checked the file name with naming.py (deliverable: OK).
- Recorded it as `discovery_summary` with `status.py mark`. No Drive upload; Paul mirrors after the approval.

**What was decided, and why**
- Nothing new was decided. The summary restates the re-approved entity (2026-10-08), the audit counts and Paul's standing decisions.
- The website NAP is shown with the full street address, following reconcile choice 1a. This replaces the older "Bluffton, SC 29910" wording in Recommendation A9.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| discovery_signed_off | Paul | Build start |
| Is CertainTeed ShingleMaster current? (one question) | Paul sends it | Using "ShingleMaster" in any copy |
| Licence class / holder; GBP secondary categories, service areas, open date | Gwen (H-2026-10-05-02) | Licence wording; BB-107 |
| Synthetic roofing offered (and which type)? | Client, through Paul | C1 redirect target (default `/roof-replacement/`) |
| Port Royal base privatized housing / access process | Client, through Paul | Port Royal on-base lines and the MCRD FAQ |
| One roof-replacement price range | Client, through Paul | Any price range in copy |
| The other F-002 claims; Metal Roofing leads | Client, through Paul | Those claims; the F-010 slug change |
| Finding Register and URL Decision Map not in Drive | Paul | Drive completeness only |
| Six page specs still DRAFT | Paul | Build writing each page type |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Summary | clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Summary - REVIEW.md | Ready for approval |
| Recommendations / Evidence Manifest / Finding Register / URL Decision Map | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/ | Approved 2026-10-08 |

**What I could not check**
- The Brand Guide itself was not re-read in this step. The unsupported-claims list comes from F-002 and the Recommendations confirmation list.

**Anything the next agent would otherwise get wrong**
- Severity counts: the S17 step note says Medium 17 / Low 10. The rendered Finding Register says High 3 · Medium 18 · Low 9 (30 active), and the register is the record.
- Service titles have no area term. The homepage title carries "Hilton Head Island Metropolitan Area" in full. The homepage H1 stays locked.

## /drive-mirror · 2026-10-08 · run 20261008-110342-drive-mirror-7c9f

**What I did**
- Resumed this run after an interruption. The earlier attempt had made no changes and touched nothing in Drive (checked: no changes logged; the four records were still in the client folder and no "(2)" archive names existed).
- Archive-and-replace in the client folder after Paul's `brand_guide_approved` and `discovery_signed_off` (2026-10-08). Approval Record, Document Checklist, Brand Guide and Handoff Log: each old copy was renamed `… - 2026-10-08 (2).md` and moved into `_Archive`, and the current local file was uploaded under the standard name (changes #135, #137, #139, #141).
- Uploaded the approved Discovery Summary as a new file, `Apex Roofing of the Lowcountry - Discovery Summary - APPROVED.md`, in `01 - Discovery and Audit/Deliverables` (content identical to the approved REVIEW file; change #142).

**What was decided, and why**
- `--n 2` archive names: this morning's mirror already put a `… - 2026-10-08.md` of each record into `_Archive`.
- The Discovery Record was not re-uploaded: it has not changed since this morning's mirror.
- The Finding Register and URL Decision Map were not uploaded: too large to paste reliably through the connector. They stay repo-only at `clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/`.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Finding Register + URL Decision Map in Drive | Paul (direct-upload tool) | Drive completeness only |
| Move the REVIEW copies (Recommendations, Evidence Manifest, proof sheet) to `_Archive`? | Paul | Nothing |
| Is CertainTeed ShingleMaster current? (one question) | Paul sends it | Using "ShingleMaster" in any copy |
| Six page specs still DRAFT | Paul | Build writing each page type |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Discovery Summary (APPROVED) | https://drive.google.com/file/d/1UPd5Y_FAMeDaqEmy-F48Ic5dyeHnJaHs/view | Uploaded |
| Brand Guide | https://drive.google.com/file/d/1NkHQNyI1s-0SSrSI2ZweyeMFXZlAJMdg/view | Current (approved) |
| Records | https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | Current as of the discovery sign-off |
| Finding Register / URL Decision Map | clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/ | Approved, repo-only |

**What I could not check**
- Byte sizes of the three generated records (Approval Record, Document Checklist, Handoff Log) against the local files: pasted unchanged from the Read output, but not compared (Drive sizes: 2,993 · 6,691 · 64,979). The Brand Guide (26,585) and Discovery Summary (6,900) match the local files byte for byte.

**Anything the next agent would otherwise get wrong**
- The Drive copy of the APPROVED Discovery Summary still says "REVIEW" in its title line and status line: it is the approved file unchanged, as the Approval Record lists it. Don't edit it.
- `_Archive` now holds `… - 2026-10-08.md` and `… - 2026-10-08 (2).md` of each of the four records; another archive of these today needs `drive.py archive-name --n 3`.
- The Drive Handoff Log does not yet include this run's section; it goes up with the next mirror.

## /build:blockers · 2026-10-08 · run 20261008-131822-build:blockers-b359

**What I did**
- Wrote the Technical Blocker Checklist from the approved Finding Register (CM-028) and marked it (`blocker_checklist`).
- Issued 5 blocker handoffs to Jonie (`--blockers`), 46 rows in all: H-2026-10-08-03-redirect (2, F-009), H-2026-10-08-04-broken_link (26, F-030), H-2026-10-08-05-sitemap (9, F-031), H-2026-10-08-06-seo_title (7 utility titles, F-003 + F-027), H-2026-10-08-07-other (2: footer brand text F-003, contact H3 → H2 F-025). Every row is logged by handoff.py.
- Paul chose (b) for the open title question: issued H-2026-10-08-08-seo_title (9 rows: 8 service titles `Service Name - Apex Roofing of the Lowcountry`, F-014; /about/ title per the settled `about_page`, F-015) and H-2026-10-08-09-h1 (1 row: /about/ H1 "About Us" → "About Apex Roofing of the Lowcountry", F-015). Two handoffs because handoff.py issues one per change kind (seo_title, h1). Not flagged `--blockers`.

**What was decided, and why**
- The 3 High findings (F-014, F-015, F-022) are on-page structure; none blocks crawling, indexing or measurement, so they are fixed in the rebuilt pages, not in the blocker batch.
- F-009 redirects use the approved default target /roof-replacement/ (the open client question can re-point them later).
- /about/ title left out of the utility-title row set; it is in H-2026-10-08-08 instead (Paul's choice b).
- The interim service titles use the current service names; if the site plan picks a different keyword for a page, its rebuilt draft carries the new title.
- F-033 alt text stays a system safe fix (cap 5); F-008 is GBP (Gwen) and waits on access; archive and blog items wait for the Blog Decision Map.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| 5 blocker handoffs returned and `/verify` passed | Jonie, then `/verify` | blockers_cleared |
| H-2026-10-08-08-seo_title and H-2026-10-08-09-h1 returned and `/verify` passed | Jonie, then `/verify` | nothing (not blockers) |
| synthetic_roofing_offered (client) | Client via Paul | F-009 target only |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Technical Blocker Checklist | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Technical Blocker Checklist - REVIEW.md | marked |
| Handoffs | clients/apex-roofing-of-the-lowcountry/handoffs/H-2026-10-08-03 … 09 (.md + .csv) | issued |

**What I could not check**
- Live values were not re-read today; row `old` values are from the 2026-10-07 crawl and captures. Jonie checks each before changing it.

**Anything the next agent would otherwise get wrong**
- The Technical Blocker Checklist (marked file) still lists the service/About retitle as an open choice; it was not edited after marking. Paul's choice (b) is in the run decision and handoffs 08-09.
- F-031 and F-030 counts in the register (11 sitemap URLs, 10 in-post links) differ from the evidence (9 and 12); the handoffs follow the evidence. The site plan (`/build plan`) can run side by side — it does not wait on blockers_cleared.

## /build:plan · 2026-10-08 · run 20261008-134424-build:plan-c61b

**What I did**
- Wrote the site plan for all 20 money pages (8 service, 12 location) plus homepage and About in the last batch: keyword, title, H1 decision with the CM-020 four-condition test, area/category variant, FAQ topics with a reason each, link targets, and the routed-row coverage check.
- Registered it with `status.py plan` (Site Plan - REVIEW.md + build/site-plan.json): 7 batches — pilot (Roof Repair + Bluffton), s1, s2, l1, l2, l3, h1.
- Recorded 20 CM-020 rows in Brand Guide H2 (proposed, pending site_plan approval) and the decision in the URL Decision Map working CSV; logged 40 keyword/H1 changes (kind site_plan).
- Applied Paul's five answers (2026-10-08): homepage keyword → 'roofing company hilton head island metro area'; permit FAQs on Bluffton and Ridgeland only (HHI, Okatie, Pritchardville dropped); ran the CM-020 SERP re-test (3 reads, $0.006); 'Residential Roofer' approved for use; 18 location FAQ gaps go to the facts interview at each evidence step. Re-registered the plan; logged changes #248–#254 and settled `site_plan_open_choices` and `cm020_serp_retest_2026_10_08`.

**What was decided, and why**
- No page gets "The Best". The SERP re-test measured condition 2 for the only three pages that pass demand (roof repair 1/10 'best' titles, roof replacement 2/10, skylights 2/10 — only directory lists, Apex not in the top 10): it fails on all three. No top-3 locks. Re-test after launch.
- Service H1s use 'South Carolina Lowcountry' or 'Beaufort and Jasper Counties' — the MSA variant contains city names (SVC-12) and 'Lowcountry' is in every service title through the brand. Location H1s: 'Roofers in/on [City]'.
- Roof Replacement owns every new-roof cost question; Roof Installation is new construction (W16). Repair = scheduled repair; Emergency = storm/active-leak response.
- Generic town questions moved to service pages, homepage FAQ (free estimates, financing, licence) or the blog list (C8, F-021); HHI permit rows FO #275, #307 → blog list.
- Brand Guide A3 was **not** edited for 'Residential Roofer': A3 is inside entity_approved (A+B1+B2) and brand_guide_approved (A+D+E+G), so the edit would void both. (The request named B2; B2 is the area pool, also inside entity_approved.) Asked once as `residential_roofer_a3_write`.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| 'Residential Roofer' into A3: (i) write now + re-approve `entity_approved brand_guide_approved` with site_plan, or (ii) write at the next Brand Guide revision | Paul | nothing (the plan can be approved either way) |
| Levy's county (inventory: Beaufort; plan: Jasper) | evidence step (l3) | Levy's batch |
| 18 location FAQ gaps (Pritchardville 3, Levy 3, Okatie/Lady's Island/St. Helena/Hardeeville 2, HHI/Beaufort/Port Royal/Ridgeland 1) | facts interview at each location batch | those pages warn at the evidence gate |
| Gated-community, base-housing and skylight-repair FAQs are conditional on client facts | client via Paul / facts interview | those FAQs only |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Site Plan | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Site Plan - REVIEW.md | awaiting Paul (site_plan) |
| Plan JSON | clients/apex-roofing-of-the-lowcountry/build/site-plan.json | re-registered |
| Brand Guide H2 | clients/apex-roofing-of-the-lowcountry/brand-guide.md | 20 proposed rows; 3 updated with the SERP result |
| SERP raw | clients/apex-roofing-of-the-lowcountry/data/rankings/raw/cm020-best-*-near-hilton-head-sc.json | saved |

**What I could not check**
- Search volume for the location/service main keywords (only ranked keywords were pulled), including the new homepage keyword.
- Positions 11–20 for the three 'best' queries (top 10 only read); url-rankings.csv shows no top-100 ranking for any service page.
- Any local fact behind the town FAQ topics (permits, historic districts, POA rules) — every one is marked "answer needs a cited source" for the evidence step.

**Anything the next agent would otherwise get wrong**
- The approved URL Decision Map .md was deliberately not edited (it would void audit_approved); the CM-020 note and the homepage keyword are in the CSV only.
- The homepage ranks #1 for 'roofing company bluffton sc' — do not write the Bluffton page to chase that query.
- Never use '24 hour', 'certified inspection' or tarping wording; no response time anywhere.
- Only Bluffton and Ridgeland carry a permit FAQ; do not add one to another town page.

## /build · 2026-10-08 · run 20261008-143018-build-a144

**What I did**
- Evidence gate (CM-041) for batch pilot. Wrote the page facts files `build/evidence/svc-roof-repair.facts.json` and `build/evidence/loc-bluffton.facts.json`, using only the returned proof sheet, Paul's answers, the Discovery Record, Brand Guide A/D/E, and Wikipedia (Bluffton, Sun City Hilton Head, both read 2026-10-08).
- Ran `evidence.py run --batch pilot`. The recorded result is **BLOCK** for both pages. Grids: `build/evidence/svc-roof-repair.grid.md` and `build/evidence/loc-bluffton.grid.md`.

| Page | Spec type | Recorded | Corrected reading |
|---|---|---|---|
| svc-roof-repair | service | BLOCK (known 1 / unknown 2 / unverified 9) | WARN: required gap service scope; supporting gaps timeframe, pricing, guarantees |
| loc-bluffton | location | BLOCK (known 4 / unverified 6) | WARN: required gap neighborhoods (5 of 6 verified); supporting gap response time |

**What was decided, and why**
- The recorded BLOCKs are mostly caused by the script, not by missing facts. `evidence.py mark()` accepts a status only when the whole cell is one bare word (`paul approved`). Every Brand Guide A/D status cell has dates and qualifiers added, for example "Paul Approved 2026-10-06 · was: Submitted". Because of that, Phone, Free estimate, Warranty, Insurance, Certifications, Rating and Emergency all show as Unverified. "Unknown — do not state…" shows as Unverified rather than Unknown.
- I did not edit the script (that is a system change, which needs tests in an Opus system session) or the Brand Guide (editing it would void entity_approved and brand_guide_approved). Nothing was waived. The decision is logged in this run.
- Roof repair scope: the only source is the live page's H3 list (Submitted), so it stays Unverified. Roof repair process: the client's own words on flashing, wood rot and sealed valleys (Client Confirmed 2026-10-07).
- Bluffton neighborhoods: Wikipedia confirms 5 districts (Old Town, Palmetto Bluff, Jones Estate, Buckwalter, Shultz Tract). Belfair and Colleton River come only from site claim W9 (Submitted). Sun City Hilton Head is excluded because Wikipedia places it in Okatie.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Fix the evidence.py status parser (use the leading status word; treat a leading "Unknown" as Unknown), with a test, in a system session | Paul (system session) | Correct gate results for every batch |
| Roof repair scope: confirm the repair types (shingle, flashing, ridge cap/starter, soffit/fascia/deck, storm damage) | Client via facts interview | svc-roof-repair brief (required gap) |
| A 6th real Bluffton neighborhood (Belfair? Colleton River? Hampton Hall?) | Client via facts interview, or public source | loc-bluffton brief (required gap) |
| Repair timeframe, repair cost drivers | Client via facts interview | Supporting gaps only |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Facts files | clients/apex-roofing-of-the-lowcountry/build/evidence/*.facts.json | written |
| Evidence grids | clients/apex-roofing-of-the-lowcountry/build/evidence/*.grid.md | BLOCK (recorded) |

**What I could not check**
- Whether Belfair and Colleton River Plantation are inside the Town of Bluffton (no public source was read).

**Anything the next agent would otherwise get wrong**
- Do not "fix" the BLOCK by rewriting Brand Guide status cells. That voids two approvals. The parser is what is wrong. After it is fixed, re-run `evidence.py run --batch pilot`; both pages should come out WARN, and the briefs then need an `## Evidence gaps` section.

## /build · 2026-10-08 · run 20261008-150539-build-a2ae

**What I did**
- Wrote the pilot service brief for Roof Repair (`svc-roof-repair`), one page in this run (CM-043), from the approved site plan, the service spec, Brand Guide A–I, the evidence grid, customer language, PAA and fan-out routing and the audit findings for /roof-repair/.
- Recorded it with `status.py page-stage … --stage brief` (accepted; the brief carries the required `## Evidence gaps` section because the page cleared the gate on Paul's waiver).

**What was decided, and why**
- H1 "Roof Leak and Damage Repair in the South Carolina Lowcountry", no "The Best" (site plan / BG-H2; CM-020 condition 2 failed on the 2026-10-08 SERP re-test).
- Variant chain set so nothing repeats at consecutive elements: first H2 uses "Beaufort and Jasper Counties", the opening uses the metro-area variant (body only), the FAQ H2 uses "Lowcountry" + "Roofer". "Residential Roofer" is not used here while its A3 write is still an open question.
- Buyer state for the opening: a non-emergency slow leak or visible damage, with a homeowner who wants an honest fix (the emergency page owns active and storm leaks, D-4).
- The six repair-type H3s come from the live page list. They are Submitted, so each is marked [NEED] and blocks publication. Hail is kept only if the client confirms it.
- The waiver's "industry standards + competitor research" is applied narrowly. No competitor research was done (it is outside the read list, and competitor claims are never Apex facts, CM-016). General industry knowledge is used only to explain, never to state what Apex does.
- The file is named by the naming convention (`SB - Roof Repair - Apex Roofing of the Lowcountry.md`), not `svc-roof-repair.brief.md` as the caller asked.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| The 25% rule FAQ needs a cited code source; the rule may be Florida's, not South Carolina's. Cite it, explain it without claiming it applies, or drop it | Paul | FAQ 1 in the draft |
| Facts interview: repair types (incl. hail), repair visit length, cost drivers or a range, repair warranty term, W10 photos / W25 owner on the roof | Client via Paul (CM-042) | Publication (the draft carries [NEED]) |
| evidence.py status-parser bug (carried over) | Paul (system session) | Correct gate results for later batches |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Roof Repair brief | clients/apex-roofing-of-the-lowcountry/build/pilot/SB - Roof Repair - Apex Roofing of the Lowcountry.md | recorded, awaits the batch pilot briefs approval |
| Evidence grid | clients/apex-roofing-of-the-lowcountry/build/evidence/svc-roof-repair.grid.md | BLOCK, waived by Paul |

**What I could not check**
- Whether South Carolina's adopted residential code, Beaufort County or Jasper County has a 25% re-roof rule (no source was read).
- Whether the client's lifetime no-leak warranty covers repairs.

**Anything the next agent would otherwise get wrong**
- The Bluffton brief is next, in its own run. Paul's waiver does not make Submitted facts publishable: repair types, W10 and W25 stay [NEED] in the draft. Never attach the lifetime warranty to a repair, and never echo the reviews' "10 year" warranty.

## /build · 2026-10-08 · run 20261008-222200-build-f8f3

**What I did**
- Wrote the Bluffton location brief (pilot, one page per run, CM-043) from the approved site plan, the location spec, Brand Guide A–I, the evidence grid and facts file, customer language, the fan-out routing (no PAA rows route to Bluffton), the sibling Roof Repair brief and the audit findings for /bluffton/.
- Recorded it: `status.py page-stage … loc-bluffton --stage brief` → "brief recorded · batch briefs collected" (both pilot briefs are now in for Paul's one approval).

**What was decided, and why**
- H1 "Roofers in Bluffton", no "The Best" (CM-020 condition 1 fails; BG-H2). First H2 must not use "Roofers".
- Paul's evidence waiver applied narrowly: no response time and no competitor claims (CM-016; BG-D Guarantees Unknown). FAQ 4 uses the client's own "always on call … high priority".
- Neighborhoods: only the 5 Wikipedia-verified names; the 6th is [NEED] (LOC-15 fails until sourced).
- CTA NAP shows the street address (Paul 2026-10-08, BG-A4), superseding F-020's older recommendation.
- File named LB (brief), not LD (reserved for the approved draft).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Sixth Bluffton neighborhood with a public source | Paul / facts interview | LOC-15 on the draft |
| Town of Bluffton permit source (FAQ 1) and Old Town design-guideline source (FAQ 2) | drafter (cite) or Paul | LOC-14 (needs 3 answerable FAQs) |
| Client confirms work in Palmetto Bluff / Belfair / gated communities (W9) | Client via Paul | FAQ 3 publication |
| Brand Guide F (confirmed NAP) empty | Paul | LOC-19 check at Finish |
| Residential Roofer A3 write (`residential_roofer_a3_write`) | Paul | use of that variant |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Bluffton brief | clients/apex-roofing-of-the-lowcountry/build/pilot/LB - Bluffton - Apex Roofing of the Lowcountry.md | recorded, awaiting batch:pilot:briefs |
| Roof Repair brief | clients/apex-roofing-of-the-lowcountry/build/pilot/SB - Roof Repair - Apex Roofing of the Lowcountry.md | recorded, awaiting batch:pilot:briefs |
| Evidence grid | clients/apex-roofing-of-the-lowcountry/build/evidence/loc-bluffton.grid.md | BLOCK, waived by Paul |

**What I could not check**
- Whether Belfair, Colleton River Plantation, Moss Creek or Hampton Hall lie in Bluffton (no public source read in this step).
- The Town of Bluffton permit and Old Town historic-district rules (no official source in the read list).

**Anything the next agent would otherwise get wrong**
- Do not write a response time, a "first response" claim or anything a competitor says, even though the waiver text mentions them. Do not explain services on this page (link table only). Do not repeat Old Town in Things to Do; it is a Top Site and a neighborhood. Keep "roofing company" out of the H tags (the homepage holds #1 for it).

## /build · 2026-10-09 · run 20261009-122305-build-e8c2

**What I did**
- Wrote the pilot service draft for `svc-roof-repair` from the approved brief (SB - Roof Repair), one page in this run (CM-043), and recorded it: `status.py page-stage … --stage draft`.
- Stages 0–2 per writing-commercial.md; Stage 3 self-critique below. No sibling drafts exist yet (loc-bluffton not drafted); no earlier approved pages.

**Stage 3 self-critique (E1–E10)**
- E1 portability: PASS — the opening buyer state (slow leak / not an emergency / not sold a new roof), the client's flashing quote, the CertainTeed + GAF match, and the no-minimum / no-travel-fee facts tie the copy to Apex and to repair. The "signs" and "Lowcountry weather" paragraphs are the most portable; the weather one is anchored by salt air and the roof types named. Batch review should re-test against Emergency and Replacement when drafted.
- E2 specificity: PASS — 6 page-specific verifiable facts: CertainTeed + GAF factory installers (Client Confirmed); flashing method in the client's words (BG-G); no minimum call charge + no travel fee (Paul Approved); SC #57706 + Town of Bluffton #0620033323 (Paul Approved); GL + workers' comp insurance (Paul Approved); Ralph and son Pierce (Client Confirmed); emergency high priority (Client Confirmed).
- E3 variants: PASS — URL roof repair → title Roof Repair → H1 "Roof Leak and Damage Repair" / South Carolina Lowcountry → first H2 "Fix a Damaged Roof" / Beaufort and Jasper Counties / Roofers. Opening uses the third set (roof repairs / metro area / roofing contractor). FAQ H2: Lowcountry + Roofer. Reserved B1 variant unused. "Residential Roofer" not used.
- E4 chunk lengths: PASS — delivery 369, types 262, FAQ 366, areas+CTA 60 words (NEED text excluded).
- E5 invention: PASS with NEEDs — every Apex fact traces to BG-D/G. W10 photos, W25 Ralph-or-Pierce-on-the-roof, W11 flashing/underlayment, all six repair types, repair warranty, 25% rule source, visit length carry `[NEED]`. Brief §2 #6 listed repair timeframes (1–4 hours, half day, 1–2+ days) — **not used**: the brief's own Evidence gaps mark job duration Unknown, so stating them would be invention. CM-049: "emergency" appears only with the Client Confirmed on-call fact; no response time.
- E6 filler: PASS — no A6 phrases; cost answer names the drivers, not a non-answer.
- E7 headers: PASS — one H1; every H2 a question; H2→H3 only; no city in any H tag. COM-11: title remainder "Roof Repair" vs H1 remainder "Roof Leak and Damage Repair" — differs, pass. Note: "Beaufort and Jasper Counties" contains the county name Beaufort (also a served city) — used as the county variant per the approved brief; flag for Paul if he reads SVC-12 strictly.
- E8 links: PASS — no link anywhere in prose/FAQ/opening; placeholder row present. **Deviation:** the brief's FAQ 6 said "link to D-4"; a link in an FAQ answer breaks CM-005 / SVC-17 / COM-09, so the answer distinguishes emergency from scheduled repair in words only. A contextual link to Emergency Roof Repair can be proposed in Finish as a CM-022 exception.
- E9 human check: PASS — reads as a roofer explaining the job; the trade terms (flashing, pipe boot, step flashing, starter strip) are explained in the next clause.
- E10 reading level: PASS — readability.py page grade 5.6, no paragraph over 10 after splitting three long sentences (signs, types intro, 25% rule). FAQ answers checked against C7: sentence one answers; no phone as answer; no link.
- Spec checks SVC-03–22: 03/04 pass (title) · 05/06/07 pass · 08 pass (COM-11) · 09 pass (no "The Best", matches BG-H2) · 10 n/a (not top 3) · 11 pass · 12 pass (see county note) · 13 pass (no H tag, 82 words, phone + free estimate, first sentence answers, own buyer state) · 14 pass (delivery → types → FAQ → areas → CTA, CTA no H tag) · 15 pass (6 FAQs; C3 empty) · 16 placeholder (Finish fills) · 17 pass · 18 pass · 19 pass (nothing from D2; no review wording echoed: no "10 year", "tarps", "permits") · 20 pass · 21 pass (none placed; Finish candidate = 25% rule code source) · 22 n/a (no schema written).

**What was decided, and why**
- Self-critique kept out of the SD file: publish.py turns the whole body into WordPress blocks, so any report text inside the page file would be published.
- FAQ 4 (repair in a day) kept with `[NEED]`: general answer only; drop it if the facts interview gives no visit length (5 FAQs remain).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Six repair types incl. hail confirmed | Client via Paul (facts interview) | publication |
| Typical repair visit length | Client via Paul | FAQ 4 |
| Warranty on a repair (reviews say 10 years) | Client via Paul | the warranty line in the delivery H2 |
| W10 photos, W25 owner on the roof, W11 flashing/underlayment | Client via Paul | publication |
| 25% rule — SC code source, or keep the general answer | Paul | FAQ 1 |
| FAQ 6 link to Emergency page — Finish exception or none | Paul (Finish) | nothing now |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Roof repair draft | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | draft recorded |
| Bluffton brief (next draft) | clients/apex-roofing-of-the-lowcountry/build/pilot/LB - Bluffton - Apex Roofing of the Lowcountry.md | approved |

**What I could not check**
- Whether South Carolina's adopted code has a 25% roofing rule (outside this step's read list; no research done).

**Anything the next agent would otherwise get wrong**
- Do not copy the brief's repair timeframes into any page — they are unsourced. Do not add a link inside FAQ answers even when a brief asks for one.

## /build · 2026-10-09 · run 20261009-123816-build-2c02

**What I did**
- Wrote the pilot location draft for `loc-bluffton` from the approved brief (LB - Bluffton), one page in this run (CM-043), and recorded it: `status.py page-stage … loc-bluffton --stage draft`.
- Route A: status.json `client.route` is unset; the Paul-approved brief states Route A (logged as a decision).
- Sibling context read: SD - Roof Repair (pilot). No earlier approved pages. Bluffton's opening angle (home base / local roofer, owners near and away), headings and FAQs do not reuse Roof Repair's.
- Per Paul's waiver ("verify during drafting") I read the Town of Bluffton forms page for FAQ 1 and searched for the Old Town material rules for FAQ 2 (primary UDO text not readable — left as `[NEED]`).
- Word count about 840 including markers (under the 1,000 ceiling).

**Stage 3 self-critique (E1–E10)**
- E1 portability: PASS — the opening (based in Bluffton, Town of Bluffton licence #0620033323, out-of-town owners), local context (May River, New River, Old Town 1996, 1,275 → 27,716 people) and FAQ 1 (the Town's own re-roof permit forms) cannot move to Okatie, Pritchardville or Hilton Head Island. Most portable line: FAQ 3's "ask your property owners' association" sentence — re-test in the batch reviews against Hilton Head Island.
- E2 specificity: PASS — 7 city-specific verifiable facts: based in Bluffton (BG-A4); Town licence (BG-D); May/New River; Old Town National Historic District 1996, 46 contributing buildings; population growth; Town re-roof permit forms (townofbluffton.sc.gov, read 2026-10-09); Church of the Cross 1854–1857 / Heyward House 1998 / Oyster Company 1899.
- E3 variants: PASS — title Roofing Contractor → H1 Roofers → first H2 Roofing Contractor (not consecutive with the title) → FAQ H2 Roofer. Opening third set: roofer / roofing contractor + Bluffton, SC / Beaufort County. Sibling H2 uses B2 #2 "Lowcountry"; body uses B2 #4. Reserved B1 variant unused; "Residential Roofer" not used.
- E4 chunk lengths: PASS — longest H2 section (FAQ) about 330 words incl. markers.
- E5 invention: PASS with NEEDs — every Apex fact traces to BG-A/D; place facts to the brief's Wikipedia read or the Town forms page. CM-049: no keyword-borne claim; no response time; "always on call" is the client's Client Confirmed wording.
- E6 filler: PASS — no A6 phrases.
- E7 headers: PASS — one H1; every H2 a spoken question with an entity; H2→H3 only. COM-11: title remainder "Roofing Contractor" vs H1 remainder "Roofers" — differs, pass.
- E8 links: PASS — no link in prose, FAQ or local context; both placeholder rows present; no outbound link placed (Finish candidates: the Town forms page for FAQ 1, the UDO for FAQ 2).
- E9 human check: PASS.
- E10 reading level: PASS — readability.py page grade 7.0, no paragraph over 10 (highest 9.1, the FAQ 3 answer). C7: sentence one answers each FAQ; no phone as answer; FAQ 2 informational, no company sentence.
- Spec checks: LOC-01–13 pass (LOC-08 n/a) · LOC-14 4 questions, but FAQ 2 and FAQ 3 rest on `[NEED]` — publication-blocked · **LOC-15 FAIL (5 of 6 neighborhoods)** · LOC-16 map placeholder (Jonie embeds) · LOC-17 pass · LOC-18 placeholder (Finish) · **LOC-19 open** — CTA uses BG-A1/A4/A8; BG-F empty so the exact-match check cannot run · LOC-20–25 pass · LOC-26 no schema written (WebPage + ItemList recommendation stands) · LOC-27 n/a.

**What was decided, and why**
- Route A applied (brief says Route A; client.route unset).
- FAQ 3 heading drops "Belfair" (not publicly placed in Bluffton); Belfair stays in the W9 `[NEED]` marker.
- FAQ 1 sourced from the Town forms page; whether Apex pulls the permit stays `[NEED]`.
- The self-critique is kept out of the LD file (publish.py would publish it).

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Sixth Bluffton neighborhood with a public source | Paul / research or facts interview | LOC-15, publication |
| Does Apex pull the Town of Bluffton re-roof permit? | Client via Paul | FAQ 1 second sentence |
| Old Town: COFA needed for a re-roof (UDO §3.18) and the Article 5 roof-material list | Research (Town UDO) | FAQ 2, publication |
| W9 work in Palmetto Bluff / Belfair / Colleton River / Moss Creek | Client via Paul | FAQ 3, publication |
| Brand Guide F (NAP) empty | Paul (before Finish) | LOC-19 |
| client.route unset in status.json | Paul | nothing now |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Bluffton draft | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | draft recorded |
| Roof Repair draft (sibling) | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | draft recorded |

**What I could not check**
- The text of the Town of Bluffton UDO (§3.18, Article 5) and the two Town PDFs (no PDF reader available) — only the Town's forms page was read directly.
- That Church of the Cross and Heyward House sit inside Old Town (not claimed on the page).

**Anything the next agent would otherwise get wrong**
- Both pilot drafts are written; the next step is the pilot batch review (`/build <slug> batch pilot drafts`), one run with both drafts side by side and the Stage 4 semantic table. FAQ 1 here (Beaufort County permit owner) must stay distinct from Ridgeland's Jasper County permit FAQ later.

## /build · 2026-10-09 · run 20261009-124809-build-ab2d

**What I did**
- Batch review for the pilot: read the Roof Repair service draft (SD) and the Bluffton location draft (LD) side by side, each written in its own run (CM-043).
- Sibling check (CM-017 as scoped by CM-043): no FAQ or heading collision between the two pages; buyer states in the openings differ; one near-identical on-call sentence on both pages; one region-level climate sentence on LD.
- Wrote the semantic review table (report only, drafts unchanged): `build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md`, 11 numbered rows.
- Recorded the batch as drafts_written with the table (`status.py batch ... --sem-findings 11`).

**What was decided, and why**
- SEM-1 to SEM-7 are undefined in writing-commercial.md, so findings are tagged SEM-8 where it applies and otherwise with the standard check that caught them (E1, C7, A7, BB-310). Logged as a run decision.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Pick SEM items 1–11 (or none) and approve the pilot drafts | Paul | apply-sem / ship for pilot |
| 12 NEED items on svc-roof-repair (W25, W10, W11, repair warranty, 6 repair types, 25% rule SC source, visit length) | Client via Paul | ship of svc-roof-repair |
| 5 NEED items on loc-bluffton (permit pulled by Apex, UDO §3.18, UDO Art. 5, W9 gated communities, 6th neighborhood) | Client via Paul / research | ship of loc-bluffton |
| SEM-1–SEM-7 definitions (from the live gem, Section G) | Paul | complete Stage 4 checks |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Semantic review table | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md | REVIEW |
| Service draft | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | awaiting approval |
| Location draft | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | awaiting approval |

**What I could not check**
- SEM-1 to SEM-7 (no definitions). Readability (E10) was not re-run; that belongs to each page's draft run.

**Anything the next agent would otherwise get wrong**
- Row 1 routes the emergency FAQ to the Emergency Roof Repair page and row 6 drops the flashing FAQ; if Paul picks both, SD keeps 4 FAQs (still within 4–6). Row 4 sets a city-bearing sibling-cities H2 pattern for all location batches — carry it into the pilot corrections if Paul picks it.

## /build · 2026-10-09 · run 20261009-130919-build-89b2

**What I did**
- Re-issued the pilot semantic review table: the 11 rows of run 20261009-124809-build-ab2d consolidated into SEM-1 to SEM-8 (the set approve.py accepts), with Paul's 2026-10-09 answers built into each action. Report only; neither draft changed.
- Re-registered the batch: `status.py batch apex-roofing-of-the-lowcountry pilot --state drafts_written --sem-findings 8` with the re-issued table.
- Logged Paul's answers (one decision), settled W25 (`w25_who_goes_on_the_roof`: Ralph and Pierce both get on the roof), and asked one question (`pilot_emergency_faq_link_cm022`).

**What was decided, and why**
- Row map: 1→SEM-1 · 2,8→SEM-2 · 6,7→SEM-3 · 9→SEM-4 · 10→SEM-5 · 3,5→SEM-6 · 4→SEM-7 · 11→SEM-8 (grouped by page and kind of fix).
- SEM-2: because SEM-1 keeps the emergency FAQ on Roof Repair, the on-call sentence stays on Roof Repair only; Bluffton gets its own next step.
- SEM-6: the climate sentence is localized with the facts already sourced in the Bluffton brief (May River, New River, ~20 ft), so nothing new is invented.
- Bluffton cut-down (Paul accepted the depth complaint) is recorded as a draft revision, not a SEM item.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| SEM-1 link to /emergency-roof-repair/ is an in-prose link: CM-022/CM-005 say Build leaves a placeholder and Finish proposes it as the page's one exception | Paul | The live link (not the drafts approval) |
| Bluffton draft cut-down | Paul / Build | Bluffton draft revision |
| Remaining [NEED]s (SD 11, LD 5) | Client via Paul | Ship |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Semantic review (8 SEM items) | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md | Ready for Paul with the drafts |
| SD Roof Repair | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | Unchanged |
| LD Bluffton | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | Unchanged |

**What I could not check**
- SEM-1 to SEM-7 as checks still have no definition in writing-commercial.md; not run.

**Anything the next agent would otherwise get wrong**
- Paul's picks are SEM numbers 1–8 from the re-issued table, not the old row numbers. In apply-sem: SEM-4 removes only the W25 [NEED]; SEM-5 removes hail from Roof Repair and routes it to the Emergency Roof Repair brief; SEM-1 keeps the FAQ and does not place a live link.

## /build · 2026-10-09 · run 20261009-131416-build-ec1c

**What I did**
- Applied the eight SEM items Paul picked (SEM-1 to SEM-8) to the two pilot drafts, exactly as the re-issued Semantic Review table's actions say.
- Roof Repair (SD): SEM-1 emergency-leak FAQ kept, with a link placeholder to /emergency-roof-repair/ (no link placed); SEM-2 opening first sentence and CTA reworded, on-call sentence kept here only; SEM-3 flashing FAQ dropped (5 FAQs), Roof Leak Repair lead sentence replaced; SEM-4 founder line now "Ralph and Pierce both get on the roof", W25 [NEED] removed; SEM-5 Hail Damage Repair H3 and "hail damage" in the lead list removed (5 repair-type H3s).
- Bluffton (LD): SEM-2 opening reworded, on-call sentence removed, own CTA form; SEM-6 FAQ "based in Bluffton" answers with the address and no travel fee, no licence repeat, plus a Bluffton next step; climate sentence tied to May River, New River and ~20 ft elevation; SEM-7 sibling H2 is now "Which Towns Near Bluffton Do We Also Serve?"; SEM-8 "each with its own page" dropped.
- Paul's depth cut on Bluffton: permit-forms list, generic climate line and repeated FAQ text removed, lead sentences shortened. Body 834 -> 788 words. No spec section dropped, no fact added.
- Re-ran E1-E10 and the service/location spec checks on every changed section: all pass. readability.py: SD grade 5.8, LD grade 6.4, no paragraph over 10.
- Logged changes #326 (SD) and #327 (LD); batch pilot recorded as sem_applied with checks passed.

**What was decided, and why**
- SEM-5 hail/storm repair routed to the svc-emergency-roof-repair brief (later batch); still needs the client's confirmation of hail repair.
- Bluffton cut kept every element location.md §3 requires (services table, local context, 3-4 FAQs, neighborhoods, map, Things to Do, Top Sites, siblings, CTA); the remaining length is spec-required.
- SEM-1 link stays a placeholder; Finish proposes it as Roof Repair's one CM-022 contextual-link exception for Paul's approval.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Roof Repair [NEED]s: W10 photos, W11 flashing/underlayment, repair warranty, 5 repair types confirmed, 25% rule SC source, repair visit length | Client via Paul (facts interview) | Ship of svc-roof-repair |
| Bluffton [NEED]s: Apex pulls Town permit, UDO §3.18, UDO Art. 5 materials list, W9 gated communities, 6th neighborhood (LOC-15 needs 6-12) | Client via Paul / research | Ship of loc-bluffton |
| Emergency FAQ link (pilot_emergency_faq_link_cm022) | Finish, Paul approves | The live link only |
| Hail repair confirmation (routed) | Client via Paul | Emergency Roof Repair brief |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| SD - Roof Repair | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | SEM applied, checks passed |
| LD - Bluffton | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | SEM applied, checks passed |
| Semantic Review table | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md | Applied (SEM-1..8) |

**What I could not check**
- E4 on Roof Repair's delivery H2 is 354 copy words now (401 with the [NEED] markers counted); when W10, W11 and the repair warranty are answered, keep each to a short sentence or the section passes 375.
- Neighborhood count (LOC-15) stays at 5 + [NEED] until a sixth is sourced.

**Anything the next agent would otherwise get wrong**
- Used forms to record in C3 at write-back: SD opening "Homeowners across … hire Apex Roofing of the Lowcountry, a roofing contractor, …", CTA "For a free repair estimate, phone …"; LD opening "Based in Bluffton, SC, Apex Roofing of the Lowcountry is a roofer …", CTA "Ask for a free estimate at …". The on-call sentence lives on Roof Repair only. Sibling-city H2 pattern for the location batches: "Which Towns Near <City> Do We Also Serve?". Pilot corrections (status.py pilot-corrections) must still be recorded before the next batch.

## /build · 2026-10-09 · run 20261009-131920-build-c283

**What I did**
- Planned the link wheel from the approved site plan (`publish.py wheel`, 20 pages).
- Generated two WordPress **drafts** from the approved pilot files (`publish.py drafts --batch pilot`), nothing published:
  - svc-roof-repair → draft id 1614 ([REDACTED]/?page_id=1614), slug `roof-repair-new` (the live /roof-repair/ is replaced in place by Jonie).
  - loc-bluffton → draft id 1615 ([REDACTED]/?page_id=1615), slug `bluffton-new` (the live /bluffton/ is replaced in place).
  - SEOPress on each: SEO title, meta description, Facebook and X title and description from the approved title and meta; robots and canonical left at defaults. The approved files carry no keyword line, so the target keyword is set only where the site plan provides one.
  - Link tables: only rows whose target is in this batch or live were filled (Roof Repair → Bluffton; Bluffton → Roof Repair). 29 rows are held in `wheel_pending` until their targets go live.
- Publish handoff H-2026-10-09-09-publish (2 rows) issued to Jonie by the script; copied to Drive `02 - Build`. Batch pilot marked `handed_off`.
- No navigation handoff: both pages replace existing live URLs, so the menu does not change.

**What was decided, and why**
- Logged: the drafts carry the approved files' open `[NEED: …]` markers (Roof Repair 10 lines, Bluffton 4 lines) and the SEM-1 emergency link placeholder (`/emergency-roof-repair/`, CM-022 exception for Finish; Build adds no link, CM-005). Paul should hold the publish handoff until they are answered.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| `[NEED: …]` markers in both pages (facts interview / client answers, then re-approval and regenerated drafts) | Paul | Jonie publishing the pilot pages |
| Emergency Roof Repair link placeholder (SEM-1) | Finish (Paul approves the CM-022 exception) | nothing in Build |
| Pilot corrections not yet recorded (`status.py pilot-corrections`) | Build / Paul | batch s1 starting |
| WordPress login is an Administrator (wordpress_login) | Paul | nothing in this run |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Publish handoff | clients/apex-roofing-of-the-lowcountry/handoffs/H-2026-10-09-09-publish.md / .csv | issued to Jonie (Paul to hold) |
| Link wheel plan | clients/apex-roofing-of-the-lowcountry/build/link-wheel.json | planned |
| Approved files | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - …md, LD - Bluffton - …md | approved, source of the drafts |

**What I could not check**
- I did not read the drafts back from WordPress: drafts are not reachable by the public `?page_id=` URL (the read resolved to the homepage), and wp.py has no read-by-id command. `/verify` checks every field after Jonie publishes.

**Anything the next agent would otherwise get wrong**
- Do not let the pilot pages go live with `[NEED: …]` text in them: the handoff tells Jonie to publish, so Paul must hold it or the markers must be resolved first. To change wording, change the approved file, have Paul re-approve, regenerate — never edit drafts 1614/1615.

## /build · 2026-10-09 · run 20261009-134712-build-eac1

**What I did**
- Revised the two pilot draft files in place from Paul's 2026-10-09 answers (working files only; nothing sent to WordPress, no handoff written).
- Roof Repair (SD): W11 [NEED] replaced with "corrosion-resistant flashing ... and synthetic underlayment" on repairs; W10 [NEED] replaced with a photos step (photos of the work, progress photos each day on a longer job); new clean-up step (daily clean-up, magnet sweep for nails); repair-warranty [NEED] removed (no repair-warranty answer); the five "client confirms this repair type" [NEED]s removed and the flashing H3 renamed "Flashing Replacement at Chimneys, Walls and Valleys" to match Paul's services list (no hail); 25% rule FAQ kept general, SC-source [NEED] removed; "Can a roof be repaired in a day?" rewritten with the review example attributed (leak fixed in under 15 minutes, review 2025-06-05), visit-length [NEED] removed; "Should I repair or replace" FAQ gets one attributed sentence on the GAF System Plus Limited Warranties after a GAF replacement (review 2026-08-15). Delivery section trimmed to 373 words to stay under the 375 cap.
- Bluffton (LD): permit FAQ now says Apex gets the Town permit on a roof replacement (review 2026-08-15); Old Town FAQ drops both UDO [NEED]s and any historic-review claim (it tells the homeowner to ask the Town first); gated-community FAQ heading changed to "...Palmetto Bluff and nearby gated communities?" and the answer places Palmetto Bluff inside the Town and Belfair, Colleton River Plantation and Moss Creek outside the Town limits in Beaufort County (Town of Bluffton Neighborhoods PDF); Hampton Hall added as the sixth neighborhood (Town PDF, inside Town limits; also named in a 2026-05-17 review).
- Brand Guide working copy: two Paul Exception rows in Section H (review-sourced facts, CM-027 exception; replacement price $20,000-$25,000 for the Roof Replacement brief only, cited to Ken Gathercole's 2026-08-15 review per Paul, not in the reviews export). Section D status cells only (W11, W9 four communities, W10, W25, ShingleMaster -> Paul Approved 2026-10-09). Checked: the entity_approved (A+B1+B2) and brand_guide_approved (A+D+E+G) hashes are unchanged.
- Changes #346-#348 logged; six decisions settled.

**What was decided, and why**
- Review-sourced facts are used only because Paul confirmed them; they are recorded as a Paul Exception to CM-027 in Brand Guide H, and timing appears only as an attributed example (no general visit length).
- The GAF System Plus warranty appears only in a replacement context and is attributed to one review; no repair warranty is stated.
- The replacement price is in neither pilot draft; it waits for the Roof Replacement brief and must be cited to the single review.
- Old Town: no historic-review or material-list claim (Paul: ignore unless evidence; none found).
- Synthetic roofing (offered) and ShingleMaster (current) settled; neither pilot page needs them.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Re-approve both revised pilot drafts (the earlier batch:pilot:drafts approval no longer covers these files) | Paul | ship; publish handoff H-2026-10-09-09-publish stays on hold |
| WordPress drafts 1614 and 1615 were generated from the old approved files and are now stale | Build (ship, after re-approval) | Jonie must not publish them |
| Pilot corrections not yet recorded (`status.py pilot-corrections`) and spec §8 lines not written | Build / Paul | batch s1 start |
| CM-022 emergency-FAQ link path (open question pilot_emergency_faq_link_cm022) | Paul | Finish |
| Port Royal base-housing work; a general replacement price range | Client via Paul | later location / replacement briefs |
| Brand Guide D value cells, D2 and R4 for ShingleMaster and the review-sourced facts | Paul (next Brand Guide revision; re-opens brand_guide_approved) | nothing in the pilot |
| Magnet sweep is per Paul only; it is not in the reviews export | Paul | nothing (flagged) |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| SD - Roof Repair | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | revised, awaiting Paul's re-approval |
| LD - Bluffton | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | revised, awaiting Paul's re-approval |
| Brand Guide (H exceptions, D status) | clients/apex-roofing-of-the-lowcountry/brand-guide.md | working copy updated; approvals intact |

**What I could not check**
- The magnet sweep and the $20,000-$25,000 figure are not in the reviews export (the export has no reviewer names either); both rest on Paul's word.
- No South Carolina source for the 25% rule; the answer stays general.

**Anything the next agent would otherwise get wrong**
- Do not ship from the existing WordPress drafts 1614/1615: they hold the old copy. After Paul re-approves, regenerate them from the revised files. The replacement price belongs only on the Roof Replacement page, cited to one review. Belfair, Colleton River Plantation and Moss Creek are never "in Bluffton".

## /build · 2026-10-09 · run 20261009-135629-build-8db7

**What I did**
- Batch review of the revised pilot drafts (SD Roof Repair, LD Bluffton) side by side (CM-017, CM-043). Report only; neither draft changed.
- Wrote a new semantic review table for the revised drafts, replacing the old one: `build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md`, 4 SEM items.
- Registered the batch: `status.py batch apex-roofing-of-the-lowcountry pilot --state drafts_written --sem-table <table> --sem-findings 4`.

**What was decided, and why**
- Sibling check clean: no FAQ or heading collision, opening and CTA sentence forms differ, on-call sentence on SD only, nothing from the revision repeated across the pages.
- Targeted checks pass: Town limits vs Greater Bluffton correct (Palmetto Bluff, Hampton Hall inside; Belfair, Colleton River, Moss Creek outside); no price claim; $20,000-$25,000 on neither page; Roof Repair services match Paul's list, no hail; warranty only in the replacement FAQ.
- New SEM items: SEM-1 Old Town 1996 listing stated 3 times on LD; SEM-2 flashing-vs-sealant point twice on SD; SEM-3 flashing quote credited to Ralph and Pierce (Brand Guide G names no speaker); SEM-4 LD says Apex "replaces roofs" in Palmetto Bluff, W9 says "works in".

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Pick SEM items (`--sem 1,2,3,4` or `--sem none`) and approve batch:pilot:drafts | Paul | apply-sem / ship |
| pilot_emergency_faq_link_cm022 (link placeholder in SD emergency FAQ) | Paul | Finish link proposal |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Semantic review table | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md | REVIEW, 4 SEM |
| SD draft | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | awaiting approval |
| LD draft | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | awaiting approval |

**What I could not check**
- Who of the owners spoke the flashing quote (SEM-3); whether Apex has done replacements specifically in Palmetto Bluff (SEM-4). SEM-1 to SEM-7 as checks still have no definition in writing-commercial.md.

**Anything the next agent would otherwise get wrong**
- These SEM numbers are new; they do not refer to the old table's SEM-1 to SEM-8 (already applied in run 20261009-131416-build-ec1c). At write-back, record the "no travel fee" sentence form in C3 so later location pages do not repeat it.

## /build · 2026-10-09 · run 20261009-140247-build-805e

**What I did**
- Applied only the SEM items Paul picked for the pilot (SEM-1, SEM-2, SEM-3 from the review table of run 20261009-135629-build-8db7). Changes #369–#371.
- SEM-1 (LD Bluffton, Old Town FAQ): removed the third "National Historic District since 1996" mention. The H2 "What Makes Roofing in Bluffton Different?" sentence and the Top Sites list keep it.
- SEM-2 (SD Roof Repair, H3 Flashing Replacement): removed "not covered over with caulk". The flashing-versus-sealant point now lives only in the delivery paragraph.
- SEM-3 (SD Roof Repair, delivery paragraph): the flashing quote is now credited to "the owners" (was "Ralph and Pierce").
- Re-ran E1–E10 and the service/location spec checks on the changed sections: all pass. Readability (E10): SD page grade 6.2, LD 5.8, no paragraph over 10.
- Recorded batch pilot as `sem_applied` with `--checks-passed` (approval pinned to the applied versions; no new stop).

**What was decided, and why**
- SEM-4 reviewed and kept: "Apex replaces roofs in Palmetto Bluff" stays as written. Paul confirmed Apex offers all services in Palmetto Bluff and the nearby communities (logged with run.py decision).
- No Brand Guide row was edited. Section G records the flashing quote as the client's verbatim answer of 2026-10-07 with no named speaker, so "the owners" matches the source.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| "the owners" is a light role word; Brand Guide D (named staff) says no job titles published. Paul chose the wording, so it stands. | Paul (FYI only) | Nothing |
| pilot_emergency_faq_link_cm022 (SD emergency FAQ link, CM-022 exception in Finish) | Paul | Finish link wheel |
| WordPress drafts 1614/1615 hold the older copy | Build (ship step) | Must be regenerated from the SEM-applied files at ship |
| Jonie handoff H-2026-10-09-09-publish | Paul / Build | Stays on hold until the drafts are regenerated |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| SD Roof Repair (SEM-applied) | clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | sem_applied, checks passed |
| LD Bluffton (SEM-applied) | clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | sem_applied, checks passed |
| Semantic Review | clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md | approved (SEM 1,2,3) |

**What I could not check**
- Nothing in WordPress was touched or compared; the live drafts 1614/1615 were not read in this run.

**Anything the next agent would otherwise get wrong**
- Do not push the old WordPress drafts 1614/1615 to Jonie: they predate these edits. Regenerate them from the files above at `/build ship pilot` (never edit a generated draft). SEM-4 was deliberately not applied.

## /build · 2026-10-09 · run 20261009-140647-build-c103

**What I did**
- Resumed the stopped ship run on Paul's option 1 (accept new drafts). WordPress check passed under this run (test drafts 1616/1617 created and trashed; NOTE: login is an Administrator; Kadence head-code key not set yet).
- Re-planned the link wheel (`publish.py wheel`, 20 pages) and ran `publish.py drafts --batch pilot`: new WordPress DRAFTS from the current approved (SEM-applied) files — svc-roof-repair → draft 1620 (slug roof-repair-new, SD sha fc7c7933af8f); loc-bluffton → draft 1621 (slug bluffton-new, LD sha 29f915db08aa). SEOPress title, meta description and target keyword set by the script. Nothing published; no `--live`; no published page touched.
- The script issued publish handoff H-2026-10-09-10-publish to Jonie (2 rows: replace the content of the live /roof-repair/ and /bluffton/ with the draft blocks, keep the URL, then trash the draft). 0 paired redirects; 29 link-table rows held until their targets go live.

**What was decided, and why**
- Paul chose to accept new drafts rather than reuse 1614/1615 (they predate the SEM edits). Old drafts and the old handoff were left untouched for Paul.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Old drafts 1614 (roof repair) and 1615 (Bluffton) superseded — trash in WordPress | Paul | Confusion for Jonie if left |
| Handoff H-2026-10-09-09-publish superseded by H-2026-10-09-10-publish — not edited or withdrawn | Paul | Jonie must work only from -10 |
| SEM-1 emergency link: the SD FAQ carries the inline text "[Link placeholder: /emergency-roof-repair/ …]" in its paragraph, and it is in draft 1620 as visible text | Paul / Finish | Would show on the live page if published as-is; decide before Jonie publishes |
| pilot_emergency_faq_link_cm022 (CM-022 exception) | Paul | Finish link wheel |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Publish handoff | clients/apex-roofing-of-the-lowcountry/handoffs/H-2026-10-09-10-publish.md / .csv | issued to Jonie |
| WP drafts | ?page_id=1620, ?page_id=1621 | draft |
| Link wheel | clients/apex-roofing-of-the-lowcountry/build/link-wheel.json | planned |

**What I could not check**
- Did not read drafts 1620/1621 back from WordPress block by block; `/verify` checks the live pages after Jonie publishes.
- No menu (navigation) handoff: both pilot pages replace existing live URLs, so no menu change was identified.
- Batch pilot set to handed_off (`run.py finish` requires it for ship); handoff .md and .csv copied to Drive `02 - Build`.

**Anything the next agent would otherwise get wrong**
- Jonie works from H-2026-10-09-10-publish only (drafts 1620/1621). 1614/1615 and H-…-09 are superseded; the SEM-1 placeholder text is inside the roof-repair FAQ paragraph and must not go live as text.

## /build · 2026-10-09 · run 20261009-142045-build-a198

**What I did**
- Recorded Paul's pilot corrections (status.py pilot-corrections) so later batches are no longer held by the pilot-corrections check.
- Logged the corrections as three run decisions: the client-level corrections, the proposed spec section 8 lines, and the publish-together project note.
- Tried to add one pilot-correction line each to methodology/specs/service.md and location.md section 8. The permission system refused the edit, so no spec file changed. The proposed lines are in the decision log.

**What was decided, and why**
- Client-level corrections, carried into every later Apex brief (already settled, not re-asked): the flashing credit reads "the owners" (Ralph and Pierce Brehany, no job titles); the Roof Repair services list is shingle repair and replacement, flashing replacement, ridge cap and starter strip repair, soffit/fascia/deck repair, leak repair (no hail; hail goes to Emergency Roof Repair); $20,000-$25,000 is a Roof Replacement brief fact only, cited to Ken Gathercole's Google review of 2026-08-15; warranty only in a replacement context; Bluffton cut down because nobody needs the depth.
- Proposed spec lines (not written): service #7/SVC-19 lists only the sub-services the client confirmed for that service and puts warranty and price claims only on the service they apply to. Location #5/#8/LOC-22/LOC-23 gives each section what its element needs and stops, and treats 1,000 words as a ceiling, not a target.
- Publish-together rule (every page stays a WordPress draft until all are drafted): this is a project note for a later Opus design session. No system change was made.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Spec section 8 lines for service.md and location.md: allow the edit or add them by hand | Paul | Nothing blocked. The s1 briefs apply the lines from the decision log. |
| Publish-together rule as a system change (ship and publish timing) | Paul (Opus design session) | Until then, Paul holds each batch's publish handoff |
| Evidence-gate status parser (dated status cells read as Unverified, see the 2026-10-08 decision) | Paul (system session) | s1 evidence results may come out BLOCK again |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Site plan (s1 pages) | clients/apex-roofing-of-the-lowcountry/build/ | approved |
| Service spec | methodology/specs/service.md | approved, section 8 empty |
| Pilot corrections | decisions.md, run 20261009-142045-build-a198 | recorded |

**What I could not check**
- Whether batch s1 passes its own gates (briefs_ready, evidence). The next run checks them with `run.py start`.

**Anything the next agent would otherwise get wrong**
- Spec section 8 is still empty. Read this run's decisions as the pilot corrections. Keep hail off every page except Emergency Roof Repair, and only with the client's confirmation. Put the $20,000-$25,000 figure on Roof Replacement only, cited to the review, never as Apex's price.

## /build · 2026-10-09 · run 20261009-142804-build-8390

**What I did**
- Evidence gate (CM-041) for batch s1 (Roof Replacement, Roof Installation, Roof Inspections, Emergency Roof Repair).
- Wrote one page facts file per page (service_scope, service_process, timeframe, pricing). Sources: the returned proof sheet, Paul's answers, Brand Guide D, decisions-settled and the live-site capture. No status was raised above what its source supports.
- Ran `evidence.py run --batch s1`. Result: all 4 pages are BLOCK.

**What was decided, and why**
- Facts recorded:
  - Replacement pricing is Paul Approved: the W20 shingle range, plus the single review example for this brief only (replacement_price_review).
  - Installation scope is Paul Approved (W16, plus CertainTeed and GAF).
  - Inspections process is Paul Approved (W25 and W10).
  - Emergency pricing records only "no minimum call charge" (Paul Approved).
  - Process on Replacement, Installation and Emergency uses the client's own words (Client Confirmed).
  - Live-site-only scope lists stay Submitted. Timeframes are Unknown.
- **Main cause of the blocks.** In Brand Guide A and D, the status cells hold dates and notes (for example "Paul Approved 2026-10-06 · was: Submitted"). evidence.py counts a fact as Known only when the status cell is exactly the status word. So these rows came out Unverified: phone, free estimate, warranty, licence, insurance, certifications, rating, Emergency and Services subcontracted.
- If those cells parsed, all 4 pages would be WARN, not BLOCK. I did not change any Brand Guide status. Decision logged.

**Unresolved — and who owns it**
| Item | Owner | Blocking what |
|---|---|---|
| Status cells with dates are read as Unverified by evidence.py. Fix the parser or the status format in a design session. | Paul (design session) | Every service brief, s1 and later |
| Choose for each s1 page: run the facts interview, or waive the block with a reason | Paul | s1 briefs |
| Service scope is confirmed only on the live site: Replacement materials, the four inspection types, the Emergency scope and tarping | Client via Paul (facts interview) | Replacement, Inspections and Emergency briefs |
| Timeframes: replacement duration, install duration, inspection visit length (Unknown on all 4 pages) | Client via Paul | Supporting gaps only (FAQ answers fall back to [NEED]) |
| Inspection pricing: W17's "independent reports priced separately", and a price for those reports | Client via Paul | Inspections FAQ 1 |
| Installation cost drivers | Client via Paul | Supporting gap only |
| Phone: is (843) 757-2739 a call-tracking number? | Paul | A8 [NEED] |

**What the next step needs, and where it is**
| Artifact | Path | Status |
|---|---|---|
| Page facts (4) | clients/apex-roofing-of-the-lowcountry/build/evidence/svc-{roof-replacement,roof-installation,roof-inspections,emergency-roof-repair}.facts.json | written |
| Evidence grids (4) | clients/apex-roofing-of-the-lowcountry/build/evidence/svc-*.grid.md (same 4 ids) | BLOCK |

**What I could not check**
- The live body text of the s1 pages. Only the headings and meta from the 2026-10-05 capture were in the read list.

**Anything the next agent would otherwise get wrong**
- Do not edit Brand Guide statuses to get these pages through the gate.
- If the parser is fixed and the gate re-run, expect WARN on all 4 pages. Even then, Replacement, Inspections and Emergency still have Submitted scope, which their briefs must list under Evidence gaps.
- The facts interview (`/interview apex-roofing-of-the-lowcountry facts s1`) would mostly re-ask facts that are already Paul Approved or Client Confirmed. Settled decisions must not be re-asked, so its pack needs trimming to the real gaps above before Paul sends it.

## /drive-mirror · 2026-10-09 · run 20261009-201529-drive-mirror-043d

**What I did**
- rewrite 2 URL migration: worklist rows for the redirect / slug clearing

## /drive-mirror · 2026-10-09 · run 20261009-222751-drive-mirror-dd35

**What I did**
- Added the worklist row "Jonie: embed a Google map of Bluffton, SC" (section 4, with the pilot publish).
- Brand Guide D2 and D3 (R4): ShingleMaster resolved per Paul 2026-10-09; the Certifications status note tidied. This changes values in Section D, so brand_guide_approved needs Paul's re-approval.

## /build · 2026-10-11 · run 20261011-212524-build-5379

**Step:** the one facts round (P10) for every page in the approved site plan (22 pages).

**Done**
- Route was null at the start. Paul answered "Route A" and the coordinator recorded it with status.py set.
- Evidence grids for all pages: `evidence.py run --all`, run 3 times (before research, after research, after the live-site facts).
- Reviews: `reviews.py extract` found 22 facts or topics, 13 of them reported by 3+ reviewers. The researcher checked them by meaning (CM-057):
  - confirmed: timeframe 4, guarantees 10, warranty 7
  - set to 0: pricing, founding, company_story
  - single reviewer, below the 3 minimum: response_time, emergency, insurance
- Page facts files:
  - 11 location pages: city_served comes from Brand Guide E. The researcher filled local_context, neighborhoods, things_to_do and top_sites, cited mostly to Wikipedia plus the Jasper County tourism page.
  - svc-metal-roofing, svc-slate-roofing, svc-skylights: live-site scope and process, status Submitted.
- Open keys closed because they were already answered (`run.py decision --settle --closes`):
  - loc_towns_served (11 city_served keys)
  - svc_timeframe_review_examples (8 keys)
  - svc_roof_repair_scope
  - named_staff_on_page
  - guarantees_review_attributed (review-attributed, 10 reviewers)
  - metal_slate_price_ranges (2 keys)
- Question set: 10 client questions grouped by fact. `settled.py filter` kept 10 of 10 and `questions.py check` passed.
  - `clients/apex-roofing-of-the-lowcountry/interviews/facts/Apex Roofing of the Lowcountry - Facts Interview - all - 2026-10-11 - REVIEW.md`
  - `clients/apex-roofing-of-the-lowcountry/interviews/facts/facts-round-all-2026-10-11.questions.json`
- Flags:
  - F-001 to F-007 (researcher): new official permit and tourism sources for the area list.
  - F-008: a second `evidence.py questions` call overwrites the set with 0 questions.
  - F-009: city_served and service_scope were asked with bad pre-fills.
  - F-010: reviews.csv has no reviewer_key column.
  - F-011: a mixed-status D row is marked Unverified as a whole.

**Gate results now**
- PASS (8): loc-bluffton, loc-hilton-head-island, loc-okatie, loc-beaufort, loc-port-royal, loc-st-helena-island, loc-hardeeville
- WARN (11):
  - svc-roof-repair, svc-roof-replacement, svc-roof-installation, svc-roof-inspections, svc-emergency-roof-repair
  - loc-pritchardville, loc-ladys-island, loc-fripp-island, loc-ridgeland, loc-levy
  - home
- BLOCK (4): svc-metal-roofing, svc-slate-roofing, svc-skylights (scope and process are live-site only, so yes/no Q1 and Q2), about (company story Q10, awards and team Q8 and Q9)

**Open for Paul**
1. Send the facts-round question set: 10 questions, mostly yes/no. Record the answers with `/interview apex-roofing-of-the-lowcountry facts-answers all`.
2. SC licence #57706: the class, holder and status could not be read (the SC LLR lookup redirect-loops, and the BBB page did not show it). Choose one:
   - (a) Jonie runs the LLR lookup by hand, or
   - (b) publish the number only.
   The key fact:d:licence_numbers stays open.
3. Public facts not found. For each, drop the element or keep it general:
   - Okatie: top sites
   - Pritchardville: neighbourhoods, things to do
   - Lady's Island: neighbourhoods, things to do, top sites
   - St. Helena Island: things to do
   - Fripp Island: neighbourhoods
   - Ridgeland: neighbourhoods
   - Levy: neighbourhoods, things to do, top sites
4. Noted only:
   - The live slate and skylights H1s say "The Best", which the CM-020 re-test rejected. The site plan's H1s replace them.
   - The metal and skylights page intros say "Beaufort and Jasper County".
   - Review row 22 (2022) is negative about an inspection.

**Next:** Paul sends the set. Once the answers are recorded and the grids re-run, `/build apex-roofing-of-the-lowcountry write services`. The WARN pages can be briefed now, with Evidence gaps sections. Nothing was approved and no gate was set.

## /build · 2026-10-11 · run 20261011-214754-build-8691

**Route:** A. **Date:** 2026-10-11.

### Done
- Evidence gate (CM-041) re-run for the services batch: Roof Replacement, Roof Installation, Roof Inspections, Emergency Roof Repair **WARN** (1 required gap each); Metal Roofing, Slate Roofing, Skylights **BLOCK** (2 required facts not known each).
- Briefs written and recorded (`status.py page-stage … --stage brief`) for the 4 WARN pages, each with an `## Evidence gaps` section:
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Roof Replacement - Apex Roofing of the Lowcountry.md`
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Roof Installation - Apex Roofing of the Lowcountry.md`
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Roof Inspections - Apex Roofing of the Lowcountry.md`
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Emergency Roof Repair - Apex Roofing of the Lowcountry.md`
- No brief for the 3 blocked pages.
- Flag F-012 raised (system): the brief step started while Paul's 2026-10-11 facts answers were unrecorded.

### Open — for Paul
| Item | Options | Blocks |
|---|---|---|
| Paul's 2026-10-11 facts answers are on disk but not recorded | record with `/interview apex-roofing-of-the-lowcountry facts-answers all`, then re-run the gate | clears most scope `[NEED]`s on the 4 briefs; likely unblocks Metal, Slate, Skylights |
| Replacement price: settled one-review $20k–$25k example vs Paul's 2026-10-11 answer ("review price mentions not used; Lowcountry standard ranges") | (a) drop the example, keep W20 $9k–$18k; (b) drop it, researcher cites a published SC/Lowcountry range; (c) keep as settled | Roof Replacement FAQ 1 |
| Emergency FAQ 2 duplicates the approved Roof Repair emergency-leak FAQ (SEM-1) | (a) replace with "Do past customers get priority in a roofing emergency?" (proposed); (b) keep, safety-only answer; (c) remove it from Roof Repair (re-approval) | Emergency brief |
| Metal, Slate, Skylights blocked | record the 2026-10-11 answers and re-run the gate, or `/approve … evidence:<page> --reason "…"` | their briefs |
| One-line client checks (optional) | tarping in emergencies; W17 free inspection / paid reports; install time on a new home; synthetic underlayment on replacements/new installs | `[NEED]`s in the briefs |

### Public facts for the researcher (never asked of the client)
SC adopted residential code on drip edge (Installation FAQ 1); inspection-frequency guidance (Inspections FAQ 4); asphalt-shingle lifespan in coastal SC (Replacement FAQ 2); if Paul picks (b) above, a published SC/Lowcountry replacement cost range.

### Not done (outside this step)
No drafts. No facts recorded. No settled decision reopened (the price conflict is listed for Paul instead).

## /interview · 2026-10-12 · run 20261012-065139-interview-b77b

## What changed
- Settled scope and process answers under `fact:<page>:<key>` for svc-metal-roofing, svc-slate-roofing and svc-skylights (six settles, Paul 2026-10-11 answers 1 and 2: "site is accurate"). The settled text is the live-site wording Paul confirmed.
- Recorded Paul's 2026-10-11 answers 3–10 as decisions (no settle; several are notes for after the page handoffs).
- Recorded `d-price-replacement-standard-2026` (paul_approved, Paul 2026-10-12 chat) with the two sources he gave.
- Recorded decision: FAQ 2 on svc-emergency-roof-repair → option (a), to be applied in a revision of that brief.
- Re-ran the evidence gate for the services batch: all seven service pages WARN, none BLOCK.

## Open for Paul
1. **replacement_price_review** (settled, $20k–$25k) conflicts with answer 3 ("work off the Lowcountry standard"). Reopen or keep?
2. **Price sources.** Both cited sources are contractor marketing blogs. Researcher to verify against an independent source?
3. **Notes after the page handoffs:** awards (client to obtain a few this week, Paul); company story about customer care; Facebook posts must be active.
4. **Bonded status** is still not sure (answer 5).

## Gate result (services batch)
| Page | Result | Unverified | Required gaps |
|---|---|---|---|
| svc-roof-replacement | WARN | 4 | 1 |
| svc-roof-installation | WARN | 5 | 1 |
| svc-roof-inspections | WARN | 5 | 1 |
| svc-emergency-roof-repair | WARN | 4 | 1 |
| svc-metal-roofing | WARN | 4 | 0 |
| svc-slate-roofing | WARN | 4 | 0 |
| svc-skylights | WARN | 4 | 0 |

## /build · 2026-10-12 · run 20261012-065658-build-15df

**Agent:** Build (Agent 2), Route A.

**Done**
- Re-ran the evidence gate for the batch in this run (`evidence.py run … --batch services`). The results were unchanged: all 7 pages WARN. The four earlier pages still have 1 required gap each, and metal, slate and skylights have 0.
- Wrote and recorded (`status.py page-stage … --stage brief`) the three briefs that were blocked and are now unblocked by Paul's 2026-10-11 answers 1–2 (settled 2026-10-12):
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Metal Roofing - Apex Roofing of the Lowcountry.md`
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Slate Roofing - Apex Roofing of the Lowcountry.md`
  - `clients/apex-roofing-of-the-lowcountry/build/services/SB - Skylights - Apex Roofing of the Lowcountry.md`
- All three gates WARN (0 required gaps); each brief has `## Evidence gaps`. The script reported "batch briefs collected" — all seven services briefs are on file for Paul's one approval.
- The four existing briefs (Replacement, Installation, Inspections, Emergency) were not touched; the batch tool did not ask for them to be re-run.
- Applied: settled scope/process wording only; Paul answer 3 (Lowcountry standard prices `d-price-replacement-standard-2026`, no client-specific or review prices, no $20k–$25k example); answers 4–6 (metal 40-year panel warranty, insurance, new construction); answer 7 (metas name replacement / emergency as the second service); coordinator's mid-run decisions (bonded status not raised; no review price figures).
- Flag F-013 raised: the service spec's `[Link wheel: …]` row placeholder vs the P11 placeholder rule. Workaround: kept the spec's form, as the pilot and sibling briefs do.

**Open for Paul (in the briefs)**
- Metal and slate: the briefs use the Lowcountry standard instead of the older client ranges W20/W19, per answer 3. Paul can keep W20/W19 instead.
- Metal: answer 4 (40-year panel warranty) is a logged decision, but `d-warranty-terms` still says Submitted. It needs a `run.py fact` record before publication.
- Slate: whether to move the synthetic-slate PAA questions (#30, #116, #124) off the blog list now that synthetic slate is confirmed. Default is no change.
- Skylights: optional yes/no question to the client: does Apex install Velux and FAKRO (W18)?
- Researcher pass (public facts, cited): metal over shingles, metal lifespan, slate lifespan, slate minimum slope, skylight energy, skylights on metal roofs, fixed vs venting skylights.
- Sibling conflict (reported, not changed): the Replacement brief still uses the W20 shingle range ($9,000–$18,000). Answer 3 points to the Lowcountry standard ($14,000–$20,000). Paul resolves this at the brief approval.

**Not done / never:** no drafts, no gates, no fact records, no edits to the four existing briefs.

## /build · 2026-10-12 · run 20261012-071055-build-c11c

Agent 2 — Build · 2026-10-12 · Route A

## What changed (three briefs, as Paul asked)
- **SB - Roof Replacement** — FAQ 1 price now uses the Lowcountry standard ranges (`d-price-replacement-standard-2026`): asphalt $350–$475/sq (about $14,000–$20,000), impact-resistant $425–$600/sq, standing seam $700–$1,200/sq (about $24,000–$45,000+), wood $800–$1,400/sq, slate/tile $1,000–$2,000+/sq. Old $9,000–$18,000 range removed (specificity, F-002, must-not-appear updated). The $20,000–$25,000 Google review (2026-08-15) allowed once, attributed, as an example only. Independent-source check added to Evidence gaps. F1 resolved; F3 (partial price support) and F4 (metal warranty fact pending) added.
- **SB - Emergency Roof Repair** — FAQ 2 replaced by "Do past customers get priority in a roofing emergency?" (Paul option a; BG-D Emergency, Client Confirmed). Old routed rows moved to the delivery H2. F1 resolved.
- **SB - Slate Roofing** — PAA #30, #116, #124 moved from the blog list to FAQ 6–8, answered from manufacturer pages. F2 resolved; F3 (CertainTeed Belmont material) and F4 (metal warranty) added.
- **SB - Metal Roofing** — consistency only: one sibling-context line no longer says Replacement carries the old shingle range.
- All four re-recorded with `status.py page-stage --stage brief`.

## Independent price sources (researcher, accessed 2026-10-12)
- This Old House, SC roof replacement cost — https://www.thisoldhouse.com/roofing/roof-replacement-cost-south-carolina (updated 2026-05-27)
- Fixr, roof replacement cost (national) — https://www.fixr.com/costs/roof-replacement (updated 2026-02-04)
Partial support: asphalt, metal, wood, slate per-square ranges roughly in line. Not confirmed: impact-resistant range; both whole-home totals (independent totals are lower). HomeGuide and Angi blocked access. Ranges kept as Paul approved; gap stated in the brief.

## Slate research (manufacturer pages, accessed 2026-10-12)
- DaVinci Province Slate (Westlake Royal): lifetime limited material warranty, 10-year non-prorated; composite resin tile. No expected-life figure found anywhere reliable.
- CertainTeed Belmont: manufacturer page says "slate-like" shingle; material (asphalt vs synthetic) not stated — conflicts with the settled scope wording "premium synthetic slate". Brief uses "slate-look shingle" pending confirmation.

## Pending / open
- **Metal warranty fact record pending:** the 40-year metal panel-finish warranty is still `Submitted` in facts; not changed in this run.
- Settled `metal_slate_price_ranges` (W20/W19 client ranges) still differs from the new standard; Metal and Slate briefs already flag it for Paul.
- No flags raised (no workflow rule found wrong). No facts recorded, no drafts written, no decisions made.

## /build · 2026-10-12 · run 20261012-071954-build-c525

Agent 2 — Build · 2026-10-12 · Route A · step build:brief (revision 2), batch services

## What changed (Paul's three answers, 2026-10-12, logged as decisions to this run)
- **SB - Roof Replacement** — FAQ 1, specificity item 4, the Evidence gaps price row and F3 now give only the two whole-home ranges: architectural asphalt about $14,000–$20,000 for a typical home, standing seam metal about $24,000–$45,000+, both varying with roof size. Every per-square figure removed. Impact-resistant, wood and slate/tile: no figure (the approved standard gives no whole-home range for them). The one attributed review example ($20,000–$25,000, 2026-08-15) unchanged: reviewer not named on the page, named in the source note only.
- **SB - Metal Roofing** — FAQ 1, FAQ 2, Evidence gaps price row and F1: whole-home ranges only, per-square removed. Change log added.
- **SB - Slate Roofing** — (1) FAQ 1 now states no price (no whole-home slate range in the approved standard); FAQ 2, F-002 row, price gap row and F1 aligned. (2) CertainTeed Belmont removed from the scope note, types H3, specificity, FAQ 7, FAQ 8, routed line, must-not list and F3 (resolved); DaVinci Roofscapes is the only synthetic brand. One-line note kept in Evidence gaps that Paul skipped the Belmont detail. (3) FAQ 6 answer: DaVinci's lifetime limited warranty with a 10-year non-prorated period, as the manufacturer's warranty; no lifespan in years.
- **SB - Roof Installation, Roof Inspections, Emergency Roof Repair, Skylights** — no per-square figure was present; "any per-square price" added to Must not appear; change-log row added.
- All seven re-recorded with `status.py page-stage --stage brief` (batch briefs collected).

## Remaining "per square" text
- No per-square price in any brief. The only "per square" figure left is the slate **weight** (800–1,500 lbs per square vs 200–350 for shingles; settled process, Slate delivery H2 and specificity 2) — a weight, not a price, kept unchanged. Other mentions are the rule itself ("no per-square price").

## Open for Paul (not decided here)
- `facts.json` `d-price-replacement-standard-2026` and settled `replacement_price_review` still hold the per-square figures; `fact:svc-slate-roofing:service_scope` still names Belmont. The briefs override both. Paul may want these records updated (`run.py fact` / `--settle`) so later batches do not pick them up.
- Slate weight "per square" wording — keep, or restate (e.g. per 100 sq ft) at brief approval.
- Earlier flags still open: F3 Replacement (whole-home ranges higher than independent sources), metal F1 (W20 vs standard), slate F1 (no price), 40-year metal warranty fact still Submitted.

## Flags raised
- None (no workflow rule or script problem met).

## /interview · 2026-10-12 · run 20261012-072350-interview-4762

## What changed
- `d-price-replacement-standard-2026` (facts.json): value now holds whole-home ranges only (asphalt about $14,000–$20,000; standing seam metal about $24,000–$45,000+; no per-square figures). Paul 2026-10-12.
- `fact:svc-slate-roofing:service_scope`: reopened and re-settled without CertainTeed Belmont (Paul: "not sure, skip"). Reopen logged as a process defect.
- `replacement_price_review`: logged as superseded. The Lowcountry whole-home ranges only, no per-square figures.

## Open for Paul
- Slate weight wording "per square" (800–1,500 lbs per square vs 200–350 for architectural shingles): keep, or reword as "per 100 sq ft"?

## /interview · 2026-10-12 · run 20261012-073051-interview-f000

## What changed
- `d-price-replacement-standard-2026` (facts.json): value now holds whole-home ranges only (asphalt about $14,000–$20,000; standing seam metal about $24,000–$45,000+; no per-square figures). Paul 2026-10-12.
- `fact:svc-slate-roofing:service_scope`: reopened and re-settled without CertainTeed Belmont (Paul: "not sure, skip"). Reopen logged as a process defect.
- `replacement_price_review`: logged as superseded. The Lowcountry whole-home ranges only, no per-square figures.

## Open for Paul
- Slate weight wording "per square" (800–1,500 lbs per square vs 200–350 for architectural shingles): keep, or reword as "per 100 sq ft"?

## /build · 2026-10-12 · run 20261012-073726-build-ecf5

**Agent:** Build (Agent 2) · 2026-10-12 · Route A

### Done
- Draft written from the approved brief (`SB - Roof Replacement`, approved 2026-10-12):
  `clients/apex-roofing-of-the-lowcountry/build/services/SD - Roof Replacement - Apex Roofing of the Lowcountry.md`
  (1,024 words incl. headings; 856 visitor-facing words scored).
- Recorded: `status.py page-stage apex-roofing-of-the-lowcountry svc-roof-replacement --stage draft` (exit 0).

### Paul's standing rules applied (2026-10-12)
- No per-square price anywhere. Only the two whole-home ranges (asphalt about $14,000–$20,000; standing seam metal
  about $24,000–$45,000+), stated as typical Lowcountry ranges that vary with roof size, never as Apex's price.
- The $20,000–$25,000 review (2026-08-15) appears once, in FAQ 1, as one customer's example; reviewer not named.
- CertainTeed Belmont not named. Impact-resistant, wood, slate/tile named with no figure.

### Stage 3 self-critique (E1–E10)
- E1 portability: opening rebuilt so it does not mirror Roof Repair's sentence pattern; delivery uses the
  "commodity / what you can't see" half of the client quote and "waves you can surf on" (Roof Repair has the
  silicone/flashing half); no GAF System Plus example (Roof Repair owns it). Pass.
- E2 specificity: 5 page-specific facts — lifetime no-leak + 50-year manufacturer warranty (transferable);
  CertainTeed + GAF factory installer and ShingleMaster; Town permit on a replacement; whole-home price ranges;
  SureStart PLUS. Pass.
- E3 variants: URL roof replacement → title Roof Replacement → H1 Re-Roofing / Beaufort and Jasper Counties →
  first H2 replace a roof / South Carolina Lowcountry / Residential Roofer → opening metro area + roofing contractor
  → FAQ H2 Lowcountry + Roofing Contractor. No consecutive repeat; reserved B1 unused. Pass.
- E4 chunk lengths: delivery 298 · types 186 · FAQ 332 · service areas + CTA 63 (all ≤ 375). Pass.
- E5 invention sweep: every fact traced to the brief / BG-D / settled decisions; 2 `[NEED]` kept (below).
  General trade statements only for material descriptions (architectural shingles layered; slate heaviest;
  synthetic made to look like slate, lighter). Pass, with those noted for batch review.
- E6 filler: none of the A6 phrases; cost FAQ answers first, no non-answer opening. Pass.
- E7 headers: one H1; every H2 a spoken question with an entity; no city in any H tag; no skipped levels.
  COM-11: title remainder "Roof Replacement" vs H1 remainder "Re-Roofing" — differ. Pass.
- E8 links: no cross-page link or `[LINK →]` in prose; service-area placeholder row present. Pass.
- E9 human: reads as the owners' trade advice (bid comparison checklist). Pass.
- E10 reading level: page grade 4.8 (856 words); first pass flagged 2 paragraphs (10.6, 10.1) — both split and
  re-run clean, no paragraph over 10. Pass.
- Spec SVC-01–23: pass, except SVC-21 (no outbound link — documented in the brief, Finish decision) and SVC-22
  (schema — Finish only).

### Open items in the draft
- `[NEED: same corrosion-resistant flashing and synthetic underlayment on a full replacement?]` (delivery, step 5)
- `[NEED: cited lifespan source for asphalt shingles in coastal SC]` (FAQ 2)

### For the batch review (not changed here)
- FAQ 2 ↔ Roof Repair "Should I repair or replace my roof?" — check side by side.
- FAQ H2 shape is close to Roof Repair's FAQ H2 ("What Do Homeowners Ask a Lowcountry Roofer About Repairs?") — reworded
  to "Which Questions Do Homeowners Ask a Lowcountry Roofing Contractor Before a New Roof?"; still a near pattern.
- Settled `replacement_price_review` text and Brand Guide H (Paul Exception rows) still carry per-square figures and
  "Town and HOA permits"; the draft follows Paul's 2026-10-12 rule and BG-D (Town permit only). Brand Guide H row
  should be tidied at the next Brand Guide revision.

### Flags raised
- None this run (the spec §8 pilot-corrections write remains as flagged in run 20261009-142045-build-a198).

### Not done (by design)
- Nothing published, nothing sent to WordPress, no link table filled, no schema.

## /build · 2026-10-12 · run 20261012-074135-build-56f3

**Agent:** Build (Agent 2) · 2026-10-12 · Route A

### Done
- Drafted `clients/apex-roofing-of-the-lowcountry/build/services/SD - Roof Installation - Apex Roofing of the Lowcountry.md` from the approved brief (SB - Roof Installation, approved 2026-10-12) and `methodology/specs/service.md`. ~900 words incl. headings; 730 counted by readability.py.
- Recorded: `status.py page-stage … svc-roof-installation --stage draft` (ok).
- Public-fact research (P6): drip edge in SC = S.C. Code Regs. 8-1228 (SC modification of IRC R905.2.8.5): "A drip edge shall be provided at eaves and rake edges of asphalt shingle roofs where required by the manufacturer." Effective history to 2022-05-27. Source: https://www.law.cornell.edu/regulations/south-carolina/R-8-1228. Clears brief flag F1; FAQ 1 now states the rule with the source named (no link — outbound authority link candidate for Finish, CM-011). Not entered in facts.json (public fact; researcher/fact-recording left to the facts round).
- Flag F-014 raised: readability.py `--exclude-terms` takes a file path, writing-commercial.md E10 implies a list. Workaround: terms file in scratchpad.

### Paul's standing rules (2026-10-12) applied
No price or cost figure at all on this page (Replacement owns cost; brief §6), so no per-square price, no whole-home range, no Ken Gathercole review. CertainTeed Belmont not named. No lifespan figure.

### [NEED] markers left (3)
1. Delivery H2: how Apex fits a builder's schedule (dry-in, return trips) — optional; delete the line if not stated.
2. FAQ 2: typical install time on a new home (answer is general without it).
3. FAQ 3: synthetic underlayment on new installs too? (Paul Approved for repairs only).

### Self-critique (Stage 3)
- E1 portability: PASS on page, two batch-review notes — (a) the "waves you can surf on" quote also appears in the Roof Replacement draft's delivery H2 (brief assigned it to this page's FAQ 4); (b) the layer sequence (underlayment → flashing/valleys → shingles) echoes Replacement step 5 in different words.
- E2 specificity: PASS — W16 subcontractor on new construction in Beaufort and Jasper County; CertainTeed + GAF factory installer, ShingleMaster; S.C. Code Regs. 8-1228; licence numbers; Ralph and Pierce on the roof.
- E3 variants: PASS — URL roof installation → title Roof Installation → H1 New-Construction Roofing / South Carolina Lowcountry → first H2 roof a new home / Beaufort and Jasper Counties / Roofers; FAQ H2 new build / Lowcountry / Roofer; reserved B1 unused.
- E4 chunks: PASS (delivery ~290 words, largest).
- E5 invention: PASS — every claim from BG-D/G or the cited regulation; Additions H3 left out (Submitted only); live wind/ventilation H3s not carried.
- E6 filler: PASS. E7 headers: PASS; COM-11 remainder "Roof Installation" vs "New-Construction Roofing" — pass. E8 links: PASS — no prose links; service-area placeholder present. E9: PASS. E10: page grade 5.9, no paragraph over 10 (after two fixes).
- Spec: SVC-01–SVC-22 pass on the draft; SVC-15 note — FAQ first sentences are 25–45 words (the spec's 40–60 read as the opening answer block); 4 FAQs; SVC-21 outbound link left to Finish.
- Types H2 has 2 H3s (additions left out per brief).

### Open
- Brief F2 (FAQ count) now moot for FAQ 1; FAQ 2 stays general unless the client gives an install time.
- Open facts keys unchanged: fact:d:services_subcontracted, fact:d:insurance (Paul's 2026-10-11 "correct" answers not yet recorded).

### Next
Remaining services drafts (Metal Roofing, Slate Roofing, Skylights, Roof Inspections, Emergency Roof Repair) each in their own run; then the services batch review.

## /build · 2026-10-12 · run 20261012-074602-build-fe96

**Agent:** Build (Agent 2), Opus · **Date:** 2026-10-12 · **Route:** A

### Done
- Draft written from the approved brief (`SB - Roof Inspections`, approved 2026-10-12): `clients/apex-roofing-of-the-lowcountry/build/services/SD - Roof Inspections - Apex Roofing of the Lowcountry.md` (about 1,000 words including headers and CTA; 840 words of visitor-facing text).
- Recorded: `status.py page-stage apex-roofing-of-the-lowcountry svc-roof-inspections --stage draft` (re-recorded after the last edit).

### Structure (spec service.md §3)
URL/title/meta/H1 per brief → opening (no H tag, phone, free estimate, buyer state: no leak yet, needs the roof's condition before a decision) → H2 delivery (311 words) → H2 types with 3 H3s (202) → H2 FAQ with 4 H3s (284) → H2 service areas with the link-wheel placeholder → CTA (no H tag).

### Choices made
- FAQ 3 (visit length) dropped, as the brief allows: a general visit length is settled as not stated (`svc_timeframe_review_examples`), and no review gives an inspection length. 4 FAQs remain (spec allows 4–6).
- No price anywhere. No per-square figure, no whole-home range, no Gathercole review, no CertainTeed Belmont, no lifespan figure.
- Customer examples, each from one review, dated, no names: the photos and written report the next day (December 2023); "found nothing that needed to be done" (January 2021). Neither is stated as Apex's standard.
- Left out: insurance-claim inspections, commercial, drone, checklist or report format as a standard, response time, "certified inspection", "bonded".
- None of the sibling drafts' quotes or definitions reused ("not just a commodity", "waves you can surf on", the silicone line, the flashing definition).

### Self-critique (E1–E10 + spec)
- E1 portability: pass. The delivery H2 is about the inspection itself, and the two review examples are specific to this page.
- E2 specificity: pass. Owners on the roof (W25), photos (W10), no minimum charge / no travel fee, SC #57706 and Bluffton #0620033323, residential only.
- E3 variants: H1 Roof Condition Inspections / Beaufort and Jasper Counties → first H2 "Roofer Checks Your Roof" / South Carolina Lowcountry. FAQ H2 Lowcountry / Residential Roofer. Reserved B1 not used. URL and title share "roof inspections", as in the approved chain (same on every sibling).
- E4: every H2 is under 375 words (max 311).
- E5 invention sweep: no unsourced noun or number. 5 NEEDs.
- E6 filler: none.
- E7 headers: every H2 is a question and names an entity, no city, one H1. COM-11: the title remainder is "Roof Inspections" and the H1 remainder is "Roof Condition Inspections", which is not the same term plus a filler word, so it passes.
- E8 links: none in prose or FAQ; the table placeholder is present.
- E9: reads like the trade.
- E10: readability.py page grade 5.5, no paragraph over 10 (the FAQ 1 cost answer was 12.5 before it was rewritten).
- C7/COM-12: the cost answer names what drives the cost first.

### Open — [NEED] markers (5)
1–3. `[NEED: client confirms this inspection type]` on Post-Storm, Pre-Purchase/Home-Sale and Annual Maintenance. These clear when Paul's 2026-10-11 answer 1 is recorded for `fact:svc-roof-inspections:service_scope` (still open).
4. `[NEED: are inspections free, and is a stand-alone written inspection report priced separately?]` (W17, open `fact:svc-roof-inspections:pricing`).
5. `[NEED: cited source on how often a roof should be inspected …]`: a public fact for the researcher, not a client question.

### Flags
None raised. One tooling note for /system-review: `readability.py --exclude-terms` takes a file path, not the comma list that the writing standard's wording suggests. The run used a scratch terms file.

### Next
The batch review (`/build … drafts services`) once the Emergency, Metal, Slate and Skylights drafts are recorded.

## /build · 2026-10-12 · run 20261012-074931-build-45cc

**Agent:** Build (Agent 2, Opus) · **Date:** 2026-10-12 · **Route:** A

### Done
- Drafted `clients/apex-roofing-of-the-lowcountry/build/services/SD - Emergency Roof Repair - Apex Roofing of the Lowcountry.md` from the approved brief (revised 2026-10-12, FAQ 2 = past-customer priority), spec `methodology/specs/service.md`.
- Recorded: `status.py page-stage … svc-emergency-roof-repair --stage draft` → "draft recorded".
- Flag F-015 raised (FAQ 40–60-word first sentence vs CM-047 reading level; readability.py `--exclude-terms` takes a file, not a list as E10 shows). Workaround applied; rules unchanged.

### Draft facts
- About 1,100 words (body). Meta 160 chars. Opening 104 words. H2 sections: delivery ~324, types ~293, FAQ ~290 words (all under 375).
- Reading level: page average grade 5.4, no paragraph over 10 (E10 passes).
- 7 `[NEED]` markers: tarping/temporary patch (×2: delivery step 4, FAQ 3); "client confirms this emergency type" (×5, one per H3 type — open question `fact:svc-emergency-roof-repair:service_scope`).

### Stage 3 self-critique
- E1 portability: opening (owners on call, past customers first) and FAQ 2 are unique to Apex. The H3 type descriptions (wind, thunderstorm, hail, leak, shingles) are general trade content and partly portable — batch review should look at them beside Inspections' post-storm H3 and Replacement's storm-damage H3.
- E2 specificity: 5 page-specific facts — owners always on call with emergency priority and past customers first (Client Confirmed); Ralph and Pierce get on the roof (Paul Approved); no minimum service-call charge; photos of the work; SC #57706 and Town of Bluffton #0620033323.
- E3 variants: URL "emergency roof repair" → title "Emergency Roof Repair" → H1 "Storm and Leak Emergency Roofing / South Carolina Lowcountry" → first H2 "urgent roof damage / Beaufort and Jasper Counties / Roofing Contractor". No consecutive repeat; reserved B1 variant unused. Opening: metro area + roofer + emergency roof repair. FAQ H2: Lowcountry + Roofers.
- E4 chunks: all H2 sections ≤ 375 words.
- E5 invention: no response time, no "24 hour"/"same-day", no after-hours-fee claim, no price, no per-square figure, no lifespan, no Ken Gathercole review, no CertainTeed Belmont, no insurance-claim help, no tarping as a service, never "bonded". Falling limb used only as one review's words ("a gaping hole in our roof"), no reviewer name. Storm-safety advice is general (stay off the roof, keep clear of water near wiring).
- E6 filler: no A6 phrases; cost FAQ does not open with the non-answer.
- E7 headers: one H1; every H2 a question with an entity; no city in any H tag; no skipped levels. COM-11: title remainder "Emergency Roof Repair" vs H1 remainder "Storm and Leak Emergency Roofing" — pass.
- E8 links: no cross-page link or link placeholder in prose/FAQ/opening; service-areas table placeholder present. Roof Repair's emergency FAQ is not duplicated (its "catch it and move what you can" text and its on-call sentence are not reused).
- E9 human: read-aloud pass done; reads like the owners talking.
- E10: grade 5.4, passes.
- Spec checks SVC-01–SVC-22: pass, except SVC-19 pending the 5 type confirmations and tarping (Submitted → blocks publication until answered). SVC-15: 4 FAQs, none matching siblings' questions. FAQ first sentences are short and stand alone; the 40–60 words sit across the first answer paragraph (F-015).

### Open
- Client answers needed: emergency types (service_scope, already asked 2026-10-11) and tarping yes/no (brief F2).
- Batch review (`/build … drafts`) once Metal Roofing, Slate Roofing and Skylights drafts exist.

## /build · 2026-10-12 · run 20261012-080147-build-944f

**Agent:** Build (Agent 2, Opus) · **Date:** 2026-10-12 · **Route:** A

### Done
- Drafted `clients/apex-roofing-of-the-lowcountry/build/services/SD - Metal Roofing - Apex Roofing of the Lowcountry.md` from the approved brief (`SB - Metal Roofing …`, approved 2026-10-12), spec `methodology/specs/service.md`. Header carries `replaces: [REDACTED]/metal-roofing-2/` (301 goes with the publish).
- Recorded: `status.py page-stage … svc-metal-roofing --stage draft` → "draft recorded" (re-recorded once after trimming the FAQ section).
- No new flag. The readability `--exclude-terms` file-vs-list mismatch and the FAQ 40–60-word first-sentence vs CM-047 tension are already flagged (F-015, run 20261012-074931-build-45cc); same workaround used.

### Draft facts
- About 1,040 words of body text (1,119 including headings and markers). Meta 157 chars (brief's proposed meta). Opening 103 words.
- H2 sections: delivery 294, types 227, FAQ 366 (incl. H3s and two NEED markers), service areas + CTA 73. All ≤ 375.
- Reading level: page average grade 6.7, no paragraph over 10 (E10 passes).
- 3 `[NEED]` markers: metal install steps (delivery step 3); cited source on metal over existing shingles in SC (FAQ 4 — drop the FAQ at approval if the researcher finds none, per brief); cited lifespan source for standing seam (FAQ 5).
- Spelling: "color" (US) used for the settled "colour".

### Stage 3 self-critique
- E1 portability: opening buyer state (coastal homeowner weighing metal vs shingles, HOA color approval) is unique on the site. The "coast is the reason" paragraph ties salt air/sun/humidity to concealed fasteners and coatings — metal-only. FAQ 3 problems list is general trade content, closed with Apex's settled scope. No sentence, quote or FAQ wording reused from Replacement, Installation, Inspections, Emergency or the pilot (no owners' "waves you can surf on"/"commodity" quote, no flashing paragraph, no tear-off steps).
- E2 specificity: Kynar 500 / Hylar 5000 coated standing seam with concealed fasteners and wind-uplift resistance (settled scope); color submittals and ARB submissions for HOA communities (settled scope + process); 40-year panel warranty against chalking and fading (Paul answer 4 — see Open); free consultation first and repair weighed against replacement (settled process); SC #57706 and Town of Bluffton #0620033323; Hearth financing.
- E3 variants: URL "metal roofing" → title "Metal Roofing" → H1 "Standing Seam Metal Roofs / Beaufort and Jasper Counties" → first H2 "put a metal roof on a home / South Carolina Lowcountry / Roofing Contractor". Opening: metro area + residential roofer + metal roofs. FAQ H2: metal roof + Lowcountry + Roofers. No consecutive repeat; reserved B1 unused.
- E4 chunks: all ≤ 375 words.
- E5 invention: no per-square price; only the whole-home standard ranges ($24,000–$45,000+ metal; $14,000–$20,000 shingles), stated as typical regional ranges that vary with roof size, not Apex's price. No W20 figure, no Ken Gathercole review, no CertainTeed Belmont, no lifespan figure, no hail/UL 2218 or energy claim, no wind/mph rating, no install duration, no re-coating/sealant/panel-replacement services (H3 kept to the assessment only), no Georgia, no commercial, no "best". "Customers often mention that the owners take the time to explain the products" is attributed, per brief §4. General trade statements only: what concealed fasteners and PVDF coatings are, the three common metal-roof problems, why a re-cover hides the deck.
- E6 filler: no A6 phrases; cost FAQ opens with the range, then drivers.
- E7 headers: one H1; every H2 a spoken question naming an entity; FAQ H2 avoids the siblings' "What Do … Ask a Lowcountry … About …?" frame; no city or community in any H tag; no skipped levels. COM-11: title remainder "Metal Roofing" vs H1 remainder "Standing Seam Metal Roofs" — different variant, pass.
- E8 links: no link or link placeholder in prose, FAQ or opening; service-areas table placeholder present.
- E9 human: read-aloud pass done.
- E10: grade 6.7, passes.
- Spec SVC-01–SVC-22: pass, except SVC-19 pending until the 40-year panel warranty has its fact record (W14 still Submitted in BG-D `d-warranty-terms`) and the two researcher NEEDs are resolved. SVC-15: 5 FAQs, none in C3 or sibling drafts. SVC-21: no outbound link (Finish candidate: the cited source for FAQ 4 or 5).

### Open
- **40-year panel-finish warranty needs a fact record before publication.** Paul confirmed it 2026-10-11 (answer 4); `d-warranty-terms` still reads W14 as Submitted. Record with `run.py fact` (open question `fact:d:warranty_terms`). Used three times on the page (types H3, FAQ 2, FAQ 5).
- Researcher: metal over existing shingles (SC/IRC source) and standing seam lifespan source.
- Batch review (`/build … drafts`) once Slate Roofing and Skylights drafts exist.

## /build · 2026-10-12 · run 20261012-080653-build-ad60

**Agent:** Build (Agent 2), Opus · **Date:** 2026-10-12 · **Route:** A

### Done
- Drafted `clients/apex-roofing-of-the-lowcountry/build/services/SD - Slate Roofing - Apex Roofing of the Lowcountry.md` from the approved brief (SB, revised 2026-10-12) and `methodology/specs/service.md`. 1,092 body words.
- Recorded: `status.py page-stage apex-roofing-of-the-lowcountry svc-slate-roofing --stage draft` (run 20261012-080653-build-ad60).
- Flag F-016 raised (readability.py `--exclude-terms` takes a file, the standard shows inline terms). Workaround: terms file in scratchpad.

### Stage 0/1 (map and plan, from the approved brief)
- Title `Slate Roofing - Apex Roofing of the Lowcountry` (46 chars) · meta 160 chars (brief wording) · H1 `Natural Slate Roofs in the South Carolina Lowcountry` · no "The Best" (BG-H2).
- Variant chain: URL slate roofing → title Slate Roofing → H1 Natural Slate Roofs / South Carolina Lowcountry → first H2 "lay a slate roof" / Beaufort and Jasper Counties / Roofer → opening: Hilton Head Island–Bluffton–Port Royal metropolitan area / roofing contractor → FAQ H2 slate / Lowcountry.
- Order: opening → delivery H2 → types H2 (Vermont, DaVinci, Repair H3s) → FAQ H2 (8 H3s, brief order) → service-areas H2 + placeholder → CTA.

### Stage 3 self-critique
- **E1 portability:** pass. Weight figures, sister rafters/purlins, City of Beaufort BAR, Vermont grades, DaVinci are slate-only. No sentence reused from Metal, Replacement, Installation, Inspections, Emergency or Roof Repair (checked: Replacement's "heaviest choice / weighs much less than real stone" not echoed; cost FAQ worded differently from Metal FAQ 1; repair FAQ is about slate tiles, not Roof Repair's repair-or-replace).
- **E2 specificity:** pass — Vermont slate in coastal-wind grades; DaVinci Roofscapes (Province Slate, virgin resins); 800–1,500 vs 200–350 lbs per square; City of Beaufort BAR; licence numbers.
- **E3 variants:** pass — no consecutive repeat; reserved B1 variant unused; B2 #1 in H1.
- **E4 chunks:** delivery 278 · types 218 · service areas 74 · **FAQ 382 words counting the H2/H3 lines and the two NEED markers** (≈ 305 of answer text). Marginally over the ~375 heading-inclusive count while 8 FAQs stand; falls well under once FAQ 3/5 are sourced-and-trimmed or dropped.
- **E5 invention sweep:** every fact from the brief's settled list. No price figure, no per-square price, no lifespan in years, no Belmont/CertainTeed, no Ken Gathercole review, no HHI ARB, no tapping, no underlayment, no duration, no re-nailing. Weight wording kept exactly. General trade statements (slate cracks underfoot; overlap needs pitch; colour is in the stone; tiles vary in colour/size/thickness) are general knowledge, no numbers. "Part of Westlake Royal Building Products" rests on the brief's cited source page (westlakeroyalbuildingproducts.com/roofing/davinci-roofscapes/...).
- **E6 filler:** pass; removed one "best" ("A good guide…" in FAQ 6). No A6 phrases.
- **E7 headers:** one H1; every H2 a spoken question with an entity; no city in any H tag (Beaufort and Jasper Counties = county variant; "Vermont" is a state, in the H3 product name); no skipped levels. COM-11: title remainder "Slate Roofing" vs H1 remainder "Natural Slate Roofs" — different variant, pass.
- **E8 links:** no cross-page link or `[LINK →]` in prose; service-area placeholder present.
- **E9 human:** reads as a slate roofer; explains square, sister rafters, purlins, penetrations, non-prorated.
- **E10 reading level:** page grade 6.6 (target ≤ 8.9); highest paragraphs 9.8 (FAQ 3, NEED text), 9.7 (types H2 heading line), 9.5 (FAQ 5) — none over 10. Read-aloud pass done.
- **Spec checks:** SVC-01–09, 11–14, 16–22 pass. **SVC-15 fails on count: 8 FAQs vs 4–6** — the brief set 8 (FAQ 3 and 5 drop if unsourced → 6). SVC-23 N/A.

### Open items (placeholders.py: 3)
1. `[NEED: slate install steps — underlayment, fastening, flashing, if they are to be described]` (delivery step 4)
2. `[NEED: cited lifespan source for natural slate roofs — researcher]` (FAQ 3)
3. `[NEED: cited minimum slope for slate roofing — researcher]` (FAQ 5)

### For the batch review
- FAQ 7 and FAQ 8 overlap (both land on DaVinci); FAQ 7 also repeats the DaVinci H3 (Province Slate, virgin resins). Candidate SEM row: merge or cut one.
- FAQ count: if FAQ 3 and 5 stay unsourced, drop them (brief rule) → 6 FAQs, SVC-15 and E4 pass.

### Not done
- No publish, no WordPress, no link table, no schema.

## /build · 2026-10-12 · run 20261012-081530-build-c16d

**Agent:** Build (Agent 2), Opus · **Date:** 2026-10-12 · **Route:** A

### Done
- Drafted `clients/apex-roofing-of-the-lowcountry/build/services/SD - Skylights - Apex Roofing of the Lowcountry.md` from the approved brief (SB - Skylights, approved 2026-10-12) and `methodology/specs/service.md`. 1,096 body words (869 visitor-facing words scored by readability.py).
- Recorded: `status.py page-stage apex-roofing-of-the-lowcountry svc-skylights --stage draft` (run 20261012-081530-build-c16d; re-recorded after the E1 rewrite).
- No new flag. The readability `--exclude-terms` file issue is already flagged (F-016); same workaround (terms file in scratchpad).

### Stage 0/1 (map and plan, from the approved brief)
- Title `Skylights - Apex Roofing of the Lowcountry` · meta 159 chars (brief wording) · H1 `Skylight Installation in Beaufort and Jasper Counties` · no "The Best" (BG-H2).
- Variant chain: URL skylights → title Skylights → H1 Skylight Installation / Beaufort and Jasper Counties → first H2 "add or fix a skylight" / South Carolina Lowcountry / Residential Roofer → opening: Hilton Head Island–Bluffton–Port Royal metropolitan area / roofer → FAQ H2 skylight / Lowcountry (no category term, per brief option).
- Headings re-worded from the brief's suggestions to avoid sibling shapes: first H2 uses "How Should …" (Replacement uses "How Does a Residential Roofer Replace …"); types H2 avoids Slate's "X, Y or a Repair: Which …" shape; FAQ H2 "Is a Skylight a Good Idea for Your Lowcountry Home?" avoids the "What Should … Know Before" (Slate) and "Which … Questions Do … Hear" (Metal) shapes.
- Order: opening → delivery H2 (5 steps) → types H2 (4 H3s) → FAQ H2 (5 H3s) → service-areas H2 + placeholder → CTA.

### Stage 3 self-critique
- **E1 portability:** pass after one rewrite. Leak-vs-fog diagnosis, curb and sealed unit, structural opening, ARB for street-visible skylights are skylight-only. Fixed two near-copies of sibling sentences (clean-up/magnet line was almost word-for-word Slate's; owner line matched Metal/Slate's "Ralph Brehany and his son Pierce own Apex, and both…"). Flashing H3 is about the skylight's own flashing and curb, not Roof Repair's chimney/wall/valley paragraph; the G "tube of silicone" quote is not reused. Emergency line uses the client's words, not Emergency's opener.
- **E2 specificity:** pass — rain = flashing/curb vs. no-rain fog = failed sealed unit; sealed-unit replacement and flashing/curb repair without a new unit; itemized written estimates; ARB for street-visible skylights in plantation communities; SC License #57706 and Town of Bluffton #0620033323.
- **E3 variants:** pass — no consecutive repeat; reserved B1 variant unused; B2 #4 in H1, B2 #1 in first H2.
- **E4 chunks:** delivery 332 · types 263 · FAQ 313 · service areas 75 (heading-inclusive) — all under 375.
- **E5 invention sweep:** no price, no per-square figure, no lifespan, no energy figure, no fixed-vs-venting claim, no warranty term, no install duration, no brand named outside the NEED marker, no Ken Gathercole review, no CertainTeed Belmont, no tubular or flat-roof skylights, no response time ("at any hour" considered and removed as a CM-049 24-hour risk). General trade explanations only (what flashing, a curb and a sealed unit are; heat and glare as a general downside; a roof replacement is a sensible time to decide on skylights). ARB step says "check with your community" — the brief does not settle that Apex prepares ARB paperwork for skylights.
- **E6 filler:** pass; no A6 phrases; cost FAQ opens with the main driver, not "costs vary".
- **E7 headers:** one H1; every H2 a spoken question naming an entity; no city or community in any H tag; no skipped levels. COM-11: title remainder "Skylights" vs H1 remainder "Skylight Installation" — "installation" is not in the filler list, and the brief/site plan set this H1 (F-012). Pass.
- **E8 links:** no cross-page link and no `[LINK →]` placeholder in prose or FAQ; service-area placeholder present.
- **E9 human:** reads as a roofer explaining a skylight job; trade terms explained in the next clause.
- **E10 reading level:** page grade 5.5 (≤ 8.9); highest paragraph 8.5 (cost FAQ); two paragraphs over 10 in the first pass (types H2 intro, metal FAQ) were split. Read-aloud pass done.
- **Spec checks:** SVC-01–09, 11–14, 16–22 pass. SVC-15: 5 FAQs (within 4–6); FAQ 5 drops if no cited source by draft approval → 4. SVC-23 N/A. FAQ first sentences run 16–42 words (spec says the answer is 40–60); FAQ 4 and 5 are short because their facts wait on cited sources.

### Open items (placeholders.py: 6, all `[NEED: …]`)
1. `[NEED: skylight install steps beyond cutting and framing the opening, if they are to be described]` (delivery step 3)
2. `[NEED: confirm Apex installs Velux and FAKRO — name the brands here only if yes]` (Full Skylight Replacement H3; client yes/no, brief F2)
3. `[NEED: cited source on skylight energy performance — researcher]` (FAQ 3)
4. `[NEED: cited manufacturer guidance on skylights for standing seam metal roofs — researcher]` (FAQ 4)
5. `[NEED: does Apex install skylights in standing seam metal roofs?]` (FAQ 4; client yes/no)
6. `[NEED: cited manufacturer source on fixed vs venting skylights — researcher; drop this FAQ if no source by draft approval]` (FAQ 5)

### For the batch review
- FAQ 4 (skylight on metal) touches Metal Roofing's scope; answers only the skylight side, no link.
- Delivery step 1 (leak diagnosis) sits close to Emergency FAQ "Is a leaking roof an emergency?" — different question (where vs. how urgent); check side by side.
- The meta names "emergency roof repair" (brief wording, Paul answer 7); the body's emergency line is one short paragraph.
- Researcher pass needed for items 3, 4, 6 (public facts — never asked of the client).

### Not done
- No publish, no WordPress, no link table, no schema, no Brand Guide write-back (that follows the batch's drafts approval).

## /build · 2026-10-12 · run 20261012-082058-build-4027

**Agent:** Build (Agent 2), Opus · **Date:** 2026-10-12 · **Route:** A

### Done
- Read all seven service drafts side by side (Roof Replacement, Roof Installation, Roof Inspections, Emergency Roof Repair, Metal Roofing, Slate Roofing, Skylights), each written in its own run (CM-043). Also read the approved pilot pages (Roof Repair, Bluffton) as the earlier-batch registry, because Brand Guide C1–C3 are still empty.
- Wrote the Stage 4 semantic review, report only, with no draft changed: `clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - services - REVIEW.md`. This is the path the step prescribes, used instead of `build/services/REVIEW - services batch drafts.md`.
- Recorded `status.py batch apex-roofing-of-the-lowcountry services --state drafts_written --sem-table <review> --sem-findings 15`. The per-page drafts were collected automatically.

### Cross-page claim checks
- Whole-home prices only, with no per-square price anywhere: pass. Slate's "per square" is a weight figure.
- Belmont is not named: pass.
- The Gathercole review is cited once, on Replacement only, with no name: pass.
- DaVinci is the only synthetic brand: pass.
- ShingleMaster is confirmed: pass.
- The B1 reserved variant is unused: pass.
- No in-prose links: pass.
- Every bracket is a NEED note: pass.
- Open: the 40-year metal warranty is stated three times on Metal while D `d-warranty-terms` still reads W14 as Submitted. It must be recorded as a fact before ship.

### SEM items (15; Paul picks)
1. Replacement: remove the "waves you can surf on" quote. Installation owns it (brief split).
2. Metal: say the 40-year warranty in the H3 and FAQ 5 only, and drop it from FAQ 2.
3. Metal: FAQ 2 stops restating FAQ 1's range in full; FAQ 3 shortens its repeat of the fasteners and coatings.
4. Replacement and Emergency: add review dates (July 2019, January 2024; the Emergency limb quote's date is looked up at apply).
5. Replacement: "Town permit" becomes "the permit" (county addresses).
6. Skylights: drop the on-call / high-priority sentence (it copies approved Roof Repair; Emergency owns it).
7. Emergency: cut within-page repeats (on-call three times, no-minimum twice, the tarp NEED twice).
8. Installation: cut within-page repeats (brand choice three times, underlayment thickness, street test, residential-only).
9. Metal: drop the standalone owners line, which near-copies Slate's.
10. Replacement, Metal, Slate, Skylights: vary the photos/clean-up step. Replacement's line copies pilot Roof Repair.
11. Inspections, Slate, Skylights: rework the openings that share sentence frames with siblings.
12. Installation (2 H2s), Inspections and Emergency FAQ H2s: reshape the headings that copy pilot Roof Repair's H2 templates.
13. Inspections: the storm-damage FAQ drops its signs list, which repeats its own H3 and Emergency's.
14. Slate: merge FAQs 7 and 8, and drop FAQs 3 and 5 if they are still unsourced, which brings the page to 5–6 FAQs.
15. Skylights: FAQ 4 (skylights on metal) stays only if the client confirms and a source is found; otherwise it goes to the blog list. Keep at least 4 FAQs.

### Open items (not fixed here)
- [NEED] counts: Replacement 2 · Installation 3 · Inspections 5 · Emergency 7 · Metal 3 · Slate 3 · Skylights 6.
- W14 fact row to record (`run.py fact … --id d-warranty-terms`).
- pilot_emergency_faq_link_cm022 is still open.
- C3 write-back after approval.

### Flags
- None new.

### Next
- Paul reviews the seven drafts with the review table and approves them with his SEM picks (`/approve apex-roofing-of-the-lowcountry batch:services:drafts --sem <ids>` or `--sem none`). Then apply-sem runs if he picks any items, then writeback.

## /interview · 2026-10-12 · run 20261012-114352-interview-44aa

## What changed
- `d-price-replacement-standard-2026` (facts.json): value now holds whole-home ranges only (asphalt about $14,000–$20,000; standing seam metal about $24,000–$45,000+; no per-square figures). Paul 2026-10-12.
- `fact:svc-slate-roofing:service_scope`: reopened and re-settled without CertainTeed Belmont (Paul: "not sure, skip"). Reopen logged as a process defect.
- `replacement_price_review`: logged as superseded. The Lowcountry whole-home ranges only, no per-square figures.

## Open for Paul
- Slate weight wording "per square" (800–1,500 lbs per square vs 200–350 for architectural shingles): keep, or reword as "per 100 sq ft"?

## /interview · 2026-10-12 · run 20261012-122518-interview-16a4

## What changed
- Recorded `d-warranty-terms` as paul_approved, with the 40-year metal panel warranty against chalking and fading (Paul 2026-10-11 answer 4).
- Recorded Paul's decisions: SEM items 1–15 all applied, with SEM-10 modified (process and standard stay in full on Emergency Roof Repair, Roof Replacement and Roof Installation; smaller services get a brief mention); Skylights FAQ 4 kept (yes, Apex installs skylights in metal roofs); Slate FAQs 3 and 5 dropped.
- Flag F-017: `scripts/approve.py` rejects SEM items 9–15 (the check accepts SEM-1 to SEM-8 only), so Paul's services drafts approval with `--sem 1,…,15` was refused. Needs a system session to widen the check.

## Open for Paul
- Services drafts approval is not recorded until F-017 is fixed in a system session.
- Brand Guide was re-approved after the warranty fact changed Section D.

## /build · 2026-10-12 · run 20261012-140216-build-c112

## What changed
All 15 SEM items Paul picked (2026-10-12) were applied to the 7 service drafts in `clients/apex-roofing-of-the-lowcountry/build/services/`. Changes #590–596 were logged.
- **Roof Replacement:** SEM-1 quote removed. SEM-5 "the permit". SEM-4 "A July 2019 review" and "A January 2024 review". SEM-10 clean-up and daily photos kept in full, reworded away from the pilot line.
- **Roof Installation:** SEM-8 brand paragraph, the "shows from the street" clause, "residential only" in the H3 and the FAQ 3 thickness sentence removed (FAQ 3 now points back to the underlayment section). SEM-12 delivery H2 "What Goes Into a New Home's Roof From Beaufort and Jasper Counties Roofers?" and FAQ H2 "What Should Builders Settle With a Lowcountry Roofer Before a New Roof Goes On?" SEM-10 one clean-up line added in new wording (Paul: process in full on this page).
- **Roof Inspections:** SEM-11 opening now leads with the buy, sell or after-storm decision. SEM-12 FAQ H2 "Which Inspection Questions Can a Lowcountry Residential Roofer Answer?" SEM-13 storm-signs sentence removed.
- **Emergency Roof Repair:** SEM-7 "no minimum" removed from step 1, FAQ 1 now ends with "call and describe what you see", duplicate tarping NEED removed from FAQ 3 (now 6 NEEDs). SEM-4 limb review dated July 2022 (from reviews.csv). SEM-12 FAQ H2 "When Should You Call Lowcountry Roofers About a Roof Emergency?" SEM-10 photos step now also covers debris and the magnet sweep, in new wording.
- **Metal Roofing:** SEM-2 FAQ 2 now says "a long finish warranty". SEM-3 FAQ 2 refers back to the price above, and FAQ 3 is shortened. SEM-9 standalone owners line removed. SEM-10 step 4 is now a brief mention.
- **Slate Roofing:** SEM-11 opening now leads with the older or historic home, with no "Maybe". SEM-14 FAQs 3 and 5 dropped (Paul), and FAQs 7 and 8 merged into "Who makes synthetic slate, and does it look like real slate?" (5 FAQs, 1 NEED). SEM-10 brief mention.
- **Skylights:** SEM-11 three "Maybe" sentences now one sentence. SEM-6 on-call sentence removed. SEM-15 FAQ 4 kept (Paul: yes, metal roofs), and the client NEED was removed. The researcher NEED stays. FAQ 5 "Do skylights open?" dropped (no source by approval). SEM-10 brief mention. 4 FAQs, 4 NEEDs.
- To meet CM-060 (40–60 words), these edited FAQ answers were adjusted: Emergency FAQ 1 (63, was 70), Metal FAQ 2 (60), Installation FAQ 3 (41), Skylights FAQ 4 (52, added one general sentence), Slate merged FAQ (51, added one general sentence).
- **Routed (decision logged):** Slate lifespan (PAA #84/#106, FO #112), Slate minimum slope and Skylights "Do skylights open?" (PAA #128) go to the blog list. The on-call message and the storm-damage signs stay with Emergency, which already has both.

## Checks
- Every edited element passes. E1: no shared lines across siblings or with the pilot. E2–E9 pass. E3 variant chains are intact and B1 is unused. E4: every H2 section is 375 words or fewer. E7: every H2 is a spoken question with an entity. E8: no links. FAQ counts are 4–6 on every page.
- **Still failing, in H2 sections the SEM edits touched but in sentences Paul did not pick (copy from the approved drafts, left as it was):**
  1. E10 · Replacement FAQ "What warranty comes with a new roof?", grade 10.1. Proposed fix: "A new shingle roof from Apex comes with two warranties. The maker's is a 50-year limited lifetime warranty. Apex adds a lifetime no-leak workmanship warranty."
  2. E10 · Slate FAQ "What is the biggest disadvantage of a slate roof?", grade 10.7. Proposed fix: split after "its weight." into "Natural slate is far heavier than architectural shingles, so not every house can carry it without extra framing."
  3. E10 · Slate types H2 intro, grade 10.1 (section not edited). Proposed fix: "Apex does three kinds of slate work. It puts on new roofs in genuine Vermont slate or DaVinci Roofscapes synthetic slate. It also repairs slate roofs that are mostly sound."
  4. CM-060 · first FAQ paragraph over 60 words: Metal "How much does a metal roof cost?" (80), Installation "Is drip edge required in South Carolina?" (72), Skylights "How much does it cost to install a skylight?" (62, section not edited).
- State: **sem_check_failed**. The drafts go back to Paul.

## Open for Paul
- Approve the four fixes above as written, or change them. They are all sentence splits and trims, with no new facts.
- Paul's yes on skylights in metal roofs (2026-10-12) is logged as a decision only, not as a fact row. The page does not state it as Apex's claim.
- The researcher still owes sources for the remaining NEEDs: Replacement 2 · Installation 3 · Inspections 5 · Emergency 6 · Metal 3 · Slate 1 · Skylights 4.

## /build · 2026-10-12 · run 20261012-142751-build-99a8

**Agent:** Agent 2 — Build (Opus) · **Date:** 2026-10-12

### What was done
SEM items 1–15 were already applied in the previous run, so they were not applied again. This run applied the six fixes Paul approved. Text came from the previous run's scratch `apply_proposed.py`, and Metal Roofing used the price ranges Paul chose.

| # | Page · section | Before | After |
|---|---|---|---|
| 1 | Roof Replacement · FAQ "What warranty comes with a new roof?" | flagged grade 10.1 (section 9.1) | section grade 7.1 · p1 58 words |
| 2 | Slate Roofing · FAQ "What is the biggest disadvantage of a slate roof?" | grade 10.7 (paragraph over 10, E10 FAIL) | grade 4.9 · p1 55 words |
| 3 | Metal Roofing · FAQ "How much does a metal roof cost?" | p1 80 words · grade 6.6 | p1 60 words · grade 4.4 |
| 4 | Roof Installation · FAQ "Is drip edge required in South Carolina?" | p1 72 words · grade 8.6 | p1 58 words · grade 4.7 · Apex-practice [NEED] kept |
| 5 | Skylights · FAQ "How much does it cost to install a skylight?" | p1 62 words · grade 8.3 | p1 60 words · grade 8.1 |
| 6 | Slate Roofing · types H2 intro "Natural, Synthetic or a Repair…" | flagged grade 10.1 (section 9.2) | grade 2.4 |

These are the Metal ranges Paul chose (settled `metal_cost_ranges`). Standing seam on a typical home runs about $16,600 to $32,000 or more. Coastal Lowcountry homes run about $30,000 to $45,000 or more. The draft says these are regional ranges from published cost guides, that Apex's price will differ, and that the free estimate gives the real figure. The Metal draft no longer contains $24,000.

### Decisions recorded
- `emergency_faq_63_words_waived`: Paul is keeping the Emergency Roof Repair FAQ "Is a leaking roof an emergency?" at 63 words. He waived the CM-060 60-word limit for this FAQ, and the FAQ was not changed.
- `exclude_terms_accepted`: Paul accepted the exclude-terms list used for the readability checks under CM-047. The list is in the previous run's scratch `terms.txt`.
- `metal_cost_ranges`: the metal price ranges listed above.

### Checks on the changed sections
- **Readability** (`readability.py --exclude-terms terms.txt`): E10 passes on all five changed pages, and no paragraph is over grade 10. Page averages are Roof Replacement 5.0, Slate 6.0, Metal 6.2, Roof Installation 5.2 and Skylights 6.0. Emergency Roof Repair was not changed and also passes at 5.1.
- **CM-060:** every changed FAQ opens with a short first sentence and has a first paragraph of 55–60 words. Every other FAQ in the batch is between 40 and 60 words, except the waived Emergency FAQ at 63.
- **E1–E10 and spec checks:**
  - No new claim about Apex was added.
  - The new public facts come from Paul's approved research: the drip-edge code (R905.2.8.5, SC Reg 8-1228), the slate weight per square and the 2–3x cost, and the metal ranges.
  - The changed FAQs have no links. No heading changed.
  - `placeholders.py`: every bracket is a `[NEED: …]`. Pass.
- Both earlier failures in untouched sections now pass: the Skylights cost FAQ (fix 5) and the Slate types H2 intro (fix 6).

### Batch state
`services` → **sem_applied** with `--checks-passed`. The approval is pinned to the applied versions, so Paul is not stopped again. Next step is `writeback services`.

### Open item for Paul (not changed — instruction D)
The Roof Replacement FAQ "What does a roof replacement cost in South Carolina?" still says standing seam metal costs "about $24,000 to $45,000 or more". The Metal page now gives $16,600–$32,000+ for a typical home and $30,000–$45,000+ for coastal homes, so the two sibling pages disagree. Paul can align Roof Replacement with the Metal ranges, which is a one-sentence change he would need to re-approve, or keep it as it is.

## /build · 2026-10-12 · run 20261012-143054-build-3339

**Agent:** Agent 2 — Build (Opus) · **Date:** 2026-10-12

### What was done
Paul asked for this revision: the Roof Replacement cost FAQ now uses the same metal ranges as the Metal Roofing page (settled `metal_cost_ranges`). Only the first paragraph of the FAQ "What does a roof replacement cost in South Carolina?" changed.

- **Before:** "Standing seam metal runs about $24,000 to $45,000 or more. Both ranges move up or down with the size of your roof."
- **After:** "Standing seam metal runs about $16,600 to $32,000 or more for a typical home. Coastal Lowcountry homes often run about $30,000 to $45,000 or more. These are regional ranges from published cost guides; Apex's price will differ."
- The sentence "Both ranges move up or down with the size of your roof" was removed for two reasons. The paragraph now gives three ranges, so "Both" was wrong. Keeping the sentence would also make the paragraph 67 words, which breaks CM-060. Roof size is still covered by the cost-driver list that follows.
- The free-estimate line was already in the FAQ's last paragraph, so it was not changed.
- $24,000 no longer appears anywhere in the draft.
- No Brand Guide change and no fact rows.

### Checks on the changed section
- **CM-060:** the first paragraph is 56 words, with a short first sentence. Pass.
- **E10 / CM-047** (`readability.py`, with the accepted exclude-terms list rebuilt from decisions-settled `exclude_terms_accepted`): the section is grade 5.2 and the page average is 5.1. No paragraph is over grade 10. Pass.
- **E4:** the FAQ H2 section is 362 words, within the 375 limit. Pass.
- **E5:** every figure comes from the settled `metal_cost_ranges`. Pass.
- **E3, E7, E8:** no variant or heading changed, and there are no links. Pass.
- **Placeholders:** the only brackets are the 2 existing `[NEED: …]` notes. Pass.
- **E1:** the metal sentences match the Metal page's wording. Paul asked for this so the two pages stay consistent, so it is not a portability failure.
- **Emergency FAQ waiver:** the 63-word waiver still stands.

### Batch state
`services` → **sem_applied** with `--checks-passed`. Next step is `writeback services`.

### Note for Paul (not changed)
The next paragraph starts "These are typical ranges for the area, not a quote." The new sentence just before it starts "These are regional ranges…", so two sentences in a row now open with "These are". This is minor. If Paul wants it fixed, he can delete the second sentence, which is a one-line change.

## /build · 2026-10-12 · run 20261012-150342-build-474a

**Step:** Brand Guide content write-back for batch `services` (P8), right after Paul's drafts approval (2026-10-12, SEM applied).

**Done**
- Brand Guide B3 (assignment log): 9 rows — the 7 services pages plus the 2 pilot pages (Roof Repair, Bluffton). Each row gives the category and area variants used in the H1 and H2s and the approved content file. Change #628.
- Brand Guide C1 (service pages): 8 rows (7 services + pilot Roof Repair) with the H1 service variant and status. C2 (location pages): pilot Bluffton row. Change #629.
- Brand Guide C3 (heading and FAQ registry): 78 rows (every H2 and FAQ question on the 9 approved pages). No question or H2 appears on two pages. Change #630.
- Brand Guide copied to Drive (`drive.py upload`).
- `status.py writeback apex-roofing-of-the-lowcountry services` recorded (exit 0).

**Checks**
- The reserved homepage variant (B1, "Hilton Head Island Metropolitan Area") appears on no approved page.
- The H1s match the approved site plan for all 7 services pages.

**Notes / open**
- The pilot batch's content (Roof Repair, Bluffton) had never been written into B3/C1/C2/C3 (the pilot shipped under the earlier flow). It is added now so the locations batch does not reuse its variants, headings or FAQs. Only the services batch write-back was recorded in status; the pilot batch's own status record was not changed.
- C2 "GBP landing page?" for Bluffton is not recorded in the Brand Guide; Section F must answer it before schema (BB-604).
- From the services semantic review (not this step): the 40-year metal panel warranty (W14) still reads Submitted in D (`d-warranty-terms`); it needs a fact row before ship.
- Edits were made only in B3 and C1–C3, which are outside the approved Brand Guide sections, so brand_guide_approved stands.

**Next:** `/build apex-roofing-of-the-lowcountry write locations` (the locations batch reads B3/C1–C3).

## /build · 2026-10-12 · run 20261012-150859-build-1044

**Route:** A. **Scope:** evidence gate + briefs for 11 location pages (CM-041, CM-054, CM-057).

### Evidence gate (`evidence.py run --batch locations`)
None blocked; every page cleared and got a brief.
- PASS (6): loc-hilton-head-island, loc-okatie, loc-beaufort, loc-port-royal, loc-st-helena-island, loc-hardeeville
- WARN (5): loc-pritchardville, loc-ladys-island, loc-fripp-island, loc-ridgeland, loc-levy. Each has a required gap (neighborhoods) and its brief carries `## Evidence gaps`.

### Research first (CM-057, P6)
Three researcher subagents (Sonnet) looked up the public gaps and FAQ sources for all 11 pages. Their output is copied to `build/locations/research-2026-10-12/<page>.json`.
- Now sourced: Lady's Island neighborhoods (12, from a county staff report), Things to Do and Top Sites; Okatie (Callawassie Island, two NRHP top sites); a St. Helena Things to Do; Fripp POA "neighborhoods" (villa regimes); Levy is in Jasper County.
- Not found: neighborhoods for Pritchardville, Ridgeland and Levy; anything for Levy.
- **Not on the grids:** recording these in `build/evidence/<page>.facts.json` was blocked (the guard stops inline scripts, and the permission classifier denied a scratchpad script). Flag **F-018** asks for a script to record a page fact. The briefs cite the research as "public research 2026-10-12 — not yet on the grid". The grids for Lady's Island, Okatie, St. Helena and Fripp therefore understate what is known.

### Briefs
- 11 briefs, each from its own brief-writer subagent (Sonnet), in `build/locations/LB - <City> - Apex Roofing of the Lowcountry.md`.
- Each was recorded with `status.py page-stage … --stage brief`, and the batch briefs were collected.
- **Build batch check:**
  - Variant chains are correct on all 11 pages: title "Roofing Contractor", H1 "Roofers", first H2 rotates Roofing Contractor / Roofer / Residential Roofer.
  - No FAQ repeats a C3 entry.
  - The sibling-cities H2 "Which Other Lowcountry Towns Do We Serve?" was on Port Royal, Ridgeland and Levy. Each now names its own town (BB-316).

### FAQ status (spec needs 3–4)
| Page | Usable | Conditional or Paul's call | Gaps |
|---|---|---|---|
| Fripp Island | 3 (two carry client `[NEED]`s) | — | — |
| Beaufort | 2 | Bailey Bill | — |
| Port Royal | 2 | Parris Island (open client question) | — |
| Hilton Head Island | 2 | Town flood rule | — |
| Ridgeland | 2 | — | 1 |
| Lady's Island | — | City/County jurisdiction; County flood rule; Dataw (not on Lady's Island) | — |
| St. Helena Island | — | Harbor Island; Cultural Protection Overlay | 1 |
| Okatie | — | Spring Island / Callawassie | 2 |
| Hardeeville | 1 (statute wording to verify) | — | 2 |
| Levy | 1 | — | 2 |
| Pritchardville | 0 | — | 3 |

**Batch overlap:** flood-rule questions are proposed on Hilton Head Island, Port Royal and Lady's Island. Keep at most one, and choose before the drafts.

### Open for Paul
1. The briefs approval (each brief's Flags for Paul section lists its options).
2. Thin pages: Pritchardville and Levy fail LOC-14, LOC-15 and LOC-17 on public sources, and Ridgeland and Okatie fail LOC-15. Options:
   - (a) client/Paul local knowledge, then the researcher verifies it
   - (b) accept `[NEED]` sections and hold the page from publication
   - (c) for Levy, decide whether it keeps a page (Paul's URL decision)
3. Dataw FAQ does not fit Lady's Island. Options: drop it, keep it as "nearby islands" if the client confirms, or move it.
4. Client facts still open:
   - Apex's work in named communities (Spring Island, Callawassie, Harbor Island, Dataw)
   - Port Royal base housing
   - a Fripp contractor decal
   - a Jasper County business licence
   - W16 (`fact:d:services_subcontracted` is still listed as waiting, although Paul re-confirmed it on 2026-10-11)
5. Brand Guide F (NAP) is still empty and needs filling before Finish.
6. The Port Royal facts file says Mossy Creek "extends into Beaufort"; the source doesn't say so. The briefs don't use it.

### Flags raised
- F-018: no script to record page facts from research (workaround above).

### Not done (by design)
No drafts, no WordPress, no links, no schema, no gates set.

## /build · 2026-10-12 · run 20261012-205526-build-9baf

- Replaces aborted run 20261012-161352-build-02ea (stalled, 0 changes; Paul chose abort, 2026-10-12).
- Paul's answers recorded: run.py fact d-communities-worked-outside-the-12-towns (new, paul_approved); d-services-subcontracted-out source updated. Settled: services_subcontracted_new_construction (closes fact:d:services_subcontracted), communities_outside_towns, location_client_questions_skipped, port_royal_mossy_creek, fripp_roofer_after_roofers, dataw_nearby_islands, flood_rule_faq_overlap_kept, hhi_faq_kept, lowcountry_research_used. Asked: brand_guide_f_address (Paul). Reopen requested: site_plan_open_choices (2a permit FAQs).
- Researcher (Sonnet) round 2: 12 public gaps logged RL-locations-1..12; results in build/locations/research-2026-10-12/round2.json; Bailey Bill verified, wording fixed (fair market value).
- Page facts files updated (8): ladys-island, port-royal, st-helena-island, okatie, fripp-island, ridgeland, levy, pritchardville (changes #656–663). Evidence gate re-run: 11/11 PASS; packs in build/locations/packs/.
- 11 briefs revised and recorded; changes #664–674. FAQs rebuilt to 3 per page (location-faq.md), brand-level fallbacks distinct per page, under-target sections trimmed or dropped (CM-061 §8).
- Flag F-019 (sources list additions). Open: Paul's A/B on 2a (Okatie, Levy, Pritchardville FAQ), then batch:locations:briefs approval with brand_guide_approved riding on it.

## /build · 2026-10-12 · run 20261012-212825-build-fdce

- Settled site_plan_open_choices: 2a revised to option A (Paul 2026-10-12) — who-issues-the-permit FAQ on Okatie, Levy and Pritchardville, each from its own jurisdiction's source, no Apex-pulls-the-permit claim; 1a, 3b, 4a, 5a unchanged.
- Settled brand_guide_f_address (closes the open question): Section F confirmed NAP = 6 Sutton Ct, Bluffton, SC 29910 in schema (matches website and BBB); GBP stays SAB with the address hidden. Fact f-confirmed-nap (paul_approved); Brand Guide F row filled (change #683).
- Briefs: Okatie FAQ 3, Levy FAQ 1 (jurisdiction folded into the permit answer), Pritchardville FAQ 2 resolved to option A; B alternatives and open markers removed; 3 FAQs per page kept (#684–686). CM-011 outbound rows updated to name the cited permit offices as Finish candidates (#687–689; Okatie row added).
- Open: Paul's one-line approval of batch:locations:briefs with brand_guide_approved. Flag F-019 (sources list) is for a /system session.

## /build · 2026-10-13 · run 20261012-213607-build-27a0

**Step:** the locations section's one Brand Guide write-back (CM-061), at the brief approval (batch locations briefs approved by Paul 2026-10-12). Route A.

**Done**
- Brand Guide B3 (assignment log): 11 rows, one per location page (Hilton Head Island, Okatie, Pritchardville, Beaufort, Port Royal, Lady's Island, St. Helena Island, Fripp Island, Hardeeville, Ridgeland, Levy). Each row gives the category variants from the brief's variant chain (H1 "Roofers"; the services H2, FAQ H2 and opening variants), the area terms (the town, plus the county or "Beaufort and Jasper Counties" in the opening, and "Lowcountry" in the Port Royal and Hardeeville sibling H2s) and the approved brief file. Change #704.
- Brand Guide C2 (location pages): 11 rows. GBP landing page: No for all (the GBP Website field points at the homepage, BG-A11). Status: briefs approved 2026-10-12, draft not yet written. C1 unchanged (no service pages in this section). Change #705.
- Brand Guide C3 (heading and FAQ registry): 107 rows, 74 H2s and 33 FAQ questions (3 per page), as briefed. Levy has no Things to Do or Top Sites H2, and Pritchardville no Things to Do H2 (both dropped: researched, not found). No H2 or question appears twice, inside the section or against the existing 78 rows. Change #706.
- Fact rows regenerated from facts.json (`facts.py render`): nothing changed.
- Brand Guide copied to Drive (`drive.py upload`).
- `status.py writeback apex-roofing-of-the-lowcountry locations` recorded (exit 0).

**Checks**
- No new row uses the reserved homepage variant (B1, "Hilton Head Island Metropolitan Area").
- Every H1 matches the approved site plan ("Roofers in/on <town>").
- The flood-rule questions on Hilton Head Island, Port Royal and Lady's Island are kept, as Paul decided (settled `flood_rule_faq_overlap_kept`). Each is worded for its own place.

**Approved values**
- Only B3, C2 and C3 were edited. They sit outside the approved Brand Guide sections, and the fact rows did not change. brand_guide_approved stands. It was already re-approved on the locations briefs line (2026-10-12).

**Flag F-020**
- C3 holds the headings as briefed, but the briefs let the writer re-word headings. Drafts never write the Brand Guide, so a re-worded heading would leave C3 out of date. Workaround: the draft review holds drafts to the briefed headings, or lists each re-word as a Fix-and-list row.

**Open [NEED]s carried by the briefs (for the drafts, not this step)**
- Hardeeville: verify the statute wording against the scstatehouse.gov text before quoting it.
- Fripp Island FAQ 2: a cited FEMA source on high-wind roof installation.
- Lady's Island FAQ 2: the Beaufort County Floodplain Administrator to confirm the cumulative period.

**Next:** `/build apex-roofing-of-the-lowcountry write locations`: drafts, one fresh subagent per page, then the draft review.

## /build · 2026-10-13 · run 20261013-070640-build-ff69

**Agent:** Build (Agent 2), Opus, fresh subagent for this one page (CM-043; agent id `build-subagent-loc-hilton-head-island-ff69`) · **Date:** 2026-10-13 · **Route:** A

### Done
- Drafted `clients/apex-roofing-of-the-lowcountry/build/locations/LD - Hilton Head Island - Apex Roofing of the Lowcountry.md` from the approved brief (LB - Hilton Head Island, briefs approved 2026-10-12), `methodology/specs/location.md`, `methodology/location-faq.md` and the evidence pack `build/locations/packs/loc-hilton-head-island.md`. About 900 body words (667 visitor-facing words scored by readability.py), under the 1,000 ceiling.
- Recorded: `status.py page-stage apex-roofing-of-the-lowcountry loc-hilton-head-island --stage draft --run 20261013-070640-build-ff69 --agent build-subagent-loc-hilton-head-island-ff69` (exit 0).
- No new flag. The readability `--exclude-terms` issue is already flagged (F-016); same workaround (terms file in scratchpad).

### Stage 0/1 (map and plan, from the approved brief)
- Title `Apex Roofing of the Lowcountry - Roofing Contractor - Hilton Head Island, South Carolina` · meta 159 chars (brief wording) · H1 `Roofers on Hilton Head Island` · no "The Best" (BG-H2, settled cm020).
- Variant chain: URL hilton-head-island → title Roofing Contractor → H1 Roofers → first H2 Roofing Contractor → opening roofer / roofing contractor + Hilton Head Island, SC · Beaufort County → FAQ H2 Roofer. Reserved B1 variant and "metro area" unused.
- Order (CM-023): opening → services H2 (8 H3s, placeholder row) → local context H2 → FAQ H2 (3 H3s) → neighborhoods H2 (8 list items) → map → Things to Do H2 (4) → Top Sites H2 (4) → sibling cities H2 (placeholder row) → CTA with NAP (no H tag).
- Every H2 and FAQ question is the C3/briefed wording, unchanged (F-020: nothing re-worded).

### Stage 3 self-critique
- **E1 portability:** pass. Opening angle (plantation review boards, Sea Pines and Palmetto Dunes) and local context (listed elevation 0 ft, sea island north / barrier island south, Broad Creek marsh, 1893 surge, 40.3% of 29,018 units vacant) are island-only. Table lead-in, neighborhoods lead-in, sibling lead-in and CTA line re-worded so none copies Bluffton's sentences; the permit sentence is re-worded from Bluffton's.
- **E2 specificity:** pass, 5+ (elevation and sea/barrier island geography; 1893 Sea Islands Hurricane 16-ft surge; 2020 housing units and vacancy; Sea Pines and Palmetto Dunes board rules incl. the 1 Jan 2026 effective date; the Town's 49% threshold).
- **E3 variants:** pass — no consecutive repeat; assigned variants used; B1 reserved unused.
- **E4 chunks (heading-inclusive words):** services 47 · local context 118 · FAQ 371 · neighborhoods 53 · Things to Do 91 · Top Sites 56 · siblings 54 — all ≤ 375 (FAQ trimmed from 505 in the first pass: Sea Pines sample/default-shingle detail, Palmetto Dunes wind/fire-rating line and the Zone VE elevation rule cut).
- **E5 invention sweep:** pass. No price, lifespan, response time, warranty, licence, rating, reviewer name or review content. No claim that Apex has worked in Sea Pines, Palmetto Dunes or Hilton Head Plantation. No Palmetto Dunes colour names. No Florida 3,000-ft code rule. Re-roof vs the 49% test left to the Town. Salt-air answer is FEMA 2004 guidance only, stated as not an SC/Beaufort code; no "Apex uses stainless nails". Apex's own part uses settled facts only (metal colour submittals and ARB submissions for HOA communities; Town permit on a replacement).
- **E6 filler:** pass; no A6 phrases.
- **E7 headers:** one H1; every H2 a spoken question naming Hilton Head Island; no skipped levels. COM-11: title remainder "Roofing Contractor" vs H1 remainder "Roofers" — pass.
- **E8 links:** no link or `[LINK →]` in prose, FAQ or local context; both link-table placeholder rows present.
- **E9 human:** reads as a local roofer explaining island rules; trade terms explained in the next clause (review board, underlayment, zinc-coated).
- **E10 reading level:** page grade 7.0 (≤ 8.9); highest paragraph 9.7 (neighborhoods); three paragraphs over 10 in the first pass split. Read-aloud pass done. FAQ first answer paragraphs 47 / 46 / 55 words (40–60).
- **Spec checks:** LOC-01–07, 09–13, 15, 17–25 pass; LOC-08 N/A; LOC-14 pass (3 FAQs, all island-only, none elsewhere in C3 except the settled flood-rule overlap, worded for the Town's own source); LOC-16 open (map placeholder); LOC-26 recommendation only (WebPage + ItemList, no LocalBusiness); LOC-27 N/A.

### Open items (placeholders.py: 1)
1. `[NEED: city-level map embed of Hilton Head Island, SC — not the Google Business Profile map]` — written as a NEED note, not the brief's `[Map: …]` wording (P11 forbids instruction brackets; the approved Bluffton pilot still carries `[Map: …]`).
- Link-table rows `| [Link wheel: populate service links here] |` and `| [Link wheel: populate sibling-city links here] |` (spec §6 form; Finish fills).

### For the draft review
- FAQ categories (location-faq.md asks one per category): the brief assigns two "local decision" FAQs (plantation boards, Town flood rule) and one "trust" FAQ (salt air), no logistics FAQ — kept as briefed and approved; the checker may list it.
- Things to Do: the pack gives no fact for the Arts Center of Coastal Carolina; the item reads "the arts center on the island" only.
- Salt-air FAQ sits closest to Fripp Island's oceanfront answer — this one stays on fasteners only.
- Flood-rule FAQ overlaps Port Royal and Lady's Island (settled `flood_rule_faq_overlap_kept`); compare wording side by side.
- Outbound authority candidates for Finish (CM-011): https://pdpoa.org/about/arb/ (FAQ 1), the FEMA advisory (FAQ 2).

### Not done
- No publish, no WordPress, no link table, no schema, no Brand Guide write-back (drafts never write it, CM-061).

