# Evidence register, [Prospect ID], [Company]

Every claim in the strategy and every figure in the deck traces to one row here. A fact that is not in this register is not stated. Kinds:

- **P0**, supplied by the prospect, on a call or in a document they sent, with the date. UPGRADE mode only. Shown back only to them.
- **P1**, the prospect's own public statement: their site, case studies, press releases, job posts, event pages.
- **P2**, a third party's public record about the prospect: an exhibitor list, a sponsor page, an agenda, press coverage.
- **P3**, our inference from P1 and P2, with its basis written out and starting "Inference". Never a percentage or a money figure, never stated as fact on screen.
- **M-A, M-B**, a market figure from the brain's evidence ledger, cleared for client assets. The source cites "ledger row N".
- **M-C**, a grade C market figure. Internal planning only. Never in the deck.
- **NEW**, a market figure found in research that is not in the ledger. Logged to the brain's `ops/signal-log.md` for grading. Never used until the ledger carries it.

Roles, never people: no name of an individual, no email address, no phone number, no personal profile address. A capture of the page goes in `raw/`, named by row ID.

captured: [YYYY-MM-DD]

| ID | Kind | Claim or figure | Source | Captured | Basis or grade | Used in |
|---|---|---|---|---|---|---|
| E01 | [P1] | [the claim, as the source states it] | [https://address] | [YYYY-MM-DD] | [what on the page supports it] | [phase number, deck slide] |

## Not used, and why

| ID | Kind | Claim or figure | Why it is out |
|---|---|---|---|
| X01 | [M-C or NEW] | [the figure] | [grade C, never in a deck. Or: not in the ledger, logged to the signal log] |
