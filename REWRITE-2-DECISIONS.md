# Rewrite 2 — Paul's start-of-session decisions (2026-10-09)

These are Paul's answers to REWRITE-2-HANDOFF.md §5 step 1. They were given in a chat that was then restarted in this
folder. Read this file after REWRITE-2-HANDOFF.md.

**(0) Baseline (the uncommitted work from design-brief-2026-10-09.md)**
- Commit it as one "pre-rewrite-2" baseline, but **first set CM-054, CM-055 and CM-056 back to PROPOSED**: Paul did
  not approve them.
- In this session: **CM-054 is rejected** (it conflicts with P10). **CM-055 is accepted.** **CM-056 is replaced by
  CM-057** (below).
- Where the baseline differs from REWRITE-2-HANDOFF.md, the handoff wins.
- The baseline commit includes `REWRITE-2-HANDOFF.md` and this file, so the reasons for the rewrite stay in the
  repo history.
- Numbering: wherever REWRITE-2-HANDOFF.md says "CM-054" for the reviews ruling (P5, §5 step 1b and step 9), read
  **CM-057**. CM-054 is already used by the rejected batch-briefs ruling.

**(a) Hooks:** Paul authorises editing `.claude/hooks/` for P2 and P3 only, in this system session.

**(b) CM-057 is approved** with this wording:
> Review content may enter `facts.json` as `customer_reported`, with the quote and the number of reviews that support
> it. It counts as Known for the evidence gate when 3 or more independent reviews support it and nothing conflicts.
> "Independent" means different reviewers: the same reviewer twice does not count, and owner replies do not count.
> The writer states it only as customers describe it ("customers mention…") until Paul or the client confirms it; one
> confirmation makes it a plain fact. Prices, timelines and warranty terms from reviews are never stated as the
> company's; they appear only as a cited customer example. A hit on the client's own site or GBP stays Unverified and
> becomes a one-line yes/no question. Reviewer names stay out of deliverables, and self-serving rating claims stay
> out of schema (CM-027 unchanged).

**(c) URLs**
- HMM: `/services/<x>/` → `/<x>/`, yes. `/service-area/<city>/` → `/<city>/`, yes.
- L-008 is accepted. HMM hubs: `/service-area/charleston/` → `/charleston-metro/` and `/service-area/hhi-beaufort/` →
  `/hilton-head-bluffton-metro/`. **Before applying, check that both metro areas have a Wikidata entry.**
- `/service-area/` → 301 to the homepage.
- Reopen HMM's settled `redirect-targets-default`: anything that pointed at `/services/` now points at the homepage,
  so there are no redirect chains.
- Apex: `/metal-roofing-2/` → `/metal-roofing/` with a 301, plus a VA Worklist row for Jonie to find and clear
  whatever currently holds `/metal-roofing/` first.

**(d) Migration:** Apex and HMM after the baseline commit and after the facts-store tests pass. Do a dry run first that
shows every approval before and after; **stop if any approval would be lost**. Gettysburg: facts only.

**(e) Red Rover:** if the open run logged nothing, abort it; if it logged anything, list it for Paul to decide. Red
Rover's service pages are done, so it is set up later with `/new-client --import`.
- Checked 2026-10-09: run `20261007-160524-new-client-fc92` logged only its STARTED line. It has 0 rows in
  `changes.jsonl`, and `inputs/crawl/` is empty. The later MIGRATION and APPROVAL lines in that log are global and
  don't belong to the run. **So: abort it.**
