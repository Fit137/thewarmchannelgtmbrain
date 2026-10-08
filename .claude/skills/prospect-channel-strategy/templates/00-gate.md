# 00. Qualification gate, [Company], [Prospect ID]

A free strategy costs founder days. This page decides, from public evidence only, whether [Company] has earned them. Nothing else in the workspace is started until it says GO.

time budget: 30 to 45 minutes
date: [YYYY-MM-DD]
how they came to attention: [the signal, by type only: an exhibitor list, a partner introduction, a comment on a founder post, an inbound call]

## 1. Conflict check, before anything else

| Check | Answer | If yes |
|---|---|---|
| Inside the founder's separate healthcare business, its clients, its guests or its references? | [yes or no] | Stop. D6, a consent boundary |
| A conflict with an active engagement or a partner commitment? | [yes or no] | Stop and tell the founder |
| Already in the pipeline, declined, or approached in the last twelve months? | [yes or no] | Stop. One approach, never a second on the same question |
| Two strategies already in flight? | [yes or no] | HOLD for capacity. Two concurrent is the ceiling for one person |

## 2. Score the six criteria

Score each from 0 to 3 on one evidence scale. Start the evidence register now: every score cites at least one row.

- **3**, direct public evidence that it holds (a P1 or P2 row)
- **2**, indirect evidence, or an inference with its basis written down (a P3 row)
- **1**, no evidence either way
- **0**, evidence that it fails

| # | Criterion | Score | Evidence rows | The signal, in one line |
|---|---|---|---|---|
| 1 | Six-figure ACV and up | [0 to 3] | [E##] | [what was seen] |
| 2 | Already spends materially on events | [0 to 3] | [E##] | [what was seen] |
| 3 | The buyer is structurally unreachable cold | [0 to 3] | [E##] | [what was seen] |
| 4 | Already distinguishes warm from cold | [0 to 3] | [E##] | [what was seen] |
| 5 | Current event spend converts badly | [0 to 3] | [E## or none] | [usually unknown from outside, score 1] |
| 6 | A named account list exists, and someone owns events measured on pipeline | [0 to 3] | [E##] | [what was seen] |

### Where to look first, one quick signal per criterion

| Criterion | Quickest public signals | A 3 looks like | A 0 looks like |
|---|---|---|---|
| ACV | Pricing page, case studies, enterprise sales job posts, analyst category | Contact-sales pricing only, and case studies describing enterprise-wide rollouts | Self-serve plans with published prices under five figures |
| Event spend | Their events page, exhibitor and sponsor lists of the segment's main shows, an own conference, event or field marketing job posts | A booth, a sponsorship and an own event in the last twelve months | No in-person presence in twelve months |
| Unreachable cold | The buyer's title and segment, and what that buyer says publicly about vendor outreach | A C-level or head-of buyer in a regulated or high-security segment | A buyer who starts with a free trial |
| Warm and cold | Customer advisory boards, reference programmes, user groups, peer-reference language in case studies | A customer advisory board and prominent peer references | A pure self-serve motion |
| Converts badly | Job posts asking someone to "prove event ROI" or fix "event attribution", public talks about event fatigue, shrinking show presence | A public statement that event return is hard to prove | Not scored 0 from outside. Leave it at 1 |
| Owner and list | Job posts naming ABM, named or target accounts, field marketing measured on pipeline | A job post with "named accounts" and "pipeline" in it | A high-volume SMB motion |

## 3. Disqualifiers

Tick any that applies. One is enough to stop.

- [ ] `low_acv`, evidence the ACV is below six figures
- [ ] `no_named_accounts`, a volume motion with no account list to build from
- [ ] `agency_request`, they want a booth, a venue or a production crew
- [ ] `needs_guarantee`, they need a guaranteed count of meetings or leads to report upward
- [ ] `events_sceptic`, they want convincing that events work at all
- [ ] `single_test_event`, one event, run once, to see if it works
- [ ] `healthcare_conflict`, D6
- [ ] `active_conflict`

## 4. Segment, D8

The concentration segment is open, default enterprise cybersecurity. [Company] sits in: [segment]. If outside the default, the reason it is still worth founder days: [one sentence].

## 5. Verdict

```bash
source ./paths.env
python3 "$STRATEGY_SKILL/scripts/gate.py" --acv [n] --event-spend [n] --unreachable [n] --warm [n] --converts [n] --owner [n] \
  --notes "[one or two sentences]" --write strategy/strategy.json
```

| Verdict | Total of 18 | What happens next |
|---|---|---|
| [GO, HOLD or NO-GO] | [n] | [GO: phase 1. HOLD: the one signal that would change it, and where to watch for it. NO-GO: logged by ID, nothing sent] |

## Done when

- Every score cites a register row, and the register rows have their source addresses and capture dates.
- The verdict is written into strategy.json by gate.py, not typed by hand.
- A HOLD names the signal that would turn it into a GO. A NO-GO names its reason in one line.
- The workspace log has a line: `[date] [Prospect ID] gate [verdict] [total]`.

## Into strategy.json

`gate.verdict`, `gate.total`, `gate.scores`, `gate.disqualifiers`, `gate.notes`, and `prospect.id`, `prospect.company`, `prospect.website`, `prospect.segment`.
