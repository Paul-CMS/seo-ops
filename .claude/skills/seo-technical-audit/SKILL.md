---
name: "seo-technical-audit"
description: "Run a full technical and local SEO audit (the Analysis step) against a client's exports, then the fresh-context review and the audit's one review sheet. Use this whenever a technical SEO audit, site audit, crawl analysis or audit review is requested for a local-business client; when Screaming Frog, site-auditor, citation tracker, Search Console or local grid exports need analyzing into findings; when someone mentions a finding register, a URL decision map, a redirect screen or an evidence manifest; or when an existing audit needs its fresh-context review. Produces an append-only finding register, the URL Decision Map, the audit review sheet and the client's confirm list. Implements nothing."
---

# Technical SEO Audit — the slim audit (CM-063)

**This skill diagnoses and decides by default. It never implements.** No schema, no drafted titles or meta
descriptions, no executable redirect rules, no content, no citation orders, no live changes. If an output could be
pasted into a CMS and shipped, the boundary has been crossed.

**The scripts do the clerical and the mechanical work; you do only the judgment.** Rules live in
`methodology/rulings.md` (cite IDs: `python3 scripts/rulings.py CM-…`, never the file whole). Standing configuration is
in `methodology/agency-profile.md`: DataforSEO OnPage crawl (no JavaScript rendering) converted to Screaming
Frog-shaped tables; missing rendered data is never a finding.

Read with this file: `references/finding-standard.md` (the record, severity, Asks) and `references/analysis-rules.md`
(what to look at). Everything else in `references/` is background the scripts already apply.

## Order of work

| Step | Who | What |
|---|---|---|
| S12 | `pipeline.py <slug> inventory --phase audit` | ingest → cross-checks → auto conformance → **redirect screen** → Evidence Manifest |
| S13 entity | you | the site against the Brand Guide: triple, NAP, brand search, supporting assets |
| S14 architecture | you + `pagedec.py screen --check` | the URL Decision Map — every URL typed and decided |
| S15 triage | `conformance.py triage` (+ `judge`) | rebuild / light fix / keep — no scorecards |
| S16 technical | you + `render.py blockers` | technical findings; the Fix rows are the blocker checklist |
| S17 review | `audit-reviewer` (fresh context) | `review.py scope <slug> audit` lists what it must open |
| S18 sheet | `review.py sheet <slug> audit`, `render.py all` | the one review sheet; the client's confirm list |

Read `00-crosschecks.md` first: anything `CONTRADICTED` blocks the related finding outright.

## S14 — the URL Decision Map

Read `redirect-screen.md`. For every URL the screen has already computed CM-019 conditions 1–3 from rankings,
backlinks, GSC/GA4, the GBP website field and the citation domains:
- **fail** → never a destructive candidate. Keep it live (`Improve`, `Keep`, or `Needs Evidence - keep live (fails C…)`),
  never with a redirect label or a target.
- **pass** → may be a redirect/merge candidate when the page has no place in the entity model; condition 4 (no leads)
  is the client's and goes on the client list by itself (the sheet asks it once for all of them).
- **needs evidence** → yours: find the missing evidence or keep it live.

Then decide what only judgment can: **entity mismatches** (a page for another area, a discontinued service, a
duplicate entity), the target of each redirect, holds. Never delete, always 301 (CM-001). Blog redirects need observed
conflict (CM-021). The map has a row for every page. Before S15: `python3 scripts/pagedec.py screen <slug> --check`
must pass (it refuses every destructive row on a failing URL — the withdrawals HMM's reviewer had to make).

## S15 — triage, not scorecards

`python3 scripts/conformance.py judge <slug> --run <RUN_ID>` (the API scores the pages Build will not rewrite), then
`python3 scripts/conformance.py triage <slug> --run <RUN_ID>` writes the `Conformance Triage` column. Pages Build
rewrites are `rebuild` and are never scored. A `light fix` page's failed checks become findings (one finding per
check, listing every page). With no API key, judge says so and you score the scoring set's judgment checks yourself
into `audit/conformance-judgment.csv`, then run triage.

A live homepage H1 that fails HP-06 stays locked (HP-08) unless CM-059's three conditions hold: `h1lock.py check` and
put its table to Paul as an Ask (kind 1; default: no H1 change).

## Findings

One row per issue in `findings.csv`, listing every affected URL, with an evidence locator — refuse, don't warn.
Severity is CM-061's (`finding-standard.md`): **Fix** · **Fix and list** · **Ask**. Append-only: a correction is a new
row with a higher `ext_revision`. Conflicts between sources go in `conflicts.csv` (PROC-01) and become kind-4 Asks.

There is no clarification stop: a question becomes an Ask row in the one sheet. A public fact is never asked (the
researcher looks it up); a client fact carries its `searched:` line (`ext_searched`) and goes to the client list.

## S17 and S18

The command runs the `audit-reviewer` on the registers only (CM-026). Then `python3 scripts/review.py sheet <slug>
audit --run <RUN_ID>` and `python3 scripts/render.py all <slug> --run <RUN_ID>`. Deliverables: the registers (CSV),
the audit review sheet and the Evidence Manifest — no Recommendations document, no Markdown register. The audit is
internal; the client sees only `client-questions.csv`, sent by Paul.

## Working record

```
clients/<slug>/audit/<date>/
  decisions.md  00-manifest.csv  00-crosschecks.md  conflicts.csv
  redirect-screen.csv/.md    the CM-019 screen (script)
  findings.csv               append-only, one row per finding revision
  url-decision-map.csv       + Conformance Triage (script column)
  review-scope.csv           the reviewer's rows (script)
  audit-review.csv/.json     the one review sheet; client-questions.csv
  deliverables/              rendered: Evidence Manifest, URL Decision Map view, Audit Review Sheet
```

## Stop conditions

Stop and escalate when identity, ownership, address, a legal claim or data provenance is disputed; when evidence for
a destructive recommendation is unavailable (keep it live); when an action would cross into implementation; when
regulated content lacks a qualified reviewer (CM-025); when spend or an external submission lacks approval.
