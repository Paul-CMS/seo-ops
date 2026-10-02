# Lessons — methodology corrections
### Append-only. Every correction to how the system applies the methodology, with the reason.

Format:

```
## L-### · YYYY-MM-DD · <short title>
Rule affected: <BB-### / CM-### / script / agent>
What we did before:
What we do now:
Why (evidence or Paul's reason):
Decided by:
Review when:
```

Threshold changes for CM-020 ("The Best") and CM-019 (destructive candidates) are recorded
here first, then reflected in `coastal-delta-addendum.md`.

---

## L-001 · 2026-10-02 · Destructive decisions without Search Console
Rule affected: CM-001, GOV-06 §3 / T1, Agency Profile §3 → new CM-019
What we did before: no GSC/GA4 meant nothing could ever be recommended for removal,
consolidation, redirect or noindex.
What we do now: candidate only when DataforSEO shows no top-100 rankings and no referring
domains, the URL is not a GBP/citation destination, and the client confirms no leads.
Otherwise `Needs Evidence`.
Why: most clients never give GSC/GA4/backlink access, so the old rule blocked every cleanup.
Paul's ruling: rest it on our own local search research, and make no recommendation where
that research cannot support one.
Decided by: Paul
Review when: after the first three clients run through it.

## L-002 · 2026-10-02 · "The Best" becomes a tested opener
Rule affected: BB-305, CM-002 → new CM-020
What we did before: "The Best" opened every service and location H1 by default.
What we do now: only when demand, opportunity, proof and not-sensitive all pass. Never on a
page already top 3 for its main keyword.
Why: the claim is grade C ("confirmed AI trigger" with no source), occupies the most valuable
slot on every page, and is a verifiable claim that needs proof.
Starting thresholds (tune here): Google rating 4.5+ with 25+ reviews; 3 of top 10 local
results using "best"; "low-hanging fruit" = our page ranks 4–20 for the "best" query.
Decided by: Paul
Review when: after 10 pages have been decided, or the cohort test reports.

## L-003 · 2026-10-02 · DataforSEO ranking overlap counts as observed blog conflict
Rule affected: BB-701, CM-007, RULE-015 → new CM-021; bb-blog-analysis `serp_overlap`
What we did before: no GSC meant no blog redirect could be proposed.
What we do now: GSC or DataforSEO showing both URLs ranking for the same query.
Why: same reason as L-001.
Decided by: Paul

## L-004 · 2026-10-02 · Crawler changed to DataforSEO OnPage
Rule affected: Agency Profile §1–2, seo-technical-audit step zero and reconciliation
What we did before: Screaming Frog free licence (500-URL cap, no rendering).
What we do now: DataforSEO OnPage basic mode via /crawl, converted to Screaming Frog-shaped
tables; Screaming Frog is the fallback. Missing JS-rendered data is never a finding.
Why: Paul's decision; no URL cap, full H2 lists, cost ~$0.15 per 1,000 pages.
Decided by: Paul

## L-005 · 2026-10-02 · Linkdominator tag LD → LNKD
Rule affected: naming convention
Why: LD now means location draft only. Old files go on the rename list, not renamed automatically.
Decided by: Paul
