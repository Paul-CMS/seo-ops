#!/usr/bin/env python3
"""Fakes for the test suite: run a real seo-ops script with WordPress, DataforSEO and the public
web replaced by local fakes. No network, no cost, no credentials.

    python3 tests/fakes.py <script> [args...]        e.g. tests/fakes.py wp create-draft <slug> ...

State lives in tests/.state/ inside the sandbox copy (never in the real repo):
  wp.json     pages/posts (status, slug, title, content, SEOPress meta), media, redirects
  dfs.json    balance and the cost each call returns
The fake web serves published pages from wp.json (title, meta description, content) and answers
redirects from wp.json "redirects", so verify.py can check live pages.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
STATE = ROOT / "tests" / ".state"
WP = STATE / "wp.json"
DFS = STATE / "dfs.json"
MODE = STATE / "wp_mode.json"   # failure modes: rest_blocked, bad_password, role, no_seopress, settings_readable


def mode():
    return json.loads(MODE.read_text()) if MODE.exists() else {}


class FakeErr(Exception):
    pass


def err(code, body=""):
    import wp
    raise wp.WpError(f"fake HTTP {code} {body}", code, body)
BASE = "https://test.example"


def load_wp():
    if WP.exists():
        return json.loads(WP.read_text())
    return {"next_id": 100, "redirects": {},
            "items": {"1": {"id": 1, "type": "pages", "slug": "", "status": "publish", "link": BASE + "/",
                            "title": {"raw": "Home"}, "content": {"raw": "<p>home</p>"}, "meta": {}},
                      "2": {"id": 2, "type": "pages", "slug": "roof-repair", "status": "publish",
                            "link": BASE + "/roof-repair/", "title": {"raw": "Roof Repair"},
                            "content": {"raw": "<p>old roof repair copy</p>"}, "meta": {}}},
            "media": {"55": {"id": 55, "source_url": BASE + "/wp-content/uploads/roof.jpg", "alt_text": "",
                             "post": 2}},
            "seo": {"2": {"title": "Roof Repair | Test", "description": "old desc"}}}


def save_wp(s):
    STATE.mkdir(parents=True, exist_ok=True)
    WP.write_text(json.dumps(s, indent=1))


def wp_call(slug, path, method="GET", body=None, auth=True):
    s = load_wp()
    md_ = mode()
    p, q = (path.split("?") + [""])[:2]
    p = p.strip("/")
    if md_.get("rest_blocked"):
        err(403, "<html>Forbidden by security plugin</html>")
    if p == "":
        ns = ["wp/v2"] + ([] if md_.get("no_seopress") else ["seopress/v1"])
        return {"name": "Test site", "namespaces": ns}
    if auth and md_.get("bad_password"):
        err(401, '{"code":"incorrect_password"}')
    if p == "wp/v2/users/me":
        return {"slug": "seo-ops", "name": "seo-ops", "roles": [md_.get("role", "editor")]}
    if p.startswith("seopress/") and md_.get("no_seopress"):
        err(404, '{"code":"rest_no_route"}')
    if p.startswith("seopress/v1/options/"):
        if md_.get("settings_readable"):
            return {"titles": {"post": "%%post_title%% - %%sitename%%"}}
        err(403, '{"code":"rest_forbidden"}')
    if p == "wp/v2/settings":
        return {"page_on_front": 1}
    m = re.match(r"wp/v2/(pages|posts)$", p)
    if m and method == "GET":
        sm = re.search(r"slug=([^&]+)", q)
        return [i for i in s["items"].values() if sm and i["slug"] == sm.group(1) and i["type"] == m.group(1)]
    if m and method == "POST":
        if md_.get("role") in ("contributor",):
            err(403, '{"code":"rest_cannot_create"}')
        n = s["next_id"]; s["next_id"] += 1
        slug_ = body.get("slug") or f"draft-{n}"
        s["items"][str(n)] = {"id": n, "type": m.group(1), "slug": slug_, "status": body["status"],
                              "link": f"{BASE}/?{'p' if m.group(1) == 'posts' else 'page_id'}={n}",
                              "title": {"raw": body["title"]}, "content": {"raw": body["content"]},
                              "meta": {}}
        save_wp(s); return s["items"][str(n)]
    m = re.match(r"wp/v2/(pages|posts)/(\d+)$", p)
    if m:
        it = s["items"].get(m.group(2))
        if not it or it["type"] != m.group(1):
            raise RuntimeError(f"fake WP 404 {method} {path}")
        if md_.get("mu_plugin_key"):            # the must-use plugin exposes the Kadence head-code key
            it["meta"].setdefault(md_["mu_plugin_key"], "")
        if method == "POST":
            if "content" in body: it["content"]["raw"] = body["content"]
            if "meta" in body: it["meta"].update(body["meta"])
            if "slug" in body: it["slug"] = body["slug"]
        if method == "DELETE":
            it["status"] = "trash"
        save_wp(s); return it
    m = re.match(r"wp/v2/media/(\d+)$", p)
    if m:
        md = s["media"][m.group(1)]
        if method == "POST":
            md["alt_text"] = body["alt_text"]; save_wp(s)
        return md
    if p == "wp/v2/media" and method == "GET":
        pm = re.search(r"parent=(\d+)", q)
        return [md for md in s["media"].values() if pm and str(md.get("post")) == pm.group(1)]
    m = re.match(r"seopress/v1/posts/(\d+)(?:/([a-z-]+))?$", p)
    if m:
        cur = s["seo"].setdefault(m.group(1), {"title": "", "description": ""})
        if method == "PUT":
            if md_.get("role") in ("author", "contributor"):
                err(403, '{"code":"rest_forbidden"}')
            cur.update(body); save_wp(s)
            return dict(cur)
        # public GET, shaped like SEOPress's response
        return {"title": cur.get("title", ""), "description": cur.get("description", ""),
                "canonical": cur.get("_seopress_robots_canonical", ""),
                "target_keywords": cur.get("_seopress_analysis_target_kw", ""),
                "og": {"title": cur.get("_seopress_social_fb_title", ""), "description": cur.get("_seopress_social_fb_desc", "")},
                "twitter": {"title": cur.get("_seopress_social_twitter_title", ""),
                            "description": cur.get("_seopress_social_twitter_desc", "")},
                "robots": {"noindex": cur.get("_seopress_robots_index") == "yes",
                           "nofollow": cur.get("_seopress_robots_follow") == "yes"}}
    if p == "seopress/v1/redirections":
        return [{"from": k, "to": v} for k, v in s["redirects"].items()]
    raise RuntimeError(f"fake WP: unhandled {method} {path}")


def web_fetch(url, follow=True):
    """Public web: published items render title/meta/content; redirects answer 301."""
    s = load_wp()
    u = url.rstrip("/") + "/"
    if u in s["redirects"]:
        loc = s["redirects"][u]
        if not follow:
            return 301, {"Location": loc}, ""
        return web_fetch(loc)
    for i in s["items"].values():
        if i["status"] == "publish" and (i["link"].rstrip("/") + "/") == u:
            seo = s["seo"].get(str(i["id"]), {})
            og = "".join(f'<meta property="og:{k}" content="{seo.get(v, "")}">' for k, v in
                         (("title", "_seopress_social_fb_title"), ("description", "_seopress_social_fb_desc")))
            tw = "".join(f'<meta name="twitter:{k}" content="{seo.get(v, "")}">' for k, v in
                         (("title", "_seopress_social_twitter_title"), ("description", "_seopress_social_twitter_desc")))
            body = (f"<html><head><title>{seo.get('title', '')}</title>"
                    f"<meta name=\"description\" content=\"{seo.get('description', '')}\">{og}{tw}</head><body>"
                    f"<h1>{i['title']['raw']}</h1>{i['content']['raw']}</body></html>")
            return 200, {}, body
    return 404, {}, ""


def dfs_request(endpoint, body=None, method=None, timeout=90, retries=3):
    cfg = json.loads(DFS.read_text()) if DFS.exists() else {}
    if endpoint.startswith("ai_optimization/"):   # the LLM fan-out answer: a JSON array inside a message
        qs = ["how much does roof repair cost", "roof repair near me", "signs you need a new roof",
              "Roof repair near me", "how long does a roof repair take"]
        return {"status_code": 20000, "cost": cfg.get("cost", 0.003),
                "tasks": [{"status_code": 20000, "result": [{"items": [{"type": "message", "sections": [
                    {"type": "text", "text": json.dumps(qs)}]}], "fan_out_queries": []}]}]}
    if endpoint.startswith("appendix/user_data"):
        return {"status_code": 20000, "tasks": [{"status_code": 20000,
                "result": [{"money": {"balance": cfg.get("balance", 10.0)}}]}]}
    return {"status_code": 20000, "cost": cfg.get("cost", 0.0123),
            "tasks": [{"status_code": 20000, "id": "fake-task", "result": [{"items": [], "total_count": 0}]}]}


def install():
    import dfs
    dfs.request = dfs_request
    try:
        import wp
        wp.call = wp_call

        def creds(slug):
            if mode().get("no_creds"):
                wp.die(f"{wp.env_prefix(slug)}_URL / _USER / _APP_PASSWORD are missing from .env.")
            return BASE, "Basic fake"
        wp.creds = creds
    except SystemExit:
        pass
    try:
        import verify
        verify.fetch = web_fetch
    except ImportError:
        pass


if __name__ == "__main__":
    name, args = sys.argv[1], sys.argv[2:]
    install()
    mod = __import__(name)
    sys.argv = [f"scripts/{name}.py", *args]
    mod.main()
