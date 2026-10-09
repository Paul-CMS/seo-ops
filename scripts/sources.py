#!/usr/bin/env python3
"""sources.py — research before asking (Paul, 2026-10-09; CM-056). Every source already on disk is searched for a
fact before the fact can become a question. Used by the evidence gate (evidence.py); read-only, no network, no cost.

    sources.py list   <slug>                       which sources exist on disk (and which do not)
    sources.py search <slug> <fact_key> [--page P] what the search finds for one fact (with citations)

Sources, in order (each one optional — a missing one is listed as "not on disk"):
    review   data/reviews/reviews.csv            Google review text, one row per review, no reviewer names (CM-027)
    review   data/reviews/reviews-summary.md     rating and count
    site     data/crawl/page-text.csv            the client's own site, body text per page (S05b)
    gbp      data/gbp/* · inputs/*gbp*           a Google Business Profile export
    grid     data/local-grid/*.md                local grid summary
    rankings data/rankings/rankings-summary.md   rankings summary
Search terms per fact: methodology/evidence-requirements.json → "find" ({service} and {city} are the page's own).
A hit is one sentence that matches every pattern of one term group. What a hit counts as in the grid is set per source
kind in evidence-requirements.json → "found_marks" (CM-056).
"""
import csv
import json
import re
import sys

from lib import ROOT, client_dir, read_json

REQ = ROOT / "methodology" / "evidence-requirements.json"


def _rel(p):
    return str(p.relative_to(ROOT))


def _csv(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def catalogue(slug):
    """[(kind, path relative to the client, exists)] — every place the search looks."""
    d = client_dir(slug)
    fixed = [("review", "data/reviews/reviews.csv"), ("review", "data/reviews/reviews-summary.md"),
             ("site", "data/crawl/page-text.csv")]
    out = [(k, r, (d / r).is_file()) for k, r in fixed]
    gbp = sorted(p for pat in ("data/gbp/*", "inputs/*gbp*", "inputs/*GBP*") for p in d.glob(pat)
                 if p.is_file() and p.suffix.lower() in (".json", ".csv", ".md", ".txt"))
    out += [("gbp", str(p.relative_to(d)), True) for p in gbp] or [("gbp", "data/gbp/ (a GBP export)", False)]
    grid = sorted(d.glob("data/local-grid/*.md"))
    out += [("grid", str(p.relative_to(d)), True) for p in grid] or [("grid", "data/local-grid/", False)]
    out.append(("rankings", "data/rankings/rankings-summary.md", (d / "data/rankings/rankings-summary.md").is_file()))
    return out


def documents(slug):
    """[{kind, label, text}] — every searchable unit (a review, a site page, a file)."""
    d = client_dir(slug)
    docs = []
    for kind, rel, ok in catalogue(slug):
        if not ok:
            continue
        p = d / rel
        if rel.endswith("reviews.csv"):
            for i, r in enumerate(_csv(p), 2):
                docs.append({"kind": "review", "text": r.get("text") or "",
                             "label": f"Google review {r.get('date', '')} ({rel} row {i})"})
        elif rel.endswith("page-text.csv"):
            for i, r in enumerate(_csv(p), 2):
                docs.append({"kind": "site", "text": r.get("text") or "",
                             "label": f"client site {r.get('url', '')} ({rel} row {i})"})
        else:
            docs.append({"kind": kind, "text": p.read_text(encoding="utf-8", errors="replace"), "label": rel})
    return docs


SENT = re.compile(r"(?<=[.!?])\s+|\n+")


def _groups(fact_key, page):
    terms = (read_json(REQ) or {}).get("find", {}).get(fact_key) or []
    subst = {"service": re.escape(page.get("service_variant") or page.get("name") or ""),
             "city": re.escape(page.get("city") or page.get("name") or "")}
    out = []
    for g in terms:
        g = [g] if isinstance(g, str) else g
        pats = []
        for t in g:
            for k, v in subst.items():
                if "{" + k + "}" in t:
                    if not v:
                        t = None
                        break
                    t = t.replace("{" + k + "}", v)
            if t is None:
                break
            pats.append(re.compile(t, re.I))
        else:
            out.append(pats)
    return out


def search(slug, fact_key, page=None, docs=None, limit=3):
    """{'hits': [{kind, label, quote}], 'searched': [labels of sources searched], 'missing': [sources not on disk],
    'terms': bool}. No terms for the fact → nothing is searched (the fact is not one a source can answer)."""
    page = page or {}
    groups = _groups(fact_key, page)
    cat = catalogue(slug)
    res = {"hits": [], "searched": [r for _, r, ok in cat if ok], "missing": [r for _, r, ok in cat if not ok],
           "terms": bool(groups)}
    if not groups:
        return res
    for doc in (docs if docs is not None else documents(slug)):
        for s in SENT.split(doc["text"]):
            s = s.strip()
            if s and any(all(p.search(s) for p in g) for g in groups):
                q = s if len(s) <= 220 else s[:217] + "…"
                res["hits"].append({"kind": doc["kind"], "label": doc["label"], "quote": q})
                break   # one sentence per document is enough to cite it
        if len(res["hits"]) >= limit:
            break
    return res


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "list":
        for kind, rel, ok in catalogue(sys.argv[2]):
            print(f"{kind:9} {'on disk    ' if ok else 'not on disk'} {rel}")
    elif len(sys.argv) >= 4 and sys.argv[1] == "search":
        page = {}
        if "--page" in sys.argv:
            import status as S
            page = S.load(sys.argv[2])["pages"].get(sys.argv[sys.argv.index("--page") + 1]) or {}
        print(json.dumps(search(sys.argv[2], sys.argv[3], page), indent=1))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
