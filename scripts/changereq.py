#!/usr/bin/env python3
"""changereq.py — the one inbox for workflow changes (rewrite 2 P3; Q2: only Paul changes the workflow).

    changereq.py list [--open]                          every change request and its state, plus flags not yet collected
    changereq.py collect                                 (system session) give every new client flag its CR-### number
    changereq.py add --title T --text T [--by B]         (system session) a proposal raised in a system session
    changereq.py decide <CR-###> accept|reject|edit --text T   (system session) Paul's answer in /system-review
    changereq.py done <CR-###> --sha SHA                 (system session) built, tested and committed
    changereq.py session                                 is this a system session? (exit 0 yes, 4 no)

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


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--open", action="store_true")
    sub.add_parser("collect")
    sub.add_parser("session")
    s = sub.add_parser("add"); s.add_argument("--title", required=True); s.add_argument("--text", required=True)
    s.add_argument("--by", default="Paul")
    s = sub.add_parser("decide"); s.add_argument("cr"); s.add_argument("answer", choices=["accept", "reject", "edit"])
    s.add_argument("--text", default="")
    s = sub.add_parser("done"); s.add_argument("cr"); s.add_argument("--sha", required=True)
    a = ap.parse_args()
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
        event(a.cr, "DONE", "system session", f"commit {a.sha}")
        print(f"{a.cr}: DONE ({a.sha})")


if __name__ == "__main__":
    main()
