---
name: "seo-technical-audit"
description: "Run a full Stage 1 technical and local SEO audit against a client's exports, then a Stage 2 self-check and recommendation package, following the GOV-02 Audit and Recommendations SOP. Use this whenever a technical SEO audit, site audit, crawl analysis, or audit recommendation package is requested for a local-business client; when Screaming Frog, site-auditor, citation tracker, Search Console or local grid exports need analyzing into findings; when someone mentions Stage 1, Stage 2, a finding register, a URL decision map, or an evidence manifest; or when an existing audit needs a self-check pass before it goes to the client. Produces an append-only finding register, reconciled inventories, a clarification question set routed to the VA or to Paul, and a rendered recommendation package. Stops at the Stage 3 boundary and implements nothing."
---

# Technical SEO Audit — Stages 1 and 2

Implements GOV-02 Stages 1 and 2. Stage 0 is a prerequisite, not part of this skill;
Stage 3 is the hard boundary.

**This skill diagnoses and recommends. It never implements.** No schema, no drafted
titles or meta descriptions, no executable redirect rules, no content, no citation
orders, no live changes of any kind. If an output could be pasted into a CMS and
shipped, the boundary has been crossed.

## Step zero — the Agency Profile

Before anything else, read the Agency Profile supplied with the evidence (or ask for it).
It states the standing crawl configuration and tool stack, and it is what stops this skill
re-deriving the same limitations on every audit.

In seo-ops the Agency Profile is `methodology/agency-profile.md`. Current standing
configuration: **DataforSEO OnPage API crawl (basic mode, no JavaScript rendering), converted
to Screaming Frog-shaped tables by `scripts/crawl.py`; free Screaming Frog (no rendering, no
custom extraction, 500-URL cap) is the fallback.** The crawl's settings are in the
`DFS - crawl-config` file next to the exports. None of these are findings — missing
JavaScript-rendered data is never a finding. Record the configuration once in the evidence
manifest and move on.

## Read first

- `references/authority-and-classification.md` — authority hierarchy, classification,
  the publication gate, conflict records, rules in force. **Read this one first.**
- `references/evidence-intake.md` — what to load, export fingerprints, readiness check
- `references/reconciliation.md` — cross-checks and known tool defects
- `references/finding-standard.md` — the finding record, classification, severity
- `references/analysis-rules.md` — the nine categories and their constraints
- `references/gate-b-questions.md` — the clarification stop
- `references/stage-2-selfcheck.md` — fresh-session review and package

`authority-and-classification.md`, `analysis-rules.md` and `finding-standard.md` carry
the rules a model gets wrong by default. Read them before writing any finding, not after.

**Register alignment:** `findings.csv` and `url-decision-map.csv` use the exact column
names and order of the Finding Register and URL Decision Map tabs in the Source and
Control Register workbook, so rows paste straight in. Columns prefixed `ext_` are this
skill's append-only additions and are dropped when pasting.

**Document status:** only documents with status `APPROVED` or `PILOT` may be cited as
operational rule. The Governance area is flagged NEEDS REVIEW / NON-OPERATIVE — its
registers are advisory. Cite the governing SOP for the rule, the register entry as
supporting reference.

---

## Phase 0 — Load, pin, check

Load the methodology and guidelines file, the brand/truth file, the Stage 0 Client
Control Record, and the evidence folder. Record versions in `README.md`.

**If the methodology file is not found, stop.** An audit run on general SEO knowledge
looks identical to one run on the client's methodology and is not the same thing.

```bash
python3 scripts/init_audit.py <client-slug>
python3 scripts/ingest_evidence.py <evidence_dir> <audit_dir>
python3 scripts/crosscheck.py   <evidence_dir> <audit_dir>
```

Fill the manifest's `tool_settings`, `date_window`, `geography_device` and `scope_limits`
— the exports don't contain them and they decide whether findings are safe. Then run the
readiness check from `evidence-intake.md`. It halts on four fatal conditions and
otherwise records limitations and proceeds.

Read `00-crosschecks.md` before anything else. **Anything marked `CONTRADICTED` blocks
the related finding outright** — that is not advisory.

**Never report our own tool constraints as defects.** Empty rendered columns, absent H2
extraction and a ~500-URL crawl are our licence, not the site's problem. State them once in
Assumptions and Limitations. A finding that would depend on rendered output is `Needs
Evidence`.

**Verify source titles against content.** The gap-prevention control loop requires it,
and it has already failed once: three of the four Bradley transcripts in the Source
Library are misnamed. Never cite a source by filename without opening it.

## Stage 1 — Two passes

GOV-02's §1–9 is a document structure, not an execution order. Dependencies run
differently: architecture analysis built on a URL list that the technical pass is still
changing produces findings that don't reconcile at the exit gate.

**Pass 1 — Inventories.** URLs, services, locations, conversions, citations, backlinks.
Enumeration only, no findings. Freeze the URL inventory before Pass 2.

**Pass 2 — Reconcile, then analyze.** The reconciliation *is* the orphan and duplicate
analysis — crawl vs sitemap vs GSC vs analytics vs backlinks vs GBP vs citations vs CMS.
Then run the analysis categories against the frozen inventories, following
`analysis-rules.md`.

Every finding is a row in `findings.csv` with all fields populated. **Never write a
finding without an evidence locator** — refuse, don't warn. That single control is what
makes the register worth reviewing.

Every finding carries a `Classification`. Check the **publication gate** on every
destructive or spend recommendation: a Working Hypothesis may appear when labelled and
paired with a validation method, but may not independently authorize deletion,
consolidation, URL change, GBP change, citation spend, migration or automation. Record
the check in `ext_publication_gate`.

Conflicts between sources go in `conflicts.csv` — recorded, not resolved inside the
audit, and never averaged. Follow the current production rule and send the proposed
ruling to Paul.

Append-only: a correction is a new row that supersedes, never an edit in place.

### Stage 1 exit gate

- Every category complete, or `N/A` with rationale
- URL, service, location, GBP, citation, backlink, conversion inventories reconcile
- Every finding has evidence, classification, confidence, alternatives, risk,
  recommendation
- Nothing implemented, nothing purchased

## Gate B — Clarification stop

Raise a question **only** if the answer would change a finding's severity, change its
direction, or determine whether a destructive recommendation is viable. Everything else
is a row in Assumptions & Limitations, not a question.

Two routes: **VA** for evidence integrity (was rendering on, was this filtered, is this
the full set), **Paul** for scope and decisions. When Paul can't answer, he marks it
`cannot answer — client` — it moves to the Stage 3 list and the blocked findings carry
`client_confirmation_required` with confidence `Assumed`. The skill never asks the client
directly.

Eight per route, one batch, each stating the finding IDs it blocks, why the answer
changes them, a proposed default, and the consequence of that default.

**If nothing passes the trigger test, there is no gate — go straight to Stage 2.** That
is the expected outcome on clean evidence.

If answers don't come back, proceed on the defaults, log each in `decisions.md`,
downgrade the affected findings to `Assumed`, and surface every one in Assumptions &
Limitations.

## Stage 2 — Self-check and package

**Run in a fresh session.** Load the register, inventories, manifest, cross-checks,
decisions, answers, methodology and Stage 0 record. Do **not** load the Stage 1
conversation or any narrative it wrote about its own reasoning — that re-imports the
reasoning the review exists to challenge.

GOV-02 requires an independent reviewer. Claude doing both roles is a **Paul Exception
and must be logged in `decisions.md` on every audit.** The fresh session is a
mitigation, not an equivalent.

For each Critical and High finding: re-derive from the evidence, state the strongest case
that it's wrong, then run the challenge list in `stage-2-selfcheck.md`. Confirm, revise
by superseding row, or withdraw.

Then render the package: executive summary, prioritized register, URL decision map,
measurement plan, assumptions and limitations, change preview, Stage 3
client-confirmation list.

## Working record

```
audits/<client>/<date>/
  README.md              state: stage, versions loaded, blocked on, handoffs
  decisions.md           append-only: exceptions, defaults, N/As, deviations
  00-manifest.csv        evidence manifest
  00-crosschecks.md      cross-check results
  00-unrecognised.md     exports that couldn't be fingerprinted
  inventories/*.csv
  findings.csv           append-only, one row per finding revision
  url-decision-map.csv
  questions/questions.csv
  deliverables/          rendered per stage exit
```

CSV for registers because they get sorted, filtered and handed to people without Claude.
Markdown for state and decisions because they're read, not queried.

**Deliverables are rendered, never edited.** To change a recommendation, change the
finding row and re-render. Editing a deliverable directly makes the record and the
deliverable diverge, and reproducibility is the property the whole SOP rests on.

`decisions.md` is the traceability spine — every Paul Exception, applied default,
`N/A` rationale and deviation, timestamped, with affected finding IDs. Append-only,
never summarized. It maps to the DEC register.

## Stop conditions

Stop and escalate when:
- identity, ownership, address, eligibility, legal claim, revenue dependency, access
  authority or data provenance is disputed
- evidence required for a destructive recommendation is unavailable
- a requested action crosses from analysis into implementation
- platform policy may control and current official guidance hasn't been checked
- regulated content lacks a qualified reviewer
- spend, subscription, external submission or vendor commitment lacks approval

## Known open items

These are gaps in GOV-02 v0.9 that this skill works around. Each needs ratifying into
the RULE or DEC register before v1.0:

- **Severity definitions** are proposed in `finding-standard.md`, not ratified. The
  workbook's Finding Register uses `Priority`, not `Severity`; the proposal maps to it.
- **RULE-013 is missing** from the Rule Register while GOV-02 cites RULE-001–013. Do not
  infer its content.
- **Independent review** is performed by Claude — a departure from RULE-011, recorded as
  an explicit exception on every audit
- **Phase 0 readiness check** is an addition to GOV-02, not in the source SOP
- **Two-pass Stage 1 ordering** deviates from the §1–9 document order
