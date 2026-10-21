# Stage 2 — Discovery

_Stage file (rewrite 2 P12). Loaded by this stage's command and agents; `run.py start` prints it with the read list. The core rules are in CLAUDE.md; gates, Drive, money and files in docs/reference.md._

Session model: Haiku · agents: discovery-audit (Opus).

| Step | Command | Ends at |
|---|---|---|
| Discovery + entity research (S02–S03), public sources, **Decision Sheet** | `/discovery` | — |
| Proof sheet (S04) — Markdown + the client Google Doc (HTML) — or the client's direct answers | `/discovery proof-sheet` \| `facts-direct` | **Approval 1**: `/approve <slug> entity_approved proof_sheet_approved` |

- Approval 1 settles every Decision Sheet answer for good. Paul sends the sheet; nothing goes to a client automatically.
- Every fact found goes into `facts.json` with its source (`run.py fact`); public facts are looked up, never asked (P6).
- Discovery is not the audit: no severity, priorities or recommendations yet — observations and questions only.

## The agent's procedure (Phase 7: moved here from `.claude/agents/discovery-audit.md`)

**discovery** (S01–S03) — public sources only; the crawl comes later.
- S01 intake facts from status.json (ask Paul for anything missing).
- S02 live site, GBP, social and review profiles, Secretary of State, licence board
  (`.claude/skills/client-intake/references/discovery.md`: source hierarchy and confidence). Sources the system cannot
  read (CAPTCHA-gated searches; the GBP dashboard — secondary categories, service-area list, open date) go to Gwen in
  **one** handoff: `handoff.py create <slug> --run <RUN_ID> --kind manual_lookup --items <csv>` (one row per lookup:
  search page URL, what to record, why). She saves `MANUAL` evidence; until then those fields keep the public copies'
  confidence (never verified).
- S03 entity foundation (BB-105–BB-110): category entity = GBP primary category verified on Wikipedia; area entity by
  the Russian Doll method with the path recorded; real candidate variants; proposed reserved homepage variant; Wikidata
  URIs for category, area, county, state.
- Conflicts: record every candidate value, never resolve one (PROC-01). Quote every public claim verbatim with its URL.
- Write the Discovery Record (`- REVIEW.md`) and Brand Guide A/B as proposals; `drive.py upload` the Record.
- **Decision Sheet** (`templates/decision-sheet.md` → `clients/<slug>/discovery/<Client> - Decision Sheet - REVIEW.md`):
  every identity and format decision together, each with a recommended default and its evidence; Paul answers only
  where he disagrees; the audit and Build apply them and never re-ask.
- Record S01–S03, then `status.py mark <slug> entity_record --file <Decision Sheet> --file <Discovery Record> --file
  clients/<slug>/brand-guide.md#A+B1+B2`. **Do not stop** — the proof sheet follows and both go to Approval 1.

**proof-sheet** (S04) — `templates/proof-sheet.md` + `client-intake/references/field-schema.md`: Access (add us as a
GBP Manager), Block A confirm, Block B verify (quoted, never guessed), Block C needs, return-by date, default. Nothing the
Decision Sheet settled. Save the `.md`; the `- CLIENT COPY` Google Doc goes through the connector as **HTML** (the only
connector upload). **Never contact the client.** Record S04; `status.py mark <slug> proof_sheet --file <sheet .md>`.
**Stop** for Approval 1.

**facts-direct** (S04) — the client answered without a sheet: save the answers **verbatim, at once** as MANUAL evidence
(`<Client> - MANUAL - client-answers - <date>.md`, `drive.py upload`), then `status.py mark <slug> facts_direct --file
<it>` and `status.py mark <slug> proof_sheet --file <it>`. Approval 1 approves them as the client facts and meets
"facts returned". Later informal answers: saved verbatim the same way, `status.py mark <slug> facts_direct`.
