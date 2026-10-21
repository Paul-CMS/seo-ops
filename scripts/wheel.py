#!/usr/bin/env python3
"""wheel.py — the Bradley link wheel, by script, from the approved site plan (Rewrite 4 Phase 5, CM-064).

    wheel.py plan  <slug> [--out F]      every page's link-table rows → build/link-wheel.json (publish.py drafts reads it)
    wheel.py show  <slug> <page>         one page's rows, table by table
    wheel.py check <slug>                counts and placement (CM-022, CM-064): exit 1 on an error
    wheel.py asks  <slug> [--out F]      the CM-022 exceptions and over-count rows as kind-1 Asks for the site plan
                                         → build/link-asks.json (review-finding shape)
    wheel.py fill  <slug> <file>         print an approved file as it ships: tables filled, [LINK → …] markers resolved
                                         (a preview — the approved file is never changed)

The wheel (BB-205/206, CM-005, CM-064; every row is a table/H3 link, never prose):
    service page   service_areas   every location page                        ("[Service variant] in [City]")
    location page  services        every service page                         ("[Service variant]")
                   siblings        its hub first, then every other location   (the target's H1)
    hub (county)   service_areas   its own cities (same plan group)           (the target's H1)
                   services        every service page                         ("[Service variant]")
    homepage       services        every service page — at most 6 (HP-11)     ("[Service variant]")
                   service_areas   every hub, then every location with no hub (the target's H1)
    about          —
A location's hub goes first in its sibling table unless the page has its own `[Link wheel: populate hub links here]`
row. Anchors are formulas, never chosen: a target's H1 comes from its approved file, else the plan row, else
outline.py's formula. Rows are filled into each page's `| [Link wheel: populate <table> links here] |` placeholder when
its WordPress draft is generated; the approved file never changes, so an in-flight section keeps what it has.

Inline markers `[LINK → /slug/ · reason]` (P11) are only for pages not yet planned. When a draft is generated:
    target planned + CM-022 exception approved (settled key linkx:<page>:<n>, answer "a"/"approve…")
                                           → the words before the marker become the link
    target planned, no approved exception  → the marker is dropped and the words kept (the table carries the link)
    target not planned                     → stays an open item (notice + worklist row), as before
CM-022 exceptions (one contextual link and 1–2 outbound authority links per page, each with a reason) are proposed in
the site plan row as "link_exceptions": [{"kind": "contextual"|"outbound", "target": "/slug/" or URL, "anchor": "…",
"reason": "…"}]; `wheel.py asks` turns each into a kind-1 Ask for the site plan's review (never applied without Paul).
"""
import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

from lib import ROOT, client_dir, die, now, write_json

HOMEPAGE_MAX_SERVICES = 6           # HP-11: "max 5–6" service links on the homepage
EXC_MAX = {"contextual": 1, "outbound": 2}   # CM-022 (one contextual), CM-011 (1–2 outbound)
TABLE_OF = {"service-area": "service_areas", "service areas": "service_areas", "service-areas": "service_areas",
            "city": "service_areas", "cities": "service_areas", "service": "services", "services": "services",
            "sibling-city": "siblings", "sibling city": "siblings", "sibling": "siblings", "hub": "hub",
            "related-service": "related", "related service": "related"}
# a trailing note after the key is allowed: "| [Link wheel: populate service-area links here — Beaufort, …] |"
PLACEHOLDER = re.compile(r"^\|\s*\[Link wheel: populate ([a-z -]+?) links here(?:\s*[—–:-][^\]]*)?\]\s*\|\s*$", re.I)
LINK_MARK = re.compile(r"\[LINK →\s*(/[^\s·\]]*/?|https?://[^\s·\]]+)\s*·\s*([^\]]+)\]")
NEEDS = {"service": ["service_areas"], "location": ["services", "siblings"], "county": ["service_areas", "services"],
         "homepage": ["services", "service_areas"]}
CORE = ("service", "location", "county", "homepage", "about")


def table_key(label):
    k = label.lower().strip()
    return TABLE_OF.get(k, k.replace(" ", "_"))


def path_of(url):
    return "/" + urllib.parse.urlparse(url or "").path.strip("/") + "/" if (url or "").strip("/") else "/"


# ------------------------------------------------------------------ the approved file of a page
def approved_file(st, pid):
    """The page's approved (or latest recorded) file, or None."""
    p = st["pages"].get(pid) or {}
    for f in ((p.get("approval") or {}).get("file"), p.get("file")):
        if f and (ROOT / f).is_file():
            return f
    for b in st.get("build", {}).get("batches") or []:
        if pid in b.get("pages", []):
            for f in (b.get("files") or {}).get("drafts") or []:
                try:
                    head = (ROOT / f).read_text(encoding="utf-8")[:1500]
                except (OSError, UnicodeDecodeError):
                    continue
                if re.search(rf"^page_id:\s*{re.escape(pid)}\s*$", head, re.M):
                    return f
    return None


def file_h1(f):
    try:
        m = re.search(r"^# (.+)$", (ROOT / f).read_text(encoding="utf-8"), re.M)
    except (OSError, UnicodeDecodeError):
        return None
    return m.group(1).strip() if m else None


def placeholders_in(f):
    """The table keys a page file has placeholder rows for."""
    if not f:
        return None
    try:
        text = (ROOT / f).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return [table_key(m.group(1)) for m in (PLACEHOLDER.match(l.strip()) for l in text.splitlines()) if m]


# ------------------------------------------------------------------ anchors (formulas)
def _title(s):
    import outline
    return outline.title_case(s)


def city_of(p):
    if p.get("city"):
        return p["city"]
    return re.sub(r",\s*[A-Z]{2}\.?$", "", (p.get("name") or "").strip()).strip()


def _ent(slug):
    import outline
    try:
        return outline.bg_entity(outline.brand_guide(slug))
    except Exception:   # noqa: BLE001 — no Brand Guide yet: the formulas fall back to the plan rows
        return {"c1": {}, "variants": [], "category": "", "reserved_cat": "", "reserved_area": "", "pool": []}


def service_variant(st, pid, ent):
    """The service's variant: plan row, else Brand Guide C1, else the H1 before ' in ', else its name."""
    import outline
    p = st["pages"][pid]
    if p.get("service_variant"):
        return _title(p["service_variant"])
    row = (ent.get("c1") or {}).get(outline._path(p.get("url")), {})
    if row.get("variant"):
        return _title(row["variant"])
    h1 = h1_of(st, pid, ent)
    if h1 and " in " in h1:
        return h1.rsplit(" in ", 1)[0].strip()
    return _title(re.sub(r"\s*\([^)]*\)", "", p.get("name") or pid).strip())


def h1_of(st, pid, ent, formula=True):
    p = st["pages"][pid]
    f = approved_file(st, pid)
    h = file_h1(f) if f else None
    if h:
        return h
    if p.get("h1"):
        return p["h1"]
    if (p.get("assigned") or {}).get("h1"):
        return p["assigned"]["h1"]
    if formula and p.get("type") in ("location", "service"):
        try:
            import outline
            v = outline.formula(st, pid, ent).get("h1")
            if v and v[0]:
                return v[0]
        except Exception:   # noqa: BLE001
            pass
    return None


def place_anchor(st, pid, ent, primary_sv):
    p = st["pages"][pid]
    if p.get("type") == "county":
        return h1_of(st, pid, ent, formula=False) or re.sub(r"\s+hub$|\s*\([^)]*\)", "", p.get("name") or pid).strip()
    return h1_of(st, pid, ent) or (f"{primary_sv} in {city_of(p)}" if primary_sv else city_of(p))


# ------------------------------------------------------------------ the wheel
def pages_of(st):
    return {pid: p for pid, p in st["pages"].items() if p.get("type") in CORE}


def hubs_by_group(pages):
    return {p.get("group"): pid for pid, p in pages.items() if p.get("type") == "county" and p.get("group")}


def plan(st, slug):
    """{page id: {table: [[anchor, url, target], …]}} plus the issues found (CM-064)."""
    pages = pages_of(st)
    ent = _ent(slug)
    svcs = [k for k, p in pages.items() if p["type"] == "service"]
    locs = [k for k, p in pages.items() if p["type"] == "location"]
    hubs = hubs_by_group(pages)
    sv = {k: service_variant(st, k, ent) for k in svcs}
    primary = sv[svcs[0]] if svcs else ""
    anchor = {k: place_anchor(st, k, ent, primary) for k in locs + list(hubs.values())}
    url = lambda k: pages[k].get("url")
    hub_of = {k: hubs.get(pages[k].get("group")) for k in locs}
    wheel = {}
    for s in svcs:
        wheel[s] = {"service_areas": [[f"{sv[s]} in {city_of(pages[l])}", url(l), l] for l in locs]}
    for l in locs:
        own = placeholders_in(approved_file(st, l)) or []
        h = hub_of[l]
        sib = [[anchor[o], url(o), o] for o in locs if o != l]
        t = {"services": [[sv[s], url(s), s] for s in svcs]}
        if h and "hub" in own:
            t["hub"] = [[anchor[h], url(h), h]]
            t["siblings"] = sib
        else:
            t["siblings"] = ([[anchor[h], url(h), h]] if h else []) + sib
        wheel[l] = t
    for g, h in hubs.items():
        wheel[h] = {"service_areas": [[anchor[l], url(l), l] for l in locs if pages[l].get("group") == g],
                    "services": [[sv[s], url(s), s] for s in svcs]}
    for k, p in pages.items():
        if p["type"] == "homepage":
            wheel[k] = {"services": [[sv[s], url(s), s] for s in svcs],
                        "service_areas": [[anchor[h], url(h), h] for h in hubs.values()]
                        + [[anchor[l], url(l), l] for l in locs if not hub_of[l]]}
    return wheel, issues(st, wheel, pages)


def issues(st, wheel, pages):
    """[(level, page, text)] — level error | ask | note."""
    out = []
    for pid, tables in wheel.items():
        anchors = {}
        for key, rows in tables.items():
            for a, u, t in rows:
                if not u:
                    out.append(("error", pid, f"{key}: {t} has no URL in the site plan"))
                if a in anchors and anchors[a] != u:
                    out.append(("error", pid, f"{key}: the anchor {a!r} points at two pages ({anchors[a]}, {u})"))
                anchors[a] = u
        own = placeholders_in(approved_file(st, pid))
        if own is not None:
            for key in NEEDS.get(pages[pid]["type"], []):
                if tables.get(key) and key not in own and not (key == "hub" and "siblings" in own):
                    phrase = {"service_areas": "service-area", "services": "service", "siblings": "sibling-city"}.get(key, key)
                    out.append(("error", pid, f"the page file has no | [Link wheel: populate {phrase} links here] | row "
                                              f"— {len(tables[key])} link(s) would be lost"))
    for pid, p in pages.items():
        if p["type"] == "homepage" and len(wheel.get(pid, {}).get("services", [])) > HOMEPAGE_MAX_SERVICES:
            out.append(("ask", pid, f"{len(wheel[pid]['services'])} service pages but the homepage links at most "
                                    f"{HOMEPAGE_MAX_SERVICES} (HP-11)"))
    return out


def write_plan(slug, st, out=None):
    wheel, probs = plan(st, slug)
    p = Path(out) if out else client_dir(slug) / "build" / "link-wheel.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    write_json(p, {"_about": {"generated": now(), "by": "wheel.py plan (CM-064)", "pages": len(wheel),
                              "rows": sum(len(r) for t in wheel.values() for r in t.values())}, **wheel})
    return p, wheel, probs


def load(slug):
    p = client_dir(slug) / "build" / "link-wheel.json"
    if not p.exists():
        return None
    return {k: v for k, v in json.loads(p.read_text(encoding="utf-8")).items() if not k.startswith("_")}


# ------------------------------------------------------------------ CM-022 exceptions
def exceptions(st, pid):
    return (st["pages"].get(pid) or {}).get("link_exceptions") or []


def exception_key(pid, n):
    return f"linkx:{pid}:{n}"


def approved_exception(slug, key):
    import settled
    e = settled.entries(slug).get(key) or {}
    return e.get("state") == "settled" and bool(re.match(r"^\s*(a\b|approve|yes)", e.get("text") or "", re.I))


def asks(st, slug):
    """The site plan's kind-1 Asks: each proposed CM-022 exception, and each count the wheel cannot meet."""
    out = []
    for pid, p in pages_of(st).items():
        seen = {}
        for n, x in enumerate(exceptions(st, pid), 1):
            kind = x.get("kind") or "contextual"
            seen[kind] = seen.get(kind, 0) + 1
            over = seen[kind] > EXC_MAX.get(kind, 1)
            out.append({"page": pid, "url": p.get("url", ""), "rule": "CM-022" if kind == "contextual" else "CM-011",
                        "item": f"{kind} link {n}", "severity": "ask", "kind": "1", "category": "ask",
                        "decision_key": exception_key(pid, n),
                        "finding": f"Proposed {kind} link on {pid}: \"{x.get('anchor', '')}\" → {x.get('target', '')}"
                                   + (f" — over the limit of {EXC_MAX.get(kind, 1)} per page" if over else ""),
                        "plain_why": x.get("reason") or "(no reason given — CM-022 needs one)",
                        "options": ["approve: link these words", "decline: keep the words, no link"],
                        "recommended": "b" if over or not x.get("reason") else "a"})
    _, probs = plan(st, slug)
    for lvl, pid, text in probs:
        if lvl == "ask":
            out.append({"page": pid, "url": st["pages"][pid].get("url", ""), "rule": "HP-11", "item": "service link count",
                        "severity": "ask", "kind": "1", "category": "ask", "decision_key": f"wheel:{pid}:services",
                        "finding": text, "plain_why": "the homepage lists 5–6 service links (BB-313 §6)",
                        "options": [f"link the first {HOMEPAGE_MAX_SERVICES} in plan order", "link every service page"],
                        "recommended": "a"})
    return out


# ------------------------------------------------------------------ markers and tables at draft time
def planned_url(st, target):
    """The planned page a marker target names, or None."""
    want = path_of(target if target.startswith("http") else "https://x" + target)
    for pid, p in pages_of(st).items():
        if p.get("url") and path_of(p["url"]) == want:
            return pid, p["url"]
    return None


def resolve_markers(slug, st, pid, text):
    """(text, [actions]) — each [LINK → …] marker to a planned page resolved (CM-064); unplanned ones are left."""
    actions = []
    exc = exceptions(st, pid)

    def one(line):
        def sub(m):
            target = m.group(1)
            hit = planned_url(st, target)
            if not hit:
                return m.group(0)
            tid, turl = hit
            n = next((i for i, x in enumerate(exc, 1) if planned_url(st, x.get("target") or "") == hit), None)
            if n and approved_exception(slug, exception_key(pid, n)):
                actions.append({"marker": m.group(0), "action": "linked", "target": tid, "key": exception_key(pid, n),
                                "anchor": exc[n - 1].get("anchor", "")})
                return f"\x00LINK {turl}\x00"
            actions.append({"marker": m.group(0), "action": "dropped", "target": tid,
                            "why": "no approved CM-022 exception — the link table carries it (CM-005)"})
            return ""
        out = LINK_MARK.sub(sub, line)
        # an approved exception links the words just before its marker (its anchor when given, else the last 3 words)
        def link(m):
            pre, u = m.group(1), m.group(2)
            act = next(a for a in actions if a["action"] == "linked" and a.get("done") is None)
            act["done"] = True
            words = act["anchor"] if act["anchor"] and pre.rstrip().endswith(act["anchor"]) else None
            if not words:
                act["action"] = "dropped"
                act["why"] = "approved, but its anchor words are not right before the marker — fix the plan's anchor"
                return pre.rstrip()
            head = pre.rstrip()[: -len(words)]
            return f"{head}[{words}]({u})"
        while "\x00LINK " in out:
            out = re.sub(r"^(.*?)\s*\x00LINK (\S+)\x00", link, out, count=1)
        return re.sub(r" {2,}", " ", out).replace(" .", ".").replace(" ,", ",")
    return "\n".join(one(l) if "[LINK →" in l else l for l in text.split("\n")), actions


def fill(slug, st, wheel, pid, text):
    """The page text as it ships: markers resolved, each table placeholder replaced by its rows (Markdown)."""
    text, acts = resolve_markers(slug, st, pid, text)
    out = []
    for line in text.split("\n"):
        m = PLACEHOLDER.match(line.strip())
        if m:
            rows = (wheel.get(pid) or {}).get(table_key(m.group(1))) or []
            out += ["| Link |", "|---|"] + [f"| [{a}]({u}) |" for a, u, _ in rows]
        else:
            out.append(line)
    return "\n".join(out), acts


# ------------------------------------------------------------------ commands
def main():
    import status as S
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("plan"); s.add_argument("slug"); s.add_argument("--out")
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("page")
    s = sub.add_parser("check"); s.add_argument("slug")
    s = sub.add_parser("asks"); s.add_argument("slug"); s.add_argument("--out")
    s = sub.add_parser("fill"); s.add_argument("slug"); s.add_argument("file")
    a = ap.parse_args()
    st = S.load(a.slug)
    if a.cmd == "plan":
        p, wheel, probs = write_plan(a.slug, st, a.out)
        n = sum(len(r) for t in wheel.values() for r in t.values())
        print(f"link wheel: {n} row(s) on {len(wheel)} page(s) → {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}")
        errs = [x for x in probs if x[0] == "error"]
        for lvl, pid, t in probs[:8]:
            print(f"  {lvl.upper()} {pid}: {t}")
        sys.exit(1 if errs else 0)
    if a.cmd == "show":
        wheel, _ = plan(st, a.slug)
        for key, rows in (wheel.get(a.page) or {}).items():
            print(f"## {key} ({len(rows)})")
            for anc, u, t in rows:
                print(f"- {anc} → {u}")
        return
    if a.cmd == "check":
        _, probs = plan(st, a.slug)
        for lvl, pid, t in probs:
            print(f"{lvl.upper()} {pid}: {t}")
        errs = sum(1 for x in probs if x[0] == "error")
        print(f"wheel check: {errs} error(s), {len(probs) - errs} other")
        sys.exit(1 if errs else 0)
    if a.cmd == "asks":
        rows = asks(st, a.slug)
        p = Path(a.out) if a.out else client_dir(a.slug) / "build" / "link-asks.json"
        write_json(p, rows)
        print(f"{len(rows)} kind-1 Ask(s) for the site plan (CM-022 exceptions, wheel counts) → "
              f"{p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}")
        return
    if a.cmd == "fill":
        wheel = load(a.slug) or plan(st, a.slug)[0]
        text = (ROOT / a.file).read_text(encoding="utf-8")
        pid = re.search(r"^page_id:\s*(\S+)", text, re.M)
        if not pid:
            die(f"{a.file}: no page_id in its header")
        out, acts = fill(a.slug, st, wheel, pid.group(1), text)
        print(out)
        for x in acts:
            print(f"<!-- marker {x['action']}: {x['marker']} ({x.get('why', x.get('key', ''))}) -->")


if __name__ == "__main__":
    main()
