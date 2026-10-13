# AB - About - Apex Roofing of the Lowcountry

About brief · page `about` · batch **h1** · Route A
Run 20261013-140538-build-1832 · 2026-10-13 · Build agent (Agent 2)
Spec: `methodology/specs/about.md` (APPROVED 2026-10-08) · Site plan: APPROVED 2026-10-11 · Paul's ruling DEC-LOCAL-015 (title, H1, owner section)
Evidence gate (CM-041): **WARN** — known 4 · unknown 2 · unverified 2 (1 required, 3 supporting). See **Evidence gaps**.
(The first gate run this session blocked the page on "named staff"; that fact was already answered by Paul — settled `named_staff_on_page`, `about_page` — and its facts.json status still read Submitted. It was synced with `run.py fact` and the gate re-run: WARN.)
Evidence pack: `build/h1/packs/about.md` — the writer's only fact source.

---

## 1 · Page assignment

| Item | Value | Source |
|---|---|---|
| Page type | About — the people and credentials behind the brand | spec §1 |
| Final URL | https://apexroofingtlc.com/about/ (unchanged) | URL Decision Map |
| SEO title (121 chars) | `About Apex Roofing of the Lowcountry - Roofing Contractor in the Hilton Head Island–Bluffton–Port Royal Metropolitan Area` | DEC-LOCAL-015 (Paul 2026-10-08); settled `about_page` |
| Meta (proposed, 158 chars) | `Roofing contractor in Bluffton since 2015, repairing and replacing roofs across the Lowcountry. Meet Ralph and Pierce Brehany. Free estimates: (843) 757-2739.` | spec #3 |
| H1 | **About Apex Roofing of the Lowcountry** (carries the brand — Paul's ruling governs over ABT-03 for this client) | DEC-LOCAL-015 |
| "The Best" | No | — |
| Category variants | Title: Roofing Contractor · body/H2s: Roofer, Roofers, Residential Roofer | BG-A3 |
| Area variants | Title: Hilton Head Island–Bluffton–Port Royal Metropolitan Area (B2 #3 — never the reserved B1) · body/H2s: South Carolina Lowcountry, Lowcountry, Beaufort and Jasper Counties | BG-B2 |
| Keyword | none assigned (brand page) | site plan JSON |
| Claims in keyword/variants | None | site plan JSON |
| Links | None in prose. CTA has no links beyond the phone. | CM-005 |

### Variant chain (CM-024)

| Element | Category term | Area term |
|---|---|---|
| Title | Roofing Contractor | Hilton Head Island–Bluffton–Port Royal Metropolitan Area |
| H1 | — (brand only) | — |
| First H2 (owners) | must differ from the title — e.g. **Roofers** | **South Carolina Lowcountry** or none |
| Opening paragraph | roofer / residential roofer | Lowcountry · Beaufort and Jasper Counties |

Suggested headings (no decorative headers — "Our Story" or "Meet the Team" alone fail; name the entity; each sayable as a question):
- Owners H2: *Who Are Ralph and Pierce Brehany, the Roofers Behind Apex?*
- Credentials H2: *Which Licences and Certifications Does Apex Roofing of the Lowcountry Hold?*
- History H2: *How Did Apex Roofing of the Lowcountry Start in Bluffton?*
- Service area H2: *Where in Beaufort and Jasper Counties Does Apex Work?*

---

## 2 · Element order (spec §3)

| # | Element | Requirement for this page | Facts (status, from the pack) |
|---|---|---|---|
| 1–3 | URL, title, meta | As §1 | — |
| 4 | H1 | As §1; exactly one | — |
| 5 | Opening (no H tag, 60–120 words) | **First sentence: who, what, where** — Apex Roofing of the Lowcountry is a family-owned residential roofer in Bluffton, run by Ralph Brehany and his son Pierce, repairing and replacing roofs across Beaufort and Jasper Counties. Phone **(843) 757-2739**. Homes only. The opening must not reuse the homepage opening's sentence shape (same batch). | Named staff Paul Approved · residential only Paul Approved · SAB in Bluffton Paul Approved · phone Paul Approved |
| 6 | H2 owners | Ralph and Pierce Brehany, **father and son, credited as the owners, no job titles** (Paul, settled). Both get on the roof themselves (Paul Approved). At its tier: customers mention dealing with Ralph and with Pierce directly (staff:Ralph 45 and staff:Pierce 19 reviewers, checked by meaning 2026-10-13) — e.g. one short attributed line from the pack (row 4, 2026-08-15: met with both owners), no reviewer name. **Visible placeholder, by Paul's ruling:** `[NEED: photo of Ralph and Pierce Brehany]` and `[NEED: their job titles, only if the client wants titles published]`. Ralph is the blog author (CM-039) — no need to say so here. | `d-named-staff…` Paul Approved · `d-who-does-the-work` Paul Approved · reviews ✓ |
| 7 | H2 credentials (cards or a list) | **Section D only**: SC License #57706 · Town of Bluffton License #0620033323 (numbers, current — never a class, holder or expiry) · general liability and workers' compensation insurance (never "bonded") · factory-certified installer of CertainTeed and GAF, in the client's words "many homeowners do have a preference" · CertainTeed ShingleMaster · BBB profile with an A+ rating since March 2021 (never "accredited") · on a new roof: lifetime no-leak workmanship warranty and 50-year limited lifetime manufacturer warranty, both transferable, plus SureStart PLUS. Word the list differently from the homepage trust cards. | Licence Paul Approved (status cell) · insurance Paul Approved · certifications Client Confirmed · ShingleMaster Paul Approved · BBB Paul Approved · warranty Paul Approved |
| 8 | H2 team | **Merged into element 6** (decided for you — Fix and list): the only staff approved for on-page use are Ralph and Pierce (BG-D). Crew leader names that appear in reviews (Alex) are **not** used. Team size Unknown — no "in-house team" (W24). | BG-D named staff |
| 9 | H2 history / story | Founded **2015** (year only — the exact date is not settled; never "November" or "December"). Father-and-son ownership. **The owner's own account of how and why they started is not on file:** write `[NEED: Ralph's or Pierce's own account of how and why they started Apex in 2015 — open client question fact:about:company_story]` where the story would go; do **not** invent a story or infer one from reviews. At its tier: two reviews call it a local family business (rows 14, 54 — 1–2 reviewers → an attributed customer example only). How they work, as the company's view in fresh words (BG-G, Client Confirmed): a roof is not a commodity — the difference is in what you can't see (underlayment, sealed valleys, flashing, nail spacing, straight shingles). **Do not reuse** the sentences already on Roof Replacement (the "commodity / what you can't see" lines) or Roof Repair (the flashing / tube-of-silicone lines); paraphrase in one or two sentences. | Founding Paul Approved · BG-G Client Confirmed · company story Unknown |
| 10 | H2 service area | Area entity stated once: the Hilton Head Island–Bluffton–Port Royal metropolitan area (Beaufort and Jasper Counties); based in Bluffton; the 12 towns may be named in one plain sentence or list, **no per-city H tags, no links**. Do not repeat the homepage FAQ on Brays Island / Lobeco / the islands — one clause at most. Never Georgia. | BG-A5, E · settled `business` |
| 11 | FAQ | **Left out** (optional per spec): every brand-level question already has an owner (homepage FAQ, service and location pages); an About FAQ would duplicate (BB-316). | BG-C3 |
| 12 | CTA with NAP (no H tag) | Free estimate · (843) 757-2739 · Mon–Sat 8 AM–5 PM · NAP exactly **Apex Roofing of the Lowcountry · 6 Sutton Ct, Bluffton, SC 29910 · (843) 757-2739**. | BG-F Paul Approved 2026-10-12 · hours Paul Approved |
| — | Every H2 section | Under ~375 words; names its entities; no decorative headers (the live H5 "We Make Roofing Easy", "Transparency", "Commitment", "Quality" and H4 "Our Values" go — F-025) | BB-308–310 |

**Specificity (CM-015):** 2015 · Ralph and Pierce Brehany, father and son · SC License #57706 and Town of Bluffton License #0620033323 · CertainTeed + GAF factory-certified, ShingleMaster · BBB A+ since March 2021.

**Schema readiness (ABT-15):** `Person` for the owners + `Organization` tied to the ID page `@id` — Finish only.

---

## 3 · Customer language (BG-I — words only, no names, CM-027)

- "local family biz" · "father and son" · "the owner" · "honest" · "explained every detail" · "kept us updated".
- **Never echo:** the 10-year warranty wording (rows 11, 36, 44, 48, 49); "absolute BEST"; reviewer names.

## 4 · Audit findings and failed spec checks

| Finding | Check | What this page does |
|---|---|---|
| F-015 rev 3 | ABT-01, ABT-04 | Title and H1 per Paul's ruling (DEC-LOCAL-015) |
| F-016 rev 3 | ABT-07 | Owners named; visible photo/title placeholders |
| F-001 | — | "homes and businesses" removed; residential only |
| F-003 | ABT-09 | Brand written "Apex Roofing of the Lowcountry" (lower-case "the") everywhere |
| F-025 | ABT-11 | Decorative H4/H5 headers removed; H2 → H3 order only |
| F-027 | ABT-02 | Title separator ` - ` (live uses ` | `) |
| F-033 | — | About images get alt text (Jonie / Finish) |
| F-017 | ABT-06 | Opening answers who/what/where first |
| F-007 | ABT-15 | Schema in Finish only |

## 5 · Must not appear

Job titles ("President", "Owner" as a title line, "CEO") · any staff name other than Ralph and Pierce · team size, trucks, jobs completed, "in-house team", "seasoned professionals" · awards or rankings · a licence class, holder or expiry · "bonded" · BBB "accredited" · an invented founding story, an exact founding date · "homes and businesses" / commercial · Georgia · prices · response times · the review warranty lengths · reviewer names · superlatives · per-city H tags · cross-page links in prose.

## 6 · Sibling context

- Homepage (same batch, briefed this run): owns the brand FAQ (free estimates, licensed and insured, travel beyond the 12 towns, commercial work, since 2015) and the short trust cards. The About page goes deeper on the people and credentials; it does not repeat the homepage's FAQ answers or its card wording.
- Approved pages already use: "the father and son who founded Apex in 2015, are the ones on the roof" (a location page) and "working from Bluffton since 2015" — word the About page's owner and history lines differently.
- St. Helena Island owns the FAQ "Who actually works on a St. Helena Island roof?" — the About owners section is prose, not that question.

---

## Evidence gaps

Gate **WARN** (run 20261013-140538-build-1832): 1 required and 3 supporting gaps.

| Fact (grid) | Need | Mark | What the writer does |
|---|---|---|---|
| How and why the company started (owner's own account) | required | Unknown (open client question `fact:about:company_story`, asked 2026-10-11; one review mentions a family business only — checked by meaning, no origin story) | History H2 is written with the founding year, father-and-son ownership and the company's view (BG-G), and carries `[NEED: Ralph's or Pierce's own account of how and why they started Apex in 2015]` where the story goes. Nothing invented. |
| Licence numbers and classes | supporting | Unverified (grid) | Numbers only, as Paul approved them; never a class or holder. |
| Awards and rankings | supporting | Unknown | Left out. |
| Team size / trucks / jobs completed | supporting | Unknown | Left out (team H2 merged into the owners section). |

## Change log

| Date | Run | Change |
|---|---|---|
| 2026-10-13 | 20261013-140538-build-1832 | Brief written after the gate cleared (BLOCK → WARN once the settled named-staff answer was synced into facts.json). |
