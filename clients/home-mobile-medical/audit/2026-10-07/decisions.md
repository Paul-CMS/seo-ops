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
