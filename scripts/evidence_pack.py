#!/usr/bin/env python3
"""evidence_pack.py — one evidence pack per page, built by script before any brief (CM-061 part 1; rewrite 3 §3.2).

    evidence_pack.py build <slug> <section> [--page P] [--run R]   build build/<section>/packs/<page-id>.md (+ .json)
    evidence_pack.py show  <slug> <page_id>                        print a page's pack
    evidence_pack.py viability <slug> <section>                    score each location from its pack (§8)

<section> is the batch id in the site plan (services, locations, pilot …). The pack is the read list for the brief and
draft writers: they never search the raw files, they use the pack. It collects, for the page's service and/or place:

  Facts       every facts.json row relevant to the page, with status and source, plus the page's own facts file
  Reviews     every review sentence matching the service, the place or a practice (photos, clean-up, communication,
              speed, warranty, insurance claims, permits, named staff) — quoted with date, counted by independent
              reviewer, and marked "checked by meaning" (the researcher's pass, reviews.py checked) or "keyword match
              only"; each topic carries its usage tier (writing-commercial.md, "Usage tiers")
  Questions   PAA questions and fan-out queries seen for this page's service or place, with how often
  Site + GBP  sentences from the client's own pages and GBP that name the service or place (site_stated)
  Public      the area source list rows for this place (methodology/sources/) and earlier research-log results
  Settled     decisions-settled.md entries that touch this page
  Gaps        each evidence item (evidence-requirements.json) with no excerpt yet — the only things research looks for

The .json beside each pack holds the excerpts for the usage check in the draft review (review.py usage). Read-only
apart from the pack files and the page's pack record in status.json (sha, counts).
"""
import argparse
import csv
import json
import re
import sys

import status as S
from lib import ROOT, append, client_dir, die, now, read_json, sha12

REQ = ROOT / "methodology" / "evidence-requirements.json"
SOURCES = ROOT / "methodology" / "sources"
PRACTICES = {   # topic -> (regex, the facts.json R keys whose meaning check covers it)
    "photos": (r"\bphotos?\b|\bpictures?\b", ["practice:photos"]),
    "clean-up": (r"\bclean(ed|ing)?[- ]?up\b|\btidy\b|\bmagnet\b|\bdebris\b", ["practice:clean-up"]),
    "communication": (r"\bcommunicat\w*|\bresponsive\b|\bkept (us|me) (informed|updated|posted)\b|\bexplain(ed|s)?\b",
                      ["practice:explains"]),
    "speed": (r"\bquick(ly)?\b|\bprompt(ly)?\b|\bsame[- ]day\b|\bnext day\b|\bon time\b|\bright away\b",
              ["fact:timeframe", "fact:response_time", "fact:guarantees"]),
    "warranty": (r"\bwarrant(y|ies)\b|\bguarantee", ["fact:warranty"]),
    "insurance claims": (r"\binsurance\b|\badjuster\b|\bclaim\b", ["fact:insurance"]),
    "permits": (r"\bpermits?\b", ["practice:permits"]),
}
MAX_QUOTES = 5
TIER_NOTE = {"known": "Customers mention… (3+ independent reviewers, checked by meaning)",
             "example": "attributed customer example only — no company claim",
             "unchecked": "keyword match only — an attributed example until the researcher checks it by meaning"}


def _csv(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


SENT = re.compile(r"(?<=[.!?])\s+|\n+")


# ------------------------------------------------------------------ what the page is about
def subjects(st, pid):
    """(service terms, place names) for the page."""
    p = st["pages"].get(pid) or die(f"page {pid} is not in the site plan")
    typ = p.get("type")
    services, places = [], []
    if typ == "service":
        services += [x for x in dict.fromkeys([p.get("name"), p.get("service_variant")]) if x] or [pid]
    elif typ in ("location", "county"):
        places.append(p.get("city") or p.get("name") or pid)
        if typ == "county":
            places += [st["pages"][x].get("city") or st["pages"][x].get("name") for x in (p.get("cities") or [])
                       if x in st["pages"]]
    return [s for s in services if s], [x for x in places if x]


def service_rx(name):
    """A sentence names the service when it has the phrase, or every content word (stemmed) of it."""
    words = [w for w in re.findall(r"[a-z]+", name.lower()) if w not in ("and", "the", "of", "services", "service")]
    phrase = re.compile(re.escape(name), re.I)
    stems = [re.compile(r"\b" + re.escape(w[:4] if len(w) > 4 else w), re.I) for w in words]
    return lambda s: bool(phrase.search(s) or (stems and all(x.search(s) for x in stems)))


def place_rx(name):
    rx = re.compile(r"\b" + re.escape(name).replace(r"\ ", r"\s+").replace("'", "['’]?") + r"\b", re.I)
    return lambda s: bool(rx.search(s))


# ------------------------------------------------------------------ the sections
def facts_rows(slug, pid, services, places):
    import facts
    rows = facts.load(slug)["facts"]
    terms = [t.lower() for t in services + places]
    out = []
    for r in rows:
        txt = f"{r.get('label', '')} {r.get('value', '')} {r.get('key', '')}".lower()
        if r["section"] == "D" or (r["section"] == "A") or any(t in txt for t in terms):
            if r["section"] == "R":
                continue   # review rows are shown with their quotes under Reviews
            out.append({"id": r["id"], "label": r.get("label", ""), "status": r.get("status", ""),
                        "value": _norm(r.get("value"))[:260], "source": _norm(r.get("source"))[:160]})
    pf = read_json(client_dir(slug) / "build" / "evidence" / f"{pid}.facts.json") or {}
    for k, v in (pf.get("facts") or {}).items():
        out.append({"id": f"page:{k}", "label": k.replace("_", " "), "status": str(v.get("status", "")),
                    "value": _norm(v.get("value"))[:260], "source": _norm(v.get("source"))[:160]})
    return out


def checked_keys(slug):
    import facts
    return {r.get("key"): r for r in facts.load(slug)["facts"] if r.get("section") == "R" and r.get("meaning_checked")}


def staff_names(slug):
    import facts
    return [r["key"].split(":", 1)[1] for r in facts.load(slug)["facts"]
            if r.get("section") == "R" and str(r.get("key", "")).startswith("staff:")]


def review_topics(slug, services, places):
    """{topic: {'matches', 'reviewers', 'quotes', 'tier', 'checked'}} from data/reviews/reviews.csv."""
    p = client_dir(slug) / "data" / "reviews" / "reviews.csv"
    if not p.is_file():
        return {}
    rows = _csv(p)
    need = int((read_json(REQ) or {}).get("review_min_independent") or 3)
    checked = checked_keys(slug)
    topics = {}
    for s in services:
        topics[f"service: {s}"] = (service_rx(s), [])
    for x in places:
        topics[f"place: {x}"] = (place_rx(x), [f"place:{x}"])
    for t, (rx, keys) in PRACTICES.items():
        r_ = re.compile(rx, re.I)
        topics[f"practice: {t}"] = ((lambda s, r_=r_: bool(r_.search(s))), keys)
    for name in staff_names(slug):
        topics[f"named staff: {name}"] = ((lambda s, n=name: re.search(rf"\b{re.escape(n)}\b", s) is not None),
                                          ["fact:staff", f"staff:{name}"])
    out = {}
    for topic, (test, keys) in topics.items():
        hits, people = [], set()
        for i, r in enumerate(rows, 2):
            who = r.get("reviewer_key") or r.get("review_id") or f"row{i}"
            for sent in SENT.split(r.get("text") or ""):
                if sent.strip() and test(sent):
                    if who not in people:
                        people.add(who)
                        hits.append({"date": r.get("date", ""), "quote": _norm(sent)[:240], "row": f"reviews.csv row {i}"})
                    break
        if not hits:
            continue
        chk = next((checked[k] for k in keys if k in checked), None)
        if chk and int(chk.get("count") or 0) >= need and len(people) >= need:
            tier = "known"
        elif len(people) >= need and not chk:
            tier = "unchecked"
        else:
            tier = "example"
        out[topic] = {"reviewers": len(people), "quotes": sorted(hits, key=lambda h: h["date"], reverse=True)[:MAX_QUOTES],
                      "tier": tier, "checked": bool(chk), "checked_at": (chk or {}).get("checked_at", "")[:10]}
    return out


def questions(slug, services, places):
    """[(kind, question, times_seen)] — PAA questions and fan-out queries seen for the page's service or place."""
    d = client_dir(slug) / "data"
    tests = [service_rx(s) for s in services] + [place_rx(x) for x in places]
    out = []
    for kind, rel, qcol, scol in (("PAA", "paa/paa-questions.csv", "question", "source_queries"),
                                  ("fan-out", "fanout/fanout-queries.csv", "query", "seeds")):
        p = d / rel
        if not p.is_file():
            continue
        for r in _csv(p):
            srcs = [x.strip() for x in str(r.get(scol) or "").split("|")]
            hits = [x for x in srcs if any(t(x) for t in tests)]
            if hits:
                out.append({"kind": kind, "q": _norm(r.get(qcol)), "seen": len(hits),
                            "total_seen": int(r.get("times_seen") or 0)})
    out.sort(key=lambda r: (-r["seen"], r["q"]))
    return out


def site_gbp(slug, services, places):
    import sources
    tests = [service_rx(s) for s in services] + [place_rx(x) for x in places]
    out = []
    for doc in sources.documents(slug):
        if doc["kind"] not in ("site", "gbp"):
            continue
        for sent in SENT.split(doc["text"]):
            if sent.strip() and any(t(sent) for t in tests):
                out.append({"kind": doc["kind"], "quote": _norm(sent)[:240], "label": doc["label"]})
                break
    return out[:12]


def area_rows(places):
    """Rows of the area source lists under a heading that names the place."""
    out = []
    for f in sorted(SOURCES.glob("*.md")):
        if f.name == "README.md":
            continue
        heading = None
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                heading = line[3:].strip()
                continue
            if heading and line.startswith("|") and not re.match(r"^\|[\s\-|:]+\|$", line.strip()) \
                    and "What it answers" not in line and any(place_rx(x)(heading) for x in places):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                out.append({"file": f"methodology/sources/{f.name}", "heading": heading, "answers": cells[0],
                            "source": cells[-1]})
    return out


def place_rows(slug, places):
    """§5: verified, current facts for these places from the place store (place layer + this client's niche layer)."""
    import places as P
    info = P.client_info(slug)
    if not info["state"]:
        return []
    out = []
    for full in places:
        pl, stt = P.split_place(full, info["state"])
        for layer, f in P.usable(stt, pl, info["niche"]):
            tier = "official" if f.get("source_type") in P.OFFICIAL_TYPES else "context"
            out.append({"place": pl, "layer": layer, "id": f["id"], "fact": f["fact"], "applies_to": f["applies_to"],
                        "source_url": f["source_url"], "publisher": f["publisher"], "date": f["date"], "tier": tier})
    return out


def research_rows(slug, section, pid):
    p = client_dir(slug) / "build" / section / "research-log.csv"
    if not p.is_file():
        return []
    return [r for r in _csv(p) if r.get("page") in (pid, "*", "") and r.get("result") in ("found", "partial")]


def settled_rows(slug, pid, services, places):
    import settled
    terms = [pid.lower()] + [t.lower() for t in services + places]
    out = []
    for k, e in settled.entries(slug).items():
        if e.get("state") not in ("settled", "answered"):
            continue
        txt = f"{k} {e.get('text', '')} {e.get('question', '')} {e.get('note', '')}".lower()
        if any(t and t in txt for t in terms):
            out.append({"key": k, "text": _norm(e.get("text") or e.get("note") or e.get("question"))[:300],
                        "at": (e.get("at") or e.get("answered_at") or "")[:10]})
    return out


def gaps(slug, st, pid):
    """Evidence items with no excerpt yet (the grid's Unknown rows) — public or client, and who looks for them."""
    import evidence
    reqs = read_json(REQ) or {}
    public = set(reqs.get("public_facts") or [])
    lookup = set((reqs.get("verify_by_lookup") or {}).keys())
    rows, *_ = evidence.grid(slug, st, pid)
    out = []
    for r in rows:
        if r["mark"] != "Unknown":
            continue
        kind = ("researched" if r.get("researched") else "public" if r["from"] in public
                else ("lookup" if r["from"] in lookup else "client"))
        out.append({"key": r["key"], "label": r["label"], "need": r["need"], "from": r["from"], "kind": kind,
                    "fact_key": r["fact_key"]})
    return out


# ------------------------------------------------------------------ build
def build_one(slug, section, pid, run_id=None, st=None):
    st = st or S.load(slug)
    page = st["pages"].get(pid) or die(f"page {pid} is not in the site plan")
    services, places = subjects(st, pid)
    pack = {"page": pid, "type": page.get("type"), "url": page.get("url"), "section": section, "built": now(),
            "services": services, "places": places,
            "facts": facts_rows(slug, pid, services, places),
            "reviews": review_topics(slug, services, places),
            "questions": questions(slug, services, places),
            "site_gbp": site_gbp(slug, services, places),
            "public": area_rows(places), "research": research_rows(slug, section, pid),
            "place": place_rows(slug, places),
            "settled": settled_rows(slug, pid, services, places),
            "gaps": gaps(slug, st, pid)}
    ex = []
    for t, v in pack["reviews"].items():
        for q in v["quotes"]:
            ex.append({"id": f"R{len(ex) + 1}", "kind": "review", "topic": t, "tier": v["tier"], "text": q["quote"]})
    for s in pack["site_gbp"]:
        ex.append({"id": f"S{len(ex) + 1}", "kind": s["kind"], "topic": "site/GBP", "tier": "site_stated", "text": s["quote"]})
    for r in pack["research"]:
        ex.append({"id": f"P{len(ex) + 1}", "kind": "public", "topic": r.get("gap", ""), "tier": "official",
                   "text": _norm(r.get("excerpt"))})
    for r in pack["place"]:
        ex.append({"id": f"L{len(ex) + 1}", "kind": "place", "topic": r["place"], "tier": r["tier"], "text": r["fact"]})
    pack["excerpts"] = ex
    pack["known"] = [{"id": f["id"], "label": f["label"], "value": f["value"]} for f in pack["facts"]
                     if f["status"].lower().replace(" ", "_").startswith(("client_confirmed", "paul_approved",
                                                                          "internally_verified"))]
    pack["known"] += [{"id": t, "label": t, "value": v["quotes"][0]["quote"]} for t, v in pack["reviews"].items()
                      if v["tier"] == "known"]
    d = client_dir(slug) / "build" / section / "packs"
    d.mkdir(parents=True, exist_ok=True)
    md, js = d / f"{pid}.md", d / f"{pid}.json"
    md.write_text(render(st, pack))
    js.write_text(json.dumps(pack, indent=1, ensure_ascii=False) + "\n")
    counts = {"facts": len(pack["facts"]), "review_topics": len(pack["reviews"]),
              "review_excerpts": sum(len(v["quotes"]) for v in pack["reviews"].values()),
              "questions": len(pack["questions"]), "site_gbp": len(pack["site_gbp"]), "public": len(pack["public"]),
              "place": len(pack["place"]), "settled": len(pack["settled"]), "gaps": len(pack["gaps"]), "excerpts": len(ex)}
    st = S.load(slug)
    st["pages"][pid]["pack"] = {"file": str(md.relative_to(ROOT)), "json": str(js.relative_to(ROOT)), "sha": sha12(md),
                                "at": now(), "run": run_id, "section": section, "counts": counts}
    S.save(slug, st)
    return md, counts


def render(st, p):
    page = st["pages"][p["page"]]
    out = [f"# Evidence pack — {page.get('name') or p['page']} ({p['type']})", "",
           f"Section **{p['section']}** · {p.get('url') or ''} · built {p['built'][:16]} by evidence_pack.py (CM-061).", "",
           "_The only place the writer looks for facts. Write every excerpt at its usage tier "
           "(methodology/writing-commercial.md, \"Usage tiers\"). Reviewer names never appear on a page._", ""]
    out += ["## Facts", "", "| Id | Fact | Status | Value | Source |", "|---|---|---|---|---|"]
    out += [f"| {f['id']} | {f['label']} | {f['status']} | {f['value'].replace('|', '/')} | {f['source'].replace('|', '/')} |"
            for f in p["facts"]] or ["| — | none | | | |"]
    out += ["", "## Reviews", ""]
    if not p["reviews"]:
        out.append("_No review on file mentions this page's service, place or a practice._")
    for t, v in sorted(p["reviews"].items(), key=lambda kv: -kv[1]["reviewers"]):
        chk = f"checked by meaning {v['checked_at']}" if v["checked"] else "keyword match only (not yet checked by meaning)"
        out += [f"### {t} — {v['reviewers']} independent reviewer(s) · {chk}", f"Usage tier: {TIER_NOTE[v['tier']]}", ""]
        out += [f"- \"{q['quote']}\" ({q['date']}; {q['row']})" for q in v["quotes"]] + [""]
    out += ["## Questions (PAA and fan-out seen for this page)", ""]
    out += [f"- [{q['kind']}] {q['q']} — seen {q['seen']}× for this page ({q['total_seen']}× in all)"
            for q in p["questions"][:30]] or ["_None tagged to this page._"]
    out += ["", "## Site and GBP (site_stated)", ""]
    out += [f"- [{s['kind']}] \"{s['quote']}\" ({s['label']})" for s in p["site_gbp"]] or ["_Nothing on the client's site or GBP names it._"]
    out += ["", "## Public facts", ""]
    out += [f"- {r['heading']}: {r['answers']} — {r['source']} ({r['file']})" for r in p["public"]]
    out += [f"- research-log: {r.get('gap')} — \"{_norm(r.get('excerpt'))[:200]}\" ({r.get('url')}, {r.get('date')})"
            for r in p["research"]]
    if not p["public"] and not p["research"]:
        out.append("_No area source list rows or research results for this place yet._")
    out += ["", "## Place research (the place store: official facts are plain statements; context only for area character)", ""]
    out += [f"- [{r['tier']}] {r['place']} ({r['layer']}, applies to {r['applies_to']}): {r['fact']} — {r['publisher']}, "
            f"{r['source_url']} ({r['date']})" for r in p.get("place", [])] or [
        "_Nothing in the place store yet for this page's place (places.py status lists what is missing)._"]
    out += ["", "## Settled decisions touching this page", ""]
    out += [f"- {s['at']} · `{s['key']}` — {s['text']}" for s in p["settled"]] or ["_None._"]
    out += ["", "## Gaps — the only things research looks for", ""]
    who = {"public": "researcher (public fact — never asked)", "lookup": "researcher (verify by public lookup — never asked)",
           "client": "client search order, then an Ask (kind 3) only with a research-log entry",
           "researched": "researched, not found — shorten or drop the element (Fix and list); never a hold"}
    out += [f"- {g['label']} ({g['need']}, `{g['from']}`) → {who[g['kind']]}" for g in p["gaps"]] or ["_None._"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ §8 viability
def viability(slug, section=None):
    """[(pid, score, of, missing, verdict)] for the location pages of a section (or of every section): neighbourhoods,
    named place entities, local conditions, the Serving facts, and the three FAQ categories, from each pack and the place
    store (§8; CM-062)."""
    st = S.load(slug)
    bs = [S.batch(st, section) or die(f"no section {section}")] if section else S.batches(st)
    out = []
    for pid, sec in [(p, b["id"]) for b in bs for p in b["pages"]]:
        if (st["pages"][pid].get("type")) != "location":
            continue
        pk = read_json(client_dir(slug) / "build" / sec / "packs" / f"{pid}.json")
        if not pk:
            out.append((pid, 0, 7, ["no evidence pack yet — evidence.py run <slug> --run <RUN_ID> --all builds every pack"],
                        "no pack"))
            continue
        gap = {g["key"] for g in pk["gaps"]}
        qs = pk["questions"]
        pub = bool(pk["public"]) or bool(pk.get("place"))   # area source list rows or verified place-store facts
        items = {
            "neighbourhoods": "neighborhoods" not in gap or len([r for r in pk.get("place", []) if r["layer"] == "place"]) >= 3,
            "named place entities": "place_entities" not in gap or len(pk.get("place", [])) >= 3,
            "local conditions": "local_context" not in gap or pub,
            "serving facts (permit office, access, response)": "permit_office" not in gap or pub,
            "FAQ 1 · local cost or decision": pub or any(re.search(r"cost|price|hoa|arb|historic|flood|code", q["q"], re.I) for q in qs),
            "FAQ 2 · logistics in this area": pub or any(re.search(r"permit|how long|fast|storm|season|access", q["q"], re.I) for q in qs),
            "FAQ 3 · trust in this area": bool(pk["reviews"]),
        }
        miss = [k for k, ok in items.items() if not ok]
        score = len(items) - len(miss)
        out.append((pid, score, len(items), miss, "merge proposal" if score * 2 < len(items) else "viable"))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("build"); s.add_argument("slug"); s.add_argument("section"); s.add_argument("--page")
    s.add_argument("--run")
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("page")
    s = sub.add_parser("viability"); s.add_argument("slug"); s.add_argument("section", nargs="?")
    s.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.cmd == "show":
        st = S.load(a.slug)
        rec = (st["pages"].get(a.page) or {}).get("pack") or die(f"{a.page}: no evidence pack yet")
        print((ROOT / rec["file"]).read_text(), end="")
        return
    if a.cmd == "viability":
        if not a.section and not a.all:
            die("give a section or --all")
        rows = viability(a.slug, None if a.all else a.section)
        for pid, sc, of, miss, verdict in rows:
            print(f"{pid:28} {sc}/{of}  {verdict.upper():15} " + (f"missing: {', '.join(miss)}" if miss else ""))
        weak = [r[0] for r in rows if r[4] == "merge proposal"]
        if weak:
            print("Merge proposals for the site plan (an Ask, kind 1, merge recommended; a 301 if a URL exists): "
                  + ", ".join(weak))
        return
    st = S.load(a.slug)
    b = S.batch(st, a.section) or die(f"no section (batch) {a.section} in the site plan")
    pids = [a.page] if a.page else b["pages"]
    for pid in pids:
        if pid not in b["pages"]:
            die(f"{pid} is not in section {a.section}")
        md, c = build_one(a.slug, a.section, pid, a.run)
        print(f"{pid:28} facts {c['facts']} · reviews {c['review_excerpts']} ({c['review_topics']} topics) · "
              f"questions {c['questions']} · site/GBP {c['site_gbp']} · public {c['public']} · settled {c['settled']} · "
              f"gaps {c['gaps']}  ({md.relative_to(ROOT)})")
    if a.run:
        append(client_dir(a.slug) / "log.md", f"- EVIDENCE PACKS {now()[:16]} · run {a.run} · section {a.section} · "
               f"{len(pids)} page(s) · build/{a.section}/packs/\n")


if __name__ == "__main__":
    main()
