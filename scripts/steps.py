#!/usr/bin/env python3
"""steps.py — audit step outcomes, from the registered list in methodology/audit-steps.md.

    steps.py list                                        the registered steps
    steps.py record <slug> --run R <ID> done|skipped|failed --reason T [--output P ...]
    steps.py check <slug>                                exit 4 if any step has no outcome
    steps.py fresh <slug> <ID>                           exit 0 = reuse (Done < 60 days), 1 = re-run
    steps.py manifest <slug>                             Markdown table for the Evidence Manifest

Skipped and Failed need a reason. Outcomes live in status.json -> audit_steps and every
record is also a line in the safety log.
"""
import argparse
import datetime
import re
import sys

import run as R
import status as S
from lib import ROOT, die, now

REG = ROOT / "methodology" / "audit-steps.md"
MAX_AGE_DAYS = 60


def registry():
    rows = []
    for line in REG.read_text().splitlines():
        m = re.match(r"^\|\s*(S\d{2}b?)\s*\|(.+)\|\s*$", line)
        if m:
            cells = [c.strip() for c in m.group(2).split("|")]
            rows.append({"id": m.group(1), "step": cells[0], "phase": cells[1], "how": cells[2],
                         "outputs": cells[3], "used_by": cells[4],
                         "reusable": cells[5].lower().startswith("y")})
    return rows


OPTIONAL = {"S05b"}   # free supplements: recorded when run, never required (an approved audit stays complete)


def missing(st):
    have = st.get("audit_steps") or {}
    return [r for r in registry() if r["id"] not in have and r["id"] not in OPTIONAL]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    s = sub.add_parser("record"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("id"); s.add_argument("outcome", choices=["done", "skipped", "failed"])
    s.add_argument("--reason", default=""); s.add_argument("--output", action="append", default=[])
    s = sub.add_parser("check"); s.add_argument("slug")
    s = sub.add_parser("fresh"); s.add_argument("slug"); s.add_argument("id")
    s = sub.add_parser("manifest"); s.add_argument("slug")
    a = ap.parse_args()

    if a.cmd == "list":
        for r in registry():
            print(f"{r['id']}  {r['phase']:16} {r['step'][:70]}")
        return
    st = S.load(a.slug)
    reg = {r["id"]: r for r in registry()}

    if a.cmd == "record":
        if a.id not in reg:
            die(f"{a.id} is not registered in methodology/audit-steps.md — register the add-on first.")
        if a.outcome in ("skipped", "failed") and not a.reason:
            die(f"{a.outcome} needs --reason")
        R.open_run(a.slug, a.run)
        st.setdefault("audit_steps", {})[a.id] = {"outcome": a.outcome, "reason": a.reason,
                                                  "outputs": a.output, "at": now(), "run": a.run}
        S.save(a.slug, st)
        R.log_change(a.slug, a.run, "audit_step", a.id, reg[a.id]["step"][:60], "", a.outcome,
                     f"{a.outcome.upper()}" + (f" — {a.reason}" if a.reason else ""), channel="local")
        print(f"{a.id} {a.outcome}")
    elif a.cmd == "check":
        left = missing(st)
        if left:
            print("NOT MET — steps with no outcome yet:")
            for r in left:
                print(f"  {r['id']} {r['step']}")
            sys.exit(4)
        print("every registered step has an outcome")
    elif a.cmd == "fresh":
        rec = (st.get("audit_steps") or {}).get(a.id)
        if not rec or rec["outcome"] != "done" or not reg.get(a.id, {}).get("reusable"):
            print("re-run"); sys.exit(1)
        age = (datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(rec["at"])).days
        if age > MAX_AGE_DAYS:
            print(f"re-run (last done {age} days ago, over {MAX_AGE_DAYS})"); sys.exit(1)
        print(f"reuse (done {age} days ago): {', '.join(rec['outputs'])}")
    elif a.cmd == "manifest":
        print("| Step | Outcome | Reason | Outputs | Date |\n|---|---|---|---|---|")
        have = st.get("audit_steps") or {}
        for r in registry():
            h = have.get(r["id"])
            print(f"| {r['id']} {r['step'][:60]} | {h['outcome'].title() if h else '**NO OUTCOME**'} | "
                  f"{(h or {}).get('reason', '')} | {', '.join((h or {}).get('outputs', []))} | "
                  f"{(h or {}).get('at', '')[:10]} |")


if __name__ == "__main__":
    main()
