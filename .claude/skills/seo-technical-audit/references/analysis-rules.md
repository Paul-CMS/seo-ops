# Analysis Rules — Stage 1 Categories

The methodology and guidelines file in the client drive governs. This file holds the
constraints that a model gets wrong by default, drawn from GOV-02 §1–9. Where the two
disagree, the client's methodology file wins and the disagreement goes in `decisions.md`.

## Contents
1. Baseline and measurement
2. Technical and crawl
3. Brand, entity and verified truth
4. GBP and local visibility
5. Architecture, services, locations, page types
6. On-page and content structure
7. Blog and supporting content
8. Citations, backlinks, authority
9. Schema readiness

---

## 1. Baseline and measurement

Record a baseline only where the source and window are both defined. An undefined
window is not a baseline, it is a number.

Annotate confounders explicitly: seasonality, tracking changes, outages, migrations,
campaigns. A year-over-year change spanning a redesign is not evidence of anything until
the redesign is accounted for.

Validate the conversion path end to end — event firing, form delivery, phone routing,
call attribution, thank-you pages, CRM handoff, duplicate-event risk. Broken measurement
is usually a High finding in its own right, because it makes every other
performance-based finding unsafe.

**Unknown metrics stay unknown.** Do not construct a proxy and then reason from it as
though it were measured.

## 2. Technical and crawl

Crawl-first baseline with Googlebot Smartphone unless a documented case requires
otherwise. Record user agent, rendering mode, robots behaviour, authentication, crawl
limits and exclusions — an export whose configuration is unknown cannot support a
finding about what Google sees.

Standard sweep: response codes including soft 404, redirect chains and loops, HTTP/HTTPS
and host consistency, canonicals, robots directives, XML sitemaps, hreflang, pagination,
parameters and facets, duplicate URLs, crawl depth, internal link distribution.

**Rendering.** Compare raw vs rendered where JS may affect primary content, links,
canonicals, metadata, structured data, forms or consent layers. If the rendered columns
in an export are systematically empty, rendering was **disabled** — that is a limitation,
not evidence that content disappears on render. This distinction has produced real false
findings; treat it as a trap, not a nicety.

**`site:` results are directional discovery only.** Never calculate an indexation rate
from the reported count. Use Search Console Page Indexing, URL Inspection samples,
sitemaps, crawl evidence, logs and performance data.

**Orphan candidates require reconciliation**, not a crawl. Cross-reference crawl, XML
sitemaps, Search Console, analytics, backlinks, GBP destinations, citations, paid
campaigns and the client URL inventory. A crawl alone cannot prove a URL has no value.
Where an auditing tool emits its own orphan list, treat it as a claim to be verified
against a link-level export with host, protocol and trailing-slash normalization applied
first — see `reconciliation.md`.

## 3. Brand, entity and verified truth

Branded SERP observation is a **sample** taken from a stated geography and device, not a
universal knowledge-graph score. Record query, location, device, date.

Inventory first-party and external supporting assets; verify each references the correct
business and location and is actually discoverable.

Apply the methodology file's entity-association reasoning to test whether the site
consistently expresses who the business is, what it provides and where it operates.
Every entity interpretation that is not directly evidenced is a Working Hypothesis and
must be labelled.

## 4. GBP and local visibility

Verify profile identity, ownership and management access, eligibility, name, address
visibility, phone, website destination, hours, categories, services, service areas,
attributes, photos, reviews, responses, posts.

Multi-location: each profile needs unique and truthful data and an appropriate landing
page. **Do not manufacture uniqueness** — invented differentiation between locations is
a misrepresentation risk, not an optimization.

Grid runs record query, center, grid size, node spacing, date and device. Minimum set:
a primary-category query, a high-value non-category service query, and a
high-urgency/proximity query where relevant. A grid without recorded parameters is not
reproducible and cannot support a finding.

Competitor selection is by actual query and geography visibility with a comparable
business model. Directories, national retailers and outliers may be included only when
labelled as such.

GBP posting cadence and CTA choice are methodology recommendations. Never present them
as platform guarantees.

## 5. Architecture, services, locations, page types

Build a complete URL inventory with page type, intended entity, search intent, business
purpose, conversion role, location relationship, parent/child relationship and current
performance evidence. Record `N/A` for absent page classes rather than omitting them —
a silently missing class reads as "checked and fine".

**A new page recommendation requires all of:** distinct user/search intent, truthful
service or location relevance, useful unique content, business value, and an
architecture role. Search volume is evidence, not the decision.

Entity references (Wikipedia, Wikidata) are supporting research, not a page-existence
test. A distinct entity does not require a page; absence from Wikipedia does not
prohibit one.

**Destructive recommendations** — merge, redirect, delete, noindex, canonical change —
may never rest on entity overlap, template similarity, word count, index status or a low
tool score. Before proposing any, complete the value/dependency check: organic traffic,
queries, conversions, leads, revenue, backlinks, paid use, GBP and citation
dependencies, and client job history. Record the check in the URL Decision Map and offer
a safer alternative.

**Cannibalization** requires overlapping intent **plus** observed evidence: unstable
ranking URLs, split impressions or clicks, competing conversions, or query-level
conflict. Entity overlap alone is insufficient and is the most common false positive in
this category.

City pages vs county/region hubs is decided on verified geography, service operations,
user intent, query evidence, internal-link usability and maintenance capacity.
Geographic subdomains are exceptional experiments requiring alternatives, success
measures, risk review, ownership and rollback — never a default recommendation.

## 6. On-page and content structure

Audit titles, H1s, heading structure, opening paragraphs, internal anchors, conversion
paths, duplication, claims, helpfulness and page focus.

**One H1 per visible page is a house standard**, not a platform requirement. Say so in
the deliverable.

The bot/human split: URLs, titles, headings and internal anchors express structure;
paragraph prose serves the buyer; the H1 must work for both. Rewrites call for a BLUF
opening and human-first copy. Headings should read as conversational and useful, not
machine-generated.

**Do not** require "the best" in a title or H1, exclude the brand from every H1, or
impose a title/H1 formula as a universal rule. Recommend the strongest truthful variant
for that page and state the tradeoff.

Any superlative or credential claim found on-page is a **truth** issue before it is an
SEO issue. Route it to the Stage 3 client-confirmation list rather than optimizing
around it.

## 7. Blog and supporting content

Inventory posts against intent, target entity, linked commercial page, performance,
conversions and assists, backlinks, freshness, expertise source and overlap.

Classify: Keep, Improve, Consolidate Candidate, Relocate Candidate, Noindex Candidate,
Remove Candidate, Needs Evidence. Recommendation only — no action status is final before
Stage 3.

**Do not assume blogging harms local SEO**, and do not assume a subdomain is safer.
Either claim requires observed conflict, a business purpose and migration risk analysis.

Flag expert-interview opportunities and AI-search gaps for the content SOP rather than
resolving them here.

## 8. Citations, backlinks, authority

Verify NAPW accuracy, duplicates, ownership, provider and renewal dependencies, location
separation, relevance, indexability, competitor context.

A citation tracker's discrepancy list is measured against **the tracker's stored NAP**,
which is not automatically the verified NAP. Reconcile against the Stage 0 Client
Control Record before calling any of it an error.

**100+ citations is the methodology's planning benchmark, not a Google threshold.**
Recommend quantity only after accuracy, relevance, competition, cost and maintenance.

No citation order occurs during the audit. The recommendation states verified NAPW,
target location, provider options, cost and renewal, prerequisites, and the approval
required. First order belongs to Stage 4, after discrepancies are resolved.

Assess anchors, topical relevance, destination distribution, referring-domain quality,
risk, historical patterns and comparable competitors. Link quantity alone establishes
neither need nor quality. Do not prescribe press-release cadence, link packages or spend
as a rule — present options with evidence, expected role, risk and the approval gate.

## 9. Schema readiness — recommendation only

Inventory existing structured data, ownership and plugins, errors, entity IDs, page-type
fit, duplicate or disconnected instances, URL dependencies.

**Generate nothing.** No JSON-LD, no drafted markup, no code. Schema work is recommended
only after page types, canonical URLs, organization/location relationships and content
are approved and stable — all of which sit beyond this skill's boundary.
