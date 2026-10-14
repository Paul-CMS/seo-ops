#!/usr/bin/env python3
"""approve.py — the only way a gate or a page approval changes. Run only via /approve.

    approve.py <slug> <gate> --decision D [--files f1,f2] [--conditions "a; b"] [--note T]
    approve.py <slug> site_plan --decision D [--files plan.md]
    approve.py <slug> batch:<id>:briefs --decision D [--files ...]
    approve.py <slug> batch:<id>:drafts --decision D [--sem 1,3,4|none] [--review T] [--practitioner T]
               the drafts approval covers every draft AND the batch's semantic review table; --sem picks
               the SEM items to apply (needed only when the review found something)
    approve.py <slug> page:<page_id> --decision D [--file F] [--review T] [--practitioner T]
    approve.py <slug> import --proposal clients/<slug>/import-proposal.json
    approve.py <slug> evidence:<page_id> --reason T     waive a BLOCK from the evidence gate (CM-041), for this grid
    approve.py <slug>|global mode:<stage>=auto|review    switch a producing stage's mode (CM-044); auto only
               after the stage passed the pilot; decisions can never be auto
    approve.py global specs                              approve the page specs (methodology/specs) once, for every
               client (R3); each spec's status line becomes APPROVED; a later change to a spec re-opens it
    approve.py <slug> entity_approved proof_sheet_approved   Approval 1 in one line (R3); every answer in the approved
               Decision Sheet is then settled (decisions-settled.md) and never asked again
    approve.py <slug> schema-offline --reason T          Wikipedia/Wikidata unreachable: let THIS open /finish schema
               run build once without the live entity check (CM-053); every other check still runs

Global approvals (global specs / mode: / model:) run only in the main folder, check everything before writing,
write only system files (spec stamp, config.json) all-or-nothing, and never touch client records: each client
applies them on its own next /next (status.apply_global).

Refuses unless Paul typed /approve in this session within the last 20 minutes: the
UserPromptSubmit hook writes a one-time token when — and only when — a real user prompt
starts with "/approve". Claude cannot create that token (the guard hook blocks it).

Every approval names the exact files it covers (--files, or by default the files the producing
command recorded with `status.py mark`). No files → refused. If one of those files changes
later, only this approval stops counting (status.py).
"""
import argparse
import os
import re
import time
from pathlib import Path

import status as S
from lib import (ROOT, append, machine, client_dir, die, git_commit, json_text, now, read_json, ref_missing, ref_sha,
                 require_main_folder, sha12, write_json)

TOKEN = ROOT / ".claude" / "state" / "approve-token.json"
MAX_AGE = 20 * 60


def take_token(slug, targets, consume=True, into=None):
    """Check Paul's /approve token names this client and every target; mark it used if consume. With `into` (a
    {path: text} dict of staged writes) the used token is staged there instead of written — a global approval writes
    the token in the same all-or-nothing step as everything else."""
    if isinstance(targets, str):
        targets = [targets]
    if machine().get("can_approve") is False:
        die("REFUSED — this Mac runs the stages but does not approve (machine.json can_approve: false). "
            "Send Paul the /approve line; he approves on his own Mac after a git pull.", 7)
    tok = read_json(TOKEN)
    if not tok:
        die("REFUSED — no /approve from Paul in this session. Only Paul can approve, by typing "
            "/approve himself.", 7)
    if tok.get("used"):
        die("REFUSED — that /approve has already been used. Paul must type /approve again.", 7)
    if time.time() - tok.get("created", 0) > MAX_AGE:
        die("REFUSED — Paul's /approve is older than 20 minutes. Ask him to type it again.", 7)
    words = tok.get("prompt", "").lower().split()
    missing = [t for t in targets if t.lower() not in words]
    if slug not in words or missing:
        die(f"REFUSED — Paul's /approve did not name '{slug}' and {', '.join(repr(t) for t in missing) or 'the client'}. "
            f"He typed: {tok.get('prompt', '')[:120]!r}", 7)
    if consume:
        tok["used"] = True
        tok["used_for"] = f"{slug} {' '.join(targets)}"
        if into is None:
            write_json(TOKEN, tok)
        else:
            into[TOKEN] = json_text(tok)
    return tok


def commit_writes(changes):
    """All or nothing: write every {path: text}; on any error put every file back as it was and refuse. The staged
    /approve token is one of the files, so a failed approval does not use it up."""
    old = {p: (p.read_text(encoding="utf-8") if p.exists() else None) for p in changes}
    done = []
    try:
        for p, text in changes.items():
            tmp = p.with_suffix(p.suffix + ".tmp")
            tmp.write_text(text, encoding="utf-8")
            os.replace(tmp, p)
            done.append(p)
    except Exception as e:  # noqa: BLE001
        for p in changes:
            p.with_suffix(p.suffix + ".tmp").unlink(missing_ok=True)
        for p in done:
            if old[p] is None:
                p.unlink(missing_ok=True)
            else:
                p.write_text(old[p], encoding="utf-8")
        die(f"REFUSED — could not write {p.name}: {e}. Nothing was changed and the /approve is not used up.")


def stage_global(cfg, changes, kind, **fields):
    """Record a global approval in config.json (global_approvals); each client applies it on its own next /next."""
    log = cfg.setdefault("global_approvals", [])
    log.append({"n": max([e.get("n", 0) for e in log] or [0]) + 1, "kind": kind, "by": "Paul", "at": now(), **fields})
    changes[ROOT / "config.json"] = json_text(cfg)


def file_map(paths):
    out = {}
    for f in paths:
        gone = ref_missing(f)
        if gone:
            die(f"{gone} — an approval names the exact version it approves.")
        out[f] = ref_sha(f)
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
        if g in S.GATES.get("retired_gates", {}):   # R3: now a condition — a signed Drive block proves it
            st.setdefault("imported_conditions", {})[g] = f"imported — {rec.get('source', src)}"
            continue
        if g not in st["gates"]:
            die(f"Unknown gate in proposal: {g}")
        st["gates"][g] = {**rec, "by": "Paul (import confirmed)", "at": now(),
                          "source": rec.get("source", src), "files": {}, "imported": True}
    # A returned proof sheet is a condition; a signed Brand Guide / discovery block proves it.
    if any(g in prop.get("gates", {}) for g in ("brand_guide_approved", "discovery_signed_off")):
        st.setdefault("imported_conditions", {})["proof_sheet_returned"] = f"imported — {src}"
    for c in prop.get("conditions") or []:
        st.setdefault("imported_conditions", {})[c] = f"imported — {src}"
    import urlcheck   # P7: the import baseline is not exempt from the URL rule
    bad = urlcheck.problems([{"id": pid, **p} for pid, p in (prop.get("pages") or {}).items()])
    if bad:
        die("REFUSED — the import breaks the URL rule (the live baseline is not exempt). In the proposal, give each "
            "page its root URL as 'url' and its old URL under 'replaces' (its 301 is paired with the publish):\n  - "
            + "\n  - ".join(bad), 4)
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
                        "pages": baseline, "state": "written_back", "briefs": bl,
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
                            "briefs": None, "drafts": None, "files": {}})
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
    if st["gates"].get("audit_approved", {}).get("state") in S.GATES["met_decisions"]:
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
    S.log_conditions(a.slug, st)
    import records
    records.render(a.slug)
    print(git_commit(f"{a.slug}: import confirmed by Paul", slug=a.slug))
    print(f"imported: {len(baseline)} live pages as baseline, {len(remaining)} pages planned in "
          f"{len(batches) - (1 if baseline else 0)} batch(es); site plan {rel}")


def sem_list(v):
    """'1,3,4' / 'SEM-1, sem-3' → ['SEM-1','SEM-3']; 'none' → []; None → None (not given)."""
    if v is None:
        return None
    if v.strip().lower() in ("none", "no", "0", ""):
        return []
    out = []
    for x in split(v.replace(" ", ",")):
        n = x.upper().replace("SEM-", "").replace("SEM", "")
        if not n.isdigit() or int(n) < 1:
            die(f"'{x}' is not a SEM item (write numbers, e.g. --sem 1,3,4).")
        out.append(f"SEM-{int(n)}")
    return out


SEM_ROW = re.compile(r"^\s*\|\s*\**\s*(SEM-\d+)\s*\**\s*\|", re.I)


def table_sem_ids(rel):
    """The SEM items in a batch's semantic review table: the rows whose first cell is SEM-n (F-017 — whatever the count)."""
    path = ROOT / rel if rel else None
    if not path or not path.is_file():
        return None
    return [m.group(1).upper() for m in map(SEM_ROW.match, path.read_text(encoding="utf-8").splitlines()) if m]


def check_sem(target, b, sem):
    """--sem must name only SEM items that are rows in this batch's review table (the last drafts file)."""
    if not sem:
        return
    table = (b.get("files") or {}).get("review_sheet") or ((b.get("files") or {}).get("drafts") or [None])[-1]
    have = table_sem_ids(table)
    if not have:
        die(f"REFUSED ({target}) — the batch's semantic review table ({table or 'not recorded'}) has no SEM rows to pick from.")
    bad = [s for s in sem if s not in have]
    if bad:
        die(f"REFUSED ({target}) — {', '.join(bad)} not in the batch's semantic review table "
            f"(it has {', '.join(have)}).")


def drafts_applied(target, b, sem):
    """CR-025: a drafts approval is accepted once the drafts and their semantic review are written — drafts_written or
    any later batch state (sem_applied included). Returns the SEM items already applied (the earlier approval's
    'applied' record), or None. Applied items are recorded as applied, never re-applied: --sem may only repeat them."""
    if b.get("state") not in S.BATCH_STATES[S.BATCH_STATES.index("drafts_written"):]:
        die(f"REFUSED ({target}) — the drafts and their semantic review are not written yet.")
    applied = (b.get("drafts") or {}).get("applied")
    if not applied:
        return None
    done = applied.get("sem_ids") or []
    if sem is not None and sorted(sem) != sorted(done):
        die(f"REFUSED ({target}) — {', '.join(done) or 'no SEM items'} already applied to these drafts; leave out "
            "--sem (or repeat exactly those) — a different pick needs the drafts revised first.")
    return applied


def parse_mode(target):
    """'mode:build:draft=auto' → ('build:draft', 'auto'). Only producing stages have a mode;
    a decision (an /approve gate) can never be auto (CM-044)."""
    body = target[5:]
    step, _, mode = body.rpartition("=")
    if mode not in ("auto", "review") or not step:
        die(f"REFUSED ({target}) — write mode:<stage>=auto or mode:<stage>=review.")
    if step in S.GATES["gates"] or step in S.GATES["conditions"] or step.startswith(("page:", "batch:", "evidence:")) \
            or step == "site_plan":
        die(f"REFUSED ({target}) — '{step}' is a decision. Decisions are always yours with /approve and can never be auto.")
    if step not in S.mode_stages():
        die(f"REFUSED ({target}) — '{step}' is not a producing stage. Stages: {', '.join(S.mode_stages())}")
    return step, mode


def global_mode(a):
    """/approve global mode:<stage>=auto — every client; auto needs the stage to have passed the pilot
    for at least one client. Writes config.json only; each client records it on its own next /next."""
    if len(a.targets) != 1 or not a.targets[0].startswith("mode:"):
        die("REFUSED — 'global' takes exactly one mode:<stage>=auto|review.")
    target = a.targets[0]
    step, mode = parse_mode(target)
    take_token("global", target, consume=False)
    from lib import CLIENTS, config
    slugs = sorted(p.parent.name for p in CLIENTS.glob("*/status.json"))
    if mode == "auto" and not any(S.pilot_passed(S.load(s), step)[0] for s in slugs):
        die(f"REFUSED ({target}) — no client has passed the pilot for {step} yet.")
    changes = {}
    take_token("global", target, into=changes)
    cfg = config()
    old = ((cfg.get("stage_modes") or {}).get(step) or {}).get("mode", S.GATES["modes"]["default"])
    rec = {"mode": mode, "by": "Paul", "at": now(), "note": a.note, "was": old}
    cfg.setdefault("stage_modes", {})[step] = rec
    stage_global(cfg, changes, "mode", step=step, mode=mode, was=old, note=a.note)
    commit_writes(changes)
    print(git_commit(f"global: {step} → {mode} by Paul", paths=["config.json"]))


def global_model(a):
    """/approve global model:build:draft=sonnet|opus (rewrite 2 §4: the Sonnet drafting test) — Paul's choice of model
    for one job, for every client. Recorded in config.json model_overrides; next.py and stages.py print it."""
    target = a.targets[0]
    m = re.match(r"^model:([a-z0-9:-]+)=(haiku|sonnet|opus)$", target)
    if not m:
        die("REFUSED — write model:<step>=haiku|sonnet|opus, e.g. model:build:draft=sonnet")
    key, model = m.groups()
    keys = {r.get("key") or step for step, rs in (S.GATES.get("models") or {}).items() for r in rs}
    if key not in keys:
        die(f"REFUSED ({target}) — no job '{key}' in gates.json → models ({', '.join(sorted(keys))})")
    take_token("global", target, consume=False)
    changes = {}
    take_token("global", target, into=changes)
    from lib import config
    cfg = config()
    old = ((cfg.get("model_overrides") or {}).get(key) or {}).get("model")
    cfg.setdefault("model_overrides", {})[key] = {"model": model, "by": "Paul", "at": now(), "note": a.note, "was": old}
    stage_global(cfg, changes, "model", key=key, model=model, was=old, note=a.note)
    commit_writes(changes)
    print(git_commit(f"global: model for {key} → {model} by Paul", paths=["config.json"]))


def global_specs(a, only=None):
    """/approve global specs (R3): the page specs are methodology, approved once for every client. Each spec's status
    line is rewritten to APPROVED; config.json records each spec's sha (status line excluded). A changed spec makes
    page_specs_approved unmet until Paul approves again (pilot corrections re-stamp themselves: status.py).
    Every check runs first; then the spec stamps, config.json and the token are written together or not at all.
    No client file is touched — each client records the approval on its own next /next."""
    target = f"specs:{only}" if only else "specs"
    take_token("global", target, consume=False)
    from lib import config
    stamp = f"**Status:** APPROVED — {now()[:10]}, Paul"
    files, changes = {}, {}
    wanted = [r for r in S.spec_files() if not only or Path(r).stem == only]
    if not wanted:
        die(f"REFUSED — no page spec named '{only}'. Specs: " + ", ".join(Path(r).stem for r in S.spec_files()))
    for rel in wanted:
        f = ROOT / rel
        text = f.read_text(encoding="utf-8")
        new = S.STATUS_LINE.sub(stamp, text, count=1) if S.STATUS_LINE.search(text) else text
        if new != text:
            changes[f] = new
        files[rel] = S.spec_sha(rel)   # the status line is not part of the sha
    take_token("global", target, into=changes)
    cfg = config()
    old = (cfg.get("specs_approval") or {}).get("files") or {}
    cfg["specs_approval"] = {"by": "Paul", "at": now(), "note": a.note, "files": {**old, **files} if only else files}   # CR-023
    stage_global(cfg, changes, "specs", only=only, files=files, note=a.note)
    commit_writes(changes)
    print(git_commit("global: page specs approved by Paul", paths=["config.json", "methodology/specs/"]))
    print(f"page specs approved: {', '.join(Path(r).name for r in files)}")


def settle_decision_sheet(slug, files):
    """Approval 1 settles every Decision Sheet row: its answer, or the recommended default when no answer was given."""
    import settled
    n = 0
    for f in files:
        path = ROOT / f.split("#", 1)[0]
        if "Decision Sheet" not in path.name or not path.is_file():
            continue
        have = settled.entries(slug)
        for line in path.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.lstrip().startswith("|") else []
            if len(cells) < 4 or not settled.KEY.match(cells[0].strip("`")) or cells[0].lower() == "key":
                continue
            key, what, default, answer = cells[0].strip("`"), cells[1], cells[2], cells[3]
            value = answer or f"{default} (recommended default)"
            if not value.strip() or value.strip() == "(recommended default)":
                continue
            if (have.get(key) or {}).get("state") == "settled":
                continue
            settled.settle(slug, "approval-1", key, f"{what}: {value}", by="Paul (Approval 1)", closed_ok=True)
            n += 1
    return n


def prepare(a, st, target, multi):
    """Check one target. Returns (apply_fn, log_text, label). Refuses (exit) on any problem,
    before anything is written — a multi-target /approve applies all or nothing."""
    approved = a.decision in S.GATES["met_decisions"]
    sem = sem_list(a.sem)
    explicit = split(a.files or a.file) if not multi else []
    applied = None   # CR-025: SEM items applied to the drafts before this approval

    if target == "site_plan" or target.startswith("batch:"):
        bp = st.get("build") or die("No site plan registered yet (status.py plan ...).")
        files = file_map(explicit)
        if target == "site_plan":
            if not files:
                files = file_map([bp["site_plan"]["file"]])
            holder, key, label_ = bp["site_plan"], "approval", "site plan"
        else:
            _, bid, stage = (target.split(":") + ["", ""])[:3]
            if stage not in S.STAGES:
                die("Use batch:<id>:briefs or batch:<id>:drafts (SEM items are picked with the drafts: --sem 1,3,4)")
            b = S.batch(st, bid) or die(f"No batch {bid}.")
            if not files:
                bf = b.get("files") or {}
                files = file_map((bf.get(stage) or []) + ([bf["review_sheet"]] if stage == "drafts" and bf.get("review_sheet") else []))
            if stage == "drafts":
                check_sem(target, b, sem)
            rv = (b.get("review") or {}).get(stage)
            if approved and rv and not rv.get("applied"):   # CM-061: the approval follows the applied review sheet
                die(f"REFUSED ({target}) — the {bid} {stage} review sheet ({rv.get('sheet')}) is not applied yet: answer it "
                    f"(\"accept all\" or \"accept all except 7b\") and the system applies it (review.py apply) first.")
            if approved:
                ok, why = S.batch_ready(st, bid, stage)
                if stage == "drafts" and f"batch:{bid}:briefs" in a.targets:   # P10: briefs approved in this same line
                    why = [w for w in why if not w.startswith(f"batch {bid} briefs")]
                    ok = not why
                if not ok:
                    die(f"REFUSED ({target}) — " + "; ".join(why))
                if not files:
                    die(f"REFUSED ({target}) — name the exact files approved (--files): one per page in the batch"
                        + (" plus the semantic review table." if stage == "drafts" else "."))
                bad = S.page_version_problems(st, bid, stage, files)
                if bad:   # nothing is approved on any mismatch: every page at the version the review answers produced
                    die(f"REFUSED ({target}) — the approval would cover pages that are not recorded at the version the "
                        f"review answers produced; nothing is approved ({len(bad)} problem(s)):\n  - " + "\n  - ".join(bad)
                        + f"\nRecord each page again (status.py page-stage … --run <the /build review run>) after the answers "
                        "are applied, then approve.", 4)
                if stage == "drafts":
                    applied = drafts_applied(target, b, sem)
                    if applied:
                        sem = list(applied.get("sem_ids") or [])
                    if b.get("sem_findings") and sem is None:
                        die(f"REFUSED ({target}) — the semantic review found {b['sem_findings']} item(s): say which "
                            "to apply (--sem 1,3,4) or --sem none.")
                    if st["client"]["sensitive"] and not a.review:
                        die("REFUSED — sensitive client: record the human review with --review.")
                    if st["client"]["practitioner_signoff"] and not a.practitioner:
                        die("REFUSED — health content: record the licensed practitioner's sign-off with --practitioner.")
            holder, key, label_ = b, stage, f"batch {bid} {stage}"
        rec = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note, "files": files,
               "conditions": [c.strip() for c in (a.conditions or "").split(";") if c.strip()],
               "sensitive_review": a.review, "practitioner": a.practitioner,
               **({"sem_ids": sem or [], "writing_fp": S.writing_fp()} if target.endswith(":drafts") else {}),
               **({"applied": applied} if applied else {})}

        def apply():
            holder[key] = rec
        text = (f"\n## APPROVAL · {now()} · {label_} · {a.decision} · by Paul\n"
                + "".join(f"Approved version: {f} (sha {h})\n" for f, h in files.items())
                + ((f"SEM items already applied (not re-applied): {', '.join(sem)}\n" if applied else
                    f"SEM items to apply: {', '.join(sem) if sem else 'none'}\n") if target.endswith(":drafts") else "")
                + (f"Human review: {a.review}\n" if a.review else "")
                + (f"Practitioner sign-off: {a.practitioner}\n" if a.practitioner else "")
                + (f"Note: {a.note}\n" if a.note else ""))
        return apply, text, label_

    if target.startswith("evidence:"):   # CM-041 waiver: Paul's name, date and reason, tied to this grid
        pid = target[9:]
        result, rec = S.evidence_state(st, pid)
        if result != "block":
            die(f"REFUSED ({target}) — " + ("the evidence gate has not run for this page." if not result else
                f"the page is not blocked (it is {result}); there is nothing to waive."))
        if not a.reason:
            die(f"REFUSED ({target}) — a waiver needs your reason: --reason \"...\"")
        ok, why = S.evidence_ok(st, pid)
        if "changed after it was scored" in why:
            die(f"REFUSED ({target}) — {why}")
        w = {"by": "Paul", "at": now(), "reason": a.reason, "grid": rec.get("grid"), "grid_sha": rec.get("sha"),
             "counts": rec.get("counts")}

        def apply():
            st["pages"][pid]["evidence"]["waiver"] = w
        text = (f"\n## WAIVER · {now()} · evidence gate · page {pid} · by Paul\n"
                f"Grid: {rec.get('grid')} (sha {rec.get('sha')}) · was BLOCK: {'; '.join(rec.get('why') or [])}\n"
                f"Reason: {a.reason}\n")
        return apply, text, f"evidence waiver {pid}"

    if target == "schema-offline":   # CM-053: one run, Paul's name and reason, only the live entity check skipped
        if not a.reason:
            die("REFUSED (schema-offline) — say why: --reason \"...\" (e.g. which site was down, since when)")
        runs = [rid for rid, info in (st.get("open_runs") or {}).items() if info.get("step") == "finish:schema"]
        if not runs:
            die("REFUSED (schema-offline) — it covers one open /finish schema run, and none is open. Start the run, "
                "let the build refuse on the unreachable check, then approve.")
        rid = sorted(runs)[-1]
        rec = {"by": "Paul", "at": now(), "reason": a.reason, "run": rid, "used": None}

        def apply():
            st["schema_offline"] = rec
        text = (f"\n## APPROVAL · {now()} · schema-offline · by Paul\n"
                f"Run: {rid} only — the live Wikipedia/Wikidata/Grokipedia entity check may be skipped once in this run; "
                f"every other check still runs.\nReason: {a.reason}\n")
        return apply, text, "schema-offline"

    if target.startswith("mode:"):
        step, mode = parse_mode(target)
        if mode == "auto":
            ok, why = S.pilot_passed(st, step)
            cond = (S.GATES["modes"]["stages"].get(step) or {}).get("pilot")
            if not ok and cond in a.targets and approved:   # P10: the pilot approved in this same line counts
                ok = True
            if not ok:
                die(f"REFUSED ({target}) — a stage goes to auto only after it has passed the pilot: {why}.")
        old = S.stage_mode(st, step)
        rec = {"mode": mode, "by": "Paul", "at": now(), "note": a.note, "was": old}

        def apply():
            st.setdefault("modes", {})[step] = rec
            st.setdefault("mode_history", []).append({"step": step, "scope": "client", **rec})
        text = f"\n## MODE · {now()} · {step}: {old} → {mode} · this client · by Paul\n" + (f"Note: {a.note}\n" if a.note else "")
        return apply, text, f"{step} {mode}"

    if target.startswith("page:"):
        pid = target[5:]
        p = st["pages"].get(pid) or die(f"Page {pid} is not registered (status.py page ...).")
        if approved and st["client"]["sensitive"] and not a.review:
            die("REFUSED — sensitive client: record the human review with --review "
                "(who reviewed the content before it goes live).")
        if approved and st["client"]["practitioner_signoff"] and not a.practitioner:
            die("REFUSED — health content: the client's licensed practitioner must sign off on "
                "health claims. Record who with --practitioner \"Name, licence\".")
        f = (explicit[0] if explicit else None) or p.get("file")
        if approved and not f:
            die(f"REFUSED ({target}) — name the draft file being approved (--file).")
        if approved and not (ROOT / f).exists():
            die(f"File {f} not found.")
        rec = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note,
               "file": f, "sha": sha12(ROOT / f) if f and (ROOT / f).exists() else None,
               "sensitive_review": a.review, "practitioner": a.practitioner}

        def apply():
            p["approval"] = rec
            if approved:
                p["state"] = "approved"
        text = (f"\n## APPROVAL · {now()} · page {pid} · {a.decision} · by Paul\n"
                + (f"File: {f} (sha {rec['sha']})\n" if f else "")
                + (f"Human review: {a.review}\n" if a.review else "")
                + (f"Practitioner sign-off: {a.practitioner}\n" if a.practitioner else "")
                + (f"Note: {a.note}\n" if a.note else ""))
        return apply, text, f"page {pid}"

    g = target
    if g in S.GATES["conditions"]:
        die(f"'{g}' is a condition the system checks itself ({S.label(g)}) — nobody approves it.")
    if g not in S.GATES["gates"]:
        die(f"Unknown decision '{g}'. Decisions: {', '.join(S.GATES['gates'])}")
    spec = S.GATES["gates"][g]
    files = file_map(explicit or S.mark_files(st, spec.get("artifact", "")))
    if approved:
        if not files:
            die(f"REFUSED ({g}) — this approval must name the files it covers. Nothing is recorded for "
                f"{S.plain(g)} yet (the producing command marks them), so pass --files.")
        missing = [r for r in S.requires(st, g) if not S._decided(st, r) and r not in a.targets]
        if missing:
            die(f"REFUSED ({g}) — these come first: "
                + "; ".join(S.condition_met(st, r)[1] if r in S.GATES["conditions"] else S.plain(r) + " — not approved yet"
                            for r in missing))
    rec = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note,
           "conditions": [c.strip() for c in (a.conditions or "").split(";") if c.strip()],
           "files": files}

    def apply():
        st["gates"][g] = rec
    text = (f"\n## APPROVAL · {now()} · {g} · {a.decision} · by Paul\n"
            + "".join(f"Approved version: {f} (sha {h})\n" for f, h in files.items())
            + "".join(f"Condition: {c}\n" for c in rec["conditions"])
            + (f"Note: {a.note}\n" if a.note else ""))
    return apply, text, g


def approved_files(st, target):
    """{file: sha} an approval just recorded, for the Drive copies."""
    if target in S.GATES["gates"]:
        return (st["gates"].get(target) or {}).get("files") or {}
    if target == "site_plan":
        return (((st.get("build") or {}).get("site_plan") or {}).get("approval") or {}).get("files") or {}
    if target.startswith("batch:"):
        _, bid, stage = (target.split(":") + ["", ""])[:3]
        return ((S.batch(st, bid) or {}).get(stage) or {}).get("files") or {}
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("targets", nargs="+")
    ap.add_argument("--decision", choices=S.GATES["decisions"], default="approved")
    ap.add_argument("--conditions"); ap.add_argument("--files"); ap.add_argument("--file")
    ap.add_argument("--note"); ap.add_argument("--review"); ap.add_argument("--practitioner")
    ap.add_argument("--proposal"); ap.add_argument("--sem", "--ids", dest="sem")
    ap.add_argument("--reason", help="evidence:<page> waivers: why Paul waives the gate")
    a = ap.parse_args()
    if a.slug == "global":
        require_main_folder("global approvals")   # they change system files only; each client applies them on its /next
        if a.targets == ["specs"]:
            return global_specs(a)
        if len(a.targets) == 1 and a.targets[0].startswith("specs:"):
            return global_specs(a, only=a.targets[0].split(":", 1)[1])
        if len(a.targets) == 1 and a.targets[0].startswith("model:"):
            return global_model(a)
        return global_mode(a)
    d = client_dir(a.slug)
    st = S.load(a.slug)

    if a.targets == ["import"]:
        return do_import(a, d, st)
    multi = len(a.targets) > 1
    if multi and (a.files or a.file):
        die("REFUSED — with several approvals in one line, each uses the files its step recorded; "
            "--files is only for a single approval.")
    take_token(a.slug, a.targets, consume=False)                 # Paul's /approve first
    broken = st.get("sequence_failure")   # a multi-step command failed and nobody resolved it: no approval runs after it
    if broken:
        die(f"REFUSED — a step failed earlier in a sequence and is not resolved: step {broken.get('step')} "
            f"({broken.get('cmd')}) — {broken.get('why')}. Fix it and re-run the sequence (seq.py), or finish/abort the "
            "run; an approval never runs after a failure.", 4)
    prepared = [prepare(a, st, t, multi) for t in a.targets]   # all checked before anything changes
    take_token(a.slug, a.targets)
    for apply, _, _ in prepared:
        apply()
    st.pop("review_pause", None)   # Paul has looked: his /approve also ends a pending review pause (CM-044)
    S.save(a.slug, st)
    for _, text, _ in prepared:
        append(d / "log.md", text)
    if a.decision in S.GATES["met_decisions"] and "entity_approved" in a.targets:
        n = settle_decision_sheet(a.slug, (st["gates"].get("entity_approved") or {}).get("files") or {})
        if n:
            print(f"Decision Sheet: {n} decision(s) settled — they are never asked again")
    S.log_conditions(a.slug, st)
    import drive
    import records
    records.render(a.slug)
    if a.decision in S.GATES["met_decisions"]:   # #10: approved deliverables get a stamped '- APPROVED' Drive copy
        for t in a.targets:
            for f, h in approved_files(st, t).items():
                drive.approved_copy(a.slug, t, f, h, a.decision)
    drive.mirror(a.slug, f"approval-{now()[:10]}", closed_ok=True)   # R4: Approval Record and Status reach Drive
    labels = ", ".join(lbl for _, _, lbl in prepared)
    print(git_commit(f"{a.slug}: {labels} {a.decision} by Paul", slug=a.slug))


if __name__ == "__main__":
    main()
