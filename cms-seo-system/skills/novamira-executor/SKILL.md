---
name: novamira-executor
description: Implement an approved client handoff on a WordPress site through Novamira — titles, H1s, meta descriptions, page copy, new pages, noindex, redirects and internal link updates — then hand off to QA. Use when a handoff folder is approved and ready to go live, when someone says "run the handoff", "stage the pages", "apply the handoff", "push it to the site" or "roll back the last run". Never use it to decide what to change; it only implements what handoff.json says.
---

# Novamira Executor

You implement. You do not decide. Load only `cms-seo-system/rules/workflow-execution.md` and
`cms-seo-system/handoff/HANDOFF-SPEC.md`. Do not load other rule files or the client's audit.

Model: Sonnet (Haiku is fine for the run itself). Disable every MCP server except this
client's Novamira server before starting (`/mcp`), so tool definitions don't eat the session.

## Hard rules

- Only `handoff.json` decides what changes (NOV-01). If something looks wrong, stop and report;
  never "fix" it on the site.
- Never send page content through the chat. Files move with `curl` through upload links.
- Never read files back from the server with read-file. The executor returns compact summaries.
- Never call write-file or execute-php to edit pages directly. Everything goes through `cms_exec`.
- Never touch the Novamira plugin or the connecting user.

## Steps

`S` = the client slug from handoff.json. `F` = the local handoff folder.

### 1. Build and validate (bash, no tokens)
```bash
python3 cms-seo-system/skills/novamira-executor/scripts/build_bundle.py F
```
Errors → stop and report the ERROR lines. Warnings → include them in your report.

### 2. Install or update the executor on the site (once per site, or when the file changes)
Call Novamira `create-upload-link` with
`{"path": "wp-content/novamira-sandbox/cms-executor.php", "overwrite": true}`, then:
```bash
curl -sS -X PUT -H "<token_header>: <upload_token>" --data-binary @cms-seo-system/skills/novamira-executor/scripts/cms-executor.php "<upload_url>"
```

If the upload returns HTTP 403/405 or the file arrives empty, the site firewall (Imunify,
Wordfence) is blocking PHP in the request body. Fallback: zip it (`zip -j /tmp/cms.zip cms-executor.php`),
upload the zip to `wp-content/novamira-sandbox/cms.zip`, then one short execute-php:
`$z = new ZipArchive(); $z->open( WP_CONTENT_DIR . '/novamira-sandbox/cms.zip' ); $z->extractTo( WP_CONTENT_DIR . '/novamira-sandbox/' ); $z->close(); return file_exists( WP_CONTENT_DIR . '/novamira-sandbox/cms-executor.php' );`
Keep every execute-php call short: long code with SQL or regex gets blocked by the same firewall (HTTP 405).

### 3. Upload the bundle
`create-upload-link` with `{"path": "wp-content/uploads/cms-handoff/S/bundle.json", "overwrite": true}`, then:
```bash
curl -sS -X PUT -H "<token_header>: <upload_token>" --data-binary @F/out/bundle.json "<upload_url>"
```

### 4. Preflight (read-only)
execute-php:
```php
if ( ! function_exists( 'cms_exec' ) ) { require_once WP_CONTENT_DIR . '/novamira-sandbox/cms-executor.php'; }
return cms_exec( 'preflight', 'S' );
```
Any `error` → stop and report. Do not continue to stage.

### 5. Stage (creates drafts only; nothing live changes)
Pick a run id `YYYYMMDD-HHMM` and keep it for the whole run.
`return cms_exec( 'stage', 'S', array( 'run_id' => 'RUN' ) );`
If `next_step` says out of time, call it again with the same run id.
Report the draft links from `issues` (level info). Then STOP: a human VA reviews each draft,
adds images and styling, and then `review.confirmed` is set in handoff.json (NOV-07).

### 6. Apply (after review is confirmed)
Rebuild the bundle (step 1) and re-upload it (step 3) so the review flag is on the server. Then:
`return cms_exec( 'apply', 'S', array( 'run_id' => 'RUN', 'phase' => 'pages', 'offset' => 0 ) );`
Repeat with `next_offset` until `next_step` says pages are done, then:
`return cms_exec( 'apply', 'S', array( 'run_id' => 'RUN', 'phase' => 'site' ) );`

### 7. Verify
`return cms_exec( 'verify', 'S' );` (database view), then hand over to the implementation-qa skill
(live view).

### Rollback
`return cms_exec( 'rollback', 'S', array( 'run_id' => 'RUN' ) );`
Content is restored from WordPress revisions; meta, titles, statuses, created pages and redirects
from the run log. If rollback reports a warning for a page, restore that page from the backup.

## Report format (keep it short)

```
Run RUN — S — <command>
Counts: changed X · unchanged X · created X · errors X · warnings X
Errors: (one line each, page id + message)
Next: <next_step from the result>
```
