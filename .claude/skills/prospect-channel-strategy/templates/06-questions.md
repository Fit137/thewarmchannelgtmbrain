# 06. Questions and the invitation, [Company]

The question is the reason a senior guest says yes. Not the host, not the venue, not the food. This page finds three candidate questions that are live for [Company]'s buyers right now, verifies each, and writes the sample invitation a guest would read, in guest words only.

time budget: 2 to 3 hours
method: reference/question-bank-method.md
audience of the invitation: the guest. Every other line on this page is client-facing.

## 1. Candidate questions

A live question is one the guest is working on this quarter, that peers answer differently, and that no vendor can answer for them. It is one line, it is about the guest's problem, never the host's product, and the host never chooses it.

| Label | The question, one line | For which roles | Why it is live now | Evidence | Verified |
|---|---|---|---|---|---|
| [Machine identities] | [How are you governing identities that now outnumber your people?] | [roles] | [three public signals] | [E##] | [yes or no] |
| [label] | | | | | |
| [label] | | | | | |

### The three-signal test

A question is verified when three independent public signals show it is live: a conference agenda giving it sessions this year, a regulatory or standards change that forces it, an incident class in the news, practitioner discussion in the buyer's own communities, an analyst note. One signal is a guess. Unverified questions are cut before sending, or carried with "would be verified before any invitation goes out" in the copy.

### Questions that fail

- [Company]'s product category with a question mark on the end.
- Anything a vendor could answer in a demo.
- Anything that needs a guest to disclose their own security posture in a room of strangers.
- Anything that asks the guest to evaluate a vendor.

Note for the deck: Each question would be verified as live before any invitation goes out. The host never chooses the question.

## 2. The sample invitation

A sample, shown to [Company] so it sees how its guests would be treated. Guest vocabulary only: the question, peers, the evening, the host. No client word. No promise frozen by D11: never "your details go to no one" or "nothing follows". The approved line is "No attendee list is circulated, before or after."

<!-- guest-copy:begin -->
Subject: [One question, one evening]

[The question, as the first line.]

[Who else is coming, by role and organisation type, never by name: "I am putting a small number of security leaders who are working on it around one table."]

[The host, disclosed: "The host is paying for the evening. They did not choose the question, and they are not presenting on it."]

[The format: "No deck, no panel, no stage time. No attendee list is circulated, before or after."]

[The ask: "Reply yes or no. Either is a fine answer."]
<!-- guest-copy:end -->

Side note for the deck, client-facing: A sample in the language your guests would read. It never describes them as a target. Your guests are treated as guests.

## Done when

- Three candidates, at least two verified by three signals each, every signal in the register.
- The invitation sits between the guest-copy markers and passes `python3 scripts/lint_claims.py` from the brain, run on the workspace.
- The invitation names no person, no attendee, and no client word.

## Into strategy.json

`questions` (label, question, for, why_live, evidence), `questions_note`, `invitation.subject`, `invitation.body` (paragraphs separated by a blank line), `invitation.note`.
