# Review — Self-Check and Recommendations

## Documented deviation from GOV-02

GOV-02 requires a reviewer other than the finding author. In this workflow Claude
performs both roles under the standing exception **CM-026**; `decisions.md` cites CM-026
rather than logging a new exception.

A same-context self-review genuinely catches less than an independent one. The
fresh-context protocol below (the `audit-reviewer` subagent) is the mitigation CM-026
requires, not an equivalent.

## The fresh session

Review runs in a **new conversation**, not by instructing the same session to set aside
what it knows.

**Load:**
- `findings.csv`
- `inventories/*.csv`
- `00-manifest.csv`
- `00-crosschecks.md`
- `decisions.md`
- `questions/*` including answers
- the methodology and brand files
- the intake record (Client Control Record)

**Do not load:**
- the Analysis conversation
- any narrative Analysis wrote explaining its own reasoning
- draft deliverables

The second list is the point. A summary explaining *why* a finding was written
re-imports exactly the reasoning the review is meant to challenge. Working from the
evidence locator and the conclusion alone forces re-derivation, which is the closest
available approximation of independence.

This only works if `findings.csv` is self-sufficient. If a finding cannot be re-derived
from its evidence locator, that is itself a Review finding: the row is inadequate and
goes back as a revision.

## Challenge protocol

For every High finding, and a representative sample of Medium and Low (scale: CM-028):

1. Open the evidence at the locator.
2. Re-derive the conclusion from the evidence alone.
3. **State the strongest case that the finding is wrong** before confirming it.
4. Check it against the fixed challenge list below.
5. Confirm, revise (append a superseding row), or withdraw.

### The challenge list

Straight from GOV-02's reviewer section:

- **Unsupported causation** — does the evidence show cause, or co-occurrence?
- **Methodology presented as platform law** — is a Bradley rule dressed as a Google
  requirement?
- **Arbitrary numeric thresholds** — where did that number come from?
- **Template absolutism** — is a house standard being applied as though universal?
- **Unverified search-volume assumptions** — is volume doing work evidence should do?
- **Missing conversion or business evidence** — is severity assigned from business
  consequence or from a tool label?
- **Implementation smuggled into a recommendation** — does it contain markup, drafted
  copy, or executable steps?

Add three specific to this stack:

- **Tool output promoted without corroboration** — check against `00-crosschecks.md`
- **A `CONTRADICTED` cross-check ignored**
- **URL comparison made without normalization**

### Destructive recommendations

Every merge, redirect, delete, noindex or canonical change must meet CM-019 (all four
conditions, else `Needs Evidence`) with the check completed in the URL Decision Map, plus a
safer alternative. Missing either, the recommendation is withdrawn, not downgraded
(CM-001). Check the publication gate (CM-009).

### Reconciliation

Totals and identifiers reconcile across every inventory. Duplicate findings merge into
one row with a superseding revision. Every category is complete or carries an explicit
`N/A` with rationale.

## The recommendation package

Rendered from the register. Never hand-edited.

**Executive summary** — verified strengths, primary constraints, overall confidence, and
the small number of highest-leverage recommendations. Strengths are not decoration; an
audit that lists only problems gets read as a sales document.

**Prioritized register** — High / Medium / Low (CM-028), each with impact,
effort, risk, dependency, evidence locator, owner placeholder.

**URL Decision Map** — Keep / Improve / Create / Merge Candidate / Redirect Candidate /
Noindex Candidate / Remove Candidate / Needs Evidence. No action status is final before
Client confirmation.

**Measurement plan** — baseline, success indicator, source, comparison window,
confounders, reassessment date. Findings whose measurement is broken must say so here.

**Assumptions and limitations** — missing access, disputed facts, sample limits,
unavailable revenue data, unresolved policy questions, tool defects, every applied
default from Gate B. This section is load-bearing. An audit that hides its limitations
is not defensible six months later.

**Change preview** — what Implementation would consider. No executable instructions.

**client-confirmation list** — every question Paul routed to the client, plus
every on-page claim found during §6 that needs substantiation.

## Boundary

Review ends at the client-confirmation boundary. Produce no schema, no drafted titles or meta
descriptions, no redirect maps as executable rules, no citation orders, no content. If a
deliverable contains something that could be pasted into a CMS and shipped,
implementation has been smuggled in and the package fails its own exit gate.
