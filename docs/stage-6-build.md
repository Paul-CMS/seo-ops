# Stage 6 — Pilot, services, locations, ship (one session each)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: build (Opus; draft-writer on Sonnet after Paul's yes), researcher (Sonnet).

**Rewrite 4 (D2, D5): no brief.** Each section is on a route (`status.py show`). **outline** — every section without approved briefs: the write run builds the evidence packs, `outline.py` writes each page's outline by script from the approved plan row + the spec (the approved plan file never changes), one fresh subagent drafts each page, one draft review sheet, one approval line. **briefs** — a section whose briefs were approved before (HMM pilot and services) finishes the old way: `docs/build-brief-route.md`.

| Step | Command | Ends at |
|---|---|---|
| **Pilot** (only when `status.py pilot` says so) — 1 service + 1 location, in ONE run | `/build write pilot` | ONE line: `/approve <slug> batch:pilot:drafts` → pilot corrections (`--none` when Paul changed nothing) |
| **All service pages** in one run | `/build write <services batch>` | the draft review sheet → `writeback` → `batch:<id>:drafts` |
| **All location and hub pages** in one run | `/build write <locations batch>` | the draft review sheet → `writeback` → `batch:<id>:drafts` |
| **Ship everything** — every approved page as a WordPress draft, link tables filled from the wheel (`wheel.py`, CM-064) | `/build ship` | condition **pages_drafted** |
| The VA Worklist handover: mechanical QA (`qa.py`, errors refuse) → schema of every page (`schema.py`, no partial schema) → Redirects, Publish (all pages together, each with its schema), After publish; then each returned worklist checked | `/build handoff`, `/build published <id>` | condition **pages_built** |

- **CM-064 — Finish folds into the plan.** The wheel and the schema are scripts, from the approved site plan and the
  Brand Guide; nobody approves them separately. Every page stays a draft until all are drafted, then all are published
  together (Paul's rule). In-flight sections keep what they already have — nothing approved is re-rendered.
  Brand Guide Section F must be complete before the handoff (`schema.py gate <slug>` lists what is missing).

- **CM-061 — one review per step.** After all pages of a section are written, one checker pass; one review sheet
  (`build/<section>/<step>-review.csv`, `review.py`): Fix (form, silent) · Fix and list (decided for you) · Ask (only
  the four kinds). Each value a writer chose that the plan did not fix is a Fix and list row. Paul answers in one line ("accept all except 7b") with `/build <slug> review <section> <step>
  "…"`; the approval follows (no `--sem`). At most two review sheets and two approval lines per section.
- Page agents run in one message and are waited for; their results are files (`build/<section>/results/`); the build
  agent reports once and the main chat relays nothing in between. After Paul answers a review sheet every page is
  recorded again at the version the answers produced — `approve.py` refuses the briefs or drafts approval otherwise.
- CM-043 holds: each page's draft comes from its own fresh subagent (`status.py page-stage … --agent <id>`, logged).
- Writing never waits on a VA (P8): open handoffs are listed under "Waiting on (not blocking)".
- The Brand Guide is written **once per section** (`/build writeback <id>`, CM-061): on the outline route from the
  reviewed drafts, before their approval line; on the brief route at the brief approval. Ship never writes it. If that write-back changes an approved value, `brand_guide_approved` rides
  on the section's approval line.
- Placeholders (P11): only `[NEED: …]` and `[LINK → /slug/ · reason]`; every one is listed in the approval line and
  becomes an "Open items" notice and a worklist row at ship; `/verify` fails a live page that still has one.
- Route B (Paul writes): the build agent lists issues against the rules and never rewrites Paul's copy.
- Sensitive clients: content needs the human review recorded; health claims need the practitioner's sign-off (CM-025).
- Homepage and about last, or with the ship when approved.
