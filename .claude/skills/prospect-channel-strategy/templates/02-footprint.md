# 02. Event footprint audit, [Company]

Every public in-person moment in [Company]'s year, read for two things: how many of its new buyers are in the building, and how much time across a table it gets with them there. The gap between the two is the strategy. The moment with the widest gap is the anchor.

time budget: 3 to 5 hours
window: [month year] to [month year], twelve months back and forward from today
sources: public only. Every moment cites the register.

## 1. Inventory

List every moment. Look in this order, and record where each one was found:

1. Their events page, newsroom and blog, and their company page's events tab.
2. Exhibitor, sponsor and speaker pages of the segment's main shows. Name the shows first, then check each one for [Company].
3. Agendas of the segment's conferences, for speaking slots.
4. Their own conference, user group, roadshow or customer summit.
5. Partner and alliance pages, for co-hosted or partner events.
6. Hosted dinners, receptions or roundtables they announced publicly.

Webinars and virtual events are recorded on the last line and kept off the map. They are not in person.

| ID | Moment | Kind | Their role | Month | Week | Today, in one or two words | Evidence |
|---|---|---|---|---|---|---|---|
| M1 | [name] | [trade show, conference, breakfast series, own conference, roadshow, hosted dinner] | [exhibitor, sponsor tier, speaker, host, co-host, attendee] | [1 to 12] | [1 to 4] | [Booth, Sponsorship, Attendee seats, Your conference] | [E##] |
| M2 | | | | | | | |
| Virtual, off the map | [webinar series and similar] | | | | | | [E##] |

A moment that repeats (a breakfast in February and November) gets one row per date, and the second points at the first with `same_as`.

## 2. Score density and access

Two axes, each from -20 to +20, read to one decimal. Round numbers hide judgement: write 7.3, not 7.

- **Density, new buyers in the room.** How many of [Company]'s not-yet-customer buyers, at the titles that matter, are in the building. Read from the organiser's published audience profile, the event's size and segment, and whether [Company]'s buyer titles are its audience. Positive: buyers in numbers. Negative: mostly customers, partners, or the wrong titles.
- **Access, time across a table.** How much uninterrupted, chosen conversation [Company] gets with those buyers there. A booth is negative: whoever walks past, for minutes. A sponsorship with a keynote is near zero: attention, not conversation. Their own conference and a hosted dinner are positive: time, and they choose who.

| ID | Moment | Density | Access | Why, in one line each |
|---|---|---|---|---|
| M1 | [name] | [-20.0 to 20.0] | [-20.0 to 20.0] | [density reason. Access reason] |

Use `scoring-rubrics.md` for the anchor points of each scale. Positions are our reading of public information, not measurement, and the deck says so.

## 3. Quadrants

```
                 ACCESS, time across a table (+20)
                               |
      KEEP FOR CUSTOMERS       |        BUILD ON
      good access, few new     |        buyers in numbers, and time
      buyers in the room       |        with them. Protect it
                               |
 FEW NEW BUYERS ---------------+--------------- NEW BUYERS IN NUMBERS
 (-20)                         |                              (+20)
                               |
      RECONSIDER               |        WRAP WITH A PRIVATE PROGRAMME
      few buyers, little time. |        the buyers are there and the
      Budget to redirect       |        time is not. The opportunity
                               |
                 ACCESS (-20)
```

| ID | Moment | Quadrant | Rationale |
|---|---|---|---|
| M1 | [name] | [Build on, Keep for customers, Reconsider, Wrap with a private programme] | [one line] |

The chart's quadrant names go into strategy.json in this order: top right, top left, bottom left, bottom right.

## 4. The anchor

The anchor is the moment in the bottom right with the widest gap between density and access, weighted toward the larger spend. Exactly one.

| Field | Answer |
|---|---|
| Anchor moment | [M#, name] |
| Map label | [the name plus today's format, for example "[Show] booth"] |
| Density minus access | [n] |
| Anchor line, a claim | Your buyers will be at [moment]. [The current format] is not where you get time with them. |
| Anchor body, one or two sentences | [what a private format in the same week does instead, without promising a result] |

If no moment sits in the bottom right, the footprint has no wedge. Record that, and consider the Lite profile or a HOLD.

## 5. The chart's claim

The quadrant slide's title is a claim the positions support, read from where the moments actually fell, for example "Your buyers are densest where your access is thinnest". Write it only after scoring.

- Quadrant title: [claim]
- Timeline title: [a claim about the year, for example "[Number in words] moments a year put [Company] in the same building as its buyers"]
- Basis line for the chart: Positions are our reading of public information, not measurement. New buyers means people in your segment who are not yet customers.

## 6. Chapter A, for the home layer and the deck

| Field | Line |
|---|---|
| Cover title | [a claim about what they already do well] |
| Cover subtitle | [what this deck reads, from the outside] |
| Claim | [the chapter's headline claim] |
| So what | [one line tying it to the ask: a change of method, not a new spend] |
| Evidence, line 1 | [the footprint fact, for example how many public moments] |
| Evidence, line 2 | Invite-only executive dinners attend at 70% of registered, vendor-owned conferences at 19% [n]. |
| Carry forward | [one line into deck B] |
| Close title | [returns to the cover] |
| Close body | [one line into the rest of the file] |

## Done when

- Every moment has a register row, a month and a week, a kind, a role and a today format.
- Every score has a one-line reason, and no score is a round number.
- Exactly one anchor, with its line and body written as claims the positions support.
- At least three moments on the map. Fewer is a HOLD or the Lite profile.

## Into strategy.json

`footprint.window`, `footprint.start_month`, `footprint.moments` (id, name, kind, role, month, week, today, density, access, evidence, anchor, map_label, label_pos, same_as), `footprint.quadrant` (title, x_label, y_label, names, range, basis), `footprint.timeline_title`, `footprint.anchor_line`, `footprint.anchor_body`, `footprint.chapter`.
