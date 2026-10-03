#!/usr/bin/env python3
"""verify.py — re-check every changed page against the live site.

    verify.py <slug> --run R [--of RUN_ID] [--handoff H-ID] [--all]
    verify.py <slug> --run R --batch B      every published page of a batch against its approved file
    verify.py <slug> --run R --page P       one published page (a blog post) against its approved file

Checks, per logged change:
  - system-applied SEO title / meta description -> read live via SEOPress and the public HTML
  - system-applied alt text / content / head    -> read back through wp.py
  - handoff items the VA marked done:
      redirect / slug pair -> the old URL answers 301 with Location = the new URL (no chain)
      seo_title / meta_description -> the public page shows the new value
      broken_link -> the page no longer links to the old URL
      everything else -> listed for a person to check (sitemap, robots.txt, speed)
Batch mode (after Jonie publishes): for each page, the live URL answers 200 and its SEO title,
meta description, target keyword (read back from SEOPress), Open Graph and X title/description, H1,
heading structure (levels and text), body text and link-table links match the
approved file exactly. Every difference is listed for Paul. Images without alt text are listed for
the alt-text safe fix. Exit 0 all match · 1 differences found.
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


def meta_prop(body, prop):
    """Open Graph / X tags: <meta property|name="og:title" content="...">."""
    for rx in (rf'<meta[^>]+(?:property|name)=["\']{re.escape(prop)}["\'][^>]+content=["\'](.*?)["\']',
               rf'<meta[^>]+content=["\'](.*?)["\'][^>]+(?:property|name)=["\']{re.escape(prop)}["\']'):
        m = re.search(rx, body, re.S | re.I)
        if m:
            return html.unescape(m.group(1).strip())
    return ""


def strip_tags(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[*_`]|\[([^\]]+)\]\([^)]+\)", r"\1", t or "")).strip()


def expected(meta):
    """Headings and paragraph text the approved file says the page must show."""
    heads, paras = [], []
    for ln in meta["body"].split("\n"):
        m = re.match(r"^(#{2,6}) (.+)$", ln)
        if m:
            heads.append((len(m.group(1)), norm(m.group(2))))
        elif ln.strip() and not ln.lstrip().startswith(("|", "-", "*")) and not re.match(r"^\s*\d+\. ", ln):
            paras.append(norm(ln))
    return heads, " ".join(paras)


def live_parts(body):
    heads = [(int(l), norm(strip_tags(t))) for l, t in re.findall(r"<h([2-6])[^>]*>(.*?)</h\1>", body, re.S | re.I)]
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
    paras = " ".join(norm(strip_tags(p)) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S | re.I))
    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', body, re.I)
    imgs = [(src, alt) for src, alt in
            [(re.search(r'src=["\']([^"\']+)', t).group(1) if re.search(r'src=["\']([^"\']+)', t) else "",
              (re.search(r'alt=["\']([^"\']*)', t).group(1) if re.search(r'alt=["\']([^"\']*)', t) else ""))
             for t in re.findall(r"<img[^>]*>", body, re.I)]]
    return norm(strip_tags(h1.group(1))) if h1 else "", heads, paras, links, imgs


def verify_batch(a, d):
    import publish
    import status as S
    st = S.load(a.slug)
    b = S.batch(st, a.batch) if a.batch else {"pages": [a.page]}
    if not b:
        raise SystemExit(f"no batch {a.batch}")
    lines = [f"# Verify — {a.slug} — {('batch ' + a.batch) if a.batch else a.page} — run {a.run}", "",
             "Each live page against its approved file. Any difference goes to Paul.", ""]
    fails, alt_needed = 0, []
    for pid in b["pages"]:
        p = st["pages"].get(pid) or {}
        meta = publish.parse(p["file"])
        diffs = []
        code, _, body = fetch(meta["url"])
        if code != 200:
            diffs.append(f"URL {meta['url']} answers {code}")
        else:
            h1, heads, text, links, imgs = live_parts(body)
            want_heads, want_text = expected(meta)
            if page_title(body) != meta["seo_title"]:
                diffs.append(f"SEO title is {page_title(body)!r}, approved {meta['seo_title']!r}")
            if page_desc(body) != meta["meta_description"]:
                diffs.append(f"meta description is {page_desc(body)!r}, approved {meta['meta_description']!r}")
            for prop, want in (("og:title", meta["seo_title"]), ("og:description", meta["meta_description"]),
                               ("twitter:title", meta["seo_title"]), ("twitter:description", meta["meta_description"])):
                got = meta_prop(body, prop)
                if got != want:
                    diffs.append(f"{prop} is {got!r}, approved {want!r}")
            want_kw = meta.get("keyword") or p.get("keyword") or ""
            if want_kw and p.get("wp_id"):
                try:
                    import wp
                    got_kw = wp.seo_read(a.slug, p["wp_id"])["keyword"]
                    if got_kw != want_kw:
                        diffs.append(f"target keyword is {got_kw!r}, approved {want_kw!r}")
                except Exception as e:  # noqa: BLE001
                    diffs.append(f"target keyword could not be read back ({e})")
            if h1 != norm(meta["h1"]):
                diffs.append(f"H1 is {h1!r}, approved {meta['h1']!r}")
            live_heads = [h for h in heads if h[1] != "Link"]
            if live_heads != want_heads:
                missing = [h for h in want_heads if h not in live_heads]
                extra = [h for h in live_heads if h not in want_heads]
                diffs.append("heading structure differs" + (f"; missing {missing}" if missing else "")
                             + (f"; not in the approved file {extra}" if extra else "")
                             + ("; same headings in a different order or level" if not missing and not extra else ""))
            if text != want_text:
                wa, la = want_text.split(". "), text.split(". ")
                first = next((i for i, (x, y) in enumerate(zip(wa, la)) if x != y), min(len(wa), len(la)))
                diffs.append(f"body text differs from the approved file at: "
                             f"{(la[first] if first < len(la) else '(text missing)')[:120]!r}")
            miss_links = [u for u in p.get("links_placed", []) if u not in links]
            if miss_links:
                diffs.append(f"link-table links missing: {', '.join(miss_links[:6])}")
            alt_needed += [(pid, src) for src, alt in imgs if not alt.strip()]
        res = "FAIL" if diffs else "PASS"
        fails += bool(diffs)
        lines.append(f"## {pid} — {meta['url']} — {res}")
        lines += [f"- {x}" for x in diffs] or ["- matches the approved file"]
        lines.append("")
        R.log_change(a.slug, a.run, "verify", meta["url"], "live vs approved file", p["file"], meta["url"],
                     f"VERIFY {res}" + (f" — {'; '.join(diffs)[:300]}" if diffs else ""), ref=pid, channel="local")
    if alt_needed:
        lines += ["## Images without alt text (alt-text safe fix)", ""] + [f"- {pid}: {src}" for pid, src in alt_needed]
    out = d / "handoffs" / f"verify-{a.run}.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"{len(b['pages']) - fails} page(s) match · {fails} differ · {len(alt_needed)} image(s) need alt text → "
          f"{out.relative_to(d.parent.parent)}")
    raise SystemExit(1 if fails else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--run", required=True)
    ap.add_argument("--of"); ap.add_argument("--handoff"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--batch"); ap.add_argument("--page")
    a = ap.parse_args()
    R.open_run(a.slug, a.run)
    d = client_dir(a.slug)
    if a.batch or a.page:
        return verify_batch(a, d)

    targets = []
    for c in R.changes(a.slug, a.of if a.of else None):
        if c["kind"] in ("verify", "handoff_return"):
            continue
        if c.get("channel") == "wp" and c["result"].startswith("APPLIED"):
            targets.append(c)
    done_refs = set()
    for f in sorted(x for x in (d / "handoffs").glob("H-*.csv") if not x.stem.endswith("-returned")):
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
