# Lessons — inbox
### Inbox — proposed corrections. Nothing here is in force. Paul moves an accepted item into rulings.md (with an ID) and marks it here as MOVED → CM-###.

Format:

```
## L-### · YYYY-MM-DD · <short title> · PROPOSED | MOVED → <ID> | REJECTED
Rule affected: <BB-### / CM-### / RULE-### / script / agent>
What we do now:
What we propose:
Why (evidence):
Proposed by:
```

---

## L-001 · 2026-10-02 · Destructive decisions without Search Console · MOVED → CM-019
Rule affected: CM-001, GOV-06 §3 / T1, Agency Profile §3.

## L-002 · 2026-10-02 · "The Best" becomes a tested opener · MOVED → CM-020
Rule affected: BB-305, CM-002. The starting thresholds now live in CM-020.

## L-003 · 2026-10-02 · DataforSEO ranking overlap counts as observed blog conflict · MOVED → CM-021
Rule affected: BB-701, CM-007, RULE-015; bb-blog-analysis `serp_overlap`.

## L-004 · 2026-10-02 · Crawler changed to DataforSEO OnPage · MOVED → agency-profile.md §1
A tool-stack fact, not a rule.

## L-005 · 2026-10-02 · Linkdominator tag LD → LNKD · MOVED → naming-convention.md
A naming fact, not a rule.

## L-006 · 2026-10-05 · Page spec additions from the Semantic Mastery Content Pipeline Suite · MOVED → CM-046, CM-047, CM-048, CM-049 (approved by Paul 2026-10-05 as proposed; applied to the specs and the self-critique checks)
Rule affected: `methodology/specs/README.md` (common checks COM-11, COM-12), `methodology/writing-commercial.md` (A1, C5, C7-wording, E7, new E10), `methodology/writing-blog.md` (new E10), `methodology/specs/service.md` / `location.md` / `county-hub.md` / `homepage.md` (E7 reference). Source: Semantic Mastery Content Pipeline Suite (content-pipeline-pages references: title-h1, reading-level, faqs, matrix-terms). Nothing below is applied.

**P1 · H1 restate test → new common check COM-11** (service, location, county hub, homepage; fails as Medium, same family as SVC-08)
What we do now: BB-304 / SVC-08 say the H1 uses "a different variant of every title entity", checked by eye.
What we propose: *Strip the brand, and the area entity / area variant / city, from both the SEO title and the H1 — and, when Brand Guide H2 approves it for this page, "The Best". If what is left of the H1 is the title's service or category term unchanged, or that term plus one filler word (service, services, company, experts, pros, specialists, solutions, near me, for, local), the H1 fails: rewrite it with a different service variant from C1 (BB-304).* Added to E7 in the self-critique.
Conflicts checked:
- BB-304 — none; COM-11 is a mechanical test of it.
- **BB-305 / BB-302 / CM-014 — partial conflict with the source, not adopted:** their title format `[Service] | [Company]` and their "write the H1 like an Ads headline" are not proposed. BB-305's `[Service Variant] in [Area Variant]` format stays.
- **CM-020 — conflict if adopted as written:** their test would read an approved "The Best Roof Repair in Greene County" vs title "Roof Repair - Brand" as service + filler and fail every CM-020-approved H1. Proposed fix above: strip "The Best" before comparing, so the service variant itself must differ.
- BB-315 location pages — none: the title keeps the GB category and the H1 a service variant; COM-11 makes them differ.

**P2 · Reading level 7th–8th grade → C5 + new self-critique check E10** (commercial and blog)
What we do now: C5 "short and plain", no measure.
What we propose: *All visitor-facing copy (opening, body, FAQ answers, H1, meta description, CTA) at grade 7–8; the SEO title is excluded. E10 reports the Flesch-Kincaid grade per H2 section, computed by a small script on the prose only — headings, tables, name lists (neighborhoods, Things to Do, Top Sites), the category/area entity terms and named sources (EPA, CDC) are left out of the count. Page average ≤ 8.9; any paragraph over grade 10 is listed with a split or plain-word rewrite. Then a read-aloud pass: any sentence that needs a second read is rewritten.* (`scripts/readability.py`, not built until approved.)
Conflicts checked: none with BB-305 / BB-315 or rulings. Tension noted: the source deliberately uses no formula (read-aloud only) — we propose both because you asked for a check. CM-040 health claims must name their source; the source names are excluded from the count so the rule doesn't push writers to drop them. BB-301 entity terms are excluded for the same reason.

**P3 · FAQ answers → WC-C7 wording + new common check COM-12**
What we do now: BB-316 / WC-C7 — first sentence is the complete answer (40–60 words).
What we propose: *Each FAQ answer: sentence one answers the question in plain English and stands alone. Then, where it helps, one sentence with the company and the next step. A phone number, "call us", "contact us for a quote" or "we offer this service" is never the answer. When the fact the answer needs is Unknown, teach the general point and invite a look at their case — no number, no promise, no narrating what we don't know. A cost question names what drives the cost (from Section D / the page facts), never just "free estimate, call".*
Conflicts checked:
- BB-316 — none (same rule, sharper).
- **CM-015 / E1 portability — conflict if the next-step sentence is boilerplate:** "Call Test Co today for a free inspection" after every FAQ on every page is the portable text CM-015 fails. Proposed: the next-step sentence is optional, never identical across pages, and left off purely informational answers.
- **CM-005 / COM-09 — the next step never carries a link** (no links in FAQ answers).
- BB-315 (3–4 city-unique location FAQs) — none.

**P4 · "A keyword inside a sentence is still a claim" → writing-commercial A1 + E5, writing-blog A1 + E2**
What we do now: CM-016 forbids invented facts; A5 forbids keyword repetition; nothing says a keyword phrase can itself be a claim.
What we propose: *A keyword, a PAA question or a fan-out query never brings an Unknown or Unverified fact into the copy. "24-hour water damage cleanup" in a heading or a sentence promises 24-hour service; if Section D's emergency / after-hours fact is not Known, the phrase is cut or rewritten. The invention sweep (E5) checks every keyword-bearing phrase against the evidence grid.*
Conflicts checked: none with rulings (extends CM-016). **One knock-on to rule on:** a site-plan keyword or a B2/C1 variant can itself encode a claim ("emergency …", "24 hour …", "certified …"). Proposed: the site plan flags any keyword or variant that encodes a claim, and the evidence gate lists that claim as a required fact for the page.

## L-007 · 2026-10-05 · Schema: what the Semantic Mastery Local Schema bundle does better · X1–X4 MOVED → CM-050 (keep v1.1) · item 2 crash fixes DONE 2026-10-05 · items 1–8 otherwise PROPOSED, Paul decides one by one
Rule affected: `.claude/skills/bb-schema-builder/` (scripts/build_schema.py, references/schema-rules.md, SKILL.md), `sop-source/BB-Standard-Schema-Section-v1.1.md`. Source: Semantic Mastery Local Schema bundle (Apache-2.0; knowsabout-entity-research, schema-markup-generator), published 2026-09-26. **woodlawntrees.com stays our schema reference (captured 2026-09-18).** Nothing below is applied.

What we do now: deterministic JSON-LD from one client config (BB-6xx v1.1), `--check` entry gate on 17 fields, GOV-T5 enforced in code, `pending_url_change` refusal, manual validator pass. No automated tests.

What we propose (ranked; none conflicts with v1.1 unless marked):
1. **Verify every entity over HTTP before building** — Wikidata Q-ID read from the Wikipedia page's `pageprops.wikibase_item`, Grokipedia probed, calls paced, a mismatched hit rejected; refuse to build on a mismatch. Today a mistyped Q-ID ships. (Enforces BB-606; new `--verify` in build_schema.py.)
2. **Fix two crashes in our gate** found in the comparison: `business.logo` is used by `homepage()` but not in `REQUIRED` (a config without a logo crashes with KeyError instead of being refused); an entity with no `wikidata` crashes `thing()` instead of failing the gate. Also `addressCountry` / `contactPoint.areaServed` are hard-coded "US".
3. **Post-emit scan:** fail if any JSON string contains process/tool text (`[NEED`, "TODO", "DataforSEO", "Brand Guide", placeholder brackets).
4. **areaServed hygiene:** only `City` / `Place` / `AdministrativeArea`; `addressCountry` only inside `PostalAddress`; optional Wikipedia `sameAs` on a city. Additive — woodlawn uses City + State only.
5. **`--wrap`:** also write CMS-ready `<script type="application/ld+json">` files beside the raw `.jsonld` (raw stays for the validator).
6. **Never-rules made explicit** in schema-rules.md + SKILL.md: no `aggregateRating` / `review` on the business entity (self-serving reviews; CM-027); never a Wikipedia URL as an `@id` (BB-606 says the `@id` is the Wikidata URI).
7. **Record the bundle's patterns we have no rule for** in "Not observed, still open": About (`AboutPage` + `Person`), Contact (`ContactPage`), sparse-site homepage, franchisor, multi-GBP city pages — each needs a ruling. **The sparse-site 3-node homepage conflicts with BB-601 ("exactly two nodes")**; multi-GBP city-page LocalBusiness is consistent with GOV-T5.
8. **Typed cross-page references** (`{"@type", "@id"}` instead of a bare `@id`) — a minor deviation from woodlawn; validate before adopting.

**Conflicts — PROC-01 items for Paul to rule on; NOT adopted.** The bundle is Bradley's own 2026-09-26 written guidance and contradicts our v1.1 / woodlawn reading in four places:
- **X1 `hasMap` and the Maps `sameAs` as a CID URL** (theirs) vs the `maps.app.goo.gl` share link (BB-608 v1.1, woodlawn). Their reason: share links hide the Company ID. Storing the resolved CID in the config as evidence is harmless either way.
- **X2 self-referencing `significantLink`** — theirs makes it mandatory and deliberate; v1.1 calls it "Defect 2" (a generation artifact). Woodlawn ships it.
- **X3 homepage URL excluded from `sameAs`** (theirs) vs BB-603 item 1 and woodlawn (included).
- **X4 homepage graph deployed site-wide** (theirs) vs BB-607 (business defined once, homepage only; no NAP repeated elsewhere).

Not taken, and why: `aggregateRating` from a Grok-built dossier; a dossier that overrides live data; LLM-generated JSON; their Wikipedia-URL `@id` fallback; ContentMaxima geo-trigger stops. Ours already defines the `WebSite` node theirs never defines (woodlawn's dangling `#website`), and keeps the `pending_url_change` refusal and GOV-T5-in-code they lack.
Note: `references/schema-rules.md` and `sop-source/BB-Standard-Schema-Section-v1.1.md` differ only at line 11 — changes 6 and 7 must land in both.
