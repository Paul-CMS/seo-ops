# Carolina Carpet Cleaning - Site Plan - REVIEW

**Status:** REVIEW — awaiting Paul (`site_plan`). Revision: run 20261029-104257-build-f364, 2026-10-29 (revises run
20261029-103448-build-a20e with Paul's answers A1 and A2). Source: the approved URL Decision Map (audit 2026-10-28,
approved 2026-10-29). Data: `build/site-plan.json`. Links are the wheel's (`wheel.py`, CM-064) — not listed here.

## What changed in this revision
- **A1 settled (`site_plan_a1_ladys_island`):** Lady's Island merges into /beaufort/. `loc-ladys-island` is no longer a
  page; /beaufort/ carries `replaces: /ladys-island/`, so the 301 /ladys-island/ → /beaufort/ is generated as a VA
  handoff row next to Beaufort's publish. Beaufort's page names Lady's Island as a town served. Lady's Island stays a
  settled served town (`towns_served`).
- **A2 settled (`site_plan_a2_homepage_services`):** the homepage links all 8 service pages (HP-11's 6-link cap waived
  by Paul). Pet Odor Removal and Boat & Auto stay on the homepage list.

## Summary

| Type | Pages | Batch |
|---|---|---|
| Service | 8 | pilot (1) + services (7) |
| Location | 5 | pilot (1) + locations (4) |
| County / metro hub | 0 | — (none planned; see Notes) |
| Homepage (light fixes, H1 locked) | 1 | home-about |
| About | 1 | home-about |
| **Total** | **15** | 4 batches |

Pilot: needed — new industry (carpet cleaning), CM-061 §9. Pilot = Carpet Cleaning + Bluffton.
All kept URLs stay as they are live. One new 301 (/ladys-island/ → /beaufort/, at publish). The four folded services
stay folded (settled F-008).

## Pages

| ID | URL | Replaces | Keyword | H1 (fixed) | Area variant | "The Best" (CM-020) |
|---|---|---|---|---|---|---|
| svc-carpet-cleaning | /carpet-cleaning/ | — | carpet cleaning | Home Carpet Cleaning in the South Carolina Lowcountry | South Carolina Lowcountry | No — live "The Best…" removed |
| svc-commercial-carpet-cleaning | /commercial-carpet-cleaning/ | — | commercial carpet cleaning | Business Carpet Cleaning in the Lowcountry | Lowcountry | No |
| svc-rug-cleaning | /rug-cleaning/ | — | rug cleaning | Area and Oriental Rug Cleaning in the South Carolina Lowcountry | South Carolina Lowcountry | No |
| svc-upholstery-cleaning | /upholstery-cleaning/ | — | upholstery cleaning | Furniture Upholstery Cleaning in the Lowcountry | Lowcountry | No |
| svc-tile-grout-cleaning | /tile-grout-cleaning/ | — | tile and grout cleaning | Tile Floor and Grout Cleaning in the South Carolina Lowcountry | South Carolina Lowcountry | No |
| svc-hardwood-floor-cleaning | /hardwood-floor-cleaning/ | — | hardwood floor cleaning | Wood Floor Cleaning in the Lowcountry | Lowcountry | No |
| svc-pet-odor-removal | /pet-odor-removal/ | — | pet odor removal | Pet Urine Odor Removal in the South Carolina Lowcountry | South Carolina Lowcountry | No |
| svc-boat-auto-interior-cleaning | /boat-and-auto-interior-cleaning/ | — | boat and auto interior cleaning | Boat and Car Interior Cleaning in the Lowcountry | Lowcountry | No |
| loc-bluffton | /bluffton/ | — | carpet cleaning bluffton sc | Carpet Cleaners in Bluffton | — | No |
| loc-hilton-head | /hilton-head/ | — | carpet cleaning hilton head | Carpet Cleaners in Hilton Head Island | — | No |
| loc-beaufort | /beaufort/ | /ladys-island/ | carpet cleaning beaufort sc | Carpet Cleaners in Beaufort | — | No |
| loc-ridgeland | /ridgeland/ | — | carpet cleaning ridgeland sc | Carpet Cleaners in Ridgeland | — | No |
| loc-hardeeville | /hardeeville/ | — | carpet cleaning hardeeville sc | Carpet Cleaners in Hardeeville | — | No |
| home | / | — | carpet cleaning bluffton sc | Carpet Cleaning in the South Carolina Lowcountry (locked, HP-08) | reserved (B1) | n/a |
| about | /about/ | — | carolina carpet cleaning | About Our Carpet Cleaning Company in the Lowcountry | Lowcountry | n/a |

FAQ topics with their one-line reason are in each JSON row (`faq`): services 4–6 each, locations three (one per
location-faq.md category). Beaufort's logistics FAQ now covers booking from Beaufort or Lady's Island. Section C3 is
empty, so no registry clash; no topic repeats across pages.

## "The Best" (CM-020)
Fails on every page at condition 3 (Proof): the Google rating is Disputed (client 6 vs Google data 29, F-002, not
recorded per CM-027) and Section D has no awards. No DataforSEO spend was needed. No page is in the top 3 for its main
keyword, so no H1 lock applies except the homepage's settled HP-08 lock. Brand Guide H2 rows are added at write-back.

## Checks
- **URL rule (`urlcheck.py`):** pass — every planned URL follows the URL rule (re-run this revision).
- **Link wheel (`wheel.py check`):** 0 errors, 1 other — the HP-11 homepage count line, answered by A2 (all 8), not an
  open Ask (flag F-010: the script does not read the settled key). **Defect found (flag F-009):** the wheel still links
  /ladys-island/ from every service page and every location's sibling table, because `status.py plan` keeps a page
  dropped from the plan in status.json. The plan is correct; the wheel must not be generated for drafts until a system
  fix removes the merged page. Not a choice for Paul here — a system session item.
- **Duplicates:** none — one page per service and per town; keywords distinct.
- **Variant conflicts (CM-013/CM-024):** service H1s share two B2 variants (correct under CM-024); the reserved title
  variant (Hilton Head Island Metro Area) is on no page but the homepage; "Hilton Head Island–Bluffton–Port Royal area"
  is kept out of service H1s (it names cities, BB-314). Each service H1 uses a service variant different from its title.
- **Claims in keywords/variants (CM-049):** none — no emergency, 24-hour, certified, licensed or same-day term.
- **PAA coverage (CM-045):** 9 rows routed to service FAQs, all homed — #2, #12 → /carpet-cleaning/; #6, #7 →
  /hardwood-floor-cleaning/; #10, #11, #13, #15 → /rug-cleaning/ (#11 + #15 merged, #13 answered inside #10). Cost
  questions are answered without figures — pricing is not in Section D.
- **Fan-out coverage:** `data/fanout/fanout-routing.md` does not exist (S21 not run) — nothing to home.
- **Viability:** the five kept towns scored 6/7; Lady's Island (1/7) is merged (A1).

## Ask rows (kind 1 — page decisions) — all answered

| # | Page | Finding | Answer (settled) |
|---|---|---|---|
| A1 | loc-ladys-island (/ladys-island/) | Viability 1/7 — no local facts could be sourced | **a — merged into /beaufort/**; 301 /ladys-island/ → /beaufort/ as a VA handoff at publish; Beaufort names Lady's Island as served (`site_plan_a1_ladys_island`, Paul 2026-10-29) |
| A2 | home (/) | 8 service pages vs HP-11's 6-link homepage list | **b — link every service page (all 8)** (`site_plan_a2_homepage_services`, Paul 2026-10-29) |

No open choice remains. One open system item (F-009, above) blocks generating the link wheel, not the plan itself.

## Notes (recommended defaults, no open choice)
- **No hub.** Five location pages in two counties; the approved map plans none and the hub trigger is still a Coastal default.
- **Homepage:** light fixes only (F-026–F-030), H1 locked, one service H3 per service page (8); no review count until
  the Google figure is recorded.
- **/bluffton-neighborhoods/** keeps live (Needs Evidence); its link from /bluffton/ is a CM-022 exception for Finish.
- **Facts the writers will hit (facts round):** pricing, furniture moving, hours, rug pickup, grout sealing, RV/camper
  interiors, marina visits — `[NEED: …]` until answered.
