"""§5 workflow notes handled outside the data scripts (rewrite 2026-10-08)."""
import json
import re


def t_templates(h):
    ps = (h.SB / "templates" / "proof-sheet.md").read_text()
    h.check("#1/#5: the proof sheet asks only for GBP Manager access and has no phone line",
            "Manager" in ps and "Search Console" not in ps and "Analytics" not in ps and "[number]" not in ps
            and "Domain registrar" not in ps, ps[:600])
    bg = (h.SB / "templates" / "brand-guide.md").read_text()
    h.check("#9: the Brand Guide template has the blog author row and a D3 content-risk list; no N/S/E/W",
            "Blog author" in bg and "### D3" in bg and "FURTHEST NORTH" not in bg and "TOWNS AT THE EDGES" in bg)
    h.check("#15: the rating row says: exactly as Google shows it on the day", "as Google shows them on the day" in bg)
    ds = (h.SB / "templates" / "decision-sheet.md").read_text()
    keys = [l.split("|")[1].strip() for l in ds.splitlines() if l.startswith("| ") and not l.startswith("| Key")]
    want = {"category_variants", "area_entity", "homepage_title_variant", "homepage_h1_variant", "title_format.homepage",
            "title_format.service", "title_format.location", "title_format.about", "title_format.blog", "brand_in_titles",
            "scope_descriptor", "service_list", "towns_served", "address_display.gbp", "address_display.website",
            "the_best_policy", "blog_author", "sensitive_category", "cms", "wordpress_login", "tools.citations",
            "tools.grid", "tools.gsc_ga4"}
    h.check("R6: the Decision Sheet template carries every identity and format decision (#3 scope, #22 login, #23 CMS)",
            want <= set(keys) and all(re.match(r"^[a-z0-9][a-z0-9_.:-]{1,60}$", k) for k in keys), set(want) - set(keys))
    wc = (h.SB / "methodology" / "writing-commercial.md").read_text()
    h.check("#2: a routed FAQ is a candidate, not an obligation; location FAQs are about the town",
            "candidate*, not an" in wc and "about that town" in wc)


def t_naming(h):
    ok = lambda n: h.sh(f'python3 scripts/naming.py check "{n}" --client "Ab Co"')[0] == 0
    h.check("#7: RETURNED, CLIENT COPY, Status and INTERNAL notes are valid names",
            ok("Ab Co - Client Proof Sheet - RETURNED.md") and ok("Ab Co - Client Proof Sheet - CLIENT COPY")
            and ok("Ab Co - Status.md") and ok("Ab Co - INTERNAL - paul-answers - 2026-10-08.md")
            and ok("Ab Co - Decision Sheet - REVIEW.md"))
    h.check("#7: a deliverable with no status is still flagged", not ok("Ab Co - Finding Register.md"))


def t_cms(h):
    h.sh('python3 scripts/status.py init cm-co --name "Cm Co" --domain cm.example --type full --industry roofing')
    ag = h.Agent("cm-co"); rid = ag.start("new-client")
    f = ag.w("inputs/home.html", '<html><head><meta name="generator" content="Astro v4.5"></head><body>x</body></html>')
    code, out = h.sh(f"python3 scripts/cms.py detect cm-co --run {rid} --html-file {f}")
    ag.fin(rid, "set up")
    st = h.status("cm-co")
    h.check("#23: /new-client detects the CMS (Astro) and settles it", code == 0 and st["client"]["cms"] == "astro"
            and "runs on astro" in (h.SB / "clients/cm-co/decisions-settled.md").read_text(), out)
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    import cms
    h.check("#23: WordPress is recognised from wp-content", cms.detect('<link href="/wp-content/themes/x.css">') == "wordpress")
    rid = ag.start("wp-check")
    code, out = h.sh(f'python3 scripts/run.py finish cm-co {rid} --summary "x"')
    import subprocess
    sys.path.pop(0)
    nxt = json.loads(h.sh("python3 -c \"import sys; sys.path.insert(0,'scripts'); import next as N, status as S; "
                          "st=S.load('cm-co'); N.SLUG='cm-co'; N.PAUSE=None\n"
                          "try:\n N.condition_step(st,'cm-co','wordpress_connected')\nexcept N.Next as e:\n "
                          "import json; print(json.dumps(e.rec))\"")[1] or "{}")
    h.check("#23: not WordPress → the WordPress steps are N/A (no /wp-check is asked)",
            nxt.get("kind") == "wait" and "N/A" in nxt.get("why", "") and "/wp-check" not in nxt.get("command", ""), nxt)



def t_reads(h):
    g = json.loads((h.SB / "scripts" / "gates.json").read_text())
    reads = " ".join(g["steps"]["discovery:audit"]["reads"])
    h.check("R5: the audit reads script-made summaries (crawl, reviews, backlinks, grid), never raw exports",
            all(x in reads for x in ("crawl-summary.csv", "reviews-summary.md", "backlinks-per-url.csv",
                                     "local-grid-summary.md")) and "inputs/crawl/" not in reads, reads)
    h.check("R6: every judgment step reads decisions-settled.md",
            all("clients/<slug>/decisions-settled.md" in v["reads"] for k, v in g["steps"].items()
                if k.startswith(("discovery:", "build:", "finish:", "blog:"))))
    import sys
    sys.path.insert(0, str(h.SB / "scripts"))
    import steps
    h.check("#11: S05b is registered but optional (an approved audit stays complete)",
            any(r["id"] == "S05b" for r in steps.registry()) and "S05b" in steps.OPTIONAL)
    sys.path.pop(0)


SCENARIOS = [t_templates, t_naming, t_cms, t_reads]
