#!/usr/bin/env python3
"""UserPromptSubmit hook. Runs only on prompts a human actually submits.

When Paul's prompt starts with /approve, write a one-time approval token that
scripts/approve.py consumes. Claude cannot trigger this hook, and the guard hook stops
Claude writing the token file itself — that is what makes /approve Paul-only.
"""
import json
import sys
import time
from pathlib import Path

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = (data.get("prompt") or "").strip()
if prompt.startswith("/approve"):
    root = Path(data.get("cwd") or Path(__file__).resolve().parents[2])
    # Resolve to the project root even when Claude was started in a subfolder.
    for p in [root, *root.parents]:
        if (p / "scripts" / "approve.py").exists():
            root = p
            break
    state = root / ".claude" / "state"
    state.mkdir(parents=True, exist_ok=True)
    (state / "approve-token.json").write_text(json.dumps(
        {"prompt": prompt, "created": time.time(), "used": False}))
sys.exit(0)
