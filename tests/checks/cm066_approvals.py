"""CM-066 (Paul, 2026-10-25): Paul's own changes never throw approved work away."""


def t_paul_changes_keep_approval(h):
    """CM-066 (first-choice-seamless-gutters: brand_guide_approved approved 5 times): Paul's own answers and the
    system's write-back keep his approval; an Updated line records the change. An agent's hand edit still voids it."""
    S_ = "cm066-co"
    ag = h.build_ready(S_)
    bg = f"clients/{S_}/brand-guide.md"
    code, out = h.paul(f"/approve {S_} brand_guide_approved --files {bg}")   # a whole-file approval, as before CM-066
    h.check("CM-066 setup: Paul approves the whole Brand Guide", code == 0, out)
    h.new_session()
    rid = ag.start("answers")
    code, out = h.sh(f'python3 scripts/run.py fact {S_} {rid} --id d-insurance-bonded-status --value "Insured (Google '
                     f'review)" --status client_confirmed --source "Google review, confirmed by Paul"')
    text = (h.SB / bg).read_text()
    upd = text.split("## Updates since approval", 1)[-1]
    h.check("CM-066: a fact Paul gives after approving adds one dated Updated line to the Brand Guide",
            code == 0 and "## Updates since approval" in text and "- Updated " in upd and "Insurance / bonded status" in upd
            and "Insured (Google review)" in upd, (out, upd[:600]))
    rec = h.status(S_)["gates"]["brand_guide_approved"]
    code, out = h.sh(f"python3 scripts/status.py require {S_} brand_guide_approved")
    h.check("CM-066: ... and his approval stands (carried forward, logged), now covering the sections he decides",
            code == 0 and rec.get("carried") and all(f.startswith(bg + "#A+D+E") for f in rec["files"])
            and "APPROVAL KEPT" in (ag.c / "log.md").read_text(), (out, rec))
    code, out = h.sh(f'python3 scripts/run.py update {S_} {rid} --text "D2: insured may be written"')
    code2, out2 = h.sh(f"python3 scripts/status.py require {S_} brand_guide_approved")
    h.check("CM-066: a Brand Guide line Paul dictates is an Updated line too, and keeps the approval",
            code == 0 and "D2: insured may be written (by Paul)" in (h.SB / bg).read_text() and code2 == 0, (out, out2))
    p = h.SB / bg
    p.write_text(p.read_text() + "\n## Section C — Page inventory\n\n| /roof-repair/ | service |\n")
    code, out = h.sh(f"python3 scripts/status.py require {S_} brand_guide_approved")
    h.check("CM-066: the write-back's own sections (B3, C) never touch the approval", code == 0, out)
    p.write_text(p.read_text().replace("## Section E — Service area truth\n",
                                       "## Section E — Service area truth\nAn agent's own sentence about the area.\n"))
    code, out = h.sh(f"python3 scripts/status.py require {S_} brand_guide_approved")
    h.check("CM-066: an edit nobody recorded as Paul's (an agent's hand edit) still needs his re-approval",
            code == 4 and "changed after approval" in out, out)
    ag.fin(rid, "answers")
    n = h.nxt(S_)
    code, out = h.sh(f"python3 scripts/status.py require {S_} brand_guide_approved")
    h.check("CM-066 (CR-045): with Build under way, a Brand Guide needing re-approval never sends the client back to "
            "Stage 4 — Build carries on", code == 4 and not str(n.get("stage", "")).startswith("4") and "reconcile" not in n["command"]
            and "brand_guide_approved" not in n["command"].split(" --")[0].split()[2:3], n)
    code, out = h.sh(f"python3 scripts/status.py mark {S_} reconciled --file {bg}")
    marks = h.status(S_)["marks"]["reconciled"]["files"]
    h.check("CM-066: a reconciled mark on the whole guide covers the sections Paul decides, never B or C",
            code == 0 and list(marks) == [bg + "#A+D+E"], (out, marks))


SCENARIOS = [t_paul_changes_keep_approval]
