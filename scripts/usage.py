#!/usr/bin/env python3
"""usage.py — what a run (or a client) cost in model tokens, measured from Claude Code's own transcripts.

    usage.py run <slug> <RUN_ID> [--by-agent] [--json]   tokens and USD for one run, per model (and per agent)
    usage.py client <slug> [--by-agent] [--json]         every run of a client, per stage and per step, the ten dearest
                                                         runs (and the cost by agent)
    usage.py baseline <slug> [<slug> …] [--write FILE]   the REWRITE-4-BASELINE.md tables (cost per stage, by agent,
                                                         top 10 runs)

The safety log records each run's start, end and session id. Claude Code keeps every session's token usage in
~/.claude/projects/<project>/<session>.jsonl and its subagents' in <session>/subagents/*.jsonl. A run's usage is
every assistant message in that session (and its subagents) between the run's start and finish. Each API message is
counted once (a message is repeated in the transcript while it streams). Prices: scripts/model_prices.json.
By agent (Rewrite 4 Phase 4): the session's own transcript is "main" (the stage chat); each subagent transcript is
named by the agentType in its <agent-…>.meta.json ("subagent" when the file says nothing).
Read-only; no network. A run with no session id, or whose transcript is gone, is reported as "no data", never as $0.
Set SEO_OPS_CLAUDE_PROJECTS to read another transcripts folder (the tests do).
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

from lib import ROOT, client_dir, die, read_json

PRICES = ROOT / "scripts" / "model_prices.json"
FIELDS = ("input", "cache_write_5m", "cache_write_1h", "cache_read", "output")
RUN_LINE = re.compile(r"^## RUN (\S+) · (STARTED|FINISHED|ABORTED) · (?:/(\S+) · )?(\S+)\s*$")
SESSION = re.compile(r"session ([\w-]+)")


def projects_dir():
    return Path(os.environ.get("SEO_OPS_CLAUDE_PROJECTS") or Path.home() / ".claude" / "projects")


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def prices():
    return (read_json(PRICES, {}) or {}).get("models", {})


def price_for(model):
    """The price row for a model id (date suffix ignored, longest listed prefix wins), or None."""
    m = re.sub(r"-\d{8}$", "", model or "")
    best = None
    for k, v in prices().items():
        if m == k or m.startswith(k + "-") or m.startswith(k):
            if best is None or len(k) > len(best[0]):
                best = (k, v)
    return best[1] if best else None


def cost(model, t):
    p = price_for(model)
    if not p:
        return 0.0
    return sum(t.get(f, 0) * p[f if f != "input" else "input"] for f in FIELDS) / 1e6


def run_log(slug):
    """{run_id: {command, step, session, start, end, state}} from the client's safety log."""
    out = {}
    cur = None
    p = client_dir(slug) / "log.md"
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        m = RUN_LINE.match(line)
        if m:
            rid, state, cmd, when = m.groups()
            r = out.setdefault(rid, {"id": rid, "command": None, "step": None, "session": None, "start": None,
                                     "end": None, "state": None})
            r["state"] = state
            if state == "STARTED":
                r["command"], r["start"], cur = cmd, when, r
            else:
                r["end"], cur = when, None
            continue
        if cur and line.startswith("Step: "):
            cur["step"] = line[6:].split(" · ")[0].strip()
            s = SESSION.search(line)
            cur["session"] = s.group(1) if s else None
    return out


def transcripts(sid):
    """Every transcript file of one session: the session's own and its subagents'."""
    found = []
    for proj in projects_dir().glob("*"):
        f = proj / f"{sid}.jsonl"
        if f.is_file():
            found.append(f)
            found += sorted((proj / sid / "subagents").glob("*.jsonl"))
    return found


def agent_of(f):
    """'main' for a session's own transcript, else the subagent's agentType from its .meta.json."""
    if f.parent.name != "subagents":
        return "main"
    meta = read_json(f.with_name(f.stem + ".meta.json"), {}) or {}
    return meta.get("agentType") or "subagent"


def read_usage(files, start, end, by_agent=False):
    """{model: {field: tokens}} for the API messages stamped between start and end (UTC datetimes);
    with by_agent, {agent: ({model: {field: tokens}}, transcripts with a message in the window)}."""
    msgs = {}
    for f in files:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except ValueError:
                continue
            m = o.get("message")
            if not isinstance(m, dict) or not m.get("usage") or not o.get("timestamp"):
                continue
            when = ts(o["timestamp"])
            if (start and when < start) or (end and when > end):
                continue
            msgs[(f.name, m.get("id") or o.get("uuid") or line[:80])] = (agent_of(f), m.get("model") or "?", m["usage"])
    if by_agent:
        split, seen = {}, {}
        for (fname, _), (agent, model, u) in msgs.items():
            split.setdefault(agent, []).append((model, u))
            seen.setdefault(agent, set()).add(fname)
        return {a: (tally(v), len(seen[a])) for a, v in split.items()}
    return tally((model, u) for _, model, u in msgs.values())


def tally(msgs):
    """{model: {field: tokens}} from (model, usage) pairs."""
    out = {}
    for model, u in msgs:
        if model == "<synthetic>":
            continue
        cc = u.get("cache_creation") or {}
        w1h = int(cc.get("ephemeral_1h_input_tokens") or 0)
        w5m = int(cc.get("ephemeral_5m_input_tokens") or 0)
        if not cc:
            w5m = int(u.get("cache_creation_input_tokens") or 0)
        t = out.setdefault(model, dict.fromkeys(FIELDS, 0))
        t["input"] += int(u.get("input_tokens") or 0)
        t["output"] += int(u.get("output_tokens") or 0)
        t["cache_read"] += int(u.get("cache_read_input_tokens") or 0)
        t["cache_write_5m"] += w5m
        t["cache_write_1h"] += w1h
    return out


def summarise(by_model):
    rows = {m: {**t, "usd": round(cost(m, t), 4), "priced": price_for(m) is not None} for m, t in by_model.items()}
    tot = {f: sum(r[f] for r in rows.values()) for f in FIELDS}
    return {"by_model": rows, "tokens": sum(tot.values()), "usd": round(sum(r["usd"] for r in rows.values()), 4),
            "unpriced": sorted(m for m, r in rows.items() if not r["priced"]), **{"total_" + f: v for f, v in tot.items()}}


def run_usage(slug, run_id, end_now=False):
    """The measured usage of one run, or None when there is no session id or no transcript for it."""
    r = run_log(slug).get(run_id)
    if not r or not r["session"] or not r["start"]:
        return None
    files = transcripts(r["session"])
    if not files:
        return None
    end = ts(dt.datetime.now(dt.timezone.utc).isoformat()) if (end_now or not r["end"]) else ts(r["end"])
    split = {a: v for a, v in read_usage(files, ts(r["start"]), end, by_agent=True).items() if v[0]}
    if not split:
        return None
    by = {}
    for per_model, _ in split.values():
        for m, t in per_model.items():
            acc = by.setdefault(m, dict.fromkeys(FIELDS, 0))
            for f in FIELDS:
                acc[f] += t[f]
    agents = {a: {**summarise(t), "transcripts": n} for a, (t, n) in split.items()}
    return {**summarise(by), "by_agent": agents, "run": run_id, "step": r["step"], "command": r["command"]}


def fmt_run(u, by_agent=False):
    lines = [f"run {u['run']} · {u.get('step') or '?'}: {u['tokens']:,} tokens · ${u['usd']:.2f}"]
    for m, r in sorted(u["by_model"].items(), key=lambda kv: -kv[1]["usd"]):
        lines.append(f"  {m}: in {r['input']:,} · cache-write {r['cache_write_5m'] + r['cache_write_1h']:,} · "
                     f"cache-read {r['cache_read']:,} · out {r['output']:,} · ${r['usd']:.2f}"
                     + ("" if r["priced"] else "  (UNPRICED model — add it to model_prices.json)"))
    if by_agent:
        lines.append("by agent (main = the stage chat):")
        for a, r in sorted(u["by_agent"].items(), key=lambda kv: -kv[1]["usd"]):
            lines.append(f"  {a}: {r['transcripts']} transcript(s) · {r['tokens']:,} tokens · ${r['usd']:.2f} · "
                         + ", ".join(f"{m} ${x['usd']:.2f}" for m, x in sorted(r["by_model"].items(), key=lambda kv: -kv[1]["usd"])))
    return "\n".join(lines)


def agent_totals(rows):
    """{agent: {runs, transcripts, tokens, usd, by_model: {model: usd}}} over a client's measured runs."""
    out = {}
    for row in rows:
        for a, r in ((row["usage"] or {}).get("by_agent") or {}).items():
            t = out.setdefault(a, {"runs": 0, "transcripts": 0, "tokens": 0, "usd": 0.0, "by_model": {}})
            t["runs"] += 1; t["transcripts"] += r["transcripts"]; t["tokens"] += r["tokens"]; t["usd"] += r["usd"]
            for m, x in r["by_model"].items():
                t["by_model"][m] = t["by_model"].get(m, 0.0) + x["usd"]
    return out


def agent_table(agents):
    lines = ["| Agent | Runs | Transcripts | Tokens | USD | Models |", "|---|---|---|---|---|---|"]
    for a, t in sorted(agents.items(), key=lambda kv: -kv[1]["usd"]):
        lines.append(f"| {a} | {t['runs']} | {t['transcripts']} | {t['tokens']:,} | ${t['usd']:.2f} | "
                     + ", ".join(f"{m} ${v:.2f}" for m, v in sorted(t["by_model"].items(), key=lambda kv: -kv[1])) + " |")
    return lines


def client_usage(slug):
    """[{run, step, stage, usage|None}] for every run in the log, and the per-stage and per-step totals."""
    import stages
    rows = []
    for rid, r in run_log(slug).items():
        if r["state"] == "STARTED" and not r["end"]:
            pass
        u = run_usage(slug, rid)
        st = stages.stage_of(r["step"] or "") if r["step"] else None
        rows.append({"run": rid, "step": r["step"], "command": r["command"],
                     "stage": (f"{st['id']}" if st else "any"), "usage": u})
    by_stage, by_step = {}, {}
    for row in rows:
        u = row["usage"]
        for key, d in ((row["stage"], by_stage), (row["step"] or "?", by_step)):
            t = d.setdefault(key, {"runs": 0, "measured": 0, "tokens": 0, "usd": 0.0})
            t["runs"] += 1
            if u:
                t["measured"] += 1; t["tokens"] += u["tokens"]; t["usd"] += u["usd"]
    return rows, by_stage, by_step


def baseline_md(slugs):
    """REWRITE-4-BASELINE.md, rendered from the measured runs — the figure every later phase is judged against."""
    out = ["# REWRITE-4 baseline — what the current route costs", "",
           f"_Generated {dt.date.today()} by `python3 scripts/usage.py baseline {' '.join(slugs)}` from Claude Code's "
           "transcripts, priced with `scripts/model_prices.json` (cache-write prices inferred). Do not edit by hand — "
           "regenerate. A run with no session id or no transcript on this Mac is counted as a run but has no cost "
           "(unmeasured); the totals are therefore a floor._", ""]
    grand = 0.0
    for slug in slugs:
        rows, by_stage, by_step = client_usage(slug)
        tot = sum(t["usd"] for t in by_stage.values())
        grand += tot
        out += [f"## {slug}", "",
                f"**${tot:.2f}** measured over {sum(t['measured'] for t in by_stage.values())} of {len(rows)} run(s); "
                f"{sum(t['tokens'] for t in by_stage.values()):,} tokens (input + cache write + cache read + output).", "",
                "### Cost per stage", "", "| Stage | Runs measured | Tokens | USD |", "|---|---|---|---|"]
        out += [f"| {k} | {t['measured']} of {t['runs']} | {t['tokens']:,} | ${t['usd']:.2f} |"
                for k, t in sorted(by_stage.items(), key=lambda kv: -kv[1]["usd"])]
        out += ["", "### Cost per step", "", "| Step | Runs measured | Tokens | USD |", "|---|---|---|---|"]
        out += [f"| {k} | {t['measured']} of {t['runs']} | {t['tokens']:,} | ${t['usd']:.2f} |"
                for k, t in sorted(by_step.items(), key=lambda kv: -kv[1]["usd"])]
        out += ["", "### Cost by agent", "",
                "_main = the stage chat itself; every other row is a subagent, named by its agent type._", ""]
        out += agent_table(agent_totals(rows))
        out += ["", "### Ten dearest runs", "", "| Run | Step | Tokens | USD | Models |", "|---|---|---|---|---|"]
        for r in sorted((r for r in rows if r["usage"]), key=lambda r: -r["usage"]["usd"])[:10]:
            u = r["usage"]
            out.append(f"| {r['run']} | {r['step']} | {u['tokens']:,} | ${u['usd']:.2f} | "
                       + ", ".join(f"{m} ${x['usd']:.2f}" for m, x in sorted(u["by_model"].items(), key=lambda kv: -kv[1]["usd"])) + " |")
        un = [r["run"] for r in rows if not r["usage"]]
        out += ["", f"Unmeasured runs ({len(un)}): " + (", ".join(un) if un else "none"), ""]
    out += ["---", f"**All clients: ${grand:.2f}**", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("run"); s.add_argument("slug"); s.add_argument("run_id"); s.add_argument("--json", action="store_true")
    s.add_argument("--by-agent", action="store_true", help="split the cost by the main chat and each subagent type")
    s = sub.add_parser("client"); s.add_argument("slug"); s.add_argument("--json", action="store_true")
    s.add_argument("--by-agent", action="store_true", help="add the cost by agent across the client's runs")
    s = sub.add_parser("baseline"); s.add_argument("slugs", nargs="+"); s.add_argument("--write")
    a = ap.parse_args()
    if a.cmd == "baseline":
        text = baseline_md(a.slugs)
        if a.write:
            Path(a.write).write_text(text, encoding="utf-8")
            print(f"wrote {a.write}")
        else:
            print(text)
        return
    if a.cmd == "run":
        u = run_usage(a.slug, a.run_id)
        if not u:
            print(f"no data for run {a.run_id}: it has no session id in the log, or that session's transcript is not on this Mac")
            sys.exit(1)
        if a.json and not a.by_agent:
            u = {k: v for k, v in u.items() if k != "by_agent"}
        print(json.dumps(u, indent=2) if a.json else fmt_run(u, a.by_agent))
        return
    rows, by_stage, by_step = client_usage(a.slug)
    if a.json:
        print(json.dumps({"runs": rows, "by_stage": by_stage, "by_step": by_step,
                          **({"by_agent": agent_totals(rows)} if a.by_agent else {})}, indent=2)); return
    tot = sum(t["usd"] for t in by_stage.values())
    print(f"{a.slug}: ${tot:.2f} measured over {sum(t['measured'] for t in by_stage.values())} of {len(rows)} run(s)\n")
    print("by stage:")
    for k, t in sorted(by_stage.items(), key=lambda kv: -kv[1]["usd"]):
        print(f"  {k:12} {t['measured']}/{t['runs']} runs · {t['tokens']:,} tokens · ${t['usd']:.2f}")
    print("\ndearest runs:")
    for row in sorted((r for r in rows if r["usage"]), key=lambda r: -r["usage"]["usd"])[:10]:
        print(f"  ${row['usage']['usd']:7.2f}  {row['usage']['tokens']:>12,}  {row['run']}  ({row['step']})")
    if a.by_agent:
        print("\nby agent (main = the stage chat):")
        for ag, t in sorted(agent_totals(rows).items(), key=lambda kv: -kv[1]["usd"]):
            print(f"  {ag:16} {t['runs']} runs · {t['transcripts']} transcript(s) · {t['tokens']:,} tokens · ${t['usd']:.2f}")


if __name__ == "__main__":
    main()
