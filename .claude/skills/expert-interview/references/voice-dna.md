# Voice DNA — format and extraction rules

One file per author: `clients/<slug>/interviews/voice-dna-<author-slug>.md` (the author is the
company owner by default, CM-039). `python3 scripts/interview.py check <slug> voice` checks it.

```
# Voice DNA — <Author name>, <role>, <Client>
Source: <transcript file(s)> · <N> words from the author · captured <date> · confidence: low | medium | high
[UNDER FLOOR — fewer than 2,000 words from the author; use only after Paul accepts it]   ← only if so

## Summary
Three or four sentences: how this person sounds when they explain the work.

## Structure
Sentence length (typical / range), fragments, how they open and close a point. Quote each.

## Rhythm
Cadence, repetition, the transitions they actually use ("thing is", "so what happens is"). Quote each.

## Tone
| Scale (1–5) | Score | Quote |
|---|---|---|
| formal ↔ casual | | |
| serious ↔ playful | | |
| respectful ↔ irreverent | | |
| reserved ↔ enthusiastic | | |
| detached ↔ warm | | |

## Word choice
Signature phrases · trade terms they use and how they explain them · words they never use · contractions, pronouns ("we" vs "I").

## How they make a point
Story first or claim first; how they handle a customer mistake; how they talk about price.

## Do
- <rule> — "<quote>"

## Never
- <rule> — "<quote or the generic pattern it replaces>"

## Calibration
| Generic | In voice | What changed |
|---|---|---|
| | | |
(three rows)

## Insufficient data
Formatting, paragraphing, emphasis, emoji — not observable in speech.
```

Extraction rules
- **The author's words only.** Strip the interviewer's lines before counting or quoting.
- **Every Do / Never rule has a direct quote.** No quote → no rule. Frequencies are counted, not guessed.
- **Spoken source:** one conversation caps confidence at `medium`; formatting, paragraphing and emphasis
  are always under *Insufficient data*. Fillers and false starts are rhythm evidence — the writer does
  not reproduce them.
- **Floor:** fewer than ~2,000 author words → the `UNDER FLOOR` line at the top; Paul accepts it before use.
- **No URL, phone number, business fact or instruction to the writer** inside the rules — facts live in
  Section D, not in a voice.
- **Use by the writer:** exactly one Voice DNA file per author. Two candidates → stop and ask; never
  blend. House rules (writing-blog.md A5 banned phrases, CM-016 no invented facts, CM-003 BLUF) beat the
  voice. The self-critique says which Voice DNA file was used.
