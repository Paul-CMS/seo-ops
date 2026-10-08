#!/usr/bin/env python3
"""PreToolUse guard. Exit 2 blocks the tool call and tells Claude why.

Protects, by refusing direct edits:
  - clients/*/status.json         -> only scripts/status.py, run.py, approve.py change it
  - clients/*/log.md, changes.jsonl, snapshots/  -> append-only, scripts only
  - .claude/state/ (approval token, session id), .claude/hooks/, .claude/settings*.json
  - .env                          -> never read, printed or edited by Claude
  - DataforSEO / WordPress APIs   -> only through scripts (cost checks, current-value checks, logging)
  - the DataforSEO connector      -> blocked; paid calls must go through scripts/dfs.py
  - the Drive connector's search  -> only inside the v3 folder (R8, Paul 2026-10-08)

Shell commands (#20, Paul 2026-10-08): read-only chains (`cd x && cat log.md | grep …`) are allowed, and a
protected name inside a quoted argument of a non-executing command (a commit message, an echo, a script's
--text) is just text. Writes to protected files stay blocked however they are written.

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

# ---- R8: the Drive connector may search only inside v3 (the root, its fixed folders, a client's folder)
if tool.startswith("mcp__") and tool.endswith("__search_files"):
    d = cfg.get("drive") or {}
    allowed = {v for k, v in d.items() if k.endswith("_id") and v}
    for p in (ROOT / "clients").glob("*/status.json"):
        try:
            fid = (json.loads(p.read_text()).get("client") or {}).get("drive_folder_id")
        except Exception:
            fid = None
        if fid:
            allowed.add(fid)
    q = str(inp.get("query") or "")
    ids = re.findall(r"parentId\s*=\s*'([^']+)'", q)
    head = re.match(r"^\s*parentId\s*=\s*'([^']+)'\s*(and\s*\((.*)\))?\s*$", q, re.S) \
        or re.match(r"^\s*parentId\s*=\s*'([^']+)'(\s+and\s+[^()]*)?$", q, re.S)
    if not ids or any(i not in allowed for i in ids) or not head or \
            (re.search(r"\bor\b", q) and not re.match(r"^\s*parentId\s*=\s*'[^']+'\s*and\s*\(", q)):
        block("Drive searches stay inside the v3 folder (R8): start the query with parentId = '<a folder id under "
              "v3>' (config.json drive ids or the client's drive_folder_id), e.g. parentId = '<id>' and title "
              "contains 'x'. Never search the rest of Drive for prior work on a client — and prefer the local "
              "v3 folder (scripts/drive.py where <slug>).")
    sys.exit(0)

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


# ------------------------------------------------------------------ shell commands
def lex(cmd):
    """[(text, quoted)] words and operators. quoted = the word was (partly) inside quotes; operators are
    ('&&'|'||'|';'|'|'|'&'|'>'|'>>'|'<'|'$('|'`', None)."""
    out, cur, quoted, q, i = [], "", False, None, 0
    while i < len(cmd):
        ch = cmd[i]
        if q:
            if ch == q:
                q = None
            elif ch == "\\" and q == '"' and i + 1 < len(cmd):
                i += 1; cur += cmd[i]
            else:
                cur += ch
        elif ch in "'\"":
            q, quoted = ch, True
        elif ch == "\\" and i + 1 < len(cmd):
            i += 1; cur += cmd[i]
        elif ch.isspace():
            if cur or quoted:
                out.append((cur, quoted))
            cur, quoted = "", False
        elif cmd.startswith(("&&", "||", ">>", "$("), i) or ch in ";|&<>`\n":
            if cur or quoted:
                out.append((cur, quoted))
            cur, quoted = "", False
            op = cmd[i:i + 2] if cmd.startswith(("&&", "||", ">>", "$("), i) else ch
            out.append((op if op != "\n" else ";", None))
            i += len(op) - 1 if op != "\n" else 0
        else:
            cur += ch
        i += 1
    if q:
        return None   # unbalanced quotes: treat as unparseable
    if cur or quoted:
        out.append((cur, quoted))
    return out


SEP = {"&&", "||", ";", "|", "&"}
EXEC = {"python", "python3", "node", "perl", "ruby", "bash", "sh", "zsh", "osascript", "awk", "gawk", "xargs",
        "env", "eval", "source", ".", "find", "make", "npx", "uv", "pip"}
WRITERS = {"rm", "mv", "cp", "tee", "touch", "truncate", "dd", "ln", "chmod", "chown", "install", "rsync", "patch",
           "unlink", "shred", "vi", "vim", "nano", "ed", "ex"}
GIT_WRITE = {"checkout", "restore", "rm", "mv", "reset", "clean", "apply", "stash", "am", "cherry-pick", "revert",
             "rebase", "filter-branch"}
MESSAGE_PROGS = {"git", "gh", "echo", "printf"}   # quoted words are text, not paths or code
REC = re.compile(r"status\.json|(^|/)log\.md\b|changes\.jsonl|/snapshots/|\bdecisions\.md|\bdocument-checklist\.md|"
                 r"\bapproval-record\.md|\bhandoff-log\.md")
HOOKS = re.compile(r"\.claude/(state|hooks)|approve-token|\.claude/settings")
ENV = re.compile(r"(^|[/=])\.env(\.[\w.-]+)?$")


def segments(toks):
    seg, redir = [], []
    i = 0
    while i < len(toks):
        t, qd = toks[i]
        if qd is None and t in SEP:
            yield seg, redir
            seg, redir = [], []
        elif qd is None and t in (">", ">>"):
            if i + 1 < len(toks) and toks[i + 1][1] is not None:
                redir.append(toks[i + 1][0]); i += 1
        elif qd is None and t in ("$(", "`"):
            yield seg, redir          # a substitution: its inner command is checked as its own segment
            seg, redir = [], []
        elif qd is None and t == "<":
            pass
        else:
            seg.append((t, qd))
        i += 1
    yield seg, redir


def check_segment(seg, redir):
    words = [t for t, _ in seg]
    if not words:
        for r in redir:
            if REC.search(r) or HOOKS.search(r) or ENV.search(r):
                block("a protected file can't be written by redirection.")
        return
    while words and re.match(r"^\w+=", words[0]):   # VAR=x cmd
        words, seg = words[1:], seg[1:]
    if not words:
        return
    prog = os.path.basename(words[0])
    sub = words[1] if len(words) > 1 else ""
    via_script = prog in ("python", "python3") and len(words) > 1 and re.match(r"^(\./)?scripts/[a-z_]+\.py$", words[1])
    is_msg = prog in MESSAGE_PROGS and not (prog == "git" and sub in GIT_WRITE)

    for r in redir:
        if REC.search(r) or ENV.search(r) or HOOKS.search(r):
            block("status.json, the safety log and the records change only through scripts/*.py "
                  "(no redirection into them).")
    for t, qd in seg:
        if HOOKS.search(t) and not (qd and is_msg):
            block("approval state and hooks are off limits.")
        if ENV.search(t) or re.search(r"(^|[\s/'\"=])\.env(\s|$|['\"])", t):
            if not (qd and prog in ("git", "gh")):
                block(".env holds credentials. Never read or print it — scripts load it themselves.")
        if any(ch in t for ch in "*?[") and not qd and glob_hits_env(t) and not t.startswith(("-", "!")):
            block(ENV_WHY)
    rec_hits = [(t, qd) for t, qd in seg if REC.search(t)]
    if rec_hits and not via_script:
        if prog in WRITERS or (prog == "sed" and any(w.startswith("-i") for w in words)) \
                or (prog == "git" and sub in GIT_WRITE):
            block("status.json and the safety log change only through scripts/*.py.")
        if prog in EXEC:
            block("status.json and the safety log change only through scripts/*.py (no inline code touching them).")
        if not is_msg and prog not in ("cat", "head", "tail", "grep", "egrep", "rg", "wc", "less", "more", "jq",
                                      "ls", "diff", "sed", "cut", "sort", "uniq", "column", "file", "stat", "cd",
                                      "test", "[", "git", "tr", "nl", "md5", "shasum", "open"):
            if any(not qd for _, qd in rec_hits):
                block("status.json and the safety log change only through scripts/*.py.")
    if prog in ("grep", "egrep", "fgrep") and re.search(r"(^|\s)-(\w*[rR]\w*|-recursive|d\s*recurse)\b", " ".join(words)) \
            and not re.search(r"--exclude(-dir)?=?\S*env", " ".join(words)):
        block(ENV_WHY + " (recursive grep needs --exclude='.env*')")
    if prog in ("rg", "ag", "ack") and re.search(r"(--hidden|--no-ignore|-u\b|-uu|-uuu|--unrestricted|--all-types)", " ".join(words)) \
            and not re.search(r"-g\s*'?!\.env|--glob\s*'?!\.env", " ".join(words)):
        block(ENV_WHY + " (searching hidden/ignored files needs -g '!.env')")
    if not via_script and any(re.search(r"api\.dataforseo\.com", t) and not (qd and is_msg) for t, qd in seg):
        block("DataforSEO calls go through scripts/dfs.py or scripts/crawl.py (cost check + log).")
    if not via_script and any(re.search(r"wp-json", t) and not (qd and is_msg) for t, qd in seg):
        block("WordPress API calls go through scripts/wp.py (current-value check + log).")
    if prog == "git" and (sub in ("rebase", "filter-branch") or (sub == "reset" and "--hard" in words)
                          or (sub == "push" and any(w in ("--force", "-f", "--force-with-lease") for w in words))):
        block("history-rewriting git commands are not allowed here; the log must stay intact.")


if tool == "Bash":
    cmd = inp.get("command") or ""
    toks = lex(cmd)
    if toks is None:
        block("the command has unbalanced quotes; write it again.")
    for seg, redir in segments(toks):
        check_segment(seg, redir)
    # heredocs / inline scripts: text after << is code or data the lexer can't see into — keep the old caution
    if re.search(r"<<-?\s*['\"]?\w+", cmd) and (REC.search(cmd) or HOOKS.search(cmd)) \
            and re.search(r"\b(python3?|bash|sh|node|perl|ruby|tee|cat\s*>)\b", cmd):
        block("status.json and the safety log change only through scripts/*.py (no inline scripts touching them).")
sys.exit(0)
