#!/usr/bin/env python3
"""stages.py — which stage a step belongs to, and which models run it (R1, R2).

    stages.py list                 every stage: number, name, session model, agents (with their models), steps
    stages.py of <step> [--batch]  the stage a step belongs to

Models are preset: Haiku and Opus only (Paul, 2026-10-08). The session model is in gates.json → stages;
each agent's model is in its .claude/agents/<name>.md frontmatter — never anywhere else, so a subagent
never causes a mid-session switch.
"""
import re
import sys
from pathlib import Path

from lib import ROOT

import status as S

ALLOWED_MODELS = ("haiku", "opus")
AGENTS = ROOT / ".claude" / "agents"


def stages():
    return S.GATES["stages"]


def total():
    return len(stages())


def agent_model(name):
    p = AGENTS / f"{name}.md"
    if not p.exists():
        return None
    m = re.search(r"^model:\s*(\S+)\s*$", p.read_text().split("\n---", 2)[0] + "\n", re.M)
    return m.group(1) if m else None


def agents_line(stage):
    return ", ".join(f"{a} ({agent_model(a) or '?'})" for a in stage["agents"])


RETIRED_STEPS = {"discovery:signoff": "discovery:reconcile"}   # R3: the sign-off is a condition now


def stage_of(step):
    """The stage dict for a step key ('discovery:audit', 'crawl'), or None for an any-stage step."""
    step = RETIRED_STEPS.get(step, step)
    if step in S.GATES.get("any_stage", []):
        return None
    for st in stages():
        if step in st["steps"]:
            return st
    return None


def session_key(step, batch=None):
    """What one session may cover: the stage id, or stage:batch for a per-batch stage. None = any session."""
    st = stage_of(step)
    if not st:
        return None
    return f"{st['id']}:{batch}" if st.get("per_batch") and batch else st["id"]


def step_of_command(command):
    """'/build x brief pilot svc' → ('build:brief', 'pilot'); '/crawl x' → ('crawl', None). None if not a step."""
    w = (command or "").split()
    if not w or not w[0].startswith("/"):
        return None, None
    name, args = w[0][1:], w[2:]
    if name in ("approve", "next", "resume"):
        return None, None
    if name == "build" and args[:1] == ["batch"]:
        return f"build:{args[2] if len(args) > 2 else 'drafts'}", (args[1] if len(args) > 1 else None)
    sub = args[0] if args else None
    key = f"{name}:{sub}" if sub and f"{name}:{sub}" in S.GATES["steps"] else name
    batch = None
    if name in ("build", "interview") and len(args) > 1 and key not in ("build:plan", "build:blockers",
                                                                       "build:pilot-corrections"):
        batch = args[1]
    if key == "build:pilot-corrections":
        batch = "pilot"
    return (key if key in S.GATES["steps"] else None), batch


SESSION_FILE = ROOT / ".claude" / "state" / "session.json"
SESSIONS_DIR = ROOT / ".claude" / "state" / "sessions"


def latest_session(state_dir):
    """The id of the newest session file (by last prompt seen) in a .claude/state folder, or None."""
    import json
    best = (None, -1)
    for f in (Path(state_dir) / "sessions").glob("*.json"):
        try:
            rec = json.loads(f.read_text())
        except Exception:
            continue
        if float(rec.get("seen") or 0) > best[1]:
            best = (rec.get("session_id"), float(rec.get("seen") or 0))
    return best[0]


def current_session():
    """This chat's session id (P2): CLAUDE_SEO_OPS_SESSION, which the SessionStart hook puts in the session's own
    environment; else the newest per-session file in this folder's .claude/state/sessions/ (each client worktree has
    its own); else the old single session.json. None if no hook ran."""
    import json
    import os
    sid = os.environ.get("CLAUDE_SEO_OPS_SESSION")
    if sid:
        return sid
    sid = latest_session(ROOT / ".claude" / "state")
    if sid:
        return sid
    try:
        return json.loads(SESSION_FILE.read_text()).get("session_id")
    except Exception:
        return None


# ------------------------------------------------------------------ client lock (P2)
def lock_path(slug):
    """Locks live in git's common folder, so every worktree of this repo sees the same lock for a client."""
    from lib import main_root
    import subprocess
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                       capture_output=True, text=True)
    base = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else main_root() / ".claude" / "state"
    return base / "seo-ops-locks" / f"{slug}.json"


def lock_holder(slug, sid):
    """The lock record if ANOTHER session has an open run for this client, else None (Paul, 2026-10-09). The lock is
    taken by run.py start and released by run.py finish / abort, so it holds exactly while a run is open — a new chat,
    even in the same folder, may take the client only when no run is open. Only Paul clears a stuck lock (unlock)."""
    import json
    p = lock_path(slug)
    try:
        rec = json.loads(p.read_text())
    except Exception:
        return None
    if not rec.get("session") or rec.get("session") == sid:
        return None
    if not rec.get("run"):   # a lock in the first (time-based) format names no run: it can never be released — ignore it
        return None
    return rec


def take_lock(slug, sid, run_id):
    import json
    import socket
    import time
    p = lock_path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"session": sid, "run": run_id, "host": socket.gethostname(), "worktree": str(ROOT),
                             "at": time.time()}))


def release_lock(slug, run_id):
    """run.py finish / abort: the lock goes with the run that took it."""
    import json
    p = lock_path(slug)
    try:
        rec = json.loads(p.read_text())
    except Exception:
        return False
    if rec.get("run") == run_id:
        p.unlink(missing_ok=True)
        return True
    return False


def unlock(slug):
    p = lock_path(slug)
    existed = p.exists()
    p.unlink(missing_ok=True)
    return existed


def session_conflict(slug, step, batch=None, sid=None):
    """R2: None if this session may run <step>; else the plain-language refusal. A session that finished a run of
    one stage (for one client) may not start another stage — bookkeeping steps (any_stage) are always allowed."""
    key = session_key(step, batch)
    if not key:
        return None
    sid = sid or current_session()
    if not sid:
        return ("No session is recorded — the seo-ops session hook is not installed (.claude/hooks/session_start.py). "
                "One session per stage is enforced through it.")
    from lib import CLIENTS
    import json
    for p in sorted(CLIENTS.glob("*/status.json")):
        rec = (json.loads(p.read_text()).get("sessions") or {}).get(sid)
        if rec and (p.parent.name != slug or rec.get("key") != key):
            done = stage_of(rec.get("step") or "") or {}
            nxt = stage_of(step) or {}
            return (f"Stage {done.get('n', '?')} ({done.get('name', rec.get('key'))}) is done in this session"
                    + (f" for {p.parent.name}" if p.parent.name != slug else "")
                    + f". Start a new session (new chat, model: {nxt.get('session_model', 'haiku').title()}) in "
                    f"the client folder (python3 scripts/worktree.py open {slug}) and type /next {slug}.")
    return None


def stage_doc(step):
    """docs/stage-<n>-*.md for the step's stage (P12: the procedure, loaded only by that stage), or None."""
    st = stage_of(step) if step else None
    if not st:
        return None
    hits = sorted((ROOT / "docs").glob(f"stage-{st['n']}-*.md"))
    return str(hits[0].relative_to(ROOT)) if hits else None


MODEL_AGENT = {("build:draft", "sonnet"): "draft-writer", ("build:draft", "opus"): "build"}


def step_models(step):
    """[(role, agent, model)] for a step, from gates.json → models with Paul's overrides (config.json
    model_overrides, set only by /approve global model:<key>=<model>)."""
    from lib import config
    over = config().get("model_overrides") or {}
    out = []
    for r in (S.GATES.get("models") or {}).get(step, []):
        key = r.get("key") or step
        model = (over.get(key) or {}).get("model") or r["model"]
        agent = MODEL_AGENT.get((key, model), r["agent"]) if model != r["model"] else r["agent"]
        out.append((r["role"], agent, model))
    return out


def models_line(step):
    return "; ".join(f"{role}: {agent} ({model})" for role, agent, model in step_models(step))


def describe(step, batch=None):
    """{'stage': '2 of 8 — Discovery', 'session_model': 'haiku', 'agents': '…'} for a step (or {} if none)."""
    st = stage_of(step) if step else None
    if not st:
        return {}
    name = st["name"] + (f" (batch {batch})" if st.get("per_batch") and batch else "")
    out = {"stage": f"{st['n']} of {total()} — {name}", "session_model": st["session_model"],
           "agents": agents_line(st)}
    if step_models(step):
        out["models"] = models_line(step)   # §4: who does each job in this step, on which model
    return out


def main():
    if sys.argv[1:2] == ["list"]:
        for st in stages():
            print(f"{st['n']} {st['name']:26} session {st['session_model']:6} agents: {agents_line(st)}")
            print(f"  {'':24} steps: {', '.join(st['steps'])}")
            for step in st["steps"]:
                if step_models(step):
                    print(f"  {'':24}   {step}: {models_line(step)}")
        print("any stage: " + ", ".join(S.GATES.get("any_stage", [])))
    elif sys.argv[1:2] == ["of"] and len(sys.argv) > 2:
        st = stage_of(sys.argv[2])
        print(f"{st['n']} {st['name']}" if st else "any stage")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
