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


def stage_of(step):
    """The stage dict for a step key ('discovery:audit', 'crawl'), or None for an any-stage step."""
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


def describe(step, batch=None):
    """{'stage': '2 of 8 — Discovery', 'session_model': 'haiku', 'agents': '…'} for a step (or {} if none)."""
    st = stage_of(step) if step else None
    if not st:
        return {}
    name = st["name"] + (f" (batch {batch})" if st.get("per_batch") and batch else "")
    return {"stage": f"{st['n']} of {total()} — {name}", "session_model": st["session_model"],
            "agents": agents_line(st)}


def main():
    if sys.argv[1:2] == ["list"]:
        for st in stages():
            print(f"{st['n']} {st['name']:26} session {st['session_model']:6} agents: {agents_line(st)}")
            print(f"  {'':24} steps: {', '.join(st['steps'])}")
        print("any stage: " + ", ".join(S.GATES.get("any_stage", [])))
    elif sys.argv[1:2] == ["of"] and len(sys.argv) > 2:
        st = stage_of(sys.argv[2])
        print(f"{st['n']} {st['name']}" if st else "any stage")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
