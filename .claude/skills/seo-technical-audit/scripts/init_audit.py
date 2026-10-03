#!/usr/bin/env python3
"""
init_audit.py — scaffold the audit working folder.

    python3 init_audit.py <client-slug> [base_dir] [--date YYYY-MM-DD]

Creates the append-only working record. Registers are CSV because they get sorted,
filtered and handed to people without Claude; state and decisions are Markdown
because they are read, not queried.
"""

import csv, os, sys, datetime

# Columns 1-19 match the "Finding Register" tab of the Source and Control Register
# workbook exactly, in order, so rows paste straight in. Columns after the marker are
# this skill's append-only extensions and are dropped when pasting to the workbook.
FINDING_COLUMNS = [
    "Finding ID", "Stage", "Category", "Affected URL / Entity", "Observation",
    "Evidence / Locator", "Classification", "Confidence", "Alternative Explanation",
    "Recommendation", "Risk if Acted", "Risk if Deferred", "Dependency",
    "Client Confirmation Needed", "Paul Approval Needed", "Priority", "Status",
    "Owner", "Reviewer",
    # --- skill extensions (not in workbook) ---
    "ext_revision", "ext_supersedes", "ext_date", "ext_analyst",
    "ext_evidence_source_id", "ext_alternative_tested", "ext_publication_gate",
]

# Columns 1-17 match the workbook's "URL Decision Map" tab exactly.
URL_MAP_COLUMNS = [
    "URL ID", "Current URL", "Page Type", "Main Entity / Intent",
    "Business / Conversion Value", "Traffic / Query Evidence",
    "Lead / Revenue Evidence", "Backlink / External Dependencies",
    "Proposed Action", "Target URL", "H2 / Content Survival",
    "Redirect / Index Rule", "Risk Tier", "Client Confirmed", "Paul Decision",
    "Status", "Owner",
    # --- skill extensions (not in workbook) ---
    "ext_url_key", "ext_value_dependency_check", "ext_safer_alternative",
]

MANIFEST_COLUMNS = [
    "source_id", "file", "recognised_as", "category", "rows", "columns",
    "sha256_12", "file_modified", "tool_settings", "date_window",
    "geography_device", "scope_limits",
]

QUESTION_COLUMNS = [
    "question_id", "route", "blocks_finding_ids", "question",
    "why_it_changes_the_finding", "proposed_default",
    "consequence_of_default", "answer", "answered_by", "answered_date", "status",
]

# Conflict record fields per the Authority and Conflict Rules document.
CONFLICT_COLUMNS = [
    "conflict_id", "topic", "claim_a", "claim_a_source", "claim_a_authority_level",
    "claim_b", "claim_b_source", "claim_b_authority_level", "dates",
    "affected_stages", "real_or_conditional", "current_production_rule",
    "proposed_ruling", "evidence", "risk", "owner", "approval_status",
    "decision_date", "sops_updated",
]

README = """# Audit — {client}

**Stage:** Phase 0 — not started
**Opened:** {date}
**SOP:** GOV-02 Stages 0–3 (record the exact version you loaded)

## Loaded inputs

| Input | Location | Version / date | Loaded |
|---|---|---|---|
| Methodology & guidelines | | | ☐ |
| Brand / truth file | | | ☐ |
| Stage 0 Client Control Record | | | ☐ |
| Evidence folder | | | ☐ |

## State

| Step | Status | Date | Notes |
|---|---|---|---|
| Phase 0 — load & pin | not started | | |
| Phase 0 — readiness check | not started | | |
| Stage 1 — inventories | not started | | |
| Stage 1 — reconciliation | not started | | |
| Stage 1 — analysis | not started | | |
| Gate B — questions | not started | | |
| Stage 2 — self-check | not started | | |
| Stage 2 — package | not started | | |
| Stage 3 boundary | blocked | | Not part of this skill |

## Blocked on

_Nothing yet._

## Handoffs

_None yet._

---
Deliverables in `deliverables/` are **rendered**, never edited. To change a
recommendation, change the finding row and re-render.
"""

DECISIONS = """# Decision log — {client}

Append-only. Never edit or summarize an existing entry. Every Paul Exception,
applied default, N/A-with-rationale and deviation from GOV-02 goes here with the
finding IDs it affects.

Format:

```
## DEC-LOCAL-001 · YYYY-MM-DD · <type>
Decision:
Reason:
Affects: <finding IDs / categories>
Decided by:
Maps to register entry:
```

---
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    slug = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") \
        else "clients"
    date = datetime.date.today().isoformat()
    if "--date" in sys.argv:
        date = sys.argv[sys.argv.index("--date") + 1]

    root = os.path.join(base, slug, "audit", date)   # one structure: clients/<slug>/audit/<date>/
    for sub in ("inventories", "questions", "deliverables"):
        os.makedirs(os.path.join(root, sub), exist_ok=True)

    def write_csv(path, cols):
        if not os.path.exists(path):
            with open(path, "w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerow(cols)

    write_csv(os.path.join(root, "findings.csv"), FINDING_COLUMNS)
    write_csv(os.path.join(root, "url-decision-map.csv"), URL_MAP_COLUMNS)
    write_csv(os.path.join(root, "00-manifest.csv"), MANIFEST_COLUMNS)
    write_csv(os.path.join(root, "questions", "questions.csv"), QUESTION_COLUMNS)
    write_csv(os.path.join(root, "conflicts.csv"), CONFLICT_COLUMNS)

    for name, body in (("README.md", README), ("decisions.md", DECISIONS)):
        p = os.path.join(root, name)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body.format(client=slug, date=date))

    print(f"scaffolded {root}")
    for dirpath, _, files in os.walk(root):
        for f in sorted(files):
            print("  ", os.path.relpath(os.path.join(dirpath, f), root))


if __name__ == "__main__":
    main()
