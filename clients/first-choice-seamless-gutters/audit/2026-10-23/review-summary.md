# S17 independent review (CM-026, fresh-context reviewer) — 2026-10-23

Scope: review-scope.csv (0 destructive, 5 Asks, 12 sampled) plus the caller's five checks. Outcomes per row: review-s17.csv.
Totals: 25 confirmed · 6 revised · 7 withdrawn (merges and duplicates). In the 17 scope rows: 13 confirmed, 3 revised, 1 withdrawn.

## Revised (superseding rows, ext_revision 2)
- F-008: only 2 pages link to the vendor domain (Lake Wales x3, Lakeland x2), not 7. Crawl links.jsonl and external_all (2 inlinks) agree, and a live fetch on 2026-10-23 found nothing on Bartow, Eagle Lake, Fort Meade, Highland City or Kathleen. The destination was re-checked live: 'Contact Us - GPHI Home Remodeling', (267) 241-7994, Southampton PA. The row also adds the homepage and Lake Wales background images loaded from that domain. Still Fix and still urgent.
- F-011: the broken header href 'http:8633303243' is on 43 pages, not 41: both blog posts carry it (SRC-055/056). The Lakeland post also has an in-body href 'http://(863) 330-3243'. Still Fix and still urgent.
- F-012: the two posts link to each other through post navigation. The row now says no crawled page links to them.
- F-015: the C3 pass rests on the GBP field only, because no citation export is on file (flag F-004). The not-served 301 now needs the citation check as well as C4. The map's U019 row is Hold with no triage and no rebuild.
- F-020: merges F-019, F-021, F-022 and F-024 (one issue: the homepage title). The settled title 'Gutter Service in Polk County, FL - First Choice Seamless Gutters' is 65 characters, so COM-T still fails. F-019 r1 said 60 or fewer, which was wrong. Flag F-005 records the COM-T vs settled-format conflict.
- F-033: merges F-029 (FAQ). The capture has no map iframe, map block or Maps script, so the missing embed is not a JavaScript-rendering artefact.

## Withdrawn
F-019, F-021, F-022, F-024 were merged into F-020. F-029 was merged into F-033. F-023 duplicates F-017. F-032 duplicates F-003/F-004/F-005/F-028.

## Caller checks
1. Conformance judgments: I re-checked every homepage and blog-post FAIL against SRC-055/056/057 and all are supported. No score was withdrawn for lack of evidence. NE items were not turned into findings.
2. C3: no decision relies on the C3 pass. There are no destructive rows, and `pagedec.py screen --check` passes. Only F-015's conditional 301 leaned on C3, and it is now gated on the citation check.
3. F-017: the default (no H1 change) is stated as ext_default/options on an Ask. It is not presented as a finding.
4. F-008 and F-011: the evidence holds. The scope of both was corrected (see above).
5. Plant City: U019 is Hold with no triage and no rebuild.

Not verified: the counts in F-006, F-009, F-010, F-035 and F-049 were outside the scope and sample. The register is ready for the review sheet (S18 render).
