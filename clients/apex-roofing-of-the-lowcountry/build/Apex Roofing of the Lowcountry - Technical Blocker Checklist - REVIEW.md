# Apex Roofing of the Lowcountry - Technical Blocker Checklist - REVIEW

**Run:** 20261008-131822-build:blockers-b359 · **Date:** 2026-10-08 · **Source:** approved Finding Register (`audit/2026-10-07/deliverables/`, audit_approved 2026-10-08) · **Severity scale:** CM-028

"Blockers cleared" is a condition: it is met when Jonie returns every handoff below `done` and `/verify` passes every row. Nobody approves it.

## 1 · High findings (CM-028) — none blocks crawling, indexing or measurement

All three High findings are on-page structure. None stops Google crawling or indexing a page, and none stops measurement. Each is fixed by the rebuilt page (WordPress draft with its SEOPress title, generated from the approved file), so none is a Jonie item in this checklist.

| ID | Sev. | What breaks | Pages | Fix | Channel / owner |
|---|---|---|---|---|---|
| F-014 | High | Service SEO titles in the wrong entity order with an area term (SVC-03, BB-302; settled: `Service Name - Apex Roofing of the Lowcountry`) | /roof-repair/, /roof-replacement/, /roof-installation/, /roof-inspections/, /emergency-roof-repair/, /metal-roofing-2/, /slate-roofing/, /skylights/ (8) | New title per settled format in each rebuilt service draft | seo_title — Build (site plan → draft); open choice below |
| F-015 | High | About title carries neither category nor area; H1 "About Us" names no entity (ABT-01, ABT-04) | /about/ (1) | Settled title and H1 (decisions-settled `about_page`) in the rebuilt About page (built last) | seo_title + h1 — Build; open choice below |
| F-022 | High | City names in service-page H3s (SVC-12, BB-314) | /roof-repair/, /roof-installation/, /roof-replacement/, /metal-roofing-2/, /slate-roofing/, /skylights/ (6) | Rebuilt service FAQs carry no city (site plan FAQ topics) | page_content — Build |

## 2 · Low technical batch — handed to Jonie (one handoff per change kind, all flagged `--blockers`)

| Finding | Sev. | Issue | Affected URLs | Change kind | Rows |
|---|---|---|---|---|---|
| F-009 | Low | /services/synthetic-roofing/ 301 → /synthetic-roofing/ (404); 1 referring domain | https://apexroofingtlc.com/services/synthetic-roofing/ (U-070), https://apexroofingtlc.com/synthetic-roofing/ (U-071) → https://apexroofingtlc.com/roof-replacement/ | redirect | 2 |
| F-030 | Low | Internal links through 301s | sitewide header/CTA `/contact` → `/contact/` (58 pages, one template row); `/metal-roofing/` → `/metal-roofing-2/` on /, /beaufort/, /bluffton/, /fripp-island/, /hardeeville/, /hilton-head-island/, /ladys-island/, /levy/, /okatie/, /port-royal/, /pritchardville/, /ridgeland/, /st-helena-island/; 12 in-post links on /does-your-roof-impact-your-energy-bill/ (4), /how-long-does-roof-last-hilton-head-humidity-salt-air/ (2), /how-your-roof-affects-a-home-sale-in-bluffton/, /new-construction-roof-installed-correctly/, /solar-panels-roof-hardeeville-sc/, /old-town-bluffton-approved-roofing-materials/, /top-questions-to-ask-your-roofing-contractor/, /why-ventilation-matters-how-your-roof-can-reduce-summer-cooling-costs/ | broken_link | 26 |
| F-031 | Low | XML sitemap lists redirecting URLs | /roof-inspections-in-bluffton-sc-…/, /emergency-roof-repair-in-hilton-head-island-sc-…/, /roof-repair-in-ridgeland-sc-…/, /transforming-homes-in-pritchardville-sc-…/, /brighten-your-beaufort-home-skylight-installation-…/, /replace-roof-before-or-after-hurricane-season-bluffton-sc/, /new-roof-before-selling-house-hardeeville-sc/, /new-construction-roof-warranty-hardeeville-sc/, /can-i-replace-my-roof-myself-beaufort-historic-district/ (full URLs in the worksheet) | sitemap | 9 |
| F-003 + F-027 | Low | Utility SEO titles: brand as "of The Lowcountry" and the ` \| ` separator | /blog/, /contact/, /terms-conditions/, /terms-conditions/accessibility-statement/, /terms-conditions/cookie-policy/, /terms-conditions/copyright-policy/, /terms-conditions/privacy-policy/ | seo_title | 7 |
| F-003 | Low | Footer About text writes "APEX ROOFING of the Lowcountry" / "APEX ROOFING'S" | sitewide footer (every page) | other (to Jonie — template edit) | 1 |
| F-025 (contact part) | Medium, routed to the Low batch by its recommendation | Contact page H1 → H3 "CALL US TODAY!" (no H2) | /contact/ | other (to Jonie — template edit) | 1 |

## 3 · Low items not in the Jonie batch (and why)

| Finding | Where it goes |
|---|---|
| F-033 alt text | System safe fix (`alt_text`, cap 5) via `/implement`, not a Jonie row |
| F-029 meta descriptions | Money pages: new metas come with the rebuilt drafts; category archives: Blog Decision Map |
| F-027 category-archive double space, F-031 archive sitemap inclusion | Blog Decision Map (archives' fate decided there first) |
| F-027 two post titles, F-026 | Blog Decision Map (Agent 4) |
| F-008 GBP website field | GBP kind (owner Gwen), waits on GBP manager access — not technical, not a blocker |
| F-032 homepage blog feature | Homepage rebuild (last), after the Blog Decision Map |
| /about/ title (F-003, F-027) | Covered by F-015 (About rebuild) — not retitled twice |
| F-010 /metal-roofing-2/ slug | Needs Evidence (CM-019) — no slug change; links pointed at /metal-roofing-2/ meanwhile (F-030) |

## 4 · Notes for Paul

- F-009's target is the approved default (/roof-replacement/). The client question `synthetic_roofing_offered` is still open; if the answer is "synthetic slate", the two redirects and the one in-post link are re-pointed to /slate-roofing/ in a later handoff.
- F-031 says 11 redirecting URLs; the sitemap capture shows 9 (the /contact entry in the sitemap is /contact/, which returns 200). The handoff carries the 9 the evidence shows.
- F-030 says 10 in-post links; the inlinks export shows 12 (8 posts). The handoff carries all 12.
