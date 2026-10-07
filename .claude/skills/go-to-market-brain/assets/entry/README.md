# {{PROJECT}} GTM

The go-to-market for {{PROJECT}}, structured so any AI agent or operator can absorb the full strategy and execute on it precisely. This repo is content and context, not application code.

## What {{PROJECT}} is
{{WHAT_IT_IS}}

## How this GTM works
{{GTM_SHAPE_PARAGRAPH}}

## How this repo is organized

| Folder | What it holds | When the agent uses it |
|---|---|---|
| root entry files | `CLAUDE.md`, `AGENTS.md`, `llms.txt` | Loaded automatically every session. Routers, not content. |
| `context/` | The master GTM context file | Source of truth. Load before any customer-facing work. |
| `rules/` | Writing rules, do-not-say, feature status, glossary | The control layer. Governs what to say and how. |
| `reference/` | Channel engine, ICP and personas, objection handling, competitor battlecards, positioning | Pulled in for content, targeting, and competitive tasks. |
| `templates/` | Skeletons for each channel in the mix | Fill a known structure instead of inventing one. |
| `examples/` | Gold-standard approved outputs | Few-shot voice reference. Match these. |
| `pages/` | Finished long-form copy | Shipped assets, not skeletons. Update rather than rewrite. |
| `ops/` | Copy bank, decision log, signal log, asset index, QA checklist, review cadence | Living state and pre-ship checks. |
| `snapshots/` | Dated captures of funnel, channel, and competitive state | Evidence of what changed and what did not. |
| `prompts/` | Reusable task prompts | Fast starts for recurring jobs. |

## What you can do with it
- **Produce on-brand copy for any surface**, inheriting the right audience, claim hygiene, and voice automatically.
- **Stop overclaiming.** `rules/do-not-say.md` and `rules/feature-status.md` prevent a certification not yet earned, a capability not yet shipped, or a claim stated too broadly from reaching a customer. `ops/QA-checklist.md` is the gate every draft passes.
- **Keep one source of truth for strategy**, so it does not live in one person's head or scattered files.
- **Onboard fast.** A new hire, freelancer, or agent absorbs the whole go-to-market in one read.
- **Compound.** Every lead conversation, customer signal, and periodic snapshot enters `ops/signal-log.md`, gets triaged, and either sharpens a ledger or is recorded as changing nothing.

## The one rule that matters most
Keep the always-loaded layer small and authoritative. Everything else is pulled in on demand. The master context is the reference brain, not something to load on every task.

## Maintenance
When status changes, update `rules/feature-status.md` and the relevant section in `context/` first, then let downstream copy follow. Never the other way around. New market input goes to `ops/signal-log.md` and is triaged on the cadence in `ops/review-cadence.md`.
