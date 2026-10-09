#!/usr/bin/env python3
"""facts.py — one store for every fact about the client (rewrite 2 P4, Q3: a question answered once is never asked
again).

    facts.py list <slug> [--section A|D]          every fact: id · status · value
    facts.py get  <slug> --ids ID[,ID…]           only those facts (read by id, never the whole Brand Guide)
    facts.py render <slug>                        regenerate the Brand Guide's Section A and D fact rows from facts.json

clients/<slug>/facts.json is the single source. Each row: id, section (A|D), label, value, status, source, quote,
date, who, count (reviews that support a customer_reported fact, CM-057). Statuses are machine values:
client_confirmed · paul_approved · internally_verified · customer_reported · submitted · unknown · disputed — their
display labels are the Brand Guide's. Every answer from Paul or the client goes in one way only:
`run.py fact <slug> <RUN_ID> --id … --value … --status … --source …` (logged). The Brand Guide's fact rows are
generated from here (records.py); nobody edits them by hand. A client with no facts.json yet is read from its Brand
Guide (bootstrap, not saved) until the migration writes it.
"""
import argparse
import json
import re
import sys

from lib import client_dir, die, now, read_json, today, write_json

STATUSES = ("client_confirmed", "paul_approved", "internally_verified", "customer_reported", "submitted", "unknown",
            "disputed")
LABELS = {"client_confirmed": "Client Confirmed", "paul_approved": "Paul Approved",
          "internally_verified": "Internally Verified", "customer_reported": "Customer Reported",
          "submitted": "Submitted", "unknown": "Unknown", "disputed": "Disputed"}
SECTIONS = {"A": ("#", "Field", "Value", "Status"), "D": ("Fact", "Value", "Status", "Source")}


def path(slug):
    return client_dir(slug) / "facts.json"


def fact_id(section, label):
    return (section.lower() + "-" + re.sub(r"[^a-z0-9]+", "-", re.sub(r"\*", "", label).lower()).strip("-"))[:60]


def status_of(cell):
    """The machine status from a Brand Guide status cell: its leading status word (P1); anything else is submitted."""
    s = re.sub(r"[\s_-]+", " ", str(cell or "")).strip().lower()
    for k in STATUSES:
        if s.startswith(k.replace("_", " ")):
            return k
    if s.startswith("n/a") or s.startswith("standard"):
        return "internally_verified"
    return "submitted" if s else "unknown"


# ------------------------------------------------------------------ Brand Guide tables
def _table(text, letter):
    """(start, end, header line index, [(line index, cells)]) of Section <letter>'s main table."""
    lines = text.splitlines()
    m = next((i for i, l in enumerate(lines) if re.match(rf"^## Section {letter}\b", l)), None)
    if m is None:
        return lines, None
    rows, head = [], None
    for i in range(m + 1, len(lines)):
        l = lines[i]
        if l.startswith("## ") or l.startswith("### "):
            break
        if l.startswith("|"):
            if re.match(r"^\|[\s\-|:]+\|\s*$", l):
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if head is None:
                head = i
            else:
                rows.append((i, cells))
        elif head is not None and rows:
            break
    return lines, (head, rows)


def from_brand_guide(text):
    """Every Section A and D fact row as a facts.json row (status_text keeps the cell exactly as it was)."""
    out = []
    for letter in ("A", "D"):
        _, t = _table(text, letter)
        if not t:
            continue
        for _, cells in t[1]:
            if letter == "A" and len(cells) >= 4:
                num, label, value, st = cells[0], cells[1], cells[2], cells[3]
                src = ""
            elif letter == "D" and len(cells) >= 4:
                num, label, value, st, src = "", cells[0], cells[1], cells[2], cells[3]
            else:
                continue
            m = re.search(r"\b(20\d\d-\d\d-\d\d)\b", st)
            out.append({"id": fact_id(letter, label), "section": letter, "num": num, "label": label, "value": value,
                        "status": status_of(st), "status_text": st, "source": src, "quote": "",
                        "date": m.group(1) if m else "", "who": "", "count": None})
    return out


def load(slug):
    """{'facts': [rows], 'bootstrap': bool}."""
    data = read_json(path(slug))
    if data is not None:
        return {"facts": data.get("facts") or [], "bootstrap": False}
    bg = client_dir(slug) / "brand-guide.md"
    return {"facts": from_brand_guide(bg.read_text(encoding="utf-8")) if bg.exists() else [], "bootstrap": True}


def save(slug, rows):
    write_json(path(slug), {"_about": "rewrite 2 P4 — the single source for every fact about the client. Written only "
                                      "by run.py fact (and migrate.py); the Brand Guide rows are generated from it.",
                            "updated": now(), "facts": rows})


def by_id(rows):
    return {r["id"]: r for r in rows}


def status_cell(r):
    if r.get("status_text") is not None:
        return r["status_text"]
    cell = f"{LABELS.get(r['status'], r['status'])} {r.get('date') or ''}".strip()
    if r.get("status") == "customer_reported" and r.get("count"):
        cell += f" ({r['count']} reviews)"
    if r.get("was"):
        cell += f" · was: {r['was']}"
    return cell


def row_cells(r):
    esc = lambda v: str(v or "").replace("|", "/")
    if r["section"] == "A":
        return [esc(r.get("num")), esc(r["label"]), esc(r["value"]), esc(status_cell(r))]
    src = r.get("source") or ""
    if r.get("quote"):
        src += f" — \"{r['quote'][:200]}\""
    return [esc(r["label"]), esc(r["value"]), esc(status_cell(r)), esc(src)]


def _line(cells):
    return "|" + "|".join(f" {c} " if c else " " for c in cells) + "|"


def render_into_text(text, rows):
    """The Brand Guide with its Section A and D fact rows regenerated from rows; every other line kept."""
    for letter in ("A", "D"):
        lines, t = _table(text, letter)
        if not t:
            continue
        head, trows = t
        mine = [r for r in rows if r["section"] == letter]
        ids = by_id(mine)
        seen = set()
        for i, cells in trows:
            label = cells[1] if letter == "A" and len(cells) > 1 else (cells[0] if cells else "")
            fid = fact_id(letter, label)
            if fid in ids:
                lines[i] = _line(row_cells(ids[fid]))
                seen.add(fid)
        new = [r for r in mine if r["id"] not in seen]
        if new:
            last = trows[-1][0] if trows else head + 1
            lines[last + 1:last + 1] = [_line(row_cells(r)) for r in new]
        text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def render(slug):
    """Regenerate the Brand Guide's fact rows from facts.json (records.py). No facts.json → nothing to do."""
    data = load(slug)
    if data["bootstrap"]:
        return False
    p = client_dir(slug) / "brand-guide.md"
    if not p.exists():
        return False
    old = p.read_text(encoding="utf-8")
    new = render_into_text(old, data["facts"])
    if new != old:
        p.write_text(new, encoding="utf-8")
    return new != old


def set_fact(slug, fid, value=None, status=None, source=None, quote=None, label=None, section=None, who="Paul",
             count=None):
    """Create or update one fact. Returns (row, old row or None). The display status text is rebuilt whenever the
    status or value changes."""
    if status and status not in STATUSES:
        die(f"unknown status {status!r} — one of: {', '.join(STATUSES)}")
    data = load(slug)
    rows = data["facts"]
    cur = by_id(rows).get(fid)
    old = dict(cur) if cur else None
    if not cur:
        if not label:
            die(f"no fact {fid} yet — a new fact needs --label (and --section A|D, default D)")
        sec = (section or (fid[0].upper() if fid[:2] in ("a-", "d-") else "D")).upper()
        cur = {"id": fid, "section": sec, "num": "", "label": label, "value": "", "status": "unknown",
               "source": "", "quote": "", "date": "", "who": "", "count": None}
        rows.append(cur)
    changed = False
    for k, v in (("value", value), ("status", status), ("source", source), ("quote", quote), ("count", count)):
        if v is not None and cur.get(k) != v:
            if k == "status":
                cur["was"] = LABELS.get(cur.get("status"), cur.get("status"))
            cur[k] = v
            changed = True
    if changed:
        cur["status_text"] = None
        cur["date"], cur["who"] = today(), who
    save(slug, rows)
    return cur, old


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("slug"); s.add_argument("--section")
    s = sub.add_parser("get"); s.add_argument("slug"); s.add_argument("--ids", required=True)
    s = sub.add_parser("render"); s.add_argument("slug")
    a = ap.parse_args()
    if a.cmd == "render":
        print("Brand Guide fact rows regenerated" if render(a.slug) else "nothing changed")
        return
    rows = load(a.slug)["facts"]
    if a.cmd == "get":
        want = [x.strip() for x in a.ids.split(",")]
        rows = [r for r in rows if r["id"] in want]
        missing = [w for w in want if w not in {r["id"] for r in rows}]
        if missing:
            print("not found: " + ", ".join(missing), file=sys.stderr)
    elif a.section:
        rows = [r for r in rows if r["section"] == a.section.upper()]
    for r in rows:
        print(f"{r['id']} · {r['status']} · {r['label']}: {r['value']}" + (f" · source {r['source']}" if r.get("source") else ""))


if __name__ == "__main__":
    main()
