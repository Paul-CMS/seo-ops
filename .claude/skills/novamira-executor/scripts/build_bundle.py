#!/usr/bin/env python3
"""
build_bundle.py — validate a client handoff and build the executor bundle.

Usage:
    python3 build_bundle.py <client-handoff-folder>

Reads:   <folder>/handoff.json and <folder>/content/*.md
Writes:  <folder>/out/bundle.json          (uploaded to the site, read by cms-executor.php)
         <folder>/out/HANDOFF-REVIEW.md     (for Paul / the VA: what will change)
Exit 0 = valid, 1 = errors (bundle not written).

No model tokens are spent here: run it with bash, read only the last lines of output.
"""
import html
import json
import re
import sys
from pathlib import Path

STATE_ABBR = r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b"
ACTIONS = {"create", "update"}
ROUTES = {"build", "spo", "meta_only"}


# --------------------------------------------------------------------------- #
# Markdown -> Gutenberg core blocks                                            #
# --------------------------------------------------------------------------- #

def inline(text: str) -> str:
    """Escape, then apply **bold**, *italic*, [text](url)."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t


def heading(level: int, text: str) -> str:
    attrs = "" if level == 2 else f' {{"level":{level}}}'
    return f'<!-- wp:heading{attrs} -->\n<h{level} class="wp-block-heading">{inline(text)}</h{level}>\n<!-- /wp:heading -->'


def paragraph(text: str) -> str:
    return f"<!-- wp:paragraph -->\n<p>{inline(text)}</p>\n<!-- /wp:paragraph -->"


def list_block(items, ordered: bool) -> str:
    tag = "ol" if ordered else "ul"
    attrs = ' {"ordered":true}' if ordered else ""
    lis = "".join(f"<!-- wp:list-item -->\n<li>{inline(i)}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list{attrs} -->\n<{tag} class="wp-block-list">{lis}</{tag}>\n<!-- /wp:list -->'


def table_block(rows) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return ('<!-- wp:table {"hasFixedLayout":false} -->\n<figure class="wp-block-table"><table>'
            f"<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></figure>\n<!-- /wp:table -->")


def md_to_blocks(md: str):
    """Returns (blocks_html, stats). Supports ## / ### / ####, paragraphs, - and 1. lists, pipe tables."""
    blocks, para, lst, ordered, tbl = [], [], [], False, []
    stats = {"h1": 0, "h2": 0, "h3": 0, "tables": 0, "words": 0, "placeholders": 0}

    def flush():
        nonlocal para, lst, tbl
        if para:
            blocks.append(paragraph(" ".join(para)))
            para = []
        if lst:
            blocks.append(list_block(lst, ordered))
            lst = []
        if tbl:
            blocks.append(table_block(tbl))
            stats["tables"] += 1
            tbl = []

    for raw in md.splitlines():
        line = raw.rstrip()
        stats["words"] += len(re.findall(r"\w+", line))
        stats["placeholders"] += line.count("[PLACEHOLDER")
        if not line.strip():
            flush()
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush()
            lvl = len(m.group(1))
            if lvl == 1:
                stats["h1"] += 1
            elif lvl in (2, 3):
                stats[f"h{lvl}"] += 1
            blocks.append(heading(max(lvl, 2), m.group(2).strip()))
            continue
        if line.lstrip().startswith("|"):
            if para or lst:
                flush()
            tbl.append(line)
            continue
        m = re.match(r"^\s*([-*]|\d+\.)\s+(.*)$", line)
        if m:
            if para or tbl:
                flush()
            is_ord = m.group(1)[0].isdigit()
            if lst and is_ord != ordered:
                flush()
            ordered = is_ord
            lst.append(m.group(2))
            continue
        if lst or tbl:
            flush()
        para.append(line.strip())
    flush()
    return "\n\n".join(blocks) + "\n", stats


# --------------------------------------------------------------------------- #
# Validation                                                                   #
# --------------------------------------------------------------------------- #

def norm(u: str) -> str:
    u = re.sub(r"^https?://[^/]+", "", u.strip())
    return "/" + u.strip("/") + ("/" if u.strip("/") else "")


def validate(h: dict, folder: Path):
    errors, warnings = [], []
    E, W = errors.append, warnings.append

    for k in ("schema_version", "client", "approved", "backup", "review", "pages", "redirects", "noindex", "link_updates"):
        if k not in h:
            E(f"missing top-level key: {k}")
    if errors:
        return errors, warnings
    if h["schema_version"] != "1.0":
        E("schema_version must be 1.0")
    for k in ("name", "slug", "domain", "brand"):
        if not h["client"].get(k):
            E(f"client.{k} is empty")
    if not re.fullmatch(r"[a-z0-9-]+", h["client"].get("slug", "")):
        E("client.slug must be lowercase letters, digits, dashes")
    if not h["approved"].get("by"):
        W("approved.by is empty: stage/apply will refuse to run")
    if not h["backup"].get("confirmed"):
        W("backup.confirmed is false: stage/apply will refuse to run (NOV-04)")

    seen_ids, seen_urls = set(), {}
    for pg in h["pages"]:
        pid = pg.get("id", "?")
        if pid in seen_ids:
            E(f"{pid}: duplicate page id")
        seen_ids.add(pid)
        for k in ("id", "action", "route", "url", "seo_title", "h1", "meta_description"):
            if not pg.get(k):
                E(f"{pid}: missing {k} (META-01: title, H1 and meta are required on every page)")
        if pg.get("action") not in ACTIONS:
            E(f"{pid}: action must be create or update")
        if pg.get("route") not in ROUTES:
            E(f"{pid}: route must be build, spo or meta_only")
        if pg.get("action") == "create" and pg.get("route") != "build":
            E(f"{pid}: a created page must use route build")
        url = norm(pg.get("url", "/"))
        if url in seen_urls:
            E(f"{pid}: url {url} also used by {seen_urls[url]}")
        seen_urls[url] = pid
        if re.search(r"-\d+/$", url):
            E(f"{pid}: url ends in -N slug (URL-04)")
        if re.search(r"^/(service|services|service-area|service-areas)/.+", url):
            W(f"{pid}: url keeps a /service/ or /service-area/ prefix (URL-01)")
        for f in ("seo_title", "h1", "meta_description"):
            v = pg.get(f, "")
            if re.search(r",\s*" + STATE_ABBR, v):
                E(f"{pid}: {f} uses a state abbreviation, write the full state name (TTL-05/NO-17)")
            if "[PLACEHOLDER" in v:
                W(f"{pid}: {f} contains a placeholder")
        if pg.get("seo_title", "").strip().lower() == pg.get("h1", "").strip().lower():
            E(f"{pid}: SEO title and H1 are identical (NO-04)")
        if pg.get("h1", "").lower().startswith("the best") and not pg.get("the_best_reason"):
            E(f"{pid}: H1 uses 'The Best' without the_best_reason (H1-04: kd30 | rank4-20 | not_top20_90d)")
        if len(pg.get("meta_description", "")) > 180:
            W(f"{pid}: meta description is {len(pg['meta_description'])} characters")
        if pg.get("route") == "build":
            cf = pg.get("content_file")
            if not cf or not (folder / cf).exists():
                E(f"{pid}: route build needs an existing content_file")
        elif pg.get("content_file"):
            W(f"{pid}: content_file ignored for route {pg.get('route')}")
        if pg.get("action") == "update" and not pg.get("post_id"):
            W(f"{pid}: no post_id; the page is matched by URL")

    froms = {norm(r.get("from", "")) for r in h["redirects"]}
    for r in h["redirects"]:
        f, t = norm(r.get("from", "")), norm(r.get("to", ""))
        for k in ("from", "to", "reason", "finding_id"):
            if not r.get(k):
                E(f"redirect {f}: missing {k} (RDR-02)")
        if "has_backlinks_or_traffic" not in r:
            E(f"redirect {f}: missing has_backlinks_or_traffic (RDR-02)")
        if r.get("type", 301) not in (301, 302, 307):
            E(f"redirect {f}: type must be 301/302/307")
        if f == t:
            E(f"redirect {f}: points to itself")
        if t in froms:
            E(f"redirect {f} -> {t}: target is itself redirected; point to the final URL (RDR-04)")
        if f in seen_urls:
            E(f"redirect {f}: source is also a page in this handoff ({seen_urls[f]})")
    for n in h["noindex"]:
        if not n.get("url") or not n.get("reason"):
            E("noindex rows need url and reason")
    for lu in h["link_updates"]:
        if not lu.get("old_url") or not lu.get("new_url"):
            E("link_updates rows need old_url and new_url")
    redirected = {norm(r["from"]): norm(r["to"]) for r in h["redirects"] if r.get("from") and r.get("to")}
    covered = {norm(lu.get("old_url", "")) for lu in h["link_updates"]}
    for f in redirected:
        if f not in covered:
            W(f"redirect {f}: no link_updates row; internal links will hit the redirect (RDR-05)")
    return errors, warnings


# --------------------------------------------------------------------------- #
# Build                                                                        #
# --------------------------------------------------------------------------- #

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    folder = Path(sys.argv[1])
    h = json.loads((folder / "handoff.json").read_text(encoding="utf-8"))
    errors, warnings = validate(h, folder)

    pages_out, review_rows, content_notes = [], [], []
    if not errors:
        for pg in h["pages"]:
            p = dict(pg)
            p.setdefault("post_type", "page")
            p["url"] = norm(pg["url"])
            if pg["route"] == "build":
                md = (folder / pg["content_file"]).read_text(encoding="utf-8")
                blocks, st = md_to_blocks(md)
                if st["h1"]:
                    errors.append(f"{pg['id']}: content file has a '# ' H1; the H1 comes from the h1 field only")
                if st["tables"] > 1:
                    warnings.append(f"{pg['id']}: {st['tables']} tables (SVC-13 allows one)")
                if st["placeholders"]:
                    warnings.append(f"{pg['id']}: {st['placeholders']} placeholder(s) in content (CORE-06)")
                p["content_blocks"] = blocks
                content_notes.append(f"{pg['id']}: {st['words']} words, {st['h2']} H2, {st['h3']} H3, {st['tables']} tables")
            review_rows.append(f"| {pg['id']} | {pg['action']} | {pg['route']} | {p['url']} | {pg['seo_title']} | {pg['h1']} |")
            pages_out.append(p)

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s). bundle.json NOT written.")
        sys.exit(1)

    out = folder / "out"
    out.mkdir(exist_ok=True)
    bundle = {k: v for k, v in h.items() if k != "pages"}
    bundle["pages"] = pages_out
    bundle["built_by"] = "build_bundle.py"
    (out / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf-8")

    rv = [f"# Handoff review — {h['client']['name']}", "",
          f"Approved by: {h['approved'].get('by') or 'NOT APPROVED'} {h['approved'].get('date', '')}  ",
          f"Backup confirmed: {h['backup'].get('confirmed')} {h['backup'].get('timestamp', '')}  ",
          f"Review confirmed: {h['review'].get('confirmed')}", "",
          f"## Pages ({len(pages_out)})", "", "| id | action | route | url | SEO title | H1 |", "|---|---|---|---|---|---|", *review_rows, ""]
    if content_notes:
        rv += ["## Content", "", *[f"- {c}" for c in content_notes], ""]
    rv += [f"## Redirects ({len(h['redirects'])})", "", "| from | to | type | reason | finding |", "|---|---|---|---|---|"]
    rv += [f"| {norm(r['from'])} | {norm(r['to'])} | {r.get('type', 301)} | {r['reason']} | {r['finding_id']} |" for r in h["redirects"]]
    rv += ["", f"## Noindex ({len(h['noindex'])})", ""] + [f"- {n['url']} — {n['reason']}" for n in h["noindex"]]
    rv += ["", f"## Link updates ({len(h['link_updates'])})", ""] + [f"- {lu['old_url']} → {lu['new_url']}" for lu in h["link_updates"]]
    rv += ["", "## SPO handoff (content NOT rewritten in this run; title/H1/meta are)", ""]
    rv += [f"- {pg['id']} {norm(pg['url'])}" for pg in h["pages"] if pg["route"] == "spo"] or ["- none"]
    if warnings:
        rv += ["", "## Warnings", ""] + [f"- {w}" for w in warnings]
    (out / "HANDOFF-REVIEW.md").write_text("\n".join(rv) + "\n", encoding="utf-8")

    size = (out / "bundle.json").stat().st_size
    print(f"\nOK: bundle.json ({size // 1024} KB) and HANDOFF-REVIEW.md written to {out}. {len(warnings)} warning(s).")


if __name__ == "__main__":
    main()
