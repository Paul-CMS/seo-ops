# Red Rover Roofing — test-run notes

Kept for this test run. Paul's notes (anything he writes as "note:") are added verbatim under
**Paul's notes**. System issues found along the way are under **System observations** — they are
proposals only; nothing here changes a rule (rule changes go through methodology/lessons.md).

## Paul's notes

_(none yet)_

## System observations

- 2026-10-07 · Import: the importer has page states for live / draft / brief / planned, but no state
  for "approved and written back, not yet live" (all 15 Red Rover service pages). Marking them
  "approved" would label them "Imported — already live" in the site plan.
- 2026-10-07 · Import: the pilot is fixed as 1 service + 1 location page. A mid-build import with
  services finished has no way to run a location-only pilot; `pilot_done: true` waives the pilot,
  `false` leaves no pilot batch at all.
- 2026-10-07 · Commits: `git_commit` stages with `git add -A`, so a run for one client also commits
  another client's uncommitted files (Apex Roofing had 3 modified files when this run started).
- 2026-10-07 · Specs: every file in methodology/specs/ is DRAFT. CLAUDE.md §5 says a DRAFT spec
  stops building that page type; the spec headers say DRAFT is "advisory". No script checks it
  either way. CLAUDE.md governs, so location/county-hub building waits on Paul approving those specs.
- 2026-10-07 · Reading safety: the guard blocks `tail`/`grep` on log.md even for reading — fine, but
  `status.py show` is then the only way to see whether another client has an open run.
