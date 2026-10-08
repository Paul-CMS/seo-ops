"""Extra scenario modules for tests/run_all.py.

Each module here defines SCENARIOS = [fn, ...]; each fn(h) takes the harness namespace h with:
h.SB (sandbox Path), h.sh(cmd) -> (code, out), h.check(name, cond, detail=""), h.status(slug) -> dict,
h.Agent(slug) (start/fin/step/mark/w helpers), h.paul(line), h.new_session().
Modules are loaded in name order after the built-in scenarios.
"""
