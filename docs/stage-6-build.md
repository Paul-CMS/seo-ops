# Stage 6 — Pilot, services, locations, ship (one session each)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: build (Opus), brief-writer (Sonnet), clerk.

| Step | Command | Ends at |
|---|---|---|
| **Pilot** — 1 service + 1 location: briefs, one draft per page (fresh subagent each), the review, in ONE run | `/build write pilot` | ONE line: `/approve <slug> batch:pilot:briefs batch:pilot:drafts mode:build:brief=auto` (+ `--sem`) → pilot corrections |
| **All service pages** in one run | `/build write <services batch>` | `batch:<id>:drafts` (+ SEM picks) → `writeback` |
| **All location and hub pages** in one run | `/build write <locations batch>` | `batch:<id>:drafts` (+ SEM picks) → `writeback` |
| **Ship everything** — every approved page as a WordPress draft, link tables complete | `/build ship` | condition **pages_drafted** |
| The VA Worklist handover (Redirects, Publish, After publish), then each returned worklist checked | `/build handoff`, `/build published <id>` | condition **pages_built** |

- CM-043 holds: each page's draft comes from its own fresh subagent (`status.py page-stage … --agent <id>`, logged).
- Writing never waits on a VA (P8): open handoffs are listed under "Waiting on (not blocking)".
- The Brand Guide content write-back runs right after each drafts approval (`/build writeback <id>`).
- Placeholders (P11): only `[NEED: …]` and `[LINK → /slug/ · reason]`; every one is listed in the approval line and
  becomes an "Open items" notice and a worklist row at ship; `/verify` fails a live page that still has one.
- Route B (Paul writes): the build agent lists issues against the rules and never rewrites Paul's copy.
- Sensitive clients: content needs the human review recorded; health claims need the practitioner's sign-off (CM-025).
- Homepage and about last, or with the ship when approved.
