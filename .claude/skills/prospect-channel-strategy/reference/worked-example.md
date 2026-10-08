# Worked example, Acme Example Co.

Load for: a first run of the skill, or to see what "done" looks like for any phase.

**Fictional.** Acme Example Co. does not exist. Every fact about Acme is invented to show the shape of a real strategy. The market figures are real, from the brain's evidence ledger. Never reuse a sentence about Acme for a real company.

The files: `assets/example/strategy.json` and `assets/example/evidence-register.md` in this skill, and the deck they produce, `assets/example/deck.json`, in the prospect-deck-builder skill.

```bash
python3 scripts/gate.py --from assets/example/strategy.json
python3 scripts/evidence_check.py assets/example/evidence-register.md --mode BUILD
python3 scripts/validate_strategy.py assets/example/strategy.json --register assets/example/evidence-register.md
python3 ../prospect-deck-builder/scripts/new_deck.py assets/example/strategy.json --out /tmp/acme-deck.json
```

## Phase 0, the gate: GO, 12 of 18

| Criterion | Score | Why |
|---|---|---|
| ACV | 2 | Case studies describe enterprise-wide rollouts and pricing is contact-sales only. An inference (E09, P3), so 2, not 3. Confirmed on a call or not at all |
| Event spend | 3 | A SecureCon booth, an Identity Summit sponsorship, two Security Forum breakfasts and an own conference, all on public pages (E03 to E07) |
| Unreachable cold | 2 | CISOs and heads of identity at regulated enterprises, from the case studies (E02) |
| Warm and cold | 2 | Peer references throughout the case studies, no advisory board found |
| Converts badly | 1 | Unknown from outside, the normal score |
| Owner and list | 2 | A field marketing job post measured on "pipeline from our named accounts" (E08) |

No disqualifier, no zero, ACV and event spend at 2 or more, total 12: GO.

## Phase 2, the footprint

| Moment | Today | Density | Access | Quadrant |
|---|---|---|---|---|
| SecureCon (April) | Booth | 14.2 | -7.4 | Wrap with a private programme. **Anchor** |
| Identity Summit (June) | Sponsorship | 8.6 | -2.3 | Wrap, near the axis |
| Security Forum breakfasts (February, November) | Attendee seats | 5.4 | 4.6 | Build on, with access that comes without a choice of guests |
| Acme Connect (October) | Their conference | -6.1 | 11.8 | Keep for customers |
| Partner roadshow (September) | Co-hosted sessions | -3.8 | 3.2 | Keep for customers, near the axis |

The anchor is SecureCon: the widest gap between density and access, and the largest spend. The chart's claim, written after scoring: "Your buyers are densest where your access is thinnest." The anchor line: "Your buyers will be at SecureCon. The booth is not where you get time with them."

Note the decimals. 14.2 and 8.6 say SecureCon is clearly denser than the Summit. Writing 14 and 9 would say almost nothing.

## Phase 3, the committee

Four roles, all from the case studies or an inference with its basis written (E02, E10): the CISO signs, the head of identity owns the problem, the security architect evaluates, the risk lead weighs exposure. Tiers by type, every count `{TBD}`: "A full coverage read on your named list fills them in."

No reply rate, anywhere: the deck uses the 70% dinner benchmark, so the cold-channel slide argues in words: "Each approach lands alone, in an inbox every other vendor is also writing to."

## Phase 5, the plan

| Moment | Recommendation |
|---|---|
| SecureCon | Keep, and wrap with two private tables that week |
| Identity Summit | Keep, and host one table the evening before |
| Security Forum breakfasts | Redirect the budget into your own tables: the upgrade for seats that come without a choice of guests |
| Acme Connect | Keep for customers, add an expansion table |
| Partner roadshow | Keep for partners. No change |

Formats: show-week tables, metro tables (where public evidence shows Tier 1 accounts cluster), an expansion table. The carrying line, which becomes the still slide: "Keep the moments you already fund. Add private tables for your named accounts around them. Follow through with the guests who choose to continue."

## Phase 6, the questions

Machine identities (verified: three sessions at Identity Summit, E14), recovery (verified, E15), and budget (not verified, carried with the verification line and flagged in before_you_send). The invitation sample is guest copy only, and uses the approved line "No attendee list is circulated, before or after."

## Phase 7, the arithmetic

Twelve seats at the 70% dinner benchmark: about seventeen confirmations. At a vendor-owned conference's 19%, the same twelve needs about sixty-three, which is the argument for the format. People approached: `{TBD}`, set by the coverage read.

After the evening, in the consent framing only: "After the evening, the conversation continues only with guests who choose it, and nobody is chased. How that step works is designed with you, and it is not offered until that design is settled."

## Phase 8, the economics

40.8% of exhibitor budgets go to the booth (CEIR 2026, B). A badge scan costs $112 to $300 (CEIR, B). Acme's own scans and spend: `{TBD}`. Three ways to spend the same budget, in words. The calculator: empty, six inputs, all Acme's.

## Phase 9, how to run it

In-house with the plan, with The Warm Channel, or a mix. "Fill" carries "Opens once our privacy position is written". "Follow through" carries "Not offered until that design is settled". The honesty line, verbatim. One call to action.

## Phase 10, before you present

Verified: the Clutch Events and CEIR figures with their ledger rows. Needs settling: the call to action address, which is a placeholder, and founder approval of the calculator copy. Designed, not supplied: every fact about Acme, the quadrant positions, the seat counts, the motif's mark count.

`validate_strategy.py` passes with two warnings, both answered here: the unverified budget question, and the placeholder call to action.
