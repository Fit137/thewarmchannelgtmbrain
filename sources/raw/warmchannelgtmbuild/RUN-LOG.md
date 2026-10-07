# gtm-builder run log

> **HISTORICAL RECORD.** This documents a run completed before the
> 2026-09-22 repositioning in `POSITIONING.md`. It is deliberately not edited:
> a record of what was researched and decided is only useful if it is not
> rewritten afterwards. Read it as evidence of what was done, not as a current
> specification.

Skill: `gtm-builder` v3.1.0, B2B SaaS Go-To-Market Builder. Run 2026-09-18 against this repository, using `GTM-BRIEF.md` and `SKILL-ADAPTATION.md` as the brief instructed.

## What was produced

| Folder | Contents |
|---|---|
| `research/` | Step 0 competitor slate, findings for steps 1.1, 2.1 and 2.7, and the evidence ledger |
| `run-a-client/` | Run A, the paying client. Nine dashboards, the lead magnet spec, the 10-slide deck |
| `run-b-guest/` | Run B, the guest. Adapted phases, the founding guest cohort, the 10-slide deck |
| `dist/` | The file formats the skill's OUTPUT FORMAT MAPPING asks for. 13 XLSX, 6 DOCX, 2 MD |
| `CLAIM-AUDIT.md` | Every claim in both runs checked against `GTM-BRIEF.md` Section 5 |
| `handover/` | Handover document with the Drive upload guide and five prompts, the decision sheet, the counsel brief, and the five research gap prompts pre-filled |
| `tools/build_outputs.py` | Rebuilds `dist/` from the markdown. The markdown is the source of truth |
| `tools/lint_claims.py` | Checks the mechanics rules in Section 5, which are absolute and lexical. Fails on an em dash, an en dash or a banned word. Warns, rather than fails, near a banned claim, because a pattern cannot tell an assertion from a report of one |

Rebuild the distributables with `python3 tools/build_outputs.py`. Check the mechanics with `python3 tools/lint_claims.py`, which currently reports 0 errors and 5 warnings, all of them documents describing a banned claim in order to forbid it.

## Execution checklist

The skill's own tracker, marked.

```
RESEARCH (added by RESEARCH-PROMPTS.md, not in the skill)
  [x] Step 0   Competitor slate sourced and verified   PARTIAL, see limits
  [x] 1.1      Service demand research                 PARTIAL
  [x] 2.1      Competitor deep research                PARTIAL
  [x] 2.7      Review analysis, substituted            PARTIAL, negative themes absent

RUN A, the client
  [x] PHASE 1  Service and Offer Matrix, six vectors
  [x] PHASE 2  Competitive Market Analysis, 2.2 to 2.16
  [x] PHASE 3  Positioning, three statements
  [x] PHASE 4  ICP, two levels re-read as problem maturity
  [x] PHASE 5  Buying Committee, two ICPs, design partner
  [x] PHASE 6  Value Proposition, 3 pillars, 9 RTBs, 9 copy drills
  [x] PHASE 7  Customer Journey, 7 stages, payment blocker added first
  [x] PHASE 8  Assets and Collaterals, all three channels replaced
  [x] PHASE 9  Pricing and Packaging, engagement pricing, all numbers {TBD}
  [x] LEAD MAGNET   Room Readiness Scorecard, ScoreApp
  [x] DECK          10 slides, validated against the skill's output rules

RUN B, the guest
  [x] PHASE 1-4     Offer matrix, competitive set, positioning, ICP
  [x] PHASE 5       Committee collapsed. Founding guest cohort as the deliverable
  [x] PHASE 6-7     Value proposition and guest journey
  [x] PHASE 8       Three channels, no advertising, no sequenced email
  [x] PHASE 9       No pricing. Attendance cost reading substituted
  [x] DECK          10 slides
```

## The substitutions that were applied

All six from `SKILL-ADAPTATION.md`, plus two the run added and recorded.

| Phase | Applied |
|---|---|
| 1 | Six-vector service matrix. The List surfaced as highest value, and the file says honestly that only the Funnel Role vector produced that result |
| 2 | G2 abandoned. In-housing and the hire profiled as non-companies. Own-product row filled from the brief with strengths and weaknesses `{TBD}` |
| 4 | Levels re-read as problem maturity. Level 2 came out as the better buyer |
| 5 | Run A as written. Run B collapsed to one persona, effort moved to 5.2 |
| 6 | All 18 proof fields held at `{TBD}`. Social proof slots substituted with method |
| 8 | All three channels replaced, with the reasoning named |
| 9 | Engagement pricing. Per-outcome denominator rejected absolutely |
| **Added** | The ROI calculator in Phase 9 was rebuilt so the client supplies deal size and close rate, because the skill's version requires a conversion claim that Section 5 bans |
| **Added** | The scorecard scale direction was inverted against the skill's template, because what is measured is readiness and a low score is the problem |

## What is not finished, and who has to finish it

### Research gaps, and they are real

The three external steps were run with web search rather than by a person with a browser, because the egress proxy in this environment blocks most of the commercial domains involved. Consequences, worst first:

1. **No competitor weakness data at all.** Step 2.7 asks for a positive and negative theme breakdown per competitor. The positive side is thin but real. **The negative side returned nothing.** Phase 2 vectors 3 and 4 are therefore structural rather than review-derived, which is weaker ground, and they are marked as such at the point of use. Revisit these two first when the research is done properly.
2. **No direct site reads.** Every competitor tagline, sub-tagline and scope line in Phase 2 is `{TBD}`.
3. **No Canadian trade show booth price.** This is the strongest line in Phase 9 Anchor 2 and it is empty. The Canadian Finance Summit sponsorship package is public at `canadianlenders.org` and is the fastest fix.
4. **No live job postings for slot 5.** Salary aggregates were used instead, which is not the same thing.
5. **No Canadian competitor found in slot 1.** Either none exists, which is the opportunity, or the search did not reach it. Those are very different facts and it is cheap to rule out.

Two competitive statements used in Run A rest on third-party summaries rather than the competitors' own pages, are graded C plus, and should be confirmed before they are used in a sales conversation: that pay-on-attendance is a category norm, and that a competitor guarantees a meeting percentage.

### The seven open decisions, in the order they block things

| # | Decision | What it blocks now | Status |
|---|---|---|---|
| 1 | Register a business name and get a tax number | **Everything downstream of Phase 7 stage 4.** No invoice a corporate accounts payable department will accept. Also blocks the scorecard email sequence, which needs a mailing address for CASL compliance | Open |
| 5 | Written counsel position on CASL and PIPEDA | **Two of three Run B channels, and the demonstration room**, which is the highest-value action in either run. This is the binding constraint on the whole business and it is invisible in Run A's own documents | Open |
| 4 | The attendance floor, its remedy, the assumed show rate | Phase 6 drill 5, the strongest copy in Run A, currently a template. Phase 9 cannot quote The Room without it | Open |
| 3 | Reconstruct the two commissioned rooms into an auditable table | The most persuasive claim available to the business is unusable. Cheapest unblocking action in the whole run | Open |
| 2 | Confirm or reject the price bands | Every number in Phase 9 | Open, and correctly last. A price set before the floor is a guess wearing a number |
| 7 | Whether the founder attends and facilitates | Phase 1 item 4, Phase 9 scope, **and Run B factor 5**, which is someone holding the no-pitching line when a paying client starts selling from the floor | Open |
| 6 | Healthcare guest list out of scope | Confirmed and applied throughout as a consent boundary | Applied |

### Business context still blank

`GTM-BRIEF.md` Section 4. Monthly burn and runway are `{TBD}`, and Phase 8 and Phase 9 both read from them. The channel plan currently assumes a business that cannot afford to buy evidence, which is probably right, and it is an assumption rather than a calculation.

## The three things worth doing first

Drawn from across both runs, not from any single phase.

1. **Get the written consent position.** It gates the demonstration room, and the demonstration room produces the first reference, the first guest cohort and the first auditable funnel table in one exercise. Every `{TBD}` in Run A Phase 6 is waiting on it indirectly.
2. **Register the entity.** It is not persuasion, it is plumbing, and the funnel fails at the last stage without it after every earlier stage has worked.
3. **Open the association conversation.** Route 3 in Run B is the only guest-side channel not blocked by anything, and it is the slowest, so it should start before the others become available rather than after.

## A note on what this run could not tell you

The two runs are internally consistent and the claim audit is clean, which means the output does not contain invented evidence. It does not mean the strategy is right. The largest untested assumption is the one the brief itself flagged and the research could not check: that fintech is less crowded than cybersecurity for this format. The saturation half is documented. The fintech half is assumed, by the brief and now by nine dashboards built on top of it. It is one afternoon of asking Canadian bank executives what they currently get invited to, and it is worth doing before the first room is priced.
