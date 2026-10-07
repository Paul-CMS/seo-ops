# AGENCY PROFILE — seo-ops
### Standing facts. Every agent reads this first and never re-asks what it answers.
**Owner:** Paul · **Updated:** 2026-10-02 · Based on the Drive v3 `Resources/AGENCY-PROFILE.md`
(24 Sept 2026) plus Paul's 2 Oct rulings. Claude Code is the only tool.

---

## 1 · Tool stack

| Purpose | Tool | Notes |
|---|---|---|
| Site crawl | **DataforSEO OnPage API, basic mode** via `/crawl` | Fallback: Screaming Frog free licence |
| Citations | **BrightLocal** citation tracker | VA uploads the CSV. Stays |
| Local grid | **BrightLocal** or **Local Dominator** (scan PDFs; results only, never its advice) | DataforSEO grid runs alongside on ONE client first; Paul compares before BrightLocal's grid role is dropped |
| Backlinks | **DataforSEO** Backlinks API | |
| Keyword volume, rankings, SERPs | **DataforSEO** | All calls through `scripts/dfs.py` |
| Search Console / GA4 | Client-dependent | **Usually unavailable.** Optional evidence |
| CMS | WordPress · **SEOPress** (full) · **Kadence** | Changes via `scripts/wp.py` after the pilot |
| Site management | ManageWP | Backups. A fresh backup is confirmed by Paul before any `--live` change |

We do not use Sitebulb.

## 2 · Crawl constraints — read before writing any finding

Basic-mode DataforSEO does **not render JavaScript**. Rendered-HTML data is absent by
configuration. **Missing JavaScript-rendered data is never a finding.** State the crawl
configuration once (the `DFS - crawl-config` file) in the evidence manifest and move on.
A JavaScript-mode crawl costs 10× and is Paul's call.

Unlike the Screaming Frog free licence, the DataforSEO crawl has no 500-URL cap and gives the
full H2 list per page.

## 3 · When Search Console and analytics are missing (the normal case)

- The audit still runs. Technical, structural and entity findings are unaffected.
- Severity cannot rest on business consequence; say what is missing, once.
- **Destructive recommendations rest on our own local search research** (Paul ruling,
  CM-019). A page is a removal / consolidation / redirect / noindex candidate only when
  **all four** hold, otherwise it is `Needs Evidence`:
  1. DataforSEO shows no ranking keywords in the top 100 for the URL
  2. DataforSEO shows no referring domains to the URL
  3. It is not a GBP or citation destination
  4. The client confirms no leads from it
- Blog redirects need observed conflict: GSC, **or** DataforSEO showing both URLs ranking for
  the same query (CM-021).

## 4 · Who decides what

| Decision | Owner |
|---|---|
| Area entity, category entity, variant list | **Paul** — nobody else, ever |
| Anything destructive (remove, merge, redirect, noindex) | **Paul** |
| Any spend (citations, links, press releases, subscriptions, DataforSEO calls over $2) | **Paul** |
| Scope: services, markets, whether the blog is in | **Paul** |
| Every gate | **Paul**, by typing `/approve` |
| Business facts (hours, licences, service area, claims) | **The client**, via the proof sheet |
| Health claims on medical / chiropractic sites | The client's **licensed practitioner** signs off |
| Everything else | The system, or the VA following a handoff |

Client confirmation establishes truth; Paul's approval authorizes action. Separate gates.
(RULE-010)

## 5 · Drive

Master folder **`v3. CMS Technical SEO Audit 2026`** (id in `config.json`). One folder per
client at its root: **`[Client Name] - TMS`**, created by copying
`_CLIENT FOLDER TEMPLATE - copy per client` (also at the root). Audits reference only that
folder. The old v1/v2 trees are ignored.

```
[Client Name] - TMS/
├── [Client] - Brand Guide.md          living records, no status
├── [Client] - Approval Record.md      mirrored from status.json by /approve
├── [Client] - Document Checklist.md
├── [Client] - Handoff Log.md
├── 01 - Discovery and Audit/{Evidence, Deliverables}
├── 02 - Build/
├── 03 - Finish/
├── 04 - Blog/
└── _Archive/
```

Folder names use "and", never "&". Drive upload conversion must be off; the system writes
real `.md` files. The one deliberate exception is the client-facing proof sheet copy (a
Google Doc), which has its own distinct name.

## 6 · File naming — `methodology/naming-convention.md`

## 7 · The team

| Person | Role | Gets handoffs for |
|---|---|---|
| Paul | Decisions, entity approval, every gate, all destructive and spend calls, sends everything to clients | — |
| Jonie | Website and technical implementation | Redirects, slugs, titles/meta (until the WordPress pilot), robots, sitemap, speed, image URLs |
| Gwen | SEO lead, VA execution | Evidence uploads, citations, content tasks, everything else |

VAs work without Claude access. A handoff must stand on its own.

## 8 · Standing output rules

- Markdown is the working format. The client proof sheet also gets a Google Doc copy.
- Cite rules by ID (`BB-304`, `CM-015`). Never restate a rule as if it were ours to invent.
- State a limitation once, in the right section.
- Nothing goes to a client automatically. Paul sends.
