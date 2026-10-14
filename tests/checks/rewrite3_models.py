"""Rewrite 3 §6.2: one models table (gates.json → models), enforced."""
import json
import re


def t_models_enforced(h):
    S = "mdl-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Mdl Co" --domain mdl.example --type full --industry roofing')
    h.new_session("claude-sonnet-5-5")
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client")
    h.check("§6.2: run.py start refuses a stage step on the wrong model when the hook saw it",
            code == 4 and "runs on Haiku; this chat is on Sonnet" in out, out)
    h.new_session("claude-haiku-4-5-20251001")
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client")
    h.check("§6.2: the right model starts, and the step prints the model it needs",
            code == 0 and "Model for this step: Haiku chat" in out, out)
    rid = out.splitlines()[-1]
    h.sh(f'python3 scripts/run.py abort {S} {rid} --reason "test"')
    h.new_session("")
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client")
    h.check("§6.2: a model the hook could not see is not refused, but the requirement is printed",
            code == 0 and "could not see this chat's model" in out, out)
    h.sh(f'python3 scripts/run.py abort {S} {out.splitlines()[-1]} --reason "test"')
    h.new_session()
    # every agent's frontmatter matches the table, including the jobs Paul's override can switch
    g = json.loads((h.SB / "scripts" / "gates.json").read_text())
    fm = {}
    for f in (h.SB / ".claude" / "agents").glob("*.md"):
        m = re.search(r"^model:\s*(\S+)", f.read_text().split("\n---", 2)[0], re.M)
        fm[f.stem] = m.group(1) if m else None
    drift = [(s, r["agent"], r["model"], fm.get(r["agent"])) for s, rs in g["models"].items() for r in rs
             if not r.get("override") and fm.get(r["agent"]) != r["model"]]
    unlisted = [a for a in fm if not any(r["agent"] == a for rs in g["models"].values() for r in rs) and a not in
                ("draft-writer", "claude")]
    h.check("§6.2: every agent's frontmatter matches gates.json → models; no agent runs outside the table",
            not drift and not unlisted, (drift, unlisted))
    mech = [(s, r["agent"]) for s, rs in g["models"].items() for r in rs
            if r["role"] in ("ship and worklist", "data pulls", "crawl", "setup") and r["model"] != "haiku"]
    h.check("§6.2: no mechanical step runs an Opus or Sonnet agent", not mech, mech)


SCENARIOS = [t_models_enforced]
