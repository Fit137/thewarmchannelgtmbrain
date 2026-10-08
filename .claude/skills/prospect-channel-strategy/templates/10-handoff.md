# 10. Before you send, and the handoff, [Company]

The last gate before the strategy becomes a deck. Every check here is run, not assumed. The section that names what was verified, what needs settling and what was designed is the highest-trust part of the whole job: never soften it.

time budget: 1 hour

## 1. The envelope is current

```bash
source ./paths.env
python3 "$STRATEGY_SKILL/scripts/claim_envelope.py" --out evidence/envelope.md --json evidence/envelope.json --prospect [Prospect ID]
```

- Brain commit when the strategy was written: [commit]
- Brain commit now: [commit]
- If they differ: [what changed in rules/ and ops/decisions.md, and what in the strategy was re-checked]

## 2. The checks

```bash
python3 "$STRATEGY_SKILL/scripts/evidence_check.py" evidence/evidence-register.md --strategy strategy/
python3 "$STRATEGY_SKILL/scripts/validate_strategy.py" strategy/strategy.json --register evidence/evidence-register.md --profile [full or lite]
python3 "$BRAIN/scripts/lint_claims.py" strategy/
```

| Check | Result | Notes |
|---|---|---|
| evidence_check.py | [0 errors] | [warnings read and answered] |
| validate_strategy.py | [0 errors] | [warnings read and answered] |
| lint_claims.py on the strategy folder | [0 errors] | [the guest-copy block passes] |
| The brain's ops/QA-checklist.md, client asset blocks | [blocks run] | [findings] |

## 3. Before you present

Name every item individually.

**Verified, and where it traces to.**
- [each market figure, with its ledger row and grade]
- [each fact about [Company] the deck states, with its register row]
- [the rules checked: for example, no reply rate appears because the 70% benchmark does]

**Needs settling, and what breaks if it goes the other way.**
- [the call to action address]
- [anything the founder has not approved, and what changes if they say no]

**Designed, not supplied, and the cost of committing to it.**
- [quadrant positions: our reading of public information, not measurement]
- [seat counts per format: designed to show the arithmetic, never a promise]
- [the calendar placements: a proposal]
- [the motif's mark count: not data, never labelled]

## 4. Profile

| Profile | When | Decks |
|---|---|---|
| Full | A clear GO, a footprint of four or more moments, a committee of three or more | Home, A to F, about 37 slides |
| Lite | A HOLD that became a GO, a thin footprint, or a prospect whose buyers are one role | Home, A, C, E and a short F, about 20 slides |

Chosen: [full or lite], because [one line].

## 5. Handoff to the deck builder

```bash
python3 "$DECK_SKILL/scripts/new_deck.py" strategy/strategy.json --profile [full] --out deck/deck.json
```

Then load the `prospect-deck-builder` skill: brand kit, presenter notes, design concepts, build, check, screenshots, send.

## 6. Log

- Workspace log: `[date] [Prospect ID] strategy [version] ready, profile [full or lite], brain [commit]`
- Brain pipeline, `ops/pipeline.md`, one row in its own columns, and never a person's name:

| ID | Company or type | Segment | ICP characteristics met, of 5 | Contact role | Stage | Last touch | Next step | Signals logged |
|---|---|---|---|---|---|---|---|---|
| [Prospect ID] | [the company type, or the name if the founder is comfortable with it] | [segment] | [n, from the gate] | [role] | 1. Identified, in-ICP | [date], strategy [version] ready | One researched approach | [signal-log date or none] |

A HOLD or NO-GO goes in the pipeline's disqualified table instead, with its reason against `reference/icp-client.md`.

## Done when

- The envelope is current, and every check above has run clean or has its warnings answered in writing.
- Before you present names things individually.
- deck/deck.json exists, scaffolded from this strategy.
