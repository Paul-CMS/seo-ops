#!/usr/bin/env python3
"""migrate2.py — rewrite 2 client migrations (2026-10-09). Never loses an approval: every approval is listed before
and after, and nothing is written when one that counted before would stop counting.

    migrate2.py urls  <slug> [--dry-run]     P7 + P10: Paul's URL decisions (REWRITE-2-DECISIONS.md c) and one batch per
                                             kind (split only above 15 pages); the site plan is re-approved once
    migrate2.py facts <slug> [--dry-run]     P4: build clients/<slug>/facts.json from the Brand Guide's A and D rows
                                             (plus the client's settled answers mapped below), regenerate the rows,
                                             re-stamp every approval on the value-only hash; Apex: P11's line-76 fix

A dry run does the work, prints the report, and puts every file back exactly as it was.
Each real run logs one MIGRATION line in the client's log.md and makes one commit of that client's folder.
"""
import json
import re
import sys

import status as S
from lib import ROOT, append, client_dir, die, git_commit, now, ref_missing, ref_sha, ref_sha_v2, sha12

APEX = "apex-roofing-of-the-lowcountry"
# Paul's 2026-10-09 answers (decisions-settled.md), recorded as facts once — the settled key is the source.
APEX_FACTS = [
    ("d-who-does-the-work", "Who does the work on the roof", "Ralph and Pierce Brehany (father and son) both get on the roof",
     "Paul 2026-10-09 (settled w25_who_goes_on_the_roof; W25)"),
    ("d-job-photos", "Job photos", "Photos of the work go to the customer, with progress photos each day on a longer job",
     "Paul 2026-10-09 (settled pilot_facts_2026_10_09; W10, reviews)"),
    ("d-repair-materials", "Repair materials", "Corrosion-resistant flashing and synthetic underlayment on repairs",
     "Paul 2026-10-09 (settled pilot_facts_2026_10_09; W11)"),
    ("d-clean-up", "Clean-up", "Clean-up each day and a magnet sweep for loose nails",
     "Paul 2026-10-09 (settled pilot_facts_2026_10_09; reviews; magnet per Paul)"),
    ("d-permits", "Permits", "On a roof replacement, Apex gets the Town permit",
     "Paul 2026-10-09 (settled pilot_facts_2026_10_09; review 2026-08-15)"),
    ("d-synthetic-roofing-offered", "Synthetic roofing offered", "Yes",
     "Paul 2026-10-09 (settled synthetic_roofing)"),
]
APEX_EDITS = [   # (fact id, old text, new text, why) — value changes Paul approved on 2026-10-09
    ("d-certifications-authorizations-factory-training", "CertainTeed ShingleMaster (W3): **not confirmed** — see D2",
     "CertainTeed ShingleMaster (W3): current (Paul 2026-10-09)",
     "settled send_the_client_one_question_is_your_cer (ShingleMaster current — yes)"),
    ("a-category-variants-4-6", "Candidate only, not approved: Residential Roofer (site wording, not Wikipedia) — the "
     "business is residential only (Paul 2026-10-06)",
     "Residential Roofer — approved by Paul 2026-10-08 (site plan choice 4a; site wording, not Wikipedia; the "
     "business is residential only)",
     "settled site_plan_open_choices 4a (closes residential_roofer_a3_write)"),
]
APEX_PAGE_FACTS = {"loc-bluffton": {"neighborhoods": {
    "value": "Inside the Town of Bluffton: Old Town, Palmetto Bluff, Jones Estate, Buckwalter, Shultz Tract, Hampton Hall. "
             "Also served, outside the Town limits (Greater Bluffton): Belfair, Colleton River Plantation, Moss Creek.",
    "status": "Paul Approved 2026-10-09",
    "source": "Paul 2026-10-09 (settled bluffton_communities); Town of Bluffton Neighborhoods PDF; Wikipedia Bluffton"}}}
APEX_LINE76 = ("[Link placeholder: /emergency-roof-repair/ — CM-022 exception, proposed in Finish; no link placed in "
               "Build (CM-005)]",
               "[LINK → /emergency-roof-repair/ · CM-022 exception, proposed in Finish; no link placed in Build (CM-005)]")


def approvals(st):
    """[(where, files map)] for every approval record that names files."""
    out = []
    for g, rec in (st.get("gates") or {}).items():
        if rec.get("files"):
            out.append((f"gate {g}", rec["files"]))
    bp = st.get("build") or {}
    if ((bp.get("site_plan") or {}).get("approval") or {}).get("files"):
        out.append(("site plan", bp["site_plan"]["approval"]["files"]))
    for b in bp.get("batches") or []:
        for stage in S.STAGES:
            if (b.get(stage) or {}).get("files"):
                out.append((f"batch {b['id']} {stage}", b[stage]["files"]))
    for pid, p in (st.get("pages") or {}).items():
        if ((p.get("approval") or {}).get("files")):
            out.append((f"page {pid}", p["approval"]["files"]))
    return out


def counts(f, h):
    if ref_missing(f):
        return False
    return ref_sha(f) == h or ("#" in f and ref_sha_v2(f) == h)


def snapshot(st):
    return {where: {f: counts(f, h) for f, h in files.items()} for where, files in approvals(st)}


def migrate_facts(slug, dry):
    import facts
    import settled
    d = client_dir(slug)
    if (d / "facts.json").exists():
        return f"{slug}: facts.json already exists — nothing to do"
    st = S.load(slug)
    before = snapshot(st)
    keep = {}   # path -> original text (restored on a dry run or a refusal)

    def write(p, text):
        if p not in keep:
            keep[p] = p.read_text(encoding="utf-8") if p.exists() else None
        p.write_text(text, encoding="utf-8")

    folded, report = [], []
    try:
        bg = d / "brand-guide.md"
        rows = facts.from_brand_guide(bg.read_text(encoding="utf-8")) if bg.exists() else []
        if slug == APEX:
            ids = facts.by_id(rows)
            for fid, old, new, why in APEX_EDITS:
                r = ids.get(fid) or die(f"{slug}: no fact {fid} in the Brand Guide — stop")
                if old not in r["value"]:
                    die(f"{slug}: {fid} no longer reads as expected — stop, nothing written")
                r["value"] = r["value"].replace(old, new)
                folded.append(f"{fid}: {why}")
            for fid, label, value, src in APEX_FACTS:
                rows.append({"id": fid, "section": "D", "num": "", "label": label, "value": value,
                             "status": "paul_approved", "status_text": None, "source": src, "quote": "",
                             "date": "2026-10-09", "who": "Paul", "count": None})
                folded.append(f"{fid}: new row ({src})")
            for pid, fx in APEX_PAGE_FACTS.items():
                pf = d / "build" / "evidence" / f"{pid}.facts.json"
                data = json.loads(pf.read_text())
                data["facts"].update(fx)
                write(pf, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
                folded.append(f"{pid} page facts: {', '.join(fx)} (settled bluffton_communities)")
            draft = d / "build" / "pilot" / "SD - Roof Repair - Apex Roofing of the Lowcountry.md"
            t = draft.read_text(encoding="utf-8")
            if APEX_LINE76[0] in t:
                write(draft, t.replace(APEX_LINE76[0], APEX_LINE76[1]))
                folded.append(f"{draft.name} line 76: inline link placeholder in the one P11 form (no wording change)")
        fj = d / "facts.json"
        keep.setdefault(fj, None)
        facts.save(slug, rows)
        if bg.exists():
            write(bg, facts.render_into_text(bg.read_text(encoding="utf-8"), rows))
        # re-stamp: every file of an approval that counted before is stamped on the new hash
        st = S.load(slug)
        restamped = 0
        for where, files in approvals(st):
            for f in list(files):
                if before.get(where, {}).get(f):
                    new = ref_sha(f)
                    if new != files[f]:
                        files[f] = new
                        restamped += 1
        after = {where: {f: counts(f, h) for f, h in files.items()} for where, files in approvals(st)}
        lost = [f"{w}: {f}" for w, fs in before.items() for f, ok in fs.items() if ok and not after.get(w, {}).get(f)]
        for w, fs in before.items():
            report.append(f"  {w}: " + ", ".join(f"{f.split('/')[-1]} {'counts' if ok else 'void'} → "
                                                 f"{'counts' if after.get(w, {}).get(f) else 'VOID'}"
                                                 for f, ok in fs.items()))
        if lost:
            raise SystemExit(f"{slug}: STOP — these approvals would be lost, nothing written:\n  - " + "\n  - ".join(lost))
        head = (f"{slug}: {len(rows)} facts · {restamped} approval stamp(s) re-stamped on the value-only hash · "
                f"0 approvals lost")
        if dry:
            return "\n".join([head + " (DRY RUN — nothing kept)", "  approvals before → after:", *report]
                             + (["  folded in (Paul's 2026-10-09 answers):"] + [f"    - {x}" for x in folded] if folded else []))
        S.save(slug, st)
        if slug == APEX:
            settled.settle(slug, "migration-rewrite2", "residential_roofer_a3_write",
                           "Residential Roofer written into Brand Guide A3 (Paul approved it 2026-10-08, site plan "
                           "choice 4a); entity and Brand Guide approvals re-stamped by the rewrite 2 migration",
                           by="Paul (site plan choice 4a, 2026-10-08)", closed_ok=True)
        append(d / "log.md", f"\n## MIGRATION · {now()} · rewrite 2 P4: facts.json\n"
               f"{len(rows)} facts from Brand Guide A and D · {restamped} approval stamp(s) re-stamped on the value-only "
               f"hash · 0 lost" + ("".join(f"\nFolded in: {x}" for x in folded)) + "\n")
        keep.clear()
        import records
        records.render(slug)
        return head + ("\n  folded in: " + "; ".join(folded) if folded else "")
    finally:
        for p, text in keep.items():   # dry run or refusal: put every file back
            if text is None:
                p.unlink(missing_ok=True)
            else:
                p.write_text(text, encoding="utf-8")


# ------------------------------------------------------------------ P7 + P10: URLs and batches
HMM = "home-mobile-medical"
URL_MOVES = {
    HMM: {"hub-hhi-beaufort": "https://homemobilemedical.com/hilton-head-bluffton-metro/",
          "hub-charleston": "https://homemobilemedical.com/charleston-metro/"},
    APEX: {"svc-metal-roofing": "https://apexroofingtlc.com/metal-roofing/"},
}
DROP = {HMM: {"hub-lowcountry": "https://homemobilemedical.com/"}}   # /service-area/ → 301 to the homepage
REBATCH = {
    HMM: [("services", "service", "All service pages", ["svc1"]),
          ("loc-hhi", "location", "Hilton Head Island–Bluffton–Port Royal metro (hub + towns)", ["loc1", "loc2", "loc3"]),
          ("loc-charleston", "location", "Charleston metro (hub + towns) + Walterboro, Edisto Island", ["loc4", "loc5", "loc6", "loc7"]),
          ("final", "homepage", "Homepage and About", ["final1", "final2"])],
    APEX: [("services", "service", "All service pages", ["s1", "s2"]),
           ("locations", "location", "All location pages", ["l1", "l2", "l3"])],
}
PLAN_JSON = {HMM: "build/site-plan-revised.plan.json", APEX: "build/site-plan.json"}
WHY = {HMM: "Paul 2026-10-09 (REWRITE-2-DECISIONS.md c): /services/<x>/ → /<x>/, /service-area/<city>/ → /<city>/, metro hubs "
            "(CM-058: Charleston Q5084207, Hilton Head Island–Bluffton–Port Royal Q17020871), /service-area/ → 301 to the homepage",
       APEX: "Paul 2026-10-09 (REWRITE-2-DECISIONS.md c): /metal-roofing-2/ → /metal-roofing/ with a 301"}


def new_url(slug, pg):
    if pg["id"] in URL_MOVES.get(slug, {}):
        return URL_MOVES[slug][pg["id"]]
    u = pg.get("url") or ""
    if slug == HMM:
        u = re.sub(r"/services/([^/]+)/$", r"/\1/", u)
        u = re.sub(r"/service-area/([^/]+)/$", r"/\1/", u)
    return u


def migrate_urls(slug, dry):
    import urlcheck
    d = client_dir(slug)
    st = S.load(slug)
    if st.get("rewrite2_urls"):
        return f"{slug}: URLs already migrated"
    before = snapshot(st)
    pj = d / PLAN_JSON[slug]
    plan = json.loads(pj.read_text())
    moves, drops = [], []
    for pg in plan["pages"]:
        if pg["id"] in DROP.get(slug, {}):
            drops.append((pg["id"], pg["url"], DROP[slug][pg["id"]]))
            continue
        planned_only = " (URL set in the site plan)" in (pg.get("url") or "")   # not live: no redirect needed
        if planned_only:
            pg["url"] = pg["url"].split(" (")[0]
            nu = new_url(slug, pg)
            moves.append((pg["id"], pg["url"] + " (planned, never live)", nu))
            pg["url"] = nu
            continue
        nu = new_url(slug, pg)
        if nu != pg["url"]:
            moves.append((pg["id"], pg["url"], nu))
            pg["replaces"] = sorted(set((pg.get("replaces") or []) + [pg["url"]]))
            pg["live_url"] = pg["url"]
            pg["url"] = nu
    plan["pages"] = [pg for pg in plan["pages"] if pg["id"] not in DROP.get(slug, {})]
    old_b = {b["id"]: b for b in plan["batches"]}
    st_b = {b["id"]: b for b in st["build"]["batches"]}
    merged, gone = [], set()
    for nid, kind, label, olds in REBATCH.get(slug, []):
        for o in olds:
            sb = st_b.get(o) or {}
            if sb.get("state") not in ("planned", None) or sb.get("briefs") or sb.get("drafts"):
                die(f"{slug}: batch {o} is already under way ({sb.get('state')}) — stop, nothing written")
        pages = [x for o in olds for x in old_b[o]["pages"] if x not in DROP.get(slug, {})]
        merged.append({"id": nid, "kind": kind, "label": label, "pages": pages})
        gone |= set(olds)
    keep = [b for b in plan["batches"] if b["id"] not in gone]
    first = next((i for i, b in enumerate(plan["batches"]) if b["id"] in gone), len(keep))
    plan["batches"] = keep[:first] + merged + keep[first:]
    bad = urlcheck.problems(plan["pages"])
    if bad:
        die(f"{slug}: the moved plan still breaks the URL rule — stop:\n  - " + "\n  - ".join(bad))
    report = [f"  {pid}: {o} → {n}" + ("" if o.endswith("never live)") else " (301 paired with the publish)")
              for pid, o, n in moves]
    report += [f"  {pid}: {o} dropped from the plan → 301 to {to}" for pid, o, to in drops]
    report += [f"  batches: {', '.join(sorted(gone))} → {', '.join(m['id'] for m in merged)}"]
    head = f"{slug}: {len(moves)} URL(s) moved, {len(drops)} page(s) dropped, {len(gone)} batch(es) merged into {len(merged)}"
    if dry:
        return head + " (DRY RUN — nothing written)\n" + "\n".join(report) + \
            "\n  approvals: unchanged except the site plan, which Paul re-approves once (its file changes)"
    pj.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    md = ROOT / st["build"]["site_plan"]["file"]
    text = md.read_text(encoding="utf-8")
    for _, o, n in moves:
        text = text.replace(o.replace(" (planned, never live)", ""), n)
    note = ("\n> **Rewrite 2 changes (2026-10-09), for Paul's re-approval:** " + WHY[slug] + ". Batches: one per kind "
            "(P10), split only above 15 pages: " + "; ".join(f"{m['id']} ({len(m['pages'])})" for m in merged) + ".\n")
    lines = text.split("\n", 1)
    md.write_text(lines[0] + "\n" + note + (lines[1] if len(lines) > 1 else ""), encoding="utf-8")
    st = S.load(slug)
    for pid, o, n in moves:
        p_ = st["pages"].get(pid) or {}
        if o.endswith(" (planned, never live)"):
            p_["url"] = n
            continue
        p_.update({"url": n, "live_url": o, "replaces": sorted(set((p_.get("replaces") or []) + [o]))})
    for pid, *_ in drops:
        st["pages"].pop(pid, None)
    sb = [b for b in st["build"]["batches"] if b["id"] not in gone]
    new = [{"id": m["id"], "kind": m["kind"], "label": m["label"], "pages": m["pages"], "state": "planned",
            "briefs": None, "drafts": None, "files": {}} for m in merged]
    i = next((k for k, b in enumerate(st["build"]["batches"]) if b["id"] in gone), len(sb))
    st["build"]["batches"] = sb[:i] + new + sb[i:]
    for b in st["build"]["batches"]:
        b["pages"] = [x for x in b["pages"] if x not in DROP.get(slug, {})]
    st["rewrite2_urls"] = {"at": now(), "moves": len(moves), "dropped": [x[0] for x in drops]}
    S.save(slug, st)
    after = snapshot(S.load(slug))
    lost = [f"{w}: {f}" for w, fs in before.items() for f, ok in fs.items()
            if ok and not after.get(w, {}).get(f) and w != "site plan"]
    if lost:
        die(f"{slug}: STOP — approvals other than the site plan would be lost: {', '.join(lost)}")
    append(d / "log.md", f"\n## MIGRATION · {now()} · rewrite 2 P7 + P10: URLs and batches\n{WHY[slug]}\n"
           + "\n".join(r.strip() for r in report) + "\nThe site plan file changed: Paul re-approves it once.\n")
    import subprocess
    rid = None
    r = subprocess.run(["python3", str(ROOT / "scripts" / "run.py"), "start", slug, "drive-mirror",
                        "--note", "rewrite 2 URL migration: worklist rows"], capture_output=True, text=True, cwd=ROOT)
    if r.returncode == 0:
        rid = r.stdout.strip().splitlines()[-1]
        rows = []
        for pid, o, to in drops:
            rows.append(("redirect", f"url,field,old,new,reason,decision_map_ref\n{o},301,,{to},"
                         f"rewrite 2: {pid} dropped (Paul 2026-10-09),{pid}\n"))
        if slug == APEX:
            rows.append(("other", "url,field,old,new,reason,decision_map_ref\nhttps://apexroofingtlc.com/metal-roofing/,"
                         "clear the slug,whatever holds /metal-roofing/ now,nothing,find and clear it first so the new "
                         "Metal Roofing page publishes at /metal-roofing/ (its 301 from /metal-roofing-2/ is with its "
                         "publish row),svc-metal-roofing\n"))
        for kind, body in rows:
            f = d / "handoffs" / f"_migration-{kind}.csv"
            f.parent.mkdir(exist_ok=True)
            f.write_text(body)
            args = ["python3", str(ROOT / "scripts" / "handoff.py"), "create", slug, "--run", rid, "--kind", kind,
                    "--items", str(f.relative_to(ROOT))]
            if kind == "other":
                args += ["--to", "Jonie", "--owner-reason", "WordPress slug work"]
            subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
            f.unlink(missing_ok=True)
        if slug == HMM:   # Paul (c): reopen the redirect default — nothing may point at /services/ any more (no chains)
            import settled
            if (settled.entries(slug).get("redirect-targets-default") or {}).get("state") == "settled":
                settled.reopen(slug, rid, "redirect-targets-default",
                               "rewrite 2 (Paul 2026-10-09, REWRITE-2-DECISIONS.md c): /services/ and /service-area/ are gone")
                settled.settle(slug, rid, "redirect-targets-default",
                               "Paul 2026-10-09 (Q2, revised in rewrite 2): redirect the 36 to the appropriate URLs — FL/MI → "
                               "/stair-lifts/, power chairs/scooter lifts → the homepage (was /services/), ramps → /porch-lifts/; "
                               "SC legacy duplicates → their canonical root service/location page. No redirect points at "
                               "/services/ or /service-area/, so there are no chains.", by="Paul (REWRITE-2-DECISIONS.md c)",
                               closed_ok=True)
        hf = d / "handoffs" / f"run-{rid}.md"
        hf.write_text("**What I did**\n- rewrite 2 URL migration: worklist rows for the redirect / slug clearing\n")
        subprocess.run(["python3", str(ROOT / "scripts" / "run.py"), "finish", slug, rid, "--summary",
                        "rewrite 2 URL migration (worklist rows)", "--handoff", str(hf.relative_to(ROOT))],
                       capture_output=True, text=True, cwd=ROOT)
    import records
    records.render(slug)
    return head + "\n" + "\n".join(report)


def repair_duplicates(slug):
    """2026-10-09 repair: the first facts render matched rows by an id rebuilt from the label, so a fact whose id
    differed (d-who-does-the-work) was appended twice after the re-stamp. Remove repeated fact rows (keep the first)
    and report which approvals count again; no stamp is changed."""
    import facts
    d = client_dir(slug)
    bg = d / "brand-guide.md"
    st = S.load(slug)
    before = snapshot(st)
    lines, seen, drop = bg.read_text(encoding="utf-8").splitlines(), set(), []
    for letter in ("A", "D"):
        _, t = facts._table("\n".join(lines), letter)
        for i, cells in (t[1] if t else []):
            if lines[i] in seen:
                drop.append(i)
            seen.add(lines[i])
    if not drop:
        return f"{slug}: no repeated fact rows"
    text = "\n".join(l for i, l in enumerate(lines) if i not in set(drop)) + "\n"
    bg.write_text(text, encoding="utf-8")
    after = snapshot(S.load(slug))
    back = [f"{w}: {f.split('/')[-1]}" for w, fs in after.items() for f, ok in fs.items() if ok and not before[w][f]]
    lost = [f"{w}: {f}" for w, fs in before.items() for f, ok in fs.items() if ok and not after[w][f]]
    if lost:
        bg.write_text("\n".join(lines) + "\n", encoding="utf-8")
        die(f"{slug}: STOP — the repair would void {', '.join(lost)}; nothing written")
    append(d / "log.md", f"\n## MIGRATION · {now()} · rewrite 2 P4 repair: {len(drop)} repeated fact row(s) removed "
           f"from the Brand Guide · approvals counting again: {', '.join(back) or 'none'} · no stamp changed\n")
    import records
    records.render(slug)
    return f"{slug}: removed {len(drop)} repeated row(s); counting again: {', '.join(back) or 'none'}"


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "repair-duplicates":
        out = repair_duplicates(sys.argv[2])
        print(out)
        if "removed" in out:
            print(git_commit(f"{sys.argv[2]}: rewrite 2 migration repair — repeated fact row removed (P4)\n\n{out}",
                             slug=sys.argv[2]))
        return
    if len(sys.argv) >= 3 and sys.argv[1] == "urls":
        out = migrate_urls(sys.argv[2], "--dry-run" in sys.argv)
        print(out)
        if "--dry-run" not in sys.argv and "already" not in out:
            print(git_commit(f"{sys.argv[2]}: rewrite 2 migration — URLs and batches (P7, P10)\n\n{out}", slug=sys.argv[2]))
        return
    if len(sys.argv) < 3 or sys.argv[1] != "facts":
        sys.exit(__doc__)
    slug, dry = sys.argv[2], "--dry-run" in sys.argv
    out = migrate_facts(slug, dry)
    print(out)
    if not dry and "already exists" not in out:
        print(git_commit(f"{slug}: rewrite 2 migration — facts.json (P4)\n\n{out}", slug=slug))


if __name__ == "__main__":
    main()
