#!/usr/bin/env python3
"""next.py — what happens next for a client, read from status.json and the safety log.

    next.py <slug>            one line of JSON: {"kind": run|decision|wait, "command": ..., "why": ...}

kind=run      -> /next runs this command now
kind=decision -> stop: Paul decides. "command" is the exact /approve line to type.
kind=wait     -> stop: waiting on the client, a VA or an unfinished run

Every decision gate in scripts/gates.json names its artifact (the files the approval covers)
and its producer. For each gate in order: met → move on; approved but its file changed →
ask Paul to re-approve; artifact recorded → stop at the decision; else run the producer.
"""
import json
import sys

import run as R
import status as S
import steps


def out(kind, command, why):
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
    out("run", f"/blog {slug} next", "next post from the approved list")


def main():
    slug = sys.argv[1]
    st = S.load(slug)
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

    # ---- Build
    gate_step(st, slug, "blockers_cleared")
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
            out("run", f"/build {slug} batch {bid}", f"briefs for batch {bid} ({b['label']})")
        if not S.check(st, f"batch:{bid}:briefs")[0]:
            out("decision", f"/approve {slug} batch:{bid}:briefs --files {q(files.get('briefs') or [])}",
                f"the briefs for batch {bid} are ready for your approval")
        if state == "briefs_written":
            out("run", f"/build {slug} batch {bid} drafts", f"drafts, self-critique and semantic review for batch {bid}")
        if not S.check(st, f"batch:{bid}:sem")[0]:
            out("decision", f"/approve {slug} batch:{bid}:sem --ids SEM-… --files {q(files.get('sem') or [])}",
                f"the semantic review table for batch {bid} is ready — approve the SEM IDs to apply (or --ids none)")
        if state == "drafts_written":
            out("run", f"/build {slug} batch {bid} apply-sem", f"apply the approved SEM IDs to batch {bid} and re-check")
        if not S.check(st, f"batch:{bid}:drafts")[0]:
            out("decision", f"/approve {slug} batch:{bid}:drafts --files {q(files.get('drafts') or [])}" + extras(st),
                f"the drafts for batch {bid} are ready for your approval")
        if state == "sem_applied":
            out("run", f"/implement {slug} batch {bid}", f"put batch {bid} in as WordPress drafts / handoffs")
        if state == "implemented":
            out("run", f"/verify {slug}", f"verify batch {bid}")
        if state == "verified":
            out("run", f"/build {slug} writeback {bid}", f"Brand Guide write-back for batch {bid}")
    condition_step(st, slug, "pages_built")

    # ---- Finish and blog
    gate_step(st, slug, "link_wheel_approved")
    gate_step(st, slug, "release_approved")
    gate_step(st, slug, "blog_map_approved")
    blog_posts(st, slug)


if __name__ == "__main__":
    main()
