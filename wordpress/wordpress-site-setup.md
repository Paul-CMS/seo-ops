# WordPress site setup — and what seo-ops does on a site

The complete WordPress spec. Code: `scripts/wp.py` (every call), `scripts/publish.py` (drafts and the
publish handoff), `scripts/verify.py` (read-back), `wordpress/mu-plugins/seo-ops-head-meta.php`.
Command: `/wp-check <client>`. No connector plugin — the WordPress REST API, directly.

## 1 · The seo-ops user (once per site — Jonie or Paul)

1. In wp-admin → Users → Add New: a dedicated user `seo-ops`, role **Editor** (never Administrator).
2. Users → `seo-ops` → Application Passwords → name it `seo-ops` → copy the password once.
3. Paul adds three lines to `.env` (never in chat). `<SLUG>` is the client slug in capitals with
   hyphens as underscores — `red-rover-roofing` → `RED_ROVER_ROOFING`:
   ```
   WP_<SLUG>_URL=https://example.com
   WP_<SLUG>_USER=seo-ops
   WP_<SLUG>_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
   ```
   The `.env` guard blocks Claude from reading, searching or listing these.

## 2 · Requirements

- **SEOPress 6.8 or later** (free is enough): 6.8 is the first version whose REST API accepts
  Application Passwords. Its per-page endpoints are used for title + meta description, target
  keyword, social (Open Graph + X), and meta robots + canonical.
- Permalinks not set to "Plain" (the REST API lives at `/wp-json/`).
- Kadence theme (head-code field for schema — §4).

## 3 · If /wp-check says the REST API or the login is blocked

- **REST API blocked** (403 / a web page instead of JSON): a security plugin — Wordfence, Solid
  Security (iThemes), All In One WP Security, "Disable REST API" — or the host firewall (ModSecurity,
  Cloudflare WAF). Allow `/wp-json/` for logged-in requests / the `seo-ops` user.
- **Application Password rejected** (401): wrong password; Application Passwords switched off by a
  security plugin; or the host strips the `Authorization` header (Apache/CGI). For the last one, add to
  `.htaccess` above the WordPress block:
  `SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1`

## 4 · The must-use plugin (schema in the Kadence head-code field)

`wordpress/mu-plugins/seo-ops-head-meta.php` exposes Kadence's per-page head-code field to the REST API
so schema can be written per page. Push it with **ManageWP** to `wp-content/mu-plugins/`. Its meta key
is found during the pilot: put head code on one page in the Kadence editor, run
`wp.py inspect <slug> <url>`, then set the key in the plugin (`SEO_OPS_HEAD_META_KEY`) and in seo-ops:
`status.py set <slug> client.kadence_head_meta_key <key>`. Never guess the key.

## 5 · /wp-check and the pilot

`/wp-check <client>` (no change to the site except two test drafts it trashes) reports in plain words:
credentials · REST API reachable · login and Editor role · draft page + draft post creation · SEOPress
6.8+ per-page fields written and read back on a test draft · site-wide SEOPress settings readable? ·
must-use plugin + Kadence head-code field. A pass meets the condition **WordPress connected** (valid
30 days); every WordPress step requires it, and `/next` runs the check before the first one.

**Site-wide SEOPress settings** (title templates, sitemap, post types set to noindex, Knowledge Graph
schema) need an Administrator, so as Editor they are normally not readable: keep Editor, and the check
issues a **one-time VA check** to Jonie that records them as audit evidence. If they are readable, they
are saved as evidence instead. They are never changed by the system — any change is a VA handoff.

**Pilot (per site):** `/wp-check <client> --pilot` = everything above + a head-code write/read-back +
at least one batch published by Jonie and verified on every field. When it passes, Paul approves
`wordpress_pilot_approved` for that site.

| | Before the pilot | After the pilot |
|---|---|---|
| New page/post drafts (all fields: slug, content, title, meta, keyword, social) | system | system |
| Safe fixes on existing pages: alt text, broken links / image URLs in content, meta descriptions | system | system |
| Structural fixes on existing pages: title, keyword, social, meta robots, canonical, schema | VA handoff (Jonie) | system |
| Publishing, redirects, menus, SEOPress site-wide settings | VA handoff (Jonie) | VA handoff (Jonie) |

## 6 · What the system writes, behind which gate

| Change | Gate | How |
|---|---|---|
| New page / post (draft) | the batch's drafts approval (posts: the post's approval) | `publish.py drafts` — status `draft`, exact slug, blocks, link tables from the wheel, SEOPress title/meta/keyword/social; robots and canonical left at SEOPress defaults |
| Meta description, alt text, broken link, image URL | audit approved (safe fixes) | `wp.py set` / `set-alt` / `fix-content` |
| Title, keyword, social, meta robots, canonical | entity + Brand Guide approved (structural) + pilot | `wp.py set` |
| Schema (Kadence head-code field) | structural + pilot | `wp.py set-head` |

Every change: the current value is read first; already correct → skipped; different from what the audit
recorded → stop; logged with URL, old, new and result. **Any change to an already-published page needs
`--live` and Paul's confirmation of a fresh ManageWP backup** (recorded in the log). `/rollback` restores
from the log (`wp.py restore`, same `--live` rule); `/verify` reads everything back.

## 7 · Publishing — the system never publishes

One **publish handoff to Jonie per batch** (and per blog post): draft links; apply the Kadence layout and
styling, add images, publish at exactly the URL given. **Do not change** the wording, headings, title,
meta description, target keyword or URL — an unavoidable change goes in the CSV as `deviated` with a
reason. A page that replaces an existing URL has its 301 on the same handoff, done together with the
publish. Menu changes: a navigation handoff to Jonie. Redirects are always a handoff (full from URL, full
to URL, 301, reason, URL Decision Map reference) and `/verify` checks them.

After Jonie returns the worksheet, `/verify` checks each live page against its approved file — URL,
SEO title, meta, target keyword, Open Graph and X, H1, heading structure, content, link-table links —
and every difference goes to Paul. Then alt text for the images Jonie added (a safe fix; the page is
live, so Paul confirms a backup first). The QA crawl covers published pages only.

## 8 · Duplicate schema

If SEOPress outputs its own site-wide schema (Knowledge Graph — Organization/Person) that overlaps the
hand-built schema, the audit reports it as a finding (schema readiness); turning it off is a VA handoff.
