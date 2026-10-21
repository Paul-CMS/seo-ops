# Stage 7 — Finish (release QA)

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: finish (Sonnet), finish-qa (Opus — sensitive clients and a sample only).

**CM-064 (Rewrite 4 Phase 5): Finish folds into the plan.** The link wheel (`wheel.py`) and the schema (`schema.py`)
are scripts and ship with the drafts (stage 6: `/build ship`, `/build handoff`); there is no wheel approval. What is
left here is the release check of the published pages.

| Step | Command | Ends at |
|---|---|---|
| Release QA: `qa.py check <slug> --stage live` (every published page against its approved file and its schema, no agent) → `qa.py explain` → content QA by finish-qa on `qa.py sample` → punch-list → acceptance | `/finish qa` | **release_approved** (needs blockers cleared) |

- The QA covers **published pages only**. Its punch list is `finish/qa/qa-live.md` (errors · warnings · notes, each
  with the fix and who acts); `qa.py explain` adds plain explanations on the Claude API (Haiku), or keeps the fixed
  hints when there is no key.
- Content QA runs in finish-qa, never the context that wrote the copy (CM-018) — on every page for a sensitive client
  (CM-025), else on the sample `qa.py sample` picks (every page type, then by a fixed hash).
- CM-022 exceptions are kind-1 Asks in the site plan (`wheel.py asks`), never proposed here.
