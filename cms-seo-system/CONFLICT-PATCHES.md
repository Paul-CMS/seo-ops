# Conflict patches for existing skills

These lines in your existing skills contradict the ruled rulebook. Change them in a SYSTEM session
(WF-05), not inside a client session. Until patched, `rules/` wins (rules/README.md says so).

| # | File | Current text (short) | Change to |
|---|---|---|---|
| 1 | seo-technical-audit/references/analysis-rules.md (≈ line 145) | "Do not require 'the best' in a title or H1, exclude the brand from every H1, or impose a title/H1 formula as a universal rule." | "Apply the title formats TTL-01..05 and H1 rules H1-01..07 from rules/entity-titles.md. 'The Best' only per H1-04. Brand is not in the H1 (H1-03). State the tradeoff when a page can't follow them." |
| 2 | bb-blog-analysis/references/tests.md (≈ line 103) | "A low indexed-to-published ratio is not a technical problem." | "Rule out technical causes first (IDX-01: noindex, canonical, robots.txt, sitemap, status codes). If clean, a low ratio is Google judging pages redundant, low-quality or self-competing." |
| 3 | bb-schema-builder/references/schema-rules.md (≈ lines 28, 341) and assets/client-config-template.yaml (line 10) | `HomeAndConstructionBusiness` as the default subtype | "Most specific schema type matching the GBP category (SCH-04); HomeAndConstructionBusiness only for home-service clients. Final rule decided at the first schema step." |
| 4 | seo-technical-audit/SKILL.md (line 12) | "no executable redirect rules" | Keep for the audit itself. Add: "Approved redirects are written to handoff.json by Agent 2 (RDR-01/02) and executed by novamira-executor." |
| 5 | link-implementation-qa/SKILL.md (Required inputs) | requires a VA completion CSV | Add: "For handoff runs executed by Novamira, use the implementation-qa skill instead; the bundle is the spec and the server change log replaces the CSV." |
| 6 | Boss's Bradley system prompt (Claude project) | Full prompt incl. "The Best" everywhere, Things to Do/Top Sites, ", CA" alt text, HomeAndConstructionBusiness, "not a technical problem" | Replace with: "Follow the rules in rules/ (load map in rules/README.md). Niche examples are calibration only." Keep the old prompt archived, not active. |
| 7 | Agent 2 instructions (build) | ends at publish-as-drafts | Add a final step: write `[client-slug]-handoff/handoff.json` + `content/*.md` per handoff/HANDOFF-SPEC.md, run build_bundle.py, fix all ERRORs, hand HANDOFF-REVIEW.md to Paul for approval. |
