# Stage 6 — Pilot, services, locations, ship (one session each)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: build (Opus), brief-writer (Sonnet), clerk.

| Step | Command | Ends at |
|---|---|---|
| **Pilot** — 1 service + 1 location: briefs, one draft per page (fresh subagent each), the review, in ONE run | `/build write pilot` | ONE line: `/approve <slug> batch:pilot:briefs batch:pilot:drafts mode:build:brief=auto` (+ `--sem`) → pilot corrections |
| **All service pages** in one run | `/build write <services batch>` | `writeback` (once, at the brief approval) → the draft review sheet → `batch:<id>:drafts` |
| **All location and hub pages** in one run | `/build write <locations batch>` | `writeback` (once, at the brief approval) → the draft review sheet → `batch:<id>:drafts` |
| **Ship everything** — every approved page as a WordPress draft, link tables complete | `/build ship` | condition **pages_drafted** |
| The VA Worklist handover (Redirects, Publish, After publish), then each returned worklist checked | `/build handoff`, `/build published <id>` | condition **pages_built** |

- **CM-061 — one review per step.** After all pages of a section are written, one checker pass; one review sheet
  (`build/<section>/<step>-review.csv`, `review.py`): Fix (form, silent) · Fix and list (decided for you) · Ask (only
  the four kinds). Paul answers in one line ("accept all except 7b") with `/build <slug> review <section> <step>
  "…"`; the approval follows (no `--sem`). At most two review sheets and two approval lines per section.
- Page agents run in one message and are waited for; their results are files (`build/<section>/results/`); the build
  agent reports once and the main chat relays nothing in between. After Paul answers a review sheet every page is
  recorded again at the version the answers produced — `approve.py` refuses the briefs or drafts approval otherwise.
- CM-043 holds: each page's draft comes from its own fresh subagent (`status.py page-stage … --agent <id>`, logged).
- Writing never waits on a VA (P8): open handoffs are listed under "Waiting on (not blocking)".
- The Brand Guide is written **once per section**, at its brief approval (`/build writeback <id>`, CM-061); drafts,
  the draft review and ship never write it. If that write-back changes an approved value, `brand_guide_approved` rides
  on the section's approval line.
- Placeholders (P11): only `[NEED: …]` and `[LINK → /slug/ · reason]`; every one is listed in the approval line and
  becomes an "Open items" notice and a worklist row at ship; `/verify` fails a live page that still has one.
- Route B (Paul writes): the build agent lists issues against the rules and never rewrites Paul's copy.
- Sensitive clients: content needs the human review recorded; health claims need the practitioner's sign-off (CM-025).
- Homepage and about last, or with the ship when approved.
