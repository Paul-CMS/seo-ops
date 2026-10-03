---
description: Start a new client (full or blog-only), or import an in-progress client from Drive
argument-hint: "<Client Name>" <domain> --industry <trade> [--blog-only] [--route A|B] | --import "<Client Name>"
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. Plain language with Paul throughout.

## New client
1. Work out the slug (lowercase, hyphens: "Red Rover Roofing" → `red-rover-roofing`) and type
   (`--blog-only` → blog-only, else full).
2. Sensitive industry (CM-025) is matched by category: `python3 scripts/status.py classify "<industry>"`.
   `yes`/`no` → use it. `unsure` (exit 9) → **ask Paul** whether it is sensitive and, if health,
   whether health claims need a practitioner's sign-off; pass his answer as `--sensitive yes|no
   [--practitioner yes|no]`. Paul can always override with `--sensitive`.
   `python3 scripts/status.py init <slug> --name "<Client Name>" --domain <domain> --type <type> --industry <industry> [--sensitive yes|no] [--route A|B]`
3. `python3 scripts/run.py start <slug> new-client` → note the RUN_ID it prints and pass it literally to every later step (shell variables do not persist between commands) — every step below is a logged change.
4. **Drive folder:** check whether `<Client Name> - TMS` already exists at the root of
   `v3. CMS Technical SEO Audit 2026` (ids in config.json). If not, create it as a copy of
   `_CLIENT FOLDER TEMPLATE - copy per client`: the folders `01 - Discovery and Audit/{Evidence,
   Deliverables}`, `02 - Build`, `03 - Finish`, `04 - Blog`, `_Archive`. If the Drive tools
   can't create folders, say so immediately and ask Paul to copy the template by hand (right
   click → Make a copy → rename → move to the root). Record the id:
   `status.py set <slug> client.drive_folder_id <id>`.
5. Living records from `templates/`: Brand Guide (`clients/<slug>/brand-guide.md`), Document
   Checklist, Handoff Log (`clients/<slug>/handoff-log.md`) — upload each as a real `.md`
   with the client name. The Approval Record is `status.py approval-record <slug>` → upload.
6. **Intake questions for Paul** (one batch): website URL, GBP link, storefront or SAB, the
   **exact URL in the GBP Website field**, WordPress env prefix (Paul adds the Application
   Password to `.env` himself — never ask for it in chat), whether GSC/GA4 access exists.
   Blog-only: services list, city list, voice guidance, customer language.
7. `run.py finish <slug> <RUN_ID> --summary "Client set up" --phase "Getting started" --next "Researching your business"`
8. Tell Paul the next command: `/next <slug>` — for a full client that runs `/discovery <slug> discovery`
   (public research and the entity foundation come before the proof sheet and the crawl); for a
   blog-only client, `/blog <slug> intake`.

## Import (A-1 Pool Service, Red Rover Roofing, any client already mid-stream)
1. Find `<Client Name> - TMS` in v3. Read its Approval Record, Handoff Log, Brand Guide and
   Document Checklist, and list every file (read-only).
2. `status.py init` as above, then start a run.
3. Write `clients/<slug>/import-proposal.json`:
   `{"source": "<Approval Record file>", "gates": {gate: {"state": "approved", "source": "<file + block>", "note": ...}},
     "pages": {page_id: {"type": "service|location|county|homepage|about|blog", "name": ..., "url": ..., "group": "<cluster or county>", "state": "live|draft_written|brief_written|planned"}},
     "pilot_done": true|false, "steps": {"S05": {"outcome": "done", "reason": "..."}}}`
   mapping each **signed** Drive block to its gate (Block 1 signed → b1_* and block1;
   anything unsigned stays pending). Pages: every service/location/county/homepage/about page
   in the Decision Map with its state as the Drive files show. **Live pages become an approved
   baseline**; the rest are planned in batches; a site plan is generated from the pages; audit
   steps are recorded as done when the audit was signed — so `/next` resumes where the client
   really is, never at `/crawl`.
4. Copy the Brand Guide into `clients/<slug>/brand-guide.md`; start `handoff-log.md` with an
   "Imported" section.
5. **Rename list:** run `scripts/naming.py rename-list` on every Drive file name (also old
   evidence tagged `LD` → `LNKD`). Save `clients/<slug>/rename-list.md`. Nothing is renamed.
6. Show Paul the proposal in plain language (what each gate will say and why) and the rename
   list. He confirms with `/approve <slug> import`.
7. Finish the run. Next: `/next <slug>` (it resumes at the client's actual stage).
