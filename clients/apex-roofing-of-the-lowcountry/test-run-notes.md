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

## Collected for the next pause

| Date | Step | Item | Blocker? |
|---|---|---|---|
| 2026-10-05 | new-client | Paul thought Apex might have been started on Oct 3. Nothing for Apex exists in the repo (main, `review-fixes`, stashes) or in the v3 Drive root — Oct 3 was Gettysburg Mold Remediation Pros. Set up fresh. | No |
| 2026-10-05 | new-client | Older Apex folders exist elsewhere in Drive, outside v3: "Apex Roofing" (owner witkowskiblair@gmail.com, with "Apex Roofing Client Images"), "Apex Commerical Pages" (Paul, Apr 2026) and "Apex Roofing of the Lowcountry" (owner mark.a.ko.08@gmail.com, May 2026). Not read, not touched. Paul decides whether any of them is source material for discovery (e.g. client images, earlier page copy). | No |
| 2026-10-05 | new-client | The GBP Website field is `http://www.apexroofingtlc.com/`; the site was given as `https://apexroofingtlc.com/`. Recorded as given — discovery checks what each resolves to (no judgement before the audit). | No |
| 2026-10-05 | new-client | The WordPress handoff (`kind other`) is gated on `client_setup`, which is only met when `/new-client` finishes — so the Editor-user request to Jonie can't go out inside the setup run itself, even though the command's step 6 asks for it there. Issued in its own run straight after. | No |
| 2026-10-05 | new-client | `kind other` defaults to Gwen; WordPress setup belongs to Jonie, so the handoff needs `--to Jonie --owner-reason`. A dedicated `wp_setup` kind (owner Jonie) would avoid the override every time. | No |
| 2026-10-05 | new-client | Same as Gettysburg: the guard blocks any shell command that names a record file (handoff-log.md, log.md, status.json) even for read-only `cp`/`ls`/`cat` chains. Cost two retries this run. | No |
