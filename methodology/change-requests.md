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
