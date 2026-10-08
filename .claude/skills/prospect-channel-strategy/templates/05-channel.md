# 05. Channel strategy, [Company]

The plan. One decision per moment [Company] already funds, the formats that carry it, a twelve-month calendar, and the carrying line: the one sentence the whole file exists to land. The default posture is to keep what they fund and add the conversations around it. A plan that starts by cutting their flagship reads as an attack on the person who chose it.

time budget: 2 to 4 hours
inputs: 02-footprint.md, 03-buyers.md, 04-landscape.md, reference/event-formats.md

## 1. One decision per moment

Read each moment's quadrant and decide. Four verbs, each with its default:

| Quadrant | Verb | Default recommendation |
|---|---|---|
| Wrap with a private programme | Keep, and wrap | Keep it, and add private tables for named accounts the same week |
| Build on | Keep, or upgrade | Protect it. If the time comes without a choice of who sits down (breakfast seats), turn the same slot into your own table |
| Keep for customers | Keep, and add | Keep it for customers, and add an expansion table, apart from prospects |
| Reconsider | Redirect | Move the budget into the plan's own tables. Say what it buys instead |

| Moment | Today | Recommendation, one line | Quadrant |
|---|---|---|---|
| [M#, name] | [Booth] | [Keep, and wrap with two private tables that week] | [quadrant] |

The anchor's row comes first. It is the row the deck highlights.

## 2. Formats

Two to four formats, chosen from `reference/event-formats.md` for what each moment can carry. Each format gets a name the deck can use and one line.

| Format | One line for the deck | Where it fits | Seats | Attendance benchmark |
|---|---|---|---|---|
| [Show-week tables] | [Small private tables during [show], for Tier 1 committees already in town.] | [M#] | [12] | [70%, invite-only executive dinner, Clutch Events] |

## 3. The calendar

Proposed moments, placed backwards from when the buyers are reachable, each with its outreach window before it. Keep the moments the plan keeps on the same strip, so the reader sees nothing they rely on was removed.

| Proposed moment | Month | Week | Around | Outreach window starts |
|---|---|---|---|---|
| [SecureCon tables] | [4] | [4] | [M#] | [six weeks before] |

- Moments kept on the calendar: [M#, M#]
- Outreach window, in weeks: [6]
- Calendar note for the deck: Placements are a proposal. [Any placement rule, for example: late summer and the weeks around year-end are avoided where possible.]

Placement rules: no proposed moment lands inside another of [Company]'s own events. No two proposed moments share an outreach window for the same tier. A metro table sits where public evidence shows Tier 1 accounts cluster, or it is not proposed.

## 4. What the plan deliberately does not recommend

Name each tempting idea that was rejected, and why. This is where the plan shows its judgement.

| Not recommended | Why |
|---|---|
| [a large hosted event at the show] | [the buyers are there for the show, and a large room is a rented audience again] |
| [cutting the flagship booth] | [it is the reason the buyers are in town] |

## 5. The carrying line

Three short sentences at most: keep, add, follow through. It becomes the deliberately still slide, the home layer's line and the deck's closing echo. Follow-through is always in the consent framing.

> [Keep the moments you already fund. Add private tables for your named accounts around them. Follow through with the guests who choose to continue.]

## 6. Chapter C

| Field | Line |
|---|---|
| Cover title | [a claim, for example: One budget, run as a channel.] |
| Cover subtitle | [one line] |
| Claim | [the plan keeps every moment and adds the conversations around it] |
| So what | [nothing they rely on is cut, the budget is redirected toward the accounts they named] |
| Evidence, line 1 | [the anchor recommendation] |
| Evidence, line 2 | [a second format] |
| Carry forward | [a plan is only as good as the right people who actually arrive] |
| Close title | [returns to the cover] |
| Close body | [one line into deck D] |

## Done when

- Every moment in the footprint has a decision, and the anchor's comes first.
- Two to four formats, each tied to a moment or to a public clustering signal.
- The calendar keeps their moments on the strip and gives every proposed moment its window.
- The carrying line fits in three sentences and holds the consent framing.

## Into strategy.json

`channel.choices` (moment, today, recommendation), `channel.formats` (name, line, fits, evidence), `channel.calendar` (label, month, week, around), `channel.keep_on_calendar`, `channel.window_weeks`, `channel.calendar_note`, `channel.timeline_title`, `channel.chapter`, and `thesis.carrying_line`.
