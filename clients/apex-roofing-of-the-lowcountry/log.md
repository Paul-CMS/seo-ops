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

## RUN 20261008-080806-discovery-b736 · STARTED · /discovery · 2026-10-08T08:08:06-05:00
Step: discovery:reconcile
Gates checked: proof_sheet_returned
- DECISION 2026-10-08T08:08 · run 20261008-080806-discovery-b736 · Paul reconcile choices: 1a street address 6 Sutton Ct on the website, GBP address stays hidden; 2a no travel fee; 3b ask the client whether CertainTeed ShingleMaster is current (stays off the site until confirmed); 4a Ralph Brehany stays owner/author on Paul's direction.
- CHANGE #133 [other] clients/apex-roofing-of-the-lowcountry/brand-guide.md | A4, D (travel fee, ShingleMaster, author), D3 R4, E, H | old: 4 open choices marked [NEED: Paul] | new: website address shown, no travel fee, ShingleMaster asked of the client, Ralph kept | result: revised per Paul
### HANDOFF · /discovery · 2026-10-08 · run 20261008-080806-discovery-b736
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
### END HANDOFF
## RUN 20261008-080806-discovery-b736 · FINISHED · 2026-10-08T08:08:45-05:00
Changes: 1 · Summary: Reconcile choices applied (website address, no travel fee, ShingleMaster asked, Ralph kept)

## APPROVAL · 2026-10-08T10:40:10-05:00 · entity_approved · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Record - REVIEW.md (sha 76a048adc3f7)
Approved version: clients/apex-roofing-of-the-lowcountry/brand-guide.md#A+B1+B2 (sha 4d43186bd478)

## APPROVAL · 2026-10-08T10:40:10-05:00 · brand_guide_approved · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/brand-guide.md#A+D+E+G (sha b8be065916a5)

## RUN 20261008-104054-discovery-3010 · STARTED · /discovery · 2026-10-08T10:40:54-05:00
Step: discovery:signoff
Gates checked: entity_approved, proof_sheet_approved, proof_sheet_returned, brand_guide_approved, audit_approved
### HANDOFF · /discovery · 2026-10-08 · run 20261008-104054-discovery-3010
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
### END HANDOFF
## RUN 20261008-104054-discovery-3010 · FINISHED · 2026-10-08T10:42:34-05:00
Changes: 0 · Summary: Discovery Summary + client-confirmation list ready for sign-off

## APPROVAL · 2026-10-08T11:03:17-05:00 · discovery_signed_off · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/discovery/Apex Roofing of the Lowcountry - Discovery Summary - REVIEW.md (sha 564167710178)

## RUN 20261008-110342-drive-mirror-7c9f · STARTED · /drive-mirror · 2026-10-08T11:03:42-05:00
Step: drive-mirror
Gates checked: client_setup
- CHANGE #134 [drive_file] https://drive.google.com/file/d/1Zn4tgOB22pgwW6zmUxzb4qlN38YcMIzg/view | archive | old: Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #135 [drive_file] https://drive.google.com/file/d/1pQQOs1cVuCyjYjgl06uckov76rrod8ew/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (2).md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha b00363e098b9 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-110342-drive-mirror-7c9f/0135-new.md
- CHANGE #136 [drive_file] https://drive.google.com/file/d/1UHwtgvaJd9_CynPdValYLvaSnBlyHqx1/view | archive | old: Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #137 [drive_file] https://drive.google.com/file/d/1aRGFbGoDS7KFKsopoSfzfjsjLOKKdpvC/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (2).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha bdceeb28ebe4 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-110342-drive-mirror-7c9f/0137-new.md
- CHANGE #138 [drive_file] https://drive.google.com/file/d/1tmQQUTXCWNTURddqsut4550czVgusJEH/view | archive | old: Apex Roofing of the Lowcountry - Brand Guide.md | new: _Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #139 [drive_file] https://drive.google.com/file/d/1NkHQNyI1s-0SSrSI2ZweyeMFXZlAJMdg/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (2).md | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha 9b1146487d9e | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-110342-drive-mirror-7c9f/0139-new.md
- CHANGE #140 [drive_file] https://drive.google.com/file/d/1kq4xPLEqgMKtsmOjgbS5SDxjcEg4eTVT/view | archive | old: Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #141 [drive_file] https://drive.google.com/file/d/1GJD1q6sCbY9wFP5KfUAW_e2yC_6KAg5V/view | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (2).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 1b9b729adc46 | result: done | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/20261008-110342-drive-mirror-7c9f/0141-new.md
- CHANGE #142 [drive_file] https://drive.google.com/file/d/1UPd5Y_FAMeDaqEmy-F48Ic5dyeHnJaHs/view | file | old:  | new: Apex Roofing of the Lowcountry - Discovery Summary - APPROVED.md (Deliverables) | result: uploaded
### HANDOFF · /drive-mirror · 2026-10-08 · run 20261008-110342-drive-mirror-7c9f
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
### END HANDOFF
## RUN 20261008-110342-drive-mirror-7c9f · FINISHED · 2026-10-08T11:13:58-05:00
Changes: 9 · Summary: Drive mirror after Brand Guide approval and discovery sign-off (resumed)

## MIGRATION · 2026-10-08T12:21:53-05:00 · schema 4 (rewrite 2026-10-08)
Section approvals re-stamped (status columns no longer hashed): 2 · void approvals left void: 0 · now conditions: discovery_signed_off, blockers_cleared
- SETTLED entity · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Entity: category Roofing Contractor (variants Roofer, Roofers); area = Hilton Head Island–Bluffton–Port Royal metro area.
- SETTLED titles · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Titles: homepage SEO title uses "Hilton Head Island Metropolitan Area"; homepage H1 uses a familiar name (Lowcountry / South Carolina Lowcountry); service titles `Service Name - Apex Roofing of the Lowcountry` (no area); brand always in full.
- SETTLED homepage · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Homepage: links all 8 services (Paul exception).
- SETTLED about_page · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · About page: title "About Apex Roofing of the Lowcountry - Roofing Contractor in the Hilton Head Island–Bluffton–Port Royal Metropolitan Area"; H1 "About Apex Roofing of the Lowcountry"; Ralph and Pierce Brehany named only, with a visible placeholder for photo and titles.
- SETTLED business · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Business: residential only · 8 services kept · 12 towns (+ Brays Island, Lobeco) · not Georgia · SAB based in Bluffton · street address 6 Sutton Ct shown on the **website**, hidden on the **Google profile** · no travel fee · no public email · financing through Hearth · CertainTeed + GAF certified installers · lifetime no-leak workmanship warranty and 50-year manufacturer warranty, both transferable · blog author Ralph Brehany.
- SETTLED not_on_the_site_until_confirmed · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Not on the site until confirmed: "& Coastal Georgia", "homes and businesses", "residential and commercial inspections", ShingleMaster, "payment arrangements".
- SETTLED audit · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Audit: 30 findings (3 High, 18 Medium, 9 Low), advisory until the specs are approved; nothing removed or merged.
- SETTLED data · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Data: citations skipped for this audit; Search Console/Analytics not used; local grid from Local Dominator (ranks only).
- SETTLED drive · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul (STATUS.md, 2026-10-08) · Drive: the Finding Register and URL Decision Map stay in the repo only (too large for the Drive connector) until Drive for desktop is set up — `clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/deliverables/`.
- OPEN wordpress_login · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul · WordPress: connected (SEOPress 10.0.1). The login is an Administrator; Paul decides once whether Jonie switches it to an Editor. (ref Decision Sheet)
- OPEN send_the_client_one_question_is_your_cer · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Paul · Send the client one question: "Is your CertainTeed ShingleMaster status current?" (ref Brand Guide D)
- OPEN synthetic_roofing_offered · 2026-10-08T12:21:53-05:00 · run migration-v4 · by Client (via Paul) · Synthetic roofing offered? (decides where the broken /services/synthetic-roofing/ redirect points) · Port Royal base-housing work? · one confirmed price range (ref audit F-009, F-001, F-002)

## CONDITION · 2026-10-08T12:21:53-05:00 · Discovery and audit signed off — Build may start (met when the Decision Sheet, entity, client facts, audit and Brand Guide are approved and the client's facts are recorded) — met (system-verified)

## APPROVAL · 2026-10-08T13:15:46-05:00 · page specs (global) · approved · by Paul
Approved version: methodology/specs/README.md (sha 13bde3165a59)
Approved version: methodology/specs/about.md (sha 633163a215ae)
Approved version: methodology/specs/blog-post.md (sha bb60f76bddb0)
Approved version: methodology/specs/county-hub.md (sha 4ed0d3bfb1d8)
Approved version: methodology/specs/homepage.md (sha 645431d1fd4c)
Approved version: methodology/specs/location.md (sha bf5b163f4357)
Approved version: methodology/specs/service.md (sha 0d679dadad45)

## CONDITION · 2026-10-08T13:15:46-05:00 · Page specs approved by Paul once, globally (methodology/specs) and unchanged since — met (system-verified)

## RUN 20261008-131822-build:blockers-b359 · STARTED · /build:blockers · 2026-10-08T13:18:22-05:00
Step: build:blockers · session ca40bb8f-c2bb-4319-996b-d590e094e946
Gates checked: discovery_signed_off
- CHANGE #143 [redirect] https://apexroofingtlc.com/services/synthetic-roofing/ | 301 | old: 301 -> [REDACTED]/synthetic-roofing/ (404) | new: [REDACTED]/roof-replacement/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-03-redirect-01
- CHANGE #144 [redirect] https://apexroofingtlc.com/synthetic-roofing/ | 301 | old: 404 (no redirect) | new: [REDACTED]/roof-replacement/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-03-redirect-02
- CHANGE #145 [broken_link] https://apexroofingtlc.com/ (sitewide header 'Request A Quote' button + CTA block, 58 pages) | link href | old: [REDACTED]/contact | new: [REDACTED]/contact/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-01
- CHANGE #146 [broken_link] https://apexroofingtlc.com/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-02
- CHANGE #147 [broken_link] https://apexroofingtlc.com/beaufort/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-03
- CHANGE #148 [broken_link] https://apexroofingtlc.com/bluffton/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-04
- CHANGE #149 [broken_link] https://apexroofingtlc.com/fripp-island/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-05
- CHANGE #150 [broken_link] https://apexroofingtlc.com/hardeeville/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-06
- CHANGE #151 [broken_link] https://apexroofingtlc.com/hilton-head-island/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-07
- CHANGE #152 [broken_link] https://apexroofingtlc.com/ladys-island/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-08
- CHANGE #153 [broken_link] https://apexroofingtlc.com/levy/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-09
- CHANGE #154 [broken_link] https://apexroofingtlc.com/okatie/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-10
- CHANGE #155 [broken_link] https://apexroofingtlc.com/port-royal/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-11
- CHANGE #156 [broken_link] https://apexroofingtlc.com/pritchardville/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-12
- CHANGE #157 [broken_link] https://apexroofingtlc.com/ridgeland/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-13
- CHANGE #158 [broken_link] https://apexroofingtlc.com/st-helena-island/ | link href (services list/table: Metal Roofing) | old: [REDACTED]/metal-roofing/ | new: [REDACTED]/metal-roofing-2/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-14
- CHANGE #159 [broken_link] https://apexroofingtlc.com/does-your-roof-impact-your-energy-bill/ | in-post link href | old: [REDACTED]/services/roof-inspections/ | new: [REDACTED]/roof-inspections/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-15
- CHANGE #160 [broken_link] https://apexroofingtlc.com/does-your-roof-impact-your-energy-bill/ | in-post link href | old: [REDACTED]/services/skylight-repair/ | new: [REDACTED]/skylights/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-16
- CHANGE #161 [broken_link] https://apexroofingtlc.com/does-your-roof-impact-your-energy-bill/ | in-post link href | old: [REDACTED]/services/slate-roofing/ | new: [REDACTED]/slate-roofing/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-17
- CHANGE #162 [broken_link] https://apexroofingtlc.com/does-your-roof-impact-your-energy-bill/ | in-post link href | old: [REDACTED]/services/synthetic-roofing/ | new: [REDACTED]/roof-replacement/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-18
- CHANGE #163 [broken_link] https://apexroofingtlc.com/how-long-does-roof-last-hilton-head-humidity-salt-air/ | in-post link href | old: [REDACTED]/can-i-replace-my-roof-myself-beaufort-historic-district/ | new: [REDACTED]/beaufort/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-19
- CHANGE #164 [broken_link] https://apexroofingtlc.com/how-long-does-roof-last-hilton-head-humidity-salt-air/ | in-post link href | old: [REDACTED]/replace-roof-before-or-after-hurricane-season-bluffton-sc/ | new: [REDACTED]/bluffton/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-20
- CHANGE #165 [broken_link] https://apexroofingtlc.com/how-your-roof-affects-a-home-sale-in-bluffton/ | in-post link href | old: [REDACTED]/replace-roof-before-or-after-hurricane-season-bluffton-sc/ | new: [REDACTED]/bluffton/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-21
- CHANGE #166 [broken_link] https://apexroofingtlc.com/new-construction-roof-installed-correctly/ | in-post link href | old: [REDACTED]/new-roof-before-selling-house-hardeeville-sc/ | new: [REDACTED]/hardeeville/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-22
- CHANGE #167 [broken_link] https://apexroofingtlc.com/solar-panels-roof-hardeeville-sc/ | in-post link href | old: [REDACTED]/new-roof-before-selling-house-hardeeville-sc/ | new: [REDACTED]/hardeeville/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-23
- CHANGE #168 [broken_link] https://apexroofingtlc.com/old-town-bluffton-approved-roofing-materials/ | in-post link href | old: [REDACTED]/new-construction-roof-warranty-hardeeville-sc/ | new: [REDACTED]/hardeeville/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-24
- CHANGE #169 [broken_link] https://apexroofingtlc.com/top-questions-to-ask-your-roofing-contractor/ | in-post link href | old: [REDACTED]/roof-inspections-in-bluffton-sc-protecting-your-home-with-apex-roofing-of-the-lowcountry/ | new: [REDACTED]/bluffton/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-25
- CHANGE #170 [broken_link] https://apexroofingtlc.com/why-ventilation-matters-how-your-roof-can-reduce-summer-cooling-costs/ | in-post link href | old: [REDACTED]/brighten-your-beaufort-home-skylight-installation-by-apex-roofing-of-the-lowcountry/ | new: [REDACTED]/skylights/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-04-broken_link-26
- CHANGE #171 [sitemap] https://apexroofingtlc.com/roof-inspections-in-bluffton-sc-protecting-your-home-with-apex-roofing-of-the-lowcountry/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-01
- CHANGE #172 [sitemap] https://apexroofingtlc.com/emergency-roof-repair-in-hilton-head-island-sc-apex-roofing-of-the-lowcountry-is-here-when-you-need-us-most/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-02
- CHANGE #173 [sitemap] https://apexroofingtlc.com/roof-repair-in-ridgeland-sc-apex-roofing-of-the-lowcountry-keeps-your-home-safe-and-sound/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-03
- CHANGE #174 [sitemap] https://apexroofingtlc.com/transforming-homes-in-pritchardville-sc-apex-roofing-of-the-lowcountrys-expertise-in-roof-replacement/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-04
- CHANGE #175 [sitemap] https://apexroofingtlc.com/brighten-your-beaufort-home-skylight-installation-by-apex-roofing-of-the-lowcountry/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-05
- CHANGE #176 [sitemap] https://apexroofingtlc.com/replace-roof-before-or-after-hurricane-season-bluffton-sc/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-06
- CHANGE #177 [sitemap] https://apexroofingtlc.com/new-roof-before-selling-house-hardeeville-sc/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-07
- CHANGE #178 [sitemap] https://apexroofingtlc.com/new-construction-roof-warranty-hardeeville-sc/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-08
- CHANGE #179 [sitemap] https://apexroofingtlc.com/can-i-replace-my-roof-myself-beaufort-historic-district/ | XML sitemap inclusion | old: listed in post-sitemap1.xml (URL 301-redirects) | new: excluded from the XML sitemap (SEOPress per-post sitemap exclusion) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-05-sitemap-09
- CHANGE #180 [seo_title] https://apexroofingtlc.com/blog/ | SEOPress title | old: Our Blog | Apex Roofing of The Lowcountry | new: Our Blog - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-01
- CHANGE #181 [seo_title] https://apexroofingtlc.com/contact/ | SEOPress title | old: Contact Us | Apex Roofing of The Lowcountry | new: Contact Us - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-02
- CHANGE #182 [seo_title] https://apexroofingtlc.com/terms-conditions/ | SEOPress title | old: Terms & Conditions | Apex Roofing of The Lowcountry | new: Terms & Conditions - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-03
- CHANGE #183 [seo_title] https://apexroofingtlc.com/terms-conditions/accessibility-statement/ | SEOPress title | old: Accessibility Statement | Apex Roofing of The Lowcountry | new: Accessibility Statement - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-04
- CHANGE #184 [seo_title] https://apexroofingtlc.com/terms-conditions/cookie-policy/ | SEOPress title | old: Cookie Policy | Apex Roofing of The Lowcountry | new: Cookie Policy - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-05
- CHANGE #185 [seo_title] https://apexroofingtlc.com/terms-conditions/copyright-policy/ | SEOPress title | old: Copyright Policy | Apex Roofing of The Lowcountry | new: Copyright Policy - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-06
- CHANGE #186 [seo_title] https://apexroofingtlc.com/terms-conditions/privacy-policy/ | SEOPress title | old: Privacy Policy | Apex Roofing of The Lowcountry | new: Privacy Policy - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-06-seo_title-07
- CHANGE #187 [other] https://apexroofingtlc.com/ (sitewide footer 'About' text, every page) | footer text | old: APEX ROOFING of the Lowcountry is a residential roofing company ... APEX ROOFING’S commitment to excellence ... | new: Apex Roofing of the Lowcountry is a residential roofing company ... Apex Roofing of the Lowcountry’s commitment to excellence ... (change only the two brand-na… | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-07-other-01
- CHANGE #188 [other] https://apexroofingtlc.com/contact/ | heading level | old: <H3> CALL US TODAY! (directly under the H1, no H2) | new: same text as an H2 (heading level only; wording unchanged) | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-07-other-02
- CHANGE #189 [seo_title] https://apexroofingtlc.com/roof-repair/ | SEOPress title | old: Apex Roofing of the Lowcountry - Roof Repair - Hilton Head Island Metro Area | new: Roof Repair - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-01
- CHANGE #190 [seo_title] https://apexroofingtlc.com/roof-replacement/ | SEOPress title | old: Apex Roofing of the Lowcountry - Roof Replacement - Hilton Head Island Metro Area | new: Roof Replacement - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-02
- CHANGE #191 [seo_title] https://apexroofingtlc.com/roof-installation/ | SEOPress title | old: Apex Roofing of the Lowcountry - Roof Installation - Hilton Head Island Metro Area | new: Roof Installation - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-03
- CHANGE #192 [seo_title] https://apexroofingtlc.com/roof-inspections/ | SEOPress title | old: Apex Roofing of the Lowcountry - Roof Inspections - Hilton Head Island Metro Area | new: Roof Inspections - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-04
- CHANGE #193 [seo_title] https://apexroofingtlc.com/emergency-roof-repair/ | SEOPress title | old: Apex Roofing of the Lowcountry - Emergency Roof Repair - Hilton Head Island Metro Area | new: Emergency Roof Repair - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-05
- CHANGE #194 [seo_title] https://apexroofingtlc.com/metal-roofing-2/ | SEOPress title | old: Apex Roofing of the Lowcountry - Metal Roofing - Hilton Head Island Metro Area | new: Metal Roofing - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-06
- CHANGE #195 [seo_title] https://apexroofingtlc.com/slate-roofing/ | SEOPress title | old: Apex Roofing of the Lowcountry - Slate Roofing - Hilton Head Island Metro Area | new: Slate Roofing - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-07
- CHANGE #196 [seo_title] https://apexroofingtlc.com/skylights/ | SEOPress title | old: Apex Roofing of the Lowcountry - Skylights - Hilton Head Island Metro Area | new: Skylights - Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-08
- CHANGE #197 [seo_title] https://apexroofingtlc.com/about/ | SEOPress title | old: About Us | Apex Roofing of The Lowcountry | new: About Apex Roofing of the Lowcountry - Roofing Contractor in the Hilton Head Island–Bluffton–Port Royal Metropolitan Area | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-08-seo_title-09
- CHANGE #198 [h1] https://apexroofingtlc.com/about/ | H1 | old: About Us | new: About Apex Roofing of the Lowcountry | result: HANDOFF ISSUED to Jonie | ref H-2026-10-08-09-h1-01
- DECISION 2026-10-08T13:36 · run 20261008-131822-build:blockers-b359 · Paul chose (b): retitle the 8 service pages and /about/ now through Jonie, ahead of the rebuild. Issued H-2026-10-08-08-seo_title (9 titles) and H-2026-10-08-09-h1 (About H1), not flagged as blockers (they do not block crawling or measurement). · affects F-014,F-015
### HANDOFF · /build:blockers · 2026-10-08 · run 20261008-131822-build:blockers-b359
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
### END HANDOFF
## RUN 20261008-131822-build:blockers-b359 · FINISHED · 2026-10-08T13:36:41-05:00
Changes: 56 · Summary: Technical blocker checklist complete: 7 handoffs to Jonie (46 rows). High findings F-014/F-015/F-022 will be fixed in the rebuild. Choice (b): service and About page titles are being retitled now (H-08/H-09). Site plan can proceed in parallel.
- CHANGE #199 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #200 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 23b4aefd5cc0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #201 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #202 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Approval Record.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha 2142335ad324 | result: done · copied (Drive for desktop syncs it)
- CHANGE #203 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #204 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha e28773981955 | result: done · copied (Drive for desktop syncs it)
- CHANGE #205 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Status.md · sha 2e03c333eeb5 | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-08T13:44 · after build:blockers (run 20261008-131822-build:blockers-b359) · Paul typed /next

## RUN 20261008-134424-build:plan-c61b · STARTED · /build:plan · 2026-10-08T13:44:24-05:00
Step: build:plan · session ca40bb8f-c2bb-4319-996b-d590e094e946
Gates checked: discovery_signed_off
- CHANGE #206 [site_plan] clients/apex-roofing-of-the-lowcountry/brand-guide.md#H2 | Brand Guide H2 (CM-020 decisions) | old:  | new:  | result: OK | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261008-134424-build:plan-c61b/0206-old.md clients/apex-roofing-of-the-lowcountry/snapshots/20261008-134424-build:plan-c61b/0206-new.md
- CHANGE #207 [site_plan] clients/apex-roofing-of-the-lowcountry/audit/2026-10-07/url-decision-map.csv | CM-020 decision (20 rows) | old:  | new:  | result: OK | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261008-134424-build:plan-c61b/0207-old.csv clients/apex-roofing-of-the-lowcountry/snapshots/20261008-134424-build:plan-c61b/0207-new.csv
- CHANGE #208 [site_plan] https://apexroofingtlc.com/roof-repair/ | keyword | old: (none recorded in the audit) | new: roof repair | result: OK
- CHANGE #209 [site_plan] https://apexroofingtlc.com/roof-repair/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roof Leak and Damage Repair in the South Carolina Lowcountry — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #210 [site_plan] https://apexroofingtlc.com/roof-replacement/ | keyword | old: (none recorded in the audit) | new: roof replacement | result: OK
- CHANGE #211 [site_plan] https://apexroofingtlc.com/roof-replacement/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Re-Roofing in Beaufort and Jasper Counties — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #212 [site_plan] https://apexroofingtlc.com/roof-installation/ | keyword | old: (none recorded in the audit) | new: roof installation | result: OK
- CHANGE #213 [site_plan] https://apexroofingtlc.com/roof-installation/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: New-Construction Roofing in the South Carolina Lowcountry — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #214 [site_plan] https://apexroofingtlc.com/roof-inspections/ | keyword | old: (none recorded in the audit) | new: roof inspection | result: OK
- CHANGE #215 [site_plan] https://apexroofingtlc.com/roof-inspections/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roof Condition Inspections in Beaufort and Jasper Counties — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #216 [site_plan] https://apexroofingtlc.com/emergency-roof-repair/ | keyword | old: (none recorded in the audit) | new: emergency roof repair | result: OK
- CHANGE #217 [site_plan] https://apexroofingtlc.com/emergency-roof-repair/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Storm and Leak Emergency Roofing in the South Carolina Lowcountry — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #218 [site_plan] https://apexroofingtlc.com/metal-roofing-2/ | keyword | old: (none recorded in the audit) | new: metal roofing | result: OK
- CHANGE #219 [site_plan] https://apexroofingtlc.com/metal-roofing-2/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Standing Seam Metal Roofs in Beaufort and Jasper Counties — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #220 [site_plan] https://apexroofingtlc.com/slate-roofing/ | keyword | old: (none recorded in the audit) | new: slate roofing | result: OK
- CHANGE #221 [site_plan] https://apexroofingtlc.com/slate-roofing/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Natural Slate Roofs in the South Carolina Lowcountry — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #222 [site_plan] https://apexroofingtlc.com/skylights/ | keyword | old: (none recorded in the audit) | new: skylight installation | result: OK
- CHANGE #223 [site_plan] https://apexroofingtlc.com/skylights/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Skylight Installation in Beaufort and Jasper Counties — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #224 [site_plan] https://apexroofingtlc.com/bluffton/ | keyword | old: (none recorded in the audit) | new: roofing contractor bluffton sc | result: OK
- CHANGE #225 [site_plan] https://apexroofingtlc.com/bluffton/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Bluffton — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #226 [site_plan] https://apexroofingtlc.com/hilton-head-island/ | keyword | old: (none recorded in the audit) | new: roofing contractor hilton head island sc | result: OK
- CHANGE #227 [site_plan] https://apexroofingtlc.com/hilton-head-island/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers on Hilton Head Island — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #228 [site_plan] https://apexroofingtlc.com/okatie/ | keyword | old: (none recorded in the audit) | new: roofing contractor okatie sc | result: OK
- CHANGE #229 [site_plan] https://apexroofingtlc.com/okatie/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Okatie — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #230 [site_plan] https://apexroofingtlc.com/pritchardville/ | keyword | old: (none recorded in the audit) | new: roofing contractor pritchardville sc | result: OK
- CHANGE #231 [site_plan] https://apexroofingtlc.com/pritchardville/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Pritchardville — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #232 [site_plan] https://apexroofingtlc.com/beaufort/ | keyword | old: (none recorded in the audit) | new: roofing contractor beaufort sc | result: OK
- CHANGE #233 [site_plan] https://apexroofingtlc.com/beaufort/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Beaufort — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #234 [site_plan] https://apexroofingtlc.com/port-royal/ | keyword | old: (none recorded in the audit) | new: roofing contractor port royal sc | result: OK
- CHANGE #235 [site_plan] https://apexroofingtlc.com/port-royal/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Port Royal — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #236 [site_plan] https://apexroofingtlc.com/ladys-island/ | keyword | old: (none recorded in the audit) | new: roofing contractor lady's island sc | result: OK
- CHANGE #237 [site_plan] https://apexroofingtlc.com/ladys-island/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers on Lady's Island — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #238 [site_plan] https://apexroofingtlc.com/st-helena-island/ | keyword | old: (none recorded in the audit) | new: roofing contractor st. helena island sc | result: OK
- CHANGE #239 [site_plan] https://apexroofingtlc.com/st-helena-island/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers on St. Helena Island — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #240 [site_plan] https://apexroofingtlc.com/fripp-island/ | keyword | old: (none recorded in the audit) | new: roofing contractor fripp island sc | result: OK
- CHANGE #241 [site_plan] https://apexroofingtlc.com/fripp-island/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers on Fripp Island — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #242 [site_plan] https://apexroofingtlc.com/hardeeville/ | keyword | old: (none recorded in the audit) | new: roofing contractor hardeeville sc | result: OK
- CHANGE #243 [site_plan] https://apexroofingtlc.com/hardeeville/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Hardeeville — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #244 [site_plan] https://apexroofingtlc.com/ridgeland/ | keyword | old: (none recorded in the audit) | new: roofing contractor ridgeland sc | result: OK
- CHANGE #245 [site_plan] https://apexroofingtlc.com/ridgeland/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Ridgeland — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- CHANGE #246 [site_plan] https://apexroofingtlc.com/levy/ | keyword | old: (none recorded in the audit) | new: roofing contractor levy sc | result: OK
- CHANGE #247 [site_plan] https://apexroofingtlc.com/levy/ | h1 | old: live H1 opens 'The Best' (F-011); repeats title variant (F-012) | new: Roofers in Levy — no 'The Best' (CM-020: condition 2 unmeasured) | result: OK
- DECISION 2026-10-08T14:02 · run 20261008-134424-build:plan-c61b · Site plan: CM-020 'The Best' applied to no service or location page — condition 2 (opportunity) unmeasured on all 20; condition 1 passes only for roof repair, roof replacement, skylights (vol 10). No top-3 locks. Re-test (~$0.04 SERP) offered to Paul, not spent. · affects F-011
- DECISION 2026-10-08T14:02 · run 20261008-134424-build:plan-c61b · Site plan: generic questions routed to towns (damage signs, when to replace, cost, best season, choosing a roofer, coastal materials on Lady's Island) moved to service pages, homepage FAQ or blog list (C8). 15 location FAQ slots have no sourced town-specific question — to the facts interview at each evidence step unless Paul supplies topics. · affects F-021
- DECISION 2026-10-08T14:02 · run 20261008-134424-build:plan-c61b · Site plan: Levy batched with Jasper County (inventory says Beaufort) — county to be sourced at the evidence step; Levy moves to l1 if Beaufort.
- DECISION 2026-10-08T14:02 · run 20261008-134424-build:plan-c61b · Site plan: B2 variant 'Hilton Head Island–Bluffton–Port Royal Metropolitan Area' contains city names, so it is not used in any service-page H tag (SVC-07/SVC-12); service H1s rotate 'South Carolina Lowcountry' and 'Beaufort and Jasper Counties'. Not exhausted — no CM-013 finding (CM-031 OPEN).
- OPEN site_plan_open_choices · 2026-10-08T14:02:54-05:00 · run 20261008-134424-build:plan-c61b · by Paul · Site plan open choices: (1) homepage vs Hilton Head Island keyword; (2) permit FAQs — 2 (F-021) or 5; (3) 'The Best' SERP re-test ~$0.04 yes/no; (4) add 'Residential Roofer' to category variants; (5) 15 location FAQ gaps — facts interview, Paul's topics, or accept 2 FAQs (ref Site Plan §6)
- CHANGE #248 [site_plan] https://apexroofingtlc.com/ | keyword | old: hilton head roofing company | new: roofing company hilton head island metro area | result: OK
- CHANGE #249 [site_plan] https://apexroofingtlc.com/hilton-head-island/ | faq_topics | old: Do I need a Town of Hilton Head Island permit for a new roof? | new: dropped (Paul 2a: permit FAQ on Bluffton and Ridgeland only); FO 275, 307 to blog list; slot to facts interview | result: OK
- CHANGE #250 [site_plan] https://apexroofingtlc.com/okatie/ | faq_topics | old: Is an Okatie home under Beaufort County or Jasper County rules? | new: dropped (Paul 2a); slot to facts interview | result: OK
- CHANGE #251 [site_plan] https://apexroofingtlc.com/pritchardville/ | faq_topics | old: Is Pritchardville inside the Town of Bluffton for roofing permits? | new: dropped (Paul 2a); slot to facts interview | result: OK
- CHANGE #252 [site_plan] https://apexroofingtlc.com/roof-repair/ | cm020_opportunity | old: Unmeasured | new: Fail: SERP 2026-10-08 best roof repair near hilton head sc, 1 of 10 titles use best (Yelp), Apex not top 10; decision unchanged, no The Best | result: OK
- CHANGE #253 [site_plan] https://apexroofingtlc.com/roof-replacement/ | cm020_opportunity | old: Unmeasured | new: Fail: SERP 2026-10-08 best roof replacement near hilton head sc, 2 of 10 titles use best (downtobid, Yelp), Apex not top 10; decision unchanged, no The Best | result: OK
- CHANGE #254 [site_plan] https://apexroofingtlc.com/skylights/ | cm020_opportunity | old: Unmeasured | new: Fail: SERP 2026-10-08 best skylights near hilton head sc, 2 of 10 titles use best (Yelp, out-of-area page), Apex not top 10; decision unchanged, no The Best | result: OK
- SETTLED site_plan_open_choices · 2026-10-08T14:25:16-05:00 · run 20261008-134424-build:plan-c61b · by Paul · Paul 2026-10-08 site plan choices: 1a homepage keyword to metro level (roofing company hilton head island metro area); 2a permit FAQ on Bluffton and Ridgeland only (HHI, Okatie, Pritchardville jurisdiction FAQs dropped, FO 275/307 to blog list); 3b The Best SERP re-test run; 4a Residential Roofer approved as a category variant; 5a location FAQ gaps (now 18) sourced in the facts interview at each location batch evidence step
- SETTLED cm020_serp_retest_2026_10_08 · 2026-10-08T14:25:16-05:00 · run 20261008-134424-build:plan-c61b · by Paul · CM-020 SERP re-test (Paul yes, spent 0.006 USD, 3 Google top-10 reads from Hilton Head Island): condition 2 fails for Roof Repair (1/10 best titles), Roof Replacement (2/10), Skylights (2/10, mostly out-of-area results); only directory lists use best, Apex not in top 10. No page gets The Best; re-test after launch once pages rank.
- OPEN residential_roofer_a3_write · 2026-10-08T14:25:16-05:00 · run 20261008-134424-build:plan-c61b · by Paul · Residential Roofer (choice 4a) lives in Brand Guide A3, inside entity_approved (A+B1+B2) and brand_guide_approved (A+D+E+G). Writing it voids both until re-approved. (i) write now and re-approve: /approve apex-roofing-of-the-lowcountry entity_approved brand_guide_approved site_plan; or (ii) use it on the site plan authority and write A3 at the next Brand Guide revision. A3 not edited.
### HANDOFF · /build:plan · 2026-10-08 · run 20261008-134424-build:plan-c61b
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
### END HANDOFF
## RUN 20261008-134424-build:plan-c61b · FINISHED · 2026-10-08T14:27:16-05:00
Changes: 49 · Summary: Site plan complete for all 20 service and location pages. Keywords assigned, H1 decisions settled (no 'The Best'), 37 service and 19 location FAQs with no repeats. Town FAQ gaps (18 slots) to be sourced in facts interviews. Google 'best' check run: no page qualifies (competitors don't rank with 'best'). Batches: pilot (Roof Repair + Bluffton) → s1/s2 (services) → l1/l2/l3 (locations) → home/about.
- CHANGE #255 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #256 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 7245469a05b0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #257 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #258 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Approval Record.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha 7b5a9d70c71e | result: done · copied (Drive for desktop syncs it)
- CHANGE #259 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #260 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 99081a96041f | result: done · copied (Drive for desktop syncs it)
- CHANGE #261 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Brand Guide.md | new: _Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #262 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Brand Guide.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha 827ca00d5281 | result: done · copied (Drive for desktop syncs it)
- CHANGE #263 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08.md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08.md | result: done · renamed and moved, nothing deleted
- CHANGE #264 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08.md | new: Apex Roofing of the Lowcountry - Status.md · sha ea2001ca35c8 | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-08T14:28:51-05:00 · site plan · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Site Plan - REVIEW.md (sha f7b3f00ad9b0)
- CHANGE #265 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/Apex Roofing of the Lowcountry - Site Plan - APPROVED.md | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Site Plan - APPROVED.md · sha dabf1e6f6bc4 | result: done · copied (Drive for desktop syncs it) | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/approval-2026-10-08/0265-new.tmp
- CHANGE #266 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #267 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (4).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 0604ddbb2451 | result: done · copied (Drive for desktop syncs it)
- CHANGE #268 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (2).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #269 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08 (2).md | new: Apex Roofing of the Lowcountry - Status.md · sha 22e996c5668c | result: done · copied (Drive for desktop syncs it)

## RUN 20261008-143018-build-a144 · STARTED · /build · 2026-10-08T14:30:18-05:00
Step: build:evidence · batch pilot · session 74dd4cab-747d-4ef8-8581-f0c3e1a48356
Gates checked: discovery_signed_off, batch:pilot:briefs_ready, page_specs_approved
- EVIDENCE 2026-10-08T14:34 · run 20261008-143018-build-a144 · svc-roof-repair: BLOCK (known 1, unknown 2, unverified 9, conflict 0)
- EVIDENCE 2026-10-08T14:34 · run 20261008-143018-build-a144 · loc-bluffton: BLOCK (known 4, unknown 0, unverified 6, conflict 0)
- DECISION 2026-10-08T14:35 · run 20261008-143018-build-a144 · Evidence gate pilot: evidence.py recorded BLOCK for svc-roof-repair and loc-bluffton, but the BLOCKs come mostly from a status-parsing mismatch: mark() accepts only a bare status word, and every Brand Guide A/D status cell carries dates and qualifiers (e.g. 'Paul Approved 2026-10-06 · was: Submitted'), so Phone, Free estimate, Warranty, Insurance, Certifications, Rating, Emergency all read Unverified. Reading each cell's leading status with the CM-041 thresholds unchanged: svc-roof-repair WARN (required gap: service scope; supporting gaps: timeframe, pricing, guarantees), loc-bluffton WARN (required gap: neighborhoods, 5 of 6 verified; supporting gap: response time). Recorded gate result left as BLOCK; nothing waived, Brand Guide and script not edited. Paul to choose: fix the parser in a system session and re-run, facts interview, or waiver.
### HANDOFF · /build · 2026-10-08 · run 20261008-143018-build-a144
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
### END HANDOFF
## RUN 20261008-143018-build-a144 · FINISHED · 2026-10-08T15:00:27-05:00
Changes: 0 · Summary: Evidence gate ran; script bug blocked both pages (status parsing). Real gaps: repair scope confirmation, 6th neighborhood for Bluffton, response time. Paul waived blocks and approved forward to briefs. Pages to brief: svc-roof-repair (service), loc-bluffton (location).
- CHANGE #270 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #271 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (4).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha d139a3c65ca2 | result: done · copied (Drive for desktop syncs it)
- CHANGE #272 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (5).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #273 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (5).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 884479eb2112 | result: done · copied (Drive for desktop syncs it)
- CHANGE #274 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #275 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08 (3).md | new: Apex Roofing of the Lowcountry - Status.md · sha 87ca25934b90 | result: done · copied (Drive for desktop syncs it)

## WAIVER · 2026-10-08T15:05:35-05:00 · evidence gate · page svc-roof-repair · by Paul
Grid: clients/apex-roofing-of-the-lowcountry/build/evidence/svc-roof-repair.grid.md (sha bb154bf1bbfc) · was BLOCK: 3 required facts are not known (block at 2); only 1 known fact(s) — fewer than 3 (CM-015)
Reason: Real gaps identified (repair scope, neighborhoods, response time); move forward with briefs using industry standards + competitor research + local context; verify during drafting.

## WAIVER · 2026-10-08T15:05:35-05:00 · evidence gate · page loc-bluffton · by Paul
Grid: clients/apex-roofing-of-the-lowcountry/build/evidence/loc-bluffton.grid.md (sha d11f68d624a4) · was BLOCK: 3 required facts are not known (block at 2)
Reason: Real gaps identified (repair scope, neighborhoods, response time); move forward with briefs using industry standards + competitor research + local context; verify during drafting.
- CHANGE #276 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (6).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #277 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (6).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha da3c2e54840a | result: done · copied (Drive for desktop syncs it)
- CHANGE #278 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #279 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08 (4).md | new: Apex Roofing of the Lowcountry - Status.md · sha d792a169baea | result: done · copied (Drive for desktop syncs it)

## RUN 20261008-150539-build-a2ae · STARTED · /build · 2026-10-08T15:05:39-05:00
Step: build:brief · batch pilot · session 74dd4cab-747d-4ef8-8581-f0c3e1a48356
Gates checked: discovery_signed_off, batch:pilot:briefs_ready, evidence:svc-roof-repair, page_specs_approved
- BRIEF 2026-10-08T22:18 · run 20261008-150539-build-a2ae · svc-roof-repair · clients/apex-roofing-of-the-lowcountry/build/pilot/SB - Roof Repair - Apex Roofing of the Lowcountry.md
- DECISION 2026-10-08T22:20 · run 20261008-150539-build-a2ae · Roof Repair brief: Paul's evidence waiver applied narrowly. Submitted repair types go into the brief marked [NEED] and block publication. No competitor research was done (CM-016; outside the read list). The 25% rule FAQ needs a cited SC code source or must be reworded or dropped (Paul's choice). Brief named SB - Roof Repair - Apex Roofing of the Lowcountry.md per the naming convention.
### HANDOFF · /build · 2026-10-08 · run 20261008-150539-build-a2ae
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
### END HANDOFF
## RUN 20261008-150539-build-a2ae · FINISHED · 2026-10-08T22:21:57-05:00
Changes: 0 · Summary: Roof Repair brief written. H1 no 'The Best' (search test failed CM-020). FAQ sections set. Evidence gaps flagged [NEED] on repair types; repair warranty, duration, cost drivers unknown. Flags: 25% rule may not apply in SC; repair warranty term needs client clarification; facts interview needed on repair scope, duration, cost drivers, warranty, methods.
- CHANGE #280 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (5).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #281 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (5).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 9fcc0fcee699 | result: done · copied (Drive for desktop syncs it)
- CHANGE #282 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (7).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #283 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (7).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha eb02a978390e | result: done · copied (Drive for desktop syncs it)
- CHANGE #284 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (5).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #285 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08 (5).md | new: Apex Roofing of the Lowcountry - Status.md · sha 25b83cab1337 | result: done · copied (Drive for desktop syncs it)

## RUN 20261008-222200-build-f8f3 · STARTED · /build · 2026-10-08T22:22:00-05:00
Step: build:brief · batch pilot · session 74dd4cab-747d-4ef8-8581-f0c3e1a48356
Gates checked: discovery_signed_off, batch:pilot:briefs_ready, evidence:loc-bluffton, page_specs_approved
- BRIEF 2026-10-08T22:27 · run 20261008-222200-build-f8f3 · loc-bluffton · clients/apex-roofing-of-the-lowcountry/build/pilot/LB - Bluffton - Apex Roofing of the Lowcountry.md
- BRIEFS COLLECTED 2026-10-08T22:27 · batch pilot · 2 page(s), one run each
- DECISION 2026-10-08T22:27 · run 20261008-222200-build-f8f3 · Bluffton brief: Paul's evidence waiver applied narrowly. No response time and no competitor claims used (CM-016; BG-D Guarantees Unknown) despite the request to use industry standards and competitor claims. Neighborhoods limited to the 5 Wikipedia-verified names (6th is [NEED], LOC-15 fails until sourced). FAQs 1-3 need a cited Town of Bluffton source or client confirmation; only FAQ 4 answerable now. Brief named LB (not LD, which is reserved for the approved draft) per the naming convention.
### HANDOFF · /build · 2026-10-08 · run 20261008-222200-build-f8f3
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
### END HANDOFF
## RUN 20261008-222200-build-f8f3 · FINISHED · 2026-10-08T22:29:33-05:00
Changes: 0 · Summary: Bluffton brief written. H1 'Roofers in Bluffton', keyword 'roofing contractor bluffton sc' (avoids homepage repeat). Based-in-Bluffton angle. FAQ: 1 answerable (based in Bluffton); 2 need Town of Bluffton sources; 1 needs client confirmation (gated communities). Neighborhoods: 5 sourced from Wikipedia (need 6 for spec). Address/phone confirmed from Paul's 2026-10-08 decision.
- CHANGE #286 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (6).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #287 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (6).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 02fabe719cf7 | result: done · copied (Drive for desktop syncs it)
- CHANGE #288 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (8).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (8).md | result: done · renamed and moved, nothing deleted
- CHANGE #289 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (8).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 9a12a059f0b4 | result: done · copied (Drive for desktop syncs it)
- CHANGE #290 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (6).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #291 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08 (6).md | new: Apex Roofing of the Lowcountry - Status.md · sha 75ea1ad803c4 | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-09T12:22:53-05:00 · batch pilot briefs · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/build/pilot/SB - Roof Repair - Apex Roofing of the Lowcountry.md (sha 5cdcd8fe897a)
Approved version: clients/apex-roofing-of-the-lowcountry/build/pilot/LB - Bluffton - Apex Roofing of the Lowcountry.md (sha 8b70358ea294)
- CHANGE #292 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (9).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (9).md | result: done · renamed and moved, nothing deleted
- CHANGE #293 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-08 (9).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha ab0d35ad957e | result: done · copied (Drive for desktop syncs it)
- CHANGE #294 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (7).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-08 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #295 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-08 (7).md | new: Apex Roofing of the Lowcountry - Status.md · sha 2461b89098dd | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-122305-build-e8c2 · STARTED · /build · 2026-10-09T12:23:05-05:00
Step: build:draft · batch pilot · session 74dd4cab-747d-4ef8-8581-f0c3e1a48356
Gates checked: discovery_signed_off, batch:pilot:briefs, page_specs_approved
- DRAFT 2026-10-09T12:33 · run 20261009-122305-build-e8c2 · svc-roof-repair · clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md
### HANDOFF · /build · 2026-10-09 · run 20261009-122305-build-e8c2
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
### END HANDOFF
## RUN 20261009-122305-build-e8c2 · FINISHED · 2026-10-09T12:35:57-05:00
Changes: 0 · Summary: Roof Repair draft written. Passes E1–E10 and all spec checks SVC-03–SVC-22. Grade 5.6 reading level, 6 page-specific facts, no city in headings, no 'The Best'. Two decisions: 25% rule (SC source, general answer, or drop); first H2 area term 'Beaufort and Jasper Counties' acceptable. Flagged [NEED]: repair types, job duration, warranty term, photos, owners on roof, flashing/underlayment (facts interview items). Emergency FAQ answer in words only (no link, CM-005).
- CHANGE #296 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (7).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #297 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-08 (7).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 1d68eacfdda7 | result: done · copied (Drive for desktop syncs it)
- CHANGE #298 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09.md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #299 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09.md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 82c05cd944e8 | result: done · copied (Drive for desktop syncs it)
- CHANGE #300 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09.md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #301 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09.md | new: Apex Roofing of the Lowcountry - Status.md · sha db85be01e567 | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-09T12:38 · after build:draft (run 20261009-122305-build-e8c2) · Paul typed /next

## RUN 20261009-123816-build-2c02 · STARTED · /build · 2026-10-09T12:38:16-05:00
Step: build:draft · batch pilot · session 40f19473-200f-425f-ad55-135b59d4f873
Gates checked: discovery_signed_off, batch:pilot:briefs, page_specs_approved
- CHANGE #302 [content_draft] https://apexroofingtlc.com/bluffton/ | LD draft file | old: (none) | new: build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | result: written
- DECISION 2026-10-09T12:43 · run 20261009-123816-build-2c02 · Route A applied for the loc-bluffton draft: status.json client.route is unset (status.py show prints no route); the Paul-approved LB brief states Route A and the pilot briefs were approved as Route A briefs. Not settled - Paul may set the route.
- DECISION 2026-10-09T12:43 · run 20261009-123816-build-2c02 · loc-bluffton draft: FAQ 1 (Town permit) sourced during drafting per Paul's waiver ('verify during drafting'): Town of Bluffton Applications, Certificates, Forms and Permitting page https://www.townofbluffton.sc.gov/228/Applications-Certificates-Forms-and-Perm (read 2026-10-09) lists a RE-Roof Building Permit Application, Roof Fastener and Shingles Certificate, Ice and Water Shield Certificate, Flashing Affidavit, and a Certificate of Appropriateness HD Application. FAQ 2 Old Town material list and the COFA-for-re-roof rule (UDO 3.18 / Article 5) not read in primary text - left as [NEED]. Whether Apex pulls the permit - [NEED] client.
- DECISION 2026-10-09T12:43 · run 20261009-123816-build-2c02 · loc-bluffton draft deviates from the approved brief in one heading: FAQ 3 H3 drops 'Belfair' ('Do you replace roofs in Palmetto Bluff and other gated Bluffton communities?') because Belfair's location in Bluffton is not publicly verified (facts file); Belfair stays inside the [NEED: W9] marker. Paul may restore it at draft approval.
- DRAFT 2026-10-09T12:43 · run 20261009-123816-build-2c02 · loc-bluffton · clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md
### HANDOFF · /build · 2026-10-09 · run 20261009-123816-build-2c02
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
### END HANDOFF
## RUN 20261009-123816-build-2c02 · FINISHED · 2026-10-09T12:43:45-05:00
Changes: 1 · Summary: Pilot Bluffton location draft written (LD), E1-E10 pass, LOC-15 fails 5/6 neighborhoods, NEEDs open
- CHANGE #303 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09.md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #304 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09.md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 06d7a06b2301 | result: done · copied (Drive for desktop syncs it)
- CHANGE #305 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (2).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #306 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (2).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha d5c185b8e786 | result: done · copied (Drive for desktop syncs it)
- CHANGE #307 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (2).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #308 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (2).md | new: Apex Roofing of the Lowcountry - Status.md · sha 488fdbc605a3 | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-09T12:48 · after build:draft (run 20261009-123816-build-2c02) · Paul typed /next

## RUN 20261009-124809-build-ab2d · STARTED · /build · 2026-10-09T12:48:09-05:00
Step: build:drafts · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts_ready
- DECISION 2026-10-09T12:50 · run 20261009-124809-build-ab2d · Pilot batch review: SEM-1 to SEM-7 have no definition in writing-commercial.md (NEED from the live gem, Section G); the semantic review used SEM-8 plus E1, C7, A7 and BB-310 to tag findings. 11 rows; sibling check found no FAQ or heading collision between svc-roof-repair and loc-bluffton.
### HANDOFF · /build · 2026-10-09 · run 20261009-124809-build-ab2d
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
### END HANDOFF
## RUN 20261009-124809-build-ab2d · FINISHED · 2026-10-09T12:50:36-05:00
Changes: 0 · Summary: Pilot batch review: sibling check clean on FAQs/headings; semantic review table with 11 SEM items for Paul
- CHANGE #309 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (2).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (2).md | result: done · renamed and moved, nothing deleted
- CHANGE #310 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (2).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 97d570f4725d | result: done · copied (Drive for desktop syncs it)
- CHANGE #311 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #312 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (3).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 3e11f611b75c | result: done · copied (Drive for desktop syncs it)
- CHANGE #313 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #314 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (3).md | new: Apex Roofing of the Lowcountry - Status.md · sha 6118f8bf5227 | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-130919-build-89b2 · STARTED · /build · 2026-10-09T13:09:19-05:00
Step: build:drafts · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts_ready
- SETTLED w25_who_goes_on_the_roof · 2026-10-09T13:10:06-05:00 · run 20261009-130919-build-89b2 · by Paul · W25 answered by Paul 2026-10-09: father and son, Ralph and Pierce Brehany, both get on the roof. Founder line on Roof Repair kept (pilot SEM row 9 -> SEM-4); only the W25 [NEED] is removed when SEM-4 is applied.
- DECISION 2026-10-09T13:10 · run 20261009-130919-build-89b2 · Paul's answers to the pilot semantic review (11 rows, re-issued as SEM-1..SEM-8): row 1 keep the emergency-leak FAQ on Roof Repair and link it to /emergency-roof-repair/ (not routed); row 9 keep founder line (W25 answered); row 10 move Hail Damage Repair to the Emergency Roof Repair page and remove the H3 from Roof Repair; rows 2-8 and 11 apply as suggested, row 5 localized to Bluffton rather than cut. Paul accepts the Bluffton depth complaint (cut Bluffton down) - not a SEM item, no copy changed in this report-only run.
- OPEN pilot_emergency_faq_link_cm022 · 2026-10-09T13:10:06-05:00 · run 20261009-130919-build-89b2 · by Paul · SEM-1: Paul wants the Roof Repair emergency-leak FAQ linked to /emergency-roof-repair/. CM-022 keeps links on service pages in tables/H3s, never in prose; an in-answer link is a contextual-link exception proposed in Finish for Paul's approval, and CM-005 bars Build from placing links. Applying SEM-1 in Build leaves a link placeholder in the answer; the link itself is proposed as the page's one CM-022 exception in Finish. Confirm that path, or name another.
### HANDOFF · /build · 2026-10-09 · run 20261009-130919-build-89b2
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
### END HANDOFF
## RUN 20261009-130919-build-89b2 · FINISHED · 2026-10-09T13:11:08-05:00
Changes: 0 · Summary: Pilot semantic review re-issued as SEM-1..SEM-8 (11 rows consolidated, Paul's answers built in; W25 settled; drafts unchanged)
- CHANGE #315 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (3).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (3).md | result: done · renamed and moved, nothing deleted
- CHANGE #316 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (3).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 6499f26a1f59 | result: done · copied (Drive for desktop syncs it)
- CHANGE #317 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #318 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (4).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha ae346eaaed21 | result: done · copied (Drive for desktop syncs it)
- CHANGE #319 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #320 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (4).md | new: Apex Roofing of the Lowcountry - Status.md · sha 34817178b4cf | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-09T13:14:08-05:00 · batch pilot drafts · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md (sha 7af4c4593579)
Approved version: clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md (sha c59a53c719cd)
Approved version: clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md (sha 9c47a05960c6)
SEM items to apply: SEM-1, SEM-2, SEM-3, SEM-4, SEM-5, SEM-6, SEM-7, SEM-8
- CHANGE #321 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED.md | upload | old: (new file) | new: Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED.md · sha 6d8e1fd46ebf | result: done · copied (Drive for desktop syncs it) | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/approval-2026-10-09/0321-new.tmp
- CHANGE #322 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (5).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #323 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (5).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 4a30fe36cf9b | result: done · copied (Drive for desktop syncs it)
- CHANGE #324 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (5).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #325 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (5).md | new: Apex Roofing of the Lowcountry - Status.md · sha 6f081e464bcc | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-131416-build-ec1c · STARTED · /build · 2026-10-09T13:14:16-05:00
Step: build:apply-sem · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts
- CHANGE #326 [content_draft] https://apexroofingtlc.com/roof-repair/ | SD draft file (SEM-1,2,3,4,5) | old:  | new:  | result: applied | ref SEM-1 emergency FAQ link placeholder; SEM-2 opening/CTA reworded, on-call kept here; SEM-3 flashing FAQ dropped, Roof Leak Repair lead replaced; SEM-4 founder line -> Ralph and Pierce both get on the roof, W25 NEED removed; SEM-5 hail H3 and mention removed (routed to svc-emergency-roof-repair) | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261009-131416-build-ec1c/0326-old.md clients/apex-roofing-of-the-lowcountry/snapshots/20261009-131416-build-ec1c/0326-new.md
- CHANGE #327 [content_draft] https://apexroofingtlc.com/bluffton/ | LD draft file (SEM-2,6,7,8 + depth cut) | old:  | new:  | result: applied | ref SEM-2 opening/CTA reworded, on-call removed; SEM-6 FAQ answer no longer repeats opening or licence, climate tied to May River/New River/20 ft; SEM-7 sibling H2 names Bluffton; SEM-8 'each with its own page' dropped; Paul's depth cut: body 834 -> 788 words | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261009-131416-build-ec1c/0327-old.md clients/apex-roofing-of-the-lowcountry/snapshots/20261009-131416-build-ec1c/0327-new.md
- DECISION 2026-10-09T13:17 · run 20261009-131416-build-ec1c · SEM-5 routed: hail/storm damage repair (H3 + lead-list mention) removed from svc-roof-repair and routed to the svc-emergency-roof-repair brief (later batch); it still needs the client's confirmation of hail repair before it ships.
- DECISION 2026-10-09T13:17 · run 20261009-131416-build-ec1c · Bluffton depth cut (Paul, 2026-10-09) applied inside this apply-sem run: no location-spec section dropped (services table, local context, 4 FAQs, neighborhoods, map, Things to Do, Top Sites, siblings, CTA all kept); cuts were the permit-forms list, the generic climate sentence, the FAQ-4 repeat of the opening and shorter lead sentences. Body 834 -> 788 words; what remains is spec-required. No fact added.
- DECISION 2026-10-09T13:17 · run 20261009-131416-build-ec1c · SEM-1 applied per Paul's yes: the Roof Repair emergency FAQ carries a link placeholder to /emergency-roof-repair/; no link placed in Build (CM-005). Finish proposes it as the page's one CM-022 contextual-link exception for Paul's approval (open question pilot_emergency_faq_link_cm022 stays open until Finish).
- SEM APPLIED 2026-10-09T13:17 · batch pilot · SEM-1, SEM-2, SEM-3, SEM-4, SEM-5, SEM-6, SEM-7, SEM-8 · E-checks passed · approval pinned to the applied versions
### HANDOFF · /build · 2026-10-09 · run 20261009-131416-build-ec1c
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
### END HANDOFF
## RUN 20261009-131416-build-ec1c · FINISHED · 2026-10-09T13:18:09-05:00
Changes: 2 · Summary: Pilot SEM-1..8 applied to Roof Repair and Bluffton, Bluffton cut 834->788 words; E1-E10 and spec checks pass
- CHANGE #328 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #329 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (4).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 88ec09fe6670 | result: done · copied (Drive for desktop syncs it)
- CHANGE #330 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (6).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #331 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (6).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha fc01962ef580 | result: done · copied (Drive for desktop syncs it)
- CHANGE #332 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (6).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #333 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (6).md | new: Apex Roofing of the Lowcountry - Status.md · sha 84fe08666882 | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-09T13:19 · after build:apply-sem (run 20261009-131416-build-ec1c) · Paul typed /next

## RUN 20261009-131920-build-c283 · STARTED · /build · 2026-10-09T13:19:20-05:00
Step: build:ship · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts, wordpress_connected
- CHANGE #334 [page_content] https://apexroofingtlc.com/?page_id=1614 | new draft page | old: (none) | new: draft id 1614 (pages) · from clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md sha 87ad23445186 · slug ro… | result: APPLIED · draft only (not live) · generated from the approved file | ref svc-roof-repair
- CHANGE #335 [page_content] https://apexroofingtlc.com/?page_id=1615 | new draft page | old: (none) | new: draft id 1615 (pages) · from clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md sha 77aebd7baddb · slug bluff… | result: APPLIED · draft only (not live) · generated from the approved file | ref loc-bluffton
- CHANGE #336 [publish] https://apexroofingtlc.com/?page_id=1614 | publish | old: (draft) | new: [REDACTED]/roof-repair/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-09-publish-01
- CHANGE #337 [publish] https://apexroofingtlc.com/?page_id=1615 | publish | old: (draft) | new: [REDACTED]/bluffton/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-09-publish-02
- DECISION 2026-10-09T13:21 · run 20261009-131920-build-c283 · Pilot drafts 1614/1615 carry the approved files' open [NEED: ...] markers (Roof Repair 10 lines, Bluffton 4 lines) and the SEM-1 emergency link placeholder. Publish handoff H-2026-10-09-09-publish should be held by Paul until the markers are answered (facts interview) and the approved files re-approved; Jonie must not publish text containing [NEED]. No menu change for this batch: both pages replace existing live URLs in place.
- CHANGE #338 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/H-2026-10-09-09-publish.md | upload | old: (new file) | new: H-2026-10-09-09-publish.md · sha 779d58125cb2 | result: done · copied (Drive for desktop syncs it)
- CHANGE #339 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/H-2026-10-09-09-publish.csv | upload | old: (new file) | new: H-2026-10-09-09-publish.csv · sha 8e2d6002a97d | result: done · copied (Drive for desktop syncs it)
### HANDOFF · /build · 2026-10-09 · run 20261009-131920-build-c283
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
### END HANDOFF
## RUN 20261009-131920-build-c283 · FINISHED · 2026-10-09T13:21:37-05:00
Changes: 6 · Summary: Pilot shipped as WordPress drafts 1614 (Roof Repair) and 1615 (Bluffton); publish handoff H-2026-10-09-09-publish issued; [NEED] markers still in both pages - Paul to hold
- CHANGE #340 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (5).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (5).md | result: done · renamed and moved, nothing deleted
- CHANGE #341 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (5).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 062d8bd69ecf | result: done · copied (Drive for desktop syncs it)
- CHANGE #342 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (7).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #343 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (7).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 725bbac9d583 | result: done · copied (Drive for desktop syncs it)
- CHANGE #344 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (7).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #345 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (7).md | new: Apex Roofing of the Lowcountry - Status.md · sha 094d72343383 | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-134712-build-eac1 · STARTED · /build · 2026-10-09T13:47:12-05:00
Step: build:pilot-corrections · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:briefs
- CHANGE #346 [page_content] clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | draft file (working copy) | old:  | new:  | result: APPLIED · local file only · Paul's 2026-10-09 answers: W11 flashing/underlayment, W10 photos, clean-up, services list (9 repair-type NEEDs removed, flashing H3 renamed), repair-warranty NEED removed, GAF System Plus on replacement only, 25% rule general, timing FAQ as attributed review example · approval of batch:pilot:drafts voided for this file — Paul re-approves | ref svc-roof-repair | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261009-134712-build-eac1/0346-old.md clients/apex-roofing-of-the-lowcountry/snapshots/20261009-134712-build-eac1/0346-new.md
- CHANGE #347 [page_content] clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | draft file (working copy) | old:  | new:  | result: APPLIED · local file only · permit FAQ (Apex gets the Town permit on a replacement), Old Town FAQ without UDO claims, gated-community FAQ split inside/outside Town limits (W9), Hampton Hall added as 6th neighborhood · approval of batch:pilot:drafts voided for this file — Paul re-approves | ref loc-bluffton | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261009-134712-build-eac1/0347-old.md clients/apex-roofing-of-the-lowcountry/snapshots/20261009-134712-build-eac1/0347-new.md
- CHANGE #348 [brand_guide] clients/apex-roofing-of-the-lowcountry/brand-guide.md | Section H Paul Exceptions + Section D status cells | old:  | new:  | result: APPLIED · local working copy · H: review-sourced facts exception + replacement price $20,000-$25,000 (Ken Gathercole review 2026-08-15, per Paul, not in export; replacement brief only) · D status only: W11, W9 (4 communities), W10, W25, ShingleMaster -> Paul Approved 2026-10-09 · approval hashes A+D+E+G and A+B1+B2 unchanged | snapshots clients/apex-roofing-of-the-lowcountry/snapshots/20261009-134712-build-eac1/0348-old.md clients/apex-roofing-of-the-lowcountry/snapshots/20261009-134712-build-eac1/0348-new.md
- SETTLED pilot_facts_2026_10_09 · 2026-10-09T13:53:44-05:00 · run 20261009-134712-build-eac1 · by Paul · Paul 2026-10-09 pilot answers: Apex uses corrosion-resistant flashing and synthetic underlayment on repairs (W11); Apex does leak repair; Roof Repair services = shingle repair/replacement, flashing replacement, ridge cap and starter strip, soffit/fascia/deck, leak repair (no hail - SEM-5 moved it to Emergency); photos of the work with daily progress photos (W10, reviews); daily clean-up and magnet sweep (reviews; magnet per Paul, not in export); no repair-warranty answer - GAF System Plus Limited Warranties mentioned only for a replacement (review 2026-08-15); on a replacement Apex gets the Town permit (review 2026-08-15); timing only as attributed review examples, no general visit length; 25% rule kept general (no SC source found). Review-sourced facts recorded as a Paul Exception to CM-027 in Brand Guide H.
- SETTLED send_the_client_one_question_is_your_cer · 2026-10-09T13:53:44-05:00 · run 20261009-134712-build-eac1 · by Paul · Paul 2026-10-09: CertainTeed ShingleMaster is current - yes (Paul's answer). Brand Guide D status set to Paul Approved; the D value, D2 row and content risk R4 still read not confirmed and change at the next Brand Guide revision (re-opens brand_guide_approved). Not used in the pilot drafts.
- SETTLED synthetic_roofing · 2026-10-09T13:53:44-05:00 · run 20261009-134712-build-eac1 · by Paul · Paul 2026-10-09: synthetic roofing is offered - yes. Neither pilot page's services list needs it (Roof Repair list per Paul has no synthetic; Bluffton lists the 8 services). Port Royal base-housing work remains open under synthetic_roofing_offered.
- SETTLED bluffton_communities · 2026-10-09T13:53:44-05:00 · run 20261009-134712-build-eac1 · by Paul · Paul 2026-10-09: Apex works in Palmetto Bluff, Belfair, Colleton River Plantation and Moss Creek (W9). Per the Town of Bluffton Neighborhoods PDF, Palmetto Bluff and Hampton Hall are inside the Town limits; Belfair, Colleton River Plantation and Moss Creek are Greater Bluffton (unincorporated Beaufort County). Bluffton page names those three only as also served, outside the Town limits. Hampton Hall is the 6th Bluffton neighborhood (Town PDF; also named in a 2026-05-17 review).
- SETTLED old_town_udo · 2026-10-09T13:53:44-05:00 · run 20261009-134712-build-eac1 · by Paul · Paul 2026-10-09: no Old Town historic review or UDO roof-material claims (UDO 3.18 and Article 5 NEEDs dropped) unless evidence is found; none found in this run. The Old Town FAQ now only tells the homeowner to ask the Town before choosing a material.
- SETTLED replacement_price_review · 2026-10-09T13:53:44-05:00 · run 20261009-134712-build-eac1 · by Paul · Paul 2026-10-09: $20,000-$25,000 for a roof replacement, source Google review, Ken Gathercole, 2026-08-15 (per Paul; the figure is not in the reviews export). For the Roof Replacement brief only, cited to that single review, never as Apex's general price. Recorded in Brand Guide H; not in either pilot draft.
### HANDOFF · /build · 2026-10-09 · run 20261009-134712-build-eac1
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
### END HANDOFF
## RUN 20261009-134712-build-eac1 · FINISHED · 2026-10-09T13:54:39-05:00
Changes: 3 · Summary: Pilot drafts SD Roof Repair and LD Bluffton revised from Paul's 2026-10-09 answers (all NEEDs closed); Brand Guide H exceptions + replacement price recorded; drafts await re-approval, not pushed
- CHANGE #349 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (6).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (6).md | result: done · renamed and moved, nothing deleted
- CHANGE #350 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (6).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha ce59681bb4ff | result: done · copied (Drive for desktop syncs it)
- CHANGE #351 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (8).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (8).md | result: done · renamed and moved, nothing deleted
- CHANGE #352 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (8).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 2de4eba95c69 | result: done · copied (Drive for desktop syncs it)
- CHANGE #353 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Brand Guide.md | new: _Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #354 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Brand Guide.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Brand Guide - 2026-10-08 (4).md | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha d0d13ef3bbe8 | result: done · copied (Drive for desktop syncs it)
- CHANGE #355 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (8).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (8).md | result: done · renamed and moved, nothing deleted
- CHANGE #356 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (8).md | new: Apex Roofing of the Lowcountry - Status.md · sha 4a0d603ba576 | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-135629-build-8db7 · STARTED · /build · 2026-10-09T13:56:29-05:00
Step: build:drafts · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts_ready
- DECISION 2026-10-09T13:58 · run 20261009-135629-build-8db7 · Pilot batch review of the revised drafts (after run 20261009-134712-build-eac1): sibling check clean (no FAQ/heading collision, opening and CTA forms differ, on-call sentence on SD only, no revision content repeated across pages). Bluffton Town-limits vs Greater Bluffton correct; no price claim; $20,000-$25,000 on neither page; Roof Repair services list matches Paul's (no hail); warranty only in the replacement FAQ. New semantic review table replaces the old one: 4 SEM items (SEM-1 Old Town 1996 listing x3 on LD; SEM-2 flashing-vs-sealant point twice on SD; SEM-3 flashing quote attributed to Ralph and Pierce, Brand Guide G names no speaker; SEM-4 LD says Apex replaces roofs in Palmetto Bluff, W9 says works in). Report only; drafts unchanged. Registered: status.py batch pilot --state drafts_written --sem-findings 4.
### HANDOFF · /build · 2026-10-09 · run 20261009-135629-build-8db7
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
### END HANDOFF
## RUN 20261009-135629-build-8db7 · FINISHED · 2026-10-09T13:58:30-05:00
Changes: 0 · Summary: Pilot batch review of revised drafts: sibling check clean, 4 new SEM items, table re-registered
- CHANGE #357 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (7).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (7).md | result: done · renamed and moved, nothing deleted
- CHANGE #358 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (7).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha d68ffa2b5266 | result: done · copied (Drive for desktop syncs it)
- CHANGE #359 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (9).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (9).md | result: done · renamed and moved, nothing deleted
- CHANGE #360 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (9).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 5dfccd91700a | result: done · copied (Drive for desktop syncs it)
- CHANGE #361 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (9).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (9).md | result: done · renamed and moved, nothing deleted
- CHANGE #362 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (9).md | new: Apex Roofing of the Lowcountry - Status.md · sha 8210a2a1788a | result: done · copied (Drive for desktop syncs it)

## APPROVAL · 2026-10-09T14:02:41-05:00 · batch pilot drafts · approved · by Paul
Approved version: clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md (sha 0e51afca8497)
Approved version: clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md (sha 928b039f6737)
Approved version: clients/apex-roofing-of-the-lowcountry/build/Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW.md (sha 06239c18bb0f)
SEM items to apply: SEM-1, SEM-2, SEM-3
- CHANGE #363 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED - 2026-10-09.md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/02 - Build/Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED.md | new: _Archive/Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #364 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED - 2026-10-09.md | new: Apex Roofing of the Lowcountry - Semantic Review - pilot - APPROVED.md · sha 9314bbc9ee8c | result: done · copied (Drive for desktop syncs it) | snapshots  clients/apex-roofing-of-the-lowcountry/snapshots/approval-2026-10-09/0364-new.tmp
- CHANGE #365 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (10).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (10).md | result: done · renamed and moved, nothing deleted
- CHANGE #366 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (10).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 7c4772c5c3a2 | result: done · copied (Drive for desktop syncs it)
- CHANGE #367 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (10).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (10).md | result: done · renamed and moved, nothing deleted
- CHANGE #368 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (10).md | new: Apex Roofing of the Lowcountry - Status.md · sha 5cae8016612c | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-140247-build-805e · STARTED · /build · 2026-10-09T14:02:47-05:00
Step: build:apply-sem · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts
- CHANGE #369 [page_content] clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md | FAQ: What roofing materials are allowed in Old Town Bluffton? (SEM-1) | old: Ask the Town of Bluffton before you pick a roof material for a home in Old Town, a National Historic District since 1996. | new: Ask the Town of Bluffton before you pick a roof material for a home in Old Town. | result: applied | ref SEM-1
- CHANGE #370 [page_content] clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | H3 Flashing Replacement at Chimneys, Walls and Valleys (SEM-2) | old: Loose or corroded flashing is removed and replaced, not covered over with caulk. | new: Loose or corroded flashing is removed and replaced. | result: applied | ref SEM-2
- CHANGE #371 [page_content] clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md | Delivery H2 flashing paragraph quote attribution (SEM-3) | old: In the words of Ralph and Pierce, a lot of water damage can be stopped | new: In the words of the owners, a lot of water damage can be stopped | result: applied | ref SEM-3
- DECISION 2026-10-09T14:03 · run 20261009-140247-build-805e · Pilot apply-sem: applied only SEM-1, SEM-2, SEM-3 as picked by Paul. SEM-4 (Bluffton FAQ 'Apex replaces roofs in Palmetto Bluff') reviewed and kept as written: Paul confirmed Apex offers all services, including roof replacement, in Palmetto Bluff, Belfair, Colleton River Plantation and Moss Creek.
- SEM APPLIED 2026-10-09T14:03 · batch pilot · SEM-1, SEM-2, SEM-3 · E-checks passed · approval pinned to the applied versions
### HANDOFF · /build · 2026-10-09 · run 20261009-140247-build-805e
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
### END HANDOFF
## RUN 20261009-140247-build-805e · FINISHED · 2026-10-09T14:04:14-05:00
Changes: 3 · Summary: Pilot SEM-1,2,3 applied to SD Roof Repair and LD Bluffton; SEM-4 kept; E1-E10 pass
- CHANGE #372 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (8).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (8).md | result: done · renamed and moved, nothing deleted
- CHANGE #373 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (8).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 887bab92e6e0 | result: done · copied (Drive for desktop syncs it)
- CHANGE #374 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (11).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (11).md | result: done · renamed and moved, nothing deleted
- CHANGE #375 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (11).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 2ee52d621684 | result: done · copied (Drive for desktop syncs it)
- CHANGE #376 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (11).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (11).md | result: done · renamed and moved, nothing deleted
- CHANGE #377 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (11).md | new: Apex Roofing of the Lowcountry - Status.md · sha 1488bb3bf31a | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-09T14:05 · after build:apply-sem (run 20261009-140247-build-805e) · Paul typed /next

## RUN 20261009-140647-build-c103 · STARTED · /build · 2026-10-09T14:06:47-05:00
Step: build:ship · batch pilot · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:drafts, wordpress_connected
- CHANGE #378 [wp_check] https://apexroofingtlc.com/?page_id=1616 | test draft page | old: (none) | new: draft id 1616 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #379 [wp_check] https://apexroofingtlc.com/?p=1617 | test draft post | old: (none) | new: draft id 1617 | result: APPLIED · test draft (trashed at the end of the check)
- CHANGE #380 [page_content] https://apexroofingtlc.com/?page_id=1620 | new draft page | old: (none) | new: draft id 1620 (pages) · from clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md sha fc7c7933af8f · slug ro… | result: APPLIED · draft only (not live) · generated from the approved file | ref svc-roof-repair
- CHANGE #381 [page_content] https://apexroofingtlc.com/?page_id=1621 | new draft page | old: (none) | new: draft id 1621 (pages) · from clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md sha 29f915db08aa · slug bluff… | result: APPLIED · draft only (not live) · generated from the approved file | ref loc-bluffton
- CHANGE #382 [publish] https://apexroofingtlc.com/?page_id=1620 | publish | old: (draft) | new: [REDACTED]/roof-repair/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-10-publish-01
- CHANGE #383 [publish] https://apexroofingtlc.com/?page_id=1621 | publish | old: (draft) | new: [REDACTED]/bluffton/ | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-10-publish-02
- CHANGE #384 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/H-2026-10-09-10-publish.md | upload | old: (new file) | new: H-2026-10-09-10-publish.md · sha c0dca769af7e | result: done · copied (Drive for desktop syncs it)
- CHANGE #385 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/02 - Build/H-2026-10-09-10-publish.csv | upload | old: (new file) | new: H-2026-10-09-10-publish.csv · sha 2bf13a70fba6 | result: done · copied (Drive for desktop syncs it)
### HANDOFF · /build · 2026-10-09 · run 20261009-140647-build-c103
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
### END HANDOFF
## RUN 20261009-140647-build-c103 · FINISHED · 2026-10-09T14:12:02-05:00
Changes: 8 · Summary: Pilot: new WP drafts 1620/1621 from SEM-applied files; publish handoff H-2026-10-09-10-publish; 1614/1615 and H-...-09 superseded
- CHANGE #386 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (9).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (9).md | result: done · renamed and moved, nothing deleted
- CHANGE #387 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (9).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 57883e427870 | result: done · copied (Drive for desktop syncs it)
- CHANGE #388 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (12).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (12).md | result: done · renamed and moved, nothing deleted
- CHANGE #389 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (12).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 6da8b4204b51 | result: done · copied (Drive for desktop syncs it)
- CHANGE #390 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (12).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (12).md | result: done · renamed and moved, nothing deleted
- CHANGE #391 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (12).md | new: Apex Roofing of the Lowcountry - Status.md · sha 0679f1ebf078 | result: done · copied (Drive for desktop syncs it)

## RUN 20261009-142045-build-a198 · STARTED · /build · 2026-10-09T14:20:45-05:00
Step: build:pilot-corrections · session 0ed9494a-d39c-458b-a350-b0f27797f264
Gates checked: discovery_signed_off, batch:pilot:briefs
- DECISION 2026-10-09T14:22 · run 20261009-142045-build-a198 · Pilot corrections (Paul, 2026-10-09), client-level, carried into every later Apex brief: (1) the flashing credit reads 'the owners' - Ralph and Pierce Brehany, no job titles published; (2) Roof Repair services list = shingle repair and replacement, flashing replacement, ridge cap and starter strip repair, soffit/fascia/deck repair, leak repair - no hail (moved to Emergency Roof Repair, SEM-5); (3) $20,000-$25,000 is a Roof Replacement brief fact only, cited to Ken Gathercole's Google review 2026-08-15, never a general price; (4) warranty mentioned only in a replacement context; (5) Bluffton cut down for depth - nobody needs the depth. Already settled (pilot_facts_2026_10_09, replacement_price_review, w25_who_goes_on_the_roof); not re-asked.
- DECISION 2026-10-09T14:22 · run 20261009-142045-build-a198 · Spec section 8 lines NOT written: the edit to methodology/specs/service.md and location.md was refused by the permission system in this run, so no spec file changed. Proposed lines for Paul: service.md #7/SVC-19 - sub-services are exactly those the client confirmed for that service, others move to the page that owns them; warranty and price claims only on the service they apply to (single-review price only on that service's brief, cited). location.md #5/#8/LOC-22/LOC-23 - each section carries what its element requires and stops; no detail lists, generic regional sentences or FAQ answers repeating the opening; 1,000 words is a ceiling, not a target; no element dropped. Paul adds them (or allows the edit) in a later session; the s1 briefs apply both from this decision.
- DECISION 2026-10-09T14:22 · run 20261009-142045-build-a198 · Project note (Paul's rule, 2026-10-09): every Apex page stays a WordPress draft until every page is drafted; then all are published together. A system change (ship/publish handoff timing) for a later Opus design session - not made now. Until then, Paul holds each batch's publish handoff (pilot handoff H-2026-10-09-09-publish already held).
### HANDOFF · /build · 2026-10-09 · run 20261009-142045-build-a198
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
### END HANDOFF
## RUN 20261009-142045-build-a198 · FINISHED · 2026-10-09T14:22:56-05:00
Changes: 0 · Summary: Pilot corrections recorded (client decisions); spec section 8 lines proposed, edit refused by permissions; publish-together rule noted for a design session
- CHANGE #392 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (10).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (10).md | result: done · renamed and moved, nothing deleted
- CHANGE #393 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (10).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha ac867633c4cc | result: done · copied (Drive for desktop syncs it)
- CHANGE #394 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (13).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (13).md | result: done · renamed and moved, nothing deleted
- CHANGE #395 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (13).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha aff1476cbc8b | result: done · copied (Drive for desktop syncs it)
- CHANGE #396 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (13).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (13).md | result: done · renamed and moved, nothing deleted
- CHANGE #397 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (13).md | new: Apex Roofing of the Lowcountry - Status.md · sha f98300e8df18 | result: done · copied (Drive for desktop syncs it)
- REVIEW CONTINUED 2026-10-09T14:25 · after build:ship (run 20261009-140647-build-c103) · Paul typed /next

## RUN 20261009-142804-build-8390 · STARTED · /build · 2026-10-09T14:28:04-05:00
Step: build:evidence · batch s1 · session a5aedfda-3fe8-4bd3-96f3-e6a505a76bac
Gates checked: discovery_signed_off, batch:s1:briefs_ready, page_specs_approved
- EVIDENCE 2026-10-09T14:30 · run 20261009-142804-build-8390 · svc-roof-replacement: BLOCK (known 2, unknown 1, unverified 9, conflict 0)
- EVIDENCE 2026-10-09T14:30 · run 20261009-142804-build-8390 · svc-roof-installation: BLOCK (known 2, unknown 2, unverified 9, conflict 0)
- EVIDENCE 2026-10-09T14:30 · run 20261009-142804-build-8390 · svc-roof-inspections: BLOCK (known 1, unknown 1, unverified 10, conflict 0)
- EVIDENCE 2026-10-09T14:30 · run 20261009-142804-build-8390 · svc-emergency-roof-repair: BLOCK (known 2, unknown 1, unverified 10, conflict 0)
- DECISION 2026-10-09T14:30 · run 20261009-142804-build-8390 · Evidence gate s1 (CM-041): all 4 service pages BLOCK. Main cause: Brand Guide A/D status cells carry dates and notes (e.g. 'Paul Approved 2026-10-06 · was: Submitted'), which evidence.py reads only as an exact status word, so phone, free estimate, warranty, licence, insurance, certifications, rating, emergency and services-subcontracted are marked Unverified. If those cells parsed, all 4 would be WARN; the real required gap left is service scope (live site only, Submitted) on Replacement, Inspections and Emergency. Brand Guide statuses not changed. Fix belongs to a design session (parser or status format); until then each page needs the facts interview or Paul's waiver.
### HANDOFF · /build · 2026-10-09 · run 20261009-142804-build-8390
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
### END HANDOFF
## RUN 20261009-142804-build-8390 · FINISHED · 2026-10-09T14:30:43-05:00
Changes: 0 · Summary: Evidence gate s1: all 4 service pages BLOCK (mainly dated Brand Guide status cells read as Unverified; real gaps = live-site-only scope on 3 pages, timeframes, inspection pricing). Facts files + grids written; no briefs.
- CHANGE #398 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (11).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (11).md | result: done · renamed and moved, nothing deleted
- CHANGE #399 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (11).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha c796ffaa0799 | result: done · copied (Drive for desktop syncs it)
- CHANGE #400 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (14).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (14).md | result: done · renamed and moved, nothing deleted
- CHANGE #401 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (14).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha 520dc02a2d7d | result: done · copied (Drive for desktop syncs it)
- CHANGE #402 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (14).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (14).md | result: done · renamed and moved, nothing deleted
- CHANGE #403 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (14).md | new: Apex Roofing of the Lowcountry - Status.md · sha b2c8371329de | result: done · copied (Drive for desktop syncs it)
- SETTLED residential_roofer_a3_write · 2026-10-09T18:08:47-05:00 · run migration-rewrite2 · by Paul (site plan choice 4a, 2026-10-08) · Residential Roofer written into Brand Guide A3 (Paul approved it 2026-10-08, site plan choice 4a); entity and Brand Guide approvals re-stamped by the rewrite 2 migration

## MIGRATION · 2026-10-09T18:08:47-05:00 · rewrite 2 P4: facts.json
44 facts from Brand Guide A and D · 3 approval stamp(s) re-stamped on the value-only hash · 0 lost
Folded in: d-certifications-authorizations-factory-training: settled send_the_client_one_question_is_your_cer (ShingleMaster current — yes)
Folded in: a-category-variants-4-6: settled site_plan_open_choices 4a (closes residential_roofer_a3_write)
Folded in: d-who-does-the-work: new row (Paul 2026-10-09 (settled w25_who_goes_on_the_roof; W25))
Folded in: d-job-photos: new row (Paul 2026-10-09 (settled pilot_facts_2026_10_09; W10, reviews))
Folded in: d-repair-materials: new row (Paul 2026-10-09 (settled pilot_facts_2026_10_09; W11))
Folded in: d-clean-up: new row (Paul 2026-10-09 (settled pilot_facts_2026_10_09; reviews; magnet per Paul))
Folded in: d-permits: new row (Paul 2026-10-09 (settled pilot_facts_2026_10_09; review 2026-08-15))
Folded in: d-synthetic-roofing-offered: new row (Paul 2026-10-09 (settled synthetic_roofing))
Folded in: loc-bluffton page facts: neighborhoods (settled bluffton_communities)
Folded in: SD - Roof Repair - Apex Roofing of the Lowcountry.md line 76: inline link placeholder in the one P11 form (no wording change)

## MIGRATION · 2026-10-09T18:09:42-05:00 · rewrite 2 P4 repair: 1 repeated fact row(s) removed from the Brand Guide · approvals counting again: gate brand_guide_approved: brand-guide.md#A+D+E+G · no stamp changed

## MIGRATION · 2026-10-09T20:15:29-05:00 · rewrite 2 P7 + P10: URLs and batches
Paul 2026-10-09 (REWRITE-2-DECISIONS.md c): /metal-roofing-2/ → /metal-roofing/ with a 301
svc-metal-roofing: https://apexroofingtlc.com/metal-roofing-2/ → https://apexroofingtlc.com/metal-roofing/ (301 paired with the publish)
batches: l1, l2, l3, s1, s2 → services, locations
The site plan file changed: Paul re-approves it once.

## RUN 20261009-201529-drive-mirror-043d · STARTED · /drive-mirror · 2026-10-09T20:15:29-05:00
Step: drive-mirror · session 55ffb3c8-069b-4af6-a4b4-8790ec003647
Gates checked: client_setup
Note: rewrite 2 URL migration: worklist rows
- CHANGE #404 [other] https://apexroofingtlc.com/metal-roofing/ | clear the slug | old: whatever holds /metal-roofing/ now | new: nothing | result: HANDOFF ISSUED to Jonie | ref H-2026-10-09-11-other-01
### HANDOFF · /drive-mirror · 2026-10-09 · run 20261009-201529-drive-mirror-043d
**What I did**
- rewrite 2 URL migration: worklist rows for the redirect / slug clearing
### END HANDOFF
## RUN 20261009-201529-drive-mirror-043d · FINISHED · 2026-10-09T20:15:29-05:00
Changes: 1 · Summary: rewrite 2 URL migration (worklist rows)
- CHANGE #405 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (12).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | new: _Archive/Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (12).md | result: done · renamed and moved, nothing deleted
- CHANGE #406 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Handoff Log.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Handoff Log - 2026-10-09 (12).md | new: Apex Roofing of the Lowcountry - Handoff Log.md · sha 0459a79f60d8 | result: done · copied (Drive for desktop syncs it)
- CHANGE #407 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (4).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Approval Record.md | new: _Archive/Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (4).md | result: done · renamed and moved, nothing deleted
- CHANGE #408 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Approval Record.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Approval Record - 2026-10-08 (4).md | new: Apex Roofing of the Lowcountry - Approval Record.md · sha c2b71d4375ec | result: done · copied (Drive for desktop syncs it)
- CHANGE #409 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (15).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | new: _Archive/Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (15).md | result: done · renamed and moved, nothing deleted
- CHANGE #410 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Document Checklist.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Document Checklist - 2026-10-09 (15).md | new: Apex Roofing of the Lowcountry - Document Checklist.md · sha c948e1f89605 | result: done · copied (Drive for desktop syncs it)
- CHANGE #411 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-09.md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Brand Guide.md | new: _Archive/Apex Roofing of the Lowcountry - Brand Guide - 2026-10-09.md | result: done · renamed and moved, nothing deleted
- CHANGE #412 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Brand Guide.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Brand Guide - 2026-10-09.md | new: Apex Roofing of the Lowcountry - Brand Guide.md · sha 08af020cd13f | result: done · copied (Drive for desktop syncs it)
- CHANGE #413 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/_Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (15).md | archive | old: drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | new: _Archive/Apex Roofing of the Lowcountry - Status - 2026-10-09 (15).md | result: done · renamed and moved, nothing deleted
- CHANGE #414 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - Status.md | upload | old: previous version archived as Apex Roofing of the Lowcountry - Status - 2026-10-09 (15).md | new: Apex Roofing of the Lowcountry - Status.md · sha ad7e05076198 | result: done · copied (Drive for desktop syncs it)
- CHANGE #415 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - VA Worklist.md | upload | old: (new file) | new: Apex Roofing of the Lowcountry - VA Worklist.md · sha 0d765c9f120d | result: done · copied (Drive for desktop syncs it)
- CHANGE #416 [drive_file] drive:Apex Roofing of the Lowcountry - TMS/Apex Roofing of the Lowcountry - VA Worklist.csv | upload | old: (new file) | new: Apex Roofing of the Lowcountry - VA Worklist.csv · sha 4a686175d061 | result: done · copied (Drive for desktop syncs it)
