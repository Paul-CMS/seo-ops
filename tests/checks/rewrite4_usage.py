"""Rewrite 4 Phase 0: usage.py measures a run's tokens and dollars from Claude Code's transcripts; run.py finish fills
--tokens/--cost from it; STATUS.md shows cost per stage."""
import datetime as dt
import json
import re


def _msg(when, mid, model, **u):
    usage = {"input_tokens": u.get("i", 0), "output_tokens": u.get("o", 0), "cache_read_input_tokens": u.get("r", 0),
             "cache_creation_input_tokens": u.get("w", 0),
             "cache_creation": {"ephemeral_1h_input_tokens": u.get("w", 0), "ephemeral_5m_input_tokens": 0}}
    return json.dumps({"type": "assistant", "timestamp": when, "message": {"id": mid, "model": model, "usage": usage}})


def _z(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def t_usage_measured(h):
    SB = h.SB
    S = "use-co"
    h.sh(f'python3 scripts/status.py init {S} --name "Use Co" --domain use.example --type full --industry roofing')
    sid = "sess-0000-aaaa"
    t0 = dt.datetime.now(dt.timezone.utc).replace(microsecond=0) - dt.timedelta(hours=2)
    t1 = t0 + dt.timedelta(hours=1)
    log = SB / f"clients/{S}/log.md"
    log.write_text(log.read_text() + (
        f"\n## RUN 20261001-100000-build-aaaa · STARTED · /build · {t0.isoformat()}\nStep: build:write · session {sid}\n"
        f"## RUN 20261001-100000-build-aaaa · FINISHED · {t1.isoformat()}\nChanges: 0 · Summary: x\n"
        f"\n## RUN 20261001-120000-wp-check-bbbb · STARTED · /wp-check · {t1.isoformat()}\nStep: wp-check\n"
        f"## RUN 20261001-120000-wp-check-bbbb · FINISHED · {t1.isoformat()}\nChanges: 0 · Summary: y\n"))
    proj = SB / "fake-projects" / "p"
    (proj / sid / "subagents").mkdir(parents=True)
    inside, outside = t0 + dt.timedelta(minutes=5), t1 + dt.timedelta(minutes=5)
    (proj / f"{sid}.jsonl").write_text("\n".join([
        _msg(_z(inside), "m1", "claude-opus-5-5", i=1000, o=500, r=10000, w=2000),
        _msg(_z(inside), "m1", "claude-opus-5-5", i=1000, o=500, r=10000, w=2000),   # a streamed repeat: counted once
        _msg(_z(outside), "m2", "claude-opus-5-5", i=999999, o=999999),               # after the run: not counted
        "not json"]))
    (proj / sid / "subagents" / "agent-1.jsonl").write_text("\n".join([
        _msg(_z(inside), "s1", "claude-haiku-5-5-20260101", i=1_000_000, o=1_000_000),
        _msg(_z(inside), "s2", "claude-mystery-9", i=5)]))
    env = f"SEO_OPS_CLAUDE_PROJECTS={SB / 'fake-projects'}"
    code, out = h.sh(f"{env} python3 scripts/usage.py run {S} 20261001-100000-build-aaaa --json")
    u = json.loads(out) if code == 0 else {}
    opus = (u.get("by_model") or {}).get("claude-opus-5-5", {})
    # opus: (1000*4 + 500*20 + 10000*0.20 + 2000*8.00) / 1e6 = 0.032 ; haiku: (1e6*0.10 + 1e6*0.50) / 1e6 = 0.60
    h.check("usage: a run's tokens are counted once per API message, only inside the run, subagents included",
            opus.get("input") == 1000 and opus.get("output") == 500 and opus.get("cache_read") == 10000
            and opus.get("cache_write_1h") == 2000, out)
    h.check("usage: dollars come from model_prices.json (date-suffixed ids match; 1-hour cache writes priced)",
            abs(opus.get("usd", 0) - 0.032) < 1e-6 and abs(u["by_model"]["claude-haiku-5-5-20260101"]["usd"] - 0.6) < 1e-6
            and abs(u["usd"] - 0.632) < 1e-6, out)
    h.check("usage: a model with no price is flagged, never silently $0", u.get("unpriced") == ["claude-mystery-9"], out)
    code, out = h.sh(f"{env} python3 scripts/usage.py run {S} 20261001-120000-wp-check-bbbb")
    h.check("usage: a run with no session id is 'no data', not $0", code == 1 and "no data" in out, out)
    code, out = h.sh(f"{env} python3 scripts/usage.py client {S}")
    h.check("usage: client view totals the runs by stage", code == 0 and "build-plan" not in out and "batches" in out
            and "$0.63" in out, out)
    code, out = h.sh(f"{env} python3 scripts/usage.py baseline {S}")
    h.check("usage: the baseline file is rendered from the runs",
            code == 0 and "### Cost per stage" in out and "20261001-100000-build-aaaa" in out and "Unmeasured runs (1)" in out, out)


def t_usage_finish_fills(h):
    """run.py finish with no --tokens/--cost records the measured figures; STATUS.md shows spend by stage."""
    SB = h.SB
    S = "use-fin"
    h.sh(f'python3 scripts/status.py init {S} --name "Use Fin" --domain usefin.example --type full --industry roofing')
    h.new_session("claude-haiku-4-5")
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client")
    rid = out.splitlines()[-1]
    sid = re.search(r"session (\S+)", (SB / f"clients/{S}/log.md").read_text().split(rid)[1])
    sid = sid.group(1) if sid else None
    h.check("usage finish: the run's session id is in the log", bool(sid), out)
    proj = SB / "fake-projects" / "p"
    proj.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    (proj / f"{sid}.jsonl").write_text(_msg(_z(now), "f1", "claude-sonnet-5-5", i=1_000_000, o=100_000) + "\n")
    env = f"SEO_OPS_CLAUDE_PROJECTS={SB / 'fake-projects'}"
    code, out = h.sh(f'{env} python3 scripts/run.py finish {S} {rid} --summary "t"')
    st = h.status(S)
    spend = (st.get("model_spend") or [{}])[-1]
    # sonnet 5.5: 1e6 * 2.00 + 1e5 * 10.00 = 3.00
    h.check("usage finish: --tokens/--cost are filled from the transcripts and recorded per model",
            spend.get("measured") and spend.get("tokens") == 1_100_000 and abs(spend.get("usd", 0) - 3.0) < 1e-6
            and "claude-sonnet-5-5" in spend.get("by_model", {}), (out, spend))
    log = (SB / f"clients/{S}/log.md").read_text()
    h.check("usage finish: the log's Spend line says it was measured", "Spend: 1100000 tokens · $3.00 (measured)" in log, out)
    status_md = (SB / f"clients/{S}/STATUS.md").read_text()
    h.check("usage finish: STATUS.md shows spend by stage", "## Spend by stage (model)" in status_md and "$3.00" in status_md,
            status_md[-800:])
    h.new_session("claude-haiku-4-5")
    code, out = h.sh(f"python3 scripts/run.py start {S} new-client")
    rid2 = out.splitlines()[-1]
    code, out = h.sh(f'python3 scripts/run.py finish {S} {rid2} --summary "t" --tokens 5 --cost 0.01')
    spend = (h.status(S).get("model_spend") or [{}])[-1]
    h.check("usage finish: figures typed by hand still win and are not marked measured",
            spend.get("tokens") == 5 and not spend.get("measured"), (out, spend))


SCENARIOS = [t_usage_measured, t_usage_finish_fills]
