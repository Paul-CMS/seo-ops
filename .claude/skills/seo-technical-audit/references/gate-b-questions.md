# Gate B — The Clarification Stop

Sits between Analysis and Review. It exists so that unresolved evidence questions get
answered before they become recommendations — and so that everything else does **not**
become a question.

## The trigger test

A question is raised only if the answer would:

1. **Change a finding's severity**, or
2. **Change its direction** (the finding is wrong, not just imprecise), or
3. **Determine whether a destructive recommendation is viable.**

Everything else is not a question. It is a row in Assumptions & Limitations.

Without this test the gate fails in one of two directions: forty questions nobody
answers, or none at all with assumptions buried in the findings. Both are worse than the
gate not existing.

## Routing

Two destinations. A third outcome, not a third route.

**Never ask anything the Agency Profile answers** — the crawler, the licence, whether
rendering was on, which tool produced which export. Those are standing facts. An agent that
asks is not reading the profile.

**VA — evidence integrity only.** Things the person who produced the export can answer:
- Was this export filtered, or is it the full crawl?
- What user agent and what date window?
- Is this the complete backlink set or a sample?
- Was the grid run at the recorded center and spacing?
- Can you re-run this export with X enabled?

The VA cannot answer business truth. Do not send them any.

**Paul — scope, direction, decisions.**
- Is this service line in scope?
- One entity or two?
- Do we treat this location as separate?
- Is the engagement covering the blog?
- Does this destructive recommendation get explored at all?

**Outcome, when Paul cannot answer:** he marks it `cannot answer — client`. The question
moves to the client-confirmation list, and every finding it blocks gets
`client_confirmation_required = Yes` and confidence `Assumed`. The skill does not decide
it and does not ask the client.

Every Paul-routed question therefore carries an explicit `cannot answer — client`
option. Without it, unanswerable questions stall the audit instead of routing.

## Format

One batch per route, capped at 8 questions each. Each question states:

- **Which finding IDs it blocks** — makes the cost of not answering visible
- **Why the answer changes the finding** — proves it passed the trigger test
- **A proposed default** — so most can be accepted at once
- **The consequence of that default** — what gets assumed if nothing comes back

```
Q3 · Paul · blocks F-014, F-015, F-022
Commercial pest control appears on 4 service pages but not in the Intake
service list. In scope?
  Why it matters: if out of scope, three "thin service page" findings become
  "remove candidate" instead, which is a destructive recommendation.
  Default: treat as in scope, findings stand as-is.
  If defaulted: F-014/015/022 carry confidence Assumed.
  [ ] default  [ ] in scope  [ ] out of scope  [ ] cannot answer — client
```

## When no question passes the test

No gate. Record "no questions — gate skipped" in `decisions.md`, then proceed straight to
Review. This is the expected outcome on a clean evidence set and should not feel like
something went wrong.

## When answers don't come back

Proceed on the stated defaults. Do not stall, and do not quietly promote an assumption
to a fact. Each defaulted question produces:

- an entry in `decisions.md` recording the default and the date it was applied
- confidence downgraded to `Assumed` on every affected finding
- a row in Assumptions & Limitations naming the assumption and its consequence

## What the gate is not

Not a place to ask the client anything. Not a second intake. Not a review of Analysis's
conclusions — that is Review's job, and doing it here contaminates the fresh-session
independence that makes Review worth running.
