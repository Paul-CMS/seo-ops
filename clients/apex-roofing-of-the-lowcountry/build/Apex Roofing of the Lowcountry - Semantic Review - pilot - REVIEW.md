# Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW

**Batch:** pilot · **Run:** 20261009-130919-build-89b2 (re-issue of run 20261009-124809-build-ab2d) · **Date:** 2026-10-09 · **Report only — the drafts are not changed.**

This re-issue consolidates the earlier 11 rows into **8 SEM items (SEM-1 to SEM-8)**, the set the approval accepts, and builds in Paul's answers of 2026-10-09 (logged in run 20261009-130919-build-89b2). The findings themselves are unchanged.

Pages reviewed side by side (each written in its own run, CM-043):
- `svc-roof-repair` — `clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md`
- `loc-bluffton` — `clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md`

Earlier approved pages: none (pilot is the first batch; Brand Guide C1–C3 are still empty).

## 1. Sibling check (CM-017 as scoped by CM-043)

| Check | Result |
|---|---|
| FAQ question on both pages (BB-316) | None. SD has 6 service questions, LD has 4 Bluffton questions; no overlap. |
| H2/H3 heading on both pages | None. |
| Opening angle reuse | Buyer states differ (SD: slow leak, not yet an emergency; LD: Bluffton-based roofer, incl. owners living out of town). The **sentence pattern** is shared — SEM-2. |
| Passage portable between the two pages (E1 across siblings) | One near-identical on-call sentence on both pages — SEM-2. One region-level climate sentence on LD that overlaps SD's weather paragraph — SEM-6. |
| Collisions with future siblings in the site plan | LD sibling-cities H2 has no city and would repeat on all 12 location pages — SEM-7. Hail/storm intent on SD belongs to Emergency Roof Repair — SEM-5. |

## 2. Semantic review table (pick by SEM number)

The **SEM #** is the item number Paul picks (`--sem`). The **Check** column is the check that caught it: SEM-1 to SEM-7 still have no definition in `methodology/writing-commercial.md` (Stage 4 `[NEED: definition from the live gem, Section G]`), so findings are tagged SEM-8 where it applies and otherwise with the standard check (E1, C7, A6, A7, BB-310, BB-316).

| SEM # | Old rows | Check | Page · element | What was found | Action (Paul's answers built in) | Blocked? |
|---|---|---|---|---|---|---|
| **SEM-1** | 1 | SEM-8 | svc-roof-repair · FAQ "What should I do if I have an emergency roof leak?" | Active-leak / storm question on the scheduled-repair page; its intent belongs to Emergency Roof Repair. | **Keep the FAQ on Roof Repair (Paul) — not routed.** Point the reader to the Emergency Roof Repair page (`/emergency-roof-repair/`) in the answer. Under CM-022/CM-005 Build does not place the link: the answer carries a link placeholder, and the link is proposed in Finish as this page's one CM-022 contextual-link exception for Paul's approval. SD keeps its FAQ count (subject to SEM-3). | Not blocked for the copy; the live link waits on Finish (open question `pilot_emergency_faq_link_cm022`). |
| **SEM-2** | 2, 8 | C7 / E1 (sibling); opening-angle reuse (CM-043 §3) | Both pages · opening paragraph first and last sentence; SD emergency FAQ last sentence; LD FAQ "Is Apex Roofing of the Lowcountry based in Bluffton?" last sentence | "Ralph and Pierce are on call and treat an emergency as high priority" appears on both pages almost word for word; both openings use "Apex Roofing of the Lowcountry is a roof[ing contractor / er] that / based…" and both close "Call (843) 757-2739 for a free estimate." | Because SEM-1 keeps the SD FAQ, the on-call sentence stays on **one** page only: keep it on SD (the emergency FAQ), and on LD replace it with a Bluffton-specific next step (or end after the answer). Vary the entity sentence and the CTA sentence so the two pages use different forms; record the used forms in C3 at write-back so later pages avoid them. | No |
| **SEM-3** | 6, 7 | E1 (within page) / A6 | svc-roof-repair · FAQ "Why do so many roof leaks start at the flashing?"; H3 "Roof Leak Repair", first sentence | Flashing is explained three times (delivery section, Flashing H3, this FAQ). The Roof Leak Repair lead sentence ("A roofing contractor fixes a leaking roof, and the work starts with finding the true entry point.") reads as an inserted query and repeats delivery steps 2–3. | **Drop the flashing FAQ** (5 FAQs remain, within spec 4–6). **Replace the generic lead sentence** under "Roof Leak Repair" with what is specific to this case (a leak in one or two areas traced to the failed flashing, shingle or seam). | No for the edits. The H3 keeps its existing `[NEED: client confirms this repair type]`, which still blocks ship. |
| **SEM-4** | 9 | SEM-8 | svc-roof-repair · H2 "How Do Our Roofers Fix a Damaged Roof in Beaufort and Jasper Counties?", 2nd sentence | "Apex was founded by Ralph Brehany and his son, Pierce." — founder line on a service page, followed by the W25 [NEED]. | **Keep (Paul).** W25 answered by Paul 2026-10-09: father and son, Ralph and Pierce, both get on the roof. Reword the line to that fact (who gets on the roof) and **remove the W25 [NEED] only**; every other [NEED] stays. | No (W25 settled: `w25_who_goes_on_the_roof`). |
| **SEM-5** | 10 | SEM-8 | svc-roof-repair · H3 "Hail Damage Repair" (and "hail damage" in the H2 lead list) | Storm/hail damage overlaps the Emergency Roof Repair page's intent; hail repair is unconfirmed. | **Move to Emergency Roof Repair (Paul).** Remove the H3 and the "hail damage" mention from the Roof Repair lead list; route hail/storm damage to the Emergency Roof Repair brief (later batch), where it still needs the client's confirmation of hail repair before it ships. Roof Repair keeps 5 repair-type H3s. | No on Roof Repair. Routed → svc-emergency-roof-repair (its own NEED travels with it). |
| **SEM-6** | 3, 5 | E1 / C7; E1 (portability, LOC-13, BB-317) | loc-bluffton · FAQ "Is Apex Roofing of the Lowcountry based in Bluffton?"; H2 "What Makes Roofing in Bluffton Different?", 3rd sentence | The FAQ answer repeats the opening (based in Bluffton, licence #0620033323 a second time, 6 Sutton Ct). The climate sentence (humid subtropical, hurricanes, wind-driven rain) is true of every town and repeats SD's weather paragraph. | FAQ: keep the question; answer with the address and what a Bluffton base means for the job (no travel fee — settled in Business), without repeating the licence number. Climate sentence: **localize to Bluffton (Paul)** — tie the storm exposure to the sourced Bluffton-only facts already in the brief (May River through the town centre, New River on the southwest edge, about 20 ft elevation; Wikipedia, LB row 7). No new fact is added. | No |
| **SEM-7** | 4 | A7 / BB-316 (heading registry) | loc-bluffton · H2 "Which Other Lowcountry Towns Do We Serve?" | No city in the heading, so it would be word for word the same on all 12 location pages. | Put the city in it, e.g. "Which Towns Near Bluffton Do We Also Serve?", and use that pattern for the location batches. | No |
| **SEM-8** | 11 | BB-310 | loc-bluffton · H2 "Which Roof Services Can You Get From a Bluffton Roofing Contractor?", lead sentence | "…eight roofing services, each with its own page." describes the website, not the service. | Drop "each with its own page": "Apex offers Bluffton homeowners eight roofing services:" (the H3s and link table stay as they are). | No |

**Old row → new item:** 1 → SEM-1 · 2 → SEM-2 · 3 → SEM-6 · 4 → SEM-7 · 5 → SEM-6 · 6 → SEM-3 · 7 → SEM-3 · 8 → SEM-2 · 9 → SEM-4 · 10 → SEM-5 · 11 → SEM-8.

Checks with no findings: FAQ collision between the two pages; H2/H3 collision between the two pages; buyer-state reuse in the openings; reserved B1 variant use (none on either page). SEM-1 to SEM-7 as checks: not run (no definition).

## 3. Outside the SEM items

- **Bluffton depth (Paul, 2026-10-09):** Paul accepts that the Bluffton draft is too long and wants it cut down. This is not a SEM item and no copy is changed in this report-only run; it is a revision of the Bluffton draft, made when the draft is next changed.

## 4. Open [NEED] items still in the drafts (not SEM items — they block ship until answered)

**svc-roof-repair (11 after SEM-4/SEM-5):** W10 photo documentation · W11 corrosion-resistant flashing and synthetic underlayment · warranty on a repair · client confirms each of the 5 remaining repair types (shingle, flashing, ridge cap/starter strip, soffit/fascia/deck, leak) · SC source for the 25% rule (or keep the answer general) · typical repair visit length (drop that FAQ if unanswered). W25 is answered (SEM-4); hail moves with SEM-5.

**loc-bluffton (5):** Apex pulls the Town of Bluffton re-roof permit · UDO §3.18 Certificate of Appropriateness for an Old Town re-roof · UDO Article 5 roof-material list · W9 work in Palmetto Bluff, Belfair, Colleton River Plantation, Moss Creek · a 6th Bluffton neighborhood with a public source (spec needs 6–12).
