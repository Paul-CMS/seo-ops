# PAA routing — People Also Ask questions

20 queries (Hilton Head Island, Bluffton, Beaufort, Ridgeland) → 15 distinct questions (deduplicated). Written by scripts/paa.py; Intent and Route are filled by `paa.py route` (llm.py), or by the discovery-audit agent when there is no API key.

Intent: informational · problem-aware · commercial investigation · comparison · transactional.  
Route: **service FAQ** (name the page) · **location FAQ** (name the city page) · **blog topic** · **drop** (off-topic, or already in the C3 registry — similarity ≥ 0.85 is pre-marked).

| # | Question | Seen | Source queries | Closest C3 heading/FAQ | Similarity | Intent | Route | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Can I use Dawn dish soap to clean a wool rug? | 2 | oriental rug cleaning Hilton Head Island / area rug cleaning Hilton Head Island |  | 0.00 | informational | blog topic | DIY care for wool rugs; one post with #3 (dish soap on rugs and upholstery) |
| 2 | How do I get brown stains out of my carpet? | 1 | upholstery cleaning Hilton Head Island |  | 0.00 | problem-aware | service FAQ — Carpet Stain Removal | brown stains / browning after cleaning |
| 3 | Can I use Dawn dish soap to clean upholstery? | 1 | upholstery cleaning Hilton Head Island |  | 0.00 | informational | blog topic | goes with #1 (dish soap DIY post) |
| 4 | How do I clean an upholstered headboard? | 1 | upholstery cleaning Hilton Head Island |  | 0.00 | informational | blog topic | DIY headboard care; whether the client cleans headboards is not in the facts |
| 5 | Does Stanley Steemer clean upholstery? | 1 | upholstery cleaning Hilton Head Island |  | 0.00 | comparison | drop | names a competitor brand |
| 6 | How much does it cost to have hardwood floors cleaned? | 1 | hardwood floor cleaning Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Hardwood Floor Cleaning | the answer needs the client's own pricing, which is not in the facts |
| 7 | Is professional hardwood floor cleaning worth it? | 1 | hardwood floor cleaning Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Hardwood Floor Cleaning |  |
| 8 | Do Stanley Steemer clean hardwood floors? | 1 | hardwood floor cleaning Hilton Head Island |  | 0.00 | comparison | drop | names a competitor brand |
| 9 | What is the best way to deep clean my hardwood floors? | 1 | hardwood floor cleaning Hilton Head Island |  | 0.00 | informational | blog topic | DIY hardwood care |
| 10 | Can you use a carpet cleaner on an oriental rug? | 1 | oriental rug cleaning Hilton Head Island |  | 0.00 | problem-aware | service FAQ — Oriental Rug Cleaning |  |
| 11 | How much does it cost to have an oriental rug cleaned? | 1 | oriental rug cleaning Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Oriental Rug Cleaning | the answer needs the client's own pricing, which is not in the facts |
| 12 | How much does it cost to pay someone to clean carpet? | 1 | oriental rug cleaning Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Carpet Cleaning | the answer needs the client's own pricing, which is not in the facts |
| 13 | Can you carpet clean an area rug? | 1 | area rug cleaning Hilton Head Island |  | 0.00 | problem-aware | service FAQ — Area Rug Cleaning |  |
| 14 | What does Mrs. Hinch use to clean carpets? | 1 | area rug cleaning Hilton Head Island |  | 0.00 | informational | drop | about a UK celebrity cleaner, off-topic |
| 15 | How much does it cost to wash an 8x10 rug? | 1 | area rug cleaning Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Area Rug Cleaning | the answer needs the client's own pricing, which is not in the facts |
