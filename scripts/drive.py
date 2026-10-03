#!/usr/bin/env python3
"""drive.py — replacing a file in the client's Drive folder without deleting anything (Paul, 2026-10-03).

The Drive connector cannot overwrite a file's content. So a new version replaces an old one this way:
  1. rename the old Drive file with its date ("<Client> - Handoff Log - 2026-10-03.md"),
  2. move it into the client folder's _Archive subfolder,
  3. upload the new file under the original name,
  4. log both steps as drive_file changes in the open run (this script).
Nothing in Drive is ever deleted. Only files the system itself uploads are renamed this way.

    drive.py records <slug>                         the records mirrored to the client folder root:
                                                    local file → Drive name (config.json drive.mirrored_records)
    drive.py archive-name "<Drive file name>" <YYYY-MM-DD> [--n 2]
                                                    the old file's archive name (its date = its last-modified
                                                    date; --n 2 when that name is already in _Archive)
    drive.py replaced <slug> --run R --name "<Drive file name>" --local <file> --new-link <url>
                      [--archived-as "<archive name>" --archived-link <url>]
                                                    log the archive step (if there was an old file) and the upload

Mirroring the records after a run (the run's own Handoff Log section exists only after finish):
    run.py start <slug> drive-mirror → for each record: archive the old file, upload the new one,
    drive.py replaced … → run.py finish <slug> <RUN_ID> --summary "Drive records mirrored"
A drive-mirror run adds no Handoff Log section, so it never makes the records stale again.
"""
import argparse
import re
from pathlib import Path

import run as R
import status as S
from lib import ROOT, client_dir, config, die, sha12

LOCAL = {"Handoff Log": "handoff-log.md", "Approval Record": "approval-record.md",
         "Document Checklist": "document-checklist.md", "Brand Guide": "brand-guide.md"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def archive_folder():
    return (config().get("drive") or {}).get("client_archive_folder", "_Archive")


def archive_name(name, date, n=None):
    if not DATE.match(date):
        die(f"'{date}' is not a date (YYYY-MM-DD).")
    stem, ext = (name[: -len(Path(name).suffix)], Path(name).suffix) if Path(name).suffix else (name, "")
    return f"{stem} - {date}" + (f" ({n})" if n and n > 1 else "") + ext


def records(slug):
    st = S.load(slug)
    out = []
    for label in (config().get("drive") or {}).get("mirrored_records") or LOCAL:
        local = client_dir(slug) / LOCAL[label]
        out.append((label, local, f"{st['client']['name']} - {label}.md"))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
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
    if a.cmd == "records":
        st = S.load(a.slug)
        print(f"Client folder: {st['client'].get('drive_folder_id') or '(not recorded)'} · archive subfolder: {archive_folder()}")
        for label, local, name in records(a.slug):
            print(f"  {label:20} {local.relative_to(ROOT)}  →  {name}" + ("" if local.exists() else "  (no local file yet)"))
        return

    R.open_run(a.slug, a.run)
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
