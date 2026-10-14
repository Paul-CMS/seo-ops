#!/usr/bin/env python3
"""pagedec.py — page decisions: drop, hold, stale drafts, a reworded open item (rewrite 3 §7a).

A decision about a page or URL (create, merge, drop, redirect, hold) is Paul's, and the VA Worklist must follow it. It is
recorded once, here, in clients/<slug>/page-decisions.json — whether it came from a review answer (review.py apply turns the
chosen option into a record) or straight from Paul — and `worklist.py` reads the file:

  drop            the page is not built: its publish and open-item rows are superseded; a "trash draft <id>" Setup row and a
                  301 from each old URL to the page it folds into (--into) are added (Redirects)
  hold            the page is held out of this batch: no publish row, no trash row, the draft stays in WordPress unpublished,
                  the live page is untouched
  stale_drafts    these WordPress drafts do not match the latest approved file: their publish rows are superseded and each gets
                  a "trash draft <id>" Setup row (a fresh draft is shipped from the approved file in a /build ship run)
  rewrite_open_item  an open-item row is replaced by a row in the standard format (--supersedes <ref>)

    pagedec.py record <slug> --page P --action drop|hold|stale_drafts|rewrite_open_item --reason R [--by Paul]
                      [--source "answers.md 25c"] [--into PAGE] [--redirect-from URL ...] [--wp-id N ...]
                      [--supersedes REF] [--match REGEX] [--run RUN_ID]
    pagedec.py list <slug>

With --run the decision is also logged and settled in the safety log; without it (a system session cannot open a client
run) only page-decisions.json is written — the Worklist and the settled register read the file either way.
Rows the decision adds carry the ids <decision>-trash…, <decision>-301…, <decision>-open and are ticked like any worklist row
(handoff.py ingest routes them back here).
"""
import argparse
import json
import re
import sys

import status as S
from lib import ROOT, append, client_dir, die, now, redact, today, write_json

ACTIONS = ("drop", "hold", "stale_drafts", "rewrite_open_item")


def path(slug):
    return client_dir(slug) / "page-decisions.json"


def load(slug):
    p = path(slug)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def save(slug, recs):
    write_json(path(slug), recs)


def _full(url, domain):
    url = (url or "").strip()
    return url if re.match(r"^https?://", url) else f"https://{domain}/{url.lstrip('/')}"


def record(slug, page, action, reason, by="Paul", source="", into=None, redirect_from=None, wp_ids=None,
           supersedes=None, match=None, run_id=None):
    if action not in ACTIONS:
        die(f"action must be one of {', '.join(ACTIONS)}")
    st = S.load(slug)
    if page not in st["pages"]:
        die(f"page {page!r} is not in the site plan")
    if into and into not in st["pages"]:
        die(f"--into {into!r} is not in the site plan")
    domain = re.sub(r"^https?://|/$", "", st["client"]["domain"])
    recs = load(slug)
    if action == "drop" and not wp_ids and st["pages"][page].get("wp_id"):
        wp_ids = [int(st["pages"][page]["wp_id"])]
    dup = next((r for r in recs if r["page"] == page and r["action"] == action and (r.get("supersedes") or "") == (supersedes or "")
                and sorted(r.get("wp_ids") or []) == sorted(wp_ids or [])), None)
    if dup:
        return dup, False   # decided once: recording the same decision again changes nothing
    rec = {"id": f"PD-{len(recs) + 1:02d}", "page": page, "action": action, "reason": redact(reason), "by": by,
           "source": source, "at": now(), "into": into,
           "redirect_from": [_full(u, domain) for u in redirect_from or []], "wp_ids": [int(x) for x in wp_ids or []],
           "supersedes": supersedes, "match": match, "rows": {}, "run": run_id}
    recs.append(rec)
    save(slug, recs)
    if run_id:   # a client run is open: the safety log and the settled register know it too
        import settled
        append(client_dir(slug) / "log.md", f"- PAGE-DECISION {now()[:16]} · run {run_id} · {rec['id']} {action} {page}"
               + (f" → {into}" if into else "") + f" · {rec['reason'][:200]} · by {by}" + (f" · {source}" if source else "") + "\n")
        try:
            settled.settle(slug, run_id, f"page_{page.replace('-', '_')}_{action}", f"{action} {page}: {rec['reason']}"[:300], by=by)
        except SystemExit:
            pass   # already settled under this key
    return rec, True


def decided(slug, page, actions=("drop", "hold")):
    return next((r for r in load(slug) if r["page"] == page and r["action"] in actions), None)


def rows(slug, st=None):
    """The worklist rows the decisions add, as group-record-shaped dicts (the worklist gives them their section)."""
    st = st or S.load(slug)
    domain = re.sub(r"^https?://|/$", "", st["client"]["domain"])
    out = []
    for rec in load(slug):
        page = st["pages"].get(rec["page"]) or {}
        base = {"owner": "Jonie", "added": rec["at"][:10], "decision_map_ref": rec["page"], "_hid": "page-decisions",
                "reason": f"page decision {rec['id']} ({rec['by']}{', ' + rec['source'] if rec.get('source') else ''}): {rec['reason']}"}

        def add(ref, kind, **kw):
            state = rec["rows"].get(ref) or {}
            out.append({**base, "ref": ref, "kind": kind, "status": state.get("status", ""), "note": state.get("note", ""), **kw})
        if rec["action"] in ("drop", "stale_drafts"):
            for wid in rec["wp_ids"]:
                add(f"{rec['id']}-trash-{wid}", "wp_setup", url=f"https://{domain}/?page_id={wid}", field="trash draft",
                    old=f"(draft {wid})", new="(in the WordPress Trash)")
        if rec["action"] == "drop" and rec.get("into"):
            tgt = (st["pages"].get(rec["into"]) or {}).get("url") or ""
            for i, u in enumerate(rec["redirect_from"], 1):
                add(f"{rec['id']}-301-{i}", "redirect", url=u, field="301", old=u, new=tgt)
        if rec["action"] == "rewrite_open_item" and page.get("file"):
            import placeholders
            rx = re.compile(rec.get("match") or r"map", re.I)
            for i, it in enumerate([x for x in placeholders.scan(ROOT / page["file"]) if rx.search(x["text"])], 1):
                add(f"{rec['id']}-open-{i}", "publish", url=f"https://{domain}/?page_id={page.get('wp_id')}", field="open item",
                    old=it["text"], new="")
    return out


def set_row(slug, ref, status, note=""):
    recs = load(slug)
    for rec in recs:
        if ref.startswith(rec["id"] + "-"):
            rec["rows"][ref] = {"status": status, "note": note}
            save(slug, recs)
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("record"); s.add_argument("slug"); s.add_argument("--page", required=True)
    s.add_argument("--action", required=True, choices=ACTIONS); s.add_argument("--reason", required=True)
    s.add_argument("--by", default="Paul"); s.add_argument("--source", default=""); s.add_argument("--into")
    s.add_argument("--redirect-from", action="append"); s.add_argument("--wp-id", action="append", type=int)
    s.add_argument("--supersedes"); s.add_argument("--match"); s.add_argument("--run")
    s = sub.add_parser("list"); s.add_argument("slug")
    a = ap.parse_args()
    if a.cmd == "list":
        for r in load(a.slug):
            print(f"{r['id']} {r['action']:18} {r['page']:22} {r['reason'][:80]}")
        return
    rec, new = record(a.slug, a.page, a.action, a.reason, a.by, a.source, a.into, a.redirect_from, a.wp_id, a.supersedes,
                      a.match, a.run)
    print(f"{rec['id']} {rec['action']} {rec['page']}" + ("" if new else " (already recorded)"))


if __name__ == "__main__":
    main()
