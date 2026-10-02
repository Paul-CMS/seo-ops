#!/usr/bin/env python3
"""rollback.py — plan a rollback from the safety log. Paul approves the plan; /rollback runs it.

    rollback.py plan <slug> --of RUN_ID [--change N ...]

Lists, newest first, what can be restored automatically (system-applied WordPress changes,
via `wp.py restore`) and what needs a reverse VA handoff (redirects, slugs and anything a
person did). Nothing here changes the site.
"""
import argparse

import run as R


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("plan"); s.add_argument("slug"); s.add_argument("--of", required=True)
    s.add_argument("--change", type=int, action="append")
    a = ap.parse_args()
    ch = [c for c in R.changes(a.slug, a.of) if c["kind"] not in ("verify", "handoff_return")]
    if a.change:
        ch = [c for c in ch if c["n"] in a.change]
    auto, manual, nothing = [], [], []
    for c in reversed(ch):
        if c.get("channel") == "wp" and c["result"].startswith("APPLIED"):
            auto.append(c)
        elif c.get("channel") == "handoff" and c["result"].startswith("HANDOFF ISSUED"):
            manual.append(c)
        else:
            nothing.append(c)
    print(f"Rollback plan for run {a.of} — newest change first\n")
    print(f"Automatic (wp.py restore, current value checked first): {len(auto)}")
    for c in auto:
        print(f"  #{c['n']} {c['kind']} {c['url']} | put back: {str(c['old'])[:80]!r}")
    print(f"\nReverse VA handoff needed (a person made these): {len(manual)}")
    for c in manual:
        rev = (f"remove the 301 from {c['url']} (currently to {c['new']})" if c["kind"] == "redirect"
               else f"restore {c['field']} to {str(c['old'])[:60]!r}")
        print(f"  #{c['n']} {c['kind']} {c.get('ref')} | {rev}")
    print(f"\nNothing to undo (skipped, stopped or local-only): {len(nothing)}")


if __name__ == "__main__":
    main()
