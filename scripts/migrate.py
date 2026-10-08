#!/usr/bin/env python3
"""migrate.py — bring a client's status.json to the 2026-10-08 rewrite (schema 4) without losing an approval.

    migrate.py <slug> [--dry-run]
    migrate.py --all [--dry-run]

What it does (once per client; schema 4 = done):
  1. Section approvals (brand-guide.md#A+B1+B2 …) are re-stamped to the new hash, which ignores row status
     columns (R3) — only where the old hash still matches, so an approval that is void stays void.
  2. discovery_signed_off and blockers_cleared are now conditions (R3): their old records move to
     status.json → retired_gates (history kept); the conditions are then checked from evidence.
  3. A hand-written STATUS.md (no "Generated" line) is carried into the settled register: each bullet under
     "Settled" becomes a SETTLED line, each "Waiting on" row that is not a handoff or the page specs becomes an
     OPEN question — then STATUS.md is regenerated (R7).
  4. A MIGRATION line goes into log.md; the records are regenerated; one git commit.
"""
import re
import sys

import status as S
from lib import CLIENTS, append, client_dir, git_commit, now, ref_sha, ref_sha_v1

RETIRED = ("discovery_signed_off", "blockers_cleared")


def key_of(text, used):
    k = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:40].strip("_") or "item"
    base, n = k, 2
    while k in used:
        k, n = f"{base}_{n}", n + 1
    used.add(k)
    return k


def restamp(files, counts):
    for f, h in list((files or {}).items()):
        if "#" not in f:
            continue
        try:
            if ref_sha_v1(f) == h:
                new = ref_sha(f)
                if new != h:
                    files[f] = new
                    counts["restamped"] += 1
            else:
                counts["void_kept"] += 1
        except FileNotFoundError:
            counts["void_kept"] += 1


def handwritten(slug):
    """(settled bullets [(label, text)], open rows [(who, what, ref)]) from a hand-written STATUS.md."""
    p = client_dir(slug) / "STATUS.md"
    if not p.exists():
        return [], []
    text = p.read_text()
    if "Generated" in text.split("\n## ", 1)[0]:
        return [], []
    settled_, open_ = [], []
    m = re.search(r"^## Settled[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if m:
        for b in re.split(r"\n(?=- )", m.group(1).strip()):
            b = " ".join(x.strip() for x in b.strip().lstrip("- ").splitlines())
            lm = re.match(r"\*\*(.+?):?\*\*:?\s*(.*)", b)
            if lm and "decides once" in lm.group(2):   # not settled yet: a question Paul answers once (#22)
                open_.append(("Paul", f"{lm.group(1).rstrip(':')}: {lm.group(2)}", "Decision Sheet"))
            elif lm:
                settled_.append((lm.group(1).rstrip(":"), lm.group(2)))
    m = re.search(r"^## Waiting on[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if m:
        for line in m.group(1).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or cells[0] in ("Who", "") or set(cells[0]) <= set("-"):
                continue
            who, what, _, ref = cells[:4]
            if ref.lower().startswith("handoff") or "page specs" in what.lower():
                continue   # handoffs and the specs decision are generated from the system itself
            open_.append((who, what.replace("`", ""), ref))
    return settled_, open_


def migrate(slug, dry=False):
    import settled
    st = S.load(slug)
    if st.get("schema", 3) >= 4:
        return f"{slug}: already migrated"
    counts = {"restamped": 0, "void_kept": 0}
    for rec in st["gates"].values():
        restamp(rec.get("files"), counts)
    bp = st.get("build") or {}
    restamp(((bp.get("site_plan") or {}).get("approval") or {}).get("files"), counts)
    for b in bp.get("batches") or []:
        for stage in S.STAGES:
            restamp((b.get(stage) or {}).get("files"), counts)
    moved = [g for g in RETIRED if g in st["gates"]]
    s_items, o_items = handwritten(slug)
    if dry:
        return (f"{slug}: would re-stamp {counts['restamped']} section approval(s) (void kept: {counts['void_kept']}), "
                f"retire {', '.join(moved) or 'nothing'}, carry {len(s_items)} settled and {len(o_items)} open item(s)")
    for g in moved:
        st.setdefault("retired_gates", {})[g] = {**st["gates"].pop(g), "retired": now(),
                                                 "why": "R3: now a condition, met from evidence"}
    st["schema"] = 4
    S.save(slug, st)
    d = client_dir(slug)
    append(d / "log.md", f"\n## MIGRATION · {now()} · schema 4 (rewrite 2026-10-08)\n"
           f"Section approvals re-stamped (status columns no longer hashed): {counts['restamped']} · "
           f"void approvals left void: {counts['void_kept']} · now conditions: {', '.join(moved) or '—'}\n")
    used = set(settled.entries(slug))
    for label, text in s_items:
        k = key_of(label, used)
        settled.settle(slug, "migration-v4", k, f"{label}: {text}", by="Paul (STATUS.md, 2026-10-08)", closed_ok=True)
    for who, what, ref in o_items:
        k = "wordpress_login" if what.lower().startswith("wordpress") and "wordpress_login" not in used \
            else key_of(what.split("?")[0], used)
        used.add(k)
        settled.ask(slug, "migration-v4", k, who, what + (f" (ref {ref})" if ref and ref != "—" else ""), closed_ok=True)
    st = S.load(slug)
    S.log_conditions(slug, st)
    import records
    records.render(slug)
    return (f"{slug}: migrated — {counts['restamped']} section approval(s) re-stamped, {counts['void_kept']} left void, "
            f"retired {', '.join(moved) or 'nothing'}, {len(s_items)} settled + {len(o_items)} open carried over")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    slugs = sorted(p.parent.name for p in CLIENTS.glob("*/status.json")) if "--all" in sys.argv else args
    if not slugs:
        sys.exit(__doc__)
    out = [migrate(s, dry) for s in slugs]
    print("\n".join(out))
    if not dry:
        print(git_commit("migrate clients to schema 4 (rewrite 2026-10-08)\n\n" + "\n".join(out)))


if __name__ == "__main__":
    main()
