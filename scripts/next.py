#!/usr/bin/env python3
"""next.py — what happens next for a client, read from status.json and the safety log.

    next.py <slug>            one line of JSON: {"kind": run|decision|wait|done, "command": ..., "why": ...}

kind=run      -> /next runs this command now
kind=decision -> stop: Paul decides (the /approve line is in "command")
kind=wait     -> stop: waiting on the client, a VA or an unfinished run
"""
import json
import sys

import run as R
import status as S
import steps


def out(kind, command, why):
    print(json.dumps({"kind": kind, "command": command, "why": why}))
    sys.exit(0)


def met(st, g):
    return S.check(st, g)[0]


def step_done(st, *ids):
    have = st.get("audit_steps") or {}
    return all(i in have for i in ids)


def main():
    slug = sys.argv[1]
    st = S.load(slug)
    left = R.unfinished(slug)
    if left:
        out("wait", f"/resume {slug}", f"run {left[0]} never finished — Paul decides: resume, /verify, /rollback or abort")
    c = st["client"]

    if c["type"] == "blog-only":
        if not met(st, "b1_entity"):
            if not step_done(st, "S03"):
                out("run", f"/blog {slug} intake", "short intake and entity foundation")
            out("decision", f"/approve {slug} b1_entity", "entity foundation is ready for your approval")
        if not met(st, "bab_topics"):
            out("run" if not (st.get("marks") or {}).get("topics_written") else "decision",
                f"/blog {slug} topics" if not (st.get("marks") or {}).get("topics_written") else f"/approve {slug} bab_topics",
                "topic list, checked against the site's service and location FAQs")
        out("run", f"/blog {slug} next", "next post from the approved topic list")

    # ---- Block 1
    if not met(st, "b1_entity"):
        if not step_done(st, "S01", "S02", "S03"):
            out("run", f"/discovery {slug} discovery", "discovery and entity research")
        out("decision", f"/approve {slug} b1_entity", "entity foundation is ready for your approval")
    if not met(st, "b1_proof_sheet_ready"):
        if not step_done(st, "S04"):
            out("run", f"/discovery {slug} proof-sheet", "build the client proof sheet")
        out("decision", f"/approve {slug} b1_proof_sheet_ready", "proof sheet ready — approve, then you send it")
    # while the client has the sheet: data steps, then the audit
    if not step_done(st, "S05"):
        out("run", f"/crawl {slug}", "crawl the site while the client has the proof sheet")
    if not step_done(st, "S06", "S07", "S08", "S09", "S10", "S11"):
        out("run", f"/discovery {slug} data", "reviews, rankings, backlinks, citations, grid, GSC — while the client has the sheet")
    if not met(st, "b1_audit"):
        if steps.missing(st):
            out("run", f"/discovery {slug} audit", "the audit: entity → architecture → conformance → technical, then review")
        out("decision", f"/approve {slug} b1_audit", "audit deliverables ready — approving unlocks the safe fixes")
    if not met(st, "b1_proof_sheet_returned"):
        out("wait", f"/approve {slug} b1_proof_sheet_returned",
            "waiting for the client's proof sheet (safe fixes can go out meanwhile: /implement " + slug + " safe)")
    if not met(st, "b1_brand_guide"):
        out("run" if not (st.get("marks") or {}).get("reconciled") else "decision",
            f"/discovery {slug} reconcile" if not (st.get("marks") or {}).get("reconciled") else f"/approve {slug} b1_brand_guide",
            "reconcile the client's answers into the Brand Guide")
    if not met(st, "block1"):
        out("decision", f"/approve {slug} block1", "Block 1 is complete — approve to start Build")

    # ---- Build
    if not met(st, "b2_blockers"):
        out("run", f"/build {slug} blockers", "technical blocker checklist, then /implement; you approve when cleared")
    bp = st.get("build")
    if not bp:
        out("run", f"/build {slug} plan", "site plan for every service and location page, in one pass")
    if not met(st, "site_plan"):
        out("decision", f"/approve {slug} site_plan", "site plan ready for your approval")
    for b in S.batches(st):
        bid, state = b["id"], b.get("state", "planned")
        if bid != "pilot" and not bp.get("pilot_corrections_applied"):
            out("run", f"/build {slug} pilot-corrections", "apply your pilot corrections to the specs before the next batch")
        if state == "planned":
            out("run", f"/build {slug} batch {bid}", f"briefs for batch {bid} ({b['label']})")
        if not met(st, f"batch:{bid}:briefs"):
            out("decision", f"/approve {slug} batch:{bid}:briefs", f"briefs for batch {bid} ready")
        if state == "briefs_written":
            out("run", f"/build {slug} batch {bid} drafts", f"drafts for batch {bid}")
        if not met(st, f"batch:{bid}:drafts"):
            out("decision", f"/approve {slug} batch:{bid}:drafts", f"drafts for batch {bid} ready")
        if state == "drafts_written":
            out("run", f"/implement {slug} batch {bid}", f"put batch {bid} in as WordPress drafts / handoffs")
        if state == "implemented":
            out("run", f"/verify {slug}", f"verify batch {bid}")
        if state == "verified":
            out("run", f"/build {slug} writeback {bid}", f"Brand Guide write-back for batch {bid}")
    if not met(st, "block2"):
        out("decision", f"/approve {slug} block2", "every page is live and written back — approve to build the link wheel")

    # ---- Finish and blog
    if not met(st, "block3"):
        out("run", f"/finish {slug} wheel", "link wheel, then verify; you approve block3")
    if not met(st, "block5"):
        out("run", f"/finish {slug}", "schema, QA, release; you approve block5")
    if not met(st, "block4"):
        out("run", f"/blog {slug} map", "Blog Decision Map; you approve block4")
    out("run", f"/blog {slug} next", "next blog rewrite brief / post")


if __name__ == "__main__":
    main()
