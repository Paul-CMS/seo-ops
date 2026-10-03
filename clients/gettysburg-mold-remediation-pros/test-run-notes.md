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
| 2026-10-03 | new-client | `status.py classify "mold remediation"` → not sensitive. Mold pages tend to make health claims (respiratory effects, allergies), so CM-025 may need a "health-adjacent" hint so that `/new-client` asks instead of answering no. | No |
| 2026-10-03 | new-client | `/new-client` step 4 talks about copying the template, but the Drive connector can't copy folders. Claude built the same folder tree by hand (01/Evidence, 01/Deliverables, 02, 03, 04, _Archive). If the template ever gets extra files or subfolders, this will drift from it. Proposal: list the template tree in config.json and check against it. | No |
| 2026-10-03 | new-client | The 5 alt-text / 2 broken-link cap exists only in this file. Nothing in gates.json/wp.py enforces it. Proposal: a per-client `safe_fix_cap` in status.json that wp.py checks. | No, Claude enforces it by hand for now |

## Fix-round log

| Date | Pause | Items fixed | tests/run_all.py |
|---|---|---|---|
| 2026-10-03 | baseline before the run | — | 130 passed, 0 failed |
