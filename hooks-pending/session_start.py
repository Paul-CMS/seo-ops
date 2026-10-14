#!/usr/bin/env python3
"""SessionStart hook (R1, R2 — Paul 2026-10-08; rewrite 2 P2; rewrite 3 §6.2).

Records the new session in .claude/state/sessions/<session_id>.json — one file per session, so two chats never
overwrite each other's id (each client worktree has its own state folder too) — plus the old session.json, and puts
CLAUDE_SEO_OPS_SESSION=<id> into the session's own environment (CLAUDE_ENV_FILE) so the scripts know exactly which
chat runs them. Prints the model reminder, which Claude Code adds to the session's context.
"""
import json
import os
import sys
import time
from pathlib import Path

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

root = Path(data.get("cwd") or Path(__file__).resolve().parents[2])
for p in [root, *root.parents]:
    if (p / "scripts" / "approve.py").exists():
        root = p
        break
sid = data.get("session_id")
model = str(data.get("model") or "")
if isinstance(data.get("model"), dict):
    model = str(data["model"].get("id") or data["model"].get("display_name") or "")
if sid:
    state = root / ".claude" / "state"
    (state / "sessions").mkdir(parents=True, exist_ok=True)
    rec = {"session_id": sid, "started": time.time(), "seen": time.time(), "model": model or None,
           "source": data.get("source")}
    (state / "sessions" / f"{sid}.json").write_text(json.dumps(rec))
    (state / "session.json").write_text(json.dumps(rec))
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    if env_file:
        try:
            with open(env_file, "a") as fh:
                fh.write(f"export CLAUDE_SEO_OPS_SESSION={sid}\n")
        except Exception:
            pass

lines = ["seo-ops: one session per stage (R2). Required model: client stage chats **Haiku** (the Sonnet and Opus agents do "
         "the judgment work); a system session that implements a written spec **Sonnet**; a system session that decides "
         "design **Opus**, only when Paul says so. Never switch a session's model mid-session: start a new session "
         "instead. Client work runs only in the client's own folder (`python3 scripts/worktree.py open <slug>` prints "
         "it) — never in ~/Documents/seo-ops; type /next <slug> there."]
low = model.lower()
if low and not any(m in low for m in ("haiku", "sonnet", "opus")):
    lines.append(f"This session's model is {model}. seo-ops uses Haiku, Sonnet and Opus — start a new session on the "
                 "model the stage names.")
print("\n".join(lines))
sys.exit(0)
