"""F-017: /approve --sem accepts exactly the SEM rows in the batch's semantic review table, whatever the count."""
import contextlib
import io
import sys


def t_sem_table(h):
    sys.path.insert(0, str(h.SB / "scripts"))
    try:
        import approve
    finally:
        sys.path.pop(0)
    d = h.SB / "clients" / "sem-co" / "build"
    d.mkdir(parents=True, exist_ok=True)

    def table(name, ids):
        (d / name).write_text("| ID | Check | Where | Finding |\n|---|---|---|---|\n"
                              + "".join(f"| **SEM-{i}** | E1 | page | see SEM-99 in prose |\n" for i in ids)
                              + "\nSEM-99 is mentioned in prose only.\n")
        return {"files": {"drafts": ["clients/sem-co/build/D-a.md", f"clients/sem-co/build/{name}"]}}

    def pick(b, v):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                approve.check_sem("batch:x:drafts", b, approve.sem_list(v))
                return True, ""
            except SystemExit:
                return False, err.getvalue()

    b15, b20 = table("sem15.md", range(1, 16)), table("sem20.md", range(1, 21))
    h.check("F-017: a 15-item table accepts SEM-1 to SEM-15 (9–15 included)",
            pick(b15, ",".join(str(i) for i in range(1, 16)))[0] and pick(b15, "SEM-9, sem-15")[0])
    ok, why = pick(b15, "3,16")
    h.check("F-017: a 15-item table refuses 16, naming it", not ok and "SEM-16" in why, why)
    h.check("F-017: a 20-item table accepts SEM-1 to SEM-20",
            pick(b20, ",".join(str(i) for i in range(1, 21)))[0])
    ok, why = pick(table("gap.md", [1, 2, 4]), "3")
    h.check("F-017: a number not in the table is refused (gap at SEM-3; prose mentions don't count)",
            not ok and "SEM-3" in why and pick(table("gap2.md", [1, 2, 4]), "99")[0] is False, why)
    h.check("F-017: --sem none needs no table", pick({"files": {}}, "none")[0])


def t_drafts_after_sem_applied(h):
    """CR-025: a drafts approval is accepted at drafts_written or any later state (sem_applied included); SEM items
    already applied are recorded as applied and never re-applied."""
    sys.path.insert(0, str(h.SB / "scripts"))
    try:
        import approve
    finally:
        sys.path.pop(0)
    done = {"sem_ids": ["SEM-1", "SEM-2"], "at": "2026-10-12T14:29", "checks": "E1–E10 passed on changed sections"}

    def run(state, v, applied=None):
        b = {"state": state, "drafts": {"sem_ids": ["SEM-1", "SEM-2"], "applied": applied} if applied else None}
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                return True, approve.drafts_applied("batch:services:drafts", b, approve.sem_list(v)), ""
            except SystemExit:
                return False, None, err.getvalue()

    ok, got, why = run("sem_applied", None, done)
    h.check("CR-025: a batch at sem_applied accepts the drafts approval and returns the applied SEM items",
            ok and got == done, why)
    ok, got, why = run("sem_applied", "2,1", done)
    h.check("CR-025: --sem repeating exactly the applied items is accepted", ok and got == done, why)
    ok, _, why = run("sem_applied", "1,3", done)
    h.check("CR-025: --sem naming items other than those applied is refused (never re-applied)",
            not ok and "already applied" in why, why)
    h.check("CR-025: drafts_written, sem_check_failed and every later state are accepted",
            all(run(s, "none")[0] for s in ("drafts_written", "sem_check_failed", "drafted", "handed_off",
                                            "corrections_requested", "published", "verified", "written_back")))
    h.check("CR-025: drafts_written with nothing applied returns no applied record", run("drafts_written", "1")[1] is None)
    ok, _, why = run("briefs_written", "none")
    h.check("CR-025: planned and briefs_written are still refused (drafts not written)",
            not ok and "not written yet" in why and not run("planned", "none")[0], why)
    nxt = (h.SB / "scripts" / "next.py").read_text(encoding="utf-8")
    h.check("CR-025: /next re-applies SEM only before they are applied (drafts_written/sem_check_failed, no 'applied')",
            'state in ("drafts_written", "sem_check_failed") and drafts.get("sem_ids") and not drafts.get("applied")' in nxt)
    src = (h.SB / "scripts" / "approve.py").read_text(encoding="utf-8")
    h.check("CR-025: the new approval keeps the applied record and logs the items as already applied",
            '**({"applied": applied} if applied else {})' in src and "already applied (not re-applied)" in src)


SCENARIOS = [t_sem_table, t_drafts_after_sem_applied]
