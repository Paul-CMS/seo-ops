#!/usr/bin/env python3
"""rulings.py — print only the rulings a step needs (rewrite 2 P12: rulings by ID, never the whole file).

    rulings.py CM-020 CM-022 RULE-005 …       the named sections of methodology/rulings.md, in the order given
    rulings.py --index                         one line per ruling: ID · title · status

Read lists cite IDs; agents run this instead of reading methodology/rulings.md whole (60 KB). An unknown ID is
reported, never guessed.
"""
import re
import sys

from lib import ROOT

FILE = ROOT / "methodology" / "rulings.md"
HEAD = re.compile(r"^## ((?:CM|RULE|PROC|GOV-T|CF)-?\d+[a-z]?) · (.+)$", re.M)


def sections():
    text = FILE.read_text(encoding="utf-8")
    ms = list(HEAD.finditer(text))
    out = {}
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[m.start():end]
        body = re.split(r"\n---\n|\n# [A-Z]\. ", body)[0].rstrip()
        out[m.group(1)] = (m.group(2), body)
    return out


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    secs = sections()
    if args == ["--index"]:
        for k, (title, body) in secs.items():
            st = re.search(r"\*\*Status\*\* ([^·]+)", body)
            print(f"{k} · {title} · {(st.group(1).strip() if st else '')}")
        return
    missing = []
    for a in args:
        k = a.upper().strip(",")
        if k in secs:
            print(secs[k][1] + "\n")
        else:
            missing.append(a)
    if missing:
        print("not found in rulings.md: " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
