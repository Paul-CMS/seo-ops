# REWRITE-4 baseline — what the current route costs

_Generated 2026-10-20 by `python3 scripts/usage.py baseline home-mobile-medical apex-roofing-of-the-lowcountry` from Claude Code's transcripts, priced with `scripts/model_prices.json` (cache-write prices inferred). Do not edit by hand — regenerate. A run with no session id or no transcript on this Mac is counted as a run but has no cost (unmeasured); the totals are therefore a floor._

## home-mobile-medical

**$29.28** measured over 20 of 28 run(s); 86,672,994 tokens (input + cache write + cache read + output).

### Cost per stage

| Stage | Runs measured | Tokens | USD |
|---|---|---|---|
| batches | 13 of 14 | 51,039,019 | $17.07 |
| build-plan | 3 of 3 | 22,746,976 | $8.01 |
| audit | 1 of 2 | 8,879,741 | $3.11 |
| any | 3 of 7 | 4,007,258 | $1.10 |
| setup | 0 of 1 | 0 | $0.00 |
| data | 0 of 1 | 0 | $0.00 |

### Cost per step

| Step | Runs measured | Tokens | USD |
|---|---|---|---|
| build:write | 2 of 2 | 31,149,887 | $9.79 |
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

### Ten dearest runs

| Run | Step | Tokens | USD | Models |
|---|---|---|---|---|
| 20261014-100458-build-2be7 | build:facts | 15,091,794 | $5.56 | claude-opus-5-5 $3.85, claude-sonnet-5-5 $1.69, claude-haiku-5-5 $0.01 |
| 20261014-125319-build-9170 | build:write | 16,200,305 | $5.22 | claude-opus-5-5 $4.63, claude-sonnet-5-5 $0.53, claude-haiku-5-5 $0.06 |
| 20261014-144852-build-6004 | build:write | 14,949,582 | $4.57 | claude-opus-5-5 $3.77, claude-sonnet-5-5 $0.71, claude-haiku-5-5 $0.09 |
| 20261009-071238-discovery-94fa | discovery:audit | 8,879,741 | $3.11 | claude-opus-5-5 $3.11 |
| 20261009-122052-build-8f9c | build:blockers | 3,935,706 | $1.55 | claude-opus-5-5 $1.55, claude-haiku-5-5 $0.00 |
| 20261014-163404-build-b049 | build:draft | 2,010,781 | $0.98 | claude-opus-5-5 $0.98, claude-haiku-5-5 $0.01 |
| 20261014-164325-build-3b84 | build:drafts | 2,999,753 | $0.96 | claude-opus-5-5 $0.96, claude-haiku-5-5 $0.01 |
| 20261014-140654-build-4002 | build:facts | 3,719,476 | $0.90 | claude-opus-5-5 $0.87, claude-haiku-5-5 $0.03 |
| 20261014-211328-build-a865 | build:writeback | 1,733,990 | $0.85 | claude-opus-5-5 $0.84, claude-haiku-5-5 $0.01 |
| 20261014-164054-build-4d84 | build:draft | 1,910,882 | $0.79 | claude-opus-5-5 $0.78, claude-haiku-5-5 $0.00 |

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
**All clients: $151.29**
