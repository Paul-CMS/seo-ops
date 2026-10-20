# PAA routing — People Also Ask questions

20 queries (Beaufort, Charleston, Hilton Head Island, Bluffton) → 35 distinct questions (deduplicated). Written by scripts/paa.py; **the discovery-audit agent fills Intent and Route** for every row.

Intent: informational · problem-aware · commercial investigation · comparison · transactional.  
Route: **service FAQ** (name the page) · **location FAQ** (name the city page) · **blog topic** · **drop** (off-topic, or already in the C3 registry — similarity ≥ 0.85 is pre-marked).

| # | Question | Seen | Source queries | Closest C3 heading/FAQ | Similarity | Intent | Route | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | What is the average cost of a curved stairlift? | 3 | curved stair lifts Beaufort / curved stair lifts Charleston / curved stair lifts Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — /services/curved-stair-lifts/ | price answer needs client figures [NEED] |
| 2 | What is the best stairlift for curved stairs? | 3 | curved stair lifts Beaufort / curved stair lifts Charleston / curved stair lifts Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — /services/curved-stair-lifts/ | answer only with brands/models in Brand Guide D |
| 3 | How much does it cost to repair a stair lift? | 3 | stair lift repair Beaufort / stair lift repair Charleston / stair lift repair Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — /services/stair-lift-repair/ | price answer needs client figures [NEED] |
| 4 | Is there an alternative to a stair lift? | 2 | stair lifts Beaufort / stair lifts Charleston |  | 0.00 | comparison | blog topic | alternatives to a stair lift; absorbs #31, #34 |
| 5 | What is the average price of a curved stairlift? | 2 | curved stair lifts Beaufort / curved stair lifts Charleston |  | 0.00 | commercial investigation | drop | duplicate of #1 |
| 6 | Will Medicare pay for a chairlift for stairs? | 2 | curved stair lifts Beaufort / curved stair lifts Hilton Head Island |  | 0.00 | informational | blog topic | existing post /are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/ (ranks #2); absorbs #14, #23, #30 |
| 7 | What are the best brands of wheelchair lifts? | 2 | wheelchair lifts Beaufort / wheelchair lifts Charleston |  | 0.00 | comparison | service FAQ — /services/wheelchair-lifts/ | answer only with brands in Brand Guide D |
| 8 | How often should a stairlift be serviced? | 2 | stair lift repair Beaufort / stair lift repair Charleston |  | 0.00 | informational | service FAQ — /services/stair-lift-repair/ |  |
| 9 | What is the average cost of stair lifts? | 2 | stair lifts Charleston / stair lifts Hilton Head Island |  | 0.00 | commercial investigation | service FAQ — /services/stair-lifts/ | price answer needs client figures [NEED] |
| 10 | Do they make chair lifts for curved stairs? | 2 | curved stair lifts Charleston / curved stair lifts Hilton Head Island |  | 0.00 | problem-aware | service FAQ — /services/curved-stair-lifts/ |  |
| 11 | What is the shuttle service in Charleston, SC? | 2 | porch lifts Charleston / wheelchair lifts Charleston |  | 0.00 | informational | drop | off-topic (Charleston shuttle) |
| 12 | What should I do if my stairlift has stopped working? | 2 | stair lift repair Charleston / stair lift repair Hilton Head Island |  | 0.00 | problem-aware | service FAQ — /services/stair-lift-repair/ |  |
| 13 | What is the average lifespan of a stairlift? | 2 | stair lift repair Charleston / stair lift repair Hilton Head Island |  | 0.00 | informational | service FAQ — /services/stair-lift-repair/ |  |
| 14 | Is a stair chair lift covered by Medicare? | 2 | stair lifts Hilton Head Island / stair lift repair Hilton Head Island |  | 0.00 | informational | drop | duplicate of #6 |
| 15 | What are the downsides of having a stair lift? | 1 | stair lifts Beaufort |  | 0.00 | comparison | blog topic | pros and cons of a stair lift; absorbs #24 |
| 16 | What is the name of the airport in Beaufort, South Carolina? | 1 | stair lifts Beaufort |  | 0.00 | informational | drop | off-topic (airport) |
| 17 | Who are the major manufacturers of stair lifts? | 1 | stair lifts Beaufort |  | 0.00 | comparison | service FAQ — /services/stair-lifts/ | answer only with brands in Brand Guide D |
| 18 | What is the best wheelchair lift for the back of a van? | 1 | wheelchair lifts Beaufort |  | 0.00 | commercial investigation | drop | vehicle wheelchair lifts are not a confirmed service (Brand Guide D) |
| 19 | What are the different types of wheelchair lifts? | 1 | wheelchair lifts Beaufort |  | 0.00 | informational | service FAQ — /services/wheelchair-lifts/ |  |
| 20 | What are some good electric wheelchair lifts for home use? | 1 | wheelchair lifts Beaufort |  | 0.00 | commercial investigation | service FAQ — /services/wheelchair-lifts/ |  |
| 21 | How to troubleshoot a stair lift? | 1 | stair lift repair Beaufort |  | 0.00 | problem-aware | blog topic | troubleshooting guide; repair page FAQ #12 covers the call-us answer |
| 22 | How do I get a stair lift for free? | 1 | stair lift repair Beaufort |  | 0.00 | informational | blog topic | funding and assistance; pairs with the Medicare post (#6) |
| 23 | How much does Medicare pay for a stair lift? | 1 | stair lifts Charleston |  | 0.00 | informational | drop | duplicate of #6 |
| 24 | What are the disadvantages of stairlifts? | 1 | stair lifts Charleston |  | 0.00 | comparison | drop | duplicate of #15 |
| 25 | Why are people leaving Charleston, SC? | 1 | porch lifts Charleston |  | 0.00 | informational | drop | off-topic |
| 26 | What are porches called in Charleston, SC? | 1 | porch lifts Charleston |  | 0.00 | informational | drop | off-topic |
| 27 | Is there free parking for disabled people in Charleston, SC? | 1 | porch lifts Charleston |  | 0.00 | informational | drop | off-topic |
| 28 | Is Charleston, SC wheelchair friendly? | 1 | wheelchair lifts Charleston |  | 0.00 | informational | drop | off-topic (travel) |
| 29 | Are wheelchair lifts ADA compliant? | 1 | wheelchair lifts Charleston |  | 0.00 | informational | service FAQ — /services/wheelchair-lifts/ | health-adjacent/regulatory: cite an authoritative source (CM-040) |
| 30 | Does Medicare pay for a stair lift for seniors? | 1 | stair lifts Hilton Head Island |  | 0.00 | informational | drop | duplicate of #6 |
| 31 | What can seniors do instead of a stair lift? | 1 | stair lifts Hilton Head Island |  | 0.00 | comparison | drop | duplicate of #4 |
| 32 | How much does a porch elevator cost? | 1 | porch lifts Bluffton |  | 0.00 | commercial investigation | service FAQ — /services/porch-lifts/ | price answer needs client figures [NEED] |
| 33 | Will Medicare pay for a platform lift? | 1 | porch lifts Bluffton |  | 0.00 | informational | blog topic | fold into the Medicare post (#6) as a platform-lift section |
| 34 | What is an alternative to lift in a house? | 1 | porch lifts Bluffton |  | 0.00 | comparison | drop | duplicate of #4 |
| 35 | What are the common problems with home lifts? | 1 | porch lifts Bluffton |  | 0.00 | problem-aware | service FAQ — /services/stair-lift-repair/ | only if lift repair beyond stair lifts is confirmed (Brand Guide D: 'any stair lift or lift') |


## Routing summary (discovery-audit agent, 2026-10-07)

- 35 questions: **15 service FAQ** · **0 location FAQ** · **6 blog topic** · **14 drop** (8 off-topic or out of scope, 6 duplicates within the list).
- No city-specific question surfaced: the Charleston PAA rows are tourism/off-topic, so no location FAQ is routed from PAA.
- C3 registry is empty, so nothing was dropped as a C3 duplicate.
- Cost answers need the client's figures; nothing is stated without Brand Guide D (CM-016).
