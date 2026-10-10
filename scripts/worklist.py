#!/usr/bin/env python3
"""worklist.py — one living VA Worklist per client (rewrite 2 P9, Q8).

    worklist.py build <slug>      regenerate clients/<slug>/handoffs/VA-WORKLIST.csv and VA-WORKLIST.md

Every item the system hands to a person is a row of ONE worklist — the document Jonie and Gwen work from (copied to
Drive as "<Client> - VA Worklist.md" and ".csv"). Sections, in order:
  1 Setup          WordPress user, SEOPress settings
  2 Blockers       the technical blocker items (they go to Jonie at once; they never hold up writing)
  3 Redirects      redirects and slug changes not paired with a publish
  4 Publish        every page to publish, its paired 301 next to it, and its open items (P11)
  5 After publish  menus, link-table updates, alt text and other live-page work
  6 Manual lookups Gwen's items (citations, GBP, records, content review)
Sections 1, 2 and 6 can go to the VA at any time (they block nothing). Sections 3–5 are handed over ONCE, when every
service and location page is a WordPress draft (`/build <slug> handoff`); until then the worklist says so.
Rows are appended as work is added; nothing is overwritten. The VA ticks `status` (done | blocked | deviated) and adds a
`note`, then returns the CSV: `handoff.py ingest <slug> --run R --returned <the returned VA-WORKLIST.csv>`. /verify
checks every done row. Behind each row sits its group record (handoffs/H-….csv: the ref, the log, /verify, rollback);
the old per-handoff documents (H-….md) are marked superseded — the VA uses only the worklist.
"""
import csv
import re
import sys

import status as S
from lib import client_dir, today

SECTIONS = {1: "Setup", 2: "Blockers", 3: "Redirects", 4: "Publish", 5: "After publish", 6: "Manual lookups"}
COLS = ["section", "ref", "owner", "added", "kind", "url", "field", "old", "new", "reason", "decision_map_ref", "status",
        "note"]
HFILE = re.compile(r"^(H-(\d{4}-\d{2}-\d{2})-\d+-([a-z_]+))\.csv$")
GUIDE = {
    1: "Set up the site for the system (the seo-ops Editor user, read-only SEOPress checks). Change nothing else.",
    2: "Technical blockers. Fix each one as written; check the current value first. These never stop page writing.",
    3: "301 redirects in SEOPress → Redirections, From URL → To URL exactly as written. Never delete the old page.",
    4: "Every page in this section is a WordPress **draft** made from its approved file. Publish **all of them together** "
       "(they link to each other): apply the Kadence layout and styling, add images, publish at exactly the URL in "
       "`new`, and add each `301` row listed under its page at the same time. Do NOT change wording, headings, title, "
       "meta, keyword or URL (an unavoidable change: mark `deviated` and say why). A page with an **open item** row, or "
       "an 'Open items on this page' notice, is not published until that row is resolved.",
    5: "After the pages are live: menus, link-table additions, alt text. Change nothing else on the page.",
    6: "Manual lookups and records (Gwen). Record what you find in `note`.",
}


def section_of(kind, hid, st):
    if hid in (st.get("blocker_handoffs") or []):
        return 2
    if kind in ("wp_setup", "seopress_settings"):
        return 1
    if kind in ("redirect", "slug", "consolidation"):
        return 3
    if kind == "publish":
        return 4
    owner = (S.GATES["change_kinds"].get(kind) or {}).get("owner", "Gwen")
    return 6 if owner == "Gwen" else 5


def read_csv(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def rows(slug):
    """Every row of every group record, with its section, owner and date added (in the order they were added)."""
    st = S.load(slug)
    d = client_dir(slug) / "handoffs"
    out = []
    for f in sorted(d.glob("H-*.csv")) if d.exists() else []:
        m = HFILE.match(f.name)
        if not m:
            continue
        hid, added, kind = m.group(1), m.group(2), m.group(3)
        md = f.with_suffix(".md")
        who = re.search(r"\*\*For:\*\* (\w+)", md.read_text()) if md.exists() else None
        owner = who.group(1) if who else (S.GATES["change_kinds"].get(kind) or {}).get("owner", "Gwen")
        sec = section_of(kind, hid, st)
        for r in read_csv(f):
            out.append({"section": sec, "ref": r["ref"], "owner": owner, "added": added, "kind": kind,
                        **{k: r.get(k, "") for k in COLS[5:]}, "_hid": hid})
    return out


def handed_over(st):
    return bool(st.get("publish_handoff"))


def build(slug):
    st = S.load(slug)
    d = client_dir(slug) / "handoffs"
    d.mkdir(parents=True, exist_ok=True)
    allr = rows(slug)
    if not allr and not (d / "VA-WORKLIST.csv").exists():
        return None
    over = handed_over(st)
    shown = [r for r in allr if over or r["section"] in (1, 2, 6)]
    held = len(allr) - len(shown)
    shown.sort(key=lambda r: (r["section"], r["added"], r["ref"]))
    with open(d / "VA-WORKLIST.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows({**r, "section": f"{r['section']} {SECTIONS[r['section']]}"} for r in shown)
    name = st["client"]["name"]
    done = sum(r["status"] in ("done", "verified") for r in shown)
    md = [f"# {name} - VA Worklist", "",
          f"**One living worklist for every VA item** · client {name} ({st['client'].get('domain')}) · updated {today()} · "
          f"**Progress:** {done} of {len(shown)} row(s) done", "",
          "Work from this document only. Tick `status` in the CSV (**done**, **blocked** or **deviated**, with a `note` on "
          "every blocked or deviated row) and send it back. Check each current value first (`old`): already done → mark "
          "`done`, note `already done`; something else → do not change it, mark `blocked` and say what you found. Do not "
          "add rows.", ""]
    if not over:
        md += ["> **Sections 3 Redirects, 4 Publish and 5 After publish come in one handover**, once every service and "
               "location page is a WordPress draft" + (f" ({held} row(s) waiting)." if held else "."), ""]
    for sec, title in SECTIONS.items():
        mine = [r for r in shown if r["section"] == sec]
        if not mine:
            continue
        md += [f"## {sec} · {title}", "", GUIDE[sec], "",
               "| Ref | For | Added | URL | Field | Now | Change to | Why | Status |", "|---|---|---|---|---|---|---|---|---|"]
        md += [f"| {r['ref']} | {r['owner']} | {r['added']} | {r['url']} | {r['field']} | {r['old']} | {r['new']} | "
               f"{r['reason']} | {r['status'] or 'issued'}{(' — ' + r['note']) if r.get('note') else ''} |" for r in mine]
        md.append("")
    (d / "VA-WORKLIST.md").write_text("\n".join(md) + "\n")
    for f in d.glob("H-*.md"):   # the per-handoff documents are superseded by the worklist
        t = f.read_text()
        if HFILE.match(f.with_suffix(".csv").name) and "Superseded by the VA Worklist" not in t:
            lines = t.split("\n", 1)
            f.write_text(lines[0] + "\n\n> **Superseded by the VA Worklist** (`VA-WORKLIST.md`, rewrite 2 P9) — work from "
                         "the worklist; this file is kept as the record.\n" + (lines[1] if len(lines) > 1 else ""))
    return {"rows": len(shown), "held": held, "done": done}


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "build":
        sys.exit(__doc__)
    r = build(sys.argv[2])
    print("no VA items yet" if r is None else f"VA Worklist: {r['rows']} row(s), {r['done']} done"
          + (f", {r['held']} waiting for the handover" if r["held"] else ""))


if __name__ == "__main__":
    main()
