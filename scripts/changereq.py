#!/usr/bin/env python3
"""changereq.py — the one inbox for workflow changes (rewrite 2 P3; Q2: only Paul changes the workflow).

    changereq.py list [--open]                          every change request and its state, plus flags not yet collected
    changereq.py collect                                 (system session) give every new client flag its CR-### number
    changereq.py add --title T --text T [--by B]         (system session) a proposal raised in a system session
    changereq.py decide <CR-###> accept|reject|edit --text T   (system session) Paul's answer in /system-review
    changereq.py done <CR-###> --sha SHA                 (system session) built, tested, committed and pushed
    changereq.py session                                 is this a system session? (exit 0 yes, 4 no)
    changereq.py start                                   /system step 1: refuse unless main, clean; then sync with origin
    changereq.py push                                    (system session) after every system commit; exit 5 = push failed, stop

Main stays in step with GitHub (2026-10-12): every system commit is pushed at once. `start` fast-forwards when only
GitHub moved, pushes when only this Mac did, and when both moved rebases on its own only if this Mac's commits touch
system files alone and GitHub's touch clients/ alone — then the fast tier must pass before it pushes. Anything else
stops and shows Paul both sides.

A client session never changes the workflow. It flags the issue instead (`run.py flag <slug> <RUN_ID> --text …`),
which appends a row to clients/<slug>/flags.jsonl (append-only; the run continues on the current rules). Flags live
in the client's own folder so two clients' branches never collide (P2); `collect`, at the start of /system-review,
gives each one its CR-### entry in methodology/change-requests.md. That file is append-only and written only here:
entries, then state events (`- CR-### · date · STATE · who · note`). The latest event is the state; none = OPEN.

A system session is one in which Paul typed /system: the UserPromptSubmit hook writes .claude/state/system-token.json
for that session id. machine.json `can_change_system: false` (a VA's Mac) refuses it.
"""
import argparse
import json
import re
import sys

from lib import CLIENTS, ROOT, append, client_dir, die, machine, now

FILE = ROOT / "methodology" / "change-requests.md"
TOKEN = ROOT / ".claude" / "state" / "system-token.json"
ENTRY = re.compile(r"^## (CR-\d{3}) · (\S+) · (.+)$", re.M)
EVENT = re.compile(r"^- (CR-\d{3}) · (\S+) · (OPEN|ACCEPTED|REJECTED|DONE) · (.*)$", re.M)
FLAG_REF = re.compile(r"^Flag: ([a-z0-9-]+) (F-\d{3})\b", re.M)
HEAD = """# Change requests — the one inbox for workflow changes
### Nothing here is in force. Paul answers each item in /system-review (accept · reject · edit); an accepted item is built in a system session, tested, committed, and marked DONE with its commit.

Written only by `scripts/changereq.py` (append-only). Client sessions never edit this file: they flag
(`run.py flag <slug> <RUN_ID> --text "…"`), and `/system-review` collects the flags here. The old proposals inbox
(`lessons.md`, L-001–L-011) is archived in `methodology/archive/lessons.md`; L-008–L-011 continue here as CR-001–CR-004.
"""


def system_session(sid=None):
    """True when Paul typed /system in this session (and this Mac may change the system)."""
    if machine().get("can_change_system") is False:
        return False
    try:
        tok = json.loads(TOKEN.read_text())
    except Exception:
        return False
    import stages
    sid = sid or stages.current_session()
    return bool(sid) and tok.get("session_id") == sid


def need_system():
    if not system_session():
        die("REFUSED — workflow changes happen in a system session (Paul types /system first). "
            "In a client session, flag it instead: python3 scripts/run.py flag <slug> <RUN_ID> --text \"…\"", 4)


def text():
    return FILE.read_text() if FILE.exists() else HEAD


def entries():
    """{CR-###: {date, title, body, state, events, flag}} in file order."""
    t = text()
    out = {}
    ms = list(ENTRY.finditer(t))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        body = t[m.end():end]
        body = body.split("\n---\n")[0].strip()
        fr = FLAG_REF.search(body)
        out[m.group(1)] = {"date": m.group(2), "title": m.group(3), "body": body, "state": "OPEN", "events": [],
                           "flag": (fr.group(1), fr.group(2)) if fr else None}
    for m in EVENT.finditer(t):
        if m.group(1) in out:
            out[m.group(1)]["state"] = m.group(3)
            out[m.group(1)]["events"].append((m.group(2), m.group(3), m.group(4)))
    return out


def _next_id(ents):
    return f"CR-{max([int(k[3:]) for k in ents] or [0]) + 1:03d}"


def _append(block):
    t = text()
    if not FILE.exists():
        FILE.write_text(t)
    append(FILE, ("" if t.endswith("\n\n") else "\n") + block.rstrip() + "\n")


def add_entry(title, body, date=None):
    ents = entries()
    cid = _next_id(ents)
    _append(f"## {cid} · {date or now()[:10]} · {title}\n{body.strip()}\n\n---")
    return cid


def event(cid, state, who, note=""):
    if cid not in entries():
        die(f"no change request {cid}")
    _append(f"- {cid} · {now()[:10]} · {state} · {who}" + (f" · {note}" if note else ""))


# ------------------------------------------------------------------ client flags
def flags(slug):
    p = client_dir(slug) / "flags.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def flag(slug, run_id, step, text_, workaround, who):
    """Append one flag to the client's flags.jsonl. Returns its id (F-###)."""
    rows = flags(slug)
    fid = f"F-{len(rows) + 1:03d}"
    row = {"id": fid, "at": now(), "client": slug, "step": step, "run": run_id, "who": who, "text": text_,
           "workaround": workaround}
    append(client_dir(slug) / "flags.jsonl", json.dumps(row) + "\n")
    return fid


def flag_state(slug, fid, ents=None):
    """(CR id or None, state) — OPEN until /system-review collects and answers it."""
    for cid, e in (ents or entries()).items():
        if e["flag"] == (slug, fid):
            return cid, e["state"]
    return None, "OPEN"


def open_flags(slug):
    """[(flag row, CR id or None, state)] for the client's flags that are not DONE or REJECTED."""
    ents = entries()
    out = []
    for r in flags(slug):
        cid, state = flag_state(slug, r["id"], ents)
        if state not in ("DONE", "REJECTED"):
            out.append((r, cid, state))
    return out


def collect():
    ents = entries()
    done = {e["flag"] for e in ents.values() if e["flag"]}
    new = []
    for d in sorted(CLIENTS.glob("*/flags.jsonl")):
        slug = d.parent.name
        for r in flags(slug):
            if (slug, r["id"]) in done:
                continue
            body = (f"Flag: {slug} {r['id']} · step {r.get('step') or '—'} · run {r.get('run')} · flagged by {r.get('who')} "
                    f"({r['at'][:16]})\nWhat: {r['text']}\nWorkaround used: {r.get('workaround') or '—'}")
            new.append(add_entry(r["text"][:80].replace("\n", " "), body, r["at"][:10]))
    return new


# ------------------------------------------------------------------ main stays in step with origin (2026-10-12)
def _lines(r):
    return [l for l in r.stdout.splitlines() if l.strip()]


def fast_tier(root):
    """(passed, last lines) of python3 tests/run_all.py (the fast tier) in root."""
    import subprocess
    r = subprocess.run([sys.executable, "tests/run_all.py"], cwd=root, capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    return r.returncode == 0 and bool(tail) and tail[-1].endswith(" 0 failed"), "\n".join(tail)


def push(git):
    """(ok, message). Every system commit goes to origin at once; a failed push is said plainly and stops the session."""
    sha = git("rev-parse", "--short", "HEAD").stdout.strip()
    r = git("push", "-q", "origin", "main")
    if r.returncode != 0:
        return False, (f"PUSH FAILED — commit {sha} is only on this Mac, not on GitHub. Stop here: nothing else until "
                       f"it is pushed. Git said:\n  " + (r.stderr or r.stdout).strip().replace("\n", "\n  "))
    return True, f"pushed {sha} to origin/main"


def on_origin(git, sha):
    """True when sha is on GitHub's main (or there is no remote to push to, as in the test sandbox)."""
    if git("remote", "get-url", "origin").returncode != 0:
        return True
    return git("merge-base", "--is-ancestor", sha, "origin/main").returncode == 0


def sync_main(git, run_fast_tier):
    """Bring main in step with origin (/system step 1). Returns (ok, message).
    behind only → fast-forward · ahead only → push · diverged, with the local commits touching only system files and
    origin's only clients/ → rebase, run the fast tier, push · anything else → stop and show Paul."""
    r = git("fetch", "-q", "origin", "main")
    if r.returncode != 0:
        return False, "REFUSED — could not fetch origin: " + (r.stderr or r.stdout).strip()
    ahead = _lines(git("log", "--oneline", "origin/main..HEAD"))
    behind = _lines(git("log", "--oneline", "HEAD..origin/main"))
    if not ahead and not behind:
        return True, "up to date"
    if behind and not ahead:
        r = git("merge", "--ff-only", "-q", "origin/main")
        return (r.returncode == 0, "fast-forwarded" if r.returncode == 0 else
                "REFUSED — could not fast-forward main: " + (r.stderr or r.stdout).strip())
    if ahead and not behind:
        return push(git)
    base = git("merge-base", "HEAD", "origin/main").stdout.strip()
    mine = _lines(git("diff", "--name-only", base, "HEAD"))
    theirs = _lines(git("diff", "--name-only", base, "origin/main"))
    show = (f"\n  This Mac has {len(ahead)} commit(s) GitHub doesn't:\n    " + "\n    ".join(ahead[:15])
            + f"\n    files: {', '.join(mine[:15]) or '—'}"
            + f"\n  GitHub has {len(behind)} commit(s) this Mac doesn't:\n    " + "\n    ".join(behind[:15])
            + f"\n    files: {', '.join(theirs[:15]) + (' …' if len(theirs) > 15 else '') or '—'}")
    safe = (mine and not any(f.startswith("clients/") for f in mine)
            and theirs and all(f.startswith("clients/") for f in theirs))
    if not safe:
        return False, ("REFUSED — main has diverged from GitHub and it is not the safe case (this Mac's commits only "
                       "system files, GitHub's only clients/). Paul decides: rebase or merge." + show)
    was = git("rev-parse", "--short", "HEAD").stdout.strip()
    r = git("rebase", "-q", "origin/main")
    if r.returncode != 0:
        git("rebase", "--abort")
        return False, "REFUSED — the rebase onto GitHub's main stopped, so it was undone. Paul decides." + show
    ok, tail = run_fast_tier()
    if not ok:
        return False, (f"REFUSED — rebased this Mac's commits onto GitHub's main, but the fast tier fails, so nothing "
                       f"was pushed. Main was {was} before the rebase. Paul decides.\n  " + tail.replace("\n", "\n  "))
    ok, msg = push(git)
    return ok, (f"rebased {len(ahead)} system commit(s) onto {len(behind)} client commit(s) from GitHub, fast tier "
                f"passed, " + msg if ok else msg)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--open", action="store_true")
    sub.add_parser("collect")
    sub.add_parser("session")
    sub.add_parser("start")
    sub.add_parser("push")
    s = sub.add_parser("add"); s.add_argument("--title", required=True); s.add_argument("--text", required=True)
    s.add_argument("--by", default="Paul")
    s = sub.add_parser("decide"); s.add_argument("cr"); s.add_argument("answer", choices=["accept", "reject", "edit"])
    s.add_argument("--text", default="")
    s = sub.add_parser("done"); s.add_argument("cr"); s.add_argument("--sha", required=True)
    a = ap.parse_args()
    if a.cmd == "start":   # /system step 1 (Paul, 2026-10-09): the main folder, clean, up to date
        import subprocess
        from lib import ROOT as _R, main_root

        def git(*x):
            return subprocess.run(["git", "-C", str(_R), *x], capture_output=True, text=True)
        if not system_session():
            die("REFUSED — not a system session: Paul types /system first (and the hooks must be installed).", 4)
        if main_root().resolve() != _R.resolve():
            die(f"REFUSED — a system session runs in the main folder ({main_root()}), never in a client worktree.", 4)
        br = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if br != "main":
            die(f"REFUSED — the main folder is on branch {br}, not main.", 4)
        dirty = [l for l in git("status", "--porcelain").stdout.splitlines() if l.strip()]
        if dirty:
            die("REFUSED — the main folder has uncommitted changes; commit or put them aside first:\n  "
                + "\n  ".join(dirty[:20]), 4)
        if git("remote", "get-url", "origin").returncode == 0:
            ok, msg = sync_main(git, lambda: fast_tier(_R))
            if not ok:
                die(msg, 4)
            if msg != "up to date":
                print(msg)
        print("system session ready: main folder, clean, up to date (" + git("rev-parse", "--short", "HEAD").stdout.strip() + ")")
        return
    if a.cmd == "push":    # after every system commit (2026-10-12): pushed at once, or the session stops
        import subprocess
        need_system()
        ok, msg = push(lambda *x: subprocess.run(["git", "-C", str(ROOT), *x], capture_output=True, text=True))
        if not ok:
            die(msg, 5)
        print(msg)
        return
    if a.cmd == "session":
        ok = system_session()
        print("system session: yes" if ok else "system session: no (Paul types /system to start one)")
        sys.exit(0 if ok else 4)
    if a.cmd == "list":
        ents = entries()
        shown = 0
        for cid, e in ents.items():
            if a.open and e["state"] in ("DONE", "REJECTED"):
                continue
            shown += 1
            print(f"{cid} · {e['state']} · {e['date']} · {e['title']}")
        pending = [(d.parent.name, r) for d in sorted(CLIENTS.glob("*/flags.jsonl")) for r in flags(d.parent.name)
                   if flag_state(d.parent.name, r["id"], ents)[0] is None]
        for slug, r in pending:
            print(f"(not collected) {slug} {r['id']} · {r['at'][:10]} · {r['text'][:100]}")
        if not shown and not pending:
            print("no change requests" + (" open" if a.open else ""))
        return
    need_system()
    if a.cmd == "collect":
        new = collect()
        print(f"collected {len(new)} flag(s)" + (": " + ", ".join(new) if new else ""))
    elif a.cmd == "add":
        print(add_entry(a.title, f"Raised in a system session by {a.by}.\n{a.text}"))
    elif a.cmd == "decide":
        if a.answer == "edit" and not a.text:
            die("edit needs --text: Paul's version of the change")
        state = {"accept": "ACCEPTED", "reject": "REJECTED", "edit": "ACCEPTED"}[a.answer]
        event(a.cr, state, "Paul", ("edited: " if a.answer == "edit" else "") + a.text)
        print(f"{a.cr}: {state}")
    elif a.cmd == "done":
        if entries().get(a.cr, {}).get("state") != "ACCEPTED":
            die(f"{a.cr} is not ACCEPTED — only an accepted change request is built and marked done")
        import subprocess
        if not on_origin(lambda *x: subprocess.run(["git", "-C", str(ROOT), *x], capture_output=True, text=True), a.sha):
            die(f"{a.cr}: commit {a.sha} is not on GitHub yet — run python3 scripts/changereq.py push first")
        event(a.cr, "DONE", "system session", f"commit {a.sha}")
        print(f"{a.cr}: DONE ({a.sha})")


if __name__ == "__main__":
    main()
