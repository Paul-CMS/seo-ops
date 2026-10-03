#!/usr/bin/env python3
"""wp.py — the one way seo-ops touches WordPress: the REST API with an Application Password for a
dedicated Editor user per site. No connector plugin. Every write is gated, checked and logged.
Site setup: wordpress/wordpress-site-setup.md.

Credentials (.env, typed by Paul, never printed): WP_<SLUG>_URL, WP_<SLUG>_USER, WP_<SLUG>_APP_PASSWORD
— <SLUG> is the client slug in capitals with hyphens as underscores (red-rover-roofing →
WP_RED_ROVER_ROOFING_URL).

Connection
    wp.py check <slug> --run R [--pilot]   /wp-check: connection, Editor role, draft creation (page + post),
                                           SEOPress 6.8+ per-page endpoints, site-wide settings readable?,
                                           must-use plugin + Kadence head-code field. Plain-language report.
                                           --pilot adds the head-code round trip and the published-batch check.
Read (no run needed)
    wp.py get <slug> <url>                 status, slug, title, every SEOPress field
    wp.py inspect <slug> <url>             post meta keys exposed (pilot: find the Kadence head-code key)
    wp.py media <slug> --post ID           images attached to a page/post: id, file, alt text
    wp.py redirects <slug>                 SEOPress redirect list (for /verify)
Write (an open run, the gate for the change kind, the current value as expected)
    wp.py set <slug> --run R --url U --field F --value V --expect OLD [--live --backup-confirmed T]
          F = title | description | keyword | social_title | social_description | robots | canonical
    wp.py set-alt <slug> --run R --media-id N --alt T --expect-alt OLD [--live --backup-confirmed T]
    wp.py fix-content <slug> --run R --url U --kind broken_link|image_url --old S --new S [--live --backup-confirmed T]
    wp.py set-head <slug> --run R --url U --file F --expect-sha OLD [--live --backup-confirmed T]   (schema)
    wp.py restore <slug> --run R --change N [--live --backup-confirmed T]                        (/rollback)
New pages and posts: drafts only, generated from approved files by publish.py (new_draft below).

Rules enforced here (CLAUDE.md §4):
  - The system NEVER publishes: new content is created with status "draft"; Jonie publishes.
  - Any change to an already-published page needs --live and Paul's ManageWP backup confirmation.
  - Safe fixes (after audit_approved): alt text, broken links and image URLs in content, meta descriptions.
  - Structural fixes (after entity + Brand Guide approved): title, keyword, social, meta robots, canonical, schema.
  - Pilot rule, per site: until Paul approves wordpress_pilot_approved, only drafts and safe fixes are
    written; structural fields go out as VA handoffs. Drafts the system creates always carry every field.
  - Check the current value first; already correct → SKIPPED; different from what the audit recorded →
    STOP. Every change is logged with URL, old, new and result; /rollback restores from the log.
  - Redirects and SEOPress site-wide settings are never changed here — always a VA handoff.
  - Per-client safe-fix cap (status.py cap): once that many of a kind are applied, the next is refused
    until Paul raises it.
"""
import argparse
import base64
import datetime
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

import run as R
import status as S
from lib import ROOT, client_dir, config, die, load_env, now, redact

GATES = S.GATES
TEST_TITLE = "seo-ops connection test — safe to delete"

# field -> (SEOPress endpoint, body keys, change kind)
FIELDS = {
    "title":              ("title-description-metas", ["title"], "seo_title"),
    "description":        ("title-description-metas", ["description"], "meta_description"),
    "keyword":            ("target-keywords", ["_seopress_analysis_target_kw"], "seo_keyword"),
    "social_title":       ("social-settings", ["_seopress_social_fb_title", "_seopress_social_twitter_title"], "social"),
    "social_description": ("social-settings", ["_seopress_social_fb_desc", "_seopress_social_twitter_desc"], "social"),
    "robots":             ("meta-robot-settings", ["_seopress_robots_index", "_seopress_robots_follow"], "meta_robots"),
    "canonical":          ("meta-robot-settings", ["_seopress_robots_canonical"], "canonical"),
}


class WpError(Exception):
    def __init__(self, msg, code=None, body=""):
        super().__init__(msg)
        self.code, self.body = code, body


# ---------------------------------------------------------------- connection
def env_prefix(slug):
    return "WP_" + re.sub(r"[^A-Z0-9]", "_", slug.upper())


def creds(slug):
    pre = env_prefix(slug)
    env = load_env()
    base, user, pw = env.get(f"{pre}_URL"), env.get(f"{pre}_USER"), env.get(f"{pre}_APP_PASSWORD")
    if not (base and user and pw):
        die(f"{pre}_URL / {pre}_USER / {pre}_APP_PASSWORD are missing from .env. Paul types them in himself "
            "(wordpress/wordpress-site-setup.md).")
    return base.rstrip("/"), "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()


def call(slug, path, method="GET", body=None, auth=True):
    base, header = creds(slug)
    url = f"{base}/wp-json/{path.lstrip('/')}" if path else f"{base}/wp-json/"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", "User-Agent": "seo-ops/1.0",
                                          **({"Authorization": header} if auth else {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            try:
                return json.loads(raw) if raw else {}
            except ValueError:
                raise WpError(f"{method} {path}: the site answered with a web page, not JSON", r.status, raw[:300])
    except urllib.error.HTTPError as e:
        body_ = e.read().decode(errors="replace")[:400]
        raise WpError(redact(f"{method} {path}: HTTP {e.code} {body_}"), e.code, body_)
    except urllib.error.URLError as e:
        raise WpError(redact(f"{method} {path}: {e}"), 0, "")


def sha(text):
    return hashlib.sha256((text or "").encode()).hexdigest()[:12]


def find(slug, url):
    """Resolve a public URL to (post_type, post) with edit context."""
    path = urllib.parse.urlparse(url).path.strip("/")
    leaf = path.split("/")[-1] if path else ""
    if not leaf:
        front = call(slug, "wp/v2/settings").get("page_on_front")
        if front:
            return "pages", call(slug, f"wp/v2/pages/{front}?context=edit")
    for kind in ("pages", "posts"):
        res = call(slug, f"wp/v2/{kind}?slug={urllib.parse.quote(leaf)}&context=edit&status=any")
        for p in res:
            if p.get("link", "").rstrip("/").endswith(path) or len(res) == 1:
                return kind, p
    raise WpError(f"No page or post found for {url}")


def seo_read(slug, post_id):
    """Every SEOPress field, normalised (public GET seopress/v1/posts/{id}). Field names are confirmed
    on the pilot site: a field this cannot read back fails the pilot instead of being guessed."""
    r = call(slug, f"seopress/v1/posts/{post_id}")
    g = lambda *ks: next((r[k] for k in ks if r.get(k) not in (None, "")), "")
    og, tw, rb = r.get("og") or {}, r.get("twitter") or {}, r.get("robots") or {}
    noindex = rb.get("noindex") if isinstance(rb, dict) else None
    noindex = noindex if noindex is not None else (g("_seopress_robots_index") == "yes")
    nofollow = rb.get("nofollow") if isinstance(rb, dict) else None
    nofollow = nofollow if nofollow is not None else (g("_seopress_robots_follow") == "yes")
    return {"title": g("title", "_seopress_titles_title"),
            "description": g("description", "_seopress_titles_desc"),
            "keyword": g("target_keywords", "target_kw", "_seopress_analysis_target_kw"),
            "social_title": og.get("title") or g("_seopress_social_fb_title"),
            "social_description": og.get("description") or g("_seopress_social_fb_desc"),
            "social_title_x": tw.get("title") or g("_seopress_social_twitter_title"),
            "social_description_x": tw.get("description") or g("_seopress_social_twitter_desc"),
            "robots": f"{'noindex' if noindex else 'index'},{'nofollow' if nofollow else 'follow'}",
            "canonical": g("canonical", "_seopress_robots_canonical"),
            "raw": r}


def seo_body(field, value, cur):
    """The PUT body for one field, carrying the endpoint's other current values so nothing is wiped."""
    ep = FIELDS[field][0]
    if ep == "title-description-metas":
        b = {"title": cur["title"], "description": cur["description"]}
        b[field] = value
    elif ep == "target-keywords":
        b = {"_seopress_analysis_target_kw": value}
    elif ep == "social-settings":
        b = {"_seopress_social_fb_title": cur["social_title"], "_seopress_social_twitter_title": cur["social_title_x"],
             "_seopress_social_fb_desc": cur["social_description"], "_seopress_social_twitter_desc": cur["social_description_x"]}
        for k in FIELDS[field][1]:
            b[k] = value
    else:  # meta-robot-settings
        robots = value if field == "robots" else cur["robots"]
        b = {"_seopress_robots_index": "yes" if robots.startswith("noindex") else "",
             "_seopress_robots_follow": "yes" if robots.endswith("nofollow") else "",
             "_seopress_robots_canonical": value if field == "canonical" else cur["canonical"]}
    return ep, b


def seo_put(slug, post_id, field, value, cur):
    ep, body = seo_body(field, value, cur)
    call(slug, f"seopress/v1/posts/{post_id}/{ep}", "PUT", body)


def new_draft(slug, ptype, title, content, slug_name, seo):
    """A new page/post as a DRAFT with every SEOPress field from the approved file (decision: drafts
    carry all fields; robots and canonical stay at SEOPress defaults). Returns the draft."""
    d = call(slug, f"wp/v2/{ptype}", "POST", {"title": title, "content": content, "status": "draft",
                                               **({"slug": slug_name} if slug_name else {})})
    call(slug, f"seopress/v1/posts/{d['id']}/title-description-metas", "PUT",
         {"title": seo["title"], "description": seo["description"]})
    if seo.get("keyword"):
        call(slug, f"seopress/v1/posts/{d['id']}/target-keywords", "PUT", {"_seopress_analysis_target_kw": seo["keyword"]})
    call(slug, f"seopress/v1/posts/{d['id']}/social-settings", "PUT",
         {"_seopress_social_fb_title": seo["title"], "_seopress_social_twitter_title": seo["title"],
          "_seopress_social_fb_desc": seo["description"], "_seopress_social_twitter_desc": seo["description"]})
    return d


# ---------------------------------------------------------------- guards
def pilot_approved(st):
    return S._decided(st, "wordpress_pilot_approved")


def require(slug, run_id, kind, page_id=None, post=None, live=False, backup=None):
    """Open run · gate for the change kind · pilot rule · --live + backup for published pages."""
    R.open_run(slug, run_id)
    st = S.load(slug)
    spec = GATES["change_kinds"][kind]
    if spec["channel"] == "handoff":
        die(f"{kind} is never changed by the system — it is a VA handoff to {spec.get('owner', 'Jonie')} (handoff.py).")
    ok, why = S.condition_met(st, "wordpress_connected")
    if not ok:
        die(f"REFUSED — {why}", 4)
    is_draft = bool(post) and post.get("status") == "draft"
    if spec["channel"] == "wp_after_pilot" and not pilot_approved(st) and not is_draft:
        die(f"{kind}: this site has not passed the WordPress pilot yet, so this goes out as a VA handoff to "
            "Jonie (handoff.py). After /wp-check --pilot passes, Paul approves wordpress_pilot_approved.")
    gate = spec["gate"]
    ok, rs = (S.page_approved(st, page_id or "") if gate == "page_approval" else S.gate_met(st, gate))
    if not ok:
        die(f"REFUSED — " + (rs if isinstance(rs, str) else "; ".join(rs)), 4)
    if post and post.get("status") == "publish" and not (live and backup):
        die("This page is live. Changing an already-published page needs --live and --backup-confirmed "
            "\"ManageWP backup <time>, confirmed by Paul\" — ask Paul to confirm a fresh backup first.")


def check_cap(slug, kind):
    """Per-client safe-fix cap (status.json client.safe_fix_cap, set by status.py cap): refuse once the
    system has applied that many of this kind for the client. Rollbacks don't free a slot."""
    cap = (S.load(slug)["client"].get("safe_fix_cap") or {}).get(kind)
    if cap is None:
        return
    done = sum(1 for c in R.changes(slug) if c["kind"] == kind and c.get("channel") == "wp"
               and str(c["result"]).startswith("APPLIED"))
    if done >= cap:
        die(f"REFUSED — safe-fix cap reached for {kind}: {done} of {cap} already applied for this client. "
            f"Paul checks them live and raises the cap (status.py cap {slug} {kind} <n> --run R) before more go out.", 4)


def log(slug, run_id, kind, url, field, old, new, result, **kw):
    return R.log_change(slug, run_id, kind, url, field, old, new, result, channel="wp", **kw)


def live_note(post, backup):
    return f" · live page, backup: {backup}" if post and post.get("status") == "publish" else ""


# ---------------------------------------------------------------- /wp-check
CAUSE_BLOCKED = ("the REST API is blocked — most likely a security plugin (Wordfence, Solid Security/iThemes, "
                 "All In One WP Security, 'Disable REST API') or the host's firewall (ModSecurity, Cloudflare WAF). "
                 "Allow /wp-json/ for the seo-ops user (wordpress-site-setup.md §3).")
CAUSE_AUTH = ("the Application Password was not accepted — wrong password, Application Passwords disabled by a "
              "security plugin, or the host strips the Authorization header (Apache/CGI: add the .htaccess line "
              "in wordpress-site-setup.md §3).")


def kadence_key(st):
    return st["client"].get("kadence_head_meta_key") or config().get("kadence_head_meta_key")


def wp_check(a):
    R.open_run(a.slug, a.run)
    st = S.load(a.slug)
    items, tests = [], []      # (ok: True/False/None, what, detail / what to do)
    add = lambda ok, what, detail="": items.append((ok, what, detail))

    def finish(passed):
        rep = render_check(st, items, a.pilot)
        d = client_dir(a.slug) / "wordpress"
        d.mkdir(exist_ok=True)
        f = d / f"wp-check-{'pilot-' if a.pilot else ''}{now()[:10]}.md"
        f.write_text(rep)
        st2 = S.load(a.slug)
        w = st2.setdefault("wordpress", {})
        w["check"] = {"at": now(), "passed": passed, "report": str(f.relative_to(ROOT)),
                      "settings_readable": w.get("check", {}).get("settings_readable")}
        w["check"].update({k: v for k, v in state.items()})
        S.save(a.slug, st2)
        if a.pilot and passed:
            import subprocess
            subprocess.run([sys.executable, str(ROOT / "scripts" / "status.py"), "mark", a.slug, "wordpress_pilot",
                            "--file", str(f.relative_to(ROOT))], check=True, capture_output=True)
        print(rep)
        sys.exit(0 if passed else 1)
    state = {}

    # 1 · credentials
    pre = env_prefix(a.slug)
    try:
        base, _ = creds(a.slug)
        add(True, "Credentials", f"{pre}_URL / _USER / _APP_PASSWORD are in .env")
    except SystemExit:
        add(False, "Credentials", f"{pre}_URL, {pre}_USER and {pre}_APP_PASSWORD must be in .env — Paul adds them")
        finish(False)
    # 2 · REST API reachable (no login)
    try:
        idx = call(a.slug, "", auth=False)
        ns = idx.get("namespaces") or []
        add(True, "REST API reachable", base + "/wp-json/")
        if "seopress/v1" not in ns:
            add(False, "SEOPress", "SEOPress's REST API is not there — SEOPress is missing, inactive or older than 5.0")
    except WpError as e:
        if e.code == 0:
            add(False, "REST API reachable", f"the site did not answer ({e}) — check the URL, DNS and SSL")
        elif e.code == 404:
            add(False, "REST API reachable", "nothing at /wp-json/ — permalinks may be set to 'Plain', or the REST API is disabled")
        else:
            add(False, "REST API reachable", CAUSE_BLOCKED)
        finish(False)
    # 3 · login and role
    try:
        me = call(a.slug, "wp/v2/users/me?context=edit")
        roles = me.get("roles") or []
        if "editor" in roles:
            add(True, "Login and role", f"logged in as {me.get('slug') or me.get('name')} (Editor)")
        elif "administrator" in roles:
            add(None, "Login and role", "works, but this is an Administrator — use a dedicated Editor user (setup §1)")
        else:
            add(False, "Login and role", f"role is {', '.join(roles) or 'unknown'} — the seo-ops user must be an Editor")
            finish(False)
    except WpError as e:
        add(False, "Login and role", CAUSE_AUTH if e.code in (401, 403) else f"could not read the user ({e})")
        finish(False)
    # 4 · draft creation (page and post), then trash both
    made = []
    try:
        for ptype in ("pages", "posts"):
            d = call(a.slug, f"wp/v2/{ptype}", "POST", {"title": TEST_TITLE, "content": "<p>test</p>", "status": "draft"})
            made.append((ptype, d))
            log(a.slug, a.run, "wp_check", d.get("link", ""), f"test draft {ptype[:-1]}", "(none)", f"draft id {d['id']}",
                "APPLIED · test draft (trashed at the end of the check)")
        add(True, "Draft creation", "can create a draft page and a draft post")
    except WpError as e:
        add(False, "Draft creation", f"cannot create drafts ({e.code}) — the user needs the Editor role")
    # 5 · SEOPress per-page endpoints (Application Password support = 6.8+)
    if made:
        pid = made[0][1]["id"]
        want = {"title": "seo-ops test title", "description": "seo-ops test description",
                "keyword": "seo-ops test keyword", "social_title": "seo-ops test social title",
                "social_description": "seo-ops test social description", "robots": "noindex,follow",
                "canonical": made[0][1].get("link", "")}
        bad = []
        try:
            for field, value in want.items():
                cur = seo_read(a.slug, pid)
                seo_put(a.slug, pid, field, value, cur)
            back = seo_read(a.slug, pid)
            bad = [f for f, v in want.items() if back.get(f) != v]
            if not bad:
                add(True, "SEOPress 6.8+ per-page fields", "title, meta, keyword, social, robots and canonical "
                    "written and read back on a test draft (Application Passwords work — 6.8 or later)")
            else:
                add(False, "SEOPress per-page fields", f"written but not read back: {', '.join(bad)} — the pilot must "
                    "confirm how this SEOPress version reports them")
        except WpError as e:
            add(False, "SEOPress per-page fields", ("SEOPress refused the Application Password — update SEOPress "
                "to 6.8 or later" if e.code in (401, 403) else f"SEOPress endpoint failed ({e.code}) — update SEOPress to 6.8+"))
        state["seopress_fields_ok"] = not bad
    # 6 · site-wide settings (need Administrator — expected unreadable as Editor)
    readable = {}
    for opt in ("titles-settings", "sitemaps-settings", "advanced-settings", "social-settings"):
        try:
            readable[opt] = call(a.slug, f"seopress/v1/options/{opt}")
        except WpError:
            pass
    state["settings_readable"] = bool(readable)
    if readable:
        ev = client_dir(a.slug) / "inputs" / f"seopress-settings-{now()[:10]}.json"
        ev.parent.mkdir(parents=True, exist_ok=True)
        ev.write_text(json.dumps(readable, indent=1))
        add(True, "SEOPress site-wide settings", f"readable — saved as audit evidence ({ev.name})")
    else:
        add(None, "SEOPress site-wide settings", "not readable as Editor (SEOPress needs an Administrator for these). "
            "Keep Editor: a one-time VA check for Jonie records title templates, sitemap settings, noindexed "
            "post types and SEOPress's own schema (Knowledge Graph) for the audit.")
        st_ = S.load(a.slug)
        if not st_.get("wordpress", {}).get("settings_check_issued"):
            state["needs_settings_handoff"] = True
    # 7 · must-use plugin + Kadence head-code field
    key = kadence_key(st)
    if not key:
        add(None, "Kadence head-code field (schema)", "meta key not set yet — found during the pilot "
            "(wp.py inspect on a page with head code), then `status.py set <slug> client.kadence_head_meta_key <key>` "
            "and the same key in the must-use plugin")
    elif made:
        meta = call(a.slug, f"wp/v2/pages/{made[0][1]['id']}?context=edit").get("meta") or {}
        if key in meta:
            add(True, "Must-use plugin + Kadence head-code field", f"'{key}' is exposed to the REST API")
            if a.pilot:
                try:
                    call(a.slug, f"wp/v2/pages/{made[0][1]['id']}", "POST", {"meta": {key: "<!-- seo-ops pilot -->"}})
                    back = (call(a.slug, f"wp/v2/pages/{made[0][1]['id']}?context=edit").get("meta") or {}).get(key)
                    add(back == "<!-- seo-ops pilot -->", "Head-code field write (pilot)",
                        "schema can be written and read back" if back == "<!-- seo-ops pilot -->" else "write did not read back")
                except WpError as e:
                    add(False, "Head-code field write (pilot)", f"failed ({e.code})")
        else:
            add(False, "Must-use plugin + Kadence head-code field", f"'{key}' is not exposed — push the must-use plugin "
                "with ManageWP and check the key (setup §4)")
    for ptype, d in made:
        try:
            call(a.slug, f"wp/v2/{ptype}/{d['id']}", "DELETE")
        except WpError:
            add(None, "Clean-up", f"could not trash test draft {d['id']} — trash it by hand")
    # pilot: a batch must have been published and verified on every field
    if a.pilot:
        verified = any(b.get("state") in ("verified", "written_back") for b in S.batches(S.load(a.slug))) or \
            any(p.get("type") == "blog" and p.get("verified") for p in S.load(a.slug)["pages"].values())
        add(verified, "Pilot: a published batch verified on every field",
            "yes" if verified else "not yet — ship a batch, let Jonie publish it, run the published check")
    if state.get("needs_settings_handoff"):
        issue_settings_check(a)
    passed = all(ok is not False for ok, _, _ in items)
    finish(passed)


def issue_settings_check(a):
    import csv
    import handoff
    d = client_dir(a.slug) / "handoffs"
    d.mkdir(exist_ok=True)
    tmp = d / "_seopress-settings.csv"
    rows = [("SEOPress → Titles & Metas", "title templates per post type, and which post types are set to noindex"),
            ("SEOPress → XML/HTML Sitemap", "is the sitemap on, which post types and taxonomies are in it"),
            ("SEOPress → Social Networks → Knowledge Graph", "is Organization/Person schema output on; name, logo, sameAs"),
            ("SEOPress → Advanced", "anything that changes canonical, attachment pages or redirects")]
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["url", "field", "old", "new", "reason", "decision_map_ref"])
        for where, what in rows:
            w.writerow([where, "screenshot or note", "", "(record what is set — change nothing)", what, "AUDIT-EVIDENCE"])
    sys.argv = ["handoff.py", "create", a.slug, "--run", a.run, "--kind", "seopress_settings",
                "--items", str(tmp.relative_to(ROOT)), "--title", "SEOPress Site-Wide Settings Check (one-time)"]
    try:
        handoff.main()
    except SystemExit as e:
        if e.code not in (0, None):
            raise
    tmp.unlink(missing_ok=True)
    st = S.load(a.slug)
    st.setdefault("wordpress", {})["settings_check_issued"] = now()
    S.save(a.slug, st)


def render_check(st, items, pilot):
    mark = {True: "OK  ", False: "FIX ", None: "NOTE"}
    out = [f"# WordPress {'pilot ' if pilot else ''}check — {st['client']['name']} — {now()[:16]}", ""]
    out += [f"- [{mark[ok]}] **{what}** — {detail}" for ok, what, detail in items]
    passed = all(ok is not False for ok, _, _ in items)
    out += ["", ("Result: **connected** — WordPress work can start." if passed and not pilot else
                 "Result: **pilot passed** — Paul may approve wordpress_pilot_approved; after that the system writes "
                 "titles, keyword, social, robots, canonical and schema directly." if passed else
                 "Result: **not connected** — fix the items marked FIX, then run /wp-check again. Nothing on the site was changed.")]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- commands
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("check"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--pilot", action="store_true")
    for n in ("get", "inspect"):
        s = sub.add_parser(n); s.add_argument("slug"); s.add_argument("url")
    s = sub.add_parser("media"); s.add_argument("slug"); s.add_argument("--post", type=int, required=True)
    s = sub.add_parser("redirects"); s.add_argument("slug")
    s = sub.add_parser("set"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--url", required=True); s.add_argument("--field", required=True, choices=sorted(FIELDS))
    s.add_argument("--value", required=True); s.add_argument("--expect", required=True)
    s = sub.add_parser("set-alt"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--media-id", type=int, required=True); s.add_argument("--alt", required=True)
    s.add_argument("--expect-alt", required=True)
    s = sub.add_parser("fix-content"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--url", required=True); s.add_argument("--kind", required=True, choices=["broken_link", "image_url"])
    s.add_argument("--old", required=True); s.add_argument("--new", required=True)
    s = sub.add_parser("set-head"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--url", required=True); s.add_argument("--file", required=True)
    s.add_argument("--expect-sha", required=True)
    s = sub.add_parser("restore"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--change", type=int, required=True)
    s = sub.add_parser("update-content"); s.add_argument("slug"); s.add_argument("rest", nargs=argparse.REMAINDER)
    for name in ("set", "set-alt", "fix-content", "set-head", "restore"):
        sub.choices[name].add_argument("--live", action="store_true")
        sub.choices[name].add_argument("--backup-confirmed")
    a = ap.parse_args()
    client_dir(a.slug)

    try:
        if a.cmd == "check":
            return wp_check(a)
        if a.cmd == "update-content":
            die("REFUSED — the system never replaces a live page's content or publishes. New and replacement content "
                "goes in as a WordPress draft from the approved file (publish.py drafts); Jonie publishes it.")
        if a.cmd == "get":
            kind, p = find(a.slug, a.url)
            s_ = seo_read(a.slug, p["id"]); s_.pop("raw")
            print(json.dumps({"type": kind, "id": p["id"], "status": p.get("status"), "slug": p.get("slug"),
                              "link": p.get("link"), "title": (p.get("title") or {}).get("raw"),
                              "content_sha": sha((p.get("content") or {}).get("raw")), "seopress": s_}, indent=1))
        elif a.cmd == "inspect":
            kind, p = find(a.slug, a.url)
            print(json.dumps({"id": p["id"], "meta_keys_exposed": sorted((p.get("meta") or {}).keys()),
                              "note": "Keys not registered with show_in_rest do not appear; the must-use plugin "
                                      "registers the Kadence head-code key once it is known."}, indent=1))
        elif a.cmd == "media":
            for md in call(a.slug, f"wp/v2/media?parent={a.post}&per_page=100&context=edit"):
                print(json.dumps({"id": md["id"], "file": md.get("source_url"), "alt": md.get("alt_text") or ""}))
        elif a.cmd == "redirects":
            print(json.dumps(call(a.slug, "seopress/v1/redirections"), indent=1))

        elif a.cmd == "set":
            kind = FIELDS[a.field][2]
            ptype, p = find(a.slug, a.url)
            require(a.slug, a.run, kind, post=p, live=a.live, backup=a.backup_confirmed)
            cur = seo_read(a.slug, p["id"])
            if cur[a.field] == a.value:
                log(a.slug, a.run, kind, a.url, a.field, cur[a.field], a.value, "SKIPPED — already correct")
                print("already correct"); return
            if cur[a.field] != a.expect:
                log(a.slug, a.run, kind, a.url, a.field, cur[a.field], a.value,
                    f"STOPPED — live value differs from what the audit recorded ({a.expect!r})")
                die("STOP — the page changed since the audit. Ask Paul.", 11)
            check_cap(a.slug, kind)
            seo_put(a.slug, p["id"], a.field, a.value, cur)
            after = seo_read(a.slug, p["id"])[a.field]
            log(a.slug, a.run, kind, a.url, a.field, cur[a.field], a.value,
                ("APPLIED · verified" if after == a.value else f"APPLIED · read-back FAILED ({after!r})")
                + live_note(p, a.backup_confirmed), ref=f"{ptype}:{p['id']}")
            print("done" if after == a.value else "applied, but the read-back differs — see the log")

        elif a.cmd == "set-alt":
            m = call(a.slug, f"wp/v2/media/{a.media_id}?context=edit")
            parent = None
            if m.get("post"):
                for ptype in ("pages", "posts"):
                    try:
                        parent = call(a.slug, f"wp/v2/{ptype}/{m['post']}?context=edit"); break
                    except WpError:
                        continue
            require(a.slug, a.run, "alt_text", post=parent, live=a.live, backup=a.backup_confirmed)
            url, cur = m.get("source_url", f"media:{a.media_id}"), m.get("alt_text") or ""
            if cur == a.alt:
                log(a.slug, a.run, "alt_text", url, "alt_text", cur, a.alt, "SKIPPED — already correct", ref=str(a.media_id))
            elif cur != a.expect_alt:
                log(a.slug, a.run, "alt_text", url, "alt_text", cur, a.alt, f"STOPPED — expected {a.expect_alt!r}", ref=str(a.media_id))
                die("STOP — the alt text changed since it was recorded. Ask Paul.", 11)
            else:
                check_cap(a.slug, "alt_text")
                call(a.slug, f"wp/v2/media/{a.media_id}", "POST", {"alt_text": a.alt})
                after = call(a.slug, f"wp/v2/media/{a.media_id}?context=edit").get("alt_text")
                log(a.slug, a.run, "alt_text", url, "alt_text", cur, a.alt,
                    ("APPLIED · verified" if after == a.alt else f"APPLIED · read-back FAILED ({after!r})")
                    + live_note(parent, a.backup_confirmed), ref=str(a.media_id))
            print("done")

        elif a.cmd == "fix-content":
            ptype, p = find(a.slug, a.url)
            require(a.slug, a.run, a.kind, post=p, live=a.live, backup=a.backup_confirmed)
            old_c = (p.get("content") or {}).get("raw") or ""
            if a.old not in old_c and a.new in old_c:
                log(a.slug, a.run, a.kind, a.url, "content", a.old, a.new, "SKIPPED — already correct")
                print("already correct"); return
            if a.old not in old_c:
                log(a.slug, a.run, a.kind, a.url, "content", a.old, a.new, "STOPPED — the old value is not on the page")
                die("STOP — the page changed since the audit (the old link/URL is not there). Ask Paul.", 11)
            check_cap(a.slug, a.kind)
            new_c = old_c.replace(a.old, a.new)
            snap = client_dir(a.slug) / "snapshots" / "_tmp_old.html"
            snap.write_text(old_c, encoding="utf-8")
            call(a.slug, f"wp/v2/{ptype}/{p['id']}", "POST", {"content": new_c})
            after = (call(a.slug, f"wp/v2/{ptype}/{p['id']}?context=edit").get("content") or {}).get("raw") or ""
            ok = a.old not in after and a.new in after
            log(a.slug, a.run, a.kind, a.url, "content", a.old, a.new,
                ("APPLIED · verified" if ok else "APPLIED · read-back FAILED") + live_note(p, a.backup_confirmed),
                ref=f"{ptype}:{p['id']}", old_file=str(snap))
            snap.unlink()
            print("done")

        elif a.cmd == "set-head":
            st = S.load(a.slug)
            key = kadence_key(st) or die("The Kadence head-code meta key is not known yet (found during the pilot).")
            ptype, p = find(a.slug, a.url)
            require(a.slug, a.run, "schema", post=p, live=a.live, backup=a.backup_confirmed)
            old = (p.get("meta") or {}).get(key, "") or ""
            new = open(a.file, encoding="utf-8").read()
            if sha(old) == sha(new):
                log(a.slug, a.run, "schema", a.url, key, f"sha {sha(old)}", f"sha {sha(new)}", "SKIPPED — already correct")
                return
            if sha(old) != a.expect_sha:
                log(a.slug, a.run, "schema", a.url, key, f"sha {sha(old)}", f"sha {sha(new)}", f"STOPPED — expected sha {a.expect_sha}")
                die("STOP — the head-code field changed since it was captured. Ask Paul.", 11)
            snap = client_dir(a.slug) / "snapshots" / "_tmp_old.txt"
            snap.write_text(old, encoding="utf-8")
            call(a.slug, f"wp/v2/{ptype}/{p['id']}", "POST", {"meta": {key: new}})
            after = (call(a.slug, f"wp/v2/{ptype}/{p['id']}?context=edit").get("meta") or {}).get(key, "")
            log(a.slug, a.run, "schema", a.url, key, f"sha {sha(old)}", f"sha {sha(new)}",
                ("APPLIED · verified" if sha(after) == sha(new) else "APPLIED · read-back FAILED") + live_note(p, a.backup_confirmed),
                ref=f"{ptype}:{p['id']}", old_file=str(snap), new_file=a.file)
            snap.unlink()

        elif a.cmd == "restore":
            restore(a)
    except WpError as e:
        die(f"WordPress error: {e}", 8)


def restore(a):
    R.open_run(a.slug, a.run)
    ch = next((c for c in R.changes(a.slug) if c["n"] == a.change), None) or die("no such change")
    if ch.get("channel") != "wp" or not ch["result"].startswith("APPLIED"):
        die(f"change #{a.change} was not applied by the system ({ch['result']}); nothing to restore.")
    k = ch["kind"]
    if k == "page_content" or k == "wp_check":
        m = re.search(r"draft id (\d+)(?: \((pages|posts)\))?", ch["new"]) or die("no WordPress id recorded")
        kind = m.group(2) or ("posts" if "post" in ch.get("field", "") else "pages")
        p = call(a.slug, f"wp/v2/{kind}/{m.group(1)}?context=edit")
        if p.get("status") != "draft":
            die(f"That draft (id {m.group(1)}) has since been {p.get('status')}; roll it back with a handoff to Jonie.")
        call(a.slug, f"wp/v2/{kind}/{p['id']}", "DELETE")
        log(a.slug, a.run, k, ch["url"], ch["field"], ch["new"], "(trashed)",
            f"ROLLED BACK change #{ch['n']} · draft moved to WordPress trash (recoverable)")
        print("restored"); return
    if k == "alt_text":
        mid = int(ch["ref"])
        cur = call(a.slug, f"wp/v2/media/{mid}?context=edit").get("alt_text") or ""
        if cur == ch["old"]:
            log(a.slug, a.run, k, ch["url"], "alt_text", cur, ch["old"], "SKIPPED — already restored", ref=ch["ref"]); return
        if cur != ch["new"]:
            die("STOP — the alt text changed again after our change. Ask Paul.", 11)
        call(a.slug, f"wp/v2/media/{mid}", "POST", {"alt_text": ch["old"]})
        log(a.slug, a.run, k, ch["url"], "alt_text", ch["new"], ch["old"], f"ROLLED BACK change #{ch['n']}", ref=ch["ref"])
        print("restored"); return
    ptype, p = find(a.slug, ch["url"])
    if p.get("status") == "publish" and not (a.live and a.backup_confirmed):
        die("This page is live: restoring needs --live and --backup-confirmed (a fresh ManageWP backup, confirmed by Paul).")
    field = ch["field"]
    if field in FIELDS:
        cur = seo_read(a.slug, p["id"])
        if cur[field] == ch["old"]:
            log(a.slug, a.run, k, ch["url"], field, cur[field], ch["old"], "SKIPPED — already restored"); return
        if cur[field] != ch["new"]:
            die("STOP — the value changed again after our change. Ask Paul.", 11)
        seo_put(a.slug, p["id"], field, ch["old"], cur)
        log(a.slug, a.run, k, ch["url"], field, ch["new"], ch["old"], f"ROLLED BACK change #{ch['n']}")
    elif ch.get("old_file"):
        old = (ROOT / ch["old_file"]).read_text(encoding="utf-8")
        if k == "schema":
            call(a.slug, f"wp/v2/{ptype}/{p['id']}", "POST", {"meta": {kadence_key(S.load(a.slug)): old}})
        else:
            cur = (p.get("content") or {}).get("raw") or ""
            if ch["new"] not in cur:
                die("STOP — the page changed again after our fix. Ask Paul.", 11)
            call(a.slug, f"wp/v2/{ptype}/{p['id']}", "POST", {"content": old})
        log(a.slug, a.run, k, ch["url"], field, ch["new"], ch["old"], f"ROLLED BACK change #{ch['n']}")
    else:
        die(f"change #{a.change} has nothing to restore from")
    print("restored")


if __name__ == "__main__":
    main()
