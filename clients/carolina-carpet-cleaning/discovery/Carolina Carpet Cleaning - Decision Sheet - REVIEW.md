# Carolina Carpet Cleaning - Decision Sheet - REVIEW

**Every identity and format decision for this client, together, once** (R6). Defaults and evidence from public
research (run 20261028-154310-discovery-622b, 2026-10-28; details in the Discovery Record). **A blank *Answer* means the
default stands.** Approved with the entity foundation and the client facts in Approval 1 (`entity_approved
proof_sheet_approved`); then settled in `decisions-settled.md`. The audit and Build apply these and never re-ask.

| Key | Decision | Recommended default | Answer (Paul) | Evidence / why |
|---|---|---|---|---|
| category_entity | GBP primary category = the category entity | **Carpet cleaning service** → Wikipedia "Carpet cleaning" (Q5045777) — provisional until Gwen reads the GBP primary category (H-2026-10-28-01); if GBP shows another category, that category stands and this row reopens | | BB-106/107. GBP is not machine-readable; the site's whole service set is carpet/floor cleaning; Birdeye shows only "Home Services". |
| category_variants | Category variants (4–6) | carpet cleaning · carpet cleaning service · carpet cleaners · carpet cleaning company · carpet cleaner | | BB-109: common search phrasings of the Wikipedia entity; volumes are checked in the data step (no spend now). "Steam cleaning" excluded: Wikipedia calls it a misnomer and the site sells low-moisture cleaning. |
| scope_descriptor | Scope descriptor | **residential and commercial** (description only, never a category variant) | | Live pages /residential-carpet-cleaning/ and /commercial-carpet-cleaning/. |
| area_entity | Area entity | **Hilton Head Island metropolitan area** (official: Hilton Head Island–Bluffton–Port Royal, SC MSA; Q17020871). Alternative: **South Carolina Lowcountry** (Q3885311) if Yemassee must sit wholly inside | | BB-105/110 (SAB → metro). Path: Bluffton → Beaufort County → MSA (Beaufort + Jasper). 17 of 18 towns wholly inside; Yemassee is in Hampton and Beaufort counties. The Lowcountry also spans Charleston to Georgetown — far wider than the 18 towns. |
| area_variants | Area variants (3–5) | Hilton Head Island Metro Area · South Carolina Lowcountry · Hilton Head Island–Bluffton–Port Royal area · Lowcountry | | Wikipedia names (MSA article: "two southernmost counties in the South Carolina Lowcountry"; Lowcountry article: "sometimes Low Country"). |
| homepage_title_variant | Area variant reserved for the homepage SEO title | **Hilton Head Island Metro Area** (exclusive; the live title already uses it) | | CM-024. Live title: "Carpet Cleaning in Hilton Head Island Metro Area - Carolina Carpet Cleaning". |
| homepage_h1_variant | Area variant for the homepage H1 | **South Carolina Lowcountry** (the live H1) | | Live H1: "Carpet Cleaning in the South Carolina Lowcountry"; the site's own copy uses "the Lowcountry" throughout. |
| title_format.homepage | SEO-title format — homepage | `Category Variant in Area - Brand` | | Matches the live title. |
| title_format.service | SEO-title format — service pages | `Service Name - Brand` | | Template default. |
| title_format.location | SEO-title format — location pages | `Category Variant in City, ST - Brand` | | Template default. |
| title_format.about | SEO-title format — about page | `About Brand - Category in Area` | | Template default. |
| title_format.blog | SEO-title format — blog posts | `Post Title - Brand` | | Template default. |
| brand_in_titles | Brand written in full in every title | yes — "Carolina Carpet Cleaning" | | Several unrelated "Carolina Carpet Cleaning" firms exist in SC/NC; the full name plus area disambiguates. |
| service_list | Services offered | Carpet Cleaning · Residential Carpet Cleaning · Commercial Carpet Cleaning · Low-Moisture Carpet Cleaning · Carpet Stain Removal · Pet Odor Removal · Upholstery Cleaning · Tile & Grout Cleaning · Hardwood Floor Cleaning · Oriental Rug Cleaning · Area Rug Cleaning · Boat & Auto Interior Cleaning (RV/camper per press release) — which become pages or fold together is the audit's URL decision | | Site nav, page inventory (Novamira, 2026-10-28) and homepage schema `makesOffer`. The client confirms the list on the proof sheet. |
| towns_served | Towns served | The 18 towns on the homepage: Bluffton, Hilton Head Island, Beaufort, Hardeeville, Ridgeland, Lady's Island, Okatie, Port Royal, St. Helena Island, Burton, Lobeco, Frogmore, Dale, Fripp Island, Sun City, Daufuskie Island, Seabrook, Yemassee — page-or-hub per town is the audit's URL decision | | 6 published location pages + 12 WordPress drafts (2026-10-27). Press release lists 7. The client confirms edges on the proof sheet; Gwen reads the GBP service-area list. |
| address_display.gbp | Street address on GBP? | **No** (service-area business) | | Paul, 2026-10-28 (Brand Guide A4, Paul Approved). |
| address_display.website | Street address on the website? | **Yes** — 273 Club Gate, Bluffton, SC 29910 (pending the client's confirmation of the Birdeye Beaufort address conflict) | | Paul, 2026-10-28: "the address still appears on the website (helps map rankings)". |
| the_best_policy | "The Best" in H1s | per page, by CM-020 | | Proof test needs Google's own rating/count (Birdeye mirror: 5.0 · 29, undated, not Google). |
| blog_author | Blog author (a real person, CM-039) | **Kevin Snow**, owner — once the returned facts confirm him | | Press release contact "Kevin Snow"; reviews name "Kevin"; About image "Owner-Kevin-Snow". |
| sensitive_category | Sensitive category | **No** | | `status.py classify "carpet cleaning"` → not sensitive, no practitioner sign-off. |
| cms | The site's CMS | WordPress | | Settled 2026-10-28 (system detected). |
| wordpress_login | WordPress access for the system | **N/A — settled**: Novamira MCP, read-only until the handoff is approved; no Application Password | | decisions-settled.md (wp-connection, Paul 2026-10-28). |
| tools.citations | Citations data this audit | BrightLocal citation tracker (VA uploads the CSV) | | Agency profile §1. Two Facebook pages, a Yola site, Birdeye and a possible second Google listing make NAP data worth having. |
| tools.grid | Local grid tool | BrightLocal | | Agency profile §1 (DataforSEO grid is on one trial client only). |
| tools.gsc_ga4 | Search Console / Analytics | **Search Console: use the exports already supplied** (coverage + per-page performance, 2026-10-28); **GA4: not used** (none) | | inputs/ GSC zips; GA4 access "none" (Paul, 2026-10-28). |

**Not decisions (facts, on the proof sheet or Gwen's lookup):** which phone is current (575-6286 vs 525-6288), legal
entity name, the Birdeye Beaufort address, "family-owned" wording, the 1993 founding year against the SOS record.
