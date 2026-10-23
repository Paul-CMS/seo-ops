# Evidence cross-checks

Run before any finding is written. CONTRADICTED items block the related finding outright.

Sources recognised: dataforseo.duplicate_content, dataforseo.duplicate_tags, dataforseo.non_indexable, dataforseo.redirect_chains, screamingfrog.all_inlinks, screamingfrog.external_all, screamingfrog.h1_all, screamingfrog.h2_all, screamingfrog.internal_all, screamingfrog.links_all, screamingfrog.meta_description_all, screamingfrog.page_titles_all, sitemap.urls

## [CONTRADICTED] Host consistency

Both apex and www forms appear across exports for: polk-county.net, weather.gov. Every URL-keyed comparison in this audit must normalize host before matching, and the host split itself is a canonical/redirect finding to verify against live response codes.

## [UNVERIFIED] Orphan candidates (zero internal inlinks)

3 of 43 pages in the crawl or sitemap have no internal inlinks in the link-level export (internal hyperlinks, self-links excluded):
  - https://www.firstchoiceseamlessgutters.net/category/uncategorized/ (sitemap only)
  - https://www.firstchoiceseamlessgutters.net/gutter-guards-winter-haven-fl/ (sitemap only)
  - https://www.firstchoiceseamlessgutters.net/gutter-services-lakeland-fl/ (sitemap only)
  → Orphan *candidates* only. Resolve against GSC, analytics, backlinks, GBP destinations and paid landing pages before any is called an orphan.

## [UNVERIFIED] Sitemap

Sitemap (44 URLs, from sitemap-urls.txt) vs crawl (47 URLs):
3 sitemap URL(s) the crawl did not find:
  - https://www.firstchoiceseamlessgutters.net/category/uncategorized/
  - https://www.firstchoiceseamlessgutters.net/gutter-guards-winter-haven-fl/
  - https://www.firstchoiceseamlessgutters.net/gutter-services-lakeland-fl/
1 sitemap URL(s) that answered non-200 in the crawl:
  - https://www.firstchoiceseamlessgutters.net/contact/ → 301
  → Not-found URLs may be crawl-scope gaps (orphan trap) — check the crawl stop reason first. Non-200 results are checked live before any finding.

## [LIMITATION] Rendering

No JS rendering export present. Per the Agency Profile our standing crawler is the DataforSEO OnPage API in basic mode (no JavaScript rendering; free Screaming Frog is the fallback), so this is expected, not a gap. Any finding that would depend on what Google renders is marked Needs Evidence. Do not recommend re-crawling with rendering unless Paul asks (JavaScript mode costs 10x).

## [CONFIRMED] Crawl coverage vs licence cap

47 URLs crawled, below the 500 cap — coverage is not truncated by the licence.

## [CONFIRMED] Host consistency (crawl, canonicals, links)

Every crawled 2xx URL, canonical and internal link target is on https://www.firstchoiceseamlessgutters.net. (crawled 2xx URLs: https://www.firstchoiceseamlessgutters.net ×41; canonicals: https://www.firstchoiceseamlessgutters.net ×41; internal link targets: https://www.firstchoiceseamlessgutters.net ×1522; redirecting URLs (expected when they 301 to the main form): https://www.firstchoiceseamlessgutters.net ×5)

