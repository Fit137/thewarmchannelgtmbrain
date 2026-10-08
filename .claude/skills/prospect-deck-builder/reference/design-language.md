# Design language

Load for: writing a slide's design block, the design concepts file, a custom slide, or any change to how the deck moves.

The deck wears the prospect's colours and reads in The Warm Channel's register. Colour and type come from their brand kit. Geometry, timing, motion and restraint come from here, so every prospect deck behaves the same way while looking like it belongs to its reader.

## Register

A calm, exact briefing for an accountable marketing leader. Objects move like documents being laid on a table: they arrive, settle and stop. Nothing loops except the motif's slow turn on the slides that carry it. Persuasion comes from arithmetic and restraint, never from spectacle: a slide that performs for attention is doubted by exactly the reader this deck is for.

## Colour, as semantic roles only

Every colour on screen is one of twelve roles, mapped once from the brand kit and held everywhere:

| Role | Carries |
|---|---|
| surface | The page and slide background |
| surface 2 | Highlighted blocks, rows, columns, the invitation card |
| ink | Titles, headings, axes, strong text |
| body | Running text |
| muted | Kickers, captions, notes, quadrant names |
| rule | Hairlines between rows, month rules |
| accent | Links, hero figures, buttons, the anchor point, proposed moments, lit marks |
| accent ink | Hover states |
| on accent | Text on buttons |
| positive | Reserved |
| caution | `{TBD}` marks and status tags |
| flag | A calculator result that does not pay back |

The design concepts file names roles only. Hex values live in the brand kit file and in brand.json, nowhere else.

## Type, as relative hierarchy

At the 1600 by 900 design size the engine sets: title, largest; subtitle and statement body, second; body, third; notes and captions, smallest. Running text is never under 20px at the design size, so a projector at the back of a room stays legible. Letter-spaced capital labels (table and comparison headers, status tags, the invitation's subject line) sit at 18px, and the calculator's help lines at 15px, because the calculator is read up close, on the reader's own screen. Figures use tabular lining numerals everywhere. The display and text faces come from the brand kit, substitutes where the brand's own faces may not be redistributed.

## Motion vocabulary

- **One curve** for the whole file: a decelerating ease out.
- **Durations:** entry 560ms, slide change 520ms, line draws 900ms.
- **Stagger:** 110ms to 160ms between siblings, in reading order.
- **Entries:** rise 18px and fade, scale from 0.94, slide in 28px from the left, or draw from the left edge. Nothing bounces, nothing overshoots.
- **Counts:** figures count up from zero once on arrival, 900ms. Never on recompute, never on revisit.
- **At rest:** still, except the motif's turn on the slides that carry it.

## The 3D rig

Real 3D, CSS only, on the motif alone: a plane tilted 52 degrees back under a 1700px perspective seen from slightly above, marks lifted 30px toward the viewer when lit. On a centrepiece the plane tilts up to 4 degrees with the pointer. No 3D on charts, tables or type: perspective distorts position, and on a chart position is the claim.

## The motif: the named-account ring

A ring of small marks, one per account, around an empty centre. It stands for the structural fact of this whole offer: the channel starts from a list of named accounts, not from an audience.

- **Geometry:** 36 marks on a ring of radius 300px. Every third mark lights in the lit and connected states. Scatter positions are seeded, so every build places them identically. The count is not data and is never stated.
- **States:**
  - **scattered:** marks spread across the field, no ring, no centre. Cold channels, one at a time.
  - **ringed:** marks gathered into an even ring around an empty centre. The named list.
  - **lit:** one in three marks lifted and turned to the accent role, the plane tilted back like a table. The accounts in the room.
  - **connected:** the lit state, with thin accent lines drawing from the centre to the lit marks only. The conversation that continues, with those who choose it.
- **Movement into a state:** marks travel 22ms apart, lit marks lift at 900ms, the centre appears at 1200ms, lines draw at 1500ms, 40ms apart.
- **At rest:** the plane turns once every 140 seconds, unless the slide is still or a cover.
- **Rules:** never labelled, never counted, never explained on screen. Three to six appearances in different states. By the third, it reads without a legend. Lines run only to lit marks: a line to every mark would claim that every guest continues, which is the opposite of the slide.

## Layouts and their default treatment

The engine has seventeen layouts. Each has a default design treatment, written out in full by `render_spec.py` for any slide without its own design block: cover, statement, points, figure, table, quadrant, timeline, arithmetic, comparison, steps, journey, words, invitation, motif, calculator, custom, close. `build-guide.md` lists each one's fields.

## A slide's design block

Seven fields, imperative and executable: milliseconds, pixels at the design size, degrees, order.

| Field | Answers |
|---|---|
| stage | What is on the slide, and where, in roles |
| hero | The one object the eye should land on |
| entry | What arrives, in what order, how fast |
| ambient | What moves at rest, if anything |
| interaction | What the reader can do, with a keyboard path |
| restraint | What deliberately does not move, and why |
| reduced | The resolved state with motion off |

"A 120ms scale to 1.02" is executable. "A satisfying impact" is not.

## Centrepieces and the still slide

Four to six centrepieces, where the motion is the claim: in the standard decks, the quadrant, the rebuilt year, the arithmetic, after the evening, and the calculator. Each carries a full design block. One deliberately still slide, the carrying line, sits immediately before the rebuilt year, the biggest moment. Stillness is what makes the next slide land.

## Restraint

Decks fail from too much motion far more often than too little, and several restraints exist because the obvious animation would contradict the slide:

- A chart never moves at rest: a chart that moves asks to be read again.
- Existing moments on the rebuilt year dim but never disappear: the plan keeps them.
- No count-up on recompute: a number that spins while someone drags reads as a slot machine.
- The calculator never animates a result: a result that performs is doubted.
- The cover motif is static: the cover introduces the shape, it does not perform it.

The design concepts file ends with every restraint collected in one table.

## Reduced motion and print

Reduced motion ships the resolved end state of every animation, and every information-revealing interaction still works as an instant swap: the slider, the format select, the calculator, the panels, the rail. Print resolves everything too, and nothing in the file is hover-only, so nothing needs printing inline.
