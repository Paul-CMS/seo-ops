#!/usr/bin/env python3
"""placeholders.py — every placeholder in a page, so none ships silently (rewrite 2 P11, Q10).

    placeholders.py scan <file> [--shipped]     list every placeholder (exit 1 if any)

Found: `[NEED: …]`, `[Link placeholder …]`, `[LINK → /slug/ · reason]`, `[Link wheel …]` (with --shipped only — before
ship the link-wheel table rows are filled from the wheel), `[PLACEHOLDER …]`, `[TBD …]`, `[PAUL'S …]`, TODO, TBD, XXX,
`{{…}}`, and any other `[…]` that is not a Markdown link.

Where they are used:
- drafts approval: the /approve line's reason lists every placeholder per page, so Paul approves knowingly (next.py);
- ship: a WordPress draft with an open placeholder gets a visible notice block at the top ("Open items on this page —
  remove before publishing: …"), and each placeholder is a row for Jonie in the publish handoff (publish.py); Jonie
  never publishes a page with a notice block until its rows are resolved;
- /verify: a live page that still contains a placeholder string fails (verify.py).

Inline link placeholders are written only as `[LINK → /slug/ · reason]` (the build writer's one form). The link-wheel
step turns each into a real link once Paul approves the CM-022 exception, or removes the bracket and keeps the text.
"""
import re
import sys
from pathlib import Path

LINK_MARK = re.compile(r"\[LINK →\s*(/[^\s·\]]*/?)\s*·\s*([^\]]+)\]")
WHEEL_ROW = re.compile(r"^\|\s*\[Link wheel: populate ([a-z -]+?) links here\]\s*\|\s*$", re.I)
KINDS = [
    ("NEED note", re.compile(r"\[NEED:[^\]]*\]")),
    ("link placeholder (use [LINK → /slug/ · reason])", re.compile(r"\[Link placeholder[^\]]*\]", re.I)),
    ("inline link marker", LINK_MARK),
    ("link wheel row", re.compile(r"\[Link wheel[^\]]*\]", re.I)),
    ("placeholder", re.compile(r"\[(PLACEHOLDER|TBD|PAUL'?S)\b[^\]]*\]", re.I)),
    ("template field", re.compile(r"\{\{[^}]*\}\}")),
    ("TODO/TBD/XXX", re.compile(r"\b(TODO|TBD|XXX)\b")),
    ("bracketed text", re.compile(r"(?<!!)\[[^\]\n]{1,200}\](?![(\[:])")),
]


def scan_text(text, shipped=False):
    """[{line, kind, text}] — one entry per placeholder; front matter is skipped."""
    out = []
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        start = end + 1 if end else 0
    for n, line in enumerate(lines[start:], start + 1):
        if not shipped and WHEEL_ROW.match(line.strip()):
            continue   # filled from the wheel at ship
        taken = []
        for kind, rx in KINDS:
            for m in rx.finditer(line):
                if any(a <= m.start() < b for a, b in taken):
                    continue
                if kind == "bracketed text" and re.fullmatch(r"\[[ xX]\]", m.group(0)):
                    continue   # a checkbox
                taken.append((m.start(), m.end()))
                out.append({"line": n, "kind": kind, "text": m.group(0)})
    return out


def scan(path, shipped=False):
    return scan_text(Path(path).read_text(encoding="utf-8"), shipped)


def summary(items, limit=6):
    """One line: 'line 76 [LINK → …]; line 80 …'."""
    s = "; ".join(f"line {i['line']} {i['text'][:70]}" for i in items[:limit])
    return s + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def instruction(text):
    """The worklist instruction for a placeholder Jonie can resolve herself (Paul, 2026-10-09), else ''."""
    m = re.match(r"^\[Map:.*?\bmap of (.+?)(?:\s+here\b|\s+—|,\s*not\b|\])", text, re.I)
    if m:
        return f"Jonie: embed a Google map of {m.group(1).strip()}"
    return ""


def notice_block(items):
    """The visible notice at the top of a WordPress draft that still has open placeholders."""
    import html
    lis = "".join(f"<li>{html.escape(i['text'][:160])} (approved file line {i['line']})</li>" for i in items)
    return ("<!-- wp:group {\"className\":\"seo-ops-open-items\"} -->\n<div class=\"wp-block-group seo-ops-open-items\" "
            "style=\"border:3px solid #c00;padding:12px\"><p><strong>Open items on this page — remove before "
            "publishing:</strong></p><ul>" + lis + "</ul></div>\n<!-- /wp:group -->")


LIVE = re.compile(r"\[NEED:|\[Link placeholder|\[LINK →|\[Link wheel|\[PLACEHOLDER|\[TBD|\[PAUL'?S|\{\{|"
                  r"\bTODO\b|\bTBD\b|\bXXX\b|Open items on this page", re.I)


def live_hits(text):
    """Placeholder strings left in a live page's text (verify.py)."""
    return sorted({m.group(0) for m in LIVE.finditer(text)})


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "scan":
        sys.exit(__doc__)
    items = scan(sys.argv[2], "--shipped" in sys.argv)
    for i in items:
        print(f"line {i['line']}: {i['kind']}: {i['text']}")
    print(f"{len(items)} placeholder(s)" if items else "no placeholders")
    sys.exit(1 if items else 0)


if __name__ == "__main__":
    main()
