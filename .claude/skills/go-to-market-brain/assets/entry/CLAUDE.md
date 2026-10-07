# {{PROJECT}} GTM, agent entry point

This repository is the {{PROJECT}} go-to-market. You are an AI agent working inside it. Read this file, then follow its pointers. Do not improvise strategy that is already decided here.

## Read before any customer-facing output
1. `context/{{PROJECT}}_GTM_Master_Context.md`, the full strategy, ICP, positioning, messaging, funnels, and campaigns. Source of truth.
2. `rules/writing-rules.md`, how every word must be written{{EAR_NOTE}}.
3. `rules/do-not-say.md`, the claims you must never make and their safe replacements.
4. `rules/feature-status.md`, what is shipped versus in build. Check before describing any capability.

## This GTM is {{GTM_SHAPE}}
{{CHANNEL_PARAGRAPH}}

The channels are: {{CHANNELS_IN}}. {{CHANNELS_OUT_SENTENCE}}

For anything {{PRIMARY_CHANNEL}}, load `reference/{{CHANNEL_ENGINE_FILE}}` first. It holds the strategy, the archetypes, and the planning, writing, and editing methodology.

## Pick the audience first
{{AUDIENCE_COUNT}} audiences with separate value propositions. Never blend them.
{{AUDIENCE_LIST}}

## Non-negotiables (short version, full detail in rules/)
{{NON_NEGOTIABLES}}

## Before you ship
Run `ops/QA-checklist.md` against your draft.

## When something changes
A new signal from a lead, customer, or competitor goes in `ops/signal-log.md` first. If it changes a rule, follow the amendment procedure: update the ledger in `rules/`, then the master context, then `ops/decisions.md`, then the copy. Never the other way around.
