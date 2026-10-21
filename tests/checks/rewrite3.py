"""Rewrite 3 Phase 1 (Paul, 2026-10-12; CM-061 — evidence first, decide by default)."""
import csv
import json
import re


def _read(h, rel):
    return (h.SB / rel).read_text(encoding="utf-8")


def t_definitions(h):
    """§2: one ruling records Phase 1; the definitions live in one file every agent and CLAUDE.md point to."""
    code, out = h.sh("python3 scripts/rulings.py CM-061")
    h.check("CM-061: the ruling is in rulings.md and readable by ID", code == 0 and "Evidence first, decide by default" in out
            and "APPROVED" in out, out[:300])
    d = _read(h, "methodology/definitions.md")
    terms = ["Client fact", "Public fact", "Place fact", "Place × niche fact", "Source", "Official source", "Context source", "Evidence pack",
             "Review mention", "Fact status", "Usage tier", "Known", "Searched", "Finding", "Severity", "Default", "Ask",
             "Section", "Step", "Review sheet", "Overdue Ask"]
    missing = [t for t in terms if f"**{t}**" not in d]
    h.check("§2: methodology/definitions.md defines every binding term", not missing, missing)
    files = sorted((h.SB / ".claude" / "agents").glob("*.md")) + [h.SB / "CLAUDE.md"]
    bad = [f.name for f in files if "methodology/definitions.md" not in f.read_text(encoding="utf-8")]
    h.check("§2: every agent file and CLAUDE.md points to methodology/definitions.md", not bad, bad)
    bad = [f.name for f in files[:-1] if "never limits web research" not in f.read_text(encoding="utf-8")]
    h.check("§4.3: every agent file says the read list never limits web research", not bad, bad)
    cfg = json.loads(_read(h, "config.json"))
    h.check("§2: the overdue-Ask window is a config value (3 working days)", cfg.get("overdue_ask_working_days") == 3)


REPO = __import__("pathlib").Path(__file__).resolve().parents[2]


def _mirror_client_files(h, slug):
    """The NAMES of every data/ and inputs/ file the real clients have (empty files — never their content) in one
    sandbox client, so the manifest is checked against every file type that exists on this Mac."""
    d = h.SB / "clients" / slug
    n = 0
    for c in sorted((REPO / "clients").glob("*")) if (REPO / "clients").is_dir() else []:
        for top in ("data", "inputs"):
            for p in (c / top).rglob("*") if (c / top).is_dir() else []:
                if p.is_file() and p.name != ".DS_Store":
                    q = d / p.relative_to(c)
                    q.parent.mkdir(parents=True, exist_ok=True)
                    q.touch()
                    n += 1
    return n


def t_manifest(h):
    """§3.1: every input type on file has a manifest entry; every consuming step's read list names it; unused inputs
    show in STATUS.md."""
    S_ = "r3-manifest-co"
    h.sh(f'python3 scripts/status.py init {S_} --name "Mf Co" --domain mf.example --type full --industry roofing')
    n = _mirror_client_files(h, S_)
    code, out = h.sh("python3 scripts/manifest.py check")
    h.check(f"§3.1: every file type in any client's data/ or inputs/ ({n} file names mirrored) has a manifest entry, and "
            "every consuming step's read list names it", code == 0, out[-1500:])
    stray = h.SB / "clients" / S_ / "data" / "mystery" / "thing.xyz"
    stray.parent.mkdir(parents=True, exist_ok=True); stray.write_text("x")
    code, out = h.sh("python3 scripts/manifest.py check")
    h.check("§3.1: a data file with no manifest entry fails the check, naming it", code == 4 and "data/mystery/thing.xyz" in out, out)
    stray.unlink()
    g = h.SB / "scripts" / "gates.json"
    orig = g.read_text(encoding="utf-8")
    gj = json.loads(orig)
    gj["steps"]["build:evidence"]["reads"] = [r for r in gj["steps"]["build:evidence"]["reads"] if "paa-questions" not in r]
    g.write_text(json.dumps(gj, indent=2, ensure_ascii=False) + "\n")
    code, out = h.sh("python3 scripts/manifest.py check")
    g.write_text(orig)
    h.check("§3.1: a consuming step whose read list leaves out its input fails the check",
            code == 4 and "paa-questions → build:evidence" in out, out)
    steps = json.loads(orig)["steps"]
    for step, must in (("build:evidence", ["reviews.csv", "mentions.csv", "paa-questions.csv", "fanout-queries.csv"]),
                       ("build:draft", ["packs/"]), ("build:brief", ["packs/"]), ("build:write", ["packs/"])):
        reads = " ".join(steps[step]["reads"])
        h.check(f"§1: {step} now reads {', '.join(must)}", all(m in reads for m in must), reads[:400])
    h.sh(f"python3 scripts/records.py render {S_}")
    stx = (h.SB / "clients" / S_ / "STATUS.md").read_text()
    sec = stx.split("## Data on file not used yet", 1)[-1].split("\n## ", 1)[0]
    h.check("§3.1: STATUS.md lists inputs on file that no finished step has read",
            "## Data on file not used yet" in stx and "**reviews**" in sec and "build:evidence" in sec, sec[:600])


PAA_CSV = """question,source_queries,times_seen,closest_existing_heading_or_faq,similarity
Do I need a permit to replace a roof in Springfield?,roof replacement Springfield | roof repair Springfield,2,,0.00
How long does a roof repair take?,roof repair Springfield | roof repair Shelbyville,3,,0.00
What is a gutter guard?,gutters Shelbyville,1,,0.00
"""
FANOUT_CSV = """query,seeds,times_seen,closest_paa_question,paa_similarity,closest_existing_heading_or_faq,c3_similarity
signs you need roof repair,roof repair Springfield,1,,0.00,,0.00
"""


def packs_client(h, slug, gaps=None):
    ag = h.build_ready(slug, gaps or {"loc-springfield": {"neighborhoods", "place_entities"},
                                      "svc-roof-repair": {"service_scope"}})
    ag.w("data/reviews/reviews.csv", h.REVIEWS_CSV)
    ag.w("data/paa/paa-questions.csv", PAA_CSV)
    ag.w("data/fanout/fanout-queries.csv", FANOUT_CSV)
    for pid in ag.batch_pages("pilot"):
        ag.write_facts(pid)
    rid = ag.start("build", "evidence", batch="pilot")
    code, out = h.sh(f"python3 scripts/evidence.py run {slug} --run {rid} --batch pilot")
    ag.fin(rid, "evidence gate and packs")
    return ag, code, out


def t_packs(h):
    """§3.2: one evidence pack per page, built by script with the evidence gate, before any brief."""
    S_ = "r3-packs-co"
    ag, code, out = packs_client(h, S_)
    st = h.status(S_)
    pk = (st["pages"]["svc-roof-repair"].get("pack") or {})
    h.check("§3.2: the evidence gate builds each page's pack in build/<section>/packs/",
            code == 0 and pk.get("file") == f"clients/{S_}/build/pilot/packs/svc-roof-repair.md"
            and (h.SB / pk["file"]).is_file() and (h.SB / pk["json"]).is_file(), (out, pk))
    md = (h.SB / pk["file"]).read_text()
    for sec in ("## Facts", "## Reviews", "## Questions", "## Site and GBP", "## Public facts", "## Settled decisions",
                "## Gaps"):
        h.check(f"§3.2: the pack has its '{sec[3:]}' section", sec in md)
    h.check("§3.2: reviews matching a practice are quoted with their independent-reviewer count and marked keyword-only",
            "### practice: photos — 2 independent reviewer(s) · keyword match only" in md
            and "attributed customer example only" in md and "reviews.csv row" in md, md[:2000])
    h.check("§3.2: reviews matching the service are collected", "### service: Roof Repair — 3 independent reviewer(s)" in md, md[:2000])
    h.check("§3.2: PAA and fan-out questions seen for the page's service, with how often",
            "[PAA] How long does a roof repair take? — seen 2×" in md and "[fan-out] signs you need roof repair" in md
            and "gutter guard" not in md, md.split("## Questions")[1][:600])
    loc = (h.SB / st["pages"]["loc-springfield"]["pack"]["file"]).read_text()
    h.check("§3.2: a location pack takes the questions seen for its place",
            "Do I need a permit to replace a roof in Springfield?" in loc, loc.split("## Questions")[1][:400])
    h.check("§3.2: the gaps are the evidence items with no excerpt yet, with who looks for each",
            "## Gaps" in loc and "Up to 12 real neighborhoods" in loc and "researcher (public fact — never asked)" in loc,
            loc.split("## Gaps")[1][:600])
    js = json.loads((h.SB / pk["json"]).read_text())
    h.check("§3.2: the pack's JSON holds its excerpts for the usage check", any(e["kind"] == "review" for e in js["excerpts"]))
    h.new_session()
    rid = ag.start("build", "facts")
    code, out = h.sh(f"python3 scripts/evidence.py questions {S_} --run {rid} --all")
    ag.fin(rid, "facts round")
    pack_q = (h.SB / h.status(S_)["build"]["facts_round"]["file"]).read_text()
    h.check("§1 (photos replay): a fact reviews mention is written at its usage tier, never asked of Paul",
            "What the service includes" not in pack_q.split("<!--")[0]
            and "Found in reviews, written at its usage tier" in pack_q and "What the service includes" in pack_q, pack_q[:1500])
    # no brief without a pack
    (h.SB / pk["file"]).unlink()
    rid = ag.start("build", "brief", batch="pilot")
    brief = ag.w("build/pilot/SB - Roof Repair - Test Co.md", "# brief\n\n## Evidence gaps\n- none\n")
    code, out = h.sh(f"python3 scripts/status.py page-stage {S_} svc-roof-repair --stage brief --file '{brief}' --run {rid}")
    h.check("§3.2: a brief is refused for a page without its evidence pack", code != 0 and "evidence pack" in out, out)
    h.sh(f'python3 scripts/run.py abort {S_} {rid} --reason "test"')
    wc = _read(h, "methodology/writing-commercial.md")
    tiers = wc.split("## Usage tiers", 1)[-1].split("\n## ", 1)[0]
    h.check("§3.3: the writing standard has the usage tiers (plain claim · customers mention · attributed example · "
            "site_stated · official · context)", all(x in tiers for x in ("A plain claim", "\"Customers mention…\"",
            "attributed customer example", "`site_stated`", "official source", "context source")), tiers[:300])
    reads = " ".join(json.loads(_read(h, "scripts/gates.json"))["steps"]["build:draft"]["reads"])
    h.check("§3.2: the pack is the draft writer's read list", "packs/<page>.md" in reads, reads)


CLIENT_SOURCES = ("facts.json || decisions-settled.md || the evidence pack || the proof sheet || the Discovery Record "
                  "|| the client's site search || GBP Q&A || GBP posts")


def t_research(h):
    """§4: research before "not found" — the log, its minimum, and the scripts that refuse what falls short."""
    S_ = "r3-research-co"
    ag, code, out = packs_client(h, S_, {"loc-springfield": {"neighborhoods", "place_entities"},
                                         "svc-roof-repair": {"pricing"}})
    h.new_session()
    rid = ag.start("build", "facts")
    log = lambda *a: h.sh(f"python3 scripts/research.py log {S_} --run {rid} --section pilot " + " ".join(a))
    code, out = log("--gap fact:loc-springfield:neighborhoods --kind public --page loc-springfield --result not_found",
                    '--queries "springfield neighborhoods || springfield subdivisions"', '--sources "Google"')
    h.check("§4.2: a public 'not found' below the minimum is refused, saying what is missing",
            code == 4 and "at least 3" in out and "official body" in out and "methodology/sources" in out
            and "Wikipedia" in out, out)
    code, out = log("--gap fact:loc-springfield:neighborhoods --kind public --page loc-springfield --result not_found",
                    '--queries "springfield neighborhoods || City of Springfield neighborhood map || springfield subdivisions list"',
                    '--sources "methodology/places/ || methodology/sources/sc-lowcountry.md || https://springfield.example.gov || Wikipedia: Springfield"')
    h.check("§4.2: a public 'not found' at the minimum is logged with its id", code == 0 and "RL-pilot-1" in out, out)
    row = next(csv.DictReader(open(h.SB / f"clients/{S_}/build/pilot/research-log.csv")))
    h.check("§4.2: the research log has the columns gap, kind, queries, sources_tried, result, excerpt, url, date",
            all(k in row for k in ("gap", "kind", "queries", "sources_tried", "result", "excerpt", "url", "date")), row)
    code, out = log("--gap fact:d:emergency --kind client --result not_found",
                    '--sources "facts.json || decisions-settled.md || the evidence pack || the proof sheet || the Discovery Record"')
    h.check("§4.2: a client 'not found' without the site search and the GBP Q&A and posts is refused",
            code == 4 and "site search" in out and "GBP Q&A" in out and "GBP posts" in out, out)
    # evidence.py refuses a facts file that says "not found" without a log entry
    pf = h.SB / f"clients/{S_}/build/evidence/loc-springfield.facts.json"
    d = json.loads(pf.read_text())
    d["facts"]["place_entities"] = {"value": "", "status": "Unknown", "source": "not found (researcher)"}
    pf.write_text(json.dumps(d))
    code, out = h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch pilot")
    h.check("§4.2: evidence.py refuses a page fact recorded 'not found' without a valid research-log entry",
            code == 4 and "place_entities" in out and "research-log" in out, out)
    log("--gap fact:loc-springfield:place_entities --kind public --page loc-springfield --result not_found",
        '--queries "things to do springfield || Town of Springfield parks || springfield attractions"',
        '--sources "methodology/places/ || methodology/sources/sc-lowcountry.md || Wikidata: Springfield"')
    code, out = h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch pilot")
    h.check("§4.2: with the logged search the gate runs", code == 0, out)
    # the facts round asks no client fact without its search
    code, out = h.sh(f"python3 scripts/evidence.py questions {S_} --run {rid} --all")
    fr = (h.SB / h.status(S_)["build"]["facts_round"]["file"]).read_text()
    asked = fr.split("<!--")[0]
    h.check("§4.1: a client fact with no research-log entry is not asked — the search order comes first",
            "Price range" not in asked and "Not asked yet — the client search order comes first" in fr
            and "fact:svc-roof-repair:pricing" in fr, fr[-1200:])
    code, out = h.sh(f"python3 scripts/research.py todo {S_} --all")
    h.check("§4.2: research.py todo lists the gaps still needing research", "fact:svc-roof-repair:pricing" in out, out)
    log("--gap fact:svc-roof-repair:pricing --kind client --page svc-roof-repair --result not_found", f'--sources "{CLIENT_SOURCES}"')
    h.sh(f"python3 scripts/evidence.py questions {S_} --run {rid} --all")
    fr = (h.SB / h.status(S_)["build"]["facts_round"]["file"]).read_text()
    h.check("§4.2: once logged, the client fact is asked and its question links the log entry",
            "Price range" in fr.split("<!--")[0] and "research log RL-pilot-" in fr, fr[-1500:])
    ag.fin(rid, "research")
    reqs = json.loads(_read(h, "methodology/evidence-requirements.json"))
    h.check("§4.1: licences, certifications and insurance are verified by public lookup before any question",
            {"D:Licence numbers", "D:Certifications", "D:Insurance"} <= set(reqs.get("verify_by_lookup") or {}))
    src = _read(h, "methodology/sources/README.md")
    h.check("§4.1: the area source lists carry the public lookups per state (licence board, manufacturer finder, "
            "business registration)", "## Public lookups" in src and "SC LLR" in src and "contractor finder" in src
            and "business entity search" in src)
    h.new_session()
    rid = ag.start("build", "facts")
    fid = "d-licence-numbers-and-classes"
    code, out = h.sh(f'python3 scripts/run.py fact {S_} {rid} --id {fid} --value "" --status unknown --source ""')
    h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch pilot")
    h.sh(f"python3 scripts/evidence.py questions {S_} --run {rid} --all")
    fr = (h.SB / h.status(S_)["build"]["facts_round"]["file"]).read_text()
    rl = (h.SB / f"clients/{S_}/build/evidence/research-all.md").read_text()
    h.check("§4.1: a licence with a public lookup goes to the researcher, never to Paul first",
            "Licence numbers" not in fr.split("<!--")[0] and "Licence numbers" in rl, (out, fr[:600], rl[-400:]))
    log2 = lambda *a: h.sh(f"python3 scripts/research.py log {S_} --run {rid} --section pilot " + " ".join(a))
    log2("--gap fact:d:licence_numbers --kind public --result not_found",
         '--queries "Test Co licence || State licensing board Test Co || Test Co contractor licence number"',
         '--sources "methodology/places/ || methodology/sources/sc-lowcountry.md (SC LLR lookup) || Wikipedia: (no entry)"')
    h.sh(f"python3 scripts/evidence.py questions {S_} --run {rid} --all")
    fr = (h.SB / h.status(S_)["build"]["facts_round"]["file"]).read_text()
    h.check("§4.1: only a lookup logged not_found at the minimum may then be asked",
            "Licence numbers" in fr.split("<!--")[0], fr[:900])
    ag.fin(rid, "lookup")


def F(page, rule, item, sev, cat, **kw):
    return {"page": page, "rule": rule, "item": item, "severity": sev, "category": cat,
            "finding": kw.pop("finding", f"{rule} on {item}"), "plain_why": kw.pop("plain_why", "it matters"), **kw}


def write_pilot(h, ag, S_, rid):
    for pid in ag.batch_pages("pilot"):
        f = ag.w(f"build/pilot/B-{pid}.md", f"# Brief {pid}\n\n## Evidence gaps\n- see the pack\n")
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {pid} --stage brief --file '{f}' --run {rid}")
        if code:
            h.check(f"the pilot brief for {pid} is recorded", False, out)
    for pid in ag.batch_pages("pilot"):
        d = ag.w(f"build/pilot/D-{pid}.md", f"# {pid}\n\nWe repair roofs carefully and on schedule. Call us today.\n")
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {pid} --stage draft --file '{d}' --run {rid} --agent sub-{pid}")
        if code:
            h.check(f"the pilot draft for {pid} is recorded", False, out)


def t_review(h):
    """§5 + §3.4: severities, one checker pass, dedupe, one review sheet per step, apply, approval, overdue."""
    S_ = "r3-review-co"
    ag, code, out = packs_client(h, S_)
    h.new_session()
    rid = ag.start("build", "write", batch="pilot")
    write_pilot(h, ag, S_, rid)
    # Apex fixtures: W16 is answered in facts.json; synthetic_roofing_offered is already asked and waiting
    h.sh(f'python3 scripts/run.py fact {S_} {rid} --id d-services-subcontracted-w16 --section D --label "Services '
         f'subcontracted (W16)" --value "Apex works as a roofing subcontractor on new construction" --status paul_approved '
         f'--source "Paul 2026-10-11"')
    h.sh(f'python3 scripts/run.py decision {S_} {rid} --ask synthetic_roofing_offered --who "Client (via Paul)" '
         f'--text "Synthetic roofing offered? Port Royal base-housing work?"')
    log = h.sh(f"python3 scripts/research.py log {S_} --run {rid} --section pilot --gap fact:d:emergency --kind client "
               f'--result not_found --sources "{CLIENT_SOURCES}"')[1].strip().splitlines()[-1]
    two = ["keep the page", "merge it into the Springfield page (301)"]
    findings = [
        F("svc-roof-repair", "E4", "FAQ 2 length", "fix", "length"),
        F("svc-roof-repair", "SEM-3", "intro angle", "fix_and_list", "semantic", decided_for_you="opened with the leak story"),
        F("svc-roof-repair", "SEM-3", "intro angle", "fix_and_list", "semantic", decided_for_you="dup"),
        F("loc-springfield", "plan", "page viability", "ask", "", kind=1, options=two, recommended="b"),
        F("loc-springfield", "C8", "FAQ wording", "ask", "", options=["reword", "drop"], recommended="a"),
        F("svc-roof-repair", "claim", "warranty years", "ask", "", kind=2, options=["state 10 years", "leave it out"], recommended="b"),
        F("loc-springfield", "D", "after-hours service", "ask", "", kind=3, log=log, options=["yes", "no"], recommended="b"),
        F("loc-hardeeville", "D", "new construction (W16)", "ask", "", kind=3, log=log, fact_key="fact:d:services_subcontracted",
          options=["yes", "no"], recommended="a"),
        F("loc-port-royal", "D", "synthetic roofing / base housing", "ask", "", kind=3, log=log,
          decision_key="synthetic_roofing_offered", options=["yes", "no"], recommended="a"),
        F("svc-roof-repair", "E2", "generic sentence", "fix", "other_content", decided_for_you="named the flashing work"),
    ]
    fj = ag.w("build/pilot/drafts-findings.json", json.dumps(findings))
    bad = ag.w("build/pilot/bad.json", json.dumps([F("svc-roof-repair", "D", "x", "ask", "", kind=3, options=["a", "b"],
                                                      recommended="a")]))
    code, out = h.sh(f"python3 scripts/review.py sheet {S_} pilot drafts --findings {bad} --run {rid}")
    h.check("§4.2/§5.2: a kind-3 Ask without its research-log entry is refused", code == 4 and "research-log" in out, out)
    code, out = h.sh(f"python3 scripts/review.py sheet {S_} pilot drafts --findings {fj} --run {rid}")
    h.check("§5.3: the one checker pass becomes one review sheet for the section's drafts", code == 0, out)
    rows = list(csv.DictReader(open(h.SB / f"clients/{S_}/build/pilot/drafts-review.csv")))
    h.check("§5.3: the sheet has the columns id, page, url, item, finding, plain_why, decided_for_you, options, "
            "recommended, answer, note", list(rows[0].keys()) == ["id", "page", "url", "item", "finding", "plain_why",
            "decided_for_you", "options", "recommended", "answer", "note"], list(rows[0].keys()))
    items = [r["item"] for r in rows]
    h.check("§5.1: a Fix (form only) is fixed silently — never in the sheet", "FAQ 2 length" not in items, items)
    h.check("§5.1: the same page + rule + item is raised once", items.count("intro angle") == 1, items)
    h.check("§5.2: an Ask that is not one of the four kinds but has a recommended option is decided by default",
            any(r["item"] == "FAQ wording" and r["decided_for_you"] == "" and "decided by default" in r["note"] for r in rows)
            or any(r["item"] == "FAQ wording" and "not one of the four Ask kinds" in r["note"] for r in rows), rows)
    h.check("§5.1: a 'Fix' that changes content is listed as Decided for you",
            any(r["item"] == "generic sentence" and r["decided_for_you"] for r in rows), rows)
    h.check("§5.2 (Apex Hardeeville W16): a question answered in facts.json never appears", "new construction (W16)" not in items)
    h.check("§5.2 (Apex Port Royal synthetic_roofing_offered): a question already asked never appears again",
            "synthetic roofing / base housing" not in items)
    data = json.loads((h.SB / f"clients/{S_}/build/pilot/drafts-review.json").read_text())
    whys = " ".join(d["why"] for d in data["dropped"])
    h.check("§5.2: the sheet says why each question was not raised", "facts.json" in whys and "synthetic_roofing_offered" in whys
            and "duplicate" in whys, data["dropped"])
    asks = [r for r in data["rows"] if r.get("severity") == "ask"]
    h.check("§5.2: only the four kinds are Asks (here 1, 2 and 3), each with options and a recommended default",
            sorted(r["kind"] for r in asks) == ["1", "2", "3"] and all(r["options"] and r["recommended"] for r in asks), asks)
    u = [r for r in rows if r["item"] == "evidence used"]
    h.check("§3.4: the draft review shows evidence used per page", len(u) == 2
            and all(re.match(r"Evidence used: \d+ of \d+ excerpts", r["finding"]) for r in u), u)
    h.check("§3.4: a pack with 2+ review excerpts the draft does not use gets a Fix-and-list row with the strongest one",
            any(r["item"] == "review evidence" and r["page"] == "svc-roof-repair" and "strongest excerpt" in r["decided_for_you"]
                for r in rows), rows)
    sheet = f"clients/{S_}/build/pilot/drafts-review.csv"
    code, out = h.sh(f"python3 scripts/status.py batch {S_} pilot --state drafts_written --review-sheet {sheet}")
    h.check("§5.3: the drafts are recorded with the review sheet (no SEM table, no --sem)", code == 0, out)
    bf = next(x for x in h.status(S_)["build"]["batches"] if x["id"] == "pilot")["files"]
    h.check("F-026: the review sheet is recorded as the review sheet, never as a draft",
            bf.get("review_sheet") == sheet and sheet not in bf["drafts"], bf)
    pg = ag.w("build/locations/SD-loc-a.md",
              "---\npage_id: loc-a\nurl: https://x.example/a/\nseo_title: T\nmeta_description: M\n---\n# A\n")
    cs = ag.w("build/locations/drafts-review.csv", "id,page\n1,loc-a\n")
    code, out = h.sh("python3 -I -c \"import sys; sys.path.insert(0, 'scripts'); import publish; "
                     f"print(publish.page_files(['{pg}', '{cs}', '{sheet}']))\"")
    h.check("F-026: Apex's case — publish ignores the review sheet CSV in an approved list, keeps the page",
            code == 0 and out.strip().splitlines()[-1] == f"['{pg}']", out)
    ag.fin(rid, "pilot written and reviewed")
    n = h.nxt(S_)
    h.check("§5.3: /next asks Paul to answer the sheet in one line before any approval",
            n["kind"] == "decision" and n["command"].startswith(f"/build {S_} review pilot drafts") and "accept all except" in n["why"], n)
    code, out = h.paul(f"/approve {S_} batch:pilot:briefs batch:pilot:drafts")
    h.check("§5.3: the approval is refused until the review sheet is applied", code != 0 and "not applied yet" in out, out)
    h.new_session()
    rid = ag.start("build", "review", batch="pilot")
    one = next(r["id"] for r in rows if r["item"] == "page viability")
    code, out = h.sh(f'python3 scripts/review.py apply {S_} pilot drafts --run {rid} --answers "accept all except {one}a"')
    ap = json.loads((h.SB / f"clients/{S_}/build/pilot/drafts-apply.json").read_text())["items"]
    pv = next(i for i in ap if i["item"] == "page viability")
    h.check("§5.3: one chat line answers the sheet — the named row takes Paul's option, every other row its default",
            code == 0 and pv["choice"] == "a" and pv["by"] == "Paul" and pv["action"] == "keep the page"
            and all(i["by"] == "default" for i in ap if i["item"] != "page viability"), ap)
    for pid in ag.batch_pages("pilot"):   # the review run applies every item and records every page again
        code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {pid} --stage draft --file "
                         f"'clients/{S_}/build/pilot/D-{pid}.md' --run {rid}")
        h.check(f"rewrite6: the review run re-records the draft of {pid} (agent kept)", code == 0, out)
    ag.fin(rid, "review applied")
    st = h.status(S_)   # the F-017 / sem_applied class: a later batch state must not refuse the approval
    next(b for b in st["build"]["batches"] if b["id"] == "pilot")["state"] = "sem_applied"
    (h.SB / f"clients/{S_}/status.json").write_text(json.dumps(st))
    code, out = h.paul(f"/approve {S_} batch:pilot:briefs batch:pilot:drafts")
    h.check("§5.3: after the review is applied the section is approved in one line, without --sem — at any later "
            "batch state (sem_applied here)", code == 0, out)
    # the same findings again in this section: never raised again
    h.new_session()
    rid = ag.start("build", "review", batch="pilot")
    code, out = h.sh(f"python3 scripts/review.py sheet {S_} pilot briefs --findings {fj} --run {rid}")
    again = json.loads((h.SB / f"clients/{S_}/build/pilot/briefs-review.json").read_text())
    h.check("§5.1: a finding decided once in the section is never raised again by a later check",
            not [r for r in again["rows"] if r.get("severity") in ("ask", "fix_and_list")]
            and "decided earlier in this section" in json.dumps(again["dropped"]), again)
    h.check("§10.8: the brief review shows the evidence-used line per page too",
            sum(1 for r in again["rows"] if r["item"] == "evidence used") == 2, again["rows"])
    ag.fin(rid, "no new findings")
    # §5.4 overdue: kinds 1, 3, 4 default; kind 2 is left out
    h.new_session()
    rid = ag.start("build", "review", batch="pilot")
    od = ag.w("build/pilot/od.json", json.dumps([
        F("loc-springfield", "plan", "merge Springfield", "ask", "", kind=1, options=two, recommended="b"),
        F("svc-roof-repair", "claim", "financing", "ask", "", kind=2, options=["say financing", "leave it out"], recommended="a")]))
    h.sh(f"python3 scripts/review.py sheet {S_} pilot drafts --findings {od} --run {rid}")
    code, out = h.sh("cd scripts && python3 -c \"import review, datetime as d; "
                     f"print(review.overdue('{S_}', '{rid}', True, d.date.today() + d.timedelta(days=7)))\"")
    rows = {r["item"]: r for r in csv.DictReader(open(h.SB / f"clients/{S_}/build/pilot/drafts-review.csv"))}
    h.check("§5.4: after 3 working days a kind-1 Ask takes the recommended option",
            rows["merge Springfield"]["answer"].startswith("b (overdue default"), rows)
    h.check("§5.4: a kind-2 Ask (legal or money) is never defaulted — it is left out", rows["financing"]["answer"] == "omit", rows)
    h.sh(f"python3 scripts/review.py apply {S_} pilot drafts --run {rid}")
    ap = {i["item"]: i for i in json.loads((h.SB / f"clients/{S_}/build/pilot/drafts-apply.json").read_text())["items"]}
    h.check("§5.4: the defaulted page carries an open-item notice; the kind-2 claim is removed, not softened",
            ap["merge Springfield"].get("open_item", "").startswith("[NEED: confirm merge Springfield")
            and "remove the sentence" in ap["financing"]["action"] and ap["financing"].get("open_item", "").startswith("[NEED:"), ap)
    ag.fin(rid, "overdue")
    sev = json.loads(_read(h, "methodology/review-severities.json"))
    h.check("§5.1: the severities file lists the form-only Fix categories and the four Ask kinds",
            {"length", "wording", "reading_grade", "internal_link", "heading_case"} <= set(sev["fix"]["categories"])
            and sorted(sev["ask"]["kinds"]) == ["1", "2", "3", "4"] and sev["ask"]["never_default"] == ["2"])


def t_brand_guide_once(h):
    """§6: the Brand Guide is written once per section, at the brief approval; never by drafts, review or ship."""
    S_ = "r3-bg-co"
    ag, code, out = packs_client(h, S_)
    h.new_session()
    rid = ag.start("build", "write", batch="pilot")
    write_pilot(h, ag, S_, rid)
    sem = ag.w("build/Test Co - Semantic Review - pilot - REVIEW.md", "| ID | Check |\n|---|---|\n")
    h.sh(f"python3 scripts/status.py batch {S_} pilot --state drafts_written --sem-table '{sem}' --sem-findings 0")
    ag.fin(rid, "pilot written")
    h.new_session()
    rid = ag.start("build", "writeback", batch="pilot")
    h.check("§6: the write-back step needs the section's briefs approved (not the drafts)", rid is None
            and any("batch:pilot:briefs" in e or "briefs" in e for e in ag.errors[-1:]), ag.errors[-1:])
    ag.errors.clear()
    code, out = h.paul(f"/approve {S_} batch:pilot:briefs batch:pilot:drafts")
    n = h.nxt(S_)
    h.check("§6: once the briefs are approved, /next runs the section's one write-back",
            code == 0 and n["kind"] == "run" and n["command"] == f"/build {S_} writeback pilot", (out, n))
    rid = ag.start("build", "writeback", batch="pilot")
    code, out = h.sh(f"python3 scripts/status.py writeback {S_} pilot --run {rid}")
    h.check("§6: the write-back is recorded once for the section", code == 0, out)
    code, out = h.sh(f"python3 scripts/status.py writeback {S_} pilot --run {rid}")
    h.check("§6: a second Brand Guide write-back for the same section is refused", code == 4 and "once per section" in out, out)
    ag.fin(rid, "write-back")
    g = json.loads(_read(h, "scripts/gates.json"))["steps"]["build:writeback"]
    h.check("§6: build:writeback is gated on the briefs approval", "batch:{batch}:briefs" in g["gates"]
            and "batch:{batch}:drafts" not in g["gates"], g)
    bm = _read(h, ".claude/agents/build.md") + _read(h, "docs/build-procedure.md")   # Phase 7: the procedure moved there
    h.check("§6: drafts, the draft review and ship never write the Brand Guide (the agent's instructions)",
            "Drafts, the draft review and ship never write the Brand Guide" in bm and "No Brand Guide write-back here" in bm)
    src = _read(h, "scripts/next.py")
    h.check("§6: a voided brand_guide_approved rides on the section's approval line (value-only approvals)",
            "def bg_reapproval" in src and "batch:{bid}:briefs{bg_reapproval(st)}" in src)


def t_brand_guide_once_walkthrough(h):
    """§6 test: a full client — every section writes the Brand Guide exactly once, never in a drafts or ship run."""
    log, decisions, runs, ag = h.walkthrough("r3-bgw", max_posts=0)
    lm = (h.SB / "clients/r3-bgw/log.md").read_text()
    wb = re.findall(r"^- WRITE-BACK \S+ · run (\S+) · batch (\S+):", lm, re.M)
    batches = [b["id"] for b in h.status("r3-bgw")["build"]["batches"]]
    per = {b: sum(1 for _, x in wb if x == b) for b in batches}
    h.check("§6: a full walkthrough writes the Brand Guide exactly once per section", log[-1] == "DONE"
            and all(v == 1 for v in per.values()), (per, log[-4:]))
    steps = dict(re.findall(r"^## RUN (\S+) · STARTED · .*\nStep: (\S+)", lm, re.M))
    h.check("§6: every write-back ran in its own write-back step — never in a drafts, review or ship run",
            all(steps.get(r) == "build:writeback" for r, _ in wb), [(r, steps.get(r)) for r, _ in wb])


def t_location_faq_viability(h):
    """§7 FAQ recipe; §8 viability check and minimums as targets."""
    faq = _read(h, "methodology/location-faq.md")
    h.check("§7: the location FAQ recipe has three categories, the question order and the brand-level fallback",
            all(x in faq for x in ("1 · Local cost or decision", "2 · Logistics in this area", "3 · Trust in this area",
                                   "PAA and fan-out questions already in the page's evidence pack", "brand-level local fallback",
                                   "\"Fix and list\" row in the review sheet, never\n  an Ask", "25% re-roof rule apply to homes on Fripp Island")), faq[:400])
    reads = " ".join(json.loads(_read(h, "scripts/gates.json"))["steps"]["build:write"]["reads"])
    h.check("§7: brief and draft writers read the FAQ recipe", "methodology/location-faq.md" in reads)
    S_ = "r3-viab-co"
    ag, code, out = packs_client(h, S_, {"loc-springfield": {"neighborhoods", "local_context", "place_entities"}})
    st = h.status(S_)
    h.check("§8 setup: two required public gaps block the location page", st["pages"]["loc-springfield"]["evidence"]["result"] == "block",
            st["pages"]["loc-springfield"]["evidence"])
    h.new_session()
    rid = ag.start("build", "evidence", batch="pilot")
    for gap in ("neighborhoods", "local_context"):
        h.sh(f"python3 scripts/research.py log {S_} --run {rid} --section pilot --gap fact:loc-springfield:{gap} --kind public "
             f'--page loc-springfield --result not_found --queries "springfield {gap} || City of Springfield {gap} || '
             f'springfield {gap} list" --sources "methodology/places/ || methodology/sources/sc-lowcountry.md || Wikipedia: Springfield"')
    h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch pilot")
    st = h.status(S_)
    grid = (h.SB / st["pages"]["loc-springfield"]["evidence"]["grid"]).read_text()
    h.check("§8: a public gap researched to the minimum is a target, not a hold — the page is no longer blocked",
            st["pages"]["loc-springfield"]["evidence"]["result"] != "block" and "a target, not a hold" in grid, grid[:900])
    pack = (h.SB / st["pages"]["loc-springfield"]["pack"]["file"]).read_text()
    h.check("§8: the pack tells the writer to shorten or drop the researched element (Fix and list)",
            "shorten or drop the element (Fix and list)" in pack, pack.split("## Gaps")[-1][:500])
    code, out = h.sh(f"python3 scripts/evidence_pack.py viability {S_} --all")
    h.check("§8: the viability check scores each location from its pack and proposes a merge for an unsourceable one",
            code == 0 and "loc-springfield" in out and "/7" in out and "MERGE PROPOSAL" in out and "Merge proposals" in out, out)
    ag.fin(rid, "viability")


def t_pilot_rule(h):
    """§9: a pilot only for a client's first section, a new industry, or after a writing change."""
    g = json.loads(_read(h, "scripts/gates.json"))["modes"]
    h.check("§9: gates.json → modes has the pilot: auto rule", (g.get("pilot") or {}).get("rule") == "auto", g.get("pilot"))
    S_ = "r3-pilot-co"
    h.sh(f'python3 scripts/status.py init {S_} --name "Pi Co" --domain pi.example --type full --industry "chimney sweeping" --sensitive no')
    code, out = h.sh(f"python3 scripts/status.py pilot {S_}")
    h.check("§9: a new industry needs a pilot, and says why", "pilot needed" in out and "new industry" in out, out)
    st = h.status(S_)   # this client already has one approved section, with today's writing fingerprint
    code, fp = h.sh("cd scripts && python3 -c \"import status; print(status.writing_fp())\"")
    st["build"] = {"site_plan": {"file": "x", "approval": None}, "pilot_corrections_applied": None,
                   "batches": [{"id": "services", "kind": "service", "label": "S", "pages": [], "state": "drafted",
                                "briefs": {"state": "approved"}, "drafts": {"state": "approved", "at": "2026-10-12T10:00",
                                                                            "writing_fp": fp.strip()}}]}
    (h.SB / f"clients/{S_}/status.json").write_text(json.dumps(st))
    code, out = h.sh(f"python3 scripts/status.py pilot {S_}")
    h.check("§9: an approved section, a known industry and unchanged writing rules → no pilot, with the reason",
            "pilot not needed" in out and "drafted in one run" in out, out)
    wc = h.SB / "methodology/writing-commercial.md"
    orig = wc.read_text()
    wc.write_text(orig + "\n- a new writing rule\n")
    code, out = h.sh(f"python3 scripts/status.py pilot {S_}")
    wc.write_text(orig)
    h.check("§9: the first section after a writing-rule change pilots again", "pilot needed" in out and "changed" in out, out)
    plan = {"pages": [{"id": "loc-a", "type": "location", "name": "A", "city": "A", "url": "https://pi.example/a/"},
                      {"id": "loc-b", "type": "location", "name": "B", "city": "B", "url": "https://pi.example/b/"}],
            "batches": [{"id": "locations", "kind": "location", "label": "L", "pages": ["loc-a", "loc-b"]}]}
    ag = h.Agent(S_)
    pj = ag.w("build/site-plan.json", json.dumps(plan)); pm = ag.w("build/Pi Co - Site Plan - REVIEW.md")
    code, out = h.sh(f"python3 scripts/status.py plan {S_} --file '{pm}' --json {pj}")
    st = h.status(S_)
    h.check("§9: a plan without a pilot is accepted when none is needed; the reason is recorded",
            code == 0 and "drafted in one run" in (st["build"].get("pilot_waived") or {}).get("reason", ""), out)
    S2 = "r3-pilot2-co"
    h.sh(f'python3 scripts/status.py init {S2} --name "Pj Co" --domain pj.example --type full --industry "chimney sweeping" --sensitive no')
    ag2 = h.Agent(S2)
    pj = ag2.w("build/site-plan.json", json.dumps(plan)); pm = ag2.w("build/Pj Co - Site Plan - REVIEW.md")
    code, out = h.sh(f"python3 scripts/status.py plan {S2} --file '{pm}' --json {pj}")
    h.check("§9: a client's first section without a pilot batch is refused, with the reason",
            code != 0 and "a pilot is needed" in out and ("first section" in out or "new industry" in out), out)


SCENARIOS = [t_definitions, t_manifest, t_packs, t_research, t_review, t_brand_guide_once, t_brand_guide_once_walkthrough,
             t_location_faq_viability, t_pilot_rule]
