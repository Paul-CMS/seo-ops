---
name: updated-link-strategy
description: Hardened internal linking system for local service sites. Runs a full existing-site link audit from a Screaming Frog crawl export (complete sitemap inventory, status-code checking, empty and weak anchor detection, orphans, cannibalization clustering, off-entity content) and qualifies every proposed link against a four-part test — named relation, question raised, relation asserted on both ends, distributed placement. Includes the four-layer entity model (organization, service, place, attribute), per-page-type link contracts, anchor city selection, the standard for content additions written to support a link, and the five-document deliverable pack. Use for link audits, internal linking plans, anchor text distribution, and topic cluster builds. Supersedes the older link-strategy skill.
plugin: seo
updated: 2026-09-14T00:00:00.000Z
metadata:
  mcpmarket-version: 1.1.0
---
plugin: seo
updated: 2026-09-14

# Link Strategy

## When to Use

- Planning internal linking structure
- Optimizing anchor text
- Building topic clusters
- Improving site architecture

## Internal Linking Principles

### 1. Link from High to Low Authority
- Homepage -> Category Pages -> Individual Posts
- Old established pages -> New pages
- High-traffic pages -> Pages you want to rank

### 2. Use Descriptive Anchor Text
- Good: "SEO keyword research guide"
- Bad: "click here", "read more"
- Include target keyword naturally

### 3. Link Contextually
- Links within body content > Navigation links
- Relevant context around link
- Natural reading flow

### 4. Maintain Reasonable Link Count
- 3-5 internal links per 1000 words
- Avoid excessive linking (100+ links)
- Focus on most relevant pages
- Volume belongs on the attribute layer (blog/question pages), not on money pages.
  A service page with 15 body links reads as a link farm; 40 posts each carrying
  3 well-formed links do the same job.

### 5. Every Link Must Name a Relation
Keyword proximity is not a reason to link. See the four-part test below.

## Topic Cluster Model

```
PILLAR PAGE: "Content Marketing" (broad, high volume)
    |
    +-- Supporting Article: "Content Marketing Strategy"
    |   (links to and from pillar)
    |
    +-- Supporting Article: "Content Marketing Examples"
    |   (links to and from pillar)
    |
    +-- Supporting Article: "Content Marketing Tools"
        (links to and from pillar)
```

**Benefits:**
- Establishes topical authority
- Passes PageRank efficiently
- Improves user navigation
- Signals content relationships

### Entity Layers (local service sites)

For a local service business, model the site as four layers before planning any links:

| Layer | Pages | Role |
|---|---|---|
| Organization | Home, About, Contact | The business entity: name, principals, locations, licensing, policies |
| Service | Category hubs + service pages | The commercial targets. Sparse, high-quality linking only |
| Place | Location/city pages | Local relevance. Designate 1-2 anchor cities; secondaries link up to them rather than meshing |
| Attribute | Blog / question pages | Question-level nodes. This is where link volume belongs |

Avoid flat meshes on the place layer (every city linking to every other city).
A mesh asserts that all markets are equally important, which is never true.

### Anchor City Selection

Designate one or two anchor locations. Basis, in order: depth of existing
content, market weight, and physical location of the business. Secondary
locations link up to the nearer anchor instead of meshing.

State the basis for each assignment and flag any that turn on a judgement call
the client should confirm. Geographic adjacency alone is not sufficient — a
mainland location whose conditions match the coastal group belongs with the
coastal group, and only the client knows whether that holds.

## Link Contracts by Page Type

| Page type | Body links | Contract |
|---|---|---|
| Service page | 4-5 | Up to its pillar once. 2-3 siblings where a relation exists. 1 anchor city where evidenced |
| Category hub | all children + 2 | Linked headings to every child (structural, exempt from distribution). Plus <=2 contextual links |
| Anchor location page | services + 2-4 | Service list stays. Plus links to location-qualified attribute pages |
| Secondary location page | services + 1 | One link up to the nearer anchor location. No sibling mesh |
| Blog / attribute page | 3 | One up to its service parent. One to its location if qualified. One sibling. No more |

The contract is a ceiling, not a target. The derived template shape overrides it
downward — see *Derive the template shape* below.

## Anchor Text Optimization

### Anchor Text Types

| Type | Example | When to Use |
|------|---------|-------------|
| Exact Match | "SEO tools" | Sparingly (1-2x per page) |
| Partial Match | "best SEO tools for startups" | Primary usage |
| Branded | "SEMrush" | Brand mentions |
| Generic | "click here" | Avoid if possible |
| Naked URL | "https://example.com" | Occasional |

### Best Practices
- Vary anchor text naturally
- Use target keyword in some anchors
- Avoid over-optimization (100% exact match)
- Make text descriptive and clickable
- Exact match is correct for hub-to-child structural links (the relationship is
  structural, not editorial). Everywhere else, anchor the entity or the relation,
  not the page title.
- No anchor repeats twice on the same page.

## Required Inputs

Do not start an audit without these. Ask for whatever is missing.

1. **Screaming Frog crawl export (CSV)** — every URL, internal HTML only.
   Required columns: `Address`, `Status Code`, `Indexability`, `Title 1`,
   `Meta Description 1`, `H1-1`, `H1-2`, `H2-1` through `H2-5`, `Word Count`,
   `Canonical Link Element 1`, `Inlinks`, `Outlinks`, `Redirect URL`.
2. **All sitemaps**, including post/blog sitemaps.
3. **Decisions log** from prior runs on this client — logged deviations from the
   literal SOP, settled scope questions, anchor market rulings. Without it every
   audit re-argues questions that were already closed.
4. **Business scope** — MSA, service area, which markets are real.

> Rule: The crawl export is the audit source. Page fetches are the exception, not the method. An audit that fetches 30 pages has been run wrong.

### What the export answers, and what it cannot

Parse the export with pandas. This is near-free and gives 100% coverage, where
fetching gives 10% coverage at 100x the cost.

**From the export alone, on every URL:**

- Status codes, redirect chains, 404s, redirect hops on internal links
- Orphans (`Inlinks` = 0), thin pages, outlier word counts where copy is
  truncated or duplicated
- Missing H1, multiple H1s, duplicate H1s or titles across pages
- Heading-order breaks
- **City token in H1 absent from any H2, or an H2 carrying a different city's
  token than the H1** — the per-page data-entry error class that sampling is
  structurally incapable of finding
- Service token mismatches between title, H1 and H2s
- Identical H2 strings appearing on more than one URL — catches duplicated FAQ
  blocks across money pages by rule rather than by luck
- Cannibalisation clustering, by grouping titles and H1s by the question they
  answer
- Off-entity URLs, by scope keyword against the business scope

**Only a page fetch answers:**

- Whether a sentence actually raises the question a link would answer
- Whether the destination asserts the relation (test 3)
- Anchor text on specific links, and which H2 block a link sits in
- Whether prose is broken, contradictory, or factually wrong

**Neither answers** — state this plainly in findings rather than implying
coverage that does not exist: prose quality across the whole site. The export
flags which pages to read; it does not read them.

### Fetch Budget

Target 10–14 fetches for a whole audit. Allocate them:

- One page per template type, to derive the template shape
- Every page the export flagged as anomalous
- Destinations needed for test 3 on the pages being planned

> Stop: After each batch of four or five fetches, write findings to a file. Do not hold them in context to the end. This is the failure that loses a whole audit at 80% context.

**Operational note:** `web_fetch` drops URLs from its allowlist after a few
calls. Re-fetch the sitemap to re-register them, then continue. Budget for this
rather than burning calls on rejections.

### Derive the template shape before writing any plan

Counting H2 blocks on two or three pages of a type gives the real link ceiling
for that page type under the distributed-placement rule, and it overrides the
general contract. A three-H2 service template caps at three contextual links
regardless of word count. Writing a five-link plan against it produces a plan the
executor must silently deviate from.

## Link Audit Process

### 0. Establish the real page inventory
- Pull **every** sitemap, including post/blog sitemaps, not just the page sitemap.
- Live, indexable pages missing from a sitemap are a common finding. Test suspected
  legacy hub URLs directly rather than assuming the sitemap is complete.
- Reconcile the sitemaps against the crawl export. URLs in one and not the other
  are a finding in themselves.
- Note the generator/template fingerprint per page. A page rendering an older
  navigation or plugin version than the rest of the site is a stale cache or a
  legacy template, not a content problem — diagnose that before anything else.

### 1. Inventory existing links
- The inventory comes from the **export**, on every URL. Fetch one page of each
  **type** (home, category hub, service page, location page, blog post) only to
  derive the template shape and to read anchor text as rendered. Link problems on
  templated sites are usually template-level, so confirm each template-level
  finding on two page types before calling it sitewide — but per-page data-entry
  errors are not template-level, and only the export finds those.
- Separate boilerplate links (header/footer nav) from body links and count both.
  Duplicated header + footer menus are common and mean body links are heavily
  outnumbered — which raises the value of contextual linking, not lowers it.
- Record anchor text exactly as rendered.

### 2. Find broken and non-canonical links
- Check **status codes**, not just whether a URL resolves. WordPress guesses a
  destination for 404s, so a link can appear to work while pointing at a dead URL
  with no redirect rule behind it. Confirm 301 vs 302 vs 404-fallback.
- Look for malformed hrefs: `http://pagename`, bare `#`, dropdown parents pointing
  at the homepage, absolute URLs to a staging domain.
- Look for **legacy URL patterns** from a previous site structure. These usually
  live in one reusable block, so a single edit fixes every page that uses it —
  confirm whether it is one block or duplicated per page before scoping the task.
- Flag cross-domain hotlinked assets (images loaded from another client's site) and
  phone numbers hrefed to search-result URLs instead of `tel:`.

### 3. Find empty and weak anchors
- Card and button links frequently render with **no anchor text at all** (icon-only
  or empty `<a>`). Hub-to-child links are the most common victims and the most
  costly, because the hub then passes no context to the money pages. This is
  invisible in a visual review — check the markup.
- Then: generic anchors, repeated anchors, anchors that are page titles.

### 4. Identify orphans and cannibalization
- Orphans: pages reachable only from the sitemap or only from the nav.
- Cannibalization: cluster pages by **the question they answer**, not by keyword.
  Several posts answering one question compete with each other and with the money
  page. On older sites, expect 4-6 posts stacked on the primary service intent.
- Where a generic page and a location-qualified page answer the same question, the
  location-qualified one is canonical and the generic merges into it.
- Flag **off-entity** content: pages asserting relations that contradict the
  business entity. DIY instructions on a contractor site, posts promoting products
  the business does not sell, trade/business-startup content aimed at competitors,
  content scoped to a market the business does not serve. These are structural
  conflicts, not tone problems.
- Triage built from slugs and titles is a hypothesis. Confirm intent overlap
  before any redirect fires. Where the number of merge candidates exceeds the
  fetch budget, confirm the highest-impact merges by fetch and ship the rest as
  proposed-pending-confirmation rather than as decided.

### 5. Qualify every proposed link (four-part test)
A link ships only when all four are true:
1. **It names a relation** — one of: is-a-component-of, is-an-alternative-to,
   is-a-prerequisite-for, remedies, is-caused-by, is-constrained-by, is-located-in.
   If you cannot name which, the link is decoration.
2. **The destination is the canonical answer to a question the sentence raises.**
   No question in the text, no link.
3. **The relation is asserted on both ends.** If the destination never discusses the
   source entity, the link is one-sided — drop it, or extend the destination first.
   This is the test that gets skipped under time pressure. Do not waive it.
4. **Placement is distributed.** One link per H2 block maximum, never two
   consecutive paragraphs, none in the closing CTA band. Three links to three
   sibling pages inside one section is the same relation firing three times.

### 6. Content additions to support a link
Only where test 3 fails and the relation is genuinely real. The addition is judged
on its own merits, not on the link it enables:
- It serves the **stated intent of the section** it lands in, not a parallel one.
- It follows from the paragraph before it and sets up the paragraph after it.
- Removing the link entirely still leaves the section reading better than before.
  If not, the addition is a pretext and does not ship.
- Write the argument up and get client approval before publishing.

Say so explicitly when a page needs **no** addition because the relation is already
asserted. Restraint is part of the standard.

### 7. Build the clusters
- Group by entity layer first, then by relation.
- Verify no remaining links point at merged or redirected URLs.

## Item Refs

Number every actionable item as it is written. The worksheet and the QA pass
join on this; without it there is no verification chain.

`FIX-{n}` technical · `LINK-{PAGE}-{n}` internal link · `CITY-{SLUG}` location
page · `BLOG-M{n}` merge · `BLOG-OE{n}` off-entity · `CONTENT-{n}` addition

Refs are assigned once and never renumbered between runs.

## Deliverable Set

Five documents, not six. Findings fold into the workbook; a separate findings doc
gets superseded before anyone reads it.

| # | Document | Role |
|---|---|---|
| 00 | Read First — Linking Standards | The rules |
| 01 | Technical Fixes | Site edits, independent of 02 and 03 |
| 02 | Internal Linking Workbook | Findings, evidence catalogue, link plans |
| 03 | Content/Blog Consolidation | Merges, removals, content additions |
| 04 | Execution & Completion Protocol | How to run the pack, what to hand back |
| 04a | Completion Worksheet (CSV) | Pre-filled, executor fills two columns |

**Write every document as markdown, then convert:**

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/md-to-docx.js 02-workbook.md 02-workbook.docx
```

> Rule: Never write a bespoke build script per document. Markdown supports headings, pipe tables, bullets, numbered lists, `> Note:` and `> Stop:` callouts, `===` page breaks, and inline bold/italic/code. That covers every deliverable produced so far.

Do not render to PDF or view page images to check formatting. The converter was
verified once. Rendering per document costs more than the document.

Filenames: common client prefix, numbered, no individual's name.

## Output Format

The per-page plan format inside document 02:

```markdown
## Internal Linking Plan

### Target Page: {url}
**Target Keyword**: {keyword}
**Entity layer**: {organization | service | place | attribute}

### Linking Opportunities

1. **Ref**: LINK-{PAGE}-{n}
   **From**: {source_page}
   - **Anchor**: {anchor_text}
   - **Section**: {which H2 block — check distribution}
   - **Relation**: {is-a-component-of | is-an-alternative-to | ...}
   - **Evidence on destination**: {the sentence on the destination page that
     asserts the relation — or FAILS, needs content addition}
   - **Priority**: HIGH/MEDIUM/LOW

### Links Considered and Rejected
- {link} — {which of the four tests it failed}

### Content Additions Required
- **Ref**: CONTENT-{n}
- **Page/section**: {where}
- **Section intent**: {what the section is for}
- **Before / after**: {what it follows from, what it sets up}
- **Argument**: {why the section is better with it, link aside}

### Topic Cluster Structure

PILLAR: {main_topic_page}
- Supporting: {page1}
- Supporting: {page2}
- Supporting: {page3}
```

## Phase Boundaries

- **Phase A — audit.** Export parse, fetch budget, findings. Ends with the
  findings written to file.
- **Phase B — plan and pack.** New chat on a large site. Inputs: the findings
  file and the export. Does not re-crawl.
- **Phase C — verification.** New chat, weeks later. Hands off to
  **link-implementation-qa**.

Say at the start of Phase A whether A and B will fit in one chat. On a site over
roughly 60 URLs they will not.

## Deviation Feedback Loop

When the QA pass rules a deviation was correct and the spec was wrong, correct
the spec and the decisions log in the same pass. Otherwise the next run reissues
the same bad instruction. Accepted deviations are spec bugs, not executor errors.

## Documentation Discipline (for the operator)

- Upload client-specific inputs only: export, sitemaps, decisions log. The method
  is in the skill; re-uploading reference SOPs costs tokens to restate what is
  already loaded.
- Never upload credential files. Config and token files carry live secrets.
- Keep the decisions log as one short running file per client.
