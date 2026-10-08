# Apex Roofing of the Lowcountry - Recommendations - REVIEW

**Status:** REVIEW. Waiting on Paul (`audit_approved`). Built from the Finding Register and URL Decision Map as they stand after the S17 review, using the latest revision of each finding. Nothing here is implemented, and nothing goes to the client automatically.
**Date:** 2026-10-07, revised 2026-10-08 with Paul's rulings · **Runs:** 20261007-194242-discovery-9495, 20261008-073627-discovery-2c41 · **Site:** https://apexroofingtlc.com/ (72 URLs crawled)

**Read this first:**
- **All six page specs are DRAFT.** Paul accepted the audit as advisory on that basis (3a, 2026-10-08), and the specs get approved before Build. Every item that rests on a spec check is marked *advisory*.
- **Every item cites its finding** (F-###) and the research behind it.
- **There is no recommendation without research support.**
- **The Local Dominator reports' written advice is not used anywhere.** Only their measured ranks were read.

---

## 1 · Executive summary

**The site is clean technically:**
- One hop to the canonical host.
- No indexing blocks.
- No duplicate titles.
- The crawl was complete.

**The work is on the pages themselves.** The money pages were built to an older pattern:
- Brand-first titles on the service pages.
- "The Best" in every H1 with no recorded decision.
- H1s that repeat the title.
- City names in service-page headings.
- Missing sections on the location and service pages.

There are also claims the client has not yet confirmed: the price ranges differ from town to town, and ShingleMaster status is unconfirmed. And two lines contradict your decisions: "Coastal Georgia" on the homepage, and "homes and businesses" on the About page.

**No page needs to be removed, merged or redirected.** No URL meets the four CM-019 conditions:
- Citations were skipped, so condition 3 is unknown.
- The client has not been asked about leads, so condition 4 is unanswered.

So the plan is to rebuild in place. The only redirect work is two repairs: an old URL that redirects to a 404, and moving `/metal-roofing-2/` to a clean slug, which is "Needs Evidence".

**The numbers:**
- **30 findings:** High 3 · Medium 18 · Low 9 (CM-028).
- **URL Decision Map, 83 rows:** Keep 78 · Redirect (fix / new 301) 2 · Merge 0 · Needs Evidence 3.

## 2 · Before you approve

**Nothing in this section is still open for a decision.** The items below were resolved by Paul's rulings (2026-10-07 and 2026-10-08). The client confirmations are not decisions; they are collected through the client-confirmation list (section 7) and don't block `audit_approved`.

1. **HP-06 vs BB-304 (CF-LOCAL-002) — resolved, Paul 2026-10-08.**
   - The reserved homepage variant "Hilton Head Island Metropolitan Area" goes in the homepage SEO title.
   - A familiar pool variant goes in the H1.
   - The live homepage H1 stays locked (BB-313 §3). If it is ever rebuilt: "Lowcountry" or "South Carolina Lowcountry".
   - The HP-06 wording is corrected when the specs are approved (DEC-LOCAL-014).
2. **About page — resolved, Paul 2026-10-08 (DEC-LOCAL-015).**
   - Title: "About Apex Roofing of the Lowcountry - Roofing Contractor in the Hilton Head Island–Bluffton–Port Royal Metropolitan Area".
   - H1: "About Apex Roofing of the Lowcountry".
   - Owners: Ralph and Pierce Brehany by name only, with a clearly visible placeholder for their photo and job titles.
3. **Specs DRAFT — resolved (3a, Paul 2026-10-08).** The audit is accepted as advisory; the specs are approved before Build (DEC-LOCAL-016).
4. **Brand Guide B2 and service titles — resolved.** B2 is now aligned with Gate B 1a: service titles are `Service Name - Brand` with no area term (DEC-LOCAL-011, DEC-LOCAL-017).
5. **Homepage services block — resolved.** All 8 services are H3 links (Paul Exception, Gate B 2a, DEC-LOCAL-012).
6. **Client confirmations — in progress, not a decision** (section 7):
   - Port Royal base housing.
   - Synthetic-roofing redirect target.
   - ShingleMaster status.
   - One price range.
   - The other claims in F-002.

## 3 · Decisions already made (respected throughout)

- **Entity:**
  - Category: Roofing Contractor (variants Roofing Contractor, Roofer, Roofers).
  - Area: Hilton Head Island–Bluffton–Port Royal MSA.
  - Reserved homepage variant: "Hilton Head Island Metropolitan Area" (re-approved 2026-10-08), used in the homepage SEO title only.
  - "Hilton Head Island–Bluffton–Port Royal Metropolitan Area" is now a pool variant.
  - Homepage H1: a familiar pool variant ("Lowcountry" or "South Carolina Lowcountry"). The live H1 is locked.
- **Brand in SEO titles:** always written in full, "Apex Roofing of the Lowcountry". "Lowcountry" variants are never added on top in an SEO title.
- **Service titles:** `Service Name - Apex Roofing of the Lowcountry`, with no area term (Q1 = 1a, DEC-LOCAL-011).
- **Homepage services block:** all 8 services as H3 links. This is a Paul Exception to BB-313 §6 (Q2 = 2a, DEC-LOCAL-012).
- **Scope of work:** residential only; Georgia is not served; all 8 services and all 12 towns are kept.
- **Address:** Service-area business based in Bluffton. The address stays hidden on the GBP; the public location is "Bluffton, SC 29910".
- **FAQs:** a FAQ or PAA question is used only if it is town-specific or tied to the page's service, and actually applies (DEC-LOCAL-004).

## 4 · Recommendations, by when and who

### A. In the site plan and page rebuilds (Build — after discovery sign-off; advisory where spec-based)

| # | Recommendation | Findings | Severity |
|---|---|---|---|
| A1 | Retitle the 8 service pages `[Service] - Apex Roofing of the Lowcountry`, with no area term *(advisory)* | F-014 | High |
| A2 | Remove city names from service-page H tags. City angles move to that city's FAQ only if they pass your FAQ note *(advisory)* | F-022 | High |
| A3 | Rebuild the About page to Paul's ruling (DEC-LOCAL-015): title "About Apex Roofing of the Lowcountry - Roofing Contractor in the Hilton Head Island–Bluffton–Port Royal Metropolitan Area"; H1 "About Apex Roofing of the Lowcountry"; Ralph and Pierce Brehany by name only, with a clearly visible placeholder for their photo and job titles *(advisory)* | F-015, F-016 | High / Medium |
| A4 | Drop the "Coastal Georgia" and "homes and businesses" wording. Repeat Port Royal base-access lines only if the client confirms that work | F-001 | Medium |
| A5 | Use only confirmed claims: one confirmed price range or none; ShingleMaster only if confirmed; code claims with a named source; no job titles in the author box | F-002 | Medium |
| A6 | Make the CM-020 "The Best" decision per page and record it in the Decision Map and Brand Guide H2. On current evidence condition 2 is unmeasured everywhere, so the rebuilt H1s drop "The Best" unless new evidence passes. Homepage H1 unchanged | F-011 | Medium |
| A7 | Give every H1 a different variant from its title (14 pages fail the restate test). No variant may repeat from one element to the next *(advisory)* | F-012 | Medium |
| A8 | Rebuild the 8 service pages in BB-314 order: add the "how it's delivered" H2; the CTA has no H tag *(advisory)* | F-018 | Medium |
| A9 | Rebuild the 12 location pages in CM-023 / BB-315 order: add real Things to Do and Top Sites; the CTA carries the NAP "Apex Roofing of the Lowcountry, Bluffton, SC 29910, (843) 757-2739" *(advisory)* | F-019, F-020 | Medium |
| A10 | Openings: who/what/where first, then the phone number and the confirmed free-estimate offer. Fix the 4 unfinished sentences *(advisory)* | F-017 | Medium |
| A11 | FAQs: one owner page per question. Location FAQs are about that town; generic cost, permit and storm questions go once to the matching service page or to a blog topic *(advisory)* | F-021 | Medium |
| A12 | Neighbourhoods: 6–12 real, sourced names per city; no road corridors; no name on two pages; "Parris Island" spelled correctly *(advisory)* | F-024 | Medium |
| A13 | Heading order H2 → H3 with entity-named headers (About, Bluffton, Port Royal; Contact template) *(advisory)* | F-025 | Medium |
| A14 | Homepage (built last): add a brand-level FAQ (4–6 questions) and a real-project gallery; all 8 service H3 links; H1 unchanged *(advisory)* | F-023 | Medium |
| A15 | Homepage title: change one word, "Metro" → "Metropolitan": "Apex Roofing of the Lowcountry - Roofing Contractor - Hilton Head Island Metropolitan Area" (reserved variant in full) | F-004 | Medium |
| A16 | Featured-blog block on the homepage only after the blog redirects are live *(advisory)* | F-032 | Low |

### B. Structural — after `entity_approved` (met) and `brand_guide_approved`

The new titles from A1, A3 and A15 go live through the WordPress pilot or a VA handoff to Jonie.

**Metal Roofing slug (F-010, Needs Evidence):** moving `/metal-roofing-2/` to `/metal-roofing/` waits on two things:
- Citations (S09).
- The client confirming that page brings no leads.

Until then the URL stays as it is, and internal links point straight to it.

### C. Safe fixes and the Low batch — after `audit_approved`, within the safe-fix caps

These go to Jonie as one technical handoff, unless the system makes the safe fix itself.

| # | Recommendation | Findings |
|---|---|---|
| C1 | Redirect `/services/synthetic-roofing/` and `/synthetic-roofing/` (301, full URLs) to a live page. Default target `/roof-replacement/`; `/slate-roofing/` if the client confirms synthetic slate. Fix the one internal link | F-009 |
| C2 | Point internal links at their final URLs: `/contact` → `/contact/` (header and CTA template), `/metal-roofing/` → `/metal-roofing-2/`, and 10 links inside posts | F-030 |
| C3 | Remove the 11 redirected URLs from the XML sitemap through SEOPress. Don't unpublish the posts; check where each redirect lives first | F-031 |
| C4 | Use the " - " separator everywhere. Write the brand exactly as approved in utility titles and the footer | F-027, F-003 |
| C5 | Meta descriptions on the 5 category archives. Money pages get theirs with the rebuild (150–160 characters) | F-029 |
| C6 | Alt text on the homepage badges (named only if confirmed) and the roof-installation image. Decorative images stay empty (cap: alt_text 5) | F-033 |

### D. GBP (Gwen) — once Paul confirms manager access

**D1:** Change the GBP Website field from `http://www.apexroofingtlc.com/` to `https://apexroofingtlc.com/`. The two "cannibalization" clusters were this host variant; this is not cannibalization (F-008).

### E. Finish (schema) and Blog

- **Schema (F-007):** build the BB-6xx v1.1 graph in Finish once pages are approved:
  - Homepage: two-node business graph with the ID page, `sameAs` and the Maps share link.
  - Service pages: `Service` nodes.
  - Blog posts: `Article` nodes.
  - Keep the SEOPress Knowledge Graph off.
- **Blog (F-026, F-028) — Blog Decision Map (`/blog`):**
  - Retitle the posts that are kept to `Post Title - Apex Roofing of the Lowcountry`.
  - Byline the 8 "Raven Paz" posts to the owner (CM-039) unless the client says otherwise.
  - The overlapping posts and the siding post have no observed search conflict. The Decision Map decides them, running Test B first.

## 5 · Measurement plan

- **No baseline is possible today.** There is no Search Console, GA4 or call tracking (S11 skipped).
- **The reference points we have:**
  - DataforSEO ranked keywords (41 keywords on 7 URLs, US, 2026-10-07).
  - Local Dominator grid ranks: "roof repair bluffton" local pack 6.99, maps 20+; "roofing contractor near me" local pack 19.29, maps 20+. Grid centre unverified.
  - Google rating 5.0 from 67 reviews (66 five-star, 1 two-star).
- **To re-measure:**
  - Re-run S07 and the same two grid scans 60 days after each batch ships. S07 is reusable data under 60 days old.
  - Re-crawl after release (Finish QA).
- **Optional:** if the client grants Search Console later, add it as S11. It would also unlock CM-030 questions.

## 6 · Assumptions and limitations

- **The specs are DRAFT** (advisory). Writing-quality checks (COM-02/06/07/12/13/14) were not scored; Build's self-critique covers them.
- **Basic crawl, no JavaScript.** These are not asserted as missing: review bar, Maps embeds, city maps, the contact form. Body text was read from free public page captures (MANUAL evidence).
- **Brand Guide D is not reconciled.** Claims were tested against the returned sheet and your answers only.
- **Rankings are US country-level.** They were used only for the CM-019 and CM-020 tests.
- **Fan-out queries carry no volume** and were never used as evidence.
- **Backlinks:** 694 of the 711 referring domains point to the homepage, and most are auto-generated SEO-checker sites. No action is recommended (CM-006).
- **Neighbourhood names** were checked for type and duplicates, not verified one by one.

## 7 · Client-confirmation list (Paul sends; nothing goes automatically)

1. **Port Royal:** does Apex work in base privatized housing and know the access process? This covers the "MCRD Paris Island" FAQ and the "on-base contractor access procedures" line (F-001).
2. **Synthetic roofing:** is it offered (shingle/shake or synthetic slate)? The answer sets the redirect target for `/services/synthetic-roofing/` (F-009).
3. **CertainTeed ShingleMaster:** is the certification current? The client confirmed "certified factory installers of both CertainTeed and GAF" (F-002).
4. **One roof-replacement price range.** Today's pages say $7,500–$14,000 up to $9,000–$20,000. Also the skylight prices and the Velux / FAKRO brands (F-002).
5. **Project history:** Sun City ("dozens of projects"), Sea Pines, Palmetto Dunes and the other named communities, and Fripp Island (F-002).
6. **Process claims:**
   - Photo documentation of every project.
   - Magnetic sweep.
   - Permit fees included in the estimate.
   - Same-day temporary seal.
   - One-day installs.
   - Paid inspection reports (F-002).
7. **The Lady's Island claim:** "largest residential community in Beaufort County" (F-002).
8. **Metal Roofing page:** only if the slug change is pursued, confirm the page brings no leads (F-010).

## 8 · Change preview (what would change, once approved — nothing changes yet)

| Area | Pages | Channel |
|---|---|---|
| Titles, H1s, sections, FAQs, openings, claims | homepage (H1 unchanged), 8 service, 12 location, About | Build: WordPress drafts → Jonie publishes |
| Redirect repair | `/services/synthetic-roofing/`, `/synthetic-roofing/` | Jonie redirect handoff |
| Internal links, sitemap, separators, meta, alt | sitewide templates, 13 + 10 links, SEOPress | safe fixes / Jonie Low batch |
| GBP Website field | GBP | Gwen |
| Schema | homepage, service, About, posts | Finish |
| Blog titles, bylines, keep/redirect | 24 posts, 5 archives | Blog Decision Map |
