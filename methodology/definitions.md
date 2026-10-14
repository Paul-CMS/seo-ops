# Definitions (CM-061)

**Binding.** Every agent file, command, doc and CLAUDE.md points here instead of restating these terms. A change to a
definition is a ruling (PROC-01), made in a system session.

| Term | Definition |
|---|---|
| **Client fact** | Something true about the client: services, practices, people, warranties, prices, licences, areas, history. |
| **Public fact** | Something true about a place, a rule, the trade or a product, independent of the client: permits, codes, flood rules, HOA/ARB regimes, neighbourhoods, landmarks, manufacturer specs. |
| **Place fact** | A public fact about a place with no niche (identity, neighbourhoods, landmarks). Stored in the place layer: `methodology/places/<state>/<place>/place.json`. |
| **Place × niche fact** | A public fact about how the client's niche is affected in a place (permits for that work, HOA rules for it, conditions that affect it). Stored in the niche layer: `methodology/places/<state>/<place>/<niche>.json`. |
| **Source** | A document the system can open again: a file in `clients/<slug>/` (data, discovery, inputs, interview transcripts), a client web page, the GBP profile, or a public URL. A chat answer from Paul is recorded as a source of type `paul` via `run.py fact`. |
| **Official source** | A government body's own site (town, city, county, state, federal agency), a manufacturer's own site, or a licensing board's lookup. Listed per area in `methodology/sources/`. |
| **Context source** | A non-official source allowed for area character only (chamber of commerce, tourism board, Wikipedia for places). Never for rules, codes, permits or claims. |
| **Evidence pack** | The per-page file of every source excerpt relevant to that page: `build/<section>/packs/<page-id>.md`, built by `scripts/evidence_pack.py` before any brief. The only place writers look for facts. |
| **Review mention** | One review's text supporting a fact. **Independent** means different reviewers. The same reviewer twice, or an owner reply, does not count. |
| **Fact status** (in `facts.json`) | `client_confirmed` · `paul_approved` · `internally_verified` (an official source confirms it) · `customer_reported` (reviews) · `site_stated` (client's own site or GBP) · `submitted` · `unknown` · `disputed`. |
| **Usage tier** | How a fact may be written on a page (`methodology/writing-commercial.md`, "Usage tiers"). |
| **Known** (evidence gate) | `client_confirmed`, `paul_approved` or `internally_verified`; or `customer_reported` with **3 or more independent mentions** checked by meaning (CM-057). |
| **Searched** | A research-log entry (`build/<section>/research-log.csv`, `scripts/research.py`) showing the queries and sources tried. "Not found" is only valid with one that meets the minimum. |
| **Finding** | One rule-check result for one page and one item, keyed `page + rule + item`. |
| **Severity** | **Fix** (form only: length within ±25% of a target, wording, order, formatting, reading grade, links, variant repetition, heading case — fixed silently, logged in the run) · **Fix and list** (content changed by default: an optional section shortened or dropped, an FAQ swapped for its fallback, a claim softened to its usage tier, pack evidence added, a `site_stated` claim used — applied, listed under "Decided for you", anyone can override) · **Ask** (only the four kinds below). Rules in `methodology/review-severities.json`. |
| **Default** | The option the system recommends for a finding. It is applied unless someone overrides it. |
| **Ask** | A question that needs Paul. Only four kinds: 1 page or URL decisions (create, merge, drop, redirect) · 2 legal or money claims about the client (warranties, prices, financing, licences, insurance, permits the client pulls, guarantees) · 3 client-only facts not found after research, batched into one pre-filled client list per section · 4 real conflicts between sources of equal standing. A question already answered in `facts.json` or `decisions-settled.md` never appears. |
| **Section** | One page kind built together: services, locations (with hubs), homepage and core pages, additional pages. In status.json a section is a batch. |
| **Step** | Briefs, brief review, drafts, draft review, ship. |
| **Review sheet** | The one file per section per step that holds every Fix-and-list and Ask row: `build/<section>/<step>-review.csv`, copied to Drive. |
| **Overdue Ask** | An Ask row unanswered for 3 working days (`config.json` → `overdue_ask_working_days`). Kinds 1, 3, 4 ship with the default; kind 2 is left out of the page until answered. |

## Search order for a client fact (CM-061 part 2)
`facts.json` → `decisions-settled.md` → evidence pack (reviews, site, GBP, interview transcripts) → proof sheet and
Discovery Record. Only then — with a research-log entry — may it become an Ask (kind 3).

## Read lists never limit research
"Your read list limits which project files you load. It never limits web research for public facts. Follow Paul's
instructions as written, never narrower."
