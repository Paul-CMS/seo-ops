# Niche modules (Rewrite 4, Phase 6)

One folder per niche (the client's niche slug: the GBP primary category's trade), reused by every client in it. The
research layers (REWRITE-4-PLAN.md §3): **niche** (this folder, once per niche) → **place** (`methodology/places/`,
once per town) → **place × niche** (once per pair) → **brand** (`scripts/footprint.py`, once per client).

| File | What | Who writes it |
|---|---|---|
| `angles.md` | The niche module for the place prompt (Prompt B): five full-depth angles and three lite angles (local cost or decision · logistics in this area · trust in this area), with the `Aliases:` line that maps a client's niche slug to this folder | By hand, once per niche |
| `entities.json` | Service entities (Wikipedia/Wikidata, variants, parent/child, kind), attributes, state licensing and programmes, official FAQs — every fact sourced, verified, dated | `niches.py ingest` from a Prompt A report; never by hand |

## `angles.md` format

```
# <Niche name>
Aliases: slug-one, slug-two          (client niche slugs this folder serves)

## Full-depth angles                 (3 to 5, numbered 1, 2, 3 …)
### 1. <Title — may use {PLACE} {STATE} {COUNTY} {NICHE} {YEAR}>
- what to look for, official sources first
## Lite angles                       (exactly 3, numbered 1-3)
### 1. Local cost or decision
### 2. Logistics in this area
### 3. Trust in this area
```

Angles 1, 2, 3 and 5 of a full run route to the place × niche layer, 4 by relevance; the fixed angles 6 (places and
entities), 7 (identity) and 8 (local questions) are added by `places.py prompt`. A missing or malformed `angles.md`
refuses the prompt — a place prompt is never built from another trade's angles.

Commands: `python3 scripts/niches.py --help` · `python3 scripts/places.py --help` · `python3 scripts/footprint.py --help`.
