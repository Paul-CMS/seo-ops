---
name: bb-schema-builder
description: "Build Bradley Benner / Semantic Links JSON-LD schema for a local business site — homepage, service pages and location pages — following the BB-6xx v1.1 node sets observed in a live Bradley-built implementation. Use this for Finish — schema work: when schema markup, JSON-LD, structured data, LocalBusiness type, sameAs, hasMap, an ID page, entity enrichment or Wikidata references are requested for a local-business client; when someone asks which schema type a page should carry; or when existing schema needs auditing against the standard. Enforces the pre-build asset gate and refuses to emit schema for pages whose URL or content is not final. Never emits LocalBusiness on a service page or a non-GBP location page."
---

# BB Schema Builder — Finish — schema

Implements **BB-6xx v1.1**, derived from direct observation of a Bradley-built live
implementation (SRC-030/031/032), not from the derived documents. Where the two disagree,
the observed implementation governs — see `references/schema-rules.md`.

## When this runs

**After** content is final and approved for that page type, and **after** the URL is
settled. Schema describes a page that will not change again.

Batch by page type. That page type's URLs being final is the gate — not "all content
done". Order: services → locations → about/contact/blog → **homepage last**, because the
homepage aggregates the service inventory and the citation list.

**Hard stop:** never write schema for a page with a pending URL change in the URL Decision
Map. `@id` and `url` are wrong the moment the redirect fires. The script refuses on
`pending_url_change: true`.

## Entry gate

Every value comes from **Brand Guide Section F**. Run the gate before anything else:

```bash
python3 scripts/build_schema.py <client.yaml> <out_dir> --check
```

It lists what is missing and why. Fill those in the Brand Guide, not in the config — the
config is generated from the Brand Guide, and patching it directly puts the two out of sync.

Wikidata URIs are required because v1.1 uses **the Wikidata URI as the `@id`**, not a kgmid.
A missing logo or an entity with no Wikidata URI is refused with a message, never a crash (CM-050).

**Entity check (CM-051).** Every run — `--check` included — confirms each entity over HTTP before
anything is built: with a Wikipedia URL, the page's own Wikidata item must equal the configured
Q-ID; without one, the Q-ID must exist and its label must match the entity's name; a Grokipedia URL
must resolve. Calls are paced. A mismatch or an unreachable source refuses the build — schema is never
built on an unchecked entity. Give every entity its Wikipedia URL where one exists: it makes the
check exact.

## Build

```bash
python3 scripts/build_schema.py <client.yaml> <out_dir>            # all pages
python3 scripts/build_schema.py <client.yaml> <out_dir> --page URL # one page
```

Each page is written twice: `<name>.jsonld` (raw — validate it at `validator.schema.org` before
implementation) and `<name>.script.html` (the same JSON-LD inside `<script type="application/ld+json">`,
ready for Jonie to paste). Everything is built in memory and checked first (CM-051): any working text
(`[NEED`, TODO, "Brand Guide", `[Placeholder]`), any `aggregateRating` / `review`, a Wikipedia URL as an
`@id`, `addressCountry` outside a `PostalAddress`, or an `areaServed` type other than City / Place /
AdministrativeArea → nothing is written. The script does not check that the facts are true; Section F does.

**Country** comes from `business.address.addressCountry` (or a top-level `country`); "US" if neither is set.

**Served areas** default to woodlawn's `City` + `State`. `area_served_extended: true` in one client's
config is a **pilot** (CM-051): it allows `type: Place` (a neighbourhood), `type: AdministrativeArea`
(a county) and a `wikipedia` link on a city. It becomes the default for every client only after Paul has
seen that client's output pass validator.schema.org and approved it.

## The node sets

| Page | Nodes |
|---|---|
| Homepage | `WebSite` + `Corporation` (`@id: /#corporation`) + LocalBusiness subtype (`@id` = **ID page URL**), linked by `parentOrganization` |
| Service | `WebPage` + `Service`, `provider` → ID page `@id` |
| Location (non-GBP) | `WebPage` + `ItemList`, `mainEntity` → ID page `@id` |
| Location (GBP landing page) | Takes the **homepage** node set, not the location one |

The business entity is defined **once**. No NAP, address or hours are repeated on any other
page — every other node reaches it by `@id`.

## The rules that matter most

**The ID page URL is the business entity's `@id`.** Not a resource the schema links to —
the canonical identifier of the business across the whole graph.

**LocalBusiness only on a verified GBP's actual landing URL.** No exception exists. Not for
the headquarters city page, not for a page that ranks well, not on client request. The
script raises if a location page is also the GBP landing page.

**Entity Things carry the Wikidata URI as `@id`**, with `sameAs` for Wikipedia and
Wikidata. No kgmid. Every `description` is contextual to this business in this place —
never a dictionary definition. Service pages enrich toward the craft; location pages enrich
toward the place. Both anchor to county and state.

**`about` appears on service and location pages only.** The homepage has none.

**Define the `WebSite` node.** The reference implementation references `#website` from
service and location pages and never defines it. The builder emits it on the homepage with
`publisher` → `#corporation`.

## Not covered

About page, contact page, blog and multi-GBP schema were not observed in the capture.
v1.0's rules for about (`Person` + `Organization`) and blog (`Article`) remain unverified,
and **there is no rule at all for contact page schema**. Do not invent one — flag it.
Bradley's written patterns for about, contact, small-site, franchisor and multi-GBP pages are listed in
`references/schema-rules.md` ("Not observed, still open"), each needing Paul's ruling; the small-site
three-node homepage is open question CM-052, and BB-601's two nodes stand until he rules.
The **Never** list is at the end of `references/schema-rules.md` (CM-050, CM-051).

## Files

- `references/schema-rules.md` — full BB-6xx v1.1, the deltas from v1.0, and the two
  defects in the reference implementation not to copy
- `assets/client-config-template.yaml` — the config shape, filled with a worked example
- `scripts/build_schema.py` — entry gate + emitter
