# Carolina Carpet Cleaning - Discovery Record - REVIEW

Run 20261028-154310-discovery-622b · 2026-10-28 · public sources only (S01–S03). **Observations and questions only —
no severity, no priorities, no recommendations** (the audit produces findings). Confidence per
`client-intake/references/discovery.md`: verified · found · inferred · unknown. Conflicts keep every candidate value
(PROC-01). Facts are in `facts.json` (Brand Guide A/D rows are generated from it).

## S01 · Intake (from status.json / facts.json)
| Field | Value | Source |
|---|---|---|
| Domain | carpetcleaningblufftonsc.com | intake |
| Industry | carpet cleaning (not a sensitive category: `status.py classify`) | intake |
| Storefront or SAB | SAB; address still shown on the website | Paul, 2026-10-28 (Paul Approved) |
| GBP link | https://maps.app.goo.gl/vvsrqH6TxL815KWB6 → cid 3992053166300574362, kg /g/11q4kbkjbt, pin 32.2743863, -80.8803687 | Paul, 2026-10-28 |
| GBP website field | https://carpetcleaningblufftonsc.com/ | Paul, 2026-10-28 |
| GA4 | none | Paul, 2026-10-28 |
| CMS / connection | WordPress; Novamira MCP read-only (settled) | decisions-settled.md |
| Search Console | exports supplied in `inputs/` (coverage + per-page performance, 2026-10-28) | inputs/ |

## S02 · Public sources

### Website (self-reported — `found`)
| Claim | Verbatim | URL |
|---|---|---|
| Name | "Carolina Carpet Cleaning" | footer, all pages |
| Address | "273 Club Gate, Bluffton, SC 29910" | footer; /contact-us/; /about/; schema |
| Phone (A) | "(843)-575-6286" — header, footer, contact, schema `+1-843-575-6286`, tel:8435756286 ×5 | https://carpetcleaningblufftonsc.com/ |
| Phone (B) | hero "Call" button `tel:8435256288` | https://carpetcleaningblufftonsc.com/ |
| Founding | "In Business Since 1993"; "Bluffton's Trusted Low-Moisture Cleaning Specialist Since 1993"; "Over 30 years of cleaning floors in the Lowcountry" | home |
| Founding | "has served the South Carolina Lowcountry since 1993" | /about/ |
| Ownership | "Family Owned & Operated"; "We are a local, family-owned business — not a franchise." | home |
| Ownership | "Locally owned, not a franchise" (no "family") | /about/ |
| Drying | "Dry in Under 1 Hour"; "walk on your floors in under one hour" | home; /about/ |
| Products | "pH-neutral and biodegradable" | home |
| Rugs | "Delicate or heirloom rugs are dye-tested before cleaning." | home |
| Estimate | "No deposit is required to schedule an appointment" (free estimate before work begins) | home |
| Hours, email | not shown | home; /contact-us/ |
| Certifications, insurance, guarantees, awards | none stated | home; /about/ |
| Owner | not named in copy; About image file "Owner-Kevin-Snow" | /about/ |
| Homepage title | "Carpet Cleaning in Hilton Head Island Metro Area - Carolina Carpet Cleaning" | home |
| Homepage H1 | "Carpet Cleaning in the South Carolina Lowcountry" | home |
| Canonical host | https://carpetcleaningblufftonsc.com/ (http, www → 301; rel=canonical matches) — `verified` (live check) | — |
| Domain registered | 2019-11-12 (WHOIS, NameCheap) — lower bound only | WHOIS |

Schema on the homepage (observations): `@type ["LocalBusiness","Corporation"]`, foundingDate "1993", telephone
+1-843-575-6286, geo 32.208585, -81.001304 (the GBP pin is 32.2743863, -80.8803687, on Club Gate Drive per
OpenStreetMap reverse lookup); areaServed lists 4 cities; hasMap cid=3992053166300574362; sameAs facebook.com/
CarolinaCarpetCleaning + yelp.com/biz/carolina-carpet-cleaning-bluffton. The JSON-LD block has a trailing comma in
`areaServed` (`json.loads` fails: "Illegal trailing comma ... line 31").

Services named on the site (nav + pages + schema): Carpet Cleaning · Residential Carpet Cleaning · Commercial Carpet
Cleaning · Low-Moisture Carpet Cleaning · Carpet Stain Removal · Pet Odor Removal · Upholstery Cleaning · Tile & Grout
Cleaning · Hardwood Floor Cleaning · Oriental Rug Cleaning ("Oriental & Area Rug Cleaning" in schema) · Area Rug
Cleaning · Boat & Auto Interior Cleaning. Press release adds "RV, and camper interiors".

Towns named on the homepage (18): Bluffton, Hilton Head Island, Beaufort, Hardeeville, Ridgeland, Lady's Island
(published location pages) · Okatie, Port Royal, St. Helena Island, Burton, Lobeco, Frogmore, Dale, Fripp Island, Sun
City, Daufuskie Island, Seabrook, Yemassee (WordPress drafts, 2026-10-27). Also a published "Bluffton Neighborhoods" page.

### Google Business Profile
Not machine-readable (Maps returns an empty shell). Known from the URL only: place name "Carolina Carpet Cleaning",
cid 3992053166300574362, pin on Club Gate Drive, Bluffton 29910 (`inferred`, OSM reverse lookup). Primary/secondary
categories, rating, review count, hours, phone shown: **unknown** → Gwen (H-2026-10-28-01).
Possible second listing: Google "Carolina Carpet, Hardwood, & Tile" (ludocid 15026650423285168794) surfaced in a phone
search — owner unknown → Gwen.

### Government records
- SC Secretary of State: CAPTCHA-gated (businessfilings.sc.gov); OpenCorporates CAPTCHA-gated → **unknown** → Gwen.
- Trade licence: no South Carolina LLR licence class for carpet cleaning was found (state licensing in SC is
  municipal business licences, e.g. Town of Bluffton) — `inferred` from lower-authority guides; the client's local
  business licence is a client fact (proof sheet).

### Third-party profiles
| Source | What it shows | URL |
|---|---|---|
| Press release, 2026-04-30 (self-issued) | "Founded in 1993"; contact "Kevin Snow"; 273 Club Gate Bluffton; 843-575-6286; "you're getting the owner on every job"; "free estimates and same-day service"; "five-star rating across multiple platforms"; areas "Bluffton, Hilton Head, Beaufort, Lady's Island, St. Helena, Hardeeville, and Ridgeland" | https://news.marketersmedia.com/carolina-carpet-cleaning-celebrates-32-years-of-professional-floor-and-carpet-cleaning-in-bluffton-and-the-lowcountry/89190379 |
| Birdeye (unclaimed) | "5922 Pleasant Farm Dr, Beaufort, SC, 29906"; "5.0"; "29 reviews"; "open 24/7"; category "Home Services" | https://reviews.birdeye.com/carolina-carpet-cleaning-166418659516441 |
| Yola site | "Call us today! 843-525-6288" (search snippet; page 403) | https://carpetcleaningbeaufortsc.yolasite.com/ |
| Facebook (footer link) | page name "Carolina Carpet Cleaning \| Beaufort SC"; rest not readable | https://www.facebook.com/carpetcleaningbeaufortsc |
| Facebook (schema sameAs) | page name "Jack Blaine Beers Jr." | https://www.facebook.com/CarolinaCarpetCleaning |
| Yelp (schema sameAs) | 403 to the system | https://www.yelp.com/biz/carolina-carpet-cleaning-bluffton |
Several unrelated "Carolina Carpet Cleaning" businesses exist (Columbia/West Columbia SC, Cornelius NC) — name
collision is an observation for entity disambiguation.

### Reviews (Birdeye mirror of Google, 5 of 29 visible)
Staff named: "Kevin" in all five ("Kevin is super professional and fast."; "Kevin showed up on time"). Services
mentioned: carpet after a pet accident, two sofas, move-out carpet cleaning. No towns named. Google's own count and
rating are not read yet.

## Conflicts (all candidates kept — PROC-01)
| Field | Candidates | Sources |
|---|---|---|
| Phone | (843) 575-6286 · (843) 525-6288 | site header/footer/schema/press release · site hero button + Yola site |
| Address | 273 Club Gate, Bluffton, SC 29910 · 5922 Pleasant Farm Dr, Beaufort, SC 29906 | site, press release, GBP pin area · Birdeye |
| Geo | 32.2743863, -80.8803687 · 32.208585, -81.001304 | GBP pin · site schema |
| Ownership wording | "family-owned" · "Locally owned" · "owner on every job" | home · about · press release |
| Facebook | facebook.com/carpetcleaningbeaufortsc · facebook.com/CarolinaCarpetCleaning (name "Jack Blaine Beers Jr.") | footer · schema |
| Founding | 1993 (site, schema, release) · domain 2019 (lower bound only) · SOS date unknown | — |

## S03 · Entity foundation (proposals — Paul decides, BB-105–BB-110)
- **Category entity:** GBP primary category unknown; proposed "Carpet cleaning service" → Wikipedia "Carpet cleaning"
  (Q5045777): "Carpet cleaning is performed to remove stains, dirt, debris, and allergens from carpets."
- **Area entity (Russian Doll, SAB → metro, BB-110):** Bluffton → Beaufort County (Q495682) → Hilton Head Island
  metropolitan area (Q17020871; "officially the Hilton Head Island–Bluffton–Port Royal, SC Metropolitan Statistical
  Area ... the two southernmost counties in the South Carolina Lowcountry"; Beaufort + Jasper (Q112957)). Contains
  17 of 18 towns wholly; Yemassee is "a town in Hampton and Beaufort counties" (Hampton Q497880 is outside the MSA).
  Next level: South Carolina Lowcountry (Q3885311). State: South Carolina (Q1456).
- **Variants and the reserved homepage variant:** see the Decision Sheet and Brand Guide B1/B2.

## Open (not client questions yet — the proof sheet step decides what to ask)
Legal entity name and formation date · GBP categories, rating, hours · which phone is current · Birdeye address ·
"family-owned" wording · insurance, local business licence, certifications (e.g. IICRC) · who owns the two Facebook
pages, the Yola site and the "Carolina Carpet, Hardwood, & Tile" listing.
