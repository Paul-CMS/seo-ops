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


_ENV_CACHE = None


def load_env():
    """Parse ROOT/.env. Values are returned, never printed."""
    global _ENV_CACHE
    if _ENV_CACHE is not None:
        return _ENV_CACHE
    env = {}
    p = ROOT / ".env"
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


def git_commit(message):
    """Commit everything git is allowed to see. Push if configured. Never fails the run."""
    out = []
    try:
        subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True,
                       capture_output=True, text=True)
        r = subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-m", message],
                           capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
            out.append("git commit failed: " + redact(r.stderr.strip()))
        elif r.returncode == 0:
            out.append("committed: " + message.splitlines()[0])
        if config().get("git_push_after_run"):
            p = subprocess.run(["git", "-C", str(ROOT), "push", "-q"],
                               capture_output=True, text=True)
            out.append("pushed" if p.returncode == 0
                       else "push failed (commit is safe locally): " + redact(p.stderr.strip()))
    except Exception as e:  # noqa: BLE001
        out.append(f"git step failed: {e}")
    return "; ".join(out)
