#!/usr/bin/env python3
"""UserPromptSubmit hook. Runs only on prompts a human actually submits.

1. When Paul's prompt starts with /approve, write a one-time approval token that scripts/approve.py
   consumes. Claude cannot trigger this hook, and the guard hook stops Claude writing the token file
   itself — that is what makes /approve Paul-only.
2. R2 (Paul, 2026-10-08): record which session is typing (.claude/state/session.json), so run.py can
   refuse a new stage in a session that already finished another one. Refreshed on every prompt, so a
   resumed or second session is always the one recorded.
"""
import json
import sys
import time
from pathlib import Path

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

root = Path(data.get("cwd") or Path(__file__).resolve().parents[2])
# Resolve to the project root even when Claude was started in a subfolder.
for p in [root, *root.parents]:
    if (p / "scripts" / "approve.py").exists():
        root = p
        break
state = root / ".claude" / "state"

sid = data.get("session_id")
if sid:
    state.mkdir(parents=True, exist_ok=True)
    f = state / "session.json"
    try:
        old = json.loads(f.read_text())
    except Exception:
        old = {}
    rec = {"session_id": sid, "seen": time.time(),
           "started": old.get("started") if old.get("session_id") == sid else time.time(),
           "model": old.get("model") if old.get("session_id") == sid else None}
    f.write_text(json.dumps(rec))

prompt = (data.get("prompt") or "").strip()
if prompt.startswith("/approve"):
    state.mkdir(parents=True, exist_ok=True)
    (state / "approve-token.json").write_text(json.dumps(
        {"prompt": prompt, "created": time.time(), "used": False}))
sys.exit(0)
