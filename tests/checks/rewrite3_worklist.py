"""Rewrite 3 §7a: the VA Worklist is accurate and detailed, and a bad one is refused before any handover."""
import csv
import json

S_FILE = "status" + ".json"
TITLE = "Roof Repair - Wl Co - Bluffton, South Carolina"
META = ("Roof repair in Bluffton and Hilton Head from Wl Co: leaks, storm damage and flashing fixed fast. Call us "
        "today for a free on-site inspection.")[:155].ljust(155, ".")
HEAD = "page_id: {pid}\nurl: {url}\nseo_title: {title}\nmeta_description: {meta}"


def _client(h, slug="r3wl-co"):
    h.sh(f'python3 scripts/status.py init {slug} --name "Wl Co" --domain r3wl.example --type full --industry roofing')
    d = h.SB / "clients" / slug
    sp = d / S_FILE
    st = json.loads(sp.read_text())
    pages = {}
    for pid, wid, typ, url, name in (("svc-a", 11, "service", "https://r3wl.example/roof-repair/", "Roof Repair"),
                                     ("loc-b", 12, "location", "https://r3wl.example/bluffton/", "Bluffton")):
        f = d / "build" / f"SD - {name}.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"---\n{HEAD.format(pid=pid, url=url, title=TITLE, meta=META)}\n---\n# {name}\n\nBody.\n")
        pages[pid] = {"type": typ, "name": name, "url": url, "wp_id": wid, "state": "handed_off",
                      "file": f"clients/{slug}/build/{f.name}"}
    st["pages"] = pages
    st["publish_handoff"] = {"id": "H-2026-10-14-01-publish", "at": "2026-10-14", "run": "x", "batches": []}
    sp.write_text(json.dumps(st))
    return d, sp


def _group(d, rows, name="H-2026-10-14-01-publish.csv"):
    cols = ["ref", "url", "field", "old", "new", "reason", "decision_map_ref", "status", "note"]
    with open(d / "handoffs" / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({"status": "issued", "note": "", "reason": "x", **r})


def _pub(n, pid, wid, new):
    return {"ref": f"H-2026-10-14-01-publish-{n:02d}", "url": f"https://r3wl.example/?page_id={wid}", "field": "publish",
            "old": "(draft)", "new": new, "decision_map_ref": pid}


def _r301(n, old, new, pid="svc-a"):
    return {"ref": f"H-2026-10-14-01-publish-{n:02d}", "url": old, "field": "301", "old": old, "new": new,
            "decision_map_ref": pid}


def _check(h, slug="r3wl-co"):
    return h.sh(f"python3 tests/fakes.py worklist check {slug} --report-only")


def t_worklist_fields_and_validator(h):
    d, sp = _client(h)
    (d / "handoffs").mkdir(exist_ok=True)
    good = [_pub(1, "svc-a", 11, "https://r3wl.example/roof-repair/"), _pub(2, "loc-b", 12, "https://r3wl.example/bluffton/"),
            _r301(3, "https://r3wl.example/old-a/", "https://r3wl.example/roof-repair/")]
    _group(d, good)
    code, out = _check(h)
    h.check("§7a: a clean worklist passes the validator", code == 0 and "0 error(s)" in out, out)
    h.sh("python3 scripts/worklist.py build r3wl-co")
    rows = list(csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8")))
    by = {r["id"]: r for r in rows}
    pub, red = by["H-2026-10-14-01-publish-01"], by["H-2026-10-14-01-publish-03"]
    h.check("§7a: every row carries id, section, task, where, how, values, depends_on, done_check, owner, source, status",
            all(r[k] for r in rows for k in ("id", "section", "task", "where", "how", "values", "done_check", "owner", "source", "status")),
            rows[0])
    h.check("§7a: where holds the live URL and the WordPress edit link; how is numbered steps",
            "https://r3wl.example/roof-repair/" in pub["where"] and "/wp-admin/post.php?post=11&action=edit" in pub["where"]
            and pub["how"].startswith("1. ") and " 2. " in pub["how"], pub)
    h.check("§7a: values hold exactly what to enter (slug, URL, SEOPress title, meta description); a redirect holds from → to",
            "slug: roof-repair" in pub["values"] and TITLE in pub["values"] and META in pub["values"]
            and "from: https://r3wl.example/old-a/ → to: https://r3wl.example/roof-repair/" in red["values"], (pub, red))
    h.check("§7a: a redirect depends on its target's publish row; status starts open; done_check says how to confirm",
            red["depends_on"] == "H-2026-10-14-01-publish-01" and red["status"] == "open" and "returns 301" in red["done_check"]
            and "loads (200)" in pub["done_check"], red)
    order = [r["id"] for r in rows]
    h.check("§7a: rows are in dependency order inside each section", order.index(red["id"]) > order.index(pub["id"]), order)
    md = (d / "handoffs" / "VA-WORKLIST.md").read_text(encoding="utf-8")
    h.check("§7a: the handover document has a cover (what it is, the order, who owns what, how to tick) then one section per type",
            "## Start here" in md and "How to tick a row" in md and "Who owns what" in md and "## 4 · Publish" in md
            and md.index("## Start here") < md.index("## 4 · Publish"), md[:600])

    def bad(name, rows_, expect, absent=None):
        _group(d, rows_)
        code, out = _check(h)
        report = (d / "handoffs" / "worklist-check.md").read_text(encoding="utf-8")
        h.check(f"§7a: validator refuses — {name}", code == 4 and all(e in report for e in expect)
                and not any(a in report for a in (absent or [])), (out, report))

    bad("a wrong slug", [_pub(1, "svc-a", 11, "https://r3wl.example/roof-repairs/"), good[1], good[2]],
        ["is not the approved site-plan URL"])
    bad("a missing publish row", [good[0], good[2]], ["loc-b (https://r3wl.example/bluffton/) is a draft with no publish row"])
    bad("a page appearing twice", good + [_pub(4, "loc-b", 12, "https://r3wl.example/bluffton/")], ["loc-b appears twice"])
    bad("a wrong WordPress draft id", [_pub(1, "svc-a", 99, "https://r3wl.example/roof-repair/"), good[1], good[2]],
        ["is not the WordPress draft of svc-a"])
    bad("a redirect chain", good + [_r301(4, "https://r3wl.example/old-c/", "https://r3wl.example/old-a/")], ["chain: https://r3wl.example/old-a/"])
    bad("a loop", good[:2] + [_r301(3, "https://r3wl.example/old-x/", "https://r3wl.example/old-y/"),
                              _r301(4, "https://r3wl.example/old-y/", "https://r3wl.example/old-x/")], ["(a loop)"])
    bad("two rows for one old URL", good + [_r301(4, "https://r3wl.example/old-a/", "https://r3wl.example/bluffton/", "loc-b")],
        ["is redirected by two rows"])
    bad("an old URL that is gone and not recorded as gone",
        good[:2] + [_r301(3, "https://r3wl.example/never-existed/", "https://r3wl.example/roof-repair/")],
        ["answers 404 and is not recorded as already gone"])
    bad("a redirect whose target is no longer a planned page (a stale row)",
        good[:2] + [_r301(3, "https://r3wl.example/old-a/", "https://r3wl.example/roof-repair-sc-2/")],
        ["no longer a planned page"])
    st = json.loads(sp.read_text())
    st["pages"]["svc-a"]["open_items"] = [{"line": 5, "text": "[NEED: cited lifespan]"}]
    sp.write_text(json.dumps(st))
    bad("an open-item notice with no row", good, ["svc-a has an open item with no row"])
    st["pages"]["svc-a"]["open_items"] = []
    sp.write_text(json.dumps(st))
    _group(d, good + [{"ref": "H-2026-10-14-01-publish-04", "url": "https://r3wl.example/?page_id=11", "field": "open item",
                       "old": "[NEED: cited lifespan]", "new": "find it", "decision_map_ref": "svc-a"}])
    code, out = _check(h)
    report = (d / "handoffs" / "worklist-check.md").read_text(encoding="utf-8")
    h.check("§7a: validator refuses an open-item row whose page no longer has the notice",
            code == 4 and "no longer has this notice" in report, report)
    h.sh("python3 scripts/worklist.py supersede r3wl-co H-2026-10-14-01-publish-04 --by none --reason 'notice resolved'")
    code, out = _check(h)
    rows = list(csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8")))
    sup = next(r for r in rows if r["id"].endswith("-04"))
    h.check("§7a: a superseded row is marked superseded (with its reason), never left open, and no longer fails the check",
            code == 0 and sup["status"] == "superseded" and "notice resolved" in sup["note"], (out, sup))
    _group(d, good)
    code, out = h.sh("python3 tests/fakes.py worklist check r3wl-co")
    code2, out2 = h.sh("python3 scripts/worklist.py build r3wl-co")
    h.check("§7a: a passing check is recorded for these rows (the Drive copy depends on it)",
            code == 0 and json.loads(sp.read_text())["worklist_check"]["ok"] is True, out)
    pinned = {r["id"]: r["status"] for r in csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8"))}
    h.check("§7a: the handover document and CSV exist for the VA only as generated, with status open", set(pinned.values()) == {"open"}, pinned)


def t_worklist_verify_reopens(h):
    S = "r3wlv-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Wlv Co" --domain r3wl.example --type full --industry roofing')
    d = h.SB / "clients" / S
    (d / "handoffs").mkdir(exist_ok=True)
    ref = "H-2026-10-14-01-redirect-01"
    _group(d, [{"ref": ref, "url": "https://r3wl.example/gone-old/", "field": "301", "old": "https://r3wl.example/gone-old/",
                "new": "https://r3wl.example/new/", "decision_map_ref": "", "status": "done"}], "H-2026-10-14-01-redirect.csv")
    ag = h.Agent(S)
    rid = ag.start("new-client")
    h.sh(f"python3 scripts/run.py change {S} {rid} --kind redirect --url https://r3wl.example/gone-old/ --field 301 "
         f"--old 'x' --new https://r3wl.example/new/ --result 'HANDOFF ISSUED' --channel handoff --ref {ref}")
    code, out = h.sh(f"python3 tests/fakes.py verify {S} --run {rid} --handoff H-2026-10-14-01-redirect")
    row = next(csv.DictReader(open(d / "handoffs" / "H-2026-10-14-01-redirect.csv", newline="", encoding="utf-8")))
    h.check("§7a: a done row whose done_check fails comes back as open, with the reason",
            "1 done row(s) reopened" in out and row["status"] == "issued" and "reopened by /verify" in row["note"]
            and "answers 404" in row["note"], (out, row))
    h.sh(f'python3 scripts/run.py abort {S} {rid} --reason "test"')


SCENARIOS = [t_worklist_fields_and_validator, t_worklist_verify_reopens]
