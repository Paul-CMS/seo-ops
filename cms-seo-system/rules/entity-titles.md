# Entity research, titles, H1, meta

## Entity research (Gate 1 — Paul approves)
ENT-01 Homepage area entity is a true, verifiable statement containing every city served.
ENT-02 Russian Doll method: city → county (Wikipedia) → region named in the county's first sentence → contains ALL served counties? If not, go up a level. Smallest true container wins.
ENT-03 Collect every Wikipedia variant of the area entity (official, abbreviation, common form, regional descriptor).
ENT-04 GB Category entity = primary GBP category, verified on Wikipedia. A close variant with at least 2x the search volume (DataforSEO) may replace it (e.g. "Carpet cleaning service" → "Carpet Cleaning").
ENT-05 Build the variant map before writing. URL → SEO title → H1 → first H2 never use the same variant consecutively.
ENT-06 Entity foundation is approved by Paul before anything else proceeds.
ENT-07 A county can be the area entity when it is the smallest true container (e.g. Polk County).
ENT-08 Local research = one Deep Research run per client (Gemini or ChatGPT), after entity approval. Per city: service-relevant climate/terrain, housing stock/age, permits/codes, 6–12 real neighborhoods, 3 real landmarks/POIs, each with a source URL. Output one file `LR - [Client] - Local Research.md` (one fixed block per city) in the client folder. Claude reads only that file; no re-research.

## SEO titles (never shortened by swapping entity terms; display truncation is not a penalty)
TTL-01 Homepage: `[Brand] - [GB Category] - [Area entity]`
TTL-02 Service page: `[Service] - [Brand] - [Area entity]` (area entity optional)
TTL-03 Location page: `[Service] - [City], [Full State] - [Brand]`
TTL-04 County hub page: `[Service] - [County], [Full State] - [Brand]`
TTL-05 Full state names only.

## H1
H1-01 One H1 per page.
H1-02 The H1 uses different variants than the SEO title. Variants must differ between page TYPES (homepage vs service vs location). Pages of the same type may share one area variant, as long as each page's own title, H1 and first H2 differ.
H1-03 No brand in the H1 (the domain implies it). H1 = [Service variant] + [Area/City variant].
H1-04 "The Best" is a valid AI trigger, used selectively. Use it if ANY is true: (1) main keyword difficulty 30+ in DataforSEO; (2) page ranks positions 4–20; (3) page indexed but not top 20 after 90 days. Otherwise leave it out; on new builds with no data, leave it out and recheck at 90 days.
H1-05 Location page H1: city only, no state ("[The Best] [Service variant] in [City]").
H1-06 Service page H1: area entity, never a city.
H1-07 Every H1 recommendation comes with an approve/reject question plus a better-fit alternative.

## Meta description
META-01 Title, H1 and meta are part of EVERY execution run, including pages routed to the Service Page Optimizer.
META-02 Entity-rich semantic triple in natural language + one conversion line (phone / free estimate). No stuffing. May include one verified differentiator or spec (e.g. "low-moisture cleaning, dry in under an hour") only when confirmed true.
