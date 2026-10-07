#!/usr/bin/env python3
"""dfs.py — every DataforSEO call goes through here.

    dfs.py balance
    dfs.py estimate <endpoint> [--tasks N] [--items N]
    dfs.py call <slug> <endpoint> --payload file.json --purpose T [--estimate USD] [--confirmed]
    dfs.py free <endpoint> [--payload file.json] [--get]      result endpoints that cost nothing
    dfs.py ledger <slug>

Costs are checked per RUN, not just per call: scripts that make several calls (paa.py,
rankings.py) call run_guard() with the whole run's estimate before the first call, and every
paid call also counts what this run has already spent. Before any paid call: the estimate is compared with the live balance. If the estimate is
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


_BAL = {"at": 0.0, "value": None}


def balance():
    """Account balance. DataforSEO allows 6 user_data calls a minute, so the value is reused for 60 s
    (spend is still checked per call against it) and a rate-limit answer (40202) is waited out."""
    import time as _t
    if _BAL["value"] is not None and _t.time() - _BAL["at"] < 60:
        return _BAL["value"]
    for attempt in range(5):
        try:
            r = request("appendix/user_data")
            _BAL.update(at=_t.time(), value=float(task_result(r)["result"][0]["money"]["balance"]))
            return _BAL["value"]
        except DfsError as e:
            if "40202" not in str(e) or attempt == 4:
                raise
            _t.sleep(15)


def price(endpoint):
    """(price entry, confirmed?). Unknown endpoints are unconfirmed."""
    p = PRICES.get(endpoint)
    if not isinstance(p, dict):
        return {}, False
    return p, bool(p.get("confirmed"))


def estimate(endpoint, tasks=1, items=0, pages=0, mode="basic", depth=None):
    """Upper-bound estimate. items = expected rows returned (Labs, Backlinks).
    depth = results requested per task (SERP: billed per 10 organic / 100 maps; reviews per 10)."""
    p, _ = price(endpoint)
    if not p:
        return None
    if "per_page" in p:
        return round(pages * p["per_page"][mode], 4)
    if "per_unit" in p:
        units = max(1, -(-(depth or p["unit_results"]) // p["unit_results"]))
        return round(tasks * (units * p["per_unit"] + p.get("per_task_extra_place_id", 0)), 4)
    return round(tasks * p.get("per_task", 0) + items * p.get("per_item", 0), 4)


def current_run(slug):
    import run as R
    left = R.unfinished(slug)
    return left[-1] if left else None


def run_spent(slug, run_id):
    p = client_dir(slug) / "dfs-costs.jsonl"
    if not run_id or not p.exists():
        return 0.0
    return sum(float(json.loads(l).get("actual_usd") or 0) for l in p.read_text().splitlines()
               if l.strip() and json.loads(l).get("run_id") == run_id)


def run_guard(slug, total_est, confirmed, what="this run"):
    """Whole-run check before the first call: the total estimate plus what this run already spent
    against the balance (exit 6) and the $2 threshold (exit 5 unless Paul confirmed the total)."""
    rid = current_run(slug)
    spent = run_spent(slug, rid)
    bal = balance()
    thr = float(config()["dfs_confirm_threshold_usd"])
    if total_est + spent > bal:
        print(f"STOP — {what} would cost about ${total_est:.4f} (plus ${spent:.4f} already spent in this run); "
              f"the DataforSEO balance is ${bal:.2f}. Not starting. Tell Paul (he tops up the balance).")
        sys.exit(6)
    if not confirmed and total_est + spent > thr:
        print(f"CONFIRM — {what} is estimated at ${total_est:.4f} (run total ${total_est + spent:.4f}, over the "
              f"${thr:.2f} threshold). Balance ${bal:.2f}. Ask Paul, then re-run with --confirmed.")
        sys.exit(5)
    return bal


def spend_guard(est, confirmed, endpoint=None, slug=None):
    """Exit 6 if the estimate (plus this run's spend so far) exceeds the balance; 5 if Paul must
    confirm first (run total over the threshold, or the endpoint's price is not confirmed)."""
    bal = balance()
    thr = float(config()["dfs_confirm_threshold_usd"])
    _, price_ok = price(endpoint) if endpoint else ({}, True)
    if est is None:
        print(f"CONFIRM — no price on file for {endpoint}. Ask Paul, then re-run with --confirmed "
              "and --estimate <USD>.")
        sys.exit(5)
    spent = run_spent(slug, current_run(slug)) if slug else 0.0
    if est > bal:
        print(f"STOP — estimated ${est:.4f} is more than the remaining DataforSEO balance "
              f"${bal:.2f}. Not starting. Tell Paul (he tops up the balance).")
        sys.exit(6)
    if not confirmed and (est + spent > thr or not price_ok):
        why = (f"run total ${est + spent:.4f} is over the ${thr:.2f} threshold" if est + spent > thr
               else "this endpoint's price is not confirmed yet")
        print(f"CONFIRM — estimated ${est:.4f} ({why}). Balance ${bal:.2f}. Ask Paul, then re-run with --confirmed.")
        sys.exit(5)
    return bal


def log_cost(slug, endpoint, purpose, est, actual, extra=None):
    import status as S
    rec = {"at": now(), "run_id": current_run(slug), "endpoint": endpoint, "purpose": purpose,
           "estimate_usd": est, "actual_usd": actual, **(extra or {})}
    append(client_dir(slug) / "dfs-costs.jsonl", json.dumps(rec) + "\n")
    st = S.load(slug)
    st["spend"]["dataforseo_usd"] = round(st["spend"].get("dataforseo_usd", 0) + float(actual or 0), 6)
    S.save(slug, st)


def paid_post(slug, endpoint, payload, purpose, est, confirmed=False, extra=None, timeout=90, retries=3):
    """retries=1 for slow paid endpoints (LLM responses): a retry after a timeout can bill twice."""
    spend_guard(est, confirmed, endpoint, slug)
    resp = request(endpoint, payload, timeout=timeout, retries=retries)
    actual = resp.get("cost")
    log_cost(slug, endpoint, purpose, est, actual, extra)
    return resp


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    s = sub.add_parser("estimate"); s.add_argument("endpoint")
    s.add_argument("--tasks", type=int, default=1); s.add_argument("--items", type=int, default=0)
    s.add_argument("--depth", type=int)
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
            e = estimate(a.endpoint, a.tasks, a.items, depth=a.depth)
            _, ok = price(a.endpoint)
            print("no price on file — Paul must confirm" if e is None else
                  f"estimate ${e:.4f}" + ("" if ok else " (price NOT confirmed — Paul must confirm each call)"))
        elif a.cmd == "call":
            client_dir(a.slug)
            payload = json.loads(open(a.payload).read())
            if not isinstance(payload, list):
                payload = [payload]
            est = a.estimate if a.estimate is not None else estimate(
                a.endpoint, len(payload), sum(int(t.get("limit", 100)) for t in payload),
                depth=max([int(t.get("depth", 0)) for t in payload] + [0]) or None)
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
            flags = 0
            for r in rows:
                act, est = float(r.get("actual_usd") or 0), r.get("estimate_usd")
                off = est is not None and abs(act - est) > max(0.005, 0.25 * est)
                flags += off
                print(f"{r['at'][:16]}  ${act:8.4f}  (est ${est if est is not None else 0:.4f})"
                      f"{'  <-- DIFFERS from price table' if off else ''}  {r['endpoint']}  — {r['purpose']}")
            print(f"total ${sum(float(r.get('actual_usd') or 0) for r in rows):.4f} over {len(rows)} call(s)")
            if flags:
                print(f"{flags} call(s) cost differently from scripts/dfs_prices.json — check the table.")
    except DfsError as e:
        die(f"DataforSEO error: {redact(e)}", 8)


if __name__ == "__main__":
    main()
