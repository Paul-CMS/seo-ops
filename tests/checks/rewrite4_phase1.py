"""Rewrite 4 Phase 1 — scripts take the clerical work: render.py (every Markdown deliverable from its CSV/JSON),
pipeline.py inventory (crawl → pulls → ingest → cross-checks → conformance → outcomes → render, no agent), the clerk
retired, script-written handoff lines with the agent's section capped at 25 lines, and outline.py assigning each page's
keyword, H1 and variants by formula when the site-plan row leaves them empty."""
import csv
import importlib.util
import json
import re
from pathlib import Path

FIND = ["Finding ID", "Stage", "Category", "Affected URL / Entity", "Observation", "Evidence / Locator", "Classification",
        "Confidence", "Alternative Explanation", "Recommendation", "Risk if Acted", "Risk if Deferred", "Dependency",
        "Client Confirmation Needed", "Paul Approval Needed", "Priority", "Status", "Owner", "Reviewer", "ext_revision"]
URLM = ["URL ID", "Current URL", "Page Type", "Main Entity / Intent", "Proposed Action", "Target URL", "Risk Tier",
        "Paul Decision", "Status", "ext_cm019_result", "ext_finding_ids"]
MAN = ["source_id", "file", "recognised_as", "category", "rows", "columns", "sha256_12", "file_modified", "tool_settings",
       "date_window", "geography_device", "scope_limits"]
SF = ["Address", "Content Type", "Status Code", "Indexability", "Title 1", "Canonical Link Element 1", "Word Count", "Crawl Depth"]


def _csv(cols, rows):
    out = [",".join(cols)]
    for r in rows:
        out.append(",".join('"' + str(r.get(c, "")).replace('"', '""') + '"' for c in cols))
    return "\n".join(out) + "\n"


def _client(h, slug, name="Rn Co"):
    h.sh(f'python3 scripts/status.py init {slug} --name "{name}" --domain test.example --type full --industry roofing')
    ag = h.Agent(slug)
    ag.fin(ag.start("new-client"), "set up")
    return ag


def _audit(h, ag):
    d = "audit/2026-10-07"
    ag.w(f"{d}/findings.csv", _csv(FIND, [
        {"Finding ID": "F-001", "Priority": "High", "Observation": "Title wrong", "Affected URL / Entity": "/", "Owner": "Build",
         "Recommendation": "Rebuild", "Status": "draft", "ext_revision": "1", "Evidence / Locator": "SRC-001"},
        {"Finding ID": "F-002", "Priority": "Low", "Observation": "Two hops", "Affected URL / Entity": "/a/", "Owner": "Jonie",
         "Recommendation": "Redirect straight", "Status": "draft", "ext_revision": "1"},
        {"Finding ID": "F-002", "Priority": "Low", "Observation": "Two hops (revised)", "Affected URL / Entity": "/a/", "Owner": "Jonie",
         "Recommendation": "Redirect straight", "Status": "reviewed", "ext_revision": "2"},
        {"Finding ID": "F-003", "Priority": "Medium", "Observation": "Claim unsourced", "Owner": "Paul",
         "Paul Approval Needed": "Yes", "Status": "draft", "ext_revision": "1"}]))
    ag.w(f"{d}/url-decision-map.csv", _csv(URLM, [
        {"URL ID": "U-001", "Current URL": "https://test.example/", "Page Type": "homepage", "Proposed Action": "Improve",
         "ext_cm019_result": "n/a"},
        {"URL ID": "U-002", "Current URL": "https://test.example/old/", "Page Type": "service", "Proposed Action": "Redirect (301)",
         "Target URL": "https://test.example/new/", "ext_cm019_result": "C1-C4 pass"},
        {"URL ID": "U-003", "Current URL": "https://test.example/x/", "Page Type": "service", "Proposed Action": "Redirect (301)",
         "Paul Decision": "approved 2026-10-09", "ext_cm019_result": "C1-C4 pass"}]))
    ag.w(f"{d}/00-manifest.csv", _csv(MAN, [
        {"source_id": "SRC-001", "file": "T - SF - internal_all - 2026-10-01.csv", "recognised_as": "screamingfrog.internal_all",
         "category": "crawl", "rows": "3", "sha256_12": "abc123abc123", "tool_settings": "SF free licence", "date_window": "2026-10-01"}]))
    ag.w(f"{d}/00-crosschecks.md", "# Cross-checks\n\n  [CONFIRMED] Host consistency\n")
    ag.w("build/site-plan.plan.json", json.dumps({
        "pages": [{"id": "svc-a", "type": "service", "name": "Stair Lifts", "url": "https://test.example/stair-lifts/", "keyword": "stair lifts"},
                  {"id": "loc-b", "type": "location", "name": "Beaufort, SC", "url": "https://test.example/beaufort-sc/"}],
        "batches": [{"id": "svc", "kind": "service", "label": "Services", "pages": ["svc-a"], "route": "outline"},
                    {"id": "loc", "kind": "location", "label": "Locations", "pages": ["loc-b"]}]}))


def t_render(h):
    S = "rn-co"
    ag = _client(h, S)
    code, out = h.sh(f"python3 scripts/render.py urlmap {S}")
    h.check("render: with no audit folder yet it says so and writes nothing", code != 0 and "no audit folder" in out, out)
    _audit(h, ag)
    for k in ("manifest", "urlmap", "findings", "auditsheet", "blockers", "siteplan"):
        code, out = h.sh(f"python3 scripts/render.py {k} {S}")
        h.check(f"render: {k} renders from its source files", code == 0 and "rendered from" in out, out)
    dl = ag.c / "audit/2026-10-07/deliverables"
    names = sorted(p.name for p in dl.glob("*.md"))
    h.check("render: the files carry the naming convention (<Client> - <Artifact> - REVIEW.md)",
            names == ["Rn Co - Audit Review Sheet - REVIEW.md", "Rn Co - Evidence Manifest - REVIEW.md",
                      "Rn Co - Finding Register - REVIEW.md", "Rn Co - URL Decision Map - REVIEW.md"]
            and (ag.c / "build/Rn Co - Technical Blocker Checklist - REVIEW.md").is_file()
            and (ag.c / "build/Rn Co - Site Plan - REVIEW.md").is_file(), names)
    man = (dl / "Rn Co - Evidence Manifest - REVIEW.md").read_text()
    h.check("render: the Evidence Manifest has sources, every step outcome and the cross-checks",
            "| SRC-001 |" in man and "## 2 · Step outcomes" in man and "NO OUTCOME" in man and "[CONFIRMED] Host consistency" in man
            and "Rendered, never edited" in man, man[:1500])
    um = (dl / "Rn Co - URL Decision Map - REVIEW.md").read_text()
    h.check("render: the URL Decision Map view counts the decisions and lists every row",
            "| Redirect (301) | 2 |" in um and "**Total** | **3**" in um and um.count("| U-00") == 3, um[:1500])
    fr = (dl / "Rn Co - Finding Register - REVIEW.md").read_text()
    h.check("render: the Finding Register shows the latest revision of each finding, High first",
            "Two hops (revised)" in fr and "| Two hops |" not in fr and fr.index("## High") < fr.index("## Medium") < fr.index("## Low"), fr)
    sheet = (dl / "Rn Co - Audit Review Sheet - REVIEW.md").read_text()
    h.check("render: the audit review sheet asks only about the undecided destructive row (U-003 is decided)",
            "Ask — Paul decides (1)" in sheet and "| U-002 |" in sheet and "| U-003 |" not in sheet
            and "F-003" in sheet.split("findings that need Paul")[1].split("##")[0], sheet[:1800])
    bl = (ag.c / "build/Rn Co - Technical Blocker Checklist - REVIEW.md").read_text()
    h.check("render: the blocker checklist splits High findings from the VA's rows",
            "## 1 · High findings (1)" in bl and "## 2 · Handed to the VA (1)" in bl and "F-002" in bl.split("## 2")[1], bl[:1500])
    sp = (ag.c / "build/Rn Co - Site Plan - REVIEW.md").read_text()
    h.check("render: the site plan view lists sections with their route and every page", "| svc | service | 1 | outline |" in sp
            and "Beaufort, SC" in sp and "stair lifts" in sp, sp)
    strip = lambda t: re.sub(r"Rendered \d{4}-\d\d-\d\dT\d\d:\d\d", "Rendered T", t)
    before = strip(fr)
    h.sh(f"python3 scripts/render.py findings {S}")
    h.check("render: the same sources give the same file (deterministic)", strip((dl / "Rn Co - Finding Register - REVIEW.md").read_text()) == before)
    code, out = h.sh(f"python3 scripts/render.py check {S}")
    h.check("render check: every rendered file is current", code == 0 and "current" in out, out)
    import os
    import time
    src = ag.c / "audit/2026-10-07/findings.csv"
    os.utime(src, (time.time() + 60, time.time() + 60))
    code, out = h.sh(f"python3 scripts/render.py check {S}")
    h.check("render check: a source newer than its rendered file is STALE (exit 4)", code == 4 and "STALE" in out and "findings.csv" in out, out)
    # an approved file is never rendered over
    st = h.status(S)
    rel = f"clients/{S}/audit/2026-10-07/deliverables/Rn Co - Finding Register - REVIEW.md"
    st["gates"]["audit_approved"] = {"state": "approved", "by": "Paul", "files": {rel: "x" * 12}}
    (ag.c / "status.json").write_text(json.dumps(st))
    before = (dl / "Rn Co - Finding Register - REVIEW.md").read_bytes()
    code, out = h.sh(f"python3 scripts/render.py findings {S}")
    h.check("render: a file an approval covers is refused (exit 4), not overwritten",
            code == 4 and "covered by an approval" in out and (dl / "Rn Co - Finding Register - REVIEW.md").read_bytes() == before, out)
    code, out = h.sh(f"python3 scripts/render.py all {S}")
    h.check("render all: the same refusal, never silently skipped", code == 4 and "covered by an approval" in out, out)
    scratch = h.SB / "scratch-render"
    code, out = h.sh(f"python3 scripts/render.py findings {S} --out {scratch}")
    h.check("render --out: looks at the new version in another folder; nothing in the client's folder changes",
            code == 0 and (scratch / "Rn Co - Finding Register - REVIEW.md").is_file()
            and (dl / "Rn Co - Finding Register - REVIEW.md").read_bytes() == before, out)
    rid = ag.start("crawl")
    code, out = h.sh(f"python3 scripts/render.py findings {S} --force --run {rid}")
    ch = [json.loads(l) for l in (ag.c / "changes.jsonl").read_text().splitlines() if l.strip()]
    h.check("render --force --run: re-rendered over the approval and logged as one change",
            code == 0 and any(c["kind"] == "rendered" and c["run_id"] == rid for c in ch), (out, ch[-2:]))
    ag.fin(rid, "rendered")


WRAP = r'''import json, os, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import pipeline
MODE = HERE / ".state" / "pl_mode.json"
LOG = HERE / ".state" / "pl_calls.log"
EST = {"crawl.py": "Estimate: up to $0.4000 for 20 pages", "reviews.py": "Google reviews: at most $0.0150",
       "rankings.py": "Total at most $0.1000", "paa.py": "5 queries = $0.0400 (all 5 would be $0.04)",
       "fanout.py": "10 seeds = $0.0700 · balance", "competitors.py": "competitor coverage: 5 SERP(s) → at most $0.0100",
       "dfs.py": "estimate $0.0600", "backlinks.py": ""}
real = pipeline.sh


def fake(argv, timeout=None):
    script = Path(argv[1]).name if len(argv) > 1 else ""
    slug_dir = HERE.parent / "clients" / sys.argv[1]
    if script in EST:
        sub = [a for a in argv[2:] if a in ("estimate", "run", "call", "text", "extract", "summary", "meaning", "route")]
        m = json.loads(MODE.read_text()) if MODE.exists() else {}
        with open(LOG, "a") as fh:
            fh.write(f"{script[:-3]} {sub[0] if sub else ''}\n")
        if sub and sub[0] == "estimate":
            return 0, EST[script]
        if script == "competitors.py" and sub and sub[0] == "run":
            Path(slug_dir, "data", "competitors").mkdir(parents=True, exist_ok=True)
            Path(slug_dir, "data", "competitors", "coverage.md").write_text("coverage\n")
        if m.get("fail") == script[:-3] and sub and sub[0] in ("run", "call"):
            return 1, "boom: the service said no"
        if m.get("busy") and script == "crawl.py" and sub[0] == "run":
            return 10, "STILL CRAWLING"
        return 0, "ok"
    return real(argv, timeout)


pipeline.sh = fake
sys.argv = ["scripts/pipeline.py", *sys.argv[1:]]
pipeline.main()
'''


def _pl(h, slug, extra, mode=None):
    st = h.SB / "tests" / ".state"
    st.mkdir(parents=True, exist_ok=True)
    (h.SB / "tests" / "pl_wrap.py").write_text(WRAP)
    (st / "pl_mode.json").write_text(json.dumps(mode or {}))
    return h.sh(f"python3 tests/pl_wrap.py {slug} inventory {extra}")


def _calls(h):
    p = h.SB / "tests" / ".state" / "pl_calls.log"
    return p.read_text().split("\n")[:-1] if p.exists() else []


def _pl_client(h, slug):
    ag = _client(h, slug, "Pl Co")
    ag.w("data/services.txt", "stair lifts\nporch lifts\n")
    ag.w("data/cities.txt", "Beaufort\nBluffton\n")
    ag.w("inputs/crawl/Pl Co - DFS - internal_all - 2026-10-01.csv", _csv(SF, [
        {"Address": f"https://test.example/{p}", "Content Type": "text/html", "Status Code": "200", "Indexability": "Indexable",
         "Title 1": "T", "Canonical Link Element 1": f"https://test.example/{p}", "Word Count": "300", "Crawl Depth": "1"}
        for p in ("", "a/", "b/")]))
    return ag


def t_pipeline_data(h):
    S = "pl-co"
    ag = _pl_client(h, S)
    log = h.SB / "tests" / ".state" / "pl_calls.log"
    log.unlink(missing_ok=True)
    rid = ag.start("crawl")
    code, out = _pl(h, S, f"--run {rid} --state SC")
    h.check("pipeline: with no --confirmed it prints ONE combined estimate and stops (exit 5)",
            code == 5 and "DataforSEO total ≈ $0.23" in out and "S05 " not in out and "CONFIRM" in out and out.count("\n") <= 3, out)
    h.check("pipeline: the estimate step made no paid call", all(c.endswith("estimate") for c in _calls(h)) and _calls(h), _calls(h))
    h.check("pipeline: fan-out is off by default (D6)", not any(c.startswith("fanout") for c in _calls(h)), _calls(h))
    log.unlink(missing_ok=True)
    code, out = _pl(h, S, f"--run {rid} --state SC --confirmed")
    runs = [c for c in _calls(h) if not c.endswith("estimate")]
    h.check("pipeline: --confirmed runs the steps in order, once each (the crawl on file is reused, not paid again)",
            code == 0 and runs == ["crawl text", "reviews run", "reviews extract", "reviews meaning", "rankings run",
                                   "dfs call", "backlinks summary", "paa run", "paa route", "competitors run"], (out, runs))
    steps = h.status(S).get("audit_steps") or {}
    h.check("pipeline: every outcome is recorded by the script — pulls done, the file-based steps skipped with a reason",
            all((steps.get(s) or {}).get("outcome") == "done" for s in ("S05b", "S06", "S07", "S08", "S19"))
            and all((steps.get(s) or {}).get("outcome") == "skipped" and steps[s].get("reason") for s in ("S09", "S10", "S11", "S20"))
            and "S21" not in steps and "S05" not in steps, steps)
    h.check("pipeline: it prints at most ten lines", out.count("\n") + 1 <= 10, out)
    log.unlink(missing_ok=True)
    code, out = _pl(h, S, f"--run {rid} --state SC --confirmed")
    h.check("pipeline: run again, everything under 60 days old is reused — no call at all",
            code == 0 and "nothing to pull" in out and _calls(h) == [], (out, _calls(h)))
    code, out = _pl(h, S, f"--run {rid} --state SC --fanout")
    h.check("pipeline: --fanout adds S21 to the estimate and waits for the yes (exit 5)",
            code == 5 and "S21 $0.07" in out and "CONFIRM" in out, out)
    code, out = _pl(h, S, f"--run {rid} --state SC --fanout --confirmed")
    h.check("pipeline: --fanout --confirmed runs only the new step",
            code == 0 and [c for c in _calls(h) if not c.endswith("estimate")] == ["fanout run", "fanout route"]
            and (h.status(S)["audit_steps"].get("S21") or {}).get("outcome") == "done", (out, _calls(h)))
    code, out = _pl(h, S, f"--state SC")
    h.check("pipeline: a run needs --run (or --dry)", code != 0 and "--run" in out, out)
    ag.fin(rid, "inventory data")
    # a failure stops the sequence: nothing after it runs, the outcome is recorded failed
    F = "pl-fail"
    ag2 = _pl_client(h, F)
    rid2 = ag2.start("crawl")
    log.unlink(missing_ok=True)
    code, out = _pl(h, F, f"--run {rid2} --state SC --confirmed", {"fail": "rankings"})
    runs = [c for c in _calls(h) if not c.endswith("estimate")]
    st2 = h.status(F).get("audit_steps") or {}
    h.check("pipeline: the first failure stops everything — exit code of the script, later steps not run, outcome failed",
            code == 1 and "STOPPED at S07" in out and "Not run: S08, S19" in out and "paa run" not in runs
            and (st2.get("S07") or {}).get("outcome") == "failed" and (st2.get("S06") or {}).get("outcome") == "done", (out, runs, st2))
    # a crawl still running is exit 10: run again, nothing else started
    B = "pl-busy"
    ag3 = _pl_client(h, B)
    rid3 = ag3.start("crawl")
    ag3.w("inputs/crawl/placeholder.txt", "x")
    for f in (ag3.c / "inputs/crawl").glob("*internal_all*"):
        f.rename(f.with_name("busy.keep"))
    log.unlink(missing_ok=True)
    code, out = _pl(h, B, f"--run {rid3} --state SC --confirmed", {"busy": True})
    h.check("pipeline: a crawl still running is exit 10 — run it again, no later step started",
            code == 10 and "STILL RUNNING" in out and [c for c in _calls(h) if not c.endswith("estimate")] == ["crawl run"], (out, _calls(h)))
    ag3.sh(f"python3 scripts/run.py abort {B} {rid3} --reason test")
    ag2.sh(f"python3 scripts/run.py abort {F} {rid2} --reason test")


def t_pipeline_audit(h):
    S = "pl-aud"
    ag = _pl_client(h, S)
    rid = ag.start("crawl")
    code, out = _pl(h, S, f"--run {rid} --phase audit")
    ad = ag.c / "audit"
    dirs = sorted(p for p in ad.glob("*") if p.is_dir())
    h.check("pipeline audit: S12 runs the ingest, the cross-checks and conformance with no agent",
            code == 0 and "S12 done" in out and dirs and (dirs[-1] / "00-manifest.csv").is_file()
            and (dirs[-1] / "00-crosschecks.md").is_file() and (ad / "conformance.csv").is_file(), (out, dirs))
    h.check("pipeline audit: S12 is recorded and the Evidence Manifest is rendered from the manifest",
            (h.status(S)["audit_steps"].get("S12") or {}).get("outcome") == "done"
            and any((dirs[-1] / "deliverables").glob("*Evidence Manifest - REVIEW.md")), out)
    man = list(csv.DictReader(open(dirs[-1] / "00-manifest.csv", newline="", encoding="utf-8-sig")))
    man[0]["tool_settings"] = "Filled in by the audit"
    cols = list(man[0].keys())
    with open(dirs[-1] / "00-manifest.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(man)
    code, out = _pl(h, S, f"--run {rid} --phase audit")
    man2 = list(csv.DictReader(open(dirs[-1] / "00-manifest.csv", newline="", encoding="utf-8-sig")))
    h.check("pipeline audit: running it again keeps what the audit wrote in the setting columns of an unchanged file",
            code == 0 and man2[0]["tool_settings"] == "Filled in by the audit", (out, man2[0]))
    before = sorted(str(p.relative_to(ag.c)) for p in ag.c.rglob("*") if p.is_file())
    st0 = (ag.c / "status.json").read_text()
    out_dir = h.SB / "dry-out"
    code, out = h.sh(f"python3 scripts/pipeline.py {S} inventory --dry --out {out_dir}")
    h.check("pipeline --dry: reproduces the S12 outputs from the data on file, no paid call, nothing written in the client's folder",
            code == 0 and "dry run" in out and "reproduced identically" in out and "cross-checks: identical" in out
            and (out_dir / "00-manifest.csv").is_file()
            and before == sorted(str(p.relative_to(ag.c)) for p in ag.c.rglob("*") if p.is_file())
            and (ag.c / "status.json").read_text() == st0, out)
    ag.fin(rid, "inventory audit")


def t_clerk_retired(h):
    SB = h.SB
    g = json.loads((SB / "scripts" / "gates.json").read_text())
    agents = {a for s in g["stages"] for a in s["agents"]} | {r["agent"] for rows in g["models"].values() for r in rows}
    text = "\n".join(p.read_text() for d in ("docs", ".claude/agents", ".claude/commands") for p in (SB / d).glob("*.md"))
    h.check("clerk retired: no clerk agent file, no stage or model row names it, no agent or doc tells anyone to hand work to it",
            not (SB / ".claude/agents/clerk.md").exists() and "clerk" not in agents and "**clerk**" not in text
            and "to `clerk`" not in text, (agents, [m.start() for m in re.finditer("clerk", text)][:3]))
    h.check("clerk retired: the agents run scripts themselves and know the 25-line handoff cap",
            "never spawn an agent for it" in (SB / ".claude/agents/discovery-audit.md").read_text()
            and "25 lines at most" in (SB / ".claude/commands/build.md").read_text())


def t_handoff_cap_and_record(h):
    S = "hf-co"
    ag = _client(h, S, "Hf Co")
    rid = ag.start("crawl")
    ag.sh(f"python3 scripts/steps.py record {S} --run {rid} S05 done")
    ag.sh(f'python3 scripts/run.py change {S} {rid} --kind test --url u --field f --old a --new b --result ok')
    ag.sh(f'python3 scripts/run.py decision {S} {rid} --text "chose A"')
    big = ag.w(f"handoffs/run-{rid}.md", "\n".join(f"- line {i}" for i in range(26)) + "\n")
    code, out = h.sh(f'python3 scripts/run.py finish {S} {rid} --summary "x" --handoff {big}')
    h.check("handoff: a 26-line agent handoff is refused (exit 4) and the run is not finished",
            code == 4 and "the cap is 25" in out and rid in (h.status(S).get("open_runs") or {}), (code, out))
    ok = ag.w(f"handoffs/run-{rid}.md", "## Handoff\n" + "\n".join(f"- line {i}" for i in range(25)) + "\n\n")
    code, out = h.sh(f'python3 scripts/run.py finish {S} {rid} --summary "x" --handoff {ok}')
    log = (ag.c / "log.md").read_text()
    blk = next(b for b in log.split("### HANDOFF") if f"run {rid}\n" in b).split("### END HANDOFF")[0]
    h.check("handoff: 25 lines pass; the scripts add the change counts, the decision and the step outcome",
            code == 0 and "- line 24" in blk and "**Changes (script):** 2 — " in blk and "DECISION" in blk and "chose A" in blk
            and "**Steps recorded (script):** S05 done" in blk, (code, out, blk))
    rid2 = ag.start("crawl")
    ag.sh(f'python3 scripts/run.py change {S} {rid2} --kind test --url u --field f --old a --new b --result ok')
    code, out = h.sh(f'python3 scripts/run.py finish {S} {rid2} --summary "y"')
    log = (ag.c / "log.md").read_text()
    h.check("handoff: with no agent handoff the script's record is the handoff — no 'nothing from this run' note",
            code == 0 and "note: no --handoff" not in out and f"run {rid2}\n**Changes (script):** 1" in log, (out, log[-600:]))


BG = """# Fm Co - Brand Guide

## Section A — Entity foundation

| # | Field | Value | Status |
|---|---|---|---|
| 1 | Brand entity (GBP name, exactly) | Test Co | Paul Approved |
| 2 | GBP primary category = the category entity | Mobility equipment supplier (Q1) | Paul Approved |
| 3 | Category variants (4–6) | Mobility equipment supplier · stair lift installer · home accessibility lifts. Excluded: "medical equipment supplier" | Submitted |
| 8 | Phone | (417) 555-0100 | Client Confirmed |

## Section B — Variant ownership

### B1 · Reserved for the homepage
```
HOMEPAGE AREA VARIANT:      South Carolina Lowcountry [Paul Approved]
HOMEPAGE CATEGORY VARIANT:  Mobility equipment supplier [Paul Approved]
```

### B2 · Rotation pool
```
1. the Lowcountry
2. Beaufort County
3. Charleston area
```

## Section C — Page inventory

### C1 · Service pages
| URL | Service name | H1 service variant | Status |
|---|---|---|---|
| /stair-lifts/ | Stair lifts · keyword "stair lifts" | stair lift installation (H1 "Stair Lift Installation in the Lowcountry") | Planned |

### C2 · Location pages
| URL | City | Status |
|---|---|---|
| /beaufort-sc/ | Beaufort | Planned |

### C3 · Heading and FAQ registry
| Heading | Owner |
|---|---|

## Section D — Verified facts

### D2 · Unsupported claims
"""


def t_outline_formula(h):
    spec = importlib.util.spec_from_file_location("r4build", Path(__file__).with_name("rewrite4_build.py"))
    r4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r4)
    S = "fm-co"
    ag = r4._ready(h, S)
    ag.w("brand-guide.md", BG)
    st = h.status(S)
    st["pages"]["hub-metro"] = {"id": "hub-metro", "type": "county", "name": "Beaufort County metro hub",
                                "url": "https://test.example/beaufort-metro/", "group": "metro"}
    (ag.c / "status.json").write_text(json.dumps(st))
    h.new_session()
    rid = ag.start("build", "write", batch="locs")
    for p in r4.LOCS:
        ag.write_facts(p)
    h.sh(f"python3 scripts/evidence.py run {S} --run {rid} --batch locs")
    code, out = h.sh(f"python3 scripts/outline.py build {S} locs --run {rid}")
    h.check("outline formula: the section's outlines are written", code == 0 and "2 outline(s) written by script" in out, out)
    o = (ag.c / "build/locs/outlines/loc-bluffton.md").read_text()
    h.check("outline formula: an empty plan row gets its keyword, H1 and variants by formula, with the rule shown",
            "## Assigned by formula" in o and "| Keyword | stair lifts Bluffton SC |" in o
            and "| H1 | Stair Lift Installer in Bluffton |" in o and "| Category variant | stair lift installer |" in o
            and "| Area variant | Beaufort County |" in o and "first A3 category variant" in o, o[:2500])
    h.check("outline formula: nothing is left open when the Brand Guide gives the inputs", "Open — the Brand Guide gives no formula input" not in o, o[:2500])
    h.check("outline formula: the H1 has no state and no brand; the variant is neither the GBP category nor the homepage's reserved one",
            "Bluffton, SC" not in o.split("| H1 |")[1].split("\n")[0] and "Test Co" not in o.split("| H1 |")[1].split("\n")[0]
            and "Mobility equipment supplier" not in o.split("| H1 |")[1].split("\n")[0], o[:1500])
    b = (ag.c / "build/locs/outlines/loc-beaufort.md").read_text()
    h.check("outline formula: a value the approved plan fixes is never overridden (Beaufort's keyword stays the plan's)",
            "| Keyword | stair lifts Beaufort SC |" in b.split("## Assigned by formula")[0]
            and "| Keyword |" not in b.split("## Assigned by formula")[1].split("## Variants")[0] and "| H1 | Stair Lift Installer in Beaufort |" in b, b[:1800])
    h.check("outline formula: the assigned values are recorded on the page, from the script",
            (h.status(S)["pages"]["loc-bluffton"].get("assigned") or {}).get("h1") == "Stair Lift Installer in Bluffton", h.status(S)["pages"]["loc-bluffton"])
    # a hub is never assigned (its H1 would repeat the same-named city's); no Brand Guide inputs → open, never invented
    ag.w("brand-guide.md", BG.replace("Mobility equipment supplier · stair lift installer · home accessibility lifts", "").replace(
        "| 3 | Category variants (4–6) |  . Excluded", "| 3 | Category variants (4–6) | . Excluded"))
    h.sh(f"python3 scripts/outline.py build {S} locs --run {rid} --page loc-bluffton")
    o2 = (ag.c / "build/locs/outlines/loc-bluffton.md").read_text()
    h.check("outline formula: with no category variants in the Brand Guide the H1 stays open for the writer — never invented",
            "| H1 |" not in o2.split("## Variants")[0].split("## Assigned by formula")[-1] and "Open — the Brand Guide gives no formula input" in o2
            and "H1" in o2.split("Open — the Brand Guide gives no formula input")[1].split("\n")[0], o2[:1800])
    ag.sh(f"python3 scripts/run.py abort {S} {rid} --reason test")


SCENARIOS = [t_render, t_pipeline_data, t_pipeline_audit, t_clerk_retired, t_handoff_cap_and_record, t_outline_formula]
