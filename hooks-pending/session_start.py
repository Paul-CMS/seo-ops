#!/usr/bin/env python3
"""SessionStart hook (R1, R2 — Paul 2026-10-08).

Records the new session's id in .claude/state/session.json (run.py refuses a second stage in one session)
and prints the model reminder, which Claude Code adds to the session's context.
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
    state.mkdir(parents=True, exist_ok=True)
    (state / "session.json").write_text(json.dumps(
        {"session_id": sid, "started": time.time(), "seen": time.time(), "model": model or None,
         "source": data.get("source")}))

lines = ["seo-ops: one session per stage (R2). Stage sessions run on **Haiku** — the Opus agents do the judgment "
         "work; a system/design session (changing seo-ops itself) runs on **Opus**. Never switch a session's model "
         "mid-session: start a new session instead. Start in ~/Documents/seo-ops and type /next <slug>."]
low = model.lower()
if low and not any(m in low for m in ("haiku", "opus")):
    lines.append(f"This session's model is {model}. seo-ops uses Haiku and Opus only — start a new session on Haiku "
                 "(stage work) or Opus (system work).")
print("\n".join(lines))
sys.exit(0)
