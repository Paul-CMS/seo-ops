---
name: bb-blog-analysis
description: "Analyze a local business blog for cannibalization and produce the Blog Decision Map. Use this whenever blog posts need classifying against service and location pages, when someone mentions blog cleanup, blog cannibalization, thin or stale posts, blog consolidation, redirect candidates, AI Search Gap posts, or asks which posts to keep, redirect or consolidate. Runs the four-test sort (competition, AI search gap, blog-versus-blog duplication, and neither) with the protected-post override applied before any redirect. Consumes blog crawl, Search Console, analytics and backlink exports plus the approved commercial URL map. Produces recommendations only and halts for approval; never deletes and never implements."
---

# BB Blog Analysis — the Blog Decision Map

Classifies every post, produces the Blog Decision Map, and stops. Paul approves the map
before any content work begins.

**Never delete. Always redirect** (CM-001). Rules cited here live in
`methodology/rulings.md`.

## Required inputs

| Input | Required? | Without it |
|---|---|---|
| Full blog post list (URL, title, word count, category, modified) | **Yes** | Cannot run |
| Approved commercial URL map — service and location pages with their entity and city | **Yes** | Test A cannot run |
| Search Console — impressions, clicks, position, ≥6 months | No, but | Test B's impression/CTR signal is unavailable, and a redirect needs observed conflict from DataforSEO instead (CM-021, `serp_overlap`). Say so in the deliverable. |
| Analytics — conversions, entrances | No | Conversion signal unavailable |
| Backlink export — referring domains per URL | No | Equity signal unavailable |

The Brand Guide's C3 heading and FAQ registry is needed for the briefs that follow, not for
the classification itself.

## Run

```bash
python3 scripts/classify_blog.py <config.yaml> <out_dir>
```

Writes `blog-decision-map.csv` with a **proposed** classification per post, the signals
behind it, ranked Test A candidates, and a confidence flag.

**Nothing the script emits is a decision.** It does the joins and the arithmetic. Test B's
mandatory criterion — does this post answer a specific real question that *no* service or
location page covers — is a judgment, and the script cannot make it.

## The four tests

Read `references/tests.md` before classifying. Summary:

**Test A — competition.** Does the post target the same entity + location as a commercial
page? The script ranks candidate targets rather than picking one, because a location page
matches any post naming the city and the homepage matches almost everything. Choose the
target yourself.

**Test B — AI search gap** (CM-007). Mandatory criterion plus one supporting signal; passing
means PROTECTED. Details in `references/tests.md`.

**Test C — blog versus blog.** Near-duplicate subjects. Consolidate into the stronger post,
redirect the other. Matching uses only *distinctive* tokens — the site's category and city
appear in nearly every title and carry no duplication signal.

**Test D — neither.** Thin, stale, low value. The only category eligible for removal, and
even here redirect wherever a relevant target exists.

## The override that matters most

**Run Test B before executing Test A's redirect.** *(CM-007)*

A post sharing an entity with a service page may still be protected — the entity match is
not what makes it competing, covering the same *question* is. The script marks any post with
Test B supporting signals as `blocked-pending-test-B` and will not let it pass as a clean
redirect.

CM-007 is a Coastal PILOT override, not Bradley's rule — label it as ours in any client
deliverable. A redirect also needs observed conflict (CM-021, RULE-015).

## Classification output

Every post ends at exactly one of:

`COMPETING` (with the chosen redirect target) · `PROTECTED` (with which criterion and
signal qualified it) · `DUPLICATE` (with the consolidation winner) ·
`CONSOLIDATE-OR-REDIRECT`

**Zero posts left unclassified, and none classified on instinct.** Every row cites which
test it passed. `NEEDS-JUDGMENT` and `blocked-*` rows are unresolved, not classified — work
them before the map goes to Paul.

## Then stop

The Blog Decision Map goes to Paul. **The workflow halts until approved.** Content briefs
are generated from the approved map, not from the proposal.

Protected posts are re-tested on refresh per CM-007 (every 6 months).

## Boundary

Recommendations only. No redirects implemented, no content written, no posts removed. The
skill does not write the replacement content — that is the Blog agent, in a separate
session, from a brief built off the approved map.

## Files

- `references/tests.md` — the four tests in full, the override, and the traps
- `assets/blog-config-template.yaml` — input shape, with a worked example
- `scripts/classify_blog.py` — the mechanical pass
