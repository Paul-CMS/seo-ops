#!/usr/bin/env python3
"""
build_schema.py — emit BB-6xx v1.1 JSON-LD for every page type from one client config.

    python3 build_schema.py <client.yaml> <out_dir> [--page URL] [--check]

Implements the node sets observed in a Bradley-built live implementation (SRC-030/031/032),
not the pattern described in the derived documents. See references/schema-rules.md.

--check runs the entry gate only and reports what is missing, emitting nothing.
"""

import json, os, re, sys

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
    ("business.founding_date", "Founding year"),
    ("business.description", "Location entity description"),
    ("corporation.description", "Brand entity description"),
    ("same_as", "Full citation and profile list"),
    ("area_served", "Every city served"),
    ("gbp_landing_page", "Which URL is the GBP Website field — decides BB-604"),
]


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
        if page.get("pending_url_change"):
            missing.append((page.get("url"),
                            "PENDING URL CHANGE — never write schema for a page whose "
                            "URL is queued to move"))
    return missing, warn


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
    return [{"@type": "City", "name": c["name"],
             "containedInPlace": {"@type": "State", "name": c["state"]}}
            for c in cfg["area_served"]]


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
                         "areaServed": "US", "availableLanguage": "English"},
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
        "address": {"@type": "PostalAddress", **b["address"], "addressCountry": "US"},
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
    if "--check" in sys.argv:
        print("\nEntry gate passed.")
        return

    os.makedirs(out_dir, exist_ok=True)
    only = None
    if "--page" in sys.argv:
        only = sys.argv[sys.argv.index("--page") + 1]

    written = []
    if not only or only in (cfg["business"]["url"], cfg["gbp_landing_page"]):
        p = os.path.join(out_dir, "homepage.jsonld")
        json.dump(homepage(cfg), open(p, "w"), indent=2, ensure_ascii=False)
        written.append(p)
    for s in cfg.get("service_pages", []):
        if only and s["url"] != only:
            continue
        p = os.path.join(out_dir, f"service-{slug(s['url'])}.jsonld")
        json.dump(service_page(cfg, s), open(p, "w"), indent=2, ensure_ascii=False)
        written.append(p)
    for l in cfg.get("location_pages", []):
        if only and l["url"] != only:
            continue
        p = os.path.join(out_dir, f"location-{slug(l['url'])}.jsonld")
        json.dump(location_page(cfg, l), open(p, "w"), indent=2, ensure_ascii=False)
        written.append(p)

    for p in written:
        print(f"wrote {p}")
    print(f"\n{len(written)} file(s). Validate each at validator.schema.org before "
          f"implementation.")


if __name__ == "__main__":
    main()
