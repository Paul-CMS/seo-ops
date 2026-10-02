---
description: Apply approved changes - check the live value first, skip what's done, drafts by default, VA handoffs for everything the system must not touch
argument-hint: <slug> [safe|structural|page <page_id>|wheel|schema] [--live]
---

Arguments: $ARGUMENTS

Follow CLAUDE.md §4. Look up each change's kind in `scripts/gates.json` → `change_kinds`.

| Scope | Gates for run.py start | What it covers |
|---|---|---|
| safe | impl_safe | broken links, alt text, image URLs, sitemap, robots.txt, meta description duplicates, speed |
| structural | impl_structural | redirects, slugs/URL changes, consolidations, SEO titles, H1s |
| page <id> | page:<id> | that page's approved content |
| wheel | block2 | link tables |
| schema | block3 | schema |

1. `python3 scripts/run.py start <slug> implement --gates <gates>` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands). Exit 4 → refuse and
   say which gate is missing; exit 3 → stop and ask Paul.
2. Build the change list from the APPROVED source only (Technical Blocker Checklist, URL
   Decision Map, approved SD/LD file, Link Wheel Tables, validated schema). Show Paul the list
   and the channel for each item before doing anything.
3. For each item, by channel:
   - **System (wp.py):** read the current value first (`wp.py get`). Already the new value →
     logged SKIPPED. Different from what the audit recorded → STOP, ask Paul. Otherwise apply
     and read back. Alt text: `wp.py set-alt`. New page content: `wp.py create-draft` (a
     WordPress draft, never published). Titles/meta/head field only once `wp_pilot_done` is true.
   - **VA handoff (handoff.py):** redirects (always), slugs (always, with their paired
     redirect), titles/meta until the pilot, robots, sitemap, speed, image URLs, broken links.
     `python3 scripts/handoff.py create <slug> --run <RUN_ID> --kind <k> --to Jonie|Gwen --items <csv>`.
     Upload the handoff `.md` and `.csv` to the client's Drive folder (`02 - Build/` or
     `03 - Finish/`). Paul or the VA sends; the system does not message anyone.
4. **--live** (publishing an existing live page): first ask Paul to confirm a fresh ManageWP
   backup and the time it was taken. Pass it as `--backup-confirmed "ManageWP backup <time>,
   confirmed by Paul"`. No confirmation → no live change.
5. When a VA returns a worksheet: `handoff.py ingest <slug> --run <RUN_ID> --handoff <H-ID> --returned <csv>`,
   report invented refs and silent omissions, then `/verify`.
6. Handoff Log section; `run.py finish <slug> <RUN_ID> --summary "<n> applied, <n> skipped, <n> handed off, <n> stopped" ...`.
