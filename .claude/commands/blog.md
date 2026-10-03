---
description: Agent 4 — Blog Decision Map, redirect handoffs, posts one at a time; or Blog Authority Builder for blog-only clients
argument-hint: <slug> [map|redirects|next|refresh|intake|topics]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. Check `client.type`.

| Client | Step | Gates |
|---|---|---|
| full | map | release_approved |
| full | redirects, next, refresh | blog_map_approved |
| blog-only | intake | *(none)* |
| blog-only | topics | entity_approved |
| blog-only | next | blog_topics_approved |

Add `,page:<prev_id>` to the gates when starting the next post (the previous post must be approved).

1. `python3 scripts/run.py start <slug> blog --gates <gates>` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   explain; exit 3 → stop and ask Paul.
2. Use the **blog** subagent with slug, `<RUN_ID>` and the step. It must not share a context with
   commercial writing or auditing.
3. Stop at every approval point and give Paul the `/approve` line (blog_map_approved for the map,
   entity_approved and blog_topics_approved for blog-only, page:<id> per post — sensitive clients with
   `--review`, medical/chiropractic with `--practitioner`).
4. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> ...` (client view e.g. "Writing articles that answer
   your customers' questions").
