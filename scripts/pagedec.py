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
    pagedec.py screen <slug> [--run R] [--check]
                      the redirect pre-screen (Rewrite 4 Phase 3): CM-019 conditions 1–3 computed for every URL the audit
                      knows (the URL Decision Map, the URL inventory, the crawl, rankings and backlinks) from the files on
                      disk — rankings (data/rankings/url-rankings.csv, C1; Search Console clicks / GA4 sessions exports in
                      inputs/ count as value too), backlinks (data/backlinks/backlinks-per-url.csv, C2), the GBP website
                      field (facts.json) and citation-tracker domains linking to the URL (C3), and the crawl's internal
                      inlinks (shown: the links to repoint). Each URL → pass · fail · needs evidence (a source is not on
                      file). Condition 4 (no leads) is the client's and is never computed. Writes
                      audit/<date>/redirect-screen.csv + .md. The audit agent decides only the `needs evidence` rows and
                      entity mismatches; a `fail` URL is never a destructive candidate.
                      --check also reads the URL Decision Map and refuses (exit 4) every destructive row (redirect, merge,
                      consolidate, noindex, remove, canonical) on a URL the screen fails — the reviewer's withdrawals,
                      caught before the review.

With --run the decision is also logged and settled in the safety log; without it (a system session cannot open a client
run) only page-decisions.json is written — the Worklist and the settled register read the file either way.
Rows the decision adds carry the ids <decision>-trash…, <decision>-301…, <decision>-open and are ticked like any worklist row
(handoff.py ingest routes them back here).
"""
import argparse
import csv
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


# ------------------------------------------------------------------ the redirect pre-screen (CM-019 conditions 1–3)
SCREEN_COLS = ["url", "url_key", "crawl_status", "internal_inlinks", "c1", "c1_detail", "c2", "c2_detail", "c3",
               "c3_detail", "c4", "result", "decided_by"]
DESTRUCTIVE = re.compile(r"\b(301|redirect|merge|consolidat|noindex|remove|delete|canonical)", re.I)


def destructive(action):
    """True when a URL Decision Map action takes the URL away (CM-019 applies). Keeping, improving, creating, holding,
    keeping live as Needs Evidence and keeping an existing 301 are not."""
    a = re.sub(r"\s+", " ", (action or "").strip().lower())
    if not a or re.match(r"^(keep|hold|improve|rebuild|create|needs evidence|n/a)\b", a):
        return False
    return bool(DESTRUCTIVE.search(a))


def url_key(u, domain=""):
    """host (no www) + path, no trailing slash, lower case — http/https and www/bare are one URL."""
    import urllib.parse
    u = (u or "").strip()
    if u.startswith("/"):
        u = domain + u
    p = urllib.parse.urlparse(u if "://" in u else "https://" + u)
    return (p.netloc.lower().replace("www.", "") + "/" + p.path.strip("/")).rstrip("/").lower()


def _csv(path):
    csv.field_size_limit(10 ** 8)
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _col(row, *names):
    low = {k.lower().strip(): k for k in row}
    return next((low[n] for n in names if n in low), None)


def _num(v):
    try:
        return float(str(v).replace(",", "").strip() or 0)
    except ValueError:
        return 0.0


def _newest(d, *pats):
    hits = sorted({h for p in pats for h in d.glob(p)}, key=lambda h: h.name) if d.exists() else []
    return hits[-1] if hits else None


def _audit(slug):
    from render import audit_dir
    return audit_dir(slug)


def _crawl(slug):
    return _newest(client_dir(slug) / "inputs" / "crawl", "* - DFS - internal_all - *.csv", "* - SF - internal_all - *.csv")


def map_rows(slug):
    """The latest revision of every URL Decision Map row ([] before the map exists)."""
    a = _audit(slug)
    f = a / "url-decision-map.csv" if a else None
    if not f or not f.is_file():
        return []
    from render import latest
    return latest(_csv(f), key="URL ID", rev="ext_revision")


def screen_sources(slug):
    """Everything the screen reads, keyed by url_key — None for a source not on file (→ needs evidence)."""
    import facts as F
    cd = client_dir(slug)
    st = S.load(slug)
    domain = re.sub(r"^https?://|/$", "", st["client"].get("domain") or "")
    src = {"domain": domain, "rank": None, "traffic": None, "links": None, "citations": set(), "gbp": None,
           "inlinks": {}, "status": {}, "files": []}
    f = cd / "data" / "rankings" / "url-rankings.csv"
    if f.is_file():
        src["rank"] = {url_key(r["url"]): (int(_num(r.get("keywords_top100"))), r.get("best_position", ""),
                                           r.get("total_volume", "")) for r in _csv(f)}
        src["files"].append(f)
    f = cd / "data" / "backlinks" / "backlinks-per-url.csv"
    f = f if f.is_file() else _newest(cd / "data" / "backlinks", "* - DFS - backlinks - *.csv")
    if f:
        src["links"] = {}
        for r in _csv(f):
            k = url_key(r.get("url_to") or r.get("url") or "")
            ex = [x.strip().lower().removeprefix("www.") for x in (r.get("example_referring_domains") or "").split("|") if x.strip()]
            old = src["links"].get(k, (0, []))
            src["links"][k] = (old[0] + int(_num(r.get("referring_domains"))), old[1] + ex)
        src["files"].append(f)
    for pat, names, val in (("*GSC*page*.csv", ("top pages", "page", "pages", "url", "landing page"), "clicks"),
                            ("*GA4*landing*.csv", ("landing page", "landing page + query string", "page path", "url"), "sessions")):
        f = _newest(cd / "inputs", pat)
        rows = _csv(f) if f else []
        uc, vc = (_col(rows[0], *names), _col(rows[0], val)) if rows else (None, None)
        if not (uc and vc):
            continue
        src["traffic"] = src["traffic"] or {}
        for r in rows:
            if _num(r[vc]) > 0:
                src["traffic"].setdefault(url_key(r[uc], domain), []).append(f"{int(_num(r[vc]))} {val}")
        src["files"].append(f)
    a = _audit(slug)
    for f in (_newest(cd / "inputs", "*citation-tracker*.csv"), (a / "inventories" / "citations.csv") if a else None):
        if not (f and f.is_file()):
            continue
        for r in _csv(f):
            c = _col(r, "domain", "site", "source")
            if c and r[c].strip():
                src["citations"].add(r[c].strip().lower().removeprefix("www."))
        src["files"].append(f)
    w = next((r.get("value") for r in F.load(slug)["facts"] if re.search(r"gbp-website|website-field", r["id"]) and r.get("value")), None)
    src["gbp"] = url_key(str(w).split()[0]) if w else None
    crawl = _crawl(slug)
    if crawl:
        for r in _csv(crawl):
            k = url_key(r.get("Address"))
            src["status"][k] = r.get("Status Code", "")
            src["inlinks"][k] = r.get("Unique Inlinks") or r.get("Inlinks") or ""
        src["files"].append(crawl)
    return src


def screen_url(url, src):
    k = url_key(url)
    out = {"url": url, "url_key": "/" + (k.split("/", 1)[1] if "/" in k else ""), "c4": "client — never computed",
           "crawl_status": src["status"].get(k, "not crawled"), "internal_inlinks": src["inlinks"].get(k, "")}
    t = (src["traffic"] or {}).get(k)
    if src["rank"] is None:
        out["c1"], out["c1_detail"] = ("fail", "; ".join(t)) if t else ("needs evidence", "no rankings pull on file (S07)")
    else:
        kw, best, vol = src["rank"].get(k, (0, "", ""))
        if kw or t:
            out["c1"] = "fail"
            out["c1_detail"] = "; ".join(([f"{kw} keyword(s) in top 100, best position {best}, volume {vol}"] if kw else []) + (t or []))
        else:
            out["c1"] = "pass"
            out["c1_detail"] = "0 keywords in top 100" + ("; no clicks or sessions (GSC/GA4)" if src["traffic"] is not None else "")
    rd, ex = (src["links"] or {}).get(k, (0, []))
    if src["links"] is None:
        out["c2"], out["c2_detail"] = "needs evidence", "no backlinks pull on file (S08)"
    else:
        out["c2"], out["c2_detail"] = (("fail", f"{rd} referring domain(s): {', '.join(sorted(set(ex))[:4])}") if rd
                                       else ("pass", "0 referring domains"))
    cites = sorted({d for d in ex if d in src["citations"] or any(d.endswith("." + c) for c in src["citations"])})
    if src["gbp"] and k == src["gbp"]:
        out["c3"], out["c3_detail"] = "fail", "the GBP website field points here"
    elif cites:
        out["c3"], out["c3_detail"] = "fail", f"citation listing(s) link here: {', '.join(cites)}"
    elif not src["gbp"]:
        out["c3"], out["c3_detail"] = "needs evidence", "the GBP website field is not in facts.json"
    else:
        out["c3"], out["c3_detail"] = "pass", ("not the GBP website field; no citation domain links here"
                                               + ("" if src["citations"] else " (no citation tracker on file)"))
    cs = (out["c1"], out["c2"], out["c3"])
    out["result"] = "fail" if "fail" in cs else "needs evidence" if "needs evidence" in cs else "pass"
    out["decided_by"] = "agent" if out["result"] == "needs evidence" else "script"
    return out


def screen(slug, run_id=None, write=True):
    """[row] for every URL the audit knows; writes audit/<date>/redirect-screen.csv + .md unless write=False."""
    src = screen_sources(slug)
    urls, seen = [], set()

    def add(u):
        k = url_key(u, src["domain"])
        if u and "." in k.split("/")[0] and k not in seen:
            seen.add(k)
            urls.append(u if "://" in u else "https://" + k)
    for r in map_rows(slug):
        add(r.get("Current URL", ""))
    a = _audit(slug)
    if a and (a / "inventories" / "url-inventory.csv").is_file():
        for r in _csv(a / "inventories" / "url-inventory.csv"):
            add(r.get("url", ""))
    if _crawl(slug):
        for r in _csv(_crawl(slug)):
            if "html" in (r.get("Content Type") or "html"):
                add(r.get("Address", ""))
    for k in list(src["rank"] or {}) + list(src["links"] or {}):
        add(k)
    rows = [screen_url(u, src) for u in urls]
    if not write:
        return rows
    if not a:
        die(f"no audit folder yet for {slug} — pipeline.py {slug} inventory --phase audit creates it", 4)
    with open(a / "redirect-screen.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=SCREEN_COLS)
        w.writeheader()
        w.writerows(rows)
    n = {x: sum(r["result"] == x for r in rows) for x in ("pass", "fail", "needs evidence")}
    md = [f"# {S.load(slug)['client']['name']} - Redirect pre-screen", "",
          f"Made by `scripts/pagedec.py screen` ({now()[:10]}) from "
          + ", ".join(f"`{p.relative_to(client_dir(slug))}`" for p in src["files"]) + ". CM-019 conditions 1–3 per URL; "
          "condition 4 (no leads) is the client's. A `fail` URL is never a destructive candidate; the audit agent decides "
          "only the `needs evidence` rows (and entity mismatches).", "",
          f"{len(rows)} URL(s): {n['pass']} pass · {n['fail']} fail · {n['needs evidence']} needs evidence", "",
          "| URL | C1 | C2 | C3 | Result |", "|---|---|---|---|---|"]
    md += [f"| {r['url_key']} | {r['c1']}: {r['c1_detail']} | {r['c2']} | {r['c3']} | {r['result']} |"
           for r in rows if r["result"] != "pass"]
    (a / "redirect-screen.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    if run_id:
        import run as R
        R.log_change(slug, run_id, "audit_screen", str((a / "redirect-screen.csv").relative_to(ROOT)),
                     "redirect pre-screen (CM-019 C1–C3)", "",
                     f"{n['pass']} pass, {n['fail']} fail, {n['needs evidence']} needs evidence", "DONE", channel="local")
    return rows


def screen_index(slug):
    """{url_key: screen row} from the saved screen (or a fresh one, not written)."""
    a = _audit(slug)
    f = a / "redirect-screen.csv" if a else None
    rows = _csv(f) if f and f.is_file() else screen(slug, write=False)
    return {url_key(r["url"]): r for r in rows}


def screen_check(slug, rows=None):
    """[(URL ID, url, action, why)] — destructive URL Decision Map rows on a URL the screen fails."""
    by = {url_key(r["url"]): r for r in rows} if rows is not None else screen_index(slug)
    out = []
    for m in map_rows(slug):
        r = by.get(url_key(m.get("Current URL", "")))
        if r and r["result"] == "fail" and destructive(m.get("Proposed Action")):
            why = "; ".join(f"{c.upper()} {r[c + '_detail']}" for c in ("c1", "c2", "c3") if r[c] == "fail")
            out.append((m.get("URL ID", ""), m.get("Current URL", ""), m.get("Proposed Action", ""), why))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("record"); s.add_argument("slug"); s.add_argument("--page", required=True)
    s.add_argument("--action", required=True, choices=ACTIONS); s.add_argument("--reason", required=True)
    s.add_argument("--by", default="Paul"); s.add_argument("--source", default=""); s.add_argument("--into")
    s.add_argument("--redirect-from", action="append"); s.add_argument("--wp-id", action="append", type=int)
    s.add_argument("--supersedes"); s.add_argument("--match"); s.add_argument("--run")
    s = sub.add_parser("list"); s.add_argument("slug")
    s = sub.add_parser("screen"); s.add_argument("slug"); s.add_argument("--run"); s.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.cmd == "screen":
        if a.run:
            import run as R
            R.open_run(a.slug, a.run)
        rows = screen(a.slug, a.run)
        n = {x: sum(r["result"] == x for r in rows) for x in ("pass", "fail", "needs evidence")}
        print(f"{len(rows)} URL(s) screened (CM-019 C1–C3): {n['pass']} pass · {n['fail']} fail · {n['needs evidence']} "
              f"needs evidence (the agent decides those) · clients/{a.slug}/audit/<date>/redirect-screen.csv")
        if a.check:
            bad = screen_check(a.slug, rows)
            for uid, url, act, why in bad[:20]:
                print(f"REFUSED {uid} {url}: '{act[:50]}' fails {why[:120]}")
            if bad:
                print(f"{len(bad)} destructive row(s) on URLs that fail CM-019 — keep each live (Needs Evidence, no "
                      "target) in a superseding row (exit 4)")
                sys.exit(4)
            print("every destructive row passes the screen")
        return
    if a.cmd == "list":
        for r in load(a.slug):
            print(f"{r['id']} {r['action']:18} {r['page']:22} {r['reason'][:80]}")
        return
    rec, new = record(a.slug, a.page, a.action, a.reason, a.by, a.source, a.into, a.redirect_from, a.wp_id, a.supersedes,
                      a.match, a.run)
    print(f"{rec['id']} {rec['action']} {rec['page']}" + ("" if new else " (already recorded)"))


if __name__ == "__main__":
    main()
