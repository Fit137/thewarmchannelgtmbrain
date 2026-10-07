# Handover

> **HISTORICAL RECORD.** This documents a run completed before the
> 2026-09-22 repositioning in `POSITIONING.md`. It is deliberately not edited:
> a record of what was researched and decided is only useful if it is not
> rewritten afterwards. Read it as evidence of what was done, not as a current
> specification.

What to upload, where it goes, what to decide, and the prompts to hand to whoever does the next piece of work.

Written 2026-09-18, after the `gtm-builder` run. The source of truth is the markdown in the repository. The files in `dist/` are renderings of it, and `tools/build_outputs.py` rebuilds them.

---

# 1. What to upload to Google Drive

28 files in `dist/`. Suggested folder structure, and it matters more than it looks, because the claim constraints have to travel with the output.

```
The Warm Channel GTM/
├── 00 Start here/
│   ├── RUN_LOG                  what ran, what is open, who has to finish it
│   ├── HANDOVER                 this document
│   └── CLAIM_AUDIT              every claim checked against Section 5
├── 01 Inputs/
│   ├── GTM_BRIEF                Section 5 is the claim constraints
│   └── SKILL_ADAPTATION         the six substitutions applied
├── 02 Research/
│   ├── R0_competitor_slate
│   ├── R_evidence_ledger        every figure cleared for use, with its grade
│   └── RESEARCH_GAPS_PROMPTS    the five gaps, pre-filled, ready to run
├── 03 Run A, the client/
│   ├── A1_service_offer_matrix        A6_value_proposition
│   ├── A2_competitive_analysis        A7_customer_journey
│   ├── A3_positioning_statements      A8_assets_library
│   ├── A4_icp_dashboard               A9_pricing_dashboard
│   ├── A5_buying_committee            A_lead_magnet_spec
│   ├── A_scorecard_spec               A_gtm_walkthrough.md
├── 04 Run B, the guest/
│   ├── B1_offer_icp_positioning       B8_channels
│   ├── B5_founding_guest_cohort       B9_attendance_cost_reading
│   ├── B6_value_and_journey           B_gtm_walkthrough.md
└── 05 Decisions/
    ├── DECISION_SHEET           the seven open decisions, with the run's read
    └── COUNSEL_BRIEF            send as-is, highest priority item here
```

## Conversion, and one thing to get right

| Format | Do this |
|---|---|
| `.xlsx` | **Convert to Google Sheets on upload.** These are working documents that need commenting and editing, particularly the competitor slate and the pricing dashboard. In Drive settings, turn on "Convert uploads to Google Docs editor format", or right click and Open with Google Sheets, then File, Save as Google Sheets |
| `.docx` | Convert to Google Docs, same reason. `A6_value_proposition` is the one people will comment on most, because it is the copy |
| `.md` | **Do not convert, and do not open in Docs.** The two `gtm_walkthrough.md` files are for pasting into Gamma AI. Converting them breaks the slide separators. Upload as-is, or keep them out of Drive and paste from the repository |

## The two files that must not be separated from the rest

`R_evidence_ledger` and `CLAIM_AUDIT`. Every number in every other file traces to the ledger with a grade, and the audit is what keeps the run honest. A dashboard read without them looks like it contains more evidence than it does. If someone is only going to open two files before writing something client-facing, those are the two.

---

# 2. Decisions that have to be made by a person

Full version in `05 Decisions/DECISION-SHEET`. Short version, in the order they block things.

| # | Decision | Blocks | My read after the run |
|---|---|---|---|
| 1 | Register a business name, get a tax number | Everything past journey stage 4, and the scorecard email sequence | Do it first. It is plumbing, not strategy, and the funnel fails at the last stage without it after every earlier stage has worked |
| 5 | Written counsel position on CASL and PIPEDA | Two of three guest-side channels, and the demonstration room | **This is the binding constraint on the business and it is invisible in Run A's documents.** Brief in `COUNSEL-BRIEF` |
| 4 | The attendance floor, its remedy, the assumed show rate | The strongest copy in Run A, and any quote for The Room | The Clutch benchmark gives you the arithmetic shape. Twelve seats needs roughly seventeen confirmations at 70% |
| 3 | Reconstruct the two commissioned rooms into an auditable table | The most persuasive claim available, currently unusable | Cheapest unblocking action in the whole run. It is an afternoon with send records |
| 2 | Confirm or reject the price bands | Every number in Phase 9 | Correctly last. A price set before the floor is a guess wearing a number |
| 7 | Does the founder attend and facilitate | Phase 1 item 4, Phase 9 scope, and holding the no-pitching line | Attend the first three. On the guest side this is how the format survives contact with a paying client |
| 6 | Healthcare guest list out of scope | Run B, Section 5 | Already applied throughout as a consent boundary |

---

# 3. Handover prompts

Five, for five different recipients. Each is written to be pasted whole.

## Prompt A. A new Claude session picking this up

Use this when the context has been lost and someone wants to continue the work rather than redo it.

```
You are continuing a go-to-market build for The Warm Channel, a pre-launch
done-for-you convening service in Toronto. The gtm-builder skill has already
been run in full, twice, and the output is in this repository.

Read these four files before doing anything else, in this order:

1. RUN-LOG.md            what was produced, what is still open
2. GTM-BRIEF.md          the input brief. Section 5 is the claim constraints
3. SKILL-ADAPTATION.md   the six substitutions that were applied
4. CLAIM-AUDIT.md        what has been checked and what could still break

Then read research/evidence-ledger.md. It is the list of every figure cleared
for use, with its source and grade. A figure not on that list does not go in
any document. If a phase needs a number that is not there, write {TBD}.

The rules that govern everything you write, taken from GTM-BRIEF.md Section 5,
and they are not negotiable:

- The business is pre-launch. No entity, no client, no delivered engagement.
  The proof set is empty and closed. Every proof point is {TBD}.
- The founder has a real prior record. It is a credential, not a proof point.
  Section 5 carries the permitted wording. It never goes in a proof field,
  and four of those claims are gated on artifacts that do not exist.
- Never write: any client count, attendee total, named client, testimonial,
  quoted praise, logo, conversion, meeting, pipeline or revenue figure, any
  guarantee of an outcome beyond attendance, any unsourced market statistic,
  any claim of an existing standing guest network, or anything drawn from the
  healthcare guest list.
- Two audiences, two vocabularies. Client-facing copy describes composed
  attendance. Guest-facing copy describes a room of peers and a live question.
  Client language never reaches a guest-facing surface. A guest who reads the
  client copy learns they were inventory, and the guest list is the only asset
  this business has.
- Mechanics: no em dash, no en dash, use commas. Do not use the words
  leverage, unlock, seamless, robust, streamline, cutting-edge or empower.

Run `python3 tools/lint_claims.py` before you finish. It fails on a mechanics
violation and warns near a banned claim. Rebuild the distributables with
`python3 tools/build_outputs.py`. The markdown is the source of truth, the
files in dist/ are renderings.

Tell me what you intend to change before you change it.
```

## Prompt B. Closing the research gaps

For a person with a browser, or a research tool that can reach commercial sites. The environment this ran in could not.

Full pre-filled versions are in `handover/RESEARCH-GAPS-PROMPTS.md`. The five gaps, in priority order:

1. The negative themes from step 2.7, which came back empty and which two positioning vectors are waiting on.
2. The Canadian trade show booth all-in cost, which is the strongest line in the pricing phase and is blank.
3. Direct site reads for the six competitors, for taglines, scope lines and published terms.
4. Live field marketing job postings in Canada, for the responsibilities list rather than the salary.
5. Whether a Canadian operator exists in slot 1 at all.

## Prompt C. Generating the decks in Gamma AI

```
Paste the entire contents of A_gtm_walkthrough.md into Gamma AI, using
"Paste in text" rather than "Generate from a prompt".

Set: 10 cards. Do not let Gamma add, split or merge slides, because the
structure is exactly the nine dashboards plus a title and each slide carries a
"So what" line that ties it to customer acquisition.

Do not let Gamma rewrite the copy. Every claim in these slides has been checked
against a constraints document and several sentences are deliberately narrower
than they read. In particular {TBD} appears where a number is unknown and it
must stay. If Gamma replaces a {TBD} with a plausible figure, that figure is
invented and has to come out.

Repeat for B_gtm_walkthrough.md as a separate deck. Do not merge the two. They
address different audiences and blending them produces a value proposition true
of neither.
```

## Prompt D. Building the scorecard in ScoreApp

```
Build the scorecard specified in A_scorecard_spec (or A_lead_magnet_spec for
the tables alone).

Seven questions, scored out of 100. The scoring values per answer are in the
spec and should be entered exactly, because the branching depends on them.

The important part, and it is easy to lose in the build: questions 1 to 3 sum
to a coverage score and questions 4 to 6 sum to an access score. The result
page names whichever is WEAKER. That branch is the whole intelligence of the
thing. A result that says "your score is 42" is worth nothing. A result that
says "only four of your fifty accounts have a Toronto decision maker" is worth
the build.

Note the scale direction: a LOW score is the problem, so the strongest call to
action sits at the bottom of the range, not the top. This is inverted against
the usual template.

The result page must not contain: any Warm Channel performance figure, any
testimonial, any client logo, any close rate, or any claim that a room run by
The Warm Channel would have filled. The 70% attendance benchmark may appear,
attributed to Clutch Events with its sample size, described as a category
benchmark.

Do not switch the email sequence on until the business is registered. Every
email needs a physical mailing address to be compliant.
```

## Prompt E. Counsel

In `handover/COUNSEL-BRIEF.md`, written to be sent as-is. It is the highest-priority item in this handover, because it gates the demonstration room, and the demonstration room is what produces the first reference, the first guest cohort and the first auditable funnel table in one exercise.

---

# 4. What a reader will get wrong unless you tell them

Four things, from the run.

1. **The dashboards look more evidenced than they are.** Competitor weaknesses are `{TBD}` across the board, because a search-only pass returned no buyer-side complaints. Two positioning vectors are built structurally rather than from complaint data and are marked as such inside the file. Anyone quoting Phase 2 in a sales conversation needs to have read that marking.
2. **Two different 70% figures are in play.** The banned unaudited reply rate, and the cleared Clutch attendance benchmark. They are unrelated numbers that share a value, and a listener who hears both in one conversation will merge them into the banned claim wearing a citation.
3. **Pay-on-attendance is not the differentiator.** It reads like one and it is a category norm among the better operators. The differentiator is the floor plus the remedy, which is `{TBD}` until decision 4.
4. **Run B is not the second half of Run A.** It is the supply side, the business cannot deliver Run A without it, and two of its three channels are legally blocked today.

---

# 5. If someone only has twenty minutes

Give them, in this order: `RUN-LOG`, then the Run A deck, then `CLAIM_AUDIT`. That is what was built, what it says, and what is not yet safe to claim.
