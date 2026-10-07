# Blueprint, the file map of a Go-to-Market Brain

The full structure, what each file holds, when it loads, and how big it is allowed to get. Build only what the project needs, but do not drop a layer.

```
<project>-gtm/
  CLAUDE.md                                  router, Claude Code and Claude apps
  AGENTS.md                                  router, tools that read AGENTS.md
  llms.txt                                   machine-readable index of every file
  README.md                                  human orientation and ROI
  context/
    <Project>_GTM_Master_Context.md          the distilled source of truth
  rules/
    writing-rules.md                         how every word is written
    do-not-say.md                            claim hygiene, forbidden and safe forms
    feature-status.md                        shipped / partial / in build / roadmap
    glossary.md                              canonical vocabulary
  reference/
    <one file per source artifact>           positioning, ICP, competitive, journey, value props
    <synthesized files>                      battlecards, objection handling, channel engine
  templates/
    <one per channel in the mix>             skeletons to fill, not blank pages
  examples/
    <one per major asset type>               approved gold standard, the voice reference
  pages/
    <finished long-form assets>              shipped copy, updated rather than rewritten
  prompts/
    common-tasks.md                          filled prompts for recurring jobs
  ops/
    copy-bank.md                             approved language, reusable verbatim
    decisions.md                             what was decided, when, and why
    signal-log.md                            raw market input and its disposition
    asset-index.md                           where sources and surfaces live
    QA-checklist.md                          the pre-ship gate
    review-cadence.md                        who reviews what, how often
  snapshots/
    YYYY-MM-DD-<label>.md                    dated state captures and what they changed
  adapters/
    <one pointer file per tool in use>       Codex, Cursor, Windsurf, Copilot, Gemini
    portable-control-layer.md                dated, for chat models with no file access
  sources/
    raw/                                     original dashboards and decks
    extracted/                               machine-readable text dumps
```

## Layer by layer

### Routers, always loaded

Three files, same content, three audiences. They are traffic control, not content. If a router starts explaining strategy, move that text into `context/` and leave a pointer.

Each router carries five things and nothing else: what this repo is, the numbered read order for the control layer, the audience split, the non-negotiables in short form, and the pre-ship instruction. Budget sixty lines. `CLAUDE.md` wins if the routers ever disagree, and `AGENTS.md` should say so.

`llms.txt` is different in kind: a linked index of every file with a one-line purpose each, grouped by layer. It exists so an agent can decide what to open without opening anything. Every new file gets a line here or it is effectively invisible.

`README.md` is for people. What the company is, why the GTM is shaped this way, the folder table, the use cases, where the return comes from, and the maintenance rule.

### adapters/, one door per tool

Pointer files, about twenty lines each, that make a tool other than Claude Code load the control layer before it writes. One per tool someone on the team actually runs, and no more, since an adapter for a tool nobody uses goes stale unnoticed. An adapter never carries strategy, a claim, or a status: it names the load order and stops. The single exception is `portable-control-layer.md`, which carries content because a chat model cannot follow a pointer, and is therefore dated and regenerated whenever a ledger changes.

Templates and the tool table: `portability.md`.

### context/, the source of truth

One file. Every source artifact distilled into numbered sections that an agent can read once and execute from.

Frontmatter contract:

```yaml
---
title: <Project> Go-To-Market Master Context
project: <Project>
type: gtm_context_file
purpose: Single source of truth for any AI agent executing <Project> go-to-market work.
version: 1.0
last_updated: YYYY-MM-DD
status_notes: <the live caveats, what is undecided, what is not yet true>
canonical_vocabulary: <comma-separated canonical terms>
---
```

`status_notes` is the most useful field in the brain. It is where an agent learns, in one line, what it is not allowed to assume. Keep it current.

Section order, adapt names but keep the sequence, because it moves from governance to strategy to execution:

0. Agent operating instructions. What this file is, how to use it, the hard guardrails.
1. House writing rules.
2. Canonical vocabulary.
3. Status ledger for capabilities.
4. Claim hygiene ledger.
5. What the product or service actually is.
6. Feature or capability matrix, what leads and what is table stakes.
7. Competitive market analysis.
8. Ideal customer profile and buying committee.
9. Strategic verdicts already decided.
10. Value proposition, audience one.
11. Value proposition, audience two.
12. Positioning statement.
13. Customer journey funnels.
14. Campaign and asset plan.
15. Quick-reference execution cheatsheet.

Section 0 is written in the second person to the agent. Section 15 is a flat list of the twenty facts an operator looks up most, so common questions never require a full read.

Budget 300 to 500 lines. Over 500 means transcription, not distillation.

### rules/, the control layer

Four files, each short enough to load on every task. They repeat material from the master context on purpose. The master is the reference brain, the rules are the enforcement layer, and enforcement has to be cheap to load or it does not happen.

- `glossary.md`. A table of canonical terms and the rule for each, including the terms that are banned because a partner or platform owns them. Ends with the distinction that must never blur, if the business has one.
- `feature-status.md`. Grouped by capability area, one line per capability, status flag in caps. Opens with the legend and the instruction to update this file before any copy follows. Name it `capability-status.md` or `service-status.md` where "feature" does not fit.
- `do-not-say.md`. Three parts: hard bans as a two-column table, channel-specific bans, and claims that need scoping with the safe form spelled out. Then any historical or reputational material that must be handled rather than repeated.
- `writing-rules.md`. Mechanics, tone, medium-specific rules such as writing for the ear, claim discipline, channel discipline, the approved signature lines, and formatting.

Budget eighty lines each. A control file nobody finishes reading controls nothing.

### reference/, loaded on demand

One file per source artifact, plus synthesized files. Each opens with one line naming what to load it for and which source it distills, so an agent can skip it accurately.

Typical set:

| File | Answers |
|---|---|
| `positioning.md` | What category are we in and what do we lead on |
| `positioning-verdict.md` | The strategic fork that was settled, and the reasoning |
| `icp-personas.md` | Who we sell to, who blocks, what wins each level |
| `competitive-analysis.md` | Market shape, scoring vectors, the wedge |
| `competitor-battlecards.md` | Per rival: strength, gap, how we win |
| `feature-matrix.md` | What leads messaging, what is table stakes |
| `customer-journey.md` | Stage by stage mindset, asset, KPI, owner |
| `value-proposition-<audience>.md` | Pillars and approved reasons to believe, per audience |
| `objection-handling.md` | The recurring pushbacks and the honest answers |
| `marketing-campaigns.md` | The campaign structure and asset backlog |
| `<channel>-engine.md` | The strategy and method behind the primary channel |

The channel engine does the most work of any synthesized file. Whatever the GTM runs on, that channel gets a file holding its thesis, its archetypes, and its plan, write, and edit methodology, and every template for that channel points back to it.

Budget sixty lines each.

### templates/, examples/, prompts/, the execution layer

Templates are shape, not content: the sections, the order, the fields to fill, and the guardrails at the bottom. Every template ends with a guardrail line pointing at the rules files, because a template is where a hurried operator stops reading.

Examples are approved output, matched one to one with the major asset types, and ideally annotated with a short "why this works" so the voice is teachable rather than only imitable.

Prompts are filled, runnable strings for recurring jobs, each naming the files to load and ending with the QA instruction.

`pages/` holds finished long-form assets. The rule is update rather than rewrite, because a shipped page carries approvals a fresh draft does not.

### ops/ and snapshots/, the state layer

This layer is why the brain compounds. Without it you have a style guide.

- `copy-bank.md`. Approved language grouped by use: reframes, hooks, one-line positioning, per-audience headlines, proof points, calls to action. Every line here has passed the claim ledger, so it is safe to reuse verbatim.
- `decisions.md`. Newest first. Each entry: date, title, DECIDED or OPEN, the verdict, the rationale, and an explicit note of what did not change. Ends with an "open, owned elsewhere" section for questions deliberately not answered here.
- `signal-log.md`. Raw market input with source, verbatim, type, and disposition. See `compounding.md`.
- `asset-index.md`. Where the source deliverables, product surfaces, channels, and related engagements live.
- `QA-checklist.md`. Tickable, grouped by writing, channel, claims, naming, audience and stage, medium-specific, and voice.
- `review-cadence.md`. Who reviews which ledger, how often, and the staleness threshold for each.

`snapshots/` holds dated captures of external state: funnel numbers, channel performance, win and loss reasons, competitive moves, product status. Each snapshot ends with a "what this changes" section that either routes to a ledger update or explicitly records that nothing changed. A snapshot that changes nothing is still worth keeping, because it is the evidence that the strategy is holding.

### sources/

Keep the originals. `sources/raw/` for the dashboards and decks as delivered, `sources/extracted/` for the machine-readable dumps. When a ledger entry is questioned six months later, the argument ends by opening the source. If the material is confidential, keep the folder out of the repo and record its location in `ops/asset-index.md` instead.

## Load policy

What an agent should read, and when.

| Task | Load |
|---|---|
| Any session | Router only |
| Any customer-facing writing | Router, all four `rules/`, the relevant `reference/` file |
| Strategy question | Master context, `ops/decisions.md` |
| Channel content | Add the channel engine, the template, the matching example |
| Competitive or sales work | Add battlecards and objection handling |
| Ingesting a signal or snapshot | `ops/signal-log.md`, `ops/decisions.md`, and the ledger the signal points at |
| Pre-ship | `ops/QA-checklist.md` |

The one rule that matters most: keep the always-loaded layer small and authoritative, and pull everything else in on demand. A brain that must be read in full to be used will not be used.
