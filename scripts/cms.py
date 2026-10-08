#!/usr/bin/env python3
"""cms.py — which CMS a client's site runs on (#23, Paul 2026-10-08). WordPress steps are N/A when it is not WordPress.

    cms.py detect <slug> --run R [--html-file F]     fetch the homepage (or read F), detect the CMS, record it in
                                                    status.json client.cms and settle it once ("cms")

Signals, strongest first: a generator meta tag; wp-content / wp-includes / wp-json links (WordPress); Astro, Wix,
Squarespace, Shopify, Webflow, Duda, GoDaddy markers. Unknown → "unknown" (Paul answers it on the Decision Sheet).
"""
import argparse
import re
import urllib.request

import status as S
from lib import die

SIGNS = [
    ("wordpress", r"wp-content/|wp-includes/|/wp-json/|<meta[^>]+generator[^>]+WordPress"),
    ("astro", r"<meta[^>]+generator[^>]+Astro|/_astro/|astro-island"),
    ("wix", r"static\.wixstatic\.com|<meta[^>]+generator[^>]+Wix"),
    ("squarespace", r"static1\.squarespace\.com|<!-- This is Squarespace"),
    ("shopify", r"cdn\.shopify\.com|Shopify\.theme"),
    ("webflow", r"<meta[^>]+generator[^>]+Webflow|assets\.website-files\.com"),
    ("duda", r"irp\.cdn-website\.com|dudaone"),
    ("godaddy", r"img1\.wsimg\.com|<meta[^>]+generator[^>]+Starfield"),
]


def detect(html):
    for name, rx in SIGNS:
        if re.search(rx, html or "", re.I):
            return name
    return "unknown"


def fetch(domain):
    url = domain if domain.startswith("http") else f"https://{domain}/"
    req = urllib.request.Request(url, headers={"User-Agent": "seo-ops-cms/1.0 (+Coastal Marketing)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read(400000).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        die(f"could not fetch {url}: {e} — Paul answers 'cms' on the Decision Sheet instead")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("detect"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--html-file")
    a = ap.parse_args()
    import run as R
    import settled
    R.open_run(a.slug, a.run)
    st = S.load(a.slug)
    html = open(a.html_file, encoding="utf-8").read() if a.html_file else fetch(st["client"]["domain"])
    cms = detect(html)
    st["client"]["cms"] = cms
    S.save(a.slug, st)
    if cms != "unknown" and (settled.entries(a.slug).get("cms") or {}).get("state") != "settled":
        settled.settle(a.slug, a.run, "cms", f"The site runs on {cms}"
                       + ("" if cms == "wordpress" else " — WordPress steps are N/A"), by="system (detected)")
    print(f"cms: {cms}" + ("" if cms in ("wordpress", "unknown") else " — WordPress steps are N/A for this client"))


if __name__ == "__main__":
    main()
