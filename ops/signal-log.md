# Signal log

Raw market input, captured before judgment. Every signal from a prospect, client, guest, partner, competitor, research pass or our own production work lands here first, whatever it turns out to mean. Newest at the top.

Capture is cheap on purpose. A signal debated before it is written down does not get written down.

**Keep the verbatim.** Never paraphrase a buyer into house vocabulary. The words a real buyer used before we taught them ours are the most valuable thing a signal carries, and they cannot be recovered later. **No personal data**: name the source by role and organisation type, never by name or email.

## How to use this file

**Types:** OBJECTION, LANGUAGE, PROOF, STATUS, COMPETITIVE, SEGMENT, CHANNEL, LOSS, RISK.

**Dispositions:**
- `NOISE`, one instance, no pattern, no action. Logged and closed.
- `WATCH (n/N)`, a plausible pattern awaiting corroboration. Increment as instances arrive.
- `PATCH`, changes copy, not strategy. Route it, edit, done. No decision entry.
- `AMEND`, changes a ledger, a position, the ICP, the channel mix or a rule. Full amendment procedure and an entry in `ops/decisions.md`.

**Corroboration thresholds** (proposed 2026-10-07, founder to confirm in `ops/gap-interview.md`):

| Signal class | Threshold to act |
|---|---|
| Opinion, preference, language, objection | 3 independent instances within 60 days |
| Verifiable fact: status, proof, competitive, risk | 1 verified instance, act immediately |
| Loss reason | 2 instances, or 1 if the prospect met all five ICP characteristics |
| Channel performance | A full measurement cycle, never a single week |
| Guest-side trust signal: a complaint about being sold to, listed or chased | **1 instance, act immediately.** The guest relationship cannot absorb a second |

Default disposition is NOISE. A brain that amends on every input has no memory. Triage runs weekly, see `ops/review-cadence.md`. A WATCH that has not incremented in two cycles expires to NOISE, and the expiry is written here.

---

## Entries

### 2026-10-22 | CHANNEL | Founder, outreach result and a new angle under test
**Verbatim:** "I reach out initially for companies that are not hosting to make them host, and I see a poor reply rate. Instead, I want to reach out to companies who already use events as a channel." Also: "Override the brain strategy for now. This is a new angle that I'm testing."
**Context:** A founder test, not a decision. The angle targets event organisers and companies that already run ticketed, sponsored events, offering a faster route to paying attendees, sponsors, exhibitors and speakers. It conflicts with the 2026-09-22 positioning (the client is a vendor that hosts, and the guest pays nothing) and with the competitor map, where hosted-buyer and summit operators sit. The reply rate was reported without send counts, so it has no denominator yet. The target list for the test was researched outside this repository and holds no personal data here.
**Disposition:** WATCH (1/1), channel performance, read after a full measurement cycle with sends and replies counted. Adopting the angle needs the full amendment procedure, starting with a decision brief. Not DECIDED.
**Routed to:** none yet.

### 2026-10-08 | STATUS | Founder, a second gift for leads
**Verbatim:** "Show-week brief let's do this one."
**Context:** Chosen from a shortlist of lighter value-first gifts: one page about the week of a show the prospect already funds. Sized for a short runway or a HOLD, where the full strategy does not fit.
**Disposition:** AMEND
**Routed to:** `ops/decisions.md` entry of 2026-10-08, `rules/service-status.md`, `.claude/skills/prospect-show-week-brief/`.

### 2026-10-08 | STATUS | Founder, a new lead magnet
**Verbatim:** "The concept here is giving free value for a high-value lead. If I find a company that is highly qualified, I want to create their event strategy and share it with them using their own branding."
**Context:** An internal decision rather than market input, captured here first so the amendment trail starts in the usual place. It turns the event portfolio teardown variant into a full, gated, per-prospect strategy and deck.
**Disposition:** AMEND
**Routed to:** `ops/decisions.md` entry of 2026-10-08, `rules/service-status.md`, the two new skills in `.claude/skills/`.

### 2026-10-07 | RISK | Brain build, live test
**Verbatim:** First draft of the category post said the two event types shared "the same buyers, often the same month", and that "most event plans skip" the arithmetic.
**Context:** Phase 9 live test, client audience, awareness. Neither claim is in the benchmark or the evidence ledger. The QA checklist caught both.
**Disposition:** PATCH
**Routed to:** `examples/linkedin-category-post.md`. Lesson: plausible framing around a real figure is where fabrication enters. The Claims block catches it only if run line by line.

### 2026-10-07 | RISK | Brain build, review of the ROI calculator
**Verbatim:** Inputs pre-filled "120000", "10" %, "28000", "24000", "12", result "5.0x" on load. Button "Use industry benchmark, 30%". Label "How many the programme is scoped to produce."
**Context:** `pages/roi-calculator.html`. A result built from our numbers is the illustration the 09-18 decision forbade. The fee default reads as a price while D2 is open.
**Disposition:** AMEND, via D16
**Routed to:** `rules/do-not-say.md` calculator rule, `reference/lead-magnets.md`, `pages/landing-page.md` item 17.

### 2026-10-07 | RISK | Brain build, review of the landing page cost table
**Verbatim:** The page lists cost per lead for cold email, LinkedIn ads, in-house SDR, trade show and ABM. The source, Growth Spree and OpGen Media 2026, also lists "in-person events $400 to $1,200, median $650".
**Context:** Omitting the row for the channel being sold is a cherry-pick any prospect who opens the source will see.
**Disposition:** AMEND, via D16
**Routed to:** `rules/do-not-say.md` scoping, `pages/landing-page.md` item 15.

### 2026-10-07 | RISK | Brain build, cross-reading POSITIONING against Run B
**Verbatim:** Landing page: "Qualified and handed over to your sellers with the context of what was actually said." Run B guest drill 8: "Your details are not passed to the host or to anyone else."
**Context:** The hero client component contradicts the guest promise that wins the second acceptance.
**Disposition:** AMEND, opened D11
**Routed to:** `ops/decisions.md` D11, `rules/service-status.md`, `reference/value-proposition-guest.md`, `reference/engagement-playbook.md`.

### 2026-10-07 | RISK | Brain build, brand name read from the guest side
**Verbatim:** POSITIONING: "A warm channel is exactly what this is: a lead generation channel whose output is warm."
**Context:** Under the new meaning, the brand name as a sender tells a guest what they are to the host.
**Disposition:** AMEND, opened D12
**Routed to:** `ops/decisions.md` D12, `rules/two-vocabularies.md`.

### 2026-09-22 | SEGMENT | Practitioner commentary, cybersecurity events, grade C opinion
**Verbatim:** Big-booth return "is just not there," while targeted meeting programmes before, during and after an event do produce pipeline.
**Context:** Cited in POSITIONING as a third party describing this product without knowing it exists. Not a buyer of ours.
**Disposition:** WATCH (1/3)
**Routed to:** none yet. Two more independent instances from in-ICP buyers would promote it to customer language in `ops/copy-bank.md`.

### 2026-09-18 | COMPETITIVE | Search summaries, slot 1
**Verbatim:** ConvergeX is reported as guaranteeing "at least 50% of attendees book a post-event meeting", claiming a current average near 70%. CXO & Co described as offering guaranteed attendance plus post-event meeting support.
**Context:** Third-party summaries, grade C plus, unconfirmed on the operators' own pages.
**Disposition:** WATCH, awaiting verification. A fact, so one verified instance is enough to act, research R4
**Routed to:** `reference/competitor-battlecards.md` with the unconfirmed marker, `reference/objection-handling.md`.

### 2026-09-18 | COMPETITIVE | Review text and search summaries, slot 1
**Verbatim:** The Ortus Club, clients describe it as "charging only for attendees who show up". MyOutreach: "confirmed before billing", "no-shows are never charged".
**Context:** Pay-on-attendance is a category norm among the better operators.
**Disposition:** AMEND, applied 09-18
**Routed to:** `rules/do-not-say.md`: never sold as our differentiator against agencies.

### 2026-09-18 | COMPETITIVE | Step 0 slate correction
**Verbatim:** "Attendir is a self-serve attendee advocacy platform that turns registered attendees into LinkedIn promoters."
**Context:** The brief had placed it in slot 1. It is software, slot 2.
**Disposition:** PATCH, applied
**Routed to:** `reference/competitive-analysis.md`.

### 2026-09-18 | SEGMENT | Research step 2.7, attendee side
**Verbatim:** "68% of CISOs report aggressive marketing makes it near impossible to tell genuine innovation from AI-washing." Category commentary: a CISO "can recognise a lead-generation dinner from the subject line."
**Context:** C plus. Supports both sides of D8: unreachability and saturation.
**Disposition:** WATCH (1/3), feeds research R1
**Routed to:** `reference/icp-client.md`.

### 2026-09-18 | RISK | Founder history, from the claim constraints
**Verbatim:** The founder's prior record "includes three accepted guests who did not appear and a room cancelled four days out."
**Context:** Real show-rate evidence for D4. The brief says to model the floor on the worst show rate actually produced.
**Disposition:** AMEND, applied
**Routed to:** `rules/do-not-say.md` historical section, D4.

---

*An empty signal log after a month of selling means the loop is not running. Every discovery call, every guest reply and every partner conversation produces at least one entry.*
