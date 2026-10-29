# Evidence cross-checks

Run before any finding is written. CONTRADICTED items block the related finding outright.

Sources recognised: cms.wordpress_all_urls, dataforseo.duplicate_content, dataforseo.duplicate_tags, dataforseo.non_indexable, dataforseo.redirect_chains, screamingfrog.all_inlinks, screamingfrog.external_all, screamingfrog.h1_all, screamingfrog.h2_all, screamingfrog.internal_all, screamingfrog.links_all, screamingfrog.meta_description_all, screamingfrog.page_titles_all

## [UNVERIFIED] Inventory reconciliation

98 URLs exist in the CMS export but were not crawled; 5 were crawled but are absent from the CMS export. These are orphan *candidates* only — resolve against sitemaps, Search Console, analytics, backlinks, GBP destinations and paid landing pages before any is called an orphan.

## [LIMITATION] Rendering

No JS rendering export present. Per the Agency Profile our standing crawler is the DataforSEO OnPage API in basic mode (no JavaScript rendering; free Screaming Frog is the fallback), so this is expected, not a gap. Any finding that would depend on what Google renders is marked Needs Evidence. Do not recommend re-crawling with rendering unless Paul asks (JavaScript mode costs 10x).

## [LIMITATION] Sitemap

No sitemap URL list in the evidence (a file named *sitemap*.txt / .xml / .csv). Sitemap coverage cannot be checked; capture the sitemap's URLs before writing any sitemap finding.

## [CONFIRMED] Crawl coverage vs licence cap

8 URLs crawled, below the 500 cap — coverage is not truncated by the licence.

## [CONFIRMED] Host consistency (crawl, canonicals, links)

Every crawled 2xx URL, canonical and internal link target is on https://carolinacarpetcleaning.com. (crawled 2xx URLs: https://carolinacarpetcleaning.com ×4; canonicals: https://carolinacarpetcleaning.com ×4; internal link targets: https://carolinacarpetcleaning.com ×22; redirecting URLs (expected when they 301 to the main form): https://carolinacarpetcleaning.com ×4)

## [CONFIRMED] Orphan candidates (zero internal inlinks)

All 3 pages in the crawl and sitemap have at least one internal inlink in the link-level export (internal hyperlinks, self-links excluded).

