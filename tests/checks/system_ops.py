"""System-session housekeeping (2026-10-12): /resume is /where everywhere; main stays in step with GitHub."""
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


def _repos(tmp):
    """A GitHub stand-in (bare), this Mac's main folder (mac) and a second clone (other), all on main."""
    import os
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t"}
    env.pop("CLAUDE_SEO_OPS_SESSION", None)

    def git_in(d):
        return lambda *x: subprocess.run(["git", "-C", str(d), *x], capture_output=True, text=True, env=env)
    mac, other, bare = tmp / "mac", tmp / "other", tmp / "bare.git"
    mac.mkdir()
    g = git_in(mac)
    g("init", "-q", "-b", "main")
    for f in ("scripts/x.py", "clients/c/log.md"):
        (mac / f).parent.mkdir(parents=True, exist_ok=True)
        (mac / f).write_text("0\n")
    g("add", "-A"); g("commit", "-qm", "base")
    subprocess.run(["git", "clone", "-q", "--bare", str(mac), str(bare)], capture_output=True)
    g("remote", "add", "origin", str(bare)); g("fetch", "-q", "origin")
    g("branch", "-q", "--set-upstream-to=origin/main")
    subprocess.run(["git", "clone", "-q", str(bare), str(other)], capture_output=True)
    return git_in(mac), git_in(other), mac, other

def _commit(g, root, rel, text):
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text)
    g("add", "-A"); g("commit", "-qm", f"edit {rel}")


def t_sync_main(h):
    import shutil
    import sys
    import tempfile
    sys.path.insert(0, str(h.SB / "scripts"))
    try:
        import changereq as C
    finally:
        sys.path.pop(0)
    head = lambda g, ref="HEAD": g("rev-parse", ref).stdout.strip()

    def case(mac_file, other_file, tier=(True, "9 passed, 0 failed")):
        tmp = Path(tempfile.mkdtemp())
        gm, go, mac, other = _repos(tmp)
        if other_file:
            _commit(go, other, other_file, "github\n"); go("push", "-q", "origin", "main")
        if mac_file:
            _commit(gm, mac, mac_file, "mac\n")
        ran = []
        before = head(gm)
        ok, msg = C.sync_main(gm, lambda: ran.append(1) or tier)
        gm("fetch", "-q", "origin")
        res = {"ok": ok, "msg": msg, "ran": bool(ran), "moved": head(gm) != before,
               "pushed": head(gm) == head(gm, "origin/main"), "g": gm, "mac": mac}
        return res, tmp

    r, tmp = case("scripts/x.py", "clients/c/log.md")
    h.check("drift: diverged, this Mac system-only and GitHub clients/-only → rebased, fast tier run, pushed",
            r["ok"] and r["ran"] and r["pushed"] and (r["mac"] / "clients/c/log.md").read_text() == "github\n"
            and "rebased 1 system commit" in r["msg"], r["msg"])
    shutil.rmtree(tmp)
    r, tmp = case("clients/c/log.md", "clients/c/other.md")
    h.check("drift: this Mac's commits touch clients/ → stopped and both sides shown, nothing rebased or pushed",
            not r["ok"] and not r["moved"] and not r["ran"] and "This Mac has 1 commit" in r["msg"]
            and "GitHub has 1 commit" in r["msg"] and "Paul decides" in r["msg"], r["msg"])
    shutil.rmtree(tmp)
    r, tmp = case("scripts/x.py", "scripts/y.py")
    h.check("drift: GitHub's commits touch a system file → stopped, nothing rebased",
            not r["ok"] and not r["moved"] and not r["ran"] and "not the safe case" in r["msg"], r["msg"])
    shutil.rmtree(tmp)
    r, tmp = case("scripts/x.py", "clients/c/log.md", tier=(False, "8 passed, 1 failed"))
    h.check("drift: safe case but the fast tier fails → stopped, nothing pushed, the old main named",
            not r["ok"] and r["ran"] and not r["pushed"] and "fast tier fails" in r["msg"] and "1 failed" in r["msg"],
            r["msg"])
    shutil.rmtree(tmp)
    r, tmp = case("scripts/x.py", None)
    h.check("drift: only this Mac moved → its commits are pushed", r["ok"] and r["pushed"] and "pushed" in r["msg"], r["msg"])
    shutil.rmtree(tmp)
    r, tmp = case(None, "clients/c/log.md")
    h.check("drift: only GitHub moved → fast-forwarded", r["ok"] and r["pushed"] and "fast-forwarded" in r["msg"], r["msg"])
    g = r["g"]
    _commit(g, r["mac"], "scripts/z.py", "new\n")
    sha = head(g)
    h.check("push: a commit not on GitHub is not 'on origin' (done refuses it)", not C.on_origin(g, sha))
    g("remote", "set-url", "origin", str(tmp / "gone.git"))
    ok, msg = C.push(g)
    h.check("push: a failed push is said plainly (only on this Mac) and fails", not ok and msg.startswith("PUSH FAILED")
            and "only on this Mac" in msg and "Stop here" in msg, msg)
    shutil.rmtree(tmp)


SCENARIOS = [t_where_rename, t_sync_main]
