# [Client Name] - Decision Sheet - REVIEW

**Every identity and format decision for this client, together, once** (R6, Paul 2026-10-08). The discovery agent
fills the *Recommended default* and the *Evidence* from public research; Paul answers only where he disagrees — a blank
*Answer* means the default stands. It is approved with the entity foundation and the client facts in **Approval 1**
(`/approve <slug> entity_approved proof_sheet_approved`); approve.py then settles every row in
`clients/<slug>/decisions-settled.md`. The audit and Build **apply** these; they never ask them again. New
contradicting evidence → one reopen request (`run.py decision … --reopen <key>`), nothing more.

Why one sheet: at Apex the entity was approved three times because the area entity and reserved homepage variant
were decided before the title format per page type was known, and the street-address display was asked three times.
Everything that shapes a title, an H1 or what a page may claim is decided here, before the audit.

Keys are fixed (lowercase); do not rename them. Mark a row `N/A` with the reason when it does not apply (e.g. blog
author for a client with no blog).

| Key | Decision | Recommended default | Answer (Paul) | Evidence / why |
|---|---|---|---|---|
| category_entity | GBP primary category = the category entity (Wikipedia-verified, BB-106/107) | | | |
| category_variants | Category variants (4–6, real search terms, BB-109) | | | |
| scope_descriptor | Scope descriptor (e.g. residential, commercial): used as a description in H1s and body, never as a category variant unless it is a real Wikipedia entity | | | |
| area_entity | Area entity (Russian Doll path recorded, BB-105/110; contains every town served) | | | |
| area_variants | Area variants (3–5) | | | |
| homepage_title_variant | Area variant reserved for the homepage **SEO title** (exclusive, CM-024) | | | |
| homepage_h1_variant | Area variant for the homepage **H1** (may be the familiar local name) | | | |
| title_format.homepage | SEO-title format — homepage | `Category Variant in Area - Brand` | | |
| title_format.service | SEO-title format — service pages | `Service Name - Brand` | | |
| title_format.location | SEO-title format — location pages | `Category Variant in City, ST - Brand` | | |
| title_format.about | SEO-title format — about page | `About Brand - Category in Area` | | |
| title_format.blog | SEO-title format — blog posts | `Post Title - Brand` | | |
| brand_in_titles | Brand written in full in every title (no abbreviation) | yes | | |
| service_list | Services offered (each becomes a service page or is folded into one) | | | |
| towns_served | Towns served (each becomes a location page or is listed on its county hub) | | | |
| address_display.gbp | Street address shown on the Google Business Profile? | | | |
| address_display.website | Street address shown on the website? | | | |
| the_best_policy | "The Best" in H1s (CM-020: only where demand, opportunity, proof and not-sensitive all pass; never on a page already top 3) | per page, by CM-020 | | |
| blog_author | Blog author (a real person, CM-039) | the owner named on the returned facts | | |
| sensitive_category | Sensitive category (CM-025, CM-040) | from `status.py classify` | | |
| cms | The site's CMS (WordPress steps are N/A when it is not WordPress) | detected at /new-client | | |
| wordpress_login | WordPress login for the system: dedicated Editor (spec) or keep the Administrator | dedicated Editor | | |
| tools.citations | Citations data this audit (BrightLocal) — or skipped | | | |
| tools.grid | Local grid tool (BrightLocal / Local Dominator / none) | | | |
| tools.gsc_ga4 | Search Console / Analytics access — or not used | not used unless already shared | | |
