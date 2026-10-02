#!/usr/bin/env python3
"""PreToolUse guard. Exit 2 blocks the tool call and tells Claude why.

Protects, by refusing direct edits:
  - clients/*/status.json         -> only scripts/status.py, run.py, approve.py change it
  - clients/*/log.md, changes.jsonl, snapshots/  -> append-only, scripts only
  - .claude/state/ (approval token), .claude/hooks/, .claude/settings*.json
  - .env                          -> never read, printed or edited by Claude
  - DataforSEO / WordPress APIs   -> only through scripts (cost checks, current-value checks, logging)
  - the DataforSEO connector      -> blocked; paid calls must go through scripts/dfs.py

This is a guard against mistakes, not a security boundary against a determined user.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def block(why):
    print(f"BLOCKED by seo-ops guard: {why}", file=sys.stderr)
    sys.exit(2)


try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
inp = data.get("tool_input") or {}

try:
    cfg = json.loads((ROOT / "config.json").read_text())
except Exception:
    cfg = {}
for prefix, why in (cfg.get("blocked_tool_prefixes") or {}).items():
    if tool.startswith(prefix):
        block(why)

PROTECTED = [
    (re.compile(r"(^|/)clients/[^/]+/status\.json$"), "status.json changes only through scripts/status.py, run.py and approve.py (/approve for gates)."),
    (re.compile(r"(^|/)clients/[^/]+/(log\.md|changes\.jsonl)$"), "the safety log is append-only; write to it only with scripts/run.py."),
    (re.compile(r"(^|/)clients/[^/]+/snapshots/"), "snapshots are the rollback record; scripts only."),
    (re.compile(r"(^|/)\.claude/(state|hooks)/"), "approval state and hooks are off limits."),
    (re.compile(r"(^|/)\.claude/settings(\.local)?\.json$"), "hook settings are off limits."),
    (re.compile(r"(^|/)\.env$"), ".env holds credentials. Never read, print or edit it — scripts load it themselves."),
]

if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit", "Read"):
    fp = str(inp.get("file_path") or inp.get("notebook_path") or "")
    for rx, why in PROTECTED:
        if rx.search(fp):
            if tool == "Read" and not fp.endswith(".env") and "/.claude/state/" not in fp:
                break  # reading status, logs and snapshots is fine
            block(why)
    sys.exit(0)

if tool == "Bash":
    cmd = inp.get("command") or ""
    # A single scripts/*.py invocation with no chaining, piping, substitution or redirection.
    via_script = bool(re.match(r"^\s*python3 scripts/[a-z_]+\.py\b[^;&|`<>]*$", cmd)) \
        and "$(" not in cmd
    if re.search(r"(^|[\s/'\"=])\.env(\s|$|['\"])", cmd):
        block(".env holds credentials. Never read or print it — scripts load it themselves.")
    if re.search(r"\.claude/(state|hooks)|approve-token", cmd):
        block("approval state and hooks are off limits.")
    if re.search(r"status\.json|log\.md|changes\.jsonl|/snapshots/", cmd) and not via_script:
        readonly = re.match(r"^\s*(cat|head|tail|grep|wc|less|jq|ls|diff)\b", cmd) \
            and not re.search(r">|\btee\b|sed\s+-i|\brm\b|\bmv\b|\bcp\b|python", cmd)
        if not readonly:
            block("status.json and the safety log change only through scripts/*.py.")
    if re.search(r"api\.dataforseo\.com", cmd) and not via_script:
        block("DataforSEO calls go through scripts/dfs.py or scripts/crawl.py (cost check + log).")
    if re.search(r"wp-json", cmd) and not via_script:
        block("WordPress API calls go through scripts/wp.py (current-value check + log).")
    if re.search(r"git\s+(push\s+.*--force|reset\s+--hard|filter-branch|rebase)", cmd):
        block("history-rewriting git commands are not allowed here; the log must stay intact.")
sys.exit(0)
