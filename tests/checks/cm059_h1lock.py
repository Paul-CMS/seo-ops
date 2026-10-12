"""CM-059 (CR-002, Paul 2026-10-12): the homepage H1 lock lifts only for a failing, unranked legacy H1 — Paul decides."""
import json


def t_h1_lock(h):
    h.sh('python3 scripts/status.py init h1-co --name "H1 Co" --domain h1.example --type full --industry roofing')
    ag = h.Agent("h1-co")
    ag.w("data/rankings/ranked-keywords.csv",
         "keyword,volume,url,position,type\n"
         "roofer beaufort sc,90,https://h1.example/,23,organic\n"
         "roofer beaufort sc,90,https://h1.example/,2,local_pack\n"
         "roof repair beaufort sc,70,https://h1.example/roof-repair/,4,organic\n"
         "roofing company beaufort,50,https://www.h1.example/,8,organic\n")
    ag.w("inputs/crawl/H1 Co - SF - internal_all - 2026-10-01.csv",
         '"Address","H1-1"\n"https://h1.example/","Welcome To Our Website"\n"https://h1.example/roof-repair/","Roof Repair"\n')
    ag.w("inputs/H1 Co - GSC - queries-homepage-90d - 2026-10-01.csv",
         "Top queries,Clicks,Impressions,CTR,Position\nroofer beaufort sc,4,300,1.3%,23\nroofing company beaufort,40,900,4%,8\n")
    gsc = "clients/h1-co/inputs/H1 Co - GSC - queries-homepage-90d - 2026-10-01.csv"
    chk = lambda kw, extra="": h.sh(f'python3 scripts/h1lock.py check h1-co --keyword "{kw}" --hp06 fail {extra}')

    code, out = chk("roofer beaufort sc", f'--gsc "{gsc}"')
    h.check("CM-059: H1 fails HP-06, organic #23 (local pack shown, not counted), 4 clicks < 10 → put to Paul, never automatic",
            code == 0 and "ALL THREE MET" in out and "Nothing changes unless he says so" in out and "organic #23" in out
            and "local pack #2 (shown, not counted)" in out and "4 clicks" in out
            and '"Welcome To Our Website"' in out, out)
    code, out = chk("roofing company beaufort", f'--gsc "{gsc}"')
    h.check("CM-059: in the organic top 10 (www. homepage row) → the lock holds", "LOCK HOLDS" in out and "organic #8" in out, out)
    code, out = h.sh(f'python3 scripts/h1lock.py check h1-co --keyword "roofer beaufort sc" --hp06 pass --gsc "{gsc}"')
    h.check("CM-059: an H1 that passes HP-06 stays locked", "LOCK HOLDS" in out and "fails HP-06" in out, out)
    code, out = chk("roofer beaufort sc")
    h.check("CM-059: no Search Console export → [NEED: …] and the lock holds (an unknown is not met)",
            "CANNOT TELL YET" in out and "[NEED: Search Console" in out, out)
    cfg_path = h.SB / "config.json"
    cfg = json.loads(cfg_path.read_text())
    old = json.dumps(cfg, indent=2)
    try:
        cfg["h1_lock_lift"]["few_clicks_90d"] = 3
        cfg_path.write_text(json.dumps(cfg, indent=2))
        code, out = chk("roofer beaufort sc", f'--gsc "{gsc}"')
        h.check("CM-059: 'few' comes from config.json (4 clicks is not under 3)", "LOCK HOLDS" in out and "under 3" in out, out)
    finally:
        cfg_path.write_text(old)

    ag.fin(ag.start("new-client"), "set up")
    rid = ag.start("wp-check")
    code, out = h.sh(f'python3 scripts/h1lock.py followup h1-co --run {rid} --keyword "roofer beaufort sc" '
                     f'--old-h1 "Welcome To Our Website" --changed 2026-10-12 --gsc "{gsc}"')
    h.sh("python3 scripts/worklist.py build h1-co")
    wl = (ag.c / "handoffs" / "VA-WORKLIST.csv")
    text = wl.read_text() if wl.exists() else ""
    h.check("CM-059: the 30-day check is a Manual lookups worklist row with the old H1, the baseline and the due date",
            code == 0 and "6 Manual lookups" in text and "Welcome To Our Website" in text and "2026-11-11" in text
            and "organic #23" in text and "4 clicks" in text, out + text[-600:])
    ag.fin(rid, "h1 follow-up")
    rul = (h.SB / "methodology" / "rulings.md").read_text()
    h.check("CM-059 is a numbered ruling and in the status table", "## CM-059 ·" in rul and "| CM-059 | APPROVED" in rul)


SCENARIOS = [t_h1_lock]
