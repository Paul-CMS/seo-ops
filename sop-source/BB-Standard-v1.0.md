# THE BRADLEY STANDARD
### Every rule in the Bradley Benner / Semantic Links methodology, with its reasoning and its evidence grade
**Coastal Marketing Strategies · v1.0 · APPROVED (Paul, 2026-10-02) · Provenance-graded**

---

## How to read this document

This contains **only Bradley's methodology**. Nothing Coastal adds, extends, overrides or
exempts itself from appears here — that is the Coastal Delta, a separate file. If you are
looking for "The Best" test status, the BLUF layer, the E-E-A-T layer or the AI Search Gap
protection, they are in the Delta, because they are ours.

Every rule has a **stable ID**. Cite the ID, never the prose. SOPs reference IDs; this
document holds the rules.

### Evidence grades — read this before trusting any rule

The two documents most of the system treats as "Bradley's source documents" — the *Local
SEO Analysis System Prompt* and the *Website Build & SEO SOP* — **are not Bradley's
writing.** Each says so in its own text:

> *"…as derived from full SEO audit videos, entity analysis videos, semantic triple
> transcripts, geographic hierarchy transcripts, AI SEO transcripts, location page
> transcripts, GBP posts transcripts, press release transcripts, subdomain strategy
> transcripts, and live implementation analysis…"*

> *"Generalized from full methodology"*

They are syntheses of Bradley's videos, made by someone else. That makes them **P2
Derived**, the same tier as this document — not P1 Primary. Four governing SOPs currently
cite them as primary sources, which inflates their authority by one level.

It also means most of the underlying transcripts are **not in the brain**: the semantic
triple, geographic hierarchy, AI SEO, location page, GBP posts, press release and
subdomain transcripts are all referenced and none are held.

So each rule carries a grade:

| Grade | Meaning | Use |
|---|---|---|
| **A** | Traceable to a transcript we hold. Quotable. | Cite freely |
| **B** | In both derived documents, mutually consistent, original source not held | Use as methodology; do not quote Bradley directly |
| **C** | In one derived document only. Cannot be verified against anything | Use with the grade stated. Do not present as confirmed |
| **D** | Contested, superseded, or contradicted by evidence or platform rule | See the Delta before applying |

**Grade C is not a reason to discard a rule.** It is a reason to say so out loud when a
client asks why, and to put it first in the queue when transcripts surface.

Sources in force: `T-ENT` entity analysis transcript · `T-ONP` website on-page transcript ·
`T-GBP` GBP on-page transcript · `T-LNK` competitive link analysis transcript ·
`D-SYS` system prompt (derived) · `D-SOP` website build SOP (derived) ·
`X-###` applied audit example.

---

# BB-1xx · ENTITY AND AREA RESEARCH

### BB-101 · The two pillars
**RULE** Local search performance rests on two things: **Branded Location Authority** (how
well the knowledge graph understands who the business is, what it does, where it does it)
and **Site Efficiency** (achieving every entity association with the fewest pages and no
redundancy). Diagnose every underperforming campaign against these two first.
**CLASS** Framework · **GRADE** A · **SOURCE** T-ENT, T-ONP, D-SYS
**WHY** A weak entity must be overcompensated for everywhere else; a strong one tolerates
deficiencies elsewhere. This is why entity work sequences before everything.

### BB-102 · Entity work comes first
**RULE** Complete entity and area research before any build, rewrite or recommendation.
**CLASS** Sequencing rule · **GRADE** A · **SOURCE** T-ENT, D-SYS, D-SOP
**WHY** Every downstream element — titles, H1s, schema, citations — encodes the area
entity. Getting it wrong late means redoing all of them.

### BB-103 · The core diagnosis
**RULE** A failing local campaign almost always makes inaccurate, inconsistent or
conflicting statements about who the business is, what it does, and where it does it.
Models verify these against Wikipedia entities, the knowledge graph and external
citations. Inconsistency produces suppression.
**CLASS** Framework · **GRADE** B · **SOURCE** D-SYS
**WHY** Treats search engines and LLMs as entity-resolution systems, not keyword matchers.

### BB-104 · Two knowledge graph levels
**RULE** A local business has an overall **brand** knowledge graph (location-neutral —
who they are, what they do), influenced through `Organization` schema or a subtype; and a
separate **branded location** knowledge graph per physical location (adds where),
influenced through `LocalBusiness` or its most specific subtype.
**CLASS** Model · **GRADE** A · **SOURCE** T-ENT
**WHY** Explains why a multi-location brand can be strong overall and weak at one
location, and why the remedy differs by level.

### BB-105 · The Wikipedia / Russian Doll method
**RULE** To find the homepage area entity: pick any city served → Wikipedia → click to the
county → read the first sentence for the region → check whether that region contains
**all** counties served → if not, go up one level → repeat. The smallest true container is
the area entity. Collect every variant name Wikipedia uses for it.
**CLASS** Method · **GRADE** B · **SOURCE** D-SYS, D-SOP
**WHY** The homepage must make a statement that is true and verifiable and contains every
city served. A business serving 22 cities cannot claim one city.
**EXAMPLES** GutterXperts (12 cities, Beaufort + Jasper) → Hilton Head Island–Bluffton–Port
Royal SC MSA / South Carolina Lowcountry. St. Mary's (22 cities, 5 counties) → Sacramento
Metropolitan Area / Greater Sacramento.

### BB-106 · The GB Category is the service entity
**RULE** The GBP primary category *is* the category entity. Verify it on Wikipedia. That
exact term or its Wikipedia-verified variant goes in every SEO title on the site. Not a
guess, not a keyword.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-GBP, D-SYS
**WHY** Optimizing at category level makes the page relevant to every query associated
with that category, including phrasings absent from the page.

### BB-107 · Broadest category primary, narrower secondary
**RULE** Keep the broadest genuinely relevant category as GBP primary; narrower relevant
ones as secondary.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-GBP
**WHY** A common error is a specific category as primary with the broader one demoted to
secondary, which narrows the query set the profile is eligible for.

### BB-108 · The entity variant map
**RULE** Before writing anything, assign entity variants to every optimization element.
**No two consecutive elements (URL → SEO title → H1 → first H2) may use the same variant.**
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Repeating a variant consecutively is over-optimization and is suppressed. Variants
create breadth; repetition creates a signal of manipulation.

### BB-109 · Variants must be real
**RULE** Every variant must be a real, verifiable name — from Wikipedia, the MSA's official
name, the county, the region, the anchor city. Never coin one.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** An invented variant is an unverifiable statement, which is the failure mode in
BB-103.

### BB-110 · Storefront vs SAB decides the area entity
**RULE** Storefront (address shown) → the city. SAB (address hidden) → the containing
metro or MSA.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP
**WHY** Get this wrong and the whole site targets the wrong entity.

---

# BB-2xx · SITE ARCHITECTURE AND SITE EFFICIENCY

### BB-201 · The silo model
**RULE** Homepage = brand hub, area entity, introduces service silos via H3 links only,
does **not** describe individual services. Service pages = one per primary service,
content-heavy, describe the service in depth. Location pages = one per city, lean,
conversion-focused, do **not** re-describe services. Blog = supporting only.
**CLASS** Architecture · **GRADE** A · **SOURCE** T-ONP, D-SYS
**WHY** Each page type does one job. Overlap between them is what creates competing pages.

### BB-202 · One page per service, one page per city
**RULE** One page per primary service. One page per city. Associations between them are
built through internal linking, not repetition.
**CLASS** Architecture · **GRADE** A · **SOURCE** T-ONP
**WHY** Language models understand variants, so restating a service on fifteen city pages
earns nothing and costs crawl budget. Worked example: 3 services × 15 cities = 45 pages
under old tactics; 3 + 15 = 18 achieves the same associations.

### BB-203 · Service+city combination pages — absolute prohibition
**RULE** `/bluffton/gutter-installation/` and every equivalent is prohibited.
**CLASS** Prohibition · **GRADE** B · **SOURCE** D-SYS
**WHY** Dilutes link equity across 100+ pages when 14 service + 12 location pages achieve
the same associations in 26.

### BB-204 · No sub-service pages
**RULE** A service that is a variant, component or sub-task of a primary service is an
**H2 section**, not a page. Only give it a page if it has its own independent Wikipedia
entity *and* genuinely distinct buyer intent.
**CLASS** Prohibition · **GRADE** B · **SOURCE** D-SYS
**WHY** Splits entity authority and creates competing pages. St. Mary's had 8 sub-service
pages competing with the main repair page.

### BB-205 · The internal linking wheel
**RULE** Every service page links **down** to all location pages via the service-areas
table. Every location page links **up** to all service pages via the services table, and
to every sibling location page. H3 anchor-text links in both directions.
**CLASS** Architecture · **GRADE** A · **SOURCE** T-ONP, D-SYS
**WHY** Any external link to any page flows through the tables to the whole network. One
direction only = a broken wheel. St. Mary's location pages had no links to service pages —
59 of 76 pages unindexed.

### BB-206 · Cross-page links live in their tables
**RULE** Cross-page service and location links belong in the dedicated tables, not embedded
in body prose.
**CLASS** Architecture · **GRADE** A · **SOURCE** T-ONP, D-SYS
**WHY** The table is the association mechanism. A buried link is not part of the wheel.

### BB-207 · No empty hub pages
**RULE** `/services/` and `/service-area/` as indexed pages are mistakes. Redirect or
remove them.
**CLASS** Prohibition · **GRADE** B · **SOURCE** D-SYS
**WHY** Orphaned hubs with no content value consuming index budget.

### BB-208 · URL structure
**RULE** Root-proximate — `/garage-door-repair/` beats `/services/garage-door-repair/`.
No city in a service page URL. No service in a location page URL. Short, clean,
entity-relevant.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Depth costs crawl priority; mixed entities in a slug send conflicting signals.

### BB-209 · Crawl resistance lowers site quality
**RULE** Technical errors, internal redirects, links to 404s, sitemap URLs marked noindex,
canonicalized pages still being crawled, redundancy and over-optimization all consume more
crawl resource than necessary and lower overall site quality.
**CLASS** Working hypothesis · **GRADE** A (as Bradley's stated model) · **SOURCE** T-ONP
**WHY** Bradley's reading of the Helpful Content Update: Google's resources are stretched
by AI content volume, so it demotes sites that waste them.
**⚠️** The site-quality-score-as-multiplier mechanism is Bradley's explanation, not
documented platform behaviour. See Delta CM-009.

### BB-210 · Low index rate is a content problem, not a technical one
**RULE** When a large share of published pages are unindexed, Google is making an editorial
judgment that they are redundant, low-quality or self-competing. Diagnose: competing
sub-service pages, competing blog posts, padded location pages, empty hubs, utility pages
consuming budget.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Reframes an apparent technical symptom as an architecture finding.
**⚠️** The method for *measuring* index rate is contested. See Delta CM-008.

---

# BB-3xx · ON-PAGE — METAS, H TAGS, CONTENT

### BB-301 · The semantic triple
**RULE** Every SEO title states **who we are (brand) + what we do (GB category) + where we
do it (area entity)**. Three entity associations in one title.
**CLASS** Methodology rule — central · **GRADE** B · **SOURCE** D-SYS
**WHY** The single densest opportunity to spoon-feed the knowledge graph.
**⚠️** This is described as the most important concept in the methodology and appears in
no transcript we hold. Highest-priority P1 retrieval.

### BB-302 · Title formats by page type
| Page type | Format |
|---|---|
| Homepage | `Brand - GB Category - Area Entity` |
| Service | `Service Name - Brand` |
| Location | `Brand - GB Category - City, Full State Name` |
| County hub | `Brand - GB Category - County, Full State Name` |
| Blog | `Post Title - Brand` |
| About | `About Brand - Area Category` |

**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP
**RULES** Full state names, never abbreviations. One city maximum. Title Case. No "The
Best" in a title. Separator used identically site-wide.

### BB-303 · Never truncate an entity term
**RULE** Never shorten a title by swapping or dropping an entity term to hit a character
count. Google truncates display only; the full title is indexed. A 72-character title is
fine.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** "Greater Sacramento" → "Sacramento" saves 8 characters and changes the entity.

### BB-304 · H1 must differ from the SEO title
**RULE** The H1 uses a **different variant of every entity** in the SEO title. Never the
same term in both.
**CLASS** Methodology rule — foundational · **GRADE** B · **SOURCE** D-SYS
**WHY** Repetition between the two is over-optimization and is suppressed. Both state the
triple; neither states it the same way.

### BB-305 · H1 format
**RULE** `The Best [Service Variant] in [Area Variant]`. One H1. No brand in it — the
branded domain implies it. Service pages use the area entity and **never a city**;
location pages use the city with **no state**.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Brand in the H1 wastes the slot on an entity already established.
**⚠️** "The Best" is described as a confirmed AI trigger word with no source given. See
Delta CM-002.

### BB-306 · H tags are optimization decisions, not styling
**RULE** *"H tags speak directly to the bots about what the page is about. They are NOT
styling tools. Every H tag is an optimization decision."*
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Every H tag declares an entity. Using one for visual weight declares something you
did not intend.

### BB-307 · H tag complete reference
| Rule | Why |
|---|---|
| One H1 per page | Multiple H1s create entity ambiguity |
| H1 differs from SEO title | Over-optimization → suppression |
| No H tags in nav, footer, sidebar | Dilutes the main entity of every page they appear on |
| Never H tags for styling | Unintended entity signals |
| No city names in service page H tags | Cities belong in the service-areas table |
| H3s are subtopics of their H2 — never skip levels | Hierarchy is the entity descent |
| Never the same variant at consecutive elements | Over-optimization |
| Every H2 section under 500 tokens | AI chunk rule, BB-309 |
| H3 anchor-text links for service and location links | Not H2s, not plain text |
| H3 question + paragraph answer for FAQs | The format AI uses for recommendation answers |

**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-308 · Every header names an entity
**RULE** Decorative headers — "Our Process", "Why Choose Us", "Get Started" — are
forbidden. Every header declares an entity. Every H2 should be sayable as a real question.
**CLASS** Methodology rule · **GRADE** C · **SOURCE** D-SYS (implied); explicit only in
Coastal's guideline
**WHY** A decorative header wastes a retrieval handle.

### BB-309 · The 500-token chunk rule
**RULE** Every H2 section — heading plus all content to the next H2 — stays under 500
tokens (~375 words). Applies to every H2 on every page.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** AI search pulls H2 sections as chunks. Sections over the limit are far less likely
to be pulled and cited.
**WHAT RAISES RETRIEVAL** Tables and lists over prose; H3 question + paragraph answer;
content referencing verifiable Wikipedia entities; schema markup.

### BB-310 · Retrieval is passage-level
**RULE** Every section must read correctly in isolation and name its own entities rather
than leaning on a pronoun or context set three headings earlier.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** One section may be pulled to answer a sub-query while the rest of the page is
ignored.

### BB-311 · The two layers
**RULE** The SEO title is for the models. The H1 is for the human who just clicked. Headers
declare entities and define chunks; the copy between them converts.
**CLASS** Framework · **GRADE** B · **SOURCE** D-SYS
**WHY** Optimize the body and you get keyword stuffing. Humanize the headers and the page
goes invisible to AI search. Both, always.

### BB-312 · Opening paragraph
**RULE** No H tag. Reinforces the semantic triple in a **third** variant set. Uses the area
variants naturally rather than repeating one. Contains the phone number and the offer.
Under 500 tokens. Unique angle per page — a distinct buyer state on a service page, this
specific city on a location page.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-313 · Homepage structure — 17 sections in order
1. Review bar (above nav) — no H tag · 2. Navigation — top-level pages only · 3. H1 —
one, never changed once live · 4. Opening paragraph — no H tag · 5. **H2: "[GB Category]
Services"** — the only H2 introducing services · 6. H3 anchor-text links to each service
page, no descriptions, max 5–6 · 7. Trust/About — H2; sub-items are styled **cards, not
H3** · 8. How It Works — 3 steps, styled bold, no H tags · 9. Social proof bar — no H tag
· 10. Gallery — H2; alt text `[service type] in [city], [State] — [Brand]`, vary cities ·
11. Testimonials — H2 · 12. FAQ — H2 + H3 per question, **brand-level questions only** ·
13. Service areas grid — H2, not H-tagged per city · 14. Google Maps embed — GBP iframe,
no H tag · 15. Featured blog posts — H2, build only after blog redirects are live · 16.
Final CTA — H2 · 17. Footer — NAP exact match, **zero H tags**

**CLASS** Methodology rule · **GRADE** C · **SOURCE** D-SYS "confirmed from felling.pro
live implementation"
**WHY** Three review-count exposure points (review bar, hero badge, social proof bar).
Testimonials chosen to mention locations and services do passive entity association work.
**⚠️** The cards-not-H3 rule in section 7 is the most commonly violated rule in the system.

### BB-314 · Service page structure
H1 → opening paragraph (unique buyer state) → H2 how the service is delivered → H2 service
types/subtypes with H3 per type → H2 FAQ → H2 service areas with H3 links to every location
page → CTA (no H tag).
**Never a city name in any H tag on a service page.**
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-315 · Location page structure
H1 (`The Best [Service Variant] in [City]`, no state) → opening paragraph (unique per city)
→ H2 services table with H3 links to all service pages, **no service descriptions** → H2
local context, 3–5 sentences on this city's genuinely unique conditions → FAQ, 3–4
questions unique to this city → H2 neighborhoods, 6–12 real ones → city-level map embed
(not the GBP map unless this is a verified GBP location) → H2 Things to Do → H2 Top Sites →
H2 sibling cities linking to every other location page → CTA with NAP.
**Under 1,000 words.**
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP
**WHY** Sites averaging 2,400–3,000 words per location page are over-optimized with
repeated service descriptions that belong on service pages. Location pages link to
services; they do not explain them.

### BB-316 · FAQ format and uniqueness
**RULE** H2 wrapper with a fresh variant pair. H3 per question, phrased as a person would
type or speak it. Each answer's **first sentence is the complete answer**. **No question
appears on two pages anywhere on the site.** Service 4–6 · location 3–4 · homepage 4–6
brand-level · blog 3–5.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Exactly the format AI uses for recommendation answers. The FAQ also absorbs query
variants that do not deserve their own page — site efficiency at the header level.

### BB-317 · Local context must be real
**RULE** The location page's local-context section must be genuinely unique to that city —
housing stock, terrain, weather, age of development, specific failure patterns. It cannot
appear on any other city page. Neighborhoods, Things to Do and Top Sites must be real and
verifiable, never invented.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** It is the only differentiator between structurally identical city pages.

### BB-318 · Never copy content between pages
**RULE** Zero copied content between any two pages.
**CLASS** Prohibition · **GRADE** B · **SOURCE** D-SYS

### BB-319 · No bloated statistics paragraphs
**RULE** Stat dumps and padded facts sections are prohibited.
**CLASS** Prohibition · **GRADE** B · **SOURCE** D-SYS
**WHY** Nobody reads them and the helpful content update penalizes them.

---

# BB-4xx · GOOGLE BUSINESS PROFILE

### BB-401 · Complete the profile accurately
**RULE** Complete the profile as fully as possible with accurate information. This has
changed least of anything in the methodology.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-GBP

### BB-402 · The location landing page decision
**RULE** Which URL the GBP points to depends on business type. Single-location storefront →
homepage, if optimized for that city. SAB → the homepage only if it is optimized for an
area that **contains** the GBP's physical city; otherwise a dedicated location landing page
for the city the GBP is actually in.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-GBP
**WHY** Google knows where the profile is physically registered. A landing page optimized
for a different city is a disconnect that suppresses both the profile and the site. A
containing county is still a true statement.

### BB-403 · Activity vs engagement signals
**RULE** **Activity** signals are business-produced: GBP posts, photo uploads, review
responses. **Engagement** signals are user-produced: expanding posts, clicking Learn More,
viewing photos and reviews, and above all leaving a review. User-generated signals are
weighted more heavily.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-GBP
**WHY** Harder to fake, so Google weights them higher.

### BB-404 · Review velocity
**RULE** Where the profile is otherwise correctly optimized, receiving reviews faster than
the top-ranked competitors is what moves it. Review velocity is among the primary GBP
ranking factors.
**CLASS** Practitioner observation · **GRADE** A · **SOURCE** T-GBP

### BB-405 · Two GBP posts per week, two types
**RULE** Minimum 2 posts per week per location, alternating:
**Type 1 — internal:** Learn More links to a page on the site, rotating homepage, service,
location, blog.
**Type 2 — external citation:** Learn More links to an external citation URL — Yelp, a
press release, HomeAdvisor, BBB.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-ENT, T-GBP, D-SYS
**WHY** Type 2 forces Google to crawl and validate the citation. The most powerful
knowledge-graph spoon-feeding available at GBP level.

### BB-406 · Never "Call Now"
**RULE** Never use the Call Now button on posts. Always Learn More.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Call Now produces almost no consumer clicks from posts, and Learn More is the
mechanism for all entity association work.

### BB-407 · Link only to accurate assets
**RULE** Only ever link out to assets with accurate published information.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-ENT
**WHY** Otherwise the mechanism manufactures NAP discrepancies.

### BB-408 · Review responses do entity work
**RULE** Always respond. Include service and location entity mentions naturally.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-GBP

### BB-409 · Photos weekly
**RULE** Upload weekly. Geo-tagged mobile job photos carry more weight than studio photos.
**CLASS** Practitioner observation · **GRADE** C · **SOURCE** D-SYS

---

# BB-5xx · OFF-PAGE — CITATIONS, PRESS RELEASES, BACKLINKS

### BB-501 · What a citation is
**RULE** Any published mention of name, address, phone number and website — or some
combination of those four — is a citation. **Link or no link.**
**CLASS** Definition · **GRADE** A · **SOURCE** T-ENT
**WHY** Press releases, Web 2.0s, social profiles and video descriptions with NAP all
count. The value is the mention near relevant content.

### BB-502 · Citation benchmarks
| Situation | Benchmark |
|---|---|
| US business, published street address | **100** structured citations minimum |
| Service area business, hidden address | **65** minimum |
| Typical local business reality | 35–65 (below minimum) |
| AI search visibility | 100+ (press releases count) |
| Competitive AI search | 200+ |

**CLASS** Planning benchmark · **GRADE** B · **SOURCE** D-SYS, D-SOP (100+ also in T-LNK)
**WHY** Citations are named as one of the most important levers for both Maps and AI
search performance.
**⚠️** Planning benchmarks, not Google thresholds. See Delta CM-006.

### BB-503 · Citation priority order
1. Yext PowerListings or BrightLocal — fastest path to 50+ · 2. Major national directories
— Yelp, BBB, Angi, HomeAdvisor, Houzz, Thumbtack, Nextdoor, Facebook, LinkedIn, Bing
Places, Apple Maps · 3. Industry-specific directories · 4. Geographically relevant —
chamber of commerce, municipal, regional publications · 5. Ongoing press releases
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-504 · NAP consistency is non-negotiable
**RULE** Identical name spelling, address format and phone format on every citation. Fix
existing inconsistencies **before** building new ones.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-ENT, D-SYS
**WHY** Variation creates conflicting knowledge graph data.

### BB-505 · Every new citation, three places
**RULE** Add every new citation URL to: the `sameAs` array immediately; the Google Sheet
feeding the ID page immediately; the GBP post rotation as a Type 2 post within a week.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-506 · Press releases are for brand mentions, not links
**RULE** *"Press releases are the silver bullet right now."* They are **not** for link
building to money pages. Never keyword anchors to service or location pages.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** The same referring domains recur on every distribution, so Google sees diminishing
value and eventually ignores them. What they *are* for: brand authority on high-authority
properties, unstructured citations, and entity associations the knowledge graph reads.

### BB-507 · What to link to from a press release
**RULE** One link per release, rotating: the ID page · Google Maps **share** URL (not CID)
· Google review share URL · knowledge panel share URL · branded Web 2.0s · social profiles
including the personal LinkedIn of whoever is quoted · the service's media room · a
previous release.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-508 · Press release silo stack
**RULE** One premium release at the top of the stack links to the money site with a
**brand** anchor. Supporting standard releases target FAQs and subtopics and link to the
top-of-stack release, not the money site.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** Relevance flows up the chain to one exit point, so you can publish as many as
needed without hammering the site from the same referring domains.

### BB-509 · Press release frequency
**RULE** Minimum 2 per month for local businesses.
**CLASS** Planning benchmark · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-510 · Five anchor text categories
| Category | Definition | Over-optimizable? |
|---|---|---|
| Brand / URL | Brand name, company name, naked URL | No |
| Miscellaneous / generic | "click here", "learn more" | No |
| Empty / frame | Image links without alt, iframes, redirects | No |
| **Target** | Keyword **+ location modifier** | **Yes** |
| **Topic** | Keyword only | **Yes** |

**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-LNK

### BB-511 · Brand anchors dominate local
**RULE** Across roughly four years of monthly competitive analyses, **90–95% of local
search queries show Brand/URL as the dominant anchor type.** Build primarily brand anchors,
preferring **compound anchors** — brand + location, or brand + service — over bare keyword
anchors.
**CLASS** Practitioner observation · **GRADE** A · **SOURCE** T-LNK

### BB-512 · Link quantity at or below the competitor average
**RULE** The average backlink count of the top five ranking pages sets the ceiling. Stay at
or below it where possible.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-LNK
**WHY** Exceeding it makes the campaign an outlier and draws attention it does not need.
**EXCEPTIONS** Correcting an anchor ratio imbalance, a topical relevance imbalance, or
inheriting a campaign already over the line.

### BB-513 · Relevance gates strength
**RULE** Google does not care about third-party metrics — not DA, not DR, not Trust Flow.
Majestic is used for one thing: **Topical Trust Flow**, which indicates the topical
*category* of a link profile. A non-relevant profile makes the Trust Flow number
meaningless; a relevant profile makes it a meaningful measure of strength.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-LNK
**WHY** Relevance is the gate, strength is the multiplier. Strong-but-irrelevant links do
not help.

### BB-514 · Determining topical requirements
**RULE** Send the target page and the top five competitor pages through Google's Natural
Language API at **page level** to get the topical categories Google itself identifies, then
match those to Majestic's Topical Trust Flow categories. That match set defines where links
should be placed.
**CLASS** Method · **GRADE** A · **SOURCE** T-LNK

### BB-515 · Competitor selection for link analysis
**RULE** Geolocate the browser to the GBP's city. Take the top five ranked **local business**
pages, deliberately excluding directories — Yelp, Angi, HomeAdvisor. Analyse at both page
level and domain level.
**CLASS** Method · **GRADE** A · **SOURCE** T-LNK
**WHY** Google ranks pages, but a page's performance is influenced by the whole domain, so
the real competition is at domain level.

### BB-516 · Backlink sources, in order
1. Own assets — Web 2.0, social profiles · 2. Press releases at the top of a silo stack,
brand anchor · 3. High-quality structured citations (links and citations, dual value) ·
4. Industry-relevant links — relevance over raw DA · 5. Guest posts and local partnerships
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**PROHIBITED** Bulk link packages · the same anchor from the same source to multiple pages
· direct keyword-anchor links from press releases to money pages.

---

# BB-6xx · SCHEMA

### BB-601 · Homepage array schema
**RULE** `WebPage` root, with `Corporation` nested four times — as `author`, `creator`,
`publisher` and `provider` — all four pointing to the same `@id` (the ID page URL), plus
`HomeAndConstructionBusiness` (or a more specific subtype) for the GBP location entity.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-602 · Homepage additional fields
**RULE** `about` array with Wikipedia entity references and kgmid values for the primary
service category, the area entity, and relevant geographic entities (county, metro, state).
`mentions` array for contextual entities. `disambiguatingDescription` distinguishing this
business from similar ones. `sameAs` with every citation URL.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-603 · Schema by page type
| Page type | Schema |
|---|---|
| Homepage (GBP landing page) | Array per BB-601 + BB-602 |
| Service pages | `Service` or `WebPage`. **Never LocalBusiness. No location data.** |
| Location page — GBP landing page | `HomeAndConstructionBusiness` or subtype; `@id` = ID page; `sameAs`; `hasMap` = that GBP's CID |
| Location page — non-GBP | `Article` or `WebPage`. **Never LocalBusiness.** |
| About page | `Person` for the owner + `Organization` for the brand |
| Blog posts | `Article` — author, datePublished, dateModified |

**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-604 · The LocalBusiness test
**RULE** Is this exact page URL entered as the Website field on an actual verified Google
Business Profile? **Yes** → it is a GBP landing page, gets a LocalBusiness subtype. **No**
→ it is never a LocalBusiness of any kind.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS
**WHY** *"22 city pages all getting LocalBusiness schema is a mistake made in nearly every
campaign."* Run the test per page, and per GBP for multi-location clients.

### BB-605 · `sameAs` is the field that matters
**RULE** Every citation built is added to `sameAs` immediately. It is the most important
schema field to maintain over time.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-ENT, D-SYS
**WHY** It works for Google and for all AI models, not just Google.

### BB-606 · The three spoon-feeding mechanisms
1. **GBP posts linking to external citation URLs** — Google-specific; forces crawl
validation · 2. **`sameAs` in schema** — works for Google and all AI models · 3. **The ID
page** — works for all AI models including ChatGPT and Perplexity
**CLASS** Framework · **GRADE** A · **SOURCE** T-ENT, D-SYS

### BB-607 · The ID page
**RULE** A dedicated hosted page consolidating every branded asset and citation URL, with
`@id` in the schema pointing to it. Build: Google Sheet, column A = anchor text, B =
citation URL, C = a CONCATENATE hyperlink formula; hide A and B; publish to web; embed the
iframe on a dedicated page. New citations are added to the sheet and the page updates
automatically.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-ENT, D-SOP
**WHY** It tells crawlers where to find all validating information and lets them spider out
from one point. It becomes an **entity hub**, and therefore a primary link target.
**TIMING** Month 2 for a new client. An established client with no ID page is a real gap.

### BB-608 · Tier-one link pattern
**RULE** Push authority at three levels simultaneously: an anchored link to the money site,
an anchored link to the ID page, and a Google Map embed.
**CLASS** Methodology rule · **GRADE** A · **SOURCE** T-ENT
**WHY** Organic, maps and the hub that ties all external assets to the brand.

---

# BB-7xx · BLOG

### BB-701 · The competition test
**RULE** Does this post target the same entity + location combination as a service or
location page? If yes, it is competing.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-702 · Redirect, never delete
**RULE** 301 a competing post to the highest-relevance service or location page. Never just
delete — the redirect captures accumulated link equity.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-703 · What a blog post can do without competing
**RULE** Brand-level content no page covers (story, milestones, community) · technical
deep-dives broader than any single service page · FAQ-style content answering questions no
page answers.
**CLASS** Methodology rule · **GRADE** B · **SOURCE** D-SYS

### BB-704 · Blog structure
**RULE** Title `Post Title - Brand` · direct answer front-loaded · H2 sections under 500
tokens · FAQ block · real named author · `Article` schema with author, datePublished,
dateModified · internal links in **one separated block at the end**, never embedded in
prose.
**CLASS** Methodology rule · **GRADE** C · **SOURCE** D-SYS partial; the separated-link-block
rule is Coastal's — see Delta CM-005

---

# BB-8xx · MEASUREMENT AND TESTING

### BB-801 · Single variable testing
**RULE** *"Single variable testing is how you determine what is effective. Not changing
eight things at a time on one site."*
1. Establish a baseline · 2. Change **one** element — title, H1, one H2, opening paragraph
or schema · 3. Resubmit in GSC immediately · 4. Wait **3 weeks minimum** — *"It is like
dropping a rock in a pond. The ripples have to subside."* · 5. If positive, test
duplicatability on 2–3 other pages · 6. If positive on **60%+**, adopt as standard.
**CLASS** Method · **GRADE** B · **SOURCE** D-SYS, D-SOP

### BB-802 · Never change multiple variables
**RULE** Changing several elements at once makes it impossible to identify what caused a
result.
**CLASS** Prohibition · **GRADE** B · **SOURCE** D-SYS

### BB-803 · Brand search diagnostics
**RULE** Geolocate to the GBP's city and search the brand. Single location → a knowledge
panel should appear. Multi-location → that location at the top of the maps pack. A maps
pack of **similarly named competitors** instead of a knowledge panel means the entity is
polluted or ambiguated.
**CLASS** Method · **GRADE** A · **SOURCE** T-ENT

### BB-804 · The 16-of-20 supporting asset threshold
**RULE** Across the top two pages (20 results) of the geolocated brand search, at least
**16** should be URLs explicitly referencing that business location. Below that, the
knowledge graph is underdeveloped and **this is where all effort should start.** For a
multi-location brand, results referencing the brand but not that location still count.
**CLASS** Practitioner benchmark · **GRADE** A · **SOURCE** T-ENT

### BB-805 · Domain search
**RULE** Search the bare root domain. The homepage should rank first. If something else
outranks it, that typically indicates an algorithmic penalty against the domain.
**CLASS** Practitioner observation · **GRADE** A · **SOURCE** T-ENT

### BB-806 · Indexation check
**RULE** Compare the URL count in the sitemaps against what is actually indexed. A large
shortfall indicates an indexing problem.
**CLASS** Method · **GRADE** A · **SOURCE** T-ENT
**⚠️** Bradley's *measurement source* for this is the `site:` operator count. Contested —
see Delta CM-008.

### BB-807 · Monthly monitoring
Crawl and page inventory monthly · GBP posts weekly · review collection ongoing across
Google, HomeAdvisor, Thumbtack, Yelp · review counts in schema and content quarterly ·
citation audit quarterly · `sameAs` and ID page updated on every new citation · GSC review
monthly · Maps rank screenshots monthly · press releases monthly · GBP job photos weekly ·
client progress update monthly.
**CLASS** Method · **GRADE** B · **SOURCE** D-SOP

---

# BB-9xx · PROHIBITED PRACTICES

Hard stops, not guidelines. Each maps to a rule above.

| # | Prohibited | Rule |
|---|---|---|
| BB-901 | Service + city combination pages | BB-203 |
| BB-902 | H tags in nav, footer or sidebar | BB-307 |
| BB-903 | H tags used for styling | BB-306 |
| BB-904 | Same entity variant in SEO title and H1 | BB-304 |
| BB-905 | City names in service page H tags | BB-307 |
| BB-906 | Copying content between pages | BB-318 |
| BB-907 | More than one page per service | BB-202 |
| BB-908 | Homepage optimized for one city when many are served | BB-105 |
| BB-909 | Multiple links, same referring domain, same anchor, same page | BB-516 |
| BB-910 | Press releases with keyword anchors to money pages | BB-506 |
| BB-911 | Bloated statistics paragraphs | BB-319 |
| BB-912 | Changing multiple variables at once | BB-802 |
| BB-913 | Blog posts targeting service + location combinations | BB-701 |
| BB-914 | Long location pages with repeated service descriptions | BB-315 |
| BB-915 | Truncating entity terms to hit a character count | BB-303 |

---

# PRIORITY ORDER

Bradley's consistent sequence when everything is broken at once:

1. Homepage semantic triple — SEO title + H1. Highest-priority SEO change.
2. Brand name consistency across all pages
3. Service page H tags — remove city references, fix variants
4. Location page cleanup — strip service descriptions, add service links
5. Sub-service page consolidation + redirects
6. Blog post redirects
7. Schema fixes
8. Citation building — **starts Day 1, alongside on-page**
9. GBP posts — fix Learn More, alternate types
10. Press releases
11. ID page — Month 2, after initial citations

**GRADE** B · **SOURCE** D-SYS, D-SOP

---

# EVIDENCE SUMMARY

| Grade | Count | What it means for you |
|---|---|---|
| **A** | 33 rules | Quotable. Traceable to a transcript we hold. |
| **B** | 44 rules | Sound and internally consistent, but sourced only to derived documents. |
| **C** | 5 rules | Single-source, unverifiable. State the grade when asked. |

**The grade C rules are:** BB-308 (decorative headers), BB-313 (17-section homepage),
BB-409 (photo weighting), BB-704 (blog structure), and — critically — the "confirmed AI
trigger" status of "The Best" inside BB-305.

**Grade B is where most of the system lives**, including the semantic triple (BB-301),
which the derived documents call the most important concept in the methodology and which
appears in no transcript we hold.

### Missing P1 sources, in priority order

Named by the derived documents and not in the brain:

1. **Semantic triple transcript** — underpins BB-301 through BB-305
2. **Geographic hierarchy transcript** — underpins BB-105
3. **AI SEO transcript** — underpins BB-309, BB-310
4. **Location page transcript** — underpins BB-315
5. **GBP posts transcript** — underpins BB-405, BB-406
6. **Press release transcript** — underpins BB-506 through BB-509
7. **Full SEO audit videos** — underpins BB-313
8. **Subdomain strategy transcript** — the deferred geographic subdomain question
9. **felling.pro implementation analysis** — the only stated source for BB-313
