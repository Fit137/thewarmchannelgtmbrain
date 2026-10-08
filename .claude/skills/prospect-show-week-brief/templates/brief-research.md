# Show-week research, [Company], [Prospect ID], [Show]

The working notes behind the brief. Every line that reaches the page traces to a row in `evidence/evidence-register.md`. Method: `reference/method.md`. Time budget: about half a day.

date: [YYYY-MM-DD]

## 1. Gate and timing

| Check | Answer |
|---|---|
| Gate verdict and total, from gate.py | [GO or HOLD, n of 18] |
| Event spend score | [2 or 3. Under 2, no brief] |
| Disqualifiers | [none] |
| Weeks from today to the first day of the show | [n] |
| Already approached with any gift, and no reply? | [no. If yes, stop: one approach per prospect] |
| On a GO with 8 weeks or more: brief or full strategy, and why | [one line] |

## 2. The show

| Field | Finding | Register |
|---|---|---|
| Name, edition and dates | [name, year, first and last day] | [E##] |
| Their presence | [booth and stand, sponsorship tier, breakfast, speaking slot] | [E##] |
| The audience, as the organiser publishes it | [the prospectus line, with any count] | [E##] |
| Opening and closing times | [the first morning, the last afternoon] | [E##] |

## 3. The week, slot by slot

One row per thing announced, and one per slot searched and found empty. Parts: breakfast, morning, lunch, afternoon, evening, late. Kinds: yours, open, session, official, competitor, side, partner.

| Day | Part | Time | Kind | What, in one line | Register |
|---|---|---|---|---|---|
| [Mon 23 Nov] | [evening] | | [open] | Nothing announced | [E## recording where we looked] |

Where we looked for side events, and found what: [the organiser's agenda and sponsor page, each competitor's events page, the associations' calendars, public event listings for the city and dates]. Read on: [date]. This date becomes `open_as_of`.

## 4. Where their buyers will be

Two to four sessions their buyer roles will attend, by title and track, never by speaker.

| Session | Day and time, track | Why their buyers are in it | Register |
|---|---|---|---|
| [title] | [Tue 24, 11:00, identity track] | [one line, in their words] | [E##] |

## 5. What already competes for their evenings

| When | Host | What, as announced | Register |
|---|---|---|---|
| [Wed 25, evening] | [Competitor A] | [an invitation-only dinner, announced on their events page] | [E##] |

Public facts only. Never a competitor's results, budget or intentions, and never a judgement of their event.

## 6. Still open

| When | Why it matters to them | Register |
|---|---|---|
| [Mon 23, evening] | [the evening before the floor opens, nothing announced against it] | [E##] |

## 7. The question the week is asking

The live question the agenda shows, by the strategy skill's three-signal test where time allows, one signal at least: a session on it this year.

- Question: [How are you ..., now that ...?]
- Why: [the session or sessions that show it is live]
- Register: [E##]

## 8. One suggestion

From `reference/suggestion-menu.md`. One, never a menu.

| Field | Answer |
|---|---|
| Title | [A private table on the evening before the show] |
| Body, two or three sentences | [what, when, for whom, on which question, and why that slot] |
| Format and cleared rate | [Invite-only executive dinner, 0.70, ledger row 11] |
| Seats, and the confirmations it implies | [12, about 17] |
| Timing, said plainly | [what the weeks left allow, and the honest fallback] |
| Status, wherever our work is described | [approaching guests on their behalf opens once our privacy position is written] |

## 9. What only they know

- [Who from their team is in town, and on which days: {TBD}]
- [Meetings already booked for the week: {TBD}]
- [Which of their named accounts will be at the show: {TBD}]

## 10. Before you send

- [ ] `validate_brief.py` clean, warnings answered
- [ ] Open slots re-checked within the last seven days
- [ ] `build_brief.py` with `--pdf`, and the PDF is two pages
- [ ] `brief_check.py` with `--brief`, `--register` and `--pdf` clean
- [ ] Read on a phone and in print
- [ ] The brain's `ops/QA-checklist.md` client blocks
- [ ] Sent once, privately, as a noindex link or the PDF, never an HTML attachment. Logged: `[date] | brief v1 sent | [format, link path, take-down date]`

## Into brief.json

`gate`, `show`, `kicker`, `headline`, `standfirst`, `days` (date, label, note, slots with part, time, kind, title, evidence), `buyer_sessions`, `competing_evenings`, `open_slots`, `open_as_of`, `question`, `suggestion`, `unknowns`, `next_step`, `cta`, `sources`, `method`, `before_you_send`.
