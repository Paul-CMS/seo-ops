# Audit — apex-roofing-of-the-lowcountry

**Stage:** Analysis complete (S12–S16) · Gate B answered (Paul, 2026-10-07) · Review (S17) next, in the fresh-context audit-reviewer
**Opened:** 2026-10-07 · run 20261007-194242-discovery-9495
**SOP:** GOV-02 Analysis + Gate B, via the seo-technical-audit skill; rules from `methodology/rulings.md`

## Loaded inputs

| Input | Location | Version / date | Loaded |
|---|---|---|---|
| Methodology & guidelines | `methodology/rulings.md`; `methodology/specs/*.md` (all DRAFT); `methodology/audit-steps.md`; skill references | rulings consolidated 2026-10-02, entries to CM-053 | ☑ |
| Brand / truth file | `brand-guide.md` (A, B1, B2 approved 2026-10-05; C–I not reconciled) | 2026-10-05 | ☑ |
| Intake record | returned proof sheet (2026-10-07) + Paul's answers (2026-10-06, addendum 2026-10-07) | 2026-10-07 | ☑ |
| Evidence folder | `inputs/crawl/` (S05), `data/` (S06–S08, S10, S19, S21), `inputs/seopress-settings-2026-10-05.json` (S20), `inputs/live-pages/` (confirmation reads) | 2026-10-05 → 2026-10-07 | ☑ |

## State

| Step | Status | Date | Notes |
|---|---|---|---|
| Phase 0 — load & pin | done | 2026-10-07 | manifest SRC-001–027 |
| Phase 0 — readiness check | done | 2026-10-07 | no halt — crawl complete (72 URLs, empty_queue); site not JS-dependent for primary content |
| Analysis — inventories | done | 2026-10-07 | urls, services, locations, backlinks, conversions, citations (N/A) |
| Analysis — reconciliation | done | 2026-10-07 | crawl vs sitemap vs backlinks vs rankings vs GBP field |
| Analysis — analysis | done | 2026-10-07 | 33 findings (4 High, 20 Medium, 9 Low); URL Decision Map 83 rows; 5 scorecards |
| Gate B — questions | answered | 2026-10-07 | Q1 = 1a, Q2 = 2a (Paul) — F-014, F-004, F-023 superseded (rev 2) |
| Review — self-check | not started | | audit-reviewer (S17) |
| Review — package | not started | | S18 |
| client-confirmation boundary | blocked | | Not part of this skill |

## Coverage (Phase 0)

| Category | Evidence | Source IDs | Assessable |
|---|---|---|---|
| 1 Baseline & measurement | none (S11 skipped) | — | N/A — DEC-LOCAL-002 |
| 2 Technical & crawl | crawl, sitemap, redirect checks, SEOPress settings | SRC-001–013, 020, 024 | yes |
| 3 Brand & entity | Brand Guide, proof sheet, Paul's answers, live captures, rankings (brand query) | SRC-021–023, 026, 027, 014 | yes |
| 4 GBP & local | GBP field (A11), rankings local pack, Local Dominator grid (ranks only) | SRC-014, 017, 026 | partly — grid centre unverified, no geographic claims |
| 5 Architecture | crawl, rankings, backlinks, sitemap | SRC-008, 001, 014, 015, 024 | yes |
| 6 On-page | crawl titles/H1/H2, live captures | SRC-006, 007, 012, 023 | yes |
| 7 Blog & supporting | crawl, post captures, rankings | SRC-008, 014, 025 | partly — classification is the Blog Decision Map's (/blog) |
| 8 Citations & authority | backlinks only | SRC-015 | citations N/A (S09 skipped) |
| 9 Schema readiness | served-HTML JSON-LD, SEOPress settings | SRC-023, 020 | yes (recommendation only) |

## Assumptions and Limitations

- **Specs are DRAFT** (all six): failed checks are advisory recommendations at the spec's severity; Paul has not approved the specs (DEC-LOCAL-003).
- **Crawl configuration** (Agency Profile): DataforSEO OnPage basic, no JavaScript rendering. Review bar, social-proof bar, Maps embeds and city maps are not in the served HTML; they may be JS-loaded and are **not** asserted as missing (HP-13, LOC-16 not assessed). Schema absence (F-007) rests on served HTML that does carry a server-rendered WebSite node.
- **No GSC / GA4 / call tracking** (S11 skipped): no baseline, no lead evidence; CM-019 condition 4 (client confirms no leads) is unanswered for every URL, and condition 3 (citation destination) is unknown because S09 was skipped — so **no URL is a full CM-019 candidate**; the one URL change considered (F-010) is `Needs Evidence`.
- **Rankings are US country-level** (DataforSEO Labs): local positions differ; used only for CM-019/CM-020 tests, never as local rank.
- **Local grid** (Local Dominator): ranks only; the reports' written advice is not used; competitor review counts unreliable; grid centre unverified — no geographic-pattern claim is made.
- **Fan-out (S21)** queries have no volume and are never evidence for CM-019/020/021 (CM-045).
- **Brand Guide Section D is not reconciled**: claims are tested against the returned sheet and Paul's answers (DEC-LOCAL-005); F-002 lists every unconfirmed claim for the client-confirmation list.
- **Writing-quality checks** (COM-02, -06, -07, -12, -13, -14) are not scored — Build's self-critique covers them on the rebuilt pages.
- **Blog checks** BLG-06–15, 17, 20–22 are left to the Blog Decision Map.
- **Neighbourhood names** were checked for type (road/corridor vs neighbourhood) and duplication, not verified one by one (F-024).
- **Backlinks**: 694 of 711 referring domains point at the homepage and most are auto-generated SEO-checker sites; reported as an inventory note, no finding (CM-006).

## Client-confirmation list (from Analysis — for Review/S18 to render)

Every claim quoted in F-002 (ShingleMaster status; replacement price range; skylight prices and brands; project history; process and code claims; Lady's Island claim; financing / payment arrangements); the synthetic-roofing offering (F-009 target); "no leads" for /metal-roofing-2/ if the slug change is pursued (F-010).

## Blocked on

Nothing — Gate B answered by Paul 2026-10-07 (DEC-LOCAL-011, DEC-LOCAL-012). Next: S17 review.

## Handoffs

None raised by the audit (recommendations only; Low items will be batched into one technical handoff after audit_approved).

---
Deliverables in `deliverables/` are **rendered**, never edited. To change a
recommendation, change the finding row and re-render.
