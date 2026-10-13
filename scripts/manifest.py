#!/usr/bin/env python3
"""manifest.py — the data manifest (CM-061 part 1; rewrite 3 §3.1). Every input the system collects is listed in
methodology/data-manifest.json with the steps that must read it.

    manifest.py check                every client's data/ and inputs/ file has an entry; every consuming step's read
                                     list names it (exit 4 on any problem)
    manifest.py unused <slug>        inputs on file for this client that no finished step has read yet
    manifest.py which <slug> <path>  the entry a file belongs to

records.py shows `unused` in STATUS.md under "Data on file not used yet". Read-only; no network.
"""
import fnmatch
import json
import re
import sys

from lib import CLIENTS, ROOT, client_dir

FILE = ROOT / "methodology" / "data-manifest.json"
GATES = ROOT / "scripts" / "gates.json"
SCANNED = ("data", "inputs")   # the folders whose every file must have an entry
STATUS_FILE = "status" + ".json"   # a client folder is one with its status file


def entries():
    return json.loads(FILE.read_text(encoding="utf-8"))["entries"]


def match(rel, ents=None):
    """The first entry whose pattern matches a path relative to the client folder (or None)."""
    for e in ents or entries():
        if any(fnmatch.fnmatch(rel, p) for p in e["patterns"]):
            return e
    return None


def client_files(slug):
    d = client_dir(slug)
    out = []
    for top in SCANNED:
        base = d / top
        if base.is_dir():
            out += [str(p.relative_to(d)) for p in sorted(base.rglob("*")) if p.is_file() and p.name != ".DS_Store"]
    return out


def unmanifested(slug):
    ents = entries()
    return [rel for rel in client_files(slug) if not match(rel, ents)]


def read_list_gaps():
    """[(entry id, step, why)] — a step the manifest says must read an input whose read list does not name it."""
    steps = json.loads(GATES.read_text(encoding="utf-8"))["steps"]
    gaps = []
    for e in entries():
        for step in e.get("read_by") or []:
            if step not in steps:
                gaps.append((e["id"], step, "no such step in gates.json"))
                continue
            reads = " ".join(steps[step].get("reads") or []).lower()
            if e["ref"].lower() not in reads:
                gaps.append((e["id"], step, f"its read list does not name {e['ref']!r}"))
        if e.get("raw_of") and not any(x["id"] == e["raw_of"] for x in entries()):
            gaps.append((e["id"], "-", f"raw_of {e['raw_of']!r} is not an entry"))
        if not e.get("read_by") and not e.get("raw_of"):
            gaps.append((e["id"], "-", "no step reads it and it feeds no entry (raw_of)"))
    return gaps


RUN = re.compile(r"^## RUN (\S+) · (STARTED|FINISHED|ABORTED) · ", re.M)
STEP = re.compile(r"^Step: (\S+)", re.M)


def finished_steps(slug):
    """Every step with at least one FINISHED run in the client's safety log."""
    p = client_dir(slug) / "log.md"
    if not p.is_file():
        return set()
    text = p.read_text(encoding="utf-8")
    step_of, done = {}, set()
    for m in RUN.finditer(text):
        rid, state = m.group(1), m.group(2)
        if state == "STARTED":
            s = STEP.search(text, m.end())
            if s:
                step_of[rid] = s.group(1)
        elif state == "FINISHED" and rid in step_of:
            done.add(step_of[rid])
    return done


def unused(slug):
    """[(entry, [files])] — inputs on file that no finished step has read (a raw file counts as read when the entry it
    feeds was read). Only client inputs (data/, inputs/, the discovery and interview files, facts)."""
    ents = entries()
    done = finished_steps(slug)
    d = client_dir(slug)
    byid = {e["id"]: e for e in ents}
    out = []
    for e in ents:
        if e.get("scope") in ("system", "derived"):
            continue
        files = sorted({str(p.relative_to(d)) for pat in e["patterns"] for p in d.glob(pat) if p.is_file()
                        and match(str(p.relative_to(d)), ents) is e})
        if not files:
            continue
        reader = byid.get(e.get("raw_of")) or e
        if not set(reader.get("read_by") or []) & done:
            out.append((e, files))
    return out


def main():
    a = sys.argv[1:]
    if a[:1] == ["check"]:
        probs = []
        clients = sorted(p.name for p in CLIENTS.iterdir() if (p / STATUS_FILE).is_file()) if CLIENTS.is_dir() else []
        for c in clients:
            probs += [f"{c}: {rel} — no entry in methodology/data-manifest.json" for rel in unmanifested(c)]
        probs += [f"manifest {eid} → {step}: {why}" for eid, step, why in read_list_gaps()]
        print("\n".join(probs) or "manifest: every input has an entry and every consuming step reads it")
        sys.exit(4 if probs else 0)
    if a[:1] == ["unused"] and len(a) == 2:
        rows = unused(a[1])
        for e, files in rows:
            print(f"{e['id']}: {len(files)} file(s) — read by {', '.join(e.get('read_by') or [byid for byid in [e.get('raw_of')]])}"
                  " (none finished yet)")
        print("" if rows else "every input on file has been read by a finished step")
        return
    if a[:1] == ["which"] and len(a) == 3:
        e = match(a[2])
        print(json.dumps(e, indent=1) if e else "no entry")
        sys.exit(0 if e else 4)
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
