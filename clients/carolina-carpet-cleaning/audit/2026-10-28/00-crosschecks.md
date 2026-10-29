# Evidence cross-checks

Run before any finding is written. CONTRADICTED items block the related finding outright.

Sources recognised: cms.wordpress_all_urls, dataforseo.duplicate_content, dataforseo.duplicate_tags, dataforseo.non_indexable, dataforseo.redirect_chains, screamingfrog.all_inlinks, screamingfrog.external_all, screamingfrog.h1_all, screamingfrog.h2_all, screamingfrog.internal_all, screamingfrog.links_all, screamingfrog.meta_description_all, screamingfrog.page_titles_all, sitemap.urls

## [UNVERIFIED] Inventory reconciliation

24 URLs exist in the CMS export but were not crawled; 18 were crawled but are absent from the CMS export. These are orphan *candidates* only — resolve against sitemaps, Search Console, analytics, backlinks, GBP destinations and paid landing pages before any is called an orphan.

## [UNVERIFIED] Orphan candidates (zero internal inlinks)

8 of 96 pages in the crawl or sitemap have no internal inlinks in the link-level export (internal hyperlinks, self-links excluded):
  - https://carpetcleaningblufftonsc.com/area-rug-cleaning/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/bluffton-neighborhoods/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/carpet-stain-removal/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/category/know-the-area/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/leave-us-a-review/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/low-moisture-carpet-cleaning/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/residential-carpet-cleaning/ (sitemap only + sitemap)
  - https://carpetcleaningblufftonsc.com/terms-of-service/privacy-policy/ (sitemap only + sitemap)
  → Orphan *candidates* only. Resolve against GSC, analytics, backlinks, GBP destinations and paid landing pages before any is called an orphan.

## [UNVERIFIED] Sitemap

Sitemap (88 URLs, from Carolina Carpet Cleaning - MANUAL - sitemap-urls - 2026-10-29.csv, Carolina Carpet Cleaning - MANUAL - sitemap-urls - 2026-10-29.csv) vs crawl (92 URLs):
8 sitemap URL(s) the crawl did not find:
  - https://carpetcleaningblufftonsc.com/area-rug-cleaning/
  - https://carpetcleaningblufftonsc.com/bluffton-neighborhoods/
  - https://carpetcleaningblufftonsc.com/carpet-stain-removal/
  - https://carpetcleaningblufftonsc.com/category/know-the-area/
  - https://carpetcleaningblufftonsc.com/leave-us-a-review/
  - https://carpetcleaningblufftonsc.com/low-moisture-carpet-cleaning/
  - https://carpetcleaningblufftonsc.com/residential-carpet-cleaning/
  - https://carpetcleaningblufftonsc.com/terms-of-service/privacy-policy/
3 sitemap URL(s) that answered non-200 in the crawl:
  - https://carpetcleaningblufftonsc.com/permanent-pet-urine-odor-removal-bluffton-sc/ → 301
  - https://carpetcleaningblufftonsc.com/the-church-of-the-cross/ → 301
  - https://carpetcleaningblufftonsc.com/travelers-should-know-about-safety-inside-vacation-rentals/ → 301
12 indexable 200 page(s) in the crawl missing from the sitemap:
  - https://carpetcleaningblufftonsc.com/blog/page/2/
  - https://carpetcleaningblufftonsc.com/blog/page/3/
  - https://carpetcleaningblufftonsc.com/blog/page/4/
  - https://carpetcleaningblufftonsc.com/blog/page/5/
  - https://carpetcleaningblufftonsc.com/blog/page/6/
  - https://carpetcleaningblufftonsc.com/category/carpet-cleaning/page/2/
  - https://carpetcleaningblufftonsc.com/category/carpet-cleaning/page/3/
  - https://carpetcleaningblufftonsc.com/category/carpet-cleaning/page/4/
  - https://carpetcleaningblufftonsc.com/category/carpet-cleaning/page/5/
  - https://carpetcleaningblufftonsc.com/category/know-the-area/local-information/page/2/
  - https://carpetcleaningblufftonsc.com/category/know-the-area/local-information/page/3/
  - https://carpetcleaningblufftonsc.com/category/know-the-area/whats-nearby/page/2/
  → Not-found URLs may be crawl-scope gaps (orphan trap) — check the crawl stop reason first. Non-200 results are checked live before any finding.

## [LIMITATION] Rendering

No JS rendering export present. Per the Agency Profile our standing crawler is the DataforSEO OnPage API in basic mode (no JavaScript rendering; free Screaming Frog is the fallback), so this is expected, not a gap. Any finding that would depend on what Google renders is marked Needs Evidence. Do not recommend re-crawling with rendering unless Paul asks (JavaScript mode costs 10x).

## [CONFIRMED] Crawl coverage vs licence cap

92 URLs crawled, below the 500 cap — coverage is not truncated by the licence.

## [CONFIRMED] Host consistency (crawl, canonicals, links)

Every crawled 2xx URL, canonical and internal link target is on https://carpetcleaningblufftonsc.com. (crawled 2xx URLs: https://carpetcleaningblufftonsc.com ×89; canonicals: https://carpetcleaningblufftonsc.com ×89; internal link targets: https://carpetcleaningblufftonsc.com ×2153; redirecting URLs (expected when they 301 to the main form): https://carpetcleaningblufftonsc.com ×3)

