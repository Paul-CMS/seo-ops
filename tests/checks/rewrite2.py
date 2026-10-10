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


def t_p7_url_rule(h):
    pages = [
        {"id": "svc-a", "type": "service", "url": "https://t.example/roof-repair/", "service_variant": "Roof Repair"},
        {"id": "svc-b", "type": "service", "url": "https://t.example/roof-repair-bluffton/"},
        {"id": "svc-c", "type": "service", "url": "https://t.example/metal-roofing-2/"},
        {"id": "loc-a", "type": "location", "url": "https://t.example/bluffton/", "city": "Bluffton"},
        {"id": "loc-b", "type": "location", "url": "https://t.example/roof-repair-beaufort/", "city": "Beaufort"},
        {"id": "loc-c", "type": "location", "url": "https://t.example/locations/okatie/", "city": "Okatie"},
        {"id": "hub-a", "type": "county", "url": "https://t.example/charleston-metro/"},
        {"id": "hub-b", "type": "county", "url": "https://t.example/hhi-beaufort/"},
        {"id": "hub-c", "type": "county", "url": "https://t.example/beaufort-county/"},
        {"id": "loc-d", "type": "location", "url": "https://t.example/okatie/", "city": "Okatie",
         "live_url": "https://t.example/service-area/okatie-sc/"},
        {"id": "loc-e", "type": "location", "url": "https://t.example/ridgeland/", "city": "Ridgeland",
         "live_url": "https://t.example/service-area/ridgeland-sc/", "replaces": ["https://t.example/service-area/ridgeland-sc/"]},
    ]
    pf = h.SB / "tests" / ".state" / "p7-plan.json"
    pf.parent.mkdir(parents=True, exist_ok=True)
    pf.write_text(json.dumps({"pages": pages}))
    code, out = h.sh(f"python3 scripts/urlcheck.py x {pf}")
    flagged = lambda frag: any(frag in l for l in out.splitlines())
    h.check("P7: a service slug that names a city is refused", flagged("roof-repair-bluffton/: a service slug never names a city"), out)
    h.check("P7: a -2 suffix is refused", flagged("metal-roofing-2/: a -2 suffix"), out)
    h.check("P7: a location slug that names a service is refused", flagged("roof-repair-beaufort/: a location slug never names a service"), out)
    h.check("P7: /locations/ and the other folders are refused", flagged("/locations/okatie/: drop the /locations/"), out)
    h.check("P7: a hub must be a county or metro slug", flagged("hhi-beaufort/: a hub slug") and not flagged("t.example/charleston-metro/:")
            and not flagged("t.example/beaufort-county/:"), out)
    h.check("P7: a changed live URL must be paired with its redirect (replaces)",
            flagged("okatie/: its live URL") and not flagged("ridgeland/"), out)
    h.check("P7: clean root URLs pass", not flagged("t.example/roof-repair/:") and not flagged("t.example/bluffton/:"), out)
    h.sh('python3 scripts/status.py init ui-co --name "Ui Co" --domain ui.example --type full --industry roofing')
    ag = h.Agent("ui-co"); rid = ag.start("new-client")
    prop = {"source": "test", "gates": {}, "pages": {
        "svc-a": {"type": "service", "state": "live", "url": "https://ui.example/services/roof-repair/"},
        "loc-a": {"type": "location", "state": "live", "url": "https://ui.example/bluffton/"}}}
    p = ag.w("import-proposal.json", json.dumps(prop)); ag.fin(rid, "proposal")
    code, out = h.paul(f"/approve ui-co import --proposal {p}")
    h.check("P7: an import whose live baseline breaks the URL rule is refused (the baseline is not exempt)",
            code == 4 and "not exempt" in out and "/services/" in out, out)


def t_p5_reviews(h):
    S = "rv-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Rv Co" --domain rv.example --type full --industry roofing')
    ag = h.Agent(S); ag.fin(ag.start("new-client"), "set up")
    long_text = "Our roof repair was great. " + ("They explained every step and the flashing work was careful. " * 50) + "The end."
    items = [
        {"review_id": "a1", "timestamp": "2026-08-01 10:00:00", "rating": {"value": 5}, "profile_name": "Jane Roe",
         "profile_url": "https://g/a", "review_text": long_text},
        {"review_id": "b1", "timestamp": "2026-07-01 10:00:00", "rating": {"value": 5}, "profile_name": "Sam Poe",
         "profile_url": "https://g/b", "review_text": "Mark did our roof. They sent photos every day. Clean up was spotless."},
        {"review_id": "c1", "timestamp": "2026-06-01 10:00:00", "rating": {"value": 5}, "profile_name": "Ann Doe",
         "profile_url": "https://g/c", "review_text": "Mark was on time. Photos of each step came by text. Great clean up."},
        {"review_id": "d1", "timestamp": "2026-05-01 10:00:00", "rating": {"value": 5}, "profile_name": "Ann Doe",
         "profile_url": "https://g/c", "review_text": "Second job with Mark. More photos.",
         "owner_answer": "Thanks Ann! We always send photos and clean up."},
        {"review_id": "e1", "timestamp": "2026-04-01 10:00:00", "rating": {"value": 5}, "profile_name": "Lee Coe",
         "profile_url": "https://g/e", "review_text": "Mark and the crew were careful. They sent photos too."},
    ]
    raw = ag.c / "data/reviews/raw"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "reviews.json").write_text(json.dumps({"rating": {"value": 5}, "reviews_count": 9, "items": items}))
    code, out = h.sh(f"python3 scripts/reviews.py summarize {S}")
    rows = (ag.c / "data/reviews/reviews.csv").read_text()
    h.check("P5: a long review text is kept whole in reviews.csv (not truncated)", long_text.strip() in rows, len(rows))
    h.check("P5: the pull is checked against Google's count — a gap is flagged", "PULL INCOMPLETE" in out and "9 reviews" in out
            and "5 were pulled" in out, out)
    h.check("P5: reviews.csv carries a reviewer key (a hash), never a reviewer name",
            "reviewer_key" in rows.splitlines()[0] and not any(n in rows for n in ("Jane Roe", "Sam Poe", "Ann Doe", "Lee Coe")))
    rid = ag.start("wp-check")
    code, out = h.sh(f"python3 scripts/reviews.py extract {S} --run {rid}")
    rf = json.loads((ag.c / "data/reviews/review-facts.json").read_text())["facts"]
    h.check("P5: photos told by 3 different reviewers (one of them twice) count 3 — the same reviewer twice counts once, owner replies never",
            rf.get("practice:photos", {}).get("count") == 3, rf.get("practice:photos"))
    h.check("P5: clean-up told by 2 reviewers stays below CM-057's 3 (not customer_reported)",
            rf.get("practice:clean-up", {}).get("count") == 2, rf.get("practice:clean-up"))
    h.check("P5: a staff member named in 3+ reviews is found", rf.get("staff:Mark", {}).get("count") == 3, sorted(rf))
    cl = (ag.c / "data/reviews/customer-language.md").read_text()
    h.check("P5: customer-language.md gains the 'Facts customers report' table (fact, reviewers, example), no names",
            "## Facts customers report" in cl and "| photos | 3 ✓ |" in cl and "Ann Doe" not in cl, cl[-700:])
    fx = json.loads((ag.c / "facts.json").read_text())["facts"]
    r = next((x for x in fx if x.get("key") == "practice:photos"), {})
    h.check("P5: candidates go into facts.json as customer_reported with the quote and the count (never a Brand Guide row)",
            r.get("status") == "customer_reported" and r.get("count") == 3 and r.get("section") == "R" and r.get("quote"), r)
    ag.fin(rid, "reviews")


def t_p6_research_first(h):
    qf = h.SB / "tests" / ".state" / "p6-qs.json"
    qf.parent.mkdir(parents=True, exist_ok=True)
    qf.write_text(json.dumps([
        {"text": "Do you go on the roof yourself?", "kind": "client", "searched": ["facts.json", "reviews"]},
        {"text": "Does Bluffton require a permit for a re-roof?", "kind": "public"},
        {"text": "What is your warranty?", "kind": "client"},
        {"text": "Any awards?"}]))
    code, out = h.sh(f"python3 scripts/questions.py check {qf}")
    h.check("P6: a question set is refused with a public question, a client question without searched:, or no kind",
            code == 1 and "Q2" in out and "never asked" in out and "Q3" in out and "searched:" in out and "Q4" in out
            and "no kind" in out and "Q1" not in out, out)
    qf.write_text(json.dumps([{"text": "Do you go on the roof yourself?", "kind": "client", "searched": ["facts.json"]}]))
    h.check("P6: a set of client questions, each with its searched: line, passes", h.sh(f"python3 scripts/questions.py check {qf}")[0] == 0)
    agents = {f.stem: f.read_text() for f in (h.SB / ".claude" / "agents").glob("*.md")}
    h.check("P6: every agent says the read list never limits web research for public facts",
            all("never limits web research for public facts" in t for t in agents.values()),
            [k for k, t in agents.items() if "never limits web research" not in t])
    h.check("P6: the researcher agent runs on Sonnet and may search the web",
            "model: sonnet" in agents.get("researcher", "") and "WebSearch" in agents.get("researcher", ""))
    h.check("P6: an area source list exists for the Lowcountry, with the SC licence lookup",
            "verify.llronline.com" in (h.SB / "methodology/sources/sc-lowcountry.md").read_text())
    # competitor coverage: top pages per service keyword, H2s and FAQ topics, never the client's own site
    S = "cp-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Cp Co" --domain cp.example --type full --industry roofing')
    ag = h.Agent(S); ag.fin(ag.start("new-client"), "set up")
    h.sh(f"python3 scripts/status.py page {S} svc-roof-repair --type service --url https://cp.example/roof-repair/ --state planned")
    dj = h.SB / "tests" / ".state" / "dfs.json"
    dj.write_text(json.dumps({"balance": 10.0, "cost": 0.002, "serp_organic": [
        "https://cp.example/roof-repair/", "https://rival.example/roof-repair/", "https://other.example/roofing/repair/"]}))
    try:
        rid = ag.start("wp-check")
        kf = ag.w("kw.txt", "roof repair\n")
        code, out = h.sh(f'python3 tests/fakes.py crawl competitors run {S} --run {rid} --location "Springfield,Missouri,United States" '
                         f'--keywords-file {kf} --confirmed')
        cov = (ag.c / "data/competitors/coverage.md").read_text() if (ag.c / "data/competitors/coverage.md").exists() else ""
        h.check("P6: competitor coverage lists each top page's H2s and FAQ topics, skipping the client's own site",
                code == 0 and "rival.example" in cov and "Signs you need a repair" in cov
                and "How long does a roof repair take?" in cov and "cp.example/roof-repair" not in cov
                and "Menu" not in cov and "Nothing here is a fact about the client" in cov, out + cov[:600])
        ag.fin(rid, "competitors")
    finally:
        dj.unlink(missing_ok=True)


def t_p9_worklist(h):
    import csv as _csv
    # after the full walkthrough: one worklist, sections in order, publish rows with their 301s, Drive copy
    wl = h.SB / "clients/wt-full/handoffs/VA-WORKLIST.md"
    t = wl.read_text() if wl.exists() else ""
    h.check("P9: the full walkthrough leaves one VA Worklist with Blockers and Publish sections, in order",
            "## 2 · Blockers" in t and "## 4 · Publish" in t and t.index("## 2 · Blockers") < t.index("## 4 · Publish")
            and "Publish **all of them together**" in t, t[:800])
    rows = list(_csv.DictReader(open(h.SB / "clients/wt-full/handoffs/VA-WORKLIST.csv", newline=""))) if wl.exists() else []
    pub = [r for r in rows if r["section"].startswith("4")]
    h.check("P9: every page's publish row and its paired 301 sit together in section 4",
            sum(r["field"] == "publish" for r in pub) >= 8 and any(r["field"] == "301" for r in pub)
            and pub[[r["field"] for r in pub].index("301") - 1]["field"] == "publish", [r["field"] for r in pub])
    old = sorted((h.SB / "clients/wt-full/handoffs").glob("H-*.md"))
    h.check("P9: the old per-handoff documents are marked superseded", old and all("Superseded by the VA Worklist" in f.read_text() for f in old))
    code, out = h.sh("cd scripts && python3 -c \"import drive; print([n for _, l, n in drive.records('wt-full')])\"")
    h.check("P9: the worklist (Markdown and CSV) is one of the records copied to the client's Drive folder",
            "Test Co - VA Worklist.md" in out and "Test Co - VA Worklist.csv" in out, out)
    # a client before the handover: setup and manual lookups show, publish waits; the returned worklist is ingested
    S = "wl-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Wl Co" --domain wl.example --type full --industry roofing')
    ag = h.Agent(S); ag.fin(ag.start("new-client"), "set up")
    st = h.status(S)
    for g in ("entity_approved", "proof_sheet_approved", "audit_approved", "brand_guide_approved"):
        st["gates"][g] = {"state": "approved", "files": {}}
    (ag.c / "status.json").write_text(json.dumps(st))
    rid = ag.start("wp-check")
    a1 = ag.w("a.csv", "url,field,old,new,reason,decision_map_ref\nhttps://wl.example/wp-admin/,user,,seo-ops,setup,\n")
    a2 = ag.w("b.csv", "url,field,old,new,reason,decision_map_ref\nhttps://sos.example/,record,,read it,legal name,\n")
    a3 = ag.w("c.csv", "url,field,old,new,reason,decision_map_ref\nhttps://wl.example/x/,publish,(draft),https://wl.example/x/,publish,svc-x\n")
    for kind, f in (("wp_setup", a1), ("manual_lookup", a2), ("publish", a3)):
        h.sh(f"python3 scripts/handoff.py create {S} --run {rid} --kind {kind} --items {f}")
    h.sh(f"python3 scripts/records.py render {S}")
    t = (ag.c / "handoffs/VA-WORKLIST.md").read_text()
    h.check("P9: before the handover the worklist carries Setup and Manual lookups; Redirects/Publish wait for it",
            "## 1 · Setup" in t and "## 6 · Manual lookups" in t and "## 4 · Publish" not in t
            and "come in one handover" in t and "1 row(s) waiting" in t, t)
    ret = list(_csv.DictReader(open(ag.c / "handoffs/VA-WORKLIST.csv", newline="")))
    for r in ret:
        r["status"], r["note"] = ("done", "") if r["section"].startswith("1") else ("blocked", "listing site down")
    rp = ag.c / "handoffs/VA-WORKLIST-returned.csv"
    with open(rp, "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=list(ret[0].keys())); w.writeheader(); w.writerows(ret)
    code, out = h.sh(f"python3 scripts/handoff.py ingest {S} --run {rid} --returned {rp.relative_to(h.SB)}")
    t = (ag.c / "handoffs/VA-WORKLIST.md").read_text()
    h.check("P9: the returned worklist is ingested row by row into its groups, and the worklist shows the ticks",
            code == 0 and "| done" in t and "blocked — listing site down" in t and "invented" not in out, out + t[-500:])
    ag.fin(rid, "worklist")
    # ship-all refuses while any service or location batch is not approved
    st = h.status(S)
    st["build"] = {"site_plan": {"file": "x", "approval": None}, "pilot_corrections_applied": None, "batches": [
        {"id": "pilot", "kind": "service", "label": "P", "pages": [], "state": "drafts_written", "files": {},
         "briefs": {"state": "approved", "files": {}}, "drafts": {"state": "approved", "files": {}}, "content_written_back": {"at": "x"}},
        {"id": "l1", "kind": "location", "label": "L", "pages": [], "state": "planned", "files": {}, "briefs": None, "drafts": None}]}
    st.setdefault("imported_conditions", {})["wordpress_connected"] = "test"
    (ag.c / "status.json").write_text(json.dumps(st))
    rid = ag.start("wp-check")
    code, out = h.sh(f"python3 tests/fakes.py publish drafts {S} --run {rid} --all")
    h.check("P9: services and locations ship as a whole — ship refuses while a location batch is not approved",
            code == 4 and "every service and location page ships together" in out and "l1 (drafts not approved yet)" in out, out)
    ag.fin(rid, "ship refused")


SCENARIOS = [t_p3_system_session, t_p3_flags_and_review, t_p2_parallel_clients, t_p7_url_rule, t_p5_reviews,
             t_p6_research_first, t_p9_worklist]
