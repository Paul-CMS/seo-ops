"""machine.json — one Mac's own settings (git-ignored): a VA's Mac points at its own Drive for desktop
path and runs the stages without approving; Paul approves on his own Mac.

Run alone: python3 tests/run_all.py -k machine
"""
import json


def t_machine_settings(h):
    m = h.SB / "machine.json"
    h.sh('python3 scripts/status.py init mc-co --name "Mc Co" --domain mc.example --type full --industry roofing')
    try:
        other = h.SB / "va-drive" / "v3"
        (other / "Mc Co - TMS").mkdir(parents=True)
        m.write_text(json.dumps({"drive_local_root": str(other)}))
        code, out = h.sh("python3 scripts/drive.py where mc-co")
        h.check("machine.json drive_local_root overrides config.json's Drive path on this Mac",
                code == 0 and str(other / "Mc Co - TMS") in out, out)

        m.write_text(json.dumps({"can_approve": False}))
        code, out = h.paul("/approve mc-co entity_approved")
        h.check("machine.json can_approve:false → /approve is refused on this Mac (Paul approves on his own)",
                code != 0 and "does not approve" in out, out)
        code, out = h.sh("python3 scripts/records.py top mc-co")
        h.check("a Mac that cannot approve still runs the other scripts", code == 0, out)
    finally:
        m.unlink(missing_ok=True)
    code, out = h.sh("git check-ignore machine.json")
    h.check("machine.json is git-ignored (each Mac keeps its own)", code == 0, out)


SCENARIOS = [t_machine_settings]
