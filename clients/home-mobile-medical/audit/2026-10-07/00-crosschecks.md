# Evidence cross-checks

Run before any finding is written. CONTRADICTED items block the related finding outright.

Sources recognised: screamingfrog.external_all, screamingfrog.h1_all, screamingfrog.h2_all, screamingfrog.internal_all, screamingfrog.javascript_all, screamingfrog.links_all, screamingfrog.meta_description_all, screamingfrog.page_titles_all

## [CONTRADICTED] Host consistency

Both apex and www forms appear across exports for: ccprc.com, southcarolinaparks.com. Every URL-keyed comparison in this audit must normalize host before matching, and the host split itself is a canonical/redirect finding to verify against live response codes.

## [LIMITATION] Rendering

Rendered columns empty on 96/96 rows. This is the configuration of the evidence used here - a Screaming Frog free-licence crawl of 2026-09-18 with no JavaScript rendering (the SF fallback; no DataforSEO OnPage crawl was run for this audit, Paul: no new crawl), NOT evidence that content disappears on render and NOT a defect to report.
  Consequence: JS dependency is unknown. Any finding that would rest on what Google renders is marked Needs Evidence.
  State this ONCE in Assumptions and Limitations. Never per finding. Do not recommend re-crawling with rendering.

## [CONFIRMED] Crawl coverage vs licence cap

284 URLs crawled, below the 500 cap — coverage is not truncated by the licence.



---

## Addendum — manual cross-checks (discovery-audit agent, 2026-10-07)

### Host consistency — CONTRADICTED is about third-party domains only
The two hosts flagged (ccprc.com, southcarolinaparks.com) are **external** outbound-link targets. All client URLs in every export are https://homemobilemedical.com (no www). No client host-split finding is written (the check blocks it anyway). All URL matching in this audit normalises protocol, www, trailing slash and case (LNKD exports omit the trailing slash).

### Missing H1 — CORROBORATED
SF h1_all (raw HTML, Occurrences = 0 on 54 of 96 HTML-200 pages) and LNKD Issues "Missing H1 tag" (56 URLs, rendered DOM; DOM parity "Yes" on all 102 pages) agree. F-022 written.

### LNKD "Canonical points to different URL" (7) — CONTRADICTED
SF internal_all shows a self-referencing canonical on all 96 HTML-200 pages. LNKD crawled slash-less URLs whose canonical is the slash form — expected behaviour, not a defect. No finding.

### LNKD tool issue lists — not promoted
291 issue rows (Heading hierarchy gap 83, Images missing alt 76, Missing H1 56, Meta description too long 22, Missing meta 12, Thin content 11, Title too long 10, Title too short 7, Canonical 7, Missing H2 4, others 3) and 100 AI-Engines rows. Only "Missing H1" (SF corroborates) and meta-description presence/length (SF corroborates) support findings. Heading-hierarchy gaps, alt text and thin content rest on the tool alone — LIMITATION, no finding.

### Orphan candidates — reconciled, not called orphans
37 sitemap URLs and 3 CMS-only/backlink-only URLs are not linked from any crawled page (SF) nor from LNKD's 102 source pages. Reconciled against CMS (published), XML sitemap, DataforSEO rankings/backlinks, GBP (homepage) and the citation tracker → reported as orphan *candidates* (F-035) with per-URL CM-019 evidence in the URL Decision Map.

### Inventory reconciliation — crawl vs CMS
Crawl: 118 HTML URLs (96 × 200, 22 × 301). CMS: 124 published (103 pages, 21 posts). In CMS not crawled: 37 (FL/MI 17, /stair-lift-installer/* 8, Georgia legacy 6, Hilton Head legacy 3, /charleston-sc/, /beaufort-sc/, /power-chairs/, /about-us-across-the-web/, /new-homepage/, /bluffton-sc/stair-lift-installer/ … see URL Decision Map ext_crawl_status). Crawled not in CMS: 11 taxonomy/pagination archives and 301 stubs (expected). Backlink-only URLs: /charleston/stair-lift/, /savannah/stair-lift/ (live status unknown).

### Crawl coverage
SF stopped at 284 URLs (below the 500 cap); coverage of internally linked pages is complete for this snapshot. Live status of the 40 uncrawled URLs was not checked (question Q6).

### Citation NAP — measured against the Brand Guide, not the tracker
Tracker discrepancies were compared with Brand Guide F (Paul Approved NAP). The tracker's "google.com — Potential" row is a tracker matching defect (the GBP exists, S06), recorded as a limitation.

### CM-019 condition 3 method
GBP destination: Brand Guide A11 (GBP Website field = homepage). Citation destination: the tracker has no destination-URL column, so DataforSEO referring domains were matched to tracked citation domains: storeboard.com → http homepage; news.marketersmedia.com (an active citation in the tracker) → homepage, /charleston/stair-lift/, /savannah/stair-lift/, /hilton-head/stair-lift/. Every other URL: no tracked citation domain links to it → "pass on available evidence".
