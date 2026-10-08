#!/usr/bin/env python3
"""run.py — the safety log. Every command starts and finishes through here.

    run.py start  <slug> <command> [--step S] [--batch ID] [--page ID] [--note T]   prints RUN_ID
                  the gates come from scripts/gates.json "steps" (<command>:<step>) — nowhere else
    run.py note   <slug> <run_id> <text>
    run.py change <slug> <run_id> --kind K --url U --field F --old V --new V --result R
                  [--old-file P] [--new-file P] [--ref REF] [--channel wp|handoff|drive|local]
    run.py decision <slug> <run_id> --text T [--ids F-001,F-004]   a decision for decisions.md
    run.py finish <slug> <run_id> --summary T [--handoff FILE]     (the client view is generated, not typed)
    run.py abort  <slug> <run_id> --reason T        only when Paul says so
    run.py check  <slug>                            exit 3 if an unfinished run exists
    run.py steps  [<command>]                       list each step's gates and outputs (from gates.json)

Exit codes: 3 unfinished run found (stop and ask Paul) · 4 gate not met · 12 the step has not
recorded what it must produce (finish refused — record it, or Paul aborts the run).
log.md and changes.jsonl are append-only; nothing here ever rewrites them. finish and abort
regenerate the readable records (records.py) and make the run's one git commit.
"""
import argparse
import json
import re
import secrets
import shutil
import time
import sys
from pathlib import Path

import status as S
from lib import ROOT, append, client_dir, die, git_commit, now, read_json, redact, ref_missing

RUN_LINE = re.compile(r"^## RUN (\S+) · (STARTED|FINISHED|ABORTED) · ")


def runs(slug):
    """{run_id: state} from log.md, in order."""
    out = {}
    for line in (client_dir(slug) / "log.md").read_text().splitlines():
        m = RUN_LINE.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def unfinished(slug):
    return [r for r, s in runs(slug).items() if s == "STARTED"]


def open_run(slug, run_id):
    if runs(slug).get(run_id) != "STARTED":
        die(f"Run {run_id} is not an open run for {slug}. Start one with run.py start.")


def changes(slug, run_id=None):
    p = client_dir(slug) / "changes.jsonl"
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    return [r for r in rows if run_id is None or r["run_id"] == run_id]


def _short(v, n=160):
    v = "" if v is None else str(v).replace("\n", " ⏎ ")
    return v if len(v) <= n else v[: n - 1] + "…"


def log_change(slug, run_id, kind, url, field, old, new, result, ref=None,
               channel=None, old_file=None, new_file=None, closed_ok=False):
    """closed_ok: the automatic Drive mirror right after a run finished (or after an approval) logs under that
    run's id without reopening it."""
    if not closed_ok:
        open_run(slug, run_id)
    d = client_dir(slug)
    n = len(changes(slug)) + 1
    snap = d / "snapshots" / run_id
    rec = {"n": n, "run_id": run_id, "at": now(), "kind": kind, "url": url, "field": field,
           "old": old, "new": new, "result": result, "ref": ref, "channel": channel}
    for label_, src in (("old_file", old_file), ("new_file", new_file)):
        if src:
            snap.mkdir(parents=True, exist_ok=True)
            dst = snap / f"{n:04d}-{label_[:3]}{Path(src).suffix or '.txt'}"
            shutil.copyfile(src, dst)
            rec[label_] = str(dst.relative_to(ROOT))
    rec = json.loads(redact(json.dumps(rec)))
    append(d / "changes.jsonl", json.dumps(rec, ensure_ascii=False) + "\n")
    append(d / "log.md",
           f"- CHANGE #{n} [{kind}] {url} | {field} | old: {_short(rec['old'])} | "
           f"new: {_short(rec['new'])} | result: {result}"
           + (f" | ref {ref}" if ref else "")
           + (f" | snapshots {rec.get('old_file', '')} {rec.get('new_file', '')}".rstrip() if old_file or new_file else "")
           + "\n")
    return n


def step_spec(st, command, step):
    key = f"{command}:{step}" if step else command
    spec = S.GATES["steps"].get(key)
    if spec is None:
        opts = sorted(k for k in S.GATES["steps"] if k == command or k.startswith(command + ":"))
        die(f"Unknown step '{key}'. Steps for /{command}: " + (", ".join(opts) or "none") +
            " (scripts/gates.json → steps).", 2)
    return key, spec


def prev_post(st):
    posts = [pid for pid, p in st["pages"].items() if p.get("type") == "blog"]
    return posts[-1] if posts else None


def resolve(st, spec, a, key):
    raw = spec.get("gates_blog_only") if st["client"]["type"] == "blog-only" and "gates_blog_only" in spec else spec["gates"]
    produces = " ".join(spec.get("produces", []))
    if "{page}" in produces and not a.page:
        die(f"step {key} needs --page <id> — one page per run (CM-043)", 2)
    if "{batch}" in produces and not a.batch:
        die(f"step {key} needs --batch <id>", 2)
    out = []
    for g in raw:
        if "{batch}" in g and not a.batch:
            die(f"step {key} needs --batch <id>", 2)
        if "{page}" in g and not a.page:
            die(f"step {key} needs --page <id>", 2)
        if "{prev_post}" in g:
            pp = prev_post(st)
            if not pp:
                continue  # the first post has no previous post to wait for
            g = g.replace("{prev_post}", pp)
        out.append(g.replace("{batch}", a.batch or "").replace("{page}", a.page or ""))
    return out


def missing_outputs(slug, st, info):
    """What the step must produce (gates.json steps → produces) and has not recorded."""
    spec = S.GATES["steps"].get(info["step"]) or {}
    miss = []
    for want in spec.get("produces", []):
        if "|" in want and not want.startswith(("batch_state:", "steps:")):
            alts = [_missing_one(slug, st, info, w) for w in want.split("|")]
            if all(alts):
                miss.append(" — or — ".join(m[0] for m in alts))
            continue
        miss += _missing_one(slug, st, info, want)
    return miss


def _missing_one(slug, st, info, want):
    miss = []
    want = want.replace("{batch}", info.get("batch") or "").replace("{page}", info.get("page") or "")
    if want.startswith("evidence_batch:"):
        b = S.batch(st, want.split(":", 1)[1]) or {}
        stale = [p for p in b.get("pages", []) if ((st["pages"].get(p) or {}).get("evidence") or {}).get("run") != info["id"]]
        if stale:
            miss.append(f"an evidence grid from this run for {', '.join(stale)} — evidence.py run <slug> --run <RUN_ID> --batch {b.get('id')}")
    elif want.startswith("facts_pack:"):
        b = S.batch(st, want.split(":", 1)[1]) or {}
        if (b.get("facts_interview") or {}).get("run") != info["id"]:
            miss.append(f"the facts interview pack — evidence.py questions <slug> --run <RUN_ID> --batch {b.get('id')}")
    elif want.startswith("page_stage:"):
        _, pid, stage = want.split(":")
        if S.page_stage(st, pid, stage).get("run") != info["id"]:
            miss.append(f"the {stage} for page {pid}, recorded by this run — status.py page-stage <slug> {pid} "
                        f"--stage {stage} --file <file> --run <RUN_ID>")
    elif want.startswith("steps:"):
        left = [x for x in want[6:].split(",") if x not in (st.get("audit_steps") or {})]
        if left:
            miss.append(f"an outcome for audit step(s) {', '.join(left)} — steps.py record <slug> --run <RUN_ID> <S##> done|skipped|failed")
    elif want.startswith("batch_state:"):
        _, bid, states = want.split(":")
        b = S.batch(st, bid) or {}
        if b.get("state") not in states.split("|"):
            miss.append(f"batch {bid} must reach {' or '.join(states.split('|'))} (it is {b.get('state')}) — "
                        f"status.py batch <slug> {bid} --state ...")
    elif want.startswith("batch:"):
        _, bid, stage = want.split(":")
        b = S.batch(st, bid) or {}
        fs = (b.get("files") or {}).get(stage) or []
        gone = [f for f in fs if not (ROOT / f).exists()]
        if not fs or gone:
            miss.append(f"the {stage} files for batch {bid}" + (f" (missing on disk: {', '.join(gone)})" if gone else "")
                        + " — status.py batch <slug> " + bid + " --state ... --files ...")
    elif want == "blog_post":
        ok = any(p.get("type") == "blog" and p.get("file") and (ROOT / p["file"]).exists()
                 and not p.get("approval") for p in st["pages"].values())
        if not ok:
            miss.append("the new blog post registered with its draft file — status.py page <slug> <id> --type blog --file <draft> --state draft_written")
    else:
        m = (st.get("marks") or {}).get(want) or {}
        files = m.get("files") or {}
        gone = [f for f in files if ref_missing(f)]
        stale = bool(m) and m.get("ts", 0) < info.get("started_ts", 0)
        if not files or gone or stale:
            what = S.GATES.get("artifacts", {}).get(want, want)
            miss.append(f"{want}: {what}"
                        + (" — recorded before this run started; record this run's version" if stale and files and not gone else "")
                        + (f" (missing on disk: {', '.join(gone)})" if gone else "")
                        + f" — status.py mark <slug> {want} --file <path> [--file ...]")
    return miss


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("slug"); s.add_argument("command")
    s.add_argument("--step"); s.add_argument("--batch"); s.add_argument("--page"); s.add_argument("--note")
    s = sub.add_parser("note"); s.add_argument("slug"); s.add_argument("run_id"); s.add_argument("text")
    s = sub.add_parser("decision"); s.add_argument("slug"); s.add_argument("run_id")
    s.add_argument("--text", required=True); s.add_argument("--ids")
    s.add_argument("--settle", metavar="KEY", help="settle this decision once (decisions-settled.md)")
    s.add_argument("--reopen", metavar="KEY", help="one reopen request for a settled decision; --text is the reason")
    s.add_argument("--ask", metavar="KEY", help="an open question, asked once; settling the same key closes it")
    s.add_argument("--who", default="Paul", help="with --ask: who the question waits on")
    s = sub.add_parser("change"); s.add_argument("slug"); s.add_argument("run_id")
    for k in ("kind", "url", "field", "result"):
        s.add_argument(f"--{k}", required=True)
    s.add_argument("--old", default=""); s.add_argument("--new", default="")
    s.add_argument("--old-file"); s.add_argument("--new-file"); s.add_argument("--ref")
    s.add_argument("--channel", choices=["wp", "handoff", "drive", "local"])
    s = sub.add_parser("finish"); s.add_argument("slug"); s.add_argument("run_id")
    s.add_argument("--summary", required=True)
    s.add_argument("--handoff", help="Markdown file with this run's Handoff Log section (templates/handoff-log.md)")
    s = sub.add_parser("abort"); s.add_argument("slug"); s.add_argument("run_id")
    s.add_argument("--reason", required=True)
    s = sub.add_parser("check"); s.add_argument("slug")
    s = sub.add_parser("steps"); s.add_argument("command", nargs="?")
    a = ap.parse_args()
    if a.cmd == "steps":
        for k, v in S.GATES["steps"].items():
            if a.command and not (k == a.command or k.startswith(a.command + ":")):
                continue
            print(f"{k:26} reads: {' · '.join(v.get('reads', [])) or '—'}")
            print(f"{k:26} gates: {', '.join(v['gates']) or '—'}"
                  + (f"  (blog-only: {', '.join(v['gates_blog_only'])})" if v.get("gates_blog_only") else "")
                  + f"\n{'':26} produces: {', '.join(v.get('produces', [])) or '—'}")
        return
    d = client_dir(a.slug)

    if a.cmd == "start":
        step_spec(S.load(a.slug), a.command, a.step)   # a mistyped step is a usage error first
    if a.cmd in ("start", "check"):
        left = unfinished(a.slug)
        if left:
            print("STOP — unfinished run(s) found for this client:")
            for r in left:
                n = len(changes(a.slug, r))
                print(f"  - {r}  ({n} change(s) logged before it stopped)")
            print("\nAsk Paul how to proceed: resume it, verify what it changed (/verify),"
                  " roll it back (/rollback), or abort it (run.py abort, Paul's call).")
            sys.exit(3)
        if a.cmd == "check":
            print("no unfinished runs"); return

    if a.cmd == "start":
        st = S.load(a.slug)
        key, spec = step_spec(st, a.command, a.step)
        gates = resolve(st, spec, a, key)
        if gates:
            reasons = []
            for g in gates:
                ok, rs = S.check(st, g)
                if not ok:
                    reasons += [r for r in rs if r not in reasons]
            if reasons:
                print(f"REFUSED — /{a.command} can't run for {a.slug} yet. It needs:\n  - " + "\n  - ".join(reasons))
                print(f"\n`python3 scripts/next.py {a.slug}` shows what to do first. Only Paul approves, with /approve.")
                sys.exit(4)
        import stages
        refusal = stages.session_conflict(a.slug, key, a.batch)   # R2: one session per stage, enforced
        if refusal:
            print(f"REFUSED — {refusal}")
            sys.exit(4)
        sid = stages.current_session()
        run_id = (f"{now()[:19].replace('-', '').replace(':', '').replace('T', '-')}-{a.command}"
                  f"-{secrets.token_hex(2)}")
        st = S.load(a.slug)
        st.setdefault("open_runs", {})[run_id] = {"step": key, "batch": a.batch, "page": a.page, "started": now(),
                                                  "started_ts": time.time(), "session": sid}
        S.save(a.slug, st)
        append(d / "log.md", f"\n## RUN {run_id} · STARTED · /{a.command} · {now()}\n"
               + f"Step: {key}" + (f" · batch {a.batch}" if a.batch else "")
               + (f" · session {sid}" if sid else "") + "\n"
               + (f"Gates checked: {', '.join(gates)}\n" if gates else "")
               + (f"Note: {a.note}\n" if a.note else ""))
        rl = spec.get("reads") or []
        if rl:
            print("Read for this step (only these): " + " · ".join(x.replace("<slug>", a.slug) for x in rl))
        print(run_id)   # always the last line
    elif a.cmd == "note":
        open_run(a.slug, a.run_id)
        append(d / "log.md", f"- NOTE {now()[11:19]} {redact(a.text)}\n")
    elif a.cmd == "decision":
        open_run(a.slug, a.run_id)
        import settled
        if a.settle and a.reopen:
            die("--settle or --reopen, not both.")
        if a.ask:
            settled.ask(a.slug, a.run_id, a.ask, a.who, a.text)
            print(f"open question '{a.ask}' logged (waiting on {a.who})")
            return
        if a.reopen:
            settled.reopen(a.slug, a.run_id, a.reopen, a.text)
            print(f"reopen request logged for '{a.reopen}' (counted as a process defect)")
            return
        if a.settle:
            settled.settle(a.slug, a.run_id, a.settle, a.text)
            print(f"settled: {a.settle}")
            return
        append(d / "log.md", f"- DECISION {now()[:16]} · run {a.run_id} · {redact(a.text)}"
               + (f" · affects {a.ids}" if a.ids else "") + "\n")
        print("decision logged")
    elif a.cmd == "change":
        n = log_change(a.slug, a.run_id, a.kind, a.url, a.field, a.old, a.new, a.result,
                       a.ref, a.channel, a.old_file, a.new_file)
        print(f"change #{n} logged")
    elif a.cmd == "finish":
        open_run(a.slug, a.run_id)
        st0 = S.load(a.slug)
        info = (st0.get("open_runs") or {}).get(a.run_id)
        if info:
            miss = missing_outputs(a.slug, st0, {**info, "id": a.run_id})
            if miss:
                print(f"NOT FINISHED — step {info['step']} has not recorded what it must produce:\n  - "
                      + "\n  - ".join(miss)
                      + "\nRecord it and finish again. If the step could not produce it, stop and ask Paul "
                        "(only he can abort a run).")
                sys.exit(12)
        ch = changes(a.slug, a.run_id)
        cmd = re.sub(r"-[0-9a-f]{4}$", "", a.run_id.split("-", 2)[-1])
        if a.handoff:
            body = Path(a.handoff).read_text(encoding="utf-8").strip()
            # records.py writes the section heading; drop the file's own (old template) so it isn't doubled
            body = re.sub(r"\A#{1,3} [^\n]*\n+", "", body)
            append(d / "log.md", f"### HANDOFF · /{cmd} · {now()[:10]} · run {a.run_id}\n{redact(body)}\n### END HANDOFF\n")
        append(d / "log.md", f"## RUN {a.run_id} · FINISHED · {now()}\n"
               f"Changes: {len(ch)} · Summary: {redact(a.summary)}\n")
        st = S.load(a.slug)
        (st.get("open_runs") or {}).pop(a.run_id, None)
        step = (info or {}).get("step")
        import stages
        skey = stages.session_key(step or "", (info or {}).get("batch"))
        if skey and (info or {}).get("session"):   # R2: this session has now done this stage
            st.setdefault("sessions", {}).setdefault(info["session"], {"key": skey, "step": step, "first_run": a.run_id,
                                                                       "at": now()})
        if S.stage_mode(st, step) == "review":   # CM-044: /next stops here until Paul types /next again
            st["review_pause"] = {"run_id": a.run_id, "step": step, "at": now()}
        if cmd != "drive-mirror":   # a records mirror is bookkeeping; "last run" stays the real work
            st["last_run"] = {"run_id": a.run_id, "command": cmd, "finished": now(),
                              "result": a.summary, "changes": len(ch), "step": step,
                              "batch": (info or {}).get("batch")}
        S.save(a.slug, st)
        S.log_conditions(a.slug, st)
        import drive
        import records
        records.render(a.slug)
        if not a.handoff:
            print("note: no --handoff section given — the Handoff Log has nothing from this run")
        m = drive.mirror(a.slug, a.run_id, closed_ok=True)   # R4: the records reach Drive by file copy, no agent
        print("Drive: " + ("copy pending sync (no local Drive folder — recorded once)" if "pending" in m
                           else f"{m.get('copied', 0)} record(s) copied, {m.get('unchanged', 0)} unchanged"))
        print(git_commit(f"{a.slug}: /{cmd} finished ({len(ch)} changes)\n\n{a.summary}"))
    elif a.cmd == "abort":
        open_run(a.slug, a.run_id)
        append(d / "log.md", f"## RUN {a.run_id} · ABORTED · {now()}\nReason (Paul): {redact(a.reason)}\n")
        st = S.load(a.slug); (st.get("open_runs") or {}).pop(a.run_id, None); S.save(a.slug, st)
        import drive
        import records
        records.render(a.slug)
        drive.mirror(a.slug, a.run_id, closed_ok=True)
        print(git_commit(f"{a.slug}: run {a.run_id} aborted"))


if __name__ == "__main__":
    main()
