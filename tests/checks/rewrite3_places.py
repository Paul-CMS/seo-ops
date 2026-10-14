"""Rewrite 3 §5: the place research store, the Deep Research flow, verification, and its use in evidence packs."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rewrite3 import packs_client   # noqa: E402

HEAD = "| id | fact (one sentence) | applies_to | source_url | publisher | source_type | date | short supporting quote |\n|---|---|---|---|---|---|---|---|\n"
GOV = "https://springfield.example.gov"
REPORT = f"""# Springfield, SC — roofing

## 1. Permits and approvals
{HEAD}| 1.1 | A roofing permit is required for any re-roof in Springfield. | all of Springfield | {GOV}/permits | City of Springfield | official | 2025-03-01 | A roofing permit is required for any re-roof |
| 1.2 | Repairs under 25 percent of a roof need no permit. | all of Springfield | {GOV}/permits | City of Springfield | official | 2025-03-01 | Repairs under 25 percent of the roof do not need one |

## 2. Community and design rules
{HEAD}| 2.1 | Oak Park HOA must approve roof colours. | Oak Park | {GOV}/hoa | Oak Park HOA | official | 2025-01-10 | roof colours need prior HOA sign-off |
| 2.2 | A county page says something else. | unincorporated Springfield County | {GOV}/missing | County | official | 2025-01-10 | anything |

## 3. Environment
{HEAD}| 3.1 | Design wind speed is 150 mph. | all of Springfield | {GOV}/wind | State code body | code body | 2019-05-01 | Design wind speed in Springfield is 150 mph |

## 6. Places and entities
{HEAD}| 6.1 | Oak Park is a neighbourhood inside Springfield. | all of Springfield | {GOV}/hoa | City of Springfield | official | 2025-01-10 | The Oak Park HOA requires approval |

## 7. Identity
{HEAD}| 7.1 | Springfield, SC; Wikidata ID Q123456. | all of Springfield | {GOV}/hoa | Wikidata | context | 2025-01-10 | The Oak Park HOA requires approval |

## 8. Questions people ask
{HEAD}| 8.1 | Does the Oak Park HOA need to approve a new roof colour? | all of Springfield | {GOV}/hoa | Local news | news | 2025-01-10 | The Oak Park HOA requires approval |

## Not found
| angle | what was searched |
|---|---|
| 5 | state and utility roofing rebates |
"""


def t_places(h):
    S_ = "r3-places-co"
    ag, code, out = packs_client(h, S_)
    bg = h.SB / "clients" / S_ / "brand-guide.md"
    bg.write_text(bg.read_text() + "\nService area: Springfield, South Carolina.\n")
    code, out = h.sh(f"python3 scripts/places.py prompt {S_} Springfield")
    pf = h.SB / "clients" / S_ / "build/places/prompts/springfield-roofing.md"
    pt = pf.read_text() if pf.exists() else ""
    h.check("§5.2: places.py prompt fills the template from the Brand Guide and the site plan, and prints at most 10 lines",
            code == 0 and "{" not in pt and "Springfield, SC" in pt and "LOCAL research" in pt and "Wikidata ID" in pt
            and len(out.splitlines()) <= 10 and "Gemini Deep Research" in out, (out, pt[:300]))
    code, out = h.sh(f"python3 scripts/places.py prompt {S_} Springfield --stdout")
    h.check("§5.3: --stdout prints the whole prompt, angles 1 to 8 and the output format",
            "8. Questions people in Springfield ask" in out and "Output format (required, used for import)" in out, out[-300:])
    rp = h.SB / "clients" / S_ / "inputs/places/springfield-roofing.md"
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(REPORT)
    code, out = h.sh(f"python3 scripts/places.py ingest {S_} clients/{S_}/inputs/places/springfield-roofing.md")
    store = h.SB / "methodology/places/sc/springfield"
    place = json.loads((store / "place.json").read_text())
    niche = json.loads((store / "roofing.json").read_text())
    h.check("§5.1/§5.2: ingest routes angles 1, 2 and 3 to the niche layer, 6 and 7 to the place layer, 8 to the FAQ questions",
            code == 0 and {f["id"] for f in niche["facts"]} == {"1.1", "1.2", "2.1", "2.2", "3.1"}
            and {f["id"] for f in place["facts"]} == {"6.1", "7.1"}
            and niche["questions"] and "Oak Park HOA" in niche["questions"][0]["question"], (out, niche["facts"]))
    h.check("§5.1: each fact carries its fields; applies_to is normalised; an unincorporated fact stays marked",
            all(k in niche["facts"][0] for k in ("fact", "applies_to", "source_url", "publisher", "source_type", "date",
                                                  "quote", "verified", "added"))
            and niche["facts"][0]["applies_to"] == "all" and niche["facts"][2]["applies_to"] == "Oak Park"
            and niche["facts"][3]["applies_to"] == "unincorporated", niche["facts"])
    h.check("§5.2: the place layer keeps the Wikidata identity, the niche layer the Not-found table",
            place["identity"].get("wikidata") == "Q123456" and niche["not_found"][0]["angle"] == "5", (place["identity"], niche["not_found"]))
    code, out = h.sh(f"python3 scripts/places.py ingest {S_} clients/{S_}/inputs/places/springfield-roofing.md")
    niche2 = json.loads((store / "roofing.json").read_text())
    h.check("§5: ingesting the same report again adds nothing (research is stored once)", "0 roofing fact(s)" in out
            and len(niche2["facts"]) == len(niche["facts"]), out)
    h.check("§5.1: a fact older than 3 years is marked stale", next(f for f in niche["facts"] if f["id"] == "3.1")["stale"])
    code, out = h.sh("python3 tests/fakes.py places verify SC Springfield roofing")
    niche = json.loads((store / "roofing.json").read_text())
    by = {f["id"]: f for f in niche["facts"]}
    h.check("§5.2: verify — a URL that loads with the quote on the page is verified; one that does not load is dropped, not asked; "
            "a quote not found word for word waits for the Sonnet meaning check",
            by["1.1"]["verified"] is True and by["1.2"]["verified"] is True and "2.2" not in by
            and niche["dropped"][0]["id"] == "2.2" and "URL did not load" in niche["dropped"][0]["reason"]
            and by["2.1"]["verified"] == "check" and len(out.splitlines()) <= 10, (out, by))
    code, out = h.sh("python3 tests/fakes.py places judge SC Springfield roofing --id 2.1 --ok --reason 'page says approval before work'")
    code2, out2 = h.sh("python3 scripts/places.py show SC Springfield roofing --check")
    h.check("§5.2: the Sonnet pass records its answer per fact (judge), and `show --check` lists what is left",
            code == 0 and "verified" in out and "2.1" not in out2, (out, out2))
    log = h.sh("git log --format=%s -n 5")[1]
    h.check("§5: the store is committed on its own, with only the place's folder", "places: " in log, log)
    # use in an evidence pack: verified and current only
    code, out = h.sh(f"python3 scripts/evidence_pack.py build {S_} pilot --page loc-springfield")
    pk = (h.SB / h.status(S_)["pages"]["loc-springfield"]["pack"]["file"]).read_text()
    place_sec = pk.split("## Place research", 1)[-1].split("## Settled", 1)[0]
    h.check("§2.2/§5: the pack holds the verified place and place × niche facts, with source and tier, and leaves out a stale "
            "or unverified one", "A roofing permit is required" in place_sec and "[official]" in place_sec
            and "Oak Park HOA must approve" in place_sec and "150 mph" not in place_sec, place_sec[:900])
    code, out = h.sh(f"python3 scripts/places.py status {S_}")
    h.check("§5.2: status lists planned places without research, with the prompt command for each, and not the one done",
            "Springfield" not in out.split("\n", 1)[-1] or "Springfield: missing" not in out, out)
    # the research minimum now includes the place store
    rid = ag.start("build", "facts")
    code, out = h.sh(f"python3 scripts/research.py log {S_} --run {rid} --section pilot --gap fact:loc-springfield:x --kind public "
                     f"--page loc-springfield --result not_found --queries 'a || City of Springfield b || c' "
                     f"--sources 'methodology/sources/sc-lowcountry.md || Wikipedia: Springfield'")
    h.check("§3.2: a public 'not found' without the place store tried is refused", code == 4 and "place store" in out, out)
    code, out = h.sh(f"python3 scripts/research.py log {S_} --run {rid} --section pilot --gap fact:loc-springfield:y --kind public "
                     f"--page loc-springfield --result not_found --queries 'a || City of Springfield b || c || d || e || f || g' "
                     f"--sources 'methodology/places/ || methodology/sources/sc-lowcountry.md || Wikipedia: Springfield'")
    h.check("§3.2: a gap uses at most 6 searches — a log with more is refused", code == 4 and "at most 6" in out, out)
    h.sh(f'python3 scripts/run.py abort {S_} {rid} --reason "test"')


SCENARIOS = [t_places]
