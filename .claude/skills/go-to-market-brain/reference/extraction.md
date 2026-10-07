# Extraction, turning source material into a brain

Phase 1 and 2 of the build. The job is to read everything, decide what each artifact settles, map it to a destination, and interview only for what is genuinely missing.

## Step 1, convert and read everything

```bash
python3 scripts/extract_sources.py <source_dir> sources/extracted
```

The script walks a directory and writes one Markdown file per source: every sheet of every workbook, every paragraph and table of every document, every slide of every deck, every page of every PDF. Read all of it. Do not sample. The single line that becomes a hard guardrail is usually buried in a cell comment or a footnote, not in a heading.

If a source is a live tool rather than a file, a CRM view, a board, an analytics dashboard, ask for an export or a screenshot set. If neither exists, interview the owner and record the answers as a source artifact in `sources/extracted/` with the date and the person's name, so the provenance survives.

## Step 2, write the source manifest

Before distilling anything, produce a table:

| Artifact | Type | What it settles | Dated | Destination |
|---|---|---|---|---|

"What it settles" is the important column. An artifact that settles nothing is background reading, not a source. If two artifacts settle the same question differently, stop and resolve it with the user. Silent resolution is how a brain gets a confident wrong answer at its core.

Record the manifest in `ops/asset-index.md` when the build is done.

## Step 3, map artifacts to destinations

The mapping is stable across engagements, because GTM work produces a recognizable set of artifacts whatever the consultancy calls them.

| Source artifact, by any name | Reference file | Also feeds |
|---|---|---|
| Positioning deck, category map, brand strategy | `reference/positioning.md` | Master context Section 12, `ops/copy-bank.md` one-liners |
| Strategic verdict or fork document | `reference/positioning-verdict.md` | Master context Section 9, `ops/decisions.md` |
| ICP dashboard, persona research, segmentation | `reference/icp-personas.md` | Master context Section 8 |
| Competitive market analysis, landscape, teardown | `reference/competitive-analysis.md` | Master context Section 7, `rules/do-not-say.md` scoping section |
| Feature or capability matrix, scoring model | `reference/feature-matrix.md` | Master context Section 6, `rules/feature-status.md` |
| Value proposition framework, one per audience | `reference/value-proposition-<audience>.md` | Master context Sections 10 and 11, `ops/copy-bank.md` headlines |
| Customer journey, funnel map, lifecycle model | `reference/customer-journey.md` | Master context Section 13 |
| Marketing asset library, campaign plan, calendar | `reference/marketing-campaigns.md` | Master context Section 14 |
| Product spec, roadmap, release plan | `rules/feature-status.md` | Master context Sections 3 and 5 |
| Brand voice guide, tone of voice doc | `rules/writing-rules.md` | `ops/QA-checklist.md` |
| Naming or terminology doc, product taxonomy | `rules/glossary.md` | Master context Section 2 |
| Legal review, compliance notes, security posture | `rules/do-not-say.md` | Master context Section 4 |
| Pricing model or workbook | `pages/` and `ops/decisions.md` | Only if pricing is decided. If not, it is an open question. |

### Synthesized files, the ones no source contains

Three files usually have to be written rather than extracted, and they are among the most used:

- **Battlecards.** The competitive analysis holds scores and gaps. A battlecard holds the three lines an operator says out loud. Derive one per rival: their real strength, their real gap, and how we win, in that order. Leading with the rival's genuine strength is what makes the card credible internally.
- **Objection handling.** Derive from the ICP dashboard's blockers, the competitive weaknesses, and the claim ledger. One heading per objection in the prospect's own words, then the honest answer. Where the honest answer is "not yet," say not yet. An objection file that pretends every objection is a misunderstanding trains agents to argue with prospects.
- **Channel engine.** For whichever channel the GTM actually runs on. Thesis, how the channels feed each other, the archetypes to rotate, the plan / write / edit method, hook patterns, calls to action, and what good looks like in measurement. This is the file that turns a channel strategy into repeatable production.

## Step 4, distill rather than transcribe

The compression is the value. A twelve-tab workbook becomes forty lines, and those forty lines are the ones an operator would actually consult.

What survives distillation:

- **Decisions and their reasoning.** Especially the reasoning, because it is what stops the decision being reopened.
- **Numbers with consequences.** A score that determines whether a capability leads messaging survives. A score that changes nothing does not.
- **Language that was approved.** Headlines, reframes, and taglines move to `ops/copy-bank.md` verbatim.
- **Constraints.** Anything that starts "we cannot say," "not until," or "only in" becomes a rule.
- **The shape of a model.** Keep the axes, the quadrants, and the placements. Drop the intermediate arithmetic.

What gets dropped: process notes, meeting history, alternatives that were considered and rejected without a live rationale, formatting, and every restatement.

Two tests for a distilled line. First, would an operator look this up? If not, cut it. Second, if this line were wrong, would an asset go out wrong? If yes, it belongs in a ledger, not in prose.

### Preserve, do not paraphrase

Three categories must be copied exactly, never reworded:

1. Approved copy. A paraphrased headline is an unapproved headline.
2. Legal and compliance phrasing. The exact permitted form of a claim is the claim.
3. Canonical terms. Including the capitalization.

## Step 5, the gap interview

Ask in one batched round. Prefer questions whose answers change the build, and offer a default so the user can confirm rather than compose.

**Almost always missing:**

1. **Channel mix.** Which channels are in, and which are explicitly out. "Out" matters more than "in," because it becomes a refusal rule. A GTM that excludes cold outreach, or paid, or a platform, needs that written as a hard ban.
2. **Proof points.** The exact set of real, permissioned facts: customer counts, metrics, named logos, quotes, certifications. This becomes a closed list, and everything outside it is fabrication. Get the precise permitted wording of each.
3. **Status by capability.** Which capabilities are live today, which are partial, which are committed but unshipped, which are vision. Without this the brain will describe a roadmap as a product.
4. **Forbidden words and claims.** The house bans, the competitor terms, the phrases legal has already rejected, the words that belong to a partner or platform.

**Often missing:**

5. Audience count and split. One audience or several, and the rule for never blending them.
6. Tone anchors. Two brands whose voice is right, and two that are wrong.
7. Pricing status. Decided, or a separate engagement. If undecided, prices become a hard ban.
8. Anything historical to handle rather than repeat: a rebrand, a prior product's reputation, a public incident.
9. Review authority. Who signs off on a claim change, and who owns each ledger.
10. Cadence. How often the ledgers get reviewed, and what the corroboration threshold is for acting on a signal.

If an answer does not exist yet, write it into `ops/decisions.md` as an open question with an owner. An open question recorded is a working brain. An open question guessed is a broken one.

## Step 6, seed the decision log during the build

Every strategic call the sources already settled becomes a dated entry in `ops/decisions.md` as you distill it, not afterwards. Include the rationale in one or two sentences, because the rationale is what prevents the decision being reopened in six months by someone who was not in the room.

By the end of the build the decision log should already hold five to ten entries. A brain that ships with an empty decision log has thrown away the most valuable thing the source material contained.
