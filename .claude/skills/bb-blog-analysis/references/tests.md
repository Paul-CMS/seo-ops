# The Four Tests

Order matters. Test B runs **before** Test A's redirect is executed, not after.

---

## Test A — Competition *(BB-701, Bradley's)*

**Question:** does this post target the same entity + location combination as an existing
service or location page?

If yes, it competes. The remedy is a 301 to the single most relevant commercial page —
**never a delete**, because the redirect captures whatever equity the post accumulated.
*(BB-702)*

### Choosing the target — do not let the script do it

The script ranks candidates and stops. Two reasons it cannot pick:

- **A location page matches any post that names the city.** "Headache Tips from an Appleton
  Chiropractic Office" scores highest against `/appleton/` because both the city and the
  category match, even though the post is about headaches and `/headaches-migraines/` is the
  right target.
- **The homepage matches almost everything**, since it carries the brand, the category and
  the area entity. It is scored down for that reason and is rarely the right answer.

Pick the page whose **subject** the post actually shares. Where the top candidates are
close, the script says so.

---

## Test B — AI Search Gap *(CM-007, Coastal — not Bradley)*

**Mandatory criterion:** does this post answer a specific, real question that **no** service
or location page covers?

If a commercial page already covers the topic, it is not a gap post — re-run Test A.

**Plus at least one supporting signal:**

| Signal | What it looks like |
|---|---|
| Impression/CTR pattern | Meaningful impressions with low click-through — the signature of a post ranking for a real query and losing the click to an AI summary rather than to a competitor |
| Assistant-shaped question | Something a customer would type into ChatGPT or Perplexity directly — a cost question, a troubleshooting or diagnostic question, an is-it-worth-it comparison — rather than an about-our-services post |
| No better-covering competitor | The gap is not covered by competitors either, so it is a genuine market gap worth strengthening |

**Mandatory plus one supporting = PROTECTED.** Never deleted, never redirected. Routed to
optimization in place.

### Why this overrides Bradley

His Test A would redirect a post that shares an entity with a service page. The entity match
is not what makes a post competing — **covering the same question is.** A post answering
something no page answers is filling a gap, not splitting a signal.

This is a Coastal rule at PILOT status. Attribute it as ours in any client deliverable.

### Without Search Console data

Test B cannot be evaluated. **Therefore no post may be redirected on Test A alone.** Record
the limitation in the deliverable and leave those posts unresolved rather than acting on
half the evidence.

---

## Test C — Blog versus blog

Do two or more posts target near-identical subjects? Consolidate into the strongest — prefer
the one with more Search Console signal, or the one that would otherwise qualify under Test
B — and 301 the others into it.

Two thin posts splitting a signal that one strong post could hold is the most common
residual defect on a site that is otherwise compliant.

### Matching only counts distinctive words

The site's category and city appear in nearly every blog title. Matching on raw overlap
pairs unrelated posts — "Finding a Chiropractor in Appleton" and "Appleton Chiropractor May
Help TMJ" share two words and nothing else.

Only tokens appearing in fewer than 40% of titles count, and at least two distinctive shared
tokens are required before a duplicate is proposed.

---

## Test D — Neither

Doesn't compete, isn't a gap post, isn't a near-duplicate. Thin, stale, or genuinely low
value.

**The only category eligible for removal from the live site** — and even here, redirect
rather than hard-delete wherever a relevant target exists.

---

## Traps

**Template clone smell is not duplication.** Location pages clustering at similar word
counts with a shared H2 skeleton is *mandated* by the methodology. Do not flag it. What it
means is that the human layer is the only differentiator, so each needs the portability test
applied — that is a content finding, not a cannibalization one.

**A low indexed-to-published ratio is not a technical problem.** It is Google judging pages
redundant, low-quality or self-competing — which means the classifications above are the
cause, not a separate issue. *(BB-210)*

**Uncategorized is a signal, not a verdict.** A cluster of short posts in an unused category
is usually legacy content, but check each against Test B before assuming.

**Recency is not quality.** A recently modified post may have had its date bumped
cosmetically. Check whether the content actually changed.

**Never average two signals.** A post with strong impressions and zero conversions is not
"medium". Report both and let the classification rest on the tests.
