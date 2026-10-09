#!/usr/bin/env python3
"""The seo-ops test suite. One command:

    python3 tests/run_all.py            run everything (about a minute)
    python3 tests/run_all.py -k import  only scenarios whose name contains "import"
    python3 tests/run_all.py --keep     keep the sandbox folder for inspection

It copies the repo into a temporary sandbox (never .env, never .git, never real clients), makes
a local git repo there with pushing off, runs every scenario against fake WordPress, fake
DataforSEO and a fake public web (tests/fakes.py), prints PASS/FAIL per check, deletes the
sandbox and exits 1 if anything failed. Nothing touches the network, the real repo, Drive or a
client site. CLAUDE.md: run this after every change to the system; never commit a failing run.
"""
import csv
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = []
SB = None  # sandbox root
SESSIONS = []   # R2: every session the tests opened (a new one each time a stage changes)


# ------------------------------------------------------------------ sandbox
def make_sandbox():
    global SB
    base = os.environ.get("SEO_OPS_TEST_DIR") or tempfile.gettempdir()
    SB = Path(tempfile.mkdtemp(prefix="seo-ops-test-", dir=base))
    ignore = shutil.ignore_patterns(".env", ".git", ".state", "__pycache__")
    for item in REPO.iterdir():
        if item.name in (".env", ".git", "clients"):
            continue
        dst = SB / item.name
        (shutil.copytree(item, dst, ignore=ignore) if item.is_dir() else shutil.copy2(item, dst))
    (SB / "clients").mkdir()
    cfg = json.loads((SB / "config.json").read_text())
    cfg["git_push_after_run"] = False
    # R4: a fake local v3 folder (Drive for desktop) inside the sandbox — never the real Drive
    v3 = SB / "fake-drive" / "v3"
    tpl = v3 / cfg["drive"]["template_folder_name"]
    for sub in ("01 - Discovery and Audit/Evidence", "01 - Discovery and Audit/Deliverables", "02 - Build",
                "03 - Finish", "04 - Blog", "_Archive"):
        (tpl / sub).mkdir(parents=True, exist_ok=True)
    (tpl / "README - how to use this template.md").write_text("template\n")
    cfg["drive"]["local_root"] = str(v3)
    (SB / "config.json").write_text(json.dumps(cfg, indent=2))
    assert str(SB) in json.loads((SB / "config.json").read_text())["drive"]["local_root"]
    # hooks Paul has not installed yet (hooks-pending/) are what the tests run, so the suite checks what he installs
    pend = SB / "hooks-pending"
    if pend.is_dir():
        for f in pend.glob("*.py"):
            shutil.copy2(f, SB / ".claude" / "hooks" / f.name)
        if (pend / "settings.json").exists():
            shutil.copy2(pend / "settings.json", SB / ".claude" / "settings.json")
    assert not (SB / ".env").exists()
    sh("git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm base")


def _sh(cmd):
    r = subprocess.run(cmd, shell=True, cwd=SB, capture_output=True, text=True,
                       env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
    return r.returncode, (r.stdout + r.stderr).strip()


def new_session(model="claude-haiku-4-5"):
    """Paul opens a new chat: the real SessionStart hook records its id."""
    sid = f"test-session-{len(SESSIONS) + 1}"
    payload = json.dumps({"session_id": sid, "cwd": str(SB), "hook_event_name": "SessionStart", "source": "startup",
                          "model": model})
    r = subprocess.run(["python3", ".claude/hooks/session_start.py"], input=payload, text=True, cwd=SB,
                       capture_output=True)
    SESSIONS.append(sid)
    return r.stdout


def sh(cmd, ok=None):
    code, out = _sh(cmd)
    if code == 4 and "Start a new session" in out and cmd.startswith("python3 scripts/run.py start"):
        new_session()   # R2: the stage changed — the tests do what Paul does: a new chat, then /next
        code, out = _sh(cmd)
    return code, out


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + ("" if cond else f"\n        {str(detail)[:600]}"))
    return cond


def status(slug):
    return json.loads((SB / "clients" / slug / "status.json").read_text())


def wp_state():
    p = SB / "tests" / ".state" / "wp.json"
    return json.loads(p.read_text()) if p.exists() else {}


# ------------------------------------------------------------------ Paul and the agent
def paul(line, expect_ok=True):
    """Paul types a /approve line: the real UserPromptSubmit hook, then approve.py."""
    payload = json.dumps({"prompt": line, "cwd": str(SB), "hook_event_name": "UserPromptSubmit",
                          "session_id": SESSIONS[-1] if SESSIONS else None})
    subprocess.run(["python3", ".claude/hooks/approve_token.py"], input=payload, text=True, cwd=SB)
    code, out = sh("python3 scripts/approve.py " + shlex.join(shlex.split(line)[1:]))
    return code, out


class Agent:
    """Carries out each /next 'run' mechanically, the way its .claude/commands file says."""

    def __init__(self, slug, kind="full"):
        self.slug, self.kind, self.posts, self.errors = slug, kind, [], []
        self.sem_findings, self.fail_checks_once = {}, set()
        self.jonie_changes_wording, self.verify_outputs = set(), []
        self.wp_reports = []
        self.evidence_gaps = {}   # page id -> fact keys the page's facts file leaves out (CM-041 tests)
        self.c = SB / "clients" / slug

    def sh(self, cmd):
        code, out = sh(cmd)
        if code:
            self.errors.append(f"{cmd}\n   -> {out[:400]}")
        return code, out

    def w(self, rel, text="x\n"):
        p = self.c / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return f"clients/{self.slug}/{rel}"

    def start(self, cmd, step=None, batch=None, page=None):
        code, out = sh(f"python3 scripts/run.py start {self.slug} {cmd}" + (f" --step {step}" if step else "")
                       + (f" --batch {batch}" if batch else "") + (f" --page {page}" if page else ""))
        if code:
            self.errors.append(f"start {cmd} {step} {batch or ''} -> {out[:300]}")
            return None
        return out.strip().splitlines()[-1]

    def fin(self, rid, summary):
        if not rid:
            return
        hf = self.w(f"handoffs/run-{rid}.md", f"**What I did**\n- {summary}\n")
        self.sh(f'python3 scripts/run.py finish {self.slug} {rid} --summary "{summary}" --handoff {hf}')

    def step(self, rid, sid, outcome="done", reason=""):
        self.sh(f"python3 scripts/steps.py record {self.slug} --run {rid} {sid} {outcome}"
                + (f' --reason "{reason}"' if reason else ""))

    def mark(self, name, *files):
        self.sh(f"python3 scripts/status.py mark {self.slug} {name} " + " ".join(f"--file {shlex.quote(f)}" for f in files))

    def batch_pages(self, bid):
        return next(b for b in status(self.slug)["build"]["batches"] if b["id"] == bid)["pages"]

    def write_facts(self, pid):
        """The page's facts file, from the 'proof sheet' — every page: fact its type needs, minus the gaps."""
        reqs = json.loads((SB / "methodology" / "evidence-requirements.json").read_text())
        ptype = status(self.slug)["pages"][pid]["type"]
        facts = {it["from"][5:]: {"value": f"{it['label']} for {pid}", "status": "Client Confirmed",
                                  "source": "Client Proof Sheet - RETURNED"}
                 for it in reqs["types"][ptype] if it["from"].startswith("page:")
                 and it["from"][5:] not in self.evidence_gaps.get(pid, set())}
        return self.w(f"build/evidence/{pid}.facts.json", json.dumps({"facts": facts}))

    def do(self, command):
        wd = command.split()
        name, args = wd[0], wd[2:]
        sub = args[0] if args else ""
        S = self.slug
        if (name, sub) == ("/discovery", "discovery"):
            rid = self.start("discovery", "discovery")
            for s in ("S01", "S02", "S03"): self.step(rid, s)
            self.mark("entity_record", self.w("discovery/Test Co - Discovery Record - REVIEW.md")); self.fin(rid, "discovery")
        elif (name, sub) == ("/discovery", "proof-sheet"):
            rid = self.start("discovery", "proof-sheet"); self.step(rid, "S04")
            self.mark("proof_sheet", self.w("discovery/Test Co - Client Proof Sheet - REVIEW.md")); self.fin(rid, "proof sheet")
        elif name == "/crawl":
            rid = self.start("crawl"); self.step(rid, "S05"); self.fin(rid, "crawl (fake)")
        elif (name, sub) == ("/discovery", "data"):
            rid = self.start("discovery", "data")
            for s in ("S06", "S07", "S08", "S11", "S19", "S20", "S21"): self.step(rid, s)
            for s in ("S09", "S10"): self.step(rid, s, "skipped", "BrightLocal upload not in yet")
            self.fin(rid, "data")
        elif (name, sub) == ("/discovery", "audit"):
            rid = self.start("discovery", "audit")
            for s in ("S12", "S13", "S14", "S15", "S16", "S17", "S18"): self.step(rid, s)
            self.mark("audit_deliverables", *[self.w(f"audit/Test Co - {n} - REVIEW.md") for n in
                                              ("Finding Register", "URL Decision Map", "Recommendations", "Evidence Manifest")])
            self.fin(rid, "audit")
        elif (name, sub) == ("/discovery", "sheet-returned"):
            rid = self.start("discovery", "sheet-returned")
            self.mark("proof_sheet_returned", self.w("discovery/Test Co - Client Proof Sheet - RETURNED.md")); self.fin(rid, "returned")
        elif (name, sub) == ("/discovery", "reconcile"):
            rid = self.start("discovery", "reconcile"); self.mark("reconciled", self.w("brand-guide.md", TEST_BG)); self.fin(rid, "reconciled")
        elif (name, sub) == ("/discovery", "facts-direct"):
            rid = self.start("discovery", "facts-direct"); self.step(rid, "S04")
            f = self.w("discovery/Test Co - MANUAL - client-answers - 2026-10-08.md", "Owner said: residential only.\n")
            self.mark("facts_direct", f); self.mark("proof_sheet", f); self.fin(rid, "facts answered directly")
        elif (name, sub) == ("/build", "blockers"):
            rid = self.start("build", "blockers")
            self.mark("blocker_checklist", self.w("build/Test Co - Technical Blocker Checklist - REVIEW.md"))
            items = self.w("build/blockers.csv", "url,field,old,new,reason,decision_map_ref\n"
                           "https://test.example/sitemap.xml,sitemap,missing pages,all pages listed,F-003,\n")
            self.sh(f"python3 scripts/handoff.py create {S} --run {rid} --kind sitemap --items {items} --blockers")
            self.fin(rid, "blockers")
        elif name == "/verify":   # Jonie returned the blocker handoff: record it, then /verify checks each row
            rid = self.start("verify")
            for hid in status(S).get("blocker_handoffs") or []:
                rows = list(csv.DictReader(open(self.c / "handoffs" / f"{hid}.csv", newline="")))
                for r_ in rows:
                    r_["status"] = "done"
                ret = self.c / "handoffs" / f"{hid}-returned.csv"
                with open(ret, "w", newline="") as fh:
                    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
                self.sh(f"python3 scripts/handoff.py ingest {S} --run {rid} --handoff {hid} --returned {ret.relative_to(SB)}")
                self.sh(f"python3 scripts/verify.py {S} --run {rid} --handoff {hid}")
            self.fin(rid, "blockers verified")
        elif (name, sub) == ("/build", "plan"):
            rid = self.start("build", "plan")
            plan = {"pages": [{"id": i, "type": t, "name": i, "url": f"https://test.example/{i}/", **x} for i, t, x in [
                ("svc-roof-repair", "service", {"service_variant": "Roof Repair"}),
                ("svc-roof-replacement", "service", {"service_variant": "Roof Replacement"}),
                ("svc-gutters", "service", {"service_variant": "Gutter Installation"}),
                ("loc-springfield", "location", {"city": "Springfield"}), ("hub-greene-county", "county", {"city": "Greene County"}),
                ("loc-nixa", "location", {"city": "Nixa"}), ("home", "homepage", {}), ("about", "about", {})]],
                "batches": [{"id": "pilot", "kind": "service", "label": "Pilot", "pages": ["svc-roof-repair", "loc-springfield"]},
                            {"id": "s1", "kind": "service", "label": "Roofing", "pages": ["svc-roof-replacement", "svc-gutters"]},
                            {"id": "l1", "kind": "location", "label": "Greene County", "pages": ["hub-greene-county", "loc-nixa"]},
                            {"id": "h1", "kind": "homepage", "label": "Home + about", "pages": ["home", "about"]}]}
            pj = self.w("build/site-plan.json", json.dumps(plan)); pm = self.w("build/Test Co - Site Plan - REVIEW.md")
            self.sh(f"python3 scripts/status.py plan {S} --file {shlex.quote(pm)} --json {pj}"); self.fin(rid, "site plan")
        elif (name, sub) == ("/build", "evidence"):
            bid = args[1]; rid = self.start("build", "evidence", batch=bid)
            for p in self.batch_pages(bid):
                self.write_facts(p)
            self.sh(f"python3 scripts/evidence.py run {S} --run {rid} --batch {bid}"); self.fin(rid, f"evidence {bid}")
        elif (name, sub) in (("/build", "brief"), ("/build", "draft")):
            bid, pid = args[1], args[2]
            rid = self.start("build", sub, batch=bid, page=pid)
            if not rid:
                return True
            if sub == "brief":
                gaps = status(S)["pages"][pid]["evidence"]["result"] in ("warn", "block")
                f = self.w(f"build/B-{pid}.md", f"# Brief {pid}\n" + ("\n## Evidence gaps\n- see the grid\n" if gaps else ""))
            else:
                f = self.w(f"build/D-{pid}.md", page_file(pid, "v1"))
            self.sh(f"python3 scripts/status.py page-stage {S} {pid} --stage {sub} --file {f} --run {rid}")
            self.fin(rid, f"{sub} {pid}")
        elif (name, sub) == ("/build", "batch"):
            bid = args[1]; stage = args[2]
            rid = self.start("build", stage, batch=bid)
            if not rid:
                return True
            pages = self.batch_pages(bid)
            if stage == "drafts":   # the batch review: every per-page draft side by side + the SEM table
                sem = self.w(f"build/Test Co - Semantic Review - {bid} - REVIEW.md")
                n = self.sem_findings.get(bid, 1)
                self.sh(f"python3 scripts/status.py batch {S} {bid} --state drafts_written "
                        f"--sem-table {shlex.quote(sem)} --sem-findings {n}")
            else:  # apply-sem
                fs = [self.w(f"build/D-{p}.md", page_file(p, "v2")) for p in pages]
                if bid in self.fail_checks_once:
                    self.fail_checks_once.discard(bid)
                    self.sh(f'python3 scripts/status.py batch {S} {bid} --state sem_check_failed --files {",".join(fs)} '
                            f'--note "E4 chunk length failed on {pages[0]}"')
                else:
                    self.sh(f"python3 scripts/status.py batch {S} {bid} --state sem_applied --files {','.join(fs)} --checks-passed")
            self.fin(rid, f"batch {bid} {stage}")
        elif (name, sub) == ("/interview", "facts"):
            bid = args[1]; rid = self.start("interview", "facts", batch=bid)
            self.sh(f"python3 scripts/evidence.py questions {S} --run {rid} --batch {bid}"); self.fin(rid, f"facts pack {bid}")
        elif (name, sub) == ("/interview", "facts-answers"):
            bid = args[1]; rid = self.start("interview", "facts-answers", batch=bid)
            for p in self.batch_pages(bid):   # the owner answered: the gaps are filled
                self.evidence_gaps.pop(p, None); self.write_facts(p)
            self.sh(f"python3 scripts/evidence.py run {S} --run {rid} --batch {bid}"); self.fin(rid, f"facts answers {bid}")
        elif (name, sub) == ("/build", "pilot-corrections"):
            rid = self.start("build", "pilot-corrections")
            self.sh(f'python3 scripts/status.py pilot-corrections {S} --note "H1 tweak in specs/service.md"'); self.fin(rid, "pilot corrections")
        elif name == "/wp-check":
            pilot = "--pilot" in command
            rid = self.start("wp-check", "pilot" if pilot else None)
            code, out = sh(f"python3 tests/fakes.py wp check {S} --run {rid}" + (" --pilot" if pilot else ""))
            self.wp_reports.append(out)
            self.fin(rid, "wp-check")
        elif (name, sub) == ("/build", "ship"):
            bid = args[1]; rid = self.start("build", "ship", batch=bid)
            self.sh(f"python3 tests/fakes.py publish wheel {S}")
            self.sh(f"python3 tests/fakes.py publish drafts {S} --run {rid} --batch {bid}")
            self.sh(f"python3 scripts/status.py batch {S} {bid} --state handed_off")
            self.fin(rid, f"drafts + publish handoff for {bid}")
        elif (name, sub) == ("/build", "published"):
            bid = args[1]; rid = self.start("build", "published", batch=bid)
            b = next(x for x in status(S)["build"]["batches"] if x["id"] == bid)
            ret = self.c / "handoffs" / f"{b['handoff']}-returned.csv"
            self.sh(f"python3 scripts/handoff.py ingest {S} --run {rid} --handoff {b['handoff']} --returned {ret.relative_to(SB)}")
            code, out = sh(f"python3 tests/fakes.py verify {S} --run {rid} --batch {bid}")
            self.verify_outputs.append(out)
            if code == 0:
                for pid in b["pages"]:
                    wid = status(S)["pages"][pid]["wp_id"]
                    _, media = sh(f"python3 tests/fakes.py wp media {S} --post {wid}")
                    for ln in media.splitlines():
                        m = json.loads(ln)
                        if not m["alt"]:
                            self.sh(f'python3 tests/fakes.py wp set-alt {S} --run {rid} --media-id {m["id"]} '
                                    f'--alt "{pid} in Springfield, Missouri — Test Co" --expect-alt "" '
                                    f'--live --backup-confirmed "ManageWP backup before alt text, confirmed by Paul"')
                for st_ in ("published", "verified", "written_back"):
                    self.sh(f"python3 scripts/status.py batch {S} {bid} --state {st_}")
                self.sh(f"python3 tests/fakes.py publish pending {S} --run {rid}")
            else:
                fix = self.w(f"tmp/fix-{bid}.csv", "url,field,old,new,reason,decision_map_ref\n"
                             + "".join(f"https://test.example/{p}/,content,live,approved file,live page differs from the approved file,{p}\n" for p in b["pages"]))
                code2, out2 = sh(f"python3 scripts/handoff.py create {S} --run {rid} --kind publish --items {fix}")
                hs = sorted((self.c / "handoffs").glob("H-*-publish.csv"), key=lambda p: p.stat().st_mtime)
                self.sh(f"python3 scripts/status.py batch {S} {bid} --state corrections_requested")
                stj = status(S); next(x for x in stj["build"]["batches"] if x["id"] == bid)["handoff"] = hs[-1].stem
                (self.c / "status.json").write_text(json.dumps(stj, indent=2))
            self.fin(rid, f"published check {bid}")
        elif name == "/finish":
            rid = self.start("finish", sub)
            m = {"wheel": ("link_wheel", "finish/Test Co - Link Wheel Tables - REVIEW.md"),
                 "schema": ("schema_built", "finish/schema/index.md"),
                 "qa": ("release_qa", "finish/Test Co - QA Punch-List - REVIEW.md")}[sub]
            self.mark(m[0], self.w(m[1])); self.fin(rid, f"finish {sub}")
        elif (name, sub) == ("/blog", "publish"):
            pid = args[1]; rid = self.start("blog", "publish", page=pid)
            self.sh(f"python3 tests/fakes.py publish drafts {S} --run {rid} --page {pid}"); self.fin(rid, f"publish {pid}")
        elif (name, sub) == ("/blog", "map"):
            rid = self.start("blog", "map"); self.mark("blog_map", self.w("blog/Test Co - Blog Decision Map - REVIEW.md")); self.fin(rid, "map")
        elif (name, sub) == ("/blog", "intake"):
            rid = self.start("blog", "intake"); self.step(rid, "S03")
            self.mark("entity_record", self.w("blog/Test Co - Entity Foundation - REVIEW.md")); self.fin(rid, "intake")
        elif (name, sub) == ("/blog", "topics"):
            rid = self.start("blog", "topics"); self.mark("topics", self.w("blog/Test Co - Blog Topic List - REVIEW.md")); self.fin(rid, "topics")
        elif (name, sub) == ("/blog", "next"):
            rid = self.start("blog", "next")
            if not rid:
                return True
            pid = f"post-{len(self.posts) + 1}"
            f = self.w(f"blog/PD-{pid}.md", f"---\npage_id: {pid}\nurl: https://test.example/blog/{pid}/\nseo_title: {pid} - Test Co\n"
                       f"meta_description: About {pid}.\n---\n# Post {pid}\n\nThe answer first.\n\n## Why it matters\n\nBecause.\n")
            self.sh(f"python3 scripts/status.py page {S} {pid} --type blog --file {f} --state draft_written")
            self.posts.append(pid); self.fin(rid, f"post {pid}")
        else:
            return False
        return True

    def handle_wait(self, n):
        if n["command"].startswith("/verify "):
            return self.do(n["command"])
        if "sheet-returned" in n["command"] or "facts-answers" in n["command"]:
            return self.do(n["command"])
        if " published " in n["command"]:
            jonie_publishes(self, n["command"].split()[-1])
            return self.do(n["command"])
        return False


TEST_BG = """# Test Co - Brand Guide

## Section A — Entity foundation

| # | Field | Value | Status |
|---|---|---|---|
| 1 | Brand entity (GBP name, exactly) | Test Co | Paul Approved |
| 8 | Phone | (417) 555-0100 | Client Confirmed |

## Section D — Verified facts

| Fact | Value | Status | Source |
|---|---|---|---|
| Founding year / years in business | 2009 | Client Confirmed | Client Proof Sheet - RETURNED |
| Licence numbers and classes | MO-RC-1234 | Client Confirmed | State licence board |
| Insurance / bonded status | Insured, $2M | Client Confirmed | Certificate on file |
| Warranty terms | 10-year workmanship | Client Confirmed | Client Proof Sheet - RETURNED |
| Free estimate — and what free means | Free on-site inspection | Client Confirmed | Client Proof Sheet - RETURNED |
| Google rating and review count (date checked) | 4.8 / 61 (2026-10-01) | Internally Verified | GBP, checked 2026-10-01 |
| Named staff for on-page use | Pat Test, owner | Client Confirmed | Client Proof Sheet - RETURNED |

### D2 · Unsupported claims

| Claim (verbatim) | Where it appears | Client answer | Action |
|---|---|---|---|

## Section E — Service area truth
"""


def page_file(pid, version):
    """An approved page file in the writer's output format (header block + markdown)."""
    tables = {"svc": "| [Link wheel: populate service-area links here] |",
              "loc": "| [Link wheel: populate service links here] |\n\n| [Link wheel: populate sibling-city links here] |",
              "hub": "| [Link wheel: populate service links here] |"}.get(pid.split("-")[0], "")
    return (f"---\npage_id: {pid}\nurl: https://test.example/{pid}/\nseo_title: {pid} - Test Co\n"
            f"meta_description: The approved description for {pid}, naming the area and two services.\n"
            + ("replaces: https://test.example/old-roofing/\nkeyword: roof repair\n" if pid == "svc-roof-repair" else "")
            + f"---\n# {pid.replace('-', ' ').title()} in Greene County\n\nThe opening answer for {pid} ({version}). "
            f"Call today.\n\n## What does {pid} cost?\n\nCost depends on **size** and pitch.\n\n"
            f"- Inspection\n- Repair\n\n## {pid} FAQs\n\n### How long does it take?\n\nMost jobs take one day.\n\n"
            f"{tables}\n")


def jonie_publishes(ag, bid):
    """Fake Jonie: publishes each draft at its final URL, adds an image (no alt), does paired redirects,
    returns the worksheet all 'done'. Optionally changes a sentence (to prove verify catches it)."""
    import csv
    wp = SB / "tests" / ".state" / "wp.json"
    s = json.loads(wp.read_text())
    st = status(ag.slug)
    b = next(x for x in st["build"]["batches"] if x["id"] == bid)
    for pid in b["pages"]:
        p = st["pages"][pid]
        it = s["items"][str(p["wp_id"])]
        it["status"], it["link"] = "publish", p["url"]
        if bid in ag.jonie_changes_wording and b.get("state") == "handed_off":
            it["content"]["raw"] = it["content"]["raw"].replace("Call today.", "Call us today for a free quote!")
        elif "Call us today for a free quote!" in it["content"]["raw"]:
            it["content"]["raw"] = it["content"]["raw"].replace("Call us today for a free quote!", "Call today.")
        mid = str(500 + p["wp_id"])
        if mid not in s["media"]:
            s["media"][mid] = {"id": int(mid), "source_url": f"https://test.example/img/{pid}.jpg", "alt_text": "", "post": p["wp_id"]}
            it["content"]["raw"] += f'<img src="https://test.example/img/{pid}.jpg" alt="">'
    hf = ag.c / "handoffs" / f"{b['handoff']}.csv"
    rows = list(csv.DictReader(open(hf, newline="")))
    for r_ in rows:
        if r_["field"] == "301":
            s["redirects"][r_["url"].rstrip("/") + "/"] = r_["new"]
        r_["status"], r_["note"] = "done", ""
    wp.write_text(json.dumps(s, indent=1))
    with open(ag.c / "handoffs" / f"{b['handoff']}-returned.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def walkthrough(slug, kind="full", industry="roofing", max_posts=2, extra_init="", setup=None, on_decision=None):
    """/new-client then /next until blog posts; returns (transcript, decisions, runs, agent)."""
    (SB / "tests" / ".state" / "wp.json").unlink(missing_ok=True)   # a fresh fake WordPress per client
    sh(f'python3 scripts/status.py init {slug} --name "Test Co" --domain test.example --type {kind} '
       f'--industry {shlex.quote(industry)} --route A {extra_init}')
    ag = Agent(slug, kind)
    if setup:
        setup(ag)
    rid = ag.start("new-client"); ag.fin(rid, "set up")
    log, prev, decisions, runs = [], None, 0, 0
    for _ in range(700):
        _, out = sh(f"python3 scripts/next.py {slug}")
        try:
            n = json.loads(out)
        except ValueError:
            log.append(f"next.py crashed: {out[:300]}"); break
        log.append(f"{n['kind']:8} {n['command']}" + (f" [{n['why'].split()[0]}]" if n["kind"] == "review" else ""))
        if n["kind"] == "run":
            if prev == n["command"]:
                log.append("LOOP"); break
            if (n["command"] == f"/blog {slug} next" and len(ag.posts) >= max_posts) or \
                    (max_posts == 0 and n["command"].startswith(f"/finish {slug}")):
                log.append("DONE"); break
            if not ag.do(n["command"]):
                log.append("NO-SIMULATION"); break
            runs += 1; prev = n["command"]
        elif n["kind"] == "decision":
            line = (n["command"].replace("<SEM items to apply, e.g. 1,3,4 — or none>", "8")
                    .replace("<who reviewed it>", "Paul read it")
                    .replace("<name, licence>", "Dr. Test, DC-123"))
            code, out = paul(line)
            if code:
                log.append(f"APPROVE FAILED: {out[:300]}"); break
            decisions += 1; prev = None
            if on_decision:
                on_decision(line)
        elif n["kind"] == "new_session":   # R2: Paul opens a new chat on the session model and types /next
            new_session(); prev = None
            log.append("SESSION")
        elif n["kind"] == "review":     # Paul looks, then types /next: the command clears the pause
            sh(f"python3 scripts/next.py {slug} --continue")
            prev = None
        else:
            waits = log[-6:].count(log[-1])
            if waits >= 3:
                log.append("WAIT-LOOP"); break
            if not ag.handle_wait(n):
                log.append("WAIT"); break
            prev = None
    return log, decisions, runs, ag


# ------------------------------------------------------------------ scenarios
def t_walkthrough_full():
    log, decisions, runs, ag = walkthrough("wt-full")
    check("full client: /next reaches blog posts", log[-1] == "DONE", "\n".join(log[-6:]))
    check("full client: no loops, no failed commands", "LOOP" not in log and "WAIT-LOOP" not in log and not ag.errors, "\n".join(ag.errors[:3]))
    check("full client: every decision line was accepted as typed", not any(l.startswith("APPROVE FAILED") for l in log),
          "\n".join(l for l in log if "FAILED" in l))
    check("full client: each run stops at the next decision (no run asked twice)", decisions > 0 and runs > 0)
    ns = log.count("SESSION")
    check("R2: the walkthrough opens a new session at each stage (and per batch), never mid-stage",
          ns >= 7 and all(log[i + 1].startswith(("run", "review", "decision", "wait")) for i, l in enumerate(log[:-1]) if l == "SESSION"),
          ns)
    print(f"        ({runs} runs, {decisions} decisions)")
    stops = {}
    for l in log:
        if l.startswith("decision") and ":batch:" not in l and " batch:" in l:
            bid = l.split(" batch:")[1].split(":")[0]
            stops[bid] = stops.get(bid, 0) + 1
    check("two stops per batch (briefs, then drafts with SEM picks)", stops and all(v == 2 for v in stops.values()), stops)
    check("SEM picks are applied by a run, not a third stop", any("apply-sem" in l for l in log))
    i_plan = next((i for i, l in enumerate(log) if "/build wt-full plan" in l), 99)
    i_blk = next((i for i, l in enumerate(log) if l.startswith("wait") and "/verify wt-full" in l), -1)
    check("the site plan runs without waiting for the blockers to clear", i_plan < i_blk, (i_plan, i_blk))
    disc = [l for l in log[:next(i for i, l in enumerate(log) if "/build wt-full" in l)]
            if l.startswith("decision") and "global specs" not in l]
    check("R3: discovery + audit take two approvals (Decision Sheet + entity + facts; audit + Brand Guide)",
          len(disc) == 2 and "entity_approved proof_sheet_approved" in disc[0]
          and "audit_approved brand_guide_approved" in disc[1], disc)
    check("R3: the page specs are approved once, globally, before the audit",
          sum("/approve global specs" in l for l in log) == 1, [l for l in log if "specs" in l])
    check("R3: no discovery sign-off or blockers approval is asked (both are conditions)",
          not any(("discovery_signed_off" in l or "blockers_cleared" in l) and l.startswith("decision") for l in log))
    check("one ship run per batch (drafts + publish handoff)", sum(" ship " in l for l in log) == len(stops), log)
    check("one check run per batch after Jonie publishes (verify + alt text + write-back)",
          sum(" published " in l and l.startswith("wait") for l in log) == len(stops),
          [l for l in log if " published " in l])
    wps = wp_state()["items"]
    pub = [i for i in wps.values() if i["status"] == "publish" and "test.example/svc-" in i["link"]]
    check("drafts generated from the approved files and published only by Jonie", len(pub) == 3, len(pub))
    first = next(i for i in wps.values() if i["link"].endswith("/svc-roof-repair/"))
    raw = first["content"]["raw"]
    check("draft content is proper blocks (headings, paragraphs, lists, table)",
          all(x in raw for x in ('<!-- wp:heading {"level":2} -->', "<!-- wp:paragraph -->", "<!-- wp:list -->",
                                 "<!-- wp:table -->", '<!-- wp:heading {"level":3} -->')) and "<h1" not in raw, raw[:300])
    check("post title is the H1; SEOPress title and meta set on the draft",
          first["title"]["raw"].startswith("Svc Roof Repair") and
          wp_state()["seo"][str(first["id"])]["title"] == "svc-roof-repair - Test Co")
    check("link tables filled from the wheel (pilot location linked from the pilot service page)",
          "https://test.example/loc-springfield/" in raw)
    check("replaced URL: redirect paired with the publish and done by Jonie",
          wp_state()["redirects"].get("https://test.example/old-roofing/") == "https://test.example/svc-roof-repair/")
    media = wp_state()["media"]
    check("alt text added to the images Jonie added (safe fix)", all(m["alt_text"] for k, m in media.items() if int(k) >= 500))
    check("every page verified against its approved file (incl. keyword and social)", all("0 differ" in o for o in ag.verify_outputs), ag.verify_outputs[:2])
    check("/next ran /wp-check before the first WordPress step", any(l.startswith("run") and "/wp-check wt-full" in l for l in log)
          and log.index(next(l for l in log if "/wp-check wt-full" in l)) < log.index(next(l for l in log if " ship " in l)))
    seo1 = wp_state()["seo"][str(first["id"])]
    check("drafts carry keyword and social (Open Graph + X) from the approved file", seo1.get("_seopress_social_fb_title") == "svc-roof-repair - Test Co"
          and seo1.get("_seopress_social_twitter_desc", "").startswith("The approved description") and "_seopress_analysis_target_kw" in seo1, seo1)
    st = status("wt-full")
    held = sum(len(v) for v in (st.get("wheel_pending") or {}).values())
    posts = [i for i in wp_state()["items"].values() if i["type"] == "posts" and not i["title"]["raw"].startswith("seo-ops connection test")]
    check("approved blog posts go in as WordPress posts (drafts) with a publish handoff", len(posts) == 2 and
          all(i["status"] == "draft" for i in posts), [(i["type"], i["status"]) for i in posts])
    check("held link rows are handed to Jonie once their target is live", held == 0 and
          any((SB / "clients/wt-full/handoffs").glob("H-*link_table.csv")), held)
    rec = SB / "clients" / "wt-full"
    lm = (rec / "log.md").read_text()
    import re as _re
    for stage in ("BRIEF", "DRAFT"):
        rows = _re.findall(rf"^- {stage} \S+ · run (\S+) · (\S+) ·", lm, _re.M)
        check(f"every {stage.lower()} came from its own run, one page each (CM-043)",
              len(rows) == 8 and len({r for r, _ in rows}) == 8 and len({p for _, p in rows}) == 8, rows)
    check("the evidence gate ran on every page before its brief (CM-041)",
          lm.count("- EVIDENCE ") >= 8 and lm.index("- EVIDENCE ") < lm.index("- BRIEF "))
    check("producing stages pause for review by default (CM-044)", any(l.startswith("review") for l in log)
          and "REVIEW CONTINUED" in lm, [l for l in log if l.startswith("review")][:3])
    check("records generated: Handoff Log, decisions, checklist, approval record",
          all((rec / f).exists() for f in ("handoff-log.md", "decisions.md", "document-checklist.md", "approval-record.md")))
    log_md = (rec / "log.md").read_text()
    check("conditions are logged when met", log_md.count("## CONDITION") >= 4, log_md.count("## CONDITION"))
    st = status("wt-full")
    check("page states follow their batch", all(p["state"] == "written_back" for p in st["pages"].values() if p.get("type") != "blog")
          and all(p["state"] == "drafted" for p in st["pages"].values() if p.get("type") == "blog"),
          {k: v["state"] for k, v in st["pages"].items()})


def t_sem_paths():
    def setup(ag):
        ag.sem_findings = {"pilot": 0, "s1": 2}
        ag.fail_checks_once = {"s1"}
    log, decisions, runs, ag = walkthrough("wt-sem", setup=setup, max_posts=0)
    pilot = [l for l in log if "batch:pilot:drafts" in l]
    check("no findings: the drafts line has nothing to select", pilot and "--sem" not in pilot[0], pilot)
    check("no findings: no apply run", not any("batch pilot apply-sem" in l for l in log))
    s1 = [l for l in log if l.startswith("decision") and "batch:s1:drafts" in l]
    check("a failed re-check sends the drafts back to Paul once more", len(s1) == 2, s1)
    lm = (SB / "clients" / "wt-sem" / "log.md").read_text()
    check("the failure and the applied SEM items are logged", "SEM CHECK FAILED" in lm and "SEM APPLIED" in lm)
    check("SEM walkthrough completes", "LOOP" not in log and not ag.errors, "\n".join(log[-4:] + ag.errors[:2]))


def t_publish_corrections():
    def setup(ag):
        ag.sem_findings = {"pilot": 0}
        ag.jonie_changes_wording = {"pilot"}
    log, decisions, runs, ag = walkthrough("wt-pub", setup=setup, max_posts=0)
    check("verify catches a wording change Jonie made", any("1 differ" in o or "2 differ" in o for o in ag.verify_outputs),
          ag.verify_outputs[:2])
    rep = sorted((SB / "clients/wt-pub/handoffs").glob("verify-*.md"))
    check("the difference is reported (verify report names the changed text)",
          any("body text differs" in f.read_text() and "free quote" in f.read_text() for f in rep), len(rep))
    check("a corrections handoff goes back to Jonie, then the batch passes",
          sum(l.startswith("wait") and "published pilot" in l for l in log) == 2, [l for l in log if "published pilot" in l])
    st = status("wt-pub")
    check("after Jonie's correction the pilot is verified and written back",
          next(b for b in st["build"]["batches"] if b["id"] == "pilot")["state"] == "written_back")
    sh("python3 scripts/status.py page wt-pub svc-new --type service --url https://test.example/svc-new/ --state planned")
    code, out = sh("python3 scripts/status.py urls wt-pub --published")
    check("QA crawl list holds only published pages", "svc-roof-repair" in out and "svc-new" not in out, out)
    code, out = sh("python3 tests/fakes.py wp update-content wt-pub --run x --page-id a --url https://test.example/a/ --content-file x --expect-sha x")
    check("the system refuses to replace a live page's content wholesale", code != 0 and "never" in out, out)


def t_walkthrough_blog_only():
    log, decisions, runs, ag = walkthrough("wt-blog", "blog-only", "chiropractic", 2)
    check("blog-only (health): reaches posts without loops", log[-1] == "DONE" and not ag.errors, "\n".join(log[-5:] + ag.errors[:2]))
    st = status("wt-blog")
    check("chiropractic is sensitive with practitioner sign-off", st["client"]["sensitive"] and st["client"]["practitioner_signoff"])


def t_gates():
    sh('python3 scripts/status.py init gates-co --name G --domain g.example --type full --industry roofing')
    code, out = sh("python3 scripts/run.py start gates-co crawl")
    check("/crawl refused before /new-client finished", code == 4 and "new-client" in out, out)
    code, out = sh("python3 scripts/run.py start gates-co build --step plan")
    check("/build refused with plain-language reasons", code == 4 and "not approved yet" in out and "b1_" not in out, out)
    code, out = sh("python3 scripts/approve.py gates-co entity_approved")
    check("approve.py refuses without Paul's typed /approve", code == 7, out)
    code, out = paul("/approve gates-co entity_approved")
    check("an approval with no recorded files is refused", code != 0 and "files" in out, out)
    code, out = paul("/approve gates-co pages_built")
    check("a condition cannot be approved", code != 0 and "condition" in out, out)


def t_voiding():
    if not (SB / "clients" / "wt-full").exists():
        t_walkthrough_full()
    f = SB / "clients" / "wt-full" / "discovery" / "Test Co - Discovery Record - REVIEW.md"
    f.write_text(f.read_text() + "typo fix\n")
    c1, o1 = sh("python3 scripts/status.py require wt-full entity_approved")
    c2, o2 = sh("python3 scripts/status.py require wt-full discovery_signed_off link_wheel_approved")
    _, show = sh("python3 scripts/status.py show wt-full")
    check("editing an approved file voids that decision", c1 == 4 and "re-approve" in o1, o1)
    check("later decisions stay met (not blocked)", c2 == 0, o2)
    check("/resume flags the upstream change", "upstream change" in show)
    _, nxt = sh("python3 scripts/next.py wt-full")
    check("/next asks Paul to re-approve with the exact line", "/approve wt-full entity_approved --files" in nxt, nxt)
    paul("/approve wt-full entity_approved")
    check("re-approval clears the void", sh("python3 scripts/status.py require wt-full entity_approved")[0] == 0)


def t_section_approval():
    """An approval can cover named sections of the Brand Guide; edits elsewhere leave it standing."""
    sh('python3 scripts/status.py init sec-co --name "Sec Co" --domain sec.example --type full --industry roofing')
    ag = Agent("sec-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    rid = ag.start("discovery", "discovery")
    rec = ag.w("discovery/Sec Co - Discovery Record - REVIEW.md", "# Record\n")
    bg = ag.w("brand-guide.md", "# BG\n\n## Section A — Entity\narea: X\n\n## Section B — Variants\n\n"
              "### B1 · Reserved\nhome: Y\n\n### B2 · Pool\n1. Z\n\n### B3 · Assignment log\n| / | |\n\n"
              "## Section C — Pages\n")
    code, out = sh(f"python3 scripts/status.py mark sec-co entity_record --file {shlex.quote(rec)} --file {bg}#A+B9")
    check("a mark naming a section that isn't there is refused", code != 0 and "B9 not found" in out, out)
    ag.mark("entity_record", rec, f"{bg}#A+B1+B2")
    for s in ("S01", "S02", "S03"):
        ag.step(rid, s)
    ag.fin(rid, "discovery")
    sh("python3 scripts/next.py sec-co --continue")
    ag.do("/discovery sec-co proof-sheet")
    _, nxt_ = sh("python3 scripts/next.py sec-co --continue")
    check("/next shows Approval 1 with the section ref it covers",
          "entity_approved proof_sheet_approved" in nxt_ and "brand-guide.md#A+B1+B2" in nxt_, nxt_)
    code, out = paul("/approve sec-co entity_approved")
    check("Paul approves the entity by sections", code == 0, out)
    p = SB / bg
    p.write_text(p.read_text().replace("| / | |", "| / | homepage | Roofing Contractor |") + "| /roof-repair/ | service |\n")
    code, out = sh("python3 scripts/status.py require sec-co entity_approved")
    check("Build write-back to B3 and C leaves the entity approval standing", code == 0, out)
    p.write_text(p.read_text().replace("area: X", "area: W"))
    code, out = sh("python3 scripts/status.py require sec-co entity_approved")
    check("an edit inside Section A cancels the entity approval", code == 4 and "changed after approval" in out, out)
    # handoff kinds with their own owner, and a handoff file with an old-style heading
    rid = ag.start("wp-check")
    items = ag.w("handoffs/_items.csv", "url,field,old,new,reason,decision_map_ref\nhttps://sec.example/wp-admin/,user,,seo-ops,setup,\n")
    _, o1 = sh(f"python3 scripts/handoff.py create sec-co --run {rid} --kind wp_setup --items {items}")
    _, o2 = sh(f"python3 scripts/handoff.py create sec-co --run {rid} --kind manual_lookup --items {items}")
    md = lambda o: (SB / o.split("→ ")[1].split(" and ")[0]).read_text()
    check("WordPress setup handoff goes to Jonie without an override", "**For:** Jonie" in md(o1), o1)
    check("manual lookups (CAPTCHA registries, GBP dashboard) go to Gwen", "**For:** Gwen" in md(o2), o2)
    hf = ag.w(f"handoffs/run-{rid}.md", "## Old heading · 2026\n\n**What I did**\n- setup handoff\n")
    sh(f'python3 scripts/run.py finish sec-co {rid} --summary x --handoff {hf}')
    log = (ag.c / "handoff-log.md").read_text()
    check("the Handoff Log has one heading per run (a file's own heading is dropped)",
          "Old heading" not in log and "- setup handoff" in log, log[-400:])


def t_reviews_parse():
    code, out = sh("python3 -c \"import sys; sys.path.insert(0, 'scripts'); import reviews; "
                   "r = {'items': [{'type': 'google_review', 'review_id': 'a'}, "
                   "{'type': 'google_reviews_search', 'review_id': 'b'}, {'type': 'something_else'}]}; "
                   "print(','.join(i['review_id'] for i in reviews.review_items(r)))\"")
    check("reviews: both DataforSEO labels for a review are read (google_review, google_reviews_search)",
          code == 0 and out.strip().endswith("a,b"), out)


def t_killed_run():
    sh('python3 scripts/status.py init kill-co --name K --domain k.example --type full --industry roofing')
    ag = Agent("kill-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    rid = ag.start("discovery", "discovery"); ag.step(rid, "S01")
    _, nxt = sh("python3 scripts/next.py kill-co")
    check("/next stops at an unfinished run", '"wait"' in nxt and rid in nxt, nxt)
    code, out = sh("python3 scripts/run.py start kill-co crawl")
    check("the next command stops and names the unfinished run", code == 3 and rid in out, out)


def t_rollback():
    sh('python3 scripts/status.py init rb-co --name R --domain test.example --type full --industry roofing')
    ag = Agent("rb-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    st = status("rb-co"); st["gates"]["audit_approved"] = {"state": "approved", "files": {}}
    st["gates"]["entity_approved"] = {"state": "approved", "files": {}}
    (SB / "clients/rb-co/status.json").write_text(json.dumps(st))
    for s in [f"S{i:02d}" for i in range(1, 22)]:
        st.setdefault("audit_steps", {})[s] = {"outcome": "done"}
    (SB / "clients/rb-co/status.json").write_text(json.dumps(st))
    (SB / "tests/.state/wp.json").unlink(missing_ok=True)
    rid = ag.start("wp-check"); sh(f"python3 tests/fakes.py wp check rb-co --run {rid}"); ag.fin(rid, "wp-check")
    rid = ag.start("implement", "safe")
    code, out = sh(f'python3 tests/fakes.py wp set-alt rb-co --run {rid} --media-id 55 --alt "Roof repair in Springfield" --expect-alt ""')
    check("a change to a live page without --live and a backup confirmation is refused", code != 0 and "--live" in out, out)
    code, out = sh(f'python3 tests/fakes.py wp set-alt rb-co --run {rid} --media-id 55 --alt "Roof repair in Springfield" '
                   f'--expect-alt "" --live --backup-confirmed "ManageWP backup 09:00, confirmed by Paul"')
    check("alt text applied through wp.py (fake) with --live + backup", code == 0 and wp_state()["media"]["55"]["alt_text"], out)
    ag.fin(rid, "alt")
    n = [json.loads(l) for l in (SB / "clients/rb-co/changes.jsonl").read_text().splitlines()][-1]["n"]
    rb = ag.start("rollback")
    sh(f'python3 tests/fakes.py wp restore rb-co --run {rb} --change {n} --live --backup-confirmed "ManageWP backup 09:05, confirmed by Paul"')
    check("rollback restores the old alt text", wp_state()["media"]["55"]["alt_text"] == "")
    ag.fin(rb, "rolled back")


def specs_ok(slug):
    """The page specs are approved once per sandbox (the first scenario that needs them approves them)."""
    if sh(f"python3 scripts/status.py require {slug} page_specs_approved")[0]:
        paul("/approve global specs")


def t_import():
    sh('python3 scripts/status.py init imp-co --name "Imp Co" --domain i.example --type full --industry roofing')
    ag = Agent("imp-co"); rid = ag.start("new-client")
    prop = {"source": "Approval Record (Block 1 signed)",
            "gates": {g: {"state": "approved"} for g in ("entity_approved", "proof_sheet_approved", "audit_approved",
                                                          "brand_guide_approved", "discovery_signed_off", "blockers_cleared")},
            "pages": {"svc-a": {"type": "service", "state": "live"}, "loc-a": {"type": "location", "state": "live"},
                      "svc-b": {"type": "service", "state": "planned", "group": "Exterior"},
                      "loc-b": {"type": "location", "state": "planned", "group": "Christian County"}},
            "pilot_done": True}
    p = ag.w("import-proposal.json", json.dumps(prop)); ag.fin(rid, "proposal")
    code, out = paul(f"/approve imp-co import --proposal {p}")
    check("import confirmed by Paul", code == 0, out)
    st = status("imp-co")
    check("import: a signed sign-off / blockers block becomes a met condition (R3), not a gate",
          "discovery_signed_off" not in st["gates"] and "discovery_signed_off" in st.get("imported_conditions", {}),
          st.get("imported_conditions"))
    specs_ok("imp-co")
    _, nxt = sh("python3 scripts/next.py imp-co")
    check("/next resumes at the next unbuilt batch, never /crawl", "/crawl" not in nxt and "batch" in nxt, nxt)
    st = status("imp-co")
    check("live pages are an approved baseline", all(st["pages"][x]["approval"].get("baseline") for x in ("svc-a", "loc-a")))


def t_multi_approve():
    if not (SB / "clients" / "wt-full").exists():
        t_walkthrough_full()
    ag = Agent("wt-full")
    for pid in ("post-8", "post-9"):
        f = ag.w(f"blog/PD-{pid}.md", "d\n")
        sh(f"python3 scripts/status.py page wt-full {pid} --type blog --file {f} --state draft_written")
    before = sh("git rev-list --count HEAD")[1]
    code, out = paul("/approve wt-full page:post-8 page:post-9")
    after = sh("git rev-list --count HEAD")[1]
    check("one /approve line approves several items with one commit", code == 0 and int(after) - int(before) == 1, out)
    code, out = paul("/approve wt-full page:post-9 blog_topics_approved")
    check("multi-approve is all-or-nothing", code != 0, out)


def t_handoffs():
    if not (SB / "clients" / "wt-full").exists():
        t_walkthrough_full()
    ag = Agent("wt-full"); rid = ag.start("implement", "structural")
    bad = ag.w("tmp/r1.csv", "url,field,old,new,reason,decision_map_ref\nold-roofing,,,/roof-repair/,merged,UDM-1\n")
    code, out = sh(f"python3 scripts/handoff.py create wt-full --run {rid} --kind redirect --items {bad}")
    check("redirect with a bare slug is refused", code != 0 and "full URL" in out, out)
    good = ag.w("tmp/r2.csv", "url,field,old,new,reason,decision_map_ref\n/old-roofing/,,,/roof-repair/,merged,UDM-1\n")
    code, out = sh(f"python3 scripts/handoff.py create wt-full --run {rid} --kind redirect --items {good} --to Gwen")
    check("redirect sent to Gwen is refused without a reason", code != 0, out)
    code, out = sh(f"python3 scripts/handoff.py create wt-full --run {rid} --kind redirect --items {good}")
    csvs = sorted((ag.c / "handoffs").glob("H-*redirect.csv"))
    row = csvs[-1].read_text().splitlines()[1] if csvs else ""
    check("redirect: 301 filled, full URLs, owner Jonie",
          ",301," in row and "https://test.example/old-roofing/" in row and
          "For:** Jonie" in csvs[-1].with_suffix(".md").read_text(), row)
    cit = ag.w("tmp/c.csv", "url,field,old,new,reason,decision_map_ref\nhttps://yelp.com/x,NAP,a,b,fix,F-1\n")
    sh(f"python3 scripts/handoff.py create wt-full --run {rid} --kind citation --items {cit}")
    md = sorted((ag.c / "handoffs").glob("H-*citation.md"))
    check("citation handoff goes to Gwen", md and "For:** Gwen" in md[-1].read_text())
    ag.fin(rid, "handoffs")


def t_costs():
    sh('python3 scripts/status.py init cost-co --name C --domain c.example --type full --industry roofing')
    ag = Agent("cost-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    (SB / "tests" / ".state").mkdir(parents=True, exist_ok=True)
    (SB / "tests" / ".state" / "dfs.json").write_text(json.dumps({"balance": 10.0, "cost": 1.2}))
    rid = ag.start("verify")
    p = ag.w("tmp/p.json", "{}")
    c1, o1 = sh(f"python3 tests/fakes.py dfs call cost-co serp/google/organic/live/advanced --payload {p} --purpose a --estimate 1.0")
    c2, o2 = sh(f"python3 tests/fakes.py dfs call cost-co serp/google/organic/live/advanced --payload {p} --purpose b --estimate 1.0")
    check("per-run total over $2 asks Paul even when each call is under $2", c1 == 0 and c2 == 5, o2)
    c3, o3 = sh(f"python3 tests/fakes.py dfs call cost-co serp/google/organic/live/advanced --payload {p} --purpose c --estimate 25 --confirmed")
    check("a call over the balance stops", c3 == 6, o3)
    c4, o4 = sh(f"python3 tests/fakes.py dfs call cost-co dataforseo_labs/google/ranked_keywords/live --payload {p} --purpose d")
    check("an unconfirmed price asks Paul", c4 == 5, o4)
    (SB / "tests" / ".state" / "dfs.json").unlink()
    ag.fin(rid, "costs")


def t_guard():
    def g(payload):
        r = subprocess.run(["python3", ".claude/hooks/guard.py"], input=json.dumps(payload), text=True,
                           cwd=SB, capture_output=True)
        return r.returncode == 2
    (SB / ".env").write_text("DFS_LOGIN=fake\n")  # a fake .env so directory checks see one
    try:
        check(".env: Read blocked", g({"tool_name": "Read", "tool_input": {"file_path": str(SB / ".env")}}))
        check(".env: Grep at repo root blocked", g({"tool_name": "Grep", "cwd": str(SB), "tool_input": {"pattern": "x"}}))
        check(".env: Glob .e* blocked", g({"tool_name": "Glob", "tool_input": {"pattern": ".e*"}}))
        check(".env: grep -r blocked", g({"tool_name": "Bash", "tool_input": {"command": "grep -r DFS_ ."}}))
        check(".env: cat ./.e* blocked", g({"tool_name": "Bash", "tool_input": {"command": "cat ./.e*"}}))
        check("Grep in a subfolder still allowed", not g({"tool_name": "Grep", "cwd": str(SB), "tool_input": {"pattern": "x", "path": "scripts"}}))
        check("status.json edit blocked", g({"tool_name": "Edit", "tool_input": {"file_path": "clients/x/status.json"}}))
        check("generated records cannot be edited by hand", g({"tool_name": "Write", "tool_input": {"file_path": "clients/x/handoff-log.md"}}))
    finally:
        (SB / ".env").unlink()


def t_sensitive():
    cases = {"roofing": "no", "chiropractor": "yes", "physical therapy": "yes", "law firm": "yes",
             "lawn care": "no", "tax preparation": "yes", "wellness center": "unsure",
             "mold remediation": "yes", "asbestos abatement": "yes", "radon mitigation": "yes",
             "indoor air quality testing": "yes", "water damage restoration": "yes", "dog grooming": "unsure"}
    for ind, want in cases.items():
        _, out = sh(f"python3 scripts/status.py classify {shlex.quote(ind)}")
        check(f"sensitive check: {ind} → {want}", f'"sensitive": "{want}"' in out, out)
    _, out = sh('python3 scripts/status.py classify "mold remediation"')
    check("mold is health-adjacent, no practitioner sign-off (CM-040)",
          '"health_adjacent"' in out and '"practitioner_signoff": false' in out, out)
    code, out = sh('python3 scripts/status.py init w-co --name W --domain w.example --type full --industry "wellness center"')
    check("/new-client asks Paul when the category is unclear", code == 9 and "ASK PAUL" in out, out)
    code, out = sh('python3 scripts/status.py init d-co --name D --domain d.example --type full --industry "dog grooming"')
    check("/new-client asks Paul when an industry is on neither list (CM-040)", code == 9 and "ASK PAUL" in out, out)
    code, out = sh('python3 scripts/status.py init d-co --name D --domain d.example --type full --industry "dog grooming" --category none')
    check("Paul's answer (--category none) creates the client", code == 0 and not status("d-co")["client"]["sensitive"], out)
    ag = Agent("d-co"); rid = ag.start("new-client")
    code, out = sh(f"python3 scripts/status.py sensitivity d-co health_adjacent --run {rid}")
    c = status("d-co")["client"]
    check("status.py sensitivity records Paul's answer and logs it as a decision",
          code == 0 and c["sensitive"] and c["sensitive_category"] == "health_adjacent" and not c["practitioner_signoff"]
          and "sensitivity set to health_adjacent" in (ag.c / "log.md").read_text(), out)
    code, out = sh("python3 scripts/status.py sensitivity d-co health_adjacent --run nope")
    check("sensitivity needs an open run", code != 0, out)
    ag.fin(rid, "set up")


def t_drive():
    sh('python3 scripts/status.py init dr-co --name "Dr Co" --domain dr.example --type full --industry roofing')
    ag = Agent("dr-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    last = status("dr-co")["last_run"]["run_id"]
    _, out = sh('python3 scripts/drive.py archive-name "Dr Co - Handoff Log.md" 2026-10-03')
    check("archive name = old name + its date", out == "Dr Co - Handoff Log - 2026-10-03.md", out)
    _, out = sh("python3 scripts/drive.py records dr-co")
    check("drive.py records lists the mirrored records with their Drive names",
          "Dr Co - Handoff Log.md" in out and "Dr Co - Approval Record.md" in out and "_Archive" in out, out)
    code, out = sh("python3 scripts/drive.py replaced dr-co --run nope --name x.md --local clients/dr-co/handoff-log.md --new-link L")
    check("a Drive upload outside an open run is refused", code != 0, out)
    m = ag.start("drive-mirror")
    code, out = sh(f'python3 scripts/drive.py replaced dr-co --run {m} --name "Dr Co - Handoff Log.md" '
                   f'--local clients/dr-co/handoff-log.md --new-link https://drive/new '
                   f'--archived-as "Dr Co - Handoff Log - 2026-10-03.md" --archived-link https://drive/old')
    ch = [json.loads(l) for l in (ag.c / "changes.jsonl").read_text().splitlines() if l.strip()]
    mine = [c for c in ch if c["run_id"] == m]
    check("archive-and-replace logs two drive changes: archive (nothing deleted) + upload",
          code == 0 and [c["field"] for c in mine] == ["archive", "upload"]
          and all(c["kind"] == "drive_file" and c["channel"] == "drive" for c in mine)
          and mine[0]["new"] == "_Archive/Dr Co - Handoff Log - 2026-10-03.md", out)
    code, out = sh(f'python3 scripts/drive.py replaced dr-co --run {m} --name "Dr Co - Handoff Log.md" '
                   f'--local clients/dr-co/handoff-log.md --new-link L --archived-as "Other name.md" --archived-link O')
    check("an archive name that is not the old name + date is refused", code != 0, out)
    before = (ag.c / "handoff-log.md").read_text()
    sh(f'python3 scripts/run.py finish dr-co {m} --summary "Drive records mirrored"')   # no handoff section
    check("a drive-mirror run leaves the Handoff Log and 'last run' unchanged (no re-mirror loop)",
          (ag.c / "handoff-log.md").read_text() == before and status("dr-co")["last_run"]["run_id"] == last)
    log = (ag.c / "log.md").read_text()
    check("R4: no local client folder → 'Drive copy pending sync' is settled once, never repeated",
          log.count("- SETTLED drive_pending_sync") == 1 and "drive_pending_sync" in (ag.c / "decisions-settled.md").read_text(),
          log[-600:])

    # ---- R4: Drive for desktop — the v3 folder is a local path; uploads are file copies
    v3 = Path(json.loads((SB / "config.json").read_text())["drive"]["local_root"])
    sh('python3 scripts/status.py init lc-co --name "Lc Co" --domain lc.example --type full --industry roofing')
    lc = Agent("lc-co"); rid = lc.start("new-client")
    code, out = sh(f"python3 scripts/drive.py folder lc-co --run {rid}")
    folder = v3 / "Lc Co - TMS"
    check("R4/R8: /new-client copies the template folder to <v3>/<Client> - TMS (a real folder copy)",
          code == 0 and (folder / "01 - Discovery and Audit" / "Evidence").is_dir() and (folder / "_Archive").is_dir()
          and (folder / "README - how to use this template.md").exists(), out)
    big = SB / "clients" / "lc-co" / "inputs" / "crawl" / "Lc Co - DFS - internal_all - 2026-10-08.csv"
    big.parent.mkdir(parents=True, exist_ok=True)
    big.write_text("url,status\n" + "".join(f"https://lc.example/p{i}/,200\n" for i in range(60000)))
    code, out = sh(f'python3 scripts/drive.py upload lc-co --run {rid} --file "{big.relative_to(SB)}"')
    dst = folder / "01 - Discovery and Audit" / "Evidence" / big.name
    check("R4: a large crawl CSV is copied byte-exact into Evidence (nothing retyped)",
          code == 0 and dst.exists() and dst.read_bytes() == big.read_bytes(), out)
    lc.fin(rid, "set up")
    names = [f"Lc Co - {n}.md" for n in ("Handoff Log", "Approval Record", "Document Checklist")]
    check("R4: run.py finish mirrors the records into the client folder by itself",
          all((folder / n).exists() for n in names)
          and (folder / "Lc Co - Handoff Log.md").read_text() == (lc.c / "handoff-log.md").read_text())
    ch = [json.loads(l) for l in (lc.c / "changes.jsonl").read_text().splitlines() if l.strip()]
    check("R4: every Drive copy is logged as a drive_file change",
          sum(1 for c in ch if c["kind"] == "drive_file" and c["field"] == "upload") >= 4, [c["field"] for c in ch])
    code, out = sh(f"python3 scripts/drive.py folder lc-co --run x")
    rid2 = lc.start("wp-check"); code, out = sh(f"python3 scripts/drive.py folder lc-co --run {rid2}")
    check("R8: an existing client folder is used as is (no second copy)", code == 0 and "existing" in out, out)
    lc.fin(rid2, "second run")
    arch = sorted(p.name for p in (folder / "_Archive").iterdir())
    check("R4: a changed record is archived with its date into _Archive, then replaced (nothing deleted)",
          any(n.startswith("Lc Co - Handoff Log - ") for n in arch)
          and (folder / "Lc Co - Handoff Log.md").read_text() == (lc.c / "handoff-log.md").read_text(), arch)
    check("R4: an unchanged record is left alone (not archived again)",
          not any(n.startswith("Lc Co - Approval Record - ") for n in arch), arch)
    # #10: an approved REVIEW deliverable gets a stamped '- APPROVED' Drive copy; the repo file is unchanged
    rid3 = lc.start("discovery", "discovery")
    for s in ("S01", "S02", "S03"):
        lc.step(rid3, s)
    rec = lc.w("discovery/Lc Co - Discovery Record - REVIEW.md", "# Lc Co - Discovery Record - REVIEW\n\nbody\n")
    lc.mark("entity_record", rec); lc.fin(rid3, "discovery")
    before = (SB / rec).read_text()
    code, out = paul("/approve lc-co entity_approved")
    ap = folder / "01 - Discovery and Audit" / "Deliverables" / "Lc Co - Discovery Record - APPROVED.md"
    txt = ap.read_text() if ap.exists() else ""
    check("#10: the approved Drive copy says APPROVED with Paul, date and sha; the repo file is unchanged",
          ap.exists() and txt.startswith("# Lc Co - Discovery Record - APPROVED") and "APPROVED by Paul on" in txt
          and "sha " in txt and (SB / rec).read_text() == before, (out, txt[:300]))


def t_finish_needs_outputs():
    sh('python3 scripts/status.py init out-co --name O --domain o.example --type full --industry roofing')
    ag = Agent("out-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    rid = ag.start("discovery", "discovery")
    for s_ in ("S01", "S02", "S03"): ag.step(rid, s_)
    code, out = sh(f'python3 scripts/run.py finish out-co {rid} --summary x')
    check("finish refuses a producing step that recorded no files, and names them",
          code == 12 and "entity_record" in out and "Discovery Record" in out, out)
    ag.mark("entity_record", ag.w("discovery/rec.md"))
    code, out = sh(f'python3 scripts/run.py finish out-co {rid} --summary x')
    check("finish closes once the files are recorded", code == 0, out)
    rid = ag.start("discovery", "discovery")
    for s_ in ("S01", "S02", "S03"): ag.step(rid, s_)
    code, out = sh(f'python3 scripts/run.py finish out-co {rid} --summary x')
    check("a mark from an earlier run does not count for this run", code == 12 and "before this run" in out, out)
    g = json.loads((SB / "scripts" / "gates.json").read_text())
    check("every step has a reading list", all(v.get("reads") for v in g["steps"].values()),
          [k for k, v in g["steps"].items() if not v.get("reads")])
    sh('python3 scripts/status.py init read-co --name R --domain r.example --type full --industry roofing')
    _, out = sh("python3 scripts/run.py start read-co new-client")
    check("run.py start prints the step's reading list, run ID last",
          "Read for this step" in out and out.splitlines()[-1].endswith("-new-client-" + out.splitlines()[-1][-4:]), out)
    code, out = sh("python3 scripts/run.py start out-co build --step nonsense")
    check("an unknown step is refused with the list of steps", code == 2 and "build:plan" in out, out)


def t_repo_hygiene():
    import re as _re
    files = [f for f in SB.rglob("*") if f.is_file() and f.suffix in (".md", ".py", ".json")
             and "tests" not in f.parts and "archive" not in f.parts and "sop-source" not in f.parts]
    text = {f: f.read_text(errors="ignore") for f in files}
    hits = lambda rx: [str(f.relative_to(SB)) for f, t in text.items() if _re.search(rx, t)]
    check("no old gate names anywhere", not hits(r"\b(b1_entity|b1_audit|bab_topics|impl_safe|block[1-5])\b"),
          hits(r"\b(b1_entity|b1_audit|bab_topics|impl_safe|block[1-5])\b"))
    check("no superseded WordPress settings (wp_env_prefix, wp_pilot_done)", not hits(r"wp_env_prefix|wp_pilot_done"),
          hits(r"wp_env_prefix|wp_pilot_done"))
    check("one WordPress spec document exists and the commands point to it",
          (SB / "wordpress/wordpress-site-setup.md").exists() and "wordpress-site-setup.md" in text.get(SB / ".claude/commands/wp-check.md", ""))
    check("no --gates in docs (gates live only in gates.json)", not [f for f in hits(r"--gates") if f.endswith(".md")])
    check("no 'Stage 0-4' names in the audit skill", not [f for f in hits(r"\bStage [0-4]\b") if "seo-technical-audit" in f])
    sev = [f for f in hits(r"\|\s*\*\*High\*\*\s*\|")]
    check("the severity scale is defined only in rulings.md", sev == ["methodology/rulings.md"], sev)
    old = r"(?<!archive/)\b(coastal-delta-addendum\.md|rule-register\.md|conflicts-register\.csv)|templates/document-checklist|stage-2-selfcheck"
    check("no references to archived or removed files (except their archive paths)", not hits(old), hits(old))
    holders = sorted(str(f.relative_to(SB)) for f in SB.rglob("*.md")
                     if "tests" not in f.parts and "## BB-601 · The two-node identity graph" in f.read_text(errors="ignore"))
    pointer = (SB / ".claude/skills/bb-schema-builder/references/schema-rules.md").read_text()
    check("schema rules live in one place: sop-source v1.1 (the skill copy is only a pointer)",
          holders == ["sop-source/BB-Standard-Schema-Section-v1.1.md"] and "sop-source/BB-Standard-Schema-Section-v1.1.md" in pointer
          and "BB-60" not in pointer.replace("BB-601–608", ""), (holders, pointer[:200]))
    check("no Stage 7/8, Gemini or ChatGPT references in CLAUDE.md, agents or skills",
          not [f for f in hits(r"Stage [78]\b|Gemini|ChatGPT") if f.startswith((".claude", "CLAUDE")) and "archive-old-instructions" not in f])


def t_client_view():
    import importlib, sys as _sys
    _sys.path.insert(0, str(SB / "scripts"))
    os.chdir(SB)
    S = importlib.import_module("status")
    P = json.loads((SB / "methodology" / "client-phrases.json").read_text())
    phrases = [v["phase"] for v in P["phases"].values()] + [v["next"] for v in P["phases"].values()] \
        + list(P["done"].values()) + list(P["waiting"].values())
    bad = [(t, S.client_view_problems(t)) for t in phrases if S.client_view_problems(t)]
    check("every client phrase passes the plain-language check", not bad, bad)
    for t in ("Entity approved per CM-020", "Next: entity_approved", "SD - Roof Repair - Test Co is ready",
              "Waiting on audit_approved", "F-012 fixed", "S07 done", "run /approve now"):
        check(f"the check blocks: {t!r}", bool(S.client_view_problems(t)))
    if not (SB / "clients" / "wt-full").exists():
        t_walkthrough_full()
    cv = status("wt-full")["client_view"]
    check("a finished full client reads 'Writing articles…' with plain milestones",
          cv["phase"].startswith("Writing articles") and "8 new pages are live" in cv["done"], cv)
    sh('python3 scripts/status.py init cv-co --name C --domain c.example --type full --industry roofing')
    check("a new client starts at 'Getting started'", status("cv-co")["client_view"]["phase"] == "Getting started")
    code, out = sh("python3 scripts/run.py finish cv-co x --summary s --phase Hello")
    check("free-text client view flags are gone from run.py finish", code != 0 and "--phase" in out, out)


def t_wordpress():
    def setmode(**m):
        (SB / "tests/.state").mkdir(parents=True, exist_ok=True)
        (SB / "tests/.state/wp_mode.json").write_text(json.dumps(m))
    sh('python3 scripts/status.py init wp-co --name "WP Co" --domain test.example --type full --industry roofing')
    ag = Agent("wp-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    (SB / "tests/.state/wp.json").unlink(missing_ok=True)

    def wpcheck(pilot=False):
        rid = ag.start("wp-check", "pilot" if pilot else None)
        code, out = sh(f"python3 tests/fakes.py wp check wp-co --run {rid}" + (" --pilot" if pilot else ""))
        sh(f"python3 scripts/run.py finish wp-co {rid} --summary wp-check")
        return code, out
    cases = [({"no_creds": True}, "missing from .env"), ({"rest_blocked": True}, "security plugin"),
             ({"bad_password": True}, "Authorization header"), ({"role": "author"}, "must be an Editor"),
             ({"no_seopress": True}, "SEOPress")]
    for m, words in cases:
        setmode(**m)
        code, out = wpcheck()
        check(f"/wp-check names the cause: {list(m)[0]}", code == 1 and words in out and "not connected" in out, out[-400:])
    setmode(no_creds=True)
    code, out = wpcheck()
    check("missing credentials → /wp-check points Paul to wp.py env-lines", "wp.py env-lines wp-co" in out, out[-400:])
    code, out = sh("python3 scripts/wp.py env-lines wp-co")
    check("env-lines: the full .env path and the exact three lines for this client",
          code == 0 and f"File: {SB.resolve() / '.env'}" in out and "WP_WP_CO_URL=https://test.example" in out
          and "WP_WP_CO_USER=seo-ops" in out and "WP_WP_CO_APP_PASSWORD=<the Application Password>" in out, out)
    check("env-lines: username, Application Password and the password's name are told apart",
          "USERNAME" in out and "24 letters/numbers" in out and "NOT the normal WordPress login password" in out
          and "Not in .env: the Application Password's NAME" in out, out)
    nxt_md = (SB / ".claude/commands/next.md").read_text()
    check("/next keeps open choices apart from the /approve line",
          "Open choices first" in nxt_md and "do not print the `/approve` line yet" in nxt_md
          and "not an approval" in nxt_md)
    st = status("wp-co")
    check("a failed /wp-check leaves WordPress work blocked", not st["wordpress"]["check"]["passed"])
    code, out = sh("python3 scripts/run.py start wp-co implement --step safe")
    check("WordPress steps refuse until /wp-check passes", code == 4 and "wp-check" in out, out)
    setmode()
    code, out = wpcheck()
    check("/wp-check passes: login, role, page + post drafts, every SEOPress field read back",
          code == 0 and "connected" in out and "SEOPress 6.8+" in out and "Draft creation" in out, out)
    check("site-wide settings unreadable as Editor → one-time VA check for Jonie",
          "not readable as Editor" in out and any((ag.c / "handoffs").glob("H-*seopress_settings.md")), out[-300:])
    items = wp_state()["items"]
    check("/wp-check trashes its test drafts and publishes nothing",
          all(i["status"] == "trash" for i in items.values() if i["title"]["raw"].startswith("seo-ops connection test")))
    setmode(seopress10=True)
    code, out = wpcheck()
    check("SEOPress 10.x ({success, data} + per-section lists): every field written and read back",
          code == 0 and "SEOPress 6.8+" in out and "not read back" not in out, out[-500:])
    setmode(settings_readable=True)
    code, out = wpcheck()
    check("readable site-wide settings are saved as audit evidence", "saved as audit evidence" in out and
          any((ag.c / "inputs").glob("seopress-settings-*.json")), out[-300:])
    setmode()
    # gates for field changes on an existing live page (page 2, /roof-repair/)
    st = status("wp-co")
    for g in ("entity_approved", "audit_approved", "brand_guide_approved", "proof_sheet_approved"):
        st["gates"][g] = {"state": "approved", "files": {}}
    st["imported_conditions"] = {"proof_sheet_returned": "test"}
    st["audit_steps"] = {f"S{i:02d}": {"outcome": "done"} for i in range(1, 22)}
    (ag.c / "status.json").write_text(json.dumps(st))
    LIVE = '--live --backup-confirmed "ManageWP backup 10:00, confirmed by Paul"'
    rid = ag.start("implement", "structural")
    code, out = sh(f'python3 tests/fakes.py wp set wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--field title --value "Roof Repair - WP Co" --expect "Roof Repair | Test" {LIVE}')
    check("before the pilot, a title change on an existing page goes to a VA handoff", code != 0 and "VA handoff" in out, out)
    code, out = sh(f'python3 tests/fakes.py wp set wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--field description --value "New approved description." --expect "old desc"')
    check("live page: a safe fix without --live is refused", code != 0 and "--live" in out, out)
    code, out = sh(f'python3 tests/fakes.py wp set wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--field description --value "New approved description." --expect "wrong old value" {LIVE}')
    check("stops when the page changed since the audit", code == 11, out)
    code, out = sh(f'python3 tests/fakes.py wp set wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--field description --value "New approved description." --expect "old desc" {LIVE}')
    check("meta description (safe fix) written before the pilot, with --live + backup", code == 0 and
          wp_state()["seo"]["2"]["description"] == "New approved description.", out)
    code, out = sh(f'python3 tests/fakes.py wp set wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--field description --value "New approved description." --expect "old desc" {LIVE}')
    check("already correct → skipped", "already correct" in out, out)
    code, out = sh(f'python3 tests/fakes.py wp fix-content wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--kind broken_link --old "old roof repair copy" --new "roof repair copy" {LIVE}')
    check("broken link / content fix written and logged", code == 0 and "roof repair copy" in wp_state()["items"]["2"]["content"]["raw"], out)
    code, out = sh(f"python3 scripts/status.py cap wp-co broken_link 1 --run {rid}")
    check("Paul's safe-fix cap is recorded per client and logged",
          code == 0 and status("wp-co")["client"]["safe_fix_cap"] == {"broken_link": 1}
          and "safe-fix cap for broken_link set to 1" in (ag.c / "log.md").read_text(), out)
    code, out = sh(f'python3 tests/fakes.py wp fix-content wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--kind broken_link --old "roof repair copy" --new "roof repair text" {LIVE}')
    check("safe-fix cap reached → the next broken-link fix is refused, the page is untouched",
          code == 4 and "cap reached" in out and "roof repair text" not in wp_state()["items"]["2"]["content"]["raw"], out)
    code, out = sh(f'python3 tests/fakes.py wp fix-content wp-co --run {rid} --url https://test.example/roof-repair/ '
                   f'--kind broken_link --old "old roof repair copy" --new "roof repair copy" {LIVE}')
    check("at the cap, an already-correct item is still checked and skipped", code == 0 and "already correct" in out, out)
    sh(f"python3 scripts/status.py cap wp-co broken_link none --run {rid}")
    check("cap none removes the cap", not status("wp-co")["client"].get("safe_fix_cap"))
    ag.fin(rid, "fixes")
    # pilot: approve, then structural fields go direct
    st = status("wp-co"); st["build"] = {"site_plan": {"file": "x", "approval": {"state": "approved"}},
                                         "batches": [{"id": "pilot", "kind": "service", "label": "p", "pages": [], "state": "written_back"}]}
    (ag.c / "status.json").write_text(json.dumps(st))
    setmode(mu_plugin_key="_kad_head")
    sh("python3 scripts/status.py set wp-co client.kadence_head_meta_key _kad_head")
    code, out = wpcheck(pilot=True)
    check("/wp-check --pilot: head-code field round trip + a verified batch → pilot passed", code == 0 and "pilot passed" in out, out[-500:])
    code, out = paul("/approve wp-co wordpress_pilot_approved")
    check("Paul approves the pilot for this site", code == 0, out)
    rid = ag.start("implement", "structural")
    for field, value, expect in (("title", "Roof Repair - WP Co", "Roof Repair | Test"), ("keyword", "roof repair", ""),
                                 ("social_title", "Roof Repair - WP Co", ""), ("robots", "index,follow", "index,follow"),
                                 ("canonical", "https://test.example/roof-repair/", "")):
        code, out = sh(f'python3 tests/fakes.py wp set wp-co --run {rid} --url https://test.example/roof-repair/ '
                       f'--field {field} --value "{value}" --expect "{expect}" {LIVE}')
        check(f"after the pilot: {field} written directly and read back", code == 0, out)
    ag.fin(rid, "structural")
    n = [json.loads(l) for l in (ag.c / "changes.jsonl").read_text().splitlines() if '"seo_title"' in l][-1]["n"]
    rb = ag.start("rollback")
    code, out = sh(f"python3 tests/fakes.py wp restore wp-co --run {rb} --change {n} {LIVE}")
    check("/rollback restores the old title from the log", code == 0 and wp_state()["seo"]["2"]["title"] == "Roof Repair | Test", out)
    n = [json.loads(l) for l in (ag.c / "changes.jsonl").read_text().splitlines() if '"broken_link"' in l and "APPLIED" in l][-1]["n"]
    code, out = sh(f"python3 tests/fakes.py wp restore wp-co --run {rb} --change {n} {LIVE}")
    check("/rollback restores the old page content", code == 0 and "old roof repair copy" in wp_state()["items"]["2"]["content"]["raw"], out)
    ag.fin(rb, "rollback")
    setmode()



def build_ready(slug, gaps=None):
    """A client with discovery signed off and the site plan approved, ready for the pilot batch."""
    sh(f'python3 scripts/status.py init {slug} --name "Test Co" --domain test.example --type full --industry roofing --route A')
    ag = Agent(slug); rid = ag.start("new-client"); ag.fin(rid, "set up")
    st = status(slug)
    for g in ("entity_approved", "proof_sheet_approved", "audit_approved", "brand_guide_approved"):
        st["gates"][g] = {"state": "approved", "files": {}}
    st["imported_conditions"] = {"proof_sheet_returned": "test", "blockers_cleared": "test"}
    st["audit_steps"] = {f"S{i:02d}": {"outcome": "done"} for i in range(1, 22)}
    (ag.c / "status.json").write_text(json.dumps(st))
    ag.w("brand-guide.md", TEST_BG)
    ag.evidence_gaps = gaps or {}
    if sh(f"python3 scripts/status.py require {slug} page_specs_approved")[0]:
        paul("/approve global specs")
    ag.do(f"/build {slug} plan")
    paul(f"/approve {slug} site_plan")
    return ag


def nxt(slug):
    """What /next would do when Paul types it (a review pause is cleared first, as the command does)."""
    n = json.loads(sh(f"python3 scripts/next.py {slug} --continue")[1])
    if n["kind"] == "new_session":   # R2: Paul opens a new chat and types /next there
        new_session()
        n = json.loads(sh(f"python3 scripts/next.py {slug} --continue")[1])
    return n


def t_evidence_gate():
    S = "ev-co"
    ag = build_ready(S, {"svc-roof-repair": {"service_scope", "service_process"}, "loc-springfield": {"neighborhoods"}})
    code, out = sh(f"python3 scripts/run.py start {S} build --step brief --batch pilot --page loc-springfield")
    check("evidence gate: no brief before the gate has run", code == 4 and "evidence gate has not run" in out, out)
    check("evidence gate: /next runs the gate before any brief", nxt(S)["command"] == f"/build {S} evidence pilot", nxt(S))
    ag.do(f"/build {S} evidence pilot")
    st = status(S)
    ev = {p: st["pages"][p]["evidence"]["result"] for p in ("svc-roof-repair", "loc-springfield")}
    check("evidence gate: two required facts unknown → BLOCK", ev["svc-roof-repair"] == "block", ev)
    check("evidence gate: one required fact unknown → WARN", ev["loc-springfield"] == "warn", ev)
    grid = (SB / st["pages"]["svc-roof-repair"]["evidence"]["grid"]).read_text()
    check("evidence grid: each fact marked Known / Unknown with its source (Section A/D + proof sheet)",
          "**Unknown**" in grid and "**Known**" in grid and "Client Proof Sheet" in grid and "State licence board" in grid, grid[:500])
    lm = lambda: (ag.c / "log.md").read_text()
    check("evidence gate: every result is logged", "svc-roof-repair: BLOCK" in lm() and "loc-springfield: WARN" in lm())
    n = nxt(S)
    check("evidence gate: /next briefs the warned page, never the blocked one",
          n["command"] == f"/build {S} brief pilot loc-springfield", n)
    rid = ag.start("build", "brief", batch="pilot", page="loc-springfield")
    f = ag.w("build/B-loc-springfield.md", "# Brief\n")
    code, out = sh(f"python3 scripts/status.py page-stage {S} loc-springfield --stage brief --file {f} --run {rid}")
    check("evidence gate (warn): a brief without an 'Evidence gaps' section is refused", code != 0 and "Evidence gaps" in out, out)
    f = ag.w("build/B-loc-springfield.md", "# Brief\n\n## Evidence gaps\n- neighborhoods: [NEED]\n")
    code, out = sh(f"python3 scripts/status.py page-stage {S} loc-springfield --stage brief --file {f} --run {rid}")
    check("evidence gate (warn): the brief that flags its gaps is accepted", code == 0, out)
    ag.fin(rid, "brief")
    code, out = sh(f"python3 scripts/run.py start {S} build --step brief --batch pilot --page svc-roof-repair")
    check("evidence gate (block): the blocked page gets no brief", code == 4 and "blocked by the evidence gate" in out, out)
    n = nxt(S)
    check("evidence gate (block): /next sends it to the facts interview and shows the waiver line",
          n["command"] == f"/interview {S} facts pilot" and f"/approve {S} evidence:svc-roof-repair --reason" in n["why"], n)
    ag.do(f"/interview {S} facts pilot")
    fi = status(S)["build"]["batches"][0]["facts_interview"]
    pack = (SB / fi["file"]).read_text()
    asked = pack.split("<!--")[0]
    check("facts interview: targeted questions for the blocked page's gaps only",
          fi["pages"] == ["svc-roof-repair"] and "What the service includes" in asked and "How the service is delivered" in asked
          and "neighborhoods" not in asked.lower() and fi["questions"] <= 15, pack[:600])
    check("facts interview: logged, and nothing is sent automatically", "FACTS INTERVIEW" in lm() and "Paul sends it" in pack)
    n = nxt(S)
    check("facts interview: /next then waits for the owner's answers (or the waiver)",
          n["kind"] == "wait" and "facts-answers" in n["command"] and "evidence:svc-roof-repair" in n["why"], n)
    # --- the waiver
    code, out = paul(f"/approve {S} evidence:svc-roof-repair")
    check("waiver: refused without a reason", code != 0 and "reason" in out, out)
    code, out = paul(f'/approve {S} evidence:loc-springfield --reason "not needed"')
    check("waiver: a page that is not blocked cannot be waived", code != 0 and "not blocked" in out, out)
    code, out = sh(f'python3 scripts/approve.py {S} evidence:svc-roof-repair --reason "Claude decided"')
    check("waiver: Claude cannot waive (only Paul's typed /approve)", code == 7, out)
    code, out = paul(f'/approve {S} evidence:svc-roof-repair --reason "owner away until May; scope taken from his 2025 quote sheet"')
    w = (status(S)["pages"]["svc-roof-repair"]["evidence"] or {}).get("waiver") or {}
    check("waiver: recorded in status.json with Paul's name, date and reason",
          code == 0 and w.get("by") == "Paul" and w.get("at", "")[:4] == "2026" and "quote sheet" in w.get("reason", ""), out)
    check("waiver: recorded in log.md", "## WAIVER" in lm() and "quote sheet" in lm())
    check("waiver: the waived page may now be briefed", sh(f"python3 scripts/status.py require {S} evidence:svc-roof-repair")[0] == 0)
    ag.evidence_gaps["svc-roof-repair"] = {"service_scope", "service_process", "timeframe"}
    rid = ag.start("build", "evidence", batch="pilot")
    for p in ("svc-roof-repair", "loc-springfield"):
        ag.write_facts(p)
    sh(f"python3 scripts/evidence.py run {S} --run {rid} --batch pilot"); ag.fin(rid, "evidence again")
    code, out = sh(f"python3 scripts/status.py require {S} evidence:svc-roof-repair")
    check("waiver: when the facts change, the old waiver no longer counts", code == 4 and "older grid" in out, out)
    # --- the facts answers
    ag.do(f"/interview {S} facts-answers pilot")
    check("facts answers: the gate re-runs and the page passes", status(S)["pages"]["svc-roof-repair"]["evidence"]["result"] == "pass")
    check("facts answers: /next goes on to that page's brief", nxt(S)["command"] == f"/build {S} brief pilot svc-roof-repair", nxt(S))
    ag.do(f"/build {S} brief pilot svc-roof-repair")
    check("the batch's briefs are collected for Paul's one approval",
          "BRIEFS COLLECTED" in lm() and nxt(S)["command"].startswith(f"/approve {S} batch:pilot:briefs"), nxt(S))
    # --- scoring edge cases
    ag.write_facts("svc-gutters")
    _, out = sh(f"python3 scripts/evidence.py show {S} svc-gutters")
    check("evidence gate: every fact known → PASS", "Result: PASS" in out, out[:300])
    fp = ag.c / "build/evidence/svc-gutters.facts.json"
    fj = json.loads(fp.read_text()); fj["facts"]["service_scope"]["status"] = "Disputed"; fp.write_text(json.dumps(fj))
    _, out = sh(f"python3 scripts/evidence.py show {S} svc-gutters")
    check("evidence gate: a required fact in conflict → BLOCK", "Result: BLOCK" in out and "conflict" in out, out[:400])
    fj["facts"]["service_scope"] = {"value": "x", "status": "Client Confirmed", "source": ""}; fp.write_text(json.dumps(fj))
    _, out = sh(f"python3 scripts/evidence.py show {S} svc-gutters")
    check("evidence gate: a confirmed value with no source is Unverified, not Known", "| **Unverified** |" in out, out[:500])
    ag.write_facts("svc-gutters")
    st = status(S); st["pages"]["svc-gutters"]["claims"] = [{"phrase": "24 hour", "label": "after-hours service", "from": "D:Emergency"}]
    (ag.c / "status.json").write_text(json.dumps(st))
    _, out = sh(f"python3 scripts/evidence.py show {S} svc-gutters")
    check("evidence gate: a keyword that makes a claim adds that fact as required (CM-049)",
          "Claim in '24 hour': after-hours service | required | **Unknown**" in out and "Result: WARN" in out, out[:900])
    code, out = sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import evidence as E; "
                   "r=[{'need':'required','mark':'Known','label':'a'},{'need':'required','mark':'Known','label':'b'},"
                   "{'need':'supporting','mark':'Unknown','label':'c'}]; print(E.score(r, E.requirements()['thresholds'])[0])\"")
    check("evidence gate: fewer than 3 known facts → BLOCK (CM-015)", out.strip() == "block", out)


def t_one_page_per_run():
    S = "op-co"
    ag = build_ready(S)
    ag.do(f"/build {S} evidence pilot")
    code, out = sh(f"python3 scripts/run.py start {S} build --step brief --batch pilot")
    check("one page per run: a brief run must name its one page", code == 2 and "--page" in out, out)
    rid = ag.start("build", "brief", batch="pilot", page="svc-roof-repair")
    f = ag.w("build/B-loc-springfield.md", "# b\n")
    code, out = sh(f"python3 scripts/status.py page-stage {S} loc-springfield --stage brief --file {f} --run {rid}")
    check("one page per run: a run cannot record a second page", code != 0 and "One page per run" in out, out)
    code, out = sh(f"python3 scripts/run.py finish {S} {rid} --summary x")
    check("one page per run: the run cannot finish without its own page's brief", code == 12 and "svc-roof-repair" in out, out)
    f = ag.w("build/B-svc-roof-repair.md", "# b\n")
    sh(f"python3 scripts/status.py page-stage {S} svc-roof-repair --stage brief --file {f} --run {rid}"); ag.fin(rid, "brief")
    b = lambda: next(x for x in status(S)["build"]["batches"] if x["id"] == "pilot")
    check("one page per run: one brief alone does not reach the batch stop", b()["state"] == "planned", b()["state"])
    code, out = sh(f"python3 scripts/status.py batch {S} pilot --state briefs_written")
    check("one page per run: the batch will not collect while a page has no brief of its own",
          code != 0 and "loc-springfield has no brief" in out, out)
    ag.do(f"/build {S} brief pilot loc-springfield")
    runs = [status(S)["pages"][p]["files"]["brief"]["run"] for p in ("svc-roof-repair", "loc-springfield")]
    check("one page per run: the last page's brief collects the batch for one approval, each from its own run",
          b()["state"] == "briefs_written" and len(b()["files"]["briefs"]) == 2 and len(set(runs)) == 2, b())
    n = nxt(S)
    check("one page per run: one stop for the whole batch's briefs", n["kind"] == "decision" and "batch:pilot:briefs" in n["command"], n)
    paul(n["command"])
    check("one page per run: drafts start one page at a time", nxt(S)["command"] == f"/build {S} draft pilot svc-roof-repair", nxt(S))
    ag.do(f"/build {S} draft pilot svc-roof-repair")
    sem = ag.w("build/sem.md")
    code, out = sh(f"python3 scripts/status.py batch {S} pilot --state drafts_written --sem-table {sem} --sem-findings 0")
    check("one page per run: the batch review waits until every page has its own draft", code != 0 and "loc-springfield has no draft" in out, out)
    check("one page per run: /next drafts the next page in its own run", nxt(S)["command"] == f"/build {S} draft pilot loc-springfield", nxt(S))
    ag.do(f"/build {S} draft pilot loc-springfield")
    check("one page per run: then one batch review run for all the drafts", nxt(S)["command"] == f"/build {S} batch pilot drafts", nxt(S))
    st = status(S); keep = st["pages"]["loc-springfield"]["files"]["draft"]["run"]
    st["pages"]["loc-springfield"]["files"]["draft"]["run"] = st["pages"]["svc-roof-repair"]["files"]["draft"]["run"]
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = sh(f"python3 scripts/status.py batch {S} pilot --state drafts_written --sem-table {sem} --sem-findings 0")
    check("one page per run: two drafts from the same run are refused", code != 0 and "same run" in out, out)
    st["pages"]["loc-springfield"]["files"]["draft"]["run"] = keep; (ag.c / "status.json").write_text(json.dumps(st))
    code, out = sh(f"python3 scripts/status.py batch {S} pilot --state drafts_written --files clients/{S}/build/D-svc-roof-repair.md "
                   f"--sem-table {sem} --sem-findings 0")
    check("one page per run: the batch collects exactly the per-page drafts", code != 0 and "exactly the per-page" in out, out)
    code, out = sh(f"python3 scripts/status.py batch {S} pilot --state drafts_written --sem-table {sem} --sem-findings 0")
    check("one page per run: the batch review collects both drafts + the table for Paul's one approval",
          code == 0 and len(b()["files"]["drafts"]) == 3, out)


def t_modes():
    sh('python3 scripts/status.py init md-co --name M --domain m.example --type full --industry roofing')
    ag = Agent("md-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    _, out = sh("python3 scripts/status.py modes md-co")
    check("modes: every producing stage starts in review", " auto " not in out and "build:draft" in out and "review" in out, out)
    code, out = paul("/approve md-co mode:build:draft=auto")
    check("modes: auto is refused before the stage has passed the pilot", code != 0 and "pilot" in out, out)
    code, out = paul("/approve md-co mode:entity_approved=auto")
    check("modes: a decision can never be auto", code != 0 and "decision" in out, out)
    code, out = paul("/approve md-co mode:batch:pilot:briefs=auto")
    check("modes: a batch approval can never be auto", code != 0 and "decision" in out, out)
    code, out = paul("/approve md-co mode:build:plan=auto")
    check("modes: a stage with no pilot always stays in review", code != 0 and "always stays in review" in out, out)
    code, out = sh("python3 scripts/approve.py md-co mode:build:draft=review")
    check("modes: only Paul switches a mode (no typed /approve → refused)", code == 7, out)

    switched = []

    def on_dec(line):     # right after Paul approves the pilot drafts, he switches four stages to auto
        if "batch:pilot:drafts" in line and not switched:
            for stg in ("build:evidence", "build:brief", "build:draft", "build:drafts"):
                switched.append((stg,) + paul(f"/approve wt-modes mode:{stg}=auto"))

    def setup(a):
        a.sem_findings = {"pilot": 0}
    log, decisions, runs, ag2 = walkthrough("wt-modes", setup=setup, max_posts=0, on_decision=on_dec)
    check("modes: Paul switches stages to auto after the pilot", switched and all(c == 0 for _, c, _ in switched[:4]), switched[:4])
    cut = next((i for i, l in enumerate(log) if l.startswith("decision") and "batch:pilot:drafts" in l), len(log))
    auto = ("[build:evidence]", "[build:brief]", "[build:draft]", "[build:drafts]")
    before = [l for l in log[:cut] if l.startswith("review") and l.endswith(auto)]
    after = [l for l in log[cut + 1:] if l.startswith("review") and l.endswith(auto)]
    check("modes: in review those stages paused after every run", len(before) > 0, before[:3])
    check("modes: in auto they chain straight on (no pause)", not after, after[:3])
    check("modes: stages still in review keep pausing",
          any(l.startswith("review") and not l.endswith(auto) for l in log[cut:]), [l for l in log[cut:] if l.startswith("review")][:3])
    stops = {}
    for l in log:
        if l.startswith("decision") and " batch:" in l:
            bid = l.split(" batch:")[1].split(":")[0]; stops[bid] = stops.get(bid, 0) + 1
    check("modes: decisions still stop in auto — the pilot twice, later batches for the drafts only (R3)",
          stops.get("pilot") == 2 and all(v == 1 for k, v in stops.items() if k != "pilot")
          and all("drafts" in l for l in log if l.startswith("decision") and " batch:" in l and "batch:pilot:" not in l), stops)
    check("modes: the walkthrough with auto stages completes", log[-1] == "DONE" and not ag2.errors, log[-4:] + ag2.errors[:2])
    st = status("wt-modes"); lm = (SB / "clients/wt-modes/log.md").read_text()
    check("modes: each switch recorded in status.json and log.md",
          st["modes"].get("build:draft", {}).get("mode") == "auto" and st["modes"]["build:draft"]["by"] == "Paul"
          and len(st.get("mode_history", [])) == 4 and lm.count("## MODE") == 4, st.get("modes"))
    code, out = paul("/approve global mode:build:ship=auto")
    cfg = json.loads((SB / "config.json").read_text())
    check("modes: a global switch is allowed once a client has passed the pilot, and recorded",
          code == 0 and cfg["stage_modes"]["build:ship"]["mode"] == "auto"
          and "GLOBAL" in (SB / "clients/md-co/log.md").read_text(), out)
    _, out = sh("python3 scripts/status.py modes md-co")
    check("modes: the global setting applies to every client", "build:ship           auto   (global)" in out, out)
    paul("/approve md-co mode:build:ship=review")
    _, out = sh("python3 scripts/status.py modes md-co")
    check("modes: a client's own setting beats the global one", "build:ship           review (this client)" in out, out)
    code, out = paul("/approve global mode:discovery:audit=auto")
    check("modes: a global auto is refused for a stage with no pilot", code != 0, out)
    paul("/approve global mode:build:ship=review")


def t_fanout():
    sh('python3 scripts/status.py init fo-co --name F --domain f.example --type full --industry roofing')
    ag = Agent("fo-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    (SB / "tests" / ".state").mkdir(parents=True, exist_ok=True)
    (SB / "tests" / ".state" / "dfs.json").write_text(json.dumps({"balance": 10.0, "cost": 0.003}))
    svc = ag.w("tmp/services.txt", "roof repair\n")
    reg = ag.w("tmp/c3.txt", "How much does roof repair cost?\n")
    rid = ag.start("verify")
    base = f"python3 tests/fakes.py fanout run fo-co --run {rid} --services-file {svc} --cities Springfield,Nixa --registry {reg}"
    _, out = sh(f"python3 tests/fakes.py fanout estimate fo-co --services-file {svc} --cities Springfield,Nixa")
    check("fan-out: estimated from the confirmed price ($0.0072 a call upper bound)", "× $0.0072" in out, out)
    code, out = sh(base)
    d = ag.c / "data" / "fanout"
    rows = list(__import__("csv").DictReader(open(d / "fanout-queries.csv"))) if (d / "fanout-queries.csv").exists() else []
    md = (d / "fanout-routing.md").read_text() if (d / "fanout-routing.md").exists() else ""
    check("fan-out: queries deduplicated across seeds into the CSV", code == 0 and len(rows) == 4
          and any(r["times_seen"] == "2" for r in rows), out + str(rows[:2]))
    check("fan-out: the routing worksheet says these are not demand, and pre-marks C3 duplicates",
          "not observed demand" in md and "drop (C3 duplicate)" in md, md[:400])
    costs = (ag.c / "dfs-costs.jsonl").read_text()
    check("fan-out: every call's cost logged", costs.count("ai_optimization/chat_gpt/llm_responses/live") == 2, costs[-300:])
    code, out = sh(base)
    costs = (ag.c / "dfs-costs.jsonl").read_text()
    check("fan-out: a second run reuses the saved seeds and pays nothing new",
          code == 0 and costs.count("ai_optimization/chat_gpt/llm_responses/live") == 2, out[-300:])
    ag.fin(rid, "fanout")
    _, out = sh("python3 scripts/steps.py list")
    check("fan-out: registered as audit step S21", "S21" in out, out[-200:])
    # PAA: a run interrupted after some queries reuses the saved results — never pays twice
    rid = ag.start("verify")
    paa = f"python3 tests/fakes.py paa run fo-co --run {rid} --services-file {svc} --cities Springfield,Nixa --state Missouri --confirmed"
    code1, o1 = sh(paa)
    n1 = (ag.c / "dfs-costs.jsonl").read_text().count("serp/google/organic")
    code2, o2 = sh(paa)
    n2 = (ag.c / "dfs-costs.jsonl").read_text().count("serp/google/organic")
    check("PAA: a second run reuses the saved queries and posts nothing new", code1 == 0 and code2 == 0 and n1 == 2 and n2 == 2,
          f"{n1} {n2} {o1[-200:]} {o2[-200:]}")
    locs = SB / "tests" / ".state" / "serp_locations.txt"
    locs.unlink(missing_ok=True)
    code, out = sh(f"python3 tests/fakes.py paa run fo-co --run {rid} --services-file {svc} --cities Springfield,Nixa,Ozark "
                   f"--max-cities 5 --search-from 'Ozark=Springfield' --state Missouri --cap 10 --confirmed")
    seen = locs.read_text() if locs.exists() else ""
    check("PAA: more towns on request, and a town with no location is searched from a nearby one",
          code == 0 and "roof repair Ozark|Springfield,Missouri,United States" in seen, seen + out[-200:])
    ag.fin(rid, "paa")
    (SB / "tests" / ".state" / "dfs.json").unlink()


def t_interviews():
    sh('python3 scripts/status.py init iv-co --name I --domain i.example --type full --industry roofing')
    ag = Agent("iv-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    code, out = sh("python3 scripts/run.py start iv-co interview --step stories")
    check("stories: not before the facts exist (Brand Guide approved)", code == 4, out)
    code, out = sh("python3 scripts/interview.py due iv-co")
    check("stories: not due before the Brand Guide is approved", code == 1 and "not yet" in out, out)
    st = status("iv-co"); st["gates"]["brand_guide_approved"] = {"state": "approved", "files": {}}
    st["imported_conditions"] = {"proof_sheet_returned": "test"}; (ag.c / "status.json").write_text(json.dumps(st))
    _, out = sh("python3 scripts/interview.py due iv-co")
    check("stories: the first round is due once the facts exist", out.startswith("due"), out)
    ag.w("interviews/story-bank.md", "# I — Story bank\n\n## S-001 · thin\n- Date: 2026-10-05 · Round: 1\n- Type: unusual_case\n"
         "- Quote: \"we see a lot\"\n- Specificity: 2\n- Publish: maybe\n- Status: fresh\n")
    code, out = sh("python3 scripts/interview.py check iv-co bank")
    check("story bank: a thin, unquoted, unclassified entry is refused", code == 4 and "specificity 2" in out and "publish" in out, out)
    ag.w("interviews/story-bank.md", "# I — Story bank\n\n## S-001 · Undersized springs in the Route 9 split-levels\n"
         "- Date: 2026-10-05 · Round: 1 · Speaker: Pat, owner\n- Type: local_condition\n"
         "- Quote: \"the split-levels off Route 9 all got undersized torsion springs, so they go around year eight\"\n"
         "- Specificity: 5\n- Tags: springs\n- Publish: public\n- Status: fresh\n")
    code, out = sh("python3 scripts/interview.py check iv-co bank")
    check("story bank: a proper entry passes", code == 0, out)
    voice = ("# Voice DNA — Pat, owner, I\nSource: t.md · 1,200 words from the author · captured 2026-10-05 · confidence: low\n\n"
             "## Summary\nPlain.\n\n## Do\n- Lead with the job — \"so first thing, we go look\"\n\n## Never\n- No hype — \"I don't do the big promises\"\n\n"
             "## Calibration\n| a | b | c |\n\n## Insufficient data\nFormatting.\n")
    ag.w("interviews/voice-dna-pat.md", voice)
    code, out = sh("python3 scripts/interview.py check iv-co voice")
    check("voice DNA: under 2,000 author words without the UNDER FLOOR line is refused", code == 4 and "UNDER FLOOR" in out, out)
    ag.w("interviews/voice-dna-pat.md", voice.replace("confidence: low\n", "confidence: low\n[UNDER FLOOR — Paul accepts before use]\n"))
    code, out = sh("python3 scripts/interview.py check iv-co voice")
    check("voice DNA: with the floor flagged, every rule quoted → ok", code == 0, out)
    ag.w("interviews/voice-dna-other.md", voice)
    code, out = sh("python3 scripts/interview.py check iv-co voice")
    check("voice DNA: two files for one author are refused (never blend)", code == 4 and "never blend" in out, out)

SCHEMA = ".claude/skills/bb-schema-builder/scripts/build_schema.py"


def schema_cfg():
    return {"business": {"name": "Test Co", "url": "https://test.example", "telephone": "+1-417-555-0100",
                         "email": "pat@test.example", "schema_type": "RoofingContractor",
                         "id_page_url": "https://test.example/id.html", "founding_date": 2009,
                         "description": "Roof repair and replacement in Greene County, Missouri.",
                         "logo": "https://test.example/logo.png",
                         "address": {"streetAddress": "1 Main St", "addressLocality": "Springfield",
                                     "addressRegion": "MO", "postalCode": "65801"},
                         "has_map": "https://maps.app.goo.gl/abc"},
            "corporation": {"description": "Family roofing company in Greene County since 2009."},
            "gbp_landing_page": "https://test.example/",
            "same_as": ["https://test.example/", "https://test.example/id.html", "https://maps.app.goo.gl/abc"],
            "area_served": [{"name": "Springfield", "state": "Missouri"}],
            "service_pages": [{"url": "https://test.example/roof-repair/", "title": "Roof Repair - Test Co",
                               "meta_description": "Roof repair in Greene County.", "service_node_name": "Roof Repair",
                               "service_type": "Roof repair", "description": "Leak and storm repair.",
                               "entities": [{"name": "Roof", "wikidata": "https://www.wikidata.org/wiki/Q83180"}]}],
            "location_pages": []}


def t_schema_gate():
    d = SB / "tests" / ".state" / "schema"; d.mkdir(parents=True, exist_ok=True)
    n = [0]

    def run(cfg, check_only=False):
        """build_schema.py through the fakes (fake Wikipedia / Wikidata / Grokipedia). Fresh output dir each time."""
        n[0] += 1
        (d / "cfg.json").write_text(json.dumps(cfg))
        out = d / f"out{n[0]}"
        code, text = sh(f"python3 tests/fakes.py build_schema {d / 'cfg.json'} {out}" + (" --check" if check_only else ""))
        return code, text, out

    def graph(out, name="homepage"):
        return json.loads((out / f"{name}.jsonld").read_text())
    code, out, o = run(schema_cfg())
    check("schema: a complete config builds", code == 0 and (o / "homepage.jsonld").exists(), out[-300:])
    # --- the two crash fixes (CM-050)
    cfg = schema_cfg(); del cfg["business"]["logo"]
    for flag in (True, False):
        code, out, _ = run(cfg, flag)
        check(f"schema: a missing logo is refused with a clear message, never a crash ({'--check' if flag else 'build'})",
              code == 2 and "business.logo" in out and "Logo image URL" in out and "Traceback" not in out, out[-400:])
    cfg = schema_cfg(); del cfg["service_pages"][0]["entities"][0]["wikidata"]
    for flag in (True, False):
        code, out, _ = run(cfg, flag)
        check(f"schema: an entity with no Wikidata URI is refused with a clear message, never a crash ({'--check' if flag else 'build'})",
              code == 2 and "entity 'Roof'" in out and "no Wikidata URI" in out and "Traceback" not in out, out[-400:])
    # --- 1 · entity check over HTTP
    ent = lambda **k: {**{"name": "Roof", "wikidata": "https://www.wikidata.org/wiki/Q83180"}, **k}

    def with_entity(e):
        c = schema_cfg(); c["service_pages"][0]["entities"] = [e]; return c
    code, out, o = run(with_entity(ent(wikipedia="https://en.wikipedia.org/wiki/Roof", grokipedia="https://grokipedia.com/page/Roof")))
    check("schema 1: an entity whose Wikipedia page, Wikidata ID and Grokipedia URL agree builds", code == 0, out[-300:])
    code, out, o = run(with_entity(ent(wikidata="https://www.wikidata.org/wiki/Q999", wikipedia="https://en.wikipedia.org/wiki/Roof")))
    check("schema 1: a Wikidata ID that doesn't match the Wikipedia page is refused, nothing written",
          code == 2 and "ENTITY CHECK FAILED" in out and "Q83180" in out and "Q999" in out and not o.exists(), out[-400:])
    code, out, _ = run(with_entity(ent(wikidata="https://www.wikidata.org/wiki/Q999", wikipedia="https://en.wikipedia.org/wiki/Roof")), True)
    check("schema 1: the entity check also runs with --check", code == 2 and "ENTITY CHECK FAILED" in out, out[-300:])
    code, out, _ = run(with_entity(ent(wikidata="https://www.wikidata.org/wiki/Q424242")))
    check("schema 1: a Wikidata ID that does not exist is refused", code == 2 and "Q424242 could not be found" in out, out[-300:])
    code, out, _ = run(with_entity(ent(name="Arborist", wikidata="https://www.wikidata.org/wiki/Q135615")))
    check("schema 1: a Wikidata ID whose label is a different thing is refused",
          code == 2 and "is 'Springfield, Missouri', not 'Arborist'" in out, out[-300:])
    code, out, _ = run(with_entity(ent(grokipedia="https://grokipedia.com/page/Nope")))
    check("schema 1: a Grokipedia URL that does not resolve is refused", code == 2 and "Grokipedia URL does not resolve" in out, out[-300:])
    code, out, _ = run(with_entity(ent(wikipedia="https://de.wikipedia.org/wiki/Dach")))
    check("schema 1: an unreachable source refuses the build (never built unchecked)", code == 2 and "try again" in out, out[-300:])
    # --- 2 · country from the config
    _, _, o = run(schema_cfg())
    g = graph(o)["@graph"]
    check("schema 2: the country defaults to US", g[2]["address"]["addressCountry"] == "US" and g[1]["contactPoint"]["areaServed"] == "US")
    cfg = schema_cfg(); cfg["business"]["address"]["addressCountry"] = "CA"
    _, _, o = run(cfg)
    g = graph(o)["@graph"]
    check("schema 2: the country comes from the config, not hard-coded",
          g[2]["address"]["addressCountry"] == "CA" and g[1]["contactPoint"]["areaServed"] == "CA", g[2]["address"])
    # --- 3 · working text never ships
    for leak in ("[NEED: description]", "Roofing for [Client Name] customers", "TODO: write this"):
        cfg = schema_cfg(); cfg["business"]["description"] = leak
        code, out, o = run(cfg)
        check(f"schema 3: working text is refused and nothing is written ({leak[:18]}…)",
              code == 3 and "OUTPUT CHECK FAILED" in out and not o.exists(), out[-300:])
    # --- 4 · areaServed (pilot)
    cfg = schema_cfg(); cfg["area_served"].append({"name": "Rountree", "type": "Place"})
    code, out, _ = run(cfg)
    check("schema 4: extended area types need the per-client pilot flag", code == 2 and "area_served_extended" in out, out[-300:])
    cfg["area_served_extended"] = True
    cfg["area_served"][0]["wikipedia"] = "https://en.wikipedia.org/wiki/Springfield,_Missouri"
    cfg["area_served"].append({"name": "Greene County", "type": "AdministrativeArea", "state": "Missouri"})
    code, out, o = run(cfg)
    areas = graph(o)["@graph"][2]["areaServed"] if code == 0 else []
    check("schema 4: with the pilot flag — Place, AdministrativeArea and a city's Wikipedia sameAs",
          [a["@type"] for a in areas] == ["City", "Place", "AdministrativeArea"] and areas[0].get("sameAs", "").endswith("Missouri")
          and "addressCountry" not in json.dumps(areas), out[-300:])
    cfg["area_served"].append({"name": "Earth", "type": "Country"})
    code, out, _ = run(cfg)
    check("schema 4: an areaServed type outside City / Place / AdministrativeArea is refused", code == 2 and "type must be one of" in out, out[-300:])
    # --- 5 · ready-to-paste files
    _, _, o = run(schema_cfg())
    wrapped = (o / "homepage.script.html").read_text() if (o / "homepage.script.html").exists() else ""
    check("schema 5: each page also written inside <script type=application/ld+json>, raw kept for the validator",
          wrapped.startswith('<script type="application/ld+json">') and wrapped.rstrip().endswith("</script>")
          and json.loads(wrapped.split(">", 1)[1].rsplit("</script>", 1)[0]) == graph(o), wrapped[:120])
    # --- 6 · never rules, checked on the output
    code, out = sh("python3 -c \"import sys,json; sys.path.insert(0,'.claude/skills/bb-schema-builder/scripts'); import build_schema as B; "
                   "g={'@graph':[{'@type':'RoofingContractor','aggregateRating':{'ratingValue':5}},"
                   "{'@type':'Thing','@id':'https://en.wikipedia.org/wiki/Roof'},"
                   "{'@type':'Corporation','addressCountry':'US'},"
                   "{'@type':'Service','areaServed':[{'@type':'Country','name':'US'}]}]}; "
                   "print(json.dumps(B.output_problems('x', g)))\"")
    probs = json.loads(out) if code == 0 else []
    check("schema 6: never aggregateRating / review, never a Wikipedia @id (plus addressCountry and areaServed hygiene)",
          len(probs) == 4 and any("aggregateRating" in p for p in probs) and any("Wikipedia URL as an @id" in p for p in probs)
          and any("addressCountry outside" in p for p in probs) and any("areaServed type Country" in p for p in probs), out)


def t_schema_offline():
    S = "so-co"
    sh(f'python3 scripts/status.py init {S} --name S --domain test.example --type full --industry roofing')
    ag = Agent(S); rid = ag.start("new-client"); ag.fin(rid, "set up")
    st = status(S)
    for g in ("entity_approved", "proof_sheet_approved", "audit_approved", "brand_guide_approved", "discovery_signed_off",
              "link_wheel_approved"):
        st["gates"][g] = {"state": "approved", "files": {}}
    st["imported_conditions"] = {"proof_sheet_returned": "test", "pages_built": "test"}
    st["audit_steps"] = {f"S{i:02d}": {"outcome": "done"} for i in range(1, 22)}
    (ag.c / "status.json").write_text(json.dumps(st))
    d = SB / "tests" / ".state" / "schema-off"; d.mkdir(parents=True, exist_ok=True)
    cfg = schema_cfg()
    cfg["service_pages"][0]["entities"] = [{"name": "Dach", "wikidata": "https://www.wikidata.org/wiki/Q83180",
                                            "wikipedia": "https://de.wikipedia.org/wiki/Dach"}]   # fake web: unreachable
    (d / "cfg.json").write_text(json.dumps(cfg))
    n = [0]

    def build(extra=""):
        n[0] += 1
        return sh(f"python3 tests/fakes.py build_schema {d / 'cfg.json'} {d / f'out{n[0]}'} {extra}")
    rid = ag.start("finish", "schema")
    code, out = build()
    check("offline: an unreachable Wikipedia still refuses the build by default", code == 2 and "try again" in out, out[-300:])
    code, out = build(f"--offline {S}")
    check("offline: --offline without Paul's approval is refused", code == 2 and "OFFLINE REFUSED" in out
          and f"/approve {S} schema-offline" in out, out[-300:])
    code, out = sh(f'python3 scripts/approve.py {S} schema-offline --reason "Claude thinks so"')
    check("offline: Claude cannot approve it (no typed /approve)", code == 7, out)
    code, out = paul(f"/approve {S} schema-offline")
    check("offline: the approval needs a reason", code != 0 and "reason" in out, out)
    code, out = paul(f'/approve {S} schema-offline --reason "Wikipedia API down since 09:10 (status page)"')
    rec = status(S).get("schema_offline") or {}
    check("offline: Paul's approval is recorded with his name, date, reason and the one run it covers",
          code == 0 and rec.get("by") == "Paul" and rec.get("at", "")[:4] == "2026" and "status page" in rec.get("reason", "")
          and rec.get("run") == rid and "schema-offline · by Paul" in (ag.c / "log.md").read_text(), out)
    cfg_bad = dict(cfg); cfg_bad["business"] = {**cfg["business"], "description": "[NEED: description]"}
    (d / "cfg.json").write_text(json.dumps(cfg_bad))
    code, out = build(f"--offline {S}")
    check("offline: every other check still runs (working text refused) and the approval is not used up",
          code == 3 and "OUTPUT CHECK FAILED" in out and not (status(S)["schema_offline"].get("used")), out[-300:])
    (d / "cfg.json").write_text(json.dumps(cfg))
    code, out = build(f"--offline {S}")
    check("offline: with the approval, the run builds once without the live entity check",
          code == 0 and "live entity check SKIPPED" in out and (d / f"out{n[0]}" / "homepage.jsonld").exists(), out[-300:])
    check("offline: the use is logged and marked used",
          status(S)["schema_offline"].get("used") and "SCHEMA OFFLINE" in (ag.c / "log.md").read_text())
    code, out = build(f"--offline {S}")
    check("offline: a second build in the same run needs a new approval", code == 2 and "already used" in out, out[-300:])
    ag.mark("schema_built", ag.w("finish/schema/index.md")); ag.fin(rid, "schema")
    code, out = paul(f'/approve {S} schema-offline --reason "still down"')
    check("offline: approving with no /finish schema run open is refused", code != 0 and "none is open" in out, out)
    rid2 = ag.start("finish", "schema")
    code, out = build(f"--offline {S}")
    check("offline: an approval does not carry over to another run", code == 2 and "OFFLINE REFUSED" in out, out[-300:])
    bad = schema_cfg(); bad["service_pages"][0]["entities"] = [{"name": "Roof", "wikidata": "Q83180"}]
    (d / "cfg.json").write_text(json.dumps(bad))
    paul(f'/approve {S} schema-offline --reason "outage again"')
    code, out = build(f"--offline {S}")
    check("offline: the Q-ID format is still checked offline", code == 2 and "must be https://www.wikidata.org/wiki/Q" in out, out[-300:])
    ag.mark("schema_built", ag.w("finish/schema/index.md")); ag.fin(rid2, "schema")


def t_readability():
    d = SB / "tests" / ".state"; d.mkdir(parents=True, exist_ok=True)
    head = ("---\npage_id: x\nurl: https://test.example/x/\nseo_title: Comprehensive Professional Environmental "
            "Remediation Methodologies - Test Co\nmeta_description: We fix leaky roofs in Greene County. Call for a free look.\n---\n")
    easy = head + ("# Roof Repair in Greene County\n\nWe fix leaks fast. Most jobs take one day. We check the whole roof first.\n\n"
                   "## How long does a roof repair take?\n\nMost repairs take one day. Big storm jobs can take two or three days.\n")
    (d / "easy.md").write_text(easy)
    code, out = sh(f"python3 scripts/readability.py {d / 'easy.md'}")
    check("reading level: plain copy passes, and the SEO title is not counted (CM-047)", code == 0 and "E10 passes" in out, out)
    hard = head + ("# Roof Repair in Greene County\n\nComprehensive professional remediation methodologies necessitate "
                   "meticulous evaluation of deteriorated architectural components, particularly considering "
                   "environmental variability, structural interdependencies and manufacturer specifications.\n")
    (d / "hard.md").write_text(hard)
    code, out = sh(f"python3 scripts/readability.py {d / 'hard.md'}")
    check("reading level: dense copy fails and the paragraph is listed", code == 1 and "OVER" in out and "E10 FAILS" in out, out)
    src = head + ("# Mold in Hanover\n\nThe Environmental Protection Agency says to fix leaks fast. "
                  "The Environmental Protection Agency says mold can grow in two days.\n")
    (d / "src.md").write_text(src); (d / "terms.txt").write_text("Environmental Protection Agency\n")
    _, o1 = sh(f"python3 scripts/readability.py {d / 'src.md'}")
    _, o2 = sh(f"python3 scripts/readability.py {d / 'src.md'} --exclude-terms {d / 'terms.txt'}")
    g = lambda o: float(o.split("page average grade ")[1].split()[0])
    check("reading level: named sources and entity terms are left out of the count", g(o2) < g(o1), (o1, o2))


def t_models():
    import re as _re
    want = {"discovery-audit": "opus", "audit-reviewer": "opus", "build": "opus", "finish": "opus", "blog": "opus",
            "clerk": "haiku"}
    got = {}
    for f in (SB / ".claude" / "agents").glob("*.md"):
        m = _re.search(r"^model:\s*(\S+)", f.read_text().split("\n---", 2)[0], _re.M)
        got[f.stem] = m.group(1) if m else None
    check("R1: every agent has a preset model — Opus for judgment, Haiku (clerk) for mechanical work",
          all(got.get(k) == v for k, v in want.items()) and set(got.values()) <= {"haiku", "opus"}, got)
    g = json.loads((SB / "scripts" / "gates.json").read_text())
    check("R1: every stage's session runs on Haiku (no Sonnet, no Fable)",
          {s["session_model"] for s in g["stages"]} == {"haiku"}, [s["session_model"] for s in g["stages"]])
    mapped = {x for s in g["stages"] for x in s["steps"]} | set(g["any_stage"])
    check("R2: every step belongs to exactly one stage (or is bookkeeping for any stage)",
          set(g["steps"]) <= mapped and len([x for s in g["stages"] for x in s["steps"]]) ==
          len({x for s in g["stages"] for x in s["steps"]}), set(g["steps"]) - mapped)
    sh('python3 scripts/status.py init md-co --name "Md Co" --domain md.example --type full --industry roofing')
    ag = Agent("md-co"); ag.fin(ag.start("new-client"), "set up")
    n = nxt("md-co")
    check("R1: next.py names the stage, the session model and the agents with their models",
          n.get("stage", "").startswith("2 of ") and n.get("session_model") == "haiku"
          and "discovery-audit (opus)" in n.get("agents", ""), n)
    _, out = sh("python3 scripts/stages.py list")
    check("stages.py lists every stage with its models", "clerk (haiku)" in out and "build (opus)" in out, out)


def t_settled_and_status():
    sh('python3 scripts/status.py init ss-co --name "Ss Co" --domain ss.example --type full --industry roofing')
    ag = Agent("ss-co"); ag.fin(ag.start("new-client"), "set up")
    rid = ag.start("discovery", "discovery")
    code, out = sh(f'python3 scripts/run.py decision ss-co {rid} --settle address_display --text "Street address shown on the website, hidden on the Google profile"')
    check("R6: a decision is settled once (logged)", code == 0 and "- SETTLED address_display" in (ag.c / "log.md").read_text(), out)
    code, out = sh(f'python3 scripts/run.py decision ss-co {rid} --settle address_display --text "ask again"')
    check("R6: settling the same decision again is refused — it is not asked twice", code == 4 and "already settled" in out, out)
    code, out = sh(f'python3 scripts/run.py decision ss-co {rid} --reopen address_display --text ""')
    check("R6: a reopen request needs the reason", code != 0, out)
    code, out = sh(f'python3 scripts/run.py decision ss-co {rid} --reopen address_display --text "client now wants it hidden on the site too"')
    code2, out2 = sh(f'python3 scripts/run.py decision ss-co {rid} --reopen address_display --text "again"')
    check("R6: one reopen request (logged with the flag), a second is refused", code == 0 and code2 == 4, (out, out2))
    sh(f'python3 scripts/run.py decision ss-co {rid} --settle address_display --text "Address hidden on the website and the Google profile"')
    sh(f"python3 scripts/run.py decision ss-co {rid} --settle citations --text \"Citations skipped for this audit (no BrightLocal)\"")
    items = ag.w("h.csv", "url,field,old,new,reason,decision_map_ref\nhttps://x.example/,SoS record,,record it,captcha,\n")
    sh(f"python3 scripts/handoff.py create ss-co --run {rid} --kind manual_lookup --items {items}")
    for s in ("S01", "S02", "S03"):
        ag.step(rid, s)
    ag.mark("entity_record", ag.w("discovery/Ss Co - Discovery Record - REVIEW.md")); ag.fin(rid, "discovery")
    reg = (ag.c / "decisions-settled.md").read_text()
    check("R6: decisions-settled.md lists each settled decision once (the latest), with the reopen counted as a defect",
          "Address hidden on the website and the Google profile" in reg and "Street address shown" not in reg
          and "Citations skipped" in reg and "Process defects (reopenings): **1**" in reg, reg)
    notes = (ag.c / "test-run-notes.md").read_text() if (ag.c / "test-run-notes.md").exists() else ""
    check("R6: the reopening is counted in the client's test-run notes", "address_display: reopened 1×" in notes, notes)
    stx = (ag.c / "STATUS.md").read_text() if (ag.c / "STATUS.md").exists() else ""
    top4 = [l for l in stx.splitlines() if l.startswith("- **")][:4]
    check("R7: STATUS.md opens with stage n of N, what is happening now, waiting on, next action",
          len(top4) == 4 and top4[0].startswith("- **Stage 2 of ") and "What is happening now" in top4[1]
          and "Waiting on" in top4[2] and "Next action" in top4[3], top4)
    check("R7: STATUS.md lists settled decisions once, open VA items with owner and id, and spend",
          stx.count("Citations skipped for this audit") == 1 and "manual_lookup" in stx and "(Gwen)" in stx
          and "DataforSEO: $" in stx and "~/Documents/seo-ops" in stx, stx)
    code, out = sh("python3 scripts/records.py top ss-co")
    check("R7: records.py top prints the four lines /next and /resume show", code == 0 and len(out.splitlines()) == 4, out)


DECISION_SHEET = """# Fd Co - Decision Sheet - REVIEW

| Key | Decision | Recommended default | Answer (Paul) | Evidence / why |
|---|---|---|---|---|
| area_entity | Area entity | Springfield metro area | | contains all 6 towns |
| address_display.website | Street address on the website? | hidden | shown | Paul |
| title_format.service | SEO-title format — service pages | `Service Name - Brand` | | |
| blog_author | Blog author | | | |
"""


def t_decide_once():
    # Approval 1 with the client's direct answers: no sheet to approve, and the facts count as returned
    sh('python3 scripts/status.py init fd-co --name "Fd Co" --domain fd.example --type full --industry roofing')
    ag = Agent("fd-co"); ag.fin(ag.start("new-client"), "set up")
    rid = ag.start("discovery", "discovery")
    for s in ("S01", "S02", "S03"):
        ag.step(rid, s)
    bg = ag.w("brand-guide.md", TEST_BG)
    ag.mark("entity_record", ag.w("discovery/Fd Co - Decision Sheet - REVIEW.md", DECISION_SHEET),
            ag.w("discovery/Fd Co - Discovery Record - REVIEW.md"), "clients/fd-co/brand-guide.md#A")
    ag.fin(rid, "discovery")
    sh("python3 scripts/next.py fd-co --continue")
    ag.do("/discovery fd-co facts-direct")
    n = nxt("fd-co")
    check("R3: with the client's direct answers, Approval 1 is one line (no sheet to approve)",
          n["kind"] == "decision" and n["command"] == "/approve fd-co entity_approved proof_sheet_approved", n)
    code, out = paul(n["command"])
    st = status("fd-co")
    check("R3: approving the direct answers meets 'proof sheet returned' — nothing waits for a sheet nobody was sent",
          code == 0 and "proof_sheet_returned" in st.get("conditions_logged", {}), out)
    reg = (ag.c / "decisions-settled.md").read_text()
    check("R6: Approval 1 settles every Decision Sheet answer (or its default) — never asked again",
          "area_entity" in reg and "Springfield metro area (recommended default)" in reg
          and "address_display.website" in reg and ": shown" in reg and "blog_author" not in reg, reg)
    rid = ag.start("crawl")
    code, out = sh(f'python3 scripts/run.py decision fd-co {rid} --settle address_display.website --text "hidden after all"')
    check("R6: a later step cannot re-ask a Decision Sheet answer", code == 4 and "already settled" in out, out)
    ag.step(rid, "S05"); ag.fin(rid, "crawl")
    # status-only reconcile edits do not void the entity approval; a value change does
    text = (SB / bg).read_text()
    (SB / bg).write_text(text.replace("| Test Co | Paul Approved |", "| Test Co | Client Confirmed 2026-10-08 |"))
    check("R3: a reconcile that only changes a row's status leaves the entity approval standing",
          sh("python3 scripts/status.py require fd-co entity_approved")[0] == 0)
    (SB / bg).write_text(text.replace("| Test Co | Paul Approved |", "| Test Co Roofing | Paul Approved |"))
    code, out = sh("python3 scripts/status.py require fd-co entity_approved")
    check("R3: a changed value in Section A still voids it (re-approve)", code == 4 and "re-approved" in out, out)
    (SB / bg).write_text(text)
    # #8: an answers-only run on the proof-sheet step finishes without re-marking an unchanged sheet
    rid = ag.start("discovery", "proof-sheet")
    ag.mark("facts_direct", ag.w("discovery/Fd Co - MANUAL - client-answers - 2026-10-09.md", "More answers.\n"))
    code, out = sh(f'python3 scripts/run.py finish fd-co {rid} --summary "answers recorded"')
    check("#8: a proof-sheet run that records only the client's answers can finish", code == 0, out)
    # page specs: a change re-opens the global approval; pilot corrections keep it
    if sh("python3 scripts/status.py require fd-co page_specs_approved")[0] != 0:
        paul("/approve global specs")
    spec = SB / "methodology" / "specs" / "service.md"
    old = spec.read_text()
    spec.write_text(old + "\nA new rule.\n")
    code, out = sh("python3 scripts/status.py require fd-co page_specs_approved")
    check("R3: a spec changed after Paul approved it re-opens the specs approval (once, globally)",
          code == 4 and "service.md" in out and "/approve global specs" in out, out)
    code, out = sh("python3 scripts/status.py require fd-co entity_approved proof_sheet_approved")
    req = json.loads((SB / "scripts" / "gates.json").read_text())["gates"]
    check("R3: a spec change never voids an approval already given (the specs gate the steps that score or write pages)",
          code == 0 and not any("page_specs_approved" in g.get("requires", []) for g in req.values()), out)
    spec.write_text(old)
    check("R3: the approved specs carry an APPROVED status line", "**Status:** APPROVED" in old, old[:200])


def t_briefs_after_pilot():
    switched = []

    def on_decision(line):
        if "batch:pilot:drafts" in line and not switched:
            code, out = paul("/approve wt-auto mode:build:brief=auto")
            switched.append((code, out))
    log, decisions, runs, ag = walkthrough("wt-auto", max_posts=0, on_decision=on_decision)
    check("R3: after the pilot Paul may switch briefs to auto", switched and switched[0][0] == 0, switched)
    later = [l for l in log if l.startswith("decision") and ":briefs" in l and "batch:pilot:" not in l]
    drafts = [l for l in log if l.startswith("decision") and ":drafts" in l and "batch:pilot:" not in l]
    check("R3: after the pilot, batches stop for the drafts only (no briefs approval)", not later and len(drafts) >= 3,
          (later, drafts))
    check("R3: the walkthrough still completes", "LOOP" not in log and not ag.errors, "\n".join(log[-4:] + ag.errors[:2]))


def t_pilot_order():
    """The pilot (1 service + 1 location) is exempt from service-before-location, in batch_ready and in /next;
    after it, a planned location batch listed before a service batch waits for the service batch."""
    S = "po-co"
    ag = build_ready(S)
    st = status(S)
    by = {b["id"]: b for b in st["build"]["batches"]}
    by["pilot"]["kind"] = "location"
    st["build"]["batches"] = [by["pilot"], by["l1"], by["s1"], by["h1"]]
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = sh(f"python3 scripts/status.py require {S} batch:pilot:briefs_ready")
    check("pilot order: a location-kind pilot is not held behind the service batches", code == 0, out)
    n = nxt(S)
    check("pilot order: /next starts with the pilot", n["command"] == f"/build {S} evidence pilot", n)
    st = status(S)
    pilot = next(b for b in st["build"]["batches"] if b["id"] == "pilot")
    pilot.update({"state": "written_back", "briefs": {"state": "approved", "files": {}},
                  "drafts": {"state": "approved", "files": {}}})
    st["build"]["pilot_corrections_applied"] = {"at": "2026-10-09", "note": "test"}
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = sh(f"python3 scripts/status.py require {S} batch:l1:briefs_ready")
    check("pilot order: a location batch still waits for the service batch", code != 0 and "batch s1" in out, out)
    n = nxt(S)
    check("pilot order: /next skips the waiting location batch and runs the service batch",
          n["command"] == f"/build {S} evidence s1", n)


def t_migration():
    sh('python3 scripts/status.py init mg-co --name "Mg Co" --domain mg.example --type full --industry roofing')
    ag = Agent("mg-co"); ag.fin(ag.start("new-client"), "set up")
    bg = SB / ag.w("brand-guide.md", TEST_BG)
    sec = "clients/mg-co/brand-guide.md#A"
    v1 = sh(f"cd scripts && python3 -c 'import lib; print(lib.ref_sha_v1(\"{sec}\"))'")[1].strip()
    st = status("mg-co")
    st["schema"] = 3
    st["gates"]["entity_approved"] = {"state": "approved", "by": "Paul", "at": "2026-10-05T10:00:00", "files": {sec: v1}}
    st["gates"]["discovery_signed_off"] = {"state": "approved", "by": "Paul", "at": "2026-10-08T10:00:00", "files": {}}
    st["gates"]["blockers_cleared"] = {"state": "pending"}
    (ag.c / "status.json").write_text(json.dumps(st, indent=2))
    (ag.c / "STATUS.md").write_text("# Mg Co — status\n\n## Waiting on\n\n| Who | What | Since | Reference |\n|---|---|---|---|\n"
                                    "| Client (via Paul) | Synthetic roofing offered? | 2026-10-08 | F-009 |\n"
                                    "| Gwen | SoS record | 2026-10-05 | handoff H-1 |\n\n"
                                    "## Settled — do not re-raise\n\n- **Entity:** category Roofing Contractor.\n"
                                    "- **WordPress:** the login is an Administrator; Paul decides once whether Jonie switches it.\n")
    code, out = sh("python3 scripts/migrate.py mg-co")
    st = status("mg-co")
    check("migration: approvals kept — the section approval is re-stamped to the new hash, not voided",
          code == 0 and st["schema"] == 4 and st["gates"]["entity_approved"]["files"][sec] != v1
          and sh("python3 scripts/status.py require mg-co entity_approved")[0] == 0, out)
    check("migration: discovery_signed_off and blockers_cleared become conditions (history kept)",
          "discovery_signed_off" not in st["gates"] and st["retired_gates"]["discovery_signed_off"]["state"] == "approved", st.get("retired_gates"))
    reg = (ag.c / "decisions-settled.md").read_text()
    check("migration: a hand-written STATUS.md is carried over — settled stays settled, open questions stay open",
          "category Roofing Contractor" in reg and "Synthetic roofing offered?" in reg and "wordpress_login" in reg
          and "SoS record" not in reg, reg)
    stx = (ag.c / "STATUS.md").read_text()
    check("migration: STATUS.md is now generated", "Generated" in stx and "- **Stage " in stx, stx[:300])
    code, out = sh("python3 scripts/migrate.py mg-co")
    check("migration runs once (a second run changes nothing)", "already migrated" in out, out)


def t_sessions():
    import shutil as _sh_
    sf = SB / ".claude" / "state" / "session.json"
    saved = sf.read_text() if sf.exists() else None
    sh('python3 scripts/status.py init se-co --name "Se Co" --domain se.example --type full --industry roofing')
    sh('python3 scripts/status.py init se2-co --name "Se2 Co" --domain se2.example --type full --industry roofing')
    sf.unlink(missing_ok=True)
    code, out = _sh("python3 scripts/run.py start se-co new-client")
    check("R2: with no session recorded (hook not installed) a stage run is refused", code == 4 and "session hook" in out, out)
    out = new_session("claude-haiku-4-5")
    check("R2: the SessionStart hook records the session and prints the model reminder",
          sf.exists() and "one session per stage" in out and "Haiku" in out, out)
    check("R1: a session on another model is warned (Haiku and Opus only)", "Haiku and Opus only" in new_session("claude-sonnet-5-5"))
    new_session()
    ag = Agent("se-co"); rid = ag.start("new-client"); ag.fin(rid, "set up")
    code, out = _sh("python3 scripts/run.py start se-co discovery --step discovery")
    check("R2: a session that finished one stage cannot start the next — the system says to open a new session",
          code == 4 and "Stage 1 (Setup) is done in this session" in out and "new session" in out and "Haiku" in out, out)
    n = json.loads(_sh("python3 scripts/next.py se-co --continue")[1])
    check("R2: /next stops with new_session instead of running the next stage here", n["kind"] == "new_session", n)
    code, out = _sh("python3 scripts/run.py start se-co wp-check")
    check("R2: bookkeeping steps (any stage) still run in the same session", code == 0, out)
    if code == 0:
        sh(f'python3 scripts/run.py finish se-co {out.splitlines()[-1]} --summary "check"')
    code, out = _sh("python3 scripts/run.py start se2-co new-client")
    check("R2: the same session cannot start a stage for another client either", code == 4 and "for se-co" in out, out)
    new_session()
    code, out = _sh("python3 scripts/run.py start se-co discovery --step discovery")
    check("R2: in a new session the next stage starts", code == 0, out)
    lm = (SB / "clients/se-co/log.md").read_text()
    check("R2: every run records its session", f"session {SESSIONS[-1]}" in lm)
    if saved is not None:
        sf.write_text(saved)


def t_guard_rewrite():
    def g(tool, inp):
        r = subprocess.run(["python3", ".claude/hooks/guard.py"], input=json.dumps({"tool_name": tool, "tool_input": inp,
                           "cwd": str(SB)}), text=True, cwd=SB, capture_output=True)
        return r.returncode == 2
    B = lambda c: g("Bash", {"command": c})
    check("#20: a read-only chain on the safety log is allowed", not B("cd clients/x && cat log.md | grep RUN | tail -3"))
    check("#20: a record name inside a quoted argument is text", not B('git commit -m "regenerate approval-record.md and decisions.md"')
          and not B('python3 scripts/run.py decision x R --text "see log.md; status.json & co"'))
    check("#20: the credentials file named in a commit message is text", not B('git commit -m "never commit .env"'))
    check("#20: writes stay blocked — redirect, rm, sed -i, tee, inline python",
          B("echo x > clients/x/log.md") and B("cd clients/x && rm status.json") and B("sed -i '' s/a/b/ clients/x/status.json")
          and B("echo x | tee -a clients/x/log.md") and B("python3 -c \"open('clients/x/status.json','w')\"")
          and B("cp /tmp/a clients/x/approval-record.md"))
    check("#20: .env stays unreadable however it is written", B("cat .env") and B('cat ".env"') and B("cd x && head -1 .env"))
    check("#20: hooks and approval state stay off limits", B("cat .claude/state/approve-token.json") and B("ls .claude/hooks"))
    check("#20: history rewriting stays blocked", B("git reset --hard HEAD~1") and B("git push --force"))
    check("#20: DataforSEO/WordPress API calls outside the scripts stay blocked",
          B("curl https://api.dataforseo.com/v3/x") and B("curl https://x.example/wp-json/wp/v2/pages"))
    cfg = json.loads((SB / "config.json").read_text())["drive"]
    D = "mcp__462fe272-2d95-47ed-a152-03251be122dc__search_files"
    check("R8: a Drive search across all of Drive is blocked", g(D, {"query": "title contains 'Apex'"}))
    check("R8: a Drive search inside the v3 folder is allowed",
          not g(D, {"query": f"parentId = '{cfg['root_folder_id']}' and title contains 'Apex'"}))
    check("R8: a search that escapes the v3 folder with 'or' is blocked",
          g(D, {"query": f"parentId = '{cfg['root_folder_id']}' or title contains 'Apex'"}))
    check("R8: a search in a folder outside v3 is blocked", g(D, {"query": "parentId = 'someOtherFolder'"}))


SCENARIOS = [t_repo_hygiene, t_finish_needs_outputs, t_walkthrough_full, t_sem_paths, t_publish_corrections, t_walkthrough_blog_only, t_gates, t_voiding, t_section_approval, t_reviews_parse, t_killed_run, t_rollback,
             t_import, t_multi_approve, t_handoffs, t_costs, t_guard, t_sensitive, t_drive, t_wordpress, t_client_view,
             t_evidence_gate, t_one_page_per_run, t_modes, t_fanout, t_interviews, t_schema_gate, t_schema_offline, t_readability, t_models, t_settled_and_status, t_decide_once, t_briefs_after_pilot, t_pilot_order, t_migration, t_sessions, t_guard_rewrite]


def extra_scenarios():
    """tests/checks/*.py: each module's SCENARIOS, called with this harness as h."""
    import importlib.util
    import types
    h = types.SimpleNamespace(SB=SB, sh=sh, check=check, status=status, Agent=Agent, paul=paul,
                              new_session=new_session, nxt=nxt)
    out = []
    for f in sorted((REPO / "tests" / "checks").glob("*.py")):
        if f.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"checks_{f.stem}", f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for fn in getattr(m, "SCENARIOS", []):
            def run(fn=fn):
                h.SB = SB
                fn(h)
            run.__name__ = f"t_{f.stem}_{fn.__name__.lstrip('t_')}"
            out.append(run)
    return out


def main():
    keep = "--keep" in sys.argv
    only = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    make_sandbox()
    new_session()
    try:
        for t in SCENARIOS + extra_scenarios():
            if only and only not in t.__name__:
                continue
            print(f"\n{t.__name__[2:].replace('_', ' ')}")
            try:
                t()
            except Exception as e:  # a crash is a failure, not a stop
                check(f"{t.__name__} ran without crashing", False, repr(e))
    finally:
        if keep:
            print(f"\nsandbox kept: {SB}")
        else:
            shutil.rmtree(SB, ignore_errors=True)
    failed = [r for r in RESULTS if not r[1]]
    print(f"\n{len(RESULTS) - len(failed)} passed, {len(failed)} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
