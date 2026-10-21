#!/usr/bin/env python3
"""pipeline.py — the inventory, run by script with no agent (Rewrite 4 Phase 1).

    pipeline.py <slug> inventory [--run R] [--phase data|audit|all] [--confirmed] [--dry] [--fanout]
                                 [--cities "A,B,C,D"] [--state ST] [--location "City,ST,United States"]
                                 [--services-file F] [--keyword "GBP name"] [--new-crawl] [--out DIR]

What it replaces: a Haiku clerk running a dozen scripts one by one, and an agent recording each outcome.

  data phase (S05–S08, S19, S21, competitor coverage — the paid pulls; the client has the proof sheet)
    1. crawl (S05) → page text (S05b), reviews (S06), rankings (S07), backlinks (S08), People Also Ask (S19),
       query fan-out (S21, only with --fanout — D6), competitor coverage — each skipped when its data on file is
       under 60 days old (steps.py fresh) or its outcome is already recorded
    2. ONE combined DataforSEO estimate for what is due. Without --confirmed the pipeline stops there (exit 5:
       ask Paul once, then run the same command with --confirmed). With it, the steps run in order; the first
       failure stops the pipeline (exit = that script's; a crawl still running is exit 10 — run it again) and
       nothing after it runs.
    3. every outcome recorded by this script (steps.py record), never by an agent: done · skipped (with the reason)
       · failed (with what went wrong). S09/S10/S11/S20 are recorded only from the files on disk.
       After S06, S19 and S21 the narrow judgment runs on the Claude API (Rewrite 4 Phase 2, scripts/llm.py):
       reviews.py meaning, paa.py route, fanout.py route. No API key → each says so once and leaves the work to its
       agent, as before; nothing fails.
  audit phase (S12: the free, offline part of the audit)
    ingest_evidence.py → crosscheck.py → conformance.py → pagedec.py screen (CM-019 C1–C3, Phase 3) → S12 recorded → the
    Evidence Manifest rendered (render.py). S21 with no --fanout is recorded skipped in the data phase (D6).
    Fills the manifest's tool/date/geography/scope columns from the previous manifest of the same file.

--dry never makes a paid call and writes nothing in the client's folder: it prints the estimate, then runs the audit
phase's free steps into --out (a scratch folder) and compares them with the files the audit already has.
It prints at most ten lines; everything else is in the files.
"""
import argparse
import csv
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

import run as R
import status as S
from lib import ROOT, client_dir, config, die, now

SKILL = ROOT / ".claude" / "skills" / "seo-technical-audit" / "scripts"
MAX_AGE_DAYS = 60
KEEP_COLS = ("tool_settings", "date_window", "geography_device", "scope_limits")


def sh(argv, timeout=None):
    r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def py(*args):
    return ["python3", *args]


def money(out, pattern):
    m = re.search(pattern, out)
    return float(m.group(1)) if m else 0.0


# ------------------------------------------------------------------ the plan (what is due, what it costs)
class Ctx:
    def __init__(self, slug, a):
        self.slug, self.a = slug, a
        self.st = S.load(slug)
        c = self.st["client"]
        self.name, self.domain = c["name"], c["domain"]
        d = client_dir(slug) / "data"
        self.data = d
        self.services = Path(a.services_file) if a.services_file else d / "services.txt"
        cf = d / "cities.txt"
        self.cities = [x.strip() for x in a.cities.split(",") if x.strip()] if a.cities else (
            [x.strip() for x in cf.read_text().splitlines() if x.strip()] if cf.is_file() else [])
        self.state = a.state or c.get("state") or ""
        self.keyword = a.keyword or self.name
        self.location = a.location or (f"{self.cities[0]},{self.state},United States" if self.cities and self.state else "")

    def need(self, what, have):
        if not have:
            die(f"the pipeline needs {what} — pass it, or save it in clients/{self.slug}/data/ (exit 4: nothing was run).", 4)
        return have


def fresh(slug, sid, run_id):
    """True when the step's outcome is Done, reusable and under 60 days old (steps.py fresh)."""
    code, _ = sh(py("scripts/steps.py", "fresh", slug, sid))
    return code == 0


def has(slug, *pats):
    d = client_dir(slug)
    return any(list(d.glob(p)) for p in pats)


def data_steps(x):
    """[(id, label, est_argv|None, est_pattern, run_argv, post_argvs, reuse_when, outputs)] in order."""
    slug, rid = x.slug, x.a.run or "<RUN>"
    sv, cit = str(x.services), ",".join(x.cities)
    st_args = ["--state", x.state] if x.state else []
    steps = [
        ("S05", "site crawl", py("scripts/crawl.py", "estimate", slug, "--domain", x.domain), r"Estimate: up to \$([\d.]+)",
         py("scripts/crawl.py", "run", slug, "--run", rid, "--domain", x.domain, "--confirmed")
         + (["--new-crawl"] if x.a.new_crawl else []), [],
         lambda: has(slug, "inputs/crawl/*internal_all*") and not x.a.new_crawl, ["data/crawl/crawl-summary.csv"]),
        ("S05b", "page text", None, "", py("scripts/crawl.py", "text", slug, "--run", rid), [],
         lambda: has(slug, "data/crawl/page-text.csv"), ["data/crawl/page-text.csv"]),
        ("S06", "reviews", py("scripts/reviews.py", "estimate", slug), r"at most \$([\d.]+)",
         py("scripts/reviews.py", "run", slug, "--run", rid, "--keyword", x.keyword, "--location", x.location,
            "--services-file", sv, "--cities", cit, "--confirmed"),
         [py("scripts/reviews.py", "extract", slug, "--run", rid), py("scripts/reviews.py", "meaning", slug, "--run", rid)],
         lambda: False, ["data/reviews/reviews-summary.md"]),
        ("S07", "rankings", py("scripts/rankings.py", "estimate", slug, "--services-file", sv, "--cities", cit, *st_args),
         r"Total at most \$([\d.]+)", py("scripts/rankings.py", "run", slug, "--run", rid, "--services-file", sv,
                                       "--cities", cit, *st_args, "--confirmed"), [], lambda: False,
         ["data/rankings/rankings-summary.md"]),
        ("S08", "backlinks", py("scripts/dfs.py", "estimate", "backlinks/backlinks/live", "--items", "1000"), r"\$([\d.]+)",
         None, [], lambda: False, ["data/backlinks/backlinks-per-url.csv"]),
        ("S19", "People Also Ask", py("scripts/paa.py", "estimate", slug, "--services-file", sv, "--cities", cit, *st_args),
         r"= \$([\d.]+)", py("scripts/paa.py", "run", slug, "--run", rid, "--services-file", sv, "--cities", cit,
                             *st_args, "--confirmed"), [py("scripts/paa.py", "route", slug, "--run", rid)], lambda: False,
         ["data/paa/paa-routing.md"]),
        ("S21", "query fan-out", py("scripts/fanout.py", "estimate", slug, "--services-file", sv, "--cities", cit),
         r"= \$([\d.]+)", py("scripts/fanout.py", "run", slug, "--run", rid, "--services-file", sv, "--cities", cit,
                             "--paa", f"clients/{slug}/data/paa/paa-questions.csv", "--confirmed"),
         [py("scripts/fanout.py", "route", slug, "--run", rid)], lambda: False,
         ["data/fanout/fanout-routing.md"]),
        ("COMP", "competitor coverage", py("scripts/competitors.py", "estimate", slug, "--keywords-file", sv),
         r"at most \$([\d.]+)", py("scripts/competitors.py", "run", slug, "--run", rid, "--location", x.location,
                                   "--keywords-file", sv, "--confirmed"), [], lambda: has(slug, "data/competitors/coverage.md"),
         ["data/competitors/coverage.md"]),
    ]
    return steps


def backlinks_payload(x):
    p = x.data / "backlinks" / "payload-backlinks-p1.json"
    if not p.is_file():
        p.parent.mkdir(parents=True, exist_ok=True)
        dom = re.sub(r"^https?://(www\.)?", "", x.domain).strip("/")
        p.write_text('[{"target": "%s", "mode": "as_is", "include_subdomains": true, "backlinks_status_type": "live", '
                     '"limit": 1000, "offset": 0, "order_by": ["domain_from_rank,desc"]}]\n' % dom)
    return p


def recent(rec):
    """A recorded Done or Skipped outcome under 60 days old."""
    import datetime
    if not rec or rec.get("outcome") not in ("done", "skipped"):
        return False
    try:
        age = (datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(rec["at"])).days
    except (KeyError, ValueError):
        return False
    return age <= MAX_AGE_DAYS


def due(x):
    """The steps that need a paid or fetching run: not on file, not recorded within 60 days, not left out."""
    out = []
    recorded = x.st.get("audit_steps") or {}
    for sid, label, est, pat, run, post, reuse, outs in data_steps(x):
        if sid == "S21" and not x.a.fanout:
            continue
        off = sid == "S21" and (recorded.get(sid) or {}).get("outcome") == "skipped"   # D6: skipped while off
        if reuse() or (recent(recorded.get(sid)) and not off and not (sid == "S05" and x.a.new_crawl)):
            continue
        out.append((sid, label, est, pat, run, post, outs))
    return out


def estimate(x, todo):
    """Combined estimate: (total, [(id, usd, note)])."""
    rows, total = [], 0.0
    for sid, label, est, pat, run, post, outs in todo:
        if est is None:
            rows.append((sid, 0.0, "free"))
            continue
        code, out = sh(est)
        if "RESUME" in out:
            rows.append((sid, 0.0, "resumes, free"))
            continue
        if code not in (0,):
            die(f"{sid} {label}: the estimate failed (exit {code}): {out.splitlines()[-1] if out else ''}", code or 1)
        usd = money(out, pat)
        total += usd
        rows.append((sid, usd, ""))
    return round(total, 4), rows


# ------------------------------------------------------------------ the data phase
def record(slug, rid, sid, outcome, reason="", outputs=()):
    argv = py("scripts/steps.py", "record", slug, "--run", rid, sid, outcome)
    if reason:
        argv += ["--reason", reason]
    for o in outputs:
        argv += ["--output", o]
    return sh(argv)


def record_from_files(x, rid):
    """S09/S10/S11/S20 outcomes come only from what is on disk (Gwen's uploads, GSC, the SEOPress check)."""
    have = x.st.get("audit_steps") or {}
    spec = {"S09": ("inputs/*citation*", "no citation tracker upload on file yet"),
            "S10": ("inputs/*local-grid*", "no local-grid report on file yet"),
            "S11": ("inputs/*GSC*", "no Search Console / GA4 access on file"),
            "S20": ("inputs/seopress-settings*", "no SEOPress settings check on file (not WordPress, or no access yet)")}
    n = 0
    if "S21" not in have and not x.a.fanout:   # D6: off by default — an outcome, so the audit can still be complete
        record(x.slug, rid, "S21", "skipped", "query fan-out is off by default (D6) — pipeline.py … --fanout runs it")
        n += 1
    for sid, (pat, why) in spec.items():
        if sid in have:
            continue
        hit = sorted(str(p.relative_to(ROOT)) for p in client_dir(x.slug).glob(pat))
        record(x.slug, rid, sid, "done" if hit else "skipped", "" if hit else why, hit[:3])
        n += 1
    return n


def run_data(x, todo, rid, confirmed):
    ran, notes = [], []
    for sid, label, est, pat, run, post, outs in todo:
        if sid == "S08":
            p = backlinks_payload(x)
            raw = f"clients/{x.slug}/data/backlinks/raw/backlinks-{now()[:10]}.json"
            run = py("scripts/dfs.py", "call", x.slug, "backlinks/backlinks/live", "--payload", str(p.relative_to(ROOT)),
                     "--purpose", "S08 backlinks", "--out", raw, "--confirmed")
            post = [py("scripts/backlinks.py", "summary", x.slug)]
        for argv in [run, *post]:
            code, out = sh(argv)
            if code == 10:
                print(f"STILL RUNNING — {sid} {label}: run the same pipeline command again (no new charge).")
                sys.exit(10)
            if code != 0:
                tail = " ".join(out.splitlines()[-2:])[:240]
                if sid == "S06" and "SKIP" in out:   # fewer than 5 reviews: the script says so itself
                    record(x.slug, rid, sid, "skipped", "fewer than 5 Google reviews")
                    notes.append("S06 skipped (<5 reviews)")
                    break
                record(x.slug, rid, sid, "failed", f"{label}: exit {code} — {tail}")
                later = [t[0] for t in todo[[t[0] for t in todo].index(sid) + 1:]]
                print(f"STOPPED at {sid} {label} (exit {code}): {tail}\nNot run: {', '.join(later) or 'nothing'}. "
                      "The outcome is recorded as failed; fix it, then run again.")
                sys.exit(code)
        else:
            if sid in ("S05b", "COMP"):
                if sid == "S05b":
                    record(x.slug, rid, "S05b", "done", "", outs)
            else:
                record(x.slug, rid, sid, "done", "", outs)
            ran.append(sid)
    return ran, notes


# ------------------------------------------------------------------ the audit phase (S12, free and offline)
def audit_dir(x):
    from render import audit_dir as ad
    return ad(x.slug)


def evidence_dir(x):
    """One flat folder of links to every export the audit reads: the crawl tables (inputs/crawl/) and the files the
    team uploaded (inputs/), as the Drive Evidence folder always was. ingest_evidence.py reads one folder, not a tree."""
    d = Path(tempfile.mkdtemp(prefix=f"evidence-{x.slug}-"))
    base = client_dir(x.slug) / "inputs"
    for f in sorted(list(base.glob("*.*")) + list((base / "crawl").glob("*.*"))):
        if f.is_file() and not (d / f.name).exists():
            (d / f.name).symlink_to(f.resolve())
    return d


def s12(x, out_dir):
    """ingest -> crosscheck into out_dir. Returns ((exit, output), (exit, output))."""
    ev = str(evidence_dir(x))
    out_dir.mkdir(parents=True, exist_ok=True)
    c1, o1 = sh(py(str(SKILL / "ingest_evidence.py"), ev, str(out_dir), "--client-dir", f"clients/{x.slug}"))
    c2, o2 = sh(py(str(SKILL / "crosscheck.py"), ev, str(out_dir), "--client-dir", f"clients/{x.slug}"))
    return (c1, o1), (c2, o2)


def carry_columns(prev, new):
    """Keep what the audit already wrote for a file that is unchanged (same hash): the four setting columns, and the
    recognised type where the header signature could not name it (a hand-typed MANUAL export)."""
    if not (prev.is_file() and new.is_file()):
        return 0
    with open(prev, newline="", encoding="utf-8-sig") as fh:
        old = {r["file"]: r for r in csv.DictReader(fh)}
    with open(new, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        cols, rows = rd.fieldnames, list(rd)
    n = 0
    for r in rows:
        o = old.get(r["file"])
        if not (o and o.get("sha256_12") == r.get("sha256_12")):
            continue
        for c in KEEP_COLS:
            if c in r and not r[c] and o.get(c):
                r[c], n = o[c], n + 1
        if r.get("recognised_as") == "UNRECOGNISED" and o.get("recognised_as") not in ("", "UNRECOGNISED", None):
            r["recognised_as"], n = o["recognised_as"], n + 1
    with open(new, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return n


def compare(existing, fresh_dir):
    """Short lines: do the free steps reproduce the files the audit already has?"""
    lines = []
    pm, nm = existing / "00-manifest.csv", fresh_dir / "00-manifest.csv"
    if pm.is_file() and nm.is_file():
        def key(p):
            with open(p, newline="", encoding="utf-8-sig") as fh:
                return {r["file"]: (r["recognised_as"], r["rows"], r["sha256_12"]) for r in csv.DictReader(fh)}
        a, b = key(pm), key(nm)
        same = sum(1 for f, v in a.items() if b.get(f) == v)
        lines.append(f"manifest: {same} of the audit's {len(a)} files reproduced identically (type, rows, hash)"
                     + (f"; {len(set(b) - set(a))} on file now that the audit did not list, {len([f for f in a if f not in b])} "
                        "it lists that the script cannot find (hand-added rows or files that moved)" if set(a) ^ set(b) else ""))
    pc, nc = existing / "00-crosschecks.md", fresh_dir / "00-crosschecks.md"
    if pc.is_file() and nc.is_file():
        tag = lambda p: sorted(re.findall(r"\[(CONTRADICTED|CONFIRMED|UNVERIFIED|LIMITATION)\] ([^\n]+)", p.read_text(encoding="utf-8")))
        a, b = tag(pc), tag(nc)
        lines.append("cross-checks: identical (%d checks)" % len(b) if a == b else
                     f"cross-checks: {len(set(a) ^ set(b))} check line(s) differ of {len(b)}")
    pu, nu = existing / "inventories" / "urls.csv", fresh_dir / "inventories" / "urls.csv"
    if pu.is_file() and nu.is_file():
        ln = lambda p: sum(1 for _ in open(p, encoding="utf-8-sig")) - 1
        lines.append(f"url inventory: {ln(nu)} URLs (the audit has {ln(pu)})")
    return lines


def run_audit(x, rid):
    ad = audit_dir(x)
    if ad is None:
        c, o = sh(py(str(SKILL / "init_audit.py"), x.slug, "clients"))
        ad = audit_dir(x)
        if ad is None:
            die(f"the audit folder could not be created: {o[:200]}", 1)
    prev = ad / "00-manifest.csv"
    keep = Path(tempfile.mkdtemp(prefix="manifest-prev-")) / "m.csv"
    if prev.is_file():
        keep.write_bytes(prev.read_bytes())
    (c1, o1), (c2, o2) = s12(x, ad)
    if c1 or c2:
        record(x.slug, rid, "S12", "failed", f"ingest exit {c1}, cross-checks exit {c2}: {(o1 + o2)[-200:]}")
        print(f"STOPPED at S12: ingest exit {c1}, cross-checks exit {c2}\n{(o1 + chr(10) + o2)[-300:]}")
        sys.exit(c1 or c2)
    kept = carry_columns(keep, ad / "00-manifest.csv")
    c3, o3 = sh(py("scripts/conformance.py", x.slug))
    if c3:
        record(x.slug, rid, "S12", "failed", f"conformance exit {c3}: {o3[-200:]}")
        print(f"STOPPED at conformance (exit {c3}): {o3[-300:]}")
        sys.exit(c3)
    c4, o4 = sh(py("scripts/pagedec.py", "screen", x.slug) + (["--run", rid] if rid else []))   # Phase 3: CM-019 C1–C3
    if c4:
        record(x.slug, rid, "S12", "failed", f"redirect screen exit {c4}: {o4[-200:]}")
        print(f"STOPPED at the redirect screen (exit {c4}): {o4[-300:]}")
        sys.exit(c4)
    record(x.slug, rid, "S12", "done", "", [str((ad / f).relative_to(ROOT)) for f in ("00-manifest.csv", "00-crosschecks.md",
                                                                                      "redirect-screen.csv")])
    import render
    try:
        p, _ = render.render_one(x.slug, "manifest", rid)
        shown = f"{p.name} rendered"
    except SystemExit as e:
        shown = "Evidence Manifest left as it is (covered by an approval)" if e.code == 4 else "Evidence Manifest not rendered"
    bad = len(re.findall(r"\[CONTRADICTED\]", (ad / "00-crosschecks.md").read_text(encoding="utf-8")))
    return [f"S12 done: manifest + cross-checks ({bad} contradicted) + conformance + redirect screen in {ad.relative_to(ROOT)}"
            + (f"; kept {kept} setting cell(s)" if kept else ""), shown]


# ------------------------------------------------------------------ main
def inventory(a):
    if not a.run and not a.dry:
        die("--run <RUN_ID> is required (start a run first: run.py start <slug> discovery --step data) — or use --dry.", 2)
    if a.run:
        R.open_run(a.slug, a.run)
    x = Ctx(a.slug, a)
    phase = a.phase
    if not phase:
        step = ((x.st.get("open_runs") or {}).get(a.run) or {}).get("step", "") if a.run else ""
        phase = "audit" if step == "discovery:audit" else "all" if a.dry else "data"
    lines = []
    todo = []
    if phase in ("data", "all"):
        for what, have in (("a services file (data/services.txt)", x.services.is_file()),
                           ("--cities (or data/cities.txt)", bool(x.cities)),
                           ("--state (or the client's state)", bool(x.state))):
            if not a.dry:
                x.need(what, have)
        todo = due(x) if (x.cities and x.state and x.services.is_file()) or not a.dry else []
        try:
            total, rows = estimate(x, todo) if todo else (0.0, [])
        except SystemExit:
            if not a.dry:
                raise
            total, rows = 0.0, [(t[0], 0.0, "no estimate on this Mac") for t in todo]
        thr = float(config()["dfs_confirm_threshold_usd"])
        lines.append(f"inventory {a.slug}: " + (", ".join(f"{s} ${u:.2f}" if u else f"{s} free" for s, u, _ in rows) if rows else
                                               ("nothing to pull — every step is on file and under 60 days old" if not a.dry or (x.cities and x.state and x.services.is_file())
                                                 else "paid steps not estimated (no cities or state on file — pass --cities and --state)"))
                     + (f" · DataforSEO total ≈ ${total:.2f}" + (f" (over ${thr:.0f}: Paul's yes needed)" if total > thr else "")
                        if rows else ""))
        if todo and not a.dry and not a.confirmed:
            print("\n".join(lines))
            print("CONFIRM — ask Paul once for this total, then run the same command with --confirmed (exit 5).")
            sys.exit(5)
    if a.dry:
        out = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix=f"pipeline-dry-{a.slug}-"))
        (c1, o1), (c2, o2) = s12(x, out)
        lines.append(f"dry run: no paid call, nothing written in clients/{a.slug}/ — S12 free steps into {out}")
        ad = audit_dir(x)
        lines += compare(ad, out) if ad else [f"manifest + cross-checks written ({'ok' if not (c1 or c2) else 'FAILED'})"]
        print("\n".join(lines[:10]))
        sys.exit(1 if (c1 or c2) else 0)
    if phase in ("data", "all"):
        ran, notes = run_data(x, todo, a.run, a.confirmed) if todo else ([], [])
        n = record_from_files(Ctx(a.slug, a), a.run)
        lines.append(f"data: ran {', '.join(ran) or 'nothing'}" + (f" · {'; '.join(notes)}" if notes else "")
                     + (f" · S09/S10/S11/S20 recorded from the files on disk ({n})" if n else ""))
    if phase in ("audit", "all"):
        lines += run_audit(Ctx(a.slug, a), a.run)
    print("\n".join(lines[:10]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("what", choices=["inventory"])
    ap.add_argument("--run")
    ap.add_argument("--phase", choices=["data", "audit", "all"])
    ap.add_argument("--confirmed", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--fanout", action="store_true", help="also run S21 query fan-out (D6: off by default)")
    ap.add_argument("--cities")
    ap.add_argument("--state")
    ap.add_argument("--location")
    ap.add_argument("--services-file")
    ap.add_argument("--keyword")
    ap.add_argument("--new-crawl", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    inventory(a)


if __name__ == "__main__":
    main()
