# Gettysburg Mold Remediation Pros — first real client run: notes

Rules for this run (Paul, 2026-10-03):
- Every "note:" from Paul goes here with the date and the current step.
- Mid-run, only true blockers get fixed. Everything else waits here for the fix round at the
  next pause (after audit approval, after the pilot, after the first batch). `tests/run_all.py`
  runs after every fix round.
- Safe fixes capped at **5 alt texts and 2 broken links** until Paul has checked them live.

## Paul's notes

| Date | Step | Note |
|---|---|---|

## Collected for the next fix round

| Date | Step | Item | Blocker? |
|---|---|---|---|
| 2026-10-03 | new-client | The session opened in `~/CMS` (empty), so `/new-client` and `/wp-check` weren't available until it moved to `~/Documents/seo-ops`. Start client sessions in seo-ops (or make `~/CMS` point at it). | No, worked around by moving the session |
| 2026-10-03 | new-client | `status.py classify "mold remediation"` → not sensitive. Mold pages tend to make health claims (respiratory effects, allergies), so CM-025 may need a "health-adjacent" hint so that `/new-client` asks instead of answering no. | **Fixed 2026-10-03 (Paul C):** health-adjacent category + CM-040; unclear industries ask Paul |
| 2026-10-03 | new-client | `/new-client` step 4 talks about copying the template, but the Drive connector can't copy folders. Claude built the same folder tree by hand (01/Evidence, 01/Deliverables, 02, 03, 04, _Archive). If the template ever gets extra files or subfolders, this will drift from it. Proposal: list the template tree in config.json and check against it. | No |
| 2026-10-03 | new-client | `run.py finish` committed but **the push failed**: the repo is on branch `review-fixes`, which has no upstream. The commits are only local. Paul decides whether to push the branch or switch back to main. | **Fixed 2026-10-03 (Paul A):** merged into main and pushed; work continues on main |
| 2026-10-03 | new-client | The generated Handoff Log has two headings per run: `## /new-client · …` from records.py, then the handoff file's own `## Setup · …`. Either the template drops its heading or records.py stops adding one. | No — Paul E: fix at the next pause |
| 2026-10-03 | new-client | The records are mirrored to Drive *after* `finish`, so that Drive write is never logged as a `drive_file` change, even though CLAUDE.md §2 says Drive writes are changes. | **Fixed 2026-10-03 (Paul B):** a logged `drive-mirror` run after finish |
| 2026-10-03 | wp-check | **The Drive connector can't overwrite a file's content.** It can only create, rename or move. "Re-upload after each run" would leave duplicates, and Drive files may not be deleted. The Drive Handoff Log/Checklist are stuck at their /new-client version. Options: Paul re-uploads by hand, a script uses the Drive API directly, or old copies move to `_Archive` on each upload. | **Fixed 2026-10-03 (Paul B):** archive-and-replace — dated name → `_Archive`, upload, both logged (`scripts/drive.py`) |
| 2026-10-03 | new-client | The Brand Guide hasn't been mirrored to Drive yet because it's still blank. Mirror it after discovery fills Section A. | No |
| 2026-10-03 | new-client | The 5 alt-text / 2 broken-link cap exists only in this file. Nothing in gates.json/wp.py enforces it. Proposal: a per-client `safe_fix_cap` in status.json that wp.py checks. | **Fixed 2026-10-03 (Paul D):** `status.py cap`, enforced by wp.py |

## Fix-round log

| Date | Pause | Items fixed | tests/run_all.py |
|---|---|---|---|
| 2026-10-03 | baseline before the run | — | 130 passed, 0 failed |
| 2026-10-03 | before discovery (Paul's decisions A–D) | branch merged to main; Drive archive-and-replace + logged mirror; health-adjacent category + ask-when-unclear (CM-040); per-client safe-fix cap | 151 passed, 0 failed |
