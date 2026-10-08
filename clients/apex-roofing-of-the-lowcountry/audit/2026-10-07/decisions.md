# Decision log — apex-roofing-of-the-lowcountry

Append-only. Never edit or summarize an existing entry. Every Paul Exception,
applied default, N/A-with-rationale and deviation from GOV-02 goes here with the
finding IDs it affects.

Format:

```
## DEC-LOCAL-001 · YYYY-MM-DD · <type>
Decision:
Reason:
Affects: <finding IDs / categories>
Decided by:
Maps to register entry:
```

---

## DEC-LOCAL-001 · 2026-10-07 · standing exception cited
Decision: Claude performs both the analysis and the review of this audit. Standing exception CM-026 applies; the review (S17) runs in the fresh-context audit-reviewer subagent, which loads only the registers, inventories, manifest, cross-checks, this log and the questions — never the analysis conversation.
Reason: CM-026 (replaces per-audit logging under RULE-011).
Affects: all findings
Decided by: standing ruling CM-026
Maps to register entry: CM-026

## DEC-LOCAL-002 · 2026-10-07 · N/A with rationale
Decision: Category 1 (Baseline and measurement) is N/A — no GSC / GA4 / call tracking (S11 skipped; Paul 2026-10-06 "Drop it — we have SEO data"). Category 8 citations part is N/A — S09 skipped (Paul). Backlink part of 8 assessed from S08 (no finding; quality judgement is not a removal reason, CM-006). Conversion path (contact form) not testable in a basic crawl.
Reason: evidence not supplied; Phase 0 readiness — limitation, not a halt.
Affects: category 1, 8; CM-019 condition 3 (citation destination) is "unknown" on every URL, so no page can be a full CM-019 candidate this audit (F-010).
Decided by: analyst (per evidence-intake readiness rules)
Maps to register entry: PROC-02 (absence of evidence is not evidence)

## DEC-LOCAL-003 · 2026-10-07 · limitation
Decision: All six page specs (methodology/specs/*.md) are DRAFT — advisory. Failed checks are reported at the severity in each spec's "Fails as" column and are recommendations, not gates. Writing-quality checks (COM-02, COM-06, COM-07, COM-12, COM-13, COM-14) are marked "not scored" in the scorecards — they are the writers' self-critique checks in Build and every money page is rebuilt anyway. Blog checks BLG-06–15, 17, 20–22 are left to the Blog Decision Map (bb-blog-analysis).
Reason: specs README status line; scope of the audit vs Build / Blog.
Affects: every S15 finding (F-004–F-007, F-010–F-028, F-032)
Decided by: analyst
Maps to register entry: specs/README.md "Status line rule"

## DEC-LOCAL-004 · 2026-10-07 · Paul direction applied
Decision: Paul's note (2026-10-07): a FAQ or PAA question that is not town-specific or tied to the page's service category must not be used just because it came up — it has to make sense and apply. Applied in the audit to the live FAQs: city-swapped generic questions fail LOC-14/SVC-15 (F-021); a town-specific question that does not apply to a residential-only business (Port Royal MCRD) is listed in F-001. The S19 PAA routing (5 rows routed to a location FAQ) and the S21 fan-out routing must be re-checked against this note in the site plan — not re-routed by the audit.
Reason: Paul's direction (passed by the calling command, 2026-10-07).
Affects: F-001, F-021, F-022, F-023 (homepage FAQ to be added)
Decided by: Paul
Maps to register entry: BB-316, CM-048, CM-015

## DEC-LOCAL-005 · 2026-10-07 · evidence basis
Decision: Brand Guide Section D is not reconciled yet. Claims are tested against the returned proof sheet (client's words, 2026-10-07) and Paul's answers (2026-10-06 with the 2026-10-07 addendum) as the best current evidence (F-002). Nothing is resolved here; reconcile writes Section D/D2.
Reason: Paul's instruction for this audit run.
Affects: F-001, F-002, F-016, F-020, F-028
Decided by: Paul
Maps to register entry: CM-016, CM-027, RULE-010

## DEC-LOCAL-006 · 2026-10-07 · evidence added
Decision: Free public page reads of the live site (served HTML, no JavaScript) were used to confirm crawl findings and saved as MANUAL evidence (SRC-023–025, inputs/live-pages/). They read the same public pages the S05 crawl and S02 discovery cover; no paid call was made. There is no separate row in audit-steps.md for these confirmation reads (noted for the next pause).
Reason: the DataforSEO basic crawl gives headings, titles and links but not body text; F-001, F-002, F-016, F-017, F-020, F-021, F-022, F-024, F-033 need the text.
Affects: those findings
Decided by: Paul allowed free public page reads for this run (calling command)
Maps to register entry: S02 / S05 (public site)

## DEC-LOCAL-007 · 2026-10-07 · interpretation
Decision: The two DataforSEO "cannibalization" clusters (CAN-001, CAN-002) are the homepage under http://www. (local-pack result, the GBP website field) and https:// (organic). Not cannibalization (RULE-005); recorded as the GBP-field finding F-008. Blog posts with overlapping intent (two "questions to ask a roofer" posts; three lifespan/salt-air posts) have no observed search conflict (none ranks) — no cannibalization finding (RULE-015, CM-021); left to the Blog Decision Map.
Reason: RULE-005, RULE-015, CM-021.
Affects: F-008; URL Decision Map blog rows
Decided by: analyst
Maps to register entry: RULE-005

## DEC-LOCAL-008 · 2026-10-07 · interpretation
Decision: "The Best" in 21 H1s is raised as "no CM-020 decision recorded" (HP-07/SVC-09/LOC-07: the H1 must match Brand Guide H2), never as a missing or present word by itself (CM-020). Conditions evaluated from S07 best-variants (demand: 3 near-me queries at volume 10; no city-level volume), rankings (no service/location page ranks; opportunity not measured — the "3 of top 10 use best" SERP test would be a paid call and was not run), S06 (5.0 / 67 → proof passes). Homepage H1 is locked (BB-313 §3) — no change recommended (HP-08).
Reason: CM-020.
Affects: F-006, F-011
Decided by: analyst
Maps to register entry: CM-020

## DEC-LOCAL-009 · 2026-10-07 · conflict recorded
Decision: CF-LOCAL-001 (conflicts.csv) — service-title format: SVC-03/BB-302 vs Brand Guide B2 note (Paul 2026-10-05). Not resolved here (PROC-01): current production rule (SVC-03) followed; F-014 carries confidence Assumed and paul_approval_required; raised as Gate B Q1.
Reason: PROC-01.
Affects: F-014, F-004
Decided by: analyst (record only)
Maps to register entry: PROC-01

## DEC-LOCAL-010 · 2026-10-07 · Gate B outcome
Decision: Gate B raised 2 questions, both routed to Paul (questions/questions.csv): Q1 — service-title format (blocks F-014, title side of F-004); Q2 — 8 service H3 links on the homepage vs BB-313's 5–6 (blocks the HP-11 part of F-023). No VA questions (the crawl is complete — stop reason empty_queue; the Agency Profile answers rendering and tool questions). Items that do not pass the trigger test (claim confirmations, synthetic-roofing redirect target, neighbourhood verification, GBP access) go to Assumptions and Limitations or the client-confirmation list, not Gate B. If no answer comes back, the stated defaults apply and the affected findings carry confidence Assumed.
Reason: gate-b-questions.md trigger test.
Affects: F-014, F-004, F-023
Decided by: analyst; answers pending from Paul
Maps to register entry: GOV-02 Gate B

## DEC-LOCAL-011 · 2026-10-07 · Paul decision (Gate B Q1)
Decision: Q1 = 1a. For this client, service-page SEO titles are `Service Name - Brand` with NO area term, "since Lowcountry is already part of the brand and therefore serves a service area entity as well." The Brand Guide B2 sentence "SEO titles take the metro-area, Hilton Head Island Metropolitan Area or county variants" is superseded for service pages by this decision (it still applies to the homepage title, which takes the reserved variant "Hilton Head Island–Bluffton–Port Royal Metropolitan Area"). brand-guide.md is not edited here (B2 is under the entity approval); the reconcile / site plan carries the note forward.
Reason: Gate B answer; resolves CF-LOCAL-001 for service pages (PROC-01 step 5 — a client-level ruling, not a rulings.md entry).
Affects: F-014 (rev 2 — confidence no longer Assumed), F-004 (rev 2 — title side)
Decided by: Paul, 2026-10-07 (logged as run decision in 20261007-194242-discovery-9495)
Maps to register entry: SVC-03 / BB-302; CF-LOCAL-001

## DEC-LOCAL-012 · 2026-10-07 · Paul Exception (Gate B Q2)
Decision: Q2 = 2a. The rebuilt homepage links all 8 services as H3 links — a Paul Exception to BB-313 §6 (maximum 5–6). Scope: this client's homepage. Reason: Paul kept all 8 services (2026-10-06). Risk: a longer services block than the Standard sets. Review trigger / exit condition: the service list changes, or the homepage pilot correction says otherwise.
Reason: Gate B answer.
Affects: F-023 (rev 2 — HP-11 part closed)
Decided by: Paul, 2026-10-07 (logged as run decision in 20261007-194242-discovery-9495)
Maps to register entry: BB-313 §6; HP-11

## DEC-LOCAL-013 · 2026-10-07 · review (S17)
Decision: Independent review per CM-026 (fresh-context reviewer). The audit-reviewer subagent loaded only findings.csv, inventories, manifest, cross-checks, this log, questions with answers, methodology and the Brand Guide, and opened the evidence at each locator. Outcome over 33 findings: 21 confirmed, 9 revised by superseding row (F-001, F-002, F-004 rev 3, F-011, F-012 rev 2, F-015, F-016, F-026, F-031), 3 withdrawn (F-005 merged into F-004; F-013 merged into F-012; F-006). Severity after review: High 3 (F-014, F-015, F-022), Medium 17, Low 10. F-004 lowered High → Medium (a wording correction inside the approved area entity, not an entity break — CM-028). URL Decision Map: 3 rows corrected (U-001 references; U-070 / U-071 "Client Confirmed" set to No — needed). Record: review-s17.csv.
Reason: CM-026 (standing exception to RULE-011); review-selfcheck.md challenge protocol.
Affects: all findings; URL Decision Map U-001, U-070, U-071
Decided by: audit-reviewer (S17)
Maps to register entry: CM-026, CM-028, CM-019

## DEC-LOCAL-014 · 2026-10-08 · Paul ruling (CF-LOCAL-002)
Decision: HP-06 vs BB-304 ruled. The reserved homepage variant goes in the homepage SEO title; the H1 takes a familiar pool variant. The reserved homepage variant is now "Hilton Head Island Metropolitan Area" (Wikipedia's article title). Brand Guide B1/B2 and Discovery Record §3.8 were updated in run 20261008-073331-discovery-a866 and the entity was re-approved by Paul on 2026-10-08. "Hilton Head Island–Bluffton–Port Royal Metropolitan Area" moved to the pool. Homepage H1: locked as live (BB-313 §3, HP-08). If it is ever rebuilt, Paul prefers "Lowcountry" or "South Carolina Lowcountry". The HP-06 wording is corrected when the specs are approved.
Reason: Paul's ruling at the audit approval.
Affects: F-004 (rev 4 — now a one-word fix, 'Metro' → 'Metropolitan', Medium per CM-028); withdrawn F-006 stays withdrawn; conflicts.csv CF-LOCAL-002 ruled
Decided by: Paul, 2026-10-08
Maps to register entry: BB-304, BB-313 §3, HP-06; PROC-01 step 5

## DEC-LOCAL-015 · 2026-10-08 · Paul ruling (About page)
Decision: About page title "About Apex Roofing of the Lowcountry - Roofing Contractor in the Hilton Head Island–Bluffton–Port Royal Metropolitan Area" (a pool area variant; the reserved variant is homepage-only). H1 "About Apex Roofing of the Lowcountry". This H1 carries the brand, which ABT-03 would otherwise fail; Paul's ruling governs for this client. Owner section: Ralph and Pierce Brehany by name only, with a clearly visible placeholder for their photo and job titles so nobody ships it unnoticed.
Reason: closes the about.md Coastal defaults (title "Area Category", H1 format, owner section) that F-015/F-016 waited on.
Affects: F-015 (rev 3, High — ABT-01 and ABT-04 now firm), F-016 (rev 3, Low → Medium — no longer a Coastal default awaiting a ruling)
Decided by: Paul, 2026-10-08
Maps to register entry: BB-302, ABT-01, ABT-03, ABT-04, ABT-07; CM-016 (placeholders)

## DEC-LOCAL-016 · 2026-10-08 · Paul ruling (3a — specs DRAFT)
Decision: The audit is accepted as advisory while the page specs are DRAFT. The specs are approved before Build starts.
Reason: Paul's ruling at the audit approval.
Affects: every spec-based finding (DEC-LOCAL-003 stands)
Decided by: Paul, 2026-10-08
Maps to register entry: specs/README.md "Status line rule"

## DEC-LOCAL-017 · 2026-10-08 · alignment and review
Decision:
- Brand Guide B2's SEO-title sentence is now aligned with Gate B 1a (DEC-LOCAL-011). The earlier "superseded for service pages" open point is closed.
- No new findings were written. F-004, F-015 and F-016 were revised only to apply Paul's rulings (DEC-LOCAL-014, -015), so no new fresh-context review is needed; S17 (DEC-LOCAL-013) stands.
- F-016's severity rises from Low to Medium mechanically: the ruling removes the "Coastal default — never above Low" condition the reviewer applied.
- Final active counts: High 3, Medium 18, Low 9.
Reason: Paul's rulings applied to existing findings.
Affects: F-004, F-015, F-016
Decided by: analyst (applying Paul's rulings)
Maps to register entry: CM-026, CM-028
