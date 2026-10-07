# The Warm Channel GTM brain

The go-to-market for The Warm Channel, held as a governed context repository: the strategy distilled, the rules that stop anyone from overclaiming, the templates that make work fast, and the operating state that keeps all of it current. Any AI agent or person can load it and execute without re-deriving anything. This repository is content and context, not application code. From 2026-10-07 it is the source of truth and the command center for everything go-to-market.

## What The Warm Channel is

A done-for-you B2B lead generation channel built on in-person events. A client names the companies it wants as customers. The Warm Channel plans the channel, gets the right people from those companies into the room, and works the conversations afterwards. Any format, any size: a table of ten, a summit of two hundred, a programme around a show the client already exhibits at. No venue, no catering, no production. The client hosts.

It is pre-launch: one founder, no entity yet, no client, no delivered engagement, and an empty proof set, which this brain treats as a rule rather than an embarrassment.

## How this go-to-market works

**Two audiences who sit in the same room.** The client, a six-figure-ACV vendor whose buyers will not answer cold outreach, pays and hosts. The guest, a senior executive, is invited to an evening, pays nothing and buys nothing. One is being sold to the other, so they get two vocabularies that never mix. A guest who reads the client's language learns they were a lead, and returning guests are the only asset this business compounds.

**Founder-led and low-volume by design.** The business argues that volume channels are being flooded, so it acquires clients and guests the way it sells: researched individual approaches, founder posts, a demonstration event, and partnerships. No paid ads, no sequences, no automation.

**The argument is structural, not performance.** "Every lead has already met you in person" is true by the nature of the channel and needs no case study. Everything that would need one is `{TBD}` until it is real.

## How this repo is organised

| Folder | What it holds | When it is used |
|---|---|---|
| Root | `CLAUDE.md`, `AGENTS.md`, `llms.txt`, `COMMAND-CENTER.md` | Routers load every session. The command center is the weekly operating view |
| `context/` | The master GTM context | Strategy questions. The reference brain |
| `rules/` | Two vocabularies, glossary, service status, do-not-say, evidence ledger, writing rules | Before every piece of writing. The control layer |
| `reference/` | 23 files: positioning, ICP, committee, cohort, competition, battlecards, value propositions, journeys, objections, channel engine, playbook, pricing, lead magnets, credentials, compliance, guest economics, brand, landing page, research | Pulled in per task |
| `templates/` | Twelve skeletons for the channels actually in use | Producing an asset |
| `examples/` | Gold-standard drafts with "why this works" | Matching the voice |
| `pages/` | The landing page draft and the calculator | Shipped and to-be-shipped copy. Update, never rewrite |
| `prompts/` | Filled prompts for recurring jobs | Fast starts |
| `ops/` | Decisions, signals, copy bank, asset index, cadence, KPIs, risks, gap interview, trackers, QA | The living state |
| `snapshots/` | Dated captures and what each changed | Monthly |
| `adapters/` | The portable control layer and pointer blocks | Tools other than Claude Code |
| `sources/raw/` | Every source document, verbatim | Settling an argument about where a rule came from |
| `scripts/` | Audit and claims lint | Every push, via CI, and every monthly sweep |
| `.claude/skills/` | The `go-to-market-brain` skill, vendored, MIT | Running UPDATE and OPERATE modes |

## What you can do with it

- **Produce on-brand copy for any surface**, client or guest, inheriting the right audience, claim hygiene and voice.
- **Stop overclaiming.** The status ledger, the do-not-say file, the evidence ledger and the QA checklist stop a result, a guarantee, a network or an ungraded number from reaching anyone.
- **Run the business week to week** from `COMMAND-CENTER.md`: the road to first revenue, the decision queue, this week's plan, the boards.
- **Settle decisions once.** `ops/decisions.md` holds every settled call with its reasoning and every open one with a default and an owner.
- **Onboard anyone in one read**: a freelancer, a hire, an agency, an agent.
- **Compound.** Every call, reply, objection and competitor move enters `ops/signal-log.md`, gets triaged weekly, and either sharpens a ledger or is recorded as changing nothing.

## The most important open decision

**D11.** The 2026-09-22 positioning sells post-event conversion, conversations "handed over to your sellers with the context of what was actually said". The guest promise says nothing about a guest goes to anyone, including the host. Both cannot ship. The brain freezes both and recommends consented continuation. Read `ops/decisions.md` D11 first.

## The one rule that matters most

Keep the always-loaded layer small and authoritative. Routers and rules are short. Everything else is pulled in on demand. The master context is the reference brain, not something to load on every task.

## Maintenance

When anything changes, the ledger in `rules/` changes first, then the master context, then a dated entry in `ops/decisions.md`, then the copy, then `adapters/portable-control-layer.md`. Never the other way around. New market input goes to `ops/signal-log.md` and is triaged every Monday, per `ops/review-cadence.md`. Run the checks before pushing:

```bash
python3 scripts/audit_brain.py .
python3 scripts/lint_claims.py
```

CI runs both on every push. Only the founder marks a decision DECIDED. No personal data about guests or prospects is ever stored here.

## Provenance

Built on 2026-10-07 with the `go-to-market-brain` skill from `alielshenawy1/Ali-GTM-Brain-Skill`, from the `Fit137/warmchannelgtmbuild` repository at commit 1aac76e: the founder briefing of 2026-09-16, two `gtm-builder` runs of 2026-09-18, the research passes of 2026-09-18 and 2026-09-20, the repositioning of 2026-09-22, the conversion landing page, and the Folio design system.
