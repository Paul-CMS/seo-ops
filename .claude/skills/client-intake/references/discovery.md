# Discovery

The goal is a record where every field is either filled with a source attached, or
explicitly marked unknown. "Unknown" is a real answer and should be recorded as one —
an unmarked empty field is indistinguishable from a field nobody checked.

## Source hierarchy

When sources disagree, this is the order of authority. But note that a *lower*-authority
source disagreeing with a higher one is not something to silently resolve — it's a
finding. Record both.

1. **Government records** — Secretary of State entity registration, state contractor
   license boards, county business licenses. Authoritative for legal name, registration
   date, officer names, license status and expiry.
2. **Google Business Profile** — authoritative for what Google currently believes, which
   is what matters operationally even when it's wrong. Also gives an open date, category
   set, and service area as configured.
3. **The business's own website** — authoritative for what they claim, not for what's
   true. Everything here is self-reported.
4. **Third-party profiles** — BBB, Angi, Yelp, Thumbtack, Facebook, Nextdoor. Useful for
   cross-checking NAP consistency and finding claims that contradict the site.
5. **Reviews** — genuinely underrated. Reviews name staff, name services the site
   doesn't list, and reveal the actual service area from customer locations.
6. **Inference** — clearly marked as such.

## What to pull from each source

### Secretary of State / entity registry
Legal name, entity type, registration date, registered agent, officers, status (active /
delinquent / dissolved), any prior names. The registration date is the single best
reality check on "serving since" claims.

### State license board
License number, class, status, expiry, the name the license is held under, any
disciplinary history. The name on the license frequently differs from the trading name —
that mismatch matters for content.

### Google Business Profile
Name, address, phone, category (primary and secondary), hours, service area
configuration, open date, attributes, photos, Q&A, review count and average, whether
it's a storefront or SAB listing, and whether the profile looks actively managed.

Also search for **duplicate listings** — old addresses, a previous business name, a
listing created by a former marketing company. Duplicates are common and finding one in
week one is worth more than most of the rest of intake.

### Website
Every service page. Footer and header NAP. About page claims. Team page. Any trust
badges, certification logos, award graphics. Copyright year. Schema markup if present.
Whether the phone number in the markup matches the one displayed.

Note every factual claim you find, with the URL, because these populate Block B.

### Reviews
Read 20–30 recent ones across platforms. Extract: staff names customers mention,
services described that aren't on the site, towns customers are in, recurring complaints
(useful context, not for the sheet), and the owner's response voice if they respond.

### Social
Facebook is usually the richest for local trades — often has hours, service area
statements, and photos the website doesn't. Check the page's "Intro" and "About" fields
specifically, since those get set once and then forgotten, which makes them both a good
source and a common source of stale NAP.

## Assigning confidence

- `verified` — a government record or other authoritative third party states it
- `found` — the business states it publicly
- `inferred` — a reasonable deduction, e.g. address type inferred from the GBP listing
  type, or service area inferred from review locations
- `unknown` — checked, nothing found

Do not mark something `verified` because it appears on three sites the business
controls. That's one source repeated.

## Recording conflicts

Whenever two sources disagree on a Block B field, record all candidate values:

```yaml
founding_year:
  value: null
  conflict:
    - {value: 1998, source: "homepage hero", confidence: found}
    - {value: 2004, source: "GBP open date", confidence: found}
    - {value: 2011, source: "SC SOS registration", confidence: verified}
  classification: verify
```

Conflicts go on the proof sheet explicitly, showing the client all three values. This
looks blunt but it's the most useful thing on the page — it's a problem the client
didn't know they had, and presenting it that way is what makes the rest of the sheet
feel worth their time.

## Traps

**The site's phone number is a tracking number** from a previous agency, and it will
stop working when that account lapses. Check whether the number on the site matches GBP
and the one on the truck in their photos.

**The copyright year is not the founding year.** Neither is the domain registration date,
though it's a useful lower bound — a business claiming 1985 with a domain registered in
2019 is fine; a business claiming 1985 with an SOS registration in 2019 is a different
conversation.

**Service area on GBP is often set to a radius nobody thought about**, frequently the
default. Don't treat it as a statement of intent.

**"Family owned and operated"** appears on roughly every local site and is often
inherited from a template. Worth verifying, gently.

**A dissolved or delinquent entity registration** is not necessarily a problem — plenty
of operators let a registration lapse and trade under a different one. But it needs
asking about before content asserts anything about the corporate entity.
