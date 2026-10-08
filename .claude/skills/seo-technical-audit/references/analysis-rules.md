# Analysis Rules — Analysis Categories

Rules live in `methodology/rulings.md` (the single rule source) and the Bradley Standard;
this file cites their IDs and holds the procedure — what to look at and how — for each of
GOV-02's nine categories. Where this file and `rulings.md` disagree, `rulings.md` wins and
the disagreement goes in `decisions.md`.

## Contents
0. Conformance scorecards (page specs)
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

## 0. Conformance scorecards (page specs)

Every page in the frozen URL inventory is scored against its page spec in
`methodology/specs/<type>.md` — `homepage.md`, `service.md`, `location.md`,
`county-hub.md`, `about.md`, `blog-post.md`. Each spec has numbered checks (e.g. `SVC-01`),
and each check names the audit category it belongs to. Score every page against every
check of its type; a page with no matching spec gets its page type questioned under §5.

**One scorecard file per page type**, never one combined file — each type has its own check
set, so a combined sheet is mostly empty columns and hides which checks apply:

| Page type | File (in `inventories/`) | Spec | Check IDs |
|---|---|---|---|
| homepage | `scorecard-homepage.csv` | `homepage.md` | HP- + COM- |
| service | `scorecard-service.csv` | `service.md` | SVC- + COM- |
| location | `scorecard-location.csv` | `location.md` | LOC- + COM- |
| county hub | `scorecard-county.csv` | `county-hub.md` | HUB- + COM- |
| about | `scorecard-about.csv` | `about.md` | ABT- + COM- |
| blog post | `scorecard-blog.csv` | `blog-post.md` | BLG- |

COM- are the checks common to every commercial page (`methodology/specs/README.md`); blog
posts don't carry them. Each file: columns `page_url`, `page_type`, then one column per check
ID — the spec's own in spec order, then COM-. One row per page of that type. Each cell is `pass`, `fail F-###` (the finding that
carries it), `N/A (<reason>)` or `not scored — <reason>`. A type with no pages on the site
still gets its file, header only, so the reviewer can see it was considered. Every page in the
URL Decision Map with one of these types appears in exactly one scorecard.

Scorecard results are reported inside the nine categories, not as a separate section:

| Spec checks | Category |
|---|---|
| Page type, URL, hub structure | §5 Architecture |
| Title, H1, headings, opening, body, FAQ, on-page link structure | §6 On-page |
| `blog-post.md` checks | §7 Blog |
| Entity / NAP | §3 Brand and entity |
| Schema readiness | §9 Schema readiness |

Severity per CM-028: a failed spec check is **Medium** unless it breaks the entity model or
page structure (**High**). One finding per failed check, listing every page that fails it
(not one finding per page). A missing "The Best" is never a failed check by itself
(CM-020).

## 1. Baseline and measurement

Record a baseline only where the source and window are both defined. An undefined
window is not a baseline, it is a number.

Annotate confounders explicitly: seasonality, tracking changes, outages, migrations,
campaigns. A year-over-year change spanning a redesign is not evidence of anything until
the redesign is accounted for.

Validate the conversion path end to end — event firing, form delivery, phone routing,
call attribution, thank-you pages, CRM handoff, duplicate-event risk. Record broken
measurement as a finding in its own right (severity per CM-028), because it makes every
other performance-based finding unsafe.

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

**`site:` results** — CM-008 / RULE-012. Measure indexation from Search Console Page
Indexing, URL Inspection samples, sitemaps, crawl evidence, logs and performance data.

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

Entity / NAP spec checks are reported here (§0).

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
follow CM-001 and CM-019: a page is a candidate only when all four CM-019 conditions hold;
otherwise it is `Needs Evidence`. Never delete, always redirect (CM-001). Entity overlap,
template similarity, word count, index status or a tool score never qualify a page on
their own (RULE-007, CM-009). How: pull DataforSEO ranked keywords and referring domains
for the URL, check it against GBP and citation destinations, and list the "no leads"
question for client confirmation. Record the check in the URL Decision Map with a safer
alternative. Where the client has supplied performance data, record it too (CM-030 is
OPEN).

**Cannibalization** — RULE-005, RULE-015, CM-021. Look for overlapping intent, then for
observed evidence: GSC query/URL data, or DataforSEO showing both URLs ranking for the same
query.

City pages vs county/region hubs is decided on verified geography, service operations,
user intent, query evidence, internal-link usability and maintenance capacity.
Geographic subdomains: RULE-008 (deferred — do not recommend).

Page-type, URL and hub-structure spec checks are reported here (§0).

## 6. On-page and content structure

Audit titles, H1s, heading structure, opening paragraphs, internal anchors, conversion
paths, duplication, claims, helpfulness and page focus.

Title, H1, heading, opening, body, FAQ and on-page link-structure spec checks are
reported here (§0).

**One H1 per page** — RULE-002 (house standard, not platform requirement).

The bot/human split: URLs, titles, headings and internal anchors express structure;
paragraph prose serves the buyer; the H1 must work for both. Openings: CM-003. Uniqueness:
CM-015. Headings should read as conversational and useful, not machine-generated.

**Titles and H1s** — BB-302, BB-304, BB-305 (classified Bradley Methodology Rule, never
Platform Requirement) and CM-020 for "The Best". Separator: CM-014. To apply CM-020, pull
the DataforSEO data its conditions name and the page's current rank, and record the
decision where CM-020 says.

Any superlative or credential claim found on-page is a **truth** issue before it is an
SEO issue. Route it to the client-confirmation list rather than optimizing
around it.

## 7. Blog and supporting content

Inventory posts against intent, target entity, linked commercial page, performance,
conversions and assists, backlinks, freshness, expertise source and overlap.

Classify: Keep, Improve, Consolidate Candidate, Relocate Candidate, Noindex Candidate,
Remove Candidate, Needs Evidence. Recommendation only — no action status is final before
Client confirmation.

**Do not assume blogging harms local SEO**, and do not assume a subdomain is safer.
Either claim requires observed conflict, a business purpose and migration risk analysis.
Blog classification and protected posts: CM-007, CM-021 (run by `bb-blog-analysis`).

`blog-post.md` spec checks are reported here (§0).

Flag expert-interview opportunities and AI-search gaps for the content step rather than
resolving them here.

## 8. Citations, backlinks, authority

Verify NAPW accuracy, duplicates, ownership, provider and renewal dependencies, location
separation, relevance, indexability, competitor context.

A citation tracker's discrepancy list is measured against **the tracker's stored NAP**,
which is not automatically the verified NAP. Reconcile against the intake record (Client Control Record) before calling any of it an error.

**Citation and link quantity** — CM-006, RULE-004. Spend — RULE-014.

No citation order occurs during the audit (RULE-009). The recommendation states verified
NAPW, target location, provider options, cost and renewal, prerequisites, and the approval
required.

Assess anchors, topical relevance, destination distribution, referring-domain quality,
risk, historical patterns and comparable competitors. Link quantity alone establishes
neither need nor quality. Do not prescribe press-release cadence, link packages or spend
as a rule — present options with evidence, expected role, risk and the approval gate.

## 9. Schema readiness — recommendation only

Inventory existing structured data, ownership and plugins, errors, entity IDs, page-type
fit, duplicate or disconnected instances, URL dependencies.

**Generate nothing.** No JSON-LD, no drafted markup, no code. Schema work is recommended
only after page types, canonical URLs, organization/location relationships and content
are approved and stable — all of which sit beyond this skill's boundary. Schema-readiness
spec checks are reported here (§0); the schema rules are BB-6xx v1.1 (incl. GOV-T5).

**Duplicate schema (wordpress-site-setup.md §8).** If SEOPress outputs its own site-wide schema
(Knowledge Graph — Organization/Person; seen in the crawl's JSON-LD or the S20 settings evidence) that
overlaps the hand-built schema, write it as a finding (one finding, every affected URL); turning it off
is a VA handoff. SEOPress title templates, sitemap configuration and noindexed post types from S20 are
evidence for §2 and §6 findings, never changed by the system.
