"""CM-067 (Paul, 2026-10-25, first-choice-seamless-gutters): Paul's words carry from one chat to the next; a draft
changes only inside a run and is recorded again in it."""
import importlib.util
from pathlib import Path


def _rewrite3():
    spec = importlib.util.spec_from_file_location("cm067_rewrite3", Path(__file__).parent / "rewrite3.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def t_carry_and_revise(h):
    r3 = _rewrite3()
    S_ = "cm067-co"
    ag, code, out = r3.packs_client(h, S_)
    h.new_session()
    rid = ag.start("build", "write", batch="pilot")
    r3.write_pilot(h, ag, S_, rid)
    sem = ag.w("build/Test Co - Semantic Review - pilot - REVIEW.md", "| ID | Check |\n|---|---|\n")
    h.sh(f"python3 scripts/status.py batch {S_} pilot --state drafts_written --sem-table '{sem}' --sem-findings 0")
    ag.fin(rid, "pilot written")
    st = h.status(S_)   # a CM-061 section (like the gutters services): its one review sheet answered and applied
    b = next(x for x in st["build"]["batches"] if x["id"] == "pilot")
    b["review"] = {"drafts": {"sheet": "x.csv", "applied": {"at": "2026-10-25T00:00:00-05:00", "ts": 1.0}}}
    (ag.c / "status.json").write_text(__import__("json").dumps(st))
    pid = ag.batch_pages("pilot")[0]
    d = h.SB / f"clients/{S_}/build/pilot/D-{pid}.md"
    d.write_text(d.read_text() + "\nA line Paul gave in chat, pasted in outside any run.\n")
    n = h.nxt(S_)
    h.check("CM-067: a draft edited after it was recorded sends /next to a revision run, not to a refused approval",
            n["kind"] == "run" and n["command"] == f"/build {S_} revise pilot" and pid in n["why"], n)
    h.new_session()   # another chat: the revision run is allowed in any chat
    rid = ag.start("build", "revise", batch="pilot")
    code, out = h.sh(f"python3 scripts/status.py page-stage {S_} {pid} --stage draft --file "
                     f"'clients/{S_}/build/pilot/D-{pid}.md' --run {rid}")
    h.check("CM-067: the revision run starts in any chat and records the changed draft again",
            rid is not None and code == 0, (ag.errors[-1:], out))
    ag.fin(rid, "revised")
    n = h.nxt(S_)
    h.check("CM-067: once recorded again, /next goes on to the approval line", "revise" not in n["command"], n)
    code, out = h.sh(f'python3 scripts/next.py {S_} --carry "drafts approved, push them to WordPress as drafts"')
    n = h.nxt(S_)
    h.check("CM-067: what Paul asked in a chat that could not do it reaches the next chat's /next first",
            code == 0 and any("push them to WordPress" in t for t in n.get("paul_said") or []), (out, n))
    h.sh(f"python3 scripts/records.py render {S_}")
    sm = (ag.c / "STATUS.md").read_text()
    h.check("CM-067: STATUS.md lists Paul's carried words at the top", "## Paul said in the last chat" in sm
            and "push them to WordPress" in sm, sm[:900])
    h.sh(f"python3 scripts/next.py {S_} --carried")
    n = h.nxt(S_)
    h.check("CM-067: --carried clears them once the new chat has done them", not n.get("paul_said"), n)
    nm = (h.SB / ".claude" / "commands" / "next.md").read_text()
    h.check("CM-067: /next tells the chat to act on paul_said first, hand Paul's words on before a new session, and "
            "change drafts only in a revision run", "paul_said" in nm and "--carry" in nm and "--step revise" in nm, nm[:600])


SCENARIOS = [t_carry_and_revise]
