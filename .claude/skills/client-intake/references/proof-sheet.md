# Proof Sheet, Reconciliation, and Stage 0

## Contents

1. Why .docx
2. Sheet structure
3. Writing rules
4. The covering message
5. Staging
6. Reconciliation
7. Stage 0 output

---

## 1. Why .docx

Generate a `.docx`, upload it to Google Drive, and share it with comment access and no
sign-in requirement. Send the link by text message, not as an email attachment.

The reasoning, in case a different format is being considered:

- It opens in one tap on a phone, which is where a contractor will read it
- They can type directly in it or comment — both are fine, and both are parseable
- Revision history shows exactly what was touched and when, so chasing is precise
- No login wall, which kills more form completions than length does

A PDF is worse: read-only means they reply in prose and the mapping back to fields is
lost. A pre-filled Google Form returns cleaner data but reads as *a form*, which is the
psychological thing this whole workflow exists to avoid, and it can't show the
already-found context that makes the sheet feel like work already done for them.

## 2. Sheet structure

Fixed order. The blocks are load-bearing — see `field-schema.md` for what lands where.

```
[Header]
  Business name
  "Prepared [date] · Please return by [deadline]"
  Two sentences: what this is, what happens if it's not returned

BLOCK A — CONFIRM THIS
  Three-column table: What we have | Correct? | Fix it here
  Middle column is ✓ or ✗ only
  Grouped by: Identity · Contact · Hours · Services · Service area · Online

BLOCK B — PLEASE VERIFY THESE CLAIMS
  Each item quoted with its source, one per row, explicit yes/no required
  Conflicts shown with all candidate values side by side
  Short lead-in explaining these are claims already public, not new questions

BLOCK C — WE NEED THIS FROM YOU
  Documents to forward
  Facts (blank fields)
  Three positioning questions
  Names and photos

ACCESS
  One row: "Add us as a Manager on your Google Business Profile" (Paul, 2026-10-08 — no GSC/GA4,
  hosting or domain questions)

[Footer]
  "Questions? Reply to the email this came with." (no phone line — Paul, 2026-10-08)
```

Target: 25–30 rows in Block A, 6–12 in Block B, under 10 in Block C. Ten minutes.

## 3. Writing rules

**Write to a contractor, not to a marketing department.** No "brand positioning," no
"value proposition," no "target persona." Ask what job they want more of.

**Never ask two things in one row.** "Service area and travel fees?" gets one answer.

**Show sources inline, small.** *(from your homepage)* next to a pre-filled value is
what makes the sheet feel researched rather than guessed.

**Free text costs the most, so spend it deliberately.** Three open questions is the
budget. Everything else is a checkbox or a correction.

**Say a sentence is enough.** Explicitly. Otherwise they'll leave it blank rather than
write an essay they don't have time for.

**Don't explain the process.** They don't care that this feeds Stage 0.

## 4. The covering message

Short, plain, three jobs: say it's pre-filled, give a deadline, state the default.

```
Hey [name] — before we start on the site, here's everything we found about
[business] publicly. It's already filled in; I just need you to fix
anything wrong and fill the handful of blanks I couldn't find.

Should take about ten minutes: [link]

The blanks matter more than the rest — mostly license and insurance stuff
we can't publish without confirming from you.

If I don't hear back by [day], we'll build with what's on there now.
```

No phone offer (Paul, 2026-10-08): the sheet carries no phone line. Clients who would rather talk reply to the
email; their answers are saved verbatim as MANUAL evidence (`/discovery <slug> facts-direct`).

## 5. Staging

If the engagement allows, send in this order, not all at once:

1. **Access + Block C blanks** — day one. Access is the only truly blocking item and it
   often uncovers a problem (GBP owned by a previous agency, domain on a dead email)
   that takes weeks to resolve.
2. **Blocks A and B** — day one or two, once discovery is complete.
3. **People and expertise** — not on a sheet at all. This is the interview, and it
   belongs to the expertise-capture process.

If the account is small enough that three touches is too many, combine 1 and 2 and keep
the order of blocks within the document.

## 6. Reconciliation

Accept any return format. Tracked changes, comments, a reply email, a text, a voice
memo, a phone call transcribed afterwards. Never ask a client to resubmit in a different
format — parsing is cheap and their willingness is not.

For each field the client touched:

```yaml
founding_year:
  value: 2011
  confidence: client_confirmed
  confirmed_on: 2026-09-18
  was: 1998
  note: "Site claims 1998 across homepage, about, 4 service pages — needs sweep"
```

Then produce a reconciliation summary for the manager:

- **Changed** — what the client corrected, with the old value
- **Site-wide implications** — any correction that contradicts existing published
  content, with the pages affected. This is the highest-value output of the whole
  workflow and should be at the top.
- **Still blank** — what didn't come back, and whether it blocks anything
- **Access outstanding** — with who to chase
- **New claims to substantiate** — anything the client asserted that content will
  publish and that has no documentation behind it yet

A client who corrects a founding year, a license number, or a service they no longer
offer has just told you that live pages are wrong. Treat that as an urgent content
finding, not a record update.

## 7. Stage 0 output

Once reconciled, generate the Stage 0 document from the final record. It should contain
only confirmed or verified values — anything still `found` or `inferred` gets flagged
inline as unconfirmed rather than silently promoted to fact.

```
# Stage 0 — [Business Name]

## Entity
Legal name, DBA, entity type, registration, license(s), insurance status

## NAP
Canonical name / address / phone exactly as it should appear everywhere,
plus the address-type decision (storefront vs SAB) and its reasoning

## Service area
Primary MSA, named cities, counties, exclusions

## Services
Confirmed list, with priority ranking from the "want more of" column

## Differentiators
Confirmed claims with substantiation source for each

## People
Names and roles only; expertise content lives in the interview record

## Unconfirmed
Every field still unresolved, with what's blocking it

## Content risks
Live claims contradicted by the client's corrections, with affected URLs
```

The **Unconfirmed** and **Content risks** sections are the ones that matter most
downstream, so don't drop them when everything else looks complete.
