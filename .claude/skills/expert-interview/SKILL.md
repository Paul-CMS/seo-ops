---
name: expert-interview
description: Run the expert-led content process for a local SEO client — generate interview questions for a client's subject-matter expert, and extract structured expertise from the voice-memo transcripts that come back. Use this whenever the user mentions expert interviews, SME interviews, expertise capture, voice memos or transcripts from a client, building an expertise file, first-party content research, or needs blog topics grounded in what a client actually knows rather than generic keyword-driven content. Also use it when the user is starting Stage 6 blog work and wants real source material, or when they say something like "process this transcript", "what should I ask the owner", or "turn this interview into content ideas".
---

# Expert Interview & Expertise Extraction

## What this is for

Generic AI content fails because the model has no firsthand knowledge of the client's business, so it fills gaps with statistically plausible filler. This skill exists to replace that filler with real material from the people who do the work.

The method is: interview a subject-matter expert at the client, extract discrete insights from what they said, and build a growing expertise file that feeds blog posts, service pages, and site builds for months.

Everything here depends on one thing — **specificity**. "We see a lot of broken springs" is worthless. "In the older split-levels off Route 9 the builders used undersized torsion springs, so we get failures around year eight and the homeowner always thinks the opener is broken" is the entire point. Every design decision below serves that distinction.

## Two modes

Ask which one applies if it isn't obvious from what the user said.

**Mode A — Generate questions.** The user needs a round of questions to send an expert. Go to "Mode A" below.

**Mode B — Process a transcript.** The user has a transcript back from a voice memo. Go to "Mode B" below.

A full cycle alternates: A → client records → B → A → client records → B. Two or three rounds usually exhausts a topic per expert.

---

## Mode A — Generate questions

### What you need first

Ask for anything missing. Do not guess at client context — inventing plausible-sounding local detail is the exact failure this process exists to prevent.

- **Client**: business name, trade, primary market, services
- **Expert**: name and role (owner, estimator, technician, CSR, office manager, project manager)
- **Round number**: is this the first round for this person, or a follow-up?
- **Existing expertise file**: if one exists for this client, read it. Questions that re-ask what's already captured waste the expert's patience, which is the scarcest resource in this whole process.

Local market context matters — housing stock and age, climate, common construction eras, regional quirks. If the user has intake data for the client, use it. If not, ask for two or three sentences about the market rather than assuming.

### How to build the questions

The seven standing categories are in `references/question-bank.md`. Read it. They are fixed; what changes is how they get instantiated for this trade, this market, and this person's role.

Weight the categories by role. An owner holds decision criteria and pricing logic. A technician holds what customers misunderstand and what they break themselves. A CSR holds the pre-booking questions and the recurring complaints. Asking a technician about pricing strategy wastes a round.

Rules that matter:

- **Three to five questions per round. Never more.** A long list reads as homework and gets abandoned. This is the single most common way the process dies.
- **Anchor each question in something concrete** — a season, a housing type, a neighborhood, a specific failure, a price range. "What's the strangest job you've handled?" gets a shrug. "What's the oddest failure you've seen in the older houses around here?" gets a story.
- **Ask for stories, not summaries.** "Walk me through a time when..." outperforms "What are common issues with..."
- **Write at the expert's reading level**, in their vocabulary, not marketing language. These go to a tradesperson on a phone.
- **One question per question.** Compound questions get half-answered.

### Output format for Mode A

```
## Round [N] — [Expert name], [role] — [Client]

Send by text or email. Ask them to reply with voice memos, one per question,
recorded whenever it suits them.

1. [Question]
2. [Question]
3. [Question]
...

---
Targeting: [one line on which categories this round covers and why]
Not asked yet: [categories still untouched for this expert]
```

Then remind the user to review before sending. Questions go out under their name and a bad one spends client goodwill that is hard to get back.

---

## Mode B — Process a transcript

### What you need first

- The transcript
- Which client and expert it came from, and which round
- The existing expertise file for that client, if one exists — read it so you can deduplicate

If the transcript looks garbled in places (job-site noise, cut-off sentences, obvious mis-transcriptions of trade terms), say so before extracting. Structuring bad audio into confident-looking output is worse than flagging it, because the error becomes invisible downstream.

### Extraction

Read `references/extraction-rubric.md` for the insight types and the specificity scale. The core discipline:

**Extract only what the expert actually said.** Do not add industry knowledge, do not smooth over gaps, do not infer what they probably meant. If the transcript is thin, the correct output is a short list plus follow-up questions, not a padded one. A round that yields four real insights out of eight questions is a successful round.

**One insight per entry.** Do not merge two observations into a paragraph. Insights are reusable units — a single interview should be able to feed a dozen different articles, and that only works if the material is atomized.

**Keep the specifics verbatim.** Neighborhoods, road names, house ages, brands, model numbers, price figures, seasons, failure modes, the words customers actually use. Stripping these out to sound more professional destroys the value.

**Score specificity 1–5.** Anything at 1–2 is generic. Do not file it as an insight; convert it into a follow-up question instead. This is the quality gate that keeps the expertise file honest.

### Follow-up questions

Generate three to five for the next round. Target the **thinnest** answers, not the most interesting ones — the interesting answers already gave you material, the thin ones are where value is still trapped.

For each, note in one line why you're asking. The user reviews before sending.

### Output format for Mode B

```
## [Client] — Expertise extract, Round [N], [Expert name] ([role])

### New insights

**[TYPE]** [The insight, in the expert's own framing]
> [supporting quote from the transcript]
Specificity: [1-5] · Tags: [tag, tag]

[repeat per insight]

### Thin answers
- [Question] — [why the answer didn't land]

### Suggested follow-ups for Round [N+1]
1. [Question] — [why]
...

### Content angles surfacing
- [Working title] — draws on [which insights] — [the angle in one line]
```

If the user keeps the expertise file in Notion, format the insights so they paste in cleanly as separate blocks rather than one wall of text.

---

## Where this fits downstream

Insights feed:

- **Blog work** — articles built around the actual questions the expert answered, direct answers near the top, deeper explanation underneath
- **Service and location pages** — real local conditions instead of a city name swapped fifty times
- **Site builds** — expertise is what stops a mass-generated authority site from reading like every other mass-generated authority site

When surfacing content angles, prefer ones that cross-reference multiple insights. A post built on one anecdote is thin; one built on a misconception plus a local condition plus a cost factor is the kind of thing competitors can't replicate.

## What this skill will not do

- **It will not invent expertise.** If asked to fill gaps or write the article without source material, say no and explain why — that's the failure mode the whole system exists to avoid.
- **It will not transcribe audio.** Claude doesn't accept audio files. Transcribe elsewhere first (Google AI Studio handles long files free) and bring the text.
- **It will not auto-send questions.** Every round is reviewed by a human before it reaches a client.
