"""Rewrite 3 Phase 1 (Paul, 2026-10-12; CM-061 — evidence first, decide by default)."""
import csv
import json
import re


def _read(h, rel):
    return (h.SB / rel).read_text(encoding="utf-8")


def t_definitions(h):
    """§2: one ruling records Phase 1; the definitions live in one file every agent and CLAUDE.md point to."""
    code, out = h.sh("python3 scripts/rulings.py CM-061")
    h.check("CM-061: the ruling is in rulings.md and readable by ID", code == 0 and "Evidence first, decide by default" in out
            and "APPROVED" in out, out[:300])
    d = _read(h, "methodology/definitions.md")
    terms = ["Client fact", "Public fact", "Source", "Official source", "Context source", "Evidence pack",
             "Review mention", "Fact status", "Usage tier", "Known", "Searched", "Finding", "Severity", "Default", "Ask",
             "Section", "Step", "Review sheet", "Overdue Ask"]
    missing = [t for t in terms if f"**{t}**" not in d]
    h.check("§2: methodology/definitions.md defines every binding term", not missing, missing)
    files = sorted((h.SB / ".claude" / "agents").glob("*.md")) + [h.SB / "CLAUDE.md"]
    bad = [f.name for f in files if "methodology/definitions.md" not in f.read_text(encoding="utf-8")]
    h.check("§2: every agent file and CLAUDE.md points to methodology/definitions.md", not bad, bad)
    bad = [f.name for f in files[:-1] if "never limits web research" not in f.read_text(encoding="utf-8")]
    h.check("§4.3: every agent file says the read list never limits web research", not bad, bad)
    cfg = json.loads(_read(h, "config.json"))
    h.check("§2: the overdue-Ask window is a config value (3 working days)", cfg.get("overdue_ask_working_days") == 3)


SCENARIOS = [t_definitions]
