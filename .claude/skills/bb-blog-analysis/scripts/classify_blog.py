#!/usr/bin/env python3
"""
classify_blog.py — mechanical pass of the blog three-way sort.

    python3 classify_blog.py <config.yaml> <out_dir>

Does the joins and the arithmetic. It does NOT make the final call: Test B's mandatory
criterion is a judgment about whether a post answers a question no commercial page covers,
and that is the analyst's, not a script's.

Output: blog-decision-map.csv with every post carrying a proposed classification, the
signals behind it, and a confidence flag. Every row needs analyst review before it goes to
Paul; rows marked NEEDS-JUDGMENT cannot be resolved mechanically at all.

Inputs (config.yaml):
  blog_posts:        url, title, word_count, published, modified, category
  commercial_pages:  url, type (service|location), entity, city
  gsc:               url, impressions, clicks, position   (optional)
  analytics:         url, conversions, entrances          (optional)
  backlinks:         url, referring_domains               (optional)
"""

import csv, os, re, sys
from difflib import SequenceMatcher

try:
    import yaml
except ImportError:
    yaml = None

STOP = {"the", "a", "an", "in", "for", "of", "to", "and", "or", "your", "you", "with",
        "how", "what", "why", "when", "is", "are", "do", "does", "can", "should", "on",
        "at", "from", "by", "it", "this", "that", "best", "top", "guide", "tips"}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", str(s or "").lower())


def canon(w):
    """Strip a single trailing 's'. Applied to both sides, this matches
    headache/headaches and migraine/migraines without over-stripping.

    An earlier version expanded each word into every plural form. That inflated one
    shared word into three shared tokens and defeated the two-token duplicate
    threshold, pairing unrelated posts.
    """
    return w[:-1] if w.endswith("s") and len(w) > 3 else w


def tokens(s):
    return {canon(w) for w in norm(s).split()
            if w and w not in STOP and len(w) > 2}


def sim(a, b):
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def load(path):
    raw = open(path, encoding="utf-8").read()
    if path.endswith(".json"):
        import json
        return json.loads(raw)
    if not yaml:
        sys.exit("install pyyaml or pass .json")
    return yaml.safe_load(raw)


def index(rows, key="url"):
    return {r[key]: r for r in (rows or [])}


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cfg = load(sys.argv[1])
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    posts = cfg.get("blog_posts", [])
    commercial = cfg.get("commercial_pages", [])
    gsc = index(cfg.get("gsc"))
    ga = index(cfg.get("analytics"))
    bl = index(cfg.get("backlinks"))

    have_gsc = bool(gsc)
    have_ga = bool(ga)

    # ---- Test A: entity + location overlap with a commercial page
    def test_a(p):
        """Return ranked candidates, not a winner.

        Picking one target mechanically produced wrong redirect destinations in
        testing: a location page matches any post naming the city, and the homepage
        matches almost everything. The analyst chooses; the script ranks.
        """
        t = tokens(p["title"])
        out = []
        for c in commercial:
            ent = tokens(c.get("entity", ""))
            city = tokens(c.get("city", ""))
            both = ent | city
            if not both:
                continue
            overlap = len(t & both) / max(len(both), 1)
            if overlap == 0:
                continue
            ent_hit = bool(ent & t)
            city_hit = bool(city & t)
            score = overlap
            if ent_hit and city_hit:
                score += 0.4
            if c.get("type") == "homepage":
                score -= 0.5          # matches brand+city on nearly any local post
            out.append((round(max(score, 0.0), 2), c, ent_hit, city_hit))
        out.sort(key=lambda x: -x[0])
        return out[:3]

    # ---- distinctiveness: a token in most titles carries no dedupe signal
    from collections import Counter as _C
    _df = _C()
    for _p in posts:
        for _t in tokens(_p["title"]):
            _df[_t] += 1
    _common = {t for t, n in _df.items() if len(posts) and n / len(posts) > 0.4}

    def distinctive(title):
        return tokens(title) - _common

    # ---- Test C: blog vs blog near-duplicate
    def test_c(p, others):
        """Two posts are near-duplicates when they share DISTINCTIVE subject tokens.

        The site's category and city appear in nearly every title, so matching on raw
        overlap flagged unrelated posts in testing. Only tokens rarer than 40% of
        titles count.
        """
        mine = distinctive(p["title"])
        best, best_score = None, 0.0
        for o in others:
            if o["url"] == p["url"]:
                continue
            shared = mine & distinctive(o["title"])
            if len(shared) < 2:
                continue
            s = sim(p["title"], o["title"])
            score = s + 0.10 * len(shared)
            if score > best_score:
                best, best_score = o, score
        return best, round(best_score, 2)

    rows = []
    for p in posts:
        u = p["url"]
        g, a, b = gsc.get(u, {}), ga.get(u, {}), bl.get(u, {})
        impressions = g.get("impressions")
        clicks = g.get("clicks")
        ctr = (clicks / impressions) if (impressions and clicks is not None
                                         and impressions > 0) else None
        conversions = a.get("conversions")
        rds = b.get("referring_domains")

        cands = test_a(p)
        comp_score = cands[0][0] if cands else 0.0
        cand_str = " ; ".join(f"{c['url']} ({sc})" for sc, c, _, _ in cands)
        dup, dup_score = test_c(p, posts)

        signals, proposed, confidence = [], None, "review"

        # Test A — competing
        if cands and comp_score >= 0.6:
            signals.append(f"A: candidates — {cand_str}")
            proposed = "COMPETING"
            if len(cands) > 1 and cands[0][0] - cands[1][0] < 0.3:
                signals.append("A: top candidates are close — analyst picks the target")

        # Test C — blog-vs-blog
        if dup and dup_score >= 0.55:
            signals.append(f"C: near-duplicate of {dup['url']} (title sim {dup_score})")
            if proposed is None:
                proposed = "DUPLICATE"

        # Test B supporting signals — never decides on its own
        b_signals = []
        if ctr is not None and impressions and impressions >= 100 and ctr < 0.02:
            b_signals.append(f"impressions {impressions} at CTR {ctr:.1%} "
                             f"(answer-engine signature)")
        if rds:
            b_signals.append(f"{rds} referring domains")
        if conversions:
            b_signals.append(f"{conversions} conversions")
        if b_signals:
            signals.append("B-support: " + "; ".join(b_signals))

        # Test D — nothing fired
        if proposed is None:
            wc = p.get("word_count")
            if wc is not None and wc < 400 and not b_signals:
                proposed = "CONSOLIDATE-OR-REDIRECT"
                signals.append(f"D: {wc} words, no supporting signal")
            else:
                proposed = "NEEDS-JUDGMENT"

        # the protected-post override — flag, never auto-resolve
        override = ""
        if proposed in ("COMPETING", "DUPLICATE") and b_signals:
            override = ("CM-007: supporting signals present. Run Test B mandatory "
                        "criterion before any redirect.")
            confidence = "blocked-pending-test-B"
        if proposed == "COMPETING" and not have_gsc:
            override = ("No GSC data — Test B cannot be evaluated. Do not redirect "
                        "on Test A alone.")
            confidence = "blocked-no-evidence"

        rows.append({
            "url": u,
            "title": p.get("title"),
            "word_count": p.get("word_count"),
            "category": p.get("category"),
            "modified": p.get("modified"),
            "proposed_classification": proposed,
            "test_a_candidates": cand_str,
            "test_a_top_score": comp_score,
            "test_c_target": dup["url"] if dup else "",
            "test_c_score": dup_score,
            "impressions": impressions, "clicks": clicks,
            "ctr": f"{ctr:.3f}" if ctr is not None else "",
            "conversions": conversions, "referring_domains": rds,
            "signals": " | ".join(signals),
            "override_flag": override,
            "confidence": confidence,
            "analyst_decision": "",
            "redirect_target": "",
            "reason": "",
        })

    path = os.path.join(out_dir, "blog-decision-map.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    from collections import Counter
    c = Counter(r["proposed_classification"] for r in rows)
    blocked = sum(1 for r in rows if r["confidence"].startswith("blocked"))
    print(f"wrote {path}  ({len(rows)} posts)")
    for k, v in c.most_common():
        print(f"  {k}: {v}")
    print(f"\n  blocked pending judgment: {blocked}")
    if not have_gsc:
        print("\n  LIMITATION: no GSC data. Test B cannot be evaluated for any post, so "
              "no post may be redirected on Test A alone. Record this in the deliverable.")
    if not have_ga:
        print("  LIMITATION: no analytics data. Conversion signal unavailable.")
    print("\n  Nothing here is a decision. Every row needs analyst review; "
          "NEEDS-JUDGMENT and blocked rows cannot be resolved mechanically.")


if __name__ == "__main__":
    main()
