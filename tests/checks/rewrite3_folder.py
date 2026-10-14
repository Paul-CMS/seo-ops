"""Rewrite 3 §00: client work runs only in the client's own folder."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rewrite2 import _hook, _run   # noqa: E402


def t_folder_rule(h):
    SB = h.SB
    origin = SB.parent / (SB.name + "-f-origin.git")
    wtroot = SB.parent / (SB.name + "-f-wt")
    cfgp = SB / "config.json"
    cfg0 = cfgp.read_text()
    S = "fold-co"
    try:
        h.sh(f'python3 scripts/status.py init {S} --name "Fold Co" --domain fold.example --type full --industry roofing')
        (SB / "machine.json").write_text('{"can_approve": true}\n')
        cfg = json.loads(cfg0)
        cfg.pop("client_work_in_main_folder", None)   # a real install
        cfg.update({"git_push_after_run": True, "client_worktrees_root": str(wtroot)})
        cfgp.write_text(json.dumps(cfg, indent=2))
        _run(SB, f"git init -q --bare {origin} && git branch -M main && git add -A && git commit -qm 'before f' "
                 f"&& git remote add origin {origin} && git push -q origin main")
        code, out = _run(SB, f"python3 scripts/run.py start {S} new-client")
        h.check("§00: run.py start is refused in the main folder with the plain message",
                code == 4 and "Client work runs in the client's folder: `python3 scripts/worktree.py open fold-co`" in out, out)
        res = {c: _run(SB, c)[:2] for c in (f'python3 scripts/run.py abort {S} X --reason t',
                                           f'python3 scripts/run.py finish {S} X --summary t',
                                           f'python3 scripts/publish.py drafts {S} --run X',
                                           f'python3 scripts/publish.py wheel {S}')}
        h.check("§00: abort, finish and publish.py are refused in the main folder too (a subagent calling from there)",
                all(c == 4 and "Client work runs in the client's folder" in o for c, o in res.values()), res)
        code, out = _run(SB, "python3 scripts/worktree.py open " + S)
        wt = wtroot / S
        _hook(h, "session_start.py", {"session_id": "fold-chat", "cwd": str(wt), "hook_event_name": "SessionStart",
                                      "source": "startup", "model": "claude-haiku-4-5"})
        code, out = _run(wt, f"python3 scripts/run.py start {S} new-client")
        rid = out.splitlines()[-1]
        h.check("§00: the same command runs in the client's worktree", code == 0 and "REFUSED" not in out, out)
        code, out = _run(wt, f"python3 scripts/publish.py wheel {S}")
        h.check("§00: a subagent call from the worktree is not refused for its folder",
                "Client work runs in the client's folder" not in out, out)
        # the open run is committed from the worktree, then another folder tries to start a second run
        _run(wt, f"git add -A clients/{S} && git commit -qm 'open run' && git push -q origin HEAD:main")
        cfg["client_work_in_main_folder"] = True   # main folder allowed now: only the origin check can refuse
        cfgp.write_text(json.dumps(cfg, indent=2))
        code, out = _run(SB, f"python3 scripts/run.py start {S} new-client")
        h.check("§00: run.py start refuses when origin records an open run from another folder",
                code == 4 and "open run recorded on origin from another folder" in out and rid in out, out)
        code, out = _run(wt, f'python3 scripts/run.py abort {S} {rid} --reason "test"')
        h.check("§00: the one abort, in the client's folder, closes the run and commits", code == 0, out)
        code2, out2 = _run(SB, f'python3 scripts/run.py abort {S} {rid} --reason "test"')
        h.check("§00: a second abort of the same run is refused (not an open run), never recorded twice",
                code2 != 0 and "not an open run" in out2
                and (wt / f"clients/{S}/log.md").read_text().count(f"RUN {rid} · ABORTED") == 1, out2)
    finally:
        _run(SB, f"git worktree remove --force {wtroot / S}")
        _run(SB, "git remote remove origin")
        shutil.rmtree(wtroot, ignore_errors=True)
        shutil.rmtree(origin, ignore_errors=True)
        (SB / "machine.json").unlink(missing_ok=True)
        cfgp.write_text(cfg0)


SCENARIOS = [t_folder_rule]
