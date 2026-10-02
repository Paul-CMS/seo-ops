---
name: link-implementation-qa
description: Verify that internal linking and technical fixes were actually implemented as specified. Use when a VA returns a completion report, when checking whether handoff work went live, or when someone says "check the VA's work", "verify the implementation", "did they do it right", or hands back a completion CSV. Companion to updated-link-strategy — that skill produces the spec, this one checks it. Do NOT use this to run a fresh audit.
---

# Link Implementation QA

## What this is for

The spec says what should be on the site. The completion report says what the
VA believes they did. Neither is evidence. The live site is evidence.

This skill checks the site against the spec, using the completion report only to
decide where to look and to surface what was left out.

**Do not re-run the audit.** If the spec is wrong, that is a separate
conversation. This pass answers one question: was the spec implemented.

## Required inputs

Ask for whatever is missing before starting:

- The linking workbook / fix pack (the spec, with item refs)
- The returned completion report CSV
- The domain

If the completion report is a coloured document rather than a CSV, say so and
ask for the CSV. Colours are not checkable and a marked-up copy of the spec
carries no information the spec did not already have.

## Step 1 — Validate the report before touching the site

Cheap checks, done first:

- **Invented refs.** Any `ref` not in the spec. Flag, do not silently accept.
- **Status values.** Only `done`, `blocked`, `deviated`. Anything else is
  invalid — treat as unverified.
- **Silent omissions.** Spec rows with no corresponding CSV row. This is the
  single most informative check in the whole pass: work that was quietly skipped
  never appears in a report and never gets caught by reviewing the report alone.
- **Blocked and deviated rows with no note.** Incomplete by definition.
- **Rows added at the bottom.** Findings the VA made outside the spec belong in
  a `found` block, not as new spec rows. Read them, keep them separate.

## Step 2 — Crawl, in batches

Crawl only the URLs the report lists, plus the pages carrying silent omissions.

**Hard rule: batch this.** Crawl by page type first, confirm the pattern holds,
then sample. Running one fetch per URL on a 100-page site will exhaust context
before any findings get written. If the URL count is large, say up front how
many batches this will take and do them in sequence, writing findings out after
each batch rather than holding everything in context to the end.

## Step 3 — Machine-checkable per row

For each `link` row:

1. Link present on the page at all
2. Anchor text matches the spec **character for character** — a paraphrase is a
   fail, not a near-miss
3. Destination returns 200 **directly**, no redirect hop, no 404-fallback guess
4. Link sits in the specified H2 block
5. That block contains no other body link (the one-per-block rule)

For each `fix` row: the change is live on production, and the page loads.

For each `merge` row: the 301 is live, and nothing on the site still links to
the retired URL.

For each `content` row: published only if approved. An unapproved published
addition is a serious finding, not a minor one.

## Step 4 — Sitewide regression

Independent of what the report claims:

- Zero remaining links to retired or legacy URLs anywhere
- No new empty anchors introduced
- No new redirect hops on internal links

## Step 5 — What a person still has to read

Everything above is deterministic. These are not:

- **100% of content additions.** Does the addition serve its section's intent,
  follow from the paragraph before, set up the paragraph after? Would the
  section still be better with the link removed? This is the one check that
  cannot be automated and the one place where the whole method gets quietly
  broken.
- **A 20% sample of link placements.** Does the link land in a sentence that
  genuinely raises the question the destination answers?

Clean sample, trust the batch. Failed sample, expand the check — and report it
as a calibration finding about that batch, not as a finding about one link.

## Output

**Mismatches only.** A list of everything that passed is noise and defeats the
purpose. Lead with the counts, then the exceptions.

```markdown
## Implementation QA — {client}, {date}

Rows reported: {n}  |  Verified: {n}  |  Mismatched: {n}  |  Omitted from report: {n}

### Reported done, not done
| Ref | Page | Expected | Found |

### Reported done, wrong
| Ref | Page | Expected | Found | Issue |

### Silently omitted
| Ref | Page | What the spec required |

### Deviations — accepted
| Ref | What they did | Why it holds |

### Deviations — rejected
| Ref | What they did | Why it fails the spec |

### Judgment sample
{content additions read, link placements sampled, verdict, whether to expand}

### For Paul
{decisions, unapproved publications, spec errors found}
```

## Calibration

Judge deviations on the four-part test, not on whether they match the letter of
the spec. A VA who moved a link because the specified placement collided with
the one-per-block rule got it right and the spec got it wrong — accept it and
correct the spec.

A VA who reworded page copy so a link would fit got it wrong even if the link
now reads well. That is the failure mode the method exists to prevent.

Report honestly. A report that finds nothing on a large batch is more likely to
mean the check was too shallow than that the work was perfect.
