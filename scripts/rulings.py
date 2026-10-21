#!/usr/bin/env python3
"""rulings.py — print only the rulings a step needs (rewrite 2 P12: rulings by ID, never the whole file).

    rulings.py CM-020 CM-022 RULE-005 …       the named sections of methodology/rulings.md, in the order given
    rulings.py --index                         one line per ruling: ID · title · status
    rulings.py BB-1xx BB-305 …                 a chapter or one rule of the Bradley Standard (sop-source/BB-Standard-v1.0.md)
    rulings.py --section <file> "<heading>"    one '## ' section of a methodology/ or docs/ file (read lists)

Read lists cite IDs; agents run this instead of reading methodology/rulings.md whole (60 KB). An unknown ID is
reported, never guessed.
"""
import re
import sys

from lib import ROOT

FILE = ROOT / "methodology" / "rulings.md"
HEAD = re.compile(r"^## ((?:CM|RULE|PROC|GOV-T|CF)-?\d+[a-z]?) · (.+)$", re.M)


def sections(text=None):
    text = FILE.read_text(encoding="utf-8") if text is None else text
    ms = list(HEAD.finditer(text))
    out = {}
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[m.start():end]
        body = re.split(r"\n---\n|\n# [A-Z]\. ", body)[0].rstrip()
        out[m.group(1)] = (m.group(2), body)
    return out


BB_FILE = ROOT / "sop-source" / "BB-Standard-v1.0.md"
BB_HEAD = re.compile(r"^(#|###) (BB-\d(?:xx|\d\d)) · .+$", re.M)


def bb_sections(text=None):
    """The Bradley Standard by ID (Phase 7): a family 'BB-1xx' (its whole chapter) or one rule 'BB-105'."""
    text = BB_FILE.read_text(encoding="utf-8") if text is None else text
    ms = list(BB_HEAD.finditer(text))
    out = {}
    for m in ms:
        stop = re.compile(r"^# " if m.group(1) == "#" else r"^#{1,3} ", re.M).search(text, m.end())
        out[m.group(2).upper()] = text[m.start():stop.start() if stop else len(text)].rstrip().rstrip("-").rstrip()
    return out


def doc_section(rel, heading, text=None):
    """The '## <heading…>' section of a methodology/ or docs/ Markdown file, up to the next '## ' heading."""
    if not rel.startswith(("methodology/", "docs/")) or ".." in rel:
        sys.exit(f"--section reads methodology/ or docs/ files only, not {rel}")
    text = (ROOT / rel).read_text(encoding="utf-8") if text is None else text
    m = re.search(rf"^## {re.escape(heading)}.*$", text, re.M)
    if not m:
        print(f"no section '## {heading}' in {rel}", file=sys.stderr)
        sys.exit(1)
    nxt = re.compile(r"^## ", re.M).search(text, m.end())
    return text[m.start():nxt.start() if nxt else len(text)].rstrip()


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--section":   # Phase 7: one '## ' section of a methodology file, never the file whole
        if len(args) != 3:
            sys.exit('usage: rulings.py --section <methodology file> "<heading start>"')
        print(doc_section(args[1], args[2]))
        return
    secs = sections()
    if args == ["--index"]:
        for k, (title, body) in secs.items():
            st = re.search(r"\*\*Status\*\* ([^·]+)", body)
            print(f"{k} · {title} · {(st.group(1).strip() if st else '')}")
        return
    missing = []
    bb = None
    for a in args:
        k = a.upper().strip(",")
        if k in secs:
            print(secs[k][1] + "\n")
        elif k.startswith("BB-"):
            bb = bb if bb is not None else bb_sections()
            if k in bb:
                print(bb[k] + "\n")
            else:
                missing.append(a)
        else:
            missing.append(a)
    if missing:
        print("not found in rulings.md or the Bradley Standard: " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
