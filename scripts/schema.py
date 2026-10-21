#!/usr/bin/env python3
"""schema.py — BB-6xx v1.1 schema by script, from the Brand Guide and the site plan (Rewrite 4 Phase 5, CM-064).

    schema.py config   <slug> [--out F]          Brand Guide A/D/F + the plan + each approved page → the builder's config
                                                 (finish/schema/config.json); the asset gate's misses are listed
    schema.py gate     <slug>                    the asset gate only — exit 2 with what is missing (nothing is built)
    schema.py build    <slug> [--offline]        gate → live entity check → every page's graph → validate → write
                                                 finish/schema/<page>.jsonld + .script.html + index.json (exit 2 gate or
                                                 entity check, 3 output check, 4 validator); nothing is written on a failure
    schema.py validate <slug> | <dir|file>       the validator on built files (exit 1 on any error)

The spec is the bb-schema-builder skill (.claude/skills/bb-schema-builder/SKILL.md, sop-source/BB-Standard-Schema-
Section-v1.1.md); its build_schema.py stays the one emitter — this script only builds its config and validates its
output. Node sets: homepage (and only the verified GBP landing page) = WebSite + Corporation + the LocalBusiness subtype;
service = WebPage + Service; location = WebPage + ItemList; county hub = WebPage only (its node set is Paul's open
ruling — never LocalBusiness, BB-604); about / contact / blog = not built (no observed rule: flagged, never invented).

Asset gate (kept): every page has an approved file whose URL is the planned URL (no pending URL change); Brand Guide
Section F gives the ID page URL, the Maps share link, the confirmed NAP, the schema subtype, the logo and the sameAs
URLs; the category, area and state Wikidata URIs are present. A [NEED: …] cell is missing, never guessed. Values read
elsewhere: brand, phone, domain and the GBP website URL from Section A; email, founding year (only a real year) and
hours from Section D; descriptions from F when given, else by formula from the approved A2 category and A5 area entity.
Offline (CM-053): `--offline` passes build_schema's own --offline <slug> (Paul's /approve <slug> schema-offline, once).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from lib import ROOT, client_dir, die, now, write_json

BUILDER = ROOT / ".claude" / "skills" / "bb-schema-builder" / "scripts"
sys.path.insert(0, str(BUILDER))
import build_schema as B  # noqa: E402

STATES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
          "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
          "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
          "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
          "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
          "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
          "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
          "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
          "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
          "WI": "Wisconsin", "WY": "Wyoming"}
URL = re.compile(r"https?://[^\s|)·,;\]]+")
SUBTYPE = re.compile(r"\b(LocalBusiness|[A-Z][a-z]+(?:[A-Z][a-z]+)*(?:Business|Contractor|Store|Service|Agency|Office|"
                     r"Clinic|Plumber|Electrician|Locksmith|Roofer|Dentist|Physician|Establishment))\b")
NEED = re.compile(r"\[NEED", re.I)
NOT_BUILT = ("about", "contact", "blog")


# ------------------------------------------------------------------ the Brand Guide
def _rows(bg, section):
    import outline
    return [r for r in outline.table_rows(outline.md_section(bg, section)) if r]


def _val(cell):
    return None if not cell or NEED.search(cell) else cell.strip()


def _f(bg):
    """{label: value} from Section F (None for a [NEED] cell)."""
    return {r[0].replace("**", "").strip(): _val(r[1]) for r in _rows(bg, r"Section F") if len(r) >= 2}


def _row(rows, rx):
    return next((v for k, v in rows.items() if re.search(rx, k, re.I)), None)


def _a(bg):
    return {r[0]: _val(r[2]) for r in _rows(bg, r"Section A") if len(r) >= 3}


def _d(bg):
    return {r[0]: _val(r[1]) for r in _rows(bg, r"Section D") if len(r) >= 2}


def phone_e164(v):
    d = re.sub(r"\D", "", v or "")
    d = d[1:] if len(d) == 11 and d.startswith("1") else d
    return f"+1-{d[:3]}-{d[3:6]}-{d[6:]}" if len(d) == 10 else None


def nap(v):
    """'Name · 2127 Boundary St #5, Beaufort, SC 29902 · (843) 476-1329' → address dict, or None."""
    for part in (v or "").split("·"):
        m = re.match(r"^\s*(.+?),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)\s*$", part)
        if m:
            return {"streetAddress": m.group(1).strip(), "addressLocality": m.group(2).strip(),
                    "addressRegion": m.group(3), "postalCode": m.group(4)}
    return None


def wikidata_pairs(v):
    """[(name, uri)] from 'Beaufort County https://…/Q495682 · Jasper …' or 'https://…/Q1 (Mobility aid, …)'."""
    out = []
    for part in (v or "").split("·"):
        m = re.search(r"(https://www\.wikidata\.org/wiki/Q\d+)", part)
        if not m:
            continue
        before = part[:m.start()].strip(" :—-")
        after = re.match(r"\s*\(([^,)]+)", part[m.end():])
        out.append(((before or (after.group(1) if after else "")).strip(), m.group(1)))
    return out


def hours(v):
    """'Monday–Friday 9:00 AM–5:00 PM; Saturday–Sunday closed' → the builder's hours rows."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def t24(s):
        m = re.match(r"(\d{1,2})(?::(\d{2}))?\s*([AP])M", s.strip(), re.I)
        if not m:
            return None
        h = int(m.group(1)) % 12 + (12 if m.group(3).upper() == "P" else 0)
        return f"{h:02d}:{m.group(2) or '00'}"
    out = []
    for seg in re.split(r"[;,]", v or ""):
        m = re.match(r"\s*([A-Z][a-z]+)(?:\s*[–-]\s*([A-Z][a-z]+))?\s+(\d.*?[AP]M)\s*[–-]\s*(\d.*?[AP]M)", seg)
        if not m or m.group(1) not in days:
            continue
        a, b = days.index(m.group(1)), days.index(m.group(2)) if m.group(2) in days else days.index(m.group(1))
        o, c = t24(m.group(3)), t24(m.group(4))
        if o and c:
            out.append({"days": days[a:b + 1], "opens": o, "closes": c})
    return out


def _clean(v):
    return re.sub(r"\s*\([^)]*\)|\*\*", "", v or "").split(" — ")[0].split(". ")[0].strip(" .")


# ------------------------------------------------------------------ the config
def approved_pages(st):
    import wheel
    out = {}
    for pid, p in st["pages"].items():
        if p.get("type") in ("service", "location", "county", "homepage", "about"):
            f = wheel.approved_file(st, pid)
            out[pid] = (p, f)
    return out


def build_config(slug, st, only=None):
    """(config, missing [(where, why)], notes) — the asset gate is the builder's entry gate plus the page checks here."""
    import publish
    import wheel
    import outline
    bg = outline.brand_guide(slug)
    if not bg:
        return None, [("brand-guide.md", "no Brand Guide")], []
    F, A, D = _f(bg), _a(bg), _d(bg)
    ent = outline.bg_entity(bg)
    missing, notes = [], []
    domain = (A.get("9") or st["client"].get("domain") or "")
    domain = domain if domain.startswith("http") else f"https://{domain}"
    domain = URL.search(domain).group(0).rstrip("/") if URL.search(domain) else domain.rstrip("/")
    addr = nap(_row(F, r"Confirmed NAP"))
    sub = SUBTYPE.search(_row(F, r"schema subtype") or "")
    if not sub:
        missing.append(("Brand Guide F · schema subtype", "name the LocalBusiness subtype (schema.org type, e.g. "
                        "HomeAndConstructionBusiness) for the GBP category — Paul's choice"))
    logo = next((u for u in URL.findall(_row(F, r"^Logo") or "") if re.search(r"\.(png|jpe?g|svg|webp|gif)$", u, re.I)), None)
    id_page = next(iter(URL.findall(_row(F, r"ID page URL") or "")), None)
    has_map = next((u for u in URL.findall(_row(F, r"Google Maps share") or "") if "maps" in u), None)
    same_as = []
    for rx in (r"citation list", r"Social profile", r"Apple Maps"):
        same_as += [u for u in URL.findall(_row(F, rx) or "") if u not in same_as]
    cites = _row(F, r"citation list")
    if cites is not None and not URL.findall(cites) and not re.match(r"^\s*none\b", cites, re.I):
        missing.append(("Brand Guide F · citation list → sameAs", "the listings are named but their URLs are not "
                        "collected — sameAs needs each profile's URL"))
    for u in (id_page, has_map):
        if u and u not in same_as:
            same_as.append(u)
    founding = re.match(r"^\s*((?:19|20)\d{2})\b", _row(D, r"^Founding year") or "")
    email = next(iter(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", _row(D, r"^E-?mail") or _row(F, r"e-?mail") or "")), None)
    cat = ent.get("category") or ""
    area = _clean(A.get("5"))
    owner = _row(F, r"^Owner name")
    owner = (owner or "").split(";")[0].strip() if owner else None
    state_abbr = (addr or {}).get("addressRegion") or ""
    state = STATES.get(state_abbr, state_abbr)
    gbp = next(iter(URL.findall(A.get("11") or "")), None)
    cfg = {"business": {"name": _clean(A.get("1")), "url": domain, "telephone": phone_e164(A.get("8")),
                        "email": email, "schema_type": sub.group(1) if sub else None, "id_page_url": id_page,
                        "founding_date": founding.group(1) if founding else None,
                        "description": _clean(_row(F, r"^Business description")) or
                        (f"{cat} serving the {area}." if cat and area else None),
                        "logo": logo, "address": addr or {}, "has_map": has_map,
                        **({"hours": hours(_row(D, r"^Hours"))} if hours(_row(D, r"^Hours")) else {})},
           "corporation": {"description": _clean(_row(F, r"^Brand description")) or
                           (f"{_clean(A.get('1'))}, a {cat.lower()} in the {area}." if cat and area else None),
                           **({"founder": {"name": owner}} if owner else {})},
           "gbp_landing_page": gbp, "same_as": same_as, "area_served": [],
           "service_catalog_label": f"{cat} services" if cat else "Services",
           "service_pages": [], "location_pages": [], "hub_pages": [],
           "catalog": [{"url": q["url"]} for q in st["pages"].values() if q.get("type") == "service" and q.get("url")]}
    if not founding:
        notes.append("foundingDate left out — Brand Guide D gives no founding year (never the owner's experience)")
    entities = [{"name": n or "category entity", "wikidata": u} for n, u in wikidata_pairs(_row(F, r"category entity"))]
    entities += [{"name": area or n, "wikidata": u} for n, u in wikidata_pairs(_row(F, r"area entity"))]
    entities += [{"name": state or n, "wikidata": u} for n, u in wikidata_pairs(_row(F, r"— state"))]
    for what, rx in (("category", r"category entity"), ("area", r"area entity"), ("state", r"— state")):
        if not wikidata_pairs(_row(F, rx)):
            missing.append((f"Brand Guide F · Wikidata URI — {what} entity", "the four Wikidata URIs are the asset gate (BB-606)"))
    counties = {n.lower(): {"name": n, "wikidata": u} for n, u in wikidata_pairs(_row(F, r"— county"))}
    pages = approved_pages(st)
    for pid, (p, f) in pages.items():
        t = p["type"]
        if t == "homepage" or (only and pid not in only):
            continue   # the homepage node set comes from Section F alone; a dry run builds only the pages named
        if t in NOT_BUILT:
            notes.append(f"{pid}: no schema — no observed node set for an {t} page (Paul's ruling open; never invented)")
            continue
        if not f:
            missing.append((pid, "no approved page file yet — schema describes a final page only"))
            continue
        m = publish.parse(f)
        pend = (m["url"].rstrip("/") != (p.get("url") or "").rstrip("/"))
        row = {"url": m["url"], "title": m["seo_title"], "meta_description": m["meta_description"],
               "pending_url_change": pend}
        if pend:
            missing.append((pid, f"PENDING URL CHANGE — the approved file says {m['url']}, the site plan "
                                 f"{p.get('url')}; never write schema for a URL that will move"))
        if t == "service":
            sv = wheel.service_variant(st, pid, ent)
            cfg["service_pages"].append({**row, "service_node_name": sv,
                                         "service_type": re.sub(r"\s*\([^)]*\)", "", p.get("name") or sv).strip(),
                                         "description": m["meta_description"], "entities": entities})
        elif t == "location":
            city = wheel.city_of(p)
            cfg["area_served"].append({"name": city, "state": state})
            own = [c for k, c in counties.items() if k.split(" county")[0] in (p.get("county") or "").lower()]
            cfg["location_pages"].append({**row, "city": city, "state": state, "state_abbr": state_abbr,
                                          "entities": entities[1:] + own})
        elif t == "county":
            cfg["hub_pages"].append(row)
    if not cfg["area_served"]:
        cfg["area_served"] = [{"name": (addr or {}).get("addressLocality", ""), "state": state}] if addr else []
    gate, warn = B.entry_gate({**cfg, "business": {k: v for k, v in cfg["business"].items()
                                                    if k != "founding_date" or v}})
    missing += [(w, why) for w, why in gate if w != "business.founding_date"]
    return cfg, missing, notes + warn


# ------------------------------------------------------------------ the graphs
def graphs(cfg):
    """[(name, page url, kind, graph)] — the builder's node sets; the GBP landing page alone carries LocalBusiness."""
    out = []
    home = cfg["business"]["url"].rstrip("/") + "/"
    gbp = cfg["gbp_landing_page"]
    hp = B.homepage(cfg)
    if cfg["business"].get("founding_date") in (None, "None"):
        for n in hp["@graph"]:
            n.pop("foundingDate", None)
    if gbp.rstrip("/") == home.rstrip("/"):
        out.append(("homepage", home, "homepage", hp))
    else:   # BB-604: the GBP landing page takes the homepage node set; the homepage keeps WebSite + Corporation
        out.append(("homepage", home, "homepage", {"@context": hp["@context"], "@graph": hp["@graph"][:2]}))
        out.append((f"gbp-{B.slug(gbp)}", gbp, "gbp", hp))
    for s in cfg["service_pages"]:
        out.append((f"service-{B.slug(s['url'])}", s["url"], "service", B.service_page(cfg, s)))
    for l in cfg["location_pages"]:
        if l["url"].rstrip("/") != gbp.rstrip("/"):
            out.append((f"location-{B.slug(l['url'])}", l["url"], "location", B.location_page({**cfg, "service_pages": cfg.get("catalog") or cfg["service_pages"]}, l)))
    for hb in cfg.get("hub_pages") or []:
        d = cfg["business"]["url"].rstrip("/")
        out.append((f"hub-{B.slug(hb['url'])}", hb["url"], "hub", {"@context": "https://schema.org", "@graph": [{
            "@type": "WebPage", "@id": f"{hb['url']}#webpage", "url": hb["url"], "name": hb["title"],
            "description": hb["meta_description"], "isPartOf": {"@id": f"{d}/#website"},
            "about": {"@id": cfg["business"]["id_page_url"]}}]}))
    return out


# ------------------------------------------------------------------ the validator
GENERIC = {"WebSite", "WebPage", "Corporation", "Service", "ItemList", "ListItem", "Thing", "City", "State", "Place",
           "AdministrativeArea", "PostalAddress", "ContactPoint", "ImageObject", "Person", "OpeningHoursSpecification",
           "EducationalOccupationalCredential"}
SHAPE = {"homepage": {"WebSite", "Corporation", "*"}, "gbp": {"WebSite", "Corporation", "*"},
         "service": {"WebPage", "Service"}, "location": {"WebPage", "ItemList"}, "hub": {"WebPage"}}
NAP_KEYS = ("address", "telephone", "openingHoursSpecification", "hasMap")


def validate(name, url, kind, g, known_ids, gbp):
    """[problem] for one page's graph (an empty list = valid)."""
    probs = list(B.output_problems(name, g))
    if g.get("@context") != "https://schema.org" or not isinstance(g.get("@graph"), list) or not g["@graph"]:
        return probs + [f"{name}: needs @context https://schema.org and a non-empty @graph"]
    try:
        json.loads(json.dumps(g))
    except (TypeError, ValueError) as e:
        probs.append(f"{name}: not valid JSON ({e})")
    ids, refs, local = set(), [], []

    def walk(n, top):
        if isinstance(n, dict):
            if "@type" not in n and set(n) != {"@id"}:
                probs.append(f"{name}: a node without @type ({list(n)[:3]})")
            if set(n) == {"@id"}:
                refs.append(n["@id"])
            elif n.get("@id"):
                if n["@id"] in ids and top:
                    probs.append(f"{name}: @id {n['@id']} defined twice")
                ids.add(n["@id"])
            t = n.get("@type")
            if isinstance(t, str) and t not in GENERIC:
                local.append(t)
            if any(k in n for k in NAP_KEYS) and kind not in ("homepage", "gbp"):
                probs.append(f"{name}: NAP ({', '.join(k for k in NAP_KEYS if k in n)}) repeated off the business entity")
            for k, v in n.items():
                walk(v, False)
        elif isinstance(n, list):
            for v in n:
                walk(v, False)
    for node in g["@graph"]:
        walk(node, True)
    tops = {n.get("@type") for n in g["@graph"] if isinstance(n, dict)}
    allowed = SHAPE.get(kind, set())
    extra = {t for t in tops if t not in allowed and not ("*" in allowed and t not in GENERIC)}
    if extra or (allowed - {"*"}) - tops:
        probs.append(f"{name}: a {kind} page carries {sorted(map(str, tops))}, the node set is {sorted(allowed - {'*'})}"
                     + (" + the LocalBusiness subtype" if "*" in allowed else ""))
    if local and kind not in ("homepage", "gbp"):
        probs.append(f"{name}: LocalBusiness-type node {sorted(set(local))} on a {kind} page — only the verified GBP "
                     "landing page carries it (BB-604)")
    if kind in ("homepage", "gbp") and "*" in allowed and not local and url.rstrip("/") == (gbp or "").rstrip("/"):
        probs.append(f"{name}: the GBP landing page has no LocalBusiness subtype node")
    for n in g["@graph"]:
        if n.get("@type") == "WebPage" and (n.get("url") or "").rstrip("/") != url.rstrip("/"):
            probs.append(f"{name}: WebPage url {n.get('url')} is not the page's URL {url}")
    for r in refs:
        if r not in ids and r not in known_ids and not r.startswith("https://www.wikidata.org/wiki/Q"):
            probs.append(f"{name}: @id reference {r} resolves to nothing in the site's graph")
    return probs


def known_ids(cfg):
    d = cfg["business"]["url"].rstrip("/")
    out = {f"{d}/#website", f"{d}/#corporation", cfg["business"].get("id_page_url")}
    for s in cfg["service_pages"] + (cfg.get("catalog") or []):
        out |= {f"{s['url']}#service", f"{s['url']}#webpage"}
    for l in cfg["location_pages"] + (cfg.get("hub_pages") or []):
        out |= {f"{l['url']}#webpage", f"{l['url']}#service-catalog"}
    return out


def out_dir(slug):
    return client_dir(slug) / "finish" / "schema"


# ------------------------------------------------------------------ commands
def cmd_gate(slug, st, quiet=False, only=None):
    cfg, missing, notes = build_config(slug, st, only)
    if not quiet:
        for n in notes:
            print(f"  note: {n}")
    return cfg, missing


def report_missing(missing):
    print("ASSET GATE FAILED — no schema built (no partial schema):")
    for w, why in missing:
        print(f"  MISSING  {w}\n           {why}")
    print("Fill these in the Brand Guide (Section F, or the page), then re-run.")


def build(slug, st, offline=False, quiet=False, only=None, out=None):
    """(exit code, index) — writes nothing unless the gate, the entity check, the output check and the validator pass."""
    cfg, missing = cmd_gate(slug, st, quiet, only)
    if missing:
        if not quiet:
            report_missing(missing)
        return 2, {"missing": missing}
    d = Path(out) if out else out_dir(slug)
    d.mkdir(parents=True, exist_ok=True)
    write_json(d / "config.json", cfg)
    if offline:
        rec = B.offline_approval(slug)
        probs = B.offline_format_check(cfg)
    else:
        rec, (probs, _) = None, B.verify_entities(cfg)
    if probs:
        if not quiet:
            print("ENTITY CHECK FAILED — no schema built (CM-051, BB-606):")
            for p, why in probs:
                print(f"  WRONG    {p}\n           {why}")
        return 2, {"entity": probs}
    gs = graphs(cfg)
    ids = known_ids(cfg)
    bad = [p for name, url, kind, g in gs for p in validate(name, url, kind, g, ids, cfg["gbp_landing_page"])]
    if bad:
        if not quiet:
            print("SCHEMA INVALID — nothing written:\n  " + "\n  ".join(bad[:20]))
        return 4, {"invalid": bad}
    index = {"built": now(), "offline": bool(offline), "gbp_landing_page": cfg["gbp_landing_page"], "pages": {}}
    by_url = {}
    for pid, p in st["pages"].items():
        if p.get("url"):
            by_url[p["url"].rstrip("/")] = pid
    for name, url, kind, g in gs:
        text = json.dumps(g, indent=2, ensure_ascii=False)
        (d / f"{name}.jsonld").write_text(text + "\n", encoding="utf-8")
        (d / f"{name}.script.html").write_text(f'<script type="application/ld+json">\n{text}\n</script>\n', encoding="utf-8")
        index["pages"][by_url.get(url.rstrip("/"), name)] = {"url": url, "kind": kind, "file": f"{name}.script.html",
                                                            "nodes": [n.get("@type") for n in g["@graph"]]}
    write_json(d / "index.json", index)
    if rec:
        B.offline_consumed(rec, len(gs))
    return 0, index


def validate_dir(d, cfg):
    gbp = cfg["gbp_landing_page"] if cfg else ""
    ids = known_ids(cfg) if cfg else set()
    index = json.loads((d / "index.json").read_text()) if (d / "index.json").exists() else {"pages": {}}
    probs, n = [], 0
    for pid, e in index["pages"].items():
        f = d / e["file"].replace(".script.html", ".jsonld")
        try:
            g = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as ex:
            probs.append(f"{f.name}: cannot be read as JSON ({ex})")
            continue
        n += 1
        probs += validate(f.stem, e["url"], e["kind"], g, ids, gbp)
    return n, probs


def main():
    import status as S
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("config"); s.add_argument("slug"); s.add_argument("--out")
    s = sub.add_parser("gate"); s.add_argument("slug")
    s = sub.add_parser("build"); s.add_argument("slug"); s.add_argument("--offline", action="store_true")
    s.add_argument("--pages", help="a dry run on these page ids only (the homepage always); needs --out")
    s.add_argument("--out", help="write here instead of the client's finish/schema/")
    s = sub.add_parser("validate"); s.add_argument("target")
    a = ap.parse_args()
    if a.cmd == "validate":
        t = Path(a.target)
        d = t if t.is_dir() else (out_dir(a.target) if not t.exists() else t.parent)
        cfg = json.loads((d / "config.json").read_text()) if (d / "config.json").exists() else None
        n, probs = validate_dir(d, cfg)
        print("\n".join(probs) or f"{n} schema file(s) valid (node sets, BB-604, @id references, no NAP repeated, "
                                  "no working text, no reviews)")
        sys.exit(1 if probs or not n else 0)
    st = S.load(a.slug)
    if a.cmd == "config":
        cfg, missing, notes = build_config(a.slug, st)
        p = Path(a.out) if a.out else out_dir(a.slug) / "config.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        write_json(p, cfg)
        print(f"config → {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p} · {len(missing)} asset(s) missing")
        for w, why in missing[:12]:
            print(f"  MISSING  {w} — {why}")
        sys.exit(2 if missing else 0)
    if a.cmd == "gate":
        _, missing = cmd_gate(a.slug, st)
        if missing:
            report_missing(missing)
            sys.exit(2)
        print("asset gate passed")
        return
    if a.pages and not a.out:
        die("--pages is a dry run: give it --out <dir> (the client's finish/schema/ holds only a whole-site build)")
    only = (set(a.pages.split(",")) | {"homepage"}) if a.pages else None
    code, index = build(a.slug, st, a.offline, only=only, out=a.out)
    if code == 0:
        n = len(index["pages"])
        print(f"{n} page(s) of schema built and valid → {a.out or out_dir(a.slug).relative_to(ROOT)} "
              "(.jsonld for validator.schema.org, .script.html for the head field)")
    sys.exit(code)


if __name__ == "__main__":
    main()
