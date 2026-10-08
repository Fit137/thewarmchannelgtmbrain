# Deck architecture

Load for: planning a prospect deck, choosing the profile, or changing what a deck contains.

A prospect deck is opened by someone who did not ask for it, with no presenter and no instructions, on whatever screen they had in hand. It has to make the whole argument on the first screen, let a curious reader go deeper in any order, and survive being forwarded to a CFO who opens only the PDF. That is why it has three levels.

## The three levels

1. **The home layer.** A scrolling overview page. The masthead with the recipient's mark and "Prepared for [Company]", the hero (kicker, headline, standfirst, the carrying line, a start button), the deck register, one chapter per deck, the next step with the one call to action, how this was made, the numbered sources, and the footer. **It stands alone:** someone who scrolls it and never opens a deck still gets the whole argument, because every chapter carries a claim, its so-what, its evidence and a line that carries into the next.
2. **The decks.** Horizontal sequences of slides, one per part of the argument. Each opens on a cover and ends on a close with exactly two actions: back to the overview, and onward to the next deck (the last deck offers the call to action instead).
3. **The slide.** A 1600 by 900 stage scaled to the viewport, with presenter notes attached in the present build only.

## The argument, deck by deck

The decks follow the strategy's phases, and the order is the argument: what you already do, who it is for, the plan, how it works, whether it pays, who runs it.

| Deck | Name | The claim it carries | From the strategy |
|---|---|---|---|
| A | What you already fund | You already fund an in-person year. It is not yet built around your buyers | Phases 1 and 2 |
| B | Who has to be in the room | Four or five people decide a deal. They are the room | Phase 3 |
| C | Run it as a channel | The plan keeps every moment you fund and adds the conversations around it | Phases 5 and 6 |
| D | How a room fills, and what happens after | A room fills by arithmetic, and the conversation continues by consent | Phases 6 and 7 |
| E | The economics | The money is already being spent. The question is what it buys | Phase 8 |
| F | How to run it | You can run this yourselves. We would like to run it with you | Phase 9 |

## Profiles

### Full, about 37 slides, about twenty minutes self-guided

| Deck | Slides |
|---|---|
| A | Cover with the ringed motif. The year as a timeline. The density and access quadrant, **centrepiece**. The attendance benchmark figure. The anchor statement. Close |
| B | Cover. The committee, in points. Cold channels, the motif scattered. The named list, the motif ringed. The tiers table. Close |
| C | Cover. One decision per moment, a table. The formats, in points. The carrying line, **the still slide**. The rebuilt year, a timeline, **centrepiece**. The questions. Close |
| D | Cover. The interactive arithmetic, **centrepiece**. The six weeks, in steps. The sample invitation. After the evening, the motif connected, **centrepiece**. The measures table. Close |
| E | Cover. The budget line, a figure. The cost per scan, arithmetic. Three ways to spend, a comparison. The calculator, **centrepiece**. Close |
| F | Cover. Three ways to run it, a comparison. What we would do and what is not set up, steps with status. The next step, a statement. Close, returning to the very first cover |

### Lite, about 20 slides

For a thin footprint, a single buyer role, or a HOLD that became a GO. Home, then:

| Deck | Slides |
|---|---|
| A | As in Full |
| B, the channel | Cover with the lit motif. Decisions. The still slide. The rebuilt year, centrepiece. The arithmetic, centrepiece. After the evening, centrepiece. Close |
| C, the economics | Cover. The budget line. The calculator, centrepiece. Close |
| D, how to run it | Cover. The steps with status. The next step. Close |

`new_deck.py --profile lite` builds it and re-letters the decks so keys stay contiguous.

## Rules of the shape

- **Nine slides per deck at most.** Over nine usually means two decks. The build warns.
- **Four to six centrepieces** in the whole file: the slides where the motion is the claim. Built with the most care.
- **One deliberately still slide,** immediately before the biggest moment. In both profiles it is the carrying line, just before the rebuilt year. A file at constant intensity has no peak.
- **The motif appears three to six times,** in different states, never explained. See `design-language.md`.
- **One call to action in the whole file,** on the home layer's next step and the last deck's close.
- **Slide 1 of every deck is a cover, the last is a close.** The close returns to its cover's claim. The last deck's close returns to the first deck's cover.
- **No slide without a job.** If a graphic could be deleted with nothing lost, it is decoration: cut it and say so in the design concepts.

## Two builds from one source

| Build | For | Notes | Sent? |
|---|---|---|---|
| send | The prospect | None in the file, and N says so | Yes, as a private link or a PDF |
| present | The founder, on a live walkthrough | N shows them, with timing | Never |

Both come from the same `deck.json` and `brand.json`. A slide can be limited to one build with `"audience": "present"` or `"send"`.

## The PDF

P, or the browser's print, prints the home layer and then every slide, one per 1600 by 900 page, in resolved states. `screenshot.py --pdf` prints it headless. The PDF is the copy that gets forwarded inside the company, so it must read alone: that is another reason the home layer carries the whole argument.
