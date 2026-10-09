#!/usr/bin/env python3
"""questions.py — every question shown to Paul has a kind and a searched: line (rewrite 2 P6, Q5).

    questions.py check <questions.json>      exit 1 and list every problem; 0 when the set may go to Paul

A question set is a JSON list of {"text", "kind", "searched", "best_answer"?, "key"|"fact_id"?}.
  kind "public" — about a place, a code, the trade or a manufacturer. NEVER asked: the researcher agent looks it up in
                  official sources (methodology/sources/<state>-<area>.md first) and cites them, or records "not found"
                  with the sources tried. Paul sees only a not-found item, as a decision: drop the element, or keep it
                  general. A public question in a set for Paul is refused.
  kind "client" — something only the client can know. Asked only after the client-fact search order:
                  facts.json → decisions-settled.md → reviews → the live site text → GBP data → the proof sheet and the
                  Discovery Record. `searched` lists what was searched; `best_answer` pre-fills what was found, so most
                  questions are a yes / no.
Used by evidence.py (the facts pack) and by the audit's Gate B question writer. Run settled.py filter first (P4).
"""
import json
import sys

SEARCH_ORDER = ["facts.json", "decisions-settled.md", "reviews", "site text", "GBP data", "proof sheet / Discovery Record"]


def problems(qs):
    out = []
    for i, q in enumerate(qs, 1):
        what = (q.get("text") or "")[:70]
        k = q.get("kind")
        if k not in ("public", "client"):
            out.append(f"Q{i} ({what}): no kind — label it public (looked up, never asked) or client")
        elif k == "public":
            out.append(f"Q{i} ({what}): a public fact is never asked — the researcher looks it up "
                       "(Paul sees it only if it is not found, as drop-or-keep-general)")
        elif not q.get("searched"):
            out.append(f"Q{i} ({what}): a client question needs its searched: line ({' → '.join(SEARCH_ORDER)})")
    return out


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        sys.exit(__doc__)
    bad = problems(json.loads(open(sys.argv[2]).read()))
    print("\n".join(bad) or "every question has a kind and a searched: line")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
