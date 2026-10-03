---
description: Re-check every changed page against the live site (system changes and VA handoffs marked done)
argument-hint: <slug> [--of RUN_ID] [--handoff H-ID]
---

Arguments: $ARGUMENTS

1. `python3 scripts/run.py start <slug> verify` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands) — exit 3 → stop and ask Paul (unless
   Paul asked to verify that unfinished run; then say so and continue).
2. `python3 scripts/verify.py <slug> --run <RUN_ID> [--of <run>] [--handoff <H-ID>]`
   It checks redirects (301 straight to the target, no chain), every system-applied field read back, removed
   broken links, and reports what needs a person (sitemap, robots, speed). After Jonie publishes a batch:
   `verify.py <slug> --run <RUN_ID> --batch <id>` (a blog post: `--page <id>`) — each live page against its
   approved file: URL, SEO title, meta, target keyword, Open Graph and X, H1, headings, content, links.
3. For CHECK items, look yourself where you can (fetch the page, the sitemap, robots.txt) and
   log the result with `run.py change ... --kind verify`.
4. Report counts and every FAIL in plain language with the fix. Failed handoff items go back
   to the VA as a new handoff.
5. `run.py finish <slug> <RUN_ID> --summary "PASS n · FAIL n · CHECK n" ...`
