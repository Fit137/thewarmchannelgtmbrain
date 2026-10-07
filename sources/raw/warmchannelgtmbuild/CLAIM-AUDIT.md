# Claim audit

Every dashboard in both runs, checked against `GTM-BRIEF.md` Section 5. The brief says the deck compresses everything and the claim ledger should be open beside it, so this is that ledger, run across the whole output rather than only the deck.

Audit date 2026-09-18.

## The eleven narrowed claims

Section 5 lists eleven things not to write and the permitted wording for each. Result across all 20 output files.

| Claim | Where it could have appeared | Used? | Result |
|---|---|---|---|
| Raised a $30M Series A after these trade shows | Phase 6 proof fields, both decks | **No** | Not used anywhere. It is a credential, not a proof point, and it is gated on documentation |
| More than $1 million in pipeline from hospital and pharma buyers | Phase 6, Phase 9 ROI | **No** | `{TBD}` until the artifact exists, and it was not reached for |
| A roughly 70% positive reply rate | Phase 3, Phase 6, both decks | **No** | Open decision 3. Held at `{TBD}` everywhere. **Note the collision risk below** |
| A named global collaboration software company commissioned both rooms | Phase 2, Phase 6, Run A deck | **No** | No client named anywhere in either run |
| Authority and experience of successful events | Phase 3, Phase 6 | **No** | The founder's record does not appear in any output file |
| AI content is eroding trust, so events are becoming necessary | Phase 6, Phase 8, Run A deck | **No** | The causal chain is not asserted. The Gartner figures were available and were not needed |
| In-person events have more trust and more conversion | Phase 2, Phase 6 | **No** | The substitute used instead is the Clutch attendance contrast, 19% against 70%, which is measured rather than believed |
| It will keep getting harder and more expensive to get leads online | Phase 8 | **No** | Phase 8 states the observed cold email trend with its dates and stops |
| We bring you attendees from your ideal customer profile | Phase 6 drill 5, Phase 9, Run A deck | **No, and this is the one to watch** | Replaced everywhere by the attendance floor with a named remedy, and the floor is `{TBD}` until open decision 4. **Until it settles, Phase 6 drill 5 is a template and must not be spoken as though it were a promise** |
| The Warm Channel, implying a network that already exists | Everywhere | **No** | Run A Phase 6 drill 1 states the opposite in the copy itself, that there is no audience to sell. Run B says guest side inventory starts at zero |
| Pipeline as an assumed adjacent outcome | Phase 6, Phase 9 | **Refused explicitly** | Run A Phase 6 drill 6 argues against it by name. Phase 9 rejects the per-outcome denominator absolutely and rebuilds the ROI calculator so the client supplies every input |

## The 70% collision, and it needs a decision

Two different 70% figures are now in play and they must never be said in the same sentence.

| Figure | What it is | Status |
|---|---|---|
| 70% positive reply rate | The founder's unaudited claim from two commissioned rooms | **Banned.** `{TBD}` until reconstructed from send records, open decision 3 |
| 70% attendance rate | Clutch Events category benchmark for invite-only executive dinners, 13,155 registrations across 191 events | **Cleared, grade B plus,** attributed wherever it appears |

They are unrelated numbers about unrelated things that happen to share a value. A listener who hears both in one conversation will merge them, and the merged version is the banned claim wearing a citation. Where the attendance benchmark is used in speech, attribute it out loud, and do not mention the reply rate in the same conversation until it has been reconstructed.

## Hard bans

| Ban | Result |
|---|---|
| Any client count | None. No output states a number of clients |
| Any attendee total | None. Room sizes are stated as scope, 12 to 20 seats, never as a total delivered |
| Any named client | None |
| Any testimonial or quoted praise | None. Run A Phase 8 explicitly forbids drafting one in advance |
| Any logo | None |
| Any conversion, meeting, pipeline or revenue figure | None. Phase 9's calculator is rebuilt so the client supplies deal size and close rate, and Phase 9 states that no illustrative example may be given |
| Any guarantee of an outcome beyond attendance | None. The only promise in either run is the attendance floor, and it is `{TBD}` |
| Any unsourced market statistic | None. Every figure used traces to `research/evidence-ledger.md` with a grade |
| Any claim of an existing standing guest network | None, and both runs state the opposite |
| Any use of the healthcare guest list or references | None. Run B treats it as a consent boundary and says so in three places |

## Mechanics

| Rule | Result |
|---|---|
| No em dash | 0 across all output files, checked programmatically |
| No en dash | 0, checked programmatically |
| Banned words: leverage, unlock, seamless, robust, streamline, cutting-edge, empower | 0. One instance was caught in Phase 1, where it was the skill's own row label, and the row was renamed with a note. **This file is the one exception, because the row above has to name the words in order to check them.** `tools/lint_claims.py` excludes this file from that rule and no other |
| `{TBD}` for unknown metrics, never invented | Held. Every price, the floor, burn, runway, the reply rate, the trade show cost and the employer cost above base are `{TBD}` |

## The two-vocabulary rule

The governing sensitivity in Section 5: the two audiences occupy the same room and one is being sold to the other.

| Check | Result |
|---|---|
| Client vocabulary on a guest-facing surface | None. Run B files separate internal analysis from guest-facing copy and mark which is which |
| Trust-scarcity argument aimed at guests | None. Run B states explicitly that it is a client argument and why running it at guests is damaging |
| Banned-from-guest words: composed attendance, access, inventory, target account, in-ICP, show rate, attendance floor, coverage | None in any guest-facing copy section. Listed as forbidden in Run B Phase 3 and repeated on the Run B deck |
| Guest treated as a lead in the lead magnet | The scorecard is client-facing only and asks the client about the client's own list. It collects nothing about the guest side, and says so |

## Where a claim could still get fabricated

The audit is clean. These are the four places it would break first, in order of likelihood.

1. **Phase 6 drill 5, the attendance floor.** The strongest copy in Run A and currently a template with two `{TBD}` fields. The temptation is to say a number in a live conversation because the sentence needs one. Settle open decision 4 first.
2. **Phase 6 drill 7's subhead.** It carries the 70% attendance benchmark with its attribution. Dropping the attribution to shorten the line turns a cited category benchmark into an unsourced claim about our own performance, which crosses two bans at once.
3. **The Phase 9 ROI calculator.** Built so the client supplies deal size and close rate. The first prospect who says "what do others usually see" is the test, and the answer is that we do not know and are not paid on it.
4. **Run B, describing the room before it is full.** Journey stage 3 requires disclosing a thin room honestly. Overstating it is the single fastest way to end the cohort, and it will feel like a small rounding at the time.

## What this audit does not cover

It checks what was written against what was permitted. It cannot check accuracy of the competitor research, which was a search-only pass with known gaps set out in `research/00-competitor-slate.md`. Two competitive statements in Run A Phase 2 and on the Run A deck, that pay-on-attendance is a category norm and that a competitor guarantees a meeting percentage, rest on third-party summaries rather than on the competitors' own pages. Both are graded C plus in the ledger and both should be confirmed before being used in a sales conversation.
