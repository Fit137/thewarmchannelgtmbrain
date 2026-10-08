# Navigation contract

Load for: anything about how the file moves, before changing the shell, and for the Claude Design handoff, which must restate this in full.

The deck engine (`assets/deck-shell.html`) implements every line of this. A bespoke build must implement every line too. Navigation is specified before content because retrofitting routing into finished slides is the expensive path.

## Routes

| Address | Shows |
|---|---|
| `#/` or no hash | The home layer |
| `#/c` | Deck C, slide 1 |
| `#/c/5` | Deck C, slide 5 |

Every slide has its own address and survives a reload. An address past the end of a deck clamps to its last slide. An unknown deck goes home.

## History

- **Changing deck pushes** a history entry. Moving between slides inside a deck **replaces** it.
- So the browser's Back from anywhere in a deck returns to where the reader was before entering that deck, never steps back through every slide.
- After crossing from the end of one deck into the next, Back returns to the last slide of the previous deck.

## Keys

| Key | On the home layer | In a deck |
|---|---|---|
| 1 to 9 | Open that deck | Jump to that slide of this deck |
| Right, Space, Page Down | | Next slide. At the end of a deck, the next deck's cover |
| Left, Shift Space, Page Up | | Previous slide. From the first deck's cover, the home layer |
| Home, End | | First or last slide of this deck |
| Esc | Closes a panel | Closes a panel, otherwise back to the home layer |
| S | Sources panel | Sources panel |
| N | | Presenter notes in the present build. In the send build, a short notice that this copy has none |
| M | Motion on or off | Motion on or off |
| F | Full screen | Full screen |
| P | Print | Print |
| ? | The key map | The key map |

Keys are ignored while a field, select or editable element has focus, so typing in the calculator never turns a slide. Keys with Ctrl, Alt or Cmd held pass through to the browser.

## Pointer and touch

- On-screen previous and next arrows at the edges of the deck view.
- A slide rail at the foot: one tick per slide, the current one marked, each clickable and labelled for screen readers.
- Swipe left and right on touch screens, ignored when the gesture starts on a field or control.
- Any `[data-go]` element: `next`, `prev`, `home`, `close`, `help`, or `deck:c` and `deck:c:5`.
- Superscript source references open the sources panel at that source in a deck, and jump to the numbered list on the home layer.

## The chrome

A top bar on every deck slide: a back link to the overview with the recipient's mark and "Prepared for [Company]", the deck letter and name, and the slide count. Panels for notes, help and sources, a toast for brief notices, and a hint to turn a phone sideways. None of it prints.

## The end of a deck

Two visible actions on every close slide, and never a third:

1. **Back to the overview.**
2. **Next: [the next deck's name]**, or on the last deck, **the call to action**.

A reader who reaches the end of a deck with no way onward closes the tab.

## Query parameters

| Parameter | Effect |
|---|---|
| `?present` | Notes panel open on load, in the present build |
| `?notes` | Prints notes under each slide |
| `?still` | Starts with motion off, every animation in its resolved state. Used by screenshot.py |

## Accessibility

- A live region announces the deck, the slide number and the slide title on every change.
- Slides off screen are inert, so focus and screen readers stay on the visible slide.
- Every interactive element is reachable and operable from the keyboard.
- The visitor's reduced-motion setting is honoured without asking, and M toggles it.

## Print

The home layer prints first, then every slide on its own 1600 by 900 page, every animation resolved, the calculator's formulas in place of its results, and none of the chrome, controls or end-of-deck actions.

## Scaling

The stage is designed at 1600 by 900 and scaled with a single transform to fit the viewport, letterboxed on the surface role. Nothing is laid out at any other size, so a slide looks the same on a laptop, a projector and a phone turned sideways.
