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
Built in rewrite 3 §7 (it was part of Paul's handoff): the Document Checklist has an "Intake documents" row for it, the data manifest lists it (read by discovery:audit), and discovery:audit's read list names it. Awaiting Paul's accept, then DONE.

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

- CR-020 · 2026-10-12 · DONE · system session · commit 9d2268f

## CR-025 · 2026-10-12 · approve.py accepts a drafts approval at drafts-reviewed or any later batch state (sem_applied included)
Raised in a system session by Paul.
Apex services: /approve batch:services:drafts was REFUSED ('the drafts and their semantic review are not written yet') because the batch is at sem_applied - the SEM answers were applied before the approval was recorded. approve.py must accept a drafts approval when the batch is at drafts_written or any later state, sem_applied included. When the SEM items are already applied, the approval records them as applied and they are not re-applied. Test for this case.

---

- CR-025 · 2026-10-12 · ACCEPTED · Paul · Paul asked for this fix directly in the 2026-10-12 system session

- CR-025 · 2026-10-12 · DONE · system session · commit f28cbdb

## CR-026 · 2026-10-12 · Rewrite 3 Phase 2: sections shown in STATUS.md and /where
Raised in a system session by Paul.
Raised in a system session by Paul (rewrite 3 handoff §11, Phase 2 — after Apex locations ship). Not built yet. STATUS.md and /where show the build by section (services, locations with hubs, homepage and core pages, additional pages) and step (briefs, brief review, drafts, draft review, ship): where each section stands, its review sheets and what Paul answers next.

---

## CR-027 · 2026-10-12 · Rewrite 3 Phase 2: homepage, core pages and additional pages as steps after locations
Raised in a system session by Paul.
Raised in a system session by Paul (rewrite 3 handoff §11, Phase 2 — after Apex locations ship). Not built yet. The homepage and core pages, then additional pages, become sections built after the locations section, with the same steps, evidence packs, review sheets and once-per-section Brand Guide write-back (CM-061).

---

## CR-028 · 2026-10-12 · Rewrite 3 Phase 2: every refusal prints what happened plus the next command
Raised in a system session by Paul.
Raised in a system session by Paul (rewrite 3 handoff §11, Phase 2 — after Apex locations ship). Not built yet. Every script refusal (exit 3/4/7) prints what happened in plain words plus the next command to run, or the one line to send Paul.

---

## CR-029 · 2026-10-12 · Rewrite 3 Phase 2: /stuck <slug>
Raised in a system session by Paul.
Raised in a system session by Paul (rewrite 3 handoff §11, Phase 2 — after Apex locations ship). Not built yet. A /stuck <slug> command: when a client run cannot go on, it says plainly why, what is open, and the one next command or the one line to send Paul.

---

## CR-030 · 2026-10-12 · Rewrite 3 Phase 3: the rehearsal client clients/_rehearsal/
Raised in a system session by Paul.
Raised in a system session by Paul (rewrite 3 handoff §11, Phase 3 — before the VA takes over). Not built yet. A rehearsal client (clients/_rehearsal/) a VA can run end to end — every section and step, the review sheets and approvals — with fake WordPress and DataforSEO, no cost and no real client data.

---

## CR-031 · 2026-10-12 · Rewrite 3 Phase 3: VA-SETUP rewritten around the steps
Raised in a system session by Paul.
Raised in a system session by Paul (rewrite 3 handoff §11, Phase 3 — before the VA takes over). Not built yet. VA-SETUP.md rewritten around the sections and steps (briefs, brief review, drafts, draft review, ship), the review sheets and the one-line answers.

---

## CR-032 · 2026-10-12 · Brief step: the SOP says Build writes public research into build/evidence/<page>
Flag: apex-roofing-of-the-lowcountry F-018 · step build:brief · run 20261012-150859-build-1044 · flagged by Claude (2026-10-12T15:32)
What: Brief step: the SOP says Build writes public research into build/evidence/<page>.facts.json, but there is no script for it. The guard blocks inline Python, and running a scratchpad script on the facts files was denied by the permission classifier (audit tampering). So the 2026-10-12 researcher findings (Lady's Island neighborhoods/things/top sites, Okatie neighborhoods+top sites, St. Helena things to do, Fripp neighborhoods, Levy county) are not on the grids. Needed: an evidence.py/facts.py subcommand that records a page fact with source and status.
Workaround used: Research kept in the run's research JSONs; each brief cites it as 'public research 2026-10-12 — not yet on the grid'. The gate already cleared all 11 pages (6 PASS, 5 WARN), so no page was held for this.

---

## CR-033 · 2026-10-12 · methodology/sources/sc-lowcountry.md: new official sources read this run should 
Flag: apex-roofing-of-the-lowcountry F-019 · step build:brief · run 20261012-205526-build-9baf · flagged by Claude (2026-10-12T21:23)
What: methodology/sources/sc-lowcountry.md: new official sources read this run should be added at /system-review — Callawassie Island POA Design Standards (https://www.callawassieisland.com/wp-content/uploads/2025/06/20240201ARC-Guidelines-.pdf), Town of Bluffton Flooding and Drainage Concerns (https://www.townofbluffton.sc.gov/444/Flooding-and-Drainage-Concerns), Beaufort County Council district maps (neighbourhood labels), Town of Ridgeland About page (incorporation 1894), Jasper County community centers / boat landings pages, City of Beaufort Bailey Bill FAQ (https://cityofbeaufort.org/m/faq?cat=28). The Town of Bluffton Neighborhoods PDF URL is still missing from the list; the Beaufort County Passive Parks page now 301s to a 403.
Workaround used: Cited directly in the page facts files and briefs for this client (research log RL-locations-1..12, round2.json).

---

## CR-034 · 2026-10-13 · CM-061 writes C3 once, at the brief approval, but the location briefs give 'sugg
Flag: apex-roofing-of-the-lowcountry F-020 · step build:writeback · run 20261012-213607-build-27a0 · flagged by Claude (2026-10-13T07:00)
What: CM-061 writes C3 once, at the brief approval, but the location briefs give 'suggested headings (writer may re-word inside the rules)' and some FAQ questions say 'writer may re-word'. Drafts never write the Brand Guide, so any heading or FAQ the draft re-words leaves C3 out of step with the shipped page, and later sections check collisions against stale rows.
Workaround used: C3 records the H2s and FAQ questions exactly as briefed (locations, 107 rows). The draft checker pass should hold each draft to its briefed headings, or list any re-word as a Fix-and-list row so the next write-back (or a system fix) can correct C3.

---

## CR-035 · 2026-10-13 · Location drafts cannot re-read official PDFs (Port Royal flood guide, Beaufort C
Flag: apex-roofing-of-the-lowcountry F-021 · step build:draft · run 20261013-082022-build-66b5 · flagged by Claude (2026-10-13T08:27)
What: Location drafts cannot re-read official PDFs (Port Royal flood guide, Beaufort County ch. 78 flood ordinance, Dataw Design Guidelines, Beaufort County District 9B map): WebFetch returns unreadable binary and no PDF text tool is installed, so drafts rest on earlier brief-time reads and some facts (e.g. the Beaufort County cumulative substantial-improvement period) stay unconfirmed.
Workaround used: Drafts state no unconfirmed figure, cite the brief-time reading, and tell the reader to ask the office; list each for the drafts review.

---

## CR-036 · 2026-10-13 · review.py apply ends with 'apply every item to its page in this run, then re-rec
Flag: apex-roofing-of-the-lowcountry F-022 · step build:drafts · run 20261013-133740-build-53f3 · flagged by Claude (2026-10-13T13:53)
What: review.py apply ends with 'apply every item to its page in this run, then re-record the files', but no command says how. Re-recording each draft with status.py page-stage from the one review run would give every page the same run and agent, which per_page_files then refuses as one context for all pages (CM-043). The page-stage sha is stored but never checked, so the edited drafts stay recorded under their own-run records.
Workaround used: Applied the review items to the drafts in this run, logged each change with run.py change (old/new snapshots), and recorded the section with status.py batch locations --state drafts_written --review-sheet …; page-stage records were not re-written.

---

## CR-037 · 2026-10-13 · evidence_pack.py maps the review topic 'communication' to the facts.json key pra
Flag: apex-roofing-of-the-lowcountry F-023 · step build:brief · run 20261013-140538-build-1832 · flagged by Claude (2026-10-13T14:13)
What: evidence_pack.py maps the review topic 'communication' to the facts.json key practice:explains, while the build agent instructions and the researcher use practice:communication; reviews.py checked under practice:communication does not mark the pack topic as checked.
Workaround used: Recorded the same by-meaning count (32) under both practice:communication and practice:explains in run 20261013-140538-build-1832.

---

## CR-038 · 2026-10-13 · run.py finish for build:write (produces batch_written:h1) requires a brief AND a
Flag: apex-roofing-of-the-lowcountry F-024 · step build:write · run 20261013-160308-build-074c · flagged by Claude (2026-10-13T16:13)
What: run.py finish for build:write (produces batch_written:h1) requires a brief AND a draft recorded from this run for every page. The h1 briefs were written in run 20261013-140538-build-1832 and approved by Paul 2026-10-13, and the write-back ran on them, so this run only had drafts to write. finish refuses (exit 12). Re-recording the approved briefs under this run would rewrite approved records just to satisfy the check. When briefs come from an earlier run and are already approved, the check should accept them.
Workaround used: Drafts recorded with their own agent ids, review sheet written (3 Ask), batch h1 recorded drafts_written, sheet copied to Drive, handoff and summary written. Run left unfinished. Paul decides: re-record the unchanged briefs under this run and finish, or abort the run (the drafts, sheet and records stay).

---

## CR-039 · 2026-10-13 · review.py apply tells the agent to 're-record the files' after applying, but sta
Flag: apex-roofing-of-the-lowcountry F-025 · step build:review · run 20261013-162715-build-f1d2 · flagged by Claude (2026-10-13T16:28)
What: review.py apply tells the agent to 're-record the files' after applying, but status.py page-stage --stage draft refuses in a build:review run ('a draft is recorded only by its own /build draft run or the batch's write run'). With F-024 the write run could not be finished either, so an edited draft has no run that can re-record it.
Workaround used: Edit applied to the draft file and logged as change #887; draft not re-recorded. build:review produces nothing, so finish is not blocked.

---

## CR-040 · 2026-10-13 · publish.py drafts --all refused the locations batch: its approved drafts file li
Flag: apex-roofing-of-the-lowcountry F-026 · step build:ship · run 20261013-163153-build-d38b · flagged by Claude (2026-10-13T16:32)
What: publish.py drafts --all refused the locations batch: its approved drafts file list (status.json batches.locations.drafts.files and files.drafts) includes build/locations/drafts-review.csv, which publish.py treats as a page file ('no header block'). The h1 batch has the same entry (build/h1/drafts-review.csv). Likely cause: status.py batch --state drafts_written --review-sheet adds the review sheet to the drafts file list; publish.py should skip review sheets (or status.py should not record them as drafts).
Workaround used: None applied in the client session. Services batch (7 pages) drafted; locations and h1 not shipped. Needs a /system fix to status.py or publish.py, then re-run /build apex-roofing-of-the-lowcountry ship.

---

- CR-040 · 2026-10-13 · ACCEPTED · Paul

- CR-040 · 2026-10-13 · DONE · system session · commit eacc53e

## CR-041 · 2026-10-25 · Agents load a short tool list; page drafts run as draft-writer
Raised in a system session by Paul.
Paul, 2026-10-25 system session, after first-choice-seamless-gutters (12 chats, ~$63 API-equivalent, 96% Opus agents). build and discovery-audit agents start at 66-71k tokens because they inherit every app tool (browser, docs, simulator); restricted agents start near 10k. Give every agent a tools list; page drafts always draft-writer (model from the models table).

---

## CR-042 · 2026-10-25 · Sonnet for page drafts (Paul's own /approve global model:build:draft=sonnet)
Raised in a system session by Paul.
Paul, 2026-10-25 system session, after first-choice-seamless-gutters (12 chats, ~$63 API-equivalent, 96% Opus agents). Recommendation only: the switch is Paul's /approve line; nothing to build.

---

## CR-043 · 2026-10-25 · Mechanical edits stay in the Haiku chat, never a new Opus agent
Raised in a system session by Paul.
Paul, 2026-10-25 system session, after first-choice-seamless-gutters (12 chats, ~$63 API-equivalent, 96% Opus agents). 'Set five Brand Guide rows to Unknown' ($1.03) and 'Mark insured confirmed' ($1.17) each spawned a full Opus discovery-audit agent for run.py fact calls.

---

## CR-044 · 2026-10-25 · Paul's own fact changes and the system's write-back never void the Brand Guide approval
Raised in a system session by Paul.
Paul, 2026-10-25 system session, after first-choice-seamless-gutters (12 chats, ~$63 API-equivalent, 96% Opus agents). brand_guide_approved was approved 5 times: whole-file approvals were voided by the services write-back (B3/C) and by Paul's own fact answers. Paul: add an Updated line with the new fact, no re-approval; only drafts that use the fact are flagged.

---

## CR-045 · 2026-10-25 · A void Brand Guide never sends a client in Build back to Stage 4
Raised in a system session by Paul.
Paul, 2026-10-25 system session, after first-choice-seamless-gutters (12 chats, ~$63 API-equivalent, 96% Opus agents). after the services write-back voided the approval, next.py showed 'Stage 4 of 8 - Audit' and the new chat told Paul the service pages had not gone through Build.

---

## CR-046 · 2026-10-25 · Paul's words carry across chats; draft edits are recorded, never a side edit
Raised in a system session by Paul.
Paul, 2026-10-25 system session, after first-choice-seamless-gutters (12 chats, ~$63 API-equivalent, 96% Opus agents). a finished chat filled the gaps in nine drafts with a one-off script (no run, not re-recorded); Paul's 'drafts approved, push to WordPress' was lost when he opened the next chat; the drafts approval then refused with 18 version problems.

---

- CR-041 · 2026-10-25 · ACCEPTED · Paul · Paul, 2026-10-25: yes, build all six

- CR-043 · 2026-10-25 · ACCEPTED · Paul · Paul, 2026-10-25: yes, build all six

- CR-044 · 2026-10-25 · ACCEPTED · Paul · Paul, 2026-10-25: yes, build all six

- CR-045 · 2026-10-25 · ACCEPTED · Paul · Paul, 2026-10-25: yes, build all six

- CR-046 · 2026-10-25 · ACCEPTED · Paul · Paul, 2026-10-25: yes, build all six

- CR-042 · 2026-10-25 · ACCEPTED · Paul · Paul, 2026-10-25: yes - the switch itself is his /approve global model:build:draft=sonnet; no code
