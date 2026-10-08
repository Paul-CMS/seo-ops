# Evidence cross-checks

Run before any finding is written. CONTRADICTED items block the related finding outright.

Sources recognised: screamingfrog.external_all, screamingfrog.h1_all, screamingfrog.h2_all, screamingfrog.internal_all, screamingfrog.javascript_all, screamingfrog.links_all, screamingfrog.meta_description_all, screamingfrog.page_titles_all

## [CONTRADICTED] Host consistency

Both apex and www forms appear across exports for: ccprc.com, southcarolinaparks.com. Every URL-keyed comparison in this audit must normalize host before matching, and the host split itself is a canonical/redirect finding to verify against live response codes.

## [LIMITATION] Rendering

Rendered columns empty on 96/96 rows. This is our standing configuration (DataforSEO OnPage, basic mode, no JavaScript rendering), NOT evidence that content disappears on render and NOT a defect to report.
  Consequence: JS dependency is unknown. Any finding that would rest on what Google renders is marked Needs Evidence.
  State this ONCE in Assumptions and Limitations. Never per finding. Do not recommend re-crawling with rendering.

## [CONFIRMED] Crawl coverage vs licence cap

284 URLs crawled, below the 500 cap — coverage is not truncated by the licence.

