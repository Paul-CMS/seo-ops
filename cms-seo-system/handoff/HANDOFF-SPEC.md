# Handoff spec v1.0

One handoff folder per client. Agent 2 writes it at the end of the build; Paul approves it;
the executor (Novamira) implements it; QA checks the live site against it.

```
[client-slug]-handoff/
  handoff.json          source of truth (machine-read, machine-written)
  content/<page-id>.md  page copy for route=build pages (human-editable)
  out/bundle.json       built by build_bundle.py; this is what gets uploaded
  out/HANDOFF-REVIEW.md built by build_bundle.py; what Paul and the VA read
  out/QA-REPORT.md      built by verify_live.py
```

## Why JSON + Markdown, not one Markdown file

- The file is read AND written by scripts and by PHP on the server. JSON parses the same way
  everywhere with no extra libraries (PHP json_decode, Python json). Markdown tables break as soon
  as a cell holds a pipe, a line break or a long paragraph, and partial edits corrupt them.
- Page copy stays in Markdown because people edit it and it converts cleanly to WordPress blocks.
- Humans never need to read the JSON: build_bundle.py renders HANDOFF-REVIEW.md from it.
- Status is not written back into handoff.json. Each run writes its own change log on the server
  (`uploads/cms-handoff/<slug>/logs/<run_id>.jsonl`), which is what resume and rollback use.

## handoff.json fields

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | `"1.0"` |
| `client.name / slug / domain / brand` | yes | slug: lowercase-dashes; domain with https:// |
| `approved.by / date` | yes to run | Paul (WF-01). Empty = executor refuses stage/apply |
| `backup.confirmed / tool / timestamp` | yes to run | ISO timestamp, within 24h of the run (NOV-04) |
| `review.confirmed / by / date` | yes for apply | set after the VA reviewed the staged drafts (NOV-07) |
| `settings.author_id` | no | WP user id for new pages |
| `pages[]` | yes | see below |
| `redirects[]` | yes (may be empty) | see below |
| `noindex[]` | yes (may be empty) | `{url, reason, finding_id}` |
| `link_updates[]` | yes (may be empty) | `{old_url, new_url}`; one per redirect (RDR-05) |

### pages[]

| Field | Required | Notes |
|---|---|---|
| `id` | yes | stable, e.g. `svc-gutter-installation`, `loc-bluffton`, `cty-beaufort`, `home` |
| `action` | yes | `create` (new page, staged as draft) or `update` (existing page) |
| `route` | yes | `build` = full copy from content file · `spo` = Service Page Optimizer handles copy; title/H1/meta only now · `meta_only` = title/H1/meta only |
| `post_id` | update: recommended | from the Novamira inventory; otherwise matched by URL |
| `url` | yes | final URL, root-proximate (URL-01) |
| `post_type` | no | default `page` |
| `seo_title` | yes | TTL-01..05 |
| `h1` | yes | H1-01..07. Written to the theme title or the content H1, whichever the page shows |
| `the_best_reason` | if H1 starts with "The Best" | `kd30` · `rank4-20` · `not_top20_90d` (H1-04) |
| `meta_description` | yes | META-02 |
| `content_file` | route=build | `content/<id>.md`; no `# ` H1 in the file |
| `noindex` | no | true/false |
| `publish` | no | `true` on an `update` page that is still a draft (e.g. drafts created earlier): apply publishes it in the batch. Slug must match `url` |
| `rule_refs`, `finding_ids`, `placeholders` | recommended | traceability; placeholders = list of what still needs client verification |

### redirects[] (RDR-02)

`{from, to, type: 301, reason, finding_id, has_backlinks_or_traffic, retire_source: true}`
`retire_source` sets the old page to draft so it leaves the sitemap (content kept).

## Content file rules (converted to core WordPress blocks)

- `##` H2, `###` H3, `####` H4. Never `#`.
- Paragraphs separated by a blank line. Lists with `- ` or `1. `. One pipe table max (SVC-13).
- Links `[anchor](/url/)`. Bold `**x**`. Placeholders `[PLACEHOLDER: what is missing]`.
- Images: not in the file. The VA adds images during review (NOV-07).

## Who writes what

| Step | Writes |
|---|---|
| Agent 2 (Sonnet) | handoff.json + content files, from approved drafts and the URL Decision Map |
| Paul | `approved`, then later `review` (or the VA sets `review` and Paul confirms) |
| Whoever runs the backup | `backup` |
| build_bundle.py | `out/bundle.json`, `out/HANDOFF-REVIEW.md` |
| cms-executor.php | server change log only |
| verify_live.py | `out/QA-REPORT.md` |
