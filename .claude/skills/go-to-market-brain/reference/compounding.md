# The compounding loop

UPDATE mode. This is what makes a brain a brain rather than a folder of documents. Every lead conversation, customer signal, competitor move, product change, and periodic snapshot enters here, gets triaged, and either changes a ledger or is recorded as having changed nothing. Both outcomes are valuable. The second one is the evidence that the strategy is holding.

The loop has one governing principle: **nothing enters the copy layer without passing through a ledger, and nothing enters a ledger without a dated decision.**

## The four-step loop

```
CAPTURE  ->  TRIAGE  ->  ROUTE  ->  PROPAGATE
   |                                     |
   +--------- snapshots, periodic -------+
```

### 1. Capture

Everything goes into `ops/signal-log.md`, raw, before any judgment. Cheap capture is the whole point. A signal that gets debated before it gets written down does not get written down.

One entry, five fields:

```markdown
### YYYY-MM-DD | <type> | <source>
**Verbatim:** "<what was actually said or observed, in their words>"
**Context:** <who, which stage, which segment, which channel>
**Disposition:** NOISE | WATCH (n/N) | PATCH | AMEND
**Routed to:** <file, or "none">
```

Keep the verbatim. Paraphrasing a customer into house vocabulary destroys the most valuable thing a signal carries, which is the language a real buyer used before we taught them ours. Copy-bank lines derived from real customer phrasing outperform lines written internally, and you cannot recover that phrasing later.

**Signal types:**

| Type | What it is | Where it usually lands |
|---|---|---|
| OBJECTION | A prospect pushed back | `reference/objection-handling.md` |
| LANGUAGE | A buyer described the problem in their own words | `ops/copy-bank.md`, value propositions |
| PROOF | A permissioned metric, quote, result, or logo | `ops/copy-bank.md` proof points, `rules/do-not-say.md` |
| STATUS | A capability shipped, a certification landed, pricing set | `rules/feature-status.md` |
| COMPETITIVE | A rival launched, repositioned, was acquired, or shut down | `reference/competitor-battlecards.md`, claim scoping |
| SEGMENT | A buyer type keeps appearing, or a named ICP is not converting | `reference/icp-personas.md`, master context |
| CHANNEL | A channel over or under performs against its role | `reference/marketing-campaigns.md`, channel engine |
| LOSS | A churn reason or a lost deal reason | Objection handling, ICP, positioning |
| RISK | A claim was challenged by a prospect, a reviewer, or legal | `rules/do-not-say.md`, immediately |

### 2. Triage

Every signal gets exactly one of four dispositions. Triage is a fixed weekly slot, not a reaction to whichever signal is loudest.

**NOISE.** One instance, no pattern, no consequence. Logged and closed. Logging noise is not waste: three noise entries that rhyme become a WATCH, and you only see the rhyme because they were written down.

**WATCH.** Plausible pattern, not yet corroborated. Record it as `WATCH (1/3)` and increment as instances arrive. When the threshold is met, it is promoted and triaged again.

Default thresholds, set with the user during the build:

| Signal class | Threshold to act |
|---|---|
| Opinion, preference, language, objection | 3 independent instances within 60 days |
| Verifiable fact: status, proof, competitive, risk | 1 verified instance, act immediately |
| Loss reason | 2 instances, or 1 if the deal was in the core ICP |
| Channel performance | A full measurement cycle, never a single week |

The distinction that matters: opinions need corroboration, facts need verification. A prospect disliking a headline is an opinion. A competitor shipping the capability that anchors your flagship claim is a fact, and it changes the claim ledger today.

**PATCH.** Changes copy, not strategy. Route it, make the edit, done. No decision entry, no version bump. Adding a heard objection to the objection file, banking a customer's phrasing, sharpening a headline: all patches.

**AMEND.** Changes a ledger, a strategic position, or a rule. This is the heavy path and it has a fixed procedure, below. Anything touching `rules/`, an ICP definition, positioning, or the channel mix is an AMEND.

**The default is NOISE.** A brain that amends on every input is a brain with no memory, and one that flip-flops on the last conversation is worse than a static document. The value of a settled decision is that it stays settled until real evidence moves it.

### 3. Route

PATCH and AMEND both route to a file. The routing rule is fixed and it is the one that keeps the brain coherent:

**Ledger first, master context second, copy third, assets last.** Never the reverse. Copy that leads the ledger is how a company ends up with a landing page making a claim its own rules forbid.

The AMEND procedure, all five steps or none:

1. **Update the ledger.** The `rules/` file that governs the thing that changed. Update its `last_reviewed` date.
2. **Update the master context.** The corresponding numbered section, in the same change. Bump `version` and `last_updated` in the frontmatter, and revise `status_notes` if the change alters what an agent may assume.
3. **Write the decision entry.** `ops/decisions.md`, newest at the top:

```markdown
## YYYY-MM Title of the decision (DECIDED)
<The verdict in one or two sentences.>
<The rationale, and the evidence that moved it: which signals, how many, over what period.>
**What this does not change:** <explicit list>
**Downstream:** <the assets that must now be revised, and who owns each>
```

   The "what this does not change" line is not filler. A positioning change that leaves the status ledger untouched must say so, or the next agent will assume the whole brain moved and rewrite things that were correct. It is also the line that stops a small amendment turning into an unplanned rewrite.

4. **Propagate to copy.** Update `ops/copy-bank.md`, and any template or reference file that repeated the old form. Grep the repo for the old phrasing. Stale approved copy is the most dangerous artifact in the brain, because it is pre-approved and therefore reused without a second look.
5. **List the affected shipped assets.** Everything in `pages/` and every live surface in `ops/asset-index.md` that carries the old claim. This becomes the downstream list in the decision entry, with an owner per item.

### 4. Propagate and close

Mark the signal entry `Routed to:` with the files changed. When the downstream list is complete, add the completion date to the decision entry. Open downstream items are the brain's debt, and the audit script reports them.

## Snapshots

A snapshot is a dated capture of external state. Signals arrive one at a time and are anecdotes. A snapshot is the periodic look at the whole board, and it catches the changes no single signal announces: a channel decaying, a segment converting better than the one the strategy prioritizes, a claim that quietly stopped being true.

Cadence: monthly for early-stage, quarterly once the motion is stable. Never skip one because "nothing changed." The record that nothing changed is the output.

File: `snapshots/YYYY-MM-DD-<label>.md`. Sections:

1. **Funnel.** Volume and conversion by stage, per audience, against the journey model.
2. **Channels.** Performance against each channel's assigned role. A channel can succeed on its own numbers and still fail its role.
3. **Segments.** Which ICP is actually converting, and which named segment is not showing up.
4. **Wins and losses.** Reasons, grouped. Loss reasons are the highest-yield input in the entire loop.
5. **Competitive.** What moved. Repositions, launches, pricing changes, funding, shutdowns.
6. **Product and delivery status.** Diffed against `rules/feature-status.md`. This diff alone justifies the ritual.
7. **What this changes.** The routing section. Either a list of AMENDs and PATCHes with owners, or the sentence "no ledger change this period," which is a real finding and should be written as one.

Every snapshot ends by updating `last_reviewed` on each ledger it examined, whether or not the ledger changed. That is what makes staleness visible.

## Review cadence

Record the agreed cadence in `ops/review-cadence.md` and give every ledger an owner.

| Ritual | Frequency | Work |
|---|---|---|
| Signal triage | Weekly, fixed slot | Disposition every new signal, increment WATCH counters, execute PATCHes |
| Ledger sweep | Monthly | Read all four `rules/` files against reality, update `last_reviewed`, clear stale WATCH items |
| Snapshot | Monthly or quarterly | The full capture above |
| Master context version | Quarterly, or on any AMEND | Bump version, refresh `status_notes`, verify sections against ledgers |
| Brain audit | Quarterly | `scripts/audit_brain.py`, plus produce one live asset using only the brain |

A WATCH item that has not incremented in two cycles expires to NOISE. Say so in the log. An indefinitely open watch list is a to-do list nobody reads.

## Why this compounds

Each mechanism converts a one-off event into a permanent asset, and each one raises the floor for every future piece of work.

- **Decisions stop being relitigated.** The dated verdict plus rationale means the same argument is had once. Time not spent reopening settled questions is the first return.
- **Language accumulates.** Every line that survives review is banked. Over a year the copy bank becomes a library of proven phrasing, and new work starts from proven language rather than a blank page.
- **Objections become pre-vetted answers.** The tenth time an objection is heard it has a tested response attached, and the response is in every agent's context.
- **Risk falls monotonically.** Every challenged claim tightens the claim ledger. The set of things that can go wrong shrinks, and it never grows back, because the counter-example stays in the file.
- **Onboarding collapses.** A new hire, freelancer, or agent absorbs the accumulated go-to-market in one read. The brain is the ramp.
- **Snapshots make drift visible.** Strategy fails slowly and quietly. A dated series of captures is the only way to see it while it is still cheap to correct.

The interest compounds because the ledgers are load-bearing. A patch to the copy bank improves the next asset. An amendment to a ledger improves every asset produced from that point on, by every operator and every agent, without anyone being told.
