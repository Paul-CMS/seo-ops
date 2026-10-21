# Stage 1 — Setup

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · no agent — the stage chat runs the scripts.

| Step | Command | Ends at |
|---|---|---|
| Intake, the client's Drive folder (v3 only), CMS detection, document checklist (S01) | `/new-client` | the client set-up (checked by `run.py start` for every later step) |

- Open the client's own folder first: `python3 scripts/worktree.py open <slug>`; the chat runs there.
- **Sensitive clients (CM-025, CM-040)** are matched by category (health, health-adjacent trades, legal, insurance,
  financial; lists in `config.json`). An industry not clearly in or out of a list → ask Paul, never decide.
- An imported client (`/new-client --import`) gets its live pages as an approved baseline and a generated site plan;
  the import is refused while a live URL breaks the URL rule (P7): give each page its root URL and its old URL under
  `replaces`.
- Blog-only clients (Blog Authority Builder): short intake → entity foundation → topic list → one post at a time.
