# Change requests — the one inbox for workflow changes
### Nothing here is in force. Paul answers each item in /system-review (accept · reject · edit); an accepted item is built in a system session, tested, committed, and marked DONE with its commit.

Written only by `scripts/changereq.py` (append-only). Client sessions never edit this file: they flag
(`run.py flag <slug> <RUN_ID> --text "…"`), and `/system-review` collects the flags here. The old proposals inbox
(`lessons.md`, L-001–L-011) is archived in `methodology/archive/lessons.md`; L-008–L-011 continue here as CR-001–CR-004.

## CR-001 · 2026-10-06 · When a hub may be a metro area instead of a county
From: L-008 (lessons.md, PROPOSED since 2026-10-06)
Rule affected: methodology/specs/county-hub.md §1 ("when a county hub exists at all" — Coastal default, needs Paul's ruling), BB-207, BB-208.
What we do now: the county-hub spec assumes one hub per county; the trigger for a hub is an open Coastal default.
What we propose: a hub may cover a metro area instead of one county **only when the metro area is a legitimate, verifiable geographic category** (an official US metropolitan statistical area with a Wikipedia/Wikidata entry, used in its official name and county list). Otherwise the hub is a county hub. Served cities outside every hub's area link from the top service-area hub.
Why (evidence): Home Mobile Medical keeps /service-area/charleston/ (Berkeley, Charleston, Dorchester counties) and /service-area/hhi-beaufort/ (Beaufort and Jasper counties); each spans more than one county but matches an official metro area. Paul 2026-10-06: "sure it can, if this provides legitimate categorization. Otherwise, maybe we hub it by county pages."
Proposed by: Claude for Paul, from his 2026-10-06 direction (home-mobile-medical import).

---

## CR-002 · 2026-10-08 · Homepage H1 lock on a legacy (pre-Standard) homepage
From: L-009 (lessons.md, PROPOSED since 2026-10-08)
Rule affected: BB-313 §3 / methodology/specs/homepage.md element 3 and HP-08 ("never changed once live") vs HP-06 (H1 uses the reserved B1 variants; BB-304, CM-024, CM-046). PROC-01 conflict record: home-mobile-medical audit 2026-10-07, conflicts.csv CF-LOCAL-001.
What we do now: the audit follows the lock — no recommendation changes a live homepage H1, even when that H1 predates the Standard and fails HP-06; the HP-06 failure is reported only.
What we propose: the BB-313 §3 lock applies to a homepage H1 that was built to the Standard, or that ranks top 3 for the homepage's main keyword (CM-020). A legacy homepage H1 that fails HP-06 and holds no top-3 entity ranking may be rebuilt once, in the homepage batch, with the change logged in the URL Decision Map and Brand Guide H; after that the lock applies.
Why (evidence): Home Mobile Medical's live H1 "Enhance Your Independence And Mobility With Our Stair Lift Solutions" (SF h1_all 2026-09-18) uses neither reserved variant ("Mobility equipment supplier", "South Carolina Lowcountry") and names no area; DataforSEO (2026-10-07) shows no entity keyword in the top 3 for the homepage. The same tension came up on Apex Roofing of the Lowcountry: Paul ruled it on 2026-10-08 for that client only (H1 stays as live with a familiar pool variant; the reserved variant goes in the title — Apex CF-LOCAL-002). That ruling is client-specific and is NOT applied to Home Mobile Medical; its question Q4 stays open for Paul. A tension recurring across clients is a candidate for a standing ruling (PROC-01).
Proposed by: Claude (discovery-audit agent), home-mobile-medical audit run 20261007-203219-discovery-784c.

---

## CR-003 · 2026-10-08 · Approve less: two discovery approvals, conditions, briefs after the pilot
From: L-010 (lessons.md, PROPOSED since 2026-10-08)
Rule affected: CM-044 ("decisions are never stages and can never be auto"), the Block 1 gate list, specs/README.md status-line rule.
What we do now (already built, REWRITE-HANDOFF.md R3, Paul's written requirement of 2026-10-08): discovery and audit take two
approvals (Approval 1 = Decision Sheet + entity + client facts; Approval 2 = audit + reconciled Brand Guide);
`discovery_signed_off` and `blockers_cleared` are conditions met from evidence; the page specs are approved once,
globally (`/approve global specs`); after the pilot, when Paul switches `build:brief` to auto, a batch's briefs are not a
stop — Paul approves the drafts only (the pilot's briefs are always approved).
What we propose: amend CM-044 to say so — the batch-briefs decision becomes a condition (every page's brief written in its
own run, evidence gate cleared) once the pilot passed and Paul switched the stage; every other decision stays Paul's.
Why (evidence): Apex Roofing of the Lowcountry needed 7 approvals for discovery + audit, three of them re-approvals
caused by decisions asked before the information that shaped them existed (REWRITE-HANDOFF.md §1, R6).
Proposed by: Claude, rewrite session 2026-10-08.

---

## CR-004 · 2026-10-08 · "The Best" proof quotes the rating as Google shows it
From: L-011 (lessons.md, PROPOSED since 2026-10-08)
Rule affected: CM-020 (proof), Brand Guide D (rating row).
What we do now (built): the rating and review count are recorded exactly as Google shows them on the day, with the date,
never recomputed or rounded by us; the Brand Guide row and the discovery agent say so.
What we propose: add that sentence to CM-020's proof condition.
Why (evidence): Apex — 66 five-star reviews and one two-star showed as "5.0" in our notes; the exact figure was 4.96.
Proposed by: Claude, rewrite session 2026-10-08 (REWRITE-HANDOFF.md §5 #15).

---

## CR-005 · 2026-10-09 · Batch drafting through the Message Batches API
Raised in rewrite 2 (REWRITE-2-HANDOFF.md P12), for a later system session.
If Paul pays API rates, location drafts can run through the Message Batches API at about half price, overnight. Not built in rewrite 2.

---

- CR-001 · 2026-10-09 · ACCEPTED · Paul · REWRITE-2-DECISIONS.md (c): HMM hubs become metro hubs (/charleston-metro/, /hilton-head-bluffton-metro/) once each metro area's Wikidata entry is checked; built in rewrite 2 P7

- CR-001 · 2026-10-11 · DONE · system session · commit f85a547

## CR-006 · 2026-10-11 · new source for Town of Hilton Head Island building permits: https://hiltonheadis
Flag: apex-roofing-of-the-lowcountry F-001 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for Town of Hilton Head Island building permits: https://hiltonheadislandsc.gov/building/permits/ — building permit applications, checklists, CSS portal
Workaround used: used in this run's facts files

---

## CR-007 · 2026-10-11 · new source for City of Beaufort building codes: https://cityofbeaufort.org/154/B
Flag: apex-roofing-of-the-lowcountry F-002 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for City of Beaufort building codes: https://cityofbeaufort.org/154/Building-Codes — city building codes department and state-adopted codes in effect
Workaround used: used in this run's facts files

---

## CR-008 · 2026-10-11 · new source for Town of Port Royal building permits: https://portroyal.org/161/Bu
Flag: apex-roofing-of-the-lowcountry F-003 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for Town of Port Royal building permits: https://portroyal.org/161/Building-Official — building official, permit application and inspections
Workaround used: used in this run's facts files

---

## CR-009 · 2026-10-11 · new source for Jasper County building permits: https://jaspercountysc.gov/servic
Flag: apex-roofing-of-the-lowcountry F-004 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for Jasper County building permits: https://jaspercountysc.gov/services/planning-and-building — county planning and building, permit applications and checklists
Workaround used: used in this run's facts files

---

## CR-010 · 2026-10-11 · new source for Town of Hardeeville building permits: https://www.hardeevillesc.g
Flag: apex-roofing-of-the-lowcountry F-005 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for Town of Hardeeville building permits: https://www.hardeevillesc.gov/2650/Building-Permits — city building permits (zoning procedures at hardeevillesc.zoninghub.com)
Workaround used: used in this run's facts files

---

## CR-011 · 2026-10-11 · new source for City of Ridgeland building permits: https://www.ridgelandsc.gov/p
Flag: apex-roofing-of-the-lowcountry F-006 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for City of Ridgeland building permits: https://www.ridgelandsc.gov/planning-and-community-development/home — planning and community development, residential permit requirements and forms
Workaround used: used in this run's facts files

---

## CR-012 · 2026-10-11 · new source for Jasper County places and attractions: https://jaspersc.org/2021/0
Flag: apex-roofing-of-the-lowcountry F-007 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:31)
What: new source for Jasper County places and attractions: https://jaspersc.org/2021/07/discover-ridgeland-and-hardeeville/ — Jasper County chamber page on Ridgeland and Hardeeville sites and parks
Workaround used: used in this run's facts files

---

## CR-013 · 2026-10-11 · evidence.py questions --all: a second call in the same round overwrites the ques
Flag: apex-roofing-of-the-lowcountry F-008 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:35)
What: evidence.py questions --all: a second call in the same round overwrites the question-set file with 0 questions, because the first call already opened every key (settled.ask) and the rewrite lists them only as 'already asked'. The first set's text survives only in log.md OPEN lines.
Workaround used: rebuilt the set by hand from the OPEN lines + grids into interviews/facts/...REVIEW.md and facts-round-all-2026-10-11.questions.json; settled.py filter + questions.py check passed

---

## CR-014 · 2026-10-11 · evidence.py questions --all opens keys before the page facts files exist: city_s
Flag: apex-roofing-of-the-lowcountry F-009 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:35)
What: evidence.py questions --all opens keys before the page facts files exist: city_served for 11 location pages was asked with a keyword-ranking row as its 'best answer', though Brand Guide E + settled 'business' already answer it; service_scope was grouped across 7 services under Roof Repair's list. Grouping by fact needs per-page pre-fills, and Section E should feed city_served.
Workaround used: wrote city_served facts files from Brand Guide E; closed the keys via run.py decision --settle --closes; per-service scope lines in the hand-built set

---

## CR-015 · 2026-10-11 · reviews.csv has no reviewer_key column, so the researcher counts one reviewer pe
Flag: apex-roofing-of-the-lowcountry F-010 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:35)
What: reviews.csv has no reviewer_key column, so the researcher counts one reviewer per row (CM-057 distinct-reviewer count is approximate).
Workaround used: counted per row; owner replies excluded

---

## CR-016 · 2026-10-11 · Grid marks a Brand Guide D row Unverified when any part is unconfirmed (Warranty
Flag: apex-roofing-of-the-lowcountry F-011 · step build:facts · run 20261011-212524-build-5379 · flagged by Claude (2026-10-11T21:35)
What: Grid marks a Brand Guide D row Unverified when any part is unconfirmed (Warranty terms: manufacturer + workmanship Client Confirmed, only W14 metal 40-year Submitted), which makes the whole row a question.
Workaround used: asked only the W14 part (Q4)

---

## CR-017 · 2026-10-11 · /next started build:brief for the services batch while Paul's 2026-10-11 facts a
Flag: apex-roofing-of-the-lowcountry F-012 · step build:brief · run 20261011-214754-build-8691 · flagged by Claude (2026-10-11T21:54)
What: /next started build:brief for the services batch while Paul's 2026-10-11 facts answers (interviews/facts/... Facts Answers - all - 2026-10-11.md) were on disk but unrecorded: the evidence gate scored on stale facts (metal, slate, skylights BLOCK; scope gaps on the other 4) although the answers likely clear them. next.py / the brief gate does not check for an unrecorded facts-answers file.
Workaround used: Briefs written for the 4 WARN pages with [NEED] markers and a note that the 2026-10-11 answers await /interview facts-answers all; 3 BLOCK pages left unbriefed; re-run the gate after recording.

---

## CR-018 · 2026-10-12 · methodology/specs/service.md §3 #9 and §6 tell writers to leave service-area row
Flag: apex-roofing-of-the-lowcountry F-013 · step build:brief · run 20261012-065658-build-15df · flagged by Claude (2026-10-12T07:03)
What: methodology/specs/service.md §3 #9 and §6 tell writers to leave service-area rows as '| [Link wheel: populate service-area links here] |', but the build rules (P11, stage-6 doc) allow only [NEED: …] and [LINK → /slug/ · reason] placeholders, and publish.py drafts refuses a placeholder without a NEED note. The two rules disagree on the service-areas table placeholder.
Workaround used: Briefs keep the spec's link-wheel row form (as the approved pilot and sibling briefs do); Finish fills the table before ship. Paul to settle the form at /system-review.

---

## CR-019 · 2026-10-12 · writing-commercial.md E10 shows readability.py --exclude-terms <entity terms + n
Flag: apex-roofing-of-the-lowcountry F-014 · step build:draft · run 20261012-074135-build-56f3 · flagged by Claude (2026-10-12T07:44)
What: writing-commercial.md E10 shows readability.py --exclude-terms <entity terms + named sources> as a list, but scripts/readability.py reads --exclude-terms as a file path (FileNotFoundError on a comma list).
Workaround used: Wrote the terms one per line to a scratchpad file and passed its path.

---

## CR-020 · 2026-10-12 · service.md element 8 says the FAQ 'first sentence is the full answer (40-60 word
Flag: apex-roofing-of-the-lowcountry F-015 · step build:draft · run 20261012-074931-build-45cc · flagged by Claude (2026-10-12T07:52)
What: service.md element 8 says the FAQ 'first sentence is the full answer (40-60 words)', which pulls against CM-047 grade 7-8 and the short sentences C5 asks for; also writing-commercial E10 shows readability.py --exclude-terms as a list of terms, but the script reads a file path.
Workaround used: Emergency draft: sentence one answers alone and is short; the whole first answer paragraph runs about 40-60 words. Exclude terms passed as a scratch file.

---

## CR-021 · 2026-10-12 · writing-commercial.md E10 shows 'readability.py <draft> --exclude-terms <entity 
Flag: apex-roofing-of-the-lowcountry F-016 · step build:draft · run 20261012-080653-build-ad60 · flagged by Claude (2026-10-12T08:10)
What: writing-commercial.md E10 shows 'readability.py <draft> --exclude-terms <entity terms + named sources>' as if terms are passed inline, but scripts/readability.py opens --exclude-terms as a file path (OSError: File name too long when given a comma list).
Workaround used: Wrote the terms one per line to a scratchpad file and passed its path.

---

## CR-022 · 2026-10-12 · approve.py rejects SEM items 9-15: the --sem check (scripts/approve.py line ~194
Flag: apex-roofing-of-the-lowcountry F-017 · step interview:facts-answers · run 20261012-122518-interview-16a4 · flagged by Claude (2026-10-12T12:25)
What: approve.py rejects SEM items 9-15: the --sem check (scripts/approve.py line ~194) hardcodes SEM-1 to SEM-8, but the services review table has SEM-1 to SEM-15. Paul's approval 'batch:services:drafts --sem 1,...,15' was refused.
Workaround used: none in a client session; the approval is not recorded until a system session widens the check

---

- CR-022 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: --sem accepts exactly the SEM rows in that batch's table, whatever the count

- CR-022 · 2026-10-12 · DONE · system session · commit fd2de4b

- CR-002 · 2026-10-12 · ACCEPTED · Paul · edited: Paul 2026-10-12: the BB-313 §3 lock lifts only when the live H1 fails HP-06 AND the homepage is not in the top 10 for its main keyword AND has few Search Console clicks for it over 90 days ('few' is a config value; the proposal shows the numbers). Always Paul's decision, never automatic. The old H1 is logged for rollback; a 30-day ranking and clicks check goes on the worklist. Then apply to home-mobile-medical Q4 with its numbers.

- CR-002 · 2026-10-12 · DONE · system session · commit 7c50c9d

- CR-006 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: official government source — add to methodology/sources/sc-lowcountry.md

- CR-007 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: official government source — add to methodology/sources/sc-lowcountry.md

- CR-008 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: official government source — add to methodology/sources/sc-lowcountry.md

- CR-009 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: official government source — add to methodology/sources/sc-lowcountry.md

- CR-010 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: official government source — add to methodology/sources/sc-lowcountry.md

- CR-011 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: official government source — add to methodology/sources/sc-lowcountry.md

- CR-012 · 2026-10-12 · ACCEPTED · Paul · edited: Paul 2026-10-12: local-context source only (things to do, landmarks, area character for location pages); never for permits, codes or any regulatory fact; labelled that way in the source list

- CR-019 · 2026-10-12 · ACCEPTED · Paul · edited: Paul 2026-10-12: merged with CR-021. writing-commercial.md E10 shows readability.py --exclude-terms as inline terms, but the script opens it as a file path (FileNotFoundError / File name too long). Build: --exclude-terms takes a file path or a comma-separated list (an existing file is read; otherwise split on commas); E10 shows both; a test for each. Covers CR-020 point 2.

- CR-021 · 2026-10-12 · REJECTED · Paul · Paul 2026-10-12: merged into CR-019 (same issue)

## CR-023 · 2026-10-12 · Spec approvals per spec file; a changed spec applies to new work only
Raised in a system session by Paul.
What happens now: /approve global specs approves every page spec at once (config.json specs_approval records each file's sha). Any edit to any spec makes page_specs_approved unmet for every client until Paul approves again, so a wording change (e.g. homepage.md element 3 for CM-059) would block clients mid-stage.
What is proposed: approvals are per spec file. A changed spec applies to new work only; a client mid-stage keeps the version it started with (recorded per client, by sha) until Paul moves it over. Paul approves a changed spec on its own, not all specs.
Raised while building CR-002 (homepage.md left unchanged). Left OPEN for a later session.

---

## CR-024 · 2026-10-12 · A 90-day Search Console queries export for the homepage is a standard intake document
Raised in a system session by Paul.
What happens now: no client has a Search Console export in inputs/, so CM-059 condition (c) — few clicks for the homepage's main keyword over 90 days — cannot be checked (Home Mobile Medical Q4: CANNOT TELL YET).
What is proposed: at intake, every client's document checklist includes a Search Console Performance → Queries export, filtered to the homepage, last 90 days (named '<Client> - GSC - queries-homepage-90d - <date>.csv', read by scripts/h1lock.py --gsc).

---

- CR-006 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-007 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-008 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-009 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-010 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-011 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-012 · 2026-10-12 · DONE · system session · commit edf3b2f

- CR-019 · 2026-10-12 · DONE · system session · commit 783a9ae

- CR-020 · 2026-10-12 · ACCEPTED · Paul · Paul 2026-10-12: CM-060 — sentence one answers alone in short plain words; the first answer paragraph is 40–60 words. Spec wording waits for CR-023 or /approve global specs.
