#!/usr/bin/env python3
"""drive.py — the client's Drive folder, through Google Drive for desktop (R4, Paul 2026-10-08).

Drive for desktop shows the v3 folder as a local path (config.json drive.local_root). Every upload is a
**file copy** into that path — byte-exact, any size, zero tokens, nothing retyped — and Drive syncs it.
Only the v3 folder is ever touched (R8): a client's folder is exactly `<v3>/<Client Name> - TMS`.

A new version never deletes the old one (Paul, 2026-10-03). Archive-and-replace:
  1. the old file is renamed with its date ("<name> - 2026-10-03.md", "(2)" if taken) and moved into
     the client folder's _Archive,
  2. the new file is copied in under the original name,
  3. both steps are logged as drive_file changes (channel drive).
An unchanged file is left alone (same bytes → nothing copied, nothing archived).

    drive.py where <slug>                         the client's local Drive folder (or why there is none)
    drive.py folder <slug> --run R                /new-client: use <v3>/<Client> - TMS if it exists, else copy
                                                  the template folder there (a real folder copy) — logged
    drive.py upload <slug> --run R --file F [--to "<subfolder>"] [--name "<Drive name>"]
                                                  copy one file in (crawl CSVs, deliverables, evidence) — logged
    drive.py mirror <slug> --run R                the records (Handoff Log, Approval Record, Document Checklist,
                                                  Brand Guide, Status) — run.py finish and approve.py do this
                                                  themselves; use it only to re-mirror by hand in a drive-mirror run
    drive.py records <slug>                       list the mirrored records: local file → Drive name
    drive.py archive-name "<Drive file name>" <YYYY-MM-DD> [--n 2]
    drive.py replaced <slug> --run R --name N --local F --new-link URL [--archived-as A --archived-link URL]
                                                  connector uploads only (the proof sheet's native Google Doc,
                                                  `- CLIENT COPY`): log what was done through the connector

No local Drive folder (Drive for desktop not set up) → nothing is copied; the run records "Drive copy
pending sync" once as a settled decision and moves on. Never retype a file into the Drive connector.
"""
import argparse
import datetime
import hashlib
import re
import shutil
from pathlib import Path

import run as R
import status as S
from lib import ROOT, append, client_dir, config, die, machine, now, sha12

LOCAL = {"Handoff Log": "handoff-log.md", "Approval Record": "approval-record.md",
         "Document Checklist": "document-checklist.md", "Brand Guide": "brand-guide.md", "Status": "STATUS.md",
         "VA Worklist": "handoffs/VA-WORKLIST.md", "VA Worklist CSV": "handoffs/VA-WORKLIST.csv"}   # P9
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# where a repo file's Drive copy goes, by its folder under clients/<slug>/
PLACES = {"discovery": "01 - Discovery and Audit/Deliverables", "audit": "01 - Discovery and Audit/Deliverables",
          "data": "01 - Discovery and Audit/Evidence", "inputs": "01 - Discovery and Audit/Evidence",
          "build": "02 - Build", "finish": "03 - Finish", "blog": "04 - Blog", "handoffs": "02 - Build"}


def cfg():
    return config().get("drive") or {}


def archive_folder():
    return cfg().get("client_archive_folder", "_Archive")


def archive_name(name, date, n=None):
    if not DATE.match(date):
        die(f"'{date}' is not a date (YYYY-MM-DD).")
    stem, ext = (name[: -len(Path(name).suffix)], Path(name).suffix) if Path(name).suffix else (name, "")
    return f"{stem} - {date}" + (f" ({n})" if n and n > 1 else "") + ext


def local_root():
    """The v3 folder on this Mac, or None if Drive for desktop is not set up."""
    raw = machine().get("drive_local_root") or cfg().get("local_root")
    if not raw:
        return None
    p = Path(raw).expanduser()
    return p if p.is_dir() else None


def client_folder(st):
    root = local_root()
    return root / f"{st['client']['name']} - TMS" if root else None


def where(slug):
    """(folder or None, why)."""
    st = S.load(slug)
    root = local_root()
    if not root:
        raw = machine().get("drive_local_root") or cfg().get("local_root")
        return None, ("Drive for desktop is not set up on this Mac (config.json drive.local_root is empty)" if not raw
                      else f"the local Drive folder {raw} is not there (Drive for desktop signed out or not syncing?)")
    f = client_folder(st)
    return (f, "") if f.is_dir() else (None, f"{f.name} does not exist in v3 yet — /new-client creates it")


def _same(a, b):
    def h(p):
        x = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                x.update(chunk)
        return x.digest()
    return a.stat().st_size == b.stat().st_size and h(a) == h(b)


def _url(dest):
    return "drive:" + str(dest.relative_to(local_root()))


def pending(slug, run_id, closed_ok=False):
    """No local Drive: record it once (a settled decision), never again."""
    st = S.load(slug)
    if st.get("drive_pending_noted"):
        return
    st["drive_pending_noted"] = now()
    S.save(slug, st)
    _, why = where(slug)
    import settled
    settled.settle(slug, run_id, "drive_pending_sync",
                   f"Drive copy pending sync — {why}. Files stay in the repo until Drive for desktop syncs; "
                   "nothing is retyped into the connector.", by="system", closed_ok=closed_ok)


def copy_in(slug, run_id, src, subdir="", name=None, text=None, closed_ok=False):
    """Copy src (or the given text) into the client's Drive folder. Returns 'copied' / 'unchanged' / 'pending'."""
    folder, _ = where(slug)
    if not folder:
        pending(slug, run_id, closed_ok)
        return "pending"
    src = Path(src)
    name = name or src.name
    dest_dir = folder / subdir if subdir else folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / name
    tmp = None
    if text is not None:
        tmp = ROOT / "clients" / slug / f".drive-{sha12(src) if src.exists() else 'x'}.tmp"
        tmp.write_text(text, encoding="utf-8")
        src = tmp
    try:
        if dest.exists() and _same(src, dest):
            return "unchanged"
        if dest.exists():
            date = datetime.date.fromtimestamp(dest.stat().st_mtime).isoformat()
            arch = folder / archive_folder()
            arch.mkdir(exist_ok=True)
            n = 1
            while (arch / archive_name(name, date, n)).exists():
                n += 1
            aname = archive_name(name, date, n)
            dest.rename(arch / aname)
            R.log_change(slug, run_id, "drive_file", _url(arch / aname), "archive", _url(dest),
                         f"{archive_folder()}/{aname}", "done · renamed and moved, nothing deleted",
                         channel="drive", closed_ok=closed_ok)
            old = f"previous version archived as {aname}"
        else:
            old = "(new file)"
        shutil.copyfile(src, dest)
        R.log_change(slug, run_id, "drive_file", _url(dest), "upload", old, f"{name} · sha {sha12(dest)}",
                     "done · copied (Drive for desktop syncs it)", channel="drive", closed_ok=closed_ok,
                     new_file=None if text is None else str(src))
        return "copied"
    finally:
        if tmp and tmp.exists():
            tmp.unlink()


def records(slug):
    st = S.load(slug)
    out = []
    for label in cfg().get("mirrored_records") or LOCAL:
        local = client_dir(slug) / LOCAL[label]
        out.append((label, local, f"{st['client']['name']} - {label.replace(' CSV', '')}{local.suffix}"))
    return out


def mirror(slug, run_id, closed_ok=False):
    """Copy every record whose content changed. Returns {'copied': n, 'unchanged': n} or {'pending': 1}."""
    if not where(slug)[0]:
        pending(slug, run_id, closed_ok)
        return {"pending": 1}
    out = {"copied": 0, "unchanged": 0}
    import worklist
    blocked = S.load(slug).get("publish_handoff") and not worklist.check_passed(slug)   # §7a: no unchecked handover
    for _, local, name in records(slug):
        if blocked and "VA Worklist" in name:
            out["held_back"] = "VA Worklist (worklist.py check has not passed for these rows)"
            continue
        if local.exists():
            r = copy_in(slug, run_id, local, "", name, closed_ok=closed_ok)
            out[r] = out.get(r, 0) + 1
    return out


def place(slug, rel):
    """The Drive subfolder for a repo file under clients/<slug>/."""
    parts = Path(rel).parts
    i = parts.index(slug) + 1 if slug in parts else 0
    return PLACES.get(parts[i] if i < len(parts) else "", "")


def approved_copy(slug, label, rel, sha, decision, closed_ok=True):
    """#10: an approved '- REVIEW' file gets a Drive copy named '- APPROVED' with a stamped header
    (approved by Paul, date, sha). The repo file is not changed."""
    src = ROOT / rel.split("#", 1)[0]
    if "- REVIEW" not in src.name or not src.is_file() or src.suffix != ".md":
        return None
    name = src.name.replace("- REVIEW", "- APPROVED")
    body = src.read_text(encoding="utf-8")
    lines = body.splitlines()
    if lines and lines[0].startswith("#"):
        lines[0] = lines[0].replace("- REVIEW", "- APPROVED")
    stamp = (f"> **APPROVED by Paul on {now()[:10]}** ({label}, {decision}). Approved version: repo file "
             f"`{rel.split('#', 1)[0]}`, sha {sha}. This Drive copy is the approved version.\n")
    text = (lines[0] + "\n\n" + stamp + "\n" + "\n".join(lines[1:]) + "\n") if lines and lines[0].startswith("#") \
        else stamp + "\n" + body
    return copy_in(slug, f"approval-{now()[:10]}", src, place(slug, rel), name, text=text, closed_ok=closed_ok)


def make_folder(slug, run_id):
    """/new-client (R8): only <v3>/<Client> - TMS is looked at. Missing → a real copy of the template folder."""
    st = S.load(slug)
    root = local_root()
    if not root:
        pending(slug, run_id)
        return "pending", None
    dest = client_folder(st)
    if dest.is_dir():
        R.log_change(slug, run_id, "drive_folder", _url(dest), "client folder", "", dest.name,
                     "exists already in v3 — used as is", channel="drive")
        return "exists", dest
    tpl = root / cfg().get("template_folder_name", "_CLIENT FOLDER TEMPLATE - copy per client")
    if not tpl.is_dir():
        die(f"The template folder '{tpl.name}' is not in v3 — ask Paul.")
    shutil.copytree(tpl, dest)
    R.log_change(slug, run_id, "drive_folder", _url(dest), "client folder", "(none)", dest.name,
                 f"done · copied from {tpl.name}", channel="drive")
    return "created", dest


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("where"); s.add_argument("slug")
    s = sub.add_parser("folder"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s = sub.add_parser("upload"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--file", required=True, action="append"); s.add_argument("--to"); s.add_argument("--name")
    s = sub.add_parser("mirror"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s = sub.add_parser("records"); s.add_argument("slug")
    s = sub.add_parser("archive-name"); s.add_argument("name"); s.add_argument("date")
    s.add_argument("--n", type=int)
    s = sub.add_parser("replaced"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--name", required=True); s.add_argument("--local", required=True)
    s.add_argument("--new-link", required=True)
    s.add_argument("--archived-as"); s.add_argument("--archived-link")
    a = ap.parse_args()

    if a.cmd == "archive-name":
        print(archive_name(a.name, a.date, a.n)); return
    if a.cmd == "where":
        f, why = where(a.slug)
        print(f if f else f"none — {why}"); return
    if a.cmd == "records":
        f, why = where(a.slug)
        print(f"Client folder: {f or 'none — ' + why} · archive subfolder: {archive_folder()}")
        for label, local, name in records(a.slug):
            print(f"  {label:20} {local.relative_to(ROOT)}  →  {name}" + ("" if local.exists() else "  (no local file yet)"))
        return

    R.open_run(a.slug, a.run)
    if a.cmd == "folder":
        r, dest = make_folder(a.slug, a.run)
        print({"pending": "Drive copy pending sync — no local Drive folder (recorded once)",
               "exists": f"using the existing folder {dest}", "created": f"created {dest} from the template"}[r])
        return
    if a.cmd == "mirror":
        print("records mirrored: " + ", ".join(f"{k} {v}" for k, v in mirror(a.slug, a.run).items()))
        return
    if a.cmd == "upload":
        if a.name and len(a.file) > 1:
            die("--name is for one file.")
        for f in a.file:
            p = Path(f) if Path(f).is_absolute() else ROOT / f
            if not p.is_file():
                die(f"{f} does not exist.")
            sub_ = a.to if a.to is not None else place(a.slug, str(p.relative_to(ROOT)) if ROOT in p.parents else f)
            print(f"{p.name}: {copy_in(a.slug, a.run, p, sub_, a.name)}")
        return

    local = Path(a.local)
    if not local.exists():
        die(f"{a.local} does not exist.")
    if bool(a.archived_as) != bool(a.archived_link):
        die("--archived-as and --archived-link go together (the old file's new name and its link).")
    if a.archived_as:
        if not a.archived_as.startswith(Path(a.name).stem + " - "):
            die(f"The archive name must be the old name plus its date: {archive_name(a.name, 'YYYY-MM-DD')}")
        R.log_change(a.slug, a.run, "drive_file", a.archived_link, "archive", a.name,
                     f"{archive_folder()}/{a.archived_as}", "done · renamed and moved, nothing deleted",
                     channel="drive")
    n = R.log_change(a.slug, a.run, "drive_file", a.new_link, "upload",
                     f"previous version archived as {a.archived_as}" if a.archived_as else "(new file)",
                     f"{a.name} · sha {sha12(local)}", "done", channel="drive", new_file=str(local))
    print(f"change #{n} logged")


if __name__ == "__main__":
    main()
