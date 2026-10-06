---
description: Test the WordPress connection for a client (or run the pilot) and report in plain language
argument-hint: <slug> [--pilot]
---

Arguments: $ARGUMENTS

Spec: `wordpress/wordpress-site-setup.md`.

1. `python3 scripts/run.py start <slug> wp-check` (with `--pilot`: `--step pilot`) → note the RUN_ID
   (last line).
2. `python3 scripts/wp.py check <slug> --run <RUN_ID> [--pilot]`. It needs only the three
   `WP_<SLUG>_…` lines in `.env` (Paul adds them; never read `.env`). If they are missing or rejected, show
   Paul the output of `python3 scripts/wp.py env-lines <slug>` and link the file `[.env](.env)`. It creates two test drafts, writes
   and reads back every SEOPress per-page field on one, trashes both, and publishes nothing.
3. Show Paul the report as it prints — each line OK / FIX / NOTE with what to do. If the REST API or the
   Application Password is blocked, the report names the likely cause (security plugin, host firewall,
   stripped Authorization header — setup §3).
4. Pass → the condition "WordPress connected" is met for 30 days. Fail → nothing on the site changed;
   Paul fixes the FIX items and runs `/wp-check` again.
5. `--pilot` pass → tell Paul he may approve the pilot for this site: `/approve <slug> wordpress_pilot_approved`.
   After that the system writes titles, keyword, social, robots, canonical and schema directly.
6. Write the Handoff Log section to `clients/<slug>/handoffs/run-<RUN_ID>.md`, then
   `run.py finish <slug> <RUN_ID> --handoff <that file> --summary "..."`.
