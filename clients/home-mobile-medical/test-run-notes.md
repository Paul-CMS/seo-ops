# Home Mobile Medical — test-run notes

Kept for this test run. Anything Paul writes as "note:" is added here verbatim, with the date.

## 2026-10-06 — import started
- Imported with `/new-client --import "Home Mobile Medical"` (run 20261006-112201-new-client-fb9a).
- Source: v3 folder `Home Mobile Medical - TMS` (Drive id 1Hlfhaelu3mvsAItJgg0Zpi7T2_ccrNRp). A second, older
  `Home Mobile Medical - TMS` sits in `CMS Technical SEO Audits 2026` (id 1rBg36WDZ5CM6haRAiydfoj8Y4DyyiSXb); not used as a source.
- Sensitivity: Paul set health_adjacent (classifier had said health). No practitioner sign-off; health/safety claims need a named authoritative source; Paul approves those pages.

## 2026-10-06 — Paul's answers (round 1)
- No Georgia locations. Savannah and Pooler come out of the location set.
- GBP address is live because it is used on the GBP profile, even though it is not a storefront; it stays in the footer for GBP ↔ website cross-reference.
- Sign off everything once all claims have been proofed and everything has been recorded.
- Search Console data is replaced with DataforSEO data.

## 2026-10-06 — round 2
- Paul: "I think the build files got lost." (homepage build sheet, service and location drafts — none found in Drive)
- Paul asked to see the pages the 410 question covers before deciding → clients/home-mobile-medical/out-of-area-pages.md
- Paul said yes to live-site access; the browser pane still refused homemobilemedical.com.

## 2026-10-06 — round 3
- Paul: drop Florida and Michigan. 301, not 410.
- Paul asked whether a case can be made to keep /service-area/ plus three regional hubs: /service-area/charleston/, /service-area/hhi-beaufort/, /service-area/savannah/ — and how that affects the entity decision.
- Paul asked whether the DataforSEO analysis is running (it is not: DFS login missing from .env).

## 2026-10-06 — round 4
- Paul: DataforSEO login now added to .env.
- Paul: strip Georgia from the site and make it its own subdomain or microsite, keeping the entity clean.

## 2026-10-06 — round 5
- Paul: DataforSEO runs after approval of the rest — stick to the workflow.
- Paul: yes, he takes jobs in Georgia; the microsite happens.
- Paul: a hub can be a metro area if that is legitimate categorization; otherwise hub by county pages. → lessons.md L-008 (proposed).

## 2026-10-07 — Paul marked the claims proof list
- A1–A9, B1–B7 confirmed (A5: 106 Arrow Road needs removal; A9: look up a business licence entry, else ask client; B5: reviews support it, keep as marketing language; B7: keep and rewrite).
- C: all confirmed; maintenance and repair scope still to clarify.
- D1: confirmed — "think he might be a one man show".
- D2–D11, E, F, G3–G4: not yet marked → asked in chat.

## 2026-10-07 — client answers (Paul relayed)
- Repairs and maintenance: yes. Team: Jason plus a helper. Free in-home estimates: yes; can quote from a photo (stair count). Wants a photo-upload-to-quote feature.
- Install: usually one day, 3–4 hours. Brands: Paul checking. Stannah as main dealer reference if evidence exists.
- Not answered yet: outdoor lifts.

## 2026-10-07 — Paul's answers (round 7)
- Outdoor = porch lifts. Manufacturer's warranty only. No licence number found. Reviews are placeholders. Legal name: Home Mobile Medical.
- "Fitted to your staircase": yes. Safety statement: partially keep, as holding himself to the highest industry standards.
- Asked: do we need to keep the Medicare/tax/ADA blogs?
- GBP: primary Mobility equipment supplier; secondary Medical equipment supplier.

## 2026-10-07 — round 8
- Primary GBP category only. Keep the blogs until later decision. Confirming everything else.
- Repairs: general scope — any stair lift or anything within service coverage, not just his installs.
- Brand line: "installing and repairing leading brands like Stannah, (1–2 more?)", no authorized-dealer claim.

## 2026-10-07 — round 9
- Brand line confirmed (Stannah, Bruno, Harmar). Folly Island. Schema assets: placeholders, check back at schema.
- Payment methods: general accepted payment methods. Asked what the site says about after-hours service.
- "Then we run B" (system runs the audit step on the existing evidence).

## 2026-10-08 — Paul's answers to the audit's open choices
1. "retire pages" — retire the 36 candidates (Paul confirms CM-019 condition 4 for the client).
2. a — default 301 targets.
3. "3.b" — Paul Exception to redirect the CM-019-failing pages (scope to confirm in the next session).
4. a — homepage H1 stays; reserved wording goes in the title (as for Apex).
5. "it was the old bme gbp, and is ours now."
- Asked for a handoff to a new session (one session per stage, new rules). → session-handoff-2026-10-08.md
