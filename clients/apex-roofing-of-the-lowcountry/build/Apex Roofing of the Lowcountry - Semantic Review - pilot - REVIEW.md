# Apex Roofing of the Lowcountry - Semantic Review - pilot - REVIEW

**Batch:** pilot · **Run:** 20261009-124809-build-ab2d · **Date:** 2026-10-09 · **Report only — the drafts are not changed.**

Pages reviewed side by side (each written in its own run, CM-043):
- `svc-roof-repair` — `clients/apex-roofing-of-the-lowcountry/build/pilot/SD - Roof Repair - Apex Roofing of the Lowcountry.md`
- `loc-bluffton` — `clients/apex-roofing-of-the-lowcountry/build/pilot/LD - Bluffton - Apex Roofing of the Lowcountry.md`

Earlier approved pages: none (pilot is the first batch; Brand Guide C1–C3 are still empty).

## 1. Sibling check (CM-017 as scoped by CM-043)

| Check | Result |
|---|---|
| FAQ question on both pages (BB-316) | None. SD has 6 service questions, LD has 4 Bluffton questions; no overlap. |
| H2/H3 heading on both pages | None. |
| Opening angle reuse | Buyer states differ (SD: slow leak, not yet an emergency; LD: Bluffton-based roofer, incl. owners living out of town). The **sentence pattern** is shared — see row 8. |
| Passage portable between the two pages (E1 across siblings) | One near-identical sentence on both pages (on-call / emergency priority) — rows 1–2. One region-level climate passage on LD that overlaps SD's weather paragraph — row 5. |
| Collisions with future siblings in the site plan | LD sibling-cities H2 has no city and will repeat on all 12 location pages — row 4. SD carries emergency and storm intent owned by the Emergency Roof Repair page — rows 1, 10. Founder line belongs to About — row 9. |

## 2. Semantic review table (pick by #)

SEM-1 to SEM-7 have no definition yet in `methodology/writing-commercial.md` (Stage 4 marks them `[NEED: definition from the live gem, Section G]`). Findings are therefore tagged with SEM-8 where it applies, and otherwise with the standard check that caught them (E1, C7, A7, BB-310).

| # | Check | Where (page · element / exact heading) | What I found | Why it matters | Suggested change | Action | Blocked by |
|---|---|---|---|---|---|---|---|
| 1 | SEM-8 | svc-roof-repair · FAQ "What should I do if I have an emergency roof leak?" | An active-leak / storm question on the scheduled-repair page; the opening even says "It is not an emergency yet". | The intent belongs to the Emergency Roof Repair page (`/emergency-roof-repair/`); keeping it here splits that page's intent. | Remove from SD and route the question to the Emergency Roof Repair brief. SD keeps 5 FAQs (spec 4–6). | ROUTED → svc-emergency-roof-repair | — |
| 2 | C7 / E1 (sibling) | svc-roof-repair · FAQ emergency answer, last sentence; loc-bluffton · FAQ "Is Apex Roofing of the Lowcountry based in Bluffton?", last sentence | "Ralph and Pierce are on call and treat an emergency as high priority" appears on both pages almost word for word. | C7: the company/next-step sentence is never the same on two pages; it will also repeat on every later page that mentions after-hours service. | LD: replace with a Bluffton-specific next step (or end after the answer sentence). SD: resolved if #1 is applied. | PROPOSED | — |
| 3 | E1 / C7 | loc-bluffton · FAQ "Is Apex Roofing of the Lowcountry based in Bluffton?" | The answer repeats the opening paragraph (based in Bluffton; Town licence #0620033323 a second time) and the CTA (6 Sutton Ct). | The FAQ adds no new fact for the reader; the licence number appears twice on one page. | Keep the question; answer with the address and what a Bluffton base means for the job (e.g. no travel fee, confirmed in D), without repeating the licence number. | PROPOSED | — |
| 4 | A7 / BB-316 (heading registry) | loc-bluffton · H2 "Which Other Lowcountry Towns Do We Serve?" | The heading has no city, so it will be word for word the same on all 12 location pages. | C3 registry: no heading reused across pages; a templated H2 also weakens the page's city entity. | Put the city in it, e.g. "Which Towns Near Bluffton Do We Also Serve?", and set that pattern for the location batches. | PROPOSED | — |
| 5 | E1 (portability) | loc-bluffton · H2 "What Makes Roofing in Bluffton Different?", 3rd sentence (humid subtropical climate, hurricanes, wind-driven rain) | True of every town in the service area; would paste onto Hilton Head Island or Okatie unchanged, and repeats the theme of SD's "Lowcountry weather is hard on roofs" paragraph. | Local context must be genuinely this city and appear on no other page (LOC-13, BB-317). | Cut the sentence (section stays at 4 sentences, within 3–5), or tie it to a sourced Bluffton-only fact (e.g. May River / New River exposure). | PROPOSED | — |
| 6 | E1 (within page) | svc-roof-repair · FAQ "Why do so many roof leaks start at the flashing?" | Flashing is explained three times: delivery section ("Flashing comes first…"), H3 "Flashing Repair at Chimneys, Walls and Valleys", and this FAQ. | The FAQ slot repeats the body instead of answering a new question. | Drop the FAQ (5 remain; 4 if #1 is also applied — still within 4–6), or replace it with an unused routed PAA question for this page. | PROPOSED | — |
| 7 | E1 / A6 | svc-roof-repair · H3 "Roof Leak Repair", first sentence | "A roofing contractor fixes a leaking roof, and the work starts with finding the true entry point." reads as an inserted query, and the leak-tracing point repeats delivery steps 2–3. | A sentence that reads the same on any roofer's site fails E1; repeated content dilutes the section. | Open with what is specific to this case (a leak in one or two areas traced to the failed flashing, shingle or seam) and drop the generic lead sentence. | PROPOSED | client confirmation of the repair type (NEED on the H3) |
| 8 | Opening-angle reuse (CM-043 §3) | Both · opening paragraph, first and last sentences | Both open "Apex Roofing of the Lowcountry is a roof[ing contractor / er] that / based…" and both end "Call (843) 757-2739 for a free estimate." | Across about 20 pages this becomes a visible template; the buyer states differ, the frame does not. | Vary the entity sentence and the CTA sentence per page; record the used forms in C3 at write-back so later pages avoid them. | PROPOSED | — |
| 9 | SEM-8 | svc-roof-repair · H2 "How Do Our Roofers Fix a Damaged Roof in Beaufort and Jasper Counties?", 2nd sentence | "Apex was founded by Ralph Brehany and his son, Pierce." — founder story on a service page; LD names them too. | The founders belong to the About page (settled About decision); here the line only sets up the W25 NEED. | Keep only if W25 is confirmed and reword to the fact that matters for repairs (who gets on the roof); otherwise cut. | PROPOSED | W25 (client) |
| 10 | SEM-8 | svc-roof-repair · H3 "Hail Damage Repair" | Storm/hail damage overlaps the Emergency Roof Repair page's intent, and hail repair is unconfirmed. | Storm work may belong to the emergency page; an unconfirmed repair type cannot ship. | If the client confirms hail repair as scheduled work, keep it here; otherwise route storm/hail damage to the Emergency Roof Repair brief and remove the H3. | BLOCKED | client confirms hail repair (NEED on the H3) |
| 11 | BB-310 | loc-bluffton · H2 "Which Roof Services Can You Get From a Bluffton Roofing Contractor?", lead sentence | "…eight roofing services, each with its own page." describes the website, not the service. | Meta sentence adds nothing for the reader. | "Apex offers Bluffton homeowners eight roofing services:" (the H3s and link table stay as they are). | PROPOSED | — |

Checks with no findings: FAQ collision between the two pages; H2/H3 collision between the two pages; buyer-state reuse in the openings; reserved B1 variant use (none on either page). SEM-1 to SEM-7: not run (no definition).

## 3. Open [NEED] items still in the drafts (not SEM items — they block ship until answered)

**svc-roof-repair (12):** W25 who goes on the roof · W10 photo documentation · W11 corrosion-resistant flashing and synthetic underlayment · warranty on a repair · client confirms each of the 6 repair types (shingle, flashing, ridge cap/starter strip, soffit/fascia/deck, leak, hail) · SC source for the 25% rule (or keep the answer general) · typical repair visit length (drop that FAQ if unanswered).

**loc-bluffton (5):** Apex pulls the Town of Bluffton re-roof permit · UDO §3.18 Certificate of Appropriateness for an Old Town re-roof · UDO Article 5 roof-material list · W9 work in Palmetto Bluff, Belfair, Colleton River Plantation, Moss Creek · a 6th Bluffton neighborhood with a public source (spec needs 6–12).
