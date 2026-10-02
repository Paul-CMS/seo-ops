#!/usr/bin/env python3
"""wp.py — WordPress REST client (SEOPress + Kadence). Every write is checked and logged.

Read (no run needed):
    wp.py get <slug> <url>                 page id, status, slug, title, SEOPress title/description
    wp.py inspect <slug> <url>             all post meta keys (pilot: find the Kadence head-code key)
    wp.py redirects <slug>                 SEOPress redirect list (for /verify)

Write (need an open run, the right gate, and the current value to match what we expect):
    wp.py set-seo <slug> --run R --url U [--title T --expect-title OLD] [--desc D --expect-desc OLD]
    wp.py set-alt <slug> --run R --media-id N --alt T --expect-alt OLD
    wp.py create-draft <slug> --run R --page-id P --title T --content-file F [--slug S] [--parent N]
    wp.py update-content <slug> --run R --page-id P --url U --content-file F --expect-sha OLD
                          --live --backup-confirmed "ManageWP backup <time>, confirmed by Paul"
    wp.py set-head <slug> --run R --url U --file F --expect-sha OLD        (schema into Kadence head field)
    wp.py restore <slug> --run R --change N        (used by /rollback: put the logged old value back)

Rules enforced here, not just in the prompts:
  - SEO titles/descriptions and the Kadence head field are blocked until config.json
    wp_pilot_done is true. Until then they go out as VA handoffs (handoff.py).
  - Slugs and redirects are never changed here. Always a VA handoff.
  - If the live value already equals the new value -> logged as SKIPPED (already done).
  - If the live value differs from the expected old value -> STOP; the page changed since
    the audit and Paul decides.
  - Published content changes only with --live and a recorded ManageWP backup confirmation.

Credentials: WP_<PREFIX>_URL / _USER / _APP_PASSWORD in .env, prefix in status.json
client.wp_env_prefix. Never printed.
"""
import argparse
import base64
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

import run as R
import status as S
from lib import ROOT, client_dir, config, die, load_env, redact

GATES = S.GATES


class WpError(Exception):
    pass


def creds(slug):
    st = S.load(slug)
    pre = st["client"].get("wp_env_prefix")
    if not pre:
        die(f"No WordPress prefix set. status.py set {slug} client.wp_env_prefix ACME  "
            "(then Paul adds WP_ACME_URL / _USER / _APP_PASSWORD to .env).")
    env = load_env()
    base, user, pw = (env.get(f"WP_{pre}_URL"), env.get(f"WP_{pre}_USER"),
                      env.get(f"WP_{pre}_APP_PASSWORD"))
    if not (base and user and pw):
        die(f"WP_{pre}_URL / _USER / _APP_PASSWORD missing from .env. Paul types them in himself.")
    return base.rstrip("/"), "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()


def call(slug, path, method="GET", body=None, auth=True):
    base, header = creds(slug)
    url = f"{base}/wp-json/{path.lstrip('/')}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json",
                                          **({"Authorization": header} if auth else {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise WpError(redact(f"{method} {path}: HTTP {e.code} {e.read().decode()[:300]}"))
    except urllib.error.URLError as e:
        raise WpError(redact(f"{method} {path}: {e}"))


def sha(text):
    return hashlib.sha256((text or "").encode()).hexdigest()[:12]


def find(slug, url):
    """Resolve a public URL to (post_type, post) with edit context."""
    path = urllib.parse.urlparse(url).path.strip("/")
    leaf = path.split("/")[-1] if path else ""
    for kind in ("pages", "posts"):
        if not leaf:
            front = call(slug, "wp/v2/settings").get("page_on_front")
            if front:
                return "pages", call(slug, f"wp/v2/pages/{front}?context=edit")
            continue
        res = call(slug, f"wp/v2/{kind}?slug={urllib.parse.quote(leaf)}&context=edit&status=any")
        for p in res:
            if p.get("link", "").rstrip("/").endswith(path) or len(res) == 1:
                return kind, p
    raise WpError(f"No page or post found for {url}")


def seo(slug, post_id):
    r = call(slug, f"seopress/v1/posts/{post_id}")
    return {"title": r.get("title") or r.get("_seopress_titles_title") or "",
            "desc": r.get("description") or r.get("_seopress_titles_desc") or "", "raw": r}


# ---------------------------------------------------------------- guards
def require(slug, run_id, kind, page_id=None):
    R.open_run(slug, run_id)
    st = S.load(slug)
    spec = GATES["change_kinds"][kind]
    if spec["channel"] == "handoff":
        die(f"{kind} is never changed by the system. Issue a VA handoff (handoff.py).")
    if spec["channel"] == "wp_after_pilot" and not config().get("wp_pilot_done"):
        die(f"{kind}: the WordPress pilot is not done yet, so this goes out as a VA handoff "
            "(handoff.py). config.json wp_pilot_done flips only after Paul approves the pilot.")
    gate = spec["gate"]
    if gate == "page_approval":
        ok, why = S.page_approved(st, page_id or "")
        if not ok:
            die(f"REFUSED — {why}", 4)
    else:
        ok, rs = S.gate_met(st, gate)
        if not ok:
            die(f"REFUSED — {S.label(gate)}: " + "; ".join(rs), 4)


def log(slug, run_id, kind, url, field, old, new, result, **kw):
    return R.log_change(slug, run_id, kind, url, field, old, new, result, channel="wp", **kw)


# ---------------------------------------------------------------- commands
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("get", "inspect"):
        s = sub.add_parser(n); s.add_argument("slug"); s.add_argument("url")
    s = sub.add_parser("redirects"); s.add_argument("slug")
    s = sub.add_parser("set-seo"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--url", required=True); s.add_argument("--title"); s.add_argument("--expect-title")
    s.add_argument("--desc"); s.add_argument("--expect-desc")
    s = sub.add_parser("set-alt"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--media-id", type=int, required=True); s.add_argument("--alt", required=True)
    s.add_argument("--expect-alt", required=True)
    s = sub.add_parser("create-draft"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--page-id", required=True); s.add_argument("--title", required=True)
    s.add_argument("--content-file", required=True); s.add_argument("--slug-name"); s.add_argument("--parent", type=int)
    s = sub.add_parser("update-content"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--page-id", required=True); s.add_argument("--url", required=True)
    s.add_argument("--content-file", required=True); s.add_argument("--expect-sha", required=True)
    s.add_argument("--live", action="store_true"); s.add_argument("--backup-confirmed")
    s = sub.add_parser("set-head"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--url", required=True); s.add_argument("--file", required=True)
    s.add_argument("--expect-sha", required=True)
    s = sub.add_parser("restore"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s.add_argument("--change", type=int, required=True)
    a = ap.parse_args()
    client_dir(a.slug)

    try:
        if a.cmd == "get":
            kind, p = find(a.slug, a.url)
            s_ = seo(a.slug, p["id"])
            print(json.dumps({"type": kind, "id": p["id"], "status": p.get("status"), "slug": p.get("slug"),
                              "link": p.get("link"), "modified": p.get("modified"),
                              "title": (p.get("title") or {}).get("raw"),
                              "content_sha": sha((p.get("content") or {}).get("raw")),
                              "seo_title": s_["title"], "seo_desc": s_["desc"]}, indent=1))
        elif a.cmd == "inspect":
            kind, p = find(a.slug, a.url)
            print(json.dumps({"id": p["id"], "meta_keys_exposed": sorted((p.get("meta") or {}).keys()),
                              "note": "Keys not registered with show_in_rest do not appear here; the "
                                      "must-use plugin registers the Kadence head-code key once known."}, indent=1))
        elif a.cmd == "redirects":
            print(json.dumps(call(a.slug, "seopress/v1/redirections"), indent=1))

        elif a.cmd == "set-seo":
            kinds = (["seo_title"] if a.title is not None else []) + (["meta_description"] if a.desc is not None else [])
            if not kinds:
                die("nothing to set")
            for k in kinds:
                require(a.slug, a.run, k)
            _, p = find(a.slug, a.url)
            cur = seo(a.slug, p["id"])
            body = {"title": cur["title"], "description": cur["desc"]}
            for k, new, exp, field in (("seo_title", a.title, a.expect_title, "title"),
                                       ("meta_description", a.desc, a.expect_desc, "desc")):
                if new is None:
                    continue
                if cur[field] == new:
                    log(a.slug, a.run, k, a.url, field, cur[field], new, "SKIPPED — already done")
                    continue
                if exp is None or cur[field] != exp:
                    log(a.slug, a.run, k, a.url, field, cur[field], new,
                        f"STOPPED — live value differs from expected '{exp}'")
                    die("STOP — the live value is not what the audit recorded. Ask Paul.", 11)
                body["title" if field == "title" else "description"] = new
            if body != {"title": cur["title"], "description": cur["desc"]}:
                call(a.slug, f"seopress/v1/posts/{p['id']}/title-description-metas", "PUT", body)
                after = seo(a.slug, p["id"])
                for k, new, field in (("seo_title", a.title, "title"), ("meta_description", a.desc, "desc")):
                    if new is not None and cur[field] != new:
                        log(a.slug, a.run, k, a.url, field, cur[field], new,
                            "APPLIED · verified" if after[field] == new else f"APPLIED · verify FAILED (now '{after[field]}')")
            print("done")

        elif a.cmd == "set-alt":
            require(a.slug, a.run, "alt_text")
            m = call(a.slug, f"wp/v2/media/{a.media_id}?context=edit")
            url = m.get("source_url", f"media:{a.media_id}")
            cur = m.get("alt_text") or ""
            if cur == a.alt:
                log(a.slug, a.run, "alt_text", url, "alt_text", cur, a.alt, "SKIPPED — already done", ref=str(a.media_id))
            elif cur != a.expect_alt:
                log(a.slug, a.run, "alt_text", url, "alt_text", cur, a.alt, f"STOPPED — expected '{a.expect_alt}'", ref=str(a.media_id))
                die("STOP — live alt text is not what the audit recorded. Ask Paul.", 11)
            else:
                call(a.slug, f"wp/v2/media/{a.media_id}", "POST", {"alt_text": a.alt})
                after = call(a.slug, f"wp/v2/media/{a.media_id}?context=edit").get("alt_text")
                log(a.slug, a.run, "alt_text", url, "alt_text", cur, a.alt,
                    "APPLIED · verified" if after == a.alt else f"APPLIED · verify FAILED ('{after}')", ref=str(a.media_id))
            print("done")

        elif a.cmd == "create-draft":
            require(a.slug, a.run, "page_content", a.page_id)
            content = open(a.content_file, encoding="utf-8").read()
            body = {"title": a.title, "content": content, "status": "draft"}
            if a.slug_name:
                body["slug"] = a.slug_name
            if a.parent:
                body["parent"] = a.parent
            p = call(a.slug, "wp/v2/pages", "POST", body)
            log(a.slug, a.run, "page_content", p.get("link", ""), "new draft page", "(none)",
                f"draft id {p['id']} · content sha {sha(content)}", "APPLIED · draft only (not live)",
                ref=a.page_id, new_file=a.content_file)
            print(f"draft created: id {p['id']}")

        elif a.cmd == "update-content":
            require(a.slug, a.run, "page_content", a.page_id)
            _, p = find(a.slug, a.url)
            if p.get("status") == "publish" and not (a.live and a.backup_confirmed):
                die("This page is live. Publishing a content change needs --live and "
                    "--backup-confirmed (Paul confirms a fresh ManageWP backup first).")
            old = (p.get("content") or {}).get("raw") or ""
            new = open(a.content_file, encoding="utf-8").read()
            if sha(old) == sha(new):
                log(a.slug, a.run, "page_content", a.url, "content", f"sha {sha(old)}", f"sha {sha(new)}",
                    "SKIPPED — already done")
                print("already done"); return
            if sha(old) != a.expect_sha:
                log(a.slug, a.run, "page_content", a.url, "content", f"sha {sha(old)}", f"sha {sha(new)}",
                    f"STOPPED — expected sha {a.expect_sha}")
                die("STOP — the live content changed since it was captured. Ask Paul.", 11)
            snap = client_dir(a.slug) / "snapshots" / "_tmp_old.html"
            snap.write_text(old, encoding="utf-8")
            call(a.slug, f"wp/v2/pages/{p['id']}", "POST", {"content": new})
            after = call(a.slug, f"wp/v2/pages/{p['id']}?context=edit")
            ok = sha((after.get("content") or {}).get("raw")) == sha(new)
            log(a.slug, a.run, "page_content", a.url, "content", f"sha {sha(old)}", f"sha {sha(new)}",
                ("APPLIED LIVE · verified" if ok else "APPLIED LIVE · verify FAILED")
                + f" · backup: {a.backup_confirmed}", ref=a.page_id, old_file=str(snap), new_file=a.content_file)
            snap.unlink()
            print("done")

        elif a.cmd == "set-head":
            require(a.slug, a.run, "schema")
            key = config().get("kadence_head_meta_key")
            if not key:
                die("The Kadence head-code meta key is not known yet (read it during the WordPress pilot).")
            kind, p = find(a.slug, a.url)
            old = (p.get("meta") or {}).get(key, "")
            new = open(a.file, encoding="utf-8").read()
            if sha(old) == sha(new):
                log(a.slug, a.run, "schema", a.url, key, f"sha {sha(old)}", f"sha {sha(new)}", "SKIPPED — already done")
                return
            if sha(old) != a.expect_sha:
                die("STOP — the head field changed since it was captured. Ask Paul.", 11)
            snap = client_dir(a.slug) / "snapshots" / "_tmp_old.txt"
            snap.write_text(old or "", encoding="utf-8")
            call(a.slug, f"wp/v2/{kind}/{p['id']}", "POST", {"meta": {key: new}})
            log(a.slug, a.run, "schema", a.url, key, f"sha {sha(old)}", f"sha {sha(new)}", "APPLIED",
                old_file=str(snap), new_file=a.file)
            snap.unlink()

        elif a.cmd == "restore":
            R.open_run(a.slug, a.run)
            ch = next((c for c in R.changes(a.slug) if c["n"] == a.change), None) or die("no such change")
            if ch.get("channel") != "wp" or not ch["result"].startswith("APPLIED"):
                die(f"change #{a.change} was not applied by the system ({ch['result']}); nothing to restore.")
            if ch["kind"] in ("seo_title", "meta_description"):
                _, p = find(a.slug, ch["url"])
                cur = seo(a.slug, p["id"])
                field = "title" if ch["kind"] == "seo_title" else "desc"
                if cur[field] == ch["old"]:
                    log(a.slug, a.run, ch["kind"], ch["url"], field, cur[field], ch["old"], "SKIPPED — already restored")
                    return
                if cur[field] != ch["new"]:
                    die("STOP — the live value changed again after our change. Ask Paul.", 11)
                body = {"title": cur["title"], "description": cur["desc"]}
                body["title" if field == "title" else "description"] = ch["old"]
                call(a.slug, f"seopress/v1/posts/{p['id']}/title-description-metas", "PUT", body)
                log(a.slug, a.run, ch["kind"], ch["url"], field, ch["new"], ch["old"], f"ROLLED BACK change #{ch['n']}")
            elif ch["kind"] == "alt_text":
                mid = int(ch["ref"])
                cur = call(a.slug, f"wp/v2/media/{mid}?context=edit").get("alt_text") or ""
                if cur == ch["old"]:
                    log(a.slug, a.run, "alt_text", ch["url"], "alt_text", cur, ch["old"], "SKIPPED — already restored", ref=ch["ref"])
                    return
                if cur != ch["new"]:
                    die("STOP — the live alt text changed again after our change. Ask Paul.", 11)
                call(a.slug, f"wp/v2/media/{mid}", "POST", {"alt_text": ch["old"]})
                log(a.slug, a.run, "alt_text", ch["url"], "alt_text", ch["new"], ch["old"],
                    f"ROLLED BACK change #{ch['n']}", ref=ch["ref"])
            elif ch["kind"] in ("page_content", "schema") and ch.get("old_file"):
                old = (ROOT / ch["old_file"]).read_text(encoding="utf-8")
                kind, p = find(a.slug, ch["url"])
                if ch["kind"] == "page_content":
                    call(a.slug, f"wp/v2/{kind}/{p['id']}", "POST", {"content": old})
                else:
                    call(a.slug, f"wp/v2/{kind}/{p['id']}", "POST", {"meta": {config()['kadence_head_meta_key']: old}})
                log(a.slug, a.run, ch["kind"], ch["url"], ch["field"], ch["new"], ch["old"],
                    f"ROLLED BACK change #{ch['n']}")
            elif ch["kind"] == "page_content":
                kind, p = find(a.slug, ch["url"])
                if p.get("status") != "draft":
                    die("That draft has since been published; Paul decides how to roll it back.")
                call(a.slug, f"wp/v2/{kind}/{p['id']}", "DELETE")
                log(a.slug, a.run, "page_content", ch["url"], "draft page", ch["new"], "(trashed)",
                    f"ROLLED BACK change #{ch['n']} · draft moved to WordPress trash (recoverable)")
            print("restored")
    except WpError as e:
        die(f"WordPress error: {e}", 8)


if __name__ == "__main__":
    main()
