---
description: Apply approved changes - check the live value first, skip what's done, drafts only, VA handoffs for everything the system must not touch
argument-hint: <slug> [safe|structural|page <page_id>|wheel|schema]
---

Arguments: $ARGUMENTS

Follow `docs/reference.md` → Implementation. Each change's kind, gate, channel and owner are in `scripts/gates.json` → `change_kinds`.

Steps (`--step`): `safe` (broken links, alt text, image URLs, sitemap, robots.txt, meta description duplicates, speed) · `structural` (redirects, slugs/URL changes, consolidations, SEO titles, H1s) · `page` (`--page <id>`: one page — blog posts, single fixes) · `wheel` (link tables) · `schema`. Batches go out with `/build ship <id>`.
Gates come from `scripts/gates.json` (steps) — `python3 scripts/run.py steps implement` lists them; `run.py start` checks them.

1. `python3 scripts/run.py start <slug> implement --step <step> [--batch <id>|--page <id>]` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   say which gate is missing; exit 3 → stop and ask Paul.
2. Build the change list from the APPROVED source only (Technical Blocker Checklist, URL
   Decision Map, the approved batch drafts, Link Wheel Tables, validated schema). Low technical
   findings go out together as **one** handoff. Show Paul the list
   and the channel for each item before doing anything.
3. For each item, by channel (spec: `wordpress/wordpress-site-setup.md` §5–6; "WordPress connected" must
   be met — `/wp-check` first):
   - **System (wp.py)** — current value first, already correct → logged SKIPPED, different from what
     the audit recorded → STOP and ask Paul:
     - safe fixes: `wp.py set --field description`, `wp.py set-alt`, `wp.py fix-content --kind broken_link|image_url`.
       A client may have a safe-fix cap (`status.py show` prints it); wp.py refuses past it — stop and tell
       Paul how many went out, so he can check them live and raise the cap;
     - structural fixes **after the site's pilot**: `wp.py set --field title|keyword|social_title|social_description|robots|canonical`,
       `wp.py set-head` (schema). Before the pilot these refuse with "VA handoff" — hand them to Jonie.
     - **A live page:** ask Paul to confirm a fresh ManageWP backup and the time it was taken; pass
       `--live --backup-confirmed "ManageWP backup <time>, confirmed by Paul"`. No confirmation → no change.
   - **VA handoff (handoff.py, owner set by the kind):** redirects (always — full URLs, 301, reason, URL
     Decision Map ref), slugs (with their paired redirect), menus, SEOPress site-wide settings, robots.txt,
     sitemap, speed, and structural fields before the pilot.
     `python3 scripts/handoff.py create <slug> --run <RUN_ID> --kind <k> --items <csv>`. Copy the `.md`
     and `.csv` into the client's Drive folder with `drive.py upload <slug> --run <RUN_ID> --file <md> --file <csv>`
     (a file copy, logged — never retyped). Paul or the VA sends;
     the system messages no one.
4. **The system never publishes.** New pages and posts go in as drafts with `/build <slug> ship <id>` /
   `/blog <slug> publish <id>`; Jonie publishes them.
5. When a VA returns a worksheet: `handoff.py ingest <slug> --run <RUN_ID> --handoff <H-ID> --returned <csv>`,
   report invented refs and silent omissions, then `/verify`.
6. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then `run.py finish <slug> <RUN_ID> --handoff <that file> --summary "<n> applied, <n> skipped, <n> handed off, <n> stopped" ...`.
