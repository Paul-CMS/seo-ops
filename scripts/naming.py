#!/usr/bin/env python3
"""naming.py — Drive file names, per methodology/naming-convention.md.

    naming.py check "<file name>" --client "Client Name"
    naming.py content <CODE> "<Service or Location>" --client "Client Name"
    naming.py rename-list <names.txt> --client "Client Name"     Markdown table for Paul

Content:   [CODE] - [Service or Location Name] - [Client Name]        (no status, no extension)
           SB SD LB LD LBCH LDCH HB HD AB AD PB PD
Deliverable: [Client Name] - [Artifact] - [DRAFT|REVIEW|APPROVED|SUPERSEDED].md
Living:    [Client Name] - Brand Guide|Approval Record|Document Checklist|Handoff Log.md
Evidence:  [Client Name] - [SF|LNKD|BL|GSC|GA4|CMS|DFS|MANUAL] - [export] - [YYYY-MM-DD].[ext]
Reference: [Client Name] - [Description] - REFERENCE.[ext]
"""
import argparse
import re
import sys

CODES = {"SB": "service brief", "SD": "service draft (approved content)", "LB": "location brief",
         "LD": "location draft (approved content)", "LBCH": "county hub brief", "LDCH": "county hub draft",
         "HB": "homepage brief", "HD": "homepage draft", "AB": "about brief", "AD": "about draft",
         "PB": "blog post brief", "PD": "blog post draft"}
SOURCES = ["SF", "LNKD", "BL", "GSC", "GA4", "CMS", "DFS", "MANUAL"]
STATUSES = ["DRAFT", "REVIEW", "APPROVED", "SUPERSEDED"]
LIVING = ["Brand Guide", "Approval Record", "Document Checklist", "Handoff Log"]
EXT = re.compile(r"\.(md|csv|xlsx|pdf|docx|txt|json)$", re.I)


LEGACY = [(re.compile(r"^Service Page Brief(?:\s+([SL]\d+(?:\.\d+)?|\d+))?$", re.I), "SB"),
          (re.compile(r"^Location Page Brief(?:\s+([SL]\d+(?:\.\d+)?|\d+))?$", re.I), "LB"),
          (re.compile(r"^(.+?)\s+Content Draft$", re.I), "SD")]


def _legacy_content(rest, client):
    """Old names like '<Client> - Service Page Brief S2.1 - Roof Replacement - REVIEW'."""
    if not rest:
        return None
    parts = [EXT.sub("", p) for p in rest]
    if parts and parts[-1].upper() in STATUSES:
        parts = parts[:-1]
    for rx, code in LEGACY:
        m = rx.match(parts[0]) if parts else None
        if not m:
            continue
        notes = []
        if code == "SD":
            subject = m.group(1)
        else:
            plan = m.group(1)
            subject = " - ".join(parts[1:])
            if plan:
                notes.append(f"plan number {plan} moves to the page-order table")
        if not subject:
            return None, ["no service or location name in the title — needs a decision"]
        if code == "LB" and re.search(r"\bCounty\b", subject):
            code = "LBCH"
        return f"{code} - {subject} - {client}", notes
    return None


def check(name, client):
    """Return (kind, problems, suggestion)."""
    probs, base = [], name
    parts = [p.strip() for p in re.split(r"\s+-\s+", name)]
    if re.search(r"\((\d+)\)|copy of", name, re.I):
        probs.append("duplicate marker '(n)' or 'copy of'")
    if parts and parts[0].upper() in CODES:
        kind = "content"
        if parts[0] != parts[0].upper():
            probs.append("code must be uppercase")
        if EXT.search(name):
            probs.append("extension in the title")
            parts[-1] = EXT.sub("", parts[-1])
        if len(parts) < 3:
            probs.append("needs [CODE] - [Service or Location] - [Client]")
        elif parts[-1] != client:
            if parts[1] == client:
                probs.append("service/location and client name are swapped")
                parts = [parts[0], " - ".join(parts[2:]), client]
            else:
                probs.append(f"client name must be last and exactly '{client}'")
        if parts[-1].upper() in STATUSES:
            probs.append("content files carry no status suffix")
        sug = f"{parts[0].upper()} - {' - '.join(p for p in parts[1:-1] if p.upper() not in STATUSES)} - {client}"
        return kind, probs, sug
    if not name.startswith(client + " - "):
        probs.append(f"must start with the client name '{client} - ' (or a content code)")
        return "unknown", probs, None
    rest = [p for p in parts[1:]]
    legacy = _legacy_content(rest, client)
    if legacy:
        return "content (old style)", ["old-style brief/draft name — needs a content code"] + legacy[1], legacy[0]
    if len(rest) >= 3 and rest[0].upper() in SOURCES + ["LD"]:
        kind = "evidence"
        if rest[0] == "LD":
            probs.append("Linkdominator tag is now LNKD (LD means location draft)")
            rest[0] = "LNKD"
        if rest[0] != rest[0].upper():
            probs.append("source tag must be uppercase")
        if not re.match(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", rest[-1]):
            probs.append("missing YYYY-MM-DD date before the extension")
        return kind, probs, f"{client} - {rest[0].upper()} - " + " - ".join(rest[1:])
    stem = EXT.sub("", rest[-1]) if rest else ""
    if len(rest) == 1 and stem in LIVING:
        return "living", probs, None
    if stem.upper() == "REFERENCE":
        return "reference", probs, None
    if stem.upper() in STATUSES:
        if not name.endswith(".md"):
            probs.append("deliverables are .md files")
        return "deliverable", probs, None
    probs.append("deliverable without a status (DRAFT, REVIEW, APPROVED or SUPERSEDED)")
    return "deliverable?", probs, None


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("check"); s.add_argument("name"); s.add_argument("--client", required=True)
    s = sub.add_parser("content"); s.add_argument("code"); s.add_argument("subject"); s.add_argument("--client", required=True)
    s = sub.add_parser("rename-list"); s.add_argument("names"); s.add_argument("--client", required=True)
    a = ap.parse_args()
    if a.cmd == "check":
        kind, probs, sug = check(a.name, a.client)
        print(f"{kind}: " + ("OK" if not probs else "; ".join(probs)) + (f"\n  suggest: {sug}" if sug and probs else ""))
        sys.exit(0 if not probs else 1)
    if a.cmd == "content":
        if a.code.upper() not in CODES:
            sys.exit(f"unknown code {a.code}. Codes: {', '.join(CODES)}")
        print(f"{a.code.upper()} - {a.subject} - {a.client}")
    if a.cmd == "rename-list":
        print("| Current name | Problem | Proposed name | Approve? |\n|---|---|---|---|")
        for n in [l.strip() for l in open(a.names, encoding="utf-8") if l.strip()]:
            kind, probs, sug = check(n, a.client)
            if probs:
                print(f"| {n} | {'; '.join(probs)} | {sug or '(needs a decision)'} | [ ] |")


if __name__ == "__main__":
    main()
