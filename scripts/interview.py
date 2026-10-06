#!/usr/bin/env python3
"""interview.py — helpers for the three client interviews (CM-042). The questions, extraction and
writing are the expert-interview skill's job; this checks timing and file format.

    interview.py due <slug>                  is a stories round due? (config.json story_cadence_days, default 30)
    interview.py check <slug> bank|voice     the story bank / Voice DNA file has the required shape

Facts interviews are generated from the evidence gate: evidence.py questions (only on a block).
"""
import argparse
import datetime
import re
import sys

import status as S
from lib import client_dir, config, die

BANK_FIELDS = ["Date:", "Type:", "Quote:", "Specificity:", "Publish:", "Status:"]
VOICE_SECTIONS = ["## Summary", "## Do", "## Never", "## Calibration", "## Insufficient data"]


def check_bank(text):
    probs, ids = [], set()
    for m in re.finditer(r"^## (S-\d{3}) · (.+?)\n(.*?)(?=^## S-|\Z)", text, re.M | re.S):
        sid, body = m.group(1), m.group(3)
        if sid in ids:
            probs.append(f"{sid} is used twice")
        ids.add(sid)
        for f in BANK_FIELDS:
            if f not in body:
                probs.append(f"{sid}: no '{f}' line")
        sp = re.search(r"Specificity:\s*(\d)", body)
        if sp and int(sp.group(1)) < 3:
            probs.append(f"{sid}: specificity {sp.group(1)} — 1–2 is a follow-up question, not an entry")
        pub = re.search(r"Publish:\s*([\w-]+)", body)
        if pub and pub.group(1) not in ("public", "framing-only", "internal"):
            probs.append(f"{sid}: publish must be public / framing-only / internal")
        q = re.search(r'Quote:\s*"(.+?)"', body, re.S)
        if not q or len(q.group(1).split()) < 5:
            probs.append(f"{sid}: needs the verbatim quote (in double quotes)")
    if not ids:
        probs.append("no entries (## S-001 · headline)")
    return probs


def check_voice(text):
    probs = [f"no '{s}' section" for s in VOICE_SECTIONS if s not in text]
    for sec in ("## Do", "## Never"):
        m = re.search(re.escape(sec) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        rules = [l for l in (m.group(1).splitlines() if m else []) if l.startswith("- ")]
        if not rules:
            probs.append(f"{sec}: no rules")
        for r in rules:
            if '"' not in r:
                probs.append(f"{sec}: rule without a quote — {r[:60]}")
            if re.search(r"https?://|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b", r):
                probs.append(f"{sec}: a URL or phone number inside a rule — {r[:60]}")
    words = re.search(r"(\d[\d,]*)\s+words from the author", text)
    if not words:
        probs.append("the Source line must say how many words came from the author")
    elif int(words.group(1).replace(",", "")) < 2000 and "UNDER FLOOR" not in text:
        probs.append("fewer than 2,000 author words: add the UNDER FLOOR line (Paul accepts it before use)")
    return probs


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("due"); s.add_argument("slug")
    s = sub.add_parser("check"); s.add_argument("slug"); s.add_argument("what", choices=["bank", "voice"])
    a = ap.parse_args()
    d = client_dir(a.slug) / "interviews"
    if a.cmd == "due":
        st = S.load(a.slug)
        if not S._decided(st, "brand_guide_approved"):
            print("not yet — stories start once the facts exist (the reconciled Brand Guide is approved)")
            sys.exit(1)
        days = int(config().get("story_cadence_days", 30))
        last = ((st.get("marks") or {}).get("story_round") or {}).get("at")
        if not last:
            print("due — no stories round yet"); return
        age = (datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(last)).days
        if age >= days:
            print(f"due — last round {age} days ago (every {days})"); return
        print(f"not due — last round {age} days ago, next in {days - age} days"); sys.exit(1)
    if a.what == "bank":
        f = d / "story-bank.md"
        probs = check_bank(f.read_text()) if f.exists() else [f"{f} does not exist"]
    else:
        fs = sorted(d.glob("voice-dna-*.md"))
        if len(fs) != 1:
            die(f"expected exactly one Voice DNA file per author in {d} (found {len(fs)}) — never blend two", 4)
        probs = check_voice(fs[0].read_text())
    if probs:
        print("NOT OK:\n  - " + "\n  - ".join(probs)); sys.exit(4)
    print("ok")


if __name__ == "__main__":
    main()
