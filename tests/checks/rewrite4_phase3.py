"""Rewrite 4 Phase 3 — the slim audit (CM-063): the redirect pre-screen (pagedec.py screen: CM-019 C1–C3 per URL),
S15 as triage (conformance.py triage: rebuild / light fix / keep, no scorecards), the audit on CM-061 with one review
sheet (review.py sheet|apply <slug> audit, the client's confirm list, the reviewer's scope), the blocker checklist at
the audit, D3 (audit_approved on its own), fan-out off by default (D6) and the audit read list under 25 KB.

Proved on HMM's saved audit (tests/fixtures/hmm/audit, copied read-only): the screen passes all 36 decided 301s and
fails exactly the 7 rows the S17 reviewer withdrew."""
import csv
import json
import shutil
from pathlib import Path

DOMAIN = "homemobilemedical.com"
GBP_FACT = "a-exact-url-in-the-gbp-website-field"


def _fx(h, name):
    return h.SB / "tests" / "fixtures" / "hmm" / "audit" / name


def _read(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _write(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _hmm(h, slug, map_rows=None, findings=True):
    """A client holding HMM's saved audit data: the map (or the rows given), rankings, backlinks, citations, the crawl,
    the URL inventory and the GBP website fact. Returns (agent, run id, audit dir)."""
    h.sh(f'python3 scripts/status.py init {slug} --name "Hmm Co" --domain {DOMAIN} --type full --industry "stair lifts" '
         "--category none")
    ag = h.Agent(slug)
    ag.fin(ag.start("new-client"), "set up")
    a = ag.c / "audit" / "2026-10-07"
    (a / "inventories").mkdir(parents=True, exist_ok=True)
    if map_rows is None:
        shutil.copyfile(_fx(h, "url-decision-map.csv"), a / "url-decision-map.csv")
    else:
        _write(a / "url-decision-map.csv", map_rows)
    if findings:
        shutil.copyfile(_fx(h, "findings.csv"), a / "findings.csv")
    shutil.copyfile(_fx(h, "url-inventory.csv"), a / "inventories" / "url-inventory.csv")
    (ag.c / "data" / "rankings").mkdir(parents=True, exist_ok=True)
    (ag.c / "data" / "backlinks").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_fx(h, "url-rankings.csv"), ag.c / "data" / "rankings" / "url-rankings.csv")
    shutil.copyfile(_fx(h, "backlinks-per-url.csv"), ag.c / "data" / "backlinks" / "backlinks-per-url.csv")
    (ag.c / "inputs").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_fx(h, "citation-tracker.csv"), ag.c / "inputs" / "Hmm Co - BL - citation-tracker - 2026-09-28.csv")
    shutil.copytree(h.SB / "tests" / "fixtures" / "hmm" / "crawl", ag.c / "inputs" / "crawl", dirs_exist_ok=True)
    rid = ag.start("crawl")
    ag.sh(f'python3 scripts/run.py fact {slug} {rid} --id {GBP_FACT} --value "https://{DOMAIN}/" --status client_confirmed '
          '--source "GBP dashboard (test)" --section A --label "Exact URL in the GBP website field"')
    return ag, rid, a


def _first_revision(h):
    """HMM's URL Decision Map as the analysis first wrote it, before the S17 reviewer's superseding rows."""
    first = {}
    for r in _read(_fx(h, "url-decision-map.csv")):
        first.setdefault(r["URL ID"], r)
    return list(first.values())


def _screen(ag):
    return {r["url"]: r for r in _read(next((ag.c / "audit").glob("*/redirect-screen.csv")))}


# ------------------------------------------------------------------ 1 · the redirect pre-screen on HMM's data
def t_hmm_screen(h):
    S = "p3-screen"
    ag, rid, a = _hmm(h, S)
    code, out = h.sh(f"python3 scripts/pagedec.py screen {S} --run {rid} --check")
    sc = _screen(ag)
    full = _read(_fx(h, "url-decision-map.csv"))
    decided = {r["Current URL"] for r in full if r["Proposed Action"].startswith("Redirect (301)")}
    h.check("phase3 HMM: the screen passes all 36 decided 301s on CM-019 C1–C3 (rankings, backlinks, GBP, citations)",
            code == 0 and len(decided) == 36 and all(sc[u]["result"] == "pass" for u in decided),
            [(u, sc.get(u, {}).get("result")) for u in decided if sc.get(u, {}).get("result") != "pass"])
    h.check("phase3 HMM: HMM's final map (after the review) has no destructive row on a failing URL — --check passes",
            code == 0 and "every destructive row passes the screen" in out, out)
    rv = _read(_fx(h, "review-s17.csv"))
    withdrawn = sorted(r["id"] for r in rv if r["register"] == "url-map" and r["outcome"].startswith("withdrawn"))
    ag2_slug = "p3-screen-rev1"
    ag2, rid2, _ = _hmm(h, ag2_slug, _first_revision(h))
    code, out = h.sh(f"python3 scripts/pagedec.py screen {ag2_slug} --run {rid2} --check")
    refused = sorted(l.split()[1] for l in out.splitlines() if l.startswith("REFUSED U-"))
    h.check("phase3 HMM: on the map as first written, --check refuses exactly the 7 rows the reviewer withdrew (exit 4)",
            code == 4 and len(withdrawn) == 7 and refused == withdrawn, (refused, withdrawn, out[-600:]))
    sc2 = _screen(ag2)
    why = {r["URL ID"]: sc2[r["Current URL"]] for r in _first_revision(h) if r["URL ID"] in withdrawn}
    h.check("phase3 HMM: the reasons are the reviewer's — five fail C1 (rankings), two fail C2+C3 (marketersmedia, a "
            "tracked citation, links there)",
            sum(w["c1"] == "fail" for w in why.values()) == 5
            and sorted(k for k, w in why.items() if w["c2"] == "fail" and w["c3"] == "fail") == ["U-088", "U-094"]
            and all("marketersmedia" in why[k]["c3_detail"] for k in ("U-088", "U-094")), why)
    first = _first_revision(h)
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    import pagedec
    dest = [r for r in first if pagedec.destructive(r["Proposed Action"])]
    h.check("phase3 HMM: of the 43 destructive rows first written, the screen settles every one with no agent — 36 pass "
            "(the decided 301s), 7 fail (the withdrawals), 0 needs evidence",
            len(dest) == 43 and sum(sc2[r["Current URL"]]["result"] == "pass" for r in dest) == 36
            and sum(sc2[r["Current URL"]]["result"] == "fail" for r in dest) == 7,
            [(r["URL ID"], sc2[r["Current URL"]]["result"]) for r in dest])
    h.check("phase3: the homepage fails C3 — the GBP website field points there", sc[f"https://{DOMAIN}/"]["c3"] == "fail")
    md = next((ag.c / "audit").glob("*/redirect-screen.md")).read_text()
    ch = [json.loads(l) for l in (ag.c / "changes.jsonl").read_text().splitlines() if l.strip()]
    h.check("phase3: the screen writes its Markdown summary and logs one change in the run",
            "CM-019 conditions 1–3" in md and any(c["kind"] == "audit_screen" and c["run_id"] == rid for c in ch), md[:400])
    ag.fin(rid, "screen")
    ag2.fin(rid2, "screen")


def t_screen_sources(h):
    """A source not on file → needs evidence (the agent's row); Search Console clicks or GA4 sessions are value (C1)."""
    S = "p3-src"
    ag, rid, a = _hmm(h, S)
    (ag.c / "data" / "rankings" / "url-rankings.csv").unlink()
    h.sh(f"python3 scripts/pagedec.py screen {S}")
    sc = _screen(ag)
    u = f"https://{DOMAIN}/services/power-chairs/"
    h.check("phase3: no rankings pull on file → C1 is needs evidence, never pass (the agent decides the row)",
            sc[u]["c1"] == "needs evidence" and sc[u]["result"] == "needs evidence" and sc[u]["decided_by"] == "agent", sc[u])
    shutil.copyfile(_fx(h, "url-rankings.csv"), ag.c / "data" / "rankings" / "url-rankings.csv")
    (ag.c / "inputs" / "Hmm Co - GSC - pages - 2026-10-01.csv").write_text(
        "Top pages,Clicks,Impressions\nhttps://homemobilemedical.com/services/power-chairs/,3,140\n"
        "https://homemobilemedical.com/services/scooter-lifts/,0,12\n")
    (ag.c / "inputs" / "Hmm Co - GA4 - landing-pages - 2026-10-01.csv").write_text(
        "Landing page,Sessions\n/services/mobility-ramps/,4\n")
    h.sh(f"python3 scripts/pagedec.py screen {S}")
    sc = _screen(ag)
    h.check("phase3: Search Console clicks and GA4 sessions count as value under C1 — those URLs fail; 0 clicks passes",
            sc[u]["c1"] == "fail" and "3 clicks" in sc[u]["c1_detail"]
            and sc[f"https://{DOMAIN}/services/mobility-ramps/"]["c1"] == "fail"
            and sc[f"https://{DOMAIN}/services/scooter-lifts/"]["result"] == "pass", (sc[u], sc[f"https://{DOMAIN}/services/scooter-lifts/"]))
    ag.fin(rid, "screen sources")


# ------------------------------------------------------------------ 2 · S15 triage
def t_triage(h):
    S = "p3-triage"
    ag, rid, a = _hmm(h, S)
    blog = "https://homemobilemedical.com/are-stair-lifts-covered-by-medicare-medicaid-or-health-insurance/"
    (ag.c / "audit" / "conformance.csv").write_text(
        f"page,url,type,check,result,detail\n{blog},{blog},blog post,COM-T,FAIL,72 characters\n")
    code, out = h.sh(f"python3 scripts/conformance.py triage {S} --run {rid}")
    rows = _read(a / "url-decision-map.csv")
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    from render import latest
    last = {r["URL ID"]: r for r in latest(rows, key="URL ID", rev="ext_revision")}
    by = lambda pred: {r["Conformance Triage"] for r in last.values() if pred(r)}
    h.check("phase3 triage: one column, written by the script, with only rebuild / light fix / keep (or blank for a URL "
            "that is going or held)",
            code == 0 and "Conformance Triage" in rows[0] and {r["Conformance Triage"] for r in rows} <= {"rebuild", "light fix", "keep", ""},
            out)
    h.check("phase3 triage: pages Build rewrites are rebuild (service and location pages the map improves)",
            by(lambda r: r["Page Type"] in ("service", "location") and r["Proposed Action"].startswith("Improve")) == {"rebuild"},
            by(lambda r: r["Page Type"] in ("service", "location")))
    h.check("phase3 triage: redirected and held URLs get no triage",
            by(lambda r: r["Proposed Action"].startswith(("Redirect (301)", "Hold", "Keep existing 301"))) == {""})
    h.check("phase3 triage: a kept blog post with a failed check is light fix, the others keep",
            last[next(k for k, r in last.items() if r["Current URL"] == blog)]["Conformance Triage"] == "light fix"
            and "keep" in by(lambda r: r["Page Type"] == "blog post"))
    code, out = h.sh(f"python3 -c \"import sys; sys.path.insert(0,'scripts'); import conformance as C, json; "
                     f"print(json.dumps([[u, t] for u, t, s in C.scoring_set('{S}')]))\"")
    scored = json.loads(out.strip().splitlines()[-1]) if code == 0 else []
    types = sorted({t for _, t in scored})
    h.check("phase3 triage: only pages Build will not rewrite are scored in full — the 21 blog posts and the homepage "
            "under the H1 lock (HP-08); never a service or location page Build rebuilds",
            sum(t == "blog post" for _, t in scored) == 21 and "homepage" in types
            and not any(t in ("service", "location", "about") for _, t in scored), (len(scored), types))
    tri = _read(ag.c / "audit" / "conformance-triage.csv")
    h.check("phase3 triage: conformance-triage.csv says why and which checks failed",
            any(r["triage"] == "light fix" and "COM-T" in r["failed_checks"] for r in tri), tri[:3])
    ag.fin(rid, "triage")


# ------------------------------------------------------------------ 3 · the audit's one review sheet
def _undecided(h):
    """HMM's final map with Paul's decisions cleared on the 36 redirects — the map as it stands before the sheet."""
    rows = _read(_fx(h, "url-decision-map.csv"))
    for r in rows:
        if r["Proposed Action"].startswith("Redirect (301)"):
            r["Paul Decision"] = ""
    return rows


def t_audit_sheet(h):
    S = "p3-sheet"
    ag, rid, a = _hmm(h, S, _undecided(h))
    code, out = h.sh(f"python3 scripts/review.py sheet {S} audit --run {rid}")
    data = json.loads((a / "audit-review.json").read_text())
    rows = data["rows"]
    k1 = [r for r in rows if r["severity"] == "ask" and r["kind"] == "1"]
    h.check("phase3 sheet: each of the 36 undecided redirects is one kind-1 Ask, recommended 'a' (the 301, once the client "
            "confirms no leads) because the screen passes it",
            code == 0 and len(k1) == 36 and all(r["recommended"] == "a" for r in k1)
            and all("screen pass" in r["finding"] for r in k1), (out, len(k1)))
    cq = _read(a / "client-questions.csv")
    h.check("phase3 sheet: CM-019 C4 is asked once, for all 36, on the client list (client-questions.csv) — the only "
            "thing the client sees",
            len(cq) == 1 and "36 page(s)" in cq[0]["question"] and cq[0]["searched"], cq)
    fl = [r for r in rows if r["severity"] == "fix_and_list"]
    h.check("phase3 sheet: an older High/Medium register maps onto Fix and list (decided for you); Low rows are Fix — "
            "they go to the blocker checklist, never the sheet",
            len(fl) > 0 and data["fixes"] > 0 and all(r["decided_for_you"] for r in fl), (len(fl), data["fixes"]))
    st = h.status(S)
    h.check("phase3 sheet: status.json records the sheet, not yet applied; log.md has one REVIEW SHEET line",
            st["audit_review"]["asks"] == 37 and st["audit_review"]["client"] == 1 and st["audit_review"]["applied"] is None
            and "REVIEW SHEET" in (ag.c / "log.md").read_text(), st.get("audit_review"))
    # the approval follows the applied sheet
    ag.mark("audit_deliverables", f"clients/{S}/audit/2026-10-07/audit-review.csv")
    code, out = h.paul(f"/approve {S} audit_approved", expect_ok=False)
    h.check("phase3 sheet: /approve audit_approved is refused while the sheet is not applied",
            code != 0 and "not applied yet" in out, out)
    code, out = h.sh(f'python3 scripts/review.py apply {S} audit --run {rid} --answers "accept all except 1b"')
    items = json.loads((a / "audit-apply.json").read_text())["items"]
    after = _read(a / "url-decision-map.csv")
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    from render import latest
    last = {r["URL ID"]: r for r in latest(after, key="URL ID", rev="ext_revision")}
    first_id = k1[0]["page"]
    h.check("phase3 apply: each decided URL gets one superseding map row with Paul's decision; '1b' keeps that URL live "
            "(no redirect, no target)",
            code == 0 and len(after) == len(_undecided(h)) + 36
            and last[first_id]["Proposed Action"].startswith("Keep live") and not last[first_id]["Target URL"]
            and "Paul" in last[first_id]["Paul Decision"]
            and all("default accepted" in last[r["page"]]["Paul Decision"] for r in k1[1:]), (out, last[first_id]))
    c4 = [i for i in items if i["choice"] is None]
    h.check("phase3 apply: the client's C4 question is never taken by default — it waits for the client",
            len(c4) == 1 and "waiting for the client" in c4[0]["by"], c4)
    code, out = h.sh(f"python3 scripts/pagedec.py screen {S} --check")
    h.check("phase3 apply: the decided map still passes the screen check", code == 0, out)
    h.check("phase3 apply: the sheet is applied (the approval may follow)", h.status(S)["audit_review"]["applied"] is not None)
    new = dict(after[-1]) | {"URL ID": "U-999", "Current URL": f"https://{DOMAIN}/services/old-scooter-page/",
                             "Proposed Action": "Redirect (301)", "Target URL": f"https://{DOMAIN}/services/stair-lifts/",
                             "Paul Decision": ""}
    with open(a / "url-decision-map.csv", "a", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=list(after[0])).writerow(new)
    h.sh(f"python3 scripts/pagedec.py screen {S}")
    code, out = h.sh(f"python3 scripts/review.py sheet {S} audit --run {rid}")
    k1b = [r for r in json.loads((a / "audit-review.json").read_text())["rows"] if r["kind"] == "1"]
    h.check("phase3 sheet: decided URL rows are not asked again, and a new URL row is never mistaken for a settled one "
            "(url_U-999 is not url_U-009)",
            code == 0 and [r["page"] for r in k1b] == ["U-999"], (out, [r["page"] for r in k1b]))
    h.sh(f'python3 scripts/review.py apply {S} audit --run {rid} --answers "accept all"')
    # render: the deliverables
    code, out = h.sh(f"python3 scripts/render.py all {S} --run {rid}")
    dl = sorted(p.name for p in (a / "deliverables").glob("*.md"))
    sheet = (a / "deliverables" / "Hmm Co - Audit Review Sheet - REVIEW.md").read_text()
    h.check("phase3 render: the deliverables are the audit review sheet, the URL Decision Map view and the Evidence "
            "Manifest — no Recommendations document, no Markdown Finding Register",
            not any("Recommendations" in n or "Finding Register" in n for n in dl) and "Hmm Co - Audit Review Sheet - REVIEW.md" in dl,
            (dl, out))
    h.check("phase3 render: the sheet view has Paul's questions, the client's list and what was decided for him",
            "## Questions for Paul (1)" in sheet and "old-scooter-page" in sheet and "## For the client to confirm (1)" in sheet and "## Decided for you" in sheet
            and "Redirect pre-screen" in sheet, sheet[:1200])
    bl = (ag.c / "build" / "Hmm Co - Technical Blocker Checklist - REVIEW.md").read_text()
    h.check("phase3 render: the blocker checklist is written at the audit from the Fix rows (S16)",
            "## 1 · Fix — the VA" in bl and "Written at the audit (S16)" in bl, bl[:600])
    ag.fin(rid, "audit sheet")


def t_sheet_refusals(h):
    S = "p3-refuse"
    ag, rid, a = _hmm(h, S, _first_revision(h), findings=False)
    code, out = h.sh(f"python3 scripts/review.py sheet {S} audit --run {rid}")
    h.check("phase3 sheet: refused while a destructive row sits on a URL the screen fails (the reviewer's withdrawals)",
            code == 4 and "U-080" in out and "U-094" in out and not (a / "audit-review.csv").exists(), out[-500:])
    S2 = "p3-badask"
    ag2, rid2, a2 = _hmm(h, S2, _undecided(h), findings=False)
    cols = ["Finding ID", "Category", "Affected URL / Entity", "Observation", "Evidence / Locator", "Recommendation",
            "Priority", "Status", "ext_revision", "ext_ask_kind", "ext_options", "ext_default", "ext_searched"]
    _write(a2 / "findings.csv", [
        dict.fromkeys(cols, "") | {"Finding ID": "F-001", "Priority": "Ask", "ext_ask_kind": "3", "Observation": "Licence?",
                                   "ext_options": "a) licensed · b) not licensed", "ext_default": "a", "ext_revision": "1"}])
    code, out = h.sh(f"python3 scripts/review.py sheet {S2} audit --run {rid2}")
    h.check("phase3 sheet: a client question without its searched: line is refused (questions.py rule)",
            code == 4 and "searched" in out, out[-300:])
    _write(a2 / "findings.csv", [
        dict.fromkeys(cols, "") | {"Finding ID": "F-001", "Priority": "Ask", "ext_ask_kind": "9", "Observation": "Tone?",
                                   "ext_options": "a) warmer · b) as is", "ext_default": "a", "ext_revision": "1"}])
    code, out = h.sh(f"python3 scripts/review.py sheet {S2} audit --run {rid2}")
    rows = json.loads((a2 / "audit-review.json").read_text())["rows"] if code == 0 else []
    h.check("phase3 sheet: a question that is not one of the four Ask kinds is decided by default (Fix and list)",
            code == 0 and any(r["page"] == "F-001" and r["severity"] == "fix_and_list" for r in rows), out[-300:])
    ag.fin(rid, "refusals")
    ag2.fin(rid2, "refusals")


# ------------------------------------------------------------------ 4 · the reviewer's scope
def t_reviewer_scope(h):
    S = "p3-scope"
    ag, rid, a = _hmm(h, S, _undecided(h))
    code, out = h.sh(f"python3 scripts/review.py scope {S} audit")
    rows = _read(a / "review-scope.csv")
    dest = [r for r in rows if r["why"] == "destructive"]
    asks = [r for r in rows if r["why"] == "ask"]
    sample = [r for r in rows if r["why"] == "sample"]
    finds = {r["Finding ID"] for r in _read(_fx(h, "findings.csv"))}
    h.check("phase3 S17: the reviewer opens every destructive URL row (36), every Ask finding and a sample of the rest — "
            "not every finding",
            code == 0 and len(dest) == 36 and asks and 5 <= len(sample) < len(finds) - len(asks)
            and len({r["id"] for r in asks + sample}) < len(finds), (len(dest), len(asks), len(sample), len(finds)))
    ag.fin(rid, "scope")


# ------------------------------------------------------------------ 5 · D3, D6, the read list
def t_d3_and_reads(h):
    g = json.loads((h.SB / "scripts" / "gates.json").read_text())
    h.check("phase3 D3: audit_approved no longer rides with brand_guide_approved; the blocker step and its condition "
            "need only the audit; the discovery sign-off still needs both",
            "with" not in g["gates"]["brand_guide_approved"] and g["steps"]["build:blockers"]["gates"] == ["audit_approved"]
            and g["conditions"]["blockers_cleared"]["requires"] == ["audit_approved"]
            and {"audit_approved", "brand_guide_approved"} <= set(g["conditions"]["discovery_signed_off"]["requires"])
            and g["change_kinds"]["alt_text"]["gate"] == "audit_approved"
            and "blocker_checklist" in g["steps"]["discovery:audit"]["produces"]
            and "discovery:review" in g["steps"])
    import glob
    total, seen = 0, []
    for r in g["steps"]["discovery:audit"]["reads"]:
        path = r.split(" ")[0]
        if path.startswith(("clients/", "python3")) or "/" not in path:
            continue
        for f in glob.glob(str(h.SB / path)):
            total += Path(f).stat().st_size
            seen.append(Path(f).name)
    h.check(f"phase3: the audit's read list (system files) is under 25 KB — {total} bytes (was about 66 KB)",
            total < 25_000 and "SKILL.md" in seen and not any("gate-b" in s or s.startswith(("location", "service")) for s in seen),
            (total, seen))
    src = (h.SB / "scripts" / "pipeline.py").read_text()
    h.check("phase3 D6: query fan-out is off by default (--fanout is a store_true flag)",
            'ap.add_argument("--fanout", action="store_true"' in src)


def t_d3_next(h):
    """/next shows the audit review, then the audit approval on its own while the client's facts are still out (D3)."""
    S = "p3-next"
    ag, rid, a = _hmm(h, S, _undecided(h))
    h.sh(f"python3 scripts/review.py sheet {S} audit --run {rid}")
    p = ag.c / "status.json"
    st = json.loads(p.read_text())
    for g in ("entity_approved", "proof_sheet_approved"):
        st["gates"][g] = {"state": "approved", "by": "Paul", "at": "2026-10-20T00:00", "files": {}}
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    import steps as STP
    for r in STP.registry():
        st["audit_steps"].setdefault(r["id"], {"outcome": "done", "reason": "", "outputs": [], "at": "2026-10-20", "run": rid})
    p.write_text(json.dumps(st))
    ag.mark("audit_deliverables", f"clients/{S}/audit/2026-10-07/audit-review.csv")
    ag.fin(rid, "audit")
    nxt = h.nxt(S)
    h.check("phase3 /next: the unapplied audit review sheet comes first — one answer line for Paul",
            nxt.get("kind") == "decision" and nxt.get("command", "").startswith(f"/discovery {S} review"), nxt)
    rid2 = ag.start("discovery", "review")
    code, out = h.sh(f'python3 scripts/review.py apply {S} audit --run {rid2} --answers "accept all"')
    ag.fin(rid2, "audit review applied")
    h.check("phase3 /next: /discovery review runs as its own step (discovery:review) and applies the sheet",
            rid2 is not None and code == 0 and h.status(S)["audit_review"]["applied"], (rid2, out, ag.errors[-2:]))
    nxt = h.nxt(S)
    h.check("phase3 D3: with the client's facts still out, /next offers /approve audit_approved on its own (not with "
            "brand_guide_approved)",
            nxt.get("kind") == "decision" and "audit_approved" in nxt.get("command", "")
            and "brand_guide_approved" not in nxt.get("command", ""), nxt)


SCENARIOS = [t_hmm_screen, t_screen_sources, t_triage, t_audit_sheet, t_sheet_refusals, t_reviewer_scope,
             t_d3_and_reads, t_d3_next]
