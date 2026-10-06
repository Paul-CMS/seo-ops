#!/usr/bin/env python3
"""next.py — what happens next for a client, read from status.json and the safety log.

    next.py <slug>            one line of JSON: {"kind": run|decision|wait|review, "command": ..., "why": ...}
    next.py <slug> --continue only at the start of a /next Paul typed: clears a review pause (logged)

kind=run      -> /next runs this command now
kind=decision -> stop: Paul decides. "command" is the exact /approve line to type.
kind=wait     -> stop: waiting on the client, a VA or an unfinished run
kind=review   -> stop: the stage that just finished is in review mode (CM-044). Paul looks at its
                 output and types /next to go on. A stage in auto mode never pauses. A pause before a
                 decision or a wait is not shown (that stop already pauses).

Every decision gate in scripts/gates.json names its artifact (the files the approval covers)
and its producer. For each gate in order: met → move on; approved but its file changed →
ask Paul to re-approve; artifact recorded → stop at the decision; else run the producer.
"""
import json
import sys

import run as R
import status as S
import steps


SLUG = None
PAUSE = None   # the review pause left by the last finished run, if its stage is in review mode


def out(kind, command, why):
    if kind == "run" and PAUSE:
        kind, why = "review", (f"{PAUSE['step']} finished (run {PAUSE['run_id']}) and that stage is in review mode — "
                               f"look at what it produced, then type /next to go on. Next would be: {command} ({why})")
        command = f"/next {SLUG}"
    print(json.dumps({"kind": kind, "command": command, "why": why}))
    sys.exit(0)


def q(files):
    return '"' + ",".join(files) + '"'


def extras(st):
    c = st["client"]
    return ((' --review "<who reviewed it>"' if c.get("sensitive") else "")
            + (' --practitioner "<name, licence>"' if c.get("practitioner_signoff") else ""))


def condition_step(st, slug, cond):
    """A condition is never approved: met → move on; else run its producer or wait."""
    ok, why = S.condition_met(st, cond)
    if ok:
        return
    spec = S.GATES["conditions"][cond]
    if spec.get("wait_for"):
        out("wait", spec["producer"].format(slug=slug),
            f"waiting for {spec['wait_for']} — when it arrives, run this to record it")
    if spec.get("producer"):
        out("run", spec["producer"].format(slug=slug), why)
    out("wait", f"/resume {slug}", why)


def gate_step(st, slug, gate):
    """Emit the next action for one decision, or return if it is met."""
    if S.gate_met(st, gate)[0]:
        return
    spec = S.GATES["gates"][gate]
    for r in S.requires(st, gate):
        if r in S.GATES["conditions"]:
            condition_step(st, slug, r)
    rec = st["gates"].get(gate) or {}
    marks = st.get("marks") or {}
    if rec.get("state") in S.GATES["met_decisions"]:
        files = S.mark_files(st, spec["artifact"]) or list(rec.get("files") or {})
        out("decision", f"/approve {slug} {gate} --files {q(files)}",
            f"{S.plain(gate)} changed after you approved it — re-approve it (later steps are not blocked; "
            "/resume flags them as 'upstream change')")
    before = spec.get("before")
    if before and before["mark"] not in marks:
        out("run", before["producer"].format(slug=slug), f"needed before {S.plain(gate)}")
    if spec["artifact"] in marks:
        out("decision", f"/approve {slug} {gate} --files {q(S.mark_files(st, spec['artifact']))}",
            f"{S.plain(gate)} is ready for your approval")
    prod = spec.get("producer_blog_only") if st["client"]["type"] == "blog-only" else None
    out("run", (prod or spec["producer"]).format(slug=slug), f"prepare {S.plain(gate)}")


def evidence_and_briefs(st, slug, b):
    """CM-041 then CM-043: the evidence gate for the batch, then one brief per page in its own run.
    A blocked page gets no brief: facts interview → owner's answers → gate re-runs, or Paul's waiver."""
    bid = b["id"]
    if any(not S.evidence_state(st, p)[0] for p in b["pages"]):
        out("run", f"/build {slug} evidence {bid}", f"evidence gate for batch {bid} — the facts each page needs, "
            "marked Known / Unknown / Unverified / Conflict")
    blocked = [p for p in b["pages"] if not S.evidence_ok(st, p)[0]]
    for pid in b["pages"]:
        if pid not in blocked and not S.page_stage(st, pid, "brief"):
            out("run", f"/build {slug} brief {bid} {pid}", f"brief for {pid} (its own run)")
    if blocked:
        waive = " · ".join(f'/approve {slug} evidence:{p} --reason "<why you waive it>"' for p in blocked)
        fi = b.get("facts_interview") or {}
        newest = max(((st["pages"][p].get("evidence") or {}).get("at", "") for p in blocked), default="")
        if not fi or fi.get("at", "") < newest:
            out("run", f"/interview {slug} facts {bid}",
                f"the evidence gate blocked {', '.join(blocked)} — targeted questions for the owner (you send them). "
                f"Or waive instead: {waive}")
        out("wait", f"/interview {slug} facts-answers {bid}",
            f"waiting for the owner's answers to the facts interview ({fi.get('file')}) — when they arrive, this "
            f"records them in the Brand Guide and re-runs the gate. Or waive instead: {waive}")


def blog_posts(st, slug):
    """Stop at any written post that is not approved yet; else write the next one."""
    for pid, p in st["pages"].items():
        if p.get("type") != "blog":
            continue
        a = p.get("approval") or {}
        if p.get("file") and a.get("state") not in S.GATES["met_decisions"] or \
                (a and not S.page_approved(st, pid)[0]):
            out("decision", f"/approve {slug} page:{pid} --file \"{p.get('file')}\"" + extras(st),
                f"blog post {p.get('name') or pid} is ready for your approval")
        if S.page_approved(st, pid)[0] and not p.get("wp_id") and not (p.get("approval") or {}).get("baseline"):
            condition_step(st, slug, "wordpress_connected")
            out("run", f"/blog {slug} publish {pid}",
                f"WordPress draft of {p.get('name') or pid} from its approved file, and the publish handoff to Jonie")
    out("run", f"/blog {slug} next", "next post from the approved list")


def main():
    global PAUSE, SLUG
    slug = SLUG = sys.argv[1]
    st = S.load(slug)
    if "--continue" in sys.argv[2:] and st.get("review_pause"):
        p = st.pop("review_pause")
        S.save(slug, st)
        from lib import append, client_dir, now
        append(client_dir(slug) / "log.md", f"- REVIEW CONTINUED {now()[:16]} · after {p['step']} (run {p['run_id']}) · Paul typed /next\n")
    PAUSE = st.get("review_pause")
    left = R.unfinished(slug)
    if left:
        out("wait", f"/resume {slug}", f"run {left[0]} never finished — you decide: resume it, /verify it, "
            "/rollback it, or abort it")
    c = st["client"]

    condition_step(st, slug, "client_setup")
    if c["type"] == "blog-only":
        gate_step(st, slug, "entity_approved")
        gate_step(st, slug, "blog_topics_approved")
        blog_posts(st, slug)

    # ---- Discovery and audit
    gate_step(st, slug, "entity_approved")
    gate_step(st, slug, "proof_sheet_approved")
    # while the client has the sheet: crawl and data steps, then the audit
    if not S.gate_met(st, "audit_approved")[0]:
        if "S05" not in st["audit_steps"]:
            out("run", f"/crawl {slug}", "crawl the site while the client has the proof sheet")
        data = [r["id"] for r in steps.registry() if r["phase"] == "Client has sheet" and r["id"] != "S05"]
        if any(i not in st["audit_steps"] for i in data):
            out("run", f"/discovery {slug} data",
                "reviews, rankings, People Also Ask, backlinks, citations, grid, GSC — while the client has the sheet")
        gate_step(st, slug, "audit_approved")
    condition_step(st, slug, "proof_sheet_returned")
    gate_step(st, slug, "brand_guide_approved")
    gate_step(st, slug, "discovery_signed_off")

    # ---- Build. The technical blocker checklist and the site plan both need only the discovery
    # sign-off and run side by side: the checklist goes to Jonie as handoffs while the plan and
    # batches proceed; Paul confirms "blockers cleared" before release (release_approved requires it).
    if "blocker_checklist" not in (st.get("marks") or {}) and not S._decided(st, "blockers_cleared"):
        out("run", f"/build {slug} blockers", "technical blocker checklist (Jonie fixes these while the site plan goes ahead)")
    bp = st.get("build")
    if not bp:
        out("run", f"/build {slug} plan", "site plan for every service and location page, in one pass")
    if not S.check(st, "site_plan")[0]:
        out("decision", f"/approve {slug} site_plan --files {q([bp['site_plan']['file']])}",
            "the site plan is ready for your approval")
    for b in S.batches(st):
        bid, state = b["id"], b.get("state", "planned")
        if state == "written_back":
            continue
        if bid != "pilot" and not S.check(st, "pilot_corrections")[0]:
            out("run", f"/build {slug} pilot-corrections", "apply your pilot corrections to the specs before the next batch")
        files = b.get("files") or {}
        if state == "planned":
            evidence_and_briefs(st, slug, b)
        if not S.check(st, f"batch:{bid}:briefs")[0]:
            out("decision", f"/approve {slug} batch:{bid}:briefs --files {q(files.get('briefs') or [])}",
                f"the briefs for batch {bid} are ready for your approval (outline before prose; one brief per page, "
                "each written in its own run)")
        if state == "briefs_written":
            for pid in b["pages"]:    # CM-043: one page per run
                if not S.page_stage(st, pid, "draft"):
                    out("run", f"/build {slug} draft {bid} {pid}", f"draft and self-critique for {pid} (its own run)")
            out("run", f"/build {slug} batch {bid} drafts",
                f"batch review for {bid}: every draft side by side (portability, FAQ and heading collisions) and the "
                "semantic review table")
        drafts = b.get("drafts") or {}
        if not S.check(st, f"batch:{bid}:drafts")[0]:
            n = b.get("sem_findings") or 0
            failed = drafts.get("check_failure")
            out("decision", f"/approve {slug} batch:{bid}:drafts"
                + (" --sem <SEM items to apply, e.g. 1,3,4 — or none>" if n else "") + extras(st),
                (f"a re-check failed after applying your SEM picks ({failed}) — review and approve again"
                 if failed else f"the drafts for batch {bid} are ready: review each with the semantic review table "
                 + (f"({n} SEM item(s) found) " if n else "(nothing found) ") + "and approve them together"))
        if state in ("drafts_written", "sem_check_failed") and drafts.get("sem_ids") and not drafts.get("applied"):
            out("run", f"/build {slug} batch {bid} apply-sem",
                f"apply {', '.join(drafts['sem_ids'])} to batch {bid} and re-run the E-checks on the changed sections")
        if state in ("handed_off", "corrections_requested"):
            condition_step(st, slug, "wordpress_connected")
            h = b.get("handoff") or "the publish handoff"
            out("wait", f"/build {slug} published {bid}",
                f"waiting for Jonie to {'correct' if state == 'corrections_requested' else 'publish'} batch {bid} ({h}). "
                "When the worksheet comes back, this checks every live page against its approved file, adds alt "
                "text to the images and writes the batch back to the Brand Guide")
        if state in ("published", "verified"):
            out("run", f"/build {slug} published {bid}", f"finish checking batch {bid} and write it back")
        condition_step(st, slug, "wordpress_connected")
        out("run", f"/build {slug} ship {bid}",
            f"generate WordPress drafts for batch {bid} from the approved files (link tables filled) and hand "
            "publishing to Jonie")
    condition_step(st, slug, "pages_built")

    # ---- Finish and blog
    gate_step(st, slug, "link_wheel_approved")
    gate_step(st, slug, "blockers_cleared")
    gate_step(st, slug, "release_approved")
    gate_step(st, slug, "blog_map_approved")
    blog_posts(st, slug)


if __name__ == "__main__":
    main()
