# Home Mobile Medical — session handoff (2026-10-08)

**For:** the next session, Stage 4 — Audit. Start a new chat in `~/Documents/seo-ops` on the stage's model and type
`/next home-mobile-medical`. Step zero: `python3 scripts/records.py top home-mobile-medical`, then read
`clients/home-mobile-medical/decisions-settled.md` and this file.

## Where it stands
- Imported 2026-10-07 (run 20261006-112201-new-client-fb9a). Paul approved via import: entity_approved,
  proof_sheet_approved, brand_guide_approved (+ proof_sheet_returned). WordPress connected (seo-ops Editor).
- Data step done (run 20261007-173133-discovery-dce1, $0.265). Audit done with independent review and four
  REVIEW deliverables marked (run 20261007-203219-discovery-784c): 40 findings (12H/13M/15L), 159-row URL Decision Map.
- All runs are FINISHED; nothing is open. Deliverables:
  `clients/home-mobile-medical/audit/2026-10-07/deliverables/` (Finding Register, URL Decision Map, Recommendations,
  Evidence Manifest — all `- REVIEW.md`).

## Paul's answers to the audit's open choices (2026-10-08, in chat) — not yet recorded in the log
Record each with `run.py decision … --settle <key>` in the revision run, then apply them to the deliverables.

| # | Question | Paul's answer | Settle key (suggested) |
|---|---|---|---|
| Q1 | Client confirms no leads on the 36 retirement candidates (17 FL/MI, 5 discontinued-service, 13 SC legacy duplicates, /services/straight-stair-lifts/) | "retire pages" — Paul confirms CM-019 condition 4 for these 36 | `hmm-retire-36-c4` |
| Q2 | 301 targets | a — FL/MI → /services/stair-lifts/; power chairs + scooter lifts → /services/; ramps → /services/porch-lifts/ (SC duplicates → their canonical, per the map) | `hmm-301-targets` |
| Q3 | The 10 URLs that fail CM-019 (rank or have links) | "3.b" — Paul Exception to redirect them | `hmm-cm019-exception` |
| Q4 | Homepage H1 (CF-LOCAL-001 / L-009) | a — H1 stays as live; reserved variant "South Carolina Lowcountry" goes in the title (same as Apex) | `hmm-homepage-h1` |
| Q9 | GBP history | "it was the old BME GBP, and is ours now" — the listing is Beaufort Medical Equipment's original GBP, renamed, now owned/controlled by Home Mobile Medical | `hmm-gbp-history` |

## Must clarify with Paul before the revision (do not guess)
1. **Q3 scope.** Three of the 10 are Georgia (`/savannah-ga/`, `/service-area/savannah-ga/`, `/savannah/stair-lift/`):
   Paul's decision holds Georgia for the microsite. Ask: does the exception cover only the 7 SC URLs (Bluffton ×3,
   /charleston-sc/mobility-ramps/, /service-area/mt-pleasant-sc/, /charleston/stair-lift/, /hilton-head/stair-lift/),
   with Georgia still held? A Paul Exception needs scope, reason, risk, review trigger and exit condition (GOV-06) —
   propose them, Paul confirms. Note /bluffton-sc/wheelchair-lift-repair/ ranks for repair terms and repair is now a
   confirmed service — ask whether it redirects to the new repair page or is kept/rewritten.
2. **CM-019 condition 3 (Q8)** is still open for every candidate: Gwen checks the website field on each of the 9 tracked
   citation listings. Paul's Q1 answer covers condition 4 only; no redirect handoff goes to Jonie until Q8 returns.

## The revision run (Stage 4)
- Apply Q1–Q4, Q9 (and the clarified Q3) to the URL Decision Map, Recommendations and Finding Register (superseding
  rows; append-only). Re-mark `audit_deliverables` with the revised files.
- **Brand Guide Section D "History"** must change: the GBP listing is BME's original listing, renamed and now HMM's;
  the business itself is still not a rebrand (BME's business was sold). This explains the 2.9★/19 old-store reviews and
  the "Our Evolution from Beaufort Medical Equipment" post. Changing the value voids brand_guide_approved — it is
  re-approved in Approval 2 together with the audit.
- Then `/next` prints Approval 2: `/approve home-mobile-medical audit_approved brand_guide_approved` with its files.
  Approving it signs discovery off and opens Build.

## Waiting on VAs (do not block Approval 2)
- Jonie: H-2026-10-07-01-wp_setup (effectively done — /wp-check logged in as seo-ops; ingest her worksheet),
  H-2026-10-07-02-seopress_settings (S20), Q5 (`/new-homepage/`, `/about-us-across-the-web/` live?), Q6 (status of 40 uncrawled URLs).
- Gwen: Q7 (grid centre/device), Q8 (citation link destinations).

## Paul's items outside the audit
- L-008 (metro hubs) and L-009 (homepage-H1 lock) are PROPOSED in methodology/lessons.md; county-hub spec DRAFT;
  page specs need `/approve global specs` before Build scores or writes pages.
- Review replies (19, honest "new focus" wording, not "new leadership") + a review-request message → Gwen handoff in Build;
  Paul approves the wording first. Now unblocked by Q9.
- Georgia microsite → its own `/new-client` later.
- Rename list (`rename-list.md`): LD → LNKD on the Linkdominator file; the old "READ FIRST" Google Doc in Deliverables.
- Optional: fan-out for Hilton Head Island and Bluffton (+$0.07). Confirm the ranked_keywords price in dfs_prices.json.

## Process notes for the next session
- This session ran under the old one-session rules; new rules (one session per stage, `--settle`, automatic Drive copy
  on finish) apply from now. The four REVIEW deliverables are not yet in Drive Deliverables — `run.py finish` / `/approve`
  copy them under the new rules.
- `clients/home-mobile-medical/test-run-notes.md` is kept; add anything Paul writes as "note:".
- At each decision, explain in plain language what Paul approves and what changes once he does.
