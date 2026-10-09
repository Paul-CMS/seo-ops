#!/usr/bin/env python3
"""urlcheck.py — Bradley's URL rule for every planned service, location and hub page (rewrite 2 P7, Q6).

    urlcheck.py <slug> <plan.json>      exit 1 and list every problem; 0 when every URL is fine

Run by `status.py plan` (a site plan is refused until it passes) and by the import (the baseline is not exempt).
Refused, per page:
  - a folder prefix: /services/, /service/, /service-area/, /service-areas/, /locations/, /areas/ (and the like);
  - more than one path segment for a service, location or hub page;
  - a -2, -3 … suffix (a WordPress duplicate slug);
  - a service slug that names a planned city; a location slug that names a planned service;
  - a hub (type county) whose slug is not a county or metro slug (…-county, …-metro, …-parish, …-area), or names a
    service (HUB-04).
Changed URLs: a page whose live URL (`live_url`, or the import's old URL) differs from its planned URL must list the
old URL under `replaces`, so its 301 row is generated next to its publish row (publish.py).
"""
import json
import re
import sys
import urllib.parse

PREFIXES = ("service", "services", "service-area", "service-areas", "areas", "areas-we-serve", "locations",
            "location", "cities")
HUB_END = re.compile(r"-(county|metro|parish|area)$")


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")


def parts(url):
    return [x for x in urllib.parse.urlparse(url or "").path.split("/") if x]


def problems(pages):
    """pages: [{id, type, url, city?, service_variant?, live_url?, replaces?}] → ['<url>: why', …]."""
    cities = {slugify(p.get("city") or p.get("name")) for p in pages if p.get("type") == "location"}
    cities |= {(parts(p["url"]) or [""])[-1] for p in pages if p.get("type") == "location" and p.get("url")}
    cities.discard("")
    services = {(parts(p["url"]) or [""])[-1] for p in pages if p.get("type") == "service" and p.get("url")}
    services |= {slugify(p.get("service_variant")) for p in pages if p.get("type") == "service" and p.get("service_variant")}
    services.discard("")
    out = []
    for p in pages:
        t, url = p.get("type"), p.get("url")
        if t not in ("service", "location", "county") or not url:
            continue
        ps = parts(url)
        if ps and ps[0].lower() in PREFIXES:
            out.append(f"{url}: drop the /{ps[0]}/ folder — service and location URLs sit at the root (BB-207, BB-208)")
            continue
        if len(ps) != 1:
            out.append(f"{url}: a {t} URL is one slug at the root, e.g. /roof-repair/ or /bluffton/ (BB-208)")
            continue
        s = ps[0].lower()
        if re.search(r"-\d+$", s):
            out.append(f"{url}: a -{s.rsplit('-', 1)[1]} suffix is a duplicate slug — use /{s.rsplit('-', 1)[0]}/ "
                       "(and clear whatever holds it first)")
        if t == "service":
            hit = next((c for c in cities if re.search(rf"(^|-){re.escape(c)}($|-)", s)), None)
            if hit:
                out.append(f"{url}: a service slug never names a city ({hit}) — the city has its own page (BB-208)")
        else:
            hit = next((v for v in services if re.search(rf"(^|-){re.escape(v)}($|-)", s)), None)
            if hit:
                out.append(f"{url}: a {'hub' if t == 'county' else 'location'} slug never names a service ({hit}) "
                           "(BB-208, HUB-04)")
        if t == "county" and not HUB_END.search(s):
            out.append(f"{url}: a hub slug names its county or metro area, e.g. /beaufort-county/ or "
                       "/charleston-metro/ (HUB-04, CR-001)")
        live = p.get("live_url")
        if live and live.rstrip("/") != url.rstrip("/") and live not in (p.get("replaces") or []):
            out.append(f"{url}: its live URL {live} changes — list it under 'replaces' so its 301 goes with the publish")
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    plan = json.loads(open(sys.argv[2]).read())
    bad = problems(plan.get("pages") or [])
    print("\n".join(bad) or "every planned URL follows the URL rule")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
