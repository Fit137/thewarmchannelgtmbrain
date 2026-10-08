---
name: prospect-channel-strategy
description: Build a free, bespoke in-person channel strategy for one highly qualified prospect, an established B2B company that already spends on events, from public information only, as The Warm Channel's value-first approach to a high-value lead. Gates the company on the client ICP, maps and scores its event year for buyer density and access, picks the anchor moment, defines the committee and account tiers, writes the plan (one decision per moment, formats, a calendar, the carrying line), finds live questions, works the confirmation arithmetic and the economics without inventing a number, and hands a validated strategy.json to prospect-deck-builder. Use when the user names a company and wants its event strategy, a free strategy or teardown for a lead, its event footprint mapped, a prospect qualified, or a strategy upgraded with call numbers or refreshed. Not for The Warm Channel's own go-to-market, which is go-to-market-brain.
---

# Prospect Channel Strategy

## Skill overview

A highly qualified prospect gets something no other vendor will send it: its own in-person year, mapped from the outside and rebuilt as a channel around the accounts it sells to, with every number about its business left for it to fill in. The strategy is given away, once, to one person. It is the work, shown before anyone pays for it, and it is the only proof The Warm Channel can offer while the proof set is empty.

This is not a go-to-market build. The prospect is an established company with a working go-to-market, a budget line for events and a team that owns them. The job is narrower and deeper: how the in-person moments it already funds could produce conversations with its named accounts, and what that would take. The structure follows the gtm-builder skill (gated phases, callable templates, an execution checklist, a deck at the end), and every nuance is changed for this purpose.

**What it produces, per prospect, in a private workspace outside the brain:**

1. Eleven phase files, `strategy/00-gate.md` to `strategy/10-handoff.md`
2. An evidence register that every claim traces to, and a research log
3. A claim envelope: the brain's rules on the day the strategy was written
4. `strategy/strategy.json`, validated, the handoff to the **prospect-deck-builder** skill, which packages it as an interactive deck in the prospect's own branding

**What governs it.** The Warm Channel's go-to-market brain is the source of truth for positioning, claims and voice. Load the brain's `CLAUDE.md` and its control layer before writing anything, in its order: `rules/two-vocabularies.md`, `rules/glossary.md`, `rules/service-status.md`, `rules/do-not-say.md`, `rules/evidence-ledger.md`, `rules/writing-rules.md`. The strategy is client copy and obeys all of it. If the brain is not reachable, paste its `adapters/portable-control-layer.md` and stop short of the handoff: `validate_strategy.py` needs the ledger.

## Route first

| The situation | Mode | Go to |
|---|---|---|
| A company has been spotted and nothing exists yet | **BUILD**, version 1 | Phase 0, then 1 to 10 only on GO |
| They replied, a call happened, they shared numbers or their named list | **UPGRADE**, version 2 | `reference/modes.md`, UPGRADE |
| A strategy exists, is about to be sent, and is old, or the brain or their calendar moved | **REFRESH** | `reference/modes.md`, REFRESH |
| NO-GO, a decline, a request to stop, or no reply | **STOP** | `reference/modes.md`, STOP |

## Non-negotiables, as they apply here

- **The proof set is empty.** No client, count, logo, testimonial, case study or result. The honesty line, verbatim: "We are new. No case study yet, and we are not going to dress that up."
- **Every number about the prospect is theirs.** Written `{TBD}` until they supply it. Never estimated, never "illustrative".
- **Market figures come only from the ledger's cleared rows**, grade A or B, attributed. Grade C never enters a strategy or a deck. A new figure goes to the brain's signal log, not into the copy.
- **The 70% collision.** A deck is one conversation. Where the 70% dinner benchmark appears, no reply rate appears, screen or notes.
- **No guarantee, no price, no network claim.** D4, D2, and the hard ban.
- **Post-event conversion and the guest promise are frozen until D11.** After the evening is described only in the consent framing, designed with the client, not offered until settled. Never a hand-over mechanism.
- **Status travels with every capability that is not READY,** in the same sentence.
- **Two audiences, never blended.** The strategy is client copy. The one guest artefact, the sample invitation, uses guest words only, between guest-copy markers.
- **Public information only, roles never people.** No personal data anywhere in the workspace or the brain. The pipeline gets one row by ID.
- **No em dash, no en dash. Banned words:** leverage, unlock, seamless, robust, streamline, cutting-edge, empower. Commonwealth spelling.
- **Channels out.** The strategy reaches the prospect through one researched approach from the founder. Never a sequence, never a follow-up to a non-reply, never paid distribution.

## Required inputs

```
BEFORE PHASE 0

□ Company name and website
□ How it came to attention, by type only (an exhibitor list, a partner, a comment, an inbound)
□ A pipeline ID, PX-0000 format, from the brain's ops/pipeline.md
□ The brain, checked out beside this repository or at $TWC_BRAIN
□ Web search and fetch in this session, or a founder willing to run the research scope by hand
```

Nothing else. The strategy is built from the outside. Asking the prospect for anything before the strategy exists would turn a gift into a questionnaire.

## External research steps

Phases that need the open web. Where the session has web search and fetch, run them directly and capture every source. Where it does not, write the research scope from `reference/research-playbook.md`, hand it to the founder, and continue when the pages come back.

| Phase | Research | Sources |
|---|---|---|
| **0** Gate | One quick signal per criterion | Pricing, case studies, careers, events page |
| **1** Account | The company in its own words | Site, newsroom, investor relations, job posts |
| **2** Footprint | Every in-person moment, twelve months back and forward | Events page, exhibitor and sponsor lists, agendas, prospectuses |
| **3** Buyers | The committee, by title | Case study quotes, webinar co-presenters, review sites |
| **4** Landscape | Competitors' in-person moments | The same event sources, per competitor |
| **6** Questions | Three signals per question | This year's agendas, regulators, trade press, practitioner communities |

## Output mapping

| Phase | File | Feeds, in the full deck profile |
|---|---|---|
| 0 Gate | `strategy/00-gate.md` | Nothing on screen. Decides whether anything else happens |
| 1 Account | `strategy/01-account.md` | The method paragraph, the notes, the glossary of their words |
| 2 Footprint | `strategy/02-footprint.md` | Deck A: the year, the quadrant, the anchor |
| 3 Buyers | `strategy/03-buyers.md` | Deck B: the committee, the named list, the tiers |
| 4 Landscape | `strategy/04-landscape.md` | The plan's judgement. Rarely a slide |
| 5 Channel | `strategy/05-channel.md` | Deck C: the choices, the formats, the still slide, the rebuilt year |
| 6 Questions | `strategy/06-questions.md` | Deck C questions, deck D invitation |
| 7 Operating | `strategy/07-operating.md` | Deck D: the arithmetic, six weeks, after the evening, measures |
| 8 Economics | `strategy/08-economics.md` | Deck E: the budget line, the cost per scan, three ways, the calculator |
| 9 Engagement | `strategy/09-engagement.md` | Deck F: three ways to run it, the steps, the next step |
| 10 Handoff | `strategy/10-handoff.md` | Before you present, the profile choice, the handoff |
| All | `strategy/strategy.json` | `new_deck.py` in prospect-deck-builder |

## Workspace

```bash
python3 scripts/init_workspace.py "[Company]" --id PX-0000 --website [address]
cd [the printed workspace path] && source ./paths.env
```

Created beside the brain as `../twc-prospects/<slug>/`, never inside it. It holds the phase files with the company and ID filled in, the register, the research log, the activity log, `paths.env`, the skeleton `strategy.json` and the claim envelope. See `reference/deliverable-spec.md` for the map.

---

# PHASE 0: QUALIFICATION GATE

Template: `templates/00-gate.md`. Rubric: `reference/scoring-rubrics.md`, part 1. Time: 30 to 45 minutes.

## Step 0.1: Conflict check

**DO:**
```
Before any research, answer four questions:
1. Is the company inside the founder's separate healthcare business, its clients, guests or references? Yes: stop. D6.
2. Does it conflict with an active engagement or a partner commitment? Yes: stop, tell the founder.
3. Was it approached, declined or disqualified in the last twelve months? Yes: stop. One approach, ever.
4. Are two strategies already in flight? Yes: HOLD for capacity.
```

## Step 0.2: One signal per criterion

**DO:**
```
For each of the six criteria, find the quickest public signal and record it as an
evidence register row (ID, kind, claim, source address, capture date, basis):

1. ACV, six figures and up: pricing page, case study scale, enterprise sales roles
2. Event spend: events page, exhibitor and sponsor lists, own conference
3. Unreachable cold: the buyer's title and segment
4. Warm and cold: advisory boards, reference programmes, peer language
5. Converts badly: public statements or job posts about proving event return. Usually unknown
6. Owner and list: job posts naming named accounts, ABM, pipeline

Stop at one good signal per criterion. The gate is a filter, not the research.
```

## Step 0.3: Score and verdict

**DO:**
```
Score each criterion 0 to 3: 3 direct public evidence, 2 indirect or an inference
with its basis, 1 no evidence, 0 evidence it fails. Tick any disqualifier.
Run gate.py and write the verdict into strategy.json:

python3 "$STRATEGY_SKILL/scripts/gate.py" --acv n --event-spend n --unreachable n \
  --warm n --converts n --owner n --notes "..." --write strategy/strategy.json

GO: 12 or more of 18, ACV and event spend at 2 or more, no zero, no disqualifier.
HOLD: name the one signal that would change it and where to watch for it.
NO-GO: log the reason by ID. Nothing is sent.
```

**OUTPUT:** `00-gate.md` complete, `gate` written into strategy.json, a line in `log.md`.

---

# PHASE 1: ACCOUNT INTELLIGENCE

Template: `templates/01-account.md`. Playbook: `reference/research-playbook.md`. Time: 2 to 3 hours.

## Step 1.1: Snapshot and how they sell

**DO:**
```
Describe the company in its own words: what it sells, to whom, in which segments and
markets, its size band and ownership, and the ACV signal. Then how it sells: the motion,
the sales cycle signal, the account-based signal, partners, and which role owns events.
Every row cites the register. No person is named: roles only.
```

## Step 1.2: Priorities and their words

**DO:**
```
List at least three things the business is visibly pushing this year, each with a public
signal and what it means for which buyers it needs to reach, and when.

Capture ten to fifteen of their own phrases verbatim, with where they appear. The deck is
written in their vocabulary: what they call their category, their buyers, their problems.
```

## Step 1.3: Sensitivities and unknowns

**DO:**
```
Record privately anything public that a careless sentence could land on: an incident, a
reorganisation, a lawsuit, a departure. Decide how the strategy handles each.

List what only the company can supply: contract value, close rate, event budget and what
the flagship produced, the named list. Each becomes a {TBD} and a question for the call.
```

**OUTPUT:** `01-account.md`, `prospect` and `account` in strategy.json.

---

# PHASE 2: EVENT FOOTPRINT AUDIT

Template: `templates/02-footprint.md`. Rubric: `reference/scoring-rubrics.md`, part 2. Time: 3 to 5 hours.

## Step 2.1: Inventory

**DO:**
```
List every public in-person moment in the twelve months behind and ahead: its name, kind,
their role, month and week, today's format in one or two words, and the register row.
Look in order: their events page and newsroom, the segment's main shows' exhibitor and
sponsor lists, agendas, their own conference and roadshows, partner pages, announced
dinners. Repeats get one row per date, pointing at the first with same_as.
Webinars are recorded and kept off the map.
```

## Step 2.2: Score density and access

**DO:**
```
Score each moment on two axes from -20 to +20, to one decimal:

- Density, new buyers in the room: how many not-yet-customer buyers at the right titles
  are in the building. Best evidence: the organiser's sponsorship prospectus.
- Access, time across a table: how much chosen, uninterrupted conversation they get with
  those buyers there. A booth is negative, a hosted dinner strongly positive.

Rank first on each axis, then assign numbers that keep the rank. Never a round number:
7.3, not 7. Write one line of reason per score.
```

## Step 2.3: Quadrants and the anchor

**DO:**
```
Place each moment:

              ACCESS +20
   KEEP FOR CUSTOMERS  |  BUILD ON
   -------------------------------- NEW BUYERS +20
   RECONSIDER          |  WRAP WITH A PRIVATE PROGRAMME
              ACCESS -20

The anchor is the bottom-right moment with the widest gap between density and access,
weighted toward the larger spend. Exactly one. Write:
- the anchor line: "Your buyers will be at [moment]. [The format] is not where you get
  time with them."
- the anchor body: what a private format the same week does instead, with no promise
- the chart's title claim, read from where the moments fell, after scoring
- the timeline's title claim about their year

No bottom-right moment: record it. The Lite profile or a HOLD are honest answers.
```

**OUTPUT:** `02-footprint.md`, `footprint` in strategy.json, chapter A.

---

# PHASE 3: BUYERS AND ACCOUNTS

Template: `templates/03-buyers.md`. Time: 2 to 3 hours.

## Step 3.1: The committee

**DO:**
```
Read the committee from what the company publishes: who its case studies quote, who its
job posts say it sells to, who co-presents its webinars. Four to five roles. For each:
what they own, what they decide, why they would give up an evening, what keeps them away.
Choose two to four for the deck, each with one line: "[Decides]. Comes for [the reason]."
```

## Step 3.2: Why cold misses them, and the tiers

**DO:**
```
One paragraph on how their sellers reach this committee today, in words. No reply rate:
the deck will use the 70% dinner benchmark.

Tiers by type, never by name: Tier 1, Tier 2, Expansion. Every count {TBD}, with the line
"A full coverage read on your named list fills them in."
Describe guests only by role and organisation type, the way an invitation would. D14.
```

**OUTPUT:** `03-buyers.md`, `buyers` in strategy.json, chapter B.

---

# PHASE 4: COMPETITIVE EVENT LANDSCAPE

Template: `templates/04-landscape.md`. Time: 1 to 2 hours.

## Step 4.1: Competitors in person, and saturation

**DO:**
```
Three to six competitors from the company's own comparison pages and category. For each,
their public in-person moments and whether they run small private formats.
Answer for the anchor moment: are competitors hosting private formats that week? If so,
the question must carry the difference, or the evening moves.
One line of white space: the moment, format or question nobody owns on public record.
Never a competitor's results, budget or plans. Default: informs the plan, stays off the deck.
```

**OUTPUT:** `04-landscape.md`, `landscape` in strategy.json.

---

# PHASE 5: CHANNEL STRATEGY

Template: `templates/05-channel.md`. Formats: `reference/event-formats.md`. Time: 2 to 4 hours.

## Step 5.1: One decision per moment

**DO:**
```
For every moment on the map, one decision from its quadrant:
- Wrap: keep it, and add private tables for named accounts the same week
- Build on: keep it, or upgrade seats that come without a choice of guests into a table
- Keep for customers: keep it, and add an expansion table apart from prospects
- Reconsider: redirect the budget into the plan's own tables
The anchor's decision comes first. Keep-first is the posture: a plan that opens by cutting
their flagship attacks the person who chose it.
```

## Step 5.2: Formats and the calendar

**DO:**
```
Two to four formats from the library, each tied to a moment or to public evidence of where
Tier 1 accounts cluster. Each gets a deck name and one line.

Place proposed moments on a twelve-month strip, each with its six-week outreach window,
with the moments they keep on the same strip. No proposed moment inside one of their own
events, no two windows for the same tier at once, no metro table without evidence.

List what the plan deliberately does not recommend, and why.
```

## Step 5.3: The carrying line

**DO:**
```
Write the line the whole file exists to land. Three short sentences at most: keep, add,
follow through, with follow-through in the consent framing. For example:
"Keep the moments you already fund. Add private tables for your named accounts around
them. Follow through with the guests who choose to continue."
It becomes the deliberately still slide and the home layer's line.
```

**OUTPUT:** `05-channel.md`, `channel` and `thesis.carrying_line` in strategy.json, chapter C.

---

# PHASE 6: QUESTIONS AND THE INVITATION

Template: `templates/06-questions.md`. Method: `reference/question-bank-method.md`. Time: 2 to 3 hours.

## Step 6.1: Three live questions

**DO:**
```
Write five candidate questions from the buyer's year, never the host's product, and keep
three. Form: "How are you [doing the hard thing], now that [the change that made it hard]?"
Verify each with three independent public signals: this year's agenda sessions, a dated
regulatory change, a recurring incident class, practitioner discussion, an analyst note.
Two signals: carry it with "would be verified before any invitation goes out". One: cut it.
The host never chooses the question.
```

## Step 6.2: The sample invitation

**DO:**
```
Write the invitation a guest would read, between guest-copy markers, in guest words only,
under 120 words: the question first; who else is coming by role and organisation type;
the host disclosed, not choosing the question, not presenting; no deck, no panel, no stage;
"No attendee list is circulated, before or after."; "Reply yes or no. Either is a fine answer."
Never a D11-frozen line. Then lint it with the brain's lint_claims.py.
```

**OUTPUT:** `06-questions.md`, `questions` and `invitation` in strategy.json.

---

# PHASE 7: HOW A ROOM FILLS, AND WHAT HAPPENS AFTER

Template: `templates/07-operating.md`. Method: `reference/arithmetic.md`. Time: 1 to 2 hours.

## Step 7.1: The arithmetic and the six weeks

**DO:**
```
Confirmations = people in the room ÷ the format's attendance rate, rounded to the nearest
whole person, from the cleared Clutch Events rows: dinners 70%, VIP and sport 86%, vendor
conferences 19%. Twelve seats: about seventeen confirmations. People approached: {TBD},
set by the coverage read.
The six weeks: weeks 6 to 4 research and approach once; weeks 4 to 1 confirm and disclose
who is coming by role; the week, reconfirm. Status wherever it is our work: approaching
guests opens once our written privacy position is in place, D5.
```

## Step 7.2: The evening, after it, and the measures

**DO:**
```
The evening: one question, no deck, no panel, no pitch from the floor including the host,
no photograph, no attendee list. The prospect hosts and contracts venue and catering.

After the evening, in the consent framing only, no mechanism:
"After the evening, the conversation continues only with guests who choose it, and nobody
is chased. How that step works is designed with you, and it is not offered until that
design is settled."

Measures: named-account coverage, arrived against confirmed, qualified conversations with
guests who chose to continue, opportunities opened. Targets {TBD}. "The report format is in
development."
```

**OUTPUT:** `07-operating.md`, `operating` in strategy.json, chapter D.

---

# PHASE 8: ECONOMICS AND THE RETURN

Template: `templates/08-economics.md`. Method: `reference/roi-framework.md`. Time: 1 to 2 hours.

## Step 8.1: The argument without an invented number

**DO:**
```
1. The money is already being spent: 40.8% of exhibitor budgets go to trade show exhibiting
   (CEIR 2026, B).
2. The cost of the problem on their numbers: their scans {TBD} at $112 to $300 a scan
   (CEIR, B) gives what the scans cost them, {TBD}.
3. Three ways to spend the same budget, in words, adapted to their real alternatives.
4. The calculator: six inputs, all theirs, empty in BUILD. Prefilled only in UPGRADE, only
   with numbers they gave, with a note naming the role and the date.
5. What we do not supply, said on the slide: a close rate, a conversion rate, a return
   multiple, a price.
```

**OUTPUT:** `08-economics.md`, `economics` in strategy.json, chapter E.

---

# PHASE 9: HOW TO RUN IT

Template: `templates/09-engagement.md`. Time: 1 hour.

## Step 9.1: Three ways, the steps, the next step

**DO:**
```
Three ways to run it, compared: in-house with this plan, with The Warm Channel, a mix.
The real decision is capacity: who carries six weeks of outreach per moment. The plan is
theirs either way, in so many words.

What we would do, with status from the envelope: Plan (READY); Fill (opens once our
privacy position is written); Follow through (not offered until that design is settled).
The honesty line, verbatim. One call to action: a call with their numbers, offering the
full coverage read. No price, no founding terms, no founder attendance promised.
```

**OUTPUT:** `09-engagement.md`, `engagement` in strategy.json, chapter F.

---

# PHASE 10: BEFORE YOU SEND, AND THE HANDOFF

Template: `templates/10-handoff.md`. Time: 1 hour.

## Step 10.1: Checks

**DO:**
```
source ./paths.env
python3 "$STRATEGY_SKILL/scripts/claim_envelope.py" --out evidence/envelope.md --json evidence/envelope.json --prospect "$PROSPECT_ID"
python3 "$STRATEGY_SKILL/scripts/evidence_check.py" evidence/evidence-register.md --strategy strategy/
python3 "$STRATEGY_SKILL/scripts/validate_strategy.py" strategy/strategy.json --register evidence/evidence-register.md --profile full
python3 "$BRAIN/scripts/lint_claims.py" strategy/

If the brain's commit changed since the strategy recorded it, diff rules/ and ops/decisions.md
and re-check every line the change touches. Run the brain's ops/QA-checklist.md client blocks.
```

## Step 10.2: Before you present

**DO:**
```
Fill before_you_send with single items, never softened:
- verified: every market figure with its ledger row and grade, every stated fact with its row
- needs settling: the call to action address, anything the founder has not approved, and
  what breaks if it goes the other way
- designed, not supplied: the quadrant positions, the seat counts, the calendar placements,
  the motif's mark count, and the cost of committing to each
```

## Step 10.3: Handoff

**DO:**
```
Choose the profile: full (a clear GO, four or more moments, three or more committee roles)
or lite (a thin footprint, one buyer role, or a HOLD that became a GO).

python3 "$DECK_SKILL/scripts/new_deck.py" strategy/strategy.json --profile full --out deck/deck.json

Then load the prospect-deck-builder skill. Log the step in log.md and one row in the brain's
ops/pipeline.md, by ID, with no person's name.
```

---

# CALLABLE TEMPLATES

| Template | Use |
|---|---|
| `templates/00-gate.md` to `10-handoff.md` | One per phase, copied into the workspace by init_workspace.py |
| `templates/evidence-register.md` | The register: kinds P0, P1, P2, P3, M-A, M-B, M-C, NEW |
| `templates/research-log.md` | Every read, and the time per phase against its budget |
| `templates/strategy.skeleton.json` | The empty strategy.json |
| `templates/workspace-README.md` | The workspace's own rules and map |

# SCRIPTS

| Script | Does |
|---|---|
| `scripts/init_workspace.py` | Creates the workspace outside the brain, with templates, register, logs, paths.env, skeleton and envelope |
| `scripts/claim_envelope.py` | Snapshots the brain's open decisions, statuses, cleared figures and bans, with what each means here |
| `scripts/gate.py` | Scores the gate, prints GO, HOLD or NO-GO with reasons, writes it into strategy.json |
| `scripts/evidence_check.py` | Checks the register's shape, kinds, ledger rows, ages and people rules, and the strategy's citations |
| `scripts/validate_strategy.py` | Checks strategy.json's shape, evidence, copy, frozen lines and readiness before the handoff |

All standard library Python, 3.8 or later. Every script takes `--help`.

# REFERENCES

| File | Load for |
|---|---|
| `reference/claim-envelope.md` | Any line touching a promise, a price, a capability, a figure or the guest side |
| `reference/research-playbook.md` | Phases 0 to 6, where to look, what never to do |
| `reference/scoring-rubrics.md` | The gate, density and access, committee roles, question liveness, format fit |
| `reference/event-formats.md` | The format library and the attendance benchmarks |
| `reference/question-bank-method.md` | Live questions and the sample invitation |
| `reference/arithmetic.md` | Confirmations, title mix, the six weeks, timing |
| `reference/roi-framework.md` | The economic case and the calculator's arithmetic |
| `reference/deliverable-spec.md` | The workspace, strategy.json field by field, the deck mapping |
| `reference/modes.md` | BUILD, UPGRADE, REFRESH, STOP |
| `reference/approach.md` | Sharing the strategy: who, when, the message, delivery, after |
| `reference/worked-example.md` | The fictional Acme Example Co., phase by phase |

---

# EXECUTION CHECKLIST

```
PROSPECT STRATEGY PROGRESS, [Prospect ID]

□ SETUP
  □ Brain loaded, control layer read in order
  □ init_workspace.py run, envelope written
□ PHASE 0: Gate
  □ 0.1 Conflict check
  ⚠️ 0.2 One signal per criterion (WEB RESEARCH)
  □ 0.3 Scored, gate.py verdict written           → STOP here unless GO
□ PHASE 1: Account intelligence
  ⚠️ 1.1 Snapshot and how they sell (WEB RESEARCH)
  □ 1.2 Priorities and their words
  □ 1.3 Sensitivities and unknowns
□ PHASE 2: Event footprint
  ⚠️ 2.1 Inventory (WEB RESEARCH)
  □ 2.2 Density and access, to one decimal
  □ 2.3 Quadrants, the anchor, the claims
□ PHASE 3: Buyers and accounts
  ⚠️ 3.1 The committee (WEB RESEARCH)
  □ 3.2 Why cold misses them, the tiers
□ PHASE 4: Landscape
  ⚠️ 4.1 Competitors in person, saturation (WEB RESEARCH)
□ PHASE 5: Channel strategy
  □ 5.1 One decision per moment
  □ 5.2 Formats and the calendar
  □ 5.3 The carrying line
□ PHASE 6: Questions
  ⚠️ 6.1 Three live questions, verified (WEB RESEARCH)
  □ 6.2 The sample invitation, linted
□ PHASE 7: Operating model
  □ 7.1 The arithmetic and the six weeks
  □ 7.2 The evening, after it, the measures
□ PHASE 8: Economics
  □ 8.1 The argument without an invented number
□ PHASE 9: How to run it
  □ 9.1 Three ways, the steps, the next step
□ PHASE 10: Handoff
  □ 10.1 Envelope current, every check clean
  □ 10.2 Before you present, named individually
  □ 10.3 new_deck.py run, logged
→ OUTPUT: strategy/strategy.json, validated, and deck/deck.json scaffolded
→ NEXT: the prospect-deck-builder skill
```

# QUICK START

When the user names a company and wants its strategy, open with:

```
I'll build [Company]'s in-person channel strategy from public information, in a private
workspace outside the brain, and gate it first so no founder time goes to a poor fit.

To start I need:
1. The company and its website
2. How it came to your attention (by type: an exhibitor list, a partner, an inbound)
3. A pipeline ID, or I'll take the next free one from ops/pipeline.md

The sequence:
0. Qualification gate, about 30 minutes, GO / HOLD / NO-GO     ⚠️ web research
1. Account intelligence                                         ⚠️ web research
2. Event footprint: every moment, mapped for density and access ⚠️ web research
3. Buyers and accounts                                          ⚠️ web research
4. Competitive event landscape                                  ⚠️ web research
5. The channel strategy: decisions, formats, calendar, carrying line
6. Live questions and a sample invitation                       ⚠️ web research
7. How a room fills, and what happens after
8. The economics, on their numbers
9. How to run it
10. Checks and handoff to the deck builder

Every number about their business stays blank for them to fill in. Nothing goes to
them until the deck is built and checked.
```

# SKILL METADATA

- **Version:** 1.0
- **Last updated:** October 2026
- **Phases:** 11, from the gate to the handoff
- **Modes:** BUILD, UPGRADE, REFRESH, STOP
- **External research steps:** 6 (phases 0, 1, 2, 3, 4, 6)
- **Outputs per prospect:** 11 phase files, an evidence register, a research log, a claim envelope, strategy.json
- **Scripts:** 5, standard library Python
- **Callable templates:** 15
- **Estimated effort:** two to four working days of founder time per BUILD, in sessions of one or two phases
- **Pairs with:** prospect-deck-builder, which turns strategy.json into the prospect's branded interactive deck
- **Governed by:** The Warm Channel go-to-market brain, through the claim envelope
