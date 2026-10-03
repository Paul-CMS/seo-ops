# Gettysburg Mold Remediation Pros - Handoff Log

Generated from the safety log (clients/gettysburg-mold-remediation-pros/log.md) — do not edit. Each run adds its section with `run.py finish --handoff <file>`. The newest section is at the bottom.

## /new-client · 2026-10-03 · run 20261003-153557-new-client-6698

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

## /wp-check · 2026-10-03 · run 20261003-153748-wp-check-16f1

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

## /discovery · 2026-10-03 · run 20261003-160508-discovery-552a

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

