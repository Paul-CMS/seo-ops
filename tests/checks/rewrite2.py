"""Rewrite 2 (REWRITE-2-HANDOFF.md, 2026-10-09) — one scenario per item.

Run alone: python3 tests/run_all.py -k rewrite2
"""
import json
import subprocess


def _hook(h, name, payload):
    r = subprocess.run(["python3", f".claude/hooks/{name}"], input=json.dumps(payload), text=True, cwd=h.SB,
                       capture_output=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def _guard(h, tool, inp, sid):
    code, out = _hook(h, "guard.py", {"tool_name": tool, "tool_input": inp, "cwd": str(h.SB), "session_id": sid})
    return code == 2, out


def _system(h, sid):
    """Paul types /system in session sid."""
    return _hook(h, "approve_token.py", {"prompt": "/system", "cwd": str(h.SB), "hook_event_name": "UserPromptSubmit",
                                         "session_id": sid})


def _current_sid(h):
    return json.loads((h.SB / ".claude" / "state" / "session.json").read_text())["session_id"]


def t_p3_system_session(h):
    tok = h.SB / ".claude" / "state" / "system-token.json"
    tok.unlink(missing_ok=True)
    WHY = "Workflow changes happen in a system session"
    b, out = _guard(h, "Edit", {"file_path": str(h.SB / "scripts" / "run.py")}, "client-chat")
    h.check("P3: a client session cannot edit a script — the refusal says to flag it", b and WHY in out
            and "run.py flag" in out, out)
    blocked = [p for p in ("scripts/gates.json", "methodology/specs/service.md", "CLAUDE.md", ".claude/agents/build.md",
                           ".claude/commands/next.md", ".claude/skills/x/SKILL.md", "templates/handoff-log.md",
                           "tests/run_all.py", "config.json", "docs/stage-6.md", "hooks-pending/guard.py")
               if _guard(h, "Write", {"file_path": p}, "client-chat")[0]]
    h.check("P3: every system path is blocked outside a system session", len(blocked) == 11, blocked)
    h.check("P3: client files and reads stay allowed",
            not _guard(h, "Write", {"file_path": "clients/x/build/SD - x.md"}, "client-chat")[0]
            and not _guard(h, "Read", {"file_path": "scripts/run.py"}, "client-chat")[0])
    B = lambda c, sid="client-chat": _guard(h, "Bash", {"command": c}, sid)[0]
    h.check("P3: shell writes to system files are blocked (sed -i, cp onto, rm, redirect, git checkout, inline python)",
            B("sed -i '' s/a/b/ scripts/run.py") and B("cp /tmp/a methodology/rulings.md") and B("rm tests/run_all.py")
            and B("echo x > CLAUDE.md") and B("git checkout -- scripts/run.py")
            and B("python3 -c \"open('scripts/x.py','w')\"") and B("python3 - <<EOF\nopen('scripts/x.py','w')\nEOF"))
    h.check("P3: running scripts and tests, reading, copying out and commit messages stay allowed",
            not B("python3 tests/run_all.py -k x") and not B("python3 scripts/run.py check x") and not B("cat scripts/run.py")
            and not B("cp scripts/run.py /tmp/run.py") and not B('git commit -m "scripts/run.py: fix"')
            and not B("grep -n def scripts/run.py"))
    code, out = _system(h, "system-chat")
    h.check("P3: /system issues the system token for the session that typed it", tok.exists() and "system session" in out, out)
    h.check("P3: the system session may edit system files; another session still may not",
            not _guard(h, "Edit", {"file_path": "scripts/run.py"}, "system-chat")[0]
            and not B("sed -i '' s/a/b/ scripts/run.py", "system-chat")
            and _guard(h, "Edit", {"file_path": "scripts/run.py"}, "client-chat")[0])
    h.check("P3: change-requests.md stays append-only, scripts only — even in a system session",
            _guard(h, "Edit", {"file_path": "methodology/change-requests.md"}, "system-chat")[0]
            and _guard(h, "Edit", {"file_path": "clients/x/flags.jsonl"}, "system-chat")[0])
    tok.unlink(missing_ok=True)
    m = h.SB / "machine.json"
    try:
        m.write_text(json.dumps({"can_change_system": False}))
        code, out = _system(h, "va-chat")
        h.check("P3: a VA Mac (can_change_system: false) gets no system token", not tok.exists() and "REFUSED" in out, out)
        _system_tok = tok.write_text(json.dumps({"session_id": "va-chat"}))
        h.check("P3: on a VA Mac even a token does not open system files",
                _guard(h, "Edit", {"file_path": "scripts/run.py"}, "va-chat")[0])
    finally:
        m.unlink(missing_ok=True)
        tok.unlink(missing_ok=True)


def t_p3_flags_and_review(h):
    h.sh('python3 scripts/status.py init fl-co --name "Fl Co" --domain fl.example --type full --industry roofing')
    ag = h.Agent("fl-co")
    rid = ag.start("new-client")
    code, out = h.sh(f'python3 scripts/run.py flag fl-co {rid} --text "The location spec asks for 6-12 neighbourhoods; '
                     f'small towns have 3" --workaround "listed the 3 and noted it"')
    rows = [json.loads(l) for l in (ag.c / "flags.jsonl").read_text().splitlines()] if (ag.c / "flags.jsonl").exists() else []
    h.check("P3: run.py flag appends F-001 to the client's flags.jsonl and the safety log; the run goes on",
            code == 0 and rows and rows[0]["id"] == "F-001" and rows[0]["workaround"]
            and "- FLAG " in (ag.c / "log.md").read_text() and "Carry on" in out, out)
    ag.fin(rid, "set up")
    stx = (ag.c / "STATUS.md").read_text()
    h.check("P3: STATUS.md lists the flag under 'Flagged for Paul (system)'",
            "## Flagged for Paul (system)" in stx and "F-001" in stx and "not yet reviewed" in stx, stx[-800:])
    code, out = h.sh("python3 scripts/changereq.py collect")
    h.check("P3: collecting flags is refused outside a system session", code == 4 and "system session" in out, out)
    code, out = h.sh("python3 scripts/changereq.py list --open")
    h.check("P3: the inbox lists L-008–L-011 as CR-001–CR-004, CR-005, and the uncollected flag",
            all(f"CR-00{i}" in out for i in range(1, 6)) and "(not collected) fl-co F-001" in out, out)
    sid = _current_sid(h)
    _system(h, sid)
    try:
        code, out = h.sh("python3 scripts/changereq.py collect")
        cr = out.split(": ")[-1].strip()
        h.check("P3: /system-review collects the flag as the next CR", code == 0 and cr == "CR-006", out)
        code, out = h.sh(f"python3 scripts/changereq.py done {cr} --sha abc1234")
        h.check("P3: a CR that Paul has not accepted cannot be marked done", code != 0, out)
        h.sh(f'python3 scripts/changereq.py decide {cr} accept --text "location spec: 3+ for towns under 5k"')
        code, out = h.sh(f"python3 scripts/changereq.py done {cr} --sha abc1234")
        h.sh("python3 scripts/records.py render fl-co")
        stx = (ag.c / "STATUS.md").read_text()
        h.check("P3: accepted → built → DONE with its commit; the flag leaves STATUS.md",
                code == 0 and "F-001" not in stx and f"- {cr} · " in (h.SB / "methodology/change-requests.md").read_text(), out)
    finally:
        (h.SB / ".claude" / "state" / "system-token.json").unlink(missing_ok=True)


def _run(cwd, cmd, env_extra=None):
    import os
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_SEO_OPS_SESSION"}
    env.update({"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                "GIT_COMMITTER_EMAIL": "t@t", **(env_extra or {})})
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


def t_p2_parallel_clients(h):
    import shutil
    SB = h.SB
    origin = SB.parent / (SB.name + "-origin.git")
    wtroot = SB.parent / (SB.name + "-wt")
    cfgp = SB / "config.json"
    cfg0 = cfgp.read_text()
    try:
        for s in ("wa-co", "wb-co"):
            h.sh(f'python3 scripts/status.py init {s} --name "{s.title()}" --domain {s}.example --type full --industry roofing')
        (SB / "clients/wa-co/inputs").mkdir(parents=True, exist_ok=True)
        (SB / "clients/wa-co/inputs/raw.csv").write_text("x\n")
        cfg = json.loads(cfg0)
        cfg.update({"git_push_after_run": True, "client_worktrees_root": str(wtroot)})
        cfgp.write_text(json.dumps(cfg, indent=2))
        _run(SB, f"git init -q --bare {origin} && git branch -M main && git add -A && git commit -qm 'before P2' "
                 f"&& git remote add origin {origin} && git push -q origin main")
        code, out = _run(SB, "python3 scripts/worktree.py open wa-co")
        code2, out2 = _run(SB, "python3 scripts/worktree.py open wb-co")
        wa, wb = wtroot / "wa-co", wtroot / "wb-co"
        h.check("P2: worktree.py open makes one folder per client on branch client/<slug> and prints it",
                code == 0 and code2 == 0 and (wa / ".git").exists() and str(wa) in out
                and _run(wa, "git rev-parse --abbrev-ref HEAD")[1] == "client/wa-co", (out, out2))
        h.check("P2: the client's git-ignored raw data is linked from the main folder",
                (wa / "clients/wa-co/inputs/raw.csv").exists(), out)
        h.check("P2: opening it again reuses the folder", "reusing" in _run(SB, "python3 scripts/worktree.py open wa-co")[1])
        for wt, sid in ((wa, "chat-a"), (wb, "chat-b")):
            _hook(h, "session_start.py", {"session_id": sid, "cwd": str(wt), "hook_event_name": "SessionStart",
                                          "source": "startup", "model": "claude-haiku-4-5"})
        h.check("P2: each chat's session file is its own, in its own folder",
                (wa / ".claude/state/sessions/chat-a.json").exists() and (wb / ".claude/state/sessions/chat-b.json").exists()
                and not (wa / ".claude/state/sessions/chat-b.json").exists())
        ra = _run(wa, "python3 scripts/run.py start wa-co new-client")[1].splitlines()[-1]
        rb = _run(wb, "python3 scripts/run.py start wb-co new-client")[1].splitlines()[-1]
        (wa / "clients/wa-co/notes.md").write_text("a\n")
        (wb / "clients/wb-co/notes.md").write_text("b\n")
        ca, oa = _run(wa, f'python3 scripts/run.py finish wa-co {ra} --summary "set up a"')
        cb, ob = _run(wb, f'python3 scripts/run.py finish wb-co {rb} --summary "set up b"')
        log = _run(SB, "git log origin/main --format=%s -n 2")[1].splitlines()
        files = {s: _run(SB, f"git log origin/main --format= --name-only -n 1 --grep='^{s}: /new-client'")[1].split()
                 for s in ("wa-co", "wb-co")}
        h.check("P2: two clients, two chats, interleaved → two commits on main, each with only its own client's files",
                ca == 0 and cb == 0 and "pushed" in oa and "pushed" in ob and len(log) == 2
                and files["wa-co"] and files["wb-co"]
                and all(f.startswith("clients/wa-co/") for f in files["wa-co"])
                and all(f.startswith("clients/wb-co/") for f in files["wb-co"]), (oa, ob, log, files))
        h.check("P2: the run records its own chat's session id", f"session chat-a" in (wa / "clients/wa-co/log.md").read_text())
        code, out = _run(SB, "python3 scripts/run.py start wa-co new-client", {"CLAUDE_SEO_OPS_SESSION": "chat-x"})
        h.check("P2: a second chat on the same client is refused while the first holds it",
                code == 4 and "another chat is working on wa-co" in out and "unlock" in out, out)
        hook = SB / ".git" / "hooks" / "pre-push"
        hook.write_text("#!/bin/sh\nif [ -f race-marker ]; then rm -f race-marker; exit 1; fi\nexit 0\n")
        hook.chmod(0o755)
        (wa / "race-marker").write_text("x")
        ra = _run(wa, "python3 scripts/run.py start wa-co new-client")[1].splitlines()[-1]
        (wa / "clients/wa-co/notes.md").write_text("a2\n")
        code, out = _run(wa, f'python3 scripts/run.py finish wa-co {ra} --summary "again"')
        h.check("P2: a push that loses a race is retried once and then succeeds", "pushed (after one retry)" in out, out)
        hook.unlink()
        g, gout = _guard(h, "Bash", {"command": "python3 scripts/run.py unlock wa-co"}, "chat-a")
        h.check("P2: Claude cannot clear a client lock (the guard blocks run.py unlock)", g, gout)
        code, out = _run(SB, "python3 scripts/run.py unlock wa-co")
        code2, out2 = _run(SB, "python3 scripts/run.py start wa-co new-client", {"CLAUDE_SEO_OPS_SESSION": "chat-x"})
        h.check("P2: after Paul's unlock the other chat may start", code == 0 and "removed" in out and code2 == 0, (out, out2))
        code, out = _run(SB, "python3 -c \"import sys; sys.path.insert(0, 'scripts'); import lib; print(lib.git_commit('sys'))\"")
        h.check("P2: a commit outside one client's folder is refused outside a system session", "NOT COMMITTED" in out, out)
    finally:
        for wt in ("wa-co", "wb-co"):
            _run(SB, f"git worktree remove --force {wtroot / wt}")
        _run(SB, "git remote remove origin")
        shutil.rmtree(wtroot, ignore_errors=True)
        shutil.rmtree(origin, ignore_errors=True)
        cfgp.write_text(cfg0)


SCENARIOS = [t_p3_system_session, t_p3_flags_and_review, t_p2_parallel_clients]
