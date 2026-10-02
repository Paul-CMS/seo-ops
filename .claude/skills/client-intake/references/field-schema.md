# Field Schema

## Contents

1. The three classifications
2. Block A — Confirm
3. Block B — Verify this claim
4. Block C — We need from you
5. Access items
6. Internal-only fields
7. Fields to deliberately not collect

---

## 1. The three classifications

Every field gets one of three treatments on the client sheet. The classification is
fixed per field type — it does not depend on how confident discovery was.

**Block A — Confirm.** Pre-filled, scannable, bulk-approvable. These are facts that are
either publicly verifiable or low-stakes if slightly wrong: address, hours, phone,
service list, service area. If it's wrong, the client fixes it; if it's wrong and they
miss it, nobody gets sued.

**Block B — Verify this claim.** A claim the business is *already making publicly*,
quoted back with its source, requiring an explicit yes or a correction. Never
bulk-approvable. These are the fields where being wrong is a real problem — legal,
financial, or trust claims. The point of quoting rather than pre-filling is that it
shifts the frame from "is this right?" to "you are currently saying this in public — is
that true?", which gets a much more careful answer.

**Block C — We need from you.** Genuinely blank. Either discovery found nothing, or the
field is on the never-pre-fill list and the business makes no public claim about it. A
blank forces an answer. A plausible guess gets approved.

**The governing rule:** if a field is in Block B or C, it stays there even when
discovery is confident. Confidence is not the criterion — consequence-of-being-wrong is.

---

## 2. Block A — Confirm

Pre-fill all of these. Mark each with its source so the client can see where it came
from.

### Identity and location
- Business name as it should appear in content
- Primary address
- Address type: office clients visit / yard or shop, no walk-ins / home-based
  *(this drives storefront vs. service-area-business treatment and is worth getting
  right — infer from GBP, then confirm)*
- Mailing address if different
- Additional locations

### Contact
- Primary phone (and flag if it looks like a tracking number)
- Secondary / after-hours number
- Email addresses, and which one reaches a human
- Contact form destination
- Booking or scheduling link

### Hours
- Regular hours by day
- Seasonal variation
- Holiday closures
- Whether "24/7" on the site means dispatch or just voicemail
  *(this one is worth a specific line — it's a claim that gets tested by real callers)*

### Services
Present as a checklist built from the current site, each marked ✓ keep / ✗ dropped / ➕ missing.
- Every service found on the site
- Service categories and how they nest
- Services found on GBP but not the site, and vice versa
- Two extra columns worth including: **"want more of"** and **"stop getting calls for"**.
  This is the single most commercially useful thing on the sheet and costs the client
  ten seconds.

### Service area
- The furthest town served in each direction, not a ZIP list
- Named cities and counties currently claimed on the site
- Anywhere they explicitly will not go
- Whether they charge a travel fee beyond a radius

### Digital presence
- Website platform and where it's hosted
- Social profiles found
- Review profiles found, with counts
- Directory listings found
- Any duplicate or stale GBP listings discovered — flag these prominently

### Brand
- How the name should be written (ampersand vs "and", LLC included or not, capitalization)
- Tagline currently in use
- Logo files available
- Brand colors as found

---

## 3. Block B — Verify this claim

For each of these, if the business already makes the claim publicly, quote it verbatim
with the URL, and require an explicit response. If they make no such claim, the field
moves to Block C as a blank.

Format each as: *"Your [source] currently says: '[exact claim]'. Is this accurate?"*

- **Founding year / "serving since" / years in business** — the most commonly wrong
  claim on local sites, and the easiest to disprove. Cross-check against Secretary of
  State registration and GBP open date; if they disagree, say so on the sheet.
- **Ownership continuity** — "family owned since 1985" is different from "bought the
  business in 2019." Both are fine; only one is true.
- **License numbers and license classes**
- **Insurance and bonded status**
- **Manufacturer certifications, authorized dealer status, factory training**
- **Trade association memberships**
- **Warranty terms** — length, what's covered, transferability
- **Guarantees** — response time, on-time arrival, satisfaction, price match
- **Awards and rankings** — especially anything with "#1" or "best"
- **BBB rating and accreditation**
- **Team size, truck count, jobs completed, customers served**
- **Years of individual staff experience**
- **Financing availability, provider, and terms**
- **Free estimate claims** — including whether free means free, or free-if-you-book
- **Emergency / 24-7 availability**
- **Pricing claims** — "starting at," "flat rate," "no overtime charges"
- **Anything superlative**: fastest, largest, only, most trusted, highest rated

If a claim is unverifiable *and* legally loaded (licensing, insurance), note on the sheet
that content won't publish it without confirmation. That's not a threat, it's the actual
constraint, and clients respond to it.

---

## 4. Block C — We need from you

Genuine blanks. Keep this block under about 10 items or completion rates fall off.
Prioritize in this order:

### Documents to forward (easiest — no composing required)
- Certificate of insurance
- License copies
- Any certification documents
- Logo files, vector if they have them
- Photos: truck wrap, storefront, crew, completed work

### Facts nobody publishes
- Legal entity name exactly as registered, plus DBA if different
- Minimum service call or trip charge
- What happens to a call at 7pm on a Saturday — real answer, not the marketing answer
- Average response time in practice
- Payment methods accepted
- Whether they subcontract any of the listed services

### Positioning (one text box each, and tell them a sentence is enough)
- What do you do that the other shops in town don't?
- What's the job you most want more of?
- What's the most common thing customers get wrong about your trade?

That last question is disproportionately productive and is often the only free-text
question worth including.

### People
Names, roles, and headshots only. Nothing else. Credentials, tenure, and bio content
come out of the interview process, not this sheet.

---

## 5. Access items

Track these separately from the content fields — they're the only genuinely blocking
part of intake, and they should go out first and get chased independently.

For each: owner, status, and "don't know" as an explicitly permitted answer, because it
usually is the answer.

- Google Business Profile — manager access
- Domain registrar
- DNS, if separate from the registrar
- Hosting
- CMS admin
- Google Analytics
- Google Search Console
- Google Tag Manager
- Call tracking platform, if any
- Review platform logins
- Social account admin
- Email/marketing platform

Two recurring realities worth designing for: the GBP is often owned by a previous
marketing company, and the domain is often registered to a personal Gmail the owner no
longer uses. Both are better discovered in week one than week six, so ask plainly:
*"Who set this up originally — you, or someone you hired?"*

---

## 6. Internal-only fields

Present in the record, never on the client sheet:

- Every conflict found during discovery, with all candidate values and sources
- Existing site claims that will need removing if the client can't substantiate them
- Competitor set
- Crawl-derived technical findings
- Engagement tier, stage plan, target MSA
- Anything from the sales call
- Confidence and source metadata

---

## 7. Fields to deliberately not collect

Leaving these out is what keeps the sheet under ten minutes.

- Anything you can read off the website — that's discovery's job
- Keyword targets and competitor lists — the client's guesses here are usually wrong
  and then they're invested in them
- Long-form brand voice questionnaires
- Target customer personas
- Anything about goals phrased as "what does success look like" — ask this on a call if
  at all
- Content topics — this is the interview's job
- Anything you would not actually use in the next 60 days
