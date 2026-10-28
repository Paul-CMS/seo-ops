# Discovery manual lookups (SOS, GBP, duplicates, profiles) - H-2026-10-28-01-manual_lookup

> **Superseded by the VA Worklist** (`VA-WORKLIST.md`, rewrite 2 P9) — work from the worklist; this file is kept as the record.

**For:** Gwen · **Prepared:** 2026-10-28 · **Client:** Carolina Carpet Cleaning (carpetcleaningblufftonsc.com)

## What to do

Work through every row in the worksheet. For each one: check the current value first (column `old`). If it is already the new value, mark `done` with note `already done`. If the current value is something else, do not change it — mark `blocked` and say what you found.

Return the worksheet CSV with the `status` column filled: **done**, **blocked** or **deviated**, and a `note` on every blocked or deviated row. Do not add rows; put anything extra you find under a separate heading in your reply.

**Progress:** 0 of 9 row(s) done (updated 2026-10-28)

| Ref | URL | Field | Now | Change to | Why | Decision Map | Status |
|---|---|---|---|---|---|---|---|
| H-2026-10-28-01-manual_lookup-01 | https://businessfilings.sc.gov/BusinessFiling/Entity/Search | SC Secretary of State: search 'Carolina Carpet Cleaning' and 'Kevin Snow'; record legal name, entity type, formation date, status, registered agent, officers, prior names (screenshot) | not read (CAPTCHA) |  | Legal entity name and the 'since 1993' claim (domain registered 2019) need the government record | Brand Guide A10 + D founding year | issued |
| H-2026-10-28-01-manual_lookup-02 | https://www.google.com/maps?cid=3992053166300574362 | GBP public Maps view: exact name, PRIMARY category, rating and review count exactly as shown with today's date, hours, phone shown, website, storefront or service-area (screenshot) | Maps not machine-readable; Birdeye mirror shows 5.0 / 29 reviews |  | Category entity is the GBP primary category (BB-106); phone is in conflict (575-6286 vs 525-6288) | Decision Sheet category_entity / A2 A8 D rating | issued |
| H-2026-10-28-01-manual_lookup-03 | https://business.google.com/ | GBP dashboard (once we are Manager): secondary categories, service-area list, opening date (screenshot) | not readable without access |  | Standing VA task; service area and open date check the towns list and the 1993 claim | Decision Sheet towns_served / category_variants | issued |
| H-2026-10-28-01-manual_lookup-04 | https://www.google.com/search?q=Carolina+Carpet+Hardwood+and+Tile&ludocid=15026650423285168794 | Second Google listing 'Carolina Carpet, Hardwood, & Tile' (ludocid 15026650423285168794): name, address, phone, website, category; is it this business (duplicate) or another company? | unknown |  | Possible duplicate GBP listing | Discovery Record duplicates | issued |
| H-2026-10-28-01-manual_lookup-05 | https://www.yelp.com/biz/carolina-carpet-cleaning-bluffton | Yelp: name, address, phone, website, categories, rating, review count, year established (screenshot) | 403 to the system |  | NAP consistency; listed in the site schema sameAs | Discovery Record citations | issued |
| H-2026-10-28-01-manual_lookup-06 | https://www.facebook.com/carpetcleaningbeaufortsc | Facebook 'Carolina Carpet Cleaning | Beaufort SC': Intro/About (address, phone, website, hours, service area) | title only readable |  | Linked from the site footer; NAP check | Discovery Record social | issued |
| H-2026-10-28-01-manual_lookup-07 | https://www.facebook.com/CarolinaCarpetCleaning | Facebook URL in the site schema sameAs: whose page is it? (system saw the name 'Jack Blaine Beers Jr.') | page name 'Jack Blaine Beers Jr.' |  | Schema sameAs may point at an unrelated profile | Discovery Record social | issued |
| H-2026-10-28-01-manual_lookup-08 | https://carpetcleaningbeaufortsc.yolasite.com/ | Second website (Yola): name, phone, address, owner, links; is it the client's? (screenshot) | search snippet shows 843-525-6288; 403 to the system |  | Second phone number and second web property | Discovery Record phone conflict | issued |
| H-2026-10-28-01-manual_lookup-09 | https://reviews.birdeye.com/carolina-carpet-cleaning-166418659516441 | Birdeye: confirm the address shown (5922 Pleasant Farm Dr, Beaufort, SC 29906); note any BBB, Angi or Nextdoor listing with the same address | 5922 Pleasant Farm Dr Beaufort SC 29906 |  | Address conflict with the site (273 Club Gate Bluffton) | Discovery Record address conflict | issued |
