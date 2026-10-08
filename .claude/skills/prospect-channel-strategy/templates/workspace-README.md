# [Prospect ID], [Company]

A private prospect workspace for a free in-person channel strategy and its branded deck. It lives outside the brain on purpose: the brain holds no data about prospects, only IDs.

created: [YYYY-MM-DD]
status: gate pending

## Rules for this folder

- Never commit it into the brain repository, and never copy its files there. The brain's pipeline gets one row by ID.
- Public information only until [Company] supplies its own numbers on a call (UPGRADE mode, P0 rows).
- Roles, never people. No name of an individual, no email address, no phone number.
- The deck built here is sent once, privately, as a noindex link or a PDF, and never reused for another company or shown as a case study.

## Map

| Path | What |
|---|---|
| `paths.env` | Absolute paths to the brain and the two skills. `source ./paths.env` before running a script |
| `log.md` | Every step, dated: gate, phases, checks, sent, response |
| `strategy/00-gate.md` to `10-handoff.md` | The strategy, one file per phase |
| `strategy/strategy.json` | The structured strategy, the handoff to the deck builder |
| `evidence/evidence-register.md` | Every fact and figure, with its kind and source |
| `evidence/research-log.md` | Every read, and the time spent |
| `evidence/envelope.md` | The brain's rules as they stood when the strategy was written |
| `evidence/raw/` | Captures of the pages the register cites, named by row ID |
| `brand/` | brand_extract.py output: the draft kit, the report, the logo candidates |
| `deck/` | deck.json, brand.json, the logo and the font files |
| `spec/` | The rendered spec files from render_spec.py |
| `build/` | The built send and present files, screenshots and the PDF |

## Commands

```bash
source ./paths.env
python3 "$STRATEGY_SKILL/scripts/gate.py" --help
python3 "$STRATEGY_SKILL/scripts/claim_envelope.py" --out evidence/envelope.md --prospect [Prospect ID]
python3 "$STRATEGY_SKILL/scripts/evidence_check.py" evidence/evidence-register.md --strategy strategy/
python3 "$STRATEGY_SKILL/scripts/validate_strategy.py" strategy/strategy.json --register evidence/evidence-register.md
python3 "$DECK_SKILL/scripts/new_deck.py" strategy/strategy.json --out deck/deck.json
```
