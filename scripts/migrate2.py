#!/usr/bin/env python3
"""migrate2.py — rewrite 2 client migrations (2026-10-09). Never loses an approval: every approval is listed before
and after, and nothing is written when one that counted before would stop counting.

    migrate2.py facts <slug> [--dry-run]     P4: build clients/<slug>/facts.json from the Brand Guide's A and D rows
                                             (plus the client's settled answers mapped below), regenerate the rows,
                                             re-stamp every approval on the value-only hash; Apex: P11's line-76 fix

A dry run does the work, prints the report, and puts every file back exactly as it was.
Each real run logs one MIGRATION line in the client's log.md and makes one commit of that client's folder.
"""
import json
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
    if len(sys.argv) < 3 or sys.argv[1] != "facts":
        sys.exit(__doc__)
    slug, dry = sys.argv[2], "--dry-run" in sys.argv
    out = migrate_facts(slug, dry)
    print(out)
    if not dry and "already exists" not in out:
        print(git_commit(f"{slug}: rewrite 2 migration — facts.json (P4)\n\n{out}", slug=slug))


if __name__ == "__main__":
    main()
