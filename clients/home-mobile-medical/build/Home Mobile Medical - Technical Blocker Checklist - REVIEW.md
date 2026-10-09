# Home Mobile Medical - Technical Blocker Checklist - REVIEW

**Run:** 20261009-122052-build-8f9c · **Date:** 2026-10-09 · **Source:** approved Finding Register (`audit/2026-10-07/findings.csv`, latest revision of each finding; audit_approved by Paul 2026-10-09) and URL Decision Map · **Severity scale:** CM-028

"Blockers cleared" is a condition. It is met when Jonie returns every handoff below `done` and `/verify` passes every row. Nobody approves it.

## 1 · High findings (CM-028): none blocks crawling, indexing or measurement

There are 12 High findings. None stops Google crawling or indexing the canonical pages, and none stops measurement. Each one is fixed by a page rebuild, by the structural step (`/implement home-mobile-medical structural`: the decided 301s and menu changes, from the URL Decision Map) or by the Blog Decision Map. So none of them is a Jonie row in this checklist.

| ID | What breaks | Pages | Fixed by |
|---|---|---|---|
| F-001 | Homepage title category slot is "Home Medical Equipment", not the GBP category | / | Homepage rebuild (final1) |
| F-002 | Site-wide nav and service pages link to Georgia pages (held for the microsite) | nav on all pages; 4 service pages; 10 GA URLs | Menu/link removal → `/implement structural` (navigation); service rebuilds (svc1) |
| F-003 | Discontinued services (power chairs, scooters, ramps, rentals) in nav and on kept pages | 17 URLs (see register) | Nav removal + decided 301s → `/implement structural`; rewrites in Build; Q3 open for 4 URLs that rank |
| F-005 | Unsourced safety/regulatory claims (health-adjacent client) | /, /service-area/beaufort-sc/ | Homepage and Beaufort rebuilds, Paul review recorded (CM-025) |
| F-013 | 20 legacy SC URLs duplicate canonical service/location pages | 20 URLs (see register) | 14 decided 301s → `/implement structural`; repair 301 paired with the svc1 publish; 6 Needs Evidence (Q3) |
| F-014 | No repair service page | /services/stair-lift-repair/ (new) | svc1 |
| F-015 | 17 FL/MI pages published and in the sitemap | 17 URLs (see register) | Decided 301s to /services/stair-lifts/ → `/implement structural`; Q6 live-status check rides with that handoff |
| F-016 | Service pages link only 4 of 24 location pages | 5 service pages | svc1 + Finish link wheel |
| F-017 | Location pages link only their own metro cluster | 24 location pages | Location batches + Finish link wheel |
| F-022 | 54 pages have no H1 | service, location, hub pages (see register) | Rebuilds |
| F-023 | Location titles in the wrong entity order | 24 location pages | Location rebuilds |
| F-032 | Unsourced coverage/tax/health claims in posts | 10 posts | Blog Decision Map |

## 2 · Low technical batch: handed to Jonie (one handoff per change kind, all flagged `--blockers`)

| Line | Finding | Issue | Affected URLs | Change kind | Rows |
|---|---|---|---|---|---|
| 1 | F-033 | Three redirects take two hops (to the slash-less URL, then to the final URL) | https://homemobilemedical.com/service-area/bluffton-sc-2/ (U-145), https://homemobilemedical.com/service-area/charleston-sc-2/ (U-146), https://homemobilemedical.com/service-area/beaufort-sc-2/ (U-147) → each straight to its `/service-area/<city>/` URL | redirect | 3 |
| 2 | F-033 | Internal links point at redirecting URLs, on pages that are not being rebuilt soon (8 posts, plus /service-area/mt-pleasant-sc/, which is kept live as Needs Evidence) | https://homemobilemedical.com/are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/, https://homemobilemedical.com/are-stair-lifts-covered-by-medicare/, https://homemobilemedical.com/are-stair-lifts-expensive-to-run/, https://homemobilemedical.com/are-stair-lifts-noisy/, https://homemobilemedical.com/are-stair-lifts-safe-and-ada-compliant/, https://homemobilemedical.com/can-stair-lifts-turn-corners-or-go-around-corners/, https://homemobilemedical.com/can-stairlifts-be-used-outside/, https://homemobilemedical.com/is-there-a-weight-limit-on-stairlifts/, https://homemobilemedical.com/service-area/mt-pleasant-sc/ | broken_link | 9 |
| 3 | F-038 (Q5) | A possible duplicate homepage and a page of unclear purpose. If /new-homepage/ is live and indexable, it is a second homepage in the index. This is a check only: record status, robots and canonical, and change nothing | https://homemobilemedical.com/new-homepage/ (U-137), https://homemobilemedical.com/about-us-across-the-web/ (U-136) | other (to Jonie: Q5 is routed to her) | 2 |

The links on service, location and hub pages that go to the same redirecting URLs are not Jonie rows. Those pages are all rebuilt, and F-033 says the links go with the rebuilds.

## 3 · Low items not in the Jonie batch (and why)

| Finding | Where it goes |
|---|---|
| F-035 sitemap removal (29 decided-301 URLs) | Goes with the redirect handoff in `/implement structural`. The finding requires each removal to be paired with that URL's 301, and the exclusion must not set noindex |
| F-034 /services/stair-lift/ redirect target | Needs Paul. It depends on /hilton-head/stair-lift/ (Needs Evidence, Q3 open). It is a redirect-target change, which is structural |
| F-036 meta descriptions | Rebuilt pages get spec metas in their drafts. Archives and posts go to the Blog Decision Map (F-039). Kept utility pages (/contact/, /terms-conditions/ and its 4 children) are a system safe fix (`meta_description`, channel wp) → `/implement safe` |
| F-037 dead outbound links | Sources are the Summerville, Bluffton and Hilton Head Island location pages (rebuilt, so the links are dropped) and Georgia pages (held). The export gives no source page per link, so there is no exact row to hand over |
| F-039 archives | Blog Decision Map |
| F-040 no GA4/GSC/call/form access | Paul: ask the client for GA4/GSC read access. A Jonie form-delivery check is the finding's alternative and is added only if Paul wants it |
| F-010, F-011, F-012 | Citations and links (Gwen / Paul / monitor). Not technical |
| F-020, F-021, F-027, F-028 | Page rebuilds (hubs, /services/, about), waiting on Paul's spec rulings |

## 4 · Notes for Paul

- **F-033 chain targets.** The URL Decision Map gives the slash-less URL as the target for U-145/146/147 (e.g. `/service-area/bluffton-sc`), which is still one hop short. The finding says "straight to the canonical slash URL", so the handoff uses `/service-area/<city>/`.
- **/services/stair-lift/ links.** That redirect currently ends on the legacy /hilton-head/stair-lift/ (Needs Evidence). The 9 link rows send those links to /services/stair-lifts/, which F-034 calls the natural target, instead of the legacy page. The redirect itself is not changed (F-034 waits on you).
- **Posts.** F-032 says posts stay as they are until the Blog Decision Map. The link rows change only link addresses, never wording.
- **Source pages per link.** The crawl export records inlink counts but not which page each link sits on. Each row therefore lists every redirecting URL, and Jonie marks the row "none found" if the page has none.
