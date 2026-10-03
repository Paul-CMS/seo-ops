#!/usr/bin/env python3
"""approve.py — the only way a gate or a page approval changes. Run only via /approve.

    approve.py <slug> <gate> --decision D [--files f1,f2] [--conditions "a; b"] [--note T]
    approve.py <slug> site_plan --decision D [--files plan.md]
    approve.py <slug> batch:<id>:briefs|drafts --decision D [--files ...] [--review T] [--practitioner T]
    approve.py <slug> batch:<id>:sem --decision D --ids SEM-1,SEM-4 [--files <semantic review table>]
    approve.py <slug> page:<page_id> --decision D [--file F] [--review T] [--practitioner T]
    approve.py <slug> import --proposal clients/<slug>/import-proposal.json

Refuses unless Paul typed /approve in this session within the last 20 minutes: the
UserPromptSubmit hook writes a one-time token when — and only when — a real user prompt
starts with "/approve". Claude cannot create that token (the guard hook blocks it).

Every approval names the exact files it covers (--files, or by default the files the producing
command recorded with `status.py mark`). No files → refused. If one of those files changes
later, only this approval stops counting (status.py).
"""
import argparse
import time

import status as S
from lib import ROOT, append, client_dir, die, git_commit, now, read_json, sha12, write_json

TOKEN = ROOT / ".claude" / "state" / "approve-token.json"
MAX_AGE = 20 * 60


def take_token(slug, target):
    tok = read_json(TOKEN)
    if not tok:
        die("REFUSED — no /approve from Paul in this session. Only Paul can approve, by typing "
            "/approve himself.", 7)
    if tok.get("used"):
        die("REFUSED — that /approve has already been used. Paul must type /approve again.", 7)
    if time.time() - tok.get("created", 0) > MAX_AGE:
        die("REFUSED — Paul's /approve is older than 20 minutes. Ask him to type it again.", 7)
    words = tok.get("prompt", "").lower().split()
    if slug not in words or target.lower() not in words:
        die(f"REFUSED — Paul's /approve did not name '{slug}' and '{target}'. "
            f"He typed: {tok.get('prompt', '')[:120]!r}", 7)
    tok["used"] = True
    tok["used_for"] = f"{slug} {target}"
    write_json(TOKEN, tok)
    return tok


def file_map(paths):
    out = {}
    for f in paths:
        if not (ROOT / f).exists():
            die(f"File {f} not found — an approval names the exact version it approves.")
        out[f] = sha12(ROOT / f)
    return out


def split(v):
    return [x.strip() for x in (v or "").split(",") if x.strip()]


def do_import(a, d, st):
    prop = read_json(ROOT / a.proposal) if a.proposal else None
    if not prop:
        die("No import proposal file.")
    take_token(a.slug, "import")
    src = prop.get("source", "Drive Approval Record")
    for g, rec in prop.get("gates", {}).items():
        if g not in st["gates"]:
            die(f"Unknown gate in proposal: {g}")
        st["gates"][g] = {**rec, "by": "Paul (import confirmed)", "at": now(),
                          "source": rec.get("source", src), "files": {}, "imported": True}
    live_states = {"live", "approved", "written_back", "verified", "implemented"}
    baseline, remaining = [], []
    for pid, p in prop.get("pages", {}).items():
        page = st["pages"].setdefault(pid, {})
        page.update({k: v for k, v in p.items() if k != "state"})
        if p.get("state") in live_states:
            page["state"] = "verified" if p.get("state") == "verified" else "written_back"
            page["approval"] = {"state": "approved", "by": "Paul (import baseline)", "at": now(),
                                "baseline": True, "source": p.get("source", src)}
            baseline.append(pid)
        else:
            page["state"] = p.get("state") if p.get("state") in S.PAGE_STATES else "planned"
            remaining.append(pid)

    # Site plan generated from the existing pages: one baseline batch (already live) plus the
    # remaining pages grouped like a normal plan (services by cluster, locations by group).
    bl = {"state": "approved", "by": "Paul (import baseline)", "at": now(), "baseline": True, "files": {}}
    batches = []
    if baseline:
        batches.append({"id": "baseline", "kind": "service", "label": "Imported — already live",
                        "pages": baseline, "state": "written_back", "briefs": bl, "sem": bl,
                        "drafts": bl, "files": {}})
    groups = {}
    for pid in remaining:
        p = st["pages"][pid]
        kind = {"county": "location"}.get(p.get("type"), p.get("type") or "service")
        key = (kind, p.get("group") or ("final" if kind in ("homepage", "about") else kind))
        groups.setdefault(key, []).append(pid)
    for (kind, grp), pids in sorted(groups.items(), key=lambda kv: S.KIND_ORDER.get(kv[0][0], 1)):
        for i in range(0, len(pids), 5):
            prefix = {"service": "svc", "location": "loc", "homepage": "final", "about": "final"}.get(kind, kind[:3])
            n = len([b for b in batches if b["id"].startswith(prefix)]) + 1
            batches.append({"id": f"{prefix}{n}", "kind": kind if kind in S.KIND_ORDER else "service",
                            "label": f"{grp} (remaining)", "pages": pids[i:i + 5], "state": "planned",
                            "briefs": None, "sem": None, "drafts": None, "files": {}})
    plan_md = d / "build" / f"{st['client']['name']} - Site Plan - IMPORTED.md"
    plan_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {st['client']['name']} - Site Plan - IMPORTED", "",
             f"Generated from the import proposal ({a.proposal}) on {now()[:10]}. Pages already live are "
             "an approved baseline; the rest are planned in batches.", "",
             "| Page | Type | State | Batch |", "|---|---|---|---|"]
    for b in batches:
        for pid in b["pages"]:
            pg = st["pages"][pid]
            lines.append(f"| {pg.get('name') or pid} | {pg.get('type', '')} | {pg['state']} | {b['id']} |")
    plan_md.write_text("\n".join(lines) + "\n")
    rel = str(plan_md.relative_to(ROOT))
    pilot_done = prop.get("pilot_done", bool(baseline))
    st["build"] = {"site_plan": {"file": rel, "approval": {"state": "approved", "by": "Paul (import confirmed)",
                                                            "at": now(), "files": file_map([rel])}},
                   "batches": batches,
                   "pilot_waived": pilot_done,
                   "pilot_corrections_applied": ({"at": now(), "note": "imported — pilot done before seo-ops"}
                                                 if pilot_done else None)}
    # Audit steps done before seo-ops are recorded, so /next never sends the client back to /crawl.
    import steps
    if st["gates"].get("b1_audit", {}).get("state") in S.GATES["met_decisions"]:
        for r in steps.registry():
            st["audit_steps"].setdefault(r["id"], {"outcome": "done", "reason": f"imported — done before seo-ops ({src})",
                                                   "outputs": [], "at": now(), "run": "import"})
    for sid, rec in (prop.get("steps") or {}).items():
        st["audit_steps"][sid] = {"outputs": [], "at": now(), "run": "import", **rec}
    st["client"]["imported"] = True
    S.save(a.slug, st)
    append(d / "log.md", f"\n## APPROVAL · {now()} · import confirmed by Paul\n"
           f"Gates set from {a.proposal}: {', '.join(prop.get('gates', {}))}\n"
           f"Baseline pages (already live): {len(baseline)} · remaining pages planned: {len(remaining)}\n"
           f"Site plan generated: {rel}\n")
    print(git_commit(f"{a.slug}: import confirmed by Paul"))
    print(f"imported: {len(baseline)} live pages as baseline, {len(remaining)} pages planned in "
          f"{len(batches) - (1 if baseline else 0)} batch(es); site plan {rel}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("target")
    ap.add_argument("--decision", choices=S.GATES["decisions"], default="approved")
    ap.add_argument("--conditions"); ap.add_argument("--files"); ap.add_argument("--file")
    ap.add_argument("--note"); ap.add_argument("--review"); ap.add_argument("--practitioner")
    ap.add_argument("--proposal"); ap.add_argument("--ids")
    a = ap.parse_args()
    d = client_dir(a.slug)
    st = S.load(a.slug)
    approved = a.decision in S.GATES["met_decisions"]

    if a.target == "import":
        return do_import(a, d, st)

    if a.target == "site_plan" or a.target.startswith("batch:"):
        bp = st.get("build") or die("No site plan registered yet (status.py plan ...).")
        files = file_map(split(a.files or a.file))
        if a.target == "site_plan":
            if not files:
                files = file_map([bp["site_plan"]["file"]])
            holder, key, label_ = bp["site_plan"], "approval", "site plan"
        else:
            _, bid, stage = (a.target.split(":") + ["", ""])[:3]
            if stage not in S.STAGES:
                die("Use batch:<id>:briefs, batch:<id>:sem or batch:<id>:drafts")
            b = S.batch(st, bid) or die(f"No batch {bid}.")
            if not files:
                files = file_map((b.get("files") or {}).get(stage) or [])
            if approved:
                ok, why = S.batch_ready(st, bid, stage)
                if not ok:
                    die("REFUSED — " + "; ".join(why))
                if not files:
                    die(f"REFUSED — name the exact files approved (--files): for {stage}, "
                        + ("the semantic review table." if stage == "sem" else "one per page in the batch."))
                if stage == "sem" and not a.ids:
                    die("REFUSED — say which SEM IDs to apply (--ids SEM-1,SEM-4), or --ids none.")
                if stage == "drafts":
                    if b.get("state") not in ("sem_applied", "implemented", "verified", "written_back"):
                        die("REFUSED — the approved SEM changes have not been applied and re-checked yet "
                            "(the batch must be at sem_applied).")
                    if st["client"]["sensitive"] and not a.review:
                        die("REFUSED — sensitive client: record the human review with --review.")
                    if st["client"]["practitioner_signoff"] and not a.practitioner:
                        die("REFUSED — health content: record the licensed practitioner's sign-off with --practitioner.")
            holder, key, label_ = b, stage, f"batch {bid} {stage}"
        take_token(a.slug, a.target)
        holder[key] = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note, "files": files,
                       "conditions": [c.strip() for c in (a.conditions or "").split(";") if c.strip()],
                       "sensitive_review": a.review, "practitioner": a.practitioner,
                       **({"sem_ids": split(a.ids)} if a.ids else {})}
        S.save(a.slug, st)
        append(d / "log.md", f"\n## APPROVAL · {now()} · {label_} · {a.decision} · by Paul\n"
               + "".join(f"Approved version: {f} (sha {h})\n" for f, h in files.items())
               + (f"SEM IDs to apply: {a.ids}\n" if a.ids else "")
               + (f"Human review: {a.review}\n" if a.review else "")
               + (f"Practitioner sign-off: {a.practitioner}\n" if a.practitioner else "")
               + (f"Note: {a.note}\n" if a.note else ""))
        print(git_commit(f"{a.slug}: {label_} {a.decision} by Paul"))
        return

    if a.target.startswith("page:"):
        pid = a.target[5:]
        p = st["pages"].get(pid) or die(f"Page {pid} is not registered (status.py page ...).")
        if approved and st["client"]["sensitive"] and not a.review:
            die("REFUSED — sensitive client: record the human review with --review "
                "(who reviewed the content before it goes live).")
        if approved and st["client"]["practitioner_signoff"] and not a.practitioner:
            die("REFUSED — health content: the client's licensed practitioner must sign off on "
                "health claims. Record who with --practitioner \"Name, licence\".")
        f = a.file or p.get("file")
        if approved and not f:
            die("REFUSED — name the draft file being approved (--file).")
        if approved and not (ROOT / f).exists():
            die(f"File {f} not found.")
        take_token(a.slug, a.target)
        p["approval"] = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note,
                         "file": f, "sha": sha12(ROOT / f) if f and (ROOT / f).exists() else None,
                         "sensitive_review": a.review, "practitioner": a.practitioner}
        if approved:
            p["state"] = "approved"
        S.save(a.slug, st)
        append(d / "log.md", f"\n## APPROVAL · {now()} · page {pid} · {a.decision} · by Paul\n"
               + (f"File: {f} (sha {p['approval']['sha']})\n" if f else "")
               + (f"Human review: {a.review}\n" if a.review else "")
               + (f"Practitioner sign-off: {a.practitioner}\n" if a.practitioner else "")
               + (f"Note: {a.note}\n" if a.note else ""))
        print(git_commit(f"{a.slug}: page {pid} {a.decision} by Paul"))
        return

    g = a.target
    if g not in S.GATES["gates"]:
        die(f"Unknown gate '{g}'. Gates: {', '.join(S.GATES['gates'])}")
    spec = S.GATES["gates"][g]
    files = file_map(split(a.files) or S.mark_files(st, spec.get("artifact", "")))
    if approved:
        if not files:
            die(f"REFUSED — this approval must name the files it covers. Nothing is recorded for "
                f"{S.plain(g)} yet (the producing command marks them), so pass --files.")
        if g == "b1_audit":
            import steps
            left = steps.missing(st)
            if left:
                die("REFUSED — audit steps with no outcome (Done / Skipped / Failed): "
                    + ", ".join(r["id"] for r in left) + ". See methodology/audit-steps.md.")
        missing = [r for r in S.requires(st, g) if not S._decided(st, r)]
        if missing:
            die("REFUSED — these come first and are not approved yet: "
                + "; ".join(S.plain(r) for r in missing))
    take_token(a.slug, g)
    st["gates"][g] = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note,
                      "conditions": [c.strip() for c in (a.conditions or "").split(";") if c.strip()],
                      "files": files}
    S.save(a.slug, st)
    append(d / "log.md", f"\n## APPROVAL · {now()} · {g} · {a.decision} · by Paul\n"
           + "".join(f"Approved version: {f} (sha {h})\n" for f, h in files.items())
           + "".join(f"Condition: {c}\n" for c in st["gates"][g]["conditions"])
           + (f"Note: {a.note}\n" if a.note else ""))
    print(git_commit(f"{a.slug}: {g} {a.decision} by Paul"))


if __name__ == "__main__":
    main()
