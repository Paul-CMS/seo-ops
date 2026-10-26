"""CM-065..CM-067 (Paul, 2026-10-25, after first-choice-seamless-gutters): spend goes to judgment, not tool lists or
rework; Paul's own changes never throw approved work away; Paul's words carry from one chat to the next."""
import json
import re


def _frontmatter(path):
    return path.read_text().split("\n---", 1)[0]


def t_lean_agents(h):
    agents = {}
    for f in (h.SB / ".claude" / "agents").glob("*.md"):
        m = re.search(r"^tools:\s*(.+)$", _frontmatter(f), re.M)
        agents[f.stem] = [t.strip() for t in m.group(1).split(",")] if m else None
    open_ = [a for a, t in agents.items() if t is None and a != "claude"]
    h.check("CM-065: every seo-ops agent names a short tool list (an agent without one loads every app tool, ~55k "
            "tokens re-read on every call)", not open_, open_)
    heavy = [(a, t) for a, ts in agents.items() if ts for t in ts if t.startswith("mcp__") or t in ("Artifact", "*")]
    h.check("CM-065: no agent carries app or connector tools", not heavy, heavy)
    g = json.loads((h.SB / "scripts" / "gates.json").read_text())
    rows = [r for rs in g["models"].values() for r in rs if r["role"] == "drafts"]
    h.check("CM-065: page drafts run as draft-writer (the lean page writer), never as build",
            rows and all(r["agent"] == "draft-writer" for r in rows), rows)
    code, out = h.sh("python3 scripts/stages.py list")
    h.check("CM-065: the stage list names draft-writer for the drafts, on Opus by default",
            "drafts: draft-writer (opus)" in out and "drafts: build" not in out, out[-600:])


def t_answers_without_agent(h):
    code, out = h.sh("python3 -c \"import sys; sys.path.insert(0, 'scripts'); import stages, status as S; "
                     "print(stages.stage_of('answers'), 'answers' in S.GATES['any_stage'], S.GATES['steps']['answers']['gates'])\"")
    h.check("CM-065: Paul's answers have their own any-stage step (no gate, allowed in any chat)",
            code == 0 and out.strip() == "None True []", out)
    nxt = (h.SB / ".claude" / "commands" / "next.md").read_text()
    h.check("CM-065: /next records Paul's answers itself in an answers run — never an Opus agent",
            "run.py start <slug> answers" in nxt and "No Opus agent for this" in nxt, nxt[-900:])


SCENARIOS = [t_lean_agents, t_answers_without_agent]
