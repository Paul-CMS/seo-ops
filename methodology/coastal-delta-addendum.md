# COASTAL DELTA — ADDENDUM (Paul rulings, 2 October 2026)
### Companion to `sop-source/Coastal-Delta-v1.0.md`. Same entry format.
**Status:** these are Paul's rulings and govern seo-ops now. They are not yet merged into the
Drive copy of the Delta — Paul decides when (his boss may still run the old workflow).

The Delta is the register of rulings; GOV-06 is the procedure for new conflicts. Where they
differ, the Delta (with this addendum) wins.

---

## CM-019 · Destructive candidates without Search Console · OVERRIDE
**Scopes:** CM-001 operational thresholds, GOV-06 §3 and T1, Agency Profile §3
**Status:** APPROVED · **Approved by:** Paul, 2026-10-02

**Was:** no GSC / analytics → nothing destructive is ever recommended.

**Now:** most clients give no GSC, GA4 or backlink access, so destructive decisions rest on
the system's own local search research. A page is a removal / consolidation / redirect /
noindex **candidate** only when **all four** hold:
1. DataforSEO shows **no ranking keywords in the top 100** for the URL
2. DataforSEO shows **no referring domains** to the URL
3. It is **not a GBP or citation destination**
4. The **client confirms no leads** from it

Any one missing → `Needs Evidence`. If the research cannot support a recommendation, make
none. Still: never delete, always redirect; still a candidate for Paul, never a decision.

## CM-020 · "The Best" in the H1 — a tested opener, not a default · OVERRIDE
**Scopes:** BB-305, CM-002, GOV-06 T2 · **Status:** APPROVED · Paul, 2026-10-02

Builds use the Bradley H1 format (BB-305, no brand), but **"The Best" is not the default.**
It goes in a service or location page H1 only if **all four** pass:
1. **Demand** — "best [service] [city]" or "best [service] near me" shows measurable search
   volume in DataforSEO, **or** at least 3 of the top 10 local results use "best" in the
   title or H1.
2. **Opportunity** — very competitive (top results use "best" and our page isn't top 3)
   **or** low-hanging fruit (our page ranks 4–20 for the "best" query).
3. **Proof** — the client can back it up from **verified** Brand Guide Section D facts
   (e.g. Google rating 4.5+ with 25+ reviews, or a real award).
4. **Not a sensitive industry** (chiropractic, medical, insurance, legal, financial) unless
   Paul approves it.

**Never change the H1 of a page already in the top 3 for its main keyword** (the
highest-volume keyword the URL ranks for that matches its service/area entity).

Every decision and its evidence goes in the URL Decision Map **and** Brand Guide Section H.
Thresholds are starting points, tuned in `methodology/lessons.md`. **Audits never flag a
missing "The Best" as a problem by itself.**

## CM-021 · Observed conflict for blog redirects · EXTEND
**Extends:** BB-701, CM-007, RULE-015 · **Status:** APPROVED · Paul, 2026-10-02

Observed search conflict = Search Console data **or** DataforSEO ranking data showing the post
and the commercial page **both ranking for the same query**. With neither: **no redirect
proposal.** Test B (the protected-post override) still runs first.

## CM-022 · Linking exceptions on any page · EXTEND
**Extends:** BB-205, BB-206, CM-005, CM-011 · **Status:** APPROVED · Paul, 2026-10-02

Bradley and the Delta govern service and location page structure: full city mesh,
table/H3 links (BB-205/206, CM-005). The `updated-link-strategy` skill governs blog posts and
the link audit / QA workflow. It may also **propose**, as an exception on any page, a
high-value outbound authority link or **one** high-value contextual anchor-text link. Each
needs a stated reason, is logged, and needs Paul's approval in Finish.

## CM-023 · Location page structure · EXTEND
**Scopes:** BB-315, the former writing standard's "2–3 H2s" rule · **Status:** APPROVED (default accepted), 2026-10-02

BB-315's section structure governs (services table, local context, FAQ, neighborhoods,
Things to Do, Top Sites, sibling cities). The "2–3 H2s" rule is dropped. CM-010 still
governs the word ceiling.

## CM-024 · Area variants are shared across pages · EXTEND
**Scopes:** BB-108, GOV-06 T7 · **Status:** APPROVED (default accepted), 2026-10-02

Variant collision is vertical, not horizontal: no variant repeats at consecutive elements on
one page. Service pages sharing an area variant from the Section B2 pool is correct. Only the
homepage's reserved variant (B1) is exclusive. GOV-06 T7's "no two pages of the same type
claim the same variant" is superseded.
