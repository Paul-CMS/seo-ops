#!/usr/bin/env python3
"""crawl.py — DataforSEO OnPage crawl for /crawl.

    crawl.py estimate <slug> --domain D [--max-pages N] [--mode basic|javascript]
    crawl.py run      <slug> --run RUN_ID --domain D [--max-pages N] [--mode basic]
                      [--crawl-delay 2000] [--confirmed] [--new-crawl] [--max-wait 540]
    crawl.py status   <slug>
    crawl.py summary  <slug>                 (re)build data/crawl/crawl-summary.csv from the crawl tables
    crawl.py competitors estimate|run <slug> …   P6: top competitor pages per service keyword — coverage ideas only (competitors.py)
    crawl.py text     <slug> --run RUN_ID [--delay 2] [--max-words 800]
                                             S05b: free, polite fetch of each crawled HTML page's body
                                             text -> data/crawl/page-text.csv

--max-pages (#18): when it is not given, it is the site's sitemap size x 1.5 (rounded up,
minimum 20, maximum 1000) — the sitemap is read from robots.txt `Sitemap:` lines, else
/sitemap.xml, else /sitemap_index.xml (indexes followed). No readable sitemap -> the old
default of 1000, and the estimate says so. The estimate always prints the value and why.

Agents read the script-made summaries (crawl-summary.csv, page-text.csv), never the raw
exports (R5).

`run` is resumable and idempotent. It reads clients/<slug>/inputs/crawl/crawl-state.json:
  - no task yet          -> estimate, spend guard, post ONE task (the only paid step)
  - task still crawling  -> poll (progress notes to log.md) up to --max-wait seconds,
                            then exit 10 so the caller simply runs it again
  - task finished        -> download every result set (free, kept 30 days by DataforSEO),
                            checkpointed so an interruption resumes where it stopped
  - downloaded           -> convert into the Screaming Frog-shaped tables the audit
                            skill expects
A second paid crawl for the same domain needs --new-crawl (and Paul's confirmation).

--domain must be the client's domain (status.json client.domain, www. ignored); another domain only with
--other-domain, on Paul's word (CR-048).

Exit codes: 4 refused · 5 needs Paul's cost confirmation · 6 would exceed balance · 10 still crawling.
"""
import argparse
import csv
import datetime
import html as htmlmod
import http
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.robotparser
from collections import Counter, defaultdict
from pathlib import Path

import dfs
import run as R
import status as S
from lib import client_dir, die, now, read_json, write_json

RESULT_SETS = ["pages", "links", "duplicate_title", "duplicate_description",
               "redirect_chains", "non_indexable", "duplicate_content"]
PACE = 0.25  # seconds between result calls — well under the 2000/min API limit
WEB_PACE = 1.0  # seconds between our own fetches of the client's public site (sitemaps)
DEFAULT_MAX_PAGES, MIN_MAX_PAGES, CAP_MAX_PAGES = 1000, 20, 1000
MAX_CHILD_SITEMAPS = 50


def crawl_dir(slug):
    d = client_dir(slug) / "inputs" / "crawl"
    (d / "raw").mkdir(parents=True, exist_ok=True)
    return d


def state_path(slug):
    return crawl_dir(slug) / "crawl-state.json"


def note(slug, run_id, text):
    R.open_run(slug, run_id)
    from lib import append
    append(client_dir(slug) / "log.md", f"- NOTE {now()[11:19]} crawl: {text}\n")


def clean_domain(d):
    d = d.strip().lower()
    for p in ("https://", "http://"):
        if d.startswith(p):
            d = d[len(p):]
    if d.startswith("www."):
        d = d[4:]
    return d.split("/")[0]


# ---------------------------------------------------------------- public web (free, polite)
def web_fetch(url):
    """The same public-web fetch verify.py uses (one GET, honest user agent, 30 s timeout).
    Looked up at call time so the test suite's fake web applies here too."""
    import verify
    return verify.fetch(url)


def data_dir(slug):
    d = client_dir(slug) / "data" / "crawl"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _same_site(url, domain):
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host == domain or host == "www." + domain


def sitemap_urls(domain):
    """Page URLs listed in the site's sitemap(s). Returns (set of urls, list of sitemap files read).
    Order: robots.txt Sitemap: lines, else /sitemap.xml, else /sitemap_index.xml; indexes followed
    (at most MAX_CHILD_SITEMAPS child files). One fetch at a time, WEB_PACE seconds apart."""
    base = f"https://{domain}"
    fetched = [0]

    def get(u):
        if fetched[0]:
            time.sleep(WEB_PACE)
        fetched[0] += 1
        code, _, body = web_fetch(u)
        return body if code == 200 and body else ""

    robots = get(base + "/robots.txt")
    starts = [l.split(":", 1)[1].strip() for l in robots.splitlines()
              if l.strip().lower().startswith("sitemap:") and l.split(":", 1)[1].strip()]
    candidates = starts or [base + "/sitemap.xml", base + "/sitemap_index.xml"]
    urls, read, seen = set(), [], set()
    for start in candidates:
        queue = [start]
        while queue and len(seen) <= MAX_CHILD_SITEMAPS:
            sm = queue.pop(0)
            if sm in seen:
                continue
            seen.add(sm)
            if sm.lower().endswith(".gz"):
                continue          # compressed sitemaps are not read; the fallback covers it
            body = get(sm)
            if "<loc" not in body.lower():
                continue
            read.append(sm)
            locs = [htmlmod.unescape(x.strip()) for x in
                    re.findall(r"<loc>\s*(.*?)\s*</loc>", body, re.S | re.I)]
            if re.search(r"<sitemapindex\b", body, re.I):
                queue += [x for x in locs if x not in seen]
            else:
                urls.update(x for x in locs if _same_site(x, domain))
        if urls and not starts:
            break                 # /sitemap.xml worked — no need for /sitemap_index.xml
    return urls, read


def choose_max_pages(domain, given):
    """(max_pages, reason). An explicit --max-pages always wins."""
    if given is not None:
        return given, "set with --max-pages"
    try:
        urls, read = sitemap_urls(domain)
    except Exception as e:      # never let a sitemap problem stop the crawl
        urls, read = set(), []
        why = f"sitemap could not be read ({e})"
    else:
        why = "no readable sitemap (robots.txt, /sitemap.xml, /sitemap_index.xml)"
    if not urls:
        return DEFAULT_MAX_PAGES, f"{why} — fell back to the old default of {DEFAULT_MAX_PAGES}"
    n = len(urls)
    mp = min(CAP_MAX_PAGES, max(MIN_MAX_PAGES, math.ceil(n * 1.5)))
    return mp, (f"sitemap lists {n} URLs ({len(read)} sitemap file(s): {', '.join(read[:3])}"
                f"{' …' if len(read) > 3 else ''}) × 1.5 = {math.ceil(n * 1.5)}, "
                f"kept between {MIN_MAX_PAGES} and {CAP_MAX_PAGES}")


# ---------------------------------------------------------------- estimate / post
def do_estimate(domain, max_pages, mode):
    est = dfs.estimate("on_page/task_post", pages=max_pages, mode=mode)
    bal = dfs.balance()
    return est, bal


def post_task(slug, run_id, st, domain, max_pages, mode, delay, confirmed, reason=""):
    est = dfs.estimate("on_page/task_post", pages=max_pages, mode=mode)
    task = {"target": domain, "max_crawl_pages": max_pages, "crawl_delay": delay,
            "enable_javascript": mode == "javascript", "load_resources": False,
            "respect_sitemap": False, "tag": f"seo-ops:{slug}:{run_id}"[:255]}
    resp = dfs.paid_post(slug, "on_page/task_post", [task],
                         f"OnPage crawl {domain} ({mode}, max {max_pages} pages)", est, confirmed)
    t = dfs.task_result(resp)
    st.update({"task_id": t["id"], "domain": domain, "max_pages": max_pages, "mode": mode,
               "crawl_delay_ms": delay, "posted_at": now(), "posted_by_run": run_id,
               "estimate_usd": est, "cost_usd": resp.get("cost"), "phase": "crawling",
               "max_pages_reason": reason, "checkpoints": {}})
    write_json(state_path(slug), st)
    note(slug, run_id, f"task posted for {domain} ({mode}, max {max_pages} pages — {reason}, "
         f"{delay} ms between hits) · cost ${resp.get('cost')} · task {t['id']}")


def poll(slug, run_id, st, max_wait):
    start, last_pct, last_note = time.time(), -1, 0
    while True:
        r = dfs.request(f"on_page/summary/{st['task_id']}", method="GET")
        res = (dfs.task_result(r).get("result") or [{}])[0]
        cs = res.get("crawl_status") or {}
        crawled, mx = cs.get("pages_crawled") or 0, cs.get("max_crawl_pages") or st["max_pages"]
        pct = int(100 * crawled / max(mx, 1))
        if res.get("crawl_progress") == "finished":
            st["phase"] = "downloading"
            st["summary"] = {"pages_crawled": crawled, "stop_reason": res.get("crawl_stop_reason"),
                             "domain_info": res.get("domain_info"), "page_metrics": res.get("page_metrics")}
            write_json(state_path(slug), st)
            note(slug, run_id, f"crawl finished: {crawled} pages, stop reason "
                 f"{res.get('crawl_stop_reason')}")
            return True
        if pct >= last_pct + 10 or time.time() - last_note > 600:
            note(slug, run_id, f"crawling — {crawled}/{mx} pages ({pct}%), "
                 f"{cs.get('pages_in_queue')} in queue")
            last_pct, last_note = pct, time.time()
        if time.time() - start > max_wait:
            return False
        time.sleep(30)


# ---------------------------------------------------------------- download
def _paginate(slug, st, name, endpoint, body):
    """Download a result set in pages of 1000 into raw/<name>.jsonl, checkpointed."""
    raw = crawl_dir(slug) / "raw" / f"{name}.jsonl"
    cp = st["checkpoints"].setdefault(name, {"offset": 0, "token": None, "done": False})
    if cp["done"]:
        return
    while True:
        req = {"id": st["task_id"], "limit": 1000, **body}
        if cp["token"]:
            req["search_after_token"] = cp["token"]
        else:
            req["offset"] = cp["offset"]
        r = dfs.request(endpoint, [req])
        res = (dfs.task_result(r).get("result") or [{}])[0]
        items = res.get("items") or []
        with open(raw, "a", encoding="utf-8") as fh:
            for it in items:
                fh.write(json.dumps(it, ensure_ascii=False) + "\n")
        cp["offset"] += len(items)
        cp["token"] = res.get("search_after_token") if cp["offset"] >= 20000 else None
        write_json(state_path(slug), st)
        if len(items) < 1000 or (cp["offset"] >= 20000 and not cp["token"]):
            cp["done"] = True
            write_json(state_path(slug), st)
            return
        time.sleep(PACE)


def download(slug, run_id, st):
    _paginate(slug, st, "pages", "on_page/pages", {})
    note(slug, run_id, f"downloaded pages ({st['checkpoints']['pages']['offset']})")
    _paginate(slug, st, "links", "on_page/links", {})
    note(slug, run_id, f"downloaded links ({st['checkpoints']['links']['offset']})")
    for t in ("duplicate_title", "duplicate_description"):
        _paginate(slug, st, t, "on_page/duplicate_tags", {"type": t})
    _paginate(slug, st, "redirect_chains", "on_page/redirect_chains", {})
    _paginate(slug, st, "non_indexable", "on_page/non_indexable", {})
    # duplicate_content works per URL, so only ask about pages the crawl flagged
    cp = st["checkpoints"].setdefault("duplicate_content", {"done_urls": [], "done": False})
    if not cp["done"]:
        raw = crawl_dir(slug) / "raw" / "duplicate_content.jsonl"
        flagged = [p["url"] for p in read_jsonl(crawl_dir(slug) / "raw" / "pages.jsonl")
                   if (p.get("checks") or {}).get("duplicate_content")]
        for u in flagged:
            if u in cp["done_urls"]:
                continue
            r = dfs.request("on_page/duplicate_content", [{"id": st["task_id"], "url": u, "limit": 100}])
            res = (dfs.task_result(r).get("result") or [{}])[0]
            with open(raw, "a", encoding="utf-8") as fh:
                for it in res.get("items") or []:
                    fh.write(json.dumps({"source_url": u, **it}, ensure_ascii=False) + "\n")
            cp["done_urls"].append(u)
            write_json(state_path(slug), st)
            time.sleep(PACE)
        cp["done"] = True
    st["phase"] = "converting"
    write_json(state_path(slug), st)
    note(slug, run_id, "all result sets downloaded (no charge for downloads)")


def read_jsonl(p):
    p = Path(p)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


# ---------------------------------------------------------------- convert
def _status_text(code):
    try:
        return http.HTTPStatus(int(code)).phrase
    except Exception:
        return ""


def _dedupe(rows, key):
    seen, out = set(), []
    for r in rows:
        k = key(r)
        if k not in seen:
            seen.add(k); out.append(r)
    return out


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)


def convert(slug, run_id, st):
    d = crawl_dir(slug)
    stc = S.load(slug)
    client = stc["client"]["name"]
    date = (st.get("posted_at") or now())[:10]
    pre = f"{client} - DFS - "
    pages = _dedupe(read_jsonl(d / "raw" / "pages.jsonl"), lambda p: p.get("url"))
    links = _dedupe(read_jsonl(d / "raw" / "links.jsonl"),
                    lambda l: (l.get("link_from"), l.get("link_to"), l.get("type"), l.get("text")))
    nonidx = {n.get("url"): n.get("reason") for n in read_jsonl(d / "raw" / "non_indexable.jsonl")}
    html = [p for p in pages if p.get("resource_type") in ("html", "redirect", "broken")]

    uniq_in = defaultdict(set)
    for l in links:
        if l.get("direction") == "internal" and l.get("type") == "anchor":
            uniq_in[l.get("link_to")].add(l.get("link_from"))

    def meta(p):
        return p.get("meta") or {}

    def htags(p, h):
        return list(((meta(p).get("htags") or {}).get(h)) or [])

    def indexability(p):
        code = p.get("status_code") or 0
        if p["url"] in nonidx:
            return "Non-Indexable", {"robots_txt": "Blocked by Robots.txt", "meta_tag": "noindex",
                                     "http_header": "noindex (X-Robots-Tag)",
                                     "attribute": "Canonicalised",
                                     "too_many_redirects": "Redirect loop"}.get(nonidx[p["url"]], nonidx[p["url"]])
        if 300 <= code < 400:
            return "Non-Indexable", "Redirected"
        if code >= 400:
            return "Non-Indexable", "Client Error" if code < 500 else "Server Error"
        can = meta(p).get("canonical")
        if can and can.rstrip("/") != p["url"].rstrip("/"):
            return "Non-Indexable", "Canonicalised"
        if (p.get("checks") or {}).get("no_index"):
            return "Non-Indexable", "noindex"
        return "Indexable", ""

    title_n = Counter(meta(p).get("title") for p in html if meta(p).get("title"))
    desc_n = Counter(meta(p).get("description") for p in html if meta(p).get("description"))
    h1_n = Counter(h for p in html for h in htags(p, "h1")[:1])
    h2_n = Counter(h for p in html for h in htags(p, "h2")[:1])

    # internal_all
    hdr = ["Address", "Content Type", "Status Code", "Status", "Indexability", "Indexability Status",
           "Title 1", "Title 1 Length", "Meta Description 1", "Meta Description 1 Length",
           "H1-1", "H1-1 Length", "H1-2", "H1-2 Length", "H2-1", "H2-1 Length", "H2-2", "H2-2 Length",
           "Meta Robots 1", "Canonical Link Element 1", "Size (bytes)", "Word Count", "Crawl Depth",
           "Inlinks", "Unique Inlinks", "Outlinks", "External Outlinks", "Redirect URL",
           "Response Time", "Crawl Timestamp"]
    rows = []
    for p in html:
        m, idx = meta(p), indexability(p)
        h1, h2 = htags(p, "h1"), htags(p, "h2")
        pt = p.get("page_timing") or {}
        rows.append([p["url"], "text/html; charset=UTF-8", p.get("status_code"), _status_text(p.get("status_code")),
                     idx[0], idx[1], m.get("title") or "", len(m.get("title") or ""),
                     m.get("description") or "", len(m.get("description") or ""),
                     h1[0] if h1 else "", len(h1[0]) if h1 else 0, h1[1] if len(h1) > 1 else "",
                     len(h1[1]) if len(h1) > 1 else 0, h2[0] if h2 else "", len(h2[0]) if h2 else 0,
                     h2[1] if len(h2) > 1 else "", len(h2[1]) if len(h2) > 1 else 0,
                     m.get("robots") or "", m.get("canonical") or "", p.get("size") or "",
                     ((m.get("content") or {}).get("plain_text_word_count")) or 0, p.get("click_depth"),
                     m.get("inbound_links_count") or 0, len(uniq_in.get(p["url"], ())),
                     m.get("internal_links_count") or 0, m.get("external_links_count") or 0,
                     p.get("location") or "", pt.get("duration_time") or pt.get("download_time") or "",
                     p.get("fetch_time") or ""])
    out = {}
    out["internal_all"] = (hdr, rows)

    # links_all (SF "Links" tab shape)
    out["links_all"] = (["Address", "Indexability", "Indexability Status", "Crawl Depth", "Link Score",
                         "Inlinks", "Unique Inlinks", "Outlinks", "Unique Outlinks", "External Outlinks"],
                        [[r[0], r[4], r[5], r[22], "", r[23], r[24], r[25], "", r[26]] for r in rows])

    def occ_table(field_name, values_of, counter, n=2):
        h = ["Address", "Occurrences"]
        for i in range(1, n + 1):
            h += [f"{field_name}-{i}" if field_name.startswith("H") else f"{field_name} {i}",
                  f"{field_name}-{i} Length" if field_name.startswith("H") else f"{field_name} {i} Length"]
        h += ["Indexability", "Indexability Status"]
        body = []
        for p in html:
            vals = values_of(p)
            row = [p["url"], counter.get(vals[0], 0) if vals else 0]
            for i in range(n):
                v = vals[i] if len(vals) > i else ""
                row += [v, len(v)]
            row += list(indexability(p))
            body.append(row)
        return h, body

    out["page_titles_all"] = occ_table("Title", lambda p: [meta(p).get("title")] if meta(p).get("title") else [], title_n, 1)
    out["meta_description_all"] = occ_table("Meta Description",
                                            lambda p: [meta(p).get("description")] if meta(p).get("description") else [], desc_n, 1)
    out["h1_all"] = occ_table("H1", lambda p: htags(p, "h1"), h1_n, 2)
    max_h2 = max([len(htags(p, "h2")) for p in html] + [1])
    out["h2_all"] = occ_table("H2", lambda p: htags(p, "h2"), h2_n, min(max_h2, 30))

    # all_inlinks
    pstatus = {p["url"]: p.get("status_code") for p in pages}
    out["all_inlinks"] = (["Type", "Source", "Destination", "Anchor Text", "Alt Text", "Follow",
                           "Status Code", "Link Path", "Link Position"],
                          [[{"anchor": "Hyperlink", "image": "Image", "canonical": "Canonical",
                             "redirect": "Redirect"}.get(l.get("type"), l.get("type")),
                            l.get("link_from"), l.get("link_to"), l.get("text") or "",
                            l.get("image_alt") or "", "True" if l.get("dofollow") else "False",
                            l.get("page_to_status_code") or pstatus.get(l.get("link_to"), ""), "", ""]
                           for l in links if l.get("direction") == "internal"])

    # external_all
    ext = defaultdict(set)
    for l in links:
        if l.get("direction") == "external":
            ext[l.get("link_to")].add(l.get("link_from"))
    out["external_all"] = (["Address", "Content Type", "Status Code", "Status", "Crawl Depth", "Inlinks"],
                           [[u, "", "", "Not checked (DataforSEO does not fetch external URLs)", "", len(s)]
                            for u, s in sorted(ext.items())])

    # DataforSEO-only tables
    def dup_tags(name):
        rows_ = []
        for it in read_jsonl(d / "raw" / f"{name}.jsonl"):
            for pg in it.get("pages") or []:
                rows_.append([it.get("accumulator"), it.get("total_count"), pg.get("url"), pg.get("status_code")])
        return ["Duplicated Value", "Pages Sharing It", "Address", "Status Code"], rows_

    out["duplicate_titles"] = dup_tags("duplicate_title")
    out["duplicate_descriptions"] = dup_tags("duplicate_description")
    dc = []
    for it in read_jsonl(d / "raw" / "duplicate_content.jsonl"):
        for pg in it.get("pages") or []:
            for x in pg.get("page") or []:
                dc.append([it.get("source_url"), x.get("url"), pg.get("similarity")])
    out["duplicate_content"] = (["Address", "Similar Address", "Similarity (0-10)"], dc)
    rc = []
    for i, it in enumerate(read_jsonl(d / "raw" / "redirect_chains.jsonl"), 1):
        for j, hop in enumerate(it.get("chain") or [], 1):
            rc.append([f"chain-{i}", j, hop.get("from_url"), hop.get("to_url"),
                       hop.get("status_code") or "", "True" if it.get("is_redirect_loop") else "False"])
    out["redirect_chains"] = (["Chain ID", "Hop", "From URL", "To URL", "Status Code", "Redirect Loop"], rc)
    out["non_indexable"] = (["Address", "Non-Indexable Reason"], sorted(nonidx.items()))

    written = []
    for name, (h, body) in out.items():
        fn = d / f"{pre}{name} - {date}.csv"
        write_csv(fn, h, body)
        written.append(f"{fn.name} ({len(body)} rows)")

    cfg = (f"# {client} - DFS - crawl-config - {date}\n\n"
           f"- Tool: DataforSEO OnPage API, task `{st['task_id']}`\n"
           f"- Mode: {st['mode']} (JavaScript {'on' if st['mode'] == 'javascript' else 'off'};"
           " missing JavaScript-rendered data is never a finding)\n"
           f"- Max pages: {st['max_pages']} ({st.get('max_pages_reason') or 'set with --max-pages'}) · crawled: {(st.get('summary') or {}).get('pages_crawled')}"
           f" · stop reason: {(st.get('summary') or {}).get('stop_reason')}\n"
           f"- Crawl delay: {st['crawl_delay_ms']} ms between hits · user agent: DataforSEO default\n"
           f"- Posted: {st['posted_at']} · cost: ${st.get('cost_usd')}\n"
           "- Converted to Screaming Frog-shaped tables (internal_all, links_all, page_titles_all,"
           " meta_description_all, h1_all, h2_all, all_inlinks, external_all). Columns DataforSEO"
           " does not provide (Link Score, external status codes) are left blank — not findings.\n"
           "- Unlike the free Screaming Frog licence: no 500-URL cap, full H2 lists available.\n")
    (d / f"{client} - DFS - crawl-config - {date}.md").write_text(cfg)
    st["phase"] = "converted"
    st["converted_at"] = now()
    write_json(state_path(slug), st)
    p, n = build_summary(slug)
    written.append(f"{p.relative_to(client_dir(slug))} ({n} rows) — the file agents read")
    note(slug, run_id, "converted: " + "; ".join(written))
    print("\n".join(written))


# ---------------------------------------------------------------- R5: compact summary for agents
SUMMARY_COLS = [  # summary column <- internal_all column
    ("url", "Address"), ("status", "Status Code"), ("indexability", "Indexability"),
    ("indexability_status", "Indexability Status"), ("title", "Title 1"), ("title_len", "Title 1 Length"),
    ("meta_description", "Meta Description 1"), ("meta_len", "Meta Description 1 Length"),
    ("h1", "H1-1"), ("h1_count", None), ("word_count", "Word Count"), ("canonical", "Canonical Link Element 1"),
    ("meta_robots", "Meta Robots 1"), ("inlinks", "Inlinks"), ("unique_inlinks", "Unique Inlinks"),
    ("outlinks", "Outlinks"), ("external_outlinks", "External Outlinks"), ("depth", "Crawl Depth"),
    ("redirect_url", "Redirect URL")]


def latest_table(slug, name):
    hits = sorted(crawl_dir(slug).glob(f"* - DFS - {name} - *.csv"), key=lambda p: (p.name[-14:], p.name))
    return hits[-1] if hits else None


def build_summary(slug):
    """data/crawl/crawl-summary.csv: one row per crawled page, audited columns only, from the
    converted internal_all table (H1 count from the raw pages when present)."""
    src = latest_table(slug, "internal_all")
    if not src:
        die(f"no converted crawl table (internal_all) in clients/{slug}/inputs/crawl/ — run /crawl first.", 4)
    h1n = {}
    for p in read_jsonl(crawl_dir(slug) / "raw" / "pages.jsonl"):
        h1n[p.get("url")] = len(((p.get("meta") or {}).get("htags") or {}).get("h1") or [])
    with open(src, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    body = []
    for r in rows:
        u = r.get("Address", "")
        cnt = h1n.get(u)
        if cnt is None:
            cnt = sum(1 for c in ("H1-1", "H1-2") if r.get(c))
            cnt = "2+" if cnt == 2 else cnt
        body.append([cnt if col is None else r.get(col, "") for _, col in SUMMARY_COLS])
    out = data_dir(slug) / "crawl-summary.csv"
    write_csv(out, [k for k, _ in SUMMARY_COLS], body)
    return out, len(body)


# ---------------------------------------------------------------- S05b: page text capture (free)
_DROP = re.compile(r"<(script|style|noscript|svg|template|iframe|nav|header|footer|form)\b.*?</\1\s*>", re.S | re.I)


def page_text(body):
    """(h1, body text). Main content when the page marks it (<main>/<article>), else <body>,
    without scripts, styles, navigation, header, footer and forms."""
    m = re.search(r"<h1\b[^>]*>(.*?)</h1\s*>", body, re.S | re.I)
    h1 = re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""
    b = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    b = _DROP.sub(" ", b)
    for tag in ("main", "article", "body"):
        mm = re.search(rf"<{tag}\b[^>]*>(.*)</{tag}\s*>", b, re.S | re.I)
        if mm:
            b = mm.group(1)
            break
    b = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/tr)\b[^>]*>", " ", b, flags=re.I)
    text = re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", b))).strip()
    return h1, text


def crawled_html_urls(slug):
    """Internal HTML pages the crawl returned with a 200, from the raw pages (else internal_all)."""
    pages = read_jsonl(crawl_dir(slug) / "raw" / "pages.jsonl")
    if pages:
        urls = [p["url"] for p in pages if p.get("url") and p.get("resource_type") == "html"
                and p.get("status_code") == 200]
    else:
        src = latest_table(slug, "internal_all")
        if not src:
            die(f"no crawl in clients/{slug}/inputs/crawl/ — run /crawl first (S05).", 4)
        with open(src, newline="", encoding="utf-8") as fh:
            urls = [r["Address"] for r in csv.DictReader(fh) if str(r.get("Status Code")) == "200"]
    return list(dict.fromkeys(urls))


def capture_text(slug, run_id, delay, max_words):
    R.open_run(slug, run_id)
    urls = crawled_html_urls(slug)
    st = read_json(state_path(slug), {})
    domain = st.get("domain") or clean_domain(S.load(slug)["client"].get("domain") or "")
    rp = urllib.robotparser.RobotFileParser()
    code, _, robots = web_fetch(f"https://{domain}/robots.txt") if domain else (0, {}, "")
    rp.parse(robots.splitlines() if code == 200 else [])
    rows, skipped, failed = [], 0, 0
    for i, u in enumerate(urls):
        if not rp.can_fetch("*", u):
            skipped += 1
            rows.append([u, "", "", 0, "", "not fetched: disallowed by robots.txt"])
            continue
        time.sleep(delay)
        code, _, body = web_fetch(u)
        if code != 200 or not body:
            failed += 1
            rows.append([u, code, "", 0, "", f"not fetched: HTTP {code}"])
            continue
        h1, text = page_text(body)
        words = text.split()
        cut = len(words) > max_words
        rows.append([u, code, h1, len(words), "yes" if cut else "no",
                     " ".join(words[:max_words]) + (" …" if cut else "")])
    out = data_dir(slug) / "page-text.csv"
    write_csv(out, ["url", "status", "h1", "word_count", "truncated", "text"], rows)
    msg = (f"S05b page text: {len(rows) - skipped - failed} of {len(urls)} pages captured"
           f" ({skipped} disallowed by robots.txt, {failed} failed) · first {max_words} words each"
           f" · {out.relative_to(client_dir(slug))} · no charge")
    note(slug, run_id, msg)
    print(msg)
    return out


# ---------------------------------------------------------------- CLI
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "competitors":   # P6: crawl.py competitors <estimate|run> <slug> …
        import competitors
        sys.argv = ["competitors.py"] + sys.argv[2:]
        return competitors.main()
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("estimate", "run"):
        s = sub.add_parser(name); s.add_argument("slug"); s.add_argument("--domain", required=True)
        s.add_argument("--max-pages", type=int, default=None,
                       help="default: sitemap size x 1.5 (min 20, max 1000); 1000 if no sitemap")
        s.add_argument("--mode", choices=["basic", "javascript"], default="basic")
        s.add_argument("--other-domain", action="store_true",
                       help="crawl a domain that is not the client's recorded one — only on Paul's word (CR-048)")
        if name == "run":
            s.add_argument("--run", required=True); s.add_argument("--crawl-delay", type=int, default=2000)
            s.add_argument("--confirmed", action="store_true"); s.add_argument("--new-crawl", action="store_true")
            s.add_argument("--max-wait", type=int, default=540)
    s = sub.add_parser("status"); s.add_argument("slug")
    s = sub.add_parser("summary"); s.add_argument("slug")
    s = sub.add_parser("text"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--delay", type=float, default=2.0, help="seconds between page fetches (minimum 1)")
    s.add_argument("--max-words", type=int, default=800, help="words kept per page (the count is always full)")
    a = ap.parse_args()

    if a.cmd == "status":
        st = read_json(state_path(a.slug), {})
        print(json.dumps({k: v for k, v in st.items() if k != "checkpoints"}, indent=1) if st else "no crawl yet")
        return
    if a.cmd == "summary":
        p, n = build_summary(a.slug)
        print(f"{p.relative_to(client_dir(a.slug).parent.parent)} — {n} pages")
        return
    if a.cmd == "text":
        if a.delay < 1:
            die("a delay below 1 second between page fetches is not polite; minimum is 1.")
        if a.max_words < 50:
            die("--max-words below 50 keeps too little text to be useful.")
        capture_text(a.slug, a.run, a.delay, a.max_words)
        return

    domain = clean_domain(a.domain)
    known = clean_domain(S.load(a.slug)["client"].get("domain") or "")
    if known and domain != known and not a.other_domain:
        die(f"REFUSED — --domain {domain} is not this client's domain ({known}, status.json client.domain). "
            f"Crawl {known}; another domain only on Paul's word, with --other-domain (CR-048).", 4)
    if a.max_pages is not None and not (1 <= a.max_pages <= 100000):
        die("--max-pages must be between 1 and 100000")
    try:
        if a.cmd == "estimate":
            st = read_json(state_path(a.slug), {})
            if st.get("task_id") and st.get("domain") == domain and _fresh(st):
                print(f"RESUME — a crawl of {domain} already exists (task {st['task_id']}, phase "
                      f"{st['phase']}, posted {st['posted_at'][:10]}). Resuming costs nothing.")
                return
            mp, why = choose_max_pages(domain, a.max_pages)
            est, bal = do_estimate(domain, mp, a.mode)
            print(f"Max pages: {mp} — {why}.")
            print(f"Estimate: up to ${est:.4f} for {mp} pages in {a.mode} mode "
                  f"(${dfs.PRICES['on_page/task_post']['per_page'][a.mode]}/page). Balance ${bal:.2f}.")
            print(f"Run with: --max-pages {mp}")
            if est > bal:
                print("STOP — this would exceed the remaining balance. Do not start; tell Paul.")
                sys.exit(6)
            return

        # run
        R.open_run(a.slug, a.run)
        if a.crawl_delay < 1000:
            die("crawl delay below 1000 ms is not polite; minimum is 1000.")
        st = read_json(state_path(a.slug), {})
        reuse = st.get("task_id") and st.get("domain") == domain and _fresh(st) and not a.new_crawl
        if st.get("task_id") and not reuse and not a.new_crawl:
            why = "older than 29 days (results expired)" if not _fresh(st) else f"for {st.get('domain')}"
            die(f"An earlier crawl exists {why}. A new paid crawl needs --new-crawl and Paul's OK.")
        if not reuse:
            if a.new_crawl and st.get("task_id"):
                old = state_path(a.slug)
                old.rename(old.with_name(f"crawl-state-{st['posted_at'][:10]}-{st['task_id'][:8]}.json"))
                for f in (crawl_dir(a.slug) / "raw").glob("*.jsonl"):
                    f.rename(f.with_suffix(f".{st['task_id'][:8]}.old"))
                st = {}
            mp, why = choose_max_pages(domain, a.max_pages)
            print(f"Max pages: {mp} — {why}.")
            post_task(a.slug, a.run, st, domain, mp, a.mode, a.crawl_delay, a.confirmed, why)
        elif (a.max_pages is not None and st["max_pages"] != a.max_pages) or st["mode"] != a.mode:
            note(a.slug, a.run, f"resuming existing task {st['task_id']} ({st['mode']}, max "
                 f"{st['max_pages']}); requested settings ignored — no new charge")
        else:
            note(a.slug, a.run, f"resuming existing task {st['task_id']} at phase '{st['phase']}' — no new charge")

        if st["phase"] == "crawling" and not poll(a.slug, a.run, st, a.max_wait):
            print("STILL CRAWLING — run the same command again to keep waiting (no new charge).")
            sys.exit(10)
        if st["phase"] == "downloading":
            download(a.slug, a.run, st)
        if st["phase"] in ("converting", "converted"):
            convert(a.slug, a.run, st)
        print(f"crawl complete · files in clients/{a.slug}/inputs/crawl/")
    except dfs.DfsError as e:
        die(f"DataforSEO error: {e}. Nothing is lost — run the same command again to resume.", 8)


def _fresh(st):
    try:
        t = datetime.datetime.fromisoformat(st["posted_at"])
        return (datetime.datetime.now(t.tzinfo) - t).days < 29
    except Exception:
        return False


if __name__ == "__main__":
    main()
