"""Rewrite 3 §4 (CM-062): the new location page structure, the ownership rules, the cross-page similarity check."""
import json
import re
import subprocess
from pathlib import Path

S_FILE = "status" + ".json"


def t_location_spec(h):
    spec = (h.SB / "methodology/specs/location.md").read_text(encoding="utf-8")
    elements = spec.split("## 3.", 1)[1].split("## 4.", 1)[0]
    rows = re.findall(r"^\| (\d+) \| (.+?) \|", elements, re.M)
    names = [n for _, n in rows]
    order = ["URL", "SEO title", "Meta description", "H1", "Opening paragraph", "H2 services table", "H2 Local context",
             "H2 Serving [City]", "FAQ", "H2 Neighbourhoods", "H2 Recent work in [City]", "City map", "H2 sibling cities", "CTA"]
    h.check("CM-062: the location spec's elements are in the new order", names == order, names)
    h.check("CM-062: no Things to Do or Top Sites element; place entities woven into Local context",
            "H2 Things to Do" not in elements and "H2 Top Sites" not in elements
            and "3–4 named, verifiable place entities woven in" in elements, elements[:300])
    h.check("CM-062: FAQ is three questions, one per category; Serving has one informational outbound link",
            "three questions, one per category" in elements and "One informational outbound link" in elements)
    h.check("CM-062: neighbourhoods up to 12 (fewer than 3 dropped), Recent work optional and dropped silently, CTA with hours",
            "**Up to 12**" in elements and "Fewer than 3 verified → drop the section" in elements
            and "Dropped silently" in elements and "name, phone and hours" in elements
            and "**only** on the GBP landing page" in elements, elements[-900:])
    h.check("CM-062: ownership rules, the swap test and the no-ratings rule are in the spec",
            "Ownership inside the page" in spec and "swap the city name for a neighbouring city" in spec
            and "No static star rating or review count" in spec and "no rating schema" in spec)
    h.check("CM-062: the schema section puts place entities in `about` with Wikidata ids, never in `mentions`",
            "Wikidata URI as `@id`" in spec and "**not** put in `mentions`" in spec)
    for lid in ("LOC-28", "LOC-29", "LOC-30", "LOC-31", "LOC-32"):
        h.check(f"CM-062: conformance check {lid} exists", f"| {lid} |" in spec)
    real = (Path(__file__).resolve().parent.parent.parent / "methodology/specs/location.md").read_text(encoding="utf-8")
    h.check("CM-062: the real spec stays a draft until Paul approves it for itself (per spec file, CR-023)",
            "**Status:** DRAFT" in real or "**Status:** APPROVED" in real and "CM-062" in real)
    legacy = (h.SB / "methodology/specs/legacy/location-2026-10-08.md").read_text(encoding="utf-8")
    h.check("CM-062: the earlier structure is kept for Apex", "H2 Things to Do" in legacy and "**Status:** APPROVED" in legacy)
    code, out = h.sh("python3 scripts/rulings.py CM-062")
    h.check("CM-062: the ruling is recorded, with Paul's three answers",
            code == 0 and "No Things to Do and no Top Sites" in out and "Recent work" in out and "Apex" in out
            and "`about`" in out and "`mentions`" in out, out[:300])
    h.sh('python3 scripts/status.py init spec-loc-co --name "Spec Loc" --domain sl.example --type full --industry roofing')
    if h.sh("python3 scripts/status.py require spec-loc-co page_specs_approved")[0] != 0:
        h.paul("/approve global specs")
    sp_ = h.SB / "methodology/specs/location.md"
    old_ = sp_.read_text(encoding="utf-8")
    sp_.write_text(old_ + "\nA new rule.\n", encoding="utf-8")   # the spec changed since Paul approved it
    code, out = h.sh("python3 scripts/status.py require spec-loc-co page_specs_approved")
    sp_.write_text(old_, encoding="utf-8")
    h.check("CM-062/CR-023: an unapproved location spec blocks new work, naming only that spec and its own approve line",
            code == 4 and "location.md" in out and "/approve global specs:location" in out and "service.md" not in out, out)
    h.sh('python3 scripts/status.py init spec-started-co --name "Spec Started" --domain ss.example --type full --industry roofing')
    ssp = h.SB / "clients" / "spec-started-co" / S_FILE
    sst = json.loads(ssp.read_text())
    sst["pages"] = {"loc-a": {"type": "location", "city": "A", "name": "A", "url": "https://ss.example/a/",
                              "files": {"draft": {"file": "clients/spec-started-co/build/LD-a.md"}}}}
    ssp.write_text(json.dumps(sst))
    sp_.write_text(old_ + "\nA new rule.\n", encoding="utf-8")
    code2, out2 = h.sh("python3 scripts/status.py require spec-started-co page_specs_approved")
    sp_.write_text(old_, encoding="utf-8")
    h.check("CR-023: a client that already drafted location pages keeps the spec version it started with (Apex keeps its "
            "structure), while a client that has not (HMM) is blocked until Paul approves the new one", code2 == 0, out2)
    req = json.loads((h.SB / "methodology/evidence-requirements.json").read_text())
    keys = [i["key"] for i in req["types"]["location"]]
    h.check("CM-062: the evidence requirements drop Things to Do and Top Sites, and ask for place entities and the permit office",
            "things_to_do" not in keys and "top_sites" not in keys and "place_entities" in keys and "permit_office" in keys, keys)


def t_similarity(h):
    S = "sim-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Sim Co" --domain sim.example --type full --industry roofing')
    d = h.SB / "clients" / S
    shared = ("Salt air and coastal humidity wear down asphalt shingles faster than most homeowners expect, so a "
              "yearly roof check pays for itself before the next hurricane season starts.")
    own_a = "Aville sits beside the Mill River and its 1920s bungalows still carry original cedar decking under newer shingles."
    own_b = "Bville grew around the old rail depot, and most of its homes are brick ranches from the 1960s with low-pitch roofs."
    for city, own in (("Aville", own_a), ("Bville", own_b)):
        f = d / "build" / "locs" / f"LD - {city}.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# Roofers in {city}\n\n## Local context\n\n{shared} {own}\n\n| Service | Link |\n|---|---|\n| Roof repair | x |\n")
    sp = d / S_FILE
    st = json.loads(sp.read_text())
    st["pages"] = {pid: {"type": "location", "city": c, "name": c, "url": f"https://sim.example/{c.lower()}/",
                         "file": f"clients/{S}/build/locs/LD - {c}.md"} for pid, c in (("loc-a", "Aville"), ("loc-b", "Bville"))}
    st["build"] = {**(st.get("build") or {}), "batches": None}
    st["build"]["batches"] = [{"id": "locs", "kind": "location", "pages": ["loc-a", "loc-b"], "state": "drafts_written"}]
    sp.write_text(json.dumps(st))
    code, out = h.sh(f"python3 scripts/similarity.py {S} locs")
    h.check("CM-062: the cross-page check flags a sentence still true when the city is swapped, on the later page only",
            code == 1 and "1 too-similar sentence" in out and "loc-b ~ loc-a" in out and "Mill River" not in out
            and "rail depot" not in out and len(out.splitlines()) <= 10, out)
    code, out = h.sh(f"python3 scripts/similarity.py {S} locs --threshold 0.99")
    h.check("CM-062: the threshold is adjustable (config.json location_similarity_threshold, default 0.7)", code == 1 or "0 too-similar" in out, out)
    r = subprocess.run(["python3", "-c", "import sys, json; sys.path.insert(0, 'scripts'); import similarity; "
                        f"print(json.dumps(similarity.findings('{S}', 'locs')))"], cwd=h.SB, capture_output=True, text=True)
    f = json.loads(r.stdout or "[]")
    h.check("CM-062: each finding is a Fix (form: wording), keyed page + rule + item, rewritten in the one apply run",
            len(f) == 1 and f[0]["severity"] == "fix" and f[0]["category"] == "wording" and f[0]["rule"] == "LOC-31"
            and f[0]["page"] == "loc-b", (f, r.stderr[-300:]))


SCENARIOS = [t_location_spec, t_similarity]
