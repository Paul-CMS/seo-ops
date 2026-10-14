#!/usr/bin/env python3
"""worklist.py — one living VA Worklist per client (rewrite 2 P9, Q8; rewrite 3 §7a: accurate and detailed).

    worklist.py build <slug>                         regenerate clients/<slug>/handoffs/VA-WORKLIST.csv and .md
    worklist.py check <slug> [--report-only]         the validator: refuses a handover on any error (exit 4)
    worklist.py supersede <slug> <ref> --by <ref|none> --reason R   mark a row replaced by a newer decision

Every item the system hands to a person is a row of ONE worklist — the document Jonie and Gwen work from (copied to
Drive as "<Client> - VA Worklist.md" and ".csv"). Every row is correct and complete on its own:
  id · section · task · where (live URL + WordPress edit link) · how (numbered steps) · values (exactly what to enter)
  · depends_on (row ids first) · done_check · owner · source · status (open | done | superseded) — plus blocked and
  deviated, which only a VA's return sets. Sections, in order:
  1 Setup · 2 Blockers · 3 Redirects · 4 Publish · 5 After publish · 6 Manual lookups.
Sections 1, 2 and 6 can go to the VA at any time (they block nothing). Sections 3–5 are handed over ONCE, when every
service and location page is a WordPress draft (`/build <slug> handoff`); until then the worklist says so.
Nothing is overwritten: rows are appended; a row a newer decision replaced is marked `superseded`, never left open.
The VA ticks `status` (done | blocked | deviated) and adds a `note`, then returns the CSV: `handoff.py ingest`.
/verify checks every done row against its done_check; a row whose check fails comes back as open, with the reason.

The validator (`check`, no agent, no spend) runs before any handover and the Drive copy of the worklist depends on it:
  publish rows   match a real WordPress draft (id), the approved file (sha) and the approved site-plan URL; no page is
                 missing and none appears twice; title and meta lengths are within the spec
  redirect rows  the old URL resolves (or is recorded as already gone); the target is a planned page with a draft; no
                 chains, no loops, no two rows for one old URL; each depends on its target's publish row
  placeholders   every page with an open-item notice has a matching row and every such row points at a page that still
                 has the notice
  links          link-table rows waiting on another page are listed in section 5; a pair now live is flagged
  superseded     a redirect whose target is no longer a planned page is stale: mark it superseded
  every row      has where, how and done_check
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import status as S
from lib import ROOT, client_dir, config, now, sha12, today, write_json

SECTIONS = {1: "Setup", 2: "Blockers", 3: "Redirects", 4: "Publish", 5: "After publish", 6: "Manual lookups"}
COLS = ["section", "ref", "owner", "added", "kind", "url", "field", "old", "new", "reason", "decision_map_ref", "status",
        "note"]
OUT_COLS = ["id", "section", "task", "where", "how", "values", "depends_on", "done_check", "owner", "source", "status",
            "ref", "added", "kind", "url", "field", "old", "new", "reason", "decision_map_ref", "note"]
HFILE = re.compile(r"^(H-(\d{4}-\d{2}-\d{2})-\d+-([a-z_]+))\.csv$")
LIVE_STATES = ("published", "verified", "written_back")
REDIRECT_OK = (200, 301, 302, 307, 308)
GUIDE = {
    1: "Set up the site for the system (the seo-ops Editor user, read-only SEOPress checks). Change nothing else.",
    2: "Technical blockers. Fix each one as written; check the current value first. These never stop page writing.",
    3: "301 redirects in SEOPress → Redirections, From URL → To URL exactly as written. Never delete the old page.",
    4: "Every page in this section is a WordPress **draft** made from its approved file. Publish **all of them together** "
       "(they link to each other): apply the Kadence layout and styling, add images, publish at exactly the URL in "
       "`values`, and add each `301` row listed for that page at the same time. Do NOT change wording, headings, title, "
       "meta, keyword or URL (an unavoidable change: mark `deviated` and say why). A page with an **open item** row, or "
       "an 'Open items on this page' notice, is not published until that row is resolved.",
    5: "After the pages are live: menus, link-table additions, alt text. Change nothing else on the page.",
    6: "Manual lookups and records (Gwen). Record what you find in `note`.",
}


def section_of(kind, hid, st):
    if hid in (st.get("blocker_handoffs") or []):
        return 2
    if kind in ("wp_setup", "seopress_settings"):
        return 1
    if kind in ("redirect", "slug", "consolidation"):
        return 3
    if kind == "publish":
        return 4
    owner = (S.GATES["change_kinds"].get(kind) or {}).get("owner", "Gwen")
    return 6 if owner == "Gwen" else 5


def read_csv(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def rows(slug):
    """Every row of every group record, with its section, owner and date added (in the order they were added)."""
    st = S.load(slug)
    d = client_dir(slug) / "handoffs"
    out = []
    for f in sorted(d.glob("H-*.csv")) if d.exists() else []:
        m = HFILE.match(f.name)
        if not m:
            continue
        hid, added, kind = m.group(1), m.group(2), m.group(3)
        md = f.with_suffix(".md")
        who = re.search(r"\*\*For:\*\* (\w+)", md.read_text()) if md.exists() else None
        owner = who.group(1) if who else (S.GATES["change_kinds"].get(kind) or {}).get("owner", "Gwen")
        sec0 = section_of(kind, hid, st)
        for r in read_csv(f):
            sec = 3 if r.get("field", "").lower().startswith("clear the slug") else sec0   # §7a: slug changes precede publishing
            out.append({"section": sec, "ref": r["ref"], "owner": owner, "added": added, "kind": kind,
                        **{k: r.get(k, "") for k in COLS[5:]}, "_hid": hid})
    return out


def handed_over(st):
    return bool(st.get("publish_handoff"))


# ------------------------------------------------------------------ the new fields
def superseded(slug):
    p = client_dir(slug) / "handoffs" / "worklist-superseded.json"
    return json.loads(p.read_text()) if p.exists() else {}


def norm_url(u):
    return (u or "").strip().rstrip("/").lower()


def slug_of(u):
    return urllib.parse.urlparse(u or "").path.strip("/").split("/")[-1]


def header(path):
    """The approved page file's header block as a dict ({} when the file or block is missing)."""
    try:
        t = (ROOT / path).read_text(encoding="utf-8")
    except (OSError, TypeError, UnicodeDecodeError):
        return {}
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


VA_TASK = re.compile(r"\[Map\b|map embed|\bembed\b|\bimage\b|\balt text\b|\bupload\b|\bmenu\b|\bredirect\b|\bplugin\b", re.I)


def open_item_owner(text):
    """§7a (e): who resolves an open item. Jonie only for a VA task (a map embed, images, menus …); a proposed link
    ([LINK → …]) and every missing fact, client answer or cited source is Paul's — the system's researcher looks up public
    facts first. Never Jonie by default."""
    return "Jonie" if VA_TASK.search(text or "") else "Paul"


def derived(c):
    """{ref: {by, reason}} — rows a recorded plan already makes pointless, so they are superseded, never left open:
    (a) a row that acts on a URL a planned page replaces (a link fix to /metal-roofing-2/ when the page moves to
        /metal-roofing/; an SEO title for the old URL) — the 301 and publish rows do the job;
    (d) an SEO title or meta row for a page shipped from its approved draft — the publish row carries both values."""
    out = {}
    replaced = {}
    for pid, p in c.st["pages"].items():
        for u in list(p.get("replaces") or []) + list((p.get("publish") or {}).get("replaces") or []):
            replaced[norm_url(u)] = pid
    shipped = {norm_url(c.st["pages"][pid].get("url")): pid for pid in c.pub}
    for r in c.raw:
        if r["ref"] in c.sup or r["field"] in ("301", "publish", "open item") or r["field"].startswith("link table"):
            continue
        hit = replaced.get(norm_url(r["new"])) or replaced.get(norm_url(r["url"]))
        if hit:
            by = c.pub.get(hit, "")
            out[r["ref"]] = {"by": by, "reason": f"derived: it acts on {r['new'] if norm_url(r['new']) in replaced else r['url']}, "
                                                 f"which the approved plan replaces with {c.st['pages'][hit].get('url')} "
                                                 f"(the publish row and its 301 do this)"}
            continue
        if re.search(r"title|meta", r["field"], re.I) and norm_url(r["url"]) in shipped:
            pid = shipped[norm_url(r["url"])]
            out[r["ref"]] = {"by": c.pub[pid], "reason": f"derived: the page is shipped from its approved draft, whose title and meta "
                                                         f"description are in the publish row {c.pub[pid]}"}
    return out


class Ctx:
    """What enrichment needs about the whole client, computed once."""

    def __init__(self, slug):
        self.slug = slug
        self.st = S.load(slug)
        self.sup = superseded(slug)
        self.base = self.st["client"].get("domain") or ""
        if self.base and not self.base.startswith("http"):
            self.base = "https://" + self.base
        self.raw = rows(slug)
        self.by_url = {norm_url(p.get("url")): pid for pid, p in self.st["pages"].items() if p.get("url")}
        self.pub = {}   # page id -> its publish row ref (not superseded)
        for r in self.raw:
            if r["field"] == "publish" and r["decision_map_ref"] in self.st["pages"] and r["ref"] not in self.sup:
                self.pub[r["decision_map_ref"]] = r["ref"]

    def edit_link(self, r, page):
        m = re.search(r"page_id=(\d+)|post=(\d+)", r.get("url") or "")
        post = page.get("wp_id") or (m.group(1) or m.group(2) if m else None)
        return f"{self.base}/wp-admin/post.php?post={post}&action=edit" if post and self.base else ""


def enrich(r, c):
    """The fields every row carries (§7a), from the group record and the client's state."""
    st, field, kind = c.st, r["field"], r["kind"]
    pid = r["decision_map_ref"] if r["decision_map_ref"] in st["pages"] else None
    page = st["pages"].get(pid) or {}
    live = page.get("url") or ""
    edit = c.edit_link(r, page)
    hdr = header(page.get("file")) if pid else {}
    name = page.get("name") or pid or ""
    steps, task, values, check = [], "", "", ""
    if field == "publish":
        slug = slug_of(r["new"])
        task = f"Publish the {name} page"
        where = " · ".join(x for x in (r["new"], f"edit: {edit}" if edit else "") if x)
        values = (f"slug: {slug} · URL: {r['new']} · SEOPress title: {hdr.get('seo_title', '[see the approved file]')} · "
                  f"meta description: {hdr.get('meta_description', '[see the approved file]')}")
        steps = [f"Open the draft: {edit or r['url']}.", "Check that no 'open item' row for this page is still open "
                 "(and that the page has no 'Open items on this page' notice).",
                 "Apply the Kadence layout and styling; add the images. Do not change wording, headings, title, meta or keyword.",
                 f"Set the slug to '{slug}' and publish so the page lives at {r['new']} (keep that URL).",
                 "Add each 301 redirect row listed for this page at the same time.", "Tick this row done."]
        check = f"{r['new']} loads (200), is published (not a draft), and its page source shows the title above."
    elif field == "open item":
        owner = open_item_owner(r["old"])
        task = f"Resolve the open item on the {name} page before it is published" + ("" if owner == "Jonie" else f" ({owner} decides)")
        where = " · ".join(x for x in (live, f"edit: {edit}" if edit else "") if x)
        values = r["new"] or r["old"]
        steps = ([f"Open the draft: {edit or r['url']} and find the line: {r['old'][:120]}", "Do what 'values' says.",
                  "Replace the line with the result and remove the 'Open items on this page' notice once none are left.",
                  "Tick this row done."] if owner == "Jonie" else
                 [f"The line on the draft: {r['old'][:120]}", "Not a VA task: Paul supplies the answer or decision (the system's "
                  "researcher looks up public facts first). Nothing to do here until it is settled.",
                  "The page is revised in the next run and this row is then closed."])
        check = "The draft no longer contains that [NEED: …] line."
    elif field == "301":
        task = f"Add a 301 redirect from {r['url'] if kind != 'slug' else r['old']} to {r['new']}"
        where = f"SEOPress → Redirections on {c.base or 'the site'} · old URL: {r['url']}"
        values = f"from: {r['url'] if kind != 'slug' else r['old']} → to: {r['new']} · type: 301"
        steps = ["In WordPress open SEOPress → Redirections → Add redirection.",
                 f"From: {r['url'] if kind != 'slug' else r['old']} (exactly).", f"To: {r['new']} (exactly). Type 301, enabled.",
                 "Save. Never delete the old page.", "Tick this row done."]
        check = f"Opening {r['url'] if kind != 'slug' else r['old']} returns 301 to {r['new']}, and the target loads (200)."
    elif field.startswith("link table"):
        task = f"Add a link-table row on the {name} page ({field.split(':', 1)[-1].strip()})"
        where = " · ".join(x for x in (live, f"edit: {edit}" if edit else "") if x)
        values = r["new"]
        steps = [f"Open {edit or live}.", "Find the link table named in 'task'.", f"Add the row exactly as in 'values': {r['new']}.",
                 "Update the page and tick this row done."]
        check = f"{live} shows the link in that table."
    elif "title" in field.lower() or field.lower().startswith("seopress"):
        task = f"Set the {field} on {r['url']}"
        where = " · ".join(x for x in (r["url"], f"edit: {edit}" if edit else "") if x)
        values = r["new"]
        steps = [f"Open {edit or r['url']}.", f"In SEOPress, set '{field}' to exactly the value in 'values'.", "Update the page.",
                 "Tick this row done."]
        check = f"The page source of {r['url']} shows '{r['new'][:80]}'."
    elif "link" in field.lower():
        task = f"Fix the link on {r['url']}"
        where = " · ".join(x for x in (r["url"], f"edit: {edit}" if edit else "") if x)
        values = f"replace {r['old']} with {r['new']}"
        steps = [f"Open {edit or r['url']}.", f"Find the link to {r['old']}.", f"Change it to {r['new']}.", "Update the page.",
                 "Tick this row done."]
        check = f"{r['url']} no longer links to {r['old']}."
    elif kind == "manual_lookup":
        task = f"Look up: {field}"
        where = r["url"] or "see 'how'"
        values = r["new"] or "record what you find in note"
        steps = [f"Look up '{field}' as the reason says: {r['reason'][:160]}", "Record exactly what you found in `note`.",
                 "Tick this row done."]
        check = "`note` holds what you found, with where you found it."
    else:
        task = f"{kind.replace('_', ' ').capitalize()}: {field}"
        where = " · ".join(x for x in (r["url"], f"edit: {edit}" if edit else "") if x)
        values = r["new"] or "—"
        steps = [f"Open {edit or r['url'] or 'the place named in where'}.", f"Check the current value first ('old': {r['old'][:80]}). "
                 "Already done → mark done and say so.", f"Make the change: {r['new'][:160] or r['reason'][:160]}.",
                 "Tick this row done; note anything unexpected."]
        check = f"The change is visible at {r['url'] or 'the place named in where'}."
    dep = []
    if field == "publish":
        dep = [x["ref"] for x in c.raw if x["field"] == "open item" and x["decision_map_ref"] == r["decision_map_ref"]
               and x["ref"] not in c.sup]
        dep += [x["ref"] for x in c.raw if x["field"].lower().startswith("clear the slug") and x["ref"] not in c.sup
                and norm_url(x["url"]) == norm_url(r["new"])]   # §7a (b): clear the slug → publish → 301 from the old URL
    elif field == "301":
        tp = c.by_url.get(norm_url(r["new"]))
        dep = [c.pub[tp]] if tp in c.pub else []
    elif r["section"] == 5:
        pids = {pid} | {c.by_url.get(norm_url(u)) for u in re.findall(r"https?://[^\s,)]+", r["new"] or "")}
        dep = [c.pub[p] for p in sorted(x for x in pids if x in c.pub)]
    src = " · ".join(x for x in (f"{r['_hid']}.csv", Path(page.get("file") or "").name) if x)
    status = (r.get("status") or "").strip()
    note = r.get("note", "")
    if r["ref"] in c.sup:
        by = c.sup[r["ref"]].get("by")
        status, note = "superseded", f"replaced by {by}" if by else "superseded — no replacement"
        if c.sup[r["ref"]].get("reason"):
            note += f" ({c.sup[r['ref']]['reason']})"
    elif status in ("", "issued"):
        status = "open"
    elif status == "verified":
        status = "done"
    if field == "open item":
        r = {**r, "owner": open_item_owner(r["old"])}
    return {**r, "id": r["ref"], "task": task, "where": where, "how": " ".join(f"{i}. {s}" for i, s in enumerate(steps, 1)),
            "values": values, "depends_on": ", ".join(dep), "done_check": check, "source": src, "status": status, "note": note}


def waiting_rows(c):
    """Section 5 rows for link-table rows held back because their target is not live yet (removed once both pages
    are published and `publish.py pending` hands the real rows over)."""
    out = []
    for pid, items in sorted((c.st.get("wheel_pending") or {}).items()):
        page = c.st["pages"].get(pid) or {}
        for i, (key, anchor, url, target) in enumerate(items, 1):
            tp = c.st["pages"].get(target) or {}
            if page.get("state") in LIVE_STATES and tp.get("state") in LIVE_STATES:
                continue
            dep = [c.pub[x] for x in (pid, target) if x in c.pub]
            ref = f"WAIT-{pid}-{i}"
            out.append({"section": 5, "ref": ref, "owner": "Jonie", "added": today(), "kind": "link_table", "url": page.get("url", ""),
                        "field": f"link table: {key}", "old": "(row missing)", "new": f"{anchor} → {url}",
                        "reason": f"waits for {target} to be published (link wheel, BB-205)", "decision_map_ref": pid,
                        "status": "", "note": "", "_hid": "wheel_pending", "_dep": dep})
    return out


def full_rows(slug):
    c = Ctx(slug)
    out = [enrich(r, c) for r in c.raw]
    for w in waiting_rows(c):
        e = enrich(w, c)
        e["depends_on"] = ", ".join(w["_dep"])
        e["how"] = "1. Do nothing yet — this row waits for the pages in 'depends_on' to be published. 2. When both are live " \
                   "the system hands over the real row; this row then disappears."
        e["done_check"] = "Not a task yet."
        out.append(e)
    return out, c


# ------------------------------------------------------------------ the validator
def fetch(url):
    """HTTP status of the URL without following redirects; None when it cannot be reached. Tests replace this."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    req = urllib.request.Request(url, headers={"User-Agent": "seo-ops-worklist/1.0"}, method="HEAD")
    try:
        return urllib.request.build_opener(NoRedirect).open(req, timeout=20).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:  # noqa: BLE001
        return None


def problems(slug):
    """([(row id or '-', rule, message)] errors, [warnings]) — what keeps this worklist from being handed over."""
    rs, c = full_rows(slug)
    st = c.st
    live_rows = [r for r in rs if r["status"] != "superseded"]
    err, warn = [], []
    over = handed_over(st)
    cfg = config()
    tmax = int(cfg.get("worklist_title_max_chars") or 70)
    mlo, mhi = cfg.get("worklist_meta_chars") or [150, 160]
    pubs = [r for r in live_rows if r["field"] == "publish"]
    seen = {}
    for r in pubs:
        pid = r["decision_map_ref"]
        page = st["pages"].get(pid)
        if not page:
            err.append((r["id"], "publish", f"page {pid!r} is not in the site plan"))
            continue
        if pid in seen:
            err.append((r["id"], "publish", f"{pid} appears twice ({seen[pid]} and {r['id']})"))
        seen[pid] = r["id"]
        wid = str(page.get("wp_id") or "")
        if not wid or not re.search(rf"(page_id|post)={wid}\b", r["url"]):
            err.append((r["id"], "publish", f"the row's draft link {r['url']!r} is not the WordPress draft of {pid} (id {wid or 'none'})"))
        if norm_url(r["new"]) != norm_url(page.get("url")) or slug_of(r["new"]) != slug_of(page.get("url")):
            err.append((r["id"], "publish", f"slug/URL {r['new']!r} is not the approved site-plan URL {page.get('url')!r}"))
        b = next((x for x in S.batches(st) if pid in x.get("pages", [])), None) or {}
        approved = ((b.get("drafts") or {}).get("files") or {}).get(page.get("file"))   # the sha Paul approved
        if approved and (ROOT / page["file"]).is_file() and sha12(ROOT / page["file"]) != approved:
            err.append((r["id"], "values", f"the approved draft {Path(page['file']).name} changed since Paul approved it"))
        h = header(page.get("file"))
        t, m = h.get("seo_title", ""), h.get("meta_description", "")
        if t and len(t) > tmax:   # the spec says "never truncated" but sets no number: a warning, not a refusal
            warn.append(f"{r['id']}: SEO title is {len(t)} characters — over {tmax}, it may truncate in search results")
        if m and not (mlo <= len(m) <= mhi):
            err.append((r["id"], "values", f"meta description is {len(m)} characters (spec: {mlo}–{mhi})"))
    if over:
        for pid, p in st["pages"].items():
            if p.get("type") in ("service", "location", "county") and p.get("wp_id") and p.get("state") not in LIVE_STATES \
                    and pid not in seen:
                err.append(("-", "publish", f"{pid} ({p.get('url')}) is a draft with no publish row"))
    old_urls, targets = {}, {}
    for r in live_rows:
        if r["field"] != "301":
            continue
        old = r["old"] if r["kind"] == "slug" else r["url"]
        if norm_url(old) in old_urls:
            err.append((r["id"], "redirect", f"{old} is redirected by two rows ({old_urls[norm_url(old)]} and {r['id']})"))
        old_urls[norm_url(old)] = r["id"]
        targets[r["id"]] = (norm_url(old), norm_url(r["new"]))
    for r in live_rows:
        if r["field"] != "301":
            continue
        old, new = targets[r["id"]]
        gone = re.search(r"404|410|gone|no redirect", r["old"], re.I)
        code = fetch(r["old"] if r["kind"] == "slug" else r["url"])
        if code is None:
            warn.append(f"{r['id']}: could not check whether {old} resolves (offline?)")
        elif code not in REDIRECT_OK and not gone:
            err.append((r["id"], "redirect", f"{old} answers {code} and is not recorded as already gone"))
        tp = c.by_url.get(new)
        if not tp:
            err.append((r["id"], "superseded", f"target {r['new']} is no longer a planned page — mark the row superseded "
                        f"(worklist.py supersede) or retarget it"))
        elif not st["pages"][tp].get("wp_id"):
            (err if over else warn).append((r["id"], "redirect", f"target {tp} has no WordPress draft yet") if over
                                           else f"{r['id']}: target {tp} has no WordPress draft yet (needed before the handover)")
        elif tp in c.pub and c.pub[tp] not in r["depends_on"]:
            err.append((r["id"], "redirect", f"does not depend on its target's publish row {c.pub[tp]}"))
        elif tp not in c.pub and over and st["pages"][tp].get("state") not in LIVE_STATES:
            err.append((r["id"], "redirect", f"target {tp} has no publish row"))
        if new == old:
            err.append((r["id"], "redirect", f"{old} redirects to itself"))
        for rid, (o2, n2) in targets.items():
            if rid != r["id"] and o2 == new:
                err.append((r["id"], "redirect", f"chain: {r['new']} is itself redirected by {rid}" +
                            (" (a loop)" if n2 == old else "")))
    if over:
        for pid, p in st["pages"].items():
            texts = [i["text"] for i in p.get("open_items") or []]
            mine = [r for r in live_rows if r["field"] == "open item" and r["decision_map_ref"] == pid]
            for t in texts:
                if not any(r["old"] == t for r in mine):
                    err.append(("-", "placeholder", f"{pid} has an open item with no row: {t[:70]}"))
            for r in mine:
                if r["old"] not in texts:
                    err.append((r["id"], "placeholder", f"{pid} no longer has this notice — mark the row superseded"))
        for pid, items in (st.get("wheel_pending") or {}).items():
            for key, anchor, url, target in items:
                a, b = st["pages"].get(pid) or {}, st["pages"].get(target) or {}
                if a.get("state") in LIVE_STATES and b.get("state") in LIVE_STATES:
                    err.append(("-", "links", f"{pid} → {target} link-table row can be handed over now (publish.py pending)"))
    for ref, d in derived(c).items():
        err.append((ref, "stale", d["reason"].replace("derived: ", "") + " — `worklist.py build` supersedes it"))
    for r in live_rows:
        if r["field"].lower().startswith("clear the slug"):
            pr = [x for x in pubs if norm_url(x["new"]) == norm_url(r["url"])]
            if pr and r["id"] not in pr[0]["depends_on"]:
                err.append((pr[0]["id"], "order", f"does not depend on {r['id']}, which clears its slug first"))
            if not pr:
                err.append((r["id"], "order", f"clears {r['url']} but no publish row uses that URL"))
    for r in live_rows:
        for k in ("where", "how", "done_check", "task"):
            if not (r.get(k) or "").strip():
                err.append((r["id"], "complete", f"{k} is empty"))
    return err, warn


def cmd_check(a):
    err, warn = problems(a.slug)
    d = client_dir(a.slug) / "handoffs"
    d.mkdir(parents=True, exist_ok=True)
    lines = [f"# Worklist check — {a.slug} — {today()}", "", f"{len(err)} error(s) · {len(warn)} warning(s)", ""]
    lines += [f"- **{i}** [{rule}] {msg}" for i, rule, msg in err] + [f"- (warning) {w}" for w in warn]
    (d / "worklist-check.md").write_text("\n".join(lines) + "\n")
    if not a.report_only:
        st = S.load(a.slug)
        st["worklist_check"] = {"ok": not err, "at": now(), "errors": len(err), "sig": signature(a.slug)}
        S.save(a.slug, st)
    print(f"worklist check: {len(err)} error(s), {len(warn)} warning(s)"
          + (" — passes" if not err else " — REFUSED, nothing is handed over until these are fixed (handoffs/worklist-check.md)"))
    for i, rule, msg in err[:8]:
        print(f"  {i} [{rule}] {msg[:150]}")
    if len(err) > 8:
        print(f"  … {len(err) - 8} more in handoffs/worklist-check.md")
    sys.exit(4 if err else 0)


def signature(slug):
    """The worklist without what the VA fills in (status, note): the check stays valid while rows are ticked."""
    rs, _ = full_rows(slug)
    keep = ("id", "task", "where", "how", "values", "depends_on", "done_check", "owner")
    return hashlib.sha256(json.dumps([[r[k] for k in keep] for r in rs if r["status"] != "superseded"]).encode()).hexdigest()[:12]


def check_passed(slug):
    """True when the last `check` passed for these very rows (Drive copy and handover depend on it)."""
    st = S.load(slug)
    wc = st.get("worklist_check") or {}
    return bool(wc.get("ok")) and wc.get("sig") == signature(slug)


def cmd_supersede(a):
    ref = a.ref
    rs, _ = full_rows(a.slug)
    ids = {r["id"] for r in rs}
    if ref not in ids:
        sys.exit(f"no row {ref} in the worklist")
    if a.by.lower() != "none" and a.by not in ids:
        sys.exit(f"the replacing row {a.by} is not in the worklist")
    p = client_dir(a.slug) / "handoffs" / "worklist-superseded.json"
    data = superseded(a.slug)
    data[ref] = {"by": "" if a.by.lower() == "none" else a.by, "reason": a.reason, "at": now()}
    write_json(p, data)
    build(a.slug)
    print(f"{ref}: superseded" + (f" by {a.by}" if a.by.lower() != "none" else ""))


# ------------------------------------------------------------------ the files
def order(rows_):
    """Rows in dependency order, stable by when they were added."""
    ids = {r["id"] for r in rows_}
    out, done = [], set()
    pending = list(rows_)
    while pending:
        n = len(out)
        for r in list(pending):
            deps = [x.strip() for x in r["depends_on"].split(",") if x.strip() and x.strip() in ids]
            if all(x in done or x in {y["id"] for y in out} for x in deps) or not deps:
                out.append(r)
                done.add(r["id"])
                pending.remove(r)
        if len(out) == n:   # a cycle: the validator reports it; keep going in file order
            out += pending
            break
    return out


def apply_derived(slug):
    """Record the derived supersessions (a, d) in worklist-superseded.json — with their reasons, once. Returns them."""
    c = Ctx(slug)
    new = derived(c)
    if new:
        data = superseded(slug)
        data.update({ref: {**d, "at": now()} for ref, d in new.items()})
        write_json(client_dir(slug) / "handoffs" / "worklist-superseded.json", data)
    return new


def build(slug):
    apply_derived(slug)
    st = S.load(slug)
    d = client_dir(slug) / "handoffs"
    d.mkdir(parents=True, exist_ok=True)
    allr, c = full_rows(slug)
    if not allr and not (d / "VA-WORKLIST.csv").exists():
        return None
    over = handed_over(st)
    # pages already with Jonie (a batch handed off before the one-handover rule, e.g. a pilot): their rows always show
    sent = {b.get("handoff") for b in S.batches(st) if b.get("handoff")}
    sent_pages = {p for b in S.batches(st) if b.get("state") in ("handed_off", "corrections_requested", "published",
                                                                  "verified", "written_back") for p in b["pages"]}
    shown = [r for r in allr if over or r["section"] in (1, 2, 6) or r["_hid"] in sent
             or r.get("decision_map_ref") in sent_pages]
    held = len(allr) - len(shown)
    shown.sort(key=lambda r: (r["section"], r["added"], r["ref"]))
    shown = [x for sec in SECTIONS for x in order([r for r in shown if r["section"] == sec])]   # dependency order inside each
    with open(d / "VA-WORKLIST.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows({**r, "section": f"{r['section']} {SECTIONS[r['section']]}"} for r in shown)
    name = st["client"]["name"]
    done = sum(r["status"] == "done" for r in shown)
    live = sum(r["status"] != "superseded" for r in shown)
    owners = sorted({r["owner"] for r in shown})
    md = [f"# {name} - VA Worklist", "",
          f"**One living worklist for every VA item** · client {name} ({st['client'].get('domain')}) · updated {today()} · "
          f"**Progress:** {done} of {live} row(s) done", "",
          "## Start here", "",
          f"- **What this is:** every task for {name}'s website that a person has to do, in one list. Nothing else is "
          "needed — each row says what to do, where, how, what to type, and how to check it worked.",
          f"- **Order:** work through the sections from 1 to 6, and inside each section from top to bottom. A row's "
          "`depends_on` lists the rows that must be done first (for example, a redirect comes after its target page is published). "
          "Section 4 is published all together.",
          f"- **Who owns what:** {', '.join(owners) or 'nobody yet'} — the `owner` column on each row. Jonie: technical and "
          "publishing. Gwen: lookups and records. Paul: decisions.",
          "- **How to tick a row:** in the CSV set `status` to **done**, **blocked** or **deviated** (a `note` is required "
          "on every blocked or deviated row) and send it back. Check the current value first: already done → mark `done` and "
          "say `already done`; something else → do not change it, mark `blocked` and say what you found. Do not add rows.",
          "- **After you return it:** the system checks every done row against its `done_check`. A row whose check fails "
          "comes back as `open`, with the reason in `note`.", ""]
    if not over:
        md += ["> **Sections 3 Redirects, 4 Publish and 5 After publish come in one handover**, once every service and "
               "location page is a WordPress draft" + (f" ({held} row(s) waiting)." if held else "."), ""]
    for sec, title in SECTIONS.items():
        mine = [r for r in shown if r["section"] == sec and r["status"] != "superseded"]
        if not mine:
            continue
        md += [f"## {sec} · {title}", "", GUIDE[sec], "",
               "| ID | Task | Where | How | Values | Depends on | Done check | Owner | Status |",
               "|---|---|---|---|---|---|---|---|---|"]
        for r in mine:
            cell = lambda t: (t or "").replace("|", "/").replace("\n", " ")   # noqa: E731
            how = cell(r["how"]).replace(" 2. ", "<br>2. ").replace(" 3. ", "<br>3. ").replace(" 4. ", "<br>4. ") \
                .replace(" 5. ", "<br>5. ").replace(" 6. ", "<br>6. ")
            md.append(f"| {r['id']} | {cell(r['task'])} | {cell(r['where'])} | {how} | {cell(r['values'])} | "
                      f"{cell(r['depends_on']) or '—'} | {cell(r['done_check'])} | {r['owner']} | "
                      f"{r['status']}{(' — ' + cell(r['note'])) if r.get('note') else ''} |")
        md.append("")
    gone = [r for r in shown if r["status"] == "superseded"]
    if gone:
        md += ["## Superseded — do not do these", "", "A newer decision replaced each row below. Skip them.", "",
               "| ID | Was | Replaced by / why |", "|---|---|---|"]
        md += [f"| {r['id']} | {(r['task'] or '').replace('|', '/')} | {(r['note'] or '').replace('|', '/')} |" for r in gone]
        md.append("")
    (d / "VA-WORKLIST.md").write_text("\n".join(md) + "\n")
    for f in d.glob("H-*.md"):   # the per-handoff documents are superseded by the worklist
        t = f.read_text()
        if HFILE.match(f.with_suffix(".csv").name) and "Superseded by the VA Worklist" not in t:
            lines = t.split("\n", 1)
            f.write_text(lines[0] + "\n\n> **Superseded by the VA Worklist** (`VA-WORKLIST.md`, rewrite 2 P9) — work from "
                         "the worklist; this file is kept as the record.\n" + (lines[1] if len(lines) > 1 else ""))
    return {"rows": len(shown), "held": held, "done": done}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("build"); s.add_argument("slug")
    s = sub.add_parser("check"); s.add_argument("slug"); s.add_argument("--report-only", action="store_true")
    s = sub.add_parser("supersede"); s.add_argument("slug"); s.add_argument("ref"); s.add_argument("--by", required=True)
    s.add_argument("--reason", default="")
    a = ap.parse_args()
    if a.cmd == "check":
        return cmd_check(a)
    if a.cmd == "supersede":
        return cmd_supersede(a)
    pre = len(superseded(a.slug))
    r = build(a.slug)
    done_now = len(superseded(a.slug)) - pre
    if done_now:
        print(f"{done_now} row(s) superseded by the approved plan (reasons in handoffs/worklist-superseded.json)")
    print("no VA items yet" if r is None else f"VA Worklist: {r['rows']} row(s), {r['done']} done"
          + (f", {r['held']} waiting for the handover" if r["held"] else ""))


if __name__ == "__main__":
    main()
