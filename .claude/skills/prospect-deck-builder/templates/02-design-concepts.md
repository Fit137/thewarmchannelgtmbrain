# [Deck title], design concepts

File 2 of 3. What gets designed on every slide to carry its argument.

> **No design system is specified here.** No hex values, no typeface names, no font stacks. Colour appears only as a semantic role: surface, surface 2, ink, body, muted, rule, accent, accent ink, on accent, positive, caution, flag. The builder maps each role once and holds it. Size appears only as relative hierarchy. Geometry, timing and motion are exact: milliseconds, pixels at the 1600 by 900 design size, degrees, order.

`render_spec.py` writes this file from deck.json, with the engine's default treatment for any slide without a design block. `deck_check.py --design` verifies it holds no hex value and no typeface name.

## Global

### Register, and how objects move because of it

[A calm, exact briefing. Objects arrive, settle and stop.]

### Motion vocabulary

[One curve, a decelerating ease out. Entry 560ms, slide change 520ms, draws 900ms. Stagger 110ms to 160ms.]

### The 3D construction rig

[Real 3D on the motif only: a plane tilted 52 degrees back, 1700px perspective, marks lifted 30px when lit.]

### Interaction contract

[Every interaction in the file, each with a keyboard path.]

### Build constraints

[Single self-contained file, no network, no libraries, tabular figures, reduced motion first class, print path mandatory.]

### Accessibility

[Contrast at least 4.5 to 1, accessible names on charts, a live region on every change.]

## The recurring motif

[The named-account ring: geometry, the four states, the movement into each state, the ambient turn, and the rules. Never labelled, never counted, never explained.]

| Slide | State | What the state says |
|---|---|---|
| [A1] | [ringed] | [the named list] |

## Centrepieces

| Slide | Title | Why the motion is the claim |
|---|---|---|
| [A3] | [title] | [one line] |

Deliberately still: [slide], immediately before [the biggest moment].

## Slide by slide

### Deck A, [name]

#### A1. [Title]

- **Stage:** [what is on the slide, where, in roles]
- **Hero object:** [the one object the eye lands on]
- **Entry motion:** [what arrives, in what order, how fast, in milliseconds]
- **Ambient:** [what moves at rest, or none, and why]
- **Interaction:** [what the reader can do, with its keyboard path, or none]
- **Restraint:** [what deliberately does not move, and why]
- **Reduced motion:** [the resolved state]

## Restraint register

| Where | Restraint | Why |
|---|---|---|
| Every chart and table | Never animates at rest | A chart that moves asks to be read again |
| [slide] | [restraint] | [why, especially where the obvious animation would contradict the slide] |

## Reduced motion and print

**Reduced motion.** [Every animation ships its resolved end state. Every information-revealing interaction works as an instant swap.]

**Print.** [The overview, then every slide, one per page, resolved. Nothing hover-only. The calculator prints its formulas.]
