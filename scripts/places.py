#!/usr/bin/env python3
"""places.py — the place research store and the Deep Research flow (CM-061; rewrite 3 §5). Research for a town and a
niche is done once and reused across clients.

    places.py prompt <slug> <place> [--state SC] [--stdout]   fill the Deep Research prompt from the Brand Guide and
                                                              the approved site plan → build/places/prompts/<place>-<niche>.md
    places.py ingest <slug> <report.md> [--place P --state SC --niche N]
                                                              parse the report's tables into the two layers
    places.py verify <state> <place> <niche>                  every URL loads (else dropped); the quote is on its page
                                                              (else listed for the Sonnet meaning check)
    places.py judge  <state> <place> <niche> --id ID --ok|--drop [--reason R]   record the Sonnet check's answer
    places.py status <slug>                                   planned places missing place or niche research, with the
                                                              prompt command for each
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

PROMPT = """You are researching {PLACE}, {STATE} for a {NICHE} business (primary category:
{PRIMARY_CATEGORY}; services: {SERVICES}). This is LOCAL research seen through
that niche: everything you report must be about how {NICHE} work and {NICHE}
customers are affected in {PLACE} specifically, current as of {YEAR}. Do not
research the services themselves, and say nothing about any specific company.

Scope: {PLACE} means the area inside {PLACE}'s official limits. Where a rule
differs for unincorporated {COUNTY} County addresses near {PLACE}, report both
and say which applies where.

Research these angles. For each, look for current official sources first.

1. Permits and approvals for {NICHE} work in {PLACE} ({YEAR})
   - Which office issues permits for {NICHE} work (town, city or county), with
     its official page.
   - Which {NICHE} jobs need a permit and which don't (repair vs replacement
     thresholds, any percentage rules), required inspections, and typical fees
     if officially published.
   - Contractor licensing: state licence type required for {NICHE} work, and
     any local business licence {PLACE} requires.
   - Building code edition in force and any local amendments that affect
     {NICHE} work (wind, impact, fire, energy, flood).

2. Community and design rules affecting {NICHE} work
   - Historic districts or design-review boards in {PLACE} and what they
     require for {NICHE} work (materials, colours, approval steps).
   - Named HOAs, POAs or ARBs inside {PLACE} with published rules about
     {NICHE} work. Name each community and its rule, with the source.
   - Contractor access rules: gates, passes, decals, work-hour limits.

3. Environment and conditions that affect {NICHE} in {PLACE}
   - Climate factors relevant to {NICHE}: hurricane and wind exposure (design
     wind speed if published), salt air, humidity, heat, storms, flooding.
   - Named storms or weather events in the last 10 years that affected {PLACE}
     and are relevant to {NICHE}.
   - Flood zones and elevation rules (including any "substantial improvement"
     rule) that change {NICHE} work.

4. Housing stock and property types
   - Age and type of homes, common construction and materials relevant to
     {NICHE}, oceanfront or waterfront exposure, historic homes, gated
     communities, second homes or vacation rentals.

5. Money and incentives relevant to {NICHE} in {PLACE}
   - Local, county, state or utility rebates, tax credits or programmes that
     apply to {NICHE} work here.
   - Insurance factors specific to this area that affect {NICHE}, from official
     or insurer sources only.

6. Places and entities (for local relevance)
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
For each angle 1–8, a table with columns:
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
    if not state:
        state = c.get("state")
    if not state:
        low = bgt.lower()
        counts = {abbr: low.count(name) for name, abbr in STATES.items() if name in low}
        state = max(counts, key=counts.get) if counts else None
    return {"niche": niche, "industry": industry, "primary": primary or industry,
            "services": services, "county": county, "state": (state or "").upper() or None, "st": st}


def planned_places(st):
    return sorted({p.get("city") or p.get("name") for p in st["pages"].values()
                   if p.get("type") == "location" and (p.get("city") or p.get("name"))})


def cmd_prompt(a):
    full = a.place
    a.place, hint = split_place(a.place, a.state)
    info = client_info(a.slug, full, hint or a.state)
    if not info["state"]:
        die("REFUSED — the state is not recorded for this client and the Brand Guide names none. Add --state SC (two letters).", 4)
    txt = PROMPT.format(PLACE=a.place, STATE=info["state"], NICHE=info["industry"] or info["niche"],
                        PRIMARY_CATEGORY=info["primary"], SERVICES=", ".join(info["services"]) or "see the site plan",
                        COUNTY=info["county"], YEAR=today()[:4]).replace("unincorporated  County", "unincorporated county")
    out = client_dir(a.slug) / "build" / "places" / "prompts" / f"{slugify(a.place)}-{info['niche']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(txt, encoding="utf-8")
    if a.stdout:
        print(txt)
        return
    print(f"prompt for {a.place}, {info['state']} ({info['industry']}) → {out.relative_to(ROOT)}\n"
          f"Paste it into Gemini Deep Research, then save the report as "
          f"clients/{a.slug}/inputs/places/{slugify(a.place)}-{info['niche']}.md and run: "
          f"python3 scripts/places.py ingest {a.slug} clients/{a.slug}/inputs/places/{slugify(a.place)}-{info['niche']}.md")


# ------------------------------------------------------------------ ingest
def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_report(text):
    """→ ([(angle, row dict)], [(angle, what was searched)]) from the report's tables."""
    facts, nf = [], []
    angle, head, nf_table = None, None, False
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            head = None
            m = re.match(r"^(?:#{1,6}\s*|\*\*)?\s*(?:angle\s*)?([1-8])\s*[.):\-—]", s, re.I)
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
                         "url": "source_url", "applies": "applies_to"}.get(h, h) for h in head]
                nf_table = False
            elif low and low[0].startswith("angle"):
                head, nf_table = ["angle", "searched"], True
            else:
                head = []
            continue
        if head and head[:2] == ["angle", "searched"]:
            nf.append((cells[0], cells[1] if len(cells) > 1 else ""))
        elif head and angle:
            row = {h: cells[i] for i, h in enumerate(head) if i < len(cells)}
            row = {k: row.get(k, "") for k in FIELDS} | {"angle": angle}
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
                    pl["identity"][key] = hit.group(0).rstrip(").,")
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
          f"Sonnet meaning check (places.py show … --check lists them; places.py judge records each)")


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
    info = client_info(a.slug)
    st = info["st"]
    if not info["state"]:
        die("REFUSED — the state is not recorded for this client; pass it to `places.py prompt --state`.", 4)
    todo = []
    for pl in planned_places(st):
        name, stt = split_place(pl, info["state"])
        p, n = have(stt, name, info["niche"])
        if not (p and n):
            todo.append((pl, "place" if not p else "", "niche" if not n else ""))
    print(f"{len(planned_places(st))} planned place(s) · {len(todo)} missing research" if todo else
          "every planned place has place and niche research")
    for pl, mp, mn in todo[:8]:
        print(f"  {pl}: missing {' + '.join(x for x in (mp, mn) if x)} → python3 scripts/places.py prompt {a.slug} \"{pl}\"")
    if len(todo) > 8:
        print(f"  … and {len(todo) - 8} more (places.py status lists them in build/places/status.md)")
    out = client_dir(a.slug) / "build" / "places" / "status.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("# Place research status\n\n" + "\n".join(
        f"- {pl}: missing {' + '.join(x for x in (mp, mn) if x)} → `python3 scripts/places.py prompt {a.slug} \"{pl}\"`"
        for pl, mp, mn in todo) + "\n", encoding="utf-8")


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
    s = sub.add_parser("ingest"); s.add_argument("slug"); s.add_argument("report"); s.add_argument("--place")
    s.add_argument("--state"); s.add_argument("--niche")
    s = sub.add_parser("verify"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s = sub.add_parser("judge"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s.add_argument("--id", required=True); g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--ok", action="store_true"); g.add_argument("--drop", action="store_true"); s.add_argument("--reason")
    s = sub.add_parser("status"); s.add_argument("slug")
    s = sub.add_parser("show"); s.add_argument("state"); s.add_argument("place"); s.add_argument("niche", nargs="?")
    s.add_argument("--check", action="store_true")
    a = ap.parse_args()
    {"prompt": cmd_prompt, "ingest": cmd_ingest, "verify": cmd_verify, "judge": cmd_judge, "status": cmd_status,
     "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    main()
