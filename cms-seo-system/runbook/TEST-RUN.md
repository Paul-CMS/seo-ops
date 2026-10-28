# Version-1 test run (step 5)

Test client: Carolina Carpet Cleaning (carpetcleaningblufftonsc.com).
The test runs the WHOLE workflow start to finish on this client: intake → Agent 1 audit →
Block 1 approval → Agent 2 briefs and drafts → handoff → stage → VA review → apply → QA.
Tasks 3–7 below cover the execution half; run Agent 1 and Agent 2 first as usual, with
the rules/ files loaded per rules/README.md.

Each task below is written as a copy-paste message. Placeholders are in [brackets].

---

## Task 1 — Install the system files (once)

App: Claude Code (terminal) · Model: Sonnet · Who: Paul

Copy the `cms-seo-system` folder into the root of the seo-ops repo, then send:

> Read cms-seo-system/rules/README.md and cms-seo-system/CONFLICT-PATCHES.md. This is a SYSTEM
> session. Apply patches 1–7 to the listed skill files exactly as written, show me a one-line
> diff summary per file, and do not touch any client data.

---

## Task 2 — Connect the client site

App: WordPress admin + Claude Code · Model: none · Who: Paul or Jonie

1. On the client site: install Novamira (+ Pro if available), connect it, note the MCP URL.
2. In Claude Code: `claude mcp add [client-slug]-novamira [MCP URL]` (or the connect command
   Novamira shows), then `/mcp` to confirm it's connected.
3. Take a ManageWP backup. Write the timestamp down.

---

## Task 3 — Write the handoff

App: Claude Code · Model: Sonnet · Who: Paul
Files needed in the client folder: approved drafts, URL Decision Map, Novamira page inventory
(post IDs). Folder name: `[client-slug]-handoff/` (copy cms-seo-system/handoff/template).

> Load cms-seo-system/rules/workflow-execution.md, cms-seo-system/rules/index-redirects.md and
> cms-seo-system/handoff/HANDOFF-SPEC.md only. Using the approved drafts and the URL Decision Map
> for [Client Name], write [client-slug]-handoff/handoff.json and the content files. Include every
> approved page, redirect and noindex from the URL Decision Map. Use the Novamira inventory for post_ids
> (read-only). Leave approved, backup and review empty. Then run build_bundle.py and fix every
> ERROR. Show me only the final summary line and the HANDOFF-REVIEW.md path.

Paul reads `out/HANDOFF-REVIEW.md`, then fills `approved` and `backup` in handoff.json.

---

## Task 4 — Preflight and stage

App: Claude Code (fresh session: `/clear`) · Model: Sonnet · Who: Paul
Before sending: `/mcp` → disable every server except [client-slug]-novamira.

> Use the novamira-executor skill for [client-slug]-handoff. Run steps 1–5 (build, install
> executor, upload bundle, preflight, stage). Stop after stage and give me the draft links.

---

## Task 5 — VA review

App: WordPress admin · Who: VA

For every draft link: add images, apply Kadence styling, check the copy reads right, and do NOT
change the URL slug. PREVIEW drafts are the new version of an existing page: edit the preview,
not the live page. When done, set `review.confirmed: true`, `review.by`, `review.date` in
handoff.json (or tell Paul to).

---

## Task 6 — Apply, verify, QA

App: Claude Code (fresh session) · Model: Sonnet · Who: Paul

> Use the novamira-executor skill for [client-slug]-handoff with run id [RUN from Task 4]. Run
> step 6 (rebuild, re-upload, apply pages then site) and step 7 (verify). Then use the
> implementation-qa skill and give me the QA summary line and the QA-REPORT.md path.

---

## Task 7 — Debrief (what to watch in the test)

- Did the H1 land where the theme shows it (title vs content H1)? Check 1 page by eye.
- Did the PREVIEW draft keep the VA's Kadence styling after apply?
- Did the redirect fire, and did the old page drop to draft?
- How much session usage did Tasks 4 and 6 take? Note it; that is the baseline.
- Test rollback once on the test page: `cms_exec('rollback', ...)` with the run id, then re-apply.
