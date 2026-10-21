# Analysis Rules — what to look at, per category

Rules live in `methodology/rulings.md`; this file cites their IDs and says what to look at. Where they disagree,
`rulings.md` wins and the disagreement goes in `decisions.md`. Severity for every finding: `finding-standard.md`.

## 0. Page conformance is triage (CM-063)

No scorecards. `conformance.py triage` writes `rebuild / light fix / keep` in the URL Decision Map. Pages Build
rewrites are never spec-scored. The pages it will not rewrite — blog posts, kept utility pages, Route B pages, the
homepage under HP-08 — are scored in full (auto checks + `conformance.py judge`); each failed check is one finding
(Fix and list) listing every page that fails it, placed in its category below.

## 1. Baseline and measurement

A baseline only where source and window are both defined. Name confounders (seasonality, tracking changes,
migrations). Validate the conversion path end to end (form delivery, call routing, thank-you pages); broken
measurement is its own finding. Unknown metrics stay unknown — never reason from a proxy.

## 2. Technical and crawl

Response codes incl. soft 404, redirect chains and loops, host consistency (`crosscheck.py`), canonicals, robots,
sitemaps, duplicate URLs, crawl depth, internal link distribution. Empty rendered columns mean rendering was off — a
limitation, not a defect. Indexation from Search Console and crawl evidence, never `site:` (CM-008). Orphan candidates
need reconciliation (crawl, sitemap, GSC, backlinks, GBP, citations), never the crawl alone. Most technical findings are
**Fix** rows: they become the Technical Blocker Checklist.

## 3. Brand, entity and verified truth

Does the site consistently say who the business is, what it provides and where (the semantic triple against the
Brand Guide)? NAP on every page against Section A. Branded SERP checks are samples: record query, place, device, date.
An entity interpretation not directly evidenced is a Working Hypothesis. A superlative or credential claim on the live
site is a truth issue first: kind-2 Ask (legal or money) or kind-3 (client fact).

## 4. GBP and local visibility

Profile identity, name, address visibility, phone, website destination, hours, categories, service areas, reviews.
Never manufacture uniqueness between locations. Grid runs record query, centre, grid size, spacing, date
(`local-grid-summary.md`). Posting cadence is methodology, never a platform guarantee.

## 5. Architecture, services, locations, page types

Every URL typed with its entity, intent and role; absent page classes recorded as `N/A`. A new page needs a distinct
intent, truthful relevance, unique content, business value and an architecture role (CM-001: construction needs no
evidence threshold). **Destructive recommendations** follow CM-019 through the screen (`redirect-screen.md`): a `fail`
URL stays live; you decide only `needs evidence` rows and entity mismatches. Entity overlap, template similarity, word
count or a tool score never qualify a page alone (RULE-007, CM-009). Cannibalization needs observed evidence (RULE-005,
RULE-015, CM-021). City pages vs hubs: verified geography and intent (CM-058). Geographic subdomains: RULE-008
(deferred — never recommend).

## 6. On-page and content structure

Titles, H1s, headings, openings, internal anchors, conversion paths, claims. One H1 (RULE-002, house standard). Titles
and H1s: BB-302/304/305 and CM-020 ("The Best"); separator CM-014; scored against the settled Decision Sheet formats,
never re-decided. On a page Build rebuilds these are one Fix-and-list row ("the rebuild sets it"), not a finding per
check.

## 7. Blog and supporting content

Inventory posts against intent, target entity, linked commercial page, performance and overlap. Disposition belongs
to the Blog Decision Map (`bb-blog-analysis`, CM-007, CM-021): in the audit a blog post is `Keep — disposition in Blog
Decision Map` unless it fails the screen's evidence for a redirect anyway. Never assume blogging harms local SEO.

## 8. Citations, backlinks, authority

NAPW accuracy against the Brand Guide, not the tracker's stored NAP. Quantity: CM-006, RULE-004; spend: RULE-014. No
citation order in the audit (RULE-009) — a citation correction is a Fix row for Gwen. Links: quality, relevance and
destination, never quantity alone.

## 9. Schema readiness — recommendation only

Inventory existing structured data and plugins (SEOPress Knowledge Graph overlap: one Fix row, turning it off is a VA
handoff). Generate nothing — schema comes in Finish (BB-6xx v1.1).
