#!/usr/bin/env python3
"""seq.py — a multi-step command runs through here: one refusal or failure stops the sequence and is reported.

    seq.py <slug> --step "python3 scripts/status.py page-stage …" --step "python3 scripts/approve.py …" [--run RUN_ID]

Steps run in order, each without a shell. The first step that exits non-zero STOPS the sequence: no later step runs
(an approval step after a failure never runs), the refusal text is printed once with the steps done and the steps not
run, and the failure is recorded in status.json (`sequence_failure`) and log.md. While it stands approve.py refuses
every approval for the client — it clears when a sequence completes, or when the run finishes or is aborted.
Exit code: the failing step's (at least 1); 0 when every step succeeded.
HMM 20261014-144852-build-6004: three of four re-records were refused and the sequence went on to the approval.
"""
import argparse
import shlex
import subprocess
import sys

import status as S
from lib import ROOT, append, client_dir, now, require_client_folder


def run_steps(slug, steps, run_id=None):
    """Returns (ok, report lines). Records or clears the standing failure."""
    done, report = [], []
    for n, cmd in enumerate(steps, 1):
        argv = shlex.split(cmd)
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            done.append(cmd)
            report.append(f"[{n}/{len(steps)}] done: {cmd[:110]}")
            continue
        why = " ".join(out.splitlines()[-3:])[:300] or f"exit {r.returncode}"
        skipped = steps[n:]
        st = S.load(slug)
        st["sequence_failure"] = {"at": now(), "run": run_id, "step": n, "of": len(steps), "cmd": cmd[:200], "code": r.returncode,
                                  "why": why, "not_run": [c[:120] for c in skipped]}
        S.save(slug, st)
        append(client_dir(slug) / "log.md", f"- SEQUENCE STOPPED {now()[:16]} · step {n} of {len(steps)} failed (exit {r.returncode}): "
               f"{cmd[:140]} · {why[:200]} · not run: {len(skipped)}\n")
        report.append(f"[{n}/{len(steps)}] FAILED (exit {r.returncode}): {cmd[:110]}")
        report += ["    " + ln for ln in out.splitlines()[-10:]]
        report.append(f"STOPPED at step {n} of {len(steps)}. NOT RUN: {len(skipped)} step(s)"
                      + "".join(f"\n    - {c[:110]}" for c in skipped))
        report.append("Report this refusal as it is; do not work around it, and do not approve anything until it is resolved.")
        return False, report, r.returncode
    st = S.load(slug)
    if st.pop("sequence_failure", None) is not None:
        S.save(slug, st)
    report.append(f"all {len(steps)} step(s) done")
    return True, report, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--step", action="append", required=True)
    ap.add_argument("--run")
    a = ap.parse_args()
    require_client_folder(a.slug)
    ok, report, code = run_steps(a.slug, a.step, a.run)
    print("\n".join(report))
    sys.exit(0 if ok else (code or 1))


if __name__ == "__main__":
    main()
