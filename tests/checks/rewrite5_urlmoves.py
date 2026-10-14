"""Fix set 2026-10-14: a URL moved — every record that pointed at the old URL follows it, and no redirect chain results
(HMM: /services/straight-stair-lifts/ "consolidated into /services/stair-lifts/", which moved to /stair-lifts/)."""
import csv
import json

S_FILE = "status" + ".json"
D = "https://r3wl.example"
BG = """# Um Co - Brand Guide

## Section A — Entity foundation
| Fact | Value |
|---|---|
| Old page evidence | /services/stair-lifts/ (live today) |

## Section C — Page inventory

### C1 · Service pages
| URL | Service name | H1 service variant | Status |
|---|---|---|---|
| /services/ | Services hub | | Planned (rewrite) |
| /services/stair-lifts/ | Stair lifts — parent; straight stair lifts consolidated in | | Planned (rewrite) |
| /services/straight-stair-lifts/ | → consolidated into /services/stair-lifts/ (301 after the CM-019 check) | | Planned |
| /roof-repair/ | Roof repair; the live URL /services/stair-lifts/ is 301'd at publish | | Planned |

## Section D — Verified facts
Source page: /services/stair-lifts/
"""
HEAD = ["ref", "url", "field", "old", "new", "reason", "decision_map_ref", "status", "note"]


def _csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=HEAD)
        w.writeheader()
        for r in rows:
            w.writerow({"status": "issued", "note": "", "reason": "x", "decision_map_ref": "svc-stair", **r})


def t_urlmoves_follow_and_no_chains(h):
    h.sh('python3 scripts/status.py init um-co --name "Um Co" --domain r3wl.example --type full --industry roofing')
    d = h.SB / "clients" / "um-co"
    sp = d / S_FILE
    st = json.loads(sp.read_text())
    st["pages"] = {
        "svc-stair": {"type": "service", "name": "Stair Lifts", "url": f"{D}/stair-lifts/", "wp_id": 11, "state": "handed_off",
                      "live_url": f"{D}/services/stair-lifts/", "replaces": [f"{D}/services/stair-lifts/"],
                      "links_placed": [f"{D}/services/stair-lifts/"]}}
    st["wheel_pending"] = {"svc-stair": [["services", "Stair lifts", f"{D}/services/stair-lifts/", "svc-stair"]]}
    sp.write_text(json.dumps(st))
    (d / "brand-guide.md").write_text(BG, encoding="utf-8")
    (d / "build" / "blockers").mkdir(parents=True, exist_ok=True)
    (d / "handoffs").mkdir(exist_ok=True)
    row301 = {"ref": "H-2026-10-14-01-redirect-01", "url": f"{D}/services/straight-stair-lifts/", "field": "301",
              "old": f"{D}/services/straight-stair-lifts/", "new": f"{D}/services/stair-lifts/"}
    fix = {"ref": "H-2026-10-14-01-redirect-02", "url": f"{D}/about/", "field": "internal links",
           "old": "links to a redirecting URL", "new": f"{D}/old-a/ -> {D}/services/stair-lifts/"}
    _csv(d / "handoffs" / "H-2026-10-14-01-redirect.csv", [row301, fix])
    _csv(d / "build" / "blockers" / "redirect-items.csv", [{"ref": "b1", "url": f"{D}/old-a/", "field": "301", "old": "",
                                                           "new": f"{D}/services/stair-lifts/"}])

    code, out = h.sh("python3 tests/fakes.py worklist check um-co --report-only")
    rep = (d / "handoffs" / "worklist-check.md").read_text(encoding="utf-8")
    h.check("urlmoves: the Worklist validator refuses a 301 whose target itself redirects (the straight-stair-lifts case), "
            "naming the final URL", code == 4 and "chain: target https://r3wl.example/services/stair-lifts/ is itself redirected" in rep
            and "to https://r3wl.example/stair-lifts/" in rep, rep)
    code, out = h.sh("python3 scripts/urlcheck.py refs um-co")
    h.check("urlmoves: the URL check lists every record that points at the moved URL — Brand Guide Section C, open handoff rows, "
            "blocker items, wheel_pending, links_placed — and nothing else",
            code == 1 and "brand-guide.md:" in out and "H-2026-10-14-01-redirect-01" in out and "H-2026-10-14-01-redirect-02" in out
            and "redirect-items.csv" in out and "wheel_pending" in out and "links_placed" in out
            and out.count("brand-guide.md:") == 2, out)

    bg0 = (d / "brand-guide.md").read_text(encoding="utf-8")
    code, out = h.sh("python3 scripts/urlmoves.py apply um-co --dry")
    h.check("urlmoves: --dry reports and writes nothing", "DRY RUN" in out and (d / "brand-guide.md").read_text(encoding="utf-8") == bg0
            and json.loads(sp.read_text())["wheel_pending"]["svc-stair"][0][2].endswith("/services/stair-lifts/"), out)
    code, out = h.sh("python3 scripts/urlmoves.py apply um-co")
    bg = (d / "brand-guide.md").read_text(encoding="utf-8")
    rows = list(csv.DictReader(open(d / "handoffs" / "H-2026-10-14-01-redirect.csv", newline="", encoding="utf-8")))
    st = json.loads(sp.read_text())
    h.check("urlmoves: the Brand Guide page row and the 'consolidated into' target follow the move; the retired URL itself stays",
            "| /stair-lifts/ | Stair lifts" in bg and "| /services/straight-stair-lifts/ | → consolidated into /stair-lifts/ (301" in bg
            and "| /services/ | Services hub | | Planned (rewrite) |" in bg, bg)
    h.check("urlmoves: what is live today is not rewritten ('live URL … is 301'd', Sections A and D)",
            "the live URL /services/stair-lifts/ is 301'd" in bg and "(live today)" in bg and "Source page: /services/stair-lifts/" in bg, bg)
    h.check("urlmoves: the 301's target and the link fix's new side point at the final URL; the old side of a pair stays",
            rows[0]["new"] == f"{D}/stair-lifts/" and rows[0]["url"] == f"{D}/services/straight-stair-lifts/"
            and rows[1]["new"] == f"{D}/old-a/ -> {D}/stair-lifts/" and "(URL move)" in rows[0]["note"], rows)
    h.check("urlmoves: blocker items, wheel_pending and links_placed follow too",
            "/stair-lifts/" in (d / "build" / "blockers" / "redirect-items.csv").read_text() and "/services/" not in
            (d / "build" / "blockers" / "redirect-items.csv").read_text()
            and st["wheel_pending"]["svc-stair"][0][2] == f"{D}/stair-lifts/" and st["pages"]["svc-stair"]["links_placed"] == [f"{D}/stair-lifts/"], st)
    h.check("urlmoves: it logs a MIGRATION line, and a second apply changes nothing",
            "URL move: references follow the new URL" in (d / "log.md").read_text(encoding="utf-8")
            and "no record points at a moved URL" in h.sh("python3 scripts/urlmoves.py apply um-co")[1]
            and h.sh("python3 scripts/urlcheck.py refs um-co")[0] == 0)
    code, out = h.sh("python3 tests/fakes.py worklist check um-co --report-only")
    rep = (d / "handoffs" / "worklist-check.md").read_text(encoding="utf-8")
    h.check("urlmoves: after the move the chain error is gone", "chain:" not in rep and "which moved to" not in rep, rep)


SCENARIOS = [t_urlmoves_follow_and_no_chains]
