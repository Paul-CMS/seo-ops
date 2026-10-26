"""CM-068 (Paul, 2026-10-25): a client's service scope and process gap is filled with cited industry-standard text until
the client answers — never invented, never a client claim, never a hold."""
import importlib.util
import json
from pathlib import Path


def _rewrite3():
    spec = importlib.util.spec_from_file_location("cm068_rewrite3", Path(__file__).parent / "rewrite3.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def t_standard_fill(h):
    r3 = _rewrite3()
    S_ = "cm068-co"
    ag, code, out = r3.packs_client(h, S_)   # svc-roof-repair: service_scope is a client gap
    pid = "svc-roof-repair"
    req = json.loads((h.SB / "methodology" / "evidence-requirements.json").read_text())
    h.check("CM-068: only scope and process take a standard fill — never pricing, timeframes or the client's own claims",
            req.get("standard_fill") == ["page:service_scope", "page:service_process"])
    before = h.status(S_)["pages"][pid]["evidence"]
    ag.w(f"build/evidence/{pid}.standard.json", json.dumps({"standard": {
        "service_scope": [
            {"text": "A roof repair addresses a defined area: damaged shingles, flashing or underlayment around the leak.",
             "publisher": "Asphalt Roofing Manufacturers Association", "url": "https://www.asphaltroofing.org/", "read": "2026-10-25"},
            {"text": "An unsourced sentence that must never reach the writer.", "publisher": "nobody", "url": ""}],
        "pricing": [{"text": "Repairs cost $300.", "publisher": "x", "url": "https://example.com/"}]}}))
    h.new_session()
    rid = ag.start("build", "evidence", batch="pilot")
    code, out = h.sh(f"python3 scripts/evidence.py run {S_} --run {rid} --batch pilot")
    ag.fin(rid, "standard fill")
    st = h.status(S_)
    ev = st["pages"][pid]["evidence"]
    grid = (h.SB / ev["grid"]).read_text()
    h.check("CM-068: a cited standard fill is not a hold at the evidence gate (the grid says so)",
            code == 0 and "industry standard, 1 cited statement(s) (CM-068)" in grid
            and not any("required facts are not known" in w for w in ev.get("why") or []), (before, ev, grid[:900]))
    pack = (h.SB / st["pages"][pid]["pack"]["file"]).read_text()
    sec = pack.split("## Industry standard — until the client answers (CM-068)", 1)[-1].split("\n## ", 1)[0]
    h.check("CM-068: the pack gives the writer the cited statement, as trade practice, with its source",
            "## Industry standard — until the client answers (CM-068)" in pack and "damaged shingles" in sec
            and "asphaltroofing.org" in sec, sec[:600])
    h.check("CM-068: an unsourced statement never reaches the writer, and pricing is never filled",
            "unsourced sentence" not in pack and "Repairs cost $300" not in pack, sec[:600])
    wr = (h.SB / ".claude" / "agents" / "build.md").read_text() + (h.SB / ".claude" / "agents" / "researcher.md").read_text()
    h.check("CM-068: the writer writes it as trade practice (never the client's claim); the researcher cites official "
            "and trade sources only", "never as the client's own claim" in wr and "Industry standard (CM-068)" in wr
            and "Never a competitor's page" in wr, wr[-400:])


SCENARIOS = [t_standard_fill]
