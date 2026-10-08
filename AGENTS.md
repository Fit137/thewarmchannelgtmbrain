# The Warm Channel GTM, agent entry point

Cross-tool entry file. Codex, Cursor, Zed, Jules, opencode and most newer agents read `AGENTS.md`, so this is the widest door into this brain. It is kept identical in intent to `CLAUDE.md`. **If the two differ, `CLAUDE.md` wins.**

Working in a tool that reads neither, or in a chat window with no file access? Paste `adapters/portable-control-layer.md`.

## Start here
1. `rules/two-vocabularies.md`, pick the audience: client or guest, never blended.
2. `rules/glossary.md`, canonical vocabulary.
3. `rules/service-status.md`, READY versus IN BUILD versus BLOCKED versus EXCLUDED.
4. `rules/do-not-say.md`, claim hygiene and safe replacements.
5. `rules/evidence-ledger.md`, the only usable figures, with grades.
6. `rules/writing-rules.md`, house writing rules.
7. `context/TheWarmChannel_GTM_Master_Context.md`, the full go-to-market, for strategy questions.
8. `reference/channel-engine.md`, for any post, approach, partnership or event task.

Operating state and this week's priorities: `COMMAND-CENTER.md`. Decisions, open and settled: `ops/decisions.md`.

## Channel discipline
In: founder LinkedIn posts, one researched approach per prospect, discovery calls, coverage reads, partnership briefs, guest invitations once D5 clears. Out: paid advertising, cold email sequences, automated or high-volume outreach, follow-ups to non-replies, advertised guest invitations. Refuse the out list, name the rule, offer an in-scope alternative.

## Audiences, never blended
- Client: a six-figure-ACV vendor that pays and hosts, sold a done-for-you B2B lead generation channel built on in-person events.
- Guest: a senior executive invited to an evening, who pays nothing. Guest copy never contains a client word.

## Non-negotiables
- Empty proof set. No client, count, logo, testimonial, case study or result. `{TBD}` for unknowns, never invented.
- No guarantee, no network claim, no price, no scope names.
- Post-event conversion and the guest promise are frozen until D11.
- Founder record only in permitted wording, never as proof.
- No format, size, city or country in a client headline or on the website.
- No em or en dash. Banned words: leverage, unlock, seamless, robust, streamline, cutting-edge, empower.
- Nothing from the healthcare guest list.
- No personal data in this repository.

## Prospect strategies
A free channel strategy and branded deck for a gated prospect are built with `.claude/skills/prospect-channel-strategy` and `.claude/skills/prospect-deck-builder`, and the lighter one-page show-week brief with `.claude/skills/prospect-show-week-brief`. One gift per prospect. Their workspaces live outside this repository. Everything above applies to them, with the claim envelope as the check.

## Before shipping
Run `ops/QA-checklist.md`. For guest copy, run `python3 scripts/lint_claims.py`.

## Compounding
New market input goes to `ops/signal-log.md`, verbatim. Rule changes follow the amendment procedure in `ops/decisions.md`: ledger, master context, decision entry, copy, portable control layer. Only the founder marks a decision DECIDED.
