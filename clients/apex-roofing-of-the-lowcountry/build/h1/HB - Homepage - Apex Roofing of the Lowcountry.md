# HB - Homepage - Apex Roofing of the Lowcountry

Homepage brief · page `home` · batch **h1** · Route A
Run 20261013-140538-build-1832 · 2026-10-13 · Build agent (Agent 2)
Spec: `methodology/specs/homepage.md` (APPROVED 2026-10-08) · Site plan: APPROVED 2026-10-11
Evidence gate (CM-041): **WARN** — known 6 · unknown 3 · unverified 2 (1 required, 4 supporting). See **Evidence gaps**.
Evidence pack: `build/h1/packs/home.md` (rebuilt this run after the researcher's by-meaning check) — the writer's only fact source.
Pilot corrections: no `build/pilot-corrections.md` on file; Paul's pilot answers are settled decisions and apply here (owners credited, no titles; warranty terms only in a replacement context).

---

## 1 · Page assignment

| Item | Value | Source |
|---|---|---|
| Page type | Homepage — the brand hub: who Apex is, what it does (Roofing Contractor), where (the metro area) | spec §1 |
| Final URL | https://apexroofingtlc.com/ (unchanged) | URL Decision Map |
| Main keyword | roofing company hilton head island metro area | site plan §2 / D-1, Paul choice 1a |
| SEO title (90 chars) | `Apex Roofing of the Lowcountry - Roofing Contractor - Hilton Head Island Metropolitan Area` | spec 0b; BG-B1; F-004 ("Metro" → "Metropolitan", never shortened) |
| Meta (proposed, 152 chars) | `Apex Roofing of the Lowcountry repairs and replaces roofs across Beaufort and Jasper Counties, from metal to slate. Free estimates: call (843) 757-2739.` | spec 0c |
| H1 | **Locked as live: "The Best Residential Roofer in the South Carolina Lowcountry"** — never changed (BB-313 §3, HP-08; DEC-LOCAL-014). The live source has two spaces before "in"; HTML shows one, so the draft writes one space and the visible text is unchanged. | DEC-LOCAL-014; F-006 (withdrawn) |
| "The Best" (CM-020) | Kept only because the live homepage H1 is locked (HP-08). No other element on the page uses "best" or any superlative. | HP-07/HP-08 |
| Category variants | Title: Roofing Contractor (B1) · H1: Residential Roofer · body/H2s: Roofer, Roofers, roofing contractor | BG-A3, B1 |
| Area variants | Title: Hilton Head Island Metropolitan Area (B1, reserved — homepage only) · H1: South Carolina Lowcountry · body/H2s: Beaufort and Jasper Counties, Hilton Head Island–Bluffton–Port Royal metropolitan area, Lowcountry | BG-A6, B1, B2 |
| Claims in keyword/variants (CM-049) | None | site plan JSON |
| Link targets | All 8 services as H3 links (Paul Exception DEC-LOCAL-012, BB-313 §6 max 5–6 waived) · the 12 towns in the areas grid. Placeholders only — Finish fills (CM-005) | site plan; settled `homepage` |

### Variant chain (HP-09, CM-024 — no variant at two consecutive elements)

| Element | Category term | Area term |
|---|---|---|
| URL `/` | — | — |
| Title | Roofing Contractor | Hilton Head Island Metropolitan Area (reserved) |
| H1 (locked) | Residential Roofer | South Carolina Lowcountry |
| First H2 (services) | **Roofer** | **Beaufort and Jasper Counties** |
| Opening paragraph (third set) | roofing contractor / roofers | Hilton Head Island–Bluffton–Port Royal metropolitan area (body only) |
| FAQ H2 (fresh pair) | Roofers | Lowcountry |

Suggested headings (writer may re-word inside the rules; each sayable as a question; no city in any H tag; none may repeat a C3 heading — the Roof Repair FAQ H2 "What Do Homeowners Ask a Lowcountry Roofer About Repairs?" and the Bluffton H2 "What Should Bluffton Homeowners Know Before Hiring a Roofer?" are close, so stay clear of both):
- Services H2: *Which Roofer Services Do We Offer in Beaufort and Jasper Counties?*
- Trust H2: *Who Is Apex Roofing of the Lowcountry?*
- Gallery H2: *What Do Our Finished Roofs Look Like?*
- Testimonials H2: *What Do Lowcountry Homeowners Say About Apex?*
- FAQ H2: *What Do Homeowners Ask Lowcountry Roofers Before They Call?*
- Service areas H2: *Where Across the Lowcountry Does Apex Roof Homes?* (not the location pages' "Which Towns Near … Do We Also Serve?" shape)
- Final CTA H2: *Ready for a Free Estimate From Apex Roofing of the Lowcountry?*

---

## 2 · Element order (spec §3, BB-313's 17 parts)

| # | Element | Requirement for this page | Facts (status, from the pack) |
|---|---|---|---|
| 0a–0c | URL, title, meta | As §1 | BG-A1, A2, A6 (B1), A9 |
| 1 | Review bar (no H tag) | "5.0 from 67 Google reviews" — the figure as checked; Jonie refreshes the count at publish. Never written as a fact about the work (CM-027). | `d-google-rating…` Internally Verified (2026-10-07) |
| 2 | Navigation | Theme-level; top-level pages only; no H tags | — |
| 3 | H1 | Locked (§1) | — |
| 4 | Opening (no H tag, 60–120 words) | **First sentence answers who, what, where:** Apex Roofing of the Lowcountry is a residential roofing contractor based in Bluffton that repairs and replaces roofs across the Hilton Head Island–Bluffton–Port Royal metropolitan area. Then: founded in 2015 by Ralph and Pierce Brehany, father and son, who both get on the roof; free estimates; phone **(843) 757-2739**. Homes only (residential). Write it as the brand-level promise; do not reuse any service or location page's opening angle. | Founding 2015 Paul Approved · owners, no titles Paul Approved · who goes on the roof Paul Approved · free estimates Paul Approved · residential only Paul Approved · SAB based in Bluffton Paul Approved |
| 5 | H2 services ("[GB Category variant] Services") | The only H2 that introduces services. | — |
| 6 | H3 service links | **All 8**, one H3 anchor link each, no descriptions, in this order: Roof Repair · Roof Replacement · Roof Installation · Roof Inspections · Emergency Roof Repair · Metal Roofing · Slate Roofing · Skylights. Link rows stay placeholders: `| [Link wheel: populate service links here] |` (the wheel uses `/metal-roofing/`, not `/metal-roofing-2/`). | Services offered Paul Approved; DEC-LOCAL-012 |
| 7 | H2 trust / about | Sub-items are **styled cards, not H3s**. Cards (Section D only): (a) **Family owned since 2015** — Ralph and Pierce Brehany, father and son, both on the roof; (b) **Factory-certified installer** — CertainTeed and GAF ("many homeowners do have a preference" — client's words, Client Confirmed); CertainTeed ShingleMaster (Paul Approved 2026-10-09); (c) **Licensed and insured** — SC License #57706, Town of Bluffton License #0620033323; general liability and workers' compensation; (d) **Warranties on a new roof** — lifetime no-leak workmanship warranty and 50-year limited lifetime manufacturer warranty, both transferable, plus SureStart PLUS (replacement context only — pilot correction); (e) **BBB A+** profile since March 2021 (never "accredited"). One line from customers may sit under the cards at its tier: customers mention clear communication and daily clean-up (checked by meaning, 32 and 14 reviewers). | Certifications Client Confirmed · ShingleMaster Paul Approved · licence numbers + current Paul Approved (status cell) · insurance Paul Approved · warranty terms Paul Approved · BBB Paul Approved · reviews: `practice:explains` 32 ✓, `practice:clean-up` 14 ✓ |
| 8 | How It Works (3 steps, bold, no H tags) | 1 **Call for a free estimate** — (843) 757-2739, Mon–Sat 8 AM–5 PM. 2 **Ralph or Pierce comes out and gets on the roof** — you get photos of what they find. 3 **The work, done and cleaned up** — clean-up each day and a magnet sweep for loose nails; photos as the job goes (progress photos each day on a longer job). No time promise anywhere. | Hours, photos, clean-up, magnet sweep, who goes on the roof: Paul Approved |
| 9 | Social proof bar (no H tag) | Rating/count as part 1; HomeAdvisor 4.8 / 53 may sit beside it (Paul: "looks accurate"). | Internally Verified |
| 10 | H2 gallery | Real project photos only: `[NEED: 6–9 real Apex project photos from the client, each with its town and roof type, for the gallery]`. Alt text `[service type] in [city], South Carolina — Apex Roofing of the Lowcountry`, cities varied. No stock photos. | — |
| 11 | H2 testimonials | 3–4 real Google reviews, quoted short, **no reviewer names**, chosen to show different services and places. Candidates from the pack: row 2 (2026-08-31, a replacement — clean-up "superb each day"); row 14 (2024-01-03, a new roof installation by the local family business); row 15 (2023-12-29, an inspection with photos and a written report the next day). One more naming a town if available in the pack (Hampton Hall in Bluffton, Sun City or Ridgeland are named in reviews). **Never** quote rows 11, 36, 44, 48 or 49 (they state a 10-year warranty that conflicts with the approved lifetime no-leak term). Testimonials are never restated as facts. | Reviews (customers' words, CM-027) |
| 12 | H2 FAQ + H3 per question | §3 below. 4–6 brand-level questions; first sentence is the full answer (40–60 words per answer). | BG-C3 checked |
| 13 | H2 service areas grid | The 12 towns as a plain grid, **not H-tagged per city**: Bluffton, Hilton Head Island, Okatie, Pritchardville, Beaufort, Port Royal, Lady's Island, St. Helena Island, Fripp Island, Hardeeville, Ridgeland, Levy. Link rows placeholder: `| [Link wheel: populate service-area links here] |`. Never "Coastal Georgia" (F-001, R1). | BG-E; settled `business`, `loc_towns_served` |
| 14 | Google Maps embed (no H tag) | GBP iframe: `[NEED: Google Maps share link for the GBP (Brand Guide F hasMap is empty)]`. The GBP is a service-area business with the address hidden — embed the profile, not a street pin. | BG-F (empty) |
| 15 | Featured blog posts | **Leave out** — the Blog Decision Map is not approved and no blog redirect is live (BB-313 §15, HP-17; F-032). The live "Roofing Tips…" section is removed in the rebuild; it may return after the blog stage. | blog_map_approved not met |
| 16 | Final CTA (H2 naming an entity) | Free estimate + phone + hours; financing through Hearth in one line (never a rate or term — Client Confirmed, terms Unknown). | BG-A8, D |
| 17 | Footer (theme) | Zero H tags; NAP exactly: **Apex Roofing of the Lowcountry · 6 Sutton Ct, Bluffton, SC 29910 · (843) 757-2739** (website shows the street address; the GBP keeps it hidden). Theme work → Jonie at publish. | BG-F Paul Approved 2026-10-12 |
| — | Every H2 section | Under ~375 words; names its own entities; sayable as a question; no decorative headers ("Why Choose Us", "Our Process", "Get Started") | BB-308–310 |

**Specificity (CM-015, HP-22)** — page-specific, verifiable:
1. Founded in 2015 by Ralph and Pierce Brehany, father and son, both on the roof (Paul Approved).
2. SC License #57706 and Town of Bluffton License #0620033323 (Paul Approved).
3. Factory-certified installer of CertainTeed and GAF; CertainTeed ShingleMaster (Client Confirmed / Paul Approved).
4. Lifetime no-leak workmanship warranty and 50-year manufacturer warranty, both transferable, on a new roof (Paul Approved).
5. BBB A+ since March 2021 (Paul Approved).

**Schema (HP-24):** two-node graph (Corporation + RoofingContractor), ID page `@id`, `sameAs`, `hasMap`, `WebSite` — Finish only; Brand Guide F still has empty rows.

---

## 3 · FAQ (site plan §1 topics, checked against C3 after the locations write-back)

| # | Question (H3) | Why it applies to this page | Routed rows | Answer source / status |
|---|---|---|---|---|
| 1 | Do you give free estimates? | the free estimate is company-wide — the same on every service | PAA #44 (homepage candidate, site plan §4c) | Yes — free estimates (Paul Approved). Say the estimate is how the homeowner gets a real price. **Do not** state that inspection reports are priced separately (W17 Submitted, `[NEED]` open) — leave that out. |
| 2 | Are you licensed and insured? | licence and insurance are company-wide | FO #156–#158 | SC License #57706 and Town of Bluffton License #0620033323, both current; general liability and workers' compensation insurance (Paul Approved, the same wording the approved service pages use). **Never** a licence class, "bonded" or an expiry date. |
| 3 | Do you travel outside the 12 towns on this page? | brand-level coverage question; the areas grid lists the towns, this answers the edges | — | Yes: Brays Island and as far as Lobeco (client's words), plus Spring Island, Callawassie Island, Harbor Island and Dataw Island (Paul Approved 2026-10-12); no travel fee and no minimum call charge (Paul Approved). Not Georgia — just the immediate Lowcountry (client's words). |
| 4 | Do you work on commercial buildings? | brand-level scope question — the live site and a GBP post said "homes and businesses" / "commercial" (R2, R3) | — | No — Apex roofs homes only, for now (Paul Approved 2026-10-06). One sentence on what that means: every job is a house. |
| 5 | How long has Apex Roofing of the Lowcountry been roofing Lowcountry homes? | the brand's track record — homepage-level, not on any other page | — | Since 2015 — the year only (exact date not settled). Founded by Ralph and Pierce Brehany. May add at its tier: customers mention dealing with Ralph and Pierce directly (checked by meaning: 45 and 19 reviewers). Say "since 2015" (it stays true; a count of years goes stale). |

**Decided for you (Fix and list):** the site plan's topic "Do you offer financing?" is **dropped from the FAQ** — the Levy page (approved 2026-10-12, C3) already carries "Can I finance a new roof on my Levy home?", whose answer is the same Hearth line (BB-316, one question per site). Financing stays on the homepage as one line in the final CTA. "Which towns do you serve?" is **reworded to FAQ 3** so it does not repeat the areas-grid H2 on the same page. FAQs 4 and 5 are added from the fallback topics (brand-level, Section D only) to keep 4–6 questions.

---

## 4 · Customer language (BG-I — words only, never facts, no names, CM-027)

- Work words: "new roof" · "roof replacement" · "re-roof" · "repair" · "inspection" · "estimate" / "quote" / "bid".
- Themes as angle, not claim: communication and explaining the job; honest assessment, no upselling; clean job site; photos and written reports; fair price, "not the lowest"; local family business (father and son).
- **Never echo:** "10 year workmanship warranty" / "10 year transferable warranty" (reviews rows 11, 36, 44, 48, 49 — conflict with the approved lifetime no-leak term); "absolute BEST" or any superlative from reviews; "free small fixes".

## 5 · Audit findings and failed spec checks

| Finding | Check | What this page does |
|---|---|---|
| F-004 rev 4 | HP-02, HP-03 | Title "Metro" → "Metropolitan" (reserved B1 variant in full) |
| F-006 (withdrawn) | HP-06, HP-08 | H1 kept exactly as live |
| F-023 rev 2 | HP-23, HP-15 | Adds the FAQ and gallery; review bar, social proof bar and Maps embed rendered in HTML; 8 service H3s (Paul Exception) |
| F-032 | HP-17 | Featured blog section left out until blog redirects are live |
| F-001 | — | "& Coastal Georgia" removed; never named |
| F-002 | HP-21 | Every claim from Section D (no D2 claim) |
| F-029 | 0c | Meta 150–160 chars |
| F-033 | HP-14 | Badge and testimonial images get alt text (Jonie / Finish) |
| F-007 | HP-24 | Schema in Finish only |
| F-011 | HP-07 | No new "best" anywhere (H1 lock only) |

## 6 · Must not appear

Georgia / "Coastal Georgia" · "homes and businesses" / commercial work · "payment arrangements" · any response time, "24 hour", "same-day" · "bonded" · a licence class or expiry · BBB "accredited" · any price or price range (service pages own them) · the review warranty lengths · reviewer names · Alex or any staff name other than Ralph and Pierce (BG-D named staff) · team size, trucks, jobs completed, "in-house team" (W24, Unknown) · any award or ranking (Unknown) · "best" / superlatives outside the locked H1 · service descriptions under the H3 links · city H tags · any cross-page link in prose or FAQ answers (`[LINK → /slug/ · reason]` only if genuinely wanted — CM-022 exception at Finish).

## 7 · Sibling context

- Every service and location page is approved (pilot 2026-10-09, services 2026-10-12, locations 2026-10-13). The homepage summarises the brand; it does not restate any page's content.
- Owned elsewhere — do not repeat: cost answers (Roof Repair, Roof Replacement, Metal, Slate), warranty FAQ (Roof Replacement "What warranty comes with a new roof?"), repair-or-replace (Roof Repair), emergency triage (Emergency Roof Repair), permits (Bluffton, Ridgeland, Okatie, Levy, Pritchardville), financing FAQ (Levy), "who works on the roof" FAQ (St. Helena Island).
- Same batch: the About page (brief written this run) owns the founder story, the credentials list in full and the service-area statement; the homepage trust cards stay short and worded differently.

---

## Evidence gaps

Gate **WARN** (run 20261013-140538-build-1832): 1 required and 4 supporting gaps.

| Fact (grid) | Need | Mark | What the writer does |
|---|---|---|---|
| Core services the business wants more of | required | Unknown (open client question `fact:home:core_services`, asked 2026-10-11) | All 8 services get equal H3 links in the order above (settled `homepage`). No service is singled out as the focus in the opening or cards. If the client answers, only the order of the H3s and one opening clause change. |
| Licence numbers and classes | supporting | Unverified (grid) | Numbers only, as Paul approved them (status cell "Paul Approved 2026-10-07"); never a class or holder. Open question `fact:d:licence_numbers` stays with the client. |
| Insurance / bonded | supporting | Unverified (grid) | "General liability and workers' compensation" (Paul Approved); never "bonded". |
| Awards and rankings | supporting | Unknown | Left out. The live "Recognition" badges are kept only if they are certifications already in Section D (CertainTeed, GAF, BBB); any other badge `[NEED: what each recognition badge is, before it ships]`. |
| Team size / trucks / jobs completed | supporting | Unknown | Left out; no "in-house team" claim. |

## Change log

| Date | Run | Change |
|---|---|---|
| 2026-10-13 | 20261013-140538-build-1832 | Brief written. Evidence gate re-run after syncing the settled named-staff answer (`named_staff_on_page`) into facts.json; review topics checked by meaning by the researcher. |
