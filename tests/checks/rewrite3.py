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
    terms = ["Client fact", "Public fact", "Source", "Official source", "Context source", "Evidence pack",
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
    S_ = "mf-co"
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
    ag = h.build_ready(slug, gaps or {"loc-springfield": {"neighborhoods", "things_to_do"},
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
    S_ = "pk-co"
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
            "## Gaps" in loc and "6-12 real neighborhoods" in loc and "researcher (public fact — never asked)" in loc,
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
    S_ = "rs-co"
    ag, code, out = packs_client(h, S_, {"loc-springfield": {"neighborhoods", "things_to_do"},
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
                    '--sources "methodology/sources/sc-lowcountry.md || https://springfield.example.gov || Wikipedia: Springfield"')
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
    d["facts"]["things_to_do"] = {"value": "", "status": "Unknown", "source": "not found (researcher)"}
    pf.write_text(json.dumps(d))
    code, out = h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch pilot")
    h.check("§4.2: evidence.py refuses a page fact recorded 'not found' without a valid research-log entry",
            code == 4 and "things_to_do" in out and "research-log" in out, out)
    log("--gap fact:loc-springfield:things_to_do --kind public --page loc-springfield --result not_found",
        '--queries "things to do springfield || Town of Springfield parks || springfield attractions"',
        '--sources "methodology/sources/sc-lowcountry.md || Wikidata: Springfield"')
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
         '--sources "methodology/sources/sc-lowcountry.md (SC LLR lookup) || Wikipedia: (no entry)"')
    h.sh(f"python3 scripts/evidence.py questions {S_} --run {rid} --all")
    fr = (h.SB / h.status(S_)["build"]["facts_round"]["file"]).read_text()
    h.check("§4.1: only a lookup logged not_found at the minimum may then be asked",
            "Licence numbers" in fr.split("<!--")[0], fr[:900])
    ag.fin(rid, "lookup")


SCENARIOS = [t_definitions, t_manifest, t_packs, t_research]
