"""Global approvals (/approve global …): never a crash on a missing client folder, all or nothing, system files only
(each client applies them on its own /next), and only in the main folder."""
import json
import os
import re
import shutil


def _tok(h):
    return json.loads((h.SB / ".claude" / "state" / "approve-token.json").read_text())


def t_global_approvals(h):
    SB = h.SB
    for s in ("gl-a", "gl-b"):
        h.sh(f'python3 scripts/status.py init {s} --name "{s}" --domain {s}.example --type full --industry roofing')
    shutil.rmtree(SB / "clients/gl-a/handoffs", ignore_errors=True)   # the red-rover case: no handoffs/ folder
    shutil.rmtree(SB / "clients/gl-b/handoffs", ignore_errors=True)
    loc = SB / "methodology/specs/location.md"
    text = loc.read_text(encoding="utf-8")
    loc.write_text(re.sub(r"^\*\*Status:\*\*.*$", "**Status:** DRAFT", text, count=1, flags=re.M), encoding="utf-8")
    cfg0 = (SB / "config.json").read_text()
    logs0 = {s: (SB / f"clients/{s}/log.md").read_text() for s in ("gl-a", "gl-b")}

    code, out = h.paul("/approve global specs:nope")
    h.check("global approval: a refusal (no such spec) does not use up Paul's /approve",
            code != 0 and "no page spec named" in out and not _tok(h).get("used"), out)

    specs = SB / "methodology/specs"
    os.chmod(specs, 0o555)   # a write error part-way: the spec stamps cannot be written
    try:
        code, out = h.paul("/approve global specs")
    finally:
        os.chmod(specs, 0o755)
    h.check("global approval: a write error leaves nothing written and the token unused",
            code != 0 and "Nothing was changed" in out and not _tok(h).get("used")
            and (SB / "config.json").read_text() == cfg0
            and "**Status:** DRAFT" in loc.read_text(encoding="utf-8"), out)

    n0 = len(json.loads((SB / "config.json").read_text()).get("global_approvals") or [])
    code, out = h.paul("/approve global specs")
    h.check("global approval: with a client that has no handoffs/ folder it does not crash", code == 0 and "approved" in out, out)
    _, files = h.sh("git show --name-only --format= HEAD")
    h.check("global approval: the commit holds system files only (spec stamp and config.json), no client file",
            "config.json" in files and "clients/" not in files
            and "**Status:** APPROVED" in loc.read_text(encoding="utf-8"), files)
    h.check("global approval: no client record is written by it (logs unchanged, no handoffs/ created)",
            all((SB / f"clients/{s}/log.md").read_text() == logs0[s] for s in logs0)
            and not (SB / "clients/gl-a/handoffs").exists(), "")
    cfg = json.loads((SB / "config.json").read_text())
    h.check("global approval: config.json records it for the clients to apply",
            len(cfg["global_approvals"]) == n0 + 1 and cfg["global_approvals"][-1]["kind"] == "specs",
            cfg.get("global_approvals"))

    code, out = h.sh("python3 scripts/next.py gl-a")
    la = (SB / "clients/gl-a/log.md").read_text()
    n_specs = sum(e["kind"] == "specs" for e in cfg["global_approvals"])
    h.check("global approval: the client applies it on its own /next (log line, entries seen, no crash, handoffs/ created)",
            code == 0 and la.count("page specs (global") == n_specs and h.status("gl-a")["global_seen"] == n0 + 1
            and (SB / "clients/gl-a/handoffs").exists(), out)
    h.sh("python3 scripts/next.py gl-a")
    h.check("global approval: applying twice never logs twice", (SB / "clients/gl-a/log.md").read_text() == la)
    h.check("global approval: a client that has not run /next yet is still untouched",
            (SB / "clients/gl-b/log.md").read_text() == logs0["gl-b"])

    code, out = h.paul("/approve global model:build:draft=sonnet")
    la0 = (SB / "clients/gl-a/log.md").read_text()
    _, files = h.sh("git show --name-only --format= HEAD")
    h.check("global approval: a model approval writes config.json only too",
            code == 0 and files.strip() == "config.json", (out, files))
    h.sh("python3 scripts/next.py gl-a")
    la1 = (SB / "clients/gl-a/log.md").read_text()
    h.check("global approval: and the client records it on its next /next",
            la1.count("## MODEL ·") == la0.count("## MODEL ·") + 1 and "build:draft:" in la1.rsplit("## MODEL ·", 1)[-1], la1[-300:])

    wt = SB.parent / (SB.name + "-gl-wt")
    h.sh(f"git add -A && git -c user.email=t@t -c user.name=t commit -qm gl-base; git worktree add -q {wt} -b gl-wt")
    try:
        c = json.loads((wt / "config.json").read_text())
        c.pop("client_work_in_main_folder", None)   # a real install: a client folder is not the main folder
        (wt / "config.json").write_text(json.dumps(c))
        code, out = h.sh(f"cd {wt} && python3 scripts/approve.py global specs")
        h.check("global approval: typed in a client folder it is refused, saying where to type it",
                code == 4 and "typed in the main folder" in out and str(SB) in out, out)
    finally:
        h.sh(f"git worktree remove --force {wt}")


SCENARIOS = [t_global_approvals]
