# Worked example, a real brain end to end

The blueprint reverse engineered from a live instance: a B2B SaaS go-to-market built from nine strategy dashboards into a working context repository. Read this when an abstract instruction in the build needs a concrete shape.

Company details are anonymized. The structure, the ratios, and the failure modes are exactly as they occurred.

## What the sources were

Nine artifacts from a GTM engagement, plus a product spec:

| Artifact | Format | What it settled |
|---|---|---|
| Product Feature Matrix | XLSX, scored on two axes | Which capability leads messaging, which is table stakes, which is the top-of-funnel hook |
| Competitive Market Analysis | XLSX, 8 competitors x ~40 rows | The competitor set, four scoring vectors, per-rival gaps, the wedge |
| ICP Dashboard | XLSX | Two ICP stages, a three-level buying committee per stage, the design-partner profile |
| Value Proposition Framework x2 | DOCX, one per audience | Brand promise, positioning, three pillars, nine reasons to believe, each at three copy lengths |
| Positioning Verdict | DOCX | A strategic fork, resolved, with five-dimension reasoning |
| Positioning deck content | MD | Category, vectors, scatter data, differentiation |
| Customer Journey Funnels | XLSX, 3 tabs | Two funnels x seven stages: mindset, assets, KPI, owning function |
| Marketing Assets Library | XLSX | Six campaigns and the asset backlog under each |
| Product spec | Doc | Every capability and its real build status |

The pattern to notice: these artifacts are recognizable across engagements whatever the consultancy calls them. The mapping table in `extraction.md` is built from exactly this set.

## What was built from them

Twenty-six files in the first pass. The compression ratio is the point: nine multi-tab workbooks and documents became one 444-line master context plus a control layer small enough to load on every task.

### The distillation

Everything went into `context/<Project>_GTM_Master_Context.md`, sixteen numbered sections, YAML frontmatter carrying version, last updated, status notes, and the canonical vocabulary as a flat list. Section 0 was written as instructions to the agent reading the file: what it is, a five-step method for using it, and six hard guardrails stated as absolutes.

Section 15 is a flat cheatsheet: one-line positioning, flagship differentiator, table stake, top-of-funnel hook, the two audiences, the two ICP stages, the permitted proof points, the signature reframe, the primary rival, the warm channels, the do-not-say list, and the mechanics. Twelve lines that answer most lookups without a full read.

### The lift

Four sections of the master context were lifted into standalone files under `rules/`:

| Master context section | Became | Why it was lifted |
|---|---|---|
| 1. House writing rules | `rules/writing-rules.md` | Checked on every word of output |
| 2. Canonical vocabulary | `rules/glossary.md` | Checked on every noun |
| 3. Feature status ledger | `rules/feature-status.md` | Checked on every capability mention |
| 4. Claim hygiene ledger | `rules/do-not-say.md` | Checked on every superlative |

The duplication is deliberate. The master context is the reference brain and is loaded when strategy is in question. The four rules files are the enforcement layer and are loaded always, which only works because they are short.

Each lifted file gained something in transit rather than being a copy. The writing rules gained a "writing for the ear" section once video became a primary channel. The claim ledger gained a scoping section with the counter-example beside each narrowed claim.

### The routers

Three entry files, each under sixty lines, each restating the same read order and the same non-negotiables:

- `CLAUDE.md`, the primary router, with the read-order list, the channel rule, the audience rule, the short-form non-negotiables, and the pre-ship instruction.
- `AGENTS.md`, near-identical for tools that read `AGENTS.md`, opening with the tie-break rule: if the two differ, `CLAUDE.md` wins.
- `llms.txt`, a linked index of every file grouped by layer, each with a one-line purpose.

`README.md` is the human file: what the product is, why the GTM is shaped this way, a folder table with a "when the agent uses it" column, seven use cases, five ROI lines, the one rule that matters most, and the maintenance rule.

### The reference layer

One short file per source artifact, each opening with a line naming the source dashboard it distills and what to load it for.

Three files were synthesized rather than extracted, and they turned out to be the most used:

- **Battlecards.** Derived from the competitive workbook. Three lines per rival: their real strength, their real gap, how we win. Leading with the genuine strength is what makes the card credible.
- **Objection handling.** Derived from the ICP dashboard's blocker rows plus the claim ledger. Eight objections in the prospect's own words. Where the answer is "not yet," it says not yet.
- **Channel engine.** The strategy file for the channel the GTM actually runs on. Thesis, how the channels feed each other, six long-form archetypes, six social archetypes, the plan / write / edit method, hook patterns, pacing, calls to action, and what good looks like in measurement. Every content template points back to it.

### The execution layer

Seven templates, one per channel actually in the mix, each ending with a guardrail line pointing back at the rules. Examples per major asset type, each closing with a short "why this works" so the voice is teachable. A prompt library of filled, runnable prompts per recurring job, each naming its files and ending with the QA instruction. The prompt file states explicitly that there are no prompts for the excluded channel, which is a rule expressed as an absence.

### The state layer

Copy bank grouped by use: reframes, hooks, one-line positioning, per-audience headlines, proof points, calls to action. Decision log, newest first, seeded during the build with every call the sources already settled. Asset index. QA checklist, thirty-odd tickable items grouped writing, channel, claims, naming, audience, scripts, voice.

## How the guardrails were derived

The instructive part. Every hard guardrail traces to a specific tension in the source material, and none of them were invented as general good practice.

| Source tension | Became |
|---|---|
| A certification was in progress and sales wanted to imply it was earned | Hard ban, with the exact permitted phrasing and the public timeline |
| The product spec listed committed but unshipped capabilities | Four-flag status ledger, plus a rule that nothing unshipped may be demoed as live |
| A privacy claim was true in one product mode and false in another | Scoped claim, plus a glossary row forbidding the two modes to blur |
| Pricing was a separate, undecided engagement | Hard ban on prices, tiers, and plan names, and an open item in the decision log |
| One real proof point existed, with pressure to imply more | Closed proof-point set, everything outside it named as fabrication |
| The incumbent platform owned a common noun the product also needed | Glossary row banning the platform's term for the product's own container |
| A verdict to expand beyond the first platform had been decided | Ban on single-platform framing, paired with a ban on claiming expansion as shipped |
| Four "only in the category" claims sat in the strategy deck | Each run through the counter-example drill. Three were narrowed, one held. |
| The GTM excluded an entire acquisition channel | Channel discipline rule in four files, and an absence in the prompt library |

The last row is the one people underestimate. A channel exclusion is not a preference to note once. It appears in the router, the writing rules, the claim ledger, and the QA checklist, because a direct request to write for that channel arrives eventually and the brain has to refuse it.

The counter-example drill in row eight is worth doing properly. Of four superlatives that the strategy deck stated flatly, only one survived contact with a real search for counter-examples. The other three were true in a narrower form that was still differentiating, and the narrow forms are what shipped.

## The compounding loop, visible in the history

The repository's own commit history demonstrates the update protocol before it was ever written down.

Later commits added new source documents, which became new `reference/` files, which were then added to `llms.txt`. Then a positioning decision landed, a category reframe that changed how the product was described without changing what it did. What happened next is the AMEND procedure exactly:

1. A dated entry went into `ops/decisions.md` with the verdict and the rationale.
2. That entry carried an explicit line: this is a positioning reframe of the existing capability ledger, nothing in the status ledger changed as a result, and every unshipped capability stays marked coming soon.
3. New approved lines were added to `ops/copy-bank.md` under a heading for the new positioning, with the prior one-liner kept and annotated as still accurate for contexts where the new frame would not land.
4. Only then were finished assets produced in `pages/` on the new positioning.
5. `llms.txt` was updated to index them.

Ledger, then decision, then copy, then assets, then index. That commit sequence is the loop in `compounding.md`, and the "nothing in the status ledger changed" line is the "what this does not change" field that the decision template now requires.

## What the example was missing

Two things this skill adds, because their absence was the brain's only real weakness:

- **No signal intake.** The decision log recorded conclusions but nothing recorded the market input that produced them. There was no place for a prospect's objection, a churn reason, or a competitor move to land before it became a decision, so most of that input was lost. `ops/signal-log.md` and the triage protocol exist because of this gap.
- **No periodic snapshot.** Nothing captured funnel, channel, segment, and competitive state on a clock, so drift would only surface when someone happened to notice. `snapshots/` and the review cadence exist because of this gap.

Everything else in the blueprint is a generalization of what that repository already did well.

## What the audit found on a real brain

Running `scripts/audit_brain.py` against the source repository, eighteen months into its life, returned four errors and seven warnings. The errors were three index links pointing at example files that had never been written, plus the missing signal log. The warnings were dominated by one pattern: not a single `rules/` file carried a `last_reviewed` date, so nobody could tell whether the claim ledger reflected the current product.

Both failures are invisible from the inside and neither shows up in the work product until something wrong ships. That is the argument for running the audit on a schedule rather than at build time only.
