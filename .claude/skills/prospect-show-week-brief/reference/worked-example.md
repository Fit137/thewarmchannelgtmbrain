# Worked example, Acme Example Co. at CloudSec Expo

Load for: a first run, or to see what "done" looks like.

**Fictional.** Acme Example Co. and CloudSec Expo do not exist. Every fact about either is invented. The attendance benchmark is real, from the brain's evidence ledger. Never reuse a sentence for a real company.

Files: `assets/example/brief.json` and `assets/example/evidence-register.md`. The brand kit is the deck builder's example, `../prospect-deck-builder/assets/example/brand.json`.

```bash
python3 scripts/validate_brief.py assets/example/brief.json --register assets/example/evidence-register.md
python3 scripts/build_brief.py assets/example/brief.json ../prospect-deck-builder/assets/example/brand.json --out /tmp/acme_brief.html --pdf /tmp/acme_brief.pdf
python3 scripts/brief_check.py /tmp/acme_brief.html --brief assets/example/brief.json --register assets/example/evidence-register.md --pdf /tmp/acme_brief.pdf
```

## Why a brief, not the strategy

Acme passed the gate as a GO, 12 of 18. CloudSec Expo opens on 24 November, about seven weeks after the brief is dated, so a full strategy would arrive with too little time to use it. The brief is the gift. If Acme replies, the full strategy for next year follows the call.

## The week

| Day | What the public pages show |
|---|---|
| Mon 23, the day before | Nothing announced for the evening. **Open** |
| Tue 24, day 1 | Acme's own opening breakfast. The machine identity session at 11:00. The organiser's welcome reception at 18:00 |
| Wed 25, day 2 | Breakfast **open**. Identity incident recovery at 10:30, the zero trust budget session at 15:00. Competitor A's invitation-only dinner and Competitor B's rooftop reception in the evening |
| Thu 26, day 3 | The closing keynote. The show closes at 14:00 |

Every row cites a register row. The two open slots cite E28, which records the pages read and the date.

## The suggestion, and why this one

A private table on the evening before the show: nothing is announced against it, it does not compete with Acme's own breakfast the next morning, and it sits before both competitors' evenings rather than against them. Twelve seats at the 70% dinner benchmark is about seventeen confirmations.

The timing is said plainly: with about seven weeks to go, a full table is tight, so the decision belongs in October, or the table belongs on next year's calendar and this year's conversations start at Acme's own breakfast. The status line carries D5: Acme can run it with its own team, we can plan it now, and approaching guests on Acme's behalf opens once our privacy position is written.

## What the checks say

- `validate_brief.py`: no errors. One warning: the call to action is a placeholder address.
- `brief_check.py`: no errors. 214, 3,500, 70%, 13,155 and 191 each trace to a register row or the ledger, with the sentence sharing words with its source. The PDF is two pages.
