---
description: Start a new client (full or blog-only), or import an in-progress client from Drive
argument-hint: "<Client Name>" <domain> --industry <trade> [--blog-only] [--route A|B] | --import "<Client Name>"
---

Arguments: $ARGUMENTS

Follow CLAUDE.md. Plain language with Paul throughout.

## New client
1. Work out the slug (lowercase, hyphens: "Red Rover Roofing" → `red-rover-roofing`) and type
   (`--blog-only` → blog-only, else full). Industry decides sensitivity (chiropractic, medical,
   insurance, legal, financial).
2. `python3 scripts/status.py init <slug> --name "<Client Name>" --domain <domain> --type <type> --industry <industry> [--route A|B]`
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
8. Tell Paul the next command: `/crawl <slug>` (full) or `/blog <slug> intake` (blog-only).

## Import (A-1 Pool Service, Red Rover Roofing, any client already mid-stream)
1. Find `<Client Name> - TMS` in v3. Read its Approval Record, Handoff Log, Brand Guide and
   Document Checklist, and list every file (read-only).
2. `status.py init` as above, then start a run.
3. Write `clients/<slug>/import-proposal.json`: `{"gates": {gate: {"state": ..., "source": "<file + block>", "note": ...}}, "pages": {...}}`
   mapping each **signed** Drive block to its gate (Block 1 signed → b1_* and block1;
   anything unsigned stays pending). Pages: one entry per service/location page in the
   Decision Map with its state (brief written, draft approved, live) as the Drive files show.
4. Copy the Brand Guide into `clients/<slug>/brand-guide.md`; start `handoff-log.md` with an
   "Imported" section.
5. **Rename list:** run `scripts/naming.py rename-list` on every Drive file name (also old
   evidence tagged `LD` → `LNKD`). Save `clients/<slug>/rename-list.md`. Nothing is renamed.
6. Show Paul the proposal in plain language (what each gate will say and why) and the rename
   list. He confirms with `/approve <slug> import`.
7. Finish the run. Next: `/resume <slug>`.
