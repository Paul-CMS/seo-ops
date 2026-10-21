"""Rewrite 4 Phase 6 — the shared research layers (plan §3): the niche module (angles.md + entities.json from Prompt A),
place identity from the Wikidata API, Prompt B built from the niche's angles at full or lite depth, the status order
(core GBP city first), and the brand footprint (Prompt C → sameAs and citation rows).

Proved with fake Deep Research reports and a faked Wikidata API (tests/fakes.py); the real Beaufort × stair lifts and
Charleston × roofing reports are run later by the VA. Run on HMM's saved site plan and Brand Guide (24 planned towns,
GBP city Beaufort) as in the Phase 5 checks."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rewrite4_phase5 import hmm_client   # noqa: E402

HEAD_A = "| id | entity or service | fact (one sentence) | source_url | publisher | source_type | date | quote (max 25 words) |\n|---|---|---|---|---|---|---|---|\n"
ASME, LIC, FAQ = "https://niche.example.org/asme", "https://niche.example.org/license", "https://niche.example.org/faq"
REPORT_A = f"""# Mobility equipment — niche and service entities

## 1. Category entity
{HEAD_A}| 1.1 | Mobility equipment supplier | Category entity: Mobility aid, Wikidata Q1001; variants: assistive device, mobility device. | https://en.wikipedia.org/wiki/Mobility_aid | Wikipedia | encyclopedia | 2026-01-10 | A mobility aid is a device designed to assist walking |

## 2. Service entities
{HEAD_A}| 2.1 | Stair Lifts | Stairlift is a distinct entity, Wikidata Q1000; variants: stair lift, chair lift. | https://en.wikipedia.org/wiki/Stairlift | Wikipedia | encyclopedia | 2026-01-10 | A stairlift is a mechanical device for lifting people up and down stairs |
| 2.2 | Porch Lifts | Porch lift is a type of Platform lift; Wikidata Q1002; variants: vertical platform lift. | https://en.wikipedia.org/wiki/Vertical_platform_lift | Wikipedia | encyclopedia | 2026-01-10 | A vertical platform lift is a type of platform lift |
| 2.3 | Hoists | A hoist is a distinct entity, Wikidata Q999999 (no such item). | https://en.wikipedia.org/wiki/Hoist_nowhere | Wikipedia | encyclopedia | 2026-01-10 | none |

## 3. Attributes
{HEAD_A}| 3.1 | Stair Lifts | ASME A18.1 is the safety standard that covers stairway chairlifts. | {ASME} | ASME | code body | 2024-05-01 | ASME A18.1 is the safety standard for platform lifts and stairway chairlifts |
| 3.2 | Stair Lifts | Installation takes about one day for a straight staircase. | {LIC} | State Board | official | 2024-05-01 | installers are licensed and the board has a lookup |
| 3.3 | Stair Lifts | A page that was removed said lifts last 20 years. | https://niche.example.org/gone | Maker | manufacturer | 2024-05-01 | lifts last 20 years |

## 4. State layer — SC
{HEAD_A}| 4.1 | Stair Lifts | The State Board of Contractors licenses lift installers under a limited-energy licence. | {LIC} | State Board | official | 2025-02-01 | licenses lift installers under a limited-energy licence |

## 5. Questions
{HEAD_A}| 5.1 | Stair Lifts | Does Medicare pay for a stair lift? | {FAQ} | Medicare | official | 2025-02-01 | Medicare Part B does not cover stair lifts |

## Not found
| section | searched |
|---|---|
| 4 | state funding programme for porch lifts |
"""

HEAD_B = "| id | fact (one sentence) | applies_to | source_url | publisher | source_type | date | short supporting quote |\n|---|---|---|---|---|---|---|---|\n"
GOV = "https://springfield.example.gov"
REPORT_LITE = f"""# Bluffton, SC — stair lifts (lite)

## 1. Local cost or decision
{HEAD_B}| 1.1 | Re-roofs need a permit; a lift install here is judged the same way by the town office. | all of Bluffton | {GOV}/permits | Town of Bluffton | official | 2025-03-01 | A roofing permit is required for any re-roof |

## 6. Places and entities
{HEAD_B}| 6.1 | Oak Park is a neighbourhood inside Bluffton. | all of Bluffton | {GOV}/hoa | Town of Bluffton | official | 2025-01-10 | The Oak Park HOA requires approval |

## 7. Identity
{HEAD_B}| 7.1 | Bluffton, SC; Wikidata ID Q999. | all of Bluffton | {GOV}/hoa | Wikidata | context | 2025-01-10 | The Oak Park HOA requires approval |

## 8. Questions people ask
{HEAD_B}| 8.1 | Do I need approval from the Oak Park HOA before a lift goes on my porch? | all of Bluffton | {GOV}/hoa | Local news | news | 2025-01-10 | The Oak Park HOA requires approval |
"""

HEAD_C = "| url | platform | name shown | address shown | phone shown | matches (yes/no/partly) | date | note |\n|---|---|---|---|---|---|---|---|\n"
REPORT_C = f"""# Footprint — Home Mobile Medical

{HEAD_C}| https://www.facebook.com/homemobilemed | Facebook | Home Mobile Medical | Beaufort, SC | (843) 476-1329 | yes | 2026-10-01 | |
| https://www.yelp.com/biz/home-mobile-medical | Yelp | Home Mobile Medical | 2127 Boundary St #5, Beaufort, SC 29902 | (843) 476-1329 | yes | 2026-10-01 | |
| https://www.hotfrog.com/company/hmm | Hotfrog | Home Mobile Medical | 2127 Boundary St #5, Beaufort, SC 29902 | (843) 555-0000 | yes | 2026-10-01 | |
| https://www.linkedin.com/company/home-mobile-medical | LinkedIn | Home Mobile Medical | Beaufort, SC | (843) 476-1329 | yes | 2026-10-01 | |
| https://www.manta.com/c/hmm | Manta | Home Mobile Medical | 2127 Boundary St #5, Beaufort, SC 29902 | (843) 476-1329 | yes | 2026-10-01 | |
| https://www.bbb.org/old-profile | BBB | Home Mobile Medical | 2127 Boundary St #5, Beaufort, SC 29902 | (843) 476-1329 | yes | 2026-10-01 | |
| https://sos.example.gov/hmm | Secretary of State registration | Home Mobile Medical, LLC | 2127 Boundary St #5, Beaufort, SC 29902 | | yes | 2026-10-01 | |
| https://thegazette.example/hmm-story | Local news | Home Mobile Medical | | | yes | 2026-09-01 | showroom story |
| | Former name | Home Mobility Medical LLC | | | no | 2019-03-01 | renamed in 2021 |

## Not found
| searched | result |
|---|---|
| Apple Maps place card | not found |
"""


def _hmm(h, slug, industry="stair lifts"):
    ag = hmm_client(h, slug)
    st = h.status(slug)
    st["client"]["industry"] = industry
    (ag.c / "status.json").write_text(json.dumps(st))
    return ag


def _env(h, fake):
    f = h.SB / "tests" / ".state" / "llm-fake.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(fake))
    return f"SEO_OPS_LLM_FAKE={f}"


def _put(h, rel, text):
    p = h.SB / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return rel


def t_niche_modules(h):
    out = {}
    for n in ("roofing", "stair-lifts", "mold-remediation"):
        code, o = h.sh(f"python3 -c \"import sys; sys.path.insert(0,'scripts'); import niches; m = niches.load_angles('{n}'); "
                       f"print(m['name'], len(m['full']), len(m['lite']), m['dir'].name)\"")
        out[n] = o.strip()
    h.check("niches: the three niches we have each carry an angles.md — five full angles and three lite angles",
            out["roofing"] == "Roofing 5 3 roofing" and out["stair-lifts"] == "Stair lifts and mobility equipment 5 3 stair-lifts"
            and out["mold-remediation"] == "Mold remediation 5 3 mold-remediation", out)
    code, o = h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import niches; "
                   "print(niches.load_angles('mobility-equipment-supplier')['dir'].name, niches.load_angles('water-damage-restoration')['dir'].name, "
                   "niches.load_angles('basket-weaving'))\"")
    h.check("niches: a client's niche slug finds its folder through the Aliases line; an unknown niche has none",
            o.strip() == "stair-lifts mold-remediation None", o)
    _put(h, "methodology/niches/bad-niche/angles.md",
         "# Bad\n\n## Full-depth angles\n### 1. Only\n- one\n### 2. Two\n- two\n\n## Lite angles\n### 1. A\n### 2. B\n### 3. C\n")
    code, o = h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import niches; niches.load_angles('bad-niche')\"")
    h.check("niches: a malformed angles.md (fewer than 3 full angles) is refused, never half used", code == 4 and "3 to 5 angles" in o, (code, o))
    (h.SB / "methodology/niches/bad-niche/angles.md").unlink()
    (h.SB / "methodology/niches/bad-niche").rmdir()
    code, o = h.sh("python3 scripts/niches.py list")
    h.check("niches: `niches.py list` shows each niche's module and that none is researched yet (no entities.json is invented)",
            "roofing" in o and "not researched yet" in o and "NO angles.md" not in o, o)


def t_prompt_b(h):
    S_ = "p6-promptb"
    _hmm(h, S_)
    code, full = h.sh(f'python3 scripts/places.py prompt {S_} "Beaufort, SC" --stdout')
    h.check("prompt B: the core GBP city gets the niche's five full-depth angles, then the fixed 6, 7 and 8",
            code == 0 and "1. Codes, permits and licensing for lift installation in Beaufort" in full
            and "3. Paying for it: programmes and funding that apply in Beaufort" in full and "5. Power, weather and service" in full
            and "6. Places and entities" in full and "8. Questions people in Beaufort ask" in full
            and "LITE run" not in full and "{" not in full, full[:1500])
    h.check("prompt B: the angles are the niche's, not roofing's — no roofing angle in a stair-lift prompt",
            "Permits and approvals for" not in full and "roofing" not in full.lower() and "Medicare" in full, "")
    code, lite = h.sh(f'python3 scripts/places.py prompt {S_} "Bluffton, SC" --stdout')
    h.check("prompt B: every other planned town is lite — the three FAQ-category angles, then 6, 7 and 8, no angle 4 or 5",
            code == 0 and "LITE run" in lite and "1. Local cost or decision" in lite and "3. Trust in this area" in lite
            and "Care ecosystem" not in lite and "6. Places and entities" in lite and "8. Questions people in Bluffton ask" in lite
            and "{" not in lite, lite[:1200])
    h.check("prompt B: lite keeps the frame's rules and the import format", "Every fact needs its own source URL" in lite
            and "Output format (required, used for import)" in lite and "Not found" in lite)
    code, out = h.sh(f'python3 scripts/places.py prompt {S_} "Beaufort, SC"')
    h.check("prompt B: the printed line names the depth and why (the core GBP city), in at most 10 lines",
            "full depth (core GBP city" in out and len(out.splitlines()) <= 10, out)
    code, out = h.sh(f'python3 scripts/places.py prompt {S_} "Bluffton, SC"')
    h.check("prompt B: the printed line names lite and why (every other planned town)", "lite depth (every other planned town" in out, out)
    code, o = h.sh(f'python3 scripts/places.py prompt {S_} "Bluffton, SC" --depth full --stdout')
    code2, o2 = h.sh(f'python3 scripts/places.py prompt {S_} "Beaufort, SC" --depth lite --stdout')
    h.check("prompt B: --depth overrides the automatic choice either way", "LITE run" not in o and "5. Power, weather" in o
            and "LITE run" in o2, "")
    # a niche with no module is refused, never built from another trade's angles
    _hmm(h, "p6-nomodule", industry="basket weaving")
    code, out = h.sh('python3 scripts/places.py prompt p6-nomodule "Beaufort, SC"')
    h.check("prompt B: a niche with no angles.md is refused, and says where it goes", code == 4 and "no niche module" in out
            and "angles.md" in out, out)
    # the roofing niche still reads its own module (and still fills every placeholder)
    code, out = h.sh("python3 scripts/places.py prompt p6-roof Springfield --stdout --state SC")
    ag = h.build_ready("p6-roof2")
    code, out = h.sh("python3 scripts/places.py prompt p6-roof2 Springfield --stdout --state SC")
    h.check("prompt B: a roofing client's prompt is built from methodology/niches/roofing/angles.md",
            code == 0 and "1. Permits and approvals for roofing work in Springfield" in out and "{" not in out
            and "roofing" in out.lower(), out[:400])
    code, out = h.sh("python3 scripts/places.py prompt p6-roof2 Springfield --stdout --state SC")


def t_status_order(h):
    S_ = "p6-status"
    _hmm(h, S_)
    code, out = h.sh(f"python3 scripts/places.py status {S_}")
    lines = [l for l in out.splitlines() if re.match(r"^\s+\d+\. ", l)]
    h.check("status: 24 planned towns, the core GBP city named from the Brand Guide's confirmed NAP",
            "24 planned place(s)" in out.splitlines()[0] and "core GBP city: Beaufort" in out.splitlines()[0], out[:300])
    h.check("status: the core GBP city is first and marked full depth; every other town is lite",
            lines and lines[0].lstrip().startswith("1. Beaufort, SC [core GBP city · full]")
            and all("[lite]" in l for l in lines[1:]) and len(lines) == 8, lines[:3])
    st = h.status(S_)
    expect, seen = [], set()
    batches = (st.get("build") or {}).get("batches") or []
    first = {}
    for i, b in enumerate(batches):
        for pid in b.get("pages", []):
            first.setdefault(pid, i)
    rows = sorted((first.get(pid, len(batches)), n, p["name"]) for n, (pid, p) in enumerate(st["pages"].items())
                  if p.get("type") == "location" and p["name"] != "Beaufort, SC")
    expect = [r[2] for r in rows]
    md = (h.SB / "clients" / S_ / "build/places/status.md").read_text()
    order = re.findall(r"^\d+\. (.+?) \[", md, re.M)
    h.check("status: after the core city the towns follow the planned pages' priority (build batches, then the plan's order)",
            order[0] == "Beaufort, SC" and order[1:] == expect and len(order) == 24, (order[:5], expect[:5]))
    h.check("status: it points at the free Wikidata identity step", "identity-all" in out and "identity-all" in md, out)
    code, out2 = h.sh(f"python3 scripts/places.py status {S_}")
    h.check("status: without a niche module it says so", "NO niche module" not in out)
    _hmm(h, "p6-status2", industry="basket weaving")
    code, out3 = h.sh("python3 scripts/places.py status p6-status2")
    h.check("status: a niche with no module is called out on the first line", "NO niche module for 'basket-weaving'" in out3.splitlines()[0], out3)


def t_identity(h):
    S_ = "p6-ident"
    _hmm(h, S_)
    code, out = h.sh("python3 tests/fakes.py places identity SC Beaufort")
    pl = json.loads((h.SB / "methodology/places/sc/beaufort/place.json").read_text())["identity"]
    h.check("identity: Beaufort, SC is the Wikidata item inside South Carolina — never the North Carolina Beaufort or the county",
            code == 0 and pl["wikidata"] == "Q1000102" and pl["official_name"] == "Beaufort" and pl["county"] == "Beaufort County"
            and pl["wikipedia"] == "https://en.wikipedia.org/wiki/Beaufort,_South_Carolina"
            and pl["website"] == "https://cityofbeaufort.example.gov" and pl["source"] == "wikidata-api" and pl["other_matches"] == 0,
            (out, pl))
    h.check("identity: the Russian Doll chain runs place → county → state → country, with its Wikidata IDs",
            [(c["name"], c["type"]) for c in pl["chain"]] == [("Beaufort", "place"), ("Beaufort County", "county"),
                                                              ("South Carolina", "state"), ("United States of America", "country")]
            and [c["wikidata"] for c in pl["chain"]] == ["Q1000102", "Q2000102", "Q3000102", "Q30"]
            and "Beaufort → Beaufort County → South Carolina" in out and len(out.splitlines()) <= 3, (out, pl["chain"]))
    code, out = h.sh("python3 tests/fakes.py places identity SC Bluffton")
    bl = json.loads((h.SB / "methodology/places/sc/bluffton/place.json").read_text())["identity"]
    h.check("identity: a town in two counties keeps both (the chain follows the first)",
            [c["name"] for c in bl["counties"]] == ["Beaufort County", "Jasper County"] and bl["county"] == "Beaufort County", bl)
    code, out = h.sh("python3 tests/fakes.py places identity SC Atlantis")
    h.check("identity: no confident match is said plainly and stores nothing", code == 4 and "no Wikidata item named Atlantis" in out
            and not (h.SB / "methodology/places/sc/atlantis").exists(), (code, out))
    # a Deep Research report names another Wikidata ID: shown, not silently kept
    _put(h, f"clients/{S_}/inputs/places/bluffton-stair-lifts.md", REPORT_LITE)
    code, out = h.sh(f"python3 scripts/places.py ingest {S_} clients/{S_}/inputs/places/bluffton-stair-lifts.md")
    bl = json.loads((h.SB / "methodology/places/sc/bluffton/place.json").read_text())["identity"]
    h.check("identity: a report ingested later does not overwrite the API's identity — its different Wikidata ID is shown beside it",
            code == 0 and bl["wikidata"] == "Q1000201" and bl["source"] == "wikidata-api" and bl["report_wikidata"] == "Q999", (out, bl))
    code, out = h.sh("python3 tests/fakes.py places identity SC Bluffton")
    bl = json.loads((h.SB / "methodology/places/sc/bluffton/place.json").read_text())["identity"]
    h.check("identity: running it again after the report flags the conflict in the identity record and the line",
            bl["wikidata"] == "Q1000201" and bl.get("report_wikidata") == "Q999" and "the report named Q999" in out, (out, bl))
    # all planned places
    code, out = h.sh(f"python3 tests/fakes.py places identity-all {S_}")
    h.check("identity-all: fills every planned place it can, skipping the done ones, and counts the rest",
            code == 0 and "Beaufort: " not in out.split("identity:")[0].replace("Beaufort, SC: no Wikidata", "")
            and "identity: 0 filled from Wikidata · 22 not found" in out.splitlines()[-1], out)
    code, out = h.sh(f"python3 scripts/places.py status {S_}")
    h.check("status: identity not yet filled is counted per place", "identity from Wikidata (free, no LLM) not filled for 22 place(s)" in out, out)


def t_prompt_b_lite_ingest(h):
    S_ = "p6-lite"
    _hmm(h, S_)
    _put(h, f"clients/{S_}/inputs/places/okatie-stair-lifts.md", REPORT_LITE.replace("Bluffton", "Okatie"))
    code, out = h.sh(f"python3 scripts/places.py ingest {S_} clients/{S_}/inputs/places/okatie-stair-lifts.md")
    store = h.SB / "methodology/places/sc/okatie"
    place = json.loads((store / "place.json").read_text())
    niche = json.loads((store / "stair-lifts.json").read_text())
    h.check("lite ingest: the lite angles 1 to 3 route to the place × niche layer, 6 and 7 to the place layer, 8 to the FAQ questions",
            code == 0 and [f["id"] for f in niche["facts"]] == ["1.1"] and {f["id"] for f in place["facts"]} == {"6.1", "7.1"}
            and "Oak Park HOA" in niche["questions"][0]["question"] and place["identity"]["wikidata"] == "Q999", (out, niche["facts"]))
    code, out = h.sh("python3 tests/fakes.py places verify SC Okatie stair-lifts")
    niche = json.loads((store / "stair-lifts.json").read_text())
    h.check("lite ingest: the same verification as a full run — the quote is on the page, so the fact is verified",
            niche["facts"][0]["verified"] is True and "3 verified" in out, (out, niche["facts"]))
    code, out = h.sh(f"python3 scripts/places.py status {S_}")
    h.check("status: a town with its place and niche research is off the list, the rest stay", "Okatie, SC [" not in out
            and "Hilton Head Island, SC [lite]" in out and "missing research" in out, out)


def t_niche_ingest(h):
    S_ = "p6-niche"
    ag = _hmm(h, S_)
    code, out = h.sh(f"python3 scripts/niches.py prompt {S_}")
    pa = (h.SB / "clients" / S_ / "build/niches/stair-lifts-prompt-a.md")
    txt = pa.read_text() if pa.exists() else ""
    h.check("prompt A: filled from the Brand Guide's GBP category, the site plan's services and the state; no placeholder left; the "
            "printed line is at most 10 lines",
            code == 0 and "{" not in txt and '"Mobility equipment supplier"' in txt and "Stair Lifts" in txt and "State layer for SC" in txt
            and "mapping the stair lifts industry" in txt and len(out.splitlines()) <= 10 and "Gemini Deep Research" in out, (out, txt[:400]))
    _put(h, f"clients/{S_}/inputs/niches/stair-lifts.md", REPORT_A)
    code, out = h.sh(f"python3 scripts/niches.py ingest {S_} clients/{S_}/inputs/niches/stair-lifts.md")
    ent_p = h.SB / "methodology/niches/stair-lifts/entities.json"
    d = json.loads(ent_p.read_text())
    by = {e["name"]: e for e in d["entities"]}
    h.check("niche ingest: the category entity, each service entity with its Wikidata ID, Wikipedia URL, variants and parent/child",
            code == 0 and d["category"]["wikidata"] == "Q1001" and d["category"]["name"] == "Mobility equipment supplier"
            and "assistive device" in d["category"]["variants"]
            and by["Stair Lifts"]["wikidata"] == "Q1000" and by["Stair Lifts"]["wikipedia"].endswith("/Stairlift")
            and "stair lift" in by["Stair Lifts"]["variants"] and by["Stair Lifts"]["kind"] == "distinct"
            and by["Porch Lifts"]["parent"] == "Platform lift" and by["Porch Lifts"]["kind"] == "sub-type", (out, d["entities"]))
    f = {x["id"]: x for x in d["facts"]}
    h.check("niche ingest: attributes and the state layer keep their fields; the state fact carries the state; questions are listed; "
            "the not-found table is kept",
            f["3.1"]["section"] == "attributes" and f["3.1"]["entity"] == "Stair Lifts" and f["4.1"]["section"] == "state"
            and f["4.1"]["state"] == "SC" and f["3.1"]["state"] == "" and d["questions"][0]["question"].startswith("Does Medicare")
            and d["not_found"][0]["section"] == "4", (f.keys(), d["not_found"]))
    code, out2 = h.sh(f"python3 scripts/niches.py ingest {S_} clients/{S_}/inputs/niches/stair-lifts.md")
    d2 = json.loads(ent_p.read_text())
    h.check("niche ingest: ingesting the same report again adds nothing", "0 entit(ies) · 0 fact(s) · 0 question(s)" in out2
            and len(d2["facts"]) == len(d["facts"]) and len(d2["entities"]) == len(d["entities"]), out2)
    code, out = h.sh("python3 tests/fakes.py niches verify stair-lifts")
    d = json.loads(ent_p.read_text())
    f = {x["id"]: x for x in d["facts"]}
    by = {e["name"]: e for e in d["entities"]}
    h.check("niche verify: a quote found on its page is verified; a page that does not load is dropped, never asked; a paraphrase waits "
            "for the meaning check — the same as the place store",
            f["3.1"]["verified"] is True and f["4.1"]["verified"] is True and "3.3" not in f and f["3.2"]["verified"] == "check"
            and any(x["id"] == "3.3" and "URL did not load" in x["reason"] for x in d["dropped"]), (out, [(k, v["verified"]) for k, v in f.items()]))
    h.check("niche verify: an entity's Wikidata ID is checked against the Wikidata API — a matching label is confirmed, a different "
            "label waits for Paul's researcher, an ID that does not exist is cleared, a Wikipedia page that does not load is cleared",
            by["Stair Lifts"]["wikidata_ok"] is True and by["Stair Lifts"]["wikipedia_ok"] is True
            and by["Porch Lifts"]["wikidata_ok"] == "check" and by["Porch Lifts"]["wikidata_label"] == "Wheelchair elevator"
            and by["Hoists"]["wikidata"] == "" and by["Hoists"]["wikipedia"] == ""
            and d["category"]["wikidata_ok"] == "check", (by["Porch Lifts"], by["Hoists"]))
    code, shown = h.sh("python3 scripts/niches.py show stair-lifts --check")
    h.check("niche show --check: lists the fact left for the meaning check and the entity label to settle",
            "3.2 [check]" in shown and "Porch Lifts" in shown and "Wheelchair elevator" in shown, shown)
    # the meaning check on the API (niche-judge), then its fallback
    rid = ag.start("build", "facts")
    code, out = h.sh(f"python3 tests/fakes.py niches judge-all stair-lifts --slug {S_} --run {rid}")
    h.check("niche judge-all: with no API key it says so and leaves the fact for the researcher (never fails)",
            code == 0 and "no API key" in out, out)
    fake = {"niche-judge": {"items": {"3.2": {"verdict": "supported", "reason": "'installers are licensed'"}}}}
    code, out = h.sh(f"{_env(h, fake)} python3 tests/fakes.py niches judge-all stair-lifts --slug {S_} --run {rid}")
    d = json.loads(ent_p.read_text())
    f = {x["id"]: x for x in d["facts"]}
    h.check("niche judge-all: supported → verified on the API (Sonnet), the client's run pays",
            code == 0 and f["3.2"]["verified"] is True and "llm.py niche-judge" in f["3.2"]["verified_how"] and "1 verified" in out
            and "niche-judge" in (h.SB / "clients" / S_ / "llm-costs.jsonl").read_text(), (out, f["3.2"]))
    code, out = h.sh("python3 scripts/niches.py entity stair-lifts \"Porch Lifts\" --drop-wikidata")
    d = json.loads(ent_p.read_text())
    h.check("niche entity: a label the researcher rejects clears the identifier", code == 0
            and {e["name"]: e for e in d["entities"]}["Porch Lifts"]["wikidata"] == "", out)
    code, out = h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import niches; "
                     "print(sorted(f['id'] for f in niches.usable('stair-lifts','SC')), sorted(f['id'] for f in niches.usable('stair-lifts','GA')))\"")
    h.check("niche usable(): verified, current facts only — the state layer is returned for its own state only",
            out.strip() == "['3.1', '3.2', '4.1'] ['3.1', '3.2']" or out.strip().startswith("['2.1'") or "4.1" in out.split("] [")[0]
            and "4.1" not in out.split("] [")[1], out)
    log = h.sh("git log --format=%s -n 12")[1]
    h.check("the niche store is committed on its own, only the niche's folder", "niches: ingested Prompt A — stair-lifts" in log
            and "niches: verified — stair-lifts" in log, log)
    h.check("the niche store has no hand-made entities.json: only the ingest wrote it (the repo holds angles.md alone)",
            not (Path(__file__).resolve().parents[2] / "methodology/niches/stair-lifts/entities.json").exists(), "")


def t_footprint(h):
    S_ = "p6-foot"
    _hmm(h, S_)
    bg = h.SB / "clients" / S_ / "brand-guide.md"
    before = bg.read_text()
    code, out = h.sh(f"python3 scripts/footprint.py prompt {S_}")
    pc = (h.SB / "clients" / S_ / "build/footprint/prompt-c.md").read_text()
    h.check("prompt C: filled from the Brand Guide — brand, confirmed address, phone, website; nothing left unfilled",
            code == 0 and "{" not in pc and '"Home Mobile Medical"' in pc and "2127 Boundary St #5, Beaufort, SC 29902" in pc
            and "(843) 476-1329" in pc and "https://homemobilemedical.com" in pc and len(out.splitlines()) <= 10, (out, pc[:300]))
    _put(h, f"clients/{S_}/inputs/footprint/report.md", REPORT_C)
    code, out = h.sh(f"python3 tests/fakes.py footprint ingest {S_} clients/{S_}/inputs/footprint/report.md")
    d = json.loads((h.SB / "clients" / S_ / "data/footprint/footprint.json").read_text())
    h.check("footprint ingest: sameAs candidates are the profiles that load, show the brand's name and match the NAP — and only those",
            code == 0 and d["sameas"] == ["https://www.facebook.com/homemobilemed", "https://www.yelp.com/biz/home-mobile-medical"], (out, d["sameas"]))
    h.check("footprint ingest: the script re-checks the report's own 'matches' — a listing with another phone number is a NAP issue, "
            "whatever the report said, with exactly what differs",
            len(d["nap_issues"]) == 1 and d["nap_issues"][0]["url"].endswith("hotfrog.com/company/hmm")
            and "phone shown (843) 555-0000, confirmed (843) 476-1329" in d["nap_issues"][0]["diff"][0], d["nap_issues"])
    h.check("footprint ingest: a URL that does not load is dropped, never asked; a site that blocks robots, or a page without the name, "
            "is listed to open by hand instead of proposed",
            [x["url"] for x in d["dropped"]] == ["https://www.bbb.org/old-profile"] and "URL did not load" in d["dropped"][0]["reason"]
            and sorted(d["open_by_hand"]) == ["https://www.linkedin.com/company/home-mobile-medical", "https://www.manta.com/c/hmm"],
            (d["dropped"], d["open_by_hand"]))
    h.check("footprint ingest: a registry record and a news mention are kept but never proposed for sameAs; a former name is a history row",
            "https://sos.example.gov/hmm" not in d["sameas"] and "https://thegazette.example/hmm-story" not in d["sameas"]
            and {r["url"]: r["class"] for r in d["rows"]}["https://sos.example.gov/hmm"] == "registry"
            and {r["url"]: r["class"] for r in d["rows"]}["https://thegazette.example/hmm-story"] == "mention"
            and d["history"][0]["what"] == "Former name" and d["history"][0]["value"] == "Home Mobility Medical LLC"
            and d["not_found"][0]["what"] == "Apple Maps place card", (d["history"], d["not_found"]))
    prop = (h.SB / "clients" / S_ / "build/footprint/section-f-proposal.md").read_text()
    h.check("footprint ingest: the proposal gives Section F's rows ready for Paul — citation list, social list, Apple Maps (a [NEED] when none "
            "was found) — plus the NAP check and the history rows",
            "| Full citation list → sameAs | https://www.yelp.com/biz/home-mobile-medical | Internally Verified (Prompt C, " in prop
            and "| Social profile list | https://www.facebook.com/homemobilemed |" in prop and "| Apple Maps link → sameAs | [NEED] | Unknown |" in prop
            and "phone shown (843) 555-0000" in prop and "Former name: Home Mobility Medical LLC" in prop
            and "Proposal only" in prop, prop)
    h.check("footprint ingest: the Brand Guide is untouched — the system proposes, Paul approves", bg.read_text() == before)
    code, out = h.sh(f"python3 scripts/footprint.py show {S_}")
    h.check("footprint show: one line and the sameAs list", "sameAs 2" in out and "sameAs https://www.yelp.com" in out, out)


SCENARIOS = [t_niche_modules, t_prompt_b, t_status_order, t_identity, t_prompt_b_lite_ingest, t_niche_ingest, t_footprint]
