#!/usr/bin/env python3
"""next.py — what happens next for a client, read from status.json and the safety log.

    next.py <slug>            one line of JSON: {"kind": run|decision|wait|review, "command": ..., "why": ...,
                              "stage": "n of N — name", "session_model": "haiku", "agents": "build (opus), researcher (sonnet)"}
                              (R1: start the stage's session on session_model; the agents' models are fixed)
    next.py <slug> --continue only at the start of a /next Paul typed: clears a review pause (logged)
    next.py <slug> --carry "<Paul's words>"   CM-067: a chat that cannot do what Paul asked hands his words to the next
    next.py <slug> --carried                  CM-067: the next chat did them (clears the carry)

kind=run      -> /next runs this command now
kind=decision -> stop: Paul decides. "command" is the exact /approve line to type.
kind=wait     -> stop: waiting on the client, a VA or an unfinished run — only when nothing else can run
kind=new_session -> stop (R2): this session already did another stage. Paul opens a new chat on the session
                 model and types /next <slug> there.
kind=review   -> stop: the stage that just finished is in review mode (CM-044). Paul looks at its
                 output and types /next to go on. A stage in auto mode never pauses. A pause before a
                 decision or a wait is not shown (that stop already pauses).

P8 (rewrite 2, Q7): a wait never stops writing. Inside Build, a wait (Jonie's blocker or publish handoff, the
owner's facts answers, a WordPress connection) is collected and the walk goes on to the next batch; /next returns the
first run or decision it finds, with "waits": every open wait (not blocking). It returns kind=wait only when nothing
else can run. An unfinished run and the discovery waits still stop.

Every decision gate in scripts/gates.json names its artifact (the files the approval covers)
and its producer. For each gate in order: met → move on; approved but its file changed →
ask Paul to re-approve; artifact recorded → stop at the decision; else run the producer.
"""
import json
import re
import sys
from pathlib import Path

import run as R
import stages
import status as S
import steps


SLUG = None
PAUSE = None   # the review pause left by the last finished run, if its stage is in review mode


WAITS = []     # P8: waits met on the way, not blocking


class Next(Exception):
    """Raised by out(): the one next action. compute() catches it."""

    def __init__(self, rec):
        super().__init__(rec["kind"])
        self.rec = rec


class Wait(Next):
    """A wait: soft() collects it and the walk goes on; otherwise it is the answer."""


def soft(fn, *args):
    """P8: run one independent part of the walk; a wait there is collected, not a stop."""
    try:
        fn(*args)
    except Wait as w:
        if all(w.rec["command"] != x["command"] for x in WAITS):
            WAITS.append(w.rec)


def decision_step(command):
    """The step that produced what an /approve line approves — its stage is the one the decision ends."""
    w = command.split()
    target = w[2] if len(w) > 2 else ""
    m = re.match(r"^batch:([\w-]+):(briefs|drafts)$", target)
    if m:
        return ("build:brief" if m.group(2) == "briefs" else "build:drafts"), m.group(1)
    if target == "site_plan":
        return "build:plan", None
    if target == "specs":   # global: the stage the client is in (from its last run)
        return None, None
    if target.startswith("evidence:"):
        return "build:evidence", None
    if target.startswith("page:"):
        return "blog:next", None
    spec = S.GATES["gates"].get(target)
    return stages.step_of_command((spec or {}).get("producer", "").replace("{slug}", SLUG)) if spec else (None, None)


def out(kind, command, why, at=None):
    step, batch = (at, None) if at else stages.step_of_command(command)
    if kind == "run" and PAUSE:
        kind, why = "review", (f"{PAUSE['step']} finished (run {PAUSE['run_id']}) and that stage is in review mode — "
                               f"look at what it produced, then type /next to go on. Next would be: {command} ({why})")
        command = f"/next {SLUG}"
    if kind == "run" and step:
        refusal = stages.session_conflict(SLUG, step, batch)   # R2: a new stage needs a new session
        if refusal:
            kind, why, command = "new_session", f"{refusal} Next there: {command} ({why})", f"/next {SLUG}"
    rec = {"kind": kind, "command": command, "why": why}
    if kind == "decision":   # P12: keep sessions short and warm
        rec["sitting"] = ("Answer and approve in one sitting; if you step away for more than a few minutes, end this "
                          "chat and start a new one with /next — STATUS.md carries everything.")
    if not step and kind == "decision":
        step, batch = decision_step(command)
    if not step and kind in ("decision", "review", "wait"):
        last = (S.load(SLUG).get("last_run") or {})
        step, batch = last.get("step"), last.get("batch")
    rec.update(stages.describe(step, batch))   # R1: the stage, the session model and the agents it uses
    if step:
        rec["step"] = step
    raise (Wait if kind == "wait" else Next)(rec)


def q(files):
    return '"' + ",".join(files) + '"'


def bg_reapproval(st):
    """CM-061 §6: approvals stay value-only; when the section's one write-back changed a value brand_guide_approved
    covers, its re-approval rides on the section's approval line — still one line for Paul."""
    return " brand_guide_approved" if not S.check(st, "brand_guide_approved")[0] else ""


def bg_before_ship(st, slug):
    """CM-066: Build under way and the Brand Guide edited after Paul approved it (not by his own answers — those keep the
    approval): the re-approval is asked at Build's stage, before ship, never as a step back to Stage 4."""
    if S._decided(st, "brand_guide_approved") and not S.gate_met(st, "brand_guide_approved")[0]:
        why = "; ".join(S.gate_met(st, "brand_guide_approved")[1])
        out("decision", approve_line(st, slug, ["brand_guide_approved"]),
            f"the Brand Guide was edited after you approved it ({why}) — look at what changed and approve it again. "
            "Build's work stands; ship waits for this one line", at="build:ship")


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
    if cond == "wordpress_connected" and (st["client"].get("cms") or "wordpress") not in ("wordpress", "unknown"):
        out("wait", f"/where {slug}", f"{st['client']['name']} runs on {st['client']['cms']}, not WordPress: the "
            "WordPress steps (/wp-check, WordPress drafts) are N/A. Paul decides how approved pages go live "
            "(a publish handoff to Jonie with the approved files)")
    if cond == "page_specs_approved":   # R3: methodology, approved once for every client
        out("decision", "/approve global specs",
            f"{why}. The specs in methodology/specs/ are the same for every client; approve them once before any "
            "audit scores pages against them or any page is written")
    if cond == "discovery_signed_off":
        for r in spec["requires"]:
            if r in S.GATES["conditions"]:
                condition_step(st, slug, r)
            else:
                gate_step(st, slug, r)
        return
    if cond == "blockers_cleared":
        if "blocker_checklist" not in (st.get("marks") or {}):
            out("run", f"/build {slug} blockers", "technical blocker checklist and its handoff to Jonie")
        if not st.get("blocker_handoffs") and not st.get("blockers_none"):
            out("run", f"/build {slug} blockers", "hand the blocker items to Jonie (one handoff, --blockers)")
        out("wait", f"/verify {slug}", f"{why}. When Jonie returns the blocker handoff, /verify checks every item; "
            "the blockers count as cleared when all are done and verified — no approval")
    if spec.get("wait_for"):
        out("wait", spec["producer"].format(slug=slug),
            f"waiting for {spec['wait_for']} — when it arrives, run this to record it")
    if spec.get("producer"):
        out("run", spec["producer"].format(slug=slug), why)
    out("wait", f"/where {slug}", why)


def gate_step(st, slug, gate):
    """Emit the next action for one decision, or return if it is met."""
    if S.gate_met(st, gate)[0]:
        return
    spec = S.GATES["gates"][gate]
    for r in S.requires(st, gate):
        if r in S.GATES["conditions"]:
            condition_step(st, slug, r)
    if gate == "audit_approved":   # Phase 7: was the audit_steps_complete condition
        ok, why = S.audit_steps_left(st)
        if not ok:
            out("run", f"/discovery {slug} audit", why)
    rec = st["gates"].get(gate) or {}
    marks = st.get("marks") or {}
    if rec.get("state") in S.GATES["met_decisions"]:
        files = S.mark_files(st, spec["artifact"]) or list(rec.get("files") or {})
        out("decision", f"/approve {slug} {gate} --files {q(files)}",
            f"{S.plain(gate)} changed after you approved it — re-approve it (later steps are not blocked; "
            "/where flags them as 'upstream change')")
    before = spec.get("before")
    if before and before["mark"] not in marks:
        out("run", before["producer"].format(slug=slug), f"needed before {S.plain(gate)}")
    if spec["artifact"] in marks:
        out("decision", f"/approve {slug} {gate} --files {q(S.mark_files(st, spec['artifact']))}",
            f"{S.plain(gate)} is ready for your approval")
    prod = spec.get("producer_blog_only") if st["client"]["type"] == "blog-only" else None
    out("run", (prod or spec["producer"]).format(slug=slug), f"prepare {S.plain(gate)}")


def approve_line(st, slug, gates):
    """One /approve line for one or several decisions. A single decision names its files; several in one line use
    the files each step recorded (approve.py refuses --files with several)."""
    if len(gates) == 1:
        g = gates[0]
        files = S.mark_files(st, S.GATES["gates"][g]["artifact"]) or list((st["gates"].get(g) or {}).get("files") or {})
        return f"/approve {slug} {g} --files {q(files)}"
    return f"/approve {slug} " + " ".join(gates)


def covers(st, gates):
    return "; ".join(f"{S.plain(g)}: {', '.join(Path(f.split('#')[0]).name + ('#' + f.split('#')[1] if '#' in f else '') for f in S.mark_files(st, S.GATES['gates'][g]['artifact']))}"
                     for g in gates)


def approval_one(st, slug):
    """Approval 1 (R3): the Decision Sheet + entity foundation and the client facts — one /approve line."""
    want = [g for g in ("entity_approved", "proof_sheet_approved") if not S.gate_met(st, g)[0]]
    if not want:
        return
    marks = st.get("marks") or {}
    if "entity_approved" in want and "entity_record" not in marks:
        out("run", f"/discovery {slug} discovery", "public research, the entity foundation and the Decision Sheet "
            "(every identity and format decision with a recommended default)")
    if "proof_sheet_approved" in want and "proof_sheet" not in marks:
        out("run", f"/discovery {slug} proof-sheet", "the client proof sheet — or, if the client already answered "
            f"directly, /discovery {slug} facts-direct (their answers saved verbatim; no sheet to approve)")
    out("decision", approve_line(st, slug, want),
        f"Discovery is ready for your approval in one line — {covers(st, want)}. Once approved, every Decision Sheet "
        "answer is settled for good and the data pulls can start")


def audit_review(st, slug):
    """The audit's one review sheet (Rewrite 4 Phase 3), not yet applied — Paul answers it in one line, or the system
    applies the defaults. audit_approved comes after."""
    ar = st.get("audit_review") or {}
    if not ar or ar.get("applied") or "audit_deliverables" not in (st.get("marks") or {}):
        return
    if ar.get("asks"):
        out("decision", f'/discovery {slug} review "accept all"',
            f"the audit review sheet has {ar['asks']} question(s) ({ar.get('client', 0)} for the client — Paul sends "
            f"client-questions.csv) and {ar.get('listed', 0)} decided for you ({ar.get('sheet')}): reply \"accept all\", or "
            "\"accept all except 3b\" — an empty answer takes the recommended option; the client's questions wait for "
            "the client")
    out("run", f"/discovery {slug} review", f"apply the audit review — nothing to ask; {ar.get('listed', 0)} decided for you")


def approval_two(st, slug):
    """Approval 2 (D3, Rewrite 4 Phase 3): the audit on its own, as soon as it is done — the URL decisions, safe fixes
    and the blocker handoff unlock there; the reconciled Brand Guide when the client's facts are back. The discovery
    sign-off is then a condition."""
    if not S.gate_met(st, "audit_approved")[0]:
        audit_review(st, slug)
        if "audit_deliverables" in (st.get("marks") or {}):
            out("decision", approve_line(st, slug, ["audit_approved"]),
                f"the audit is ready for your approval on its own — {covers(st, ['audit_approved'])}. Safe fixes and the "
                "technical blocker handoff start at once; the Brand Guide follows when the client's facts are back")
        return
    if "blocker_checklist" in (st.get("marks") or {}) and not st.get("blocker_handoffs") and not st.get("blockers_none") \
            and not S.condition_met(st, "blockers_cleared")[0]:
        out("run", f"/build {slug} blockers", "hand the technical blockers to Jonie (one handoff from the checklist "
            "the audit wrote) — they are fixed while the client's facts come back")
    if S.gate_met(st, "brand_guide_approved")[0]:
        return
    if S._decided(st, "brand_guide_approved") and st.get("build"):
        return   # CM-066: approved once and Build under way — a later edit never sends the client back to Stage 4; the
        # re-approval rides on Build's next approval line (bg_reapproval) or comes just before ship (bg_before_ship)
    if not S.condition_met(st, "proof_sheet_returned")[0]:
        out("wait", f"/discovery {slug} sheet-returned",
            "waiting for the client's facts (the returned proof sheet) — when they arrive, this records them, then "
            "reconcile, and the Brand Guide comes to you for approval")
    if "reconciled" not in (st.get("marks") or {}):
        out("run", f"/discovery {slug} reconcile", "reconcile the client's facts into the Brand Guide")
    out("decision", approve_line(st, slug, ["brand_guide_approved"]),
        f"the reconciled Brand Guide is ready for your approval — {covers(st, ['brand_guide_approved'])}. Discovery is "
        "then signed off automatically and Build starts")


def evidence_and_briefs(st, slug, b):
    """CM-054: one brief run for the batch — it runs the evidence gate per page (CM-041; research on disk first,
    CM-056), then writes every cleared page's brief. A blocked page gets no brief: facts interview → owner's answers →
    gate re-runs (then one more brief run for those pages), or Paul's waiver."""
    bid = b["id"]
    outline = S.route(b) == "outline"   # Rewrite 4: no brief — the write run runs the gate, then outlines by script
    if any(not S.evidence_state(st, p)[0] for p in b["pages"]):
        if outline:
            out("run", f"/build {slug} write {bid}", f"section {bid} in one run: the evidence gate per page, an outline "
                "per cleared page by script (no brief), one draft per page (each its own fresh sub-agent), the review")
        out("run", f"/build {slug} brief {bid}", f"briefs for batch {bid} in one run: the evidence gate per page "
            "(sources on disk searched first), then a brief for every page it clears")
    blocked = [p for p in b["pages"] if not S.evidence_ok(st, p)[0]]
    todo = [p for p in b["pages"] if p not in blocked and not S.page_stage(st, p, S.plan_stage(b))]
    if todo and not outline:
        out("run", f"/build {slug} brief {bid}", f"briefs for {', '.join(todo)} (one run for the batch)")
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


def review_sheet(st, slug, b, step):
    """CM-061: a section's review sheet for a step, not yet applied — Paul answers it in one line (questions), or the
    system applies the defaults (nothing to ask). The approval line comes after."""
    rv = (b.get("review") or {}).get(step)
    if not rv or rv.get("applied"):
        return
    bid = b["id"]
    if rv.get("asks"):
        out("decision", f'/build {slug} review {bid} {step} "accept all"',
            f"the {bid} {step} review sheet has {rv['asks']} question(s) for you and {rv.get('listed', 0)} decided for you "
            f"({rv.get('md')}): reply \"accept all\", or \"accept all except 7b, 12c\" — an empty answer takes the "
            "recommended option")
    out("run", f"/build {slug} review {bid} {step}",
        f"apply the {bid} {step} review — nothing to ask; {rv.get('listed', 0)} decided for you")


def build_batch(st, slug, b):
    """One batch's next step (P8: run softly, so a wait here never stops the next batch)."""
    bid, state = b["id"], b.get("state", "planned")
    if state in S.DRAFTED_OR_LATER:
        return
    if bid != "pilot" and S.batch(st, "pilot") and not S.check(st, "batch:pilot:drafts")[0]:
        return    # every batch after the pilot waits for the pilot's drafts approval (its corrections shape them)
    if state == "planned" and S.batch_order_blocks(st, bid):
        return    # an earlier-kind batch (service before location) goes first — the same check as batch_ready
    if state == "planned" or state == "briefs_written":
        condition_step(st, slug, "page_specs_approved")   # no page is written against unapproved specs
    if bid != "pilot" and not S.check(st, "pilot_corrections")[0]:
        out("run", f"/build {slug} pilot-corrections", "apply your pilot corrections to the specs before the next batch")
    files = b.get("files") or {}
    outline = S.route(b) == "outline"
    write_flow = bid == "pilot" or not S.briefs_need_approval(st, bid)   # P10
    if state == "planned" and write_flow and all(S.evidence_ok(st, p)[0] for p in b["pages"]):
        out("run", f"/build {slug} write {bid}",
            (f"section {bid} in one run: an outline per page by script from the approved plan and the spec (no brief), "
             "one draft per page (each from its own fresh sub-agent, CM-043), then the one draft review sheet"
             if outline else
             f"batch {bid} in one run: every brief, then one draft per page (each from its own fresh sub-agent, "
             "CM-043), then the batch review side by side"))
    if state == "planned":
        evidence_and_briefs(st, slug, b)
    if not outline and not S.check(st, f"batch:{bid}:briefs")[0]:
        review_sheet(st, slug, b, "briefs")
    if state in ("drafts_written", "sem_check_failed") and not S.check(st, f"batch:{bid}:drafts")[0]:
        review_sheet(st, slug, b, "drafts")
        drift = S.drafts_drifted(st, bid)
        if drift:   # CM-067: an edit made outside a run is recorded in a revision run before the write-back and approval
            out("run", f"/build {slug} revise {bid}", f"{len(drift)} draft(s) changed after they were recorded "
                f"({', '.join(drift[:5])}{' …' if len(drift) > 5 else ''}) — record them again in a revision run (it "
                "logs what changed), then the approval line")
    if bid == "pilot" and state in ("drafts_written", "sem_check_failed") and not S.check(st, "batch:pilot:briefs")[0]:
        n = b.get("sem_findings") or 0   # P10: the pilot's briefs and drafts are approved together, in one line
        out("decision", f"/approve {slug} batch:pilot:briefs batch:pilot:drafts mode:build:brief=auto{bg_reapproval(st)}"
            + (" --sem <SEM items to apply, e.g. 1,3,4 — or none>" if n else "") + extras(st),
            "the pilot's briefs and drafts are ready for one approval (and, in the same line, later batches' briefs "
            "switch to auto, so each later batch stops once, for its drafts): review the drafts with the semantic "
            "review table " + (f"({n} SEM item(s) found)" if n else "(nothing found)") + open_items_note(st, b))
    if not outline and not S.check(st, f"batch:{bid}:briefs")[0]:
        out("decision", f"/approve {slug} batch:{bid}:briefs{bg_reapproval(st)} --files {q(files.get('briefs') or [])}",
            f"the briefs for batch {bid} are ready for your approval (outline before prose; one brief per page, "
            "each written in its own run)")
    if not b.get("content_written_back") and (not outline or state in ("drafts_written", "sem_check_failed")):
        # CM-061 §6: once per section — at the brief approval, or (outline route) from the reviewed drafts, before
        # their one approval line; the next section reads it
        out("run", f"/build {slug} writeback {bid}",
            f"Brand Guide write-back for section {bid} (B3, C1/C2, C3) from its "
            + ("reviewed drafts, before their one approval" if outline else "approved briefs")
            + " — once per section; ship never writes it")
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
        out("decision", f"/approve {slug} batch:{bid}:drafts{bg_reapproval(st)}"
            + (" --sem <SEM items to apply, e.g. 1,3,4 — or none>" if n else "") + extras(st),
            (f"a re-check failed after applying your SEM picks ({failed}) — review and approve again"
             if failed else f"the drafts for batch {bid} are ready: review each with the semantic review table "
             + (f"({n} SEM item(s) found) " if n else "(nothing found) ") + "and approve them together")
            + open_items_note(st, b))
    if state in ("drafts_written", "sem_check_failed") and drafts.get("sem_ids") and not drafts.get("applied"):
        out("run", f"/build {slug} batch {bid} apply-sem",
            f"apply {', '.join(drafts['sem_ids'])} to batch {bid} and re-run the E-checks on the changed sections")
    # P9: no per-batch ship — every service and location page ships together once all are approved


def ship_all(st, slug):
    """P9: one ship run once every service and location batch is approved and written back."""
    import publish
    ok, why, todo = publish.ship_ready(st)
    if ok:
        condition_step(st, slug, "wordpress_connected")
        out("run", f"/build {slug} ship", f"every approved page as a WordPress draft in one run ({', '.join(todo)}) — "
            "link tables complete, every target already has its final URL")


def facts_answers_wait(st, slug, fr):
    """P10: the facts round's questions are answered once; writing goes on for every page that already cleared."""
    if not fr or not fr.get("questions"):
        return
    import settled
    ents = settled.entries(slug)
    open_ = [k for k, e in ents.items() if e.get("state") == "open" and k.startswith("fact:")]
    if open_:
        out("wait", f"/interview {slug} facts-answers all",
            f"waiting for the answers to the facts round ({fr.get('file')}; {len(open_)} fact(s) open) — when they "
            "arrive, each is recorded once (run.py fact / --settle) and the grids re-run")


def open_items_note(st, b):
    """P11: every placeholder per page, in the drafts approval line, so Paul approves knowingly."""
    import placeholders
    from lib import ROOT
    parts = []
    for f in (b.get("files") or {}).get("drafts") or []:
        p = ROOT / f
        if p.is_file() and "Semantic Review" not in f:
            items = placeholders.scan(p)
            if items:
                parts.append(f"{Path(f).name}: {placeholders.summary(items)}")
    return (". Placeholders still in the drafts (each becomes an 'Open items' notice on the WordPress draft and a "
            "row for Jonie): " + " | ".join(parts)) if parts else ". No placeholders in the drafts"


def publish_wait(st, slug, b):
    bid, state = b["id"], b.get("state")
    h = b.get("handoff") or "the publish handoff"
    out("wait", f"/build {slug} published {bid}",
        f"waiting for Jonie to {'correct' if state == 'corrections_requested' else 'publish'} the pages "
        f"({h}). When the worksheet comes back, this checks batch {bid}'s live pages against their approved "
        "files, adds alt text and updates the living handoff")


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


def compute(slug, cont=False):
    """The next action as a dict (kind, command, why, stage, session_model, agents)."""
    WAITS.clear()
    try:
        _walk(slug, cont)
        rec = {"kind": "wait", "command": f"/where {slug}", "why": "nothing left to do"}
    except Next as n:
        rec = n.rec
    _survey(slug)
    waits = [w for w in WAITS if w["command"] != rec["command"]]
    if rec["kind"] == "wait" and waits:   # nothing can run: the first wait met on the way is the answer
        rec, waits = waits[0], waits[1:] + ([rec] if rec["why"] != "nothing left to do" else [])
    rec["waits"] = [{"command": w["command"], "why": w["why"]} for w in waits]
    said = S.load(slug).get("carry") or []
    if said:   # CM-067: what Paul asked in an earlier chat that it could not do — the new chat acts on it first
        rec["paul_said"] = [f"{c['at'][:16]} · {c['text']}" for c in said]
    return rec


def carry(slug, text):
    """CM-067: a chat that cannot do what Paul asked (its stage is done, a new session is needed) records his words;
    the next chat's /next shows them first (paul_said) and STATUS.md lists them. Cleared with --carried once done."""
    from lib import append, client_dir, now
    st = S.load(slug)
    st.setdefault("carry", []).append({"at": now(), "text": " ".join(text.split())})
    S.save(slug, st)
    append(client_dir(slug) / "log.md", f"- PAUL SAID {now()[:16]} · carried to the next chat · {' '.join(text.split())}\n")


def carried(slug):
    from lib import append, client_dir, now
    st = S.load(slug)
    done = st.pop("carry", [])
    S.save(slug, st)
    if done:
        append(client_dir(slug) / "log.md", f"- PAUL SAID {now()[:16]} · done in this chat · {len(done)} item(s)\n")
    return done


def _survey(slug):
    """P8: every open wait in Build, even past the action found — listed as 'not blocking'."""
    st = S.load(slug)
    if not st.get("build"):
        return

    def look(fn, *args):
        try:
            fn(*args)
        except Wait as w:
            if all(w.rec["command"] != x["command"] for x in WAITS):
                WAITS.append(w.rec)
        except Next:
            pass
    for b in S.batches(st):
        if b.get("state") in ("handed_off", "corrections_requested"):
            look(publish_wait, st, slug, b)
        else:
            look(build_batch, st, slug, b)
    if st.get("blocker_handoffs") and not S.condition_met(st, "blockers_cleared")[0]:
        look(condition_step, st, slug, "blockers_cleared")


def main():
    args = sys.argv[2:]
    if "--carry" in args:   # CM-067
        carry(sys.argv[1], args[args.index("--carry") + 1])
        print("carried: the next chat's /next shows Paul's words first")
        return
    if "--carried" in args:
        print(f"cleared {len(carried(sys.argv[1]))} carried item(s)")
        return
    print(json.dumps(compute(sys.argv[1], "--continue" in args)))


def _walk(slug, cont):
    global PAUSE, SLUG
    SLUG = slug
    applied = S.apply_global(slug)   # global approvals reach a client here, in its own folder — never written from main
    if applied:
        import records
        from lib import git_commit
        records.render(slug)
        git_commit(f"{slug}: global approval(s) {', '.join(str(e['n']) for e in applied)} applied on /next", slug=slug)
    import urlmoves   # a URL moved: every record that points at the old URL follows it, here, in the client's own folder
    moved = urlmoves.apply(slug)
    if moved:
        import records
        from lib import git_commit
        records.render(slug)
        git_commit(f"{slug}: {len(moved)} record(s) pointing at a moved URL updated on /next\n\n" + "\n".join(moved[:40]), slug=slug)
    st = S.load(slug)
    routed = S.assign_routes(slug, st)   # Rewrite 4 (D5): which sections keep briefs and which take the outline route
    if routed:
        S.save(slug, st)
        import records
        from lib import git_commit
        records.render(slug)
        git_commit(f"{slug}: Rewrite 4 routes set on /next\n\n" + "\n".join(routed), slug=slug)
        st = S.load(slug)
    voided = S.void_unreviewed_approvals(slug, st)   # an approval whose pages do not match the reviewed versions stops counting
    if voided:
        S.save(slug, st)
        import records
        from lib import git_commit
        records.render(slug)
        git_commit(f"{slug}: {len(voided)} approval(s) voided on /next — the approved pages do not match the reviewed versions\n\n"
                   + "\n".join(voided[:20]), slug=slug)
        st = S.load(slug)
    if cont and st.get("review_pause"):
        p = st.pop("review_pause")
        S.save(slug, st)
        from lib import append, client_dir, now
        append(client_dir(slug) / "log.md", f"- REVIEW CONTINUED {now()[:16]} · after {p['step']} (run {p['run_id']}) · Paul typed /next\n")
    PAUSE = st.get("review_pause")
    left = R.unfinished(slug)
    if left:
        out("wait", f"/where {slug}", f"run {left[0]} never finished — you decide: resume it, /verify it, "
            "/rollback it, or abort it")
    c = st["client"]

    ok, why = S.client_set_up(st)
    if not ok:
        out("run", "/new-client", why)
    if c["type"] == "blog-only":
        gate_step(st, slug, "entity_approved")
        gate_step(st, slug, "blog_topics_approved")
        blog_posts(st, slug)

    # ---- Discovery and audit — two approvals (R3). Approval 1: the Decision Sheet + entity + client facts.
    approval_one(st, slug)
    # Data while the client has the sheet, then the audit (specs approved once, globally, before any scoring).
    if not S.gate_met(st, "audit_approved")[0]:
        if "S05" not in st["audit_steps"]:
            out("run", f"/crawl {slug}", "crawl the site while the client has the proof sheet")
        data = [r["id"] for r in steps.registry() if r["phase"] == "Client has sheet" and r["id"] not in ("S05", "S05b")]
        if any(i not in st["audit_steps"] for i in data):
            out("run", f"/discovery {slug} data",
                "reviews, rankings, People Also Ask, backlinks, citations, grid, GSC — one cost yes for the whole step")
        if "audit_deliverables" not in (st.get("marks") or {}):
            condition_step(st, slug, "page_specs_approved")   # gates the audit step, never an approval given
        for r in S.requires(st, "audit_approved"):
            if r in S.GATES["conditions"]:
                condition_step(st, slug, r)
        if "audit_deliverables" not in (st.get("marks") or {}):
            out("run", f"/discovery {slug} audit", "the audit: entity → architecture → page conformance → technical, "
                "then the fresh-context review")
    approval_two(st, slug)

    # ---- Build. The technical blocker checklist and the site plan both need only the discovery
    # sign-off and run side by side: the checklist goes to Jonie as handoffs while the plan and
    # batches proceed; Paul confirms "blockers cleared" before release (release_approved requires it).
    condition_step(st, slug, "discovery_signed_off")
    if "blocker_checklist" not in (st.get("marks") or {}) and not S.condition_met(st, "blockers_cleared")[0]:
        out("run", f"/build {slug} blockers", "technical blocker checklist and one handoff to Jonie (she fixes them "
            "while the site plan goes ahead)")
    bp = st.get("build")
    if not bp:
        out("run", f"/build {slug} plan", "site plan for every service and location page, in one pass")
    if not S.check(st, "site_plan")[0]:
        out("decision", f"/approve {slug} site_plan --files {q([bp['site_plan']['file']])}",
            "the site plan is ready for your approval")
    # P10: one facts round for every page, before the pilot
    fr = (st.get("build") or {}).get("facts_round")
    if not fr and any(not S.evidence_state(st, p)[0] for b in S.batches(st) for p in b["pages"]
                      if b.get("state") in ("planned", None)):
        out("run", f"/build {slug} facts", "one facts round for every page: the evidence grids, the researcher looks up "
            "every public fact, reviews attached (CM-057), then one pre-filled question set grouped by fact")
    soft(facts_answers_wait, st, slug, fr)
    # CM-055: batches are drafted one after another and never wait on publishing; every page goes to Jonie together.
    for b in S.batches(st):
        soft(build_batch, st, slug, b)
    bg_before_ship(st, slug)
    soft(ship_all, st, slug)
    if S.batches(st) and S.condition_met(st, "pages_drafted")[0]:
        if any(b.get("state") == "drafted" for b in S.batches(st)):
            out("run", f"/build {slug} handoff", "every page is a WordPress draft: one living publish handoff to Jonie "
                "for all of them (with their redirects and the open technical blockers), published together")
        for b in S.batches(st):
            bid, state = b["id"], b.get("state")
            if state in ("published", "verified"):
                out("run", f"/build {slug} published {bid}", f"finish checking batch {bid} and write it back")
        for b in S.batches(st):
            bid, state = b["id"], b.get("state")
            if state in ("handed_off", "corrections_requested"):
                soft(publish_wait, st, slug, b)   # P8: every batch Jonie has is listed, none stops the others
    condition_step(st, slug, "pages_built")

    # ---- Finish and blog
    condition_step(st, slug, "blockers_cleared")   # CM-064: no wheel approval — the wheel and schema ship with the drafts
    gate_step(st, slug, "release_approved")
    gate_step(st, slug, "blog_map_approved")
    blog_posts(st, slug)


if __name__ == "__main__":
    main()
