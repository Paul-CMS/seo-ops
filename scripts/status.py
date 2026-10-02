#!/usr/bin/env python3
"""status.py — read and maintain clients/<slug>/status.json.

    status.py init <slug> --name "Client Name" --domain example.com --type full|blog-only
                          --industry roofing [--route A|B] [--drive-folder-id ID]
    status.py show <slug> [--json]
    status.py require <slug> <gate> [<gate> ...]     exit 0 if met, 4 if not
    status.py set <slug> <field> <value>              non-gate fields only
    status.py view <slug> [--phase T] [--done T] [--waiting T ...] [--clear-waiting] [--next T]
    status.py page <slug> <page_id> --type service|location|county|homepage|about|blog
                          [--name N] [--url U] [--state S] [--file F]
    status.py approval-record <slug>                  render the Drive Approval Record (Markdown)

Gates are NOT settable here. Only approve.py, run through /approve, can set a gate.
"""
import argparse
import json
import sys

from lib import ROOT, client_dir, die, now, read_json, sha12, write_json, config

GATES = json.loads((ROOT / "scripts" / "gates.json").read_text())

SETTABLE = {
    "client.name", "client.domain", "client.industry", "client.route",
    "client.drive_folder_id", "client.wp_env_prefix", "client.gbp_url",
    "client.gbp_website_url", "client.address_type", "client.notes",
}
PAGE_STATES = ["planned", "brief_written", "draft_written", "approved", "live",
               "written_back", "verified"]


def path(slug):
    return client_dir(slug) / "status.json"


def load(slug):
    return read_json(path(slug))


def save(slug, st):
    st["updated"] = now()
    write_json(path(slug), st)


def new_status(slug, name, domain, ctype, industry, route=None, folder=None):
    cfg = config()
    sensitive = industry.lower() in cfg["sensitive_industries"]
    return {
        "schema": 1,
        "client": {
            "slug": slug, "name": name, "domain": domain, "type": ctype,
            "industry": industry.lower(), "sensitive": sensitive,
            "practitioner_signoff": industry.lower() in cfg["practitioner_signoff_industries"],
            "route": route, "drive_folder_id": folder, "wp_env_prefix": None,
            "gbp_url": None, "gbp_website_url": None, "address_type": None,
            "imported": False, "notes": None,
        },
        "gates": {g: {"state": "pending"} for g in GATES["gates"]},
        "pages": {},
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


# ------------------------------------------------------------------ gate logic
def _gate_record_ok(st, gate):
    rec = st["gates"].get(gate, {})
    if rec.get("state") not in GATES["met_decisions"]:
        return False, f"{gate} is '{rec.get('state', 'pending')}'"
    for f, h in (rec.get("files") or {}).items():
        p = ROOT / f
        if not p.exists():
            return False, f"{gate}: approved file {f} no longer exists — re-approve"
        if sha12(p) != h:
            return False, f"{gate}: approved file {f} changed after approval — re-approve"
    return True, ""


def gate_met(st, gate, _seen=None):
    """Return (ok, [reasons]). Checks prerequisites too."""
    _seen = _seen or set()
    if gate in _seen:
        return True, []
    _seen.add(gate)
    reasons = []
    if gate in GATES["derived"]:
        reqs = GATES["derived"][gate]["requires"]
        for r in reqs:
            ok, rs = gate_met(st, r, _seen)
            reasons += rs
        return not reasons, reasons
    if gate not in GATES["gates"]:
        return False, [f"unknown gate {gate}"]
    spec = GATES["gates"][gate]
    reqs = spec["requires"]
    if st["client"]["type"] == "blog-only" and "requires_blog_only" in spec:
        reqs = spec["requires_blog_only"]
    for r in reqs:
        ok, rs = gate_met(st, r, _seen)
        reasons += rs
    ok, why = _gate_record_ok(st, gate)
    if not ok:
        reasons.append(why)
    return not reasons, reasons


def label(gate):
    return (GATES["gates"].get(gate) or GATES["derived"].get(gate) or {}).get("label", gate)


def page_approved(st, page_id):
    p = st["pages"].get(page_id)
    if not p:
        return False, f"page {page_id} is not registered"
    a = p.get("approval") or {}
    if a.get("state") not in GATES["met_decisions"]:
        return False, f"page {page_id} content is not approved"
    if st["client"]["sensitive"] and not a.get("sensitive_review"):
        return False, f"page {page_id}: sensitive client — human review not recorded"
    if st["client"]["practitioner_signoff"] and not a.get("practitioner"):
        return False, f"page {page_id}: licensed practitioner sign-off on health claims not recorded"
    f = a.get("file")
    if f and (ROOT / f).exists() and a.get("sha") != sha12(ROOT / f):
        return False, f"page {page_id}: approved file changed after approval — re-approve"
    return True, ""


# ------------------------------------------------------------------ rendering
def render_show(st):
    c = st["client"]
    out = [f"{c['name']} ({c['slug']}) · {c['domain']} · {c['type']} · industry {c['industry']}"
           + (" · SENSITIVE" if c["sensitive"] else "")
           + (f" · Route {c['route']}" if c.get("route") else "")]
    out.append("")
    out.append("Gates:")
    for g in GATES["gates"]:
        if st["client"]["type"] == "blog-only" and g not in ("b1_entity", "bab_topics", "block4"):
            continue
        if st["client"]["type"] == "full" and g == "bab_topics":
            continue
        rec = st["gates"].get(g, {})
        ok, _ = gate_met(st, g)
        mark = "MET " if ok else ("----" if rec.get("state") == "pending" else rec.get("state", "")[:4].upper())
        by = f" · {rec.get('by')} {rec.get('at', '')[:10]}" if rec.get("by") else ""
        out.append(f"  [{mark}] {g:24} {label(g)}{by}")
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
                         f"{a.get('by', '')} | {a.get('at', '')[:10]} | {a.get('sensitive_review', '')} | "
                         f"{a.get('practitioner', '')} |")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ CLI
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("slug")
    s.add_argument("--name", required=True); s.add_argument("--domain", required=True)
    s.add_argument("--type", choices=["full", "blog-only"], required=True)
    s.add_argument("--industry", required=True); s.add_argument("--route", choices=["A", "B"])
    s.add_argument("--drive-folder-id")

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
    a = ap.parse_args()

    if a.cmd == "init":
        d = client_dir(a.slug, must_exist=False)
        if (d / "status.json").exists():
            die(f"{a.slug} already exists.")
        for sub_ in ("discovery", "audit", "build", "finish", "blog", "handoffs",
                     "snapshots", "inputs", "inputs/crawl"):
            (d / sub_).mkdir(parents=True, exist_ok=True)
        st = new_status(a.slug, a.name, a.domain, a.type, a.industry, a.route, a.drive_folder_id)
        write_json(d / "status.json", st)
        (d / "log.md").write_text(
            f"# Safety log — {a.name}\n\nAppend-only. Every command writes STARTED before it acts "
            "and FINISHED after. Every change lists URL, old value, new value and result.\n"
            "Machine-readable mirror for /rollback: changes.jsonl.\n\n")
        (d / "changes.jsonl").write_text("")
        (d / "decisions.md").write_text(
            f"# Decision log — {a.name}\n\nAppend-only. Paul Exceptions, applied defaults, "
            "N/A rationales and deviations, with the finding or page IDs they affect.\n\n")
        print(f"created clients/{a.slug}/ (sensitive={st['client']['sensitive']})")
        return

    st = load(a.slug)
    if a.cmd == "show":
        print(json.dumps(st, indent=2) if a.json else render_show(st))
    elif a.cmd == "require":
        reasons = []
        for g in a.gates:
            if g.startswith("page:"):
                ok, why = page_approved(st, g[5:])
                if not ok:
                    reasons.append(why)
                continue
            ok, rs = gate_met(st, g)
            if not ok:
                reasons.append(f"{label(g)}: " + "; ".join(rs))
        if reasons:
            print("REFUSED — gate not met:\n  - " + "\n  - ".join(reasons))
            print("\nOnly Paul can set a gate, with /approve.")
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


if __name__ == "__main__":
    main()
