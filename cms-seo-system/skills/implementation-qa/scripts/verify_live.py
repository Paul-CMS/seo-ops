#!/usr/bin/env python3
"""
verify_live.py — check the LIVE site against the handoff bundle (the outside view).

Usage:
    python3 verify_live.py <client-handoff-folder>

Reads <folder>/out/bundle.json, fetches the live URLs, writes <folder>/out/QA-REPORT.md
(mismatches only, link-implementation-qa format) and prints one summary line.
Standard library only. No model tokens: the model reads only the summary + report.
"""
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

UA = "Mozilla/5.0 (compatible; CMS-QA/1.0)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with OPENER.open(req, timeout=25) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), ""
    except Exception as e:  # network error
        return 0, {}, str(e)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.h1s, self.desc, self.robots, self.hrefs = "", [], None, "", []
        self._in_title = self._in_h1 = False
        self._title_done = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title" and not self._title_done:
            self._in_title = True
        elif tag == "h1":
            self._in_h1, self._buf = True, ""
        elif tag == "meta" and (a.get("name") or "").lower() == "description":
            self.desc = a.get("content") or ""
        elif tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots = (a.get("content") or "").lower()
        elif tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self._in_title, self._title_done = False, True
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.h1s.append(self._buf)

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._in_h1:
            self._buf += d


def clean(s):
    s = html.unescape(s or "")
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def rel(u, domain):
    u = re.sub(r"^" + re.escape(domain.rstrip("/")), "", u.strip())
    u = re.sub(r"^https?://[^/]+", "", u)
    u = u.split("#")[0].split("?")[0]
    return "/" + u.strip("/") + ("/" if u.strip("/") else "")


def check_page(domain, pg):
    url = domain.rstrip("/") + pg["url"]
    status, _, body = fetch(url)
    if status != 200:
        return [("Reported done, not done", pg["id"], pg["url"], "200", f"HTTP {status}")]
    p = Page()
    p.feed(body)
    out = []
    pairs = [("SEO title", pg.get("seo_title"), p.title), ("Meta description", pg.get("meta_description"), p.desc)]
    for label, want, have in pairs:
        if want and clean(want) != clean(have):
            out.append(("Reported done, wrong", pg["id"], pg["url"], f"{label}: {want}", clean(have) or "(missing)"))
    if pg.get("h1"):
        if len(p.h1s) != 1:
            out.append(("Reported done, wrong", pg["id"], pg["url"], "exactly one H1 (H1-01)", f"{len(p.h1s)} H1s: {[clean(x) for x in p.h1s][:3]}"))
        elif clean(p.h1s[0]) != clean(pg["h1"]):
            out.append(("Reported done, wrong", pg["id"], pg["url"], f"H1: {pg['h1']}", clean(p.h1s[0])))
    if pg.get("noindex") and "noindex" not in p.robots:
        out.append(("Reported done, not done", pg["id"], pg["url"], "noindex", p.robots or "(no robots meta)"))
    if not pg.get("noindex") and "noindex" in p.robots:
        out.append(("Reported done, wrong", pg["id"], pg["url"], "indexable", "page is noindex"))
    return out, p


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    folder = Path(sys.argv[1])
    b = json.loads((folder / "out" / "bundle.json").read_text(encoding="utf-8"))
    domain = b["client"]["domain"]
    rows, checked, hrefs_by_page = [], 0, {}

    for pg in b["pages"]:
        res = check_page(domain, pg)
        checked += 1
        if isinstance(res, list):
            rows += res
            continue
        found, parsed = res
        if found:  # retry once past the page cache before calling it a failure
            pg2 = dict(pg, url=pg["url"] + f"?qa={int(time.time())}")
            res2 = check_page(domain, pg2)
            if not isinstance(res2, list) and not res2[0]:
                found = [("Reported done, wrong", pg["id"], pg["url"], "fresh page served from cache", "stale cache: clear WP Rocket for this URL")]
        rows += found
        hrefs_by_page[pg["url"]] = {rel(h, domain) for h in parsed.hrefs if h.startswith("/") or domain in h}

    for r in b["redirects"]:
        checked += 1
        src = domain.rstrip("/") + rel(r["from"], domain)
        status, headers, _ = fetch(src)
        loc = rel(headers.get("Location") or headers.get("location") or "", domain)
        want = rel(r["to"], domain)
        if status != int(r.get("type", 301)) or loc != want:
            rows.append(("Reported done, not done", "redirect", rel(r["from"], domain), f"{r.get('type', 301)} → {want}", f"HTTP {status} → {loc or '-'}"))
            continue
        s2, _, _ = fetch(domain.rstrip("/") + want)
        if s2 != 200:
            rows.append(("Reported done, wrong", "redirect", rel(r["from"], domain), f"{want} returns 200 directly", f"HTTP {s2} (chain or broken target)"))

    for n in b["noindex"]:
        checked += 1
        status, _, body = fetch(domain.rstrip("/") + rel(n["url"], domain))
        p = Page()
        p.feed(body)
        if "noindex" not in p.robots:
            rows.append(("Reported done, not done", "noindex", n["url"], "noindex", p.robots or f"HTTP {status}, no robots meta"))

    retired = {rel(lu["old_url"], domain) for lu in b["link_updates"]} | {rel(r["from"], domain) for r in b["redirects"]}
    for page_url, hrefs in hrefs_by_page.items():
        stale = sorted(hrefs & retired)
        if stale:
            rows.append(("Sitewide regression", "links", page_url, "no links to retired URLs (RDR-05)", ", ".join(stale)))

    groups = {}
    for g, ref, page, exp, got in rows:
        groups.setdefault(g, []).append(f"| {ref} | {page} | {exp} | {got} |")
    rep = [f"## Implementation QA — {b['client']['name']}, {time.strftime('%Y-%m-%d')}", "",
           f"Items checked: {checked}  |  Mismatched: {len(rows)}", ""]
    for g in ("Reported done, not done", "Reported done, wrong", "Sitewide regression"):
        if g in groups:
            rep += [f"### {g}", "", "| Ref | Page | Expected | Found |", "|---|---|---|---|", *groups[g], ""]
    rep += ["### Judgment sample (human)", "",
            "- Read 100% of new or rebuilt page copy (content additions).",
            "- Spot-check 20% of internal link placements.", "",
            "### For Paul", "", "- (decisions, unapproved publications, spec errors)"]
    (folder / "out" / "QA-REPORT.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"QA: {checked} checked, {len(rows)} mismatched -> {folder / 'out' / 'QA-REPORT.md'}")
    sys.exit(1 if rows else 0)


if __name__ == "__main__":
    main()
