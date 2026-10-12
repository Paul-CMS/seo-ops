#!/usr/bin/env python3
"""UserPromptSubmit hook. Runs only on prompts a human actually submits.

1. When Paul's prompt starts with /approve, write a one-time approval token that scripts/approve.py
   consumes. Claude cannot trigger this hook, and the guard hook stops Claude writing the token file
   itself — that is what makes /approve Paul-only.
2. R2 (Paul, 2026-10-08): record which session is typing (.claude/state/session.json), so run.py can
   refuse a new stage in a session that already finished another one. Refreshed on every prompt, so a
   resumed or second session is always the one recorded.
3. Rewrite 2 P3: when Paul's prompt is /system, write .claude/state/system-token.json for this session — the
   guard then lets this session (only) change the system files. Refused on a Mac whose machine.json says
   can_change_system: false (a VA's Mac).
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
    # P2: one file per session — the newest prompt marks the newest session in this folder
    (state / "sessions").mkdir(parents=True, exist_ok=True)
    sf = state / "sessions" / f"{sid}.json"
    try:
        mine = json.loads(sf.read_text())
    except Exception:
        mine = {"session_id": sid, "started": time.time(), "model": None}
    mine["seen"] = time.time()
    sf.write_text(json.dumps(mine))

prompt = (data.get("prompt") or "").strip()
if prompt.startswith("/approve"):
    state.mkdir(parents=True, exist_ok=True)
    (state / "approve-token.json").write_text(json.dumps(
        {"prompt": prompt, "created": time.time(), "used": False}))
if prompt.split()[:1] == ["/system"]:
    try:
        machine = json.loads((root / "machine.json").read_text())
    except Exception:
        machine = {}
    if machine.get("can_change_system") is False:
        print("seo-ops: /system REFUSED — this Mac runs client stages only (machine.json can_change_system: false). "
              "Workflow changes happen on Paul's Mac. Flag the issue with run.py flag instead.")
    elif sid:
        state.mkdir(parents=True, exist_ok=True)
        (state / "system-token.json").write_text(json.dumps({"session_id": sid, "created": time.time()}))
        print("seo-ops: this is a system session (Paul typed /system). System files may be changed in this session "
              "only; run python3 tests/run_all.py after every change.")
sys.exit(0)
