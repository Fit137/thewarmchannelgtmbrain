# Ledgers, deriving the control layer

Phase 4 of the build. The control layer is what stops an agent, or a hurried human, from shipping something the company cannot stand behind. It is derived from the master context, not invented, and it is written to be checked rather than admired.

Derive in this order. Each step depends on the one before it.

## 1. Glossary, the canonical vocabulary

Names come first, because every other rule refers to things by name.

Collect every term the business uses for its own entities, then decide the single canonical form of each. A term earns a row when getting it wrong would be visibly wrong to a customer.

Three kinds of rows:

- **Canonical terms.** The word, and what it means in this business. Include capitalization and whether it is one word.
- **Banned near-synonyms.** The word customers or the team reach for instead, and why it is wrong. Terms owned by a platform, a partner, or a competitor are the common case, and they are the ones that damage credibility fastest.
- **Distinctions that must never blur.** Two terms that sound interchangeable but where a claim is true of one and false of the other. This row usually explains a rule in the claim ledger, so cross-reference it.

Close the file with the single distinction that matters most, stated plainly. If the business has one pair of terms that a wrong claim hinges on, an agent should meet it at the end of the shortest file in the repo.

## 2. Status ledger

What may be promised. The most operationally important file in the brain, and the one that goes stale fastest.

Pick four flags and define them in a legend at the top:

- **SHIPPED**, live now, claimable in the present tense.
- **PARTIAL**, partially shipped. Say what works today, not what it will do.
- **IN BUILD**, committed and unshipped. Mark "coming soon" or omit.
- **ROADMAP**, vision. Never a launch claim.

Group by capability area, one line per capability, flag in caps at the end so the file can be scanned in seconds. Where a single capability is split across states, split the line, because "backups are shipped" and "instant backups are in build" are different promises.

Open the file with the maintenance rule in one sentence: update this file the moment status changes, before any copy follows. Add `last_reviewed: YYYY-MM-DD` so staleness is detectable.

Rename to fit the business. A services firm has a capability or service status ledger. An agency has a deliverable status ledger. The mechanism is identical.

Add a demo rule where relevant: nothing unshipped may be screen-recorded, narrated, or shown as if a customer could do it today. Video and live demos are where status discipline breaks first.

## 3. Claim ledger, the do-not-say file

The claim hygiene spine. Two columns, forbidden or risky on the left, the safe replacement on the right. **Never write a prohibition without a replacement.** A ban with no alternative gets ignored by whoever is on deadline, and it teaches an agent to route around the rule rather than obey it.

Four sections:

### Hard bans

The claims that are always wrong. Sources:

- Certifications and compliance not yet earned. The safe form is almost always "in progress," with the timeline if it is public.
- Unshipped capabilities described as live. Points at the status ledger.
- Blanket versions of conditional claims. Scope them to the mode, tier, or configuration where they are true.
- Pricing, tiers, and plan names when pricing is undecided.
- Invented proof: testimonials, customer counts, metrics, logos. The replacement names the closed set of real proof points.
- Banned vocabulary from the glossary.
- Framing that contradicts a strategic verdict, for example single-platform framing when expansion is decided.
- Channels the GTM excludes. The replacement is a redirect, not a softer version.

### Channel and medium specific bans

Some rules only bite in one medium. Spoken and video content is where unshipped capability gets demonstrated as live and where a caveat gets dropped for pacing. Write those rules separately, because a general rule does not survive contact with a script.

### Claims that need scoping

The valuable section, and the one that takes real work. For every superlative in the source material, run this drill:

1. State the claim as the strategy document phrases it.
2. Name the counter-example. Search for it properly. There is almost always one.
3. Write the narrowed form that survives the counter-example.
4. Record the verdict: the safe form, or "holds" if the claim is genuinely defensible.

Keep the counter-example in the file. It is what stops the broad form creeping back in six months, and it is what an operator needs when a prospect pushes back mid-call.

A claim that cannot be narrowed into a defensible form goes to hard bans.

### Historical and reputational material

Prior products, rebrands, public incidents, competitor history. State the accurate version and the instruction: handle it, do not repeat it as a selling point, and do not pretend it did not happen. Include competitor facts that are commonly misremembered, because an operator repeating a stale rumor about a rival is a credibility loss that is entirely avoidable.

## 4. Writing rules

How every word is written. Six sections:

- **Mechanics.** Punctuation bans, banned words and their obvious variants, paragraph length, and the preference for specifics over adjectives. Be concrete enough to check mechanically.
- **Tone.** Two or three sentences naming the register, then the reason it fits this product and this audience. The reason matters more than the adjectives: "the audience is technical and accountable" gives an agent something to reason from, "professional yet friendly" does not.
- **Medium-specific rules.** Writing for the ear if there is spoken content, and whatever the equivalent is for the mediums in the mix. Spoken writing has genuinely different rules and needs its own block.
- **Claim discipline.** One paragraph pointing at the claim ledger and the status ledger, and naming what triggers a check: every superlative, every capability mention, every conditional claim.
- **Channel discipline.** What this GTM writes and what it refuses to write.
- **Signature lines.** The reframes and phrases that are approved and reusable. This is where voice becomes concrete.

**Default starting set, to confirm or replace with the user.** Ship a brain with a real control layer rather than an empty one, then tune:

- No em dashes. Use commas, or restructure.
- Banned words: leverage, unlock, seamless, robust, streamline, cutting-edge, empower, and their obvious variants.
- Short paragraphs, one to three sentences.
- Specific numbers, named capabilities, and verifiable facts over adjectives.
- No stacked adjectives, no hype, no superlative that is not backed by the claim ledger.
- Prose over lists. Use a list only when the content is genuinely a list.

These are defaults, not doctrine. Ask the user to confirm each one and to add the bans specific to their brand. A brand with its own strong voice will replace half of this list, and that is the correct outcome.

## 5. QA checklist

The mechanical mirror of everything above. It is the last thing anyone reads before shipping, so every item must be answerable yes or no by looking at the draft. If an item requires judgment, rewrite it until it does not.

Group in this order, cheapest checks first:

1. **Writing.** Mechanics and banned words.
2. **Channel.** Is this a channel we produce for at all.
3. **Claims.** One line per hard ban, each pointing at its ledger.
4. **Naming and strategy.** Canonical vocabulary, and no framing that contradicts a decided verdict.
5. **Audience and stage.** One audience only, and copy matched to the funnel stage.
6. **Medium-specific.** A separate block for scripts, video, or anything with its own failure modes.
7. **Voice.** Does it read like the matching file in `examples/`.

The rule that keeps this honest: if a rule exists that cannot be turned into a checkbox, it is not a rule yet, it is a preference. Either sharpen it or move it to the writing rules as guidance.

## Keeping the layers in sync

The rules files duplicate the master context on purpose. Duplication has a cost, and the cost is paid by one convention:

- The master context is authoritative when the two disagree.
- A status or claim change updates the `rules/` file first, because that is what gets loaded on every task, then the corresponding master context section in the same change, then downstream copy.
- The audit script flags a rules file whose `last_reviewed` date is older than the master context's `last_updated`, because that ordering means a change landed in the reference layer and never reached the control layer.
