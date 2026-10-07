# Prompt library, common GTM tasks

Filled, runnable prompts for recurring jobs. Each assumes the agent has loaded `CLAUDE.md` or `AGENTS.md`. Copy one, fill the brackets, run. Every prompt ends with the QA instruction, because that is where a hurried run skips.

There are no prompts for paid ads, cold email sequences, automated outreach, follow-ups to guests who did not reply, or advertised invitations, because this go-to-market excludes them. A rule expressed as an absence is a rule an agent notices. If asked for one, refuse, name the rule in `rules/writing-rules.md`, and offer the nearest in-scope job below.

## Client-facing production

**Founder post.** "Write a founder LinkedIn post, [teardown / category / arithmetic / wedge / trend / scope] archetype, client audience, awareness stage. Follow `templates/linkedin-post.md` and `reference/channel-engine.md`, match the voice of `examples/linkedin-category-post.md`. Use only figures from `rules/evidence-ledger.md`, attributed. Assume guests read it. Then run `ops/QA-checklist.md` and report each block."

**Composition teardown.** "Write a composition teardown of [public event], from these public sources only: [paste speaker list, programme, attendee announcements]. Who was there against who the host presumably wanted, and what that costs a host. No speculation about named individuals and no claim about the host's results. Follow `templates/linkedin-post.md`. QA before returning."

**Prospect approach.** "Draft one researched approach to [title] at [company]. Research notes: [paste]. Follow `templates/prospect-approach.md` and match `examples/prospect-approach.md`. Under 120 words, the reason in the first line, the coverage read as the only offer, no claim of any kind. If the research does not support a specific first line, tell me instead of writing a generic one. QA before returning."

**Discovery call prep.** "Prepare a discovery call guide for [company], [attendee titles]. Use `templates/discovery-call.md`. Score the five ICP characteristics from what is public, pick the positioning statement from `reference/positioning.md`, and list the three objections most likely from `reference/objection-handling.md` with their answers. Flag any disqualifier."

**Coverage read.** "Build a coverage read from this named account list [paste or path] for [segment], title [title], using `templates/coverage-read.md`. Counts only, never named individuals in the output. Name coverage or access plainly. QA before returning. Do not store any personal data in this repository."

**Objection reply.** "Draft a written reply to this objection from a [role]: '[objection]'. Ground it in `reference/objection-handling.md` and `reference/competitor-battlecards.md`, match `examples/objection-response.md`. Honest about anything not yet decided, and check `ops/decisions.md` for the current state of D4, D10 and D11. QA before returning."

**Competitive positioning.** "Write positioning against [competitor or alternative] for a [role] at a [segment] vendor, using `reference/competitor-battlecards.md`. Lead with their real strength, then the gap, then how we win. Never claim a weakness that is not marked structural or sourced. Check every superlative against `rules/do-not-say.md`."

**Landing page edit.** "Edit block [n] of `pages/landing-page.md` to [goal]. Keep the anatomy in `reference/landing-page-structure.md`, one call to action, no format or geography. Apply only safe forms the founder has approved under D16. Return the edit, a list of what changed, and the QA result."

## Guest-facing production

**Guest invitation.** "Draft a guest invitation for [role] at [organisation type] on this question: [question, verified live]. Use `templates/guest-invitation.md` and match `examples/guest-invitation.md`. Guest vocabulary only, per `rules/two-vocabularies.md`. Question first, who else by role, exact time cost, host named, 'No attendee list goes out, before or after.' No frozen D11 lines. Put the copy between the guest-copy markers and run `scripts/lint_claims.py`, then the QA checklist."

**Note afterwards.** "Draft the note afterwards for [event]. Summary offer and one nomination ask only, per `templates/guest-invitation.md`, until D11 lands. Guest vocabulary only."

## Partnership

**Partnership brief.** "Draft a partnership brief for [partner] using `templates/partnership-brief.md`. State list ownership explicitly. No claim of an existing network. Member-facing lines in guest vocabulary. QA before returning."

## Operating the brain

**Log a signal.** "Log this in `ops/signal-log.md`: [paste call note, objection, review, competitor move, research result]. Keep the verbatim. Classify the type, assign a disposition using the thresholds in that file, increment any matching WATCH, and if it is a PATCH or AMEND tell me exactly which files change and in what order."

**Amend a ledger.** "This changed: [fact]. Run the amendment procedure: update the right `rules/` file and its `last_reviewed`, the master context section with a version bump, a dated entry in `ops/decisions.md` including what it does not change and the downstream list, then grep the repo for the old phrasing, update `ops/copy-bank.md`, and regenerate `adapters/portable-control-layer.md`."

**Decision brief.** "Prepare a decision brief for D[n] using `templates/decision-brief.md`. Pull every dependency from `rules/service-status.md`, `ops/decisions.md` and `COMMAND-CENTER.md`. Recommend one option, and say where counsel must confirm."

**Weekly triage.** "Run this week's triage on `ops/signal-log.md`: disposition every new entry, increment and expire WATCH items per the thresholds, execute the PATCHes, list any AMEND for the founder. Then update the This week section of `COMMAND-CENTER.md`."

**Snapshot.** "Build this period's snapshot in `snapshots/` from [data]. Fill every section of the format in `snapshots/2026-10-07-baseline.md`, diff section 6 against `rules/service-status.md`, and finish with what this changes, including 'no ledger change this period' if that is the honest answer. Update `last_reviewed` on each ledger examined."

**Audit.** "Run `python3 scripts/audit_brain.py .` and `python3 scripts/lint_claims.py`, fix every error, then produce one real asset using only the brain and QA it. Report anything the brain could not supply."

## Tools without file access

**Deck in Gamma.** "Paste the content using Paste in text, not Generate. Do not let the tool add, split, merge or rewrite slides. Every `{TBD}` must survive. If one is replaced with a figure, the figure is invented and comes out." Paste `adapters/portable-control-layer.md` into the tool's instructions first.

**Claude Design or any design tool.** Attach `sources/raw/warmchannelgtmbuild/brand/DESIGN.md` and paste `sources/raw/warmchannelgtmbuild/brand/CLAUDE-DESIGN-PROMPT.md`. Folio replaces Roster and is never merged with it. Copy on the page is not rewritten by the design tool.
