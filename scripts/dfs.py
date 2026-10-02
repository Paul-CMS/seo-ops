#!/usr/bin/env python3
"""dfs.py — every DataforSEO call goes through here.

    dfs.py balance
    dfs.py estimate <endpoint> [--tasks N] [--items N]
    dfs.py call <slug> <endpoint> --payload file.json --purpose T [--estimate USD] [--confirmed]
    dfs.py free <endpoint> [--payload file.json] [--get]      result endpoints that cost nothing
    dfs.py ledger <slug>

Before any paid call: the estimate is compared with the live balance. If the estimate is
more than the remaining balance -> exit 6 (stop and tell Paul, do not start). If it is over
the confirmation threshold (config.json, $2) and --confirmed is absent -> exit 5 (ask Paul
first). Every paid call is logged with estimate and actual cost to
clients/<slug>/dfs-costs.jsonl and added to status.json spend.

Credentials come from .env (DFS_LOGIN, DFS_PASSWORD). They are never printed.
"""
import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request

from lib import ROOT, append, client_dir, config, die, load_env, now, redact

API = "https://api.dataforseo.com/v3/"
PRICES = json.loads((ROOT / "scripts" / "dfs_prices.json").read_text())


class DfsError(Exception):
    pass


def _auth():
    env = load_env()
    login, pw = env.get("DFS_LOGIN"), env.get("DFS_PASSWORD")
    if not login or not pw:
        die("DFS_LOGIN / DFS_PASSWORD are missing from .env. Paul types them in himself.")
    return "Basic " + base64.b64encode(f"{login}:{pw}".encode()).decode()


def request(endpoint, body=None, method=None, timeout=90, retries=3):
    url = API + endpoint.lstrip("/")
    data = json.dumps(body).encode() if body is not None else None
    method = method or ("POST" if data is not None else "GET")
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": _auth(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.loads(r.read().decode())
            if resp.get("status_code") not in (20000,):
                raise DfsError(f"{resp.get('status_code')} {resp.get('status_message')}")
            return resp
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (401, 402, 403, 404):
                break
        except (urllib.error.URLError, TimeoutError) as e:
            last = f"network: {e}"
        except DfsError as e:
            last = str(e)
            if not last.startswith(("50", "40202")):  # retry only server-side / rate errors
                break
        time.sleep(2 * (attempt + 1))
    raise DfsError(redact(f"{endpoint}: {last}"))


def task_result(resp, i=0):
    t = (resp.get("tasks") or [{}])[i]
    if t.get("status_code") not in (20000, 20100):
        raise DfsError(f"task {t.get('status_code')} {t.get('status_message')}")
    return t


def balance():
    r = request("appendix/user_data")
    return float(task_result(r)["result"][0]["money"]["balance"])


def estimate(endpoint, tasks=1, items=0, pages=0, mode="basic"):
    p = PRICES.get(endpoint, PRICES["default"])
    if "per_page" in p:
        return round(pages * p["per_page"][mode], 4)
    return round(tasks * p.get("per_task", 0) + items * p.get("per_item", 0), 4)


def spend_guard(est, confirmed):
    """Exit 6 if the estimate exceeds the balance, 5 if it needs Paul's confirmation."""
    bal = balance()
    thr = float(config()["dfs_confirm_threshold_usd"])
    if est > bal:
        print(f"STOP — estimated ${est:.4f} is more than the remaining DataforSEO balance "
              f"${bal:.2f}. Not starting. Tell Paul (he tops up the balance).")
        sys.exit(6)
    if est > thr and not confirmed:
        print(f"CONFIRM — estimated ${est:.4f} (over the ${thr:.2f} threshold). Balance ${bal:.2f}."
              " Ask Paul, then re-run with --confirmed.")
        sys.exit(5)
    return bal


def log_cost(slug, endpoint, purpose, est, actual, extra=None):
    import status as S
    rec = {"at": now(), "endpoint": endpoint, "purpose": purpose, "estimate_usd": est,
           "actual_usd": actual, **(extra or {})}
    append(client_dir(slug) / "dfs-costs.jsonl", json.dumps(rec) + "\n")
    st = S.load(slug)
    st["spend"]["dataforseo_usd"] = round(st["spend"].get("dataforseo_usd", 0) + float(actual or 0), 6)
    S.save(slug, st)


def paid_post(slug, endpoint, payload, purpose, est, confirmed=False, extra=None):
    spend_guard(est, confirmed)
    resp = request(endpoint, payload)
    actual = resp.get("cost")
    log_cost(slug, endpoint, purpose, est, actual, extra)
    return resp


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    s = sub.add_parser("estimate"); s.add_argument("endpoint")
    s.add_argument("--tasks", type=int, default=1); s.add_argument("--items", type=int, default=0)
    s = sub.add_parser("call"); s.add_argument("slug"); s.add_argument("endpoint")
    s.add_argument("--payload", required=True); s.add_argument("--purpose", required=True)
    s.add_argument("--estimate", type=float); s.add_argument("--confirmed", action="store_true")
    s.add_argument("--out")
    s = sub.add_parser("free"); s.add_argument("endpoint"); s.add_argument("--payload")
    s.add_argument("--get", action="store_true"); s.add_argument("--out")
    s = sub.add_parser("ledger"); s.add_argument("slug")
    a = ap.parse_args()

    try:
        if a.cmd == "balance":
            print(f"DataforSEO balance: ${balance():.2f}")
        elif a.cmd == "estimate":
            print(f"estimate ${estimate(a.endpoint, a.tasks, a.items):.4f}")
        elif a.cmd == "call":
            client_dir(a.slug)
            payload = json.loads(open(a.payload).read())
            if not isinstance(payload, list):
                payload = [payload]
            est = a.estimate if a.estimate is not None else estimate(a.endpoint, len(payload))
            resp = paid_post(a.slug, a.endpoint, payload, a.purpose, est, a.confirmed)
            text = json.dumps(resp, indent=1)
            if a.out:
                open(a.out, "w").write(text); print(f"saved {a.out} · cost ${resp.get('cost')}")
            else:
                print(text)
        elif a.cmd == "free":
            if a.endpoint in PRICES or "task_post" in a.endpoint or a.endpoint.endswith("/live"):
                die(f"{a.endpoint} is a paid endpoint. Use 'dfs.py call'.")
            body = json.loads(open(a.payload).read()) if a.payload else None
            resp = request(a.endpoint, None if a.get else body, "GET" if a.get else None)
            if resp.get("cost"):
                print(f"WARNING: this call cost ${resp['cost']} — it should have gone through 'call'.",
                      file=sys.stderr)
            text = json.dumps(resp, indent=1)
            if a.out:
                open(a.out, "w").write(text); print(f"saved {a.out}")
            else:
                print(text)
        elif a.cmd == "ledger":
            p = client_dir(a.slug) / "dfs-costs.jsonl"
            rows = [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []
            for r in rows:
                print(f"{r['at'][:16]}  ${float(r.get('actual_usd') or 0):8.4f}  (est ${r['estimate_usd']:.4f})"
                      f"  {r['endpoint']}  — {r['purpose']}")
            print(f"total ${sum(float(r.get('actual_usd') or 0) for r in rows):.4f} over {len(rows)} call(s)")
    except DfsError as e:
        die(f"DataforSEO error: {redact(e)}", 8)


if __name__ == "__main__":
    main()
