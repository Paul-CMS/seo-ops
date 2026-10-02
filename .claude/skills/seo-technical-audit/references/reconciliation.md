# Reconciliation and Cross-Checks

Run before analysis, not after. The purpose is to find out which evidence can be trusted
for what, so that eighty findings are not written on a defective export.

## Why this exists

An audit tool's issue list is evidence of **what the tool concluded**. It is not evidence
of the condition. Tools are wrong in structured, repeatable ways, and their own companion
exports frequently disprove them. Promoting tool output to findings in bulk is the fastest
route to putting a false claim in front of a client.

`scripts/crosscheck.py` automates the checks below and writes `00-crosschecks.md`.
Anything it marks `CONTRADICTED` blocks the related finding outright.

## URL normalization

Every cross-source comparison normalizes first: strip protocol, strip `www.`, strip the
fragment, strip the trailing slash, lowercase. This is not cosmetic — skipping it is the
cause of the most common false positive in the whole workflow.

Keep the raw URL alongside the normalized key. The raw form is what goes in a finding;
the key is only for matching.

## The checks

### Orphan claims
Compare the tool's orphan list against a link-level export (anchor text, all inlinks)
with normalization applied. Any flagged orphan that appears as a link target is a false
positive.

**This has been observed in the wild at 100% false-positive rate.** In one Mr. Pest
Control export, all 39 pages flagged "No internal links pointing to this page" had
inbound links in the same tool's anchor-text export — one of them with 145. The tool
crawled pages under `www.` and recorded link targets under the apex domain, so nothing
matched. Every "orphan" finding from that export would have been wrong.

If no link-level export exists, orphan status is `LIMITATION`, not a finding.

### Host consistency
If both apex and `www.` forms appear across exports, two things follow: every comparison
must normalize, and the host split itself is a canonical/redirect question to verify
against live response codes. Do not assume which is canonical from the export.

### Crawl coverage
The overview's page count against the page export's row count. A mismatch means neither
can be used as a denominator until reconciled. Percentages computed on an unreconciled
denominator are wrong in a way nobody notices.

### Rendering
If the rendered columns are systematically empty, that is **our standing configuration** —
Screaming Frog free licence, no JavaScript rendering. Per the Agency Profile this is not a
gap, not a defect, and not a finding.

The conclusion is "JS dependency unknown", never "content disappears on render". Findings
that would rest on what Google renders are marked `Needs Evidence`.

**Do not request a re-crawl with rendering enabled.** The licence does not support it, and
asking for it every audit is the kind of repetition the Agency Profile exists to stop.

### Crawl truncation
The free licence caps the crawl at 500 URLs. A crawl returning ~500 is partial by
definition. Never use that count as a denominator, and never treat absence from the export
as evidence a URL does not exist — that is the orphan trap in a different costume.
Reconcile against the sitemap and CMS export to size the gap.

### Tool issue lists
Count them, then treat every one as unverified. Each that becomes a finding needs an
independent corroborating source. None may be promoted in bulk.

### Inventory reconciliation
CMS export vs crawl, in both directions. URLs in the CMS but not crawled, and crawled
but not in the CMS. These are orphan **candidates** — resolve against sitemaps, Search
Console, analytics, backlinks, GBP destinations, citations and paid landing pages before
any is called an orphan.

### Citation NAP
Tracker discrepancies are measured against the tracker's stored NAP. Reconcile against
the Stage 0 record first — the tracker may be comparing to a stale or wrong value, in
which case the "discrepancy" is in the tracker.

## Inventories to build

Before analysis, and from reconciled sources:

| Inventory | Key | Built from |
|---|---|---|
| URLs | normalized key | crawl + CMS + sitemap + GSC + analytics |
| Services | service ID from Stage 0 | Stage 0 record, mapped to URLs |
| Locations | location ID from Stage 0 | Stage 0 record, mapped to URLs and GBP |
| Conversions | event/goal | analytics, call tracking, CRM |
| Citations | domain | citation tracker |
| Backlinks | referring domain | backlink export |

The URL inventory is built first and frozen before the architecture work in §5 begins.
Analyzing architecture against a URL list that the technical pass is still changing
produces findings that do not reconcile at the exit gate.

## Recording a tool defect

A tool defect is not a site finding. It goes in `decisions.md` as a limitation, with the
affected checks named, and into Assumptions & Limitations in the Stage 2 package. If the
defect makes a required category unassessable, that category is `N/A` with rationale —
which the Stage 1 exit gate requires anyway.
