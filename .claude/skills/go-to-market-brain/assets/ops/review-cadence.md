# Review cadence

Who reviews what, how often, and when a file is considered stale. Agreed {{DATE}}.

## Rituals

| Ritual | Frequency | Owner | Work |
|---|---|---|---|
| Signal triage | {{Weekly, day}} | {{owner}} | Disposition every new signal, increment WATCH counters, execute PATCHes |
| Ledger sweep | {{Monthly}} | {{owner}} | Read all four `rules/` files against reality, update `last_reviewed`, expire stale WATCH items |
| Snapshot | {{Monthly or quarterly}} | {{owner}} | The full capture in `snapshots/`, ending in what it changed |
| Master context version | {{Quarterly}}, or on any AMEND | {{owner}} | Bump version, refresh `status_notes`, verify sections against the ledgers |
| Brain audit | {{Quarterly}} | {{owner}} | Run the audit script, then produce one live asset using only the brain |

## Ledger ownership and staleness

| File | Owner | Stale after |
|---|---|---|
| `rules/feature-status.md` | {{product}} | {{30}} days |
| `rules/do-not-say.md` | {{marketing + legal}} | {{90}} days |
| `rules/glossary.md` | {{product}} | {{90}} days |
| `rules/writing-rules.md` | {{marketing}} | {{180}} days |
| `context/` master context | {{GTM owner}} | {{90}} days |

Staleness is not a formality. `feature-status.md` goes stale fastest and is the file whose staleness does the most damage, because it is what stands between a roadmap and a promise.

## Authority
- A PATCH can be made by {{anyone producing work}}.
- An AMEND to any `rules/` file requires {{named approver}}.
- A change to positioning, ICP, or the channel mix requires {{named approver}} and a dated entry in `ops/decisions.md`.
