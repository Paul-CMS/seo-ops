# Site architecture, link wheel, URLs

ARC-01 Homepage = brand hub for the area entity; E-E-A-T trust and gateway to service and location pages. Introduces service silos via H3 links only; does not describe services.
ARC-02 Service pages: one per primary service, the depth pages; link to ALL location pages via the service areas table.
ARC-03 Location pages: one per city, lean, conversion-focused; link to ALL service pages; never re-describe services.
ARC-04 County hub pages are kept. Each links down to every city in its county; those cities link back up.
ARC-05 Blog = supporting content only; never targets the same entity + location as a service or location page.
WHL-01 Link wheel complete both ways: service → every location, location → every service, as H3 anchor links. One direction only = broken.
WHL-02 Every location page links to every other location page except itself (sibling table).
WHL-03 Bradley rules govern service/location linking. The link-strategy skill applies to blogs and high-value outbound / anchor exceptions only.
PG-01 Sub-services (variants, components, sub-tasks) are H2 sections on the main service page. Own page only with an independent Wikipedia entity AND distinct buyer intent.
PG-02 Service+city combination pages are prohibited.
PG-03 Hub pages like /services/ and /service-area/ are not indexed: 301 to homepage or delete.
URL-01 Root-proximate: /[service]/ and /[city]/. Strip /service/ and /service-area/ prefixes.
URL-02 No city names in service URLs; no service names in location URLs.
URL-03 Short, clean, entity-relevant slugs. No "best-", no city stuffing.
URL-04 A live URL never ends in -2 (or any -N).

## H tags and the 500-token rule
HT-01 Every H2 section (heading + content to next H2) is under 500 tokens (~375 words).
HT-02 Raise AI chunk retrieval with tables/lists, H3 question + paragraph answers, verifiable entities, schema.
HT-03 No H tags in nav, footer or sidebar. HT-04 Never use H tags for styling. HT-05 H3s are subtopics of their H2; never skip levels.
HT-06 Title, H1, first H2: three different variants. HT-07 Cross-links between service and location pages are H3 anchor links.
HT-08 FAQs: H3 question + paragraph answer. HT-09 No city names in service page H tags.
HT-10 Trust-section items and How It Works steps are styled cards/bold text, not H tags.
