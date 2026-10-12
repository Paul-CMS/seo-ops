# LB - Levy - Apex Roofing of the Lowcountry

Location brief · page `loc-levy` · batch **locations** · Route A
Run 20261012-150859-build-1044 · 2026-10-12 · Build agent (brief-writer) · one page per run (CM-043)
Spec: `methodology/specs/location.md` (APPROVED 2026-10-08) · Site plan: APPROVED 2026-10-11
Evidence gate: **WARN** (known 6 · unknown 3 · unverified 1) — one required gap (neighborhoods); supporting gaps (Things to Do, Top Sites, response time). A second public search on 2026-10-12 found none of the three: honest count is **0 each**. That search settled the county: Levy is an unincorporated community in southern **Jasper County** (Wikipedia, read 2026-10-12) — the site plan's "Jasper (to verify)" is resolved.

**This is a very thin page.** Read the section "Checks that fail" before drafting.

---

## 1 · Page assignment (from the approved site plan)

| Item | Value | Source |
|---|---|---|
| Page type | Location page — one city, lean, conversion-focused | site plan §3 |
| Final URL | https://apexroofingtlc.com/levy/ (URL unchanged — Build never changes a URL) | site-plan.json |
| Main keyword | roofing contractor levy sc | site-plan.json |
| SEO title | `Apex Roofing of the Lowcountry - Roofing Contractor - Levy, South Carolina` | spec #2 |
| Meta description (proposed, 151 chars) | `Levy, SC roofers for roof repair, replacement, metal roofing and inspections in Jasper County. Call Apex Roofing of the Lowcountry for a free estimate.` | spec #3 (150–160, city, two or more services, soft CTA) |
| H1 | **Roofers in Levy** | site plan §3 |
| "The Best" (CM-020) | **No.** Demand fails (no city-level "best" query with volume); not in the top 100 for the keyword; BG-H2 row /levy/: No | BG-H2; site-plan `the_best: false` |
| GBP landing page? | No — city map, not the GBP map; no LocalBusiness schema | BG-A11, LOC-26 |
| Claims in keyword/variants (CM-049) | None | site-plan `claims: []` |
| Link targets | H3 services table → 8 service pages; sibling table → the 11 other location pages. **Placeholders only** (CM-005) | site plan §3 |

### Variant chain (LOC-09, CM-024)

| Element | Category term | City term |
|---|---|---|
| URL `/levy/` | — | levy |
| Title | Roofing Contractor | Levy, South Carolina |
| H1 | **Roofers** | Levy |
| First H2 (services table) | **Roofer** (assigned) — never "Roofers" | Levy |
| Opening paragraph | roofer / roofing contractor (third set — do not echo the H1 wording back-to-back) | Levy, SC · Jasper County |
| FAQ H2 | **Residential Roofer** (assigned; written into A3, settled `residential_roofer_a3_write`) | Levy |

Suggested headings (writer may re-word inside the rules; each names its entity; no decorative headers — F-025). None of these exists in the C3 registry:
- Services H2: *What Can a Roofer Do for Your Levy Home?*
- Local context H2: *What Should a Levy Homeowner Know About Where Levy Sits?*
- FAQ H2: *What Do Levy Homeowners Ask a Residential Roofer?*
- Neighborhoods H2: *Which Levy Neighborhoods Do We Serve?*
- Things to Do H2: *What Are Some Things to Do in Levy?*
- Top Sites H2: *What Are the Top Sites to See in Levy?*
- Sibling cities H2: *Which Towns Near Levy Do We Also Serve?* (Build batch check: the generic "Which Other Lowcountry Towns Do We Serve?" was proposed on three pages — each page's H2 now names its own town, BB-316)

---

## 2 · Element order (spec §3, CM-023) and what each element carries

| # | Element | Requirement for this page | Facts to use (status) |
|---|---|---|---|
| 1 | URL | `/levy/` unchanged | — |
| 2 | SEO title | as above | BG-A1, A2 |
| 3 | Meta | as above | — |
| 4 | H1 | `Roofers in Levy` — exactly one H1 | — |
| 5 | Opening paragraph (no H tag, 60–120 words) | **First sentence answers** who, what, where: Apex Roofing of the Lowcountry is a residential roofer that serves Levy, a small community in southern Jasper County, from its base in Bluffton. Phone **(843) 757-2739** and **free estimates** in the paragraph. **Angle — Levy only:** a small **unincorporated community in southern Jasper County**, about **13 ft** above sea level, reached by **SC Highway 315**, once served by the now-abandoned Seaboard Air Line rail line. Use the county, SC 315 and the community's small size here; **keep the elevation and rail history for the local-context section** so the two sections do not repeat each other. "No travel fee" is settled (`business`) and may be said once. **Do not state a distance or drive time from Bluffton** (not sourced), no response time. Do not say or imply Georgia or Savannah. Do not call Levy a "town" or "city" (it is unincorporated) | Levy served: Paul Approved (BG-E, 2026-10-06) · county, SC 315, 13 ft, rail line: Internally Verified, Wikipedia (read 2026-10-11 and 2026-10-12) · based in Bluffton, no travel fee: settled `business` · residential only: settled · phone, free estimates: Paul Approved |
| 6 | H2 services table | H3 per service, **all 8**, no descriptions (LOC-12): Roof Repair · Roof Replacement · Roof Installation · Roof Inspections · Emergency Roof Repair · Metal Roofing · Slate Roofing · Skylights. Rows: `| [Link wheel: populate service links here] |`. One short lead-in sentence at most | BG-D services (Paul Approved) |
| 7 | H2 local context (3–5 sentences, no links) | **Only these sourced facts** (Wikipedia, https://en.wikipedia.org/wiki/Levy,_South_Carolina): unincorporated community in southern Jasper County; elevation 13 ft; reached by SC Highway 315; formerly served by the Seaboard Air Line Charleston Subdivision, now abandoned. The source gives **no population, climate, terrain or housing data** — write none. Tie to roofing in general terms only; **no hurricane, flood, soil or housing-age claim for Levy** (not sourced for this community — Bluffton's hurricane sentence does not transfer). If the facts fill only 3 short sentences, that is correct; never pad with invented conditions (spec §7) | Internally Verified (read 2026-10-11 and 2026-10-12) |
| 8 | FAQ (H2 + H3, 3–4, first sentence answers in 40–60 words) | See §3 — **1 usable, 2 gaps** | — |
| 9 | H2 neighborhoods (6–12) | **0 sourced.** Plain list under the H2, not H-tagged. Write `[NEED: 6–12 Levy neighborhoods with a public source]` and no names. See §4 | Unknown (grid) |
| 10 | City map | `[Map: embed a city-level map of Levy, SC here — not the Google Business Profile map]`, no H tag | spec #10 |
| 11 | H2 Things to Do | **0 sourced.** `[NEED: a real, verifiable Levy thing to do with a public source]`. Savannah National Wildlife Refuge is sourced to the Hardeeville area, **not Levy — do not list it** (also a Georgia-border proximity risk) | Unknown (grid) |
| 12 | H2 Top Sites | **0 sourced.** `[NEED: a real, verifiable Levy site with a public source]`. Wikipedia lists no Levy landmark; none of the 10 Jasper County NRHP entries is in Levy. The rail line is a history fact and sits in local context, not here (no item in both) | Unknown (grid) |
| 13 | H2 sibling cities | All 11 other towns as rows: `| [Link wheel: populate sibling-city links here] |` — Bluffton, Hilton Head Island, Okatie, Pritchardville, Beaufort, Port Royal, Lady's Island, St. Helena Island, Fripp Island, Hardeeville, Ridgeland | BG-E |
| 14 | CTA with NAP (no H tag) | **Apex Roofing of the Lowcountry · 6 Sutton Ct, Bluffton, SC 29910 · (843) 757-2739** · free estimates · Monday–Saturday 8 AM–5 PM. No response-time promise | BG-A1, A4, A8; BG-D hours |
| — | Word ceiling | Under 1,000 words; this page will be far under | LOC-22 |
| — | Outbound authority link (CM-011) | None in the draft. Finish candidate: Wikipedia is not an authority link; none proposed. Reason: no official Levy page exists | spec §6 |
| — | Schema readiness (LOC-26) | `WebPage` + `ItemList` of the 8 service `@id`s; no LocalBusiness, no NAP in schema. Recommendation only | BB-604, BB-605 |

**Specificity (CM-015, LOC-24 — need 3 city-specific verifiable facts).** Usable now, all Wikipedia (Internally Verified):
1. Unincorporated community in southern Jasper County.
2. Reached by SC Highway 315.
3. Elevation about 13 ft.
4. Formerly served by the now-abandoned Seaboard Air Line Charleston Subdivision.

Four facts: LOC-24 **passes by count** and each fails the portability test against Ridgeland and Hardeeville. It passes only narrowly: all four come from one short Wikipedia page, and none is a roofing fact. The writer must not stretch them into roofing claims.

### Checks that fail (state these to Paul at the brief gate)

| Check | Status | Why |
|---|---|---|
| LOC-14 (3–4 unique city FAQs) | **Fails** | 1 of 3 minimum is answerable. The site plan carries 0 sourced FAQs (3 gaps) |
| LOC-15 (6–12 neighborhoods) | **Fails** | 0 sourced, 3 on-disk sources and the 2026-10-12 web search found none |
| LOC-17 (Things to Do and Top Sites, every item real) | **Fails** | 0 sourced items for each; the sections are `[NEED]` shells |
| LOC-24 (3 city-specific facts) | Passes narrowly | 4 facts: county, SC 315, 13 ft, former rail line |
| LOC-13 (local context 3–5 sentences) | Passes at 3 sentences | Only if the writer stays inside the four facts |
| All others (LOC-01–12, 16, 18–23, 25–27) | Pass if the draft follows this brief | — |

---

## 3 · FAQ (site plan §3a — each with its reason; C3 has no Levy entry)

FAQ H2 uses "Residential Roofer". 0 sourced FAQ topics in the site plan (3 gaps). Public research 2026-10-12 offered three candidates; only the first is Levy-specific.

| # | Question (H3) | Why it belongs on this page | Answer source / status |
|---|---|---|---|
| 1 | **Is Levy a town, and who covers a Levy address?** (may be shortened to "Is Levy its own town?") | Levy is unincorporated: no town government. True of this community only; Ridgeland and Hardeeville are incorporated | **Usable now, jurisdiction only.** First sentence (40–60 words): Levy is an unincorporated community in southern Jasper County with no town government of its own, so county rules apply to a Levy address (public research 2026-10-12 — not yet on the grid; Wikipedia read 2026-10-12). **Do not add** permit rules, fees, forms, offices or phone numbers — the Jasper County permit answer belongs to Ridgeland's FAQ (settled `site_plan_open_choices` 2a: one permit FAQ per county). **Do not state** that a particular Levy parcel is or is not inside Hardeeville limits: the researcher found annexation only in search summaries (unread council agendas). Safe closing line: ask Jasper County which jurisdiction a specific parcel is in. No Apex claim about pulling permits here. Source for the writer to cite: https://en.wikipedia.org/wiki/Levy,_South_Carolina |
| 2 | How do I check whether my Levy home is in a flood zone? | Levy sits at 13 ft elevation. **Weak on portability** (the lookup is county-wide) | **GAP — do not hand to the writer.** Source is a search summary of the Jasper County forms-and-links page (https://www.jaspercountysc.gov/services/planning-and-building/forms-links/), never opened; no source says whether a re-roof triggers flood rules. Usable only if a researcher opens the official page and Paul accepts the portability weakness |
| 3 | Do Levy homeowners qualify for SC Safe Home roof grants? | Levy is in Jasper County. **Fails portability** (statewide programme, not Levy) | **GAP — do not use.** Official SC Safe Home / SC Department of Insurance page not read; eligibility and amounts known only from news search summaries; may be out of date. A grant claim is also a financial claim (CM-025) |

Not offered, and why: "Do you serve Levy / is there a travel fee in Levy?" The facts are settled (served, no travel fee), but the question is brand-level and would share its answer with Ridgeland's ("farther from Bluffton") and Hardeeville's likely FAQ; one answer per question site-wide (BB-316). It is the only other candidate that would be safe, so it is listed as option (d) in Flag F1, not placed in the brief.

**Count:** 1 usable, 0 conditional, 2 gaps. The spec needs 3 (LOC-14 fails). Routed elsewhere (not answered here): roof tax, deductible, cost and 25%-rule questions routed to blog or service pages in `paa-routing.md`; no Levy-specific PAA or fan-out row exists (Levy: 0 rows in the fan-out routing).

---

## 4 · Neighborhoods (spec #9, LOC-15: 6–12, all real and verifiable; F-024)

| Neighborhood | Status | Source |
|---|---|---|
| — | **0 verified** | Wikipedia Levy names none; Wikipedia Ridgeland and jaspersc.org Discover pages have no Levy content; web search returned only Wikipedia, county history pages and legislature bills (2026-10-12) |

The writer lists nothing and writes `[NEED: 6–12 Levy neighborhoods with a public source]` under the H2.

**Not usable:** the live page's "SC-462 corridor" and "Shell Point Road area" (F-024: roads and areas, not neighborhoods; Shell Point is also a Beaufort-side name). No name that appears on another location page. Other communities that Wikipedia lists as Jasper County unincorporated places are not Levy neighborhoods and must not be listed as if they were.

---

## 5 · Customer language (Brand Guide I — words only, never facts, no names; CM-027)

- Ways customers describe the company: "local roofer", "Local Family Biz", "honest", "responsive" (about 30 reviews on communication, roughly 6 on the local family business).
- Work words: "new roof", "replace my roof", "estimate", "quote", "bid".
- Levy: no review names Levy. No Levy situation or buyer quote exists — the writer may not invent one.
- **Never echo:** "10 year workmanship warranty", "tarps during rain", "handles permits", "County inspection" (review-only claims, not in Section D); the one review that says Apex "responded quickly" (a 2022-07-17 single reviewer, response-time claim — Unverified, and a single reviewer cannot support "customers mention" under CM-057); the Google rating as a fact.

---

## 6 · Audit findings and failed spec checks for this page

| Finding | Check | What this page does about it |
|---|---|---|
| F-011 rev 2 | LOC-07 | H1 "Roofers in Levy" has no "The Best" — matches BG-H2 |
| F-012 rev 2 | LOC-06, LOC-09 | H1 differs from the title's "Roofing Contractor"; first H2 uses "Roofer", not "Roofers"; FAQ H2 "Residential Roofer" |
| F-017 | LOC-10 | Opening: first sentence answers; phone and free estimate in it; Levy-only angle |
| F-019 | LOC-17, LOC-20 | Things to Do and Top Sites sections are present in CM-023 order but empty (`[NEED]`) — **LOC-17 still fails** |
| F-020 | LOC-19 | CTA carries NAP |
| F-021 | LOC-14 | Old city-swapped FAQs dropped; 1 Levy-only FAQ replaces them — **LOC-14 still fails (1 of 3)** |
| F-024 | LOC-15 | Old "SC-462 corridor / Shell Point Road area" removed; no names → **LOC-15 still fails (0 of 6)** |
| F-025 | LOC-23 | Neighborhoods as list items, not H-tags |
| F-002 | LOC-25 | No price; ShingleMaster not carried over |
| F-029 | meta | New meta, 151 chars |
| W22 (Brand Guide D2 row R5) | CM-016 | The old Levy page said "rural Beaufort County" and "payment arrangements": **wrong county** (Levy is Jasper) and an unconfirmed claim. Do not carry over either; financing is through Hearth, but nothing in this brief calls for a financing line |

## 7 · Must not appear (BG-D2, settled `not_on_the_site_until_confirmed`, CM-016, CM-049)

ShingleMaster · commercial / "homes and businesses" · **Georgia / "Coastal Georgia" / Savannah**, and any geography sentence that could read as Georgia service (settled `business`: not Georgia) · "Beaufort County" for Levy (it is Jasper) · "rural" (not sourced) · "payment arrangements" · any response time, "same-day", "24 hour", "fast" as a promise · "bonded" · a licence class · any price · Google rating · a warranty term · "best"/superlatives · service descriptions · any cross-page link in prose, FAQ answers or local context (CM-005) — use `[LINK → /slug/ · reason]` only (none proposed on this page) · reviewer names · "town" or "city" for Levy · hurricane, flood, soil or housing-age claims for Levy · Savannah National Wildlife Refuge as a Levy site · a distance or drive time from Bluffton.

## 8 · Sibling context

- **Briefs written earlier in this batch:** none were in the folder when this brief was written (only the research folder). The writer's check against sibling briefs is therefore against the approved Bluffton draft and the services' C3 entries only.
- Opening angle unique to Levy (unincorporated, SC 315, 13 ft, former rail line). Bluffton's angle is home base and the Town licence; Hardeeville and Ridgeland angles must not use unincorporated status.
- **Close siblings: Hardeeville, Ridgeland.** Ridgeland owns the Jasper County permit FAQ; Levy's FAQ 1 stays on jurisdiction only and must not answer a permit question. Do not put an annexation or Hardeeville-limits claim on this page: it belongs, if sourced, on Hardeeville.
- Bluffton draft headings and FAQs are not reused. Levy's local context cannot reuse Bluffton's hurricane, river or historic-district sentences (different facts; none sourced for Levy).

---

## Evidence gaps

| Fact (grid) | Need | Grid mark | Real status (incl. 2026-10-12 research) | What the writer does |
|---|---|---|---|---|
| Phone | required | Known | Paul Approved | Use (843) 757-2739 |
| City actually served | required | Known | Paul Approved (BG-E, 2026-10-06) | State it |
| City-specific conditions | required | Known | Internally Verified, Wikipedia; county confirmed Jasper 2026-10-12 | §2 #5 and #7 only |
| 6–12 real neighborhoods | **required** | **Unknown** | **0 sourced** (2026-10-12 search found none) | `[NEED: 6–12 Levy neighborhoods with a public source]` |
| Free estimate / offer | required | Known | Paul Approved ("free estimates"); W17 detail Submitted | Say "free estimates" only |
| Things to Do | supporting | Unknown | **0 sourced** | `[NEED: …]`; do not list Savannah National Wildlife Refuge |
| Top Sites | supporting | Unknown | **0 sourced**; no NRHP entry in Levy | `[NEED: …]` |
| Response time / guarantees | supporting | Unverified | One review, 2022-07-17 ("responded quickly") — one reviewer, keyword match only, not a fact (CM-027, CM-057) | **State none.** Not even "customers mention" (needs 3+ reviewers) |
| Emergency / after-hours | supporting | Known | Client's words: "always on call … treat an emergency as high priority" | Optional, client's words only; no hours, no time |
| Google rating | supporting | Known | Evidence for CM-020 only | Leave off the page |

Public research 2026-10-12 — not yet on the grid: county = Jasper (Wikipedia, read); no town government (Wikipedia); FAQ 1 jurisdiction answer (Wikipedia). The three FAQ candidates' source pages on jaspercountysc.gov, hardeevillesc.gov and SC Safe Home were **not opened** by the researcher and are not usable.

**Open items for this page.** Public facts are researched, never asked (CM-016/042); only the client holds local knowledge.
1. Neighborhoods, Things to Do, Top Sites: no public source found. The only path is local knowledge from the client or Paul (communities, places), which a researcher then verifies against a public source. Client question (one, with its searched line): "Which communities or subdivisions in Levy do you have roofs in?" (searched: Wikipedia, county, chamber, web search 2026-10-12; none found). W9 lists no Levy project, so any named place is `[NEED: client confirms Apex works there]` until the client answers.
2. FAQ 2 and 3: a researcher opens the official pages (Jasper County forms-links; SC Department of Insurance SC Safe Home) before either is usable. Even if opened, both fail portability.
3. Whether any Levy parcel lies inside Hardeeville limits: Jasper County GIS or Hardeeville planning (public, researcher task). Needed only if Paul wants the annexation point on the Hardeeville page.

## Flags for Paul

1. **Levy cannot pass LOC-14, LOC-15 or LOC-17 on public sources.** 1 of 3 FAQs, 0 of 6 neighborhoods, 0 Things to Do, 0 Top Sites. LOC-24 passes only narrowly (4 Wikipedia facts, none about roofing). Options:
   - (a) The client or Paul supplies local knowledge (communities, places); a researcher verifies each against a public source; the sections are filled and the page passes.
   - (b) Paul accepts a short page with the neighborhoods, Things to Do, Top Sites and two FAQs marked `[NEED]` and **held from publication** until filled (the draft ships structurally complete; LOC-14, 15, 17 stay open).
   - (c) Paul reconsiders whether Levy keeps its own page. This is a URL decision and Paul's alone; Build never changes a URL, and nothing in this brief or the draft does. Note: the keyword is not in the top 100 (BG-H2) and the old page named the wrong county ("Beaufort County").
   - (d) Add the brand-level "Do you serve Levy / no travel fee?" question as FAQ 2 to reach 2 of 3 — still below the minimum, and its answer collides with Ridgeland and Hardeeville; only if Paul wants the count nearer 3.
2. **The county is Jasper, not "Jasper (to verify)".** Settled by Wikipedia 2026-10-12. The site-plan group label can be corrected at the next site-plan revision (Paul's call; this brief does not change the site plan). The old live page's "rural Beaufort County" was wrong.
3. **FAQ 1 is jurisdiction only.** The Jasper County permit answer stays on Ridgeland (settled 2a). If Paul wants a permit line on Levy, it needs the official Jasper County Planning and Building page read and a decision on how it differs from Ridgeland's FAQ.
4. **No response time and no "responded quickly".** One 2022 review is the only support; it is a single reviewer. Section D has no response time (CM-016).
5. **Brand Guide F (NAP) is still empty (BG-F).** The brief uses A1 + A4 + A8; fill BG-F before Finish.
