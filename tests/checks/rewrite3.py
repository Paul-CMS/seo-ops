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


REPO = __import__("pathlib").Path(__file__).resolve().parents[2]


def _mirror_client_files(h, slug):
    """The NAMES of every data/ and inputs/ file the real clients have (empty files — never their content) in one
    sandbox client, so the manifest is checked against every file type that exists on this Mac."""
    d = h.SB / "clients" / slug
    n = 0
    for c in sorted((REPO / "clients").glob("*")) if (REPO / "clients").is_dir() else []:
        for top in ("data", "inputs"):
            for p in (c / top).rglob("*") if (c / top).is_dir() else []:
                if p.is_file() and p.name != ".DS_Store":
                    q = d / p.relative_to(c)
                    q.parent.mkdir(parents=True, exist_ok=True)
                    q.touch()
                    n += 1
    return n


def t_manifest(h):
    """§3.1: every input type on file has a manifest entry; every consuming step's read list names it; unused inputs
    show in STATUS.md."""
    S_ = "mf-co"
    h.sh(f'python3 scripts/status.py init {S_} --name "Mf Co" --domain mf.example --type full --industry roofing')
    n = _mirror_client_files(h, S_)
    code, out = h.sh("python3 scripts/manifest.py check")
    h.check(f"§3.1: every file type in any client's data/ or inputs/ ({n} file names mirrored) has a manifest entry, and "
            "every consuming step's read list names it", code == 0, out[-1500:])
    stray = h.SB / "clients" / S_ / "data" / "mystery" / "thing.xyz"
    stray.parent.mkdir(parents=True, exist_ok=True); stray.write_text("x")
    code, out = h.sh("python3 scripts/manifest.py check")
    h.check("§3.1: a data file with no manifest entry fails the check, naming it", code == 4 and "data/mystery/thing.xyz" in out, out)
    stray.unlink()
    g = h.SB / "scripts" / "gates.json"
    orig = g.read_text(encoding="utf-8")
    gj = json.loads(orig)
    gj["steps"]["build:evidence"]["reads"] = [r for r in gj["steps"]["build:evidence"]["reads"] if "paa-questions" not in r]
    g.write_text(json.dumps(gj, indent=2, ensure_ascii=False) + "\n")
    code, out = h.sh("python3 scripts/manifest.py check")
    g.write_text(orig)
    h.check("§3.1: a consuming step whose read list leaves out its input fails the check",
            code == 4 and "paa-questions → build:evidence" in out, out)
    steps = json.loads(orig)["steps"]
    for step, must in (("build:evidence", ["reviews.csv", "mentions.csv", "paa-questions.csv", "fanout-queries.csv"]),
                       ("build:draft", ["packs/"]), ("build:brief", ["packs/"]), ("build:write", ["packs/"])):
        reads = " ".join(steps[step]["reads"])
        h.check(f"§1: {step} now reads {', '.join(must)}", all(m in reads for m in must), reads[:400])
    h.sh(f"python3 scripts/records.py render {S_}")
    stx = (h.SB / "clients" / S_ / "STATUS.md").read_text()
    sec = stx.split("## Data on file not used yet", 1)[-1].split("\n## ", 1)[0]
    h.check("§3.1: STATUS.md lists inputs on file that no finished step has read",
            "## Data on file not used yet" in stx and "**reviews**" in sec and "build:evidence" in sec, sec[:600])


SCENARIOS = [t_definitions, t_manifest]
