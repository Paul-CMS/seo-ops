---
name: client-intake
description: "Run new-client intake for a local SEO engagement by researching the business first and sending the client a pre-filled proof sheet to correct, instead of a blank questionnaire. Use this whenever a new local-business client is being onboarded, when someone mentions client intake, onboarding, an onboarding form or questionnaire, a Stage 0 document, NAP or business-facts confirmation, collecting services, service area, staff or license information from a client, or asks how to get accurate brand facts out of a contractor without burning their time. Also use when a filled-in or redlined proof sheet comes back from a client and needs reconciling into the internal record. Covers the full loop — discovery pass, gap interview with the account manager, client-facing proof sheet, reconciliation, and Stage 0 output."
---

# Client Intake — Proof Sheet Workflow

## The core idea

Local business owners will not fill in a blank 60-question form. They will red-line a
document that is already mostly filled out, because correcting is faster and less
cognitively expensive than composing.

So the work order is inverted from a normal intake: **research first, ask second.**
Everything discoverable from public sources gets filled in before the client sees
anything. The client's job is to correct, confirm, and fill a small number of
deliberate blanks.

The second idea, which matters just as much: **a pre-filled sheet invites
rubber-stamping.** Someone scrolls, sees plausible text, types "looks good," and now a
guess has been approved as fact. So factual and legal claims are never quietly
pre-filled. They are either quoted back as an existing public claim that needs explicit
sign-off, or left blank on purpose. See `references/field-schema.md` for which fields
fall where and why.

## The five phases

Run these in order. Phases 1–3 happen before the client is contacted at all.

| # | Phase | Who's involved | Output |
|---|---|---|---|
| 1 | Discovery | nobody — automated research | draft record, every field sourced |
| 2 | Gap interview | the account manager | resolved conflicts, filled internal blanks |
| 3 | Render | nobody | proof sheet `.docx` + internal record |
| 4 | Client pass | the client | corrections, blanks filled, access granted |
| 5 | Reconcile | the account manager | final record → Stage 0 |

---

### Phase 1 — Discovery

Inputs needed to start: the domain. Everything else is optional but helps — GBP link,
sales call notes or recording, a crawl export, whatever old intake docs exist.

Read `references/discovery.md` for the source hierarchy and what to check on each
source. Work through the field schema and populate every field you can, recording for
each one:

- the **value**
- the **source** (specific URL or record, not "their website")
- the **confidence**: `verified` (authoritative third-party record), `found` (stated by
  the business itself), `inferred` (deduction), or `unknown`

Record conflicts rather than silently picking a winner. A founding year that appears as
1998 on the homepage, 2004 on GBP, and 2011 on the Secretary of State registration is
one of the most useful things discovery produces — it's a liability the client needs to
resolve, and it's exactly the kind of thing a blank form would never surface.

Write the record to `<client-slug>-record.yaml` using `assets/record-template.yaml` as
the shape.

### Phase 2 — Gap interview

This is a short conversation with the account manager, not the client. Its only purpose
is to resolve things the client shouldn't be bothered with or that would make the proof
sheet wrong before it's sent.

Read `references/gap-interview.md` for what qualifies as a question and what doesn't.
The short version: ask about conflicts between sources, about knowledge from the sales
call that isn't public, and about scope decisions that change the sheet's structure.
Everything else, leave for the client or leave blank.

Hard ceiling of 8 questions, asked in a single batch, each with a proposed default so
the manager can accept most of them at once. If there's a tool available for presenting
tappable options, use it — the manager is often on a phone.

### Phase 3 — Render

Two artifacts come out of the same record:

1. **The client proof sheet** — a `.docx`, because it uploads to Google Drive and opens
   as a Google Doc with comment access, which is the format clients actually complete.
   Generate it with `scripts/render_proof_sheet.js`.
2. **The internal record** — the YAML, which is what Stage 0 gets built from later.

The renderer needs `js-yaml`, which is usually not preinstalled — run `npm install
js-yaml` in the skill directory first, or pass a `.json` record instead, which the
script reads without any dependency. `docx` itself is preinstalled.

The proof sheet has a strict three-block structure. Read `references/proof-sheet.md`
before rendering — the block a field lands in is a deliberate decision, not a layout
choice, and the blocks are what prevents rubber-stamping.

### Phase 4 — Client pass

The sheet goes out with a short covering message, not an explanation of the process.
Template in `references/proof-sheet.md`. Three things the message must do: say what's
already filled in, give a deadline, and state what gets published if nothing comes back.
Silence-is-consent with a named default gets far better response rates from contractors
than an open-ended ask.

Do not send all sections at once if the engagement can tolerate staging. Facts and
access first, since access is the only genuinely blocking item. People and expertise
should not be collected on a form at all — that's an interview, and it belongs to the
expert-interview process, not here.

### Phase 5 — Reconcile

Whatever comes back — tracked changes, comments, a reply email, a text message, a voice
memo — parse it and update the record. This is the part that makes the client's return
format irrelevant, so never push back on how they replied.

For each change: update the value, set confidence to `client_confirmed`, and record the
date. For anything the client contradicted, keep the old value in a `was:` field. Those
contradictions are where the content risk lives — a client who corrects "since 1998" to
"since 2011" has just told you that every page on the site carries a false claim that
needs a sweep.

Produce a short reconciliation summary for the manager covering: what the client
changed, what's still blank, what access is still missing, and any corrections that
imply site-wide edits.

Then generate the Stage 0 document from the final record — format in
`references/proof-sheet.md`.

---

## Files

- `references/field-schema.md` — every field, and the confirm / verify / blank
  classification that drives the whole sheet. Read this first.
- `references/discovery.md` — source hierarchy, what to pull from each source, how to
  assign confidence, common traps.
- `references/gap-interview.md` — what to ask the manager, what not to, how to batch.
- `references/proof-sheet.md` — proof sheet structure, covering message, reconciliation
  rules, Stage 0 output format.
- `assets/record-template.yaml` — the record shape.
- `scripts/render_proof_sheet.js` — record YAML → client-facing `.docx`.

## Things that go wrong

**Asking the client something you could have found.** Every avoidable question spends
goodwill you need for the questions that aren't avoidable. If a field is on the site,
fill it in.

**Pre-filling a claim you can't stand behind.** If the sheet asserts a license number
and the client skims past it, the agency now owns that error. Blanks are a feature.

**Treating the gap interview as a second intake form.** If the manager is answering
twenty questions, the workflow has failed and the burden just moved.

**Collecting expertise on a form.** A form returns "20 years experience, family owned."
A recorded conversation returns six blog posts. Keep them separate.
