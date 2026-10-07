# Operating a built brain

OPERATE mode. The brain exists and the job is to produce, check, or ship something with it. This is the mode most sessions are in, so it should be fast and mechanical.

## The session contract

Six steps, in order.

1. **Load the router.** `CLAUDE.md` or `AGENTS.md`. It carries the read order and the non-negotiables. Never skip it on the grounds that the task is small. Small tasks are where claims leak.
2. **Pick the audience.** If the business has more than one, choose before writing a word, and never blend them in a single asset. Blending is the most common failure and the hardest to spot in review, because each half reads fine.
3. **Load the control layer.** All four `rules/` files for anything customer-facing. They are short by design.
4. **Load what the task needs.** The load policy table in `blueprint.md` maps task to files. For channel content that means the channel engine, the template, and the matching example.
5. **Produce.** Fill the template. Use the copy bank verbatim where a line exists, because those lines have already passed the claim ledger. Never invent a proof point, a price, or a status.
6. **Run the QA checklist.** `ops/QA-checklist.md`, item by item, before returning anything. Then state which checks were run.

## While producing

**Copy bank first.** If an approved line covers the point, use it. Rewriting an approved line is how a checked claim becomes an unchecked one.

**Status flags travel with capabilities.** Any mention of an unshipped capability carries its marker in line, in the same sentence, not in a footnote and not once at the top of the page.

**Superlatives get checked, every time.** Every "only," "first," "best," "never," and "no other" goes through `rules/do-not-say.md`. Most will need the narrowed form.

**Conditional claims name the condition.** If a claim is true in one mode, tier, or configuration and false in another, the condition is part of the sentence.

**Refuse out-of-scope channels.** If the GTM excludes a channel, say so plainly and offer the in-scope alternative. Do not quietly produce it because the request was direct.

**Flag gaps rather than filling them.** If the task needs a fact the brain does not hold, say so and ask. Inventing a plausible fact is the single worst failure mode available here, because the output looks correct.

## Returning work

State the audience, the funnel stage, and the template used. List every capability mentioned with its status flag. Name any claim that was narrowed and why. Note anything the brain could not supply.

If the work produced a reusable line, propose it for `ops/copy-bank.md`. If it surfaced a gap, log it as a signal. Production work is a signal source, and treating it as one is free.

## After shipping

Two closing moves, both cheap and both routinely skipped:

- **File the asset.** Long-form assets go in `pages/`. Live surfaces get a line in `ops/asset-index.md` with their location, so the next amendment can find everything that carries the old claim.
- **Log what the work taught you.** A gap, a line that landed, an objection that came up in review. Into `ops/signal-log.md`. This is the loop closing on itself, and it is why the brain gets sharper through use rather than through maintenance.
