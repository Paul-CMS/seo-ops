#!/usr/bin/env python3
"""review.py — one review sheet per section per step; decide by default (CM-061 part 3; rewrite 3 §5, §3.4).

    review.py sheet <slug> <section> <briefs|drafts> --findings F.json --run R
                    the ONE checker pass's findings → build/<section>/<step>-review.csv (+ .md for Paul, .json)
    review.py apply <slug> <section> <briefs|drafts> --run R [--answers "accept all except 7b, 12c"]
                    record the answers (an empty answer = the recommended option) → build/<section>/<step>-apply.json,
                    the list the agent applies to every page in one run
    review.py overdue <slug> [--run R --apply]   Ask rows unanswered for N working days (config.json
                    overdue_ask_working_days): kinds 1, 3, 4 ship with the recommended option and an open-item notice;
                    kind 2 (legal or money) is left out of the page until answered
    review.py usage <slug> <section>             evidence used per page: "Evidence used: 6 of 9 excerpts"

Findings (JSON list) — one per page + rule + item: {page, rule, item, finding, severity fix|fix_and_list|ask,
category, plain_why, decided_for_you, options [..], recommended "a", kind 1–4 (asks), fact_key/fact_id/decision_key,
log (kind 3: a research-log id), sources (kind 4: two)}. methodology/review-severities.json says what each severity may
cover; this script enforces it:
  - a Fix is form only (fixed silently, logged in the run only); content is "Fix and list" (listed, applied by default)
  - an Ask is one of four kinds; anything else with a recommended option becomes "Fix and list"
  - a kind-3 Ask links a valid client research-log entry (research.py); a kind-4 Ask names two sources
  - a finding is keyed page + rule + item: a duplicate, or one already decided in this section, is never raised again
  - an Ask already answered in facts.json or decisions-settled.md — or already asked and waiting — never appears
  - in the drafts step the usage check adds a per-page line and, when a pack has 2+ review excerpts the draft does not
    use, a "Fix and list" row (rewrite one passage with the strongest excerpt)
Paul answers in the sheet or in one chat line; the approval then accepts the section at any later state.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys

import status as S
from lib import ROOT, append, client_dir, config, die, now, read_json, today, write_json

SEV = json.loads((ROOT / "methodology" / "review-severities.json").read_text(encoding="utf-8"))
STEPS = ("briefs", "drafts")
COLS = ["id", "page", "url", "item", "finding", "plain_why", "decided_for_you", "options", "recommended", "answer", "note"]
KNOWN = ("client_confirmed", "paul_approved", "internally_verified")
LETTERS = "abcdefghij"


def paths(slug, section, step):
    d = client_dir(slug) / "build" / section
    return {"csv": d / f"{step}-review.csv", "json": d / f"{step}-review.json", "md": d / f"{step}-review.md",
            "apply": d / f"{step}-apply.json", "fixes": d / f"{step}-fixes.json", "ledger": d / "findings-ledger.json"}


def _norm(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower()).strip("-")


def fkey(f):
    return "|".join(_norm(f.get(x)) for x in ("page", "rule", "item"))


# ------------------------------------------------------------------ answered already?
def _fact_rows(slug):
    import facts
    return facts.load(slug)["facts"]


def known_fact(slug, fact_key=None, fact_id=None):
    """A Known facts.json row for a facts id or a fact key (fact:d:<label words>), or None."""
    words = None
    if fact_key and fact_key.startswith("fact:d:"):
        words = fact_key[7:].replace("_", " ")
    for r in _fact_rows(slug):
        if r.get("status") not in KNOWN:
            continue
        if fact_id and r["id"] == fact_id:
            return r
        lab = re.sub(r"[^a-z ]+", " ", str(r.get("label", "")).lower())
        lab = re.sub(r"\s+", " ", lab).strip()
        if words and r.get("section") == "D" and lab.startswith(words):
            return r
        if fact_key and r.get("key") == fact_key:
            return r
    return None


def answered(slug, f, ents):
    """Why this Ask must not appear (answered in facts.json or decisions-settled.md, or asked and waiting), or None."""
    import settled
    r = known_fact(slug, f.get("fact_key"), f.get("fact_id"))
    if r:
        return f"answered in facts.json ({r['id']}, {r.get('status')})"
    for k in [f.get(x) for x in ("decision_key", "fact_key") if f.get(x)]:
        e = ents.get(k) or {}
        if e.get("state") in ("settled", "answered"):
            return f"answered in decisions-settled.md ({k}, {(e.get('at') or e.get('answered_at') or '')[:10]})"
        if e.get("state") == "open":
            return f"already asked {e.get('asked_at', '')[:10]} ({k}) — waiting, not asked again"
        rel = [(rk, re_) for rk, re_ in ents.items() if rk != k and re_.get("state") in ("settled", "answered", "open")
               and settled.related(rk, k)]
        if rel:
            rk, re_ = rel[0]
            return f"{'already asked, waiting' if re_.get('state') == 'open' else 'answered'} under {rk} (decisions-settled.md)"
    kept, dropped, _ = settled.filter_questions(slug, [{"text": f.get("finding", ""), "key": f.get("decision_key") or "",
                                                        "fact_id": f.get("fact_id") or ""}])
    if dropped:
        return f"answered in decisions-settled.md ({dropped[0][1]})"
    return None


# ------------------------------------------------------------------ severity rules
def classify(f, slug):
    """(severity, note, problem) — the severity the finding may have, a note when it was changed, or a problem."""
    sev = f.get("severity")
    cat = f.get("category") or ""
    has_default = bool(f.get("recommended") or f.get("decided_for_you"))
    if sev == "fix":
        if cat in SEV["fix"]["categories"] or cat == "known_fact_used":
            return "fix", "", None
        if has_default:
            return "fix_and_list", f"not form ({cat or 'no category'}) — listed as Decided for you", None
        return None, "", "a Fix is form only; a content change needs its default (decided_for_you)"
    if sev == "ask":
        kind = str(f.get("kind") or "")
        if kind not in SEV["ask"]["kinds"]:
            if has_default:
                return "fix_and_list", "has a recommended option and is not one of the four Ask kinds — decided by default", None
            return None, "", "an Ask must be one of the four kinds (1 page/URL · 2 legal or money · 3 client fact · 4 conflict)"
        if len(f.get("options") or []) < 2 or not f.get("recommended"):
            return None, "", "an Ask needs at least two options and a recommended default"
        if kind == "3":
            import research
            row = next((r for r in research.entries(slug) if r.get("id") == f.get("log")), None)
            if not row or row.get("kind") != "client" or row.get("result") != "not_found" or research.problems(row):
                return None, "", (f"a kind-3 Ask links a valid client research-log entry (research.py log … --kind client "
                                  f"--result not_found); got {f.get('log') or 'none'}")
        if kind == "4" and len(f.get("sources") or []) < 2:
            return "fix_and_list" if has_default else None, "a conflict names two sources of equal standing — none given", \
                (None if has_default else "a kind-4 Ask names the two sources that disagree")
        return "ask", "", None
    if sev == "fix_and_list":
        if not has_default:
            return None, "", "a Fix-and-list row says what was decided for you (decided_for_you)"
        return "fix_and_list", "", None
    return None, "", f"severity must be fix, fix_and_list or ask (got {sev!r})"


# ------------------------------------------------------------------ §3.4 usage check
def _words(t):
    return re.findall(r"[a-z0-9$%]+", str(t).lower())


def usage(slug, section, pid, st=None, stage="draft"):
    """(used, total, unused review excerpts [..], draft text) for one page — excerpts from its pack JSON."""
    st = st or S.load(slug)
    pk = read_json(client_dir(slug) / "build" / section / "packs" / f"{pid}.json") or {}
    ex = pk.get("excerpts") or []
    rec = ((st["pages"].get(pid) or {}).get("files") or {}).get(stage) or {}
    text = (ROOT / rec["file"]).read_text(encoding="utf-8") if rec.get("file") and (ROOT / rec["file"]).is_file() else ""
    tw = " ".join(_words(text))
    used, topics_hit = set(), set()
    for e in ex:
        w = _words(e["text"])
        if any(" ".join(w[i:i + 5]) in tw for i in range(0, max(1, len(w) - 4))) and len(w) >= 5:
            used.add(e["id"])
    import evidence_pack as EP
    for e in ex:   # a paraphrase counts once per topic (the writer quotes the gist, not the review)
        t = e.get("topic", "")
        if e["id"] in used or t in topics_hit or not t.startswith("practice: "):
            continue
        rx = (EP.PRACTICES.get(t[len("practice: "):]) or (None,))[0]
        if rx and re.search(rx, text, re.I):
            used.add(e["id"]); topics_hit.add(t)
    reviews = [e for e in ex if e["kind"] == "review"]
    unused = [e for e in reviews if e["id"] not in used]
    return len(used), len(ex), (unused if reviews and not any(e["id"] in used for e in reviews) else []), text


def usage_findings(slug, section, st, stage="draft"):
    b = S.batch(st, section) or die(f"no section {section}")
    lines, out = [], []
    for pid in b["pages"]:
        u, n, unused, _ = usage(slug, section, pid, st, stage)
        lines.append({"page": pid, "url": st["pages"][pid].get("url", ""), "used": u, "total": n})
        if len(unused) >= 2:
            best = sorted(unused, key=lambda e: ({"known": 0, "unchecked": 1, "example": 2}.get(e.get("tier"), 3), -len(e["text"])))[0]
            out.append({"page": pid, "url": st["pages"][pid].get("url", ""), "rule": "usage", "item": "review evidence",
                        "severity": "fix_and_list", "category": "pack_evidence_added",
                        "finding": f"The pack has {len(unused)} review excerpts and the {stage} uses none.",
                        "plain_why": "Real customer words make the page specific and trustworthy; the evidence is already on file.",
                        "decided_for_you": f"Rewrite one passage to use the strongest excerpt at its usage tier ({best['topic']}): "
                                           f"\"{best['text'][:160]}\"",
                        "options": ["use the strongest excerpt (attributed, at its tier)", "leave the draft as written"],
                        "recommended": "a"})
    return lines, out


# ------------------------------------------------------------------ sheet
def _opts(f):
    o = f.get("options") or ([f["decided_for_you"], "keep it as it was"] if f.get("decided_for_you") else [])
    return o


def build_sheet(slug, section, step, findings, run_id):
    if step not in STEPS:
        die(f"step must be one of {', '.join(STEPS)}")
    st = S.load(slug)
    b = S.batch(st, section) or die(f"no section (batch) {section} in the site plan")
    p = paths(slug, section, step)
    ledger = read_json(p["ledger"]) or {}
    import settled
    ents = settled.entries(slug)
    usage_lines = []
    usage_lines, extra = usage_findings(slug, section, st, "draft" if step == "drafts" else "brief")   # §3.4
    findings = list(findings) + extra
    if step == "drafts":
        prev = read_json(paths(slug, section, "briefs")["json"]) or {}   # a brief Ask still open is carried, once
        if prev and not (b.get("review") or {}).get("briefs", {}).get("applied"):
            findings += [r["_finding"] for r in prev.get("rows", []) if r.get("severity") == "ask"]
    rows, fixes, dropped, problems, seen = [], [], [], [], set()
    for f in findings:
        f = dict(f)
        f.setdefault("url", (st["pages"].get(f.get("page")) or {}).get("url", ""))
        if f.get("severity") == "ask":
            f.setdefault("category", "ask")
            f["category"] = f["category"] or "ask"
        missing = [x for x in SEV["finding_fields"]["required"] if not f.get(x)]
        if missing:
            problems.append(f"{f.get('page')} · {f.get('rule')} · {f.get('item')}: missing {', '.join(missing)}")
            continue
        k = fkey(f)
        if k in seen:
            dropped.append((f, "duplicate — the same page + rule + item is raised once"))
            continue
        seen.add(k)
        if k in ledger:
            dropped.append((f, f"decided earlier in this section ({ledger[k]['step']}, {ledger[k]['at'][:10]}) — never raised again"))
            continue
        sev, note, prob = classify(f, slug)
        if prob:
            problems.append(f"{f['page']} · {f['rule']} · {f['item']}: {prob}")
            continue
        if sev == "ask":
            why = answered(slug, f, ents)
            if why:
                dropped.append((f, why))
                continue
        if sev == "fix":
            fixes.append(f)
            continue
        rows.append({"severity": sev, "kind": str(f.get("kind") or ""), "key": k, "note": note, "_finding": f})
    if problems:
        die("REFUSED — findings break the review rules (methodology/review-severities.json, CM-061):\n  - "
            + "\n  - ".join(problems), 4)
    rows.sort(key=lambda r: (r["severity"] != "ask", r["kind"], r["_finding"]["page"]))
    out_rows = []
    for i, r in enumerate(rows, 1):
        f = r["_finding"]
        opts = _opts(f)
        rec = f.get("recommended") or "a"
        out_rows.append({**r, "id": str(i), "page": f["page"], "url": f.get("url", ""), "item": f["item"],
                         "finding": f["finding"], "plain_why": f.get("plain_why", ""),
                         "decided_for_you": f.get("decided_for_you", "") if r["severity"] == "fix_and_list" else "",
                         "options": " · ".join(f"{LETTERS[j]}) {o}" for j, o in enumerate(opts)), "recommended": rec,
                         "answer": "", "note": "; ".join(x for x in (r["note"], f.get("note", ""),
                                                                     f"Ask kind {r['kind']}" if r["kind"] else "") if x)})
    for j, u in enumerate(usage_lines, 1):
        out_rows.append({"id": f"U{j}", "page": u["page"], "url": u["url"], "item": "evidence used",
                         "finding": f"Evidence used: {u['used']} of {u['total']} excerpts", "plain_why": "", "decided_for_you": "",
                         "options": "", "recommended": "", "answer": "", "note": "usage check (§3.4)", "severity": "info"})
    p["csv"].parent.mkdir(parents=True, exist_ok=True)
    with open(p["csv"], "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(out_rows)
    write_json(p["json"], {"made": now(), "run": run_id, "step": step, "section": section, "rows": out_rows,
                           "dropped": [{"page": f["page"], "rule": f["rule"], "item": f["item"], "why": why} for f, why in dropped],
                           "usage": usage_lines})
    write_json(p["fixes"], {"made": now(), "run": run_id, "fixes": fixes})
    asks = [r for r in out_rows if r.get("severity") == "ask"]
    listed = [r for r in out_rows if r.get("severity") == "fix_and_list"]
    p["md"].write_text(render(st, section, step, asks, listed, usage_lines, dropped, fixes))
    st = S.load(slug)
    b = S.batch(st, section)
    b.setdefault("review", {})[step] = {"sheet": str(p["csv"].relative_to(ROOT)), "md": str(p["md"].relative_to(ROOT)),
                                        "at": now(), "run": run_id, "asks": len(asks), "listed": len(listed),
                                        "fixes": len(fixes), "dropped": len(dropped), "applied": None}
    S.save(slug, st)
    append(client_dir(slug) / "log.md", f"- REVIEW SHEET {now()[:16]} · run {run_id} · {section} {step}: {len(asks)} Ask, "
           f"{len(listed)} decided for you, {len(fixes)} fixed silently, {len(dropped)} not raised (duplicate, decided or "
           f"answered) · {p['csv'].relative_to(ROOT)}\n")
    return p, asks, listed, fixes, dropped


def render(st, section, step, asks, listed, usage_lines, dropped, fixes):
    name = st["client"]["name"]
    out = [f"# {name} — {section} {step} review", "",
           f"_One sheet for the section's {step} (CM-061). Answer in the CSV (`{step}-review.csv`, an empty answer accepts "
           f"the recommended option) or in one line: \"accept all\" or \"accept all except 7b, 12c\"._", ""]
    out += [f"## Questions for you ({len(asks)})", ""]
    for r in asks:
        out += [f"**{r['id']}. {r['item']}** — {r['page']} ({r['url']})", f"- What: {r['finding']}",
                f"- Why it matters: {r['plain_why']}", f"- Options: {r['options']} — recommended **{r['recommended']}**", ""]
    if not asks:
        out += ["_None._", ""]
    out += [f"## Decided for you ({len(listed)}) — change any by naming its number", ""]
    out += [f"- **{r['id']}.** {r['page']} · {r['item']}: {r['finding']} → **{r['decided_for_you']}**" for r in listed] or ["_None._"]
    if usage_lines:
        out += ["", "## Evidence used per page", ""]
        out += [f"- {u['page']}: Evidence used: {u['used']} of {u['total']} excerpts" for u in usage_lines]
    out += ["", f"_Fixed silently (form only): {len(fixes)}. Not raised again (duplicate, decided earlier in the section, "
                f"or already answered): {len(dropped)}._"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ apply
def parse_answers(line):
    """'accept all except 7b, 12c' / '7b 12c' / 'accept all' → {'7': 'b', '12': 'c'}."""
    if not line:
        return {}
    tail = re.split(r"\bexcept\b", line, 1, flags=re.I)[-1] if re.search(r"\bexcept\b", line, re.I) else line
    return {m.group(1): m.group(2).lower() for m in re.finditer(r"\b(\d+)\s*([a-j])\b", tail, re.I)}


def apply(slug, section, step, run_id, answers_line=None):
    p = paths(slug, section, step)
    data = read_json(p["json"]) or die(f"no {step} review sheet for {section} — review.py sheet first")
    over = parse_answers(answers_line)
    cells = {}
    if p["csv"].is_file():
        with open(p["csv"], newline="", encoding="utf-8-sig") as fh:
            cells = {r["id"]: (r.get("answer") or "").strip() for r in csv.DictReader(fh)}
    rows = [r for r in data["rows"] if r.get("severity") in ("ask", "fix_and_list")]
    ids = {r["id"] for r in rows}
    bad = [i for i in over if i not in ids]
    if bad:
        die(f"REFUSED — no row {', '.join(bad)} in the {section} {step} review sheet (rows {', '.join(sorted(ids, key=int))})", 4)
    ledger = read_json(p["ledger"]) or {}
    out, explicit = [], 0
    for r in rows:
        opts = [re.sub(r"^[a-j]\)\s*", "", o) for o in r["options"].split(" · ")] if r["options"] else []
        cell = cells.get(r["id"], "")
        omit = cell.lower().startswith("omit")
        if r["id"] in over:
            choice, by = over[r["id"]], "Paul"
        elif re.fullmatch(r"[a-j]", cell.lower()[:1] or "-") and (len(cell) == 1 or not cell[1].isalpha()):
            choice, by = cell.lower()[0], "Paul" if "overdue default" not in cell else "overdue default"
        elif cell and not omit:
            choice, by = "other", "Paul"
        elif omit:
            choice, by = "omit", "overdue (legal or money claim)"
        else:
            choice, by = r["recommended"] or "a", "default"
        explicit += by == "Paul"
        if choice == "other":
            action = cell
        elif choice == "omit":
            action = "Leave the claim out of the page — remove the sentence, do not soften it — until Paul answers"
        else:
            idx = LETTERS.index(choice)
            if idx >= len(opts):
                die(f"REFUSED — row {r['id']} has no option {choice} ({r['options']})", 4)
            action = opts[idx]
        item = {"id": r["id"], "page": r["page"], "url": r["url"], "item": r["item"], "severity": r["severity"],
                "kind": r.get("kind", ""), "choice": choice, "action": action, "by": by}
        if "overdue" in by:
            item["open_item"] = (f"[NEED: {r['item']} — legal or money claim left out until answered ({today()})]" if choice == "omit"
                                 else f"[NEED: confirm {r['item']} — shipped with the default \"{action[:80]}\" after "
                                      f"{config().get('overdue_ask_working_days', 3)} working days ({today()})]")
        out.append(item)
        ledger[r["key"]] = {"step": step, "at": now(), "choice": choice, "action": action[:200], "by": by}
    write_json(p["apply"], {"made": now(), "run": run_id, "section": section, "step": step, "answers": answers_line or "",
                            "items": out})
    write_json(p["ledger"], ledger)
    st = S.load(slug)
    b = S.batch(st, section)
    rv = b.setdefault("review", {}).setdefault(step, {})
    rv["applied"] = {"at": now(), "run": run_id, "answers": answers_line or "", "explicit": explicit,
                     "file": str(p["apply"].relative_to(ROOT))}
    S.save(slug, st)
    append(client_dir(slug) / "log.md", f"- REVIEW APPLIED {now()[:16]} · run {run_id} · {section} {step}: {len(out)} row(s) "
           f"({explicit} answered by Paul, the rest by default) · {p['apply'].relative_to(ROOT)}\n")
    return out


def applied(st, bid, step):
    """(has a sheet, applied) for a batch step — the approval accepts the section only after the review is applied."""
    rv = ((S.batch(st, bid) or {}).get("review") or {}).get(step)
    return bool(rv), bool(rv and rv.get("applied"))


# ------------------------------------------------------------------ §5.4 overdue
def working_days(since, until=None):
    d0 = dt.date.fromisoformat(since[:10])
    d1 = until or dt.date.fromisoformat(today())
    n, d = 0, d0
    while d < d1:
        d += dt.timedelta(days=1)
        n += d.weekday() < 5
    return n


def overdue(slug, run_id=None, do_apply=False, until=None):
    limit = int(config().get("overdue_ask_working_days") or 3)
    st = S.load(slug)
    out = []
    for b in S.batches(st):
        for step, rv in (b.get("review") or {}).items():
            if rv.get("applied"):
                continue
            p = paths(slug, b["id"], step)
            age = working_days(rv["at"], until)
            if age < limit or not p["csv"].is_file():
                continue
            with open(p["csv"], newline="", encoding="utf-8-sig") as fh:
                rows = list(csv.DictReader(fh))
            data = read_json(p["json"]) or {}
            kinds = {r["id"]: r.get("kind", "") for r in data.get("rows", [])}
            sev = {r["id"]: r.get("severity") for r in data.get("rows", [])}
            changed = False
            for r in rows:
                if sev.get(r["id"]) != "ask" or (r.get("answer") or "").strip():
                    continue
                k = kinds.get(r["id"], "")
                out.append((b["id"], step, r["id"], k, r["item"], age))
                if do_apply:
                    r["answer"] = ("omit" if k in SEV["ask"]["never_default"]
                                   else f"{r['recommended']} (overdue default {today()})")
                    changed = True
            if changed:
                with open(p["csv"], "w", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=COLS)
                    w.writeheader(); w.writerows(rows)
                append(client_dir(slug) / "log.md", f"- OVERDUE ASKS {now()[:16]} · run {run_id} · {b['id']} {step}: "
                       f"{sum(1 for x in out if x[0] == b['id'] and x[1] == step)} row(s) after {age} working days — kinds 1, 3, 4 "
                       "take the recommended option; kind 2 is left out of the page until answered\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet"); s.add_argument("slug"); s.add_argument("section"); s.add_argument("step", choices=STEPS)
    s.add_argument("--findings", required=True); s.add_argument("--run", required=True)
    s = sub.add_parser("apply"); s.add_argument("slug"); s.add_argument("section"); s.add_argument("step", choices=STEPS)
    s.add_argument("--run", required=True); s.add_argument("--answers")
    s = sub.add_parser("overdue"); s.add_argument("slug"); s.add_argument("--run"); s.add_argument("--apply", action="store_true")
    s = sub.add_parser("usage"); s.add_argument("slug"); s.add_argument("section")
    a = ap.parse_args()
    if a.cmd in ("sheet", "apply") or (a.cmd == "overdue" and a.apply):
        if not a.run:
            die("--run is required to change anything")
        import run as R
        R.open_run(a.slug, a.run)
    if a.cmd == "sheet":
        f = ROOT / a.findings if not a.findings.startswith("/") else __import__("pathlib").Path(a.findings)
        findings = json.loads(f.read_text(encoding="utf-8"))
        p, asks, listed, fixes, dropped = build_sheet(a.slug, a.section, a.step, findings, a.run)
        print(f"{a.section} {a.step} review: {len(asks)} question(s) for Paul, {len(listed)} decided for you, "
              f"{len(fixes)} fixed silently, {len(dropped)} not raised → {p['csv'].relative_to(ROOT)}")
        for f_, why in dropped:
            print(f"  not raised: {f_['page']} · {f_['rule']} · {f_['item']} — {why}")
        if not asks:
            print("No questions: apply it now (review.py apply …) — the approval line follows.")
    elif a.cmd == "apply":
        items = apply(a.slug, a.section, a.step, a.run, a.answers)
        print(f"{a.section} {a.step}: {len(items)} row(s) recorded → {paths(a.slug, a.section, a.step)['apply'].relative_to(ROOT)}"
              " — apply every item to its page in this run, then re-record the files.")
    elif a.cmd == "overdue":
        rows = overdue(a.slug, a.run, a.apply)
        for bid, step, rid, k, item, age in rows:
            print(f"{bid} {step} row {rid} (kind {k or '?'}) · {item} · {age} working days · "
                  + ("left out of the page until answered" if k in SEV["ask"]["never_default"] else "ships with the recommended option"))
        print(f"{len(rows)} overdue Ask(s)" + (" — answers written; run review.py apply" if a.apply and rows else ""))
    elif a.cmd == "usage":
        st = S.load(a.slug)
        for u in usage_findings(a.slug, a.section, st)[0]:
            print(f"{u['page']:28} Evidence used: {u['used']} of {u['total']} excerpts")


if __name__ == "__main__":
    main()
