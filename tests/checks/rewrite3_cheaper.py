"""Rewrite 3 §6.3 / §6.4: dry run, quiet runs, CLAUDE.md core size, the compact suggestion."""
import json


def t_cheaper_runs(h):
    S = "chp-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Chp Co" --domain chp.example --type full --industry roofing')
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client --dry")
    h.check("§6.3: --dry checks everything and records no run",
            code == 0 and "dry run passed" in out and not h.status(S).get("open_runs")
            and "· STARTED ·" not in (h.SB / "clients" / S / "log.md").read_text(), out)
    code, out = h.sh(f"python3 scripts/run.py start {S} crawl --dry")
    h.check("§6.3: a dry run refuses what a real start would refuse, before any agent is spawned",
            code == 4 and "REFUSED" in out, out)
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client")
    rid = out.splitlines()[-1]
    h.check("§6.3: run.py start prints at most 10 lines", len(out.splitlines()) <= 10, out)
    hp = h.SB / "clients" / S / "handoffs" / f"run-{rid}.md"
    hp.parent.mkdir(parents=True, exist_ok=True)
    hp.write_text("**What I did**\n- x\n")
    code, out = h.sh(f'python3 scripts/run.py finish {S} {rid} --summary "x" --handoff clients/{S}/handoffs/run-{rid}.md --tokens 150000')
    h.check("§6.4: run.py finish suggests /compact past 120k tokens (a suggestion only) and prints at most 10 lines",
            "/compact Keep: the handoff file" in out and len(out.splitlines()) <= 10, out)
    bad = [f.name for f in (h.SB / ".claude" / "agents").glob("*.md") if "at most 15 lines" not in f.read_text()]
    h.check("§6.3: every agent file caps its reply to the main chat at 15 lines", not bad, bad)
    n = len((h.SB / "CLAUDE.md").read_text().splitlines())
    h.check("§6.3: the CLAUDE.md core stays under about 200 lines", n < 200, n)


SCENARIOS = [t_cheaper_runs]
