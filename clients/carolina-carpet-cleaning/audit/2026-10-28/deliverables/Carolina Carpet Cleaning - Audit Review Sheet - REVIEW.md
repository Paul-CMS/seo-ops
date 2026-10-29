# Carolina Carpet Cleaning - Audit Review Sheet - REVIEW

**Status:** REVIEW — awaiting Paul. Rendered 2026-10-29T08:17 by `scripts/render.py` from `audit-review.json`, `redirect-screen.csv`, `audit step outcomes`. Rendered, never edited: to change anything, change the source row and render again.

One sheet, one approval line (CM-061). Answer in `audit-review.csv` (an empty answer accepts the recommended option) or in one line: "accept all" or "accept all except 3b". Fix rows are not here: they are the Technical Blocker Checklist, handed to the VA once the audit is approved.

## Questions for Paul (2)

| # | Kind | Where | What | Why it matters | Options | Recommended |
|---|---|---|---|---|---|---|
| 1 | URL decision | https://carpetcleaningblufftonsc.com/residential-carpet-cleaning/ ; https://carpetcleanin… | Four published WordPress pages (1,290–1,623 words) answer 301 live: residential, low-moisture and stain removal → /carpet-cleaning/, area rug → /rug-cleaning/. They are still in page-sitemap1.xml and… | Four service pages now redirect into two main pages; decide whether they stay folded or come back as their own pages. | a) keep the four services folded into Carpet Cleaning and Rug Cleaning (the live 301s stay) · b) give Residential, Low-Moisture, Stain Removal and Area Rug their own pages again (remove the 301s; Bui… | **a** |
| 2 | legal or money claim | https://carpetcleaningblufftonsc.com/the-4-main-factors-affecting-carpet-cleaning-costs/ | The post states "We are an expert team of professionals that guarantee quality carpet cleaning at a reasonable price." Section D: Guarantees = N/A and Team = Kevin alone (Client Confirmed 2026-10-28). | An old blog post promises a guarantee the owner says he does not offer. | a) remove the guarantee sentence now (VA edit) · b) keep it live until the Blog Decision Map | **a** |

## For the client to confirm (2) — `client-questions.csv`, sent by Paul

The only part of the audit the client sees. A client answer is never taken by default.

| # | Question | Best answer found | Searched |
|---|---|---|---|
| 3 | The site states drying time three ways. Absolute: "Carpets Dry in Under 1 Hour" / "under one hour" (homepage hero and section, /carpet-cleaning/), "dry within one hour" (/commercial-carpet-cleaning/), "dry in under an hour" (3 blog posts). Hedged: "most carpe… | a) carpets dry in under one hour on a typical job · b) most carpets dry within about an hour (the wording most live pag… | searched: facts.json (no drying fact) → decisions-settled.md (none) → reviews (one: "dry within a few minutes") → live site text (claims under 1 hour) → GBP (n… |
| 4 | The site says the carpet solution is "pH-neutral and biodegradable" and "safe for pets and children" (/, /carpet-cleaning/); /upholstery-cleaning-on-hilton-head-island/ says "non-toxic pre-treatments"; /hardwood-floor-cleaning/ says "every product we use is p… | a) name the cleaning products used (carpet, upholstery, tile, hardwood) — we check their safety data and keep supported… | searched: facts.json (none) → decisions-settled.md (none) → reviews (no product named) → live site text ("pH-neutral and biodegradable", no brand) → GBP (not r… |

## Decided for you (16) — change any by naming its number

- **5.** F-002 · 3. Brand, entity and verified truth: Section D records "6 Google reviews, all 5 stars" (client-stated 2026-10-28). The DataforSEO Google reviews pull for the same profile (owner Kevin named in the… → **At reconcile, Paul records the Google figure as shown on the day ("5.0 · 29 reviews, <date>") with run.py fact; no page states a review count until then.**
- **6.** F-003 · 3. Brand, entity and verified truth: The brand query "carolina carpet cleaning" averages position 9.14 for the homepage (338 impressions, 18 clicks, 16 months); /about/ ranks 38 for "carolina carp… → **Build ties the brand to Bluffton, the Lowcountry and Kevin Snow on the homepage and About page (already in the rebuild specs); no separate action.**
- **7.** F-007 · 5. Architecture, services, locations, page types: The 15 pages Build rebuilds have titles, H1s and meta descriptions outside the settled formats: location titles read "<City> Carpet Cleaning - Carolina Carpet… → **The rebuild sets every title, H1 and meta description to the settled formats (one row, decided for you); "The Best" only by CM-020.**
- **8.** F-009 · 5. Architecture, services, locations, page types: 22 "Know the Area" posts sit beside 30 carpet posts. Three describe Savannah, GA places (outside the six settled towns); three cover the same Heyward House. 17… → **Keep all live; the Blog Decision Map (bb-blog-analysis) decides each. No redirect in the audit: no backlinks evidence (C2) and no observed conflict (CM-021).**
- **9.** F-011 · 2. Technical and crawl: Old Bluffton URLs redirect to the homepage although /bluffton/ and matching service pages exist (e.g. /service-area/bluffton/ → /, /bluffton/pet-odor-removal/… → **Retarget: /service-area/bluffton/ and /location/bluffton-sc/ → /bluffton/ (301); /bluffton/<service>/ → the matching service page (301).**
- **10.** F-012 · 5. Architecture, services, locations, page types: Two published pages have no internal link from any crawled page: /bluffton-neighborhoods/ (858 words, GSC "Crawled – currently not indexed") and /leave-us-a-re… → **Keep both live; Build links /bluffton-neighborhoods/ from /bluffton/ and /leave-us-a-review/ from /contact-us/ in the rebuild.**
- **11.** F-020 · 6. On-page and content structure: Blog post titles do not follow "Post Title - Brand": the brand is missing (or uses " / "). 44 page(s). → **Add " - Carolina Carpet Cleaning" to each post title (SEOPress title, VA); keep the post wording.**
- **12.** F-021 · 3. Brand, entity and verified truth: Blog posts are attributed to generic WordPress users ("Tech Writer", "Staff Writer", "Support Crew", "seogwen007"), not the approved author Kevin Snow (CM-039)… → **Reassign these posts to the Kevin Snow user (VA, bulk edit).**
- **13.** F-023 · 3. Brand, entity and verified truth: Posts state facts not in Section D: a rug-cleaning price range ("$2 to $5 per square foot … $160 to $400"), "our personnel is highly-trained and insured" (team… → **Remove the price range and the "personnel" sentence (VA); the guarantee sentence follows F-004.**
- **14.** F-024 · 6. On-page and content structure: Meta descriptions on kept pages are outside 120–160 characters (category archives have none). 49 page(s). → **Rewrite to 120–160 characters (VA, SEOPress; archives via the taxonomy template); the homepage description keeps its facts.**
- **15.** F-025 · 6. On-page and content structure: SEO titles on kept blog posts exceed 60 characters (the homepage is excluded: its length follows the settled format). 17 page(s). → **Shorten to 60 characters or fewer when adding the brand (BLG-03), keeping the post topic first (VA).**
- **16.** F-026 · 3. Brand, entity and verified truth: Homepage: the category variant "Carpet Cleaning" repeats at title → H1 → first H2 ("Carpet Cleaning Services"). 1 page(s). → **Rename the first H2 with another variant (e.g. "Carpet Cleaners and Floor Care Services") — H1 unchanged (HP-08).**
- **17.** F-027 · 6. On-page and content structure: Homepage opening paragraph is about Hilton Head Island upholstery, not who/what/where for the business; its call button shows the unapproved number (F-001). 1… → **Replace the opening with one paragraph naming Carolina Carpet Cleaning, carpet cleaning, the Lowcountry, the phone and the free estimate (Build drafts the passage; H1 unchanged).**
- **18.** F-028 · 5. Architecture, services, locations, page types: Homepage services section lists 8 services as H3s (spec: max 5–6). 1 page(s). → **Keep 6 as H3 links and fold the rest into a text line (Build, light edit).**
- **19.** F-029 · 6. On-page and content structure: Homepage testimonials sit under an H2 heading; the review figure to show is unsettled (F-002). 1 page(s). → **Remove the H tag from the review section heading (styled text) and show Google's figure once F-002 is recorded.**
- **20.** F-030 · 6. On-page and content structure: Homepage carries decorative headers ("Why Lowcountry Homeowners Trust Carolina Carpet Cleaning", "How It Works"). 1 page(s). → **Turn them into styled text or descriptive headings (Build, light edit).**

## Redirect pre-screen (CM-019 C1–C3, `pagedec.py screen`)

0 pass · 6 fail · 103 needs evidence of 109 URL(s). A `fail` URL is never redirected.

_Fix rows (to the blocker checklist): 10. Not raised (duplicate or already answered): 0._

## Evidence

Every registered step has an outcome.
