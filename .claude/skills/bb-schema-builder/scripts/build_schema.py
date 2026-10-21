#!/usr/bin/env python3
"""
build_schema.py — emit BB-6xx v1.1 JSON-LD for every page type from one client config.

    python3 build_schema.py <client.yaml> <out_dir> [--page URL] [--check]

Implements the node sets observed in a Bradley-built live implementation (SRC-030/031/032),
not the pattern described in the derived documents. See sop-source/BB-Standard-Schema-Section-v1.1.md (the single source).

--check runs the entry gate and the entity check only, and reports what is wrong, emitting nothing.
--offline <slug> skips ONLY the live entity check, and only with Paul's approval for the open
/build handoff run (/approve <slug> schema-offline --reason "...", CM-053) — once, logged with his name.
The Q-ID / Wikipedia URL formats are still checked offline, and the entry gate and output check still run.

Three checks, in order (CM-051); any failure writes nothing:
  1. Entry gate — every required Section F value is present (a missing logo or an entity with no
     Wikidata URI is refused, never a crash).
  2. Entity check — every entity's Wikidata Q-ID is confirmed over HTTP: against the Wikipedia page's
     own Wikidata item when a Wikipedia URL is given, else the Q-ID must exist; Grokipedia URLs must
     resolve. Calls are paced. A mismatch or an unreachable source refuses the build.
  3. Output check — no working text ([NEED, TODO, "Brand Guide", placeholders) in any string; no
     aggregateRating / review on anything; no Wikipedia URL as an @id; addressCountry only inside a
     PostalAddress; areaServed types only City / Place / AdministrativeArea.
Each page is written twice: <name>.jsonld (raw, for validator.schema.org) and <name>.script.html
(the same JSON-LD inside <script type="application/ld+json">, ready to paste).
"""

import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

try:
    import yaml
except ImportError:
    yaml = None


# ---------------------------------------------------------------- entry gate
REQUIRED = [
    ("business.name", "Brand entity, exactly as on GBP"),
    ("business.url", "Primary domain, canonical host form"),
    ("business.telephone", "Phone in +1-XXX-XXX-XXXX form"),
    ("business.email", "Public email"),
    ("business.schema_type", "LocalBusiness subtype, e.g. HomeAndConstructionBusiness"),
    ("business.id_page_url", "ID page URL — becomes the business entity @id"),
    ("business.address.streetAddress", "Confirmed NAP"),
    ("business.address.addressLocality", "Confirmed NAP"),
    ("business.address.addressRegion", "Confirmed NAP"),
    ("business.address.postalCode", "Confirmed NAP"),
    ("business.has_map", "Google Maps share link (maps.app.goo.gl)"),
    ("business.logo", "Logo image URL (Brand Guide F: logo files) — the Corporation logo and the default image"),
    ("business.founding_date", "Founding year"),
    ("business.description", "Location entity description"),
    ("corporation.description", "Brand entity description"),
    ("same_as", "Full citation and profile list"),
    ("area_served", "Every city served"),
    ("gbp_landing_page", "Which URL is the GBP Website field — decides BB-604"),
]


AREA_TYPES = ("City", "Place", "AdministrativeArea")


def dig(cfg, path):
    cur = cfg
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur or None


def entry_gate(cfg):
    missing = [(p, why) for p, why in REQUIRED if not dig(cfg, p)]
    warn = []
    if not dig(cfg, "corporation.legal_name"):
        warn.append("corporation.legal_name absent — omit the field rather than "
                    "duplicating name")
    for page in cfg.get("service_pages", []) + cfg.get("location_pages", []):
        if not page.get("entities"):
            warn.append(f"{page.get('url')}: no entity Things — about[] will be thin")
        for e in page.get("entities") or []:
            label = f"{page.get('url')} → entity '{(e or {}).get('name') or '(no name)'}'"
            if not (e or {}).get("name"):
                missing.append((label, "entity has no name"))
            if not (e or {}).get("wikidata"):
                missing.append((label, "no Wikidata URI — BB-606 (v1.1) makes the Wikidata URI the entity's @id. "
                                       "Find it (Brand Guide F) or remove the entity from this page"))
        if page.get("pending_url_change"):
            missing.append((page.get("url"),
                            "PENDING URL CHANGE — never write schema for a page whose "
                            "URL is queued to move"))
    ext = cfg.get("area_served_extended")
    for c in cfg.get("area_served") or []:
        name = (c or {}).get("name") or "(no name)"
        if not ext and ((c or {}).get("type") or (c or {}).get("wikipedia")):
            missing.append((f"area_served → {name}", "'type' / 'wikipedia' on a served area need area_served_extended: true "
                            "(pilot — Paul validates one client before it is the default, CM-051)"))
        t = (c or {}).get("type", "City") if ext else "City"
        if t not in AREA_TYPES:
            missing.append((f"area_served → {name}", f"type must be one of {', '.join(AREA_TYPES)} (got {t})"))
        if t == "City" and not (c or {}).get("state"):
            missing.append((f"area_served → {name}", "a City needs its state"))
    return missing, warn


# ---------------------------------------------------------------- entity check (CM-051 · BB-606)
UA = "seo-ops bb-schema-builder (Coastal Marketing Strategies; schema entity check)"
PACE = 0.5      # seconds between calls to Wikipedia / Wikidata / Grokipedia
QID = re.compile(r"^https://www\.wikidata\.org/wiki/(Q\d+)$")


def fetch(url, method="GET"):
    """(status, text). A network failure is (None, reason). Replaced by a fake in the tests."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, (r.read().decode("utf-8", "replace") if method != "HEAD" else "")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def all_entities(cfg):
    seen = {}
    for page in cfg.get("service_pages", []) + cfg.get("location_pages", []):
        for e in page.get("entities") or []:
            if e and e.get("wikidata"):
                seen.setdefault(e["wikidata"] + "|" + (e.get("wikipedia") or ""), (e, page.get("url")))
    return list(seen.values())


def verify_entities(cfg):
    problems, notes = [], []
    for e, url in all_entities(cfg):
        label = f"{url} → entity '{e.get('name')}'"
        m = QID.match(e["wikidata"])
        if not m:
            problems.append((label, f"wikidata must be https://www.wikidata.org/wiki/Q… (got {e['wikidata']})"))
            continue
        q = m.group(1)
        if e.get("wikipedia"):
            wm = re.match(r"^https://([a-z\-]+)\.wikipedia\.org/wiki/(.+)$", e["wikipedia"])
            if not wm:
                problems.append((label, "wikipedia must be a https://<lang>.wikipedia.org/wiki/<Title> URL"))
                continue
            title = urllib.parse.quote(urllib.parse.unquote(wm.group(2)))
            code, body = fetch(f"https://{wm.group(1)}.wikipedia.org/w/api.php?action=query&prop=pageprops"
                               f"&ppprop=wikibase_item&redirects=1&format=json&titles={title}")
            time.sleep(PACE)
            if code != 200:
                problems.append((label, f"could not check {e['wikipedia']} ({code or body}) — try again later; "
                                        "schema is never built on an unchecked entity"))
                continue
            pages = (json.loads(body).get("query") or {}).get("pages") or {}
            item = next(((p.get("pageprops") or {}).get("wikibase_item") for p in pages.values()), None)
            if not item:
                problems.append((label, f"{e['wikipedia']} does not exist or has no Wikidata item"))
            elif item != q:
                problems.append((label, f"the Wikipedia page is Wikidata {item}, but the config says {q} — one of them is wrong"))
        else:
            code, body = fetch(f"https://www.wikidata.org/wiki/Special:EntityData/{q}.json")
            time.sleep(PACE)
            if code != 200:
                problems.append((label, f"Wikidata {q} could not be found ({code or body})"))
                continue
            ents = json.loads(body).get("entities") or {}
            ent = ents.get(q) or next(iter(ents.values()), {})
            lab = ((ent.get("labels") or {}).get("en") or {}).get("value", "")
            n = (e.get("name") or "").lower()
            if lab and n not in lab.lower() and lab.lower() not in n:
                problems.append((label, f"Wikidata {q} is '{lab}', not '{e.get('name')}' — fix the ID, or add the entity's "
                                        "Wikipedia URL so the check can match them exactly"))
        if e.get("grokipedia"):
            code, _ = fetch(e["grokipedia"], "HEAD")
            time.sleep(PACE)
            if code != 200:
                problems.append((label, f"the Grokipedia URL does not resolve ({code}) — fix it or remove it"))
    return problems, notes


# ---------------------------------------------------------------- offline override (CM-053)
def _ops():
    """The seo-ops status and run scripts (repo root/scripts), for the offline approval only."""
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
    import run as R, status as S   # noqa: E401
    return R, S


def offline_approval(slug):
    """Paul's /approve <slug> schema-offline for the open /build handoff run, not used yet — else refuse."""
    R, S = _ops()
    rec = S.load(slug).get("schema_offline") or {}
    why = None
    if not rec:
        why = "Paul has not approved an offline build"
    elif rec.get("used"):
        why = f"Paul's offline approval was already used ({rec['used']['at'][:16]}) — it covers one build"
    elif rec.get("run") not in R.unfinished(slug):
        why = f"Paul's offline approval was for run {rec.get('run')}, which is no longer open — it covers that run only"
    if why:
        print(f"OFFLINE REFUSED — {why}. The live entity check stays on; to skip it once, Paul types:\n"
              f"  /approve {slug} schema-offline --reason \"<what is down and since when>\"")
        sys.exit(2)
    rec["slug"] = slug
    return rec


def offline_format_check(cfg):
    """What can be checked without the network: the shape of every Wikidata / Wikipedia URL."""
    probs = []
    for e, url in all_entities(cfg):
        label = f"{url} → entity '{e.get('name')}'"
        if not QID.match(e["wikidata"]):
            probs.append((label, f"wikidata must be https://www.wikidata.org/wiki/Q… (got {e['wikidata']})"))
        if e.get("wikipedia") and not re.match(r"^https://[a-z\-]+\.wikipedia\.org/wiki/.+$", e["wikipedia"]):
            probs.append((label, "wikipedia must be a https://<lang>.wikipedia.org/wiki/<Title> URL"))
    return probs


def offline_consumed(rec, pages):
    R, S = _ops()
    slug = rec.pop("slug")
    st = S.load(slug)
    from datetime import datetime
    at = datetime.now().astimezone().isoformat(timespec="seconds")
    st["schema_offline"]["used"] = {"at": at, "pages": pages}
    S.save(slug, st)
    with open(S.client_dir(slug) / "log.md", "a", encoding="utf-8") as fh:
        fh.write(f"- SCHEMA OFFLINE {at[:16]} · run {rec['run']} · {pages} page(s) built WITHOUT the live entity check, "
                 f"under Paul's approval ({rec['reason']}) · re-run the full build when Wikipedia/Wikidata are back\n")


# ---------------------------------------------------------------- output check (CM-051)
LEAK = re.compile(r"\[NEED|\bTODO\b|\bTBD\b|\bFIXME\b|DataforSEO|Brand Guide|seo-ops|lorem ipsum|\{\{|\}\}", re.I)
PLACEHOLDER = re.compile(r"\[[A-Z][A-Za-z /]{2,40}\]")
NEVER_KEYS = ("aggregateRating", "review", "reviews")


def output_problems(name, graph):
    probs = []

    def walk(node, path, parent_key=None):
        if isinstance(node, dict):
            t = node.get("@type")
            for k in NEVER_KEYS:
                if k in node:
                    probs.append(f"{name}: '{k}' at {path} — never on the business (self-serving reviews; CM-027)")
            if str(node.get("@id", "")).find("wikipedia.org") >= 0:
                probs.append(f"{name}: a Wikipedia URL as an @id at {path} — the @id is the Wikidata URI (BB-606)")
            if "addressCountry" in node and t != "PostalAddress":
                probs.append(f"{name}: addressCountry outside a PostalAddress at {path}")
            if parent_key == "areaServed" and t not in AREA_TYPES:
                probs.append(f"{name}: areaServed type {t} at {path} — only {', '.join(AREA_TYPES)}")
            for k, v in node.items():
                walk(v, f"{path}.{k}", k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]", parent_key)
        elif isinstance(node, str):
            if LEAK.search(node) or PLACEHOLDER.search(node):
                probs.append(f"{name}: working text in {path}: {node[:80]!r}")
    walk(graph, "$")
    return probs


# ---------------------------------------------------------------- builders
def thing(e):
    """One entity node. @id IS the Wikidata URI (BB-606 v1.1)."""
    same = [u for u in (e.get("wikipedia"), e.get("wikidata"), e.get("grokipedia")) if u]
    node = {"@type": "Thing", "@id": e["wikidata"], "name": e["name"]}
    if e.get("description"):
        node["description"] = e["description"]
    node["sameAs"] = same
    return node


def area_served(cfg):
    """City + State by default (woodlawn). With area_served_extended (pilot, CM-051): Place for a
    neighbourhood, AdministrativeArea for a county, and an optional Wikipedia sameAs on a city."""
    ext = cfg.get("area_served_extended")
    out = []
    for c in cfg["area_served"]:
        node = {"@type": c.get("type", "City") if ext else "City", "name": c["name"]}
        if c.get("state"):
            node["containedInPlace"] = {"@type": "State", "name": c["state"]}
        if ext and c.get("wikipedia"):
            node["sameAs"] = c["wikipedia"]
        out.append(node)
    return out


def country(cfg):
    """From the config (business.address.addressCountry, else country); 'US' when neither is set."""
    return (cfg["business"].get("address") or {}).get("addressCountry") or cfg.get("country") or "US"


def website_node(cfg):
    """Defined so #website references actually resolve — the reference site's defect."""
    d = cfg["business"]["url"].rstrip("/")
    return {"@type": "WebSite", "@id": f"{d}/#website",
            "name": cfg["business"]["name"], "url": f"{d}/",
            "publisher": {"@id": f"{d}/#corporation"}}


def homepage(cfg):
    b, c = cfg["business"], cfg.get("corporation", {})
    d = b["url"].rstrip("/")
    corp = {
        "@type": "Corporation", "@id": f"{d}/#corporation",
        "name": b["name"],
    }
    if c.get("legal_name"):
        corp["legalName"] = c["legal_name"]
    if b.get("alternate_name"):
        corp["alternateName"] = b["alternate_name"]
    corp.update({
        "url": f"{d}/",
        "logo": {"@type": "ImageObject", "url": b["logo"]},
        "image": b.get("images", [b["logo"]]),
        "description": c.get("description"),
        "foundingDate": str(b["founding_date"]),
    })
    if c.get("founder"):
        f = c["founder"]
        person = {"@type": "Person", "name": f["name"]}
        for k in ("alternate_name", "job_title"):
            if f.get(k):
                person["alternateName" if k == "alternate_name" else "jobTitle"] = f[k]
        if f.get("credential"):
            cr = f["credential"]
            person["hasCredential"] = {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "certification",
                "name": cr["name"], "identifier": cr["identifier"]}
        corp["founder"] = person
    corp.update({
        "email": b["email"],
        "contactPoint": {"@type": "ContactPoint", "telephone": b["telephone"],
                         "email": b["email"], "contactType": "customer service",
                         "areaServed": country(cfg), "availableLanguage": "English"},
        "sameAs": cfg["same_as"],
    })

    loc = {
        "@type": b["schema_type"],
        "@id": b["id_page_url"],
        "name": b["name"],
    }
    if b.get("alternate_name"):
        loc["alternateName"] = b["alternate_name"]
    loc.update({
        "url": f"{d}/",
        "mainEntityOfPage": cfg["gbp_landing_page"],
        "image": b.get("images", [b["logo"]]),
        "telephone": b["telephone"], "email": b["email"],
        "description": b["description"],
        "parentOrganization": {"@id": f"{d}/#corporation"},
        "address": {"@type": "PostalAddress", **b["address"], "addressCountry": country(cfg)},
        "hasMap": b["has_map"],
    })
    if b.get("hours"):
        loc["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"],
             "opens": h["opens"], "closes": h["closes"]} for h in b["hours"]]
    loc["areaServed"] = area_served(cfg)
    loc["sameAs"] = cfg["same_as"]

    return {"@context": "https://schema.org",
            "@graph": [website_node(cfg), corp, loc]}


def service_page(cfg, p):
    b = cfg["business"]
    d = b["url"].rstrip("/")
    about = [{"@id": f"{p['url']}#service"}] + [thing(e) for e in p.get("entities", [])]
    web = {
        "@type": "WebPage", "@id": f"{p['url']}#webpage", "url": p["url"],
        "name": p["title"], "description": p["meta_description"],
        "isPartOf": {"@type": "WebSite", "@id": f"{d}/#website",
                     "name": b["name"], "url": f"{d}/"},
        "mainEntity": {"@id": f"{p['url']}#service"},
        "about": about,
    }
    if p.get("image"):
        web["primaryImageOfPage"] = {"@type": "ImageObject", "url": p["image"]}
    svc = {
        "@type": "Service", "@id": f"{p['url']}#service",
        "name": p["service_node_name"], "serviceType": p["service_type"],
        "description": p["description"], "url": p["url"],
        "provider": {"@id": b["id_page_url"]},
        "areaServed": area_served(cfg),
    }
    if p.get("image"):
        svc["image"] = p["image"]
    return {"@context": "https://schema.org", "@graph": [web, svc]}


def location_page(cfg, p):
    b = cfg["business"]
    d = b["url"].rstrip("/")
    if p["url"] == cfg["gbp_landing_page"]:
        raise SystemExit(
            f"{p['url']} is the GBP landing page — it takes the homepage node set, "
            f"not the location node set. Check BB-604.")
    about = [{"@id": b["id_page_url"]},
             {"@type": "City", "name": p["city"],
              "containedInPlace": {"@type": "State", "name": p["state"]}}]
    about += [thing(e) for e in p.get("entities", [])]
    web = {
        "@type": "WebPage", "@id": f"{p['url']}#webpage", "url": p["url"],
        "name": p["title"], "description": p["meta_description"],
        "isPartOf": {"@type": "WebSite", "@id": f"{d}/#website",
                     "name": b["name"], "url": f"{d}/"},
        "mainEntity": {"@id": b["id_page_url"]},
        "mentions": {"@id": f"{p['url']}#service-catalog"},
        "about": about,
    }
    if p.get("image"):
        web["primaryImageOfPage"] = {"@type": "ImageObject", "url": p["image"]}
    catalog = {
        "@type": "ItemList", "@id": f"{p['url']}#service-catalog",
        "name": f"{cfg.get('service_catalog_label', 'Services')} in "
                f"{p['city']}, {p.get('state_abbr', p['state'])}",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "item": {"@id": f"{s['url']}#service"}}
            for i, s in enumerate(cfg.get("service_pages", []))],
    }
    return {"@context": "https://schema.org", "@graph": [web, catalog]}


# ---------------------------------------------------------------- main
def slug(url):
    s = re.sub(r"^https?://[^/]+", "", url).strip("/")
    return s.replace("/", "-") or "homepage"


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cfg_path, out_dir = sys.argv[1], sys.argv[2]
    raw = open(cfg_path, encoding="utf-8").read()
    cfg = json.loads(raw) if cfg_path.endswith(".json") else (
        yaml.safe_load(raw) if yaml else sys.exit("install pyyaml or pass .json"))

    missing, warn = entry_gate(cfg)
    if missing:
        print("ENTRY GATE FAILED — schema not written.\n")
        for p, why in missing:
            print(f"  MISSING  {p}\n           {why}")
        print("\nFill these in the Brand Guide Section F, then re-run.")
        sys.exit(2)
    for w in warn:
        print(f"  note: {w}")
    offline = offline_approval(sys.argv[sys.argv.index("--offline") + 1]) if "--offline" in sys.argv else None
    if offline:
        problems, notes = offline_format_check(cfg), []
        print(f"  OFFLINE — live entity check SKIPPED under Paul's approval of {offline['at'][:16]} "
              f"(reason: {offline['reason']}). Re-run the full build once Wikipedia/Wikidata are back.")
    else:
        problems, notes = verify_entities(cfg)
    for n in notes:
        print(f"  note: {n}")
    if problems:
        print("\nENTITY CHECK FAILED — schema not written (CM-051, BB-606).\n")
        for p, why in problems:
            print(f"  WRONG    {p}\n           {why}")
        print("\nFix the Wikidata / Wikipedia / Grokipedia links in Brand Guide Section F, then re-run.")
        sys.exit(2)
    if "--check" in sys.argv:
        print("\nEntry gate and entity check passed.")
        return

    only = None
    if "--page" in sys.argv:
        only = sys.argv[sys.argv.index("--page") + 1]

    graphs = []     # built in memory first: nothing is written unless every graph passes
    if not only or only in (cfg["business"]["url"], cfg["gbp_landing_page"]):
        graphs.append(("homepage", homepage(cfg)))
    for s_ in cfg.get("service_pages", []):
        if not only or s_["url"] == only:
            graphs.append((f"service-{slug(s_['url'])}", service_page(cfg, s_)))
    for l in cfg.get("location_pages", []):
        if not only or l["url"] == only:
            graphs.append((f"location-{slug(l['url'])}", location_page(cfg, l)))
    probs = [p for name, g in graphs for p in output_problems(name, g)]
    if probs:
        print("OUTPUT CHECK FAILED — schema not written (CM-051).\n")
        for p in probs:
            print(f"  {p}")
        sys.exit(3)

    os.makedirs(out_dir, exist_ok=True)
    written = []
    for name, g in graphs:
        text = json.dumps(g, indent=2, ensure_ascii=False)
        raw = os.path.join(out_dir, f"{name}.jsonld")
        open(raw, "w", encoding="utf-8").write(text + "\n")
        wrapped = os.path.join(out_dir, f"{name}.script.html")
        open(wrapped, "w", encoding="utf-8").write(
            f'<script type="application/ld+json">\n{text}\n</script>\n')
        written += [raw, wrapped]

    if offline:
        offline_consumed(offline, len(graphs))
    for p in written:
        print(f"wrote {p}")
    print(f"\n{len(graphs)} page(s): .jsonld (raw — validate each at validator.schema.org first) and "
          f".script.html (the same, ready to paste) before implementation.")


if __name__ == "__main__":
    main()
