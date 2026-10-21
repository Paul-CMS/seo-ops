"""Rewrite 4 Phase 7 — prune the governance. Four gates folded into checks inside their scripts (Paul, 2026-10-21):
client_setup (run.py start, handoff.py, wp.py), audit_steps_complete (approve.py at audit_approved, a /next step),
safe_fixes_allowed (= audit_approved) and structural_changes_allowed (= entity_approved + brand_guide_approved).
Every decision Paul makes stays a gate; each fold refuses exactly what the gate refused."""
import json

FOLDED = ("client_setup", "audit_steps_complete", "safe_fixes_allowed", "structural_changes_allowed")


def t_gates_json(h):
    g = json.loads((h.SB / "scripts/gates.json").read_text())
    named = set(g["gates"]) | set(g["conditions"]) | set(g.get("derived") or {})
    used = {x for s in g["steps"].values() for k in ("gates", "gates_blog_only") for x in s.get(k, [])}
    h.check("phase7 gates: the four folded names are gone from gates, conditions and every step, and kept as history",
            not (set(FOLDED) & (named | used)) and all(f in g["retired_gates"] for f in FOLDED) and "derived" not in g,
            sorted(set(FOLDED) & (named | used)))
    h.check("phase7 gates: every decision Paul makes is still a gate",
            set(g["gates"]) == {"entity_approved", "proof_sheet_approved", "audit_approved", "brand_guide_approved",
                                "release_approved", "blog_map_approved", "blog_topics_approved",
                                "wordpress_pilot_approved"}, sorted(g["gates"]))
    ck = g["change_kinds"]
    h.check("phase7 gates: safe kinds need audit_approved; structural kinds need entity + Brand Guide; set-up kinds no gate",
            all(ck[k]["gate"] == "audit_approved" for k in ("alt_text", "broken_link", "sitemap", "robots_txt", "speed"))
            and all(ck[k]["gate"] == ["entity_approved", "brand_guide_approved"] for k in ("redirect", "slug", "h1", "seo_title"))
            and all("gate" not in ck[k] for k in ("other", "wp_setup", "seopress_settings", "manual_lookup"))
            and g["steps"]["implement:structural"]["gates"][:2] == ["entity_approved", "brand_guide_approved"]
            and g["steps"]["implement:safe"]["gates"][0] == "audit_approved", {k: ck[k].get("gate") for k in ck})


def t_client_set_up(h):
    S = "p7-setup"
    h.sh(f"python3 scripts/status.py init {S} --name P7 --domain p7.example --type full --industry roofing")
    ag = h.Agent(S)
    code, out = h.sh(f"python3 scripts/run.py start {S} wp-check")
    h.check("phase7 set-up: before /new-client finishes, any later step is refused (it was the client_setup gate)",
            code == 4 and "run /new-client first" in out, out[-300:])
    p = ag.w("tmp/o.csv", "url,field,old,new,reason,decision_map_ref\nhttps://p7.example/,x,a,b,why,F-1\n")
    code, out = h.sh(f"python3 scripts/handoff.py create {S} --run none --kind other --items {p}")
    h.check("phase7 set-up: a handoff of a set-up kind is refused before /new-client too", code != 0, out[-300:])
    ag.fin(ag.start("new-client"), "set up")
    rid = ag.start("wp-check")
    h.check("phase7 set-up: after /new-client the same step starts, with no gate named", bool(rid), ag.errors[-1:])
    ag.fin(rid, "checked")


def t_audit_steps(h):
    S = "p7-audit"
    h.sh(f"python3 scripts/status.py init {S} --name P7a --domain p7a.example --type full --industry roofing")
    ag = h.Agent(S)
    ag.fin(ag.start("new-client"), "set up")
    f = ag.w("audit/2026-10-21/audit-review.md", "the audit\n")
    ag.mark("audit_deliverables", f)
    st = h.status(S)
    for g in ("entity_approved", "proof_sheet_approved"):
        st["gates"][g] = {"state": "approved", "by": "Paul", "at": "2026-10-21T09:00:00-05:00", "files": {}}
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = h.paul(f"/approve {S} audit_approved --files {f}")
    h.check("phase7 audit: audit_approved is refused while an audit step has no outcome (was audit_steps_complete)",
            code != 0 and "audit steps with no outcome yet" in out
            and (h.status(S)["gates"].get("audit_approved") or {}).get("state") != "approved", out[-300:])
    code, out = h.sh(f"python3 scripts/next.py {S}")
    h.check("phase7 audit: /next sends the missing steps to run first (the crawl here), never to an /approve that would be refused",
            "/approve" not in out and f"/crawl {S}" in out, out[-400:])
    st = h.status(S)
    st["imported_conditions"] = {**(st.get("imported_conditions") or {}), "audit_steps_complete": "test"}
    (ag.c / "status.json").write_text(json.dumps(st))
    code, out = h.paul(f"/approve {S} audit_approved --files {f}")
    h.check("phase7 audit: with every step recorded, Paul's approval goes through",
            code == 0 and h.status(S)["gates"].get("audit_approved", {}).get("state") == "approved", out[-300:])


def t_rulings_enforced(h):
    """A ruling reduced to one line names the scripts that enforce it and the tests that prove it — and they exist."""
    import re
    text = (h.SB / "methodology/rulings.md").read_text()
    lines = re.findall(r"^\*\*ID\*\* (\S+) · .*\*\*Enforced by\*\* (.+?) · \*\*Proved by\*\* (.+?) · full text: `([^`]+)`$",
                       text, re.M)
    bad = []
    for rid, enf, proof, arch in lines:
        for s in re.findall(r"`(?:scripts/)?([\w./-]+\.py)", enf):
            if not ((h.SB / "scripts" / s).exists() or (h.SB / s).exists()):
                bad.append(f"{rid}: no script {s}")
        files = re.findall(r"`(tests/[\w./-]+\.py)`", proof)
        if not files:
            bad.append(f"{rid}: no test file named")
        for f in files:
            src = (h.SB / f).read_text() if (h.SB / f).exists() else None
            if src is None:
                bad.append(f"{rid}: no test file {f}")
                continue
            after = proof.split(f"`{f}`", 1)[1].split("`tests/")[0]
            for fn in re.findall(r"\bt_\w+", after):
                if f"def {fn}(" not in src:
                    bad.append(f"{rid}: {f} has no {fn}")
        if not (h.SB / arch).exists() or f"## {rid} · " not in (h.SB / arch).read_text():
            bad.append(f"{rid}: the full text is not in {arch}")
    ids = re.findall(r"^## ((?:CM|RULE|PROC|GOV-T|CF)-?\d+[a-z]?) · ", text, re.M)
    h.check("phase7 rulings: every enforced ruling names a script and a test that exist, and keeps its ID and its full "
            "text in the archive; no ID was removed", len(lines) >= 12 and not bad and len(ids) == len(set(ids)) >= 86,
            bad or len(lines))


def t_sizes_and_reads(h):
    """Agent files point to IDs and the stage docs; read lists name sections and commands, never a whole big file."""
    for a in ("discovery-audit", "build"):
        n = len((h.SB / f".claude/agents/{a}.md").read_bytes())
        h.check(f"phase7 size: {a}.md is under 12 KB", n < 12 * 1024, n)
    g = json.loads((h.SB / "scripts/gates.json").read_text())
    reads = [r for s in g["steps"].values() for r in s["reads"]]
    h.check("phase7 reads: no read list names gates.json, the Bradley Standard or writing-commercial.md just for a part",
            not [r for r in reads if r.startswith(("scripts/gates.json", "sop-source/BB-Standard-v1.0.md"))
                 or r == "methodology/writing-commercial.md (Usage tiers)"], [r for r in reads if "gates.json" in r])
    code, out = h.sh("python3 scripts/handoff.py kinds")
    h.check("phase7 reads: handoff.py kinds prints each change kind with the decisions it needs",
            code == 0 and "| redirect | entity_approved + brand_guide_approved | handoff | Jonie |" in out
            and "| manual_lookup | the client set-up |" in out, out[:300])
    code, out = h.sh("python3 scripts/rulings.py BB-1xx")
    code2, out2 = h.sh("python3 scripts/rulings.py BB-105")
    h.check("phase7 reads: rulings.py prints a Bradley Standard chapter (BB-1xx) or one rule (BB-105), not the file",
            code == 0 and "BB-110" in out and "BB-201" not in out and code2 == 0 and out2.startswith("### BB-105")
            and "BB-106" not in out2, out2[:200])
    code, out = h.sh('python3 scripts/rulings.py --section methodology/writing-commercial.md "Usage tiers"')
    code2, _ = h.sh('python3 scripts/rulings.py --section .env "x"')
    h.check("phase7 reads: rulings.py --section prints one section of a methodology file, and only methodology/docs",
            code == 0 and out.startswith("## Usage tiers") and "## B — Required inputs" not in out and code2 != 0, out[:200])
    code, out = h.sh("python3 scripts/usage.py reads --json")
    d = json.loads(out) if code == 0 else {}
    h.check("phase7 usage: usage.py reads measures every step's read list and agent file (the before/after table)",
            code == 0 and set(d["after"]) == set(g["steps"]) and d["after"]["discovery:discovery"]["reads"] < 30 * 1024
            and d["agents"]["build"] < 12 * 1024, out[-300:])


SCENARIOS = [t_gates_json, t_client_set_up, t_audit_steps, t_rulings_enforced, t_sizes_and_reads]
