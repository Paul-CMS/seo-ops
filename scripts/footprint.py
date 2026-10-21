#!/usr/bin/env python3
"""footprint.py — the brand layer of the research store: Prompt C, the client's public footprint (Rewrite 4 Phase 6,
plan §3). Optional, once per client. Standard library only. The report comes from Gemini Deep Research (the VA).

    footprint.py prompt <slug> [--stdout]      Prompt C filled from the Brand Guide (name, confirmed NAP, phone, website)
                                               → build/footprint/prompt-c.md
    footprint.py ingest <slug> <report.md>     parse the table, check every URL (loads; the name is on the page; the
                                               address and phone match the confirmed NAP — the script re-checks the
                                               report's own "matches" column) → data/footprint/footprint.json and
                                               build/footprint/section-f-proposal.md
    footprint.py show <slug>                   the stored footprint in short

What it proposes (Paul approves; the Brand Guide is never edited here):
  sameAs candidates   profiles and listings that load and match the NAP → Section F "Full citation list → sameAs",
                      "Social profile list", "Apple Maps link → sameAs"
  citation / NAP check  listings that do not match (or partly) — with exactly what differs — for the citation clean-up
  history rows        former names, former addresses, former lines of business → the Decision Sheet
Press and awards are mentions, not profiles: kept in the footprint, never proposed for sameAs.
A URL that does not load is dropped, never asked. A site that blocks robots (403/429/999) is listed "open it by hand".
"""
import argparse
import json
import re

from lib import ROOT, client_dir, die, read_json, today, write_json

PROMPT_C = """Find every public profile and mention of "{BRAND}" at {ADDRESS_OR_AREA}, phone {PHONE},
website {WEBSITE}, current as of {YEAR}: Google Business Profile, social profiles, directory
and citation listings, Secretary of State registration, licence board record, manufacturer
dealer/installer listings, BBB, local news and press, awards. For each: URL, the name,
address and phone exactly as shown, the date seen, and whether it matches the details above.
List former names, former addresses and former lines of business you find. Never infer;
list "not found" with what was searched.
Output: url | platform | name shown | address shown | phone shown | matches (yes/no/partly) |
date | note.
"""
SOCIAL = re.compile(r"facebook|instagram|linkedin|youtube|twitter|x\.com|tiktok|pinterest|nextdoor|threads", re.I)
MENTION = re.compile(r"news|press|award|article|magazine|podcast|blog", re.I)
REGISTRY = re.compile(r"secretary of state|sos\b|licen[sc]e|board|registry|registration", re.I)
FORMER = re.compile(r"former|previous|history|prior|old (name|address)", re.I)
ROBOT_BLOCK = (401, 403, 429, 999)


def _row(bgt, rx):
    for l in bgt.splitlines():
        if l.startswith("|") and re.search(rx, l):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            i = 2 if cells[0].isdigit() else 1   # Section A: # | Field | Value | Status; the other sections: Asset | Value | Status
            return cells[i] if len(cells) > i else ""
    return ""


def brand_facts(slug):
    st = read_json(client_dir(slug) / "status.json", {})
    bg = client_dir(slug) / "brand-guide.md"
    bgt = bg.read_text(encoding="utf-8") if bg.is_file() else ""
    nap = _row(bgt, r"Confirmed NAP")
    parts = [x.strip() for x in nap.split("·")]
    name = _row(bgt, r"^\|\s*1\s*\|") or (parts[0] if parts and parts[0] else "") or st.get("client", {}).get("name", "")
    address = parts[1] if len(parts) > 1 else ""
    phone = (parts[2] if len(parts) > 2 else "") or _row(bgt, r"^\|\s*8\s*\|")
    site = (re.search(r"https?://[^\s|)]+", _row(bgt, r"^\|\s*9\s*\|")) or [None])[0] or st.get("client", {}).get("domain", "")
    return {"brand": name, "address": address, "phone": phone, "website": site}


def cmd_prompt(a):
    f = brand_facts(a.slug)
    miss = [k for k in ("brand", "website") if not f[k]]
    if miss:
        die(f"REFUSED — the Brand Guide / status has no {', '.join(miss)} for this client.", 4)
    txt = PROMPT_C.format(BRAND=f["brand"], ADDRESS_OR_AREA=f["address"] or "its service area", PHONE=f["phone"] or "(not on file)",
                          WEBSITE=f["website"], YEAR=today()[:4])
    out = client_dir(a.slug) / "build" / "footprint" / "prompt-c.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(txt, encoding="utf-8")
    if a.stdout:
        print(txt)
        return
    print(f"Prompt C for {f['brand']} → {out.relative_to(ROOT)}\n"
          f"Paste it into Gemini Deep Research, save the report as clients/{a.slug}/inputs/footprint/report.md and run: "
          f"python3 scripts/footprint.py ingest {a.slug} clients/{a.slug}/inputs/footprint/report.md")


# ------------------------------------------------------------------ ingest
def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse(text):
    """→ ([row], [(what, searched)]) from the report's tables: url | platform | name shown | address shown | phone shown |
    matches | date | note."""
    rows, nf, head, in_nf = [], [], None, False
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            head = None
            in_nf = bool(re.search(r"not found", s, re.I))
            continue
        if re.match(r"^\|[\s\-:|]+\|$", s):
            continue
        c = _cells(s)
        low = [x.lower() for x in c]
        if head is None:
            if low and low[0].startswith("url") and any(x.startswith("platform") for x in low):
                head = [re.sub(r"[^a-z_]", "", x.split("(")[0].strip().replace(" ", "_")) for x in low]
            else:
                head = ["what", "searched"] if in_nf or "searched" in " ".join(low) else []
            continue
        if head[:2] == ["what", "searched"] or (in_nf and not head):
            nf.append((c[0], c[1] if len(c) > 1 else ""))
        elif head:
            r = {h: c[i] if i < len(c) else "" for i, h in enumerate(head)}
            if re.match(r"^https?://", r.get("url", "")) or FORMER.search(r.get("platform", "")):
                rows.append(r)
    return rows, nf


def _digits(s):
    d = re.sub(r"\D", "", s or "")
    return d[-10:] if len(d) >= 10 else d


def _words(s):
    return set(re.findall(r"[a-z0-9]+", re.sub(r"\b(suite|ste|unit|apt|#)\b", " ", (s or "").lower()))) - {"st", "street", "road", "rd", "ave", "avenue", "blvd", "drive", "dr", "usa"}


def nap_diff(shown, truth):
    """What differs between a listing and the confirmed NAP: [] when it matches."""
    out = []
    if truth["phone"] and shown["phone"] and _digits(shown["phone"]) != _digits(truth["phone"]):
        out.append(f"phone shown {shown['phone']}, confirmed {truth['phone']}")
    if truth["address"] and shown["address"]:
        ta, sa = _words(truth["address"]), _words(shown["address"])
        tn = next((w for w in re.findall(r"[a-z0-9]+", truth["address"].lower()) if w.isdigit()), "")
        sn = next((w for w in re.findall(r"[a-z0-9]+", shown["address"].lower()) if w.isdigit()), "")
        # a profile that shows only "Beaufort, SC" is a partial address, not a different one; a street number must agree
        if (sn and tn and sn != tn) or not (sa <= ta or (sn and ta <= sa)):
            out.append(f"address shown {shown['address']}, confirmed {truth['address']}")
    t = _words(truth["brand"])
    if t and shown["name"] and not (t <= _words(shown["name"]) or _words(shown["name"]) <= t):
        out.append(f"name shown {shown['name']}, confirmed {truth['brand']}")
    return out


def check_row(r, truth):
    """The script's own checks on one row. → the row with loads/name_on_page/matches_checked/diff/class filled."""
    import places
    code, body = places.fetch(r["url"])
    plat = r.get("platform", "")
    name_ok = bool(code == 200 and places._plain(truth["brand"]) in places._plain(body)) if truth["brand"] else False
    shown = {"name": r.get("name_shown", ""), "address": r.get("address_shown", ""), "phone": r.get("phone_shown", "")}
    diff = nap_diff(shown, truth)
    claimed = ((r.get("matches") or "").strip().lower().split() or [""])[0]
    checked = ("no" if claimed == "no" else "partly") if diff else claimed   # the report's own word never beats a mismatch
    kind = ("history" if FORMER.search(plat) else "mention" if MENTION.search(plat) and not SOCIAL.search(plat) else
            "registry" if REGISTRY.search(plat) else "social" if SOCIAL.search(plat) else "listing")
    return {**r, "http": code, "loads": code == 200, "blocked": code in ROBOT_BLOCK, "name_on_page": name_ok,
            "nap_diff": diff, "matches_checked": checked, "class": kind}


def cmd_ingest(a):
    import places
    rep = ROOT / a.report
    if not rep.is_file():
        die(f"no such report: {a.report}")
    truth = brand_facts(a.slug)
    rows, nf = parse(rep.read_text(encoding="utf-8"))
    if not rows:
        die("REFUSED — the report has no table in the required format (url | platform | name shown | address shown | phone "
            "shown | matches | date | note). Ask the VA to re-run Prompt C.", 4)
    kept, dropped, history, seen = [], [], [], set()
    for r in rows:
        if FORMER.search(r.get("platform", "")) and not re.match(r"^https?://", r.get("url", "")):
            history.append({"what": r["platform"], "value": r.get("name_shown") or r.get("address_shown") or r.get("note", ""),
                            "date": r.get("date", ""), "note": r.get("note", "")})
            continue
        if r["url"] in seen:
            continue
        seen.add(r["url"])
        c = check_row(r, truth)
        if c["class"] == "history":
            history.append({"what": r["platform"], "value": r.get("name_shown") or r.get("address_shown") or r.get("note", ""),
                            "date": r.get("date", ""), "note": r.get("note", ""), "url": r["url"]})
        elif not c["loads"] and not c["blocked"]:
            dropped.append({**c, "reason": f"URL did not load ({c['http'] or 'no answer'})"})
        else:
            kept.append(c)
    sameas = [c for c in kept if c["class"] in ("social", "listing") and c["matches_checked"] == "yes" and c["loads"]
              and c["name_on_page"]]
    by_hand = [c for c in kept if c["class"] in ("social", "listing") and c["matches_checked"] == "yes" and c not in sameas]
    issues = [c for c in kept if c["class"] in ("social", "listing", "registry") and c["matches_checked"] in ("no", "partly")]
    data = {"brand": truth, "checked": today(), "rows": kept, "dropped": dropped, "history": history,
            "not_found": [{"what": x, "searched": y} for x, y in nf],
            "sameas": [c["url"] for c in sameas], "open_by_hand": [c["url"] for c in by_hand],
            "nap_issues": [{"url": c["url"], "platform": c["platform"], "diff": c["nap_diff"] or [c.get("note", "")]}
                           for c in issues]}
    base = client_dir(a.slug)
    (base / "data" / "footprint").mkdir(parents=True, exist_ok=True)
    write_json(base / "data" / "footprint" / "footprint.json", data)
    prop = base / "build" / "footprint" / "section-f-proposal.md"
    prop.parent.mkdir(parents=True, exist_ok=True)
    prop.write_text(proposal(a.slug, data, sameas), encoding="utf-8")
    print(f"{truth['brand']}: {len(kept)} listing(s) kept · {len(dropped)} dropped (URL failed) · {len(sameas)} sameAs "
          f"candidate(s) · {len(by_hand)} to open by hand · {len(issues)} NAP mismatch(es) · {len(history)} history row(s)\n"
          f"Proposal for Paul (the Brand Guide is not edited) → {prop.relative_to(ROOT)}")


def proposal(slug, d, sameas):
    day = d["checked"]
    soc = [c["url"] for c in sameas if c["class"] == "social"]
    lst = [c["url"] for c in sameas if c["class"] == "listing"]
    apple = [c["url"] for c in sameas if "apple" in c.get("platform", "").lower()]
    L = [f"# Prompt C — proposed Section F rows ({day})", "",
         "Proposal only. Paul approves; nothing here is in the Brand Guide yet. Each URL loaded and showed the brand's name;"
         " the NAP on it matched the confirmed NAP.", "",
         "| Asset | Value | Status |", "|---|---|---|",
         f"| Full citation list → sameAs | {' · '.join(lst) if lst else '[NEED: none found that match]'} | "
         f"{'Internally Verified (Prompt C, ' + day + ')' if lst else 'Unknown'} |",
         f"| Social profile list | {' · '.join(soc) if soc else '[NEED: none found that match]'} | "
         f"{'Internally Verified (Prompt C, ' + day + ')' if soc else 'Unknown'} |",
         f"| Apple Maps link → sameAs | {apple[0] if apple else '[NEED]'} | "
         f"{'Internally Verified (Prompt C, ' + day + ')' if apple else 'Unknown'} |", ""]
    if d["open_by_hand"]:
        L += ["## Open by hand (the site blocks robots; the report says it matches)", ""] + [f"- {u}" for u in d["open_by_hand"]] + [""]
    L += ["## Citation / NAP check — listings that do not match", ""]
    L += ([f"- {i['platform']} {i['url']} — " + "; ".join(i["diff"]) for i in d["nap_issues"]] or ["- none"]) + [""]
    L += ["## History rows for the Decision Sheet (former names, addresses, lines of business)", ""]
    L += ([f"- {h['what']}: {h['value']}" + (f" ({h['date']})" if h.get("date") else "") + (f" — {h['note']}" if h.get("note") else "")
           for h in d["history"]] or ["- none found"]) + [""]
    if d["not_found"]:
        L += ["## Not found (what was searched)", ""] + [f"- {n['what']}: {n['searched']}" for n in d["not_found"]] + [""]
    return "\n".join(L)


def cmd_show(a):
    d = read_json(client_dir(a.slug) / "data" / "footprint" / "footprint.json")
    if not d:
        die("no footprint stored — footprint.py prompt, then ingest", 4)
    print(f"{d['brand']['brand']} ({d['checked']}): {len(d['rows'])} listing(s) · sameAs {len(d['sameas'])} · "
          f"NAP issues {len(d['nap_issues'])} · history {len(d['history'])}")
    for u in d["sameas"]:
        print(f"  sameAs {u}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prompt"); s.add_argument("slug"); s.add_argument("--stdout", action="store_true")
    s = sub.add_parser("ingest"); s.add_argument("slug"); s.add_argument("report")
    s = sub.add_parser("show"); s.add_argument("slug")
    a = ap.parse_args()
    {"prompt": cmd_prompt, "ingest": cmd_ingest, "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    main()
