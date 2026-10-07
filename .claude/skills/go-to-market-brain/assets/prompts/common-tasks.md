# Prompt library, common GTM tasks

Reusable prompts for recurring jobs. Each assumes the agent has already loaded the entry file and the master context. Copy, fill the brackets, run.

State the channels this GTM excludes here, as an absence: "There is no {{excluded channel}} in this GTM, so there are no {{excluded channel}} prompts." A rule expressed as a missing section is a rule an agent notices.

## Plan a {{primary channel asset}}
"Plan a {{asset}} for the [{{audience 1}} / {{audience 2}}] audience, [archetype] archetype, targeting [{{query or topic}}]. Follow Phase 1 of `templates/{{template}}.md`: give the one-sentence takeaway, the working title, the beats, and the single call to action. Do not write it yet."

## Write it
"Write the full {{asset}} from this plan [paste plan], following `templates/{{template}}.md` and the voice in `examples/{{example}}.md`. {{Medium-specific instruction.}} Mark any unshipped capability coming soon. Then QA against `ops/QA-checklist.md`."

## Edit an existing draft
"Edit this [paste draft] using the edit discipline in `reference/{{channel-engine}}.md`: tighten the opening, cut warm-up, enforce one idea, check every claim against `rules/do-not-say.md` and every capability against `rules/feature-status.md`, and confirm a single call to action. Return the edit plus a short list of what changed and why."

## Repurpose one asset into many
"Repurpose this [asset] into the full set in `templates/repurposing.md`. Each output stands alone, vary the opening, one call to action each. QA before returning."

## Landing page
"Draft a long-form landing page for the [{{audience}}] audience following `templates/landing-page.md`. Lead the hero with {{the primary hook}}. Use that audience's pillars only. Mark unshipped capabilities coming soon. Match `examples/{{example}}.md`. QA before returning."

## Objection response
"Draft a response to the objection '[objection]' for the [{{audience}}], grounded in `reference/objection-handling.md`. Keep it honest about anything unshipped."

## Competitive positioning
"Write positioning against [competitor] for a [prospect type], using `reference/competitor-battlecards.md`. Lead with the vectors we own. No overclaiming, and check every superlative against `rules/do-not-say.md`."

## Log a signal
"Log this in `ops/signal-log.md`: [paste the call note, review, objection, or competitor move]. Keep the verbatim. Classify the type, assign a disposition using the thresholds in that file, and if it is a PATCH or AMEND, route it and tell me exactly which files change."

## Take a snapshot
"Build this period's snapshot in `snapshots/` from [paste or point at the data]. Fill every section, diff section 6 against `rules/feature-status.md`, and finish with what this changes, including 'no ledger change this period' if that is the honest answer."

## Audit the brain
"Run `scripts/audit_brain.py` on this repo, then produce one real asset using only the brain and QA it. Report anything the brain could not supply."
