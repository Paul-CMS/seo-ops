# Decision log — carolina-carpet-cleaning

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

## DEC-LOCAL-001 · 2026-10-29 · applied default (CM-019)
Decision: No backlinks pull is on file (S08), so C2 is "needs evidence" on every URL; every URL the screen did not fail is kept live. No redirect, merge, noindex or canonical change is proposed. Off-area and duplicate posts are "Needs Evidence - keep live" with disposition in the Blog Decision Map.
Reason: CM-019 — any condition missing → Needs Evidence; CM-021 — no observed conflict for blog redirects.
Affects: URL Decision Map U-007, U-045, U-053, U-054, U-082, U-107; F-009
Decided by: audit agent (default)
Maps to register entry: url-decision-map.csv; redirect-screen.csv

## DEC-LOCAL-002 · 2026-10-29 · N/A with rationale (contradicted auto check)
Decision: COM-N (Brand Guide phone in page text) failures are not written as findings. The live HTML of every sampled page carries (843) 575-6286 and tel:8435756286 in the footer; page-text.csv is truncated / footer-less. The 7 COM-N-only "light fix" rows (/blog/ + 5 pagination pages, /contact-us/) carry no finding.
Reason: a tool result contradicted by a second source blocks the finding. Flagged as flag F-004 for a system session.
Affects: conformance triage column; no finding IDs
Decided by: audit agent
Maps to register entry: SRC-059

## DEC-LOCAL-003 · 2026-10-29 · evidence captured
Decision: Three free live captures were added as MANUAL evidence: sitemap URL list (SRC-061), live redirect check of every GSC redirect/404/indexed URL and sitemap URL (SRC-060), homepage headings + phone links + JSON-LD (SRC-059). No DataforSEO spend in this step.
Reason: the cross-check reported no sitemap list; redirect findings need the live status.
Affects: F-001, F-008, F-010, F-011, F-015, F-016, F-018, F-019
Decided by: audit agent
Maps to register entry: 00-manifest.csv

## DEC-LOCAL-004 · 2026-10-29 · settled decision applied
Decision: The homepage title is scored against the settled format (title_format.homepage), so HP-01 passes and the homepage is left out of the COM-T (60-character) finding; its H1 is the settled homepage_h1_variant and stays locked (HP-08). The CM-059 H1-lock check was not run: HP-06 passes and the homepage sits at 6.14 for "carpet cleaning bluffton sc" (GSC, SRC-056), inside the top 10.
Reason: settled is settled (decisions-settled.md).
Affects: COM-T finding, homepage light-fix rows (F-026..F-031)
Decided by: audit agent
Maps to register entry: audit/conformance-judgment.csv HP-01, HP-06

## DEC-LOCAL-005 · 2026-10-29 · limitation
Decision: With no API key, the agent scored the 53 kept pages' judgment checks itself. Checks that need link positions (BLG-07..12) or a full-content reading (BLG-01, 06, 13–15, 17, 21, 22) are NE and go to the Blog Decision Map; BLG-20 is measured on the (possibly truncated) captured text. No citation tracker (S09) or local grid (S10) export is on file and Gwen's GBP lookup (H-2026-10-28-01) is open, so no GBP, citation or grid findings are written.
Reason: no finding without a locator; missing data is never a finding.
Affects: audit/conformance-judgment.csv; categories 4 and 8 (none)
Decided by: audit agent
Maps to register entry: audit/conformance-judgment.csv

## DEC-LOCAL-006 · 2026-10-29 · independent review
Decision: Independent review per CM-026 (fresh-context reviewer). Scope from review-scope.csv: 0 destructive URL rows, 4 Asks, 7 sampled findings, plus the 7 COM-N-only triage rows. Outcome: 5 confirmed (F-004, F-009, F-014, F-018, F-027); 5 revised as r2 (F-001, F-005, F-006, F-008, F-022); 1 withdrawn (F-031, duplicate of F-019); 7 map rows revised (U-011..U-016, U-044 triage light fix → keep). No finding rests on COM-N alone. Defaults changed: F-005 → b (hedged "within about an hour"), F-006 → b interim (claims not repeated until the products are named).
Reason: CM-026 mitigation; CM-061 severity; CM-016 (an unconfirmed claim is not shipped as a default).
Affects: F-001, F-005, F-006, F-008, F-022, F-031; U-011..U-016, U-044
Decided by: audit-reviewer (S17)
Maps to register entry: review-s17.csv

## DEC-LOCAL-007 · 2026-10-29 · review sheet notes (S18)
Decision: (1) Naming: "flag F-004" in DEC-LOCAL-002 means the phone-check system flag (COM-N, flags.jsonl entry #4), not audit finding F-004 (the blog guarantee claim); likewise flags.jsonl #5 and #6 raised in this step are not findings F-005/F-006. Flag and finding IDs share the F-### label (system flag raised). (2) conformance-triage.csv (generated) still says "light fix" for /blog/, /blog/page/2-6/ and /contact-us/; the URL Decision Map rev 2 (U-011..U-016, U-044) says keep and governs. The triage file is not hand-edited; the fix is the phone-check system flag (#4), for a system session. (3) Open check at Build: the footer phone (843) 575-6286 must render on /contact-us/. (4) The rendered sheet does not show the client items' interim defaults; they are F-005 → b, F-006 → b (audit-review.csv, recommended column).
Reason: S17 outcome (review-s17.csv); generated files change only through scripts.
Affects: F-004, F-005, F-006; U-011..U-016, U-044; conformance-triage.csv
Decided by: audit agent (S18)
Maps to register entry: audit-review.csv; flags.jsonl #4–#6
