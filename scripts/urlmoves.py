#!/usr/bin/env python3
"""urlmoves.py — a URL moved: every record that points at the old URL moves with it (fix set, 2026-10-14).

    urlmoves.py check <slug>          list every record that still points at a moved URL; exit 1 when there is one
    urlmoves.py apply <slug> [--dry]  rewrite them, in the client's own folder (run on /next; also by migrate2 after a move)
    urlmoves.py map   <slug>          the moves the plan records: old URL → final URL

What counts as a move: a planned page whose URL differs from `live_url` / `replaces` / `publish.replaces` (the old URLs
now 301 to it), a page dropped by a page decision (`pagedec.py … drop`), and `url_drops` (old URL → where it now goes).
Chains are resolved to the final URL: nothing may point at a URL that itself redirects (no redirect chains).

A *target* is a record that says where something goes or points. These are checked and rewritten:
  - Brand Guide Section C (page inventory) — a moved page's URL, a "consolidated into /x/" target; a dropped page's row
    becomes "Dropped — 301 to …"; per-client prose that no rule can rewrite is in LINE_EDITS;
  - open handoff rows (handoffs/H-*.csv, and the table in the .md): the `new` column (a 301's target, the replacement
    href of a link fix). A redirect row already done gets a target-change row (handoff.py retarget) — apply needs --run;
  - build/blockers/*.csv `new` column, build/link-wheel.json, status wheel_pending, page links_placed.
Never touched: a URL in the `url`/`old` column (the source of a 301 is meant to be the old URL), the audit and its
registers, snapshots, the log, the settled register — history says what was true then.
The Worklist validator (worklist.py check) reports the same errors and, for a 301 whose target itself redirects, the chain.
"""
import argparse
import csv
import re
import sys
import urllib.parse

import status as S
from lib import ROOT, append, client_dir, die, now

HOME = "https://homemobilemedical.com/"
# Drops recorded before the state kept them (rewrite 2 P7: Paul 2026-10-09; handoffs H-2026-10-09-06 and -07).
LEGACY_DROPS = {"home-mobile-medical": {"/service-area/": HOME, "/services/": HOME}}
# Prose in Section C that names the old pattern: not a URL, so no rule can rewrite it. Exact text → new text.
LINE_EDITS = {"home-mobile-medical": [
    ("Canonical pattern `/service-area/{city-state}/` (Decision 023). Hubs: `/service-area/` (Lowcountry) · "
     "`/service-area/charleston/` (Charleston metro area) · `/service-area/hhi-beaufort/` (Hilton Head Island–Bluffton–Port "
     "Royal metro area)",
     "Canonical pattern `/{city-state}/` at the root (Decision 023, revised in rewrite 2, Paul 2026-10-09; no folder). Hubs: "
     "`/charleston-metro/` (Charleston metro area) · `/hilton-head-bluffton-metro/` (Hilton Head Island–Bluffton–Port Royal "
     "metro area); the Lowcountry hub `/service-area/` is dropped (301 to the homepage)"),
]}

CAND = re.compile(r"https?://[^\s|)\]\"'`,;<>]+|(?<![\w/.:{-])/[A-Za-z0-9._~%/-]*[A-Za-z0-9._~%-]/(?![\w{<\[-])")


def path_of(u):
    p = (urllib.parse.urlparse((u or "").strip()).path or "/").lower()
    return p if p.endswith("/") else p + "/"


def moves(slug, st=None):
    """(page_moves, drops): {old path: final full URL} each, chains resolved."""
    st = st or S.load(slug)
    pages = st["pages"]
    cur = {path_of(p["url"]) for p in pages.values() if p.get("url")}
    mv, dr = {}, {}
    for p in pages.values():
        new = p.get("url")
        if not new:
            continue
        olds = list(p.get("replaces") or []) + list((p.get("publish") or {}).get("replaces") or [])
        if p.get("live_url"):
            olds.append(p["live_url"])
        for o in olds:
            k = path_of(o)
            if k != path_of(new) and k not in cur:
                mv[k] = new
    for k, to in {**LEGACY_DROPS.get(slug, {}), **(st.get("url_drops") or {})}.items():
        dr[path_of(k)] = to
    import pagedec
    for rec in pagedec.load(slug):
        if rec["action"] == "drop" and rec.get("into") and (pages.get(rec["into"]) or {}).get("url"):
            to = pages[rec["into"]]["url"]
            for u in [(pages.get(rec["page"]) or {}).get("url")] + list(rec.get("redirect_from") or []):
                if u and path_of(u) not in cur:
                    dr[path_of(u)] = to
    both = {**dr, **mv}
    for k in list(both):
        both[k] = final(both, both[k])
    return {k: both[k] for k in mv}, {k: both[k] for k in dr if k not in mv}


def final(m, url):
    for _ in range(12):
        nxt = m.get(path_of(url))
        if not nxt or path_of(nxt) == path_of(url):
            break
        url = nxt
    return url


def rewrite_text(text, m, ok=None):
    """text with every URL whose path is a moved URL replaced by its final URL (same form: full or path only).
    A URL followed by ' -> ' is the old side of a pair and stays; ok(match, text) can veto a match. Returns (text, count)."""
    out, last, n = [], 0, 0
    for mt in CAND.finditer(text):
        new = m.get(path_of(mt.group(0)))
        if not new or text[mt.end():mt.end() + 4] == " -> " or (ok and not ok(mt, text)):
            continue
        out.append(text[last:mt.start()])
        out.append(new if mt.group(0).startswith("http") else path_of(new))
        last, n = mt.end(), n + 1
    out.append(text[last:])
    return "".join(out), n


def _stale_in(text, m, ok=None):
    return [mt.group(0) for mt in CAND.finditer(text)
            if path_of(mt.group(0)) in m and text[mt.end():mt.end() + 4] != " -> " and (not ok or ok(mt, text))]


_TARGETISH = re.compile(r"(?:\binto|→|->|\bto|\bwith|\bat)\s+$", re.I)


def _bg_ok(mt, text):
    """Brand Guide Section C: a URL is a target to move when it is the row's page URL (first cell) or follows 'into', '→',
    'to' …; 'live URL /x/ is 301'd', 'existing: /x/' and other mentions of what is live today stay."""
    before = text[:mt.start()]
    return before.strip(" |") == "" or bool(_TARGETISH.search(before))


def _section_c(lines):
    a = next((i for i, x in enumerate(lines) if re.match(r"^## Section C\b", x)), None)
    if a is None:
        return range(0)
    b = next((i for i in range(a + 1, len(lines)) if re.match(r"^## ", lines[i])), len(lines))
    return range(a + 1, b)


def _cells(ln):
    return [c.strip() for c in ln.strip().strip("|").split("|")] if ln.lstrip().startswith("|") else []


def _drop_row(ln, dr):
    c = _cells(ln)
    return bool(c) and c[0].startswith(("/", "http")) and path_of(c[0]) in dr and not c[-1].lower().startswith("dropped")


def _csv_rows(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        return list(rd), rd.fieldnames


def _write_csv(p, rows, fields):
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def scan(slug):
    """[{kind, where, old, new, auto, …}] — every stale target. Nothing is written."""
    d = client_dir(slug)
    st = S.load(slug)
    mv, dr = moves(slug, st)
    allm = {**dr, **mv}
    out = []
    bg = d / "brand-guide.md"
    if bg.exists():
        lines = bg.read_text(encoding="utf-8").split("\n")
        for i in _section_c(lines):
            if _drop_row(lines[i], dr):
                c0 = _cells(lines[i])[0]
                out.append({"kind": "brand-guide", "where": f"brand-guide.md:{i + 1}", "old": c0, "new": dr[path_of(c0)], "auto": True})
                continue
            for u in _stale_in(lines[i], mv, _bg_ok):
                out.append({"kind": "brand-guide", "where": f"brand-guide.md:{i + 1}", "old": u, "new": mv[path_of(u)], "auto": True})
        text = "\n".join(lines)
        for old, _new in LINE_EDITS.get(slug, []):
            if old in text:
                out.append({"kind": "brand-guide", "where": "brand-guide.md (Section C prose)", "old": old[:50] + "…",
                            "new": "the root pattern", "auto": True})
    hd = d / "handoffs"
    import worklist
    sup = worklist.superseded(slug)   # rows the Worklist already supersedes need no rewrite
    for f in sorted(hd.glob("H-*.csv")) if hd.exists() else []:
        if not re.match(r"^H-\d{4}-\d{2}-\d{2}-\d+-[a-z_]+\.csv$", f.name):
            continue
        for r in _csv_rows(f)[0]:
            if r.get("status") == "superseded" or r["ref"] in sup:
                continue
            hit = _stale_in(r.get("new") or "", allm)
            if hit:
                done = r.get("status") in ("done", "verified")
                out.append({"kind": "handoff-done" if done else "handoff-open", "where": f"{f.name} {r['ref']}", "old": hit[0],
                            "new": allm[path_of(hit[0])], "auto": not done, "ref": r["ref"], "file": f.name})
    bl = d / "build" / "blockers"
    for f in sorted(bl.glob("*.csv")) if bl.exists() else []:
        for i, r in enumerate(_csv_rows(f)[0], 2):
            hit = _stale_in(r.get("new") or "", allm)
            if hit:
                out.append({"kind": "blocker-items", "where": f"build/blockers/{f.name}:{i}", "old": hit[0],
                            "new": allm[path_of(hit[0])], "auto": True, "file": f"build/blockers/{f.name}"})
    wh = d / "build" / "link-wheel.json"
    if wh.exists():
        n = rewrite_text(wh.read_text(encoding="utf-8"), allm)[1]
        if n:
            out.append({"kind": "link-wheel", "where": "build/link-wheel.json", "old": f"{n} link target(s)", "new": "their final URLs", "auto": True})
    for pid, items in (st.get("wheel_pending") or {}).items():
        for it in items:
            if path_of(it[2]) in allm:
                out.append({"kind": "wheel-pending", "where": f"wheel_pending {pid}", "old": it[2], "new": allm[path_of(it[2])], "auto": True})
    for pid, p in st["pages"].items():
        for u in p.get("links_placed") or []:
            if path_of(u) in allm:
                out.append({"kind": "links-placed", "where": f"page {pid} links_placed", "old": u, "new": allm[path_of(u)], "auto": True})
    return out


def _approvals(st):
    from lib import ref_sha
    out = {}
    for g, rec in (st.get("gates") or {}).items():
        for f, h in ((rec or {}).get("files") or {}).items():
            try:
                out[f"{g}:{f}"] = ref_sha(f) == h
            except OSError:
                out[f"{g}:{f}"] = False
    return out


def apply(slug, dry=False, run=None):
    """Rewrite every stale target scan() finds. Returns report lines ([] when there is nothing to do)."""
    d = client_dir(slug)
    st = S.load(slug)
    todo = scan(slug)
    legacy = LEGACY_DROPS.get(slug) or {}
    need_state = bool(legacy) and not st.get("url_drops")
    if not todo and not need_state:
        return []
    report = [f"  {t['where']}: {t['old']} → {t['new']}" + ("" if t["auto"] else "  (NOT changed: already done — needs a target-change row)")
              for t in todo]
    if dry:
        return report
    before = _approvals(st)
    if need_state:
        st["url_drops"] = dict(legacy)
        S.save(slug, st)
    mv, dr = moves(slug, S.load(slug))
    allm = {**dr, **mv}
    bg = d / "brand-guide.md"
    if bg.exists() and any(t["kind"] == "brand-guide" for t in todo):
        lines = bg.read_text(encoding="utf-8").split("\n")
        for i in _section_c(lines):
            if _drop_row(lines[i], dr):
                lines[i] = re.sub(r"\|[^|]*\|\s*$", f"| Dropped — 301 to {dr[path_of(_cells(lines[i])[0])]} (URL move) |", lines[i].rstrip())
            else:
                lines[i] = rewrite_text(lines[i], mv, _bg_ok)[0]
        text = "\n".join(lines)
        for old, new in LINE_EDITS.get(slug, []):
            text = text.replace(old, new)
        bg.write_text(text, encoding="utf-8")
    hd = d / "handoffs"
    import worklist
    sup = worklist.superseded(slug)
    for f in sorted({t["file"] for t in todo if t["kind"] == "handoff-open"}):
        rows, fields = _csv_rows(hd / f)
        for r in rows:
            if r.get("status") in ("done", "verified", "superseded") or r["ref"] in sup:
                continue
            new, n = rewrite_text(r.get("new") or "", allm)
            if n:
                r["new"] = new
                r["note"] = (r.get("note") + " · " if r.get("note") else "") + f"target updated {now()[:10]} (URL move)"
        _write_csv(hd / f, rows, fields)
        mdp = hd / f.replace(".csv", ".md")
        if mdp.exists() and "**Progress:**" in mdp.read_text(encoding="utf-8"):
            import handoff
            text = mdp.read_text(encoding="utf-8")
            mdp.write_text(text[:text.index("**Progress:**")] + "\n".join(handoff.table(rows)) + "\n", encoding="utf-8")
    for f in sorted({t["file"] for t in todo if t["kind"] == "blocker-items"}):
        rows, fields = _csv_rows(d / f.replace("build/blockers/", "build/blockers/"))
        for r in rows:
            r["new"] = rewrite_text(r.get("new") or "", allm)[0]
        _write_csv(d / f, rows, fields)
    wh = d / "build" / "link-wheel.json"
    if wh.exists() and any(t["kind"] == "link-wheel" for t in todo):
        wh.write_text(rewrite_text(wh.read_text(encoding="utf-8"), allm)[0], encoding="utf-8")
    st = S.load(slug)
    for items in (st.get("wheel_pending") or {}).values():
        for it in items:
            if path_of(it[2]) in allm:
                it[2] = allm[path_of(it[2])]
    for p in st["pages"].values():
        if p.get("links_placed"):
            p["links_placed"] = [allm.get(path_of(u), u) for u in p["links_placed"]]
    S.save(slug, st)
    if run:
        import subprocess
        for t in todo:
            if t["kind"] == "handoff-done":
                subprocess.run([sys.executable, str(ROOT / "scripts" / "handoff.py"), "retarget", slug, "--run", run, "--ref", t["ref"],
                                "--new", t["new"], "--reason", "the URL it pointed at moved (no chains)"], cwd=ROOT)
    after = _approvals(S.load(slug))
    lost = [k for k, ok in before.items() if ok and not after.get(k)]
    if lost:
        die(f"{slug}: STOP — a URL-move rewrite voided approval(s): {', '.join(lost)}")
    append(d / "log.md", f"\n## MIGRATION · {now()} · URL move: references follow the new URL\n" + "\n".join(r.strip() for r in report) + "\n")
    worklist.build(slug)
    return report


def stale(slug):
    """[(where, message)] for the URL check and the Worklist validator."""
    return [(t["where"], f"points at {t['old']}, which moved to {t['new']} — `urlmoves.py apply {slug}` (or /next) updates it")
            for t in scan(slug)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("check", "apply", "map"):
        s = sub.add_parser(c)
        s.add_argument("slug")
        if c == "apply":
            s.add_argument("--dry", action="store_true")
            s.add_argument("--run")
    a = ap.parse_args()
    if a.cmd == "map":
        mv, dr = moves(a.slug)
        for k, v in sorted(mv.items()):
            print(f"{k} → {v}")
        for k, v in sorted(dr.items()):
            print(f"{k} → {v} (dropped)")
    elif a.cmd == "check":
        bad = stale(a.slug)
        print("\n".join(f"{w}: {m}" for w, m in bad) or "no record points at a moved URL")
        sys.exit(1 if bad else 0)
    else:
        rep = apply(a.slug, a.dry, a.run)
        print(("\n".join(rep) if rep else f"{a.slug}: no record points at a moved URL") + (" (DRY RUN)" if a.dry and rep else ""))


if __name__ == "__main__":
    main()
