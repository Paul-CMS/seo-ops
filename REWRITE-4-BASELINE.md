# REWRITE-4 baseline — what the current route costs

_Generated 2026-10-21 by `python3 scripts/usage.py baseline home-mobile-medical apex-roofing-of-the-lowcountry` from Claude Code's transcripts, priced with `scripts/model_prices.json` (cache-write prices inferred). Do not edit by hand — regenerate. A run with no session id or no transcript on this Mac is counted as a run but has no cost (unmeasured); the totals are therefore a floor._

## home-mobile-medical

**$44.44** measured over 21 of 29 run(s); 108,289,180 tokens (input + cache write + cache read + output).

### Cost per stage

| Stage | Runs measured | Tokens | USD |
|---|---|---|---|
| batches | 14 of 15 | 72,655,205 | $32.22 |
| build-plan | 3 of 3 | 22,746,976 | $8.01 |
| audit | 1 of 2 | 8,879,741 | $3.11 |
| any | 3 of 7 | 4,007,258 | $1.10 |
| setup | 0 of 1 | 0 | $0.00 |
| data | 0 of 1 | 0 | $0.00 |

### Cost per step

| Step | Runs measured | Tokens | USD |
|---|---|---|---|
| build:write | 3 of 3 | 52,766,073 | $24.94 |
| build:facts | 2 of 2 | 18,811,270 | $6.45 |
| build:draft | 4 of 4 | 7,719,847 | $3.24 |
| discovery:audit | 1 of 2 | 8,879,741 | $3.11 |
| build:writeback | 2 of 2 | 3,559,125 | $1.63 |
| build:blockers | 1 of 1 | 3,935,706 | $1.55 |
| build:review | 3 of 3 | 3,302,838 | $1.42 |
| build:drafts | 1 of 2 | 2,999,753 | $0.96 |
| build:pilot-corrections | 2 of 2 | 2,252,967 | $0.71 |
| drive-mirror | 1 of 3 | 1,754,291 | $0.39 |
| interview:facts-answers | 1 of 1 | 2,307,569 | $0.04 |
| new-client | 0 of 1 | 0 | $0.00 |
| wp-check | 0 of 2 | 0 | $0.00 |
| discovery:data | 0 of 1 | 0 | $0.00 |

### Cost by agent

_main = the stage chat itself; every other row is a subagent, named by its agent type._

| Agent | Runs | Transcripts | Tokens | USD | Models |
|---|---|---|---|---|---|
| build | 16 | 35 | 63,852,238 | $34.60 | claude-opus-5-5 $34.60 |
| brief-writer | 3 | 18 | 8,331,179 | $4.34 | claude-sonnet-5-5 $4.34 |
| discovery-audit | 1 | 1 | 7,609,449 | $2.53 | claude-opus-5-5 $2.53 |
| researcher | 1 | 5 | 4,667,505 | $1.69 | claude-sonnet-5-5 $1.69 |
| main | 21 | 21 | 23,828,809 | $1.28 | claude-opus-5-5 $0.97, claude-haiku-5-5 $0.31 |

### Ten dearest runs

| Run | Step | Tokens | USD | Models |
|---|---|---|---|---|
| 20261014-215429-build-9289 | build:write | 21,616,186 | $15.15 | claude-opus-5-5 $12.05, claude-sonnet-5-5 $3.10, claude-haiku-5-5 $0.00 |
| 20261014-100458-build-2be7 | build:facts | 15,091,794 | $5.56 | claude-opus-5-5 $3.85, claude-sonnet-5-5 $1.69, claude-haiku-5-5 $0.01 |
| 20261014-125319-build-9170 | build:write | 16,200,305 | $5.22 | claude-opus-5-5 $4.63, claude-sonnet-5-5 $0.53, claude-haiku-5-5 $0.06 |
| 20261014-144852-build-6004 | build:write | 14,949,582 | $4.57 | claude-opus-5-5 $3.77, claude-sonnet-5-5 $0.71, claude-haiku-5-5 $0.09 |
| 20261009-071238-discovery-94fa | discovery:audit | 8,879,741 | $3.11 | claude-opus-5-5 $3.11 |
| 20261009-122052-build-8f9c | build:blockers | 3,935,706 | $1.55 | claude-opus-5-5 $1.55, claude-haiku-5-5 $0.00 |
| 20261014-163404-build-b049 | build:draft | 2,010,781 | $0.98 | claude-opus-5-5 $0.98, claude-haiku-5-5 $0.01 |
| 20261014-164325-build-3b84 | build:drafts | 2,999,753 | $0.96 | claude-opus-5-5 $0.96, claude-haiku-5-5 $0.01 |
| 20261014-140654-build-4002 | build:facts | 3,719,476 | $0.90 | claude-opus-5-5 $0.87, claude-haiku-5-5 $0.03 |
| 20261014-211328-build-a865 | build:writeback | 1,733,990 | $0.85 | claude-opus-5-5 $0.84, claude-haiku-5-5 $0.01 |

Unmeasured runs (8): 20261006-112201-new-client-fb9a, 20261007-172152-wp-check-12e0, 20261007-172720-wp-check-bb94, 20261007-172819-drive-mirror-bbb0, 20261007-173133-discovery-dce1, 20261007-203219-discovery-784c, 20261009-201533-drive-mirror-0325, 20261014-144522-build-adbe

## apex-roofing-of-the-lowcountry

**$122.00** measured over 68 of 102 run(s); 334,391,946 tokens (input + cache write + cache read + output).

### Cost per stage

| Stage | Runs measured | Tokens | USD |
|---|---|---|---|
| batches | 62 of 65 | 296,075,557 | $105.93 |
| build-plan | 3 of 3 | 25,647,934 | $12.07 |
| any | 3 of 15 | 12,668,455 | $3.99 |
| setup | 0 of 1 | 0 | $0.00 |
| discovery | 0 of 10 | 0 | $0.00 |
| data | 0 of 3 | 0 | $0.00 |
| audit | 0 of 5 | 0 | $0.00 |

### Cost per step

| Step | Runs measured | Tokens | USD |
|---|---|---|---|
| build:brief | 11 of 11 | 122,807,397 | $42.44 |
| build:draft | 25 of 26 | 89,327,811 | $34.97 |
| build:drafts | 5 of 5 | 24,430,577 | $8.15 |
| build:plan | 1 of 1 | 14,473,183 | $7.37 |
| build:write | 1 of 1 | 19,467,148 | $6.49 |
| build:apply-sem | 5 of 5 | 13,385,340 | $4.50 |
| build:writeback | 3 of 3 | 8,923,904 | $4.45 |
| build:pilot-corrections | 2 of 2 | 8,265,855 | $3.02 |
| build:blockers | 1 of 1 | 4,639,872 | $2.53 |
| build:evidence | 2 of 2 | 4,912,282 | $2.34 |
| build:facts | 1 of 1 | 6,534,879 | $2.17 |
| build:ship | 5 of 5 | 6,361,107 | $2.09 |
| drive-mirror | 1 of 9 | 4,402,600 | $0.97 |
| build:review | 1 of 1 | 1,367,525 | $0.43 |
| interview:facts-answers | 3 of 5 | 4,753,832 | $0.07 |
| build:handoff | 1 of 1 | 338,634 | $0.01 |
| new-client | 0 of 1 | 0 | $0.00 |
| wp-check | 0 of 3 | 0 | $0.00 |
| discovery:discovery | 0 of 5 | 0 | $0.00 |
| discovery:proof-sheet | 0 of 5 | 0 | $0.00 |
| discovery:sheet-returned | 0 of 1 | 0 | $0.00 |
| crawl | 0 of 1 | 0 | $0.00 |
| discovery:data | 0 of 2 | 0 | $0.00 |
| discovery:audit | 0 of 2 | 0 | $0.00 |
| discovery:reconcile | 0 of 2 | 0 | $0.00 |
| discovery:signoff | 0 of 1 | 0 | $0.00 |

### Cost by agent

_main = the stage chat itself; every other row is a subagent, named by its agent type._

| Agent | Runs | Transcripts | Tokens | USD | Models |
|---|---|---|---|---|---|
| build | 60 | 67 | 265,223,585 | $105.56 | claude-opus-5-5 $105.56 |
| main | 66 | 66 | 44,213,879 | $7.39 | claude-opus-5-5 $6.34, claude-haiku-4-5-20251001 $0.70, claude-haiku-5-5 $0.35 |
| researcher | 6 | 11 | 19,186,430 | $5.94 | claude-sonnet-5-5 $5.94 |
| brief-writer | 1 | 11 | 5,508,547 | $3.06 | claude-sonnet-5-5 $3.06 |
| clerk | 3 | 3 | 259,505 | $0.05 | claude-haiku-4-5-20251001 $0.05, claude-haiku-5-5 $0.00 |

### Ten dearest runs

| Run | Step | Tokens | USD | Models |
|---|---|---|---|---|
| 20261012-205526-build-9baf | build:brief | 52,728,946 | $13.18 | claude-opus-5-5 $11.89, claude-sonnet-5-5 $1.29 |
| 20261012-150859-build-1044 | build:brief | 30,355,064 | $11.67 | claude-sonnet-5-5 $6.61, claude-opus-5-5 $5.03, claude-haiku-5-5 $0.03 |
| 20261008-134424-build:plan-c61b | build:plan | 14,473,183 | $7.37 | claude-opus-5-5 $7.26, claude-haiku-4-5-20251001 $0.11 |
| 20261013-160308-build-074c | build:write | 19,467,148 | $6.49 | claude-opus-5-5 $6.44, claude-haiku-5-5 $0.06 |
| 20261013-133740-build-53f3 | build:drafts | 17,860,104 | $5.04 | claude-opus-5-5 $5.04 |
| 20261008-150539-build-a2ae | build:brief | 4,601,751 | $3.51 | claude-opus-5-5 $3.29, claude-haiku-4-5-20251001 $0.22 |
| 20261013-140538-build-1832 | build:brief | 9,326,726 | $3.07 | claude-opus-5-5 $2.97, claude-sonnet-5-5 $0.10, claude-haiku-5-5 $0.00 |
| 20261008-131822-build:blockers-b359 | build:blockers | 4,639,872 | $2.53 | claude-opus-5-5 $2.25, claude-haiku-4-5-20251001 $0.28 |
| 20261013-130728-build-8ef0 | build:draft | 7,352,137 | $2.28 | claude-opus-5-5 $2.28 |
| 20261012-213607-build-27a0 | build:writeback | 3,305,444 | $2.21 | claude-opus-5-5 $2.21 |

Unmeasured runs (34): 20261005-210907-new-client-b5e9, 20261005-211116-wp-check-0f33, 20261005-211145-drive-mirror-3ea9, 20261005-211303-discovery-aee7, 20261005-212655-drive-mirror-c34f, 20261005-215259-discovery-acd3, 20261005-221139-discovery-5ddf, 20261005-221818-wp-check-1c23, 20261005-223142-wp-check-24f5, 20261005-223335-discovery-40fe, 20261005-223638-drive-mirror-d324, 20261006-085120-drive-mirror-4406, 20261006-085141-discovery-bb0e, 20261006-104753-discovery-44eb, 20261007-144926-discovery-20d6, 20261007-151404-discovery-f9a6, 20261007-151906-discovery-3a31, 20261007-152000-discovery-9b0e, 20261007-152058-drive-mirror-c605, 20261007-152559-crawl-0206, 20261007-154441-discovery-64db, 20261007-170552-discovery-4092, 20261007-194242-discovery-9495, 20261008-073331-discovery-a866, 20261008-073627-discovery-2c41, 20261008-074416-drive-mirror-b726, 20261008-075515-discovery-24a2, 20261008-080806-discovery-b736, 20261008-104054-discovery-3010, 20261008-110342-drive-mirror-7c9f, 20261009-123816-build-2c02, 20261009-201529-drive-mirror-043d, 20261012-073051-interview-f000, 20261012-114352-interview-44aa

---
**All clients: $166.44**

## Phase 7 — governance size, before (a92f6cf) and after

_`python3 scripts/usage.py reads --before a92f6cf`. Read list = the stage doc + the step's system files (methodology, docs, skills, templates, `rulings.py` output by ID, commands run), in KB; client files are the job's input and are left out. Targets: read list < 30 KB, agent file < 12 KB. A file named with a section note still counts whole, so every figure is a ceiling._

### Agent files

| Agent | Before KB | After KB |
|---|---|---|
| discovery-audit | 20.9 | 5.2 |
| build | 13.3 | 4.8 |
| blog | 8.8 | 8.8 |
| researcher | 7.2 | 7.2 |
| finish | 6.1 | 6.1 |
| audit-reviewer | 5.8 | 5.8 |
| brief-writer | 3.4 | 3.4 |
| draft-writer | 3.0 | 3.0 |
| finish-qa | 2.5 | 2.5 |

### Read list per step

| Step | Read list before KB | after KB | Agent file before KB | after KB |
|---|---|---|---|---|
| build:plan | 80.5 | 73.3 ⚠ | 13.3 | 4.8 |
| discovery:discovery | 66.2 | 27.1 | 20.9 | 5.2 |
| blog:intake | 54.0 | 15.0 | 20.9 | 5.2 |
| build:blockers | 51.3 | 6.3 | 13.3 | 4.8 |
| implement:safe | 49.1 | 1.7 | 0.0 | 0.0 |
| implement:structural | 49.1 | 1.7 | 0.0 | 0.0 |
| build:write | 45.0 | 46.9 ⚠ | 13.3 | 4.8 |
| build:brief | 37.4 | 24.3 | 13.3 | 4.8 |
| build:drafts | 34.6 | 34.7 ⚠ | 13.3 | 4.8 |
| build:evidence | 34.2 | 25.9 | 13.3 | 4.8 |
| build:draft | 33.5 | 33.6 ⚠ | 13.3 | 4.8 |
| build:apply-sem | 30.3 | 30.4 ⚠ | 13.3 | 4.8 |
| blog:next | 28.3 | 28.3 | 8.8 | 8.8 |
| build:pilot-corrections | 26.0 | 26.0 | 0.0 | 0.0 |
| discovery:data | 23.3 | 25.4 | 7.2 | 7.2 |
| discovery:audit | 21.1 | 24.3 | 20.9 | 5.8 |
| build:facts | 20.4 | 22.8 | 7.2 | 7.2 |
| interview:facts | 19.1 | 16.4 | 13.3 | 4.8 |
| build:review | 18.6 | 12.1 | 13.3 | 4.8 |
| interview:stories-answers | 18.5 | 17.5 | 8.8 | 8.8 |
| interview:stories | 18.2 | 17.2 | 8.8 | 8.8 |
| discovery:proof-sheet | 18.1 | 20.9 | 20.9 | 5.2 |
| build:published | 17.9 | 22.1 | 13.3 | 4.8 |
| interview:facts-answers | 17.9 | 17.0 | 13.3 | 4.8 |
| discovery:reconcile | 17.3 | 20.5 | 20.9 | 5.2 |
| interview:voice | 16.4 | 15.4 | 8.8 | 8.8 |
| drive-mirror | 14.2 | 14.2 | 0.0 | 0.0 |
| new-client | 13.2 | 13.2 | 0.0 | 0.0 |
| blog:map | 12.9 | 12.9 | 8.8 | 8.8 |
| discovery:fanout | 12.2 | 14.3 | 7.2 | 7.2 |
| wp-check | 7.6 | 7.6 | 0.0 | 0.0 |
| wp-check:pilot | 7.6 | 7.6 | 0.0 | 0.0 |
| crawl | 7.5 | 9.6 | 7.2 | 7.2 |
| finish:qa | 6.9 | 6.9 | 6.1 | 6.1 |
| blog:refresh | 5.7 | 5.7 | 8.8 | 8.8 |
| discovery:review | 4.7 | 7.9 | 20.9 | 5.2 |
| build:writeback | 4.2 | 8.5 | 13.3 | 4.8 |
| build:handoff | 4.2 | 8.5 | 13.3 | 4.8 |
| build:ship | 4.2 | 8.5 | 13.3 | 4.8 |
| implement:wheel | 1.5 | 1.5 | 6.1 | 6.1 |
| implement:schema | 1.5 | 1.5 | 6.1 | 6.1 |
| blog:topics | 1.2 | 1.2 | 8.8 | 8.8 |
| discovery:facts-direct | 0.9 | 3.8 | 20.9 | 5.2 |
| blog:redirects | 0.7 | 0.7 | 8.8 | 8.8 |
| blog:publish | 0.7 | 0.7 | 8.8 | 8.8 |
| verify | 0.0 | 0.0 | 0.0 | 0.0 |
| rollback | 0.0 | 0.0 | 0.0 | 0.0 |
| implement:page | 0.0 | 0.0 | 0.0 | 0.0 |
| discovery:sheet-returned | 0.0 | 0.0 | 0.0 | 0.0 |

Steps still at or over 30 KB: build:apply-sem, build:draft, build:drafts, build:plan, build:write

