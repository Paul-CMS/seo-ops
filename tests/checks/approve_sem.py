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


SCENARIOS = [t_sem_table]
