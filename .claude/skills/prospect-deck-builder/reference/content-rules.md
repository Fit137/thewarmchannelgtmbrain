# Content rules

Load for: writing or editing any word in deck.json: slide copy, presenter notes, the home layer.

The brain's rules apply to every word in the deck. These are the ones that bite in a deck, plus the craft rules of the walkthrough format.

## Audience

The deck is client copy, written for the person who owns events and pipeline at the prospect, in client vocabulary: lead generation channel, named accounts, pipeline. The one exception is the invitation slide's card, which is guest copy, in guest words only, and is checked for client words by deck_check.py.

## Their words, not ours

Phase 1 of the strategy captured the prospect's own vocabulary. Use it: their name for their category, their buyers and their programmes. A deck that calls their "identity security platform" an "IAM tool" has told them it was written by an outsider.

## On screen

- **Headlines are claims, not labels.** "Your buyers are densest where your access is thinnest", never "Event analysis". A title under four words is flagged.
- **No on-screen paragraph exceeds two sentences.** The screen holds the artefact, the presenter holds the argument.
- **One idea per slide.** If a slide needs two headlines, it is two slides.
- **Every percentage and money figure carries its source**, as a `[n]` reference to the numbered sources list, which renders as a superscript that opens the sources panel.
- **Unknowns stay `{TBD}`,** rendered in the caution role. A `{TBD}` is never replaced with a plausible figure. Every one must be a number only the prospect can supply, and the copy around it says so.
- **Labels on charts are printed,** never hidden behind a hover.

## Say it, the presenter notes

- **First person, contractions, sayable at speed.** "I've only used public pages, so I'm sure your real calendar has more on it."
- **About 2.5 words a second.** `seconds` on each slide is the speaking time of its notes. deck_check.py warns when the two disagree by more than a third.
- **Screen and notes share no sentence.** The notes carry the argument the slide only shows. deck_check.py --deck flags a notes sentence of five words or more that appears on screen.
- **Notes obey every rule the screen does.** No reply rate when the 70% figure is in the deck. No price, no guarantee, no network, no client, nothing frozen by D11. The present build is still a conversation with the prospect.
- **Say the source aloud** whenever the 70% attendance benchmark is used: "That's the Clutch Events benchmark, across 191 invite-only events."

## The lines that are frozen or ruled

| Never | Write |
|---|---|
| Any reply rate, in a deck that uses the 70% benchmark | Argue cold channels in words: "Each approach lands alone, in an inbox every other vendor is also writing to" |
| "We guarantee", "you will get", "we will fill" | "You know what this channel can deliver against your real list before you spend" |
| A price, a fee, a range, a founding discount | "Written scope agreed before anything starts" |
| "Our network", "our community", "executives we know" | "Built per engagement from your named account list" |
| "Handed to your sellers with what was said", any hand-over mechanism | "After the evening, the conversation continues only with guests who choose it. How that step works is designed with you, and it is not offered until that design is settled" |
| "Your details go to no one. Nothing follows." in the invitation | "No attendee list is circulated, before or after" |
| "Founder-led", "the founder hosts every table" | Nothing. D7 is open |
| A capability that is not READY, in the present tense | The capability with its status in the same sentence, or a status tag on the step |
| A client, a count, a testimonial, a result | "We are new. No case study yet, and we are not going to dress that up" |
| The List, The Room, The Channel, as names | "Run it as a channel", lower case, as a description |

## Style

- No em dash, no en dash, anywhere, including the notes. A comma, a full stop, or "to" for a range.
- **Banned words:** leverage, unlock, seamless, robust, streamline, cutting-edge, empower. No exceptions inside a deck.
- Commonwealth spelling: programme, organisation, colour, behaviour, centre, favour.
- Numbers: figures in tables and on charts, words in sentences under ten except with units ("12 seats" on a block, "twelve seats" in a title is fine either way, but one deck is consistent).
- No exclamation marks. No rhetorical questions in titles.

## The home layer

The home layer must stand alone. Each chapter carries:

1. **A claim** as its headline.
2. **A so-what** line that ties it to the ask.
3. **Two lines of evidence,** each with its source reference where it holds a figure.
4. **A carry-forward** line into the next chapter.

The hero's headline is the strategy's thesis. The standfirst says it was built from the outside, from public information only, and that every number about their business is left for them. The carrying line sits under it.

## Close slides

The close returns to its deck's cover claim and carries one line into the next deck. The engine adds the two actions. The last deck's close returns to the very first cover of the file.

## Before you present

`before_you_send` in deck.json is the highest-trust part of the spec, rendered at the end of File 1. Three lists of single items, never softened: verified and where it traces to; needs settling and what breaks if it goes the other way; designed, not supplied, and the cost of committing to it.
