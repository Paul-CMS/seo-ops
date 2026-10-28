# Bradley Rules — Index and Load Map

Source of truth: the master rulebook Claude Doc (rulings through 2026-10-27). These files are the
machine copy. If a file here and an older skill disagree, THIS FOLDER WINS. See
`../CONFLICT-PATCHES.md` for the older skill lines that must be changed.

Rule IDs are stable. Cite them in findings, briefs and handoffs (e.g. "per TTL-05").

## Load only what the step needs (saves usage)

| Step | Load these files |
|---|---|
| Agent 1 — Audit / Rehaul | core, entity-titles, architecture, index-redirects, prohibited |
| Agent 2 — Briefs and drafts | core, entity-titles, pages-homepage / pages-service / pages-location (only the page type being written), prohibited |
| Handoff build (end of Agent 2) | workflow-execution, index-redirects, `../handoff/HANDOFF-SPEC.md` |
| Novamira executor | workflow-execution only, plus `../handoff/HANDOFF-SPEC.md` |
| Implementation QA | workflow-execution only |
| Schema step | schema |
| Blog work | blog |
| Off-page (Paul only) | offpage |

## Global conventions

- Placeholders in rules are generic: [Brand], [Service], [Service variant], [Area entity], [City], [County], [Full State].
- Niche examples (garage door, gutters, California) are calibration only, never templates.
- State names are always written in full ("South Carolina", never "SC") in titles, H tags, alt text and copy.
- "Ruled" = decided by Paul. Do not re-open a ruled item inside a client session; flag it for a system session.
