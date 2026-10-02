# Extraction Rubric

## Insight types

Tag every insight with exactly one. If something seems to fit two, split it — that usually means there are two insights.

| Type | What it captures |
|---|---|
| `customer_question` | Something customers actually ask, in their words |
| `misconception` | Something customers believe that's wrong |
| `unusual_case` | A specific job, project, or event |
| `decision_criterion` | What changes the recommendation |
| `local_condition` | Geography, housing stock, climate, code, construction era |
| `terminology` | Words customers use — including wrong ones |
| `objection` | Why people hesitate or don't buy |
| `process_detail` | How the work is actually done, when non-obvious |
| `cost_factor` | What drives price; cheap vs. right |

`terminology` looks minor and isn't. When a customer says "the thing that makes the door go up" instead of "opener", that's the language they search in. Capture their wording, not the trade term.

---

## Specificity scale

Score every candidate 1–5. This is the quality gate.

**5 — Named specifics.** Neighborhood, road, construction era, brand, model, price, or date. Could only have come from this person.
> "The Cranbrook development, built around '94 — those builders used a 7-foot door with a single spring rated for maybe 10,000 cycles. We're replacing those at year eight, ten at the outside, and the homeowner always thinks it's the opener because that's the part that makes noise."

**4 — Concrete but unnamed.** Real detail, particular circumstances, no proper nouns.
> "Anything built in the mid-nineties around here has undersized springs, and they fail right around year eight. Customers always blame the opener."

**3 — Real but thin.** True observation, plausible from anyone in the trade in this region. Usable, but push for more in the next round.
> "Older homes in this area tend to have undersized springs that fail early."

**2 — Generic.** Could appear on any competitor site.
> "Springs wear out over time and eventually need replacing."

**1 — Filler.** Says nothing.
> "Garage doors require regular maintenance."

**Rule: 3 and above gets filed. 1 and 2 do not.** Convert them into follow-up questions instead. A generic insight in the file is worse than no insight, because a VA later treats it as real material and writes generic content from it — the exact loop this process exists to break.

---

## Extraction discipline

**Only what was said.** The strongest temptation is to round an answer up toward what you know about the trade. Don't. If the expert said springs fail early and you know why, that "why" is not theirs and doesn't go in the file. It becomes a follow-up question.

**Atomize.** One observation per insight. Merged paragraphs can't be recombined later.

**Preserve their voice in `content`.** Not a marketing rewrite, not a summary in your register. If they said "she was ready to replace the whole unit over a $40 part", keep that.

**Always attach a supporting quote.** Verbatim from the transcript. It's the audit trail — six months later, someone should be able to check whether a claim on a client's site actually traces to something the owner said.

**Deduplicate against the existing file.** Same fact, more detail → update the existing insight and raise its score. Same fact, no new detail → skip it and note the repetition, which is a signal that this expert is tapped out on that category.

**Contradictions get flagged, not resolved.** If a technician contradicts what the owner said, surface it. Sometimes it's a correction; sometimes it's two people with different vantage points and both are worth having. Never quietly pick one.

---

## Handling bad transcripts

Voice memos get recorded in trucks, on job sites, next to running equipment. Expect:

- Trade terms mangled by the transcription model
- Sentences cut off at the start or end of a memo
- Numbers misheard — prices and measurements are the worst offenders

**Flag rather than fix.** Structuring garbage into a clean-looking insight is the most dangerous output this skill can produce, because the error becomes invisible once it's formatted. If a price or measurement looks wrong, mark it for confirmation rather than filing it. If a whole passage is unusable, say which part and move on.

---

## Tagging

Free-text tags on each insight, aimed at retrieval. Include:

- The service or product involved
- The customer situation, if there is one
- Any location or property type mentioned
- The season or timing, if relevant

Tags are what let a VA later pull "everything about spring failures" or "everything about the older subdivisions" without rereading the whole file. Be consistent within a client — reuse an existing tag rather than coining a near-synonym.
