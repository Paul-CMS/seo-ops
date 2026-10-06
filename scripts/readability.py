#!/usr/bin/env python3
"""readability.py — the reading-level check (CM-047), self-critique E10 for commercial and blog drafts.

    readability.py <draft.md> [--exclude-terms terms.txt]      report; exit 1 if the page misses the target

Visitor-facing copy targets grade 7–8 (Flesch-Kincaid). Counted: the meta description and every prose
paragraph, FAQ answers included. Not counted: the header block's seo_title (excluded by CM-047), headings
(too short for a formula; the H1 restate test COM-11 covers the H1), tables, short list items (names:
neighborhoods, Things to Do, Top Sites), link-wheel placeholders, [NEED: …] markers, and every term in
--exclude-terms (the category and area entity terms, service names, named sources such as "Environmental
Protection Agency") — so the check never pushes a writer to drop an entity or a CM-040 source.

Target: page average ≤ 8.9 and no paragraph over grade 10. Each paragraph over 10 is listed for a
split or a plainer word. Then the writer still does the read-aloud pass (writing-commercial.md E10).
"""
import argparse
import re
import sys

PAGE_MAX, PARA_MAX = 8.9, 10.0


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def grade(text):
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n", text) if re.search(r"[A-Za-z]", s)]
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", text)
    if not sents or not words:
        return None, 0
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59, len(words)


def units(md, terms):
    """[(section heading, paragraph text)] — prose only, as described above."""
    head, body = {}, md
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if m:
        body = md[m.end():]
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            head[k.strip()] = v.strip()
    out = []
    if head.get("meta_description"):
        out.append(("meta description", head["meta_description"]))
    section, para = "opening", []

    def flush():
        if para:
            out.append((section, " ".join(para)))
            para.clear()
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("#"):
            flush(); section = s.lstrip("#").strip(); continue
        if not s or s.startswith("|") or s.startswith("<"):
            flush(); continue
        if re.match(r"^([-*]|\d+\.)\s", s):
            item = re.sub(r"^([-*]|\d+\.)\s+", "", s)
            if len(item.split()) < 6:      # a name, not a sentence
                flush(); continue
            s = item if item.endswith((".", "!", "?")) else item + "."
        para.append(s)
    flush()
    cleaned = []
    for sec, t in out:
        t = re.sub(r"\[NEED:[^\]]*\]", "", t)
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
        for term in terms:
            t = re.sub(re.escape(term), "it", t, flags=re.I)
        t = re.sub(r"[*_`]", "", t)
        cleaned.append((sec, t))
    return cleaned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft"); ap.add_argument("--exclude-terms")
    a = ap.parse_args()
    terms = sorted({l.strip() for l in open(a.exclude_terms) if l.strip()}, key=len, reverse=True) if a.exclude_terms else []
    rows = [(sec, t, *grade(t)) for sec, t in units(open(a.draft, encoding="utf-8").read(), terms)]
    rows = [r for r in rows if r[2] is not None]
    if not rows:
        print("no prose to score"); return
    total = sum(r[3] for r in rows)
    avg = sum(r[2] * r[3] for r in rows) / total
    hard = [r for r in rows if r[2] > PARA_MAX and r[3] >= 12]
    print(f"Reading level (Flesch-Kincaid, CM-047): page average grade {avg:.1f} over {total} words — "
          f"target 7–8 (≤ {PAGE_MAX}), no paragraph over {PARA_MAX:.0f}")
    by = {}
    for sec, _, g, n in rows:
        by.setdefault(sec, []).append((g, n))
    for sec, gs in by.items():
        n = sum(x[1] for x in gs)
        print(f"  {sum(g * w for g, w in gs) / n:5.1f}  {sec[:70]}")
    for sec, t, g, n in hard:
        print(f"  OVER {g:.1f} in '{sec[:40]}': {t[:140]}{'…' if len(t) > 140 else ''}")
    if avg > PAGE_MAX or hard:
        print("E10 FAILS — split long sentences and swap long words; keep entity terms and named sources.")
        sys.exit(1)
    print("E10 passes (now the read-aloud pass).")


if __name__ == "__main__":
    main()
