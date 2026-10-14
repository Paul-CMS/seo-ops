"""Shared helpers for the seo-ops scripts. Standard library only.

Nothing in here prints credentials. load_env() returns values to the caller and
redact() scrubs them from any text that might be shown or logged.
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENTS = ROOT / "clients"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,60}$")


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def today():
    return datetime.date.today().isoformat()


def config():
    return json.loads((ROOT / "config.json").read_text())


def machine():
    """This Mac's own settings (machine.json, git-ignored; missing = Paul's Mac, the defaults).
    drive_local_root: this Mac's path to the v3 folder (overrides config.json drive.local_root).
    can_approve: false on a VA's Mac - the VA runs the stages, Paul approves on his own Mac.
    can_change_system: false on a VA's Mac - /system is refused there (rewrite 2 P3)."""
    p = ROOT / "machine.json"
    if not p.exists():   # a client worktree (P2) uses its Mac's settings from the main checkout
        p = main_root() / "machine.json"
    return json.loads(p.read_text()) if p.exists() else {}


def client_dir(slug, must_exist=True):
    if not SLUG_RE.match(slug or ""):
        die(f"Bad client slug '{slug}'. Use lowercase letters, digits and hyphens.")
    d = CLIENTS / slug
    if must_exist and not (d / "status.json").exists():
        die(f"No client '{slug}'. Run /new-client first.")
    return d


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())


def write_json(path, data):
    p = Path(path)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, p)


def append(path, text):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(text)


def sha12(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


# An approval can cover named sections of a Markdown file instead of the whole file:
#   clients/x/brand-guide.md#A+B1+B2  → "## Section A …" and "### B1 …" / "### B2 …" only.
# A section runs from its heading to the next heading of the same or a higher level. Edits outside the
# named sections (e.g. Build's write-back to B3, C, D) then leave the approval standing.
def ref_path(ref):
    return ROOT / ref.split("#", 1)[0]


def _md_section(text, sid):
    pats = [rf"^(#{{2}}) Section {re.escape(sid)}\b", rf"^(#{{2,3}}) {re.escape(sid)}\b"]
    lines = text.splitlines()
    for pat in pats:
        for i, line in enumerate(lines):
            m = re.match(pat, line)
            if m:
                level = len(m.group(1))
                end = next((j for j in range(i + 1, len(lines))
                            if re.match(r"^(#{1,%d}) " % level, lines[j])), len(lines))
                return "\n".join(lines[i:end])
    return None


def ref_missing(ref):
    """'' if the file (and every named section) exists, else what is missing."""
    p = ref_path(ref)
    if not p.exists():
        return f"file {ref.split('#', 1)[0]} not found"
    if "#" in ref:
        text = p.read_text(encoding="utf-8")
        gone = [s for s in ref.split("#", 1)[1].split("+") if _md_section(text, s) is None]
        if gone:
            return f"section {', '.join(gone)} not found in {ref.split('#', 1)[0]}"
    return ""


STATUS_COLS = ("status", "confidence")
STATUS_TAG = re.compile(r"\[(?:status|Submitted|Internally Verified|Client Confirmed|Disputed|Unknown|Paul Approved)"
                        r"[^\]]*\]", re.I)


def _strip_status(section):
    """R3 (2026-10-08): a row's status is not part of what Paul approved. Drop every table column headed
    Status/Confidence, inline [status] tags and 'Paul approved this section on' lines, so a reconcile that only
    moves a row from Proposed to Client Confirmed leaves the approval standing. Values still count."""
    out, drop = [], None
    for line in section.splitlines():
        if line.lstrip().startswith("|"):
            cells = line.strip().strip("|").split("|")
            if drop is None or set(line.replace("|", "").strip()) <= set("-: "):
                if not set(line.replace("|", "").strip()) <= set("-: "):
                    drop = {i for i, c in enumerate(cells) if c.strip().strip("*").lower() in STATUS_COLS}
            line = "|".join(c for i, c in enumerate(cells) if i not in (drop or set()))
        else:
            drop = None
            if re.match(r"^\*\*Paul approved this section on", line.strip()):
                continue
        out.append(STATUS_TAG.sub("", line).rstrip())
    return "\n".join(out)


VALUE_DROP = {"status", "confidence", "source", "sources", "date", "checked", "evidence", "note", "notes", "who", "by",
              "was", "quote", "where"}


def _values_only(section):
    """P4 (rewrite 2): what Paul approves in a Brand Guide section is its values. Each table row becomes a normalised
    'field = value' line (status, source, date, note and quote columns dropped); text outside tables is kept,
    without status tags and 'Paul approved this section on' lines. A confirmation or a new source never voids an
    approval; a changed value does."""
    out, keep, header = [], None, None
    for line in section.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if re.match(r"^\*\*Paul approved this section on", s):
                continue
            s = STATUS_TAG.sub("", s).strip()
        if s.startswith("|"):
            cells = [c.strip().strip("*").strip() for c in s.strip("|").split("|")]
            if set(s.replace("|", "").strip()) <= set("-: "):
                continue
            if header is None:
                header = [c.lower() for c in cells]
                keep = [i for i, c in enumerate(header) if c not in VALUE_DROP]
                continue
            vals = [re.sub(r"\s+", " ", cells[i]) for i in keep if i < len(cells)]
            out.append(" = ".join(v for v in vals if v))
        else:
            header = None
            if s:
                out.append(re.sub(r"\s+", " ", s))
    return "\n".join(out)


def ref_sha(ref):
    """sha12 of the file, or of only the named sections when the ref has #A+B1…. Brand Guide sections hash their
    values only (P4); other section refs ignore status columns (R3)."""
    if "#" not in ref:
        return sha12(ref_path(ref))
    text = ref_path(ref).read_text(encoding="utf-8")
    norm = _values_only if ref.split("#", 1)[0].endswith("brand-guide.md") else _strip_status
    parts = [norm(_md_section(text, s) or f"<missing {s}>") for s in ref.split("#", 1)[1].split("+")]
    return hashlib.sha256("\n\x00\n".join(parts).encode()).hexdigest()[:12]


def ref_sha_v2(ref):
    """The section hash of 2026-10-08 (status columns ignored, sources and notes counted) — only for migrate.py."""
    if "#" not in ref:
        return sha12(ref_path(ref))
    text = ref_path(ref).read_text(encoding="utf-8")
    parts = [_strip_status(_md_section(text, s) or f"<missing {s}>") for s in ref.split("#", 1)[1].split("+")]
    return hashlib.sha256("\n\x00\n".join(parts).encode()).hexdigest()[:12]


def ref_sha_v1(ref):
    """The section hash before 2026-10-08 (status columns counted) — only for migrate.py to re-stamp approvals."""
    if "#" not in ref:
        return sha12(ref_path(ref))
    text = ref_path(ref).read_text(encoding="utf-8")
    parts = [_md_section(text, s) or f"<missing {s}>" for s in ref.split("#", 1)[1].split("+")]
    return hashlib.sha256("\n\x00\n".join(parts).encode()).hexdigest()[:12]


_ENV_CACHE = None


def load_env():
    """Parse ROOT/.env. Values are returned, never printed."""
    global _ENV_CACHE
    if _ENV_CACHE is not None:
        return _ENV_CACHE
    env = {}
    p = ROOT / ".env"
    if not p.exists():   # a client worktree (P2): the credentials stay in the main checkout only
        p = main_root() / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    _ENV_CACHE = env
    return env


def redact(text):
    """Remove every .env value (and its base64 basic-auth form) from text."""
    text = str(text)
    import base64
    env = load_env()
    secrets = [v for v in env.values() if v and len(v) >= 4]
    for k in env:
        if k.endswith("_LOGIN") or k.endswith("_USER"):
            pw_key = k.rsplit("_", 1)[0] + ("_PASSWORD" if k.endswith("_LOGIN") else "_APP_PASSWORD")
            if env.get(pw_key):
                pair = f"{env[k]}:{env[pw_key]}".encode()
                secrets.append(base64.b64encode(pair).decode())
    for s in sorted(secrets, key=len, reverse=True):
        text = text.replace(s, "[REDACTED]")
    return text


def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def main_root():
    """The main checkout of this repo (Paul's ~/Documents/seo-ops). In a client worktree (P2) ROOT is the worktree;
    git-ignored per-Mac files (.env, machine.json) live only in the main checkout."""
    try:
        r = _git("rev-parse", "--path-format=absolute", "--git-common-dir")
        if r.returncode == 0 and r.stdout.strip():
            return Path(r.stdout.strip()).parent
    except Exception:  # noqa: BLE001
        pass
    return ROOT


def require_client_folder(slug="<slug>"):
    """§00: client work runs only in the client's own folder (a worktree). The main folder is for system sessions.
    config client_work_in_main_folder is the test sandbox's switch only; the real config never sets it."""
    if config().get("client_work_in_main_folder") or ROOT.resolve() != main_root().resolve():
        return
    die(f"REFUSED — Client work runs in the client's folder: `python3 scripts/worktree.py open {slug}`. "
        f"This is the main folder ({ROOT}); it is for system sessions only. Open the client's folder, start a chat "
        f"there, and run the command there.", 4)


def git_branch():
    r = _git("rev-parse", "--abbrev-ref", "HEAD")
    return r.stdout.strip() if r.returncode == 0 else ""


def system_session():
    import changereq
    return changereq.system_session()


def _sync_main(out):
    """P2: bring this branch up to origin/main and push it there as a fast-forward; one retry on a race. A real
    conflict stops with a plain message. Never forces."""
    if not config().get("git_push_after_run"):
        return
    if _git("remote", "get-url", "origin").returncode != 0:
        out.append("no remote — the commit is safe locally")
        return
    for attempt in (1, 2):
        pr = _git("pull", "--rebase", "--autostash", "-q", "origin", "main")
        if pr.returncode != 0:
            _git("rebase", "--abort")
            out.append("NOT PUSHED — this client's commit conflicts with newer work on main. Nothing was lost: the "
                       "commit is safe here. Tell Paul; a system session resolves it (never force). "
                       + redact((pr.stderr or pr.stdout).strip()[:300]))
            return
        ps = _git("push", "-q", "origin", "HEAD:main")
        if ps.returncode == 0:
            out.append("pushed" + (" (after one retry)" if attempt == 2 else ""))
            return
    out.append("push failed twice (commit is safe locally): " + redact(ps.stderr.strip()[:300]))


def git_commit(message, slug=None, paths=None):
    """Commit and push. Never fails the run.
    P2: with a slug, only clients/<slug>/ is staged and committed — never another client's files (`git add -A` is
    gone). paths: the exact files a script changed (global approvals). Neither: a system commit, allowed only in a
    system session (P3). After the commit the branch is rebased on origin/main and pushed to main (one retry)."""
    out = []
    try:
        if slug:
            spec = [f"clients/{slug}/"]
        elif paths:
            spec = list(paths)
        elif system_session():
            spec = ["."]
        else:
            return "NOT COMMITTED — a commit outside one client's folder happens only in a system session (P3)."
        _git("add", "-A", "--", *spec)
        r = _git("commit", "-q", "-m", message, "--", *spec)
        if r.returncode != 0 and not re.search(r"nothing|no changes", r.stdout + r.stderr):
            out.append("git commit failed: " + redact(r.stderr.strip()))
        elif r.returncode == 0:
            out.append("committed: " + message.splitlines()[0])
        _sync_main(out)
    except Exception as e:  # noqa: BLE001
        out.append(f"git step failed: {e}")
    return "; ".join(out)
