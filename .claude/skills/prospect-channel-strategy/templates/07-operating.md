# 07. How a room fills, and what happens after, [Company]

The operating model, told honestly: the arithmetic that sets how many confirmations a table needs, the six weeks of individual work behind it, the evening itself, what happens after the evening, and how the result is reported. Every number here is either a cleared benchmark, attributed, or `{TBD}` for [Company] to supply.

time budget: 1 to 2 hours
method: reference/arithmetic.md

## 1. The arithmetic

Confirmations needed = people in the room divided by the format's attendance rate, rounded to the nearest whole person. Rates come only from the evidence ledger, cleared rows.

| Format | Attendance rate | Source | People in the room | Confirmations needed |
|---|---|---|---|---|
| Invite-only executive dinner | 70% | Clutch Events, ledger row 11, B plus | [12] | [17] |
| VIP or sport hospitality | 86% | Clutch Events, ledger row 12, B plus | [12] | [14] |
| Vendor-owned conference | 19% | Clutch Events, ledger row 12, B plus | [12] | [63] |

- Title mix: directors and above attend at 62%, technical individual contributors at 56%, with three times the no-show rate (Clutch Events, ledger row 13, B plus). Adjust the confirmation target for the mix.
- People approached: `{TBD}`, set by the coverage read on [Company]'s list. Never estimated from outside.
- Any floor is set against confirmations, never against invitations, and no floor is promised while D4 is open.
- The slide's title, in words: [Twelve] seats needs about [seventeen] confirmations. The format sets the arithmetic.

## 2. The six weeks

| Window | The work | What is counted |
|---|---|---|
| Weeks 6 to 4 | Research each named person and approach once, with the question in the first line. | Approaches made |
| Weeks 4 to 1 | Confirm, and tell everyone honestly who else is coming, by role. | Confirmations against target |
| The week | Reconfirm close to the date. Update anyone if the room changed. | Arrivals against confirmations |

Status, carried wherever this is described as our work: approaching guests opens once our written privacy position is in place, D5.

## 3. The evening

One question, set from what is live at the guests' organisations and named in the invitation. No deck, no panel, no stage time beyond a welcome. Nobody pitches from the floor, including the host. No photograph of the table. No attendee list circulated. [Company] hosts and contracts the venue, the catering and any production directly: The Warm Channel supplies none of them, by design.

## 4. After the evening

Post-event conversion and the guest promise are frozen until D11. The plan describes the step only in its consent framing, and never describes a mechanism:

- Title: After the evening, the conversation continues with the people who choose to continue it
- Body: After the evening, the conversation continues only with guests who choose it, and nobody is chased. How that step works is designed with you, and it is not offered until that design is settled.

Do not write: who receives what, when sellers call, what is passed on, or any line about what a guest said reaching the host.

## 5. Measures

| Measure | What it counts | Target |
|---|---|---|
| Named-account coverage | Named accounts with a senior person at a table | {TBD} |
| Arrived against confirmed | Arrivals over confirmations, per table | {TBD} |
| Qualified conversations | Conversations that continue after the evening, with guests who chose it | {TBD} |
| Opportunities opened | From those conversations, in your CRM | {TBD} |

Note for the deck: The report format is in development. Targets are set with you, from your own numbers.

## 6. Chapter D

| Field | Line |
|---|---|
| Cover title | A room fills by arithmetic. The conversation continues by consent. |
| Cover subtitle | The confirmation maths, the six-week window, the evening, and the step after it. |
| Claim | A room fills by arithmetic, and the conversation continues by consent. |
| So what | [Twelve] seats needs about [seventeen] confirmations at the dinner benchmark, and that is weeks of individual work. |
| Evidence, line 1 | Attendance depends on format: 86% for VIP and sport hospitality, 70% for executive dinners, 19% for vendor-owned conferences [n]. |
| Evidence, line 2 | Follow-through runs only with guests who choose to continue. |
| Carry forward | The work is real. The next question is whether it pays. |
| Close title | [returns to the cover] |
| Close body | Next: whether the economics work on your numbers. |

## Done when

- Every rate cites its ledger row, and the confirmations are rounded, not ceilinged.
- The approached count is `{TBD}`.
- The after-the-evening lines are the consent framing, with no mechanism.
- Every capability that is not READY carries its status in the sentence that describes it.

## Into strategy.json

`operating.arithmetic` (seats, formats with label and rate as a fraction, source_n, approached, approached_label, note), `operating.six_weeks`, `operating.after` (title, body), `operating.measures`, `operating.measures_note`, `operating.chapter`.
