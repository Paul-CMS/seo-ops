# Stage 4 — Audit

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md. The slim audit: CM-063 (Rewrite 4 Phase 3)._

Session model: Haiku · agents: discovery-audit (Opus), audit-reviewer (Opus) — the mechanical steps are scripts.

| Step | Command | Ends at |
|---|---|---|
| Audit (page specs approved once, globally): screen → entity → URL decisions → triage → technical → fresh-context review → the one review sheet (S12–S18) | `/discovery audit` | — |
| Paul answers the audit review sheet | `/discovery review "accept all"` | **Approval 2a**: `/approve <slug> audit_approved` — safe fixes and the blocker handoff start (D3) |
| The client's facts recorded and reconciled into the Brand Guide | `/discovery sheet-returned`, `reconcile` | **Approval 2b**: `/approve <slug> brand_guide_approved` → **discovery_signed_off** |

- **S12 is a script:** `python3 scripts/pipeline.py <slug> inventory --run <RUN_ID> --phase audit` (ingest, cross-checks,
  auto conformance, the **redirect screen** `pagedec.py screen`, the Evidence Manifest).
- **The screen decides CM-019 C1–C3** for every URL (rankings, backlinks, GSC/GA4, GBP website, citations): pass / fail /
  needs evidence. The agent decides only the `needs evidence` rows and entity mismatches; `pagedec.py screen <slug>
  --check` refuses a destructive row on a failing URL.
- **S15 is triage:** `conformance.py judge` (the API scores pages Build will not rewrite), then `conformance.py triage`
  writes rebuild / light fix / keep into the URL Decision Map. No scorecard files.
- **Severity is CM-061's:** Fix (→ the Technical Blocker Checklist, rendered at the audit by `render.py blockers`) ·
  Fix and list · Ask (four kinds; URL decisions become kind-1 Asks by themselves).
- **S17:** `review.py scope <slug> audit` lists the reviewer's rows (every destructive URL row, every Ask, a sample); the
  reviewer reads the registers only (CM-018; CM-026 standing).
- **S18:** `review.py sheet <slug> audit --run <RUN_ID>` → `audit-review.csv` + `client-questions.csv` (the only thing the
  client ever sees; Paul sends it), then `render.py all <slug> --run <RUN_ID>`. Deliverables: the registers (CSV), the
  audit review sheet and the Evidence Manifest — no Recommendations document, no Markdown Finding Register.
- `/discovery review` applies Paul's answer line (`review.py apply <slug> audit`); `audit_approved` is refused until it is
  applied. Audits approved before CM-063 (Home Mobile Medical, Apex) keep their documents and approvals.
- Conflicts are recorded per PROC-01 (`conflicts.csv`) and become kind-4 Asks, never resolved inside the work.

## The agent's procedure (Phase 7: moved here from `.claude/agents/discovery-audit.md`)

**audit** (S12–S18) — the crawl (S05) and data steps have outcomes. Follow the **seo-technical-audit** skill (`SKILL.md`,
`finding-standard.md`, `analysis-rules.md` — nothing else from it).
1. S12: the `pipeline.py … --phase audit` run above (it keeps the manifest's setting columns already written). Read
   `00-crosschecks.md` (CONTRADICTED blocks the related finding), `redirect-screen.md`, `crawl-summary.csv` and
   `page-text.csv` — never the raw crawl tables.
2. S13 **entity** — the site against the Brand Guide: semantic triple, NAP, brand search, supporting assets.
3. S14 **URL Decision Map** — every page typed and decided; you decide only `needs evidence` rows and entity mismatches
   (another area, a discontinued service, a duplicate entity). `pagedec.py screen <slug> --check` must pass.
4. S15 **triage** — `conformance.py judge <slug> --run <RUN_ID>` (with "no API key" you score that set's judgment checks
   into `audit/conformance-judgment.csv`), then `conformance.py triage <slug> --run <RUN_ID>`. A `light fix` page's failed
   checks are findings (one per check, every page listed).
5. S16 **technical** findings; `render.py blockers <slug> --run <RUN_ID>`.

Findings follow `finding-standard.md`: one per issue, every affected URL, an evidence locator or no finding. A client fact
is a kind-3 Ask with its `ext_searched` line (`questions.py`); a public fact goes to the researcher. Never a finding: a
missing "The Best" (CM-020), missing JavaScript-rendered data. The homepage H1 lock (HP-08) lifts only under CM-059:
`h1lock.py check <slug> --keyword "<main keyword>" --hp06 fail [--gsc <export>]`, its table a kind-1 Ask (default: no
change). Refuse your own output if a finding lacks a locator or the map has fewer rows than the site has pages. The
command then runs the **audit-reviewer** (S17). S18: `review.py sheet`, `render.py all`, then
`status.py mark <slug> audit_deliverables --file <audit-review.csv> --file <findings.csv> --file <url-decision-map.csv>
--file <Audit Review Sheet .md> --file <Evidence Manifest .md>` and `status.py mark <slug> blocker_checklist --file
<Technical Blocker Checklist .md>`.

**review** — `review.py apply <slug> audit --run <RUN_ID> --answers "<Paul's line>"`; a decided URL row gets its
superseding map row; the client's questions wait for the client. Then Paul: `/approve <slug> audit_approved`.

**reconcile** — parse the return (`client-intake/references/proof-sheet.md` §6): `Client Confirmed` + date, keep `was:`
values, complete the Brand Guide (Unknown/Disputed stay so), D2 unsupported claims, the D3 content-risk list. A status
change never voids the entity approval; a changed **value** in A/B1/B2 does — only when the client corrected an entity
fact, as one `--reopen <key>`, never a new question. The owner on the returned sheet is the author (CM-039) unless the
Decision Sheet settled it. `status.py mark <slug> reconciled --file clients/<slug>/brand-guide.md#A+D+E+G` (not B3/C,
which Build writes back to, nor F, completed at the handoff). Paul: Approval 2b. Discovery is then signed off
automatically (a condition). **The agent never starts Build.**
