#!/usr/bin/env python3
"""worktree.py — one git worktree per client (rewrite 2 P2, Q1: two clients, two chats, no mixing).

    worktree.py open <slug>     create or reuse <client_worktrees_root>/<slug>/ on branch client/<slug> (from main)
                                and print the folder to open the chat in
    worktree.py check [<slug>]  exit 4 with a plain message if this worktree is missing a link (run.py start, /where)
    worktree.py list            every client worktree

Each worktree has its own git index (one client's commit can never pick up another's files) and its own
.claude/state/ (its own session files). Everything git ignores that a stage needs — machine.json, .env and the
client's inputs/, crawl/ and data/*/raw/ — lives only in the main checkout and is symlinked into the worktree
(created when missing, never copied), so nothing already pulled is pulled again and each secret has one copy. A system session never runs in a worktree — only in the main folder.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from lib import ROOT, SLUG_RE, config, die, main_root


def git(*args, cwd=None):
    return subprocess.run(["git", "-C", str(cwd or main_root()), *args], capture_output=True, text=True)


def root_dir():
    return Path(config().get("client_worktrees_root") or "~/Documents/seo-ops-clients").expanduser()


SHARED = {"machine.json": "this Mac's settings", ".env": "the credentials"}
DATA = {"inputs": "the client's inputs", "crawl": "the client's crawl files"}


def is_worktree():
    return ROOT.resolve() != main_root().resolve()


def wanted(slug):
    """Every git-ignored path a client worktree must see from the main folder, as {relative path: what it is}.
    Only what exists in the main folder is wanted (no machine.json there = this Mac uses the defaults)."""
    main = main_root()
    out = {rel: what for rel, what in SHARED.items() if (main / rel).exists()}
    c = main / "clients" / slug if slug else None
    if c and c.exists():
        out.update({f"clients/{slug}/{rel}": what for rel, what in DATA.items() if (c / rel).exists()})
        out.update({str(p.relative_to(main)): f"raw data pulled for {p.parent.name}" for p in sorted(c.glob("data/*/raw"))})
    return out


def linked(rel, wt):
    d = wt / rel
    return d.is_symlink() and d.resolve() == (main_root() / rel).resolve()


def link_ignored(slug, wt):
    """Link machine.json, the credentials and the client's git-ignored data (inputs/, crawl/, data/*/raw/) from the
    main folder into the worktree — symlinks, created when missing, never copied. Returns (linked now, not linked)."""
    main = main_root()
    if (main / "clients" / slug / "status.json").exists():
        (main / "clients" / slug / "inputs").mkdir(parents=True, exist_ok=True)
    done, left = [], []
    for rel in wanted(slug):
        s, d = main / rel, wt / rel
        if linked(rel, wt):
            continue
        if d.is_symlink():                       # a link to somewhere else, or to nothing: only the link is replaced
            d.unlink()
        elif d.is_dir() and not any(d.iterdir()):
            d.rmdir()                            # an empty real folder: nothing in it to lose
        elif d.exists():
            left.append(rel)                     # a real file, or a folder with files in it: never touched
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        d.symlink_to(s)
        done.append(rel)
    return done, left


def problems(slug=None):
    """In a client worktree: every wanted path that is not linked to the main folder. [] in the main folder."""
    if not is_worktree():
        return []
    want = wanted(slug)
    return [f"{rel} ({want[rel]})" for rel in want if not linked(rel, ROOT)]


def refusal(slug=None):
    """The plain message for /where and run.py start, or None when nothing is missing."""
    bad = problems(slug)
    if not bad:
        return None
    return (f"REFUSED — this client folder ({ROOT}) can't see files that live only in the main folder:\n  - "
            + "\n  - ".join(bad)
            + f"\nFix: run `python3 scripts/worktree.py open {slug or '<slug>'}`, then try again. It links them; "
            "nothing is copied. If it says a folder has its own files, move those files into the same place in the "
            f"main folder ({main_root()}) first.")


def open_wt(slug):
    if not SLUG_RE.match(slug):
        die(f"Bad client slug '{slug}'.")
    wt = root_dir() / slug
    branch = f"client/{slug}"
    if (wt / ".git").exists():
        print(f"reusing {wt} (branch {git('rev-parse', '--abbrev-ref', 'HEAD', cwd=wt).stdout.strip()})")
    else:
        has_origin = git("remote", "get-url", "origin").returncode == 0
        if has_origin:
            git("fetch", "-q", "origin", "main")
        base = "origin/main" if has_origin else "main"
        exists = git("rev-parse", "--verify", "-q", branch).returncode == 0
        wt.parent.mkdir(parents=True, exist_ok=True)
        r = git("worktree", "add", "-q", str(wt), branch) if exists else git("worktree", "add", "-q", "-b", branch, str(wt), base)
        if r.returncode != 0:
            die(f"could not create the worktree: {r.stderr.strip()}")
        if has_origin:
            git("branch", "--set-upstream-to=origin/main", branch, cwd=wt)
        print(f"created {wt} on branch {branch} (from {base})")
    done, left = link_ignored(slug, wt)
    if done:
        print("linked from the main folder: " + ", ".join(done))
    for rel in left:
        print(f"NOT LINKED — {wt / rel} has its own files. Move them into {main_root() / rel}, then run this again.")
    seen = [rel for rel in wanted(slug) if linked(rel, wt)]
    print("sees from the main folder: " + (", ".join(seen) or "nothing (none of them exist there)"))
    print(f"Open the chat for {slug} in this folder:\n{wt}")
    return wt


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("open"); s.add_argument("slug")
    s = sub.add_parser("check"); s.add_argument("slug", nargs="?")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "open":
        open_wt(a.slug)
    elif a.cmd == "check":
        msg = refusal(a.slug)
        if msg:
            die(msg, 4)
        print("this folder sees everything it needs from the main folder" if is_worktree() else "main folder")
    else:
        out = git("worktree", "list").stdout.strip().splitlines()
        rows = [l for l in out if "[client/" in l]
        print("\n".join(rows) or "no client worktrees")


if __name__ == "__main__":
    main()
