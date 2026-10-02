#!/usr/bin/env python3
"""handoff.py — VA handoffs: work the system prepares but a person carries out.

    handoff.py create <slug> --run R --kind K --to Jonie|Gwen --items items.csv [--title T]
    handoff.py ingest <slug> --run R --handoff H-ID --returned returned.csv
    handoff.py list   <slug> [--open]

items.csv columns: url, field, old, new, reason, decision_map_ref
  - kind redirect: url = from URL, new = to URL, field = 301. Every row needs a
    decision_map_ref (its URL Decision Map entry) and a reason.
  - kind slug: a slug change ALWAYS produces its paired 301 redirect rows automatically.

Each handoff becomes clients/<slug>/handoffs/<id>.md (instructions) + <id>.csv (the
worksheet the VA returns: status done | blocked | deviated, note). Every item is logged
in the safety log. /verify checks each item after the VA marks it done.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import run as R
import status as S
from lib import ROOT, client_dir, die, today

KINDS = S.GATES["change_kinds"]
COLS = ["ref", "url", "field", "old", "new", "reason", "decision_map_ref", "status", "note"]


def hdir(slug):
    d = client_dir(slug) / "handoffs"
    d.mkdir(exist_ok=True)
    return d


def read_csv(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def write_csv(p, rows):
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("create"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--kind", required=True, choices=sorted(KINDS)); s.add_argument("--to", required=True)
    s.add_argument("--items", required=True); s.add_argument("--title")
    s = sub.add_parser("ingest"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--handoff", required=True); s.add_argument("--returned", required=True)
    s = sub.add_parser("list"); s.add_argument("slug"); s.add_argument("--open", action="store_true")
    a = ap.parse_args()
    d = hdir(a.slug)

    if a.cmd == "list":
        for f in sorted(d.glob("H-*.csv")):
            rows = read_csv(f)
            open_ = [r for r in rows if r["status"] not in ("done", "verified")]
            if a.open and not open_:
                continue
            print(f"{f.stem}: {len(rows)} item(s), {len(open_)} open")
        return

    R.open_run(a.slug, a.run)
    st = S.load(a.slug)

    if a.cmd == "create":
        gate = KINDS[a.kind]["gate"]
        if gate != "page_approval":
            ok, rs = S.gate_met(st, gate)
            if not ok:
                die(f"REFUSED — {S.label(gate)}: " + "; ".join(rs), 4)
        items = read_csv(a.items)
        if not items:
            die("no items")
        n = len(list(d.glob("H-*.csv"))) + 1
        hid = f"H-{today()}-{n:02d}-{a.kind}"
        rows = []
        for i, it in enumerate(items, 1):
            if a.kind in ("redirect", "slug", "consolidation") and not (it.get("reason") and it.get("decision_map_ref")):
                die(f"row {i}: {a.kind} needs a reason and its URL Decision Map reference")
            rows.append({"ref": f"{hid}-{i:02d}", **{k: it.get(k, "") for k in COLS[1:7]},
                         "status": "issued", "note": ""})
            if a.kind == "slug":
                rows.append({"ref": f"{hid}-{i:02d}R", "url": it["url"], "field": "301",
                             "old": it["url"], "new": it["new_url"] if it.get("new_url") else it["new"],
                             "reason": f"paired redirect for slug change {hid}-{i:02d}",
                             "decision_map_ref": it.get("decision_map_ref", ""), "status": "issued", "note": ""})
        write_csv(d / f"{hid}.csv", rows)
        title = a.title or f"{st['client']['name']} - {a.kind.replace('_', ' ').title()} Handoff"
        md = [f"# {title} - {hid}", "",
              f"**For:** {a.to} · **Prepared:** {today()} · **Client:** {st['client']['name']} ({st['client']['domain']})", "",
              "## What to do", "",
              "Work through every row in the worksheet. For each one: check the current value first "
              "(column `old`). If it is already the new value, mark `done` with note `already done`. "
              "If the current value is something else, do not change it — mark `blocked` and say what you found.", "",
              "Return the worksheet CSV with the `status` column filled: **done**, **blocked** or **deviated**, "
              "and a `note` on every blocked or deviated row. Do not add rows; put anything extra you find "
              "under a separate heading in your reply.", ""]
        if a.kind in ("redirect", "slug"):
            md += ["**Redirects:** 301 only. From URL → To URL exactly as written. Use SEOPress → Redirections. "
                   "Never delete the old page.", ""]
        md += ["| Ref | URL | Field | Now | Change to | Why | Decision Map |", "|---|---|---|---|---|---|---|"]
        md += [f"| {r['ref']} | {r['url']} | {r['field']} | {r['old']} | {r['new']} | {r['reason']} | "
               f"{r['decision_map_ref']} |" for r in rows]
        (d / f"{hid}.md").write_text("\n".join(md) + "\n")
        for r in rows:
            R.log_change(a.slug, a.run, a.kind, r["url"], r["field"], r["old"], r["new"],
                         f"HANDOFF ISSUED to {a.to}", ref=r["ref"], channel="handoff")
        print(f"{hid}: {len(rows)} item(s) → clients/{a.slug}/handoffs/{hid}.md and .csv")

    elif a.cmd == "ingest":
        mine = {r["ref"]: r for r in read_csv(d / f"{a.handoff}.csv")}
        back = read_csv(a.returned)
        problems, seen = [], set()
        for r in back:
            ref = r.get("ref", "")
            if ref not in mine:
                problems.append(f"invented ref {ref!r} — not in the handoff"); continue
            seen.add(ref)
            stt = (r.get("status") or "").strip().lower()
            if stt not in ("done", "blocked", "deviated"):
                problems.append(f"{ref}: invalid status {stt!r} — treated as not done"); continue
            if stt in ("blocked", "deviated") and not r.get("note"):
                problems.append(f"{ref}: {stt} with no note — incomplete")
            mine[ref]["status"], mine[ref]["note"] = stt, r.get("note", "")
            R.log_change(a.slug, a.run, "handoff_return", mine[ref]["url"], mine[ref]["field"],
                         mine[ref]["old"], mine[ref]["new"], f"VA reported {stt}" + (f": {r.get('note')}" if r.get("note") else ""),
                         ref=ref, channel="handoff")
        omitted = [ref for ref in mine if ref not in seen and mine[ref]["status"] == "issued"]
        for ref in omitted:
            problems.append(f"{ref}: silently omitted from the returned worksheet")
        write_csv(d / f"{a.handoff}.csv", list(mine.values()))
        print(f"ingested {len(seen)} row(s). Problems: {len(problems)}")
        for p in problems:
            print("  - " + p)
        print("Next: /verify checks every row marked done against the live site.")


if __name__ == "__main__":
    main()
