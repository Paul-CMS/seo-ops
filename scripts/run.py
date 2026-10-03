#!/usr/bin/env python3
"""run.py — the safety log. Every command starts and finishes through here.

    run.py start  <slug> <command> [--gates g1,g2,page:<id>] [--note T]   prints RUN_ID
    run.py note   <slug> <run_id> <text>
    run.py change <slug> <run_id> --kind K --url U --field F --old V --new V --result R
                  [--old-file P] [--new-file P] [--ref REF] [--channel wp|handoff|drive|local]
    run.py finish <slug> <run_id> --summary T [--phase T] [--done T] [--waiting T] [--next T]
    run.py abort  <slug> <run_id> --reason T        only when Paul says so
    run.py check  <slug>                            exit 3 if an unfinished run exists

Exit codes: 3 unfinished run found (stop and ask Paul) · 4 gate not met.
log.md and changes.jsonl are append-only; nothing here ever rewrites them.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import status as S
from lib import ROOT, append, client_dir, die, git_commit, now, read_json, redact

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
               channel=None, old_file=None, new_file=None):
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


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("slug"); s.add_argument("command")
    s.add_argument("--gates", default=""); s.add_argument("--note")
    s = sub.add_parser("note"); s.add_argument("slug"); s.add_argument("run_id"); s.add_argument("text")
    s = sub.add_parser("change"); s.add_argument("slug"); s.add_argument("run_id")
    for k in ("kind", "url", "field", "result"):
        s.add_argument(f"--{k}", required=True)
    s.add_argument("--old", default=""); s.add_argument("--new", default="")
    s.add_argument("--old-file"); s.add_argument("--new-file"); s.add_argument("--ref")
    s.add_argument("--channel", choices=["wp", "handoff", "drive", "local"])
    s = sub.add_parser("finish"); s.add_argument("slug"); s.add_argument("run_id")
    s.add_argument("--summary", required=True); s.add_argument("--phase")
    s.add_argument("--done", action="append"); s.add_argument("--waiting", action="append")
    s.add_argument("--clear-waiting", action="store_true"); s.add_argument("--next")
    s = sub.add_parser("abort"); s.add_argument("slug"); s.add_argument("run_id")
    s.add_argument("--reason", required=True)
    s = sub.add_parser("check"); s.add_argument("slug")
    a = ap.parse_args()
    d = client_dir(a.slug)

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
        gates = [g for g in a.gates.split(",") if g]
        if gates:
            st = S.load(a.slug)
            reasons = []
            for g in gates:
                ok, rs = S.check(st, g)
                if not ok:
                    reasons += [r for r in rs if r not in reasons]
            if reasons:
                print(f"REFUSED — /{a.command} can't run for {a.slug} yet. It needs:\n  - " + "\n  - ".join(reasons))
                print(f"\n`python3 scripts/next.py {a.slug}` shows what to do first. Only Paul approves, with /approve.")
                sys.exit(4)
        run_id = f"{now()[:19].replace('-', '').replace(':', '').replace('T', '-')}-{a.command}"
        append(d / "log.md", f"\n## RUN {run_id} · STARTED · /{a.command} · {now()}\n"
               + (f"Gates checked: {', '.join(gates)}\n" if gates else "")
               + (f"Note: {a.note}\n" if a.note else ""))
        print(run_id)
    elif a.cmd == "note":
        open_run(a.slug, a.run_id)
        append(d / "log.md", f"- NOTE {now()[11:19]} {redact(a.text)}\n")
    elif a.cmd == "change":
        n = log_change(a.slug, a.run_id, a.kind, a.url, a.field, a.old, a.new, a.result,
                       a.ref, a.channel, a.old_file, a.new_file)
        print(f"change #{n} logged")
    elif a.cmd == "finish":
        open_run(a.slug, a.run_id)
        ch = changes(a.slug, a.run_id)
        append(d / "log.md", f"## RUN {a.run_id} · FINISHED · {now()}\n"
               f"Changes: {len(ch)} · Summary: {redact(a.summary)}\n")
        st = S.load(a.slug)
        cmd = a.run_id.split("-", 2)[-1]
        st["last_run"] = {"run_id": a.run_id, "command": cmd, "finished": now(),
                          "result": a.summary, "changes": len(ch)}
        cv = st["client_view"]
        if a.phase: cv["phase"] = a.phase
        if a.done: cv["done"] += [x for x in a.done if x not in cv["done"]]
        if a.clear_waiting: cv["waiting_on_client"] = []
        if a.waiting: cv["waiting_on_client"] += [x for x in a.waiting if x not in cv["waiting_on_client"]]
        if a.next: cv["next"] = a.next
        S.save(a.slug, st)
        print(git_commit(f"{a.slug}: /{cmd} finished ({len(ch)} changes)\n\n{a.summary}"))
    elif a.cmd == "abort":
        open_run(a.slug, a.run_id)
        append(d / "log.md", f"## RUN {a.run_id} · ABORTED · {now()}\nReason (Paul): {redact(a.reason)}\n")
        print(git_commit(f"{a.slug}: run {a.run_id} aborted"))


if __name__ == "__main__":
    main()
