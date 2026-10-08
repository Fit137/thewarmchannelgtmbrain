# 08. Economics and the return, [Company]

The economic argument, made without inventing a single number about [Company]. The money is already being spent. The question is what it buys. Market figures come from the cleared ledger, attributed. Every figure about [Company] is `{TBD}` until [Company] types it into the calculator, or, in UPGRADE mode, supplies it on a call.

time budget: 1 to 2 hours
method: reference/roi-framework.md

## 1. The budget line

| Figure | Source | Grade | Use |
|---|---|---|---|
| Trade show exhibiting is 40.8% of exhibitor marketing budgets, the largest single channel line | CEIR 2026 Marketing Spend Decision Report, ledger row new | B | The figure slide |

If [Company] publishes its own event spend (an annual report, an investor deck, a public talk), it outranks the benchmark: record it as P1 and use it, attributed.

## 2. The cost of the problem, on their numbers

| Step | Value | Label for the deck |
|---|---|---|
| Their badge scans at the anchor moment | {TBD} | badge scans from your last [anchor moment] |
| The benchmark cost per scan | $112 to $300 | cost per scan, the industry benchmark [n], CEIR, ledger row 5, B |
| What those scans cost them | {TBD} | what those scans cost you, from your own budget |

Note for the deck: We do not estimate your spend. Your own number outranks any benchmark.

## 3. Three ways to spend the same budget

A qualitative comparison. No figures in the cells.

| | A booth only | A field marketing hire | Run it as a channel |
|---|---|---|---|
| What you get | Floor space and scans | Capacity, split across many jobs | Conversations with named accounts |
| Who fills the room | Whoever walks past | The hire, around other work | Six weeks of individual approaches |
| After the event | It ends | It usually ends | Follow-through with guests who choose to continue |
| Reported in | Scans | Activity | Coverage and opportunities |

Adapt the rows to [Company]'s actual alternatives: if it already has a field marketing team, the second column is "More of the same team", not a hire.

## 4. The calculator

Inputs, all [Company]'s own. Required: average first-year contract value, close rate from a qualified first conversation, programme investment (any number they want to test, for example what one trade show costs them today), qualified conversations. Optional: current cost to acquire a customer, current cost per senior meeting.

Outputs: cost per qualified conversation, expected new customers, expected first-year revenue, cost to acquire a customer through this channel, and the comparisons for the optional fields. When the answer is bad, it says so in words and turns the figure to the flag role.

Rules:
- BUILD mode: no field is prefilled. No result shows before the reader types.
- UPGRADE mode: a field may be prefilled only with a number [Company] supplied (a P0 row), with a note naming who supplied it, by role, and when.
- The investment field is never our price. D2 is open, and no price appears anywhere.
- We never supply a close rate, a conversion rate or a return multiple of our own. The ledger's grade C conversion figures never enter a deck.

Intro line for the deck: Every number is yours. We do not supply a close rate, because we do not know yours.

## 5. Chapter E

| Field | Line |
|---|---|
| Cover title | The money is already being spent. The question is what it buys. |
| Cover subtitle | The budget share, the cost of the problem, three ways to spend it, and a calculator that runs on your numbers. |
| Claim | The money is already being spent. The question is what it buys. |
| So what | You can test the economics on your own numbers in the calculator. We do not supply a single conversion figure. |
| Evidence, line 1 | Trade show exhibiting is 40.8% of exhibitor marketing budgets, the largest single line [n]. |
| Evidence, line 2 | A badge scan costs $112 to $300 [n]. |
| Carry forward | If the arithmetic works, the last question is who runs it. |
| Close title | [returns to the cover] |
| Close body | Next: who runs it. |

## Done when

- Every market figure cites a cleared ledger row with its grade, and every [Company] figure is `{TBD}` or a P0 row.
- The comparison is in words, adapted to [Company]'s real alternatives.
- The calculator spec has no default, no example value and no price.

## Into strategy.json

`economics.budget_line` (value, caption, source_n, ledger), `economics.scan_cost` (theirs_label, benchmark, benchmark_label, source_n, ledger, cost_label, note), `economics.options` (columns, highlight, rows), `economics.calculator` (inputs, currency, intro, and prefill with prefill_note in UPGRADE only), `economics.chapter`.
