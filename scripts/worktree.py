#!/usr/bin/env python3
"""worktree.py — one git worktree per client (rewrite 2 P2, Q1: two clients, two chats, no mixing).

    worktree.py open <slug>     create or reuse <client_worktrees_root>/<slug>/ on branch client/<slug> (from main)
                                and print the folder to open the chat in
    worktree.py list            every client worktree

Each worktree has its own git index (one client's commit can never pick up another's files) and its own
.claude/state/ (its own session files). Credentials and machine.json stay in the main checkout; lib.py reads them
from there. The client's git-ignored raw data (inputs/, crawl/, data/*/raw/) is linked from the main checkout, so
nothing already pulled has to be pulled again. A system session never runs in a worktree — only in the main folder.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from lib import SLUG_RE, config, die, main_root


def git(*args, cwd=None):
    return subprocess.run(["git", "-C", str(cwd or main_root()), *args], capture_output=True, text=True)


def root_dir():
    return Path(config().get("client_worktrees_root") or "~/Documents/seo-ops-clients").expanduser()


def link_ignored(slug, wt):
    """Link the client's git-ignored raw data from the main checkout into the worktree."""
    src = main_root() / "clients" / slug
    dst = wt / "clients" / slug
    linked = []
    pats = ["inputs", "crawl"] + [str(p.relative_to(src)) for p in src.glob("data/*/raw")] if src.exists() else []
    for rel in pats:
        s, d = src / rel, dst / rel
        if s.exists() and not d.exists() and not d.is_symlink():
            d.parent.mkdir(parents=True, exist_ok=True)
            d.symlink_to(s)
            linked.append(rel)
    return linked


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
    linked = link_ignored(slug, wt)
    if linked:
        print("linked from the main folder: " + ", ".join(linked))
    print(f"Open the chat for {slug} in this folder:\n{wt}")
    return wt


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("open"); s.add_argument("slug")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "open":
        open_wt(a.slug)
    else:
        out = git("worktree", "list").stdout.strip().splitlines()
        rows = [l for l in out if "[client/" in l]
        print("\n".join(rows) or "no client worktrees")


if __name__ == "__main__":
    main()
