"""Fix set 2026-10-14 (HMM run 20261014-144852-build-6004): an approval covers every page at the version the review
answers produced; a failed step stops a sequence and no approval follows; F-011 (re-records refused after a revise);
the integrity migration; the build agent's wait-and-report-once rules."""
import json

PAGES = ["svc-curved", "svc-porch", "svc-wheelchair", "svc-repair"]


def _plan():
    pages = [{"id": i, "type": "service", "name": i, "url": f"https://test.example/{i}/", "service_variant": i} for i in PAGES]
    pages += [{"id": "svc-pilot", "type": "service", "name": "p", "url": "https://test.example/svc-pilot/", "service_variant": "P"},
              {"id": "loc-pilot", "type": "location", "name": "l", "url": "https://test.example/loc-pilot/", "city": "Springfield"}]
    return {"pages": pages,
            "batches": [{"id": "pilot", "kind": "service", "label": "Pilot", "pages": ["svc-pilot", "loc-pilot"]},
                        {"id": "services", "kind": "service", "label": "Services", "pages": PAGES}]}


def svc(h, S_):
    return next(b for b in h.status(S_)["build"]["batches"] if b["id"] == "services")


def _setup(h, S_):
    ag = h.build_ready(S_, plan=_plan())
    st = h.status(S_)
    st["build"]["pilot_waived"] = True
    st["build"]["pilot_corrections_applied"] = {"at": "2026-10-14", "note": "test"}
    (ag.c / "status.json").write_text(json.dumps(st))
    h.new_session()
    rid = ag.start("build", "brief", batch="services")
    for p in PAGES:
        ag.write_facts(p)
    h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch services")
    for p in PAGES:
        f = ag.w(f"build/services/briefs/SB-{p}.md", f"# Brief {p}\n\n## Evidence gaps\n- see the grid\n")
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {p} --stage brief --file '{f}' --run {rid}")
        h.check(f"rewrite6: brief of {p} recorded", code == 0, out)
    row = {"page": "svc-porch", "rule": "C8", "item": "FAQ 6 ramps", "severity": "fix_and_list", "category": "semantic",
           "finding": "ramps", "plain_why": "lifts only", "decided_for_you": "dropped the FAQ"}
    fj = ag.w("build/services/briefs-findings.json", json.dumps([row]))
    code, out = h.sh(f"python3 scripts/review.py sheet {S_} services briefs --findings {fj} --run {rid}")
    h.check("rewrite6: the briefs review sheet is written", code == 0, out)
    ag.fin(rid, "briefs written and reviewed")
    return ag


def t_approval_needs_reviewed_versions(h):
    """Paul's HMM case: the review is applied, only 1 of 4 briefs is re-recorded — 3 are refused, nothing is approved."""
    S_ = "r6-rv-co"
    ag = _setup(h, S_)
    h.new_session()
    rid = ag.start("build", "review", batch="services")
    code, out = h.sh(f"python3 scripts/review.py apply {S_} services briefs --run {rid}")
    h.check("rewrite6: the answers are applied", code == 0, out)
    for p in PAGES:   # the agent edits every brief to apply the answers
        (ag.c / f"build/services/briefs/SB-{p}.md").write_text(f"# Brief {p}\n\nedited after the review\n\n## Evidence gaps\n- see the grid\n")
    f0 = f"clients/{S_}/build/services/briefs/SB-svc-curved.md"
    code, out = h.sh(f"python3 scripts/status.py page-stage {S_} svc-curved --stage brief --file '{f0}' --run {rid}")
    h.check("rewrite6: the review run may record a page again once the answers are applied", code == 0, out)
    before = (ag.c / "status.json").read_text()
    code, out = h.paul(f"/approve {S_} batch:services:briefs")
    st = h.status(S_)
    h.check("rewrite6: HMM — 1 of 4 re-recorded: the approval is refused naming the 3, and nothing is approved",
            code != 0 and "nothing is approved" in out and out.count("approved at version") + out.count("not the version recorded")
            + out.count("recorded before") >= 3 and all(p in out for p in PAGES[1:]) and "svc-curved:" not in out
            and not (next(b for b in st["build"]["batches"] if b["id"] == "services").get("briefs") or {}).get("state"), out)
    h.check("rewrite6: a refused approval changes no record", (ag.c / "status.json").read_text() == before)
    for p in PAGES[1:]:
        f = f"clients/{S_}/build/services/briefs/SB-{p}.md"
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {p} --stage brief --file '{f}' --run {rid}")
        h.check(f"rewrite6: {p} re-recorded", code == 0, out)
    ag.fin(rid, "review applied")
    code, out = h.paul(f"/approve {S_} batch:services:briefs")
    h.check("rewrite6: with every page re-recorded the approval goes through", code == 0, out)
    # an edit after the page was recorded is a mismatch too
    st = h.status(S_)
    b = next(b for b in st["build"]["batches"] if b["id"] == "services")
    b["briefs"] = {"state": "revise", "by": "Paul", "at": "x", "files": {}}
    (ag.c / "status.json").write_text(json.dumps(st))
    (ag.c / "build/services/briefs/SB-svc-repair.md").write_text("# changed later\n\n## Evidence gaps\n- x\n")
    code, out = h.paul(f"/approve {S_} batch:services:briefs")
    h.check("rewrite6: a brief edited after it was recorded refuses the approval", code != 0 and "svc-repair" in out, out)


def t_rerecord_after_revise_in_auto_mode(h):
    """F-011: after Paul's revise, the first re-record cleared the revise record and auto mode then read the batch as
    approved — the other three pages were refused 'already approved'."""
    S_ = "r6-f011-co"
    ag = _setup(h, S_)
    st = h.status(S_)
    st["modes"] = {"build:brief": {"mode": "auto", "by": "Paul", "at": "2026-10-14"}}
    (ag.c / "status.json").write_text(json.dumps(st))
    h.new_session()
    rid = ag.start("build", "review", batch="services")
    h.sh(f"python3 scripts/review.py apply {S_} services briefs --run {rid}")
    for p in PAGES:
        f = f"clients/{S_}/build/services/briefs/SB-{p}.md"
        h.sh(f"python3 scripts/status.py page-stage {S_} {p} --stage brief --file '{f}' --run {rid}")
    ag.fin(rid, "applied")
    code, out = h.paul(f"/approve {S_} batch:services:briefs")
    h.check("rewrite6: the briefs are approved", code == 0, out)
    code, out = h.paul(f"/approve {S_} batch:services:briefs --decision revise")
    h.check("rewrite6: Paul re-opens the briefs", code == 0 and svc(h, S_)["briefs"]["state"] == "revise", out)
    h.new_session()
    rid = ag.start("build", "brief", batch="services")
    for p in PAGES:
        f = f"clients/{S_}/build/services/briefs/SB-{p}.md"
        (ag.c / f"build/services/briefs/SB-{p}.md").write_text(f"# Brief {p}\n\nrevised\n\n## Evidence gaps\n- see the grid\n")
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {p} --stage brief --file '{f}' --run {rid}")
        h.check(f"rewrite6: F-011 — after the revise, {p} is recorded again (auto mode)", code == 0, out)
    b = svc(h, S_)
    h.check("rewrite6: F-011 — the revise record stands until Paul approves again", b["briefs"]["state"] == "revise", b["briefs"])
    ag.sh(f'python3 scripts/run.py abort {S_} {rid} --reason test')


def t_sequence_stops(h):
    """A refusal stops the sequence: no later step, no approval, reported once; approve.py refuses while it stands."""
    S_ = "r6-seq-co"
    h.sh(f'python3 scripts/status.py init {S_} --name "Seq" --domain seq.example --type full --industry roofing')
    c = h.SB / "clients" / S_
    code, out = h.sh(f"python3 scripts/seq.py {S_} --step 'python3 -c \"open(\\\"{c}/one.txt\\\",\\\"w\\\").write(\\\"1\\\")\"' "
                     f"--step 'python3 scripts/status.py page-stage {S_} nope --stage brief --file x --run none' "
                     f"--step 'python3 -c \"open(\\\"{c}/three.txt\\\",\\\"w\\\").write(\\\"3\\\")\"' "
                     f"--step 'python3 scripts/approve.py {S_} brand_guide_approved'")
    h.check("rewrite6: a failing step stops the sequence with its exit code and says what was not run",
            code != 0 and "STOPPED at step 2 of 4" in out and "NOT RUN: 2" in out and "[1/4] done" in out, out)
    h.check("rewrite6: no step after the failure ran", (c / "one.txt").exists() and not (c / "three.txt").exists())
    st = h.status(S_)
    h.check("rewrite6: the failure is recorded", (st.get("sequence_failure") or {}).get("step") == 2, st.get("sequence_failure"))
    code, out = h.paul(f"/approve {S_} entity_approved")
    h.check("rewrite6: an approval never runs after a failure", code != 0 and "never runs after a failure" in out, out)
    code, out = h.sh(f"python3 scripts/seq.py {S_} --step 'python3 -c \"print(1)\"'")
    h.check("rewrite6: a sequence that completes clears the failure",
            code == 0 and not h.status(S_).get("sequence_failure"), out)
    for f in (".claude/agents/build.md", ".claude/commands/build.md", ".claude/commands/next.md", "CLAUDE.md"):
        t = (h.SB / f).read_text()
        h.check(f"rewrite6: {f} says a failure stops the sequence", "seq.py" in t or "stops" in t and "failure" in t, f)


def t_agents_wait_and_report_once(h):
    """F-008/F-009/F-010: the build agent waits for every page agent, reads files, reports once."""
    t = (h.SB / ".claude/agents/build.md").read_text()
    h.check("rewrite6: the build agent runs page agents in one message and waits for all of them",
            "do not end your turn until every one has returned" in t and "never leave an agent" in t)
    h.check("rewrite6: results are read from files, and it reports once",
            "results/<page>-<stage>.md" in t and "ONE report" in t and "main chat never relays" in t)
    n = (h.SB / ".claude/commands/next.md").read_text() + (h.SB / ".claude/commands/build.md").read_text()
    h.check("rewrite6: the main chat relays no interim status", "never relay interim status" in n and "relays nothing in between" in n)


def t_integrity_migration(h):
    """On /next, an approval whose recorded pages do not match the versions it names is voided and logged (HMM
    services briefs approval: 1 of 4 recorded at the approved version)."""
    S_ = "r6-mig-co"
    ag = _setup(h, S_)
    st = h.status(S_)
    b = next(b for b in st["build"]["batches"] if b["id"] == "services")
    # Paul's old approval: page records as they are, files named at versions that differ for three pages
    files = {}
    for p in PAGES:
        f = f"clients/{S_}/build/services/briefs/SB-{p}.md"
        files[f] = st["pages"][p]["files"]["brief"]["sha"] if p == "svc-curved" else "0123456789ab"
    b["briefs"] = {"state": "approved", "by": "Paul", "at": "2026-10-14T15:15:48-05:00", "files": files, "conditions": []}
    (ag.c / "status.json").write_text(json.dumps(st))
    n = h.sh(f"python3 scripts/next.py {S_}")
    st = h.status(S_)
    rec = next(b for b in st["build"]["batches"] if b["id"] == "services")["briefs"]
    lm = (ag.c / "log.md").read_text()
    h.check("rewrite6: /next voids the approval (kept as a revise record with why) and logs it",
            rec["state"] == "revise" and rec.get("voided") and rec["was"]["state"] == "approved"
            and "INTEGRITY" in lm and "approval voided" in lm and "batch services briefs" in lm, (rec, lm[-600:]))
    code, out = h.sh(f"python3 scripts/next.py {S_}")
    h.check("rewrite6: a second /next voids nothing more", lm.count("approval voided") == (ag.c / "log.md").read_text().count("approval voided"))
    # a sound approval is left alone
    st = h.status(S_)
    b = next(b for b in st["build"]["batches"] if b["id"] == "services")
    b["briefs"] = {"state": "approved", "by": "Paul", "at": "x", "conditions": [],
                   "files": {f: st["pages"][p]["files"]["brief"]["sha"] for p, f in
                             ((p, f"clients/{S_}/build/services/briefs/SB-{p}.md") for p in PAGES)}}
    (ag.c / "status.json").write_text(json.dumps(st))
    h.sh(f"python3 scripts/next.py {S_}")
    h.check("rewrite6: an approval that matches the recorded pages stands",
            next(b for b in h.status(S_)["build"]["batches"] if b["id"] == "services")["briefs"]["state"] == "approved")


SCENARIOS = [t_approval_needs_reviewed_versions, t_rerecord_after_revise_in_auto_mode, t_sequence_stops,
             t_agents_wait_and_report_once, t_integrity_migration]
