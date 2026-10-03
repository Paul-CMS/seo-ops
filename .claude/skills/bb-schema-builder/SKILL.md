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

## Build

```bash
python3 scripts/build_schema.py <client.yaml> <out_dir>            # all pages
python3 scripts/build_schema.py <client.yaml> <out_dir> --page URL # one page
```

Then validate each file at `validator.schema.org` before implementation. The script emits
structurally correct JSON-LD; it does not check that the facts inside are true.

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

## Files

- `references/schema-rules.md` — full BB-6xx v1.1, the deltas from v1.0, and the two
  defects in the reference implementation not to copy
- `assets/client-config-template.yaml` — the config shape, filled with a worked example
- `scripts/build_schema.py` — entry gate + emitter
