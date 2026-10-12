#!/usr/bin/env python3
"""h1lock.py — the numbers behind a homepage H1 lock decision (CM-059; CR-002, Paul 2026-10-12).

    h1lock.py check <slug> --keyword K --hp06 pass|fail [--gsc FILE] [--h1 TEXT]
        prints the proposal block for Paul: the live H1, HP-06, the homepage's organic and local-pack positions for its
        main keyword (data/rankings/ranked-keywords.csv), its 90-day Search Console clicks for it (a GSC queries
        export, filtered to the homepage), the thresholds (config.json h1_lock_lift) and which conditions hold.
        Read-only. It never lifts the lock: all three conditions met means "put it to Paul", nothing more.
    h1lock.py followup <slug> --run R --keyword K --old-h1 TEXT --changed YYYY-MM-DD [--gsc FILE]
        the day the new H1 is live: one Manual lookups row on the VA Worklist (handoff.py, kind manual_lookup) for the
        30-day check — organic position and 90-day clicks against today's baseline, with the old H1 for rollback.

Exit codes: 0 printed · 1 bad input. An unknown number is shown as [NEED: …] and counts as not met (CM-016).
"""
import argparse
import csv
import datetime as dt
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import status as S
from lib import ROOT, client_dir, config, die


def thresholds():
    t = config().get("h1_lock_lift") or {}
    return {"rank_top_n": int(t.get("rank_top_n", 10)), "few_clicks_90d": int(t.get("few_clicks_90d", 10)),
            "followup_days": int(t.get("followup_days", 30))}


def is_home(url, domain):
    u = urlparse(url if "://" in url else "https://" + url)
    host = (u.hostname or "").lower().removeprefix("www.")
    return host == domain.lower().removeprefix("www.") and u.path in ("", "/")


def domain_of(slug):
    d = (S.load(slug).get("client") or {}).get("domain") or die(f"{slug}: no domain in status.json")
    return d.replace("https://", "").replace("http://", "").strip("/")


def positions(slug, keyword, domain):
    """{'organic': n|None, 'local_pack': n|None, 'volume': v|None, 'file': rel|None} for the homepage and keyword."""
    f = client_dir(slug) / "data" / "rankings" / "ranked-keywords.csv"
    out = {"organic": None, "local_pack": None, "volume": None, "file": None}
    if not f.is_file():
        return out
    out["file"] = str(f.relative_to(ROOT))
    with f.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r.get("keyword", "").strip().lower() != keyword.lower() or not is_home(r.get("url", ""), domain):
                continue
            kind = "local_pack" if "local" in (r.get("type") or "") else "organic"
            pos = int(float(r["position"])) if (r.get("position") or "").strip() else None
            if pos is not None and (out[kind] is None or pos < out[kind]):
                out[kind] = pos
            out["volume"] = r.get("volume") or out["volume"]
    return out


def gsc_clicks(path, keyword, domain):
    """Clicks for the keyword in a Search Console queries export (rows for other pages are skipped). None = not there."""
    if not path:
        return None
    p = Path(path) if Path(path).is_absolute() else ROOT / path
    if not p.is_file():
        die(f"{path} not found")
    with p.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return 0
    cols = {c.strip().lower(): c for c in rows[0]}
    qc = next((cols[c] for c in ("top queries", "query", "queries") if c in cols), None)
    cc = cols.get("clicks")
    pc = next((cols[c] for c in ("page", "top pages", "landing page") if c in cols), None)
    if not qc or not cc:
        die(f"{path}: needs a query column (Top queries / Query) and a Clicks column")
    n = 0
    for r in rows:
        if r[qc].strip().lower() == keyword.lower() and (not pc or is_home(r[pc], domain)):
            n += int(float((r[cc] or "0").replace(",", "")))
    return n


def live_h1(slug, domain):
    for f in sorted((client_dir(slug) / "inputs" / "crawl").glob("* - SF - internal_all - *.csv"), reverse=True):
        with f.open(newline="", encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                if is_home(r.get("Address", ""), domain):
                    return r.get("H1-1") or "", f.name
    return None, None


def evaluate(hp06, pos, clicks, t):
    """[(condition, 'met'|'not met'|'unknown', why)] and the verdict."""
    org = pos["organic"]
    conds = [
        ("a. the live H1 fails HP-06", "met" if hp06 == "fail" else "not met", f"HP-06: {hp06}"),
        (f"b. not in the organic top {t['rank_top_n']}",
         "unknown" if org is None and not pos["file"] else ("met" if org is None or org > t["rank_top_n"] else "not met"),
         ("[NEED: rankings — data/rankings/ranked-keywords.csv]" if not pos["file"] else
          f"organic #{org}" if org else "not in the top 100 for this keyword")
         + (f" · local pack #{pos['local_pack']} (shown, not counted)" if pos["local_pack"] else "")),
        (f"c. fewer than {t['few_clicks_90d']} Search Console clicks in 90 days",
         "unknown" if clicks is None else ("met" if clicks < t["few_clicks_90d"] else "not met"),
         "[NEED: Search Console queries export for the homepage, last 90 days]" if clicks is None else f"{clicks} clicks"),
    ]
    states = [c[1] for c in conds]
    if all(s == "met" for s in states):
        verdict = "ALL THREE MET — this may be put to Paul as a decision. Nothing changes unless he says so (CM-059)."
    elif "not met" in states:
        verdict = "LOCK HOLDS — " + "; ".join(c[0] for c in conds if c[1] == "not met") + " is not met."
    else:
        verdict = "CANNOT TELL YET — the lock holds until the missing numbers are in: " + \
                  "; ".join(c[2] for c in conds if c[1] == "unknown")
    return conds, verdict


def check(a):
    domain = domain_of(a.slug)
    t = thresholds()
    h1, src = (a.h1, "given") if a.h1 else live_h1(a.slug, domain)
    pos = positions(a.slug, a.keyword, domain)
    clicks = gsc_clicks(a.gsc, a.keyword, domain)
    conds, verdict = evaluate(a.hp06, pos, clicks, t)
    print(f"## Homepage H1 lock — {a.slug} (CM-059)\n")
    print(f"- Live H1: \"{h1}\" ({src})" if h1 is not None else "- Live H1: [NEED: crawl internal_all or --h1]")
    print(f"- Main keyword: \"{a.keyword}\"" + (f" (volume {pos['volume']})" if pos["volume"] else ""))
    print(f"- Thresholds (config.json h1_lock_lift): organic top {t['rank_top_n']}; few = under {t['few_clicks_90d']} "
          f"clicks in 90 days")
    print(f"- Sources: {pos['file'] or '[NEED: rankings]'}" + (f"; {a.gsc}" if a.gsc else "; Search Console: none given"))
    print("\n| Condition | State | Numbers |\n|---|---|---|")
    for c in conds:
        print(f"| {c[0]} | {c[1]} | {c[2]} |")
    print(f"\n**{verdict}**")
    return 0


def followup(a):
    domain = domain_of(a.slug)
    t = thresholds()
    try:
        changed = dt.date.fromisoformat(a.changed)
    except ValueError:
        die("--changed must be YYYY-MM-DD (the day the new H1 went live)")
    due = changed + dt.timedelta(days=t["followup_days"])
    pos = positions(a.slug, a.keyword, domain)
    clicks = gsc_clicks(a.gsc, a.keyword, domain)
    base = (f"organic #{pos['organic']}" if pos["organic"] else "organic: not in the top 100") \
        + (f" · {clicks} clicks (90 days)" if clicks is not None else " · clicks: [NEED: GSC baseline]")
    row = {"url": f"https://{domain}/", "field": "H1 30-day check",
           "old": f"H1 before {a.changed}: \"{a.old_h1}\" · baseline {base}",
           "new": f"on {due}: organic position and 90-day Search Console clicks for \"{a.keyword}\"",
           "reason": f"CM-059: the homepage H1 changed on {a.changed}. Record both numbers in note; if both are worse "
                     "than the baseline, Paul decides whether to roll back to the old H1.",
           "decision_map_ref": "CM-059 homepage H1"}
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row))
        w.writeheader(); w.writerow(row)
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "handoff.py"), "create", a.slug, "--run", a.run,
                        "--kind", "manual_lookup", "--items", fh.name, "--title", "Homepage H1 — 30-day check"],
                       capture_output=True, text=True)
    Path(fh.name).unlink(missing_ok=True)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("check"); s.add_argument("slug"); s.add_argument("--keyword", required=True)
    s.add_argument("--hp06", required=True, choices=["pass", "fail"]); s.add_argument("--gsc"); s.add_argument("--h1")
    s = sub.add_parser("followup"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--keyword", required=True); s.add_argument("--old-h1", required=True)
    s.add_argument("--changed", required=True); s.add_argument("--gsc")
    a = ap.parse_args()
    sys.exit(check(a) if a.cmd == "check" else followup(a))


if __name__ == "__main__":
    main()
