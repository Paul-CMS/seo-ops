# Design brief — seo-ops workflow fixes (for an Opus design session)

Start a NEW session on Opus in ~/Documents/seo-ops. Do not run this in a Haiku stage session.
Paste this file as the first message, or ask the session to read it.

## Ground rules (from CLAUDE.md)
- Paul decides. The system prepares, checks, logs and stops.
- After every system change run `python3 tests/run_all.py`. Never commit a change that fails it. Each new behaviour gets a new check in tests/run_all.py.
- Never read, search or list `.env`. Recursive greps must exclude `.env*`.
- Do not hand-edit generated records (decisions-settled.md, decisions.md, STATUS.md, handoff-log.md, document-checklist.md, approval-record.md). Change the scripts that generate them.
- status.json and log.md are the only records written by hand-free scripts; keep it that way.
- Do not change Apex Roofing client files without Paul's yes. Apex is the live test case.
- Do not commit until Paul asks.

## Problems Paul reported (2026-10-09), with what we verified so far

### 1. Questions get re-asked across sessions
A new session must treat anything already answered as settled.
- Verified: `clients/apex-roofing-of-the-lowcountry/decisions-settled.md` exists and lists Paul's answers.
- Not verified: whether an answer recorded as free text, or with a key that differs from the one the next agent asks, is checked against the settled list. Trace how `/next` and the agents check settled items, and make every answer land in that list under a key the agents actually check.
- Acceptance: a test that records an answer in one run, then starts a new run that would ask the same question, and shows it is not asked again.

### 2. Slug structure
Bradley's standard (per Paul) says: strip `/service-area/` and `/service/` from slugs; keep cities and services as close to the root as possible.
- Verified: `methodology/specs/location.md` row 1 cites BB-208, "city slug only, no service". County hub: "root-proximate, no service in slug".
- Not verified: whether the Apex URL Decision Map or site plan follows this, and whether any slug still carries a prefix. Check against `sop-source/` (BB-208 and the service slug rule).
- Acceptance: a check in tests that fails any generated service or location URL containing `/service-area/` or `/service/`.

### 3. A VA handoff should not stop service page writes; one living handoff document
- Verified: `scripts/gates.json` → condition `blockers_cleared` requires `discovery_signed_off` and is produced by `/build blockers`, waiting on Jonie's handoff. CLAUDE.md §3 step table puts blockers before batches. Confirm which batch steps list `blockers_cleared` as a requirement.
- Requirement: service and location drafting must not wait on any VA handoff. The VA handoff becomes one ongoing document that is handed off after the published service and location pages exist, and is updated as pages are published.
- Acceptance: a test showing batch drafting runs with a blocker handoff still open.

### 4. Provided evidence (reviews, facts) is not used
- Verified: `clients/apex-roofing-of-the-lowcountry/data/reviews/` holds `reviews.csv`, `customer-language.md` and `mentions.csv`. No script in `scripts/*.py` reads `data/reviews`. The evidence gate (CLAUDE.md §5, `methodology/evidence-requirements.json`) reads Brand Guide A and D and the page facts file only.
- Requirement: the evidence step must read the review data and the crawl text, and cite where each fact was found.
- Acceptance: an evidence grid cell that a review answers is marked Known with a source, not Unknown.

### 5. Shallow research before asking
- Requirement: before any gap becomes a question, search every source already on disk (reviews, crawl page text, local grid, rankings, GBP export). Each gap is then either "found (source)" or "searched, not found" with the sources listed. Only "searched, not found" becomes a facts question.
- Acceptance: a gap question is not generated for a fact present in a fixture review.

### 6. A service brief takes a day
- Verified: CM-043 (CLAUDE.md §5) makes each page its own run with its own approval, and the evidence gate runs per page.
- Requirement: one brief run and one approval per batch, with per-page sections inside it. Keep the evidence gate per page, but run it in the batch step.
- Acceptance: a batch of 5 produces 5 briefs in one run, with one approval.

### 7. Publishing as a whole
- Requirement: services and locations are published together, not one at a time. Publication of one page must never block creation of the next. Drafts stay WordPress drafts; Jonie publishes (CLAUDE.md §4).
- Acceptance: a test where page N+1 is drafted while page N is still a draft.

### 8. Placeholders without a note
- Verified: `methodology/rulings.md:181` says missing facts are written `[NEED: …]`. `methodology/rulings.md:554` (output check) bans `[NEED` in any string. These two conflict, so an unlabeled placeholder link can get through. Confirm by reading the lines in context.
- Requirement: every placeholder, including placeholder links, carries a visible `[NEED: …]` note in the final draft. Resolve the conflict in rulings.md through the PROC-01 / lessons.md route (CLAUDE.md §6), not by editing the rule silently.
- Acceptance: a test that fails a draft containing a placeholder href (for example "#", "TBD" or "till present") without a `[NEED` note.

## Deliverable
1. A short plan (a list of changes, file by file) before editing. Paul approves it.
2. The changes, with new checks in `tests/run_all.py`.
3. `python3 tests/run_all.py` output, quoted in full.
4. A list of anything not done, and why.
