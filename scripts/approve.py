#!/usr/bin/env python3
"""approve.py — the only way a gate or a page approval changes. Run only via /approve.

    approve.py <slug> <gate> --decision D [--conditions "a; b"] [--files f1,f2] [--note T]
    approve.py <slug> page:<page_id> --decision D [--file F] [--review "Paul reviewed"]
               [--practitioner "Name, licence"] [--note T]
    approve.py <slug> import --proposal clients/<slug>/import-proposal.json

Refuses unless Paul typed /approve in this session within the last 20 minutes: the
UserPromptSubmit hook writes a one-time token when — and only when — a real user prompt
starts with "/approve". Claude cannot create that token (the guard hook blocks it), so
a gate cannot be set on Claude's initiative. Each token approves one invocation.
"""
import argparse
import json
import sys
import time

import status as S
from lib import ROOT, append, client_dir, die, git_commit, now, read_json, sha12, write_json

TOKEN = ROOT / ".claude" / "state" / "approve-token.json"
MAX_AGE = 20 * 60


def take_token(slug, target):
    tok = read_json(TOKEN)
    if not tok:
        die("REFUSED — no /approve from Paul in this session. Only Paul can approve, by typing "
            "/approve himself.", 7)
    if tok.get("used"):
        die("REFUSED — that /approve has already been used. Paul must type /approve again.", 7)
    if time.time() - tok.get("created", 0) > MAX_AGE:
        die("REFUSED — Paul's /approve is older than 20 minutes. Ask him to type it again.", 7)
    words = tok.get("prompt", "").lower()
    parts = [x for x in target.lower().split(":") if x not in ("page", "batch")]
    if slug not in words or not all(x in words for x in parts):
        die(f"REFUSED — Paul's /approve did not name '{slug}' and '{target}'. "
            f"He typed: {tok.get('prompt', '')[:120]!r}", 7)
    tok["used"] = True
    tok["used_for"] = f"{slug} {target}"
    write_json(TOKEN, tok)
    return tok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("target")
    ap.add_argument("--decision", choices=S.GATES["decisions"])
    ap.add_argument("--conditions"); ap.add_argument("--files"); ap.add_argument("--file")
    ap.add_argument("--note"); ap.add_argument("--review"); ap.add_argument("--practitioner")
    ap.add_argument("--proposal")
    a = ap.parse_args()
    d = client_dir(a.slug)
    st = S.load(a.slug)

    if a.target == "import":
        prop = read_json(ROOT / a.proposal) if a.proposal else None
        if not prop:
            die("No import proposal file.")
        take_token(a.slug, "import")
        for g, rec in prop.get("gates", {}).items():
            if g not in st["gates"]:
                die(f"Unknown gate in proposal: {g}")
            st["gates"][g] = {**rec, "by": "Paul (import confirmed)", "at": now(),
                              "source": rec.get("source", "Drive Approval Record")}
        for pid, p in prop.get("pages", {}).items():
            st["pages"][pid] = p
        st["client"]["imported"] = True
        S.save(a.slug, st)
        append(d / "log.md", f"\n## APPROVAL · {now()} · import confirmed by Paul\n"
               f"Gates set from {a.proposal}: {', '.join(prop.get('gates', {}))}\n")
        print(git_commit(f"{a.slug}: import confirmed by Paul"))
        return

    if not a.decision:
        die("--decision is required")

    if a.target == "site_plan" or a.target.startswith("batch:"):
        bp = st.get("build") or die("No site plan registered yet (status.py plan ...).")
        files = {}
        for f in [x.strip() for x in (a.files or a.file or "").split(",") if x.strip()]:
            if not (ROOT / f).exists():
                die(f"File {f} not found.")
            files[f] = sha12(ROOT / f)
        approved = a.decision in S.GATES["met_decisions"]
        if a.target == "site_plan":
            if not files:
                files[bp["site_plan"]["file"]] = sha12(ROOT / bp["site_plan"]["file"])
            holder, key, label_ = bp["site_plan"], "approval", "site plan"
        else:
            _, bid, stage = (a.target.split(":") + ["", ""])[:3]
            if stage not in ("briefs", "drafts"):
                die("Use batch:<id>:briefs or batch:<id>:drafts")
            b = S.batch(st, bid) or die(f"No batch {bid}.")
            if approved:
                ok, why = S.batch_ready(st, bid, stage)
                if not ok:
                    die("REFUSED — " + "; ".join(why))
                if not files:
                    die("Name the exact files approved (--files), one per page in the batch.")
                if stage == "drafts" and st["client"]["sensitive"] and not a.review:
                    die("REFUSED — sensitive client: record the human review with --review.")
                if stage == "drafts" and st["client"]["practitioner_signoff"] and not a.practitioner:
                    die("REFUSED — health content: record the licensed practitioner's sign-off with --practitioner.")
            holder, key, label_ = b, stage, f"batch {bid} {stage}"
        take_token(a.slug, a.target)
        holder[key] = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note, "files": files,
                       "conditions": [c.strip() for c in (a.conditions or "").split(";") if c.strip()],
                       "sensitive_review": a.review, "practitioner": a.practitioner}
        S.save(a.slug, st)
        append(d / "log.md", f"\n## APPROVAL · {now()} · {label_} · {a.decision} · by Paul\n"
               + "".join(f"Approved version: {f} (sha {h})\n" for f, h in files.items())
               + (f"Human review: {a.review}\n" if a.review else "")
               + (f"Practitioner sign-off: {a.practitioner}\n" if a.practitioner else "")
               + (f"Note: {a.note}\n" if a.note else ""))
        print(git_commit(f"{a.slug}: {label_} {a.decision} by Paul"))
        return

    if a.target.startswith("page:"):
        pid = a.target[5:]
        p = st["pages"].get(pid) or die(f"Page {pid} is not registered (status.py page ...).")
        approved = a.decision in S.GATES["met_decisions"]
        if approved and st["client"]["sensitive"] and not a.review:
            die("REFUSED — sensitive client: record the human review with --review "
                "(who reviewed the content before it goes live).")
        if approved and st["client"]["practitioner_signoff"] and not a.practitioner:
            die("REFUSED — health content: the client's licensed practitioner must sign off on "
                "health claims. Record who with --practitioner \"Name, licence\".")
        f = a.file or p.get("file")
        if approved and f and not (ROOT / f).exists():
            die(f"File {f} not found.")
        take_token(a.slug, a.target)
        p["approval"] = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note,
                         "file": f, "sha": sha12(ROOT / f) if f and (ROOT / f).exists() else None,
                         "sensitive_review": a.review, "practitioner": a.practitioner}
        if approved:
            p["state"] = "approved"
        S.save(a.slug, st)
        append(d / "log.md", f"\n## APPROVAL · {now()} · page {pid} · {a.decision} · by Paul\n"
               + (f"File: {f} (sha {p['approval']['sha']})\n" if f else "")
               + (f"Human review: {a.review}\n" if a.review else "")
               + (f"Practitioner sign-off: {a.practitioner}\n" if a.practitioner else "")
               + (f"Note: {a.note}\n" if a.note else ""))
        print(git_commit(f"{a.slug}: page {pid} {a.decision} by Paul"))
        return

    g = a.target
    if g not in S.GATES["gates"]:
        die(f"Unknown gate '{g}'. Gates: {', '.join(S.GATES['gates'])}")
    files = {}
    for f in (a.files or "").split(","):
        f = f.strip()
        if f:
            if not (ROOT / f).exists():
                die(f"File {f} not found — an approval names the exact version it approves.")
            files[f] = sha12(ROOT / f)
    if a.decision in S.GATES["met_decisions"] and g == "b1_audit":
        import steps
        left = steps.missing(st)
        if left:
            die("REFUSED — audit steps with no outcome (Done / Skipped / Failed): "
                + ", ".join(r["id"] for r in left) + ". See methodology/audit-steps.md.")
    if a.decision in S.GATES["met_decisions"]:
        spec = S.GATES["gates"][g]
        reqs = spec.get("requires_blog_only") if (st["client"]["type"] == "blog-only"
                                                  and "requires_blog_only" in spec) else spec["requires"]
        missing = [r for r in reqs if not S.gate_met(st, r)[0]]
        if missing:
            die("REFUSED — earlier gates are not met yet: " + ", ".join(missing))
    take_token(a.slug, g)
    st["gates"][g] = {"state": a.decision, "by": "Paul", "at": now(), "note": a.note,
                      "conditions": [c.strip() for c in (a.conditions or "").split(";") if c.strip()],
                      "files": files}
    S.save(a.slug, st)
    append(d / "log.md", f"\n## APPROVAL · {now()} · {g} · {a.decision} · by Paul\n"
           + "".join(f"Approved version: {f} (sha {h})\n" for f, h in files.items())
           + "".join(f"Condition: {c}\n" for c in st["gates"][g]["conditions"])
           + (f"Note: {a.note}\n" if a.note else ""))
    print(git_commit(f"{a.slug}: {g} {a.decision} by Paul"))


if __name__ == "__main__":
    main()
