# Review — the fresh-context self-check (S17, CM-026, CM-063)

Claude writes and reviews the audit under the standing exception **CM-026**; the mitigation is this review, run by the
`audit-reviewer` subagent in a fresh context. `decisions.md` cites CM-026; it logs no new exception.

## What it loads — the registers only

`findings.csv`, `url-decision-map.csv`, `redirect-screen.csv`, `conformance-triage.csv`, `00-manifest.csv`,
`00-crosschecks.md`, `decisions.md`, `conflicts.csv`, the Brand Guide and the rulings it needs by ID. **Never** the
analysis conversation, notes that explain why a finding was written, or draft deliverables. A finding that cannot be
re-derived from its locator alone goes back as a revision.

## What it opens

`python3 scripts/review.py scope <slug> audit` writes `review-scope.csv`: **every destructive URL row, every Ask, and
an evenly spaced sample of the rest.** Open exactly those rows. For each:

1. Open the evidence at the locator (for a URL row: its screen row).
2. Re-derive the conclusion from the evidence alone.
3. **State the strongest case that it is wrong.**
4. Run the challenge list.
5. Confirm, revise (a superseding row with a higher `ext_revision` — never an edit) or withdraw.

## Challenge list

- Unsupported causation — cause, or co-occurrence?
- Methodology presented as platform law
- Arbitrary thresholds; volume doing the work evidence should do
- Severity from a tool label rather than CM-061 (Fix · Fix and list · Ask; only the four Ask kinds)
- Implementation smuggled in (markup, drafted copy, executable steps)
- Tool output promoted without corroboration; a `CONTRADICTED` cross-check ignored; URLs compared without normalisation
- A missing "The Best" (CM-020) or missing JavaScript-rendered data treated as a defect
- A blog redirect without observed conflict (CM-021)

## Destructive rows

Every merge, redirect, noindex or canonical change sits on a URL the screen **passes** (or a `needs evidence` row
whose missing evidence the map now cites), has a target and a safer alternative. `python3 scripts/pagedec.py screen
<slug> --check` must pass. Otherwise the row is withdrawn — kept live, no redirect label, no target — never
downgraded (CM-001).

## Record

`review-s17.csv` (register, id, reviewed_revision, outcome, new_revision, reason), the superseding rows, and in
`decisions.md`: "Independent review per CM-026 (fresh-context reviewer)." Report counts: confirmed, revised, withdrawn.
The reviewer never renders anything and never writes the review sheet.
