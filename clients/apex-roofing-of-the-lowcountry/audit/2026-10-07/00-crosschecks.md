# Evidence cross-checks

Run before any finding is written. CONTRADICTED items block the related finding outright.

Sources recognised: dataforseo.duplicate_content, dataforseo.duplicate_tags, dataforseo.non_indexable, dataforseo.redirect_chains, screamingfrog.all_inlinks, screamingfrog.external_all, screamingfrog.h1_all, screamingfrog.h2_all, screamingfrog.internal_all, screamingfrog.links_all, screamingfrog.meta_description_all, screamingfrog.page_titles_all

## [LIMITATION] Rendering

No JS rendering export present. Per the Agency Profile our standing crawler is the DataforSEO OnPage API in basic mode (no JavaScript rendering; free Screaming Frog is the fallback), so this is expected, not a gap. Any finding that would depend on what Google renders is marked Needs Evidence. Do not recommend re-crawling with rendering unless Paul asks (JavaScript mode costs 10x).

## [CONFIRMED] Crawl coverage vs licence cap

72 URLs crawled, below the 500 cap — coverage is not truncated by the licence.

