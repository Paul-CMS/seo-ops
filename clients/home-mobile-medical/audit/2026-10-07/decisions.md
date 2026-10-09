# Decision log — home-mobile-medical

Append-only. Never edit or summarize an existing entry. Every Paul Exception,
applied default, N/A-with-rationale and deviation from GOV-02 goes here with the
finding IDs it affects.

Format:

```
## DEC-LOCAL-001 · 2026-10-07 · Standing exception cited
Decision: Analysis and review are both performed by Claude under the standing exception CM-026; the review (S17) runs in the fresh-context audit-reviewer subagent.
Affects: all findings. Decided by: rulings.md CM-026.

## DEC-LOCAL-002 · 2026-10-07 · Paul decisions applied (not re-litigated)
Decision: SAB, Lowcountry only; Georgia URLs Hold for microsite (no redirect to SC pages); FL/MI dropped; destructive actions 301 only (never 410) after CM-019, DataforSEO replacing GSC; hubs /service-area/, /service-area/charleston/, /service-area/hhi-beaufort/ kept (metro-hub rule L-008 PROPOSED, county-hub spec DRAFT → hub conformance Low at most); services = stair lifts parent (straight consolidated), curved, porch, wheelchair lifts, repair & maintenance; blog posts kept as-is until the Blog Decision Map; Folly Island naming; 24 SC towns confirmed; every page audited as live (pre-seo-ops build files lost). The old URL Decision Map (SRC-021) is input evidence only; its 410 rows, hub redirects and Georgia KEEP rows are superseded.
Affects: URL Decision Map; F-002, F-003, F-013, F-015, F-020, F-029–F-032, F-039. Decided by: Paul (Brand Guide H; decision record 2026-10-06/07).

## DEC-LOCAL-003 · 2026-10-07 · Interpretation applied — CM-019 condition 3
Decision: the citation tracker records no destination URL; condition 3 is tested by matching DataforSEO referring domains to tracked citation domains (marketersmedia.com is an "active" citation in the tracker and is treated as one). URLs with no tracked-citation referring domain = "pass on available evidence".
Affects: URL Decision Map ext_cm019_c3; F-013, F-015. Decided by: analyst (method), flagged for review.

## DEC-LOCAL-004 · 2026-10-07 · N/A and limitations
- §9 Schema readiness: N/A — no structured-data export (SF free) and S20 SEOPress settings pending with Jonie; all HP-24/SVC-22/LOC-26/HUB-17/ABT-15/BLG-18 = Needs Evidence.
- §4 Local grid: no finding — grid centre and device not stated (analysis-rules §4); measured results kept in inventories/local-grid.csv (question Q7).
- §1 Baseline: no GSC/GA4 (S11 skipped) — finding F-040 records the gap.
- Body text and H2s beyond the first two are not exported: most section/FAQ/claim checks are NE in the scorecard; claims quoted from Brand Guide D2 and CMS excerpts only.
- Crawl is the Screaming Frog free fallback (2026-09-18), not DataforSEO OnPage; no rendering — LNKD DOM parity used to rule out JS-only headings/links.
- All page specs are DRAFT — every failed check is advisory (a recommendation, not a gate).
- LNKD tool-only issues (heading gaps, alt text, thin content) not promoted (no corroboration).

## DEC-LOCAL-005 · 2026-10-07 · Gate B outcome
Questions raised: Paul Q1 (CM-019 C4 for 36 URLs), Q2 (redirect targets), Q3 (10 value URLs — keep or Paul Exception), Q4 (CF-001 homepage H1); VA Q5 (/new-homepage/ status), Q6 (live status of 40 uncrawled URLs), Q7 (grid centre/device). Defaults recorded in questions/questions.csv; until answered, affected dispositions stay Needs Evidence (confidence Assumed for the disposition part).
Affects: F-003, F-013, F-015, F-026, F-035, F-038. Decided by: Gate B (gate-b-questions.md).

## DEC-LOCAL-006 · 2026-10-08 · Independent review (S17)
Decision: Independent review per CM-026 (fresh-context reviewer). The audit-reviewer subagent loaded only findings.csv, the inventories, the manifest, the cross-checks, this log, questions/questions.csv (no answers yet), conflicts.csv, the methodology and the Brand Guide, and opened the evidence at each locator (SF exports, LNKD workbook, CMS export, sitemap export, citation tracker, DataforSEO rankings/backlinks/reviews). Every High finding was re-derived; Medium and Low were sampled (most opened at the locator; F-011 and F-039 only partly — rows/columns sampled). Outcome over 40 findings: 28 confirmed, 12 revised by superseding row (F-003, F-004, F-009, F-015, F-023, F-026, F-027, F-028, F-030, F-033, F-035, F-038), 0 withdrawn. Severity after review: High 12, Medium 13, Low 15 (F-027 High → Low and F-028 Medium → Low: Coastal-default elements, never above Low until Paul rules — specs/README.md). URL Decision Map (159 rows): 151 confirmed; 7 redirect-candidate recommendations withdrawn because the URL fails CM-019 C1 or C2 (U-080, U-088, U-090, U-091, U-092, U-093, U-094 → Needs Evidence, keep live, Paul Exception only via Q3); 1 revised (U-089 finding reference). Superseding rows appended; no row edited. CM-019 condition-3 method (DEC-LOCAL-003) judged sound as a negative check with its limitation stated; it can miss a citation that DataforSEO has not indexed, so the website field of the tracked active listings should be checked before any URL goes to Paul as a 301 candidate. Record: review-s17.csv.
Affects: all findings; URL Decision Map U-080, U-088–U-094. Decided by: audit-reviewer (S17), rulings.md CM-026, CM-028, CM-019.

## DEC-LOCAL-007 · 2026-10-08 · S18 corrections from the S17 review
Decision: (1) the audit-local conflict CF-001 is renumbered CF-LOCAL-001 everywhere it is live (conflicts.csv, README, scorecard, questions, URL map draft rows; F-026 rev 3 supersedes rev 2) because CF-001 is a resolved register entry (rulings.md section E); earlier log entries (DEC-LOCAL-005, the run decision of 2026-10-07) keep the old label as history. (2) PROC-01 step 4 done: the proposed ruling is methodology/lessons.md L-009 (PROPOSED); Paul's 2026-10-08 Apex ruling on the same tension is client-specific and not applied; Q4 stays open; tests/run_all.py 283 passed, 0 failed. (3) 00-manifest.csv SRC-009 to SRC-027 metadata corrected (they had carried the SF crawl settings). (4) 00-crosschecks.md rendering paragraph now names the Screaming Frog free crawl (2026-09-18). (5) URL map rows U-138 to U-159: superseding metadata rows correct the source label to the SF crawl row; decisions unchanged. (6) Questions Q8 (Gwen: website field of every tracked citation, closes CM-019 C3 before any 301 goes to Paul) and Q9 (GBP history, F-009) added from the review.
Affects: F-026; URL map U-138 to U-159; F-009, F-013, F-015, F-003. Decided by: audit-reviewer hand-back (S17) applied by the discovery-audit agent.

## DEC-LOCAL-008 · 2026-10-09 · Gate B outcome (update) - Q1, Q2, Q8 answered by Paul
Decision: Q1 answered - the client confirms no leads from any of the 36 retirement URLs; CM-019 C4 passes for them (settled: cm019-c4-no-leads). Q2 answered - redirect targets are the audit defaults (settled: redirect-targets-default). Q8 answered by **Paul Exception** - Gwen's citation link-destination check is waived and CM-019 C3 is accepted on DataforSEO referring-domain evidence (DEC-LOCAL-003 method) for the 36 URLs (settled: cm019-c3-citation-check-waived); the limitation recorded in DEC-LOCAL-006 (a listing DataforSEO has not indexed could point at a URL) is accepted by Paul. Result: the 36 URLs pass C1-C4 and are decided 301s (URL Decision Map superseding rows, Status "decided - supersedes"); every redirect is a VA handoff to Jonie after audit approval, never implemented by the system; /hilton-head/stair-lift-repair/ is paired with the publish of /services/stair-lift-repair/ (its target does not exist yet). Findings F-003 rev 3, F-013 rev 2, F-014 rev 2, F-015 rev 3 and F-035 rev 3 supersede the earlier rows; the disposition part is no longer Assumed. Still open: Q3, Q4, Q5, Q6, Q7, Q9; the Georgia rows stay Hold and the 10 CM-019-failing URLs are unchanged.
Affects: URL Decision Map (36 rows); F-003, F-013, F-014, F-015, F-035. Decided by: Paul 2026-10-09 (Q8 = Paul Exception); applied by the discovery-audit agent, run 20261009-071238-discovery-94fa.
