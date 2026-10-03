# BB-6xx · SCHEMA — v1.1
### Rewritten from direct observation of a Bradley-built implementation
**Replaces BB-601 through BB-608 in BB-Standard-v1.0**
**Sources:** SRC-030 (homepage), SRC-031 (service page), SRC-032 (location page) — woodlawntrees.com, captured 18 September 2026

---

## Scope and grading

**These sources are scoped to schema only.** Page structure, headings and copy on that site
are not optimized to the methodology and must not be cited for anything outside Finish — schema.

New grade introduced for this section:

**A-obs** — directly observed in a Bradley-built live implementation. For schema this
outranks grade B, because the derived documents describe schema Bradley no longer ships.

Every rule below is A-obs unless noted. Where v1.0 said something different, the change is
called out.

---

## BB-601 · The two-node identity graph *(replaces v1.0 entirely)*

**RULE** The homepage carries a `@graph` with exactly two nodes:

1. **`Corporation`** — `@id: {domain}/#corporation` — the brand-level entity
2. **`HomeAndConstructionBusiness`** (or the most specific applicable subtype) —
   **`@id: {ID page URL}`** — the location-level entity

The location entity points up with `parentOrganization: { "@id": "{domain}/#corporation" }`.

**WHY** This is BB-104's two knowledge-graph levels expressed directly in markup. The brand
graph and the branded-location graph get one node each, explicitly linked. That structural
match is the strongest evidence in the whole capture that the methodology is being executed
deliberately rather than by template.

### ⚠️ What changed from v1.0

v1.0 stated: `WebPage` root with `Corporation` nested four times as `author`, `creator`,
`publisher` and `provider`, all pointing to one `@id`.

**Not observed.** The homepage has **no `WebPage` node at all**, and no four-role nesting.
That pattern came from the felling.pro generation and the derived documents. It is either
superseded or was never general. Do not build it.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Corporation",
      "@id": "https://example.com/#corporation",
      "name": "...", "legalName": "...", "alternateName": "...",
      "url": "https://example.com/",
      "logo": { "@type": "ImageObject", "url": "..." },
      "image": ["...", "..."],
      "description": "...",
      "foundingDate": "2012",
      "founder": {
        "@type": "Person",
        "name": "...", "alternateName": "...", "jobTitle": "...",
        "hasCredential": {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "certification",
          "name": "ISA Board Certified Master Arborist",
          "identifier": "PD-1052B"
        }
      },
      "email": "...",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+1-304-844-0054", "email": "...",
        "contactType": "customer service",
        "areaServed": "US", "availableLanguage": "English"
      },
      "sameAs": [ "…every citation and profile…" ]
    },
    {
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://s3.amazonaws.com/slstacks/{client}/id.html",
      "name": "...", "alternateName": "...",
      "url": "https://example.com/",
      "mainEntityOfPage": "https://example.com/",
      "image": ["..."],
      "telephone": "+1-304-844-0054", "email": "...",
      "description": "...",
      "parentOrganization": { "@id": "https://example.com/#corporation" },
      "address": { "@type": "PostalAddress", "streetAddress": "...",
                   "addressLocality": "...", "addressRegion": "...",
                   "postalCode": "...", "addressCountry": "US" },
      "hasMap": "https://maps.app.goo.gl/…",
      "openingHoursSpecification": [ { "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","…"], "opens": "07:00", "closes": "17:00" } ],
      "areaServed": [ { "@type": "City", "name": "Cabins",
        "containedInPlace": { "@type": "State", "name": "West Virginia" } } ],
      "sameAs": [ "…same list as Corporation…" ]
    }
  ]
}
```

---

## BB-602 · The ID page URL is the business entity's `@id`

**RULE** The location entity's `@id` is **the ID page URL itself**, not a fragment on the
site. Every other node on every other page that needs to reference the business points at
that URL.

**WHY** This is a stronger claim than v1.0 made. The ID page is not a linked resource the
schema mentions — it **is** the canonical identifier of the business entity across the
whole graph. Crawlers resolving `@id` land on the page that consolidates every citation.

Observed value: `https://s3.amazonaws.com/slstacks/{client}/id.html` — S3-hosted, off the
client's own domain. v1.0 described a `/id/` page on the site with an embedded Google
Sheet iframe. Both satisfy the rule; the off-domain form is what is currently shipped.

---

## BB-603 · `sameAs` is identical on both nodes, and lists everything

**RULE** The same complete `sameAs` array appears on the `Corporation` and on the location
entity. Observed contents, in order:

1. The site's own homepage URL
2. **The ID page URL**
3. Google Maps share link
4. Apple Maps place link
5. Facebook
6. Yelp · Nextdoor · Chamber of Commerce · industry directory · MapQuest · DexKnows ·
   Superpages · YellowPages · EZLocal · CitySquares

The homepage and the ID page appearing inside `sameAs` is deliberate — the entity asserts
its own identity endpoints alongside third-party ones.

---

## BB-604 · Service page — `WebPage` + `Service`

**RULE** Two nodes, no LocalBusiness of any kind, no address, no NAP.

```json
{
  "@graph": [
    { "@type": "WebPage",
      "@id": "{url}#webpage",
      "url": "{url}", "name": "{title tag}", "description": "{meta description}",
      "isPartOf": { "@type": "WebSite", "@id": "{domain}/#website",
                    "name": "...", "url": "{domain}/" },
      "primaryImageOfPage": { "@type": "ImageObject", "url": "..." },
      "mainEntity": { "@id": "{url}#service" },
      "about": [ { "@id": "{url}#service" }, "…entity Things, see BB-606…" ] },
    { "@type": "Service",
      "@id": "{url}#service",
      "name": "Tree Trimming Service",
      "serviceType": "Tree Trimming & Pruning",
      "description": "...", "url": "{url}", "image": "...",
      "provider": { "@id": "{ID page URL}" },
      "areaServed": [ "…every city served, City + containedInPlace State…" ] }
  ]
}
```

Note `name` and `serviceType` carry different values — the node name and the
customer-facing service label.

`provider` points at the ID page `@id`, which is how the service attaches to the business
entity without restating any of it.

---

## BB-605 · Location page — `WebPage` + `ItemList`

**RULE** Two nodes. **No LocalBusiness**, even on the page for the city where the business
is physically headquartered — because the GBP's landing page is the homepage, not this
page. This is BB-604's test from v1.0 applied exactly, and it holds.

```json
{
  "@graph": [
    { "@type": "WebPage",
      "@id": "{url}#webpage",
      "url": "{url}", "name": "...", "description": "...",
      "isPartOf": { "@type": "WebSite", "@id": "{domain}/#website", … },
      "primaryImageOfPage": { … },
      "mainEntity": { "@id": "{ID page URL}" },
      "mentions": { "@id": "{url}#service-catalog" },
      "about": [
        { "@id": "{ID page URL}" },
        { "@type": "City", "name": "Cabins",
          "containedInPlace": { "@type": "State", "name": "West Virginia" } },
        "…geographic and topical Things, see BB-606…"
      ] },
    { "@type": "ItemList",
      "@id": "{url}#service-catalog",
      "name": "Tree Services in Cabins, WV",
      "itemListElement": [
        { "@type": "ListItem", "position": 1,
          "item": { "@id": "{domain}/tree-trimming#service" } },
        "…one per service page…"
      ] }
  ]
}
```

**Three things worth naming:**

- `mainEntity` on a location page is **the business**, not the page's city. On a service
  page it is the service.
- The `ItemList` is the schema-level link wheel. It references the service pages' `#service`
  `@id`s directly, so the graph carries the service-to-location relationship independently
  of the HTML links.
- The city appears **twice** in `about` — once as a bare `City` node with
  `containedInPlace`, once as a `Thing` with its Wikidata URI. Typed place plus resolved
  entity, both.

---

## BB-606 · Entity enrichment — Wikidata `@id`, not kgmid *(major change)*

**RULE** `about` arrays appear on **service and location pages only**. Each entity is:

```json
{
  "@type": "Thing",
  "@id": "https://www.wikidata.org/wiki/Q500094",
  "name": "Pruning",
  "description": "Core technique for removing dead diseased or interfering branches to improve structure and safety on Grant County properties.",
  "sameAs": [
    "https://en.wikipedia.org/wiki/Pruning",
    "https://www.wikidata.org/wiki/Q500094",
    "https://grokipedia.com/page/Pruning"
  ]
}
```

### What changed from v1.0

| v1.0 said | Observed |
|---|---|
| `about` + `mentions` arrays on the **homepage** | `about` on service and location pages; **homepage has neither** |
| Wikipedia + Wikidata + **kgmid** per entity | Wikipedia + Wikidata + **grokipedia.com**. No kgmid anywhere. |
| Entities identified by name | `@id` **is the Wikidata URI** — the node is the entity |
| `disambiguatingDescription` on the homepage | Not present |

**The `@id`-as-Wikidata-URI move is the important one.** Rather than describing an entity
and hoping it resolves, the node declares itself to *be* that Wikidata entity. Nothing to
disambiguate.

**Every `description` is contextual, never generic.** Not "pruning is the removal of
branches" but what pruning means *for this business in this county*. Observed consistently
across all 23 entity nodes.

### Entity selection

**Service page (11 observed, for tree trimming):** the service's core technique · the
governing professional field · the certifying body · two technique-specific concepts ·
the practitioner role · the underlying science · the assessment method · the risk
condition · the service county · the state · a domain-specific mechanism.

**Location page (12 observed):** the city itself · the county · the state · two landmarks ·
a watershed · two neighbouring served cities · the discipline · the practitioner role ·
the mountain range · the adjacent federal forest.

The pattern: service pages enrich toward **the craft**; location pages enrich toward
**the place**. Both anchor to county and state.

---

## BB-607 · Cross-page `@id` graph

**RULE** The pages form one graph through `@id` references, not through duplicated data:

```
location #webpage ──mainEntity──→ ID page @id (the business)
        └──mentions──→ location #service-catalog (ItemList)
                            └──item──→ service page #service
                                            └──provider──→ ID page @id

homepage Corporation ←──parentOrganization── homepage HomeAndConstructionBusiness
                                                    (@id = ID page URL)
```

The business entity is defined **once**, on the homepage. Every other page references it.
No NAP, no address, no hours are repeated anywhere else.

---

## BB-608 · `hasMap` uses the share link *(change)*

**RULE** `hasMap` carries the Google Maps **share link** (`https://maps.app.goo.gl/…`).

v1.0 specified the CID URL (`maps.google.com/maps?cid=…`). **Not observed.** The short
share link is what is shipped. Apple Maps sits in `sameAs`, not `hasMap`.

---

## Two defects in the reference implementation

Do not copy these.

**1. Dangling `WebSite` node.** Service and location pages both declare
`isPartOf: { "@id": "{domain}/#website" }`, but **no `#website` node is defined anywhere**,
including the homepage. The reference resolves to nothing.

*Fix in our builds:* define a `WebSite` node in the homepage graph with
`@id: {domain}/#website`, `url`, `name`, and `publisher` pointing at `#corporation`.

**2. Self-referencing `significantLink`.** The location page carries
`"significantLink": "https://woodlawntrees.com/cabins"` — the page pointing at itself.
`significantLink` is for *other* pages this one links to. Almost certainly a generation
artifact. Omit it, or populate it with the service page URLs.

Also noted, lower stakes: `legalName` duplicates `name` on the `Corporation` node. Where a
registered entity name differs from the trading name, `legalName` should carry the
registered one.

---

## Not observed, still open

The capture covers homepage, one service page, one location page. Not answered:

- **About page schema** — the site has no about page; it is a homepage anchor
- **Contact page schema** — same
- **Blog schema** — no blog on the site
- **Multi-GBP handling** — single-location business

v1.0's rules for these were sourced only to the derived documents and stay grade B or C.
The `Person` + `Organization` about-page rule is unverified; the `Article` blog rule is
unverified. **There remains no rule at all for contact page schema.**

---

## Rules confirmed unchanged

- Service pages never carry LocalBusiness and carry no location data *(confirmed)*
- Non-GBP location pages never carry LocalBusiness *(confirmed, including the HQ city)*
- The GBP landing page test decides which page gets the LocalBusiness subtype *(confirmed)*
- `HomeAndConstructionBusiness` as the default subtype *(confirmed)*
- The ID page exists and is referenced from the schema *(confirmed, and strengthened)*
- `sameAs` reflects the full current citation list *(confirmed)*
