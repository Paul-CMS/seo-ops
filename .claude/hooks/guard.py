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
import fnmatch
import json
import os
import re
import shlex
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
    (re.compile(r"(^|/)clients/[^/]+/(handoff-log|decisions|document-checklist|approval-record)\.md$"),
     "this record is generated from status.json and log.md (scripts/records.py). Change the source: "
     "run.py finish --handoff, run.py decision, or /approve."),
    (re.compile(r"(^|/)\.claude/(state|hooks)/"), "approval state and hooks are off limits."),
    (re.compile(r"(^|/)\.claude/settings(\.local)?\.json$"), "hook settings are off limits."),
    (re.compile(r"(^|/)\.env$"), ".env holds credentials. Never read, print or edit it — scripts load it themselves."),
]

ENV_WHY = (".env holds credentials. Never read, search or list it — scripts load it themselves. "
           "Search a subfolder, or add a glob/type filter that cannot match .env.")


def glob_hits_env(pattern):
    """True if a file glob could match '.env' (dotfile-aware: only patterns whose last part starts
    with '.' or names env reach a dotfile)."""
    base = (pattern or "").rstrip("/").split("/")[-1]
    if not base:
        return False
    if ".env" in pattern and not pattern.endswith(".env.example"):
        return True
    return (base.startswith(".") or "env" in base) and fnmatch.fnmatch(".env", base)


def dir_holds_env(p):
    try:
        d = Path(p or data.get("cwd") or ".")
        if not d.is_absolute():
            d = Path(data.get("cwd") or ".") / d
        return d.is_dir() and (d / ".env").exists()
    except Exception:
        return False


if tool == "Grep":
    p = str(inp.get("path") or "")
    g = str(inp.get("glob") or "")
    if p.rstrip("/").endswith(".env") or (g and glob_hits_env(g)):
        block(ENV_WHY)
    if dir_holds_env(p) and not (g or inp.get("type")):
        block(ENV_WHY)
    sys.exit(0)

if tool == "Glob":
    if glob_hits_env(str(inp.get("pattern") or "")):
        block(ENV_WHY)
    sys.exit(0)

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
    try:
        toks = shlex.split(cmd, posix=True)
    except ValueError:
        toks = cmd.split()
    for i, t in enumerate(toks):
        if t.startswith(("-", "!")) or (i and toks[i - 1] in ("-g", "--glob", "--exclude", "--exclude-dir")):
            continue  # an exclusion pattern, not a file glob
        if any(ch in t for ch in "*?[") and glob_hits_env(t):
            block(ENV_WHY)
    segs = re.split(r"[|;&]+", cmd)
    for seg in segs:
        w = seg.split()
        if not w:
            continue
        prog = os.path.basename(w[0])
        if prog in ("grep", "egrep", "fgrep") and re.search(r"(^|\s)-(\w*[rR]\w*|-recursive|d\s*recurse)\b", seg) \
                and not re.search(r"--exclude(-dir)?=?\S*env", seg):
            block(ENV_WHY + " (recursive grep needs --exclude='.env*')")
        if prog in ("rg", "ag", "ack") and re.search(r"(--hidden|--no-ignore|-u\b|-uu|-uuu|--unrestricted|--all-types)", seg) \
                and not re.search(r"-g\s*'?!\.env|--glob\s*'?!\.env", seg):
            block(ENV_WHY + " (searching hidden/ignored files needs -g '!.env')")
    if re.search(r"\.claude/(state|hooks)|approve-token", cmd):
        block("approval state and hooks are off limits.")
    if re.search(r"status\.json|log\.md|changes\.jsonl|/snapshots/|decisions\.md|document-checklist\.md|approval-record\.md", cmd) and not via_script:
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
