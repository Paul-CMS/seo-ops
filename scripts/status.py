#!/usr/bin/env python3
"""status.py — read and maintain clients/<slug>/status.json.

    status.py init <slug> --name "Client Name" --domain example.com --type full|blog-only
                          --industry roofing [--sensitive yes|no] [--route A|B] [--drive-folder-id ID]
    status.py classify "<industry>"                  sensitive-industry check (CM-025)
    status.py show <slug> [--json]
    status.py require <slug> <gate> [<gate> ...]     exit 0 if met, 4 if not
    status.py set <slug> <field> <value>              non-gate fields only
    status.py view <slug> [--phase T] [--done T] [--waiting T ...] [--clear-waiting] [--next T]
    status.py page <slug> <page_id> --type service|location|county|homepage|about|blog
                          [--name N] [--url U] [--state S] [--file F]
    status.py mark <slug> <artifact> --file F [--file F2 ...]   record the files an approval will cover
    status.py plan <slug> --file plan.md --json plan.json
    status.py batch <slug> <batch_id> --state S [--files f1,f2]
    status.py pilot-corrections <slug> --note T
    status.py approval-record <slug>                  render the Drive Approval Record (Markdown)

Gates are NOT settable here. Only approve.py, run through /approve, can set a gate.

Voiding (Paul, 2026-10-02): an approval names the files it covers. If one of them changes,
only THAT gate stops counting as met. Later gates that depend on it stay open and are
flagged "upstream change — check whether it affects this"; Paul decides.
"""
import argparse
import json
import re
import sys
import time

from lib import ROOT, client_dir, die, now, read_json, sha12, write_json, config

GATES = json.loads((ROOT / "scripts" / "gates.json").read_text())

SETTABLE = {
    "client.name", "client.domain", "client.industry", "client.route",
    "client.drive_folder_id", "client.wp_env_prefix", "client.gbp_url",
    "client.gbp_website_url", "client.address_type", "client.notes", "client.state",
}
BATCH_STATES = ["planned", "briefs_written", "drafts_written", "sem_applied", "sem_check_failed",
                "implemented", "verified", "written_back"]
PAGE_STATES = ["planned", "brief_written", "draft_written", "approved", "implemented", "live",
               "written_back", "verified"]
# batch state -> the state every page in the batch moves to
BATCH_TO_PAGE = {"briefs_written": "brief_written", "drafts_written": "draft_written",
                 "sem_applied": "draft_written", "implemented": "implemented",
                 "verified": "verified", "written_back": "written_back"}
STAGES = ["briefs", "drafts"]   # two stops per batch: briefs (outline before prose), then drafts + SEM picks


def path(slug):
    return client_dir(slug) / "status.json"


def load(slug):
    return read_json(path(slug))


def save(slug, st):
    st["updated"] = now()
    write_json(path(slug), st)


# ------------------------------------------------------------------ sensitive industries (CM-025)
def classify(industry):
    """('yes', category, practitioner) · ('no', None, False) · ('unsure', hint, False)."""
    text = " " + re.sub(r"[^a-z0-9 ]+", " ", (industry or "").lower()) + " "
    cfg = config()
    for cat, spec in (cfg.get("sensitive_categories") or {}).items():
        for term in spec["terms"]:
            if re.search(r"\b" + term + r"\b", text):
                return "yes", cat, bool(spec.get("practitioner_signoff"))
    for hint in cfg.get("sensitive_unsure_hints") or []:
        if re.search(r"\b" + hint + r"\b", text):
            return "unsure", hint, False
    return "no", None, False


def new_status(slug, name, domain, ctype, industry, route=None, folder=None, sensitive=None,
               category=None, practitioner=False):
    return {
        "schema": 3,
        "client": {
            "slug": slug, "name": name, "domain": domain, "type": ctype,
            "industry": industry.lower(), "sensitive": sensitive,
            "sensitive_category": category, "practitioner_signoff": practitioner,
            "route": route, "drive_folder_id": folder, "wp_env_prefix": None,
            "gbp_url": None, "gbp_website_url": None, "address_type": None, "state": None,
            "imported": False, "notes": None,
        },
        "gates": {g: {"state": "pending"} for g in GATES["gates"]},
        "marks": {},
        "pages": {},
        "build": None,
        "audit_steps": {},
        "last_run": None,
        "spend": {"dataforseo_usd": 0.0},
        "client_view": {
            "_note": "The only client-facing part of this file. Plain language. Nothing else here is ever shown to a client.",
            "phase": "Getting started",
            "done": [],
            "waiting_on_client": [],
            "next": "We are researching your business before we ask you anything.",
        },
        "created": now(),
        "updated": now(),
    }


# ------------------------------------------------------------------ files and marks
def files_ok(files):
    """(ok, why) for a {path: sha} map recorded with an approval."""
    for f, h in (files or {}).items():
        p = ROOT / f
        if not p.exists():
            return False, f"file {f} no longer exists"
        if sha12(p) != h:
            return False, f"{f} changed after approval"
    return True, ""


def mark_files(st, name):
    return list(((st.get("marks") or {}).get(name) or {}).get("files") or {})


def plain(gate):
    spec = GATES["gates"].get(gate) or GATES["derived"].get(gate) or GATES["conditions"].get(gate) or {}
    return spec.get("plain") or spec.get("label") or gate


def label(gate):
    return (GATES["gates"].get(gate) or GATES["derived"].get(gate)
            or GATES["conditions"].get(gate) or {}).get("label", gate)


def requires(st, gate):
    spec = GATES["gates"].get(gate) or GATES["conditions"].get(gate) or {}
    if st["client"]["type"] == "blog-only" and "requires_blog_only" in spec:
        return spec["requires_blog_only"]
    return spec.get("requires", [])


# ------------------------------------------------------------------ conditions
def condition_met(st, name):
    """(ok, why) — checked from evidence, never approved."""
    slug = st["client"]["slug"]
    if name in (st.get("imported_conditions") or {}):
        return True, ""
    if name == "client_setup":
        log = path(slug).parent / "log.md"
        ok = log.exists() and re.search(r"^## RUN \S+-new-client\S* · FINISHED", log.read_text(), re.M)
        return bool(ok), ("" if ok else "the client has not been set up yet — run /new-client first")
    if name == "proof_sheet_returned":
        files = (st.get("marks") or {}).get("proof_sheet_returned", {}).get("files") or {}
        ok = bool(files) and all((ROOT / f).exists() for f in files)
        return ok, ("" if ok else "the client has not returned the proof sheet yet "
                    f"(when it arrives: /discovery {slug} sheet-returned)")
    if name == "audit_steps_complete":
        import steps
        left = steps.missing(st)
        return not left, ("" if not left else "audit steps with no outcome yet: " + ", ".join(x["id"] for x in left))
    if name == "pages_built":
        bs = batches(st)
        left = [b["id"] for b in bs if b.get("state") != "written_back"]
        ok = bool(bs) and not left
        return ok, ("" if ok else ("no site plan yet" if not bs else
                                   "batches not yet built and written back: " + ", ".join(left)))
    return False, f"unknown condition {name}"


def log_conditions(slug, st):
    """Append a CONDITION line to log.md the first time each condition is met. Returns names logged."""
    seen = st.setdefault("conditions_logged", {})
    new = []
    for c in GATES["conditions"]:
        if c in seen:
            continue
        ok, _ = condition_met(st, c)
        if ok:
            seen[c] = now()
            new.append(c)
    if new:
        with open(path(slug).parent / "log.md", "a", encoding="utf-8") as fh:
            for c in new:
                fh.write(f"\n## CONDITION · {seen[c]} · {label(c)} — met (system-verified)\n")
        save(slug, st)
    return new


# ------------------------------------------------------------------ gate logic
def _decided(st, gate):
    if gate in GATES["conditions"]:
        return condition_met(st, gate)[0]
    return (st["gates"].get(gate) or {}).get("state") in GATES["met_decisions"]


def _own_ok(st, gate):
    rec = st["gates"].get(gate) or {}
    if rec.get("state") not in GATES["met_decisions"]:
        return False, f"{plain(gate)} — not approved yet"
    ok, why = files_ok(rec.get("files"))
    return (True, "") if ok else (False, f"{plain(gate)} must be re-approved ({why})")


def gate_met(st, gate):
    """Return (ok, [reasons]). The gate's own files are checked; earlier gates only need their
    decision (an edit upstream is a flag, not a block)."""
    if gate in GATES["derived"]:
        reasons = []
        for r in GATES["derived"][gate]["requires"]:
            reasons += gate_met(st, r)[1]
        return not reasons, reasons
    if gate not in GATES["gates"] and gate not in GATES["conditions"]:
        return False, [f"unknown gate {gate}"]
    reasons = []
    seen = set()

    def walk(g):
        for r in requires(st, g):
            if r in seen:
                continue
            seen.add(r)
            if not _decided(st, r):
                reasons.append(condition_met(st, r)[1] if r in GATES["conditions"]
                               else f"{plain(r)} — not approved yet")
            walk(r)
    walk(gate)
    if gate in GATES["conditions"]:
        ok, why = condition_met(st, gate)
        if not ok:
            reasons.append(why)
        return not reasons, reasons
    ok, why = _own_ok(st, gate)
    if not ok:
        reasons.append(why)
    return not reasons, reasons


def upstream_changes(st, gate):
    """Earlier gates that are approved but whose approved files changed since."""
    out, seen = [], set()

    def walk(g):
        for r in requires(st, g):
            if r in seen:
                continue
            seen.add(r)
            rec = st["gates"].get(r) or {} if r in GATES["gates"] else {}
            if rec.get("state") in GATES["met_decisions"] and not files_ok(rec.get("files"))[0]:
                out.append(r)
            walk(r)
    if gate in GATES["gates"] or gate in GATES["conditions"]:
        walk(gate)
    return out


def page_approved(st, page_id):
    p = st["pages"].get(page_id)
    if not p:
        return False, f"page {page_id} is not registered"
    a = p.get("approval") or {}
    if a.get("baseline"):
        return True, ""
    b = batch_of(st, page_id)
    if b and not a:
        return batch_stage_ok(st, b["id"], "drafts")
    if a.get("state") not in GATES["met_decisions"]:
        return False, f"page {page_id} content is not approved yet"
    if st["client"]["sensitive"] and not a.get("sensitive_review"):
        return False, f"page {page_id}: sensitive client — the human review is not recorded"
    if st["client"]["practitioner_signoff"] and not a.get("practitioner"):
        return False, f"page {page_id}: the licensed practitioner's sign-off on health claims is not recorded"
    f = a.get("file")
    if f and (ROOT / f).exists() and a.get("sha") != sha12(ROOT / f):
        return False, f"page {page_id}: the approved file changed after approval — re-approve"
    return True, ""


# ------------------------------------------------------------------ build plan & batches
KIND_ORDER = {"service": 0, "location": 1, "county": 1, "homepage": 2, "about": 2}


def batches(st):
    return ((st.get("build") or {}).get("batches")) or []


def batch(st, bid):
    return next((b for b in batches(st) if b["id"] == bid), None)


def batch_of(st, page_id):
    return next((b for b in batches(st) if page_id in b["pages"]), None)


def _approval_ok(rec, label_, check_files=True):
    if not rec or rec.get("state") not in GATES["met_decisions"]:
        return False, f"{label_} is not approved yet"
    if check_files:
        ok, why = files_ok(rec.get("files"))
        if not ok:
            return False, f"{label_} must be re-approved: {why}"
    return True, ""


def batch_stage_ok(st, bid, stage, check_files=True):
    b = batch(st, bid)
    if not b:
        return False, f"batch {bid} is not in the site plan"
    ok, why = _approval_ok(b.get(stage), f"batch {bid} {stage}", check_files)
    if not ok:
        return ok, why
    if stage == "drafts":
        a = b["drafts"]
        if a.get("baseline"):
            return True, ""
        if st["client"]["sensitive"] and not a.get("sensitive_review"):
            return False, f"batch {bid}: sensitive client — the human review is not recorded"
        if st["client"]["practitioner_signoff"] and not a.get("practitioner"):
            return False, f"batch {bid}: the licensed practitioner's sign-off on health claims is not recorded"
    return True, ""


def batch_ready(st, bid, stage):
    """May work on <stage> of this batch start (or may Paul approve it)? (ok, [reasons]).
    Earlier approvals are checked by decision only (upstream edits are flags, not blocks)."""
    r = []
    bp = st.get("build") or {}
    ok, why = _approval_ok((bp.get("site_plan") or {}).get("approval"), "the site plan", False)
    if not ok:
        r.append(why)
    b = batch(st, bid)
    if not b:
        return False, r + [f"batch {bid} is not in the site plan"]
    prev = {"drafts": "briefs"}.get(stage)
    if prev:
        ok, why = batch_stage_ok(st, bid, prev, False)
        if not ok:
            r.append(why)
    if bid != "pilot" and not bp.get("pilot_waived"):
        ok, why = batch_stage_ok(st, "pilot", "briefs", False)
        if not ok:
            r.append("pilot: " + why)
        if not bp.get("pilot_corrections_applied"):
            r.append("the pilot corrections are not yet applied to the specs (status.py pilot-corrections)")
    mine = KIND_ORDER.get(b["kind"], 1)
    for o in batches(st):
        if o["id"] in ("pilot", bid):
            continue
        if KIND_ORDER.get(o["kind"], 1) < mine and o.get("state") != "written_back":
            r.append(f"{o['kind']} batch {o['id']} must be written back to the Brand Guide first")
    return not r, r


def check(st, target):
    """One entry point for every gate-like target. Returns (ok, [reasons])."""
    if target.startswith("page:"):
        ok, why = page_approved(st, target[5:])
        return ok, ([] if ok else [why])
    if target == "site_plan":
        ok, why = _approval_ok(((st.get("build") or {}).get("site_plan") or {}).get("approval"), "the site plan")
        return ok, ([] if ok else [why])
    if target == "pilot_corrections":
        bp = st.get("build") or {}
        ok = bool(bp.get("pilot_corrections_applied") or bp.get("pilot_waived"))
        return ok, ([] if ok else ["the pilot corrections are not yet applied to the specs"])
    m = re.match(r"^batch:([\w-]+):(briefs|drafts)(_ready)?$", target)
    if m:
        if m.group(3):
            return batch_ready(st, m.group(1), m.group(2))
        ok, why = batch_stage_ok(st, m.group(1), m.group(2))
        return ok, ([] if ok else [why])
    return gate_met(st, target)


def render_build(st):
    bp = st.get("build")
    if not bp:
        return "Build plan: none yet (site plan not written)."
    sp = (bp.get("site_plan") or {})
    ok, _ = check(st, "site_plan")
    pc = bp.get("pilot_corrections_applied")
    out = [f"Build plan: site plan {'APPROVED' if ok else 'not approved'} ({sp.get('file')})",
           f"  pilot corrections applied: {'yes — ' + pc['note'] if pc else ('waived (imported)' if bp.get('pilot_waived') else 'no')}"]
    for b in batches(st):
        marks = []
        for stage in STAGES:
            marks.append(f"{stage} {'OK' if batch_stage_ok(st, b['id'], stage)[0] else '--'}")
        out.append(f"  [{b['id']:10}] {b['kind']:8} {b['label'][:34]:34} {len(b['pages'])} pages · "
                   + " · ".join(marks) + f" · {b.get('state', 'planned')}")
    return "\n".join(out)


# ------------------------------------------------------------------ rendering
def visible_gates(st):
    for g in GATES["gates"]:
        if st["client"]["type"] == "blog-only" and g not in ("entity_approved", "blog_topics_approved", "blog_map_approved"):
            continue
        if st["client"]["type"] == "full" and g == "blog_topics_approved":
            continue
        yield g


def render_show(st):
    c = st["client"]
    out = [f"{c['name']} ({c['slug']}) · {c['domain']} · {c['type']} · industry {c['industry']}"
           + (f" · SENSITIVE ({c.get('sensitive_category')})" if c["sensitive"] else "")
           + (f" · Route {c['route']}" if c.get("route") else "")]
    out.append("")
    out.append("Conditions (checked by the system):")
    for g in GATES["conditions"]:
        if st["client"]["type"] == "blog-only" and g != "client_setup":
            continue
        ok, why = condition_met(st, g)
        out.append(f"  [{'MET ' if ok else '----'}] {g:24} {label(g)}" + ("" if ok else f" — {why}"))
    out.append("")
    out.append("Decisions (Paul, with /approve):")
    for g in visible_gates(st):
        rec = st["gates"].get(g, {})
        ok, why = gate_met(st, g)
        if ok:
            mark = "MET "
        elif rec.get("state") in GATES["met_decisions"]:
            mark = "VOID"
        else:
            mark = "----" if rec.get("state", "pending") == "pending" else rec.get("state", "")[:4].upper()
        by = f" · {rec.get('by')} {rec.get('at', '')[:10]}" if rec.get("by") else ""
        out.append(f"  [{mark}] {g:24} {label(g)}{by}")
        if mark == "VOID":
            out.append(f"         ! {why[-1]}")
        if rec.get("state") in GATES["met_decisions"]:
            for u in upstream_changes(st, g):
                out.append(f"         ! upstream change — {plain(u)} changed after it was approved; "
                           "check whether it affects this")
    for g in GATES["derived"]:
        ok, _ = gate_met(st, g)
        out.append(f"  [{'MET ' if ok else '----'}] {g:24} {label(g)}")
    if st["pages"]:
        out.append("")
        out.append("Pages:")
        for pid, p in st["pages"].items():
            ok, _ = page_approved(st, pid)
            out.append(f"  {pid:30} {p.get('type', ''):9} {p.get('state', ''):13}"
                       f" approved={'yes' if ok else 'no'}  {p.get('url') or ''}")
    out.append("")
    out.append(render_build(st))
    lr = st.get("last_run")
    if lr:
        out.append("")
        out.append(f"Last run: {lr.get('command')} {lr.get('run_id')} — {lr.get('result')}")
    cv = st["client_view"]
    out.append("")
    out.append(f"Client view: {cv['phase']} | next: {cv['next']}")
    return "\n".join(out)


def render_approval_record(st):
    c = st["client"]
    lines = [f"# {c['name']} - Approval Record", "",
             "Generated from the seo-ops system (clients/{}/status.json). Do not edit by hand —"
             " approvals are made with /approve and mirrored here.".format(c["slug"]), ""]
    for g in GATES["gates"]:
        rec = st["gates"][g]
        lines.append(f"## {label(g)}")
        lines.append("")
        lines.append(f"- Decision: **{rec.get('state', 'pending')}**")
        if rec.get("by"):
            lines.append(f"- Decided by: {rec['by']} · {rec.get('at', '')}")
        for cnd in rec.get("conditions") or []:
            lines.append(f"- Condition: {cnd}")
        for f, h in (rec.get("files") or {}).items():
            lines.append(f"- Approved version: `{f}` (sha {h})")
        if rec.get("note"):
            lines.append(f"- Note: {rec['note']}")
        lines.append("")
    if st["pages"]:
        lines.append("## Page content approvals")
        lines.append("")
        lines.append("| Page | Type | Decision | By | Date | Human review | Practitioner |")
        lines.append("|---|---|---|---|---|---|---|")
        for pid, p in st["pages"].items():
            a = p.get("approval") or {}
            lines.append(f"| {p.get('name') or pid} | {p.get('type')} | {a.get('state', 'pending')} | "
                         f"{a.get('by', '')} | {a.get('at', '')[:10]} | {a.get('sensitive_review') or ''} | "
                         f"{a.get('practitioner') or ''} |")
    return "\n".join(lines) + "\n"


def set_batch_state(st, b, state):
    b["state"] = state
    ps = BATCH_TO_PAGE.get(state)
    if ps:
        for pid in b["pages"]:
            p = st["pages"].setdefault(pid, {"state": "planned"})
            if not (p.get("approval") or {}).get("baseline"):
                p["state"] = ps


# ------------------------------------------------------------------ CLI
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("slug")
    s.add_argument("--name", required=True); s.add_argument("--domain", required=True)
    s.add_argument("--type", choices=["full", "blog-only"], required=True)
    s.add_argument("--industry", required=True); s.add_argument("--route", choices=["A", "B"])
    s.add_argument("--drive-folder-id"); s.add_argument("--sensitive", choices=["yes", "no"])
    s.add_argument("--practitioner", choices=["yes", "no"])
    s = sub.add_parser("classify"); s.add_argument("industry")
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("require"); s.add_argument("slug"); s.add_argument("gates", nargs="+")
    s = sub.add_parser("set"); s.add_argument("slug"); s.add_argument("field"); s.add_argument("value")
    s = sub.add_parser("view"); s.add_argument("slug")
    s.add_argument("--phase"); s.add_argument("--done", action="append")
    s.add_argument("--waiting", action="append"); s.add_argument("--clear-waiting", action="store_true")
    s.add_argument("--next")
    s = sub.add_parser("page"); s.add_argument("slug"); s.add_argument("page_id")
    s.add_argument("--type", choices=["service", "location", "county", "homepage", "about", "blog"])
    s.add_argument("--name"); s.add_argument("--url"); s.add_argument("--state", choices=PAGE_STATES)
    s.add_argument("--file")
    s = sub.add_parser("approval-record"); s.add_argument("slug")
    s = sub.add_parser("plan"); s.add_argument("slug"); s.add_argument("--file", required=True)
    s.add_argument("--json", required=True)
    s = sub.add_parser("batch"); s.add_argument("slug"); s.add_argument("batch_id")
    s.add_argument("--state", required=True, choices=BATCH_STATES); s.add_argument("--files")
    s.add_argument("--sem-table"); s.add_argument("--sem-findings", type=int)
    s.add_argument("--checks-passed", action="store_true"); s.add_argument("--note")
    s = sub.add_parser("pilot-corrections"); s.add_argument("slug"); s.add_argument("--note", required=True)
    s = sub.add_parser("mark"); s.add_argument("slug"); s.add_argument("name")
    s.add_argument("--file", required=True, action="append")
    a = ap.parse_args()

    if a.cmd == "classify":
        v, cat, prac = classify(a.industry)
        print(json.dumps({"sensitive": v, "category": cat, "practitioner_signoff": prac}))
        sys.exit(9 if v == "unsure" else 0)

    if a.cmd == "init":
        d = client_dir(a.slug, must_exist=False)
        if (d / "status.json").exists():
            die(f"{a.slug} already exists.")
        v, cat, prac = classify(a.industry)
        if a.sensitive:
            sensitive = a.sensitive == "yes"
            cat = (cat if v == "yes" else "set by Paul") if sensitive else None
            prac = (a.practitioner == "yes") if a.practitioner else (prac if sensitive else False)
        elif v == "unsure":
            die(f"ASK PAUL — is '{a.industry}' a sensitive industry (CM-025: health, legal, insurance, "
                f"financial)? It mentions '{cat}'. Re-run with --sensitive yes|no "
                "(and --practitioner yes for health claims).", 9)
        else:
            sensitive = v == "yes"
        for sub_ in ("discovery", "audit", "build", "finish", "blog", "handoffs",
                     "snapshots", "inputs", "inputs/crawl"):
            (d / sub_).mkdir(parents=True, exist_ok=True)
        st = new_status(a.slug, a.name, a.domain, a.type, a.industry, a.route, a.drive_folder_id,
                        sensitive, cat, prac)
        write_json(d / "status.json", st)
        (d / "log.md").write_text(
            f"# Safety log — {a.name}\n\nAppend-only. Every command writes STARTED before it acts "
            "and FINISHED after. Every change lists URL, old value, new value and result.\n"
            "Machine-readable mirror for /rollback: changes.jsonl.\n\n")
        (d / "changes.jsonl").write_text("")
        import records
        records.render(a.slug)
        print(f"created clients/{a.slug}/ (sensitive={sensitive}"
              + (f", category={cat}, practitioner sign-off={prac}" if sensitive else "") + ")")
        return

    st = load(a.slug)
    if a.cmd == "show":
        print(json.dumps(st, indent=2) if a.json else render_show(st))
    elif a.cmd == "require":
        reasons = []
        for g in a.gates:
            ok, rs = check(st, g)
            if not ok:
                reasons += [r for r in rs if r not in reasons]
        if reasons:
            print("Not yet — this needs:\n  - " + "\n  - ".join(reasons))
            print("\nOnly Paul can approve, with /approve.")
            sys.exit(4)
        print("gates met: " + ", ".join(a.gates))
    elif a.cmd == "set":
        if a.field not in SETTABLE:
            die(f"'{a.field}' is not settable here. Settable: {', '.join(sorted(SETTABLE))}."
                " Gates change only through /approve.")
        sect, key = a.field.split(".", 1)
        st[sect][key] = a.value
        save(a.slug, st); print(f"{a.field} = {a.value}")
    elif a.cmd == "view":
        cv = st["client_view"]
        if a.phase: cv["phase"] = a.phase
        if a.done: cv["done"] += [d for d in a.done if d not in cv["done"]]
        if a.clear_waiting: cv["waiting_on_client"] = []
        if a.waiting: cv["waiting_on_client"] += [w for w in a.waiting if w not in cv["waiting_on_client"]]
        if a.next: cv["next"] = a.next
        save(a.slug, st); print(json.dumps(cv, indent=2))
    elif a.cmd == "page":
        p = st["pages"].setdefault(a.page_id, {"state": "planned"})
        for k in ("type", "name", "url", "file"):
            v = getattr(a, k)
            if v: p[k] = v
        if a.state:
            if a.state == "approved":
                die("Page approval is set only through /approve.")
            p["state"] = a.state
        save(a.slug, st); print(json.dumps({a.page_id: p}, indent=2))
    elif a.cmd == "approval-record":
        print(render_approval_record(st), end="")
    elif a.cmd == "plan":
        if check(st, "site_plan")[0]:
            die("The site plan is already approved. Changing it needs Paul to re-open it (/approve <slug> site_plan --decision revise).")
        plan = json.loads(open(a.json).read())
        pages = {p["id"]: p for p in plan["pages"]}
        seen = {}
        for b in plan["batches"]:
            for pid in b["pages"]:
                if pid not in pages:
                    die(f"batch {b['id']} lists unknown page {pid}")
                if pid in seen:
                    die(f"page {pid} is in two batches ({seen[pid]}, {b['id']})")
                seen[pid] = b["id"]
        missing = [pid for pid, p in pages.items() if p["type"] in KIND_ORDER and pid not in seen]
        if missing:
            die("pages in no batch: " + ", ".join(missing))
        pilot = next((b for b in plan["batches"] if b["id"] == "pilot"), None)
        if not pilot or sorted(pages[x]["type"] for x in pilot["pages"]) != ["location", "service"]:
            die("the first batch must be 'pilot' with exactly 1 service + 1 location page")
        for pid, p in pages.items():
            st["pages"].setdefault(pid, {"state": "planned"}).update(
                {k: p[k] for k in ("type", "name", "url", "group") if k in p})
        st["build"] = {"site_plan": {"file": a.file, "approval": None},
                       "batches": [{**{k: b[k] for k in ("id", "kind", "label", "pages")},
                                    "state": "planned", "briefs": None, "drafts": None,
                                    "files": {}}
                                   for b in plan["batches"]],
                       "pilot_corrections_applied": None}
        st.setdefault("marks", {})["site_plan"] = {"files": {a.file: sha12(ROOT / a.file)}, "at": now(), "ts": time.time()}
        save(a.slug, st); print(render_build(st))
    elif a.cmd == "batch":
        b = batch(st, a.batch_id) or die(f"no batch {a.batch_id}")
        if a.state == "briefs_written":
            ok, why = batch_ready(st, a.batch_id, "briefs")
            if not ok:
                die(f"batch {a.batch_id}: " + "; ".join(why))
        stage_needed = {"drafts_written": "briefs", "sem_applied": "drafts", "sem_check_failed": "drafts",
                        "implemented": "drafts", "verified": "drafts", "written_back": "drafts"}.get(a.state)
        if stage_needed and not batch_stage_ok(st, a.batch_id, stage_needed, False)[0]:
            die(f"batch {a.batch_id}: {stage_needed} are not approved yet")
        fs = [f.strip() for f in (a.files or "").split(",") if f.strip()]
        for f in fs + ([a.sem_table] if a.sem_table else []):
            if not (ROOT / f).exists():
                die(f"{f} not found")
        log_line = None
        if a.state == "briefs_written" and fs:
            b.setdefault("files", {})["briefs"] = fs
        elif a.state == "drafts_written":
            if not fs or not a.sem_table or a.sem_findings is None:
                die("drafts_written needs --files <one draft per page> --sem-table <semantic review table> "
                    "--sem-findings <number of SEM rows>")
            # Paul reviews each draft with the batch's semantic review table and approves both at once.
            b.setdefault("files", {})["drafts"] = fs + [a.sem_table]
            b["sem_findings"] = a.sem_findings
            b["drafts"] = None
        elif a.state == "sem_applied":
            ids = (b.get("drafts") or {}).get("sem_ids") or []
            if not ids:
                die(f"batch {a.batch_id}: Paul approved no SEM items — nothing to apply")
            if not a.checks_passed or not fs:
                die("sem_applied needs --files <the drafts after applying the approved SEM items> and "
                    "--checks-passed (E1–E9 re-run on every changed section). If a check failed, use "
                    "--state sem_check_failed --note \"<which check, which page>\".")
            # Re-pin the approval to the applied versions: the change is exactly what Paul approved.
            table = [f for f in (b["drafts"].get("files") or {}) if f not in fs]
            b["drafts"]["files"] = {f: sha12(ROOT / f) for f in fs + table}
            b["drafts"]["applied"] = {"sem_ids": ids, "at": now(), "checks": "E1–E9 passed on changed sections"}
            b["files"]["drafts"] = fs + table
            log_line = (f"- SEM APPLIED {now()[:16]} · batch {a.batch_id} · {', '.join(ids)} · E-checks passed · "
                        "approval pinned to the applied versions\n")
        elif a.state == "sem_check_failed":
            if not a.note or not fs:
                die("sem_check_failed needs --files <the drafts as they now stand> --note \"<which check failed, where>\"")
            b["drafts"] = {**(b.get("drafts") or {}), "state": "revise",
                           "check_failure": a.note, "at": now()}
            b["files"]["drafts"] = fs + [f for f in b["files"].get("drafts", []) if f not in fs and "Semantic" in f]
            log_line = f"- SEM CHECK FAILED {now()[:16]} · batch {a.batch_id} · {a.note} · back to Paul\n"
        elif fs:
            b.setdefault("files", {})[a.state] = fs
        set_batch_state(st, b, a.state)
        save(a.slug, st)
        if log_line:
            with open(path(a.slug).parent / "log.md", "a", encoding="utf-8") as fh:
                fh.write(log_line)
        print(f"batch {a.batch_id}: {a.state}")
    elif a.cmd == "mark":
        files = {}
        for f in a.file:
            if not (ROOT / f).exists():
                die(f"{f} not found — a mark needs the file that proves it")
            files[f] = sha12(ROOT / f)
        st.setdefault("marks", {})[a.name] = {"files": files, "at": now(), "ts": time.time()}
        save(a.slug, st); print(f"{a.name}: {', '.join(files)}")
    elif a.cmd == "pilot-corrections":
        if not batch_stage_ok(st, "pilot", "briefs", False)[0]:
            die("the pilot briefs are not approved yet")
        st["build"]["pilot_corrections_applied"] = {"at": now(), "note": a.note}
        save(a.slug, st); print("pilot corrections recorded")


if __name__ == "__main__":
    main()
