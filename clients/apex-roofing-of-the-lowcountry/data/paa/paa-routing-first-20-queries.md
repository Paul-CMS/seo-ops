# PAA routing — People Also Ask questions

20 queries (Bluffton, Hilton Head Island, Beaufort, Hardeeville) → 50 distinct questions (deduplicated). Written by scripts/paa.py; **the discovery-audit agent fills Intent and Route** for every row.

Intent: informational · problem-aware · commercial investigation · comparison · transactional.  
Route: **service FAQ** (name the page) · **location FAQ** (name the city page) · **blog topic** · **drop** (off-topic, or already in the C3 registry — similarity ≥ 0.85 is pre-marked).

| # | Question | Seen | Source queries | Closest C3 heading/FAQ | Similarity | Intent | Route | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | What is the 25% rule for roofing? | 12 | roof repair Bluffton / roof replacement Bluffton / roof installation Bluffton / roof inspection Bluffton / emergency roof repair Bluffton / roof repair Hilton Head Island / roof replacement Hilton Head Island / roof installation Hilton Head Island / roof inspection Hilton Head Island / roof repair Beaufort / roof installation Beaufort / roof inspection Beaufort |  | 0.00 | informational | service FAQ — Roof Repair (/roof-repair/) | seen in 12 of 20 queries; the answer needs a cited code source (SC / Beaufort County) — CM-016 |
| 2 | Should a 20 year old roof replace? | 4 | roof replacement Bluffton / roof repair Hilton Head Island / roof repair Beaufort / roof installation Beaufort |  | 0.00 | problem-aware | service FAQ — Roof Replacement (/roof-replacement/) | lead "when to replace" question |
| 3 | Is roof restoration worth it? | 2 | roof repair Bluffton / roof replacement Beaufort |  | 0.00 | comparison | blog topic | restoration is not one of the 8 services |
| 4 | What do you call someone who does roofing? | 2 | roof repair Bluffton / roof replacement Beaufort |  | 0.00 | informational | drop | no service or local intent |
| 5 | What is the average cost of a new roof in South Carolina? | 2 | roof installation Bluffton / roof installation Beaufort |  | 0.00 | commercial investigation | service FAQ — Roof Installation (/roof-installation/) | lead cost question for a new roof; a figure needs a client-confirmed range or [NEED] — CM-016 |
| 6 | Is $50,000 for a new roof good? | 2 | roof installation Bluffton / roof installation Hilton Head Island |  | 0.00 | commercial investigation | blog topic | cluster: "what a new roof costs" guide (with #16 framing, #49) |
| 7 | How to tell if a roofer is lying? | 2 | roof installation Bluffton / roof replacement Beaufort |  | 0.00 | commercial investigation | blog topic | existing post /how-to-spot-and-prevent-common-roofing-scams-a-homeowners-guide/ |
| 8 | How much does a typical roof inspection cost? | 2 | roof inspection Bluffton / roof inspection Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Roof Inspections (/roof-inspections/) | lead cost question (merge #17); price needs Brand Guide D or [NEED] |
| 9 | What is included in a roof inspection? | 2 | roof inspection Bluffton / roof inspection Hilton Head Island |  | 0.00 | informational | service FAQ — Roof Inspections (/roof-inspections/) |  |
| 10 | How much is 1000 sq ft of metal roofing? | 2 | metal roofing Bluffton / metal roofing Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Metal Roofing (/metal-roofing-2/) | merge into one metal cost FAQ with #21, #35, #37 |
| 11 | What is the average price of a roof repair? | 2 | roof repair Hilton Head Island / roof repair Beaufort |  | 0.00 | commercial investigation | service FAQ — Roof Repair (/roof-repair/) | lead cost question; price needs Brand Guide D or [NEED] |
| 12 | What is the lifespan of a roof in South Carolina? | 2 | roof repair Hilton Head Island / roof repair Beaufort |  | 0.00 | informational | blog topic | existing posts /asphalt-shingle-roof-lifespan-coastal-sc/ and /how-long-does-roof-last-hilton-head-humidity-salt-air/ (merge #33) |
| 13 | What is the average cost to replace a roof in South Carolina? | 2 | roof replacement Hilton Head Island / roof installation Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Roof Replacement (/roof-replacement/) | lead cost question (merge #15, #16, #27, #32) |
| 14 | How can I get a new roof if I can't afford it? | 1 | roof repair Bluffton |  | 0.00 | commercial investigation | blog topic | cluster: paying for a roof — financing, grants, insurance (with #28); financing facts need Brand Guide D |
| 15 | What does it typically cost to replace a roof? | 1 | roof replacement Bluffton |  | 0.00 | commercial investigation | service FAQ — Roof Replacement (/roof-replacement/) | merge with #13 |
| 16 | How much does it cost to replace a roof on a $4000 square-foot house? | 1 | roof replacement Bluffton |  | 0.00 | commercial investigation | service FAQ — Roof Replacement (/roof-replacement/) | merge with #13 (size-based cost) |
| 17 | How much does it cost to check a roof? | 1 | roof inspection Bluffton |  | 0.00 | commercial investigation | service FAQ — Roof Inspections (/roof-inspections/) | merge with #8 |
| 18 | Can a roof be repaired in a day? | 1 | emergency roof repair Bluffton |  | 0.00 | informational | service FAQ — Roof Repair (/roof-repair/) |  |
| 19 | How urgent is roof repair? | 1 | emergency roof repair Bluffton |  | 0.00 | problem-aware | service FAQ — Emergency Roof Repair (/emergency-roof-repair/) | lead urgency question |
| 20 | How to do a temporary roof repair? | 1 | emergency roof repair Bluffton |  | 0.00 | problem-aware | service FAQ — Emergency Roof Repair (/emergency-roof-repair/) | "what to do until we arrive" — safety framing; tarping facts need Brand Guide D |
| 21 | How much does a metal roof cost for a 2000 sq ft home? | 1 | metal roofing Bluffton |  | 0.00 | commercial investigation | service FAQ — Metal Roofing (/metal-roofing-2/) | merge with #10 |
| 22 | What is the average price for a 3 ft by 8 ft metal roof? | 1 | metal roofing Bluffton |  | 0.00 | commercial investigation | drop | material sheet pricing (supply / DIY), not installed-roof intent |
| 23 | How much is a 20 ft sheet of metal roofing? | 1 | metal roofing Bluffton |  | 0.00 | commercial investigation | drop | material sheet pricing (supply / DIY) |
| 24 | What is a major disadvantage of a slate roof? | 1 | slate roofing Bluffton |  | 0.00 | comparison | service FAQ — Slate Roofing (/slate-roofing/) |  |
| 25 | How much do slate roofs cost? | 1 | slate roofing Bluffton |  | 0.00 | commercial investigation | service FAQ — Slate Roofing (/slate-roofing/) | lead cost question; fan-out #115 routes with it |
| 26 | Do insurance companies like slate roofs? | 1 | slate roofing Bluffton |  | 0.00 | informational | service FAQ — Slate Roofing (/slate-roofing/) | insurer stance needs a cited source — CM-016 |
| 27 | How much does it cost to replace a roof on a $4000 square foot house? | 1 | slate roofing Bluffton |  | 0.00 | commercial investigation | service FAQ — Roof Replacement (/roof-replacement/) | duplicate wording of #16 (surfaced under a slate query); merge with #13 |
| 28 | Can I get a grant to replace my roof in South Carolina? | 1 | roof replacement Hilton Head Island |  | 0.00 | commercial investigation | blog topic | with #14; any programme named needs a cited source |
| 29 | How much does it cost to replace a roof on a 2000 square-foot house with hip roof in Texas? | 1 | roof replacement Hilton Head Island |  | 0.00 | commercial investigation | drop | Texas — outside the service area |
| 30 | What is the average cost to put on a roof? | 1 | roof installation Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Roof Installation (/roof-installation/) | merge with #5 |
| 31 | How long should a roof inspection take? | 1 | roof inspection Hilton Head Island |  | 0.00 | informational | service FAQ — Roof Inspections (/roof-inspections/) | fan-out #110 routes with it |
| 32 | How much does it cost to replace a roof in SC? | 1 | emergency roof repair Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Roof Replacement (/roof-replacement/) | merge with #13 |
| 33 | How long does a roof last in South Carolina? | 1 | emergency roof repair Hilton Head Island |  | 0.00 | informational | blog topic | merge with #12 (existing lifespan posts) |
| 34 | Who can I call for an emergency roofing service in Manchester? | 1 | emergency roof repair Hilton Head Island |  | 0.00 | transactional | drop | Manchester — outside the service area |
| 35 | How much does a metal roof cost for a 2000 sq ft house? | 1 | metal roofing Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Metal Roofing (/metal-roofing-2/) | merge with #10 |
| 36 | What is the average price for a 3 ft by 10 ft metal roof? | 1 | metal roofing Hilton Head Island |  | 0.00 | commercial investigation | drop | material sheet pricing (supply / DIY) |
| 37 | How much does a metal roof cost in South Carolina? | 1 | metal roofing Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — Metal Roofing (/metal-roofing-2/) | lead metal cost question (merge #10, #21, #35) |
| 38 | What does slate roofing look like? | 1 | slate roofing Hilton Head Island |  | 0.00 | informational | drop | image-led query, no FAQ answer |
| 39 | What famous people live on Hilton Head Island? | 1 | slate roofing Hilton Head Island |  | 0.00 | informational | drop | tourism, off-topic |
| 40 | Do slate roofs need a membrane? | 1 | slate roofing Hilton Head Island |  | 0.00 | informational | service FAQ — Slate Roofing (/slate-roofing/) | underlayment question |
| 41 | What is cheaper, a slate or tile roof? | 1 | slate roofing Hilton Head Island |  | 0.00 | comparison | blog topic | cluster: slate vs tile vs metal comparison (fan-out #180, #361) |
| 42 | What celebs live in Hilton Head? | 1 | skylights Hilton Head Island |  | 0.00 | informational | drop | tourism, off-topic |
| 43 | What is the prettiest beach on Hilton Head Island? | 1 | skylights Hilton Head Island |  | 0.00 | informational | drop | tourism, off-topic |
| 44 | What is the best month to go to Hilton Head Island? | 1 | skylights Hilton Head Island |  | 0.00 | informational | drop | tourism, off-topic |
| 45 | Where is the best place to watch the sunrise on Hilton Head Island? | 1 | skylights Hilton Head Island |  | 0.00 | informational | drop | tourism, off-topic |
| 46 | Do Lowes do roof replacement? | 1 | roof replacement Beaufort |  | 0.00 | comparison | blog topic | big-box vs local roofer; fits existing post /questions-to-ask-roofing-contractor-hilton-head/ |
| 47 | How much does it cost to replace a roof on a 2 200 square foot house in California? | 1 | roof installation Beaufort |  | 0.00 | commercial investigation | drop | California — outside the service area |
| 48 | Who inspects roofs for damage? | 1 | roof inspection Beaufort |  | 0.00 | informational | service FAQ — Roof Inspections (/roof-inspections/) |  |
| 49 | Is $30,000 too much for a roof? | 1 | roof inspection Beaufort |  | 0.00 | commercial investigation | blog topic | with #6 ("what a new roof costs" guide) |
| 50 | Are roof repair estimates free? | 1 | roof inspection Beaufort |  | 0.00 | commercial investigation | service FAQ — Roof Repair (/roof-repair/) | answer needs Brand Guide D "Free estimate — and what free means" — CM-016 |

## Routing summary (discovery-audit agent, 2026-10-07 · run 20261007-154441-discovery-64db)

Planning input for the site plan and blog topic list — not findings, no priorities.

| Route | Questions |
|---|---|
| service FAQ | 27 — Roof Replacement 6 · Roof Inspections 5 · Roof Repair 4 · Metal Roofing 4 · Slate Roofing 4 · Roof Installation 2 · Emergency Roof Repair 2 · Skylights 0 |
| location FAQ | 0 — no PAA question was city-specific except Hilton Head Island tourism questions (dropped) |
| blog topic | 10 — clusters: roof cost guide (#6, #49), paying for a roof (#14, #28), roof lifespan (#12, #33, existing posts), choosing a roofer / scams (#7, #46, existing posts), material comparison (#41), restoration (#3) |
| drop | 13 — tourism (6), outside the service area: Texas, California, Manchester (3), material-sheet pricing (3), no intent (1) |

- Brand Guide C3 is empty, so no C3 duplicates were dropped.
- Many cost questions merge into one FAQ per page (notes say which). Any figure or "free estimate" answer needs a Brand Guide D fact or `[NEED: …]` (CM-016).
- Hardeeville replaced Okatie as the fourth city (DataforSEO has no Okatie location); no Beaufort- or Hardeeville-specific questions surfaced.
- Skylights Bluffton returned no PAA box.
