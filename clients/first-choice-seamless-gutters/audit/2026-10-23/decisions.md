# Decision log — first-choice-seamless-gutters

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

## DEC-LOCAL-001 · 2026-10-23 · N/A-with-rationale
Decision: The [CONTRADICTED] host-consistency cross-check (apex vs www for polk-county.net and weather.gov) blocks no finding.
Reason: Both hosts are external outbound-link targets, not the client's site; the client host check is [CONFIRMED].
Affects: none
Decided by: discovery-audit (agent), S12
Maps to register entry: 00-crosschecks.md

## DEC-LOCAL-002 · 2026-10-23 · applied default
Decision: Live public evidence captured to inputs/public-site-2026-10-23/ (sitemap URL list, homepage, Lake Wales page, the two sitemap-only blog posts, robots.txt) — SRC-055…SRC-060 — and S12 re-run so the sitemap cross-check and the screen include them.
Reason: the crawl had no sitemap list and missed the two posts and the category archive (no internal links).
Affects: F-001, F-008, F-009, F-011, F-012, F-013, F-017, F-019–F-034, F-038–F-048
Decided by: discovery-audit (agent)
Maps to register entry: 00-manifest.csv SRC-055–SRC-060

## DEC-LOCAL-003 · 2026-10-23 · applied default
Decision: C3 in the screen rests on the GBP website field only — no citation tracker export is on file (S09). The only conditional redirect in this audit is Plant City (F-015, screen pass, C4 still required), so the gap changes no decision.
Reason: CM-019.
Affects: F-015, url-decision-map.csv
Decided by: discovery-audit (agent)
Maps to register entry: redirect-screen.csv

## DEC-LOCAL-004 · 2026-10-23 · applied default
Decision: Homepage main keyword for the CM-059 check = 'gutters lakeland' (390/mo, organic #15) — the highest-volume non-brand query the homepage ranks for (SRC-028). HP-06 scored fail (H1 not on the reserved B1 variants).
Reason: no main keyword is recorded in facts.json; the H1-lock Ask (F-017) defaults to no change either way.
Affects: F-017, F-023
Decided by: discovery-audit (agent)
Maps to register entry: h1lock-check.md

## DEC-LOCAL-005 · 2026-10-23 · applied default
Decision: No create rows in the URL Decision Map. Lakeland Highlands (GBP area, settled towns_served) and any hub are left to Build's site plan; the audit recommends no county hub (F-016).
Reason: Lakeland Highlands adjoins Lakeland with no ranking evidence; a Polk County hub would duplicate the homepage's area entity (CM-024, CM-058).
Affects: F-016
Decided by: discovery-audit (agent)
Maps to register entry: url-decision-map.csv

## DEC-LOCAL-006 · 2026-10-23 · applied default
Decision: Questions already on the client's proof sheet (base_town, towns_outside_polk, licence_number, insurance_status, warranty_terms, military_seniors_discount, subcontracting, after_hours) are not re-asked; the findings carry the returned sheet as a Dependency. No kind-3 Ask is written.
Reason: a question is asked once (P4).
Affects: F-001, F-003, F-004, F-005, F-006, F-015, F-049
Decided by: discovery-audit (agent)
Maps to register entry: findings.csv Dependency column

## DEC-LOCAL-007 · 2026-10-23 · N/A-with-rationale
Decision: S15 judgment checks scored by the agent (conformance.py judge: no API key) into audit/conformance-judgment.csv for the scoring set (homepage, two blog posts). Checks the capture cannot measure (link counts, readability, plugin-rendered gallery) are NE, not FAIL.
Reason: CM-063; a missing measurement is never a finding.
Affects: F-019–F-034, F-038–F-048
Decided by: discovery-audit (agent)
Maps to register entry: conformance-judgment.csv

## DEC-LOCAL-008 · 2026-10-23 · review
Decision: Independent review per CM-026 (fresh-context reviewer).
Reason: S17 self-check of findings.csv and url-decision-map.csv; outcomes in review-s17.csv.
Affects: F-008, F-011, F-012, F-015, F-019–F-024, F-029, F-032, F-033
Decided by: audit-reviewer (agent)
Maps to register entry: review-s17.csv
