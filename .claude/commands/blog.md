---
description: Agent 4 — Blog Decision Map, redirect handoffs, posts one at a time; or Blog Authority Builder for blog-only clients
argument-hint: <slug> [map|redirects|next|publish <id>|refresh|intake|topics]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md and `docs/stage-8-blog.md`. Check `client.type`.

Steps — full client: `map` · `redirects` · `next` · `publish` (`--page <id>`) · `refresh`; blog-only client: `intake` · `topics` · `next` · `publish`.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps blog` lists them; `run.py start` checks them. `next` waits for the previous post's approval automatically.


1. `python3 scripts/run.py start <slug> blog --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   explain; exit 3 → stop and ask Paul.
2. Use the **blog** subagent with slug, `<RUN_ID>` and the step. It must not share a context with
   commercial writing or auditing.
3. Stop at every approval point and give Paul the `/approve` line (blog_map_approved for the map,
   entity_approved and blog_topics_approved for blog-only, page:<id> per post — sensitive clients with
   `--review`, medical/chiropractic with `--practitioner`).
4. Write the Handoff Log section (25 lines at most; the scripts add the change, decision and step lines) to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> ...`.
