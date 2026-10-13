# Handoff: batch h1 drafts run is blocked (write run 20261013-160308-build-074c)

**Client:** Apex Roofing of the Lowcountry · **Stage:** 6 of 8 (batch h1: homepage + about) · **Date:** 2026-10-13
**Purpose:** Explain why the drafts run for batch h1 cannot finish, what is already done, and exactly what to do next, so the work does not have to be repeated in a new session.

---

## 1. Short version

- The drafts for both h1 pages (homepage and about) are written, checked and recorded. Nothing has been published or sent to WordPress.
- The run that wrote them, `20261013-160308-build-074c`, cannot be closed. `run.py finish` refuses it (exit 12).
- The review of those drafts has three Ask rows. Paul answered **a, a, a** (one answer per row, the recommended option each time). That answer is **not applied yet**, because a new review run can't start while the write run is open (exit 3).
- Paul has chosen to **abort** the write run himself. Abort is his call and has not been run.
- The homepage and about drafts are not approved yet. "The drafts are approved" in chat does not count: only a `/approve` line typed by Paul sets the gate.

---

## 2. Why it failed (the root cause)

**The finish check (exit 12) wants a brief and a draft recorded in the run being finished, for every page.**

- The h1 briefs were written and approved in an earlier run, `20261013-140538-build-1832`. Paul approved them at `batch:h1:briefs`.
- The Brand Guide write-back (`20261013-144954-build-6134`) also ran on those approved briefs.
- So the write run only had drafts to record. It had no briefs of its own to record.
- Re-recording the briefs under the write run is refused by the system: `status.py page-stage … --stage brief` returns "batch h1 briefs are already approved; Paul re-opens them first (--decision revise)". Re-opening them would mean approving the briefs again, which adds an approval step only to pass a check.
- This is logged as **F-024** in `flags.jsonl`. Its own text says: "When briefs come from an earlier run and are already approved, the check should accept them." This needs a fix in a **system session** (`/system`), not in this client session.

**Contributing factor:** the build agent that ran the drafts step stopped before the drafts subagents finished, then was resumed. The write run was not closed before the review step was started, so the review run was refused (exit 3). Both problems come from the same run being left open.

---

## 3. What is done (recorded, do not redo)

| Item | Status | Where |
|---|---|---|
| Brief, homepage (approved, with Paul's two H2 edits) | Approved at `batch:h1:briefs` | `build/h1/HB - Homepage - Apex Roofing of the Lowcountry.md` |
| Brief, about (approved) | Approved at `batch:h1:briefs` | `build/h1/AB - About - Apex Roofing of the Lowcountry.md` |
| Brand Guide write-back for h1 (B3, C1–C3) | Done, exit 0; no approved value changed | run `20261013-144954-build-6134`; changes #865–866 |
| Homepage draft | Written and recorded (`status.py page-stage … --stage draft`, agent `build-subagent-home-074c`) | `build/h1/HD - Homepage - Apex Roofing of the Lowcountry.md` |
| About draft | Written and recorded (agent `build-subagent-about-074c`) | `build/h1/AD - About - Apex Roofing of the Lowcountry.md` |
| Silent fixes to drafts | Logged as changes #877 and #878 | — |
| Checker pass findings | Written | `build/h1/drafts-findings.json` |
| Review sheet | Written: 3 Ask, 6 Fix-and-list, 3 Fix | `build/h1/drafts-review.csv` (also `.md`, `.json`) |
| Batch state | `drafts_written`, with the review sheet attached | `status.py batch … h1` (exit 0) |
| Drive copies | Review sheet `.md` and `.csv` copied to "02 - Build" | Drive |
| Handoff log and summary for write run | Written | `handoffs/run-20261013-160308-build-074c.md` and `.summary.md` |

**Silent fixes (already in the draft files, do not re-run):**
- Homepage: "licences"/"licence" changed to "licenses"/"license" (2 places).
- Homepage: testimonials intro changed from "most" to "again and again" (no ranking implied).
- About: "enough flashing at every joint" changed to "using enough flashing".

**Placeholders still open (valid `[NEED: …]`, not blockers for drafting):**
- Homepage: gallery photos (6–9 real Apex project photos); Google Maps share link.
- About: photo of Ralph and Pierce Brehany; job titles (only if wanted); the owners' own account of starting Apex (open client question `fact:about:company_story`).

---

## 4. Paul's three Ask rows and his answer

| # | Page | Row | Approved wording | Draft wording | Paul's answer |
|---|---|---|---|---|---|
| 1 | About | licences-spelling-h2 | "Which Licences and Certifications Does Apex Roofing of the Lowcountry Hold?" | Same as approved (not changed yet) | **a** → change to "Which Licenses and Certifications Does Apex Roofing of the Lowcountry Hold?" |
| 2 | Homepage | testimonials-h2-reworded | "What Do Lowcountry Homeowners Say About Apex?" | "What Do Homeowners Say About Working With Apex?" | **a** → keep the draft wording |
| 3 | Homepage | faq-h2-reworded | "What Do Homeowners Ask Lowcountry Roofers Before They Call?" | "What Do Homeowners Ask Roofers in Beaufort and Jasper Counties Before They Call?" | **a** → keep the draft wording |

**Not applied yet.** Row 1 means the About draft (`AD`, line 23) must change from "Licences" to "Licenses". Row 2 and row 3 are already in the homepage draft. Brand Guide C3 still shows the approved wording for rows 2 and 3, and for row 1. That mismatch is expected: drafts never write the Brand Guide, so C3 will update at the next write-back.

Paul said "the drafts are approved, no changes needed". That is not the same as his a/a/a answer. Row 1 still needs applying, because his answer was "a", not "keep". Do not treat the drafts as approved until the answers are applied and Paul types the `/approve` line.

---

## 5. What Paul must decide before the next step

Paul chooses how to close the write run `20261013-160308-build-074c`:

- **(a) Abort it (recommended by the build agent).** Paul runs `python3 scripts/run.py abort …` himself. The build agent's understanding is that the drafts, review sheet, batch state, change records and Drive copies stay. **I have not read the abort script and have not verified this.** Check the abort output before continuing.
- **(b) Re-open the h1 briefs with `--decision revise` and re-approve them.** This adds an approval step only to satisfy the check. Not recommended.

**Chosen direction:** Paul has said he will abort. This file records what to do after he does.

---

## 6. What to do after the abort (in this order)

1. **Confirm the abort worked.** `python3 scripts/next.py apex-roofing-of-the-lowcountry` should no longer report an open write run. If it still does, stop and check what the abort printed.
2. **Start the review run:** `python3 scripts/run.py start apex-roofing-of-the-lowcountry build --step review --batch h1`. Note the RUN_ID.
3. **Apply Paul's answer:** `python3 scripts/review.py apply apex-roofing-of-the-lowcountry h1 drafts --run <review RUN_ID> --answers "a, a, a"`. Check the output before the next step. Note that `--answers` may need to be used; if the script takes a different argument form, use the form the procedure names.
4. **Apply row 1 in the About draft.** Change the H2 at line 23 of `build/h1/AD - About - …md` from "Licences" to "Licenses". Use the review script if it does this; do not hand-edit if the script does it.
5. **Re-run the checks:** `placeholders.py` on both drafts (expect the same valid `[NEED: …]` notes, exit 1 is normal when NEEDs exist), and the sentence-uniqueness check across the h1 drafts.
6. **Log the C3 mismatch** for the next Brand Guide write-back: the About H2 (row 1) and the homepage Testimonials and FAQ H2s (rows 2 and 3) differ from C3.
7. **Finish the review run** with its own handoff file and summary.
8. **Get the approval line:** `python3 scripts/next.py apex-roofing-of-the-lowcountry`. It should give the drafts approval line for batch h1. Paul types that line himself.
9. **Do not run ship yet.** Ship is a later step and needs its own approval.

---

## 7. System fixes to raise in a system session (not here)

- **F-024:** `run.py finish` for `build:write` should accept briefs approved in an earlier run, instead of requiring them to be recorded under the current run. The current check is what blocks this batch.
- **F-023:** evidence script uses `practice:explains` for the "communication" review topic; agent instructions use `practice:communication`. Workaround: both keys were recorded with count 32.
- **F-020 (existing):** Brand Guide C3 is written only at brief approval, so any H2 change made at the drafts review is not reflected in C3 until a later write-back.

---

## 8. Waiting on (not blocking this batch)

- Jonie: publish of the pilot pages (`H-2026-10-09-10-publish`), then `/build apex-roofing-of-the-lowcountry published pilot`.
- Jonie: the blocker redirects and broken links (43 items), then `/verify apex-roofing-of-the-lowcountry`.
- Paul: the WordPress login is an Administrator; SEM-1 (the emergency-leak FAQ link to `/emergency-roof-repair/`) is still open.
- Paul: the open client questions on the homepage and about placeholders (above).

---

## 9. References

- Write run handoff: `handoffs/run-20261013-160308-build-074c.md` and `.summary.md`
- Brief run: `handoffs/run-20261013-140538-build-1832.md` and `.summary.md`
- Write-back run: `handoffs/run-20261013-144954-build-6134.md` and `.summary.md`
- Brief approval record: batch h1 briefs approved 2026-10-13 (`batch:h1:briefs`)
- Review sheet: `build/h1/drafts-review.csv`
- Findings: `build/h1/drafts-findings.json`
- Flag F-024: `flags.jsonl`
