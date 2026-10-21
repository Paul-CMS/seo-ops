"""Rewrite 4 Phase 5 — Finish folds into the plan (CM-064): the link wheel by script (wheel.py), schema by script
(schema.py, the BB-6xx node sets with the asset gate and a validator), mechanical QA by script (qa.py, with the QA
explanations job on llm.py and its no-key fallback), and the ship: every page drafted → links and schema in place →
one VA worklist → published together. link_wheel_approved is retired; release_approved stays.

Proved on HMM's saved site plan and its two approved pilot pages (tests/fixtures/hmm/plan, copied read-only): the wheel
rows and valid schema, with no agent."""
import json
import re
import shutil

DOMAIN = "homemobilemedical.com"
FX = ("tests", "fixtures", "hmm", "plan")
SECTION_F_FILLED = {   # the fake answers to Section F's [NEED] rows (the real ones are Paul's, in Finish)
    "| ID page URL (becomes the business entity @id) | [NEED: decide — About page or a new ID page] | Unknown — deferred to Finish (Paul 2026-10-07) |":
        "| ID page URL (becomes the business entity @id) | https://homemobilemedical.com/about/ | Paul Approved (test) |",
    "| Logo files with pixel dimensions | [NEED] | Unknown — deferred to Finish (Paul 2026-10-07) |":
        "| Logo files with pixel dimensions | https://homemobilemedical.com/wp-content/uploads/logo.png (512×512) | Internally Verified (test) |",
    "| Confirmed GBP category → schema subtype | Mobility equipment supplier → subtype chosen in Finish (bb-schema-builder) | Paul Approved |":
        "| Confirmed GBP category → schema subtype | Mobility equipment supplier → HomeAndConstructionBusiness | Paul Approved (test) |",
    "| Full citation list → sameAs | Facebook, Bing, Yelp, Storeboard, Chamber of Commerce, Hotfrog, Tupalo (BrightLocal 2026-09-28) — URLs to collect; Beaufort Medical Equipment listings excluded | Internally Verified (list), URLs Unknown |":
        "| Full citation list → sameAs | https://www.yelp.com/biz/home-mobile-medical-test · https://www.hotfrog.com/company/hmm-test | Internally Verified (test) |",
}
PILOT = ["svc-stair-lifts", "loc-beaufort-sc"]


def t_gates(h):
    g = json.loads((h.SB / "scripts/gates.json").read_text())
    fin = next(s for s in g["stages"] if s["id"] == "finish")
    h.check("gates: link_wheel_approved is retired (kept as history); release_approved stays, after the live QA",
            "link_wheel_approved" not in g["gates"] and "link_wheel_approved" in g["retired_gates"]
            and g["gates"]["release_approved"]["requires"] == ["pages_built", "blockers_cleared"]
            and g["gates"]["release_approved"]["before"]["producer"] == "/build {slug} handoff", g["gates"]["release_approved"])
    h.check("gates: Finish keeps only qa — the wheel and schema steps are gone",
            "finish:wheel" not in g["steps"] and "finish:schema" not in g["steps"] and fin["steps"][0] == "finish:qa", fin)


def t_dry_ship_hmm(h):
    """The Phase 5 'done when': a dry ship on HMM's pilot pages — WordPress drafts (fake) with the wheel's rows in their
    link tables, plus valid schema — with no agent."""
    S_ = "p5-ship"
    ag = hmm_client(h, S_)
    st = h.status(S_)
    st["imported_conditions"] = {**(st.get("imported_conditions") or {}), "wordpress_connected": "test"}
    b = next(x for x in st["build"]["batches"] if x["id"] == "pilot")
    b["drafts"] = {"state": "approved", "files": {}, "baseline": True}
    b["files"] = {"drafts": [st["pages"][p]["file"] for p in PILOT]}
    b["content_written_back"] = True
    (ag.c / "status.json").write_text(json.dumps(st))
    rid = ag.start("build", "ship")
    code, out = h.sh(f"python3 tests/fakes.py publish drafts {S_} --run {rid} --batch pilot")
    h.check("dry ship: the pilot's two pages become WordPress drafts with no agent", code == 0 and "2 drafts created" in out, out)
    wp = json.loads((h.SB / "tests/.state/wp.json").read_text())["items"]
    st = h.status(S_)
    raw = {p: wp[str(st["pages"][p]["wp_id"])]["content"]["raw"] for p in PILOT}
    h.check("dry ship: drafts only — nothing published", all(wp[str(st["pages"][p]["wp_id"])]["status"] == "draft" for p in PILOT))
    svc_links = re.findall(r'href="([^"]+)"', raw["svc-stair-lifts"])
    h.check("dry ship: the service draft's service-area table carries all 24 location pages",
            sum(u.endswith("-sc/") for u in svc_links) == 24 and ">Stair Lift Installation in Beaufort<" in raw["svc-stair-lifts"],
            svc_links[:5])
    loc = raw["loc-beaufort-sc"]
    h.check("dry ship: the location draft links every service, then its hub first and every other city",
            all(f"homemobilemedical.com/{s}/" in loc for s in ("stair-lifts", "curved-stair-lifts", "porch-lifts",
                                                              "wheelchair-lifts", "stair-lift-repair"))
            and loc.index("hilton-head-bluffton-metro/") < loc.index("bluffton-sc/\"") and "[Link wheel" not in loc, loc[-900:])
    h.check("dry ship: every placed link is recorded on the page (for /verify)",
            len(st["pages"]["loc-beaufort-sc"]["links_placed"]) == 5 + 1 + 23, len(st["pages"]["loc-beaufort-sc"]["links_placed"]))
    code, out = h.sh(f"python3 tests/fakes.py schema build {S_} --pages {','.join(PILOT)} --out {ag.c / 'tmp/ship-schema'}")
    h.check("dry ship: and the pilot's schema is valid", code == 0 and "built and valid" in out, out)
    ag.sh(f"python3 scripts/run.py abort {S_} {rid} --reason test")


def t_markers_and_asks(h):
    """[LINK → …] only for pages not yet planned (CM-064); CM-022 exceptions are kind-1 Asks in the site plan."""
    S_ = "p5-mark"
    ag = hmm_client(h, S_)
    st = h.status(S_)
    st["pages"]["loc-beaufort-sc"]["link_exceptions"] = [
        {"kind": "contextual", "target": "/stair-lift-repair/", "anchor": "stair lift repair", "reason": "readers ask who fixes it"},
        {"kind": "contextual", "target": "/porch-lifts/", "anchor": "porch lifts", "reason": "second one"}]
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = h.sh(f"python3 scripts/wheel.py asks {S_}")
    asks = json.loads((ag.c / "build/link-asks.json").read_text())
    h.check("asks: each proposed CM-022 exception is a kind-1 Ask for the site plan; one over the limit defaults to decline",
            code == 0 and len(asks) == 2 and all(a["kind"] == "1" and a["severity"] == "ask" for a in asks)
            and asks[0]["recommended"] == "a" and asks[1]["recommended"] == "b" and "over the limit" in asks[1]["finding"]
            and asks[0]["decision_key"] == "linkx:loc-beaufort-sc:1", asks)
    text = ("We also handle stair lift repair [LINK → /stair-lift-repair/ · readers ask who fixes it] and ramps "
            "[LINK → /ramps/ · not planned yet] and porch lifts [LINK → /porch-lifts/ · second one].")
    f = ag.w("tmp/mark.md", f"---\npage_id: loc-beaufort-sc\nurl: https://homemobilemedical.com/beaufort-sc/\n---\n# X\n\n{text}\n")
    _, out = h.sh(f"python3 scripts/wheel.py fill {S_} {f}")
    h.check("markers: with no approved exception a marker to a planned page is dropped and the words kept; an unplanned "
            "page's marker stays an open item",
            "We also handle stair lift repair and ramps [LINK → /ramps/ · not planned yet] and porch lifts." in out
            and "marker dropped" in out, out)
    rid = ag.start("build", "plan")
    ag.sh(f'python3 scripts/run.py decision {S_} {rid} --settle linkx:loc-beaufort-sc:1 --text "a — approved (Paul)"')
    ag.sh(f"python3 scripts/run.py abort {S_} {rid} --reason test")
    _, out = h.sh(f"python3 scripts/wheel.py fill {S_} {f}")
    h.check("markers: an approved exception links its words; the declined one is still dropped",
            "We also handle [stair lift repair](https://homemobilemedical.com/stair-lift-repair/) and ramps" in out
            and "and porch lifts." in out, out)


def t_qa_on_hmm(h):
    S_ = "p5-qa"
    ag = hmm_client(h, S_)
    out_d = ag.c / "tmp/qa-dry"
    code, out = h.sh(f"python3 scripts/qa.py check {S_} --pages {','.join(PILOT)} --out {out_d}")
    rows = list(__import__("csv").DictReader(open(out_d / "qa-ship.csv")))
    errs = [r for r in rows if r["level"] == "error"]
    h.check("qa: HMM's approved pilot pages pass the mechanical QA with no error, by script", code == 0 and not errs,
            out + "\n" + "\n".join(f"{r['page']} {r['check']} {r['detail']}" for r in errs))
    h.check("qa: the punch list is written for Paul (Markdown) next to the CSV", (out_d / "qa-ship.md").exists()
            and "QA Punch-List — ship" in (out_d / "qa-ship.md").read_text(), out)
    # a broken copy of the Beaufort page: every mechanical rule fires
    st = h.status(S_)
    bad = fx(h, "loc-beaufort-sc.md").read_text()
    bad = bad.replace("seo_title: Home Mobile Medical - Mobility Equipment Supplier - Beaufort, South Carolina",
                      "seo_title: The Best Stair Lifts Beaufort SC")
    bad = bad.replace("# Stair Lift Installer in Beaufort", "# Home Mobile Medical Stair Lifts in Beaufort, SC")
    bad = bad.replace("Call (843) 476-1329.\n\n## Accessibility",
                      "Call (843) 476-1329. See [our ramps](/ramps/) and [repairs](https://homemobilemedical.com/stair-lift-repair/). TBD\n\n## Accessibility", 1)
    bad = bad.replace("| [Link wheel: populate sibling-city links here] |", "")
    f = ag.w("build/pilot/drafts/loc-beaufort-sc.md", bad)
    code, out = h.sh(f"python3 scripts/qa.py check {S_} --pages loc-beaufort-sc --out {out_d}")
    rows = list(__import__("csv").DictReader(open(out_d / "qa-ship.csv")))
    got = {(r["check"], r["rule"]) for r in rows if r["level"] == "error"}
    h.check("qa: a wrong title format, 'The Best', a branded H1 with the state, a link to an unplanned page and a lost "
            "link table are errors",
            code == 1 and {("title", "BB-302"), ("title", "CM-020"), ("h1", "BB-305"), ("h1", "location §3.4"),
                           ("links", "CM-064")} <= got
            and any("sibling-city" in r["detail"] for r in rows if r["check"] == "links"), got)
    h.check("qa: a cross-page link in prose is flagged (CM-005) and an open placeholder is listed for the worklist",
            any(r["rule"] == "CM-005" for r in rows) and any(r["check"] == "placeholders" and "TBD" in r["detail"] for r in rows),
            [(r["check"], r["rule"], r["detail"][:60]) for r in rows])
    rid = ag.start("build", "ship")
    (h.SB / "tests/.state").mkdir(parents=True, exist_ok=True)
    nokey = h.SB / "tests/.state/llm-401.json"
    nokey.write_text(json.dumps({"qa-explain": {"error": 401}}))
    h.sh(f"python3 scripts/qa.py check {S_} --pages loc-beaufort-sc")
    code, out = h.sh(f"SEO_OPS_LLM_FAKE={nokey} python3 scripts/qa.py explain {S_} --run {rid}")
    md = (ag.c / "finish/qa/qa-ship.md").read_text()
    h.check("qa explain: with no API key nothing fails — it says so once and each row keeps a fixed hint and an owner",
            code == 0 and "no API key — ran on the agent route" in out and "by the fixed hints" in out
            and "rewrite the title in the approved file | writer" in md, out + md[-600:])
    rows = list(__import__("csv").DictReader(open(ag.c / "finish/qa/qa-ship.csv")))
    ans = {str(i): {"explain": f"plain words {i}", "fix": f"do {i}", "who": "writer"}
           for i, r in enumerate(r for r in rows if r["level"] in ("error", "warn"))}
    fake = h.SB / "tests/.state/llm-qa.json"
    fake.write_text(json.dumps({"qa-explain": {"items": ans}}))
    code, out = h.sh(f"SEO_OPS_LLM_FAKE={fake} python3 scripts/qa.py explain {S_} --run {rid}")
    md = (ag.c / "finish/qa/qa-ship.md").read_text()
    led = [json.loads(l) for l in (ag.c / "llm-costs.jsonl").read_text().splitlines()] if (ag.c / "llm-costs.jsonl").exists() else []
    h.check("qa explain: on the API (Haiku) each error and warning gets a plain explanation, the fix and who acts — logged",
            code == 0 and "on the Claude API" in out and "| do 0 | writer |" in md
            and any(x.get("job") == "qa-explain" or "qa-explain" in json.dumps(x) for x in led), out + md[-400:])
    ag.sh(f"python3 scripts/run.py abort {S_} {rid} --reason test")
    code, out = h.sh(f"python3 scripts/qa.py sample {S_}")
    picked = (ag.c / "finish/qa/finish-qa-pages.txt").read_text().split()
    h.check("qa sample: finish-qa (Opus) reads only a sample for a client that is not sensitive — every page type in it",
            code == 0 and 5 <= len(picked) < 33 and {"homepage", "about"} <= set(picked)
            and any(p.startswith("svc-") for p in picked) and any(p.startswith("hub-") for p in picked), out)
    st = h.status(S_)
    st["client"]["sensitive"] = True
    st["client"]["sensitive_category"] = "health"
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = h.sh(f"python3 scripts/qa.py sample {S_}")
    h.check("qa sample: a sensitive client (CM-025) gets every page read by finish-qa",
            len((ag.c / "finish/qa/finish-qa-pages.txt").read_text().split()) == 33 and "every page" in out, out)


def t_schema_on_hmm(h):
    S_ = "p5-schema-real"
    hmm_client(h, S_, filled=False)
    code, out = h.sh(f"python3 scripts/schema.py gate {S_}")
    h.check("schema: HMM's real Section F fails the asset gate and names what Paul still owes (no partial schema)",
            code == 2 and "ASSET GATE FAILED" in out and "id_page_url" in out and "business.logo" in out
            and "schema subtype" in out and "citation list" in out, out)
    S_ = "p5-schema"
    ag = hmm_client(h, S_)
    code, out = h.sh(f"python3 tests/fakes.py schema build {S_} --pages {','.join(PILOT)} --out {ag.c / 'tmp/schema-dry'}")
    h.check("schema: a dry build on HMM's pilot pages passes the gate, the entity check and the validator, with no agent",
            code == 0 and "3 page(s) of schema built and valid" in out, out)
    d = ag.c / "tmp/schema-dry"
    g = {f.stem: json.loads(f.read_text()) for f in d.glob("*.jsonld")}
    types = {k: [n["@type"] for n in v["@graph"]] for k, v in g.items()}
    h.check("schema: the homepage (the GBP landing page) carries WebSite + Corporation + the LocalBusiness subtype",
            types.get("homepage") == ["WebSite", "Corporation", "HomeAndConstructionBusiness"], types)
    h.check("schema: the service page is WebPage + Service and the location page WebPage + ItemList — no LocalBusiness",
            types.get("service-stair-lifts") == ["WebPage", "Service"] and types.get("location-beaufort-sc") == ["WebPage", "ItemList"],
            types)
    biz = g["homepage"]["@graph"][2]
    h.check("schema: the business entity's @id is the ID page, NAP and hours from the Brand Guide, no invented founding year",
            biz["@id"] == "https://homemobilemedical.com/about/" and biz["telephone"] == "+1-843-476-1329"
            and biz["address"]["postalCode"] == "29902" and biz["openingHoursSpecification"][0]["opens"] == "09:00"
            and "foundingDate" not in g["homepage"]["@graph"][1], biz)
    cat = g["location-beaufort-sc"]["@graph"][1]["itemListElement"]
    h.check("schema: the location's service catalog lists every planned service page",
            len(cat) == 5 and cat[0]["item"]["@id"] == "https://homemobilemedical.com/stair-lifts/#service", cat)
    svc = g["service-stair-lifts"]["@graph"][0]
    h.check("schema: the service page's title and description are its approved file's; entities carry Wikidata @ids",
            svc["name"] == "Stair Lifts - Home Mobile Medical"
            and {e.get("@id") for e in svc["about"][1:]} == {"https://www.wikidata.org/wiki/Q6887300",
                                                             "https://www.wikidata.org/wiki/Q3885311", "https://www.wikidata.org/wiki/Q1456"},
            svc)
    code, out = h.sh(f"python3 scripts/schema.py validate {d}")
    h.check("schema validate: the built files pass", code == 0 and "3 schema file(s) valid" in out, out)
    bad = json.loads((d / "service-stair-lifts.jsonld").read_text())
    bad["@graph"].append({"@type": "HomeAndConstructionBusiness", "@id": "https://homemobilemedical.com/about/",
                          "telephone": "+1-843-476-1329"})
    bad["@graph"][0]["about"].append({"@id": "https://homemobilemedical.com/nowhere/#service"})
    (d / "service-stair-lifts.jsonld").write_text(json.dumps(bad))
    code, out = h.sh(f"python3 scripts/schema.py validate {d}")
    h.check("schema validate: LocalBusiness on a service page, NAP off the business entity and a dangling @id all fail (BB-604)",
            code == 1 and "BB-604" in out and "NAP" in out and "resolves to nothing" in out, out)
    code, out = h.sh(f"python3 tests/fakes.py schema build {S_} --pages {','.join(PILOT)}")
    h.check("schema: a dry run never writes into the client's schema folder", code != 0 and "--out" in out
            and not (ag.c / "finish/schema/index.json").exists(), out)


def fx(h, name):
    return h.SB.joinpath(*FX, name)


def hmm_plan(h):
    return json.loads(fx(h, "site-plan.plan.json").read_text())


def hmm_client(h, slug, filled=True):
    """A client holding HMM's saved site plan (approved), its Brand Guide and its two approved pilot pages."""
    plan = hmm_plan(h)
    ag = h.build_ready(slug, plan=plan)
    bg = fx(h, "brand-guide.md").read_text()
    if filled:
        for a, b in SECTION_F_FILLED.items():
            bg = bg.replace(a, b)
    ag.w("brand-guide.md", bg)
    st = h.status(slug)
    for pid in ("svc-stair-lifts", "loc-beaufort-sc"):
        f = ag.w(f"build/pilot/drafts/{pid}.md", fx(h, f"{pid}.md").read_text())
        st["pages"][pid].update({"file": f, "state": "drafts_approved"})
    (ag.c / "status.json").write_text(json.dumps(st))
    return ag


def t_wheel_on_hmm(h):
    S_ = "p5-wheel"
    ag = hmm_client(h, S_)
    code, out = h.sh(f"python3 scripts/wheel.py plan {S_}")
    h.check("wheel: plans every page of HMM's site plan by script, with no agent", code == 0 and "link wheel:" in out, out)
    w = json.loads((ag.c / "build/link-wheel.json").read_text())
    svc, loc = w["svc-stair-lifts"], w["loc-beaufort-sc"]
    locs = [p["id"] for p in hmm_plan(h)["pages"] if p["type"] == "location"]
    svcs = [p["id"] for p in hmm_plan(h)["pages"] if p["type"] == "service"]
    h.check("wheel: a service page links every location page (BB-205)",
            [r[2] for r in svc["service_areas"]] == locs and len(locs) == 24, svc["service_areas"][:3])
    h.check("wheel: service → location anchors are '[service variant] in [City]' from the approved H1",
            svc["service_areas"][0][0] == "Stair Lift Installation in Beaufort"
            and any(r[0] == "Stair Lift Installation in Lady's Island" for r in svc["service_areas"]), svc["service_areas"][:4])
    h.check("wheel: a location page links every service page", [r[2] for r in loc["services"]] == svcs, loc["services"])
    h.check("wheel: a location page's sibling table opens with its hub, then every other location",
            loc["siblings"][0][2] == "hub-hhi-beaufort" and [r[2] for r in loc["siblings"][1:]] == [l for l in locs if l != "loc-beaufort-sc"],
            loc["siblings"][:3])
    h.check("wheel: a sibling row's anchor is the target's H1 (approved file, else outline.py's formula)",
            any(r[2] == "loc-bluffton-sc" and r[0] == "Stair Lift Installer in Bluffton" for r in loc["siblings"]), loc["siblings"][:4])
    hub = w["hub-hhi-beaufort"]
    hhi = [p["id"] for p in hmm_plan(h)["pages"] if p["type"] == "location" and p.get("group") == "HHI-Bluffton-Port Royal metro"]
    h.check("wheel: a hub links its own cities (and only those) and every service page",
            [r[2] for r in hub["service_areas"]] == hhi and [r[2] for r in hub["services"]] == svcs, hub)
    hp = w["homepage"]
    h.check("wheel: the homepage links every service page and every hub, plus the cities with no hub",
            [r[2] for r in hp["services"]] == svcs
            and [r[2] for r in hp["service_areas"]] == ["hub-hhi-beaufort", "hub-charleston", "loc-walterboro-sc", "loc-edisto-island-sc"],
            hp)
    h.check("wheel: the about page has no link tables", "about" not in w or not any(w["about"].values()), w.get("about"))
    code, out = h.sh(f"python3 scripts/wheel.py check {S_}")
    h.check("wheel check: HMM's plan and pilot files place every row (no error)", code == 0 and "0 error(s)" in out, out)


SCENARIOS = [t_gates, t_wheel_on_hmm, t_schema_on_hmm, t_dry_ship_hmm, t_markers_and_asks, t_qa_on_hmm]
