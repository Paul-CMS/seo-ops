# Safety log — Apex Roofing of the Lowcountry

Append-only. Every command writes STARTED before it acts and FINISHED after. Every change lists URL, old value, new value and result.
Machine-readable mirror for /rollback: changes.jsonl.


## RUN 20261005-210907-new-client-b5e9 · STARTED · /new-client · 2026-10-05T21:09:07-05:00
Step: new-client
- DECISION 2026-10-05T21:09 · run 20261005-210907-new-client-b5e9 · Paul: safe-fix cap for alt_text set to 5
- DECISION 2026-10-05T21:09 · run 20261005-210907-new-client-b5e9 · Paul: safe-fix cap for broken_link set to 2
- CHANGE #1 [drive_file] https://drive.google.com/drive/folders/1DN9Lji_McIOo9i2eFLV-u7eXrvY00G37 | folder | old:  | new: Apex Roofing of the Lowcountry - TMS (01 - Discovery and Audit/{Evidence,Deliverables}, 02 - Build, 03 - Finish, 04 - Blog, _Archive) | result: created
### HANDOFF · /new-client · 2026-10-05 · run 20261005-210907-new-client-b5e9
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
### END HANDOFF
## RUN 20261005-210907-new-client-b5e9 · FINISHED · 2026-10-05T21:10:52-05:00
Changes: 1 · Summary: Client set up

## CONDITION · 2026-10-05T21:10:52-05:00 · Client set up (/new-client finished) — met (system-verified)

## RUN 20261005-211116-wp-check-0f33 · STARTED · /wp-check · 2026-10-05T21:11:16-05:00
Step: wp-check
Gates checked: client_setup
- CHANGE #2 [other] https://apexroofingtlc.com/wp-admin/user-new.php | User seo-ops | old: no seo-ops user | new: Add user: username seo-ops, role Editor (never Administrator). Use an agency email you control. | result: HANDOFF ISSUED to Jonie | ref H-2026-10-05-01-other-01
- CHANGE #3 [other] https://apexroofingtlc.com/wp-admin/users.php | Application Password | old: none | new: Users → seo-ops → Application Passwords → name it seo-ops → Add. Copy the password once and send it to Paul privately (password manager share or by phone — nev… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-05-01-other-02
- CHANGE #4 [other] https://apexroofingtlc.com/wp-admin/plugins.php | SEOPress version | old: unknown | new: Record only (change nothing): is SEOPress installed and active, and which version? Note it here. 6.8 or later is needed; if older or missing, mark blocked and … | result: HANDOFF ISSUED to Jonie | ref H-2026-10-05-01-other-03
- CHANGE #5 [other] https://apexroofingtlc.com/wp-admin/options-permalink.php | Permalinks | old: unknown | new: Record only (change nothing): the permalink setting. Must not be "Plain". Note what it is. | result: HANDOFF ISSUED to Jonie | ref H-2026-10-05-01-other-04
- CHANGE #6 [other] https://apexroofingtlc.com/wp-admin/plugins.php | Security plugin | old: unknown | new: Record only (change nothing): any security plugin (Wordfence, Solid Security, All In One WP Security, Disable REST API) or host firewall that could block /wp-j… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-05-01-other-05
### HANDOFF · /wp-check · 2026-10-05 · run 20261005-211116-wp-check-0f33
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
### END HANDOFF
## RUN 20261005-211116-wp-check-0f33 · FINISHED · 2026-10-05T21:11:38-05:00
Changes: 5 · Summary: WordPress setup handoff issued to Jonie; connection test waits for credentials

## RUN 20261005-211145-drive-mirror-3ea9 · STARTED · /drive-mirror · 2026-10-05T21:11:45-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #7 [drive_file] https://drive.google.com/file/d/1xjKRRsQFihLC5BZCr2YbT8SlshxuUDkl/view | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 19890a697a4c | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-211145-drive-mirror-3ea9/0007-new.md
- CHANGE #8 [drive_file] https://drive.google.com/file/d/1obnlpMw1OavfmWrdLmPSqgA03WO29rcO/view | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Approval Record.md · sha 5aefc2a6d4aa | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-211145-drive-mirror-3ea9/0008-new.md
- CHANGE #9 [drive_file] https://drive.google.com/file/d/1Fhz6qpIWOYDLHp2OIBH6iOo3CTEgSA_L/view | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 393d6e4acc83 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-211145-drive-mirror-3ea9/0009-new.md
### HANDOFF · /drive-mirror · 2026-10-05 · run 20261005-211145-drive-mirror-3ea9
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
### END HANDOFF
## RUN 20261005-211145-drive-mirror-3ea9 · FINISHED · 2026-10-05T21:12:50-05:00
Changes: 3 · Summary: Records mirrored to Drive (first upload)

## RUN 20261005-211303-discovery-aee7 · STARTED · /discovery · 2026-10-05T21:13:03-05:00
Step: discovery:discovery
Gates checked: client_setup
- CHANGE #10 [drive_file] https://drive.google.com/file/d/1rwCwFByhKeO4g2NQbZeYuWharwMBGP1C/view?usp=drivesdk | file | old:  | new: Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | result: uploaded
- CHANGE #11 [drive_file] https://drive.google.com/file/d/1KRun10jn91aLeCsUkm-lmzq-NZj_jtmN/view?usp=drivesdk | file | old:  | new: Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05.md | result: uploaded
- CHANGE #12 [audit_step] S01 | Intake facts: website, GBP link, storefront/SAB, exact GBP W | old:  | new: done | result: DONE — Intake facts complete from the client record (GBP link, SAB, GBP Website field, no GSC/GA4, WordPress/Kadence); nothing missing
- CHANGE #13 [audit_step] S02 | Public discovery: live site, GBP, social, review profiles, S | old:  | new: done | result: DONE — Live site (sitemap pages), public GBP view, BBB, HomeAdvisor list page, Facebook, RDAP, OpenCorporates copy of SC SOS read. Not read: SC SOS primary and SC LLR (both CAPTCHA), GBP secondary categories/service areas/open date (limited view), HomeAdvisor profile (403), Yelp/Angi/Nextdoor/Apple/Bing
- CHANGE #14 [audit_step] S03 | Entity research: category entity (Wikipedia), area entity (R | old:  | new: done | result: DONE — Category entity Roofing contractor (Wikipedia Roofer, Q552378); area entity Hilton Head Island-Bluffton-Port Royal SC MSA (Q17020871) by Russian Doll from Bluffton, contains all 12 location-page cities; variants, reserved homepage variant and Wikidata URIs proposed. Open: Georgia service-area conflict (C1)
### HANDOFF · /discovery · 2026-10-05 · run 20261005-211303-discovery-aee7
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
### END HANDOFF
## RUN 20261005-211303-discovery-aee7 · FINISHED · 2026-10-05T21:26:51-05:00
Changes: 5 · Summary: Discovery and entity foundation proposed (public sources)

## RUN 20261005-212655-drive-mirror-c34f · STARTED · /drive-mirror · 2026-10-05T21:26:55-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #15 [drive_file] https://drive.google.com/file/d/1xjKRRsQFihLC5BZCr2YbT8SlshxuUDkl/view | archive | old: Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-05.md | result: done · renamed and moved, nothing deleted
- CHANGE #16 [drive_file] https://drive.google.com/file/d/15LibutpKZwORcfYnNgMqGkSFcu4PYVJr/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-05.md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha b266a5de2221 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-212655-drive-mirror-c34f/0016-new.md
- CHANGE #17 [drive_file] https://drive.google.com/file/d/1Fhz6qpIWOYDLHp2OIBH6iOo3CTEgSA_L/view | archive | old: Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-05.md | result: done · renamed and moved, nothing deleted
- CHANGE #18 [drive_file] https://drive.google.com/file/d/1Zy6ltDSL75b_yR7v1n0dNDKpVilTfrQy/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-05.md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 5a9830b56085 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-212655-drive-mirror-c34f/0018-new.md
- CHANGE #19 [drive_file] https://drive.google.com/file/d/1XD4qhquLAI94tS1-_PseCh_kVW8VeIsJ/view | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha 33f0aefc0a42 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-212655-drive-mirror-c34f/0019-new.md
### HANDOFF · /drive-mirror · 2026-10-05 · run 20261005-212655-drive-mirror-c34f
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
### END HANDOFF
## RUN 20261005-212655-drive-mirror-c34f · FINISHED · 2026-10-05T21:28:44-05:00
Changes: 5 · Summary: Records and Brand Guide mirrored to Drive after discovery

## RUN 20261005-215259-discovery-acd3 · STARTED · /discovery · 2026-10-05T21:52:59-05:00
Step: discovery:discovery
Gates checked: client_setup
- DECISION 2026-10-05T21:53 · run 20261005-215259-discovery-acd3 · Paul (deviation from BB-105 smallest container): area entity is South Carolina Lowcountry (Q3885311), one level above the Hilton Head Island-Bluffton-Port Royal MSA; reserved homepage variant South Carolina Lowcountry; category variants Roofing Contractor, Roofer, Roofers (Roof Mechanic excluded). Georgia is not served currently (C1).
- CHANGE #20 [other] clients/apex-roofing-of-the-lowcountry/brand-guide.md | Sections A, B, F (entity) | old: Area: HHI-Bluffton-Port Royal MSA (Q17020871); reserved: Hilton Head Island Metropolitan Area; variants incl. Roof Mechanic | new: Area: South Carolina Lowcountry (Q3885311); reserved: South Carolina Lowcountry; variants Roofing Contractor, Roofer, Roofers | result: revised per Paul
- CHANGE #21 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | 3.6 Paul's direction; C1 | old:  | new: Section 3.6 added; C1 annotated: Georgia not served | result: revised per Paul
### HANDOFF · /discovery · 2026-10-05 · run 20261005-215259-discovery-acd3
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
### END HANDOFF
## RUN 20261005-215259-discovery-acd3 · FINISHED · 2026-10-05T21:54:09-05:00
Changes: 2 · Summary: Entity proposal revised per Paul (SC Lowcountry area, variants)

## RUN 20261005-221139-discovery-5ddf · STARTED · /discovery · 2026-10-05T22:11:39-05:00
Step: discovery:discovery
Gates checked: client_setup
- DECISION 2026-10-05T22:12 · run 20261005-221139-discovery-5ddf · Paul (supersedes the earlier decision this day): area entity is the Hilton Head Island-Bluffton-Port Royal SC MSA (Q17020871), the BB-105 smallest container, because the brand name already carries Lowcountry into every SEO title. Reserved homepage variant: Hilton Head Island-Bluffton-Port Royal Metropolitan Area. South Carolina Lowcountry and Lowcountry stay in the pool but never in an SEO title.
- CHANGE #22 [other] clients/apex-roofing-of-the-lowcountry/brand-guide.md | Sections A, B, F (area entity) | old: Area: South Carolina Lowcountry (Q3885311); reserved: South Carolina Lowcountry | new: Area: HHI-Bluffton-Port Royal MSA (Q17020871); reserved: Hilton Head Island-Bluffton-Port Royal Metropolitan Area; Lowcountry variants never in SEO titles | result: revised per Paul
- CHANGE #23 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | 3.7 Paul's second direction | old:  | new: Section 3.7 added (area entity back to the MSA for SEO titles) | result: revised per Paul
### HANDOFF · /discovery · 2026-10-05 · run 20261005-221139-discovery-5ddf
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
### END HANDOFF
## RUN 20261005-221139-discovery-5ddf · FINISHED · 2026-10-05T22:12:29-05:00
Changes: 2 · Summary: Area entity revised per Paul: HHI-Bluffton-Port Royal MSA in SEO titles

## RUN 20261005-221818-wp-check-1c23 · STARTED · /wp-check · 2026-10-05T22:18:18-05:00
Step: wp-check
Gates checked: client_setup
- CHANGE #24 [wp_check] https://apexroofingtlc.com/?page_id=1606 | test draft page | old: (none) | new: draft id 1606 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #25 [wp_check] https://apexroofingtlc.com/?p=1607 | test draft post | old: (none) | new: draft id 1607 | result: APPLIED · test draft (trashed at the end of the check)
### HANDOFF · /wp-check · 2026-10-05 · run 20261005-221818-wp-check-1c23
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
### END HANDOFF
## RUN 20261005-221818-wp-check-1c23 · FINISHED · 2026-10-05T22:19:50-05:00
Changes: 2 · Summary: wp-check: connected except SEOPress 10.0.1 per-page fields can't be read back

## RUN 20261005-223142-wp-check-24f5 · STARTED · /wp-check · 2026-10-05T22:31:42-05:00
Step: wp-check
Gates checked: client_setup
- CHANGE #26 [wp_check] https://apexroofingtlc.com/?page_id=1610 | test draft page | old: (none) | new: draft id 1610 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #27 [wp_check] https://apexroofingtlc.com/?p=1611 | test draft post | old: (none) | new: draft id 1611 | result: APPLIED · test draft (trashed at the end of the check)
### HANDOFF · /wp-check · 2026-10-05 · run 20261005-223142-wp-check-24f5
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
### END HANDOFF
## RUN 20261005-223142-wp-check-24f5 · FINISHED · 2026-10-05T22:33:28-05:00
Changes: 2 · Summary: wp-check passed: WordPress connected (SEOPress 10.0.1 read fixed)

## CONDITION · 2026-10-05T22:33:28-05:00 · WordPress connected (/wp-check passed in the last 30 days) — met (system-verified)

## RUN 20261005-223335-discovery-40fe · STARTED · /discovery · 2026-10-05T22:33:35-05:00
Step: discovery:discovery
Gates checked: client_setup
- DECISION 2026-10-05T22:33 · run 20261005-223335-discovery-40fe · Paul: brand written in full (Apex Roofing of the Lowcountry) in every SEO title that carries it - Lowcountry is part of the official brand name; Lowcountry area variants not added on top in SEO titles, site-wide. Reserved variant wording: Hilton Head Island-Bluffton-Port Royal Metropolitan Area (Wikipedia form; Q8: no Metro shortening).
- CHANGE #28 [other] clients/apex-roofing-of-the-lowcountry/brand-guide.md | B2 SEO-title rule | old: Lowcountry variants never in an SEO title | new: Brand in full in every branded SEO title; Lowcountry variants not added on top | result: revised per Paul
- CHANGE #29 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | 3.7 confirmations | old:  | new: Q8 answered; brand-in-full rule added | result: revised per Paul
- CHANGE #30 [manual_lookup] https://businessfilings.sc.gov/BusinessFiling/Entity/Search | SC Secretary of State record | old: OpenCorporates copy: APEX ROOFING OF THE LOWCOUNTRY LLC, no. 493170, Good Standing, filed 2015-12-02 | new: Search "Apex Roofing of the Lowcountry". Record: exact legal name, entity number, status, formation date, registered agent. Screenshot the record. | result: HANDOFF ISSUED to Gwen | ref H-2026-10-05-02-manual_lookup-01
- CHANGE #31 [manual_lookup] https://verify.llronline.com/LicLookup/LookupMain.aspx | SC LLR contractor licence | old: BBB text only: #57706, expires 2027-06-30 | new: Search the business name and licence 57706. Record: licence number, class/classification, status, expiry, and the name it is held under. Screenshot. | result: HANDOFF ISSUED to Gwen | ref H-2026-10-05-02-manual_lookup-02
- CHANGE #32 [manual_lookup] https://business.google.com/ | GBP primary + secondary categories | old: Public view shows only the primary: Roofing contractor | new: Record the primary and every secondary category exactly as listed in the GBP dashboard. | result: HANDOFF ISSUED to Gwen | ref H-2026-10-05-02-manual_lookup-03
- CHANGE #33 [manual_lookup] https://business.google.com/ | GBP service-area list | old: not visible | new: Record every service area listed in the GBP dashboard, exactly as written. | result: HANDOFF ISSUED to Gwen | ref H-2026-10-05-02-manual_lookup-04
- CHANGE #34 [manual_lookup] https://business.google.com/ | GBP opening date | old: not visible | new: Record the opening date shown in the GBP dashboard, if any. | result: HANDOFF ISSUED to Gwen | ref H-2026-10-05-02-manual_lookup-05
### HANDOFF · /discovery · 2026-10-05 · run 20261005-223335-discovery-40fe
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
### END HANDOFF
## RUN 20261005-223335-discovery-40fe · FINISHED · 2026-10-05T22:34:18-05:00
Changes: 7 · Summary: Entity files final per Paul; manual lookups to Gwen

## APPROVAL · 2026-10-05T22:36:31-05:00 · entity_approved · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md (sha d06cc3b66d1c)
Approved version: clients/apex-roofing-of-the-lowcountry/brand-guide.md#A+B1+B2 (sha 858a9bcbb587)

## RUN 20261005-223638-drive-mirror-d324 · STARTED · /drive-mirror · 2026-10-05T22:36:38-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #35 [drive_file] https://drive.google.com/file/d/1obnlpMw1OavfmWrdLmPSqgA03WO29rcO/view | archive | old: Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-05.md | result: done · renamed and moved, nothing deleted
- CHANGE #36 [drive_file] https://drive.google.com/file/d/1ngaXSEt27YfyCLQasQQGfBArETeiUqS5/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-05.md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha 88f5d1b100c5 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-223638-drive-mirror-d324/0036-new.md
- CHANGE #37 [drive_file] https://drive.google.com/file/d/1Zy6ltDSL75b_yR7v1n0dNDKpVilTfrQy/view | archive | old: Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-05 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #38 [drive_file] https://drive.google.com/file/d/1qa3cnRer6mkjF8IXqPpMVuEwqcMwZZ3k/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-05 (2).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 2102c6391dec | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-223638-drive-mirror-d324/0038-new.md
- CHANGE #39 [drive_file] https://drive.google.com/file/d/1XD4qhquLAI94tS1-_PseCh_kVW8VeIsJ/view | archive | old: Apex Roofing of the Lowcountry - Brand Guide.md | new: _Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-05.md | result: done · renamed and moved, nothing deleted
- CHANGE #40 [drive_file] https://drive.google.com/file/d/171IbX2mAYPOkXoqzPNNWZIu87zJCylw5/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Brand Guide - 2026-10-05.md | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha 1c6c4aaa376c | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-223638-drive-mirror-d324/0040-new.md
- CHANGE #41 [drive_file] https://drive.google.com/file/d/15LibutpKZwORcfYnNgMqGkSFcu4PYVJr/view | archive | old: Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-05 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #42 [drive_file] https://drive.google.com/file/d/1CxTAIYxzvlYHYjAvvEClCzKuZJ6Ijrlk/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-05 (2).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 85ec5ab04f2d | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261005-223638-drive-mirror-d324/0042-new.md
- CHANGE #43 [drive_file] https://drive.google.com/file/d/1gsWwLPrf9Wtfa5Ffc4GKOtqq315kpmpF/view | file | old:  | new: Apex Roofing of the Lowcountry - Discovery Record - APPROVED.md (01 - Discovery and Audit/Deliverables; the approved version, unchanged) | result: uploaded
### HANDOFF · /drive-mirror · 2026-10-05 · run 20261005-223638-drive-mirror-d324
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
### END HANDOFF
## RUN 20261005-223638-drive-mirror-d324 · FINISHED · 2026-10-05T22:40:58-05:00
Changes: 9 · Summary: Drive mirror after entity approval; APPROVED Discovery Record uploaded

## RUN 20261006-085120-drive-mirror-4406 · STARTED · /drive-mirror · 2026-10-06T08:51:20-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #44 [drive_file] https://drive.google.com/file/d/1rwCwFByhKeO4g2NQbZeYuWharwMBGP1C/view | name + folder | old: Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md (01 - Discovery and Audit/Deliverables) | new: Apex Roofing of the Lowcountry - Discovery Record - REVIEW - 2026-10-05.md (_Archive) | result: archived on Paul's yes (2026-10-06)
### HANDOFF · /drive-mirror · 2026-10-06 · run 20261006-085120-drive-mirror-4406
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
### END HANDOFF
## RUN 20261006-085120-drive-mirror-4406 · FINISHED · 2026-10-06T08:51:36-05:00
Changes: 1 · Summary: Discovery Record REVIEW copy archived (Paul's yes)

## RUN 20261006-085141-discovery-bb0e · STARTED · /discovery · 2026-10-06T08:51:41-05:00
Step: discovery:proof-sheet
Gates checked: entity_approved
- CHANGE #45 [drive_file] https://drive.google.com/file/d/1InOV2XI8lZIA2iQsWbuja6pidepTX948/view?usp=drivesdk | file | old:  | new: Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md | result: uploaded
- CHANGE #46 [drive_file] https://docs.google.com/document/d/11uhrPAeoOdQjw1x5ZolTDuL1FkntxL369dK3Rr7NfoU/edit | file | old:  | new: Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY | result: uploaded
- CHANGE #47 [audit_step] S04 | Proof sheet built (Markdown + client Google Doc) | old:  | new: done | result: DONE — Proof sheet built from the approved Discovery Record and Brand Guide A; .md and CLIENT COPY Google Doc in Drive Deliverables; return by 2026-10-20
### HANDOFF · /discovery · 2026-10-06 · run 20261006-085141-discovery-bb0e
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
### END HANDOFF
## RUN 20261006-085141-discovery-bb0e · FINISHED · 2026-10-06T08:56:15-05:00
Changes: 3 · Summary: Client proof sheet built (REVIEW); open choices for Paul

## RUN 20261006-104753-discovery-44eb · STARTED · /discovery · 2026-10-06T10:47:53-05:00
Step: discovery:proof-sheet
Gates checked: entity_approved
- CHANGE #48 [drive_file] https://drive.google.com/file/d/1InOV2XI8lZIA2iQsWbuja6pidepTX948/view | archive | old: Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md | new: _Archive/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW - 2026-10-06.md | result: done · renamed and moved, nothing deleted
- CHANGE #49 [drive_file] https://drive.google.com/file/d/11cC7ZXnisRSNK09Q3Tr1KKhFAkLXPIFB/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW - 2026-10-06.md | new: Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md · sha 1194b244e779 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261006-104753-discovery-44eb/0049-new.md
- CHANGE #50 [drive_file] https://docs.google.com/document/d/11uhrPAeoOdQjw1x5ZolTDuL1FkntxL369dK3Rr7NfoU/edit | archive | old: Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY | new: _Archive/Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY - 2026-10-06 | result: done · renamed and moved, nothing deleted
- CHANGE #51 [drive_file] https://docs.google.com/document/d/1AU2GdOlZvpjAby3USOBzeQgOcvd5pXGYk0UoPsnO2N0/edit | upload | old: previous version archived as Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY - 2026-10-06 | new: Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY · sha 1194b244e779 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261006-104753-discovery-44eb/0051-new.md
- CHANGE #52 [drive_file] https://drive.google.com/file/d/1KRun10jn91aLeCsUkm-lmzq-NZj_jtmN/view | archive | old: Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05.md | new: _Archive/Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05 - 2026-10-06.md | result: done · renamed and moved, nothing deleted
- CHANGE #53 [drive_file] https://drive.google.com/file/d/1tVYKQJwwUd8XB9XA6tgZX2c6p7t0PBPC/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05 - 2026-10-06.md | new: Apex Roofing of the Lowcountry - MANUAL - public-sources-capture - 2026-10-05.md · sha 684629004ea6 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261006-104753-discovery-44eb/0053-new.md
### HANDOFF · /discovery · 2026-10-06 · run 20261006-104753-discovery-44eb
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
### END HANDOFF
## RUN 20261006-104753-discovery-44eb · FINISHED · 2026-10-06T10:54:40-05:00
Changes: 6 · Summary: Proof sheet revised with Paul's answers; profiles checked

## RUN 20261007-144926-discovery-20d6 · STARTED · /discovery · 2026-10-07T14:49:26-05:00
Step: discovery:proof-sheet
Gates checked: entity_approved
- DECISION 2026-10-07T14:49 · run 20261007-144926-discovery-20d6 · Paul: 'residential' is used as a description in headings and page text (e.g. residential roofing contractor), not as a category name variant; the approved entity is unchanged. Paul: no phone line on the proof sheet.
- CHANGE #54 [drive_file] https://drive.google.com/file/d/11cC7ZXnisRSNK09Q3Tr1KKhFAkLXPIFB/view | archive | old: Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md | new: _Archive/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #55 [drive_file] https://drive.google.com/file/d/1MRVuiezDpyRafYHUoY3lKdA20kPaGvPe/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW - 2026-10-07.md | new: Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md · sha f8bb8b6123c6 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261007-144926-discovery-20d6/0055-new.md
- CHANGE #56 [drive_file] https://docs.google.com/document/d/1AU2GdOlZvpjAby3USOBzeQgOcvd5pXGYk0UoPsnO2N0/edit | archive | old: Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY | new: _Archive/Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY - 2026-10-07 | result: done · renamed and moved, nothing deleted
- CHANGE #57 [drive_file] https://docs.google.com/document/d/17jqGB3i9Dfk791-_VCboakbX_Z5PM3BaFaR2mtZ8vTA/edit | upload | old: previous version archived as Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY - 2026-10-07 | new: Apex Roofing of the Lowcountry - Client Proof Sheet - CLIENT COPY · sha f8bb8b6123c6 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261007-144926-discovery-20d6/0057-new.md
- CHANGE #58 [drive_file] https://drive.google.com/file/d/1QUNMOJpa-7YXgRgWV7lFDAxW6yPZvhBW/view | file | old:  | new: Apex Roofing of the Lowcountry - MANUAL - client-answers-informal - 2026-10-07.md (Evidence; client's words verbatim) | result: uploaded
### HANDOFF · /discovery · 2026-10-07 · run 20261007-144926-discovery-20d6
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
### END HANDOFF
## RUN 20261007-144926-discovery-20d6 · FINISHED · 2026-10-07T14:51:59-05:00
Changes: 5 · Summary: Proof sheet cut to 8 open questions; client's informal answers saved

## RUN 20261007-151404-discovery-f9a6 · STARTED · /discovery · 2026-10-07T15:14:04-05:00
Step: discovery:proof-sheet
Gates checked: entity_approved
- DECISION 2026-10-07T15:14 · run 20261007-151404-discovery-f9a6 · Paul: address option (a) - 6 Sutton Ct stays hidden on the GBP (service-area business); the approved Hilton Head Island-Bluffton-Port Royal metro area stays the area entity. Street address on the website only if wanted. Paul answered the 8 follow-up questions himself; the sheet is not sent to the client. Owner titles not published (sources conflict); site keeps 'Founded by Ralph and Pierce Brehany'.
- CHANGE #59 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | Addendum 2026-10-07 | old:  | new: Paul's answers to the 8 follow-up questions + address decision (a) | result: recorded
### HANDOFF · /discovery · 2026-10-07 · run 20261007-151404-discovery-f9a6
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
### END HANDOFF
## RUN 20261007-151404-discovery-f9a6 · FINISHED · 2026-10-07T15:14:35-05:00
Changes: 1 · Summary: Paul answered the 8 follow-up questions; address option (a)

## RUN 20261007-151906-discovery-3a31 · STARTED · /discovery · 2026-10-07T15:19:06-05:00
Step: discovery:proof-sheet
Gates checked: entity_approved
- CHANGE #60 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - MANUAL - proof-sheet-answers-paul - 2026-10-06.md | licences | old: found - not verified | new: Paul confirmed both current (SC 57706, Bluffton 0620033323) | result: recorded
### HANDOFF · /discovery · 2026-10-07 · run 20261007-151906-discovery-3a31
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
### END HANDOFF
## RUN 20261007-151906-discovery-3a31 · FINISHED · 2026-10-07T15:19:16-05:00
Changes: 1 · Summary: Paul confirmed both licences current

## APPROVAL · 2026-10-07T15:19:52-05:00 · proof_sheet_approved · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - REVIEW.md (sha f8bb8b6123c6)

## RUN 20261007-152000-discovery-9b0e · STARTED · /discovery · 2026-10-07T15:20:00-05:00
Step: discovery:sheet-returned
Gates checked: proof_sheet_approved
- CHANGE #61 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md | file | old:  | new: Returned sheet: the client's 2026-10-07 answers as given | result: saved
### HANDOFF · /discovery · 2026-10-07 · run 20261007-152000-discovery-9b0e
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
### END HANDOFF
## RUN 20261007-152000-discovery-9b0e · FINISHED · 2026-10-07T15:20:21-05:00
Changes: 1 · Summary: Returned sheet recorded (client's answers as given)

## CONDITION · 2026-10-07T15:20:21-05:00 · The client returned the proof sheet (the returned sheet is recorded) — met (system-verified)

## RUN 20261007-152058-drive-mirror-c605 · STARTED · /drive-mirror · 2026-10-07T15:20:58-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #62 [drive_file] https://drive.google.com/file/d/1ngaXSEt27YfyCLQasQQGfBArETeiUqS5/view | archive | old: Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #63 [drive_file] https://drive.google.com/file/d/1_wDST9piHEVew3E6PQAXG9QT6zzMkak7/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-07.md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha 21d19c13d534 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261007-152058-drive-mirror-c605/0063-new.md
- CHANGE #64 [drive_file] https://drive.google.com/file/d/1qa3cnRer6mkjF8IXqPpMVuEwqcMwZZ3k/view | archive | old: Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #65 [drive_file] https://drive.google.com/file/d/1lVdp7A91qH_LGoxHYEpZUtaF2oPV7Jd8/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-07.md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha f3c9baaa5002 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261007-152058-drive-mirror-c605/0065-new.md
- CHANGE #66 [drive_file] https://drive.google.com/file/d/1CxTAIYxzvlYHYjAvvEClCzKuZJ6Ijrlk/view | archive | old: Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #67 [drive_file] https://drive.google.com/file/d/1UhPgZ6TTaJfH0RzQEVp2Zypj7ZoVIPIy/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-07.md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 4f8c78e1deb0 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261007-152058-drive-mirror-c605/0067-new.md
- CHANGE #68 [drive_file] https://drive.google.com/file/d/11VXD7vHg63DetZkx8pwfo9JMnTUF91ew/view | file | old:  | new: Apex Roofing of the Lowcountry - Client Proof Sheet - APPROVED.md (Deliverables) | result: uploaded
- CHANGE #69 [drive_file] https://drive.google.com/file/d/1QFqzGVhdibzTnnydNiJg_aP7gqvZHNED/view | file | old:  | new: Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md (Deliverables) | result: uploaded
- CHANGE #70 [drive_file] https://drive.google.com/file/d/1QFqzGVhdibzTnnydNiJg_aP7gqvZHNED/view | archive | old: Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md | new: _Archive/Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED - 2026-10-07.md | result: done · renamed and moved, nothing deleted
- CHANGE #71 [drive_file] https://drive.google.com/file/d/1BgZFVGn5WQIe9Hin1jOn2OQ7P5jAnuN8/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED - 2026-10-07.md | new: Apex Roofing of the Lowcountry - Client Proof Sheet - RETURNED.md · sha 0b789ca32d56 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261007-152058-drive-mirror-c605/0071-new.md
### HANDOFF · /drive-mirror · 2026-10-07 · run 20261007-152058-drive-mirror-c605
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
### END HANDOFF
## RUN 20261007-152058-drive-mirror-c605 · FINISHED · 2026-10-07T15:25:37-05:00
Changes: 10 · Summary: Drive mirror after proof sheet approval; APPROVED and RETURNED sheets uploaded

## RUN 20261007-152559-crawl-0206 · STARTED · /crawl · 2026-10-07T15:25:59-05:00
Step: crawl
Gates checked: client_setup
- NOTE 15:30:34 crawl: task posted for apexroofingtlc.com (basic, max 1000 pages, 2000 ms between hits) · cost $0.15 · task 10072030-1266-0216-0000-dd125d58970b
- NOTE 15:30:35 crawl: crawling — 0/1000 pages (0%), 0 in queue
- NOTE 15:33:45 crawl: crawl finished: 72 pages, stop reason empty_queue
- NOTE 15:33:47 crawl: downloaded pages (72)
- NOTE 15:33:51 crawl: downloaded links (2466)
- NOTE 15:33:57 crawl: all result sets downloaded (no charge for downloads)
- NOTE 15:33:57 crawl: converted: Apex Roofing of the Lowcountry - DFS - internal_all - 2026-10-07.csv (72 rows); Apex Roofing of the Lowcountry - DFS - links_all - 2026-10-07.csv (72 rows); Apex Roofing of the Lowcountry - DFS - page_titles_all - 2026-10-07.csv (72 rows); Apex Roofing of the Lowcountry - DFS - meta_description_all - 2026-10-07.csv (72 rows); Apex Roofing of the Lowcountry - DFS - h1_all - 2026-10-07.csv (72 rows); Apex Roofing of the Lowcountry - DFS - h2_all - 2026-10-07.csv (72 rows); Apex Roofing of the Lowcountry - DFS - all_inlinks - 2026-10-07.csv (2225 rows); Apex Roofing of the Lowcountry - DFS - external_all - 2026-10-07.csv (10 rows); Apex Roofing of the Lowcountry - DFS - duplicate_titles - 2026-10-07.csv (0 rows); Apex Roofing of the Lowcountry - DFS - duplicate_descriptions - 2026-10-07.csv (0 rows); Apex Roofing of the Lowcountry - DFS - duplicate_content - 2026-10-07.csv (0 rows); Apex Roofing of the Lowcountry - DFS - redirect_chains - 2026-10-07.csv (0 rows); Apex Roofing of the Lowcountry - DFS - non_indexable - 2026-10-07.csv (6 rows)
- CHANGE #72 [drive_file] https://drive.google.com/file/d/11yAc7me_kxls2mukEgK2h3L_vA4Qp503/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - duplicate_content - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #73 [drive_file] https://drive.google.com/file/d/1WxC6rfi-bFvYe1l0viiF17fQRpBoVXTu/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - duplicate_descriptions - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #74 [drive_file] https://drive.google.com/file/d/1ChRQe--_WloIv9EbvV0Y4UK1f_5nPGfa/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - duplicate_titles - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #75 [drive_file] https://drive.google.com/file/d/1nMv8ehjVL9Q7qu3rfEsrvtPFmEEY_JbW/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - redirect_chains - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #76 [drive_file] https://drive.google.com/file/d/1OhV5Cs184nJvgqN1pRHGVXPbuPtWHBzV/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - non_indexable - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #77 [drive_file] https://drive.google.com/file/d/1vvXFDvJZ7rtQIl7a1iW2JW85DQPun0mD/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - crawl-config - 2026-10-07.md (Evidence) | result: uploaded
- CHANGE #78 [drive_file] https://drive.google.com/file/d/1cr0bjT3rf8DXdCX8bwFM4e8TCfavIAli/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - external_all - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #79 [drive_file] https://drive.google.com/file/d/1kwc2H7bIVZCXxT_bcJzWNbjHP2Lc-yzd/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - links_all - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #80 [drive_file] https://drive.google.com/file/d/1NNskPyBtm7s3ygalK-pwhSko9k1ETMV_/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - h1_all - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #81 [drive_file] https://drive.google.com/file/d/188OWsJYmaWeSUHpnXu1N5Az5uBwkrKaL/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - page_titles_all - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #82 [drive_file] https://drive.google.com/file/d/1Gc8pK58FJfO3VePX-r5ZzxPS-cVOR6on/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - meta_description_all - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #83 [drive_file] https://drive.google.com/file/d/1Xu5JlStfHfit-B4Z33OvQlqn0x4Y5voi/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - internal_all - 2026-10-07.csv (Evidence) | result: uploaded
- CHANGE #84 [drive_file] https://drive.google.com/file/d/1e2nD4p88A-LFLd7tUBDLc9MICT9QH7_B/view | file | old:  | new: Apex Roofing of the Lowcountry - DFS - h2_all - 2026-10-07.csv (Evidence) - NOT FAITHFUL: 30416 bytes vs 30377 expected (paste error) | result: uploaded, then archived as unfaithful
- CHANGE #85 [drive_file] https://drive.google.com/file/d/1e2nD4p88A-LFLd7tUBDLc9MICT9QH7_B/view | name + folder | old: Apex Roofing of the Lowcountry - DFS - h2_all - 2026-10-07.csv (Evidence) | new: Apex Roofing of the Lowcountry - DFS - h2_all - 2026-10-07 - 2026-10-07.csv (_Archive) | result: archived - unfaithful copy; the local file is the evidence
- CHANGE #86 [audit_step] S05 | Site crawl | old:  | new: done | result: DONE — DataforSEO basic crawl, 72 URLs, $0.15. 12 of 14 files in Drive Evidence; h2_all and all_inlinks local only (connector paste limits)
### HANDOFF · /crawl · 2026-10-07 · run 20261007-152559-crawl-0206
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
### END HANDOFF
## RUN 20261007-152559-crawl-0206 · FINISHED · 2026-10-07T15:44:33-05:00
Changes: 15 · Summary: Crawled 72 URLs, $0.15

## RUN 20261007-154441-discovery-64db · STARTED · /discovery · 2026-10-07T15:44:41-05:00
Step: discovery:data
Gates checked: proof_sheet_approved
- CHANGE #87 [audit_step] S11 | Search Console / GA4 | old:  | new: skipped | result: SKIPPED — No Search Console or GA4 access (intake 2026-10-05); Paul 2026-10-06: not needed, we use our own SEO data
- CHANGE #88 [audit_step] S20 | SEOPress site-wide settings (title templates, sitemap, noind | old:  | new: done | result: DONE — Readable during /wp-check 2026-10-05 (Administrator login); saved as evidence
- CHANGE #89 [audit_step] S09 | Citations | old:  | new: skipped | result: SKIPPED — Paul 2026-10-07: skip citations for this audit (no BrightLocal citation tracker export)
- CHANGE #90 [other] clients/apex-roofing-of-the-lowcountry/inputs/local-grid/ | local grid PDFs (4) | old:  | new: Paul's 4 grid scans 2026-10-07 (roof repair bluffton + roofing contractor near me; local pack + maps; 176 pins, 3 mi) saved as MANUAL evidence - tool not yet r… | result: saved
- CHANGE #91 [audit_step] S10 | Local grid | old:  | new: done | result: DONE — Local Dominator scans 2026-10-07: roof repair bluffton (local pack 6.99, maps 20+), roofing contractor near me (local pack 19.29, maps 20+); 176 pins, 3 mi. Results only; report advice not used
- CHANGE #92 [other] clients/apex-roofing-of-the-lowcountry/data/local-grid/local-grid-summary.md | S10 local grid summary | old:  | new: Local Dominator results logged (4 scans; ranks + competitors; advice excluded) | result: saved
- CHANGE #93 [data_pull] Apex Roofing of the Lowcountry | reviews task | old:  | new: 10072134-1266-0298-0000-424efb2c3d68 | result: POSTED
- CHANGE #94 [data_pull] apexroofingtlc.com | rankings | old:  | new: 43 rows, 2 clusters | result: DONE
- CHANGE #95 [audit_step] S08 | Backlinks pull: referring domains per URL | old:  | new: done | result: DONE — DataforSEO backlinks one_per_domain: 711 referring domains (694 to the homepage), 6 target URLs incl. 2 old URLs; $0.05
- CHANGE #96 [data_pull] Bluffton,Hilton Head Island,Beaufort,Hardeeville | PAA | old:  | new: 20 queries, 50 questions | result: DONE
- CHANGE #97 [data_pull] Bluffton,Hilton Head Island,Beaufort,Hardeeville | fan-out | old:  | new: 10 seeds, 379 queries | result: DONE
- CHANGE #98 [audit_step] S07 | Rankings + cannibalization: every ranked keyword per URL (to | old:  | new: done | result: DONE — DataforSEO Labs ranked keywords (US): 41 keywords on 7 URLs; 2 'cannibalization' clusters are the homepage under http://www and https (host duplicate); 3 of 104 'best' variants with volume; $0.107
- CHANGE #99 [audit_step] S06 | Reviews pull: Google rating, count, recent review text (no r | old:  | new: done | result: DONE — 67 reviews (rating 5.0; 66 five-star, 1 two-star); themes, symptom words and review-only claims added to customer-language.md; nothing to Brand Guide D (CM-027)
- CHANGE #100 [audit_step] S19 | People Also Ask: core services × primary city + top 3 cities | old:  | new: done | result: DONE — 20 queries, 50 questions routed: 27 service FAQ, 0 location FAQ, 10 blog topic, 13 drop; C3 empty so no C3 drops
- CHANGE #101 [audit_step] S21 | Query fan-out (CM-045): core services × primary city + top 3 | old:  | new: done | result: DONE — 10 seeds, 379 queries routed: 269 service H2/FAQ (about 75 head terms), 35 location FAQ, 55 blog topic, 20 drop; 2 PAA repeats route with PAA; no volumes (CM-012)
- CHANGE #102 [other] clients/apex-roofing-of-the-lowcountry/data/reviews/reviews.csv | review ChZDSUhNMG9n… text | old: (ends with the reviewer's signed name) | new: [reviewer's name removed] | result: redacted before commit (no reviewer names, CM-027)
### HANDOFF · /discovery · 2026-10-07 · run 20261007-154441-discovery-64db
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
### END HANDOFF
## RUN 20261007-154441-discovery-64db · FINISHED · 2026-10-07T17:00:51-05:00
Changes: 16 · Summary: Data step: reviews, rankings, backlinks, PAA, fan-out ($0.236), local grid; citations and GSC skipped

## RUN 20261007-170552-discovery-4092 · STARTED · /discovery · 2026-10-07T17:05:52-05:00
Step: discovery:data
Gates checked: proof_sheet_approved
- REVIEW CONTINUED 2026-10-07T17:18 · after discovery:data (run 20261007-154441-discovery-64db) · Paul typed /next
- CHANGE #103 [data_pull] Bluffton,Hilton Head Island,Beaufort,Hardeeville,Port Royal,St. Helena Island,Ridgeland,Okatie,Lady's Island,Fripp Island,Pritchardville,Levy | PAA | old:  | new: 96 queries, 140 questions | result: DONE
- CHANGE #104 [audit_step] S19 | People Also Ask: core services × primary city + top 3 cities | old:  | new: done | result: DONE — PAA: 96 queries (8 services x 12 towns), 140 distinct questions routed - 76 service FAQ, 2 location FAQ (Lady's Island, Fripp Island), 28 blog topic, 34 drop; first 50 routes carried over unchanged
### HANDOFF · /discovery · 2026-10-07 · run 20261007-170552-discovery-4092
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
### END HANDOFF
## RUN 20261007-170552-discovery-4092 · FINISHED · 2026-10-07T17:31:09-05:00
Changes: 2 · Summary: People Also Ask extended to all 12 towns: 140 questions routed ($0.20)
- REVIEW CONTINUED 2026-10-07T19:42 · after discovery:data (run 20261007-170552-discovery-4092) · Paul typed /next

## RUN 20261007-194242-discovery-9495 · STARTED · /discovery · 2026-10-07T19:42:42-05:00
Step: discovery:audit
Gates checked: entity_approved
- CHANGE #105 [audit_step] S12 | Ingest + cross-checks | old:  | new: done | result: DONE — Ingest + cross-checks: 13/13 crawl exports recognised, manifest SRC-001-027; crosscheck: rendering LIMITATION (standing config), coverage CONFIRMED; nothing CONTRADICTED
- CHANGE #106 [audit_step] S13 | Entity analysis: site vs Brand Guide (triple, NAP, brand sea | old:  | new: done | result: DONE — Entity: site vs Brand Guide (triple, NAP, brand forms, GBP field, schema readiness) - findings F-001 to F-008
- CHANGE #107 [audit_step] S14 | Architecture: every page typed, keep/merge/redirect per CM-0 | old:  | new: done | result: DONE — URL Decision Map: 83 rows (72 crawled + 2 sitemap-only + 1 backlink-only + 2 host variants + 6 noindexed archives); no CM-019 candidate (conditions 3-4 unmet everywhere); 1 Needs Evidence slug change, 1 redirect fix
- CHANGE #108 [audit_step] S15 | Page conformance: every page scored against its spec (check  | old:  | new: done | result: DONE — Conformance scorecards for 46 spec'd pages (homepage, 8 service, 12 location, about, 24 posts); all specs DRAFT (advisory); utility pages have no spec
- CHANGE #109 [audit_step] S16 | Technical findings (Low batched into one handoff) | old:  | new: done | result: DONE — Technical findings F-009, F-027, F-029, F-030, F-031, F-033 (Low, one batch) - redirect to 404, internal links to redirects, sitemap redirects, separators, meta descriptions, alt text
- DECISION 2026-10-07T20:01 · run 20261007-194242-discovery-9495 · Gate B: 2 questions raised, both to Paul. Q1 service-title format (SVC-03 vs Brand Guide B2 note; conflict CF-LOCAL-001) blocks F-014 and the title side of F-004 - default: Service Name - Brand, no area. Q2 homepage shows all 8 services as H3 vs BB-313 max 5-6 blocks the HP-11 part of F-023 - default: all 8, logged as a Paul Exception. No VA questions. Specs are DRAFT (advisory). CM-026 cited. · affects F-014,F-004,F-023
- DECISION 2026-10-07T20:10 · run 20261007-194242-discovery-9495 · Gate B Q1 (Paul): option 1a for this client - service-page SEO titles are 'Service Name - Brand' with no area term, because 'Lowcountry' in the brand name already carries the service-area entity. Overrides the B2 note's 'SEO titles take the metro-area/county variants' for service pages (B2 text to be aligned with Paul's re-approval of the entity sections). Homepage title keeps the reserved variant (B1). · affects F-014,F-004
- DECISION 2026-10-07T20:10 · run 20261007-194242-discovery-9495 · Gate B Q2 (Paul): option 2a - the rebuilt homepage links all 8 services as H3 links (Paul Exception to BB-313's 5-6). · affects F-023
- CHANGE #110 [audit_step] S17 | Fresh-context review of Finding Register + URL Decision Map | old:  | new: done | result: DONE — Fresh-context review: 21 confirmed, 9 revised, 3 withdrawn; High 3 / Medium 17 / Low 10; map 3 rows corrected
- CHANGE #111 [audit_step] S18 | Render deliverables | old:  | new: done | result: DONE — Rendered Finding Register, URL Decision Map, Recommendations, Evidence Manifest (REVIEW) from the latest revision of each finding (30 active: High 3, Medium 17, Low 10; 3 withdrawn listed). Recommendations and Evidence Manifest uploaded to Drive Deliverables; Finding Register (87 KB) and URL Decision Map (40 KB) kept local - too large to paste reliably
- CHANGE #112 [drive_file] https://drive.google.com/file/d/1d6uL99jW-PCmFPjMDHd6UVFzpE_ZygDl/view?usp=drivesdk | file | old:  | new: Apex Roofing of the Lowcountry - Recommendations - REVIEW.md | result: uploaded
- CHANGE #113 [drive_file] https://drive.google.com/file/d/1brOXSWq2d-COpf0-HVrzNiJ0FT1HJh8p/view?usp=drivesdk | file | old:  | new: Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW.md | result: uploaded
### HANDOFF · /discovery · 2026-10-07 · run 20261007-194242-discovery-9495
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
### END HANDOFF
## RUN 20261007-194242-discovery-9495 · FINISHED · 2026-10-07T20:25:32-05:00
Changes: 9 · Summary: Audit S12-S18: 30 findings (3 High, 17 Medium, 10 Low, all spec-based advisory), URL Decision Map 83 rows, no removals; reviewed in a fresh context

## CONDITION · 2026-10-07T20:25:32-05:00 · Every registered audit step has an outcome (Done / Skipped / Failed) — met (system-verified)

## RUN 20261008-073331-discovery-a866 · STARTED · /discovery · 2026-10-08T07:33:31-05:00
Step: discovery:discovery
Gates checked: client_setup
- DECISION 2026-10-08T07:33 · run 20261008-073331-discovery-a866 · Paul (supersedes the 2026-10-05 reserved variant): the homepage SEO title carries 'Hilton Head Island Metropolitan Area' (Wikipedia article title, a real name); the homepage H1 uses a familiar pool variant - Lowcountry or South Carolina Lowcountry. 'Hilton Head Island-Bluffton-Port Royal Metropolitan Area' moves to the pool. Rules CF-LOCAL-002 (HP-06 vs BB-304): reserved variant in the title, pool variant in the H1. B2 now states service titles 'Service Name - Brand' (Gate B 1a).
- CHANGE #114 [other] clients/apex-roofing-of-the-lowcountry/brand-guide.md | A6, B1, B2 | old: reserved: Hilton Head Island-Bluffton-Port Royal Metropolitan Area; B2 'SEO titles take metro/county variants' | new: reserved: Hilton Head Island Metropolitan Area (title); H1 Lowcountry/SC Lowcountry; MSA name to pool; B2 title rules per page type | result: revised per Paul
- CHANGE #115 [other] clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md | 3.8 | old:  | new: Section 3.8 added: reserved variant Hilton Head Island Metropolitan Area; H1 pool variant; service titles | result: revised per Paul
### HANDOFF · /discovery · 2026-10-08 · run 20261008-073331-discovery-a866
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
### END HANDOFF
## RUN 20261008-073331-discovery-a866 · FINISHED · 2026-10-08T07:34:12-05:00
Changes: 2 · Summary: Reserved homepage variant -> Hilton Head Island Metropolitan Area; H1 pool variant (Paul)

## APPROVAL · 2026-10-08T07:36:22-05:00 · entity_approved · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md (sha 76a048adc3f7)
Approved version: clients/apex-roofing-of-the-lowcountry/brand-guide.md#A+B1+B2 (sha d5673fb2dcf3)

## RUN 20261008-073627-discovery-2c41 · STARTED · /discovery · 2026-10-08T07:36:27-05:00
Step: discovery:audit
Gates checked: entity_approved
- CHANGE #116 [drive_file] https://drive.google.com/file/d/1d6uL99jW-PCmFPjMDHd6UVFzpE_ZygDl/view?usp=drivesdk | archive | old: Apex Roofing of the Lowcountry - Recommendations - REVIEW.md | new: _Archive/Apex Roofing of the Lowcountry - Recommendations - REVIEW - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #117 [drive_file] https://drive.google.com/file/d/1dVCYpd3KlpBmAWDbHKJWmMgyzZHVzNlG/view?usp=drivesdk | upload | old: previous version archived as Apex Roofing of the Lowcountry - Recommendations - REVIEW - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Recommendations - REVIEW.md · sha c4a2bebda187 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-073627-discovery-2c41/0117-new.md
- CHANGE #118 [drive_file] https://drive.google.com/file/d/1brOXSWq2d-COpf0-HVrzNiJ0FT1HJh8p/view?usp=drivesdk | archive | old: Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW.md | new: _Archive/Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #119 [drive_file] https://drive.google.com/file/d/1-M0Pzd79LUGQ2wMIs6QFmf565IEnfr3y/view?usp=drivesdk | upload | old: previous version archived as Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW.md · sha 6c2076437ccc | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-073627-discovery-2c41/0119-new.md
### HANDOFF · /discovery · 2026-10-08 · run 20261008-073627-discovery-2c41
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
### END HANDOFF
## RUN 20261008-073627-discovery-2c41 · FINISHED · 2026-10-08T07:40:48-05:00
Changes: 4 · Summary: Audit deliverables revised to Paul's rulings (homepage title/H1, About page, advisory); 30 findings: 3 High, 18 Medium, 9 Low

## APPROVAL · 2026-10-08T07:43:38-05:00 · audit_approved · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Finding Register - REVIEW.md (sha 962665eb263e)
Approved version: clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - URL Decision Map - REVIEW.md (sha 38f22236658e)
Approved version: clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Recommendations - REVIEW.md (sha c4a2bebda187)
Approved version: clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/Apex Roofing of the Lowcountry - Evidence Manifest - REVIEW.md (sha 6c2076437ccc)

## RUN 20261008-074416-drive-mirror-b726 · STARTED · /drive-mirror · 2026-10-08T07:44:16-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #120 [drive_file] https://drive.google.com/file/d/1_wDST9piHEVew3E6PQAXG9QT6zzMkak7/view | archive | old: Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #121 [drive_file] https://drive.google.com/file/d/1Zn4tgOB22pgwW6zmUxzb4qlN38YcMIzg/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha cde86db23d8e | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-074416-drive-mirror-b726/0121-new.md
- CHANGE #122 [drive_file] https://drive.google.com/file/d/1lVdp7A91qH_LGoxHYEpZUtaF2oPV7Jd8/view | archive | old: Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #123 [drive_file] https://drive.google.com/file/d/1UHwtgvaJd9_CynPdValYLvaSnBlyHqx1/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 00ed13da8135 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-074416-drive-mirror-b726/0123-new.md
- CHANGE #124 [drive_file] https://drive.google.com/file/d/171IbX2mAYPOkXoqzPNNWZIu87zJCylw5/view | archive | old: Apex Roofing of the Lowcountry - Brand Guide.md | new: _Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #125 [drive_file] https://drive.google.com/file/d/1tmQQUTXCWNTURddqsut4550czVgusJEH/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha fe68f5fe48a2 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-074416-drive-mirror-b726/0125-new.md
- CHANGE #126 [drive_file] https://drive.google.com/file/d/1d3cHvGIIB9cWe5nkIyOQvbDzll5hdywi/view | file | old:  | new: Apex Roofing of the Lowcountry - Recommendations - APPROVED.md (Deliverables) | result: uploaded
- CHANGE #127 [drive_file] https://drive.google.com/file/d/1UHMkUobIeLAI2p6DVfo-WM552kNLWZbK/view | file | old:  | new: Apex Roofing of the Lowcountry - Evidence Manifest - APPROVED.md (Deliverables) | result: uploaded
- CHANGE #128 [drive_file] https://drive.google.com/file/d/1gsWwLPrf9Wtfa5Ffc4GKOtqq315kpmpF/view | archive | old: Apex Roofing of the Lowcountry - Discovery Record - APPROVED.md | new: _Archive/Apex Roofing of the Lowcountry - Discovery Record - APPROVED - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #129 [drive_file] https://drive.google.com/file/d/1Pmm-Ix7kfWE4MVfcT_vIj-i7cUIKrXoe/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Discovery Record - APPROVED - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Discovery Record - APPROVED.md · sha 76a048adc3f7 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-074416-drive-mirror-b726/0129-new.md
- CHANGE #130 [drive_file] https://drive.google.com/file/d/1UhPgZ6TTaJfH0RzQEVp2Zypj7ZoVIPIy/view | archive | old: Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #131 [drive_file] https://drive.google.com/file/d/1kq4xPLEqgMKtsmOjgbS5SDxjcEg4eTVT/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 3742d7cf178b | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-074416-drive-mirror-b726/0131-new.md
### HANDOFF · /drive-mirror · 2026-10-08 · run 20261008-074416-drive-mirror-b726
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
### END HANDOFF
## RUN 20261008-074416-drive-mirror-b726 · FINISHED · 2026-10-08T07:53:03-05:00
Changes: 12 · Summary: Drive mirror after entity re-approval and audit approval

## RUN 20261008-075515-discovery-24a2 · STARTED · /discovery · 2026-10-08T07:55:15-05:00
Step: discovery:reconcile
Gates checked: proof_sheet_returned
- CHANGE #132 [other] clients/apex-roofing-of-the-lowcountry/brand-guide.md | reconcile (A, D, D2, E, G, author) | old: A rows Proposed/Submitted (awaits entity_approved); D, D2, E, G empty | new: A statuses reconciled (rows 1,4,8 Paul Approved; 10,11 unchanged Submitted); D filled (Client Confirmed 2026-10-07 / Paul Approved / Submitted with NEED), D2 5… | result: reconciled
### HANDOFF · /discovery · 2026-10-08 · run 20261008-075515-discovery-24a2
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
### END HANDOFF
## RUN 20261008-075515-discovery-24a2 · FINISHED · 2026-10-08T08:00:06-05:00
Changes: 1 · Summary: Brand Guide reconciled (client + Paul answers); entity re-approval needed; 4 open choices for Paul
