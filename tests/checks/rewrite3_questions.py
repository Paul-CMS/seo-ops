"""Rewrite 3 §7: a question already answered is never asked again — the Apex replay (W16, synthetic_roofing_offered)."""
import json


def _log(h, S):
    return (h.SB / "clients" / S / "log.md").read_text(encoding="utf-8")


def t_unanswered_questions(h):
    S = "qa-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Qa Co" --domain qa.example --type full --industry roofing')
    ag = h.Agent(S)
    rid = ag.start("new-client")
    # W16: the question is open under the facts-interview key; the answer is recorded as a fact under another name
    code, out = h.sh(f'python3 scripts/run.py decision {S} {rid} --ask fact:d:services_subcontracted --who "Client (via Paul)" '
                     f'--text "Is Apex a subcontractor on new construction?"')
    code2, out2 = h.sh(f'python3 scripts/run.py fact {S} {rid} --id d-services-subcontracted-out --label "Services subcontracted out" '
                       f'--value "Yes, on new construction" --status paul_approved --source "Paul 2026-10-11 answer 16"')
    h.check("§7 (W16): recording the answer as a fact closes the open question asked under the facts-interview key",
            code == 0 and code2 == 0 and "closed open question(s): fact:d:services_subcontracted" in out2
            and "- CLOSED fact:d:services_subcontracted" in _log(h, S), (out, out2))
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    code, out = h.sh(f"python3 scripts/settled.py show {S}")
    h.check("§7 (W16): the register no longer lists it as waiting", "fact:d:services_subcontracted" not in
            out.split("Waiting")[-1] if "Waiting" in out else True, out[-400:])
    # the filter drops a question about it, whatever key the set uses
    qs = h.SB / "q.json"
    qs.write_text(json.dumps([{"key": "fact:d:services_subcontracted", "keys": ["fact:d:services_subcontracted"], "text": "Subcontracted?"},
                              {"key": "fact:d:warranty_terms", "text": "What is the warranty?"}]))
    code, out = h.sh(f"python3 scripts/settled.py filter {S} {qs}")
    kept = json.loads(out)["kept"]
    h.check("§7 (W16): a question set drops what a Known fact already answers by its name, and keeps the rest",
            [q["key"] for q in kept] == ["fact:d:warranty_terms"] and "services_subcontracted" in json.loads(out)["note"], out)
    h.sh(f'python3 scripts/run.py fact {S} {rid} --id d-insurance-bonded-status --label "Insurance bonded status" '
         f'--value "Insured" --status client_confirmed --source "certificate"')
    qs.write_text(json.dumps([{"key": "fact:d:insurance_bonded", "text": "Insured?"}]))
    code, out = h.sh(f"python3 scripts/settled.py filter {S} {qs}")
    h.check("§7: a question never opened is dropped too when a Known fact already answers it by name (the fact id is shown)",
            json.loads(out)["kept"] == [] and "d-insurance-bonded-status" in json.loads(out)["note"], out)
    # synthetic_roofing_offered: settled under another key, the old question left open (written before the relatedness rule)
    h.sh(f'python3 scripts/run.py decision {S} {rid} --ask synthetic_roofing_offered --who "Client (via Paul)" --text "Synthetic roofing offered?"')
    code, out = h.sh(f'python3 scripts/run.py decision {S} {rid} --settle synthetic_roofing --text "Paul: synthetic roofing is offered - yes"')
    h.check("§7: settling a related key without naming the open question is refused (existing rule holds)",
            code == 4 and "synthetic_roofing_offered" in out and "--closes" in out, out)
    log = h.SB / "clients" / S / "log.md"
    log.write_text(log.read_text() + "- SETTLED synthetic_roofing · 2026-10-09T13:53:44-05:00 · run old · by Paul · yes, offered\n")
    code, out = h.sh(f"python3 scripts/settled.py reconcile {S}")
    h.check("§7 (Port Royal): a legacy open question that a settled decision already answers is closed by the sweep",
            "synthetic_roofing_offered (by synthetic_roofing)" in out and "- CLOSED synthetic_roofing_offered" in _log(h, S), out)
    code, out = h.sh(f"python3 scripts/settled.py reconcile {S}")
    h.check("§7: the sweep is idempotent", "no open question is already answered" in out, out)
    # a question left open on purpose is kept
    h.sh(f'python3 scripts/run.py decision {S} {rid} --ask roof_pitch_known --who "Client (via Paul)" --text "What pitch?"')
    h.sh(f'python3 scripts/run.py decision {S} {rid} --settle roof_pitch --text "pitch recorded for two pages" --leaves-open "other pages still unknown"')
    code, out = h.sh(f"python3 scripts/settled.py reconcile {S}")
    h.check("§7: a question left open on purpose (--leaves-open) is not closed by the sweep", "roof_pitch_known" not in out, out)
    # asking again a question a settled decision answers is refused (the facts-interview key vs a settled name)
    h.sh(f'python3 scripts/run.py decision {S} {rid} --settle services_subcontracted_new_construction --text "yes"')
    code, out = h.sh(f'python3 scripts/run.py decision {S} {rid} --ask fact:d:services_subcontracted --who Paul --text "again?"')
    h.check("§7: a facts-interview key is not asked once a settled decision covers the same fact (by the fact's name)",
            code == 4 and "REFUSED" in out, out)
    h.sh(f'python3 scripts/run.py abort {S} {rid} --reason "test"')


def t_gsc_intake(h):
    """CR-024: the homepage's 90-day Search Console export is a standard intake document."""
    S = "gsc-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Gsc Co" --domain gsc.example --type full --industry roofing')
    h.sh(f"python3 scripts/records.py render {S}")
    cl = (h.SB / "clients" / S / "document-checklist.md").read_text(encoding="utf-8")
    h.check("CR-024: the document checklist asks for the Search Console homepage export, with how to get and name it",
            "## Intake documents" in cl and "- [ ] Search Console homepage queries, last 90 days — ask for it" in cl
            and "queries-homepage-90d" in cl, cl[:700])
    f = h.SB / "clients" / S / "inputs" / "Gsc Co - GSC - queries-homepage-90d - 2026-10-14.csv"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("query,clicks\nroofing,3\n")
    h.sh(f"python3 scripts/records.py render {S}")
    cl = (h.SB / "clients" / S / "document-checklist.md").read_text(encoding="utf-8")
    h.check("CR-024: once the file is in inputs/ the row is ticked", "- [x] Search Console homepage queries" in cl, cl[:500])
    entry = json.loads((h.SB / "methodology/data-manifest.json").read_text())["entries"]
    h.check("CR-024: the data manifest lists it and discovery:audit reads it",
            any(e["id"] == "gsc-homepage-90d" and "discovery:audit" in e["read_by"] for e in entry)
            and "GSC" in " ".join(json.loads((h.SB / "scripts/gates.json").read_text())["steps"]["discovery:audit"]["reads"]))


SCENARIOS = [t_unanswered_questions, t_gsc_intake]
