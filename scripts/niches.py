#!/usr/bin/env python3
"""niches.py — the niche layer of the research store (Rewrite 4 Phase 6, plan §3 Prompt A). Research of the industry as
entities, done once per niche and reused by every client in it. Standard library only.

    niches.py prompt <slug> [--state SC]       Prompt A (niche and service entities) filled from the client's Brand Guide
                                               and site plan → build/niches/<niche>-prompt-a.md
    niches.py ingest <slug> <report.md> [--niche N --state SC]
                                               parse the Deep Research report into methodology/niches/<niche>/entities.json
    niches.py verify <niche>                   every URL loads (else dropped); the quote is on its page (else left for the
                                               meaning check); each entity's Wikipedia page loads and its Wikidata label matches
    niches.py judge-all <niche> --slug S --run R [--confirmed]
                                               the meaning check on the Claude API (llm.py niche-judge, Sonnet); no key → the
                                               researcher reads them and records each with `judge`
    niches.py judge <niche> --id ID --ok|--drop [--reason R]
    niches.py entity <niche> <name> --ok|--drop-wikidata|--drop-wikipedia      settle an entity's identifier by hand
    niches.py show <niche> [--check]           what the store holds for a niche
    niches.py list                             every niche: angles.md and entities.json present?

A niche folder (methodology/niches/<niche>/) holds two files. `angles.md` is the niche module for the place prompt
(Prompt B): written once by hand, parsed here (`load_angles`). `entities.json` is filled only by `ingest`:
  category   {name, wikipedia, wikidata, variants[]}  the GBP category's entity
  entities   [{name, section, wikipedia, wikidata, variants[], parent, kind}]  the service entities
  facts      [{id, section, entity, state, fact, source_url, publisher, source_type, date, quote, verified, …}]
             sections: attributes (3), state (4: licensing, code edition, programmes — `state` is the two letters)
  questions  [{entity, question, source_url, publisher, date}]  from official, manufacturer and programme FAQs (5)
  dropped, not_found
A fact older than 3 years is `stale`; a failed fact is dropped, never asked. The niche folder is the shared
store: its changes are committed on their own, only the niche's folder.
"""
import argparse
import re
import sys

from lib import ROOT, client_dir, die, git_commit, read_json, today, write_json

STORE = ROOT / "methodology" / "niches"
SECTIONS = {"1": "category", "2": "entity", "3": "attributes", "4": "state", "5": "questions"}

PROMPT_A = """You are mapping the {NICHE} industry as entities, for local businesses whose Google Business
Profile primary category is "{GBP_CATEGORY}", in the United States, current as of {YEAR}.
Say nothing about any specific company.

1. Category entity: the Wikipedia article and Wikidata ID that best match "{GBP_CATEGORY}";
   broader and narrower entities; real name variants people and Wikipedia use (no invented ones).
2. Service entities: for each of {SERVICES} (and any core service of this category missing from
   the list): Wikipedia article, Wikidata ID, common names/variants, parent/child services
   (a type of / part of), and whether it is a distinct entity or a sub-type.
3. For each service: its attributes — types and components, how the work is done (steps),
   what decides the cost (factors, not prices), lifespan/maintenance, safety standards and
   codes (e.g. ASME, ICC, NFPA) with the issuing body, federal rules, major manufacturers
   and their certification programmes.
4. State layer for {STATE}: the licence type required for this work, the licensing board's
   lookup page, the state building/accessibility code edition in force, state programmes
   or funding that pay for this work.
5. Questions customers commonly ask about each service, found in official, manufacturer or
   programme FAQs (not other contractors' blogs), each with its source.

Rules: every fact has its own source URL, publisher, source type (official / code body /
manufacturer / encyclopedia / news) and date; government > code bodies and manufacturers >
encyclopedias > news; never a contractor's website for a rule or code; "not found" with what
was searched rather than a guess.
Output: one table per section: id | entity or service | fact (one sentence) | source_url |
publisher | source_type | date | quote (max 25 words). Then "Not found": section | searched.
"""


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"['’`]", "", (t or "").lower())).strip("-")


# ------------------------------------------------------------------ the niche module (angles.md)
def _aliases(text):
    m = re.search(r"^aliases:\s*(.+)$", text, re.I | re.M)
    return [slugify(x) for x in re.split(r"[,;]", m.group(1)) if slugify(x)] if m else []


def folder(niche):
    """The niche folder for a client's niche slug: the folder of that name, else the one whose `Aliases:` line lists it."""
    key = slugify(niche)
    if not key or not STORE.is_dir():
        return None
    if (STORE / key).is_dir():
        return STORE / key
    for d in sorted(STORE.iterdir()):
        a = d / "angles.md"
        if a.is_file() and key in _aliases(a.read_text(encoding="utf-8")):
            return d
    return None


def _angles(block, label):
    """[(n, title, [lines])] from `### N. Title` blocks."""
    out = []
    for m in re.finditer(r"^###\s*(\d+)\s*[.):\-]\s*(.+?)\s*$\n(.*?)(?=^###\s|\Z)", block, re.M | re.S):
        lines = [l.rstrip() for l in m.group(3).splitlines() if l.strip()]
        out.append((int(m.group(1)), m.group(2).strip(), lines))
    if [n for n, _, _ in out] != list(range(1, len(out) + 1)):
        die(f"REFUSED — angles.md ({label}): the angles must be numbered 1, 2, 3 … in order.", 4)
    return out


def load_angles(niche):
    """{'name', 'dir', 'aliases', 'full': [(n, title, lines)], 'lite': […]} from the niche's angles.md, or None when the
    niche has none. A malformed file is refused: never a prompt built from half a module."""
    d = folder(niche)
    f = d / "angles.md" if d else None
    if not f or not f.is_file():
        return None
    text = f.read_text(encoding="utf-8")
    parts = re.split(r"^##\s+", text, flags=re.M)
    blocks = {}
    for p in parts[1:]:
        head = p.splitlines()[0].lower()
        if head.startswith("full"):
            blocks["full"] = p
        elif head.startswith("lite"):
            blocks["lite"] = p
    if set(blocks) != {"full", "lite"}:
        die(f"REFUSED — {f.relative_to(ROOT)} needs a '## Full-depth angles' and a '## Lite angles' section.", 4)
    full, lite = _angles(blocks["full"], "full"), _angles(blocks["lite"], "lite")
    if not 3 <= len(full) <= 5:
        die(f"REFUSED — {f.relative_to(ROOT)}: the full-depth section needs 3 to 5 angles (it has {len(full)}).", 4)
    if len(lite) != 3:
        die(f"REFUSED — {f.relative_to(ROOT)}: the lite section needs exactly 3 angles — local cost or decision · "
            f"logistics in this area · trust in this area (it has {len(lite)}).", 4)
    name = re.match(r"^#\s*(.+)", text)
    return {"name": name.group(1).strip() if name else d.name, "dir": d, "aliases": _aliases(text), "full": full, "lite": lite}


def render_angles(angles, vals):
    """The angles as the prompt's numbered list, placeholders filled ({PLACE}, {NICHE}, …)."""
    out = []
    for n, title, lines in angles:
        out.append(f"{n}. {title}\n" + "\n".join(("     " if l.startswith("  ") else "   ") + l.strip() for l in lines))
    text = "\n\n".join(out) + "\n\n"
    for k, v in vals.items():
        text = text.replace("{" + k + "}", v)
    return text


# ------------------------------------------------------------------ the entity store
def layer_path(niche):
    return STORE / slugify(niche) / "entities.json"


def load(niche):
    return read_json(layer_path(niche), None) or {"niche": slugify(niche), "category": {}, "entities": [], "facts": [],
                                                  "questions": [], "dropped": [], "not_found": []}


def save(niche, data):
    p = layer_path(niche)
    p.parent.mkdir(parents=True, exist_ok=True)
    write_json(p, data)


def commit(niche, what):
    git_commit(f"niches: {what} — {slugify(niche)}", paths=[str(layer_path(niche).parent.relative_to(ROOT))])


def usable(niche, state=None):
    """[fact] a page may use: verified and current, for any state or the given one."""
    d = load(niche)
    return [f for f in d["facts"] if f.get("verified") is True and not f.get("stale")
            and (not f.get("state") or not state or f["state"] == state.upper())]


# ------------------------------------------------------------------ the client's side
def cmd_prompt(a):
    import places
    info = places.client_info(a.slug, state=a.state)
    if not info["state"]:
        die("REFUSED — the state is not recorded for this client and the Brand Guide names none. Add --state SC.", 4)
    niche = folder(info["niche"]).name if folder(info["niche"]) else info["niche"]
    txt = PROMPT_A.format(NICHE=info["industry"] or info["niche"], GBP_CATEGORY=info["primary"],
                          SERVICES=", ".join(info["services"]) or "see the site plan", STATE=info["state"], YEAR=today()[:4])
    out = client_dir(a.slug) / "build" / "niches" / f"{niche}-prompt-a.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(txt, encoding="utf-8")
    if a.stdout:
        print(txt)
        return
    have = "has an entities.json already — the new report adds to it" if layer_path(niche).is_file() else "has no entities.json yet"
    print(f"Prompt A for {info['industry']} ({niche} {have}) → {out.relative_to(ROOT)}\n"
          f"Paste it into Gemini Deep Research, save the report as clients/{a.slug}/inputs/niches/{niche}.md and run: "
          f"python3 scripts/niches.py ingest {a.slug} clients/{a.slug}/inputs/niches/{niche}.md --niche {niche}")


# ------------------------------------------------------------------ ingest
QID = re.compile(r"\bQ\d{2,}\b")
WIKI = re.compile(r"https?://[a-z.]*wikipedia\.org/wiki/[^\s|)\]]+", re.I)


def _entity_from(row, section):
    text = f"{row['fact']} {row['source_url']}"
    q, w = QID.search(text), WIKI.search(text)
    variants = []
    m = re.search(r"(?:variants?|also called|also known as|names?)\s*:\s*([^.;]+)", row["fact"], re.I)
    if m:
        variants = [v.strip(" \"'") for v in re.split(r",| or ", m.group(1)) if v.strip(" \"'")]
    parent = None
    m = re.search(r"(?:a type of|a kind of|sub-?type of|part of|child of|parent(?: service)?:)\s*([A-Za-z][^.;,]*)", row["fact"], re.I)
    if m:
        parent = m.group(1).strip()
    kind = "sub-type" if re.search(r"sub-?type|a type of|a kind of", row["fact"], re.I) and parent else (
        "distinct" if re.search(r"distinct entity|own (wikipedia|wikidata)", row["fact"], re.I) or not parent else "part")
    return {"name": row["entity"], "section": section, "wikipedia": w.group(0).rstrip(").,") if w else "",
            "wikidata": q.group(0) if q else "", "variants": variants, "parent": parent, "kind": kind}


def _merge_entity(data, new):
    if new["section"] == "category":
        c = data["category"]
        c.update({k: v for k, v in {"name": new["name"], "wikipedia": new["wikipedia"], "wikidata": new["wikidata"]}.items()
                  if v and not c.get(k)})
        c["variants"] = sorted(set(c.get("variants", []) + new["variants"]))
        return
    ex = next((e for e in data["entities"] if slugify(e["name"]) == slugify(new["name"])), None)
    if not ex:
        data["entities"].append(new)
        return
    for k in ("wikipedia", "wikidata", "parent"):
        if new.get(k) and not ex.get(k):
            ex[k] = new[k]
    ex["variants"] = sorted(set(ex.get("variants", []) + new["variants"]))


def cmd_ingest(a):
    import places
    rep = ROOT / a.report
    if not rep.is_file():
        die(f"no such report: {a.report}")
    info = places.client_info(a.slug, state=a.state)
    niche = slugify(a.niche or (folder(info["niche"]).name if folder(info["niche"]) else info["niche"]))
    facts, nf = places.parse_report(rep.read_text(encoding="utf-8"), extra=("entity",))
    if not facts:
        die("REFUSED — the report has no tables in the required format (id | entity or service | fact | source_url | "
            "publisher | source_type | date | quote). Ask the VA to re-run Prompt A.", 4)
    if any(x[0] == "4" for x in facts) and not info["state"]:
        die("REFUSED — the report has a state layer (section 4) and the state is not known. Add --state SC.", 4)
    data = load(niche)
    seen = {re.sub(r"\W+", " ", f["fact"]).lower() + f["source_url"] for f in data["facts"] + data["dropped"]}
    added = {"entities": 0, "facts": 0, "questions": 0}
    for sec, row in facts:
        kind = SECTIONS.get(sec)
        if not kind:
            continue
        row["source_type"] = (row["source_type"] or "").strip().lower()
        if kind in ("category", "entity"):
            before = len(data["entities"]) + (1 if data["category"] else 0)
            _merge_entity(data, _entity_from(row, kind))
            added["entities"] += len(data["entities"]) + (1 if data["category"] else 0) - before
        if kind == "questions":
            if row["fact"] not in {q["question"] for q in data["questions"]}:
                data["questions"].append({"entity": row["entity"], "question": row["fact"], "source_url": row["source_url"],
                                          "publisher": row["publisher"], "date": row["date"]})
                added["questions"] += 1
            continue
        key = re.sub(r"\W+", " ", row["fact"]).lower() + row["source_url"]
        if key in seen:
            continue
        seen.add(key)
        taken = {x["id"] for x in data["facts"] + data["dropped"]}
        rid = (row.get("id") or "").strip()
        f = {"id": rid if rid and re.match(r"^[\w.\-]+$", rid) and rid not in taken else f"{sec}.{len(taken) + 1}",
             "section": kind, "entity": row["entity"], "state": info["state"] if kind == "state" else "",
             "fact": row["fact"], "applies_to": "all", "source_url": row["source_url"], "publisher": row["publisher"],
             "source_type": row["source_type"], "date": row["date"], "quote": row["quote"], "verified": False,
             "added": today(), "stale": places._stale(row["date"])}
        data["facts"].append(f)
        added["facts"] += 1
    data["not_found"] = [{"section": x, "searched": y} for x, y in nf]
    save(niche, data)
    commit(niche, "ingested Prompt A")
    print(f"{niche}: {added['entities']} entit(ies) · {added['facts']} fact(s) · {added['questions']} question(s) · "
          f"{len(nf)} not found — saved to {layer_path(niche).relative_to(ROOT)}\n"
          f"Next: python3 scripts/niches.py verify {niche}")


# ------------------------------------------------------------------ verification
def _label_ok(label, ent):
    """The Wikidata label is the entity (or one of its variants) apart from spacing and a plural: "Stairlift" is "Stair Lifts"."""
    squash = lambda t: re.sub(r"[^a-z0-9]+", "", (t or "").lower())
    lab = squash(label)
    want = {squash(n) for n in [ent["name"]] + ent.get("variants", []) if n}
    return bool(lab) and any(lab == w or (min(len(lab), len(w)) >= 5 and (lab in w or w in lab)) for w in want)


def _wikidata_label(places, qid):
    import json
    code, body = places.fetch(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json")
    if code != 200:
        return code, ""
    try:
        return 200, (((json.loads(body).get("entities") or {}).get(qid) or {}).get("labels") or {}).get("en", {}).get("value", "")
    except ValueError:
        return 200, ""


def verify_entities(data):
    """(ok, dropped, check): a Wikipedia URL that does not load is cleared; a Wikidata ID that does not exist is cleared;
    one whose English label does not match the entity or its variants waits for `entity --ok|--drop-wikidata`."""
    import places
    ok = dropped = check = 0
    cat = data.get("category") or {}
    for e in ([dict(cat, name=cat.get("name", ""), _cat=True)] if cat else []) + data["entities"]:
        real = cat if e.get("_cat") else e
        if real.get("wikipedia") and real.get("wikipedia_ok") is None:
            real["wikipedia_ok"] = places.fetch(real["wikipedia"])[0] == 200
            if not real["wikipedia_ok"]:
                data["dropped"].append({"id": f"entity:{real.get('name')}", "fact": f"Wikipedia: {real['wikipedia']}",
                                        "reason": "URL did not load"})
                real["wikipedia"] = ""
                dropped += 1
            else:
                ok += 1
        if real.get("wikidata") and real.get("wikidata_ok") is None:
            code, label = _wikidata_label(places, real["wikidata"])
            if code != 200:
                data["dropped"].append({"id": f"entity:{real.get('name')}", "fact": f"Wikidata: {real['wikidata']}",
                                        "reason": f"the Wikidata API has no such item ({code or 'no answer'})"})
                real["wikidata"], real["wikidata_ok"] = "", False
                dropped += 1
            elif _label_ok(label, e):
                real["wikidata_ok"], real["wikidata_label"] = True, label
                ok += 1
            else:
                real["wikidata_ok"], real["wikidata_label"] = "check", label
                check += 1
    return ok, dropped, check


def cmd_verify(a):
    import places
    data = load(a.niche)
    if not data["facts"] and not data["entities"]:
        die(f"nothing stored for {a.niche} — ingest a Prompt A report first", 4)
    ok, dropped, check = places.verify_layer(data)
    eok, edrop, echeck = verify_entities(data)
    save(a.niche, data)
    commit(a.niche, "verified")
    print(f"{a.niche}: {ok} fact(s) verified · {dropped} dropped (URL failed) · {check} for the meaning check; "
          f"entities: {eok} identifier(s) confirmed · {edrop} cleared · {echeck} label(s) to settle "
          f"(niches.py judge-all reads the facts on the API; with no key, niches.py show {a.niche} --check lists them and "
          f"niches.py judge / entity record each)")


def _find(data, fid):
    return next((f for f in data["facts"] if f["id"] == fid), None)


def cmd_judge(a):
    data = load(a.niche)
    f = _find(data, a.id) or die(f"no fact {a.id} in {a.niche}")
    if a.drop:
        f["verified"] = "dropped"
        data["dropped"].append({**f, "reason": a.reason or "quote does not support the fact"})
        data["facts"].remove(f)
    else:
        f["verified"], f["verified_how"], f["verified_on"] = True, a.reason or "meaning checked", today()
    save(a.niche, data)
    commit(a.niche, f"judged {a.id}")
    print(f"{a.id}: {'dropped' if a.drop else 'verified'}")


def cmd_entity(a):
    data = load(a.niche)
    cat = data.get("category") or {}
    ent = next((e for e in data["entities"] + ([cat] if cat else []) if slugify(e.get("name", "")) == slugify(a.name)), None)
    if not ent:
        die(f"no entity '{a.name}' in {a.niche}")
    if a.ok:
        ent["wikidata_ok"] = True
    elif a.drop_wikidata:
        ent["wikidata"], ent["wikidata_ok"] = "", False
    elif a.drop_wikipedia:
        ent["wikipedia"], ent["wikipedia_ok"] = "", False
    save(a.niche, data)
    commit(a.niche, f"entity {a.name}")
    print(f"{ent.get('name')}: {'wikidata confirmed' if a.ok else 'identifier cleared'}")


def cmd_judge_all(a):
    import llm
    import places
    import run as R
    R.open_run(a.slug, a.run)
    data = load(a.niche)
    n = places.judge_layers(a.slug, a.run, "niche-judge", {"niche": a.niche, "state": ""}, [(None, data)],
                            f"niche facts by meaning - {a.niche}", "the researcher reads each one and records it "
                            "(niches.py judge)", a.confirmed, lambda niche, layer: save(a.niche, layer), a.niche)
    if n is not None:
        commit(a.niche, "meaning checked on the API")


def cmd_show(a):
    d = load(a.niche)
    if not a.check:
        c = d.get("category") or {}
        print(f"{a.niche}: category {c.get('name') or '—'} {c.get('wikidata') or ''} · {len(d['entities'])} entit(ies) · "
              f"{len(d['facts'])} fact(s) · {len(d['questions'])} question(s) · {len(d['dropped'])} dropped")
        for e in d["entities"]:
            print(f"  {e['name']} [{e['kind']}{', ' + e['parent'] if e.get('parent') else ''}] {e.get('wikidata') or '—'} "
                  f"{e.get('wikipedia') or '—'}")
    for e in ([d["category"]] if d.get("category") else []) + d["entities"]:
        if e.get("wikidata_ok") == "check":
            print(f"  entity {e.get('name')}: Wikidata {e['wikidata']} is labelled '{e.get('wikidata_label')}' — "
                  f"niches.py entity {a.niche} \"{e.get('name')}\" --ok|--drop-wikidata")
    for f in d["facts"]:
        if a.check and f.get("verified") != "check":
            continue
        print(f"  {f['id']} [{f.get('verified')}] ({f['section']}{' ' + f['state'] if f.get('state') else ''}) "
              f"{f['fact'][:100]} — {f['source_url']}")


def cmd_list(a):
    if not STORE.is_dir():
        print("no niche folders yet")
        return
    for d in sorted(STORE.iterdir()):
        if not d.is_dir():
            continue
        ang = "angles.md" if (d / "angles.md").is_file() else "NO angles.md"
        ent = load(d.name)
        print(f"{d.name:20} {ang:12} entities.json: " + (f"{len(ent['entities'])} entities, {len(ent['facts'])} facts"
                                                         if (d / "entities.json").is_file() else "not researched yet (Prompt A)"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prompt"); s.add_argument("slug"); s.add_argument("--state"); s.add_argument("--stdout", action="store_true")
    s = sub.add_parser("ingest"); s.add_argument("slug"); s.add_argument("report"); s.add_argument("--niche"); s.add_argument("--state")
    s = sub.add_parser("verify"); s.add_argument("niche")
    s = sub.add_parser("judge"); s.add_argument("niche"); s.add_argument("--id", required=True)
    g = s.add_mutually_exclusive_group(required=True); g.add_argument("--ok", action="store_true")
    g.add_argument("--drop", action="store_true"); s.add_argument("--reason")
    s = sub.add_parser("judge-all"); s.add_argument("niche"); s.add_argument("--slug", required=True)
    s.add_argument("--run", required=True); s.add_argument("--confirmed", action="store_true")
    s = sub.add_parser("entity"); s.add_argument("niche"); s.add_argument("name")
    g = s.add_mutually_exclusive_group(required=True); g.add_argument("--ok", action="store_true")
    g.add_argument("--drop-wikidata", action="store_true"); g.add_argument("--drop-wikipedia", action="store_true")
    s = sub.add_parser("show"); s.add_argument("niche"); s.add_argument("--check", action="store_true")
    sub.add_parser("list")
    a = ap.parse_args()
    {"prompt": cmd_prompt, "ingest": cmd_ingest, "verify": cmd_verify, "judge": cmd_judge, "judge-all": cmd_judge_all,
     "entity": cmd_entity, "show": cmd_show, "list": cmd_list}[a.cmd](a)


if __name__ == "__main__":
    main()
