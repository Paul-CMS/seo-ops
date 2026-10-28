---
name: implementation-qa
description: Check that an executed handoff is actually live and correct — titles, H1s, meta descriptions, status codes, redirects, noindex and links to retired URLs — by comparing the live site to the handoff bundle, then hand the judgment sample to a human. Use right after a novamira-executor apply run, or when someone asks "did it go live", "check the run", "QA the handoff". Do not use it to re-audit the site.
---

# Implementation QA (handoff runs)

Companion to `link-implementation-qa` (which still covers link-strategy fix packs with a VA
completion CSV). For handoff runs, the change log replaces the completion CSV and the bundle is the spec.

Model: Haiku or Sonnet. Load `cms-seo-system/rules/workflow-execution.md` only.

## Steps

1. Database view (already done by the executor's `verify`): note its errors.
2. Live view, no tokens:
   ```bash
   python3 cms-seo-system/skills/implementation-qa/scripts/verify_live.py F
   ```
   Read only the printed summary line and `F/out/QA-REPORT.md`. Never fetch pages yourself.
3. If a mismatch says "stale cache", clear WP Rocket for that URL and re-run step 2 once.
4. Human judgment sample (from link-implementation-qa Step 5): a person reads 100% of new or
   rebuilt copy and 20% of link placements. List those pages in the report; don't do it yourself.
5. Report: counts, then mismatches only, then "For Paul". Mismatches go back to the executor
   with a corrected handoff, never patched by hand on the site.
