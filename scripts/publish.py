#!/usr/bin/env python3
"""publish.py — approved page files → WordPress drafts → a publish handoff to Jonie.

The system NEVER publishes. It generates drafts one-way from the approved SD/LD/... files (the file
stays the source; never edit the draft by hand), and hands publishing to Jonie.

    publish.py wheel  <slug>                          plan the link wheel from the site plan → build/link-wheel.json
    publish.py drafts  <slug> --run R --batch B       one WordPress draft per page in the batch — no handoff yet (CM-055)
    publish.py drafts  <slug> --run R --page P        one approved blog post as a WordPress post draft + its publish handoff
    publish.py handoff <slug> --run R                 once every batch is drafted: ONE living publish handoff to Jonie for
                                                      every service, location, hub, home and about page (CM-055)
    publish.py check   <file>                         placeholders without a [NEED: ...] note (exit 1 if any)
    publish.py blocks  <file>                         print the block markup a file turns into (for checking)
    publish.py pending <slug> --run R                 link-table rows that can now be filled on published pages → handoff

Approved page file format (the writer's output; methodology/specs/README.md):
    ---
    page_id: svc-roof-repair
    url: https://example.com/roof-repair/
    seo_title: Roof Repair - Brand
    meta_description: 150–160 characters ...
    keyword: roof repair                                 (optional; else the site plan's keyword for the page)
    replaces: https://example.com/old-roof-repair/      (optional; comma-separated old URLs)
    ---
    # H1 text
    ...markdown body (H2/H3, paragraphs, lists, tables, FAQ)...
    | [Link wheel: populate service-area links here] |

Drafts: post title = the H1 (the theme shows it as the H1, so the content carries no second H1);
exact slug from the URL; SEOPress title, description, target keyword and social (Open Graph + X, from
the approved title and meta) set on the draft — drafts always carry every field, before and after
the site's pilot; robots and canonical stay at SEOPress defaults; content as Gutenberg
blocks; link-table placeholders filled from the wheel. Rows pointing at pages not yet published
are left out (unless config "wheel_link_unpublished" is true) and handed to Jonie later as a
link-table update once their target is live (publish.py pending).

Publishing as a whole (Paul, 2026-10-09; CM-055): service, location, hub, homepage and about pages are published
together. A batch's ship run only creates its WordPress drafts — publishing never holds up the next batch. Because
every planned page goes live at once, a batch draft's link tables carry every planned page that has a URL (nothing is
held back). When every batch is drafted, `publish.py handoff` writes one living handoff (every page to publish with its
paired redirects, plus the technical blockers already with Jonie, for reference); each `/build published` updates the
same document's status column as Jonie publishes.

Placeholders (CM-016): a draft is refused if it carries a placeholder — a link to "#", "TBD", "till present", an empty
or bracketed href, or TBD / TODO / [Insert …] text — on a line without a visible `[NEED: …]` note.
"""
import argparse
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

import placeholders
import run as R
import status as S
from lib import ROOT, client_dir, config, die, now, require_client_folder, sha12

PLACEHOLDER = re.compile(r"^\|\s*\[Link wheel: populate ([a-z -]+?) links here\]\s*\|\s*$", re.I)
TABLE_KEYS = {"service-area": "service_areas", "service areas": "service_areas", "service": "services",
              "services": "services", "sibling-city": "siblings", "sibling city": "siblings",
              "sibling": "siblings", "related-service": "related", "related service": "related"}


# ------------------------------------------------------------------ the approved file
def parse(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        die(f"{path}: no header block. Approved page files start with --- page_id / url / seo_title / "
            "meta_description --- (methodology/specs/README.md).")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for k in ("page_id", "url", "seo_title", "meta_description"):
        if not meta.get(k):
            die(f"{path}: header is missing {k}")
    body = m.group(2).strip("\n")
    h1 = re.search(r"^# (.+)$", body, re.M)
    if not h1:
        die(f"{path}: no H1 (# ...)")
    meta["h1"] = h1.group(1).strip()
    meta["body"] = body[:h1.start()] + body[h1.end():]
    meta["replaces"] = [u.strip() for u in meta.get("replaces", "").split(",") if u.strip()]
    return meta


def page_files(files):
    """F-026: an approved list may also hold review sheets, CSVs and other non-page files — only a file that starts
    with a page header block (--- … page_id: …) is a page."""
    out = []
    for f in files:
        if "Semantic Review" in f or not str(f).endswith((".md", ".txt")):
            continue
        try:
            head = (ROOT / f).read_text(encoding="utf-8")[:2000]
        except (OSError, UnicodeDecodeError):
            continue
        m = re.match(r"^---\n(.*?)\n---\n", head, re.S)
        if m and re.search(r"^page_id\s*:", m.group(1), re.M):
            out.append(f)
    return out


def slug_of(url):
    path = urllib.parse.urlparse(url).path.strip("/")
    return path.split("/")[-1] if path else ""


# ------------------------------------------------------------------ placeholders (CM-016)
PH_HREF = re.compile(r"^(|#|\.\.\.|…|x+|tb[ad]|todo|link|url|placeholder|till present|n/?a)$", re.I)
PH_HREF_PART = re.compile(r"tbd|todo|placeholder|till present|insert|^[\[<{]", re.I)
PH_TEXT = re.compile(r"\b(TBD|TODO|TBA|XXX)\b|till present|lorem ipsum|\{\{|\[(insert|placeholder|add|link to|url)\b[^\]]*\]", re.I)


def placeholder_problems(text):
    """Every placeholder needs a visible [NEED: …] note on the same line (CM-016; Paul, 2026-10-09). [] when clean."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if re.search(r"\[Link placeholder", line, re.I):   # P11: one form only, so the link-wheel step can find it
            out.append(f"line {n}: inline link placeholder — write it as [LINK → /slug/ · reason]")
            continue
        if "[NEED:" in line or "[LINK →" in line or PLACEHOLDER.match(line.strip()):
            continue
        hrefs = [m.group(1).strip() for m in re.finditer(r"\[[^\]]*\]\(([^)]*)\)", line)]
        hrefs += [m.group(1).strip() for m in re.finditer(r"href=[\"']([^\"']*)[\"']", line, re.I)]
        bad = [h for h in hrefs if PH_HREF.match(h) or PH_HREF_PART.search(h)]
        text_hit = PH_TEXT.search(re.sub(r"\[[^\]]*\]\([^)]*\)", "", line))
        if bad:
            out.append(f"line {n}: placeholder link {', '.join(repr(h) for h in bad)} — add [NEED: <what the link needs>]")
        elif text_hit:
            out.append(f"line {n}: placeholder {text_hit.group(0)!r} — add [NEED: <exactly what is missing>]")
    return out


# ------------------------------------------------------------------ markdown → blocks
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return t


def table_block(rows):
    head, body = rows[0], rows[1:]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return ("<!-- wp:table -->\n<figure class=\"wp-block-table\"><table><thead><tr>" + th +
            "</tr></thead><tbody>" + trs + "</tbody></table></figure>\n<!-- /wp:table -->")


def to_blocks(body, tables=None):
    """Markdown body → Gutenberg block markup. tables: {placeholder key: [(anchor, url), ...]}."""
    tables = tables or {}
    out, lines, i = [], body.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        pm = PLACEHOLDER.match(ln.strip())
        if pm:
            key = TABLE_KEYS.get(pm.group(1).lower().strip(), pm.group(1).lower())
            rows = tables.get(key) or []
            if rows:
                out.append(table_block([["Link"]] + [[f"[{a}]({u})"] for a, u in rows]))
            i += 1; continue
        hm = re.match(r"^(#{2,6}) (.+)$", ln)
        if hm:
            lvl = len(hm.group(1))
            out.append(f'<!-- wp:heading {{"level":{lvl}}} -->\n<h{lvl} class="wp-block-heading">'
                       f"{inline(hm.group(2).strip())}</h{lvl}>\n<!-- /wp:heading -->")
            i += 1; continue
        if ln.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                out.append(table_block(rows))
            continue
        lm = re.match(r"^(\s*)([-*]|\d+\.) (.+)$", ln)
        if lm:
            ordered = lm.group(2)[0].isdigit()
            items = []
            while i < len(lines):
                m2 = re.match(r"^\s*([-*]|\d+\.) (.+)$", lines[i])
                if not m2:
                    break
                items.append(f"<li>{inline(m2.group(2).strip())}</li>"); i += 1
            tag = "ol" if ordered else "ul"
            attrs = ' {"ordered":true}' if ordered else ""
            out.append(f"<!-- wp:list{attrs} -->\n<{tag} class=\"wp-block-list\">" + "".join(items) +
                       f"</{tag}>\n<!-- /wp:list -->")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6} |\s*([-*]|\d+\.) |\s*\|)", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(f"<!-- wp:paragraph -->\n<p>{inline(' '.join(para))}</p>\n<!-- /wp:paragraph -->")
    return "\n\n".join(out)


# ------------------------------------------------------------------ link wheel
def site_pages(st):
    return {pid: p for pid, p in st["pages"].items() if p.get("type") in ("service", "location", "county", "homepage", "about")}


def plan_wheel(st):
    """BB-205/206, CM-005: each service page → every location page; each location page → every
    service page + every other location page. Anchors per the Finish agent's rules."""
    pages = site_pages(st)
    svcs = {k: p for k, p in pages.items() if p["type"] == "service"}
    locs = {k: p for k, p in pages.items() if p["type"] in ("location", "county")}
    main_variant = next((p.get("service_variant") for p in svcs.values() if p.get("service_variant")), None)
    wheel = {}
    for sid, sp in svcs.items():
        sv = sp.get("service_variant") or sp.get("name") or sid
        wheel[sid] = {"service_areas": [(f"{sv} in {lp.get('city') or lp.get('name') or lid}", lp.get("url"), lid)
                                        for lid, lp in locs.items()]}
    for lid, lp in locs.items():
        wheel[lid] = {"services": [(sp.get("h1") or sp.get("service_variant") or sp.get("name") or sid, sp.get("url"), sid)
                                   for sid, sp in svcs.items()],
                      "siblings": [(f"{main_variant or 'Services'} in {op.get('city') or op.get('name') or oid}", op.get("url"), oid)
                                   for oid, op in locs.items() if oid != lid]}
    return wheel


def live_or_batch(st, target, batch_pages):
    p = st["pages"].get(target) or {}
    return target in batch_pages or p.get("state") in ("published", "verified", "written_back") \
        or (p.get("approval") or {}).get("baseline")


def tables_for(st, wheel, pid, batch_pages, together=False):
    """together (CM-055): every planned page goes live in the same publish, so every row with a URL is placed."""
    allow_all = together or config().get("wheel_link_unpublished", False)
    tables, pending = {}, []
    for key, rows in (wheel.get(pid) or {}).items():
        keep = []
        for anchor, url, target in rows:
            if not url:
                pending.append((key, anchor, None, target)); continue
            if allow_all or live_or_batch(st, target, batch_pages):
                keep.append((anchor, url))
            else:
                pending.append((key, anchor, url, target))
        tables[key] = keep
    return tables, pending


# ------------------------------------------------------------------ commands
def cmd_wheel(a):
    st = S.load(a.slug)
    wheel = plan_wheel(st)
    p = client_dir(a.slug) / "build" / "link-wheel.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(wheel, indent=1))
    print(f"link wheel planned for {len(wheel)} pages → {p.relative_to(ROOT)}")


def load_wheel(slug):
    p = client_dir(slug) / "build" / "link-wheel.json"
    if not p.exists():
        die("No link wheel yet — run publish.py wheel <slug> (it is planned from the approved site plan).")
    return json.loads(p.read_text())


def cmd_drafts(a):
    import handoff
    import wp
    R.open_run(a.slug, a.run)
    st = S.load(a.slug)
    ok, why = S.condition_met(st, "wordpress_connected")
    if not ok:
        die(f"REFUSED — {why}", 4)
    if a.page:
        ok, why = S.page_approved(st, a.page)
        if not ok:
            die(f"REFUSED — {why}", 4)
        f = (st["pages"][a.page].get("approval") or {}).get("file") or st["pages"][a.page].get("file")
        b = {"pages": [a.page], "files": {"drafts": [f]}}
        wheel = {}
    else:
        b = S.batch(st, a.batch) or die(f"no batch {a.batch}")
        ok, why = S.batch_stage_ok(st, a.batch, "drafts")
        if not ok:
            die(f"REFUSED — {why}", 4)
        wheel = load_wheel(a.slug)
    files = page_files((b.get("files") or {}).get("drafts", []))
    by_page, bad = {}, []
    for f in files:
        m = parse(f)
        by_page[m["page_id"]] = (f, m)
        bad += [f"{Path(f).name}: {x}" for x in placeholder_problems((ROOT / f).read_text(encoding="utf-8"))]
        bad += S.slug_problems(m["url"], (st["pages"].get(m["page_id"]) or {}).get("type"))
    if bad:
        die("REFUSED — nothing was sent to WordPress:\n  - " + "\n  - ".join(bad), 4)
    missing = [p for p in b["pages"] if p not in by_page]
    if missing:
        die(f"approved files for pages {', '.join(missing)} not found in the batch's drafts approval")
    rows_pub, rows_redirect, pend_all = [], [], {}
    for pid in b["pages"]:
        f, m = by_page[pid]
        tables, pending = tables_for(st, wheel, pid, b["pages"], together=not a.page)
        content = to_blocks(m["body"], tables)
        # P7: every old URL this page replaces gets its 301 next to its publish — from the file's header and from the
        # site plan / migration (status.json pages → replaces), never only one of them
        m["replaces"] = sorted({u for u in (m.get("replaces") or []) + ((st["pages"].get(pid) or {}).get("replaces") or [])
                                if u and u.rstrip("/") != m["url"].rstrip("/")})
        # P11: every open placeholder is a visible notice at the top of the draft and a row for Jonie
        open_items = placeholders.scan(ROOT / f)
        if open_items:
            content = placeholders.notice_block(open_items) + "\n\n" + content
        slug_name = slug_of(m["url"])
        existing = None
        try:
            existing = wp.find(a.slug, m["url"])
        except Exception:
            existing = None
        in_place = bool(existing and existing[1].get("status") == "publish" and slug_name)
        ptype = "posts" if st["pages"].get(pid, {}).get("type") == "blog" else "pages"
        keyword = m.get("keyword") or st["pages"].get(pid, {}).get("keyword") or ""
        body = {"slug": (slug_name + "-new") if in_place else slug_name}
        d = wp.new_draft(a.slug, ptype, m["h1"], content, body["slug"],
                         {"title": m["seo_title"], "description": m["meta_description"], "keyword": keyword})
        R.log_change(a.slug, a.run, "page_content", d.get("link", ""), f"new draft {ptype[:-1]}", "(none)",
                     f"draft id {d['id']} ({ptype}) · from {f} sha {sha12(ROOT / f)} · slug {body['slug']}",
                     "APPLIED · draft only (not live) · generated from the approved file", ref=pid, channel="wp")
        page = st["pages"].setdefault(pid, {})
        placed = {TABLE_KEYS.get(x.group(1).lower().strip(), x.group(1).lower())
                  for x in (PLACEHOLDER.match(l.strip()) for l in m["body"].split("\n")) if x}
        how = (f"Replace the content of the live page at {m['url']} with this draft's blocks (keep that URL), "
               "then trash the draft" if in_place else f"Publish at exactly {m['url']}")
        page.update({"wp_id": d["id"], "wp_type": ptype, "url": m["url"], "file": f, "state": "drafted",
                     "open_items": [{"line": i["line"], "text": i["text"]} for i in open_items],
                     "links_placed": [u for k, rows in tables.items() if k in placed for _, u in rows],
                     "publish": {"draft_link": d.get("link", ""), "how": how, "replaces": m["replaces"]}})
        pending = [x for x in pending if x[0] in placed]
        rows_pub.append({"url": d.get("link", ""), "field": "publish", "old": "(draft)", "new": m["url"],
                         "reason": how, "decision_map_ref": pid})
        for old in m["replaces"]:
            rows_redirect.append({"url": old, "field": "301", "old": old, "new": m["url"],
                                  "reason": f"replaced by {pid} — do it together with the publish", "decision_map_ref": pid})
        if pending:
            pend_all[pid] = pending
    if a.batch:   # CM-055: drafts only — the one living publish handoff comes once every batch is drafted
        S.set_batch_state(st, b, "drafted")
        st.setdefault("wheel_pending", {}).update({k: v for k, v in pend_all.items()})
        S.save(a.slug, st)
        print(f"{len(rows_pub)} drafts created for batch {a.batch} · nothing handed to Jonie yet — every service and "
              "location page is published together from one living handoff once all batches are drafted (CM-055)")
        return
    S.save(a.slug, st)
    tmp = client_dir(a.slug) / "handoffs" / f"_publish-{a.batch or a.page}.csv"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    import csv
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["url", "field", "old", "new", "reason", "decision_map_ref"])
        w.writeheader(); w.writerows(rows_pub + rows_redirect)
    sys.argv = ["handoff.py", "create", a.slug, "--run", a.run, "--kind", "publish", "--items", str(tmp.relative_to(ROOT)),
                "--title", f"{st['client']['name']} - Publish Handoff - " + (f"batch {a.batch}" if a.batch else a.page)]
    handoff.main()
    tmp.unlink()
    st = S.load(a.slug)
    hs = sorted((client_dir(a.slug) / "handoffs").glob("H-*-publish.csv"), key=lambda p: p.stat().st_mtime)
    if hs and a.batch:
        S.batch(st, a.batch)["handoff"] = hs[-1].stem
    elif hs:
        st["pages"][a.page]["handoff"] = hs[-1].stem
    st.setdefault("wheel_pending", {}).update({k: v for k, v in pend_all.items()})
    S.save(a.slug, st)
    print(f"{len(rows_pub)} drafts created · {len(rows_redirect)} paired redirect(s) · "
          f"{sum(len(v) for v in pend_all.values())} link row(s) waiting for their target to go live")


CORE = ("service", "location", "county")


def ship_ready(st):
    """(ok, why, batch ids to ship) — P9: services and locations ship as a whole. Every service and location batch
    (the pilot included) must have its drafts approved and its Brand Guide write-back done; homepage and about batches
    ship with them when approved, otherwise later as a worklist addition."""
    todo, missing = [], []
    for b in S.batches(st):
        if b.get("state") in S.DRAFTED_OR_LATER or (b.get("drafts") or {}).get("baseline"):
            continue
        approved = S.check(st, f"batch:{b['id']}:drafts")[0]
        core = b.get("kind") in CORE or b["id"] == "pilot"
        if approved and (b.get("content_written_back") or not core):
            todo.append(b["id"])
        elif core:
            missing.append(f"{b['id']} ({'Brand Guide write-back not done' if approved else 'drafts not approved yet'})")
    if missing:
        return False, "every service and location page ships together — still waiting for: " + ", ".join(missing), todo
    return bool(todo), ("" if todo else "nothing left to ship"), todo


def cmd_drafts_all(a):
    """P9: one run creates the WordPress draft of every approved page; link tables are complete, because every target
    exists as a draft with its final URL."""
    R.open_run(a.slug, a.run)
    st = S.load(a.slug)
    ok, why, todo = ship_ready(st)
    if not ok:
        die(f"REFUSED — {why}", 4)
    for bid in todo:
        a.batch = bid
        cmd_drafts(a)
    a.batch = None
    print(f"shipped {len(todo)} batch(es) as WordPress drafts in one run: {', '.join(todo)} — next, the one VA Worklist "
          "handover (/build <slug> handoff)")


def cmd_handoff(a):
    """CM-055: one living publish handoff for every drafted page, once every batch is drafted."""
    import csv
    import handoff
    R.open_run(a.slug, a.run)
    st = S.load(a.slug)
    ok, why = S.condition_met(st, "pages_drafted")
    if not ok:
        die(f"REFUSED — not every page is a WordPress draft yet: {why}. Pages are published together (CM-055).", 4)
    todo = [b for b in S.batches(st) if b.get("state") == "drafted"]
    if not todo:
        die("nothing to hand off — every drafted batch is already in the living publish handoff "
            f"({(st.get('publish_handoff') or {}).get('id')})")
    rows = []
    for b in todo:
        for pid in b["pages"]:
            p = st["pages"][pid]
            pub = p.get("publish") or {}
            rows.append({"url": pub.get("draft_link", ""), "field": "publish", "old": "(draft)", "new": p["url"],
                         "reason": pub.get("how") or f"Publish at exactly {p['url']}", "decision_map_ref": pid})
            rows += [{"url": old, "field": "301", "old": old, "new": p["url"],
                      "reason": f"replaced by {pid} — do it together with the publish", "decision_map_ref": pid}
                     for old in pub.get("replaces") or []]
            rows += [{"url": pub.get("draft_link", ""), "field": "open item", "old": i["text"],
                      "new": placeholders.instruction(i["text"]),
                      "reason": f"approved file line {i['line']}: resolve before publishing — do not publish {p['url']} "
                                "while its 'Open items' notice is on the page (P11)", "decision_map_ref": pid}
                     for i in p.get("open_items") or []]
    d = client_dir(a.slug) / "handoffs"
    pre = ["## Technical blockers (already sent — listed here so this is the one place to look)", ""]
    for hid in st.get("blocker_handoffs") or []:
        f = d / f"{hid}.csv"
        br = list(csv.DictReader(open(f, newline="", encoding="utf-8-sig"))) if f.exists() else []
        left = [r for r in br if r.get("status") not in ("done", "verified")]
        pre.append(f"- **{hid}** — {len(br) - len(left)} of {len(br)} done" + (": still open " + ", ".join(
            f"{r['ref']} ({r['field']} {r['url']})" for r in left[:8]) if left else ""))
    if len(pre) == 2:
        pre.append("- none" if st.get("blockers_none") else "- the blocker checklist has not been handed over yet")
    pre += ["", "## Publish — every page together",
            "", "Publish **all** rows in one go (they link to each other), each with the redirects listed under it. "
            "This document is updated each time you return the worksheet: the Status column shows what is done.", ""]
    tmp, prf = d / "_publish-all.csv", d / "_publish-all-preface.md"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["url", "field", "old", "new", "reason", "decision_map_ref"])
        w.writeheader(); w.writerows(rows)
    prf.write_text("\n".join(pre) + "\n")
    sys.argv = ["handoff.py", "create", a.slug, "--run", a.run, "--kind", "publish", "--items", str(tmp.relative_to(ROOT)),
                "--preface", str(prf.relative_to(ROOT)),
                "--title", f"{st['client']['name']} - Publish Handoff - all pages (living document)"]
    handoff.main()
    tmp.unlink(); prf.unlink()
    hid = sorted(d.glob("H-*-publish.csv"), key=lambda x: x.stat().st_mtime)[-1].stem
    st = S.load(a.slug)
    for b in S.batches(st):
        if b.get("state") == "drafted":
            S.set_batch_state(st, b, "handed_off")
            b["handoff"] = hid
    st["publish_handoff"] = {"id": hid, "at": now(), "run": a.run,
                             "batches": [b["id"] for b in todo]}
    S.save(a.slug, st)
    print(f"{hid}: one living publish handoff for {sum(len(b['pages']) for b in todo)} page(s) in "
          f"{len(todo)} batch(es) → Jonie publishes them together")


def cmd_pending(a):
    """Rows held back because their target was not live: hand to Jonie once it is."""
    import csv
    import handoff
    R.open_run(a.slug, a.run)
    st = S.load(a.slug)
    rows, keep = [], {}
    for pid, items in (st.get("wheel_pending") or {}).items():
        page = st["pages"].get(pid) or {}
        still = []
        for key, anchor, url, target in items:
            tp = st["pages"].get(target) or {}
            if url and page.get("state") in ("published", "verified", "written_back") and \
                    tp.get("state") in ("published", "verified", "written_back"):
                rows.append({"url": page.get("url"), "field": f"link table: {key}", "old": "(row missing)",
                             "new": f"{anchor} → {url}", "reason": "target page is now live (link wheel, BB-205)",
                             "decision_map_ref": pid})
            else:
                still.append([key, anchor, url, target])
        if still:
            keep[pid] = still
    if not rows:
        print("no held link rows are ready yet"); return
    tmp = client_dir(a.slug) / "handoffs" / "_wheel-update.csv"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["url", "field", "old", "new", "reason", "decision_map_ref"])
        w.writeheader(); w.writerows(rows)
    sys.argv = ["handoff.py", "create", a.slug, "--run", a.run, "--kind", "link_table", "--items", str(tmp.relative_to(ROOT))]
    handoff.main()
    tmp.unlink()
    st = S.load(a.slug); st["wheel_pending"] = keep; S.save(a.slug, st)
    print(f"{len(rows)} link row(s) handed to Jonie")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("wheel"); s.add_argument("slug")
    s = sub.add_parser("drafts"); s.add_argument("slug"); s.add_argument("--run", required=True)
    g = s.add_mutually_exclusive_group(); g.add_argument("--batch"); g.add_argument("--page")
    g.add_argument("--all", action="store_true", help="the default: every approved page in one run (P9)")
    s = sub.add_parser("blocks"); s.add_argument("file")
    s = sub.add_parser("check"); s.add_argument("file")
    s = sub.add_parser("handoff"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s = sub.add_parser("pending"); s.add_argument("slug"); s.add_argument("--run", required=True)
    a = ap.parse_args()
    if getattr(a, "slug", None):
        require_client_folder(a.slug)   # §00: never client work in the main folder
    if a.cmd == "wheel":
        cmd_wheel(a)
    elif a.cmd == "drafts":
        if a.batch or a.page:
            cmd_drafts(a)
        else:
            cmd_drafts_all(a)
    elif a.cmd == "pending":
        cmd_pending(a)
    elif a.cmd == "handoff":
        cmd_handoff(a)
    elif a.cmd == "check":
        bad = placeholder_problems((ROOT / a.file).read_text(encoding="utf-8"))
        print("\n".join(bad) or "no placeholders without a [NEED: ...] note")
        sys.exit(1 if bad else 0)
    else:
        m = parse(a.file)
        print(to_blocks(m["body"]))


if __name__ == "__main__":
    main()
