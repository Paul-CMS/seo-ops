---
name: expert-interview
description: Run the three client interviews for a local SEO client (CM-042) — FACTS (targeted questions when the evidence gate blocks a page; answers update the proof sheet / Brand Guide Section D), STORIES (a recurring round of story-seeking questions for the owner or another expert; answers go to the client's story bank, which the blog writer uses for information gain), and VOICE (a Voice DNA file for the blog author, built from a recorded or transcribed conversation). Use this whenever the user mentions expert or owner interviews, SME interviews, a facts interview, an evidence-gate block, voice memos or transcripts from a client, a story bank, expertise capture, a voice profile or Voice DNA, "what should I ask the owner", "process this transcript", or needs blog material grounded in what the client actually knows.
---

# Client interviews — Facts, Stories, Voice

## What this is for

Generic AI content fails because the model has no firsthand knowledge of the client's business,
so it fills gaps with statistically plausible filler. These interviews replace that filler with
real material from the people who do the work. There are three, because they answer three
different needs and have three different owners of the answer (CM-042):

| Interview | Triggered by | Answers go to | Used by |
|---|---|---|---|
| **Facts** | an evidence-gate **block** only (CM-041) | the proof sheet / Brand Guide Section D (or the page's facts file), then the gate re-runs | Build briefs and drafts |
| **Stories** | a schedule, once the facts exist (`brand_guide_approved`) — default every 30 days | the client's **story bank** (`clients/<slug>/interviews/story-bank.md`) | the blog writer, for information gain (WB-C6) |
| **Voice** | once per author, from a recorded or transcribed conversation | the author's **Voice DNA** (`clients/<slug>/interviews/voice-dna-<author>.md`) | the blog writer, at draft |

The command is `/interview <slug> facts|facts-answers|stories|stories-answers|voice`. Nothing is
sent to a client automatically: every question set is reviewed by Paul, and Paul sends it.

Everything depends on one thing — **specificity**. "We see a lot of broken springs" is worthless.
"In the older split-levels off Route 9 the builders used undersized torsion springs, so we get
failures around year eight and the homeowner always thinks the opener is broken" is the entire point.

Pick the track from what the user said; ask if it is not clear.

---

## Facts — gap-driven, only on an evidence-gate block

**When:** `/next` says the evidence gate blocked one or more pages in a batch. Never for a page that
passed or warned — those go ahead with `[NEED: …]` markers (CM-016).

**Questions** come from the gaps, not from a bank: `python3 scripts/evidence.py questions <slug> --run <RUN_ID> --batch <id>`
writes the pack (`clients/<slug>/interviews/facts/<Client> - Facts Interview - <batch> - <date> - REVIEW.md`)
from every Unknown / Unverified / Conflict fact on the blocked pages, required facts first, shared
facts asked once, **15 questions at most**. Three question shapes:

- **Describe** (Unknown) — "what should we say? If it depends, on what?" plus "can we say this on your website? yes / only in general terms / no".
- **Verify** (Unverified) — quotes what we have and where it came from; "yes / partly — correction / no".
- **Verify** (Conflict) — shows the versions we found; "which is right?"

Edit the wording for the trade and the person (plain, phone-friendly, one question per question),
but never add a question that is not a gap, and never pre-fill an answer. Paul reviews and sends.

**Answers** (`facts-answers`): save the reply as given in `clients/<slug>/interviews/facts/`. Then, for
each answer, update the fact it fills — Brand Guide Section D (status `Client Confirmed`, source
`Facts interview <date>`) or the page's facts file (`clients/<slug>/build/evidence/<page>.facts.json`).
- "Only in general terms" → status `Client Confirmed` with the value written as the general claim the owner allowed.
- "No" (not for publication) → leave the fact Unknown and note why in the source column.
- "I don't know" → stays Unknown.
- A correction to something the site claims publicly → also a row in D2.
- Anything from reviews or customer language is still never a fact (CM-027).
Then re-run the gate: `python3 scripts/evidence.py run <slug> --run <RUN_ID> --batch <id>`. Editing
the Brand Guide voids `brand_guide_approved` until Paul re-approves it — that is intended: Paul sees
every new fact before it reaches a page.

---

## Stories — a recurring round, into the story bank

**When:** after `brand_guide_approved` (the facts exist), every **30 days** by default
(`config.json` `story_cadence_days`; `python3 scripts/interview.py due <slug>` says whether a round is
due). One person per round; rounds 1–3 usually exhaust a topic per expert, then switch person.

### Generate the round (`stories`)

Read the story bank first — questions that re-ask what is already captured waste the expert's
patience, which is the scarcest resource in this whole process. Use the seven standing categories in
`references/question-bank.md`, weighted by role (an owner holds decision criteria and pricing
logic; a technician holds what customers misunderstand and break; a CSR holds the pre-booking
questions). Steer toward the blog topics and service clusters that are thinnest in the bank.

- **Three to five questions per round. Never more.** A long list reads as homework and gets abandoned.
- **Anchor each question in something concrete** — a season, a housing type, a neighborhood, a failure, a price range.
- **Ask for stories, not summaries.** "Walk me through a time when…" beats "What are common issues with…"
- **Write at the expert's reading level**, in their vocabulary. These go to a tradesperson on a phone.
- **One question per question.**

Do not invent local context. If intake does not give the market (housing stock, climate,
construction eras), ask for two or three sentences rather than assuming.

Output `clients/<slug>/interviews/stories/<Client> - Stories Round <N> - <expert> - <date> - REVIEW.md`:

```
## Round [N] — [Expert name], [role] — [Client]

Reply with voice memos, one per question, whenever it suits you.

1. [Question]
...

---
Targeting: [categories this round covers and why]
Not asked yet: [categories still untouched for this expert]
```

`status.py mark <slug> story_round --file <it>`. Paul reviews and sends.

### Process the transcript (`stories-answers`)

Claude does not take audio — transcribe elsewhere first and bring the text. Save it as given in
`clients/<slug>/interviews/stories/`. If it is garbled (site noise, cut-off sentences, mis-heard
trade terms), say so before extracting — confident structure on bad audio hides the error.

Read `references/extraction-rubric.md`. **Extract only what the expert said** — no added industry
knowledge, no smoothing, no inferring. One story per entry. Keep the specifics verbatim. **Score
specificity 1–5**; 1–2 is not filed — it becomes a follow-up question.

Append each entry to `clients/<slug>/interviews/story-bank.md` (format in `references/story-bank.md`):
ID, date, round, speaker, type, headline, the verbatim quote, specificity, tags, **publish**
(`public` / `framing-only` / `internal` — ask when unclear; default `framing-only`), **status**
(`fresh` → `used` with the post it went into → `retired`). A story that states a business fact
(a warranty, a price, a licence) is **flagged `fact?`** and goes to the facts track — it never
writes Section D directly.

Then follow-ups for the next round (3–5, targeting the thinnest answers, each with one line on why)
and content angles that combine several stories. `python3 scripts/interview.py check <slug> bank`
must pass; `status.py mark <slug> story_bank --file clients/<slug>/interviews/story-bank.md`.

---

## Voice — a Voice DNA file for the blog author

**Who:** the blog author — the company owner by default (CM-039), unless the client says otherwise.
**Source:** a recorded or transcribed conversation with that person: a 20–30 minute call about the
business, how they got into the trade, a few jobs they remember. Stories-round voice memos can be
pooled. Save the transcript(s) as given in `clients/<slug>/interviews/voice/`.

Extract **from the author's own words only** (not the interviewer's). Read `references/voice-dna.md`
for the sections and rules. In short:
- Structure (sentence length, fragments), rhythm (cadence, repetition, transitions), tone (five 1–5
  scales, each with a quote), word choice (signature phrases, jargon they use and explain, words they
  never use), how they make a point, and the anti-patterns to suppress (the generic AI voice).
- **Every rule is backed by a direct quote.** No quote → no rule.
- **Spoken source limits:** formatting, paragraphing and emphasis are `insufficient data` — never
  infer "never uses bold" from speech. Fillers and false starts are rhythm evidence, not things to copy.
- **Floor:** under ~2,000 words from the author → mark the file `UNDER FLOOR` at the top; the writer may
  use it only after Paul accepts it.
- Output: summary · do rules · never rules · 3 calibration rewrites (generic sentence → in-voice →
  what changed). No URL, phone number or instruction to the writer inside the rules.

Write `clients/<slug>/interviews/voice-dna-<author-slug>.md`; `python3 scripts/interview.py check <slug> voice`
must pass; `status.py mark <slug> voice_dna --file <it>`. The blog writer reads it at draft
(`methodology/writing-blog.md` B5): **one** Voice DNA file per author — if two match, stop and ask;
never blend. House rules (A5 banned phrases, CM-016) still win over the voice.

---

## Where this fits downstream

- **Facts** → the evidence gate (CM-041) → briefs and drafts for service and location pages.
- **Stories** → blog briefs list the story IDs they use ("Story bank entries used: S-007, S-012");
  the post's information gain (WB-C6) cites them. Service and location pages may use `public`
  stories as real local conditions (BB-317).
- **Voice** → the blog writer's draft and self-critique.

## What this skill will not do

- **Invent expertise, facts or voice.** If asked to fill gaps or write without source material, say no and explain why.
- **Transcribe audio.** Bring text.
- **Send anything.** Every round is reviewed and sent by Paul. No phone bot, no automatic calls.
- **Move a story into Section D.** A fact in a story goes to the facts track.
