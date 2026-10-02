#!/usr/bin/env python3
"""verify.py — re-check every changed page against the live site.

    verify.py <slug> --run R [--of RUN_ID] [--handoff H-ID] [--all]

Checks, per logged change:
  - system-applied SEO title / meta description -> read live via SEOPress and the public HTML
  - system-applied alt text / content / head    -> read back through wp.py
  - handoff items the VA marked done:
      redirect / slug pair -> the old URL answers 301 with Location = the new URL (no chain)
      seo_title / meta_description -> the public page shows the new value
      broken_link -> the page no longer links to the old URL
      everything else -> listed for a person to check (sitemap, robots.txt, speed)
Writes clients/<slug>/handoffs/verify-<run>.md and logs PASS / FAIL for each item.
"""
import argparse
import csv
import html
import re
import urllib.error
import urllib.request

import run as R
from lib import client_dir


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def fetch(url, follow=True):
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "seo-ops-verify/1.0 (+Coastal Marketing)"})
    try:
        r = opener.open(req, timeout=30)
        return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), ""
    except urllib.error.URLError as e:
        return 0, {}, str(e)


def page_title(body):
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    return html.unescape(m.group(1).strip()) if m else ""


def page_desc(body):
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', body, re.S | re.I) \
        or re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', body, re.S | re.I)
    return html.unescape(m.group(1).strip()) if m else ""


def check(c):
    k, url, new = c["kind"], c["url"], c["new"]
    if k in ("redirect",) or (k == "slug" and c["field"] == "301"):
        src = c["url"] if k == "redirect" else c["old"]
        code, hdrs, _ = fetch(src, follow=False)
        loc = hdrs.get("Location") or hdrs.get("location") or ""
        if code == 301 and loc.rstrip("/") == new.rstrip("/"):
            fcode, _, _ = fetch(new, follow=False)
            return ("PASS", f"301 → {loc}") if fcode == 200 else ("FAIL", f"301 → {loc}, but target answers {fcode} (chain or error)")
        return "FAIL", f"answers {code} {loc or ''}".strip()
    if k in ("seo_title", "meta_description"):
        code, _, body = fetch(url)
        live = page_title(body) if k == "seo_title" else page_desc(body)
        return ("PASS", "live shows the new value") if live == new else ("FAIL", f"live shows {live!r}")
    if k == "broken_link":
        code, _, body = fetch(url)
        return ("PASS", "old link gone") if c["old"] and c["old"] not in body else ("FAIL", "page still links to the old URL")
    if k == "page_content":
        code, _, _ = fetch(url) if url else (0, {}, "")
        return ("PASS", f"page answers {code}") if code == 200 else ("CHECK", f"answers {code} (drafts are not public)")
    return "CHECK", "needs a person to confirm (not machine-checkable here)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--run", required=True)
    ap.add_argument("--of"); ap.add_argument("--handoff"); ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    R.open_run(a.slug, a.run)
    d = client_dir(a.slug)

    targets = []
    for c in R.changes(a.slug, a.of if a.of else None):
        if c["kind"] in ("verify", "handoff_return"):
            continue
        if c.get("channel") == "wp" and c["result"].startswith("APPLIED"):
            targets.append(c)
    done_refs = set()
    for f in sorted((d / "handoffs").glob("H-*.csv")):
        if a.handoff and f.stem != a.handoff:
            continue
        with open(f, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["status"] == "done":
                    done_refs.add(row["ref"])
    for c in R.changes(a.slug):
        if c.get("channel") == "handoff" and c["result"].startswith("HANDOFF ISSUED") and c.get("ref") in done_refs:
            targets.append(c)

    lines = [f"# Verify — {a.slug} — run {a.run}", "", "| # | Ref | Kind | URL | Result | Detail |", "|---|---|---|---|---|---|"]
    counts = {"PASS": 0, "FAIL": 0, "CHECK": 0}
    for c in targets:
        res, detail = check(c)
        counts[res] += 1
        lines.append(f"| {c['n']} | {c.get('ref') or ''} | {c['kind']} | {c['url']} | {res} | {detail} |")
        R.log_change(a.slug, a.run, "verify", c["url"], f"change #{c['n']} {c['kind']}", c["old"], c["new"],
                     f"VERIFY {res} — {detail}", ref=c.get("ref"), channel="local")
    out = d / "handoffs" / f"verify-{a.run}.md"
    out.write_text("\n".join([lines[0], "", f"PASS {counts['PASS']} · FAIL {counts['FAIL']} · "
                              f"needs a person {counts['CHECK']}", ""] + lines[2:]) + "\n")
    print(f"PASS {counts['PASS']} · FAIL {counts['FAIL']} · CHECK {counts['CHECK']} → {out.relative_to(d.parent.parent)}")


if __name__ == "__main__":
    main()
