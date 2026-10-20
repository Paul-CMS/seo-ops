"""Rewrite 4 Phase 4 — slim build: no brief step (D2). A section on the outline route goes from the approved site plan to
its one draft review sheet and one approval line with outlines written by script; sections whose briefs were approved
before keep the brief route (D5, migrated on /next); the pilot rule (three clean pilots); the writer's three fact
states in the evidence pack."""
import json

LOCS = ["loc-beaufort", "loc-bluffton"]


def _plan():
    pages = [{"id": "svc-lifts", "type": "service", "name": "Stair Lifts", "url": "https://test.example/stair-lifts/",
              "service_variant": "stair lifts"},
             {"id": "loc-beaufort", "type": "location", "name": "Beaufort, SC", "url": "https://test.example/beaufort-sc/",
              "city": "Beaufort", "group": "metro", "keyword": "stair lifts Beaufort SC"},
             {"id": "loc-bluffton", "type": "location", "name": "Bluffton, SC", "url": "https://test.example/bluffton-sc/",
              "city": "Bluffton", "group": "metro"},
             {"id": "svc-pilot", "type": "service", "name": "P", "url": "https://test.example/svc-pilot/", "service_variant": "p"},
             {"id": "loc-pilot", "type": "location", "name": "L", "url": "https://test.example/loc-pilot/", "city": "Lpilot"}]
    return {"pages": pages,
            "batches": [{"id": "pilot", "kind": "service", "label": "Pilot", "pages": ["svc-pilot", "loc-pilot"]},
                        {"id": "services", "kind": "service", "label": "Services", "pages": ["svc-lifts"], "route": "briefs"},
                        {"id": "locs", "kind": "location", "label": "Locations", "pages": LOCS, "route": "outline"}]}


def _ready(h, S_):
    ag = h.build_ready(S_, plan=_plan())
    st = h.status(S_)
    st["build"]["batches"] = [b for b in st["build"]["batches"] if b["id"] != "pilot"]   # no pilot (CM-061 §9)
    st["build"]["pilot_waived"] = True
    st["build"]["pilot_corrections_applied"] = {"at": "2026-10-14", "note": "test"}
    for b in st["build"]["batches"]:
        if b["id"] == "services":   # HMM: the services section finished on the old route
            b["state"] = "drafted"
    (ag.c / "status.json").write_text(json.dumps(st))
    return ag


def t_outline_route_walk(h):
    """The Phase 4 'done when': a locations section, approved plan → draft review sheet → one approval, no brief."""
    S_ = "r4-out-co"
    ag = _ready(h, S_)
    b = next(b for b in h.status(S_)["build"]["batches"] if b["id"] == "locs")
    h.check("r4: the plan records each section's route", b.get("route") == "outline", b)
    h.new_session()
    n = h.nxt(S_)
    h.check("r4: /next sends the outline-route section to ONE write run, no brief", n["command"] == f"/build {S_} write locs"
            and "no brief" in n["why"], n)
    rid = ag.start("build", "write", batch="locs")
    h.check("r4: the write run starts", bool(rid), ag.errors)
    f = ag.w("build/locs/briefs/LB-x.md", "# Brief\n\n## Evidence gaps\n- x\n")
    code, out = h.sh(f"python3 scripts/status.py page-stage {S_} loc-beaufort --stage brief --file {f} --run {rid}")
    h.check("r4: a brief is refused on the outline route", code == 4 and "outline route" in out, out)
    code, out = h.sh(f"python3 scripts/outline.py build {S_} locs --run {rid}")
    h.check("r4: no outline before the evidence gate has cleared the page", code == 0 and "0 outline(s)" in out, out)
    for p in LOCS:
        ag.write_facts(p)
    h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch locs")
    code, out = h.sh(f"python3 scripts/outline.py build {S_} locs --run {rid}")
    h.check("r4: outline.py writes one outline per page by script", code == 0 and "2 outline(s) written by script" in out, out)
    o = (ag.c / "build/locs/outlines/loc-beaufort.md").read_text()
    h.check("r4: the outline carries the spec's element order, plan values, links and the claims list",
            "## Page order" in o and "Local context" in o and "stair lifts Beaufort SC" in o
            and "Stair Lifts (https://test.example/stair-lifts/)" in o and "Bluffton, SC" in o
            and "## Claims" in o and " confirmed · " in o and "### Unknown" in o and "## The writer reports" in o, o[:1500])
    h.check("r4: a plan value the Brand Guide cannot give by formula is left to the writer and the review sheet",
            "Open — the Brand Guide gives no formula input" in o
            and "H1" in o.split("Open — the Brand Guide gives no formula input")[1].split("\n")[0], o[:900])
    pk = (ag.c / "build/locs/packs/loc-beaufort.md").read_text()
    h.check("r4: the pack shows the writer three fact states, never the statuses",
            "### Confirmed — a plain claim" in pk and "### Sourced public" in pk and "### Unknown" in pk
            and "| Id | Fact | Status |" not in pk, pk[:1200])
    code, out = h.sh(f"python3 scripts/outline.py show {S_} loc-beaufort")
    h.check("r4: outline.py show says the outline is current", code == 0 and "current" in out and "STALE" not in out, out)
    code, out = h.paul(f"/approve {S_} batch:locs:briefs")
    h.check("r4: there is no briefs approval on the outline route", code != 0 and "outline route" in out, out)
    code, out = h.sh(f"python3 scripts/status.py writeback {S_} locs --run {rid}")
    h.check("r4: the write-back waits for the drafts", code == 4 and "outline route" in out, out)
    for i, p in enumerate(LOCS):
        d = ag.w(f"build/locs/drafts/{p}.md", f"# Stair Lift Installer in {p}\n\nDraft text for {p}.\n")
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {p} --stage draft --file {d} --run {rid} --agent a{i}")
        h.check(f"r4: the draft of {p} is recorded with no brief (its own subagent)", code == 0, out)
    rows = [{"page": p, "rule": "R4-chosen", "item": "H1", "severity": "fix_and_list", "category": "plan",
             "finding": "H1 chosen by the writer", "plain_why": "the plan fixed no H1",
             "decided_for_you": f"H1 'Stair Lift Installer in {p}'"} for p in LOCS]
    fj = ag.w("build/locs/drafts-findings.json", json.dumps(rows))
    code, out = h.sh(f"python3 scripts/review.py sheet {S_} locs drafts --findings {fj} --run {rid}")
    h.check("r4: one draft review sheet for the section", code == 0, out)
    code, out = h.sh(f"python3 scripts/status.py batch {S_} locs --state drafts_written "
                     f"--review-sheet clients/{S_}/build/locs/drafts-review.csv")
    h.check("r4: the section is recorded as written, with no brief approval", code == 0, out)
    code, out = h.sh(f"python3 scripts/review.py apply {S_} locs drafts --run {rid}")
    h.check("r4: the review with no Ask rows is applied at once", code == 0, out)
    for i, p in enumerate(LOCS):
        h.sh(f"python3 scripts/status.py page-stage {S_} {p} --stage draft --file clients/{S_}/build/locs/drafts/{p}.md "
             f"--run {rid} --agent a{i}")
    code, out = h.sh(f"python3 scripts/status.py writeback {S_} locs --run {rid}")
    h.check("r4: the write-back runs from the reviewed drafts, before the approval", code == 0, out)
    ag.fin(rid, "outlines, drafts, review, write-back")
    st = h.status(S_)
    h.check("r4: the write run finished (outline + draft per page from this run)",
            rid not in (st.get("open_runs") or {}), st.get("open_runs"))
    h.new_session()
    n = h.nxt(S_)
    h.check("r4: /next ends at ONE approval line for the section's drafts", n["kind"] == "decision"
            and n["command"].startswith(f"/approve {S_} batch:locs:drafts") and ":briefs" not in n["command"], n)
    code, out = h.paul(f"/approve {S_} batch:locs:drafts")
    h.check("r4: Paul's one line approves the section", code == 0, out)
    log = (ag.c / "log.md").read_text()
    h.check("r4: no brief was written or recorded; the log names the outlines",
            "- OUTLINES" in log and "- BRIEF " not in log and "from its reviewed drafts" in log, log[-1500:])


def t_routes_migration(h):
    """D5: on /next, sections with briefs approved or under way keep the brief route; the rest take the outline route;
    a pilot noted 'No corrections' is recorded as clean."""
    S_ = "r4-mig-co"
    ag = _ready(h, S_)
    st = h.status(S_)
    for b in st["build"]["batches"]:
        b.pop("route", None)
        if b["id"] == "services":
            b["briefs"] = {"state": "approved", "by": "Paul", "at": "2026-10-14", "files": {}}
    st.pop("rewrite4_routes", None)
    st["build"]["pilot_corrections_applied"] = {"at": "2026-10-14", "note": "No corrections from Paul (accept all)"}
    (ag.c / "status.json").write_text(json.dumps(st))
    cfg = json.loads((h.SB / "config.json").read_text())
    cfg["build_route"] = "outline"   # a real install: no build_route set → outline
    (h.SB / "config.json").write_text(json.dumps(cfg))
    try:
        h.new_session()
        h.nxt(S_)
    finally:
        cfg["build_route"] = "briefs"
        (h.SB / "config.json").write_text(json.dumps(cfg))
    st = h.status(S_)
    r = {b["id"]: b.get("route") for b in st["build"]["batches"]}
    h.check("r4 D5: briefs approved → brief route; untouched → outline route", r == {"services": "briefs", "locs": "outline"}, r)
    h.check("r4 D5: the pilot noted 'No corrections' is recorded as clean",
            (st["build"].get("pilot_corrections_applied") or {}).get("none") is True, st["build"].get("pilot_corrections_applied"))
    log = (ag.c / "log.md").read_text()
    h.check("r4 D5: the migration is logged once", log.count("MIGRATION") >= 2 and "Rewrite 4" in log, log[-800:])
    st["build"]["batches"][0]["route"] = None
    (ag.c / "status.json").write_text(json.dumps(st))
    h.nxt(S_)
    h.check("r4 D5: it runs once per client", h.status(S_)["build"]["batches"][0].get("route") is None)


def t_clean_pilots(h):
    """CM-061 §9 (Rewrite 4): three clean pilots at today's writing rules end the pilot for the next client's first
    section; one with corrections keeps it."""
    code, fp = h.sh("python3 -c \"import sys; sys.path.insert(0, 'scripts'); import status; print(status.writing_fp())\"")
    fp = fp.strip().splitlines()[-1]
    ind = "stairlifts-r4"
    for i in range(3):
        s = f"r4-clean-{i}"
        code, out = h.sh(f'python3 scripts/status.py init {s} --name "C{i}" --domain c{i}.example --type full --industry {ind} --category none')
        h.check(f"r4 §9: client {s} set up", code == 0, out)
        st = h.status(s)
        st["build"] = {"batches": [{"id": "pilot", "kind": "service", "label": "Pilot", "pages": [], "state": "drafted",
                                    "drafts": {"state": "approved", "by": "Paul", "at": f"2099-01-0{i + 1}T00:00:00",
                                               "writing_fp": fp, "files": {}}}],
                       "pilot_corrections_applied": {"at": "2099-01-01", "note": "none", "none": True}}
        (h.SB / f"clients/{s}/status.json").write_text(json.dumps(st))
    S_ = "r4-clean-new"
    h.sh(f'python3 scripts/status.py init {S_} --name "New" --domain new.example --type full --industry {ind} --category none')
    code, out = h.sh(f"python3 scripts/status.py pilot {S_}")
    h.check("r4 §9: no pilot once the last 3 clients' pilots had no corrections at unchanged rules",
            "not needed" in out and "last 3 clients" in out, out)
    st = h.status("r4-clean-2")
    st["build"]["pilot_corrections_applied"].pop("none")
    (h.SB / "clients/r4-clean-2/status.json").write_text(json.dumps(st))
    code, out = h.sh(f"python3 scripts/status.py pilot {S_}")
    h.check("r4 §9: one pilot with corrections among the last 3 → the pilot stays", "pilot needed" in out, out)


SCENARIOS = [t_outline_route_walk, t_routes_migration, t_clean_pilots]
