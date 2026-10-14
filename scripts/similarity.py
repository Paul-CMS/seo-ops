#!/usr/bin/env python3
"""similarity.py — the cross-page similarity check for location pages (CM-062; rewrite 3 §4).

    similarity.py <slug> <section> [--threshold 0.7]    sentences too alike across the section's drafts

Swap test, by script: every planned place name in a sentence is masked ("PLACE"), then each sentence is compared with
every sentence on the other pages of the section. A pair at or above the threshold (config.json
`location_similarity_threshold`, default 0.7; Jaccard over words) means the sentence would still be true after swapping
the city name for a neighbour — it is raised on the later page as a Fix (form: wording), rewritten by the section's one
apply run. review.py runs this itself in the drafts step of a location section; this CLI is for looking.
"""
import argparse
import hashlib
import re
import sys

import status as S
from lib import ROOT, client_dir, config, die

MIN_WORDS = 8
STOP = {"the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "is", "are", "at", "by", "with", "your", "you", "we"}


def _text(path):
    t = (ROOT / path).read_text(encoding="utf-8")
    t = re.sub(r"\A---.*?\n---\n", "", t, flags=re.S)
    lines = [ln for ln in t.splitlines() if ln.strip() and not ln.lstrip().startswith(("|", "#", "[", ">", "<", "```"))]
    t = " ".join(lines)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    return re.sub(r"[*_`]", "", t)


def _sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(re.findall(r"\w+", s)) >= MIN_WORDS]


def _mask(s, places):
    for pl in sorted(places, key=len, reverse=True):
        s = re.sub(r"\b" + re.escape(pl).replace(r"\ ", r"\s+") + r"\b", "PLACE", s, flags=re.I)
    return s


def _tokens(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}


def draft_file(p):
    return ((p.get("files") or {}).get("draft") or {}).get("file") or p.get("file")


def pairs(slug, section, st=None, threshold=None):
    """[(page, sentence, other page, other sentence, score)] — the later page of each pair carries the finding."""
    st = st or S.load(slug)
    b = S.batch(st, section) or die(f"no section '{section}'")
    thr = threshold or float(config().get("location_similarity_threshold") or 0.7)
    places = sorted({(p.get("city") or p.get("name")) for p in st["pages"].values()
                     if p.get("type") in ("location", "county") and (p.get("city") or p.get("name"))})
    docs = []
    for pid in b["pages"]:
        p = st["pages"].get(pid) or {}
        f = draft_file(p)
        if p.get("type") == "location" and f and (ROOT / f).is_file():
            docs.append((pid, [(s, _tokens(_mask(s, places))) for s in _sentences(_text(f))]))
    out, seen = [], set()
    for i, (pid, sents) in enumerate(docs):
        for pj, others in docs[:i]:
            for s, ts in sents:
                for o, to in others:
                    if not ts or not to or (pid, s) in seen:
                        continue
                    score = len(ts & to) / len(ts | to)
                    if score >= thr:
                        seen.add((pid, s))
                        out.append((pid, s, pj, o, round(score, 2)))
    return out


def findings(slug, section, st=None):
    """review.py findings (severity fix, category wording) — one per too-similar sentence, keyed page + rule + item."""
    out = []
    for pid, s, pj, o, score in pairs(slug, section, st):
        key = hashlib.sha1(_mask(s, []).encode()).hexdigest()[:8]
        out.append({"page": pid, "rule": "LOC-31", "item": f"sentence {key}", "severity": "fix", "category": "wording",
                    "finding": f"Sentence \"{s[:140]}\" is {int(score * 100)}% the same as one on {pj} once the city name is "
                               "masked — swap the city for a neighbour and it is still true. Rewrite it with this city's own fact.",
                    "note": f"also on {pj}: \"{o[:100]}\""})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("section"); ap.add_argument("--threshold", type=float)
    a = ap.parse_args()
    client_dir(a.slug)
    rows = pairs(a.slug, a.section, threshold=a.threshold)
    print(f"{len(rows)} too-similar sentence(s) across the {a.section} drafts")
    for pid, s, pj, o, score in rows[:8]:
        print(f"  {pid} ~ {pj} ({int(score * 100)}%): {s[:90]}")
    if len(rows) > 8:
        print(f"  … {len(rows) - 8} more")
    sys.exit(1 if rows else 0)


if __name__ == "__main__":
    main()
