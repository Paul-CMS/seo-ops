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
    (SB / "config.json").write_text(json.dumps(cfg, indent=2))
    assert not (SB / ".env").exists()
    sh("git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm base")


def sh(cmd, ok=None):
    r = subprocess.run(cmd, shell=True, cwd=SB, capture_output=True, text=True,
                       env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
    return r.returncode, (r.stdout + r.stderr).strip()


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
    payload = json.dumps({"prompt": line, "cwd": str(SB), "hook_event_name": "UserPromptSubmit"})
    subprocess.run(["python3", ".claude/hooks/approve_token.py"], input=payload, text=True, cwd=SB)
    code, out = sh("python3 scripts/approve.py " + shlex.join(shlex.split(line)[1:]))
    return code, out


class Agent:
    """Carries out each /next 'run' mechanically, the way its .claude/commands file says."""

    def __init__(self, slug, kind="full"):
        self.slug, self.kind, self.posts, self.errors = slug, kind, [], []
        self.sem_findings, self.fail_checks_once = {}, set()
        self.jonie_changes_wording, self.verify_outputs = set(), []
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
            for s in ("S06", "S07", "S08", "S11", "S19"): self.step(rid, s)
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
            rid = self.start("discovery", "reconcile"); self.mark("reconciled", self.w("brand-guide.md", "bg\n")); self.fin(rid, "reconciled")
        elif (name, sub) == ("/discovery", "signoff"):
            rid = self.start("discovery", "signoff")
            self.mark("discovery_summary", self.w("discovery/Test Co - Discovery Summary - REVIEW.md")); self.fin(rid, "signoff")
        elif (name, sub) == ("/build", "blockers"):
            rid = self.start("build", "blockers")
            self.mark("blocker_checklist", self.w("build/Test Co - Technical Blocker Checklist - REVIEW.md")); self.fin(rid, "blockers")
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
        elif (name, sub) == ("/build", "batch"):
            bid = args[1]; stage = args[2] if len(args) > 2 else "briefs"
            rid = self.start("build", {"briefs": "batch"}.get(stage, stage), batch=bid)
            if not rid:
                return True
            pages = self.batch_pages(bid)
            if stage == "briefs":
                fs = [self.w(f"build/B-{p}.md") for p in pages]
                self.sh(f"python3 scripts/status.py batch {S} {bid} --state briefs_written --files {','.join(fs)}")
            elif stage == "drafts":
                fs = [self.w(f"build/D-{p}.md", page_file(p, "v1")) for p in pages]
                sem = self.w(f"build/Test Co - Semantic Review - {bid} - REVIEW.md")
                n = self.sem_findings.get(bid, 1)
                self.sh(f"python3 scripts/status.py batch {S} {bid} --state drafts_written --files {','.join(fs)} "
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
        elif (name, sub) == ("/build", "pilot-corrections"):
            rid = self.start("build", "pilot-corrections")
            self.sh(f'python3 scripts/status.py pilot-corrections {S} --note "H1 tweak in specs/service.md"'); self.fin(rid, "pilot corrections")
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
                                    f'--alt "{pid} in Springfield, Missouri — Test Co" --expect-alt ""')
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
        if "sheet-returned" in n["command"]:
            return self.do(n["command"])
        if " published " in n["command"]:
            jonie_publishes(self, n["command"].split()[-1])
            return self.do(n["command"])
        return False


def page_file(pid, version):
    """An approved page file in the writer's output format (header block + markdown)."""
    tables = {"svc": "| [Link wheel: populate service-area links here] |",
              "loc": "| [Link wheel: populate service links here] |\n\n| [Link wheel: populate sibling-city links here] |",
              "hub": "| [Link wheel: populate service links here] |"}.get(pid.split("-")[0], "")
    return (f"---\npage_id: {pid}\nurl: https://test.example/{pid}/\nseo_title: {pid} - Test Co\n"
            f"meta_description: The approved description for {pid}, naming the area and two services.\n"
            + ("replaces: https://test.example/old-roofing/\n" if pid == "svc-roof-repair" else "")
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


def walkthrough(slug, kind="full", industry="roofing", max_posts=2, extra_init="", setup=None):
    """/new-client then /next until blog posts; returns (transcript, decisions, runs, agent)."""
    (SB / "tests" / ".state" / "wp.json").unlink(missing_ok=True)   # a fresh fake WordPress per client
    sh(f'python3 scripts/status.py init {slug} --name "Test Co" --domain test.example --type {kind} '
       f'--industry {shlex.quote(industry)} --route A {extra_init}')
    ag = Agent(slug, kind)
    if setup:
        setup(ag)
    rid = ag.start("new-client"); ag.fin(rid, "set up")
    log, prev, decisions, runs = [], None, 0, 0
    for _ in range(160):
        _, out = sh(f"python3 scripts/next.py {slug}")
        try:
            n = json.loads(out)
        except ValueError:
            log.append(f"next.py crashed: {out[:300]}"); break
        log.append(f"{n['kind']:8} {n['command']}")
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
    print(f"        ({runs} runs, {decisions} decisions)")
    stops = {}
    for l in log:
        if l.startswith("decision") and ":batch:" not in l and " batch:" in l:
            bid = l.split(" batch:")[1].split(":")[0]
            stops[bid] = stops.get(bid, 0) + 1
    check("two stops per batch (briefs, then drafts with SEM picks)", stops and all(v == 2 for v in stops.values()), stops)
    check("SEM picks are applied by a run, not a third stop", any("apply-sem" in l for l in log))
    i_plan = next((i for i, l in enumerate(log) if "/build wt-full plan" in l), 99)
    i_blk = next((i for i, l in enumerate(log) if "blockers_cleared" in l), -1)
    check("the site plan runs without waiting for the blockers decision", i_plan < i_blk, (i_plan, i_blk))
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
    check("every page verified against its approved file", all("0 differ" in o for o in ag.verify_outputs), ag.verify_outputs[:2])
    st = status("wt-full")
    held = sum(len(v) for v in (st.get("wheel_pending") or {}).values())
    posts = [i for i in wp_state()["items"].values() if i["type"] == "posts"]
    check("approved blog posts go in as WordPress posts (drafts) with a publish handoff", len(posts) == 2 and
          all(i["status"] == "draft" for i in posts), [(i["type"], i["status"]) for i in posts])
    check("held link rows are handed to Jonie once their target is live", held == 0 and
          any((SB / "clients/wt-full/handoffs").glob("H-*link_table.csv")), held)
    rec = SB / "clients" / "wt-full"
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
    check("the system refuses to change a live page", code != 0 and "never" in out, out)


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
    for s in [f"S{i:02d}" for i in range(1, 20)]:
        st.setdefault("audit_steps", {})[s] = {"outcome": "done"}
    (SB / "clients/rb-co/status.json").write_text(json.dumps(st))
    rid = ag.start("implement", "safe")
    code, out = sh(f'python3 tests/fakes.py wp set-alt rb-co --run {rid} --media-id 55 --alt "Roof repair in Springfield" --expect-alt ""')
    check("alt text applied through wp.py (fake)", code == 0 and wp_state()["media"]["55"]["alt_text"], out)
    ag.fin(rid, "alt")
    n = [json.loads(l) for l in (SB / "clients/rb-co/changes.jsonl").read_text().splitlines()][-1]["n"]
    rb = ag.start("rollback")
    sh(f"python3 tests/fakes.py wp restore rb-co --run {rb} --change {n}")
    check("rollback restores the old alt text", wp_state()["media"]["55"]["alt_text"] == "")
    ag.fin(rb, "rolled back")


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
             "lawn care": "no", "tax preparation": "yes", "wellness center": "unsure"}
    for ind, want in cases.items():
        _, out = sh(f"python3 scripts/status.py classify {shlex.quote(ind)}")
        check(f"sensitive check: {ind} → {want}", f'"sensitive": "{want}"' in out, out)
    code, out = sh('python3 scripts/status.py init w-co --name W --domain w.example --type full --industry "wellness center"')
    check("/new-client asks Paul when the category is unclear", code == 9 and "ASK PAUL" in out, out)


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
    check("no --gates in docs (gates live only in gates.json)", not [f for f in hits(r"--gates") if f.endswith(".md")])
    check("no 'Stage 0-4' names in the audit skill", not [f for f in hits(r"\bStage [0-4]\b") if "seo-technical-audit" in f])
    sev = [f for f in hits(r"\|\s*\*\*High\*\*\s*\|")]
    check("the severity scale is defined only in rulings.md", sev == ["methodology/rulings.md"], sev)
    old = r"(?<!archive/)\b(coastal-delta-addendum\.md|rule-register\.md|conflicts-register\.csv)|templates/document-checklist|stage-2-selfcheck"
    check("no references to archived or removed files (except their archive paths)", not hits(old), hits(old))
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


SCENARIOS = [t_repo_hygiene, t_finish_needs_outputs, t_walkthrough_full, t_sem_paths, t_publish_corrections, t_walkthrough_blog_only, t_gates, t_voiding, t_killed_run, t_rollback,
             t_import, t_multi_approve, t_handoffs, t_costs, t_guard, t_sensitive, t_client_view]


def main():
    keep = "--keep" in sys.argv
    only = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    make_sandbox()
    try:
        for t in SCENARIOS:
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
