# The return, without inventing a number

Load for: phase 8, the economics deck, and any question about the return on the call.

The brain decided on 2026-09-18 that the client supplies every conversion input. The strategy makes the economic argument anyway, and it is stronger for it: a prospect who types their own close rate into a calculator believes the answer in a way no slide of ours could make them.

## The argument, in five steps

1. **The money is already being spent.** Trade show exhibiting is 40.8% of exhibitor marketing budgets, the largest single channel line (CEIR 2026, ledger, grade B). This is a reallocation question, not a new budget.
2. **The cost of the problem, on their numbers.** Their badge scans at the anchor moment, `{TBD}`, against the benchmark cost per scan, $112 to $300 (CEIR, ledger row 5, grade B), gives what the scans cost them, `{TBD}`. "We do not estimate your spend. Your own number outranks any benchmark."
3. **Three ways to spend the same budget.** A booth only, a hire (or more of the same team), or run it as a channel, compared in words: what you get, who fills the room, what happens after, what it is reported in.
4. **The calculator, on their numbers.** It shows what the channel returns at their deal size and their close rate, and says so plainly when it does not pay back.
5. **What we do not supply.** A close rate, a conversion rate, a return multiple of ours, a price. Said on the slide, not hidden.

## The calculator's arithmetic

Exactly what the deck engine computes, so the notes and the spec can state it:

| Output | Formula |
|---|---|
| Cost per qualified conversation | programme investment ÷ qualified conversations |
| Expected new customers | qualified conversations × close rate |
| Expected first-year revenue | expected new customers × average first-year contract value |
| Return, per unit invested | expected first-year revenue ÷ programme investment |
| Cost to acquire a customer through this channel | programme investment ÷ expected new customers |
| Against their current cost to acquire | their current cost to acquire minus the channel's, shown as "less" or "more" |
| Against their cost per senior meeting | cost per qualified conversation against their cost per senior meeting |

The break-even, for the notes, never for the slide unless they ask: qualified conversations needed to pay back = programme investment ÷ (close rate × first-year contract value). Every term in it is theirs.

## Inputs

| Input | Label | Required | Whose |
|---|---|---|---|
| deal | Average first-year contract value | yes | theirs |
| close | Close rate from a qualified first conversation | yes | theirs |
| investment | Programme investment: any number they want to test, for example what one trade show costs them today | yes | theirs, never our price |
| conversations | Qualified conversations | yes | theirs: how many they would want |
| cac | Current cost to acquire a customer | optional | theirs |
| meeting | Current cost per senior meeting | optional | theirs |

## BUILD and UPGRADE

- **BUILD:** every field empty. No result until the reader has typed the four required numbers. The privacy line says nothing they type leaves the page, and it is true: the deck makes no network request.
- **UPGRADE:** after a call, a field may be prefilled with a number they supplied, recorded as a P0 row, with a note on the slide naming who supplied it, by role, and when. Never prefill a number they did not give us, and never adjust theirs.

## When the answer is bad

The calculator turns the figure to the flag role and says: "At your numbers, the programme does not pay back in its first year. Either the investment is too high for your deal size, or the programme is too small." That sentence is a feature. A strategy that admits its own arithmetic can fail is believed when it says the arithmetic works. Never tune an input to rescue a result.

## Adapting the ROI anchors

The go-to-market builder anchors return three ways: the cost of the problem, the alternative comparison, and the break-even. The strategy keeps all three and drops the price that each one assumed:

| Anchor | In gtm-builder | Here |
|---|---|---|
| Cost of the problem | Problem cost against our subscription | Their scans at the benchmark cost per scan, both their numbers and a cleared figure |
| Alternative comparison | Their cost against our cost | Three ways to spend the same budget, in words |
| Break-even | Value needed against our plan's cost | Conversations needed against their own investment figure, in the notes |

## Never

- A conversion figure, "illustrative" or otherwise. Grade C rows, such as the 30% to 50% dinner-to-opportunity figure, never enter a deck.
- "Pays for itself", "a return of", "typically returns".
- Our fee, a range, or a founding discount (D2, D13).
- A cost-per-lead table from the landing page. Its grade C plus rows are for the landing page only, attributed inline, and never a deck.
