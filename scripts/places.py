#!/usr/bin/env python3
"""places.py — the place research store and the Deep Research flow (CM-061; rewrite 3 §5). Research for a town and a
niche is done once and reused across clients.

    places.py prompt <slug> <place> [--state SC] [--depth auto|full|lite] [--stdout]
                                                              fill the Deep Research prompt (Prompt B) from the Brand Guide,
                                                              the approved site plan and the niche's angles.md
                                                              (methodology/niches/<niche>/) → build/places/prompts/<place>-<niche>.md
                                                              full: the niche's angles 1-5 + 6-8; lite: three FAQ-category
                                                              angles + 6-8. auto = the core GBP city full, other towns lite (D4)
    places.py identity <state> <place>                        place.json identity from the Wikidata API (free, no LLM):
                                                              official name, county, Wikidata ID, Wikipedia URL, the
                                                              Russian Doll chain (identity-all <slug>: every planned place)
    places.py ingest <slug> <report.md> [--place P --state SC --niche N]
                                                              parse the report's tables into the two layers
    places.py verify <state> <place> <niche>                  every URL loads (else dropped); the quote is on its page
                                                              (else listed for the Sonnet meaning check)
    places.py judge-all <state> <place> <niche> --slug S --run R [--confirmed]
                                                              the meaning check on the Claude API (llm.py place-judge,
                                                              Sonnet - Rewrite 4 Phase 2); no API key -> the researcher:
    places.py judge  <state> <place> <niche> --id ID --ok|--drop [--reason R]   record the Sonnet check's answer
    places.py status <slug>                                   planned places missing place or niche research, in the order
                                                              to do them (core GBP city, then planned-page priority), with
                                                              the prompt command for each
    places.py show   <state> <place> [<niche>]                the store's facts for a place

Layers (methodology/places/<state>/<place>/):  place.json = niche-free (identity, official limits, county,
neighbourhoods, landmarks) · <niche>.json = place × niche facts (permits, community rules, conditions, money, FAQ
questions). Each fact: id, fact, applies_to, source_url, publisher, source_type, date, quote, verified, added.
`applies_to = unincorporated` is never stated as a town rule. A fact older than 3 years is `stale` and re-checked
before use. Failed facts are dropped, never asked. Saved reports live in clients/<slug>/inputs/places/.
"""
import argparse
import json
import re
import sys
import urllib.request

import niches
from lib import ROOT, client_dir, die, git_commit, read_json, today, write_json

STORE = ROOT / "methodology" / "places"
STALE_YEARS = 3
OFFICIAL_TYPES = ("official", "code body", "manufacturer")
STATES = {"alabama": "AL", "arizona": "AZ", "arkansas": "AR", "california": "CA", "colorado": "CO", "connecticut": "CT",
          "delaware": "DE", "florida": "FL", "georgia": "GA", "idaho": "ID", "illinois": "IL", "indiana": "IN",
          "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
          "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
          "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
          "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
          "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
          "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA",
          "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY"}
FIELDS = ["id", "fact", "applies_to", "source_url", "publisher", "source_type", "date", "quote"]

FRAME = """You are researching {PLACE}, {STATE} for a {NICHE} business (primary category:
{PRIMARY_CATEGORY}; services: {SERVICES}). This is LOCAL research seen through
that niche: everything you report must be about how {NICHE} work and {NICHE}
customers are affected in {PLACE} specifically, current as of {YEAR}. Do not
research the services themselves, and say nothing about any specific company.

Scope: {PLACE} means the area inside {PLACE}'s official limits. Where a rule
differs for unincorporated {COUNTY} County addresses near {PLACE}, report both
and say which applies where.
{LITE}
Research these angles. For each, look for current official sources first.

"""
LITE_NOTE = """
This is a LITE run: research only the angles listed below (the niche angles 4 and 5
are not part of it). Keep each table short; "not found" is an acceptable answer.
"""
FIXED = """6. Places and entities (for local relevance)
   - Neighbourhoods and subdivisions inside {PLACE} limits (confirm each is
     inside).
   - Landmarks, waterways, districts and main roads, preferring ones tied to
     the conditions above (for example oceanfront areas most exposed to wind).

7. Identity
   - Official name, incorporated status, county, official website, Wikipedia
     URL and Wikidata ID.

8. Questions people in {PLACE} ask about {NICHE}
   - Locally specific questions (not generic ones) found in official FAQs,
     local news or community sources, each with its source.

Rules:
- Every fact needs its own source URL. No source, no fact.
- Source priority: government sites > code bodies and manufacturers >
  established local news > other. Never use a {NICHE} company's website as a
  source for a rule, a code or a requirement.
- Give each fact a date (published or effective). Flag anything older than
  3 years as possibly outdated.
- Don't guess or generalise from other towns. If you can't find something,
  say "not found" and list what you searched.

Output format (required, used for import):
For each angle above, a table with columns:
id | fact (one sentence) | applies_to (all of {PLACE} / named community /
unincorporated) | source_url | publisher | source_type (official / code body /
manufacturer / news / context) | date | short supporting quote (max 25 words)
Then a final table "Not found": angle | what was searched.
"""
ROUTE = {"1": "niche", "2": "niche", "3": "niche", "5": "niche", "6": "place", "7": "place"}   # 4: by relevance; 8: FAQ


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"['’`]", "", (t or "").lower())).strip("-")


def split_place(name, state=None):
    """'Beaufort, SC' -> ('Beaufort', 'SC'); 'Okatie' -> ('Okatie', state). A site plan may carry the state in the city."""
    m = re.match(r"^(.*?),\s*([A-Za-z]{2})\s*$", (name or "").strip())
    return (m.group(1).strip(), m.group(2).upper()) if m else ((name or "").strip(), (state or "").upper() or None)


def place_dir(state, place):
    return STORE / state.lower() / slugify(place)


def layer_path(state, place, niche=None):
    return place_dir(state, place) / ("place.json" if not niche else f"{slugify(niche)}.json")


def load_layer(state, place, niche=None):
    return read_json(layer_path(state, place, niche), None) or {"state": state.upper(), "place": place, "niche": niche,
                                                                 "facts": [], "dropped": [], "not_found": [],
                                                                 "questions": [], "identity": {}}


def commit(state, place, what):
    """The store is shared across clients: its changes are committed on their own, only the place's folder."""
    git_commit(f"places: {what} — {place}, {state.upper()}", paths=[str(place_dir(state, place).relative_to(ROOT))])


def save_layer(state, place, niche, data):
    p = layer_path(state, place, niche)
    p.parent.mkdir(parents=True, exist_ok=True)
    write_json(p, data)


# ------------------------------------------------------------------ the client's side: niche, state, services, county
def client_info(slug, place=None, state=None):
    import status as S
    st = S.load(slug)
    c = st["client"]
    industry = (c.get("industry") or "").strip()
    bg = client_dir(slug) / "brand-guide.md"
    bgt = bg.read_text(encoding="utf-8") if bg.exists() else ""
    primary = ""
    m = re.search(r"GBP primary category[^|]*\|\s*([^|]+)\|", bgt)
    if m:
        primary = re.split(r"\s+—\s+|\s+\(", m.group(1).strip())[0].strip()
    if re.search(r"no gbp", primary, re.I):
        primary = ""
    if len(industry.split()) > 3 and primary:   # a long industry line is not a niche: use the primary category
        industry = primary.lower()
    niche = slugify(industry)
    services = [re.sub(r"\s*\([^)]*\)", "", p["name"]).strip() for p in st["pages"].values()
                if p.get("type") == "service" and p.get("name")]   # "Stair Lifts (parent; …)" → "Stair Lifts"
    county = ""
    for p in st["pages"].values():
        if p.get("type") == "location" and (p.get("city") or p.get("name")) == place and p.get("group"):
            if re.search(r"County$", p["group"].strip()):   # a metro hub (HMM) is not a county: left for the prompt's wording
                county = re.sub(r"\s+County$", "", p["group"].strip())
    core = core_city(bgt)
    if not state:
        state = c.get("state")
    if not state and core:
        state = core[1]
    if not state:
        low = bgt.lower()
        counts = {abbr: low.count(name) for name, abbr in STATES.items() if name in low}
        state = max(counts, key=counts.get) if counts else None
    return {"niche": niche, "industry": industry, "primary": primary or industry,
            "services": services, "county": county, "state": (state or "").upper() or None, "st": st, "core": core}


def core_city(bgt):
    """(city, 'SC') of the GBP address — the Brand Guide's confirmed NAP row — or None. The core GBP city anchors the
    homepage, the primary service page and the area entity, so it is researched first and at full depth (D4)."""
    row = next((l for l in bgt.splitlines() if re.search(r"Confirmed NAP", l)), "")
    m = re.search(r",\s*([^,·|]+?),\s*([A-Z]{2})\s+\d{5}", row)
    return (m.group(1).strip(), m.group(2)) if m else None


def planned_places(st):
    return sorted({p.get("city") or p.get("name") for p in st["pages"].values()
                   if p.get("type") == "location" and (p.get("city") or p.get("name"))})


def is_core(name, core):
    return bool(core) and split_place(name)[0].lower() == core[0].lower()


def ordered_places(st, core=None):
    """Planned places in the order the research is done: the core GBP city first, then the towns by planned-page
    priority — the build plan's batch order (the pilot first), then the order of the site plan. A core GBP city with
    no location page planned still leads the list."""
    batches = (st.get("build") or {}).get("batches") or []
    first = {}
    for i, b in enumerate(batches):
        for pid in b.get("pages", []):
            first.setdefault(pid, i)
    rows = []
    for n, (pid, p) in enumerate(st["pages"].items()):
        name = p.get("city") or p.get("name")
        if p.get("type") == "location" and name:
            rows.append((0 if is_core(name, core) else 1, first.get(pid, len(batches)), n, name))
    out = []
    for *_, name in sorted(rows):
        if name not in out:
            out.append(name)
    if core and not any(is_core(x, core) for x in out):
        out.insert(0, f"{core[0]}, {core[1]}")
    return out


def build_prompt(vals, mod, depth):
    """Prompt B: the fixed frame, the niche's angles (full: its 1–5; lite: its three FAQ-category angles), then the
    fixed angles 6–8, the rules and the output format. `mod` is niches.load_angles()."""
    angles = mod["lite"] if depth == "lite" else mod["full"]
    head = FRAME.replace("{LITE}", LITE_NOTE if depth == "lite" else "")
    text = head + niches.render_angles(angles, vals) + FIXED
    for k, v in vals.items():
        text = text.replace("{" + k + "}", v)
    return text.replace("unincorporated  County", "unincorporated county")


def cmd_prompt(a):
    full = a.place
    a.place, hint = split_place(a.place, a.state)
    info = client_info(a.slug, full, hint or a.state)
    if not info["state"]:
        die("REFUSED — the state is not recorded for this client and the Brand Guide names none. Add --state SC (two letters).", 4)
    mod = niches.load_angles(info["niche"])
    if not mod:
        die(f"REFUSED — there is no niche module for '{info['niche']}': methodology/niches/<niche>/angles.md (one per niche, "
            f"written once; see methodology/niches/README.md). The place prompt is built from it, never from another "
            f"trade's angles.", 4)
    core = is_core(a.place, info["core"])
    depth = a.depth if a.depth != "auto" else ("full" if core or not info["core"] else "lite")
    vals = {"PLACE": a.place, "STATE": info["state"], "NICHE": info["industry"] or info["niche"],
            "PRIMARY_CATEGORY": info["primary"], "SERVICES": ", ".join(info["services"]) or "see the site plan",
            "COUNTY": info["county"], "YEAR": today()[:4]}
    txt = build_prompt(vals, mod, depth)
    out = client_dir(a.slug) / "build" / "places" / "prompts" / f"{slugify(a.place)}-{info['niche']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(txt, encoding="utf-8")
    if a.stdout:
        print(txt)
        return
    why = "core GBP city" if core else ("every other planned town" if info["core"] else "the GBP city is not known")
    print(f"prompt for {a.place}, {info['state']} ({info['industry']}) — {depth} depth ({why}; niche module "
          f"{mod['dir'].name}) → {out.relative_to(ROOT)}\n"
          f"Paste it into Gemini Deep Research, then save the report as "
          f"clients/{a.slug}/inputs/places/{slugify(a.place)}-{info['niche']}.md and run: "
          f"python3 scripts/places.py ingest {a.slug} clients/{a.slug}/inputs/places/{slugify(a.place)}-{info['niche']}.md")


# ------------------------------------------------------------------ ingest
def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_report(text, extra=()):
    """→ ([(angle, row dict)], [(angle, what was searched)]) from the report's tables. `extra`: more columns to keep
    (Prompt A's "entity or service" as `entity`)."""
    facts, nf = [], []
    angle, head, nf_table = None, None, False
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            head = None
            m = re.match(r"^(?:#{1,6}\s*|\*\*)?\s*(?:angle\s*|section\s*)?([1-8])\s*[.):\-—]", s, re.I)
            if m:
                angle = m.group(1)
            nf_table = bool(re.search(r"not found", s, re.I))
            continue
        if re.match(r"^\|[\s\-:|]+\|$", s):
            continue
        cells = _cells(s)
        low = [c.lower() for c in cells]
        if head is None:   # a header row
            if any(x.startswith("fact") for x in low) and any("source" in x for x in low):
                head = [re.sub(r"[^a-z_]", "", x.split("(")[0].strip().replace(" ", "_")) for x in low]
                head = [{"short_supporting_quote": "quote", "supporting_quote": "quote", "source": "source_url",
                         "url": "source_url", "applies": "applies_to", "entity_or_service": "entity",
                         "service": "entity"}.get(h, h) for h in head]
                nf_table = False
            elif low and low[0].startswith(("angle", "section")):
                head, nf_table = ["angle", "searched"], True
            else:
                head = []
            continue
        if head and head[:2] == ["angle", "searched"]:
            nf.append((cells[0], cells[1] if len(cells) > 1 else ""))
        elif head and angle:
            row = {h: cells[i] for i, h in enumerate(head) if i < len(cells)}
            row = {k: row.get(k, "") for k in (*FIELDS, *extra)} | {"angle": angle}
            if row["fact"] and row["source_url"] and not re.match(r"^(not found|none)", row["fact"], re.I):
                facts.append((angle, row))
    return facts, nf


def _applies(v, place):
    v = (v or "").strip()
    low = v.lower()
    if not v or low.startswith("all"):
        return "all"
    if "unincorp" in low:
        return "unincorporated"
    return v


def _niche_relevant(row, info):
    words = {w for w in re.findall(r"[a-z]{4,}", (info["industry"] + " " + info["niche"] + " " + " ".join(info["services"])).lower())}
    return any(w in (row["fact"] + " " + row["quote"]).lower() for w in words)


def _stale(date):
    m = re.search(r"(19|20)\d\d", date or "")
    return bool(m) and int(today()[:4]) - int(m.group(0)) >= STALE_YEARS


def _merge(layer, new):
    have = {(re.sub(r"\W+", " ", f["fact"]).lower(), f["source_url"]) for f in layer["facts"]}
    n = 0
    for f in new:
        key = (re.sub(r"\W+", " ", f["fact"]).lower(), f["source_url"])
        if key in have:
            continue
        have.add(key)
        angle, rid = f.pop("angle"), (f.get("id") or "").strip()
        taken = {x["id"] for x in layer["facts"] + layer["dropped"]}
        f["id"] = rid if rid and re.match(r"^[\w.\-]+$", rid) and rid not in taken else f"{angle}.{len(taken) + 1}"
        f.update({"verified": False, "added": today(), "stale": _stale(f.get("date"))})
        layer["facts"].append(f)
        n += 1
    return n


def cmd_ingest(a):
    rep = ROOT / a.report
    if not rep.is_file():
        die(f"no such report: {a.report}")
    m = re.match(r"^(.+?)-([a-z0-9-]+)\.md$", rep.name)
    info = client_info(a.slug, state=a.state)
    place = a.place or (m.group(1).replace("-", " ").title() if m else None) or die("--place is needed")
    niche = slugify(a.niche or info["niche"])
    if not info["state"]:
        die("REFUSED — the state is not known. Add --state SC.", 4)
    facts, nf = parse_report(rep.read_text(encoding="utf-8"))
    if not facts:
        die("REFUSED — the report has no fact tables in the required format (id | fact | applies_to | source_url | "
            "publisher | source_type | date | quote). Ask the VA to re-run the prompt.", 4)
    pl, ni = load_layer(info["state"], place), load_layer(info["state"], place, niche)
    pl["place"], ni["place"], ni["niche"] = place, place, niche
    new_p, new_n, qs = [], [], []
    for angle, row in facts:
        row["applies_to"] = _applies(row["applies_to"], place)
        row["source_type"] = (row["source_type"] or "").strip().lower()
        if angle == "8":
            qs.append({"question": row["fact"], "source_url": row["source_url"], "publisher": row["publisher"],
                       "date": row["date"]})
            continue
        if angle == "7":
            for rx, key in ((r"Q\d+", "wikidata"), (r"https?://\S*wikipedia\.org/\S+", "wikipedia")):
                hit = re.search(rx, row["fact"] + " " + row["source_url"])
                if hit:
                    val = hit.group(0).rstrip(").,")
                    if pl["identity"].get("source") == "wikidata-api" and pl["identity"].get(key) not in (None, val):
                        pl["identity"][f"report_{key}"] = val   # the API's identity stands; the report's is shown beside it
                    else:
                        pl["identity"][key] = val
        dest = ROUTE.get(angle) or ("niche" if _niche_relevant(row, info) else "place")
        (new_n if dest == "niche" else new_p).append(row)
    added_p, added_n = _merge(pl, new_p), _merge(ni, new_n)
    seen = {q["question"] for q in ni["questions"]}
    ni["questions"] += [q for q in qs if q["question"] not in seen]
    ni["not_found"] = [{"angle": x, "searched": y} for x, y in nf]
    save_layer(info["state"], place, None, pl)
    save_layer(info["state"], place, niche, ni)
    commit(info["state"], place, f"ingested {niche}")
    print(f"{place}, {info['state']}: {added_p} place fact(s) · {added_n} {niche} fact(s) · {len(qs)} question(s) · "
          f"{len(nf)} not found — saved to {place_dir(info['state'], place).relative_to(ROOT)}\n"
          f"Next: python3 scripts/places.py verify {info['state']} {place} {niche}")


# ------------------------------------------------------------------ verification
def fetch(url):
    """(status, text) — None status when it cannot be reached. Tests replace this."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (seo-ops place check)"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read(2_000_000).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", None), ""


def _plain(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s or "", flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def verify_layer(layer):
    cache, ok, dropped, check = {}, 0, 0, 0
    for f in list(layer["facts"]):
        if f.get("verified") is not False:
            continue
        code, body = cache.setdefault(f["source_url"], fetch(f["source_url"]))
        if code != 200:
            f["verified"] = "dropped"
            layer["dropped"].append({**f, "reason": f"URL did not load ({code or 'no answer'})"})
            layer["facts"].remove(f)
            dropped += 1
            continue
        q = _plain(f.get("quote")).strip(" .\"'…")
        if q and q in _plain(body):
            f["verified"], f["verified_how"], f["verified_on"] = True, "quote found on the page", today()
            ok += 1
        else:
            f["verified"], f["verified_how"] = "check", "URL loads; quote not found word for word — Sonnet meaning check"
            check += 1
    return ok, dropped, check


def cmd_verify(a):
    total = [0, 0, 0]
    for niche in [None] + ([slugify(a.niche)] if a.niche else []):
        layer = load_layer(a.state, a.place, niche)
        r = verify_layer(layer)
        save_layer(a.state, a.place, niche, layer)
        total = [x + y for x, y in zip(total, r)]
    commit(a.state, a.place, "verified")
    print(f"{a.place}, {a.state.upper()}: {total[0]} verified · {total[1]} dropped (URL failed) · {total[2]} for the "
          f"Sonnet meaning check (places.py judge-all reads them on the API; with no key, places.py show … --check "
          f"lists them and places.py judge records each)")


def cmd_judge(a):
    for niche in (None, slugify(a.niche) if a.niche else None):
        layer = load_layer(a.state, a.place, niche)
        f = next((x for x in layer["facts"] if x["id"] == a.id), None)
        if not f:
            continue
        if a.drop:
            f["verified"] = "dropped"
            layer["dropped"].append({**f, "reason": a.reason or "quote does not support the fact"})
            layer["facts"].remove(f)
        else:
            f["verified"], f["verified_how"], f["verified_on"] = True, a.reason or "meaning checked", today()
        save_layer(a.state, a.place, niche, layer)
        commit(a.state, a.place, f"judged {a.id}")
        print(f"{a.id}: {'dropped' if a.drop else 'verified'}")
        return
    die(f"no fact {a.id} in {a.place}")


def passage(body, quote, fact, width=1500):
    """The stretch of the page's plain text that shares the most words with the quote and the fact."""
    words = set(w for w in re.findall(r"[a-z0-9]+", _plain(f"{quote} {fact}")) if len(w) > 3)
    if not body or not words:
        return (body or "")[:width]
    toks = body.split(" ")
    span, step, best, at = width // 6, max(20, width // 12), -1, 0
    for i in range(0, max(1, len(toks)), step):
        win = " ".join(toks[i:i + span])
        sc = sum(w in win for w in words)
        if sc > best:
            best, at = sc, i
    return " ".join(toks[at:at + span])[:width]


def judge_layers(slug, run_id, job, context, layers, purpose, route, confirmed, save, where_label):
    """The meaning check on the API for every fact of the layers [(key, layer)] left at "check": supported → verified;
    not supported → dropped (never asked); unclear → left for the researcher. `save(key, layer)` stores a changed layer.
    Returns (n, items) or None when the job ran on its agent route (no key). Shared by places.py and niches.py."""
    import llm
    cache, items, where = {}, [], {}
    for key, layer in layers:
        for f in layer["facts"]:
            if f.get("verified") != "check":
                continue
            code, body = cache.setdefault(f["source_url"], fetch(f["source_url"]))
            if code != 200:
                continue
            items.append({"id": f["id"], "fact": f["fact"], "applies_to": f.get("applies_to", ""),
                          "quote": f.get("quote", ""), "passage": passage(_plain(body), f.get("quote", ""), f["fact"])})
            where[f["id"]] = key
    if not items:
        print(f"{where_label}: nothing waits for the meaning check")
        return None
    ans = llm.attempt(slug, run_id, job, context, items, f"{purpose} ({len(items)})", route, confirmed)
    if ans is None:
        return None
    who = f"meaning checked by llm.py {job} ({llm.JOBS[job]['model']})"
    n = {"supported": 0, "not_supported": 0, "unclear": 0}
    for key, layer in layers:
        for f in list(layer["facts"]):
            r = ans.get(f["id"]) if f["id"] in where and where[f["id"]] == key else None
            if not r:
                continue
            n[r["verdict"]] += 1
            if r["verdict"] == "supported":
                f["verified"], f["verified_how"], f["verified_on"] = True, f"{who}: {r['reason']}", today()
            elif r["verdict"] == "not_supported":
                f["verified"] = "dropped"
                layer["dropped"].append({**f, "reason": f"{who}: {r['reason']}"})
                layer["facts"].remove(f)
            else:
                f["verified_how"] = (f"URL loads; quote not found word for word; unclear on the API ({r['reason']}) - "
                                     "the researcher reads it")
        save(key, layer)
    print(f"{where_label}: {n['supported']} verified · {n['not_supported']} dropped · {n['unclear']} "
          f"unclear (left for the researcher: show … --check)"
          + (f" · {len(items) - len(ans)} not answered" if len(items) > len(ans) else ""))
    return n


def cmd_judge_all(a):
    """Every fact left for the meaning check, read on the Claude API (llm.py place-judge, Sonnet - Rewrite 4 Phase 2):
    supported -> verified; not supported -> dropped (never asked); unclear -> left for the researcher. No API key: the
    researcher reads them and records each with `places.py judge`, as before."""
    import run as R
    R.open_run(a.slug, a.run)
    layers = [(None, load_layer(a.state, a.place))]
    if a.niche:
        layers.append((slugify(a.niche), load_layer(a.state, a.place, slugify(a.niche))))
    n = judge_layers(a.slug, a.run, "place-judge", {"place": a.place, "state": a.state.upper(), "niche": a.niche or ""},
                     layers, f"place facts by meaning - {a.place}, {a.state.upper()}",
                     "the researcher reads each one and records it (places.py judge)", a.confirmed,
                     lambda niche, layer: save_layer(a.state, a.place, niche, layer), f"{a.place}, {a.state.upper()}")
    if n is not None:
        commit(a.state, a.place, "meaning checked on the API")


# ------------------------------------------------------------------ identity from Wikidata (free, no LLM)
WD_API = "https://www.wikidata.org/w/api.php"
COUNTY_RX = re.compile(r"\b(county|parish|borough)$", re.I)
COUNTRY = ("united states", "united states of america")


def wd_api(**params):
    """One Wikidata API call → dict ({} when it fails). Goes through fetch(), the one network hook tests replace."""
    import urllib.parse
    code, body = fetch(f"{WD_API}?{urllib.parse.urlencode({**params, 'format': 'json'})}")
    try:
        return json.loads(body) if code == 200 else {}
    except ValueError:
        return {}


def _wd_entities(ids, cache):
    need = [i for i in ids if i not in cache]
    if need:
        cache.update(wd_api(action="wbgetentities", ids="|".join(need), props="labels|claims|sitelinks", languages="en",
                            sitefilter="enwiki").get("entities") or {})
    return [cache.get(i) or {} for i in ids]


def _claim_ids(ent, prop):
    out = []
    for c in (ent.get("claims") or {}).get(prop, []):
        v = ((c.get("mainsnak") or {}).get("datavalue") or {}).get("value")
        if c.get("rank") != "deprecated" and isinstance(v, dict) and v.get("id"):
            out.append(v["id"])
    return out


def _claim_text(ent, prop):
    for c in (ent.get("claims") or {}).get(prop, []):
        v = ((c.get("mainsnak") or {}).get("datavalue") or {}).get("value")
        if isinstance(v, str):
            return v
    return ""


def _label(ent):
    return ((ent.get("labels") or {}).get("en") or {}).get("value", "")


def wd_chain(qid, cache, state_name):
    """The Russian Doll chain of a Wikidata place, smallest first: [{name, wikidata, type}] by following "located in
    the administrative territorial entity" (P131) up to the country. All parents of the first step are kept as
    `counties` (a town in two counties), the chain follows the first."""
    chain, counties, cur = [], [], qid
    for depth in range(7):
        ent = _wd_entities([cur], cache)[0]
        name = _label(ent)
        kind = ("country" if name.lower() in COUNTRY else "state" if name.lower() == (state_name or "").lower()
                else "county" if COUNTY_RX.search(name) else "place" if depth == 0 else "district")
        chain.append({"name": name, "wikidata": cur, "type": kind})
        parents = _claim_ids(ent, "P131")
        if depth == 0:
            _wd_entities(parents, cache)
            counties = [{"name": _label(cache.get(x) or {}), "wikidata": x} for x in parents
                        if COUNTY_RX.search(_label(cache.get(x) or {}))]
        if kind == "country" or not parents:
            break
        cur = parents[0]
    return chain, counties


def wd_identity(state, place):
    """The identity of a place from the Wikidata API: official name, county, Wikidata ID, Wikipedia URL, website and the
    Russian Doll chain (place → county → state → country). The candidate must sit inside the state — a "Beaufort" in
    another state is never taken. None when there is no confident match."""
    import urllib.parse
    state_name = next((n for n, ab in STATES.items() if ab == state.upper()), state).title()
    found = wd_api(action="wbsearchentities", search=place, language="en", type="item", limit=10).get("search") or []
    ids = [r["id"] for r in found if r.get("id")]
    cache = {}
    ents = dict(zip(ids, _wd_entities(ids, cache)))
    plain = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
    best = []
    for qid in ids:
        label = _label(ents[qid])
        if not label or plain(place) not in plain(label):
            continue
        chain, counties = wd_chain(qid, cache, state_name)
        if chain[0]["type"] != "county" and any(c["type"] == "state" for c in chain):   # a county that shares the name is not the town
            best.append((plain(label) != plain(place), qid, chain, counties))
    if not best:
        return None
    best.sort(key=lambda b: b[0])
    _, qid, chain, counties = best[0]
    ent = ents[qid]
    title = ((ent.get("sitelinks") or {}).get("enwiki") or {}).get("title", "")
    return {"official_name": chain[0]["name"], "wikidata": qid,
            "wikipedia": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="_,()'") if title else "",
            "county": counties[0]["name"] if counties else "", "counties": counties,
            "website": _claim_text(ent, "P856"), "chain": chain, "source": "wikidata-api", "checked": today(),
            "other_matches": len(best) - 1}


def fill_identity(state, place):
    """Store the Wikidata identity in place.json. → (identity, note) · (None, why)."""
    ident = wd_identity(state, place)
    if not ident:
        return None, f"no Wikidata item named {place} sits inside {state.upper()} — angle 7 of the report may still name it"
    pl = load_layer(state, place)
    pl["place"] = place
    old = pl["identity"].get("wikidata")
    if old and old != ident["wikidata"] and pl["identity"].get("source") != "wikidata-api":
        ident["report_wikidata"] = old   # the Deep Research report named another item: shown, never silently kept
    pl["identity"].update(ident)
    if pl["identity"].get("report_wikidata") == ident["wikidata"]:
        del pl["identity"]["report_wikidata"]
    save_layer(state, place, None, pl)
    commit(state, place, "identity from Wikidata")
    return pl["identity"], ""


def _say_identity(place, ident):
    chain = " → ".join(c["name"] for c in ident["chain"])
    extra = (f" · the report named {ident['report_wikidata']} — check" if ident.get("report_wikidata") else "") + (
        f" · {ident['other_matches']} other match(es) in the state, the closest name taken" if ident.get("other_matches") else "")
    return f"{place}: {ident['wikidata']} · {chain}{extra}"


def cmd_identity(a):
    ident, why = fill_identity(a.state, a.place)
    if not ident:
        die(f"{a.place}, {a.state.upper()}: {why}", 4)
    print(_say_identity(f"{a.place}, {a.state.upper()}", ident))


def cmd_identity_all(a):
    info = client_info(a.slug)
    if not info["state"]:
        die("REFUSED — the state is not recorded for this client; pass it with --state.", 4)
    done = miss = 0
    for pl in ordered_places(info["st"], info["core"]):
        name, stt = split_place(pl, info["state"])
        if (load_layer(stt, name)["identity"] or {}).get("source") == "wikidata-api":
            continue
        ident, why = fill_identity(stt, name)
        done, miss = done + bool(ident), miss + (not ident)
        print(_say_identity(pl, ident) if ident else f"{pl}: {why}")
    print(f"identity: {done} filled from Wikidata · {miss} not found" if done or miss else "every planned place has its identity")


# ------------------------------------------------------------------ use in packs and status
def usable(state, place, niche):
    """[(layer, fact)] a pack may use: verified, not stale, from the place and niche layers."""
    out = []
    for lay in ("place", "niche"):
        d = load_layer(state, place, niche if lay == "niche" else None)
        if lay == "niche" and not niche:
            continue
        out += [(lay, f) for f in d["facts"] if f.get("verified") is True and not f.get("stale")]
    return out


def have(state, place, niche):
    return layer_path(state, place).is_file(), layer_path(state, place, niche).is_file()


def cmd_status(a):
    """The research still to do, in the order to do it: the core GBP city first (full depth), then the other planned
    towns by planned-page priority (lite depth, D4)."""
    info = client_info(a.slug)
    st = info["st"]
    if not info["state"]:
        die("REFUSED — the state is not recorded for this client; pass it to `places.py prompt --state`.", 4)
    order = ordered_places(st, info["core"])
    todo, no_ident = [], []
    for pl in order:
        name, stt = split_place(pl, info["state"])
        p, n = have(stt, name, info["niche"])
        depth = "core GBP city · full" if is_core(pl, info["core"]) else "lite"
        if not (p and n):
            todo.append((pl, "place" if not p else "", "niche" if not n else "", depth))
        if not p or (load_layer(stt, name)["identity"] or {}).get("source") != "wikidata-api":
            no_ident.append(pl)
    mod = niches.load_angles(info["niche"])
    head = (f"{len(order)} planned place(s) · {len(todo)} missing research" if todo else
            "every planned place has place and niche research")
    print(head + (f" · core GBP city: {info['core'][0]}" if info["core"] else " · GBP city not found in the Brand Guide NAP")
          + ("" if mod else f" · NO niche module for '{info['niche']}' (methodology/niches/<niche>/angles.md)"))
    cmd = lambda pl: f'python3 scripts/places.py prompt {a.slug} "{pl}"'
    for i, (pl, mp, mn, depth) in enumerate(todo[:8], 1):
        print(f"  {i}. {pl} [{depth}]: missing {' + '.join(x for x in (mp, mn) if x)} → {cmd(pl)}")
    if len(todo) > 8:
        print(f"  … and {len(todo) - 8} more (places.py status lists them in build/places/status.md)")
    if no_ident:
        print(f"identity from Wikidata (free, no LLM) not filled for {len(no_ident)} place(s) → "
              f"python3 scripts/places.py identity-all {a.slug}")
    out = client_dir(a.slug) / "build" / "places" / "status.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{i}. {pl} [{depth}]: missing {' + '.join(x for x in (mp, mn) if x)} → `{cmd(pl)}`"
             for i, (pl, mp, mn, depth) in enumerate(todo, 1)]
    tail = (f"\nIdentity not yet filled from Wikidata: {', '.join(no_ident)} → "
            f"`python3 scripts/places.py identity-all {a.slug}`\n") if no_ident else ""
    out.write_text("# Place research status\n\nIn this order: the core GBP city first, then the planned pages' priority.\n\n"
                   + "\n".join(lines) + "\n" + tail, encoding="utf-8")


def cmd_show(a):
    for niche in ([None, slugify(a.niche)] if a.niche else [None]):
        d = load_layer(a.state, a.place, niche)
        print(f"{niche or 'place'}: {len(d['facts'])} fact(s), {len(d['dropped'])} dropped")
        for f in d["facts"]:
            if a.check and f.get("verified") != "check":
                continue
            print(f"  {f['id']} [{f.get('verified')}] {f['fact'][:110]} — {f['source_url']}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prompt"); s.add_argument("slug"); s.add_argument("place"); s.add_argument("--state")
    s.add_argument("--stdout", action="store_true")
    s.add_argument("--depth", choices=["auto", "full", "lite"], default="auto",
                   help="auto: the core GBP city full, every other planned town lite (D4)")
    s = sub.add_parser("ingest"); s.add_argument("slug"); s.add_argument("report"); s.add_argument("--place")
    s.add_argument("--state"); s.add_argument("--niche")
    s = sub.add_parser("verify"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s = sub.add_parser("judge"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s.add_argument("--id", required=True); g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--ok", action="store_true"); g.add_argument("--drop", action="store_true"); s.add_argument("--reason")
    s = sub.add_parser("judge-all"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s.add_argument("--slug", required=True, help="the client whose run pays (llm-costs.jsonl)")
    s.add_argument("--run", required=True); s.add_argument("--confirmed", action="store_true")
    s = sub.add_parser("status"); s.add_argument("slug")
    s = sub.add_parser("identity"); s.add_argument("state"); s.add_argument("place")
    s = sub.add_parser("identity-all"); s.add_argument("slug")
    s = sub.add_parser("show"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s.add_argument("--check", action="store_true")
    a = ap.parse_args()
    {"prompt": cmd_prompt, "ingest": cmd_ingest, "verify": cmd_verify, "judge": cmd_judge, "judge-all": cmd_judge_all,
     "status": cmd_status, "identity": cmd_identity, "identity-all": cmd_identity_all,
     "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    main()
