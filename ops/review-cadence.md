# Review cadence

Who reviews what, how often, and when a file is stale. Proposed 2026-10-07 for a solo, pre-launch founder. The founder confirms or changes it in `ops/gap-interview.md`. Until confirmed, these are the operating defaults.

## Rituals

| Ritual | Frequency | Owner | Time | Work |
|---|---|---|---|---|
| Signal triage | Weekly, Monday | Founder, an agent prepares | 20 minutes | Disposition every new signal, increment and expire WATCH items, execute PATCHes, list AMENDs. Update the This week block in `COMMAND-CENTER.md` |
| Decision review | Weekly, Monday, straight after triage | Founder | 10 minutes | Walk the open queue in `ops/decisions.md`. Settle at least one, or record why not |
| Ledger sweep | Monthly, first Monday | Founder, an agent prepares | 45 minutes | Read every `rules/` file against reality, update `last_reviewed`, expire stale WATCH items, check the portable control layer's date |
| Snapshot | Monthly while pre-launch, quarterly once engagements run | Founder, an agent drafts | 1 hour | A dated file in `snapshots/`, ending in what it changed |
| Master context version | Quarterly, or on any AMEND | Founder | 30 minutes | Bump version, refresh `status_notes`, verify each section against the ledgers |
| Brain audit | Monthly, with the ledger sweep, and in CI on every push | Automated, then founder | 15 minutes | `python3 scripts/audit_brain.py .` and `python3 scripts/lint_claims.py`, then one live asset produced from the brain and QA'd |
| Adapter check | Quarterly | Founder | 15 minutes | In each tool in use, ask for something the brain forbids and something it allows. It should refuse the first, naming the rule, and produce the second |

## Ledger ownership and staleness

| File | Owner | Stale after | Why that threshold |
|---|---|---|---|
| `rules/service-status.md` | Founder | 30 days | Goes stale fastest and does the most damage: it stands between a roadmap and a promise |
| `rules/do-not-say.md` | Founder, counsel on legal lines | 60 days | Every live surface and every call depends on it |
| `rules/evidence-ledger.md` | Founder | 90 days | Benchmarks date. A 2026 figure quoted in 2028 is a liability |
| `rules/two-vocabularies.md` | Founder | 90 days | Changes only when a surface or a segment changes |
| `rules/glossary.md` | Founder | 90 days | Changes with D9, D12 and any rename |
| `rules/writing-rules.md` | Founder | 180 days | Slow-moving |
| `context/` master context | Founder | 60 days | Must never trail a ledger |
| `adapters/portable-control-layer.md` | Founder | Regenerated on every amendment. Audit fails it after 90 days | It carries content, so it decays |
| `ops/decisions.md` open queue | Founder | Reviewed weekly | An unsettled decision is a blocked funnel |

`scripts/audit_brain.py` flags any `rules/` or `context/` file older than 90 days by default. Run it with `--max-age-days 30` in the monthly sweep to catch the status ledger.

## Authority

- **A PATCH** can be made by anyone producing work, human or agent, and is logged.
- **An AMEND** to any `rules/` file, the master context, the ICP, positioning or the channel mix requires the founder and a dated entry in `ops/decisions.md`.
- **Any legal or consent wording** requires counsel's written position first.
- **An agent never marks a decision DECIDED.** It prepares the brief.

## Triggers outside the calendar

Act the same day, without waiting for triage, on: a competitor shipping or repositioning on a claim we scope; any challenge to a claim from a prospect, partner or counsel; a guest complaining about being sold to, listed or chased; anything going live on a new surface; any decision moving from OPEN to DECIDED.
