#!/usr/bin/env python3
"""status.py — read and maintain clients/<slug>/status.json.

    status.py init <slug> --name "Client Name" --domain example.com --type full|blog-only
                          --industry roofing [--category C|none | --sensitive yes|no] [--practitioner yes|no]
                          [--route A|B] [--drive-folder-id ID]
    status.py classify "<industry>"                  sensitive-industry check (CM-025, CM-040); exit 9 = ask Paul
    status.py sensitivity <slug> <category>|none --run R [--practitioner yes|no]   Paul's answer, logged
    status.py cap <slug> alt_text|broken_link|image_url|meta_description <n>|none --run R
                                                     per-client safe-fix cap (wp.py enforces it), logged
    status.py show <slug> [--json]
    status.py require <slug> <gate> [<gate> ...]     exit 0 if met, 4 if not
    status.py set <slug> <field> <value>              non-gate fields only
    status.py view <slug>                             the client-facing summary (generated; read-only)
    status.py page <slug> <page_id> --type service|location|county|homepage|about|blog
                          [--name N] [--url U] [--state S] [--file F]
    status.py mark <slug> <artifact> --file F [--file F2 ...]   record the files an approval will cover
    status.py plan <slug> --file plan.md --json plan.json
    status.py batch <slug> <batch_id> --state S [--files f1,f2]   briefs_written / drafts_written collect the
                                                      per-page files (each from its own run, CM-043)
    status.py page-stage <slug> <page_id> --stage brief|draft --file F --run R
                                                      record one page's brief (from the batch's one brief run, CM-054)
                                                      or draft (from its own run, CM-043); a brief needs the evidence
                                                      gate cleared (CM-041); a draft is refused with a placeholder
                                                      that has no [NEED: ...] note (CM-016)
    status.py modes <slug>                            each producing stage's mode: review / auto (CM-044)
    status.py pilot-corrections <slug> --note T      (re-stamps the specs it changed: the global approval stands)
    status.py blockers-none <slug> --run R            the blocker checklist has no items (blockers_cleared is met)
    status.py approval-record <slug>                  render the Drive Approval Record (Markdown)

Gates are NOT settable here. Only approve.py, run through /approve, can set a gate.

Voiding (Paul, 2026-10-02): an approval names the files it covers. If one of them changes,
only THAT gate stops counting as met. Later gates that depend on it stay open and are
flagged "upstream change — check whether it affects this"; Paul decides.
"""
import argparse
import datetime
import json
import re
import sys
import time
from pathlib import Path

from lib import ROOT, append, client_dir, die, now, read_json, ref_missing, ref_sha, ref_sha_v2, sha12, write_json, config

GATES = json.loads((ROOT / "scripts" / "gates.json").read_text())

SETTABLE = {
    "client.name", "client.domain", "client.industry", "client.route",
    "client.drive_folder_id", "client.kadence_head_meta_key", "client.gbp_url",
    "client.gbp_website_url", "client.address_type", "client.notes", "client.state", "client.cms",
}
SAFE_FIX_CAP_KINDS = ["alt_text", "broken_link", "image_url", "meta_description"]
BATCH_STATES = ["planned", "briefs_written", "drafts_written", "sem_applied", "sem_check_failed", "drafted",
                "handed_off", "corrections_requested", "published", "verified", "written_back"]
# CM-055: a batch whose pages are WordPress drafts (or later) never holds up the next batch
DRAFTED_OR_LATER = ("drafted", "handed_off", "corrections_requested", "published", "verified", "written_back")
PAGE_STATES = ["planned", "brief_written", "draft_written", "approved", "drafted", "published",
               "written_back", "verified"]
# batch state -> the state every page in the batch moves to
BATCH_TO_PAGE = {"briefs_written": "brief_written", "drafts_written": "draft_written",
                 "sem_applied": "draft_written", "drafted": "drafted", "handed_off": "drafted", "published": "published",
                 "verified": "verified", "written_back": "written_back"}
STAGES = ["briefs", "drafts"]   # two stops per batch: briefs (outline before prose), then drafts + SEM picks


def path(slug):
    return client_dir(slug) / "status.json"


def load(slug):
    return read_json(path(slug))


def save(slug, st):
    st["updated"] = now()
    st["client_view"] = client_view(st)
    write_json(path(slug), st)


# ------------------------------------------------------------------ client-facing summary
PHRASES = json.loads((ROOT / "methodology" / "client-phrases.json").read_text())
FILE_CODES = r"\b(SB|SD|LB|LD|LBCH|LDCH|HB|HD|AB|AD|PB|PD|SF|LNKD|DFS|GSC|BL)\b"
RULE_IDS = r"\b(CM|RULE|BB|SEM|GOV|PROC|CF|HP|SVC|LOC|HUB|ABT|BLG|COM)-?\d+|\bF-\d+|\bS\d{2}\b|\bGOV-T\d+"


def client_view_problems(text):
    """Anything a client must never see: rule IDs, gate names, file codes, internal names."""
    probs = []
    if re.search(RULE_IDS, text):
        probs.append(f"rule ID {re.search(RULE_IDS, text).group(0)!r}")
    names = set(GATES["gates"]) | set(GATES["conditions"]) | set(GATES["retired_gates"]) | {"site_plan"}
    for n in names:
        if re.search(r"\b" + re.escape(n) + r"\b", text):
            probs.append(f"gate name {n!r}")
    if re.search(FILE_CODES, text):
        probs.append(f"file code {re.search(FILE_CODES, text).group(0)!r}")
    if re.search(r"batch:|page:|status\.json|\.py\b|/approve|\bslug\b", text):
        probs.append("an internal command or file name")
    return probs


def client_view(st):
    """Built only from methodology/client-phrases.json, from where the client stands."""
    P, done, waiting = PHRASES, [], []
    decided = lambda g: _decided(st, g)
    c = st["client"]
    if c["type"] == "blog-only":
        phase = "articles" if decided("entity_approved") else "getting_started"
        order = ["entity_approved", "blog_topics_approved"]
    else:
        bs = batches(st)
        if not decided("entity_approved"):
            phase = "getting_started"
        elif not condition_met(st, "proof_sheet_returned")[0]:
            phase = "confirming_details"
        elif not decided("discovery_signed_off"):
            phase = "reviewing_site"
        elif not check(st, "site_plan")[0]:
            phase = "planning_pages"
        elif not condition_met(st, "pages_built")[0]:
            later = ("handed_off", "corrections_requested", "published", "verified", "written_back")
            phase = "publishing" if any(b.get("state") in later for b in bs) else "writing_pages"
        elif not decided("release_approved"):
            phase = "final_checks"
        else:
            phase = "articles"
        order = ["entity_approved", "proof_sheet_approved", "proof_sheet_returned", "audit_approved",
                 "brand_guide_approved", "discovery_signed_off", "site_plan", "pages_live",
                 "release_approved"]
        if decided("proof_sheet_approved") and not condition_met(st, "proof_sheet_returned")[0]:
            waiting.append(P["waiting"]["proof_sheet"])
    live = sum(1 for p in st["pages"].values() if p.get("type") != "blog"
               and p.get("state") in ("published", "verified", "written_back"))
    posts = sum(1 for p in st["pages"].values() if p.get("type") == "blog"
                and (p.get("approval") or {}).get("state") in GATES["met_decisions"])
    for k in order + ["posts_published"]:
        if k == "pages_live":
            ok = live > 0
        elif k == "posts_published":
            ok = posts > 0
        elif k == "site_plan":
            ok = check(st, "site_plan")[0]
        elif k in GATES["conditions"]:
            ok = condition_met(st, k)[0]
        else:
            ok = decided(k)
        if ok:
            done.append(P["done"][k].format(n=live if k == "pages_live" else posts))
    view = {"_note": "The only client-facing part of this file, built from methodology/client-phrases.json. "
                     "Nothing else here is ever shown to a client.",
            "phase": P["phases"][phase]["phase"], "done": done, "waiting_on_client": waiting,
            "next": P["phases"][phase]["next"]}
    for t in [view["phase"], view["next"]] + done + waiting:
        bad = client_view_problems(t)
        if bad:
            die(f"client view blocked — {t!r} contains {', '.join(bad)}. Fix methodology/client-phrases.json.")
    return view


# ------------------------------------------------------------------ sensitive industries (CM-025)
def classify(industry):
    """('yes', category, practitioner) · ('no', None, False) · ('unsure', hint or None, False).

    'no' only for a trade on config.json not_sensitive_trades; anything not clearly in or out of
    a list is 'unsure', so /new-client asks Paul (CM-040)."""
    text = " " + re.sub(r"[^a-z0-9 ]+", " ", (industry or "").lower()) + " "
    cfg = config()
    for cat, spec in (cfg.get("sensitive_categories") or {}).items():
        for term in spec["terms"]:
            if re.search(r"\b" + term + r"\b", text):
                return "yes", cat, bool(spec.get("practitioner_signoff"))
    for hint in cfg.get("sensitive_unsure_hints") or []:
        if re.search(r"\b" + hint + r"\b", text):
            return "unsure", hint, False
    for trade in cfg.get("not_sensitive_trades") or []:
        if re.search(r"\b" + trade + r"\b", text):
            return "no", None, False
    return "unsure", None, False


def sensitivity_fields(category, practitioner=None):
    """(sensitive, category, practitioner) for a category Paul named; 'none' = not sensitive."""
    cats = config().get("sensitive_categories") or {}
    if category in (None, "none"):
        return False, None, False
    if category not in cats:
        die(f"Unknown category '{category}'. Categories: {', '.join(cats)}, none.")
    prac = (practitioner == "yes") if practitioner else bool(cats[category].get("practitioner_signoff"))
    return True, category, prac


def new_status(slug, name, domain, ctype, industry, route=None, folder=None, sensitive=None,
               category=None, practitioner=False):
    return {
        "schema": 4,
        "client": {
            "slug": slug, "name": name, "domain": domain, "type": ctype,
            "industry": industry.lower(), "sensitive": sensitive,
            "sensitive_category": category, "practitioner_signoff": practitioner,
            "route": route, "drive_folder_id": folder, "kadence_head_meta_key": None,
            "gbp_url": None, "gbp_website_url": None, "address_type": None, "state": None,
            "imported": False, "notes": None,
        },
        "gates": {g: {"state": "pending"} for g in GATES["gates"]},
        "marks": {},
        "pages": {},
        "build": None,
        "audit_steps": {},
        "last_run": None,
        "spend": {"dataforseo_usd": 0.0},
        "client_view": {
            "_note": "The only client-facing part of this file. Plain language. Nothing else here is ever shown to a client.",
            "phase": "Getting started",
            "done": [],
            "waiting_on_client": [],
            "next": "We are researching your business before we ask you anything.",
        },
        "created": now(),
        "updated": now(),
    }


# ------------------------------------------------------------------ files and marks
def files_ok(files):
    """(ok, why) for a {path: sha} map recorded with an approval."""
    for f, h in (files or {}).items():
        gone = ref_missing(f)
        if gone:
            return False, f"{gone} (approved as {f})"
        if ref_sha(f) != h and not ("#" in f and ref_sha_v2(f) == h):   # a pre-P4 stamp: values unchanged too
            return False, f"{f} changed after approval"
    return True, ""


def mark_files(st, name):
    return list(((st.get("marks") or {}).get(name) or {}).get("files") or {})


def plain(gate):
    spec = GATES["gates"].get(gate) or GATES["conditions"].get(gate) or {}
    return spec.get("plain") or spec.get("label") or gate


def label(gate):
    return (GATES["gates"].get(gate) or GATES["conditions"].get(gate) or {}).get("label", gate)


def requires(st, gate):
    spec = GATES["gates"].get(gate) or GATES["conditions"].get(gate) or {}
    if st["client"]["type"] == "blog-only" and "requires_blog_only" in spec:
        return spec["requires_blog_only"]
    return spec.get("requires", [])


# ------------------------------------------------------------------ conditions
def client_set_up(st):
    """(ok, why) — /new-client finished. Phase 7 (Paul, 2026-10-21): a check inside run.py start, handoff.py and
    wp.py, no longer a gate — it was never false for a client with a status.json."""
    if "client_setup" in (st.get("imported_conditions") or {}):
        return True, ""
    log = path(st["client"]["slug"]).parent / "log.md"
    ok = log.exists() and re.search(r"^## RUN \S+-new-client\S* · FINISHED", log.read_text(), re.M)
    return bool(ok), ("" if ok else "the client has not been set up yet — run /new-client first")


def audit_steps_left(st):
    """(ok, why) — every registered audit step has an outcome. Phase 7: a check inside approve.py at
    audit_approved, no longer a condition of its own."""
    if "audit_steps_complete" in (st.get("imported_conditions") or {}):
        return True, ""
    import steps
    left = steps.missing(st)
    return not left, ("" if not left else "audit steps with no outcome yet: " + ", ".join(x["id"] for x in left))


def kind_met(st, kind):
    """(ok, [reasons]) for a change kind (gates.json change_kinds → gate: one name, a list, or none): the client is
    set up and each named decision is met. 'page_approval' is checked per page by the caller."""
    ok, why = client_set_up(st)
    reasons = [] if ok else [why]
    g = GATES["change_kinds"][kind].get("gate")
    for name in ([g] if isinstance(g, str) else list(g or [])):
        if name != "page_approval":
            reasons += [r for r in gate_met(st, name)[1] if r not in reasons]
    return not reasons, reasons


def condition_met(st, name):
    """(ok, why) — checked from evidence, never approved."""
    slug = st["client"]["slug"]
    if name in (st.get("imported_conditions") or {}):
        return True, ""
    if name == "wordpress_connected":
        chk = (st.get("wordpress") or {}).get("check") or {}
        if not chk.get("passed"):
            return False, (f"WordPress is not connected yet — run /wp-check {slug}" if not chk else
                           f"the last /wp-check failed — fix what it reported ({chk.get('report')}) and run /wp-check {slug} again")
        import datetime as _dt
        age = (_dt.datetime.now().astimezone() - _dt.datetime.fromisoformat(chk["at"])).days
        return (age <= 30), ("" if age <= 30 else f"the last /wp-check was {age} days ago — run /wp-check {slug} again")
    if name == "proof_sheet_returned":
        files = (st.get("marks") or {}).get("proof_sheet_returned", {}).get("files") or {}
        ok = bool(files) and all((ROOT / f).exists() for f in files)
        if not ok and facts_direct_approved(st):   # R3: the client's answers came directly and Paul approved them
            ok = True
        return ok, ("" if ok else "the client has not returned the proof sheet yet "
                    f"(when it arrives: /discovery {slug} sheet-returned)")
    if name == "discovery_signed_off":   # R3: derived — no summary to approve
        left = [r for r in GATES["conditions"][name]["requires"] if not _decided(st, r)]
        return not left, ("" if not left else "discovery is not signed off yet — still open: "
                          + ", ".join(plain(r) for r in left))
    if name == "blockers_cleared":
        return blockers_cleared(st)
    if name == "page_specs_approved":
        return specs_approved(st)
    if name == "pages_drafted":   # CM-055: every page is a WordPress draft — one living handoff, published together
        bs = [b for b in batches(st) if b.get("kind") in ("service", "location", "county") or b["id"] == "pilot"]
        left = [b["id"] for b in bs if b.get("state") not in DRAFTED_OR_LATER]   # P9: homepage/about may follow later
        ok = bool(bs) and not left
        return ok, ("" if ok else ("no site plan yet" if not bs else
                                   "batches not yet in WordPress as drafts: " + ", ".join(left)))
    if name == "pages_built":
        bs = batches(st)
        left = [b["id"] for b in bs if b.get("state") != "written_back"]
        ok = bool(bs) and not left
        return ok, ("" if ok else ("no site plan yet" if not bs else
                                   "batches not yet built and written back: " + ", ".join(left)))
    return False, f"unknown condition {name}"


def facts_direct_approved(st):
    """The client's direct answers (no sheet sent) are recorded and Paul approved them as the client facts."""
    fd = ((st.get("marks") or {}).get("facts_direct") or {}).get("files") or {}
    rec = st["gates"].get("proof_sheet_approved") or {}
    return bool(fd) and rec.get("state") in GATES["met_decisions"] and set(fd) <= set(rec.get("files") or {}) \
        and all(not ref_missing(f) for f in fd)


# ------------------------------------------------------------------ page specs, approved once for every client (R3)
SPECS = ROOT / "methodology" / "specs"
STATUS_LINE = re.compile(r"^\*\*Status:\*\*.*$", re.M)


def spec_files():
    return sorted(str(p.relative_to(ROOT)) for p in SPECS.glob("*.md"))


def spec_sha(rel):
    """A spec's content without its status line (approving it rewrites that line)."""
    import hashlib
    text = STATUS_LINE.sub("", (ROOT / rel).read_text(encoding="utf-8"))
    return hashlib.sha256(text.encode()).hexdigest()[:12]


SPEC_TYPE = {"service.md": "service", "location.md": "location", "county-hub.md": "county", "homepage.md": "homepage",
             "about.md": "about"}


def spec_started(st, rel):
    """CR-023: the client already has a page of this spec's type drafted — it keeps the spec version it started with
    (Apex's location pages keep the structure they were drafted in), whether or not a pin was recorded."""
    typ = SPEC_TYPE.get(Path(rel).name)
    return bool(st and typ and any(p.get("type") == typ and ((p.get("files") or {}).get("draft") or p.get("file"))
                                   for p in (st.get("pages") or {}).values()))


def specs_approved(st=None):
    """CR-023: approval is per spec file. A spec edited since its approval blocks new work (a client that has not
    started) but not a client mid-stage: it keeps the version it started with, pinned by sha in its status
    (st['specs_pinned'], set by pin_specs at run start) until Paul moves it over (status.py specs-adopt)."""
    rec = config().get("specs_approval") or {}
    files = rec.get("files") or {}
    if not files:
        return False, "the page specs are not approved yet — Paul approves them once, for every client: /approve global specs"
    pinned = (st or {}).get("specs_pinned") or {}
    changed = [f for f in spec_files() if files.get(f) != spec_sha(f) and f not in pinned and not spec_started(st, f)]
    if changed:
        return False, ("page spec(s) not approved in their current version: " + ", ".join(Path(f).name for f in changed)
                       + " — " + " ".join(f"/approve global specs:{Path(f).stem}" for f in changed))
    return True, ""


def pin_specs(st):
    """CR-023: record the approved version of every spec this client starts work with (by sha), once."""
    files = (config().get("specs_approval") or {}).get("files") or {}
    pins = st.setdefault("specs_pinned", {})
    for f, sha in files.items():
        pins.setdefault(f, sha)
    return pins


WRITING_EXTRA = ["methodology/writing-commercial.md", "methodology/location-faq.md"]


def writing_fp():
    """CM-061 §9: one fingerprint of what shapes the writing — the specs (status lines ignored), the writing standard
    and the location FAQ recipe. Each drafts approval records it; a change means the next section pilots again."""
    import hashlib
    parts = [f"{f}:{spec_sha(f)}" for f in spec_files()]
    parts += [f"{f}:{sha12(ROOT / f)}" for f in WRITING_EXTRA if (ROOT / f).is_file()]
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:12]


def _approved_sections(st):
    return [b for b in batches(st) if (b.get("drafts") or {}).get("state") in GATES["met_decisions"]
            and not (b.get("drafts") or {}).get("baseline")]


CLEAN_PILOTS = 3


def clean_pilots(st):
    """CM-061 §9 (Rewrite 4): the slugs of the last 3 other clients' approved pilots when every one had no corrections
    (status.py pilot-corrections --none) and was approved at today's writing fingerprint — else []."""
    me = st["client"].get("slug", st.get("slug"))
    done = []
    for d in sorted(p for p in (ROOT / "clients").iterdir() if (p / "status.json").is_file()):
        if d.name == me:
            continue
        try:
            o = load(d.name)
        except SystemExit:
            continue
        rec = (batch(o, "pilot") or {}).get("drafts") or {}
        if rec.get("state") in GATES["met_decisions"] and not rec.get("baseline"):
            pc = (o.get("build") or {}).get("pilot_corrections_applied") or {}
            done.append((rec.get("at", ""), d.name, bool(pc.get("none")), rec.get("writing_fp")))
    last = sorted(done, reverse=True)[:CLEAN_PILOTS]
    fp = writing_fp()
    if len(last) == CLEAN_PILOTS and all(none and wfp == fp for _, _, none, wfp in last):
        return [name for _, name, _, _ in last]
    return []


def pilot_needed(st):
    """(needed, reason) — gates.json → modes → pilot (CM-061 §9)."""
    rule = (GATES["modes"].get("pilot") or {}).get("rule", "always")
    if rule != "auto":
        return True, "the pilot rule is 'always' (gates.json → modes → pilot)"
    ind = (st["client"].get("industry") or "").strip().lower()
    mine = _approved_sections(st)
    others = []
    for d in sorted(p for p in (ROOT / "clients").iterdir() if (p / "status.json").is_file()):
        if d.name == st["client"].get("slug", st.get("slug")):
            continue
        try:
            o = load(d.name)
        except SystemExit:
            continue
        if (o["client"].get("industry") or "").strip().lower() == ind and _approved_sections(o):
            others.append(d.name)
    if not mine and not others:
        return True, f"a new industry ({ind or 'not set'}): no client has an approved section in it yet"
    if not mine:
        clean = clean_pilots(st)
        if clean:
            return False, ("no pilot: the last 3 clients' pilots (" + ", ".join(clean) + ") had no corrections and the "
                           "specs and writing rules are unchanged since (CM-061 §9) — every page of the section is "
                           "drafted in one run")
        return True, "this client's first section"
    last = max(mine, key=lambda b: b["drafts"].get("at", ""))
    if last["drafts"].get("writing_fp") and last["drafts"]["writing_fp"] != writing_fp():
        return True, (f"the specs or writing rules changed since section {last['id']} was approved "
                      f"({last['drafts'].get('at', '')[:10]})")
    return False, ("no pilot: this client has an approved section, its industry is not new, and the specs and writing "
                   "rules have not changed since — every page of the section is drafted in one run")


# ------------------------------------------------------------------ technical blockers (R3: a condition)
def blockers_cleared(st):
    """Met when the blocker checklist is recorded and every row of every blocker handoff came back done and
    /verify passed it (PASS, or CHECK = confirmed by a person) — or the checklist recorded no blockers."""
    if "blocker_checklist" not in (st.get("marks") or {}):
        return False, "the technical blocker checklist is not written yet"
    hs = st.get("blocker_handoffs") or []
    if not hs:
        if st.get("blockers_none"):
            return True, ""
        return False, "the blocker items have not been handed to Jonie yet (handoff.py create … --blockers)"
    import csv
    slug = st["client"]["slug"]
    d = path(slug).parent
    verdict = {}
    p = d / "changes.jsonl"
    for line in (p.read_text().splitlines() if p.exists() else []):
        if '"verify"' in line:
            c = json.loads(line)
            if c.get("kind") == "verify" and c.get("ref"):
                verdict[c["ref"]] = c["result"]
    left = []
    for hid in hs:
        f = d / "handoffs" / f"{hid}.csv"
        rows = list(csv.DictReader(open(f, newline="", encoding="utf-8-sig"))) if f.exists() else []
        for r in rows:
            v = verdict.get(r["ref"], "")
            if r.get("status") != "done":
                left.append(f"{r['ref']} is {r.get('status') or 'open'}")
            elif not v.startswith(("VERIFY PASS", "VERIFY CHECK")):
                left.append(f"{r['ref']} is done but not verified yet" if not v else f"{r['ref']} failed /verify")
    return not left, ("" if not left else "blockers not cleared: " + "; ".join(left[:5])
                      + (f" (+{len(left) - 5} more)" if len(left) > 5 else ""))


def log_conditions(slug, st):
    """Append a CONDITION line to log.md the first time each condition is met. Returns names logged."""
    seen = st.setdefault("conditions_logged", {})
    new = []
    for c in GATES["conditions"]:
        if c in seen:
            continue
        ok, _ = condition_met(st, c)
        if ok:
            seen[c] = now()
            new.append(c)
    if new:
        with open(path(slug).parent / "log.md", "a", encoding="utf-8") as fh:
            for c in new:
                fh.write(f"\n## CONDITION · {seen[c]} · {label(c)} — met (system-verified)\n")
        save(slug, st)
    return new


def apply_global(slug):
    """A global approval (/approve global …, typed in the main folder) writes system files only: config.json's
    global_approvals list. Each client records it here, on its own next /next, in its own folder: the log line, the
    mode history, and the entry number it has seen (st['global_seen']). Returns the entries applied."""
    import lib
    lib.pull_main()   # a client folder reads config.json from its own branch: bring it up to main first
    st = load(slug)
    seen = st.get("global_seen", 0)
    new = [e for e in (config().get("global_approvals") or []) if e.get("n", 0) > seen]
    if not new:
        return []
    text = ""
    for e in new:
        note = f"Note: {e['note']}\n" if e.get("note") else ""
        if e["kind"] == "specs":
            text += (f"\n## APPROVAL · {e['at']} · page specs (global{': ' + e['only'] if e.get('only') else ''}) · approved · by Paul\n"
                     + "".join(f"Approved version: {r} (sha {h})\n" for r, h in (e.get("files") or {}).items()) + note)
        elif e["kind"] == "mode":
            st.setdefault("mode_history", []).append({"step": e["step"], "scope": "global", "mode": e["mode"], "by": "Paul",
                                                      "at": e["at"], "note": e.get("note"), "was": e.get("was")})
            own = (st.get("modes") or {}).get(e["step"])
            text += (f"\n## MODE · {e['at']} · {e['step']}: {e.get('was')} → {e['mode']} · GLOBAL · by Paul\n"
                     + (f"(this client keeps its own setting: {own['mode']})\n" if own else "") + note)
        elif e["kind"] == "model":
            text += f"\n## MODEL · {e['at']} · {e['key']}: {e.get('was') or 'default'} → {e['model']} · GLOBAL · by Paul\n" + note
    append(path(slug).parent / "log.md", text)
    st["global_seen"] = max(e["n"] for e in new)
    save(slug, st)
    log_conditions(slug, st)
    return new


# ------------------------------------------------------------------ gate logic
def _decided(st, gate):
    if gate in GATES["conditions"]:
        return condition_met(st, gate)[0]
    return (st["gates"].get(gate) or {}).get("state") in GATES["met_decisions"]


def _own_ok(st, gate):
    rec = st["gates"].get(gate) or {}
    if rec.get("state") not in GATES["met_decisions"]:
        return False, f"{plain(gate)} — not approved yet"
    ok, why = files_ok(rec.get("files"))
    return (True, "") if ok else (False, f"{plain(gate)} must be re-approved ({why})")


def gate_met(st, gate):
    """Return (ok, [reasons]). The gate's own files are checked; earlier gates only need their
    decision (an edit upstream is a flag, not a block)."""
    if gate not in GATES["gates"] and gate not in GATES["conditions"]:
        return False, [f"unknown gate {gate}"]
    reasons = []
    seen = set()

    def walk(g):
        for r in requires(st, g):
            if r in seen:
                continue
            seen.add(r)
            if not _decided(st, r):
                reasons.append(condition_met(st, r)[1] if r in GATES["conditions"]
                               else f"{plain(r)} — not approved yet")
            walk(r)
    walk(gate)
    if gate in GATES["conditions"]:
        ok, why = condition_met(st, gate)
        if not ok:
            reasons.append(why)
        return not reasons, reasons
    ok, why = _own_ok(st, gate)
    if not ok:
        reasons.append(why)
    return not reasons, reasons


def upstream_changes(st, gate):
    """Earlier gates that are approved but whose approved files changed since."""
    out, seen = [], set()

    def walk(g):
        for r in requires(st, g):
            if r in seen:
                continue
            seen.add(r)
            rec = st["gates"].get(r) or {} if r in GATES["gates"] else {}
            if rec.get("state") in GATES["met_decisions"] and not files_ok(rec.get("files"))[0]:
                out.append(r)
            walk(r)
    if gate in GATES["gates"] or gate in GATES["conditions"]:
        walk(gate)
    return out


def page_approved(st, page_id):
    p = st["pages"].get(page_id)
    if not p:
        return False, f"page {page_id} is not registered"
    a = p.get("approval") or {}
    if a.get("baseline"):
        return True, ""
    b = batch_of(st, page_id)
    if b and not a:
        return batch_stage_ok(st, b["id"], "drafts")
    if a.get("state") not in GATES["met_decisions"]:
        return False, f"page {page_id} content is not approved yet"
    if st["client"]["sensitive"] and not a.get("sensitive_review"):
        return False, f"page {page_id}: sensitive client — the human review is not recorded"
    if st["client"]["practitioner_signoff"] and not a.get("practitioner"):
        return False, f"page {page_id}: the licensed practitioner's sign-off on health claims is not recorded"
    f = a.get("file")
    if f and (ROOT / f).exists() and a.get("sha") != sha12(ROOT / f):
        return False, f"page {page_id}: the approved file changed after approval — re-approve"
    return True, ""


# ------------------------------------------------------------------ URL structure (BB-207, BB-208)
SLUG_PREFIXES = ("service", "services", "service-area", "service-areas", "areas", "areas-we-serve", "locations",
                 "location", "cities")


def slug_problems(url, ptype):
    """Bradley's URL rule for service, location and county pages: root-proximate — one path segment, never under
    /service/, /services/, /service-area/ (or a similar folder). Paul, 2026-10-09. [] when the URL is fine."""
    import urllib.parse
    if ptype not in ("service", "location", "county") or not url:
        return []
    parts = [x for x in urllib.parse.urlparse(url).path.split("/") if x]
    if parts and parts[0].lower() in SLUG_PREFIXES:
        return [f"{url}: drop the /{parts[0]}/ folder — service and location URLs sit at the root (BB-207, BB-208)"]
    if len(parts) != 1:
        return [f"{url}: a {ptype} URL is one slug at the root, e.g. /roof-repair/ or /bluffton/ (BB-208)"]
    return []


# ------------------------------------------------------------------ build plan & batches
KIND_ORDER = {"service": 0, "location": 1, "county": 1, "homepage": 2, "about": 2}


def batches(st):
    return ((st.get("build") or {}).get("batches")) or []


def batch(st, bid):
    return next((b for b in batches(st) if b["id"] == bid), None)


def batch_of(st, page_id):
    return next((b for b in batches(st) if page_id in b["pages"]), None)


def _approval_ok(rec, label_, check_files=True):
    if not rec or rec.get("state") not in GATES["met_decisions"]:
        return False, f"{label_} is not approved yet"
    if check_files:
        ok, why = files_ok(rec.get("files"))
        if not ok:
            return False, f"{label_} must be re-approved: {why}"
    return True, ""


def route(b):
    """Rewrite 4 Phase 4 (D2, D5): 'outline' — no brief; outline.py derives each page's outline at draft time and the
    section stops once, for its drafts. 'briefs' — the old route, kept by a section whose briefs were approved before
    (assign_routes, on /next, marks which is which). A section with no route recorded is on the old route."""
    return (b or {}).get("route") or "briefs"


def plan_stage(b):
    """The per-page file written before the draft: the outline (outline route) or the brief."""
    return "outline" if route(b) == "outline" else "brief"


def briefs_need_approval(st, bid):
    """R3: after the pilot, once Paul has switched build:brief to auto (only possible after the pilot passed),
    a batch's briefs are not a stop — Paul approves the drafts only. The pilot's briefs are always approved.
    A section on the outline route has no briefs at all."""
    if route(batch(st, bid)) == "outline":
        return False
    return bid == "pilot" or stage_mode(st, "build:brief") != "auto"


def batch_stage_ok(st, bid, stage, check_files=True):
    b = batch(st, bid)
    if not b:
        return False, f"batch {bid} is not in the site plan"
    if stage == "briefs" and not b.get(stage) and not briefs_need_approval(st, bid):
        _, probs = per_page_files(st, b, plan_stage(b))
        return (not probs), ("" if not probs else f"batch {bid} briefs: " + "; ".join(probs))
    ok, why = _approval_ok(b.get(stage), f"batch {bid} {stage}", check_files)
    if not ok:
        return ok, why
    if stage == "drafts":
        a = b["drafts"]
        if a.get("baseline"):
            return True, ""
        if st["client"]["sensitive"] and not a.get("sensitive_review"):
            return False, f"batch {bid}: sensitive client — the human review is not recorded"
        if st["client"]["practitioner_signoff"] and not a.get("practitioner"):
            return False, f"batch {bid}: the licensed practitioner's sign-off on health claims is not recorded"
    return True, ""


def batch_ready(st, bid, stage):
    """May work on <stage> of this batch start (or may Paul approve it)? (ok, [reasons]).
    Earlier approvals are checked by decision only (upstream edits are flags, not blocks)."""
    r = []
    bp = st.get("build") or {}
    ok, why = _approval_ok((bp.get("site_plan") or {}).get("approval"), "the site plan", False)
    if not ok:
        r.append(why)
    b = batch(st, bid)
    if not b:
        return False, r + [f"batch {bid} is not in the site plan"]
    prev = {"drafts": "briefs"}.get(stage)
    if prev:
        ok, why = batch_stage_ok(st, bid, prev, False)
        if not ok:
            r.append(why)
    if bid != "pilot" and not bp.get("pilot_waived"):
        ok, why = batch_stage_ok(st, "pilot", "briefs", False)
        if not ok:
            r.append("pilot: " + why)
        if not bp.get("pilot_corrections_applied"):
            r.append("the pilot corrections are not yet applied to the specs (status.py pilot-corrections)")
    r += batch_order_blocks(st, bid)
    return not r, r


def batch_order_blocks(st, bid):
    """Service batches before any location batch, homepage and about last — by Paul's drafts approval, never by
    publishing (CM-055: nothing waits on Jonie; the pages are published together at the end). The pilot (1 service +
    1 location) is exempt both ways: it runs first and never waits on, or holds up, the order."""
    b = batch(st, bid)
    if not b or bid == "pilot":
        return []
    mine = KIND_ORDER.get(b["kind"], 1)
    return [f"{o['kind']} batch {o['id']} needs its drafts approved first"
            for o in batches(st)
            if o["id"] not in ("pilot", bid) and KIND_ORDER.get(o["kind"], 1) < mine
            and o.get("state") not in DRAFTED_OR_LATER and not batch_stage_ok(st, o["id"], "drafts", False)[0]]


# ------------------------------------------------------------------ evidence gate (CM-041)
def evidence_state(st, pid):
    """(result or None, record). result: pass / warn / block / None (gate not run)."""
    rec = ((st["pages"].get(pid) or {}).get("evidence")) or {}
    return rec.get("result"), rec


def evidence_ok(st, pid):
    """(ok, why) — may a brief be written for this page? pass/warn yes; block only with Paul's waiver
    for exactly this grid (the grid's sha at the time he waived it)."""
    result, rec = evidence_state(st, pid)
    if not result:
        return False, f"page {pid}: the evidence gate has not run (evidence.py run)"
    g = ROOT / rec.get("grid", "")
    if not g.is_file() or sha12(g) != rec.get("sha"):
        return False, f"page {pid}: the evidence grid changed after it was scored — re-run the gate"
    if result in ("pass", "warn"):
        return True, ""
    w = rec.get("waiver") or {}
    if w and w.get("grid_sha") == rec.get("sha"):
        return True, ""
    if w:
        return False, (f"page {pid}: blocked by the evidence gate — your waiver of {w.get('at', '')[:10]} was for an "
                       "older grid; the facts changed, so it no longer counts")
    return False, f"page {pid}: blocked by the evidence gate ({'; '.join(rec.get('why') or [])})"


# ------------------------------------------------------------------ one page per run (CM-043)
def page_stage(st, pid, stage):
    return (((st["pages"].get(pid) or {}).get("files") or {}).get(stage)) or {}


def per_page_files(st, b, stage):
    """(files in batch order, problems) — one file per page. Drafts each from their own run (CM-043); briefs come
    from the batch's one brief run (CM-054)."""
    files, runs, probs = [], {}, []
    for pid in b["pages"]:
        rec = page_stage(st, pid, stage)
        if not rec.get("file"):
            probs.append(f"{pid} has no {stage} yet (" + ("outline.py writes it in the section's write run)"
                                                          if stage == "outline" else f"/build <slug> {stage} {b['id']} {pid})"))
            continue
        who = (rec.get("run"), rec.get("agent"))   # P10: one fresh sub-agent per page inside one run keeps CM-043
        if stage == "draft" and who in runs:
            probs.append(f"{pid} and {runs[who]} were written in the same context ({rec['run']}) — one page per agent")
        runs[who] = pid
        files.append(rec["file"])
    return files, probs


STAGE_ONE = {"briefs": "brief", "drafts": "draft"}


def _when(rec):
    """When a record was made: its `ts` (sub-second) when it has one, else its `at` — None if neither reads."""
    if rec.get("ts") is not None:
        return rec["ts"]
    try:
        return datetime.datetime.fromisoformat(rec["at"]).timestamp()
    except (KeyError, TypeError, ValueError):
        return None


def page_version_problems(st, bid, stage, files, strict=True):
    """[why, …] — an approval of a batch's briefs or drafts covers every page at the version the review answers
    produced (CM-061; HMM run 20261014-144852-build-6004: one of four briefs was re-recorded, the approval signed all
    four). Per page: a record exists; the file approved is the file recorded; its version is the recorded version; and
    the record was made after the review's answers were applied. `files` is the {file: sha} the approval names.
    strict=False (the integrity migration, over approvals made before this rule) judges the order only when both
    records carry a sub-second `ts`, so an old approval is never voided on a second-resolution guess."""
    b = batch(st, bid)
    if not b or b.get("baseline") or (b.get(stage) or {}).get("baseline"):
        return []
    if stage == "drafts" and not (b.get("review") or {}).get("drafts"):
        return []   # a batch under way with a semantic review table (before CM-061): apply-sem edits the drafts and pins their versions
    one = STAGE_ONE[stage]
    applied =(((b.get("review") or {}).get(stage) or {}).get("applied")) or {}
    out = []
    for pid in b.get("pages", []):
        rec = page_stage(st, pid, one)
        if not rec.get("file"):
            out.append(f"{pid}: no {one} is recorded for it")
            continue
        f = rec["file"]
        if f not in (files or {}):
            out.append(f"{pid}: its recorded {one} ({f}) is not among the files approved")
        elif files[f] != rec.get("sha"):
            out.append(f"{pid}: approved at version {files[f]} but recorded at {rec.get('sha')}")
        if ref_missing(f):
            out.append(f"{pid}: {ref_missing(f)}")
        elif sha12(ROOT / f) != rec.get("sha"):
            out.append(f"{pid}: {f} is not the version recorded for it (edited after it was recorded)")
        t_rec, t_app = _when(rec), _when(applied)
        if applied and t_rec is not None and t_app is not None and t_rec < t_app \
                and (strict or (rec.get("ts") is not None and applied.get("ts") is not None)):
            out.append(f"{pid}: recorded before the review answers were applied")
    return out


def assign_routes(slug, st):
    """Rewrite 4 migration (D5, on /next, once per client): a section with no route recorded keeps the brief route when
    its briefs are approved, any of its pages has a brief, or it is past 'planned'; every other section takes the
    outline route (config build_route, default 'outline'). A pilot Paul made no corrections to is marked so (CM-061
    §9). Returns the log lines; the caller saves."""
    if st.get("rewrite4_routes"):
        return []
    lines = []
    for b in batches(st):
        if b.get("route"):
            continue
        started = (b.get("briefs") or {}).get("state") in GATES["met_decisions"] or b.get("state", "planned") != "planned" \
            or any(page_stage(st, p, "brief") for p in b.get("pages", []))
        b["route"] = "briefs" if started else (config().get("build_route") or "outline")
        lines.append(f"section {b['id']}: {b['route']} route"
                     + (" (briefs approved or under way — finishes on the old route)" if started else " (no brief)"))
    pc = (st.get("build") or {}).get("pilot_corrections_applied") or {}
    if pc and "none" not in pc and re.match(r"\s*no corrections", pc.get("note", ""), re.I):
        pc["none"] = True
        lines.append("pilot: recorded as 'no corrections' (from its note)")
    st["rewrite4_routes"] = {"at": now(), "rule": "REWRITE-4-PLAN.md D5"}
    for ln in lines:
        append(client_dir(slug) / "log.md", f"- MIGRATION {now()[:16]} · Rewrite 4 · {ln}\n")
    return lines


def void_unreviewed_approvals(slug, st):
    """Integrity migration (on /next): an approval of a batch's briefs or drafts whose recorded pages do not match the
    versions it names is voided — the approval becomes a `revise` record (kept, with why) and is logged. Returns the
    log lines. The caller saves."""
    lines = []
    for b in batches(st):
        for stage in STAGES:
            rec = b.get(stage)
            if not rec or rec.get("state") not in GATES["met_decisions"] or rec.get("baseline") or not rec.get("files"):
                continue
            probs = [p for p in page_version_problems(st, b["id"], stage, rec["files"], strict=False)
                     if "no brief is recorded" not in p and "no draft is recorded" not in p]
            if not probs:
                continue
            b[stage] = {"state": "revise", "by": "integrity check", "at": now(), "voided": True, "files": {},
                        "note": "voided: the approved versions do not match the recorded pages — " + "; ".join(probs)[:600],
                        "was": rec}
            lines.append(f"batch {b['id']} {stage}: " + "; ".join(probs))
    for ln in lines:
        append(client_dir(slug) / "log.md", f"- INTEGRITY {now()[:16]} · approval voided · {ln}\n")
    return lines


# ------------------------------------------------------------------ review / auto mode per stage (CM-044)
def mode_stages():
    return GATES["modes"]["stages"]


def stage_mode(st, step):
    """'review' / 'auto' for a producing stage; None for a step that is not one."""
    if step not in mode_stages():
        return None
    mine = (st.get("modes") or {}).get(step)
    if mine:
        return mine["mode"]
    glob = (config().get("stage_modes") or {}).get(step)
    return glob["mode"] if glob else GATES["modes"]["default"]


def pilot_passed(st, step):
    """(ok, why) — has this stage passed the pilot for this client?"""
    spec = (mode_stages().get(step) or {}).get("pilot")
    if not spec:
        return False, f"{step} has no pilot, so it always stays in review"
    if spec.startswith("batch_state:"):
        _, bid, want = spec.split(":")
        b = batch(st, bid) or {}
        ok = b.get("state") == want
        return ok, ("" if ok else f"the pilot batch has not reached {want} yet")
    if spec == "first_post":
        ok = any(p.get("type") == "blog" and page_approved(st, pid)[0] for pid, p in st["pages"].items())
        return ok, ("" if ok else "no blog post has been approved yet")
    ok, rs = check(st, spec)
    return ok, ("" if ok else "the pilot has not passed this stage yet: " + "; ".join(rs))


def check(st, target):
    """One entry point for every gate-like target. Returns (ok, [reasons])."""
    if target.startswith("marked:"):
        art = target[7:]
        files = ((st.get("marks") or {}).get(art) or {}).get("files") or {}
        ok = bool(files) and not any(ref_missing(f) for f in files)
        return ok, ([] if ok else [f"{GATES['artifacts'].get(art, art)} is not recorded yet"])
    if target.startswith("evidence:"):
        ok, why = evidence_ok(st, target[9:])
        return ok, ([] if ok else [why])
    if target.startswith("page:"):
        ok, why = page_approved(st, target[5:])
        return ok, ([] if ok else [why])
    if target == "site_plan":
        ok, why = _approval_ok(((st.get("build") or {}).get("site_plan") or {}).get("approval"), "the site plan")
        return ok, ([] if ok else [why])
    if target == "pilot_corrections":
        bp = st.get("build") or {}
        ok = bool(bp.get("pilot_corrections_applied") or bp.get("pilot_waived"))
        return ok, ([] if ok else ["the pilot corrections are not yet applied to the specs"])
    m = re.match(r"^batch:([\w-]+):(briefs|drafts)(_ready)?$", target)
    if m:
        if m.group(3):
            return batch_ready(st, m.group(1), m.group(2))
        ok, why = batch_stage_ok(st, m.group(1), m.group(2))
        return ok, ([] if ok else [why])
    return gate_met(st, target)


def render_build(st):
    bp = st.get("build")
    if not bp:
        return "Build plan: none yet (site plan not written)."
    sp = (bp.get("site_plan") or {})
    ok, _ = check(st, "site_plan")
    pc = bp.get("pilot_corrections_applied")
    out = [f"Build plan: site plan {'APPROVED' if ok else 'not approved'} ({sp.get('file')})",
           f"  pilot corrections applied: {'yes — ' + pc['note'] if pc else ('waived (imported)' if bp.get('pilot_waived') else 'no')}"]
    for b in batches(st):
        marks = []
        for stage in STAGES:
            marks.append(f"{stage} {'OK' if batch_stage_ok(st, b['id'], stage)[0] else '--'}")
        out.append(f"  [{b['id']:10}] {b['kind']:8} {b['label'][:34]:34} {len(b['pages'])} pages · "
                   + " · ".join(marks) + f" · {b.get('state', 'planned')}")
    return "\n".join(out)


# ------------------------------------------------------------------ rendering
def visible_gates(st):
    for g in GATES["gates"]:
        if st["client"]["type"] == "blog-only" and g not in ("entity_approved", "blog_topics_approved", "blog_map_approved",
                                                             "wordpress_pilot_approved"):
            continue
        if st["client"]["type"] == "full" and g == "blog_topics_approved":
            continue
        yield g


def render_show(st):
    c = st["client"]
    out = [f"{c['name']} ({c['slug']}) · {c['domain']} · {c['type']} · industry {c['industry']}"
           + (f" · SENSITIVE ({c.get('sensitive_category')})" if c["sensitive"] else "")
           + (f" · Route {c['route']}" if c.get("route") else "")]
    if c.get("safe_fix_cap"):
        out.append("Safe-fix cap: " + ", ".join(f"{k} {v}" for k, v in c["safe_fix_cap"].items()))
    out.append("")
    out.append("Conditions (checked by the system):")
    for g in GATES["conditions"]:
        if st["client"]["type"] == "blog-only" and g != "wordpress_connected":
            continue
        ok, why = condition_met(st, g)
        out.append(f"  [{'MET ' if ok else '----'}] {g:24} {label(g)}" + ("" if ok else f" — {why}"))
    out.append("")
    out.append("Decisions (Paul, with /approve):")
    for g in visible_gates(st):
        rec = st["gates"].get(g, {})
        ok, why = gate_met(st, g)
        if ok:
            mark = "MET "
        elif rec.get("state") in GATES["met_decisions"]:
            mark = "VOID"
        else:
            mark = "----" if rec.get("state", "pending") == "pending" else rec.get("state", "")[:4].upper()
        by = f" · {rec.get('by')} {rec.get('at', '')[:10]}" if rec.get("by") else ""
        out.append(f"  [{mark}] {g:24} {label(g)}{by}")
        if mark == "VOID":
            out.append(f"         ! {why[-1]}")
        if rec.get("state") in GATES["met_decisions"]:
            for u in upstream_changes(st, g):
                out.append(f"         ! upstream change — {plain(u)} changed after it was approved; "
                           "check whether it affects this")
    if st["pages"]:
        out.append("")
        out.append("Pages:")
        for pid, p in st["pages"].items():
            ok, _ = page_approved(st, pid)
            out.append(f"  {pid:30} {p.get('type', ''):9} {p.get('state', ''):13}"
                       f" approved={'yes' if ok else 'no'}  {p.get('url') or ''}")
    out.append("")
    out.append(render_build(st))
    lr = st.get("last_run")
    if lr:
        out.append("")
        out.append(f"Last run: {lr.get('command')} {lr.get('run_id')} — {lr.get('result')}")
    cv = st["client_view"]
    out.append("")
    out.append(f"Client view: {cv['phase']} | next: {cv['next']}")
    return "\n".join(out)


def render_approval_record(st):
    c = st["client"]
    lines = [f"# {c['name']} - Approval Record", "",
             "Generated from the seo-ops system (clients/{}/status.json). Do not edit by hand —"
             " approvals are made with /approve and mirrored here.".format(c["slug"]), ""]
    for g in GATES["gates"]:
        rec = st["gates"][g]
        lines.append(f"## {label(g)}")
        lines.append("")
        lines.append(f"- Decision: **{rec.get('state', 'pending')}**")
        if rec.get("by"):
            lines.append(f"- Decided by: {rec['by']} · {rec.get('at', '')}")
        for cnd in rec.get("conditions") or []:
            lines.append(f"- Condition: {cnd}")
        for f, h in (rec.get("files") or {}).items():
            lines.append(f"- Approved version: `{f}` (sha {h})")
        if rec.get("note"):
            lines.append(f"- Note: {rec['note']}")
        lines.append("")
    if st["pages"]:
        lines.append("## Page content approvals")
        lines.append("")
        lines.append("| Page | Type | Decision | By | Date | Human review | Practitioner |")
        lines.append("|---|---|---|---|---|---|---|")
        for pid, p in st["pages"].items():
            a = p.get("approval") or {}
            lines.append(f"| {p.get('name') or pid} | {p.get('type')} | {a.get('state', 'pending')} | "
                         f"{a.get('by', '')} | {a.get('at', '')[:10]} | {a.get('sensitive_review') or ''} | "
                         f"{a.get('practitioner') or ''} |")
    return "\n".join(lines) + "\n"


def set_batch_state(st, b, state):
    b["state"] = state
    ps = BATCH_TO_PAGE.get(state)
    if ps:
        for pid in b["pages"]:
            p = st["pages"].setdefault(pid, {"state": "planned"})
            if not (p.get("approval") or {}).get("baseline"):
                p["state"] = ps


# ------------------------------------------------------------------ CLI
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("slug")
    s.add_argument("--name", required=True); s.add_argument("--domain", required=True)
    s.add_argument("--type", choices=["full", "blog-only"], required=True)
    s.add_argument("--industry", required=True); s.add_argument("--route", choices=["A", "B"])
    s.add_argument("--drive-folder-id"); s.add_argument("--sensitive", choices=["yes", "no"])
    s.add_argument("--practitioner", choices=["yes", "no"]); s.add_argument("--category")
    s = sub.add_parser("classify"); s.add_argument("industry")
    s = sub.add_parser("sensitivity"); s.add_argument("slug"); s.add_argument("category")
    s.add_argument("--practitioner", choices=["yes", "no"]); s.add_argument("--run", required=True)
    s = sub.add_parser("cap"); s.add_argument("slug"); s.add_argument("kind", choices=SAFE_FIX_CAP_KINDS)
    s.add_argument("limit"); s.add_argument("--run", required=True)
    s = sub.add_parser("show"); s.add_argument("slug"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("require"); s.add_argument("slug"); s.add_argument("gates", nargs="+")
    s = sub.add_parser("set"); s.add_argument("slug"); s.add_argument("field"); s.add_argument("value")
    s = sub.add_parser("view"); s.add_argument("slug")
    s = sub.add_parser("page"); s.add_argument("slug"); s.add_argument("page_id")
    s.add_argument("--type", choices=["service", "location", "county", "homepage", "about", "blog"])
    s.add_argument("--name"); s.add_argument("--url"); s.add_argument("--state", choices=PAGE_STATES)
    s.add_argument("--file")
    s = sub.add_parser("approval-record"); s.add_argument("slug")
    s = sub.add_parser("urls"); s.add_argument("slug"); s.add_argument("--published", action="store_true")
    s = sub.add_parser("plan"); s.add_argument("slug"); s.add_argument("--file", required=True)
    s.add_argument("--json", required=True)
    s = sub.add_parser("batch"); s.add_argument("slug"); s.add_argument("batch_id")
    s.add_argument("--state", required=True, choices=BATCH_STATES); s.add_argument("--files")
    s.add_argument("--sem-table"); s.add_argument("--sem-findings", type=int)
    s.add_argument("--review-sheet", help="CM-061: the section's drafts review sheet (review.py sheet), instead of --sem-table")
    s.add_argument("--checks-passed", action="store_true"); s.add_argument("--note")
    s = sub.add_parser("page-stage"); s.add_argument("slug"); s.add_argument("page_id")
    s.add_argument("--stage", required=True, choices=["brief", "draft"]); s.add_argument("--file", required=True)
    s.add_argument("--run", required=True)
    s.add_argument("--agent", help="P10: in a write run (or --pages all), the id of the fresh sub-agent that wrote this page")
    s = sub.add_parser("modes"); s.add_argument("slug")
    s = sub.add_parser("pilot"); s.add_argument("slug")
    s = sub.add_parser("writeback"); s.add_argument("slug"); s.add_argument("batch_id"); s.add_argument("--run", required=True)
    s = sub.add_parser("specs-adopt"); s.add_argument("slug")   # CR-023: move a client to the currently approved specs
    s = sub.add_parser("pilot-corrections"); s.add_argument("slug"); s.add_argument("--note", required=True)
    s.add_argument("--none", action="store_true", help="Paul made no corrections to the pilot (CM-061 §9: three such "
                   "pilots in a row at the same writing rules end the pilot for later clients)")
    s = sub.add_parser("blockers-none"); s.add_argument("slug"); s.add_argument("--run", required=True)
    s = sub.add_parser("mark"); s.add_argument("slug"); s.add_argument("name")
    s.add_argument("--file", required=True, action="append")
    a = ap.parse_args()

    if a.cmd == "classify":
        v, cat, prac = classify(a.industry)
        print(json.dumps({"sensitive": v, "category": cat, "practitioner_signoff": prac}))
        sys.exit(9 if v == "unsure" else 0)

    if a.cmd == "init":
        d = client_dir(a.slug, must_exist=False)
        if (d / "status.json").exists():
            die(f"{a.slug} already exists.")
        v, cat, prac = classify(a.industry)
        if a.category:
            sensitive, cat, prac = sensitivity_fields(a.category, a.practitioner)
        elif a.sensitive:
            sensitive = a.sensitive == "yes"
            cat = (cat if v == "yes" else "set by Paul") if sensitive else None
            prac = (a.practitioner == "yes") if a.practitioner else (prac if sensitive else False)
        elif v == "unsure":
            why = (f"It mentions '{cat}'." if cat else "It is not clearly in or out of a list "
                   "(config.json sensitive_categories / not_sensitive_trades).")
            die(f"ASK PAUL — is '{a.industry}' a sensitive industry (CM-025, CM-040: "
                f"{', '.join(config().get('sensitive_categories') or {})})? {why} Re-run with "
                "--category <category>|none (--practitioner yes|no overrides the category's default).", 9)
        else:
            sensitive = v == "yes"
        for sub_ in ("discovery", "audit", "build", "finish", "blog", "handoffs",
                     "snapshots", "inputs", "inputs/crawl"):
            (d / sub_).mkdir(parents=True, exist_ok=True)
        st = new_status(a.slug, a.name, a.domain, a.type, a.industry, a.route, a.drive_folder_id,
                        sensitive, cat, prac)
        write_json(d / "status.json", st)
        save(a.slug, st)
        (d / "log.md").write_text(
            f"# Safety log — {a.name}\n\nAppend-only. Every command writes STARTED before it acts "
            "and FINISHED after. Every change lists URL, old value, new value and result.\n"
            "Machine-readable mirror for /rollback: changes.jsonl.\n\n")
        (d / "changes.jsonl").write_text("")
        import records
        records.render(a.slug)
        print(f"created clients/{a.slug}/ (sensitive={sensitive}"
              + (f", category={cat}, practitioner sign-off={prac}" if sensitive else "") + ")")
        return

    st = load(a.slug)
    if a.cmd == "blockers-none":   # the checklist found nothing to hand to Jonie
        import run as R
        R.open_run(a.slug, a.run)
        st["blockers_none"] = {"at": now(), "run": a.run}
        save(a.slug, st)
        append(client_dir(a.slug) / "log.md", f"- DECISION {now()[:16]} · run {a.run} · the technical blocker checklist "
               "has no items — nothing to hand to Jonie\n")
        print("recorded: no technical blockers")
        return
    if a.cmd in ("sensitivity", "cap"):   # Paul's answers in chat, recorded as decisions in the open run
        import run as R
        R.open_run(a.slug, a.run)
        if a.cmd == "sensitivity":
            sensitive, cat, prac = sensitivity_fields(a.category, a.practitioner)
            st["client"].update(sensitive=sensitive, sensitive_category=cat, practitioner_signoff=prac)
            text = (f"Paul: sensitivity set to {cat or 'not sensitive'}"
                    + (f", practitioner sign-off {'yes' if prac else 'no'}" if sensitive else "") + " (CM-025, CM-040)")
        else:
            if a.limit != "none" and not a.limit.isdigit():
                die("limit must be a whole number or 'none'")
            caps = st["client"].setdefault("safe_fix_cap", {})
            caps.pop(a.kind, None) if a.limit == "none" else caps.update({a.kind: int(a.limit)})
            text = f"Paul: safe-fix cap for {a.kind} set to {a.limit}"
        save(a.slug, st)
        append(client_dir(a.slug) / "log.md", f"- DECISION {now()[:16]} · run {a.run} · {text}\n")
        print(text)
        return
    if a.cmd == "show":
        print(json.dumps(st, indent=2) if a.json else render_show(st))
    elif a.cmd == "require":
        reasons = []
        for g in a.gates:
            ok, rs = check(st, g)
            if not ok:
                reasons += [r for r in rs if r not in reasons]
        if reasons:
            print("Not yet — this needs:\n  - " + "\n  - ".join(reasons))
            print("\nOnly Paul can approve, with /approve.")
            sys.exit(4)
        print("gates met: " + ", ".join(a.gates))
    elif a.cmd == "set":
        if a.field not in SETTABLE:
            die(f"'{a.field}' is not settable here. Settable: {', '.join(sorted(SETTABLE))}."
                " Gates change only through /approve.")
        sect, key = a.field.split(".", 1)
        st[sect][key] = a.value
        save(a.slug, st); print(f"{a.field} = {a.value}")
    elif a.cmd == "view":
        print(json.dumps(client_view(st), indent=2))
    elif a.cmd == "page":
        p = st["pages"].setdefault(a.page_id, {"state": "planned"})
        for k in ("type", "name", "url", "file"):
            v = getattr(a, k)
            if v: p[k] = v
        if a.state:
            if a.state == "approved":
                die("Page approval is set only through /approve.")
            p["state"] = a.state
        if a.file and p.get("type") == "blog" and (ROOT / a.file).is_file():
            import publish
            bad = publish.placeholder_problems((ROOT / a.file).read_text(encoding="utf-8"))
            if bad:
                die(f"{a.page_id}: placeholder(s) without a visible [NEED: ...] note (CM-016):\n  - " + "\n  - ".join(bad))
        save(a.slug, st); print(json.dumps({a.page_id: p}, indent=2))
    elif a.cmd == "urls":
        live = ("published", "verified", "written_back")
        for pid, p in st["pages"].items():
            if p.get("url") and (not a.published or p.get("state") in live or (p.get("approval") or {}).get("baseline")):
                print(p["url"])
    elif a.cmd == "approval-record":
        print(render_approval_record(st), end="")
    elif a.cmd == "plan":
        if check(st, "site_plan")[0]:
            die("The site plan is already approved. Changing it needs Paul to re-open it (/approve <slug> site_plan --decision revise).")
        plan = json.loads(open(a.json).read())
        pages = {p["id"]: p for p in plan["pages"]}
        seen = {}
        for b in plan["batches"]:
            for pid in b["pages"]:
                if pid not in pages:
                    die(f"batch {b['id']} lists unknown page {pid}")
                if pid in seen:
                    die(f"page {pid} is in two batches ({seen[pid]}, {b['id']})")
                seen[pid] = b["id"]
        groups = {}
        for b in plan["batches"]:
            if b["id"] != "pilot":
                g = {"county": "location", "about": "homepage"}.get(b["kind"], b["kind"])
                groups.setdefault(g, []).append(b)
        for g, bs in groups.items():
            n = sum(len(b["pages"]) for b in bs)
            if n <= 15 and len(bs) > 1:
                die(f"P10: all {n} {g} page(s) are one batch, written in one run — split only above 15 pages "
                    f"({', '.join(b['id'] for b in bs)})")
            big = [b["id"] for b in bs if len(b["pages"]) > 15]
            if big:
                die(f"P10: a batch holds at most 15 pages — split {', '.join(big)} by cluster or county")
        import urlcheck   # P7: the whole plan, incl. city/service mixing, -2 suffixes, hubs, changed URLs
        bad = urlcheck.problems(list(pages.values()))
        if bad:
            die("site plan URLs break the URL rule:\n  - " + "\n  - ".join(bad))
        missing = [pid for pid, p in pages.items() if p["type"] in KIND_ORDER and pid not in seen]
        if missing:
            die("pages in no batch: " + ", ".join(missing))
        pilot = next((b for b in plan["batches"] if b["id"] == "pilot"), None)
        needed, why_pilot = pilot_needed(st)   # CM-061 §9: a pilot only when it is worth it
        if needed and not pilot:
            die(f"a pilot is needed ({why_pilot}): the first batch must be 'pilot' with exactly 1 service + 1 location page")
        if pilot and sorted(pages[x]["type"] for x in pilot["pages"]) != ["location", "service"]:
            die("the pilot batch must have exactly 1 service + 1 location page")
        for pid, p in pages.items():
            st["pages"].setdefault(pid, {"state": "planned"}).update(
                {k: p[k] for k in ("type", "name", "url", "group", "city", "service_variant", "h1", "replaces", "nav", "claims",
                                   "keyword", "category_variant", "area_variant", "faq", "h2s", "link_exceptions") if k in p})   # Rewrite 4: outline.py; CM-064: wheel.py asks
        st["build"] = {"site_plan": {"file": a.file, "approval": None},
                       "batches": [{**{k: b[k] for k in ("id", "kind", "label", "pages")},
                                    "state": "planned", "briefs": None, "drafts": None,
                                    # Rewrite 4 (D2): a new section has no brief — outline.py derives the outline
                                    "route": b.get("route") or config().get("build_route") or "outline",
                                    "files": {}}
                                   for b in plan["batches"]],
                       "pilot_corrections_applied": None,
                       **({} if pilot else {"pilot_waived": {"at": now(), "reason": why_pilot, "rule": "CM-061 §9"}})}
        print(f"pilot: {'yes — ' if needed else ''}{why_pilot}")
        st.setdefault("marks", {})["site_plan"] = {"files": {a.file: sha12(ROOT / a.file)}, "at": now(), "ts": time.time()}
        save(a.slug, st); print(render_build(st))
    elif a.cmd == "batch":
        b = batch(st, a.batch_id) or die(f"no batch {a.batch_id}")
        if a.state in ("briefs_written", "drafts_written"):
            stage = "brief" if a.state == "briefs_written" else "draft"
            if a.state == "briefs_written":
                ok, why = batch_ready(st, a.batch_id, "briefs")
                if not ok:
                    die(f"batch {a.batch_id}: " + "; ".join(why))
            # CM-043: each page's brief and draft come from its own run; the batch only collects them.
            per_page, probs = per_page_files(st, b, stage)
            if probs:
                die(f"batch {a.batch_id}: " + "; ".join(probs))
            given = [f.strip() for f in (a.files or "").split(",") if f.strip()]
            if given and sorted(given) != sorted(per_page):
                die(f"batch {a.batch_id}: --files must be exactly the per-page {stage}s recorded with "
                    f"status.py page-stage ({', '.join(per_page)})")
            a.files = ",".join(per_page)
        stage_needed = {"drafts_written": "briefs", "sem_applied": "drafts", "sem_check_failed": "drafts",
                        "drafted": "drafts", "handed_off": "drafts", "corrections_requested": "drafts", "published": "drafts",
                        "verified": "drafts", "written_back": "drafts"}.get(a.state)
        pilot_write = (a.state == "drafts_written" and a.batch_id == "pilot"
                       and not per_page_files(st, b, plan_stage(b))[1])   # P10: pilot briefs + drafts approved together
        if stage_needed and not pilot_write and not batch_stage_ok(st, a.batch_id, stage_needed, False)[0]:
            die(f"batch {a.batch_id}: {stage_needed} are not approved yet")
        fs = [f.strip() for f in (a.files or "").split(",") if f.strip()]
        for f in fs + [x for x in (a.sem_table, a.review_sheet) if x]:
            if not (ROOT / f).exists():
                die(f"{f} not found")
        if a.state in ("drafts_written", "sem_applied"):
            import publish
            bad = [f"{Path(f).name}: {x}" for f in fs for x in publish.placeholder_problems((ROOT / f).read_text(encoding="utf-8"))]
            if bad:
                die(f"batch {a.batch_id}: placeholder(s) without a visible [NEED: ...] note (CM-016):\n  - " + "\n  - ".join(bad))
        log_line = None
        if a.state == "briefs_written" and fs:
            b.setdefault("files", {})["briefs"] = fs
        elif a.state == "drafts_written" and a.review_sheet:
            # CM-061: the one draft review sheet (review.py sheet) — SEM picks are rows in it, never a --sem list
            rv = ((b.get("review") or {}).get("drafts") or {})
            if rv.get("sheet") != a.review_sheet:
                die(f"batch {a.batch_id}: {a.review_sheet} is not this section's draft review sheet (review.py sheet "
                    f"{a.slug} {a.batch_id} drafts) — recorded: {rv.get('sheet') or 'none'}")
            b.setdefault("files", {})["drafts"] = fs   # F-026: the sheet is not a draft
            b["files"]["review_sheet"] = a.review_sheet
            b["sem_findings"] = 0
            b["drafts"] = None
        elif a.state == "drafts_written":
            if not fs or not a.sem_table or a.sem_findings is None:
                die("drafts_written needs --files <one draft per page> and --review-sheet <the section's drafts review "
                    "sheet> (CM-061) — or, for a batch already under way, --sem-table <table> --sem-findings <n>")
            # Paul reviews each draft with the batch's semantic review table and approves both at once.
            b.setdefault("files", {})["drafts"] = fs + [a.sem_table]
            b["sem_findings"] = a.sem_findings
            b["drafts"] = None
        elif a.state == "sem_applied":
            ids = (b.get("drafts") or {}).get("sem_ids") or []
            if not ids:
                die(f"batch {a.batch_id}: Paul approved no SEM items — nothing to apply")
            if not a.checks_passed or not fs:
                die("sem_applied needs --files <the drafts after applying the approved SEM items> and "
                    "--checks-passed (E1–E10 re-run on every changed section). If a check failed, use "
                    "--state sem_check_failed --note \"<which check, which page>\".")
            # Re-pin the approval to the applied versions: the change is exactly what Paul approved.
            table = [f for f in (b["drafts"].get("files") or {}) if f not in fs]
            b["drafts"]["files"] = {f: sha12(ROOT / f) for f in fs + table}
            b["drafts"]["applied"] = {"sem_ids": ids, "at": now(), "checks": "E1–E10 passed on changed sections"}
            b["files"]["drafts"] = fs + table
            log_line = (f"- SEM APPLIED {now()[:16]} · batch {a.batch_id} · {', '.join(ids)} · E-checks passed · "
                        "approval pinned to the applied versions\n")
        elif a.state == "sem_check_failed":
            if not a.note or not fs:
                die("sem_check_failed needs --files <the drafts as they now stand> --note \"<which check failed, where>\"")
            b["drafts"] = {**(b.get("drafts") or {}), "state": "revise",
                           "check_failure": a.note, "at": now()}
            b["files"]["drafts"] = fs + [f for f in b["files"].get("drafts", []) if f not in fs and "Semantic" in f]
            log_line = f"- SEM CHECK FAILED {now()[:16]} · batch {a.batch_id} · {a.note} · back to Paul\n"
        elif fs:
            b.setdefault("files", {})[a.state] = fs
        set_batch_state(st, b, a.state)
        save(a.slug, st)
        if log_line:
            with open(path(a.slug).parent / "log.md", "a", encoding="utf-8") as fh:
                fh.write(log_line)
        print(f"batch {a.batch_id}: {a.state}")
    elif a.cmd == "mark":
        files = {}
        for f in a.file:
            gone = ref_missing(f)
            if gone:
                die(f"{gone} — a mark needs the file (and sections) that prove it")
            files[f] = ref_sha(f)
        st.setdefault("marks", {})[a.name] = {"files": files, "at": now(), "ts": time.time()}
        save(a.slug, st); print(f"{a.name}: {', '.join(files)}")
    elif a.cmd == "page-stage":
        import run as R
        R.open_run(a.slug, a.run)
        info = (st.get("open_runs") or {}).get(a.run) or {}
        want = f"build:{a.stage}"
        write_run = info.get("step") == "build:write" or (info.get("step") == want and info.get("pages") == "all")
        b = batch_of(st, a.page_id) or die(f"{a.page_id} is in no batch")
        # F-011/HMM: after Paul answers a review sheet, the review run records every page again at the version the
        # answers produced — the only way the approval can cover it (approve.py page_version_problems)
        rv_applied = (((b.get("review") or {}).get(f"{a.stage}s") or {}).get("applied"))
        review_run = info.get("step") == "build:review" and bool(rv_applied) and a.page_id in b["pages"]
        if info.get("step") != want and not write_run and not review_run:
            die(f"a {a.stage} is recorded only by its own /build {a.stage} run, the batch's write run, or (after the "
                f"review answers are applied) the review run (this run is {info.get('step')}).")
        prior = (st["pages"].get(a.page_id, {}).get("files") or {}).get(a.stage) or {}
        if review_run and a.stage == "draft" and not a.agent:
            a.agent = prior.get("agent")   # a re-record keeps the fresh sub-agent that wrote the page (CM-043)
        if write_run and a.stage == "draft" and not a.agent:
            die("in a write run each page's draft comes from its own fresh sub-agent (CM-043): pass --agent <its id>.")
        if write_run or review_run:
            pass
        elif a.stage == "draft" and info.get("page") != a.page_id:
            die(f"run {a.run} was started for page {info.get('page')}; it cannot record {a.page_id}. "
                "One page per run (CM-043): start a run for that page.")
        if a.stage == "brief" and info.get("page") not in (None, a.page_id):
            die(f"run {a.run} was started for page {info.get('page')}; it cannot record {a.page_id}.")
        if info.get("batch") and info["batch"] != b["id"]:
            die(f"{a.page_id} is in batch {b['id']}, not {info['batch']}")
        f = ROOT / a.file
        if not f.is_file():
            die(f"{a.file} not found")
        if a.stage == "brief" and route(b) == "outline":
            die(f"section {b['id']} is on the outline route (Rewrite 4): no brief — outline.py writes each page's "
                "outline in the write run.", 4)
        if a.stage == "brief":
            ok, why = evidence_ok(st, a.page_id)
            if not ok:
                die(f"no brief for a page the evidence gate has not cleared (CM-041): {why}")
            pk = (st["pages"][a.page_id].get("pack") or {})
            if not pk.get("file") or not (ROOT / pk["file"]).is_file():
                die(f"no brief for {a.page_id} without its evidence pack (CM-061) — evidence_pack.py build {a.slug} "
                    f"{b['id']} (the evidence gate builds it)")
            res = evidence_state(st, a.page_id)[0]
            if res in ("warn", "block") and not re.search(r"^#+\s*Evidence gaps", f.read_text(), re.M | re.I):
                die(f"{a.page_id} cleared the evidence gate with {'a WARN' if res == 'warn' else 'your waiver'}: the brief "
                    "must carry an 'Evidence gaps' section listing every gap from the grid.")
            if _approval_ok(b.get("briefs"), "briefs", False)[0]:   # F-011: Paul's recorded approval, never auto mode's "nothing to approve"
                die(f"batch {b['id']} briefs are already approved; Paul re-opens them first (--decision revise).")
        else:
            in_write = write_run and (b["id"] == "pilot" or not briefs_need_approval(st, b["id"])) \
                and not per_page_files(st, b, plan_stage(b))[1]   # P10: the pilot, briefs on auto, or the outline route
            if not in_write and not review_run and not batch_stage_ok(st, b["id"], "briefs", False)[0]:
                die(f"batch {b['id']}: the briefs are not approved yet — no drafts before Paul approves the briefs.")
            import publish
            bad = publish.placeholder_problems(f.read_text(encoding="utf-8"))
            if bad:
                die(f"{a.page_id}: placeholder(s) without a visible [NEED: ...] note (CM-016):\n  - " + "\n  - ".join(bad))
            if batch_stage_ok(st, b["id"], "drafts", False)[0]:
                die(f"batch {b['id']} drafts are already approved; Paul re-opens them first (--decision revise).")
        p = st["pages"][a.page_id]
        p.setdefault("files", {})[a.stage] = {"file": a.file, "run": a.run, "at": now(), "sha": sha12(f),
                                               "ts": time.time(), **({"agent": a.agent} if a.agent else {})}
        p["state"] = "brief_written" if a.stage == "brief" else "draft_written"
        log_line = (f"- {a.stage.upper()} {now()[:16]} · run {a.run} · {a.page_id} · {a.file}"
                    + (f" · agent {a.agent}" if a.agent else "") + "\n")
        if a.stage == "brief" and b.get("state") in ("planned", "briefs_written"):
            files, probs = per_page_files(st, b, "brief")
            if not probs:   # every page has its brief: collect them for Paul's one approval
                b.setdefault("files", {})["briefs"] = files
                if (b.get("briefs") or {}).get("state") in GATES["met_decisions"]:
                    b["briefs"] = None   # F-011: a revise record stays — wiping it made auto mode read the batch as approved
                set_batch_state(st, b, "briefs_written")
                log_line += f"- BRIEFS COLLECTED {now()[:16]} · batch {b['id']} · {len(files)} page(s), one run each\n"
        save(a.slug, st)
        with open(path(a.slug).parent / "log.md", "a", encoding="utf-8") as fh:
            fh.write(log_line)
        print(f"{a.page_id}: {a.stage} recorded" + (" · batch briefs collected" if "COLLECTED" in log_line else ""))
    elif a.cmd == "pilot":   # CM-061 §9: does this client's next section need a pilot, and why
        needed, why = pilot_needed(st)
        print(f"pilot {'needed' if needed else 'not needed'}: {why}")
    elif a.cmd == "modes":
        for step, spec in mode_stages().items():
            m = stage_mode(st, step)
            own = (st.get("modes") or {}).get(step)
            src = "this client" if own else ("global" if (config().get("stage_modes") or {}).get(step) else "default")
            ok, _ = pilot_passed(st, step)
            print(f"  {step:20} {m:6} ({src})  pilot {'passed' if ok else ('—' if not spec.get('pilot') else 'not yet')}")
    elif a.cmd == "writeback":   # CM-061 §6: ONE Brand Guide write-back per section, at the brief approval
        b = batch(st, a.batch_id) or die(f"no batch {a.batch_id}")
        if route(b) == "outline":   # Rewrite 4: no briefs — written once, from the drafts, before their one approval
            _, probs = per_page_files(st, b, "draft")
            rv = (b.get("review") or {}).get("drafts") or {}
            why = probs + ([] if b.get("state") in ("drafts_written", "sem_applied", "sem_check_failed") else
                           [f"section {a.batch_id} is not written yet (state {b.get('state')})"])
            why += [f"the {a.batch_id} drafts review sheet is not applied yet"] if rv and not rv.get("applied") else []
            if why:
                die("REFUSED — on the outline route the Brand Guide is written once per section, from its drafts after "
                    "the review answers and before the drafts approval (Rewrite 4): " + "; ".join(why), 4)
        else:
            ok, why = check(st, f"batch:{a.batch_id}:briefs")
            if not ok:
                die("REFUSED — the Brand Guide is written once per section, at the brief approval (CM-061): "
                    + "; ".join(why), 4)
        if b.get("content_written_back"):
            die(f"REFUSED — section {a.batch_id} already wrote the Brand Guide ({b['content_written_back']['at'][:16]}, "
                f"run {b['content_written_back']['run']}). It is written once per section (CM-061); drafts, the draft "
                "review and ship never write it.", 4)
        b["content_written_back"] = {"at": now(), "run": a.run}
        save(a.slug, st)
        append(client_dir(a.slug) / "log.md", f"- WRITE-BACK {now()[:16]} · run {a.run} · batch {a.batch_id}: Brand Guide "
               "B3, C1/C2, C3 updated once for the section, from its "
               + ("reviewed drafts" if route(b) == "outline" else "approved briefs") + "\n")
        print(f"batch {a.batch_id}: Brand Guide write-back recorded")
    elif a.cmd == "specs-adopt":
        st = load(a.slug)
        st["specs_pinned"] = {}
        pin_specs(st)
        save(a.slug, st)
        print(f"{a.slug}: now on the currently approved page specs ({len(st['specs_pinned'])} files pinned)")
    elif a.cmd == "pilot-corrections":
        pstage = "drafts" if route(batch(st, "pilot")) == "outline" else "briefs"
        if not batch_stage_ok(st, "pilot", pstage, False)[0]:
            die(f"the pilot {pstage} are not approved yet")
        st["build"]["pilot_corrections_applied"] = {"at": now(), "note": a.note,
                                                    **({"none": True} if a.none else {})}
        save(a.slug, st); print("pilot corrections recorded")
        cfg = config()
        rec = cfg.get("specs_approval") or {}
        moved = [f for f in spec_files() if rec.get("files") and (rec["files"].get(f) != spec_sha(f))]
        if moved:   # a logged pilot correction keeps a spec APPROVED (specs/README.md, status line rule)
            for f in moved:
                rec["files"][f] = spec_sha(f)
            rec.setdefault("pilot_corrections", []).append({"at": now(), "client": a.slug, "specs": moved, "note": a.note})
            write_json(ROOT / "config.json", cfg)
            append(path(a.slug).parent / "log.md", f"- PILOT CORRECTIONS {now()[:16]} · specs re-stamped (approval kept): "
                   f"{', '.join(Path(f).name for f in moved)} · {a.note}\n")


if __name__ == "__main__":
    main()
