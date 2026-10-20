# Stage 8 — Blog

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agent: blog (map on Sonnet, posts on Opus).

| Step | Command | Ends at |
|---|---|---|
| Blog Decision Map → redirects (worklist) → posts one at a time | `/blog` | **blog_map_approved**, then **page:<id>** per post |

- Blog redirects need observed overlap (CM-021); protected posts first (CM-007). Links: CM-038 caps; author CM-039.
- Interviews (CM-042): stories every 30 days → the story bank; voice → the author's Voice DNA. Paul sends every set.
