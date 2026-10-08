# Lead magnets, the coverage read, the calculator, the scorecard

Load for: building, editing or offering any top-of-funnel asset. Distils Run A Phase 1 step 1.6, the lead magnet specification, the ROI calculator and the copy notes.

## 1. The coverage read, READY

The human version and the hinge of the funnel. Template: `templates/coverage-read.md`.

- **Input**: the prospect's named target account list, for one segment and one title.
- **Output, one page**: how many accounts have a reachable decision maker at the target title, which events those people already attend, what a realistic audience from that list looks like, and whether the gap is coverage or access.
- **Never**: names an individual before an engagement, predicts who would accept, or says anything about what The Warm Channel would deliver.
- **Cost**: founder time, 3 to 5 days per full read in the 2026-09-18 estimate. The one-segment sample is lighter. Reserve full reads for qualified prospects.
- **Founding offer**: "Free coverage read on your named accounts." Scope and turnaround are D13.

## 2. The ROI calculator, READY as logic, pre-ship fixes required

Built in `pages/roi-calculator.html` (source: `sources/raw/warmchannelgtmbuild/landing-page/roi-calculator.html`). Inputs: average deal size, close rate from a qualified first conversation, current cost to acquire a customer, engagement fee, qualified conversations needed. Outputs: ROI multiple, cost per qualified conversation, expected new customers and first-year revenue, cost to acquire, and a comparison against outbound benchmarks. It turns the figure `#6E2A2A` and says so in words when the answer is bad.

**The rule it embodies**: every conversion input is the client's. We supply only the fee and the scope. "If the numbers do not work, it will say so."

**Pre-ship fixes**, found 2026-10-07:

| Problem | Why it breaks a rule | Fix |
|---|---|---|
| Opens pre-filled: deal $120,000, close rate 10%, CAC $28,000, fee $24,000, 12 conversations, showing a 5.0x result on load | A result built from numbers we supplied is the illustration Phase 9 forbade | Empty inputs, no result until the user types |
| Fee default $24,000 | Reads as a price while D2 is open | Empty, labelled "the number we quoted you" |
| "Use industry benchmark, 30%" button | Figure 32, grade C, from companies that sell executive events | Remove, or label as agency-sourced and not ours, per the 2026-09-20 decision |
| "How many the programme is scoped to produce" | Implies a promised quantity, D4 | "How many qualified conversations you would need" |
| Money inputs are `type=number`, no thousands separators | Readability | Text input that formats on blur, already noted in the build |
| Comparison rows assign $800 to $2,500 to both cold email and ABM | The source range is not split by channel | Label as enterprise cost per meeting, one row |

## 3. The coverage scorecard, IN BUILD

The self-assessment version, for ScoreApp. The 2026-09-18 "Room Readiness Scorecard" is stale: its questions ask about Canadian financial services accounts and Greater Toronto Area decision makers. Keep its structure and rebuild the wording.

**Keep**:
- Seven questions out of 100. Questions 1 to 3 sum to **coverage**, 4 to 6 to **access**, 7 to **capacity**.
- **The result names whichever of coverage or access is weaker**, in plain words. That branch is the whole intelligence. "Only four of your fifty accounts have a reachable decision maker at that title" teaches something. "Your score is 42" does not.
- **Scale direction inverted**: a low score is the problem, so the strongest call to action sits at the bottom of the range.
- Tiers: 0 to 39 at risk, book the free coverage read. 40 to 69 workable with work, get the confirmation arithmetic. 70 to 100 ready, the constraint is capacity.
- Question 7, who does the outreach today, is read as a resourcing fact, never a competence judgment.
- The result page never contains a Warm Channel figure, a testimonial, a logo, a close rate, or a claim that we would have filled it. The Clutch 70% may appear, attributed, as a category benchmark.
- It asks the client about the client's own list and collects nothing about guests.

**Rebuild**: question 1 for the segment rather than Canadian financial services. Question 2 from "share with a GTA decision maker" to "share with an identifiable senior decision maker at your target title". Every "room" to "event". Name it the coverage scorecard.

**Consent**: completing it with an email is express consent, the cleanest position available. **The four-email sequence cannot go live without a mailing address, so it waits on D1.** Email 1 result and arithmetic, email 2 the confirmation arithmetic, email 3 coverage against access, email 4 a final note that offers the read once more and stops. No email contains a case study, testimonial, named client, figure of ours or the founder's record.

## 4. The prospect channel strategy and its branded deck, READY as method

Decided 2026-10-08. The event portfolio teardown taken all the way: for one named priority prospect, its own in-person year mapped from public information and rebuilt as a channel around its named accounts, then packaged as an interactive deck in its own branding. Built with the skills `.claude/skills/prospect-channel-strategy` and `.claude/skills/prospect-deck-builder`.

- **Who gets one**: a company that passes the gate: six criteria from `reference/icp-client.md` scored 0 to 3 on public evidence, GO at 12 of 18 with ACV and event spend at 2 or more. Never more than two in flight.
- **What it contains**: the event footprint scored for buyer density and access, the anchor moment, the committee and account tiers, one decision per moment, formats and a twelve-month calendar, live questions and a sample invitation, the confirmation arithmetic, the economics with a calculator the prospect fills in, and three ways to run it, one of which is us.
- **What it never contains**: a number about the prospect that the prospect did not supply, a grade C figure, a reply rate beside the 70% benchmark, a price, a promise, a client, or a described hand-over after the evening.
- **Cost**: two to four founder days per strategy. That cost is why the gate exists.
- **Delivery**: one researched approach from the founder to one person, as a private noindex link or a PDF. Never published, never reused for another company, never followed up after a non-reply.
- **Where it leads**: a call with their numbers, the full coverage read on their list, and version 2 of the strategy, built on what they supplied.
- **Privacy**: each prospect's workspace lives outside this repository. This brain holds the prospect's ID in `ops/pipeline.md` and nothing else.

## Rejected for every magnet

Anything that promises a lead count, a meeting count or a named attendee, or that collects anything about the guest side.
