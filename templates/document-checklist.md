# [Client Name] - Document Checklist
### The Discovery & Audit agent's first action. Each tier names what it blocks.

## TIER 1 — Blocks the audit

| [ ] | Item | File name | Source |
|---|---|---|---|
| [ ] | Website URL | — | Paul |
| [ ] | GBP link, and storefront or SAB | — | Paul |
| [ ] | **The exact URL in the GBP Website field** | — | Paul |
| [ ] | DataforSEO crawl (`/crawl`) | `[Client] - DFS - internal_all - [date].csv` + 12 more | System |
| [ ] | BrightLocal citation tracker | `[Client] - BL - citation-tracker - [date].csv` | Gwen |
| [ ] | Sitemap URL list | `[Client] - MANUAL - sitemap - [date].csv` (or from the crawl) | System |

Rendering: basic-mode crawl, no JavaScript. Standing setup, not a gap, never a finding.

## TIER 2 — Strengthens severity and destructive decisions (optional; usually unavailable)

| [ ] | Item | File name | Source |
|---|---|---|---|
| [ ] | Search Console — queries, 12 months | `[Client] - GSC - queries - [date].csv` | Client access |
| [ ] | Search Console — pages, 12 months | `[Client] - GSC - pages - [date].csv` | Client access |
| [ ] | GA4 — conversions by landing page | `[Client] - GA4 - conversions - [date].csv` | Client access |
| [ ] | DataforSEO ranked keywords per URL | `[Client] - DFS - ranked-keywords - [date].csv` | System |
| [ ] | DataforSEO referring domains per URL | `[Client] - DFS - backlinks - [date].csv` | System |
| [ ] | Local grid runs (BrightLocal; DataforSEO alongside on the pilot client) | `[Client] - BL - local-grid - [date].csv` | Gwen |

Without GSC, destructive candidates follow CM-019 (all four conditions) or park at `Needs Evidence`.

## TIER 3 — Blocks content writing

| [ ] | Item | Where it lands |
|---|---|---|
| [ ] | Client proof sheet returned | Brand Guide A, D |
| [ ] | **Entity foundation approved by Paul** | Brand Guide A, B |
| [ ] | Licence numbers, insurance, certifications | D |
| [ ] | Warranty, guarantees, financing terms | D |
| [ ] | Named staff for on-page use | D |
| [ ] | Licensed practitioner named *(medical / chiropractic)* | D |
| [ ] | Expertise capture or interview notes | Briefs |
| [ ] | Customer language — call notes, reviews, chat logs | I |
| [ ] | CMS access (WordPress Application Password in .env, typed by Paul) | Implementation |

## TIER 4 — Blocks schema

| [ ] | Item | Where it lands |
|---|---|---|
| [ ] | ID page URL, or confirmation none exists | F |
| [ ] | Full current citation list | F |
| [ ] | Social profile list | F |
| [ ] | Google Maps share link · Apple Maps link | F |
| [ ] | Logo files with pixel dimensions · owner name and photo | F |
| [ ] | Wikidata URIs — category, area, county, state | F |

## TIER 5 — Blocks blog analysis

| [ ] | Item | File name |
|---|---|---|
| [ ] | Blog post list — URL, title, word count, category, modified | `[Client] - CMS - blog-inventory - [date].csv` |
| [ ] | GSC for blog URLs, or DataforSEO ranking overlap | Tier 2 / `[Client] - DFS - blog-serp-overlap - [date].csv` |

## Outstanding

| Item | Owner | Chased on | Notes |
|---|---|---|---|
