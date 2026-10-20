#!/usr/bin/env python3
"""render.py — every Markdown deliverable and summary is rendered from its CSV/JSON by template (Rewrite 4 Phase 1).
Agents never type a rendered file; to change one, change the register row and render again.

    render.py manifest  <slug> [--run R]   Evidence Manifest        ← 00-manifest.csv + 00-crosschecks.md + step outcomes
    render.py urlmap    <slug> [--run R]   URL Decision Map view     ← url-decision-map.csv
    render.py findings  <slug> [--run R]   Finding Register view     ← findings.csv (latest revision of each finding)
    render.py auditsheet <slug> [--run R]  the audit review sheet    ← the two registers: what Paul decides, what is listed
    render.py blockers  <slug> [--run R]   Technical Blocker Checklist ← findings.csv + the blocker handoffs
    render.py siteplan  <slug> [--run R]   site plan view            ← the plan JSON (build/site-plan*.plan.json)
    render.py status    <slug>             STATUS.md and the living records (records.py)
    render.py all       <slug> [--run R]   every one of these whose source file exists
    render.py … --out DIR                      write to DIR instead; nothing in the client's folder changes
    render.py check     <slug>             exit 4 if a rendered file is older than its source (re-render it)

Audit files are written to clients/<slug>/audit/<date>/deliverables/, build files to clients/<slug>/build/, named
"<Client> - <Artifact> - REVIEW.md" (naming-convention.md). Free, offline, deterministic: the same sources always
give the same file. With --run each render is recorded as one change in the safety log. A file an approval covers is never rendered over
(that would void the approval): --out looks at a new version, --force is for when Paul asked for the revision.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import status as S
from lib import ROOT, client_dir, die, now, read_json

NAMES = {"manifest": "Evidence Manifest", "urlmap": "URL Decision Map", "findings": "Finding Register",
         "auditsheet": "Audit Review Sheet", "blockers": "Technical Blocker Checklist", "siteplan": "Site Plan"}
csv.field_size_limit(10 ** 8)


# ------------------------------------------------------------------ helpers
def cell(v, n=200):
    v = re.sub(r"\s+", " ", str(v if v is not None else "")).replace("|", "/").strip()
    return v if len(v) <= n else v[: n - 1].rstrip() + "…"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(cell(c, 300) if not isinstance(c, tuple) else cell(c[0], c[1]) for c in r) + " |" for r in rows]
    return out


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def audit_dir(slug):
    """The newest audit working folder, clients/<slug>/audit/<YYYY-MM-DD>/ (None before the audit starts)."""
    d = client_dir(slug) / "audit"
    hits = sorted(x for x in d.glob("*") if x.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", x.name)) if d.exists() else []
    return hits[-1] if hits else None


def latest(rows, key="Finding ID", rev="ext_revision"):
    """The latest revision of each register row (append-only registers: a revision is a new row)."""
    best = {}
    for r in rows:
        k = r.get(key)
        if not k:
            continue
        try:
            n = int(r.get(rev) or 1)
        except ValueError:
            n = 1
        if k not in best or n >= best[k][0]:
            best[k] = (n, r)
    return [r for _, r in best.values()]


def need_audit(slug):
    return audit_dir(slug) or die(f"no audit folder yet for {slug} (clients/{slug}/audit/<date>/) — nothing to render")


def head(st, artifact, sources, note=""):
    return [f"# {st['client']['name']} - {artifact} - REVIEW", "",
            f"**Status:** REVIEW — awaiting Paul. Rendered {now()[:16]} by `scripts/render.py` from "
            f"{', '.join('`' + s + '`' for s in sources)}. Rendered, never edited: to change anything, change the "
            f"source row and render again." + (f" {note}" if note else ""), ""]


def out_path(slug, kind, st):
    name = f"{st['client']['name']} - {NAMES[kind]} - REVIEW.md"
    if kind in ("blockers", "siteplan"):
        d = client_dir(slug) / "build"
    else:
        a = need_audit(slug)
        d = a / "deliverables"
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def sev(r):
    return {"High": 0, "Medium": 1, "Low": 2}.get(r.get("Priority", ""), 3)


# ------------------------------------------------------------------ renderers (each returns (lines, [source files]))
def r_manifest(slug, st):
    a = need_audit(slug)
    mf = a / "00-manifest.csv"
    if not mf.is_file():
        die(f"{mf.relative_to(ROOT)} is missing — run the ingest first (pipeline.py {slug} inventory)")
    rows = read_csv(mf)
    srcs = [str(mf.relative_to(ROOT))]
    out = head(st, NAMES["manifest"], ["00-manifest.csv", "00-crosschecks.md", "audit step outcomes"])
    out += ["## 1 · Sources", "", f"{len(rows)} evidence file(s). Tool settings that repeat are shown once below the table.", ""]
    settings, key = {}, {}
    for r in rows:
        t = r.get("tool_settings", "")
        if t and t not in settings:
            settings[t] = f"T{len(settings) + 1}"
        key[r["source_id"]] = settings.get(t, "")
    out += table(["ID", "File", "Recognised as", "Category", "Rows", "SHA-256 (12)", "Settings", "Date window", "Geography / device"],
                 [[r["source_id"], (r["file"], 90), r["recognised_as"], r["category"], r["rows"], r["sha256_12"],
                   key[r["source_id"]], (r.get("date_window", ""), 80), (r.get("geography_device", ""), 80)] for r in rows])
    if settings:
        out += ["", "### Tool settings", ""] + [f"- **{k}** — {t}" for t, k in settings.items()]
    limits = sorted({r.get("scope_limits", "") for r in rows if r.get("scope_limits")})
    if limits:
        out += ["", "### Scope limits", ""] + [f"- {l}" for l in limits]
    import steps
    have = st.get("audit_steps") or {}
    out += ["", "## 2 · Step outcomes", "", "Every registered step has an outcome, or this table says **NO OUTCOME**.", ""]
    out += table(["Step", "Outcome", "Reason", "Outputs", "Date"],
                 [[f"{r['id']} {r['step'][:60]}", have[r["id"]]["outcome"].title() if r["id"] in have else "**NO OUTCOME**",
                   ((have.get(r["id"]) or {}).get("reason", ""), 160),
                   (", ".join((have.get(r["id"]) or {}).get("outputs", [])), 120), (have.get(r["id"]) or {}).get("at", "")[:10]]
                  for r in steps.registry()])
    cc = a / "00-crosschecks.md"
    if cc.is_file():
        srcs.append(str(cc.relative_to(ROOT)))
        body = re.sub(r"\A#[^\n]*\n+", "", cc.read_text(encoding="utf-8").strip())
        out += ["", "## 3 · Cross-checks", "", body.replace("\n#", "\n##")]
    return out, srcs


def r_urlmap(slug, st):
    a = need_audit(slug)
    f = a / "url-decision-map.csv"
    if not f.is_file():
        die(f"{f.relative_to(ROOT)} is missing — the audit writes the URL Decision Map first")
    rows = latest(read_csv(f), key="URL ID", rev="ext_revision")
    out = head(st, NAMES["urlmap"], ["url-decision-map.csv"])
    acts = {}
    for r in rows:
        acts[r.get("Proposed Action", "").strip() or "(none)"] = acts.get(r.get("Proposed Action", "").strip() or "(none)", 0) + 1
    out += [f"{len(rows)} row(s). Destructive actions follow CM-019 (all four conditions, else Needs Evidence); never "
            "delete, 301 only. Redirects are VA handoffs after Paul's approval; the system never implements one.", "",
            "## Summary", ""]
    out += table(["Decision", "Rows"], sorted(acts.items(), key=lambda kv: -kv[1]) + [["**Total**", f"**{len(rows)}**"]])
    cm = {}
    for r in rows:
        v = (r.get("ext_cm019_result") or "").strip()
        if v and not v.lower().startswith("n/a"):
            cm[v[:110]] = cm.get(v[:110], 0) + 1
    if cm:
        out += ["", "### CM-019 results (rows where a destructive action is in question)", ""]
        out += table(["Result", "Rows"], sorted(cm.items(), key=lambda kv: -kv[1]))
    out += ["", "## Rows", ""]
    out += table(["ID", "Current URL", "Type", "Action", "Target", "Risk", "Status", "Findings"],
                 [[r["URL ID"], (r.get("Current URL", ""), 110), r.get("Page Type", ""), (r.get("Proposed Action", ""), 60),
                   (r.get("Target URL", ""), 110), r.get("Risk Tier", ""), (r.get("Status", ""), 40),
                   (r.get("ext_finding_ids", ""), 60)] for r in sorted(rows, key=lambda r: r["URL ID"])])
    return out, [str(f.relative_to(ROOT))]


def r_findings(slug, st):
    a = need_audit(slug)
    f = a / "findings.csv"
    if not f.is_file():
        die(f"{f.relative_to(ROOT)} is missing — the audit writes the Finding Register first")
    rows = sorted(latest(read_csv(f)), key=lambda r: (sev(r), r["Finding ID"]))
    out = head(st, NAMES["findings"], ["findings.csv"], "Latest revision of each finding (CM-028 severity).")
    pr = {}
    for r in rows:
        pr[r.get("Priority", "?")] = pr.get(r.get("Priority", "?"), 0) + 1
    out += [f"{len(rows)} finding(s): " + " · ".join(f"{n} {k}" for k, n in sorted(pr.items(), key=lambda kv: sev({'Priority': kv[0]}))), ""]
    for p in ("High", "Medium", "Low"):
        grp = [r for r in rows if r.get("Priority") == p]
        if grp:
            out += [f"## {p}", ""] + table(["ID", "Where", "Observation", "Evidence", "Recommendation", "Owner", "Status"],
                                           [[r["Finding ID"], (r.get("Affected URL / Entity", ""), 80), (r.get("Observation", ""), 260),
                                             (r.get("Evidence / Locator", ""), 120), (r.get("Recommendation", ""), 200),
                                             r.get("Owner", ""), (r.get("Status", ""), 40)] for r in grp]) + [""]
    return out, [str(f.relative_to(ROOT))]


def _paul_rows(urlrows):
    return [r for r in urlrows if re.search(r"redirect|needs evidence|merge|consolidat", r.get("Proposed Action", ""), re.I)
            and not (r.get("Paul Decision") or "").strip()]


def r_auditsheet(slug, st):
    a = need_audit(slug)
    fr, ur = a / "findings.csv", a / "url-decision-map.csv"
    if not (fr.is_file() and ur.is_file()):
        die("the audit review sheet needs findings.csv and url-decision-map.csv — the audit writes both first")
    finds = sorted(latest(read_csv(fr)), key=lambda r: (sev(r), r["Finding ID"]))
    urls = latest(read_csv(ur), key="URL ID")
    out = head(st, NAMES["auditsheet"], ["findings.csv", "url-decision-map.csv", "audit step outcomes"])
    asks = _paul_rows(urls)
    out += ["One sheet, one approval line. **Ask** rows are Paul's decision (a URL action that is destructive or still needs "
            "evidence); everything else is listed, and stands unless Paul changes it.", "",
            f"## Ask — Paul decides ({len(asks)})", ""]
    out += table(["URL ID", "URL", "Proposed action", "Target", "CM-019", "Default"],
                 [[r["URL ID"], (r.get("Current URL", ""), 100), (r.get("Proposed Action", ""), 60), (r.get("Target URL", ""), 100),
                   (r.get("ext_cm019_result", ""), 120), "Keep live (never delete)"] for r in asks]) if asks else ["_None._"]
    needs = [r for r in finds if (r.get("Paul Approval Needed", "").strip().lower() not in ("", "no", "n/a"))
             or (r.get("Client Confirmation Needed", "").strip().lower() not in ("", "no", "n/a"))]
    out += ["", f"## Ask — findings that need Paul or the client ({len(needs)})", ""]
    out += table(["ID", "Priority", "Observation", "Needs", "Owner"],
                 [[r["Finding ID"], r.get("Priority", ""), (r.get("Observation", ""), 220),
                   (r.get("Paul Approval Needed", "") + " / " + r.get("Client Confirmation Needed", ""), 80), r.get("Owner", "")]
                  for r in needs]) if needs else ["_None._"]
    rest = [r for r in finds if r not in needs]
    out += ["", f"## Fix and list — the system carries on ({len(rest)})", ""]
    out += table(["ID", "Priority", "Where", "Recommendation", "Owner"],
                 [[r["Finding ID"], r.get("Priority", ""), (r.get("Affected URL / Entity", ""), 80),
                   (r.get("Recommendation", ""), 200), r.get("Owner", "")] for r in rest]) if rest else ["_None._"]
    have = st.get("audit_steps") or {}
    import steps
    gaps = [r["id"] for r in steps.registry() if r["id"] not in have and r["id"] not in steps.OPTIONAL]
    out += ["", "## Evidence", "", "Every registered step has an outcome." if not gaps else
            "**Steps with no outcome yet: " + ", ".join(gaps) + "** — the audit cannot be approved until each is Done, Skipped or Failed."]
    return out, [str(fr.relative_to(ROOT)), str(ur.relative_to(ROOT))]


def r_blockers(slug, st):
    a = need_audit(slug)
    f = a / "findings.csv"
    if not f.is_file():
        die("the checklist is built from the audit's findings.csv — the audit writes it first")
    finds = sorted(latest(read_csv(f)), key=lambda r: (sev(r), r["Finding ID"]))
    out = head(st, NAMES["blockers"], ["findings.csv", "status.json (blocker handoffs)"],
               "Severity scale: CM-028.")
    out += ["\"Blockers cleared\" is a condition: it is met when the VA returns every blocker handoff `done` and `/verify` "
            "passes every row. Nobody approves it.", ""]
    high = [r for r in finds if r.get("Priority") == "High"]
    va = [r for r in finds if re.search(r"jonie|gwen|\bva\b", r.get("Owner", ""), re.I) and r.get("Priority") != "High"]
    other = [r for r in finds if r not in high and r not in va]
    out += [f"## 1 · High findings ({len(high)})", "", "Fixed by a page rebuild, the structural step or the Blog Decision "
            "Map unless the owner column names the VA.", ""]
    out += table(["ID", "What breaks", "Pages", "Fixed by"], [[r["Finding ID"], (r.get("Observation", ""), 200),
                 (r.get("Affected URL / Entity", ""), 100), (r.get("Owner", "") + " — " + r.get("Recommendation", ""), 200)]
                 for r in high]) if high else ["_None._"]
    out += ["", f"## 2 · Handed to the VA ({len(va)})", ""]
    out += table(["ID", "Issue", "Affected", "Owner", "Status"], [[r["Finding ID"], (r.get("Observation", ""), 200),
                 (r.get("Affected URL / Entity", ""), 120), r.get("Owner", ""), (r.get("Status", ""), 40)] for r in va]) if va else ["_None._"]
    out += ["", f"## 3 · Everything else ({len(other)})", ""]
    out += table(["ID", "Priority", "Where it goes", "Owner"], [[r["Finding ID"], r.get("Priority", ""),
                 (r.get("Recommendation", ""), 200), r.get("Owner", "")] for r in other]) if other else ["_None._"]
    hs = st.get("blocker_handoffs") or []
    ids = list(hs) if isinstance(hs, (list, tuple)) else list(hs)
    out += ["", "## 4 · Blocker handoffs", ""]
    out += [f"- `{h}`" for h in ids] if ids else ["_No blocker handoff issued yet._" if not st.get("blockers_none")
                                                   else "_Paul recorded: no blockers._"]
    return out, [str(f.relative_to(ROOT))]


def r_siteplan(slug, st):
    d = client_dir(slug) / "build"
    plans = sorted(d.glob("site-plan*.plan.json"), key=lambda p: p.stat().st_mtime) if d.exists() else []
    if not plans:
        die(f"no site plan JSON in clients/{slug}/build/ (site-plan*.plan.json)")
    p = plans[-1]
    plan = read_json(p, {}) or {}
    batch_of = {pid: b for b in plan.get("batches", []) for pid in b.get("pages", [])}
    out = head(st, NAMES["siteplan"], [p.name], "The plan file is the source; this is a view of it.")
    out += ["## Sections", ""]
    out += table(["Section", "Kind", "Pages", "Route"], [[b["id"], b.get("kind", ""), len(b.get("pages", [])), b.get("route", "")]
                                                     for b in plan.get("batches", [])])
    out += ["", "## Pages", ""]
    out += table(["Page", "Type", "Section", "Final URL", "Replaces", "Keyword", "H1", "Variant"],
                 [[pg.get("name") or pg["id"], pg.get("type", ""), (batch_of.get(pg["id"]) or {}).get("id", ""),
                   (pg.get("url", ""), 100), ("; ".join(pg.get("replaces") or []), 100), pg.get("keyword", ""),
                   pg.get("h1", ""), pg.get("service_variant") or pg.get("category_variant") or pg.get("area_variant") or ""]
                  for pg in plan.get("pages", [])])
    return out, [str(p.relative_to(ROOT))]


RENDERERS = {"manifest": r_manifest, "urlmap": r_urlmap, "findings": r_findings, "auditsheet": r_auditsheet,
             "blockers": r_blockers, "siteplan": r_siteplan}


def approved_paths(st):
    """Files an approval covers (gates, section approvals, the site plan): rendering over one voids that approval."""
    out = set()

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("files"), dict) and str(o.get("state", "")).startswith("approved"):
                out.update(o["files"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(st.get("gates") or {})
    walk(st.get("build") or {})
    return out


def render_one(slug, kind, run_id=None, out_dir=None, force=False):
    st = S.load(slug)
    lines, sources = RENDERERS[kind](slug, st)
    p = out_path(slug, kind, st)
    if out_dir:
        p = Path(out_dir) / p.name
        p.parent.mkdir(parents=True, exist_ok=True)
    elif str(p.relative_to(ROOT)) in approved_paths(st) and not force:
        die(f"{p.relative_to(ROOT)} is covered by an approval — rendering over it would void that approval. Render with "
            "--out <folder> to look at the new version, or --force when Paul has asked for the revision.", 4)
    p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    if run_id and not out_dir:
        import run as R
        R.log_change(slug, run_id, "rendered", str(p.relative_to(ROOT)), NAMES[kind], "", f"{len(lines)} lines",
                     "RENDERED by render.py from " + ", ".join(sources), channel="local")
    return p, sources


def render_all(slug, run_id=None, out_dir=None, force=False):
    done, skipped = [], []
    for kind in RENDERERS:
        try:
            done.append(render_one(slug, kind, run_id, out_dir, force)[0])
        except SystemExit as e:
            if e.code == 4:   # covered by an approval: say so, never skip silently
                raise
            skipped.append(kind)
    return done, skipped


def stale(slug):
    """[(rendered file, newer source)] — a rendered file older than a file it was rendered from."""
    out = []
    st = S.load(slug)
    for kind in RENDERERS:
        try:
            p = out_path(slug, kind, st)
        except SystemExit:
            continue
        if not p.is_file():
            continue
        try:
            _, srcs = RENDERERS[kind](slug, st)
        except SystemExit:
            continue
        out += [(p, s) for s in srcs if (ROOT / s).stat().st_mtime > p.stat().st_mtime + 1]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=list(RENDERERS) + ["status", "all", "check"])
    ap.add_argument("slug")
    ap.add_argument("--run")
    ap.add_argument("--out", help="write to this folder instead (nothing in the client's folder changes)")
    ap.add_argument("--force", action="store_true", help="render over an approved file — only when Paul asked for the revision")
    a = ap.parse_args()
    if a.what == "status":
        import records
        records.render(a.slug)
        print(f"clients/{a.slug}/STATUS.md and the living records rendered")
    elif a.what == "all":
        done, skipped = render_all(a.slug, a.run, a.out, a.force)
        print(f"rendered {len(done)}: " + ", ".join(p.name for p in done) + (f" · no source yet: {', '.join(skipped)}" if skipped else ""))
    elif a.what == "check":
        old = stale(a.slug)
        for p, s in old:
            print(f"STALE {p.relative_to(ROOT)} — {s} is newer; render.py all {a.slug}")
        if old:
            sys.exit(4)
        print("every rendered file is current")
    else:
        p, srcs = render_one(a.slug, a.what, a.run, a.out, a.force)
        print(f"{p} rendered from {', '.join(srcs)}")


if __name__ == "__main__":
    main()
