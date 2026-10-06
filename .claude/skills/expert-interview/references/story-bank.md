# Story bank — format

One file per client: `clients/<slug>/interviews/story-bank.md`. Append-only in practice: entries
change only in **Publish** and **Status**. `python3 scripts/interview.py check <slug> bank` checks it.

```
# <Client> — Story bank

## S-001 · <headline in plain words>
- Date: 2026-11-04 · Round: 2 · Speaker: <name>, <role>
- Type: unusual_case | misconception | local_condition | process_detail | cost_factor | customer_question | decision_criterion | objection | terminology
- Quote: "<verbatim from the transcript>"
- Specificity: 4
- Tags: crawl space, older homes, Hanover
- Publish: public | framing-only | internal
- Status: fresh | used (<post id>, <date>) | retired
- Flags: fact? (a business fact — goes to the facts track) | sensitive
```

Rules
- **IDs** are `S-` + three digits, never reused.
- **Specificity 3–5 only.** 1–2 becomes a follow-up question, not an entry (extraction-rubric.md).
- **Publish:** `public` = the specifics may appear in a post · `framing-only` = use the lesson, never
  the identifying specifics (names, addresses, exact prices) · `internal` = background only, never on a
  page. When unclear, `framing-only` and ask Paul.
- **Status:** a blog brief lists the IDs it uses ("Story bank entries used: S-007, S-012"); when Paul
  approves the post, those entries become `used (<post id>, <date>)`. A `used` story is not the centre
  of a second post for 6 months; after that it may be `retired` or reused with a new angle.
- **Health-adjacent clients (CM-040):** a story that makes a health claim keeps the quote but is
  flagged `sensitive`; a post may use it only with a named authoritative source.
- **Never** a reviewer's name or a customer's personal detail (CM-027).
