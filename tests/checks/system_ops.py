"""System-session housekeeping (2026-10-12): /resume is /where everywhere."""
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HISTORY = {"REWRITE-HANDOFF.md", "design-brief-2026-10-09-test-output.txt"}   # dated records, left as written


def t_where_rename(h):
    cmds = REPO / ".claude" / "commands"
    h.check("/where replaces /resume: where.md exists, resume.md is gone, and /where runs the missing-links check",
            (cmds / "where.md").is_file() and not (cmds / "resume.md").exists()
            and "worktree.py check" in (cmds / "where.md").read_text())
    files = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True).stdout.split()
    left = [f for f in files if not f.startswith("clients/") and f not in HISTORY and Path(f).name != ".env"
            and (REPO / f).is_file() and "/resume" in (REPO / f).read_text(encoding="utf-8", errors="ignore")
            and f != "tests/checks/system_ops.py"]
    h.check("/where replaces /resume: no live file names /resume", not left, left)


SCENARIOS = [t_where_rename]
