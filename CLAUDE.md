# The Warm Channel GTM, agent entry point

This repository is The Warm Channel go-to-market brain and command center. You are an AI agent working inside it. Read this file, then follow its pointers. Do not improvise strategy that is already decided here, and never present an open decision as settled.

## Read before any client-facing or guest-facing output
1. `rules/two-vocabularies.md`, pick the audience first. Client or guest, never blended.
2. `rules/glossary.md`, the canonical name for everything.
3. `rules/service-status.md`, what is READY, IN BUILD, BLOCKED or EXCLUDED. Check before describing any capability.
4. `rules/do-not-say.md`, forbidden claims and their safe replacements.
5. `rules/evidence-ledger.md`, the only numbers that exist, with grades.
6. `rules/writing-rules.md`, how every word is written.

For strategy, load `context/TheWarmChannel_GTM_Master_Context.md` and `ops/decisions.md`. For operating state, `COMMAND-CENTER.md`.

## This GTM is founder-led and low-volume by design
The Warm Channel argues that volume channels are decaying, so it acquires clients and guests by small numbers of researched approaches, founder posts, a demonstration event and partnerships. Channels in: founder LinkedIn posts, one researched approach per prospect, discovery calls, coverage reads, partnerships, guest invitations once D5 clears. **Channels out, refuse and redirect: paid advertising, cold email sequences, automated or high-volume outreach, follow-ups to anyone who did not reply, advertised guest invitations.** For any channel task load `reference/channel-engine.md` first.

## Two audiences, never blended
- **Client**: a six-figure-ACV vendor that pays, hosts and wants sales-qualified leads. Client words: lead generation channel, named accounts, pipeline.
- **Guest**: a senior executive invited to an evening, who pays nothing and buys nothing. Guest words: the question, peers, the evening, the host. No client word ever reaches a guest.

## Non-negotiables
- The proof set is empty. No client, count, logo, testimonial, case study or result. Unknown numbers are `{TBD}`. Never invent one, including a plausible sourcing line.
- No guarantee of leads, meetings, pipeline or attendance until D4 and D10.
- No claim of an existing network or guest list.
- No price, tier or scope name until D2 and D10.
- Post-event conversion and the guest promise conflict. Both are frozen until D11.
- The founder's record is a credential, never proof, and only in `reference/founder-credentials.md` wording.
- No format, event size, city or country in a client headline or on the website.
- No em dash, no en dash. Banned words: leverage, unlock, seamless, robust, streamline, cutting-edge, empower.
- Never use the healthcare guest list or that business's references.
- **No personal data about any guest or prospect in this repository.** IDs only.

## Before you ship
Run `ops/QA-checklist.md` against the draft and say which blocks you ran. For guest copy, also run `python3 scripts/lint_claims.py`.

## When something changes
New input from a prospect, client, guest, partner or competitor goes in `ops/signal-log.md` first, verbatim. If it changes a rule, follow the amendment procedure at the top of `ops/decisions.md`: ledger in `rules/`, then the master context, then the decision entry, then copy, then `adapters/portable-control-layer.md`. Never the other way around. Only the founder marks a decision DECIDED.

## Skills
Three skills live in `.claude/skills/`.
- `go-to-market-brain`, vendored, MIT. UPDATE mode for signals and snapshots, OPERATE mode for producing assets, and its audit script, as adapted in `scripts/audit_brain.py`.
- `prospect-channel-strategy`. A free in-person channel strategy for one gated, highly qualified prospect, from public information, in a workspace outside this repository. Decided 2026-10-08.
- `prospect-deck-builder`. Packages that strategy as an interactive deck in the prospect's own branding, checks it and sends it privately. Prospect data never enters this repository: the pipeline gets an ID.
