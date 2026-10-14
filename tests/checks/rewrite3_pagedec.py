"""Rewrite 3 §7a: page decisions (drop, hold, stale drafts, a reworded open item) become records the Worklist follows;
open items split into VA tasks, the researcher's gaps and the client's questions."""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rewrite3_worklist import S_FILE, _check, _group, META, TITLE   # noqa: E402

D = "https://r3wl.example"
MAP = "[NEED: city-level map embed of {} — not the Google Business Profile map]"


def _page_file(d, name, extra=""):
    f = d / "build" / f"LD - {name}.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f"---\npage_id: x\nurl: {D}/{name.lower()}/\nseo_title: {TITLE}\nmeta_description: {META}\n---\n# {name}\n\n"
                 f"Opening line.\n\n{extra}\n")
    return f"clients/{d.name}/build/{f.name}"


def t_page_decisions(h):
    S = "r3pd-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Pd Co" --domain r3wl.example --type full --industry roofing')
    d = h.SB / "clients" / S
    (d / "handoffs").mkdir(exist_ok=True)
    sp = d / S_FILE
    st = json.loads(sp.read_text())
    pages = {}
    for pid, name, wid in (("loc-hard", "Hardeeville", 43), ("loc-levy", "Levy", 42), ("loc-pritch", "Pritchardville", 44)):
        pages[pid] = {"type": "location", "name": name, "city": name, "url": f"{D}/{name.lower()}/", "wp_id": wid, "state": "handed_off",
                      "file": _page_file(d, name, MAP.format(name + ", SC")),
                      "open_items": [{"line": 8, "text": MAP.format(name + ", SC")}],
                      "links_placed": [f"{D}/levy/", f"{D}/pritchardville/"] if pid == "loc-hard" else []}
    pages["svc-rr"] = {"type": "service", "name": "Roof Repair", "url": f"{D}/roof-repair/", "wp_id": 20, "state": "handed_off",
                       "file": _page_file(d, "Roof-Repair", "Cited line.")}
    st["pages"] = pages
    st["build"] = {"batches": [{"id": "locs", "kind": "location", "pages": ["loc-hard", "loc-levy", "loc-pritch"],
                                "state": "drafts_written"}]}
    st["publish_handoff"] = {"id": "H-2026-10-14-01-publish", "at": "x", "run": "x", "batches": []}
    sp.write_text(json.dumps(st))
    H = "H-2026-10-14-01-publish-"
    rows = []
    n = 0
    for pid, wid in (("loc-hard", 43), ("loc-levy", 42), ("loc-pritch", 44), ("svc-rr", 20)):
        n += 1
        rows.append({"ref": f"{H}{n:02d}", "url": f"{D}/?page_id={wid}", "field": "publish", "old": "(draft)", "new": pages[pid]["url"],
                     "decision_map_ref": pid})
        if pid != "svc-rr":
            n += 1
            rows.append({"ref": f"{H}{n:02d}", "url": f"{D}/?page_id={wid}", "field": "open item",
                         "old": MAP.format(pages[pid]["name"] + ", SC"), "new": "", "decision_map_ref": pid,
                         "reason": "approved file line 8: resolve before publishing"})
    n += 1
    rows.append({"ref": f"{H}{n:02d}", "url": f"{D}/?page_id=10", "field": "publish", "old": "(draft)", "new": pages["svc-rr"]["url"],
                 "decision_map_ref": "svc-rr"})   # an older, stale draft of Roof Repair
    _group(d, rows)
    ag = h.Agent(S)
    rid = ag.start("new-client")
    # --- a page decision given in a review answer becomes a record
    findings = [{"page": "loc-levy", "rule": "viability", "item": "page decision", "severity": "ask", "kind": 1,
                 "finding": "Levy cannot fill its sections.", "plain_why": "A thin page.", "category": "ask",
                 "options": ["keep the Levy page", "merge Levy into Hardeeville", "no Levy page: mention Levy on Hardeeville, 301 /levy/ to /hardeeville/"],
                 "recommended": "a", "page_actions": {"c": {"action": "drop", "into": "loc-hard", "redirect_from": [f"{D}/levy/"],
                                                             "reason": "no Levy page: mention Levy on Hardeeville"}}},
                {"page": "loc-pritch", "rule": "viability", "item": "page decision", "severity": "ask", "kind": 1,
                 "finding": "Pritchardville waits for evidence.", "plain_why": "Thin.", "category": "ask",
                 "options": ["publish it", "hold it out of this batch"], "recommended": "a",
                 "page_actions": {"b": {"action": "hold", "reason": "hold out of this batch"}}}]
    fp = d / "build" / "findings.json"
    fp.write_text(json.dumps(findings))
    code, out = h.sh(f"python3 scripts/review.py sheet {S} locs drafts --findings clients/{S}/build/findings.json --run {rid}")
    code2, out2 = h.sh(f'python3 scripts/review.py apply {S} locs drafts --run {rid} --answers "accept all except 1c, 2b"')
    recs = json.loads((d / "page-decisions.json").read_text())
    h.check("§7a: a page decision answered in a review sheet (Levy 1c, Pritchardville 2b) becomes a page-decision record, with its source",
            code == 0 and code2 == 0 and [(r["page"], r["action"]) for r in recs] == [("loc-levy", "drop"), ("loc-pritch", "hold")]
            and "row 1c" in recs[0]["source"] and recs[0]["into"] == "loc-hard" and recs[0]["wp_ids"] == [42]
            and "PAGE-DECISION" in (d / "log.md").read_text(), (out, out2, recs))
    code, out = h.sh(f'python3 scripts/pagedec.py record {S} --page loc-levy --action drop --into loc-hard --reason "again"')
    h.check("§7a: recording the same decision again changes nothing", "already recorded" in out and len(json.loads(
        (d / "page-decisions.json").read_text())) == 2, out)
    h.sh(f'python3 scripts/pagedec.py record {S} --page svc-rr --action stale_drafts --wp-id 10 --reason "draft 10 does not match the approved file"')
    code, out = h.sh(f"python3 scripts/worklist.py build {S}")
    rws = list(csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8")))
    by = {r["id"]: r for r in rws}
    live = {i for i, r in by.items() if r["status"] != "superseded"}
    h.check("§7a (Levy): its publish row and open item are superseded by the decision; a trash-draft Setup row and a 301 /levy/ → "
            "/hardeeville/ in Redirects are added",
            by[H + "03"]["status"] == "superseded" and by[H + "04"]["status"] == "superseded" and "PD-01" in by[H + "03"]["note"]
            and by["PD-01-trash-42"]["section"].startswith("1") and "Trash WordPress draft 42" in by["PD-01-trash-42"]["task"]
            and by["PD-01-301-1"]["section"].startswith("3") and by["PD-01-301-1"]["new"] == f"{D}/hardeeville/"
            and H + "01" in by["PD-01-301-1"]["depends_on"], {k: v["status"] for k, v in by.items()})
    h.check("§7a (Pritchardville): held — no publish row, no open item, no trash row; the draft is not touched",
            by[H + "05"]["status"] == "superseded" and by[H + "06"]["status"] == "superseded"
            and not [i for i in by if i.startswith("PD-02")], sorted(by))
    h.check("§7a (stale drafts): the older Roof Repair draft's publish row is superseded and a trash row added; the current draft's row stays",
            by[H + "08"]["status"] == "superseded" and by["PD-03-trash-10"]["status"] == "open" and by[H + "07"]["status"] == "open",
            {k: v["status"] for k, v in by.items()})
    code, out = _check(h, S)
    rep = (d / "handoffs" / "worklist-check.md").read_text(encoding="utf-8")
    h.check("§7a: the validator accepts the decisions (no error for the dropped or held pages) and warns that Hardeeville's draft "
            "still links to them", code == 0 and "still link to" not in "".join(l for l in rep.splitlines() if "**" in l), (out, rep))
    h.check("§7a: the warning names the links to the dropped and held pages", "page(s) still link to" in rep, rep)
    h.check("§7a: the decisions appear in the settled register",
            "## Page decisions" in h.sh(f"python3 scripts/settled.py show {S}")[1], "")
    # --- ticking a decision row
    ret = d / "returned.csv"
    with open(ret, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["ref", "status", "note"])
        w.writeheader()
        w.writerow({"ref": "PD-01-trash-42", "status": "done", "note": "trashed"})
    code, out = h.sh(f"python3 scripts/handoff.py ingest {S} --run {rid} --returned clients/{S}/returned.csv")
    rws = list(csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8")))
    h.check("§7a: a returned tick on a decision row is kept in page-decisions.json and shown on the Worklist",
            next(r for r in rws if r["id"] == "PD-01-trash-42")["status"] == "done", out)
    h.sh(f'python3 scripts/run.py abort {S} {rid} --reason "test"')


def t_open_item_lists(h):
    S = "r3ol-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Ol Co" --domain r3wl.example --type full --industry roofing')
    d = h.SB / "clients" / S
    (d / "handoffs").mkdir(exist_ok=True)
    sp = d / S_FILE
    st = json.loads(sp.read_text())
    items = ["[NEED: cited lifespan source for metal roofing — researcher]", "[NEED: does Apex tarp or patch temporarily in an emergency?]",
             "[NEED: typical install time on a new home, if a figure will be stated]", "[NEED: 6–9 real project photos from the client]",
             "[NEED: Google Maps share link for the GBP]", "[LINK → /metal-roofing/ · reader wants it]",
             "[NEED: city-level map embed of Okatie, SC — not the Google Business Profile map]"]
    f = d / "build" / "LD-Metal.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f"---\npage_id: x\nurl: {D}/metal-roofing/\nseo_title: {TITLE}\nmeta_description: {META}\n---\n# Metal\n\n"
                 + "\n\n".join(f"Line {i}. Drip edge on every roof. {t}" for i, t in enumerate(items)) + "\n")
    st["pages"] = {"svc-m": {"type": "service", "name": "Metal Roofing", "url": f"{D}/metal-roofing/", "wp_id": 21,
                             "state": "handed_off", "file": f"clients/{S}/build/LD-Metal.md",
                             "open_items": [{"line": i + 8, "text": t} for i, t in enumerate(items)]}}
    st["publish_handoff"] = {"id": "H-2026-10-14-01-publish", "at": "x", "run": "x", "batches": []}
    sp.write_text(json.dumps(st))
    rows = [{"ref": "H-2026-10-14-01-publish-01", "url": f"{D}/?page_id=21", "field": "publish", "old": "(draft)",
             "new": f"{D}/metal-roofing/", "decision_map_ref": "svc-m"}]
    rows += [{"ref": f"H-2026-10-14-01-publish-{i + 2:02d}", "url": f"{D}/?page_id=21", "field": "open item", "old": t, "new": "",
              "decision_map_ref": "svc-m", "reason": f"approved file line {i + 8}: resolve before publishing"} for i, t in enumerate(items)]
    _group(d, rows)
    fx = d / "facts.json"
    fj = json.loads(fx.read_text()) if fx.exists() else {"facts": []}
    fj["facts"].append({"id": "d-emergency-tarping", "section": "D", "label": "Emergency tarping and temporary patching", "value": "Yes — tarps and patches after storm damage",
                        "status": "client_confirmed", "source": "call", "quote": "", "date": "2026-10-10", "who": "Paul", "count": None})
    fx.write_text(json.dumps(fj))
    code, out = h.sh(f"python3 scripts/worklist.py build {S}")
    rws = list(csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8")))
    own = {r["old"][:30]: r["owner"] for r in rws if r["field"] == "open item"}
    h.check("§7a: open items are split by who resolves them — the cited source is the researcher's, the client's facts and photos "
            "are Paul's to send, a proposed link is Paul's decision, a GBP link is Gwen's lookup, the map embed is Jonie's",
            [own[k] for k in (items[0][:30], items[1][:30], items[2][:30], items[3][:30], items[4][:30], items[5][:30], items[6][:30])]
            == ["Researcher", "Paul", "Paul", "Paul", "Gwen", "Paul", "Jonie"], own)
    rl = (d / "handoffs" / "researcher-list.md").read_text(encoding="utf-8")
    cq = (d / "handoffs" / "client-questions.md").read_text(encoding="utf-8")
    h.check("§7a: every cited-source gap is on the researcher's list and none is on the client's",
            "cited lifespan source for metal roofing" in rl and "cited" not in cq, (rl, cq))
    h.check("§7a: the client list has only client questions, grouped by page, in plain words (no row ids, no [NEED], no GBP link, "
            "no map, no proposed link)",
            "## Metal Roofing page" in cq and "tarp or patch" in cq and "typical install time" in cq.lower() and "project photos" in cq
            and "[NEED" not in cq and "H-2026" not in cq and "Google Maps share" not in cq and "map embed" not in cq
            and "LINK" not in cq, cq)
    h.check("§7a: a question is pre-filled where the evidence suggests an answer, and says so when nothing is on file",
            "Our best guess: We have this on file: Yes — tarps and patches after storm damage" in cq
            and "We have nothing on file for this one." in cq and "Your answer:" in cq, cq)


def t_rewrite_open_item(h):
    """A hand-written open-item row (the 10-09 Bluffton map) is replaced by a row in the standard map-embed format."""
    S = "r3ro-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Ro Co" --domain r3wl.example --type full --industry roofing')
    d = h.SB / "clients" / S
    (d / "handoffs").mkdir(exist_ok=True)
    sp = d / S_FILE
    st = json.loads(sp.read_text())
    line = "[Map: embed a city-level map of Bluffton, SC here — not the Google Business Profile map]"
    st["pages"] = {"loc-b": {"type": "location", "name": "Bluffton", "url": f"{D}/bluffton/", "wp_id": 21, "state": "handed_off",
                             "file": _page_file(d, "Bluffton", line)}}
    st["publish_handoff"] = {"id": "H-2026-10-14-01-publish", "at": "x", "run": "x", "batches": []}
    sp.write_text(json.dumps(st))
    _group(d, [{"ref": "H-2026-10-14-01-publish-01", "url": f"{D}/?page_id=21", "field": "publish", "old": "(draft)",
                "new": f"{D}/bluffton/", "decision_map_ref": "loc-b"},
               {"ref": "H-2026-10-14-01-publish-02", "url": f"{D}/bluffton/", "field": "open item",
                "old": "[Map: embed a city-level map of Bluffton SC here — not the Google Business Profile map]",
                "new": "Jonie: embed a Google map of Bluffton, SC", "decision_map_ref": "loc-b"}])
    code, out = _check(h, S)
    rep = (d / "handoffs" / "worklist-check.md").read_text(encoding="utf-8")
    h.check("§7a: a hand-written open-item row that does not match the line in the approved file is flagged both ways",
            code == 4 and "has an open item with no row" in rep and "no longer has this notice" in rep, rep)
    h.sh(f'python3 scripts/pagedec.py record {S} --page loc-b --action rewrite_open_item --supersedes H-2026-10-14-01-publish-02 '
         f'--match map --reason "standard map-embed format"')
    code, out = h.sh(f"python3 scripts/worklist.py build {S}")
    rws = {r["id"]: r for r in csv.DictReader(open(d / "handoffs" / "VA-WORKLIST.csv", newline="", encoding="utf-8"))}
    new = rws["PD-01-open-1"]
    h.check("§7a: the old row is superseded by one in the standard format (task, values, owner Jonie, the file's exact line)",
            rws["H-2026-10-14-01-publish-02"]["status"] == "superseded" and new["old"] == line and new["owner"] == "Jonie"
            and new["task"] == "Embed a city-level map of Bluffton, SC on the Bluffton page"
            and "not the Google Business Profile map" in new["values"] and "PD-01-open-1" in rws["H-2026-10-14-01-publish-01"]["depends_on"],
            (new, rws["H-2026-10-14-01-publish-01"]["depends_on"]))
    code, out = _check(h, S)
    h.check("§7a: after the rewrite the worklist passes", code == 0, out)


SCENARIOS = [t_page_decisions, t_open_item_lists, t_rewrite_open_item]
