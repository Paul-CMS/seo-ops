---
description: Apply approved changes - check the live value first, skip what's done, drafts only, VA handoffs for everything the system must not touch
argument-hint: <slug> [safe|structural|page <page_id>|wheel|schema]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §4. Each change's kind, gate, channel and owner are in `scripts/gates.json` → `change_kinds`.

Steps (`--step`): `safe` (broken links, alt text, image URLs, sitemap, robots.txt, meta description duplicates, speed) · `structural` (redirects, slugs/URL changes, consolidations, SEO titles, H1s) · `page` (`--page <id>`: one page — blog posts, single fixes) · `wheel` (link tables) · `schema`. Batches go out with `/build ship <id>`.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps implement` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> implement --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   say which gate is missing; exit 3 → stop and ask Paul.
2. Build the change list from the APPROVED source only (Technical Blocker Checklist, URL
   Decision Map, the approved batch drafts, Link Wheel Tables, validated schema). Low technical
   findings go out together as **one** handoff. Show Paul the list
   and the channel for each item before doing anything.
3. For each item, by channel:
   - **System (wp.py):** read the current value first (`wp.py get`). Already the new value →
     logged SKIPPED. Different from what the audit recorded → STOP, ask Paul. Otherwise apply
     and read back. Alt text: `wp.py set-alt`. New page content: only through `/build ship` (publish.py drafts). Titles/meta/head field only once `wp_pilot_done` is true.
   - **VA handoff (handoff.py):** redirects (always), slugs (always, with their paired
     redirect), titles/meta until the pilot, robots, sitemap, speed, image URLs, broken links.
     `python3 scripts/handoff.py create <slug> --run <RUN_ID> --kind <k> --items <csv>` — the owner is set by
     the kind (WordPress/technical/redirect/title-meta → Jonie, everything else → Gwen); redirect rows get
     301 and must be full URLs.
     Upload the handoff `.md` and `.csv` to the client's Drive folder (`02 - Build/` or
     `03 - Finish/`). Paul or the VA sends; the system does not message anyone.
4. **The system never publishes or changes a live page's content.** New pages and replacement
   content go in as WordPress drafts with `/build <slug> ship <id>` and Jonie publishes them.
5. When a VA returns a worksheet: `handoff.py ingest <slug> --run <RUN_ID> --handoff <H-ID> --returned <csv>`,
   report invented refs and silent omissions, then `/verify`.
6. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary "<n> applied, <n> skipped, <n> handed off, <n> stopped" ...`.
