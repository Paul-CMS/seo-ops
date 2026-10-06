# Apex Roofing of the Lowcountry — run notes

Rules for this run (Paul, 2026-10-05):
- Every "note:" from Paul goes here with the date and the current step.
- Mid-run, only true blockers get fixed. Everything else is collected here for the next pause.
- At each decision: plain-language explanation of what is being approved and what changes once it is.
- Safe fixes capped at **5 alt texts and 2 broken links** until Paul has checked them live
  (set with `status.py cap`, enforced by wp.py).
- VA handoff to Jonie for the WordPress `seo-ops` Editor user + Application Password; Paul adds the
  `.env` lines himself.

## Paul's notes

| Date | Step | Note |
|---|---|---|
| 2026-10-05 | entity decision | Paul: SEOPress version on apexroofingtlc.com is 10.0.1 (meets the 6.8+ requirement). WordPress username given as PaulMeisner rather than a dedicated `seo-ops` user; password given in chat (not recorded here). Area entity → Lowcountry / SC Lowcountry; Roof Mechanic out; no Coastal Georgia currently. |

## Collected for the next pause

| Date | Step | Item | Blocker? |
|---|---|---|---|
| 2026-10-05 | new-client | Paul thought Apex might have been started on Oct 3. Nothing for Apex exists in the repo (main, `review-fixes`, stashes) or in the v3 Drive root — Oct 3 was Gettysburg Mold Remediation Pros. Set up fresh. | No |
| 2026-10-05 | new-client | Older Apex folders exist elsewhere in Drive, outside v3: "Apex Roofing" (owner witkowskiblair@gmail.com, with "Apex Roofing Client Images"), "Apex Commerical Pages" (Paul, Apr 2026) and "Apex Roofing of the Lowcountry" (owner mark.a.ko.08@gmail.com, May 2026). Not read, not touched. Paul decides whether any of them is source material for discovery (e.g. client images, earlier page copy). | No |
| 2026-10-05 | new-client | The GBP Website field is `http://www.apexroofingtlc.com/`; the site was given as `https://apexroofingtlc.com/`. Recorded as given — discovery checks what each resolves to (no judgement before the audit). | No |
| 2026-10-05 | new-client | The WordPress handoff (`kind other`) is gated on `client_setup`, which is only met when `/new-client` finishes — so the Editor-user request to Jonie can't go out inside the setup run itself, even though the command's step 6 asks for it there. Issued in its own run straight after. | No |
| 2026-10-05 | new-client | `kind other` defaults to Gwen; WordPress setup belongs to Jonie, so the handoff needs `--to Jonie --owner-reason`. A dedicated `wp_setup` kind (owner Jonie) would avoid the override every time. | No |
| 2026-10-05 | new-client | Same as Gettysburg: the guard blocks any shell command that names a record file (handoff-log.md, log.md, status.json) even for read-only `cp`/`ls`/`cat` chains. Cost two retries this run. A leading `cd ~/Documents/seo-ops &&` also counts as a chain, so even a single `drive.py replaced` call was refused until the `cd` was dropped. | No |
| 2026-10-05 | drive-mirror | A plain `curl` of the public homepage was blocked as a "WordPress API call" because the same command also probed `/wp-json/`. Dropping that probe worked. Fine as is (the probe belongs in wp.py), noting it only because the message reads as if any curl to a WP site is blocked. | No |
| 2026-10-05 | discovery | The guard blocks any command whose *text* contains the record-file name — including a `steps.py record --reason "...status.json..."` call and a python heredoc that only edited brand-guide.md but mentioned "status.json" in a string. Two retries; rewording worked. | No |
| 2026-10-05 | discovery | Both government sources in the discovery hierarchy are CAPTCHA-gated (SC SOS Business Entities Online; SC LLR licence lookup). The system cannot read them, so legal entity, formation date and licence class/status stay `found` (OpenCorporates / BBB copies). A standing manual step (Gwen or Paul reads them and saves a MANUAL evidence file) would close this every time. | No |
| 2026-10-05 | discovery | The public Google Maps view is limited: GBP secondary categories, service-area list and open date are not visible, so BB-107 (broadest category primary) can't be checked in discovery without GBP dashboard access. | No |
| 2026-10-05 | discovery | Brand Guide Section F has one "Wikidata URI — county" row; Apex's MSA is two counties (Beaufort + Jasper). Both written into the one row for now. | No |
| 2026-10-05 | discovery | `drive.py` has no upload command, so first-time uploads go through the Drive connector by pasting the whole file as text (the 33 KB evidence file came through 1 byte short — trailing newline). An `upload` subcommand would make it exact and cheaper. | No |
| 2026-10-05 | entity decision | The `entity_approved` line covers the whole `brand-guide.md`. Every later Brand Guide write (proof-sheet reconcile, Build write-back to B3/C/D) changes that file, so the entity approval would "stop counting" each time even though Section A didn't change. Worth checking how Gettysburg behaved; a per-section hash (Section A + B only) would fit better. | Not yet — it becomes one at reconcile |
| 2026-10-05 | entity decision | Paul typed `/approve` at the end of a message that also changed the proposal. It wasn't run as an approval command, and approving would have locked in the rejected metro area anyway. The changes were applied in a revision run instead and Paul re-types `/approve` on the revised files. Worth a line in CLAUDE.md §3: an approval with changes = revise first, then approve. | No |
| 2026-10-05 | entity decision | WordPress credentials arrived in chat instead of `.env`, and for a personal account (PaulMeisner) rather than a dedicated `seo-ops` Editor. The password looks like a login password, not an Application Password (24 characters in groups of four), which the REST connection needs. Not written anywhere by the system. | Yes for /wp-check — not for discovery |
| 2026-10-05 | entity decision | The Drive copy of the Discovery Record (REVIEW) is the version from before Paul's changes. Per /approve step 5 the approved version goes up as a new `- APPROVED.md` file after the approval, so it wasn't re-uploaded now. | No |
