---
name: Folio
brand: The Warm Channel
version: 1.0.0
mode: light-only
replaces: Roster 1.0.0 (dark, superseded 2026-09-22, archived in brand/_superseded/)
colors:
  paper: "#FBF9F5"
  paper-sunk: "#F4F1EB"
  ink: "#14120F"
  body: "#3A3733"
  muted: "#6B655C"
  rule: "#DDD8CF"
  rule-strong: "#C3BBAE"
  accent: "#1F3A5F"
  accent-ink: "#162B46"
  on-accent: "#FBF9F5"
  flag: "#6E2A2A"
typography:
  serif: "Folio Serif"
  sans: "Folio Sans"
  display-size: "62px"
  h2-size: "33px"
  body-size: "18px"
  body-leading: "1.62"
  figure-size: "74px"
  label-size: "10px"
  label-tracking: "0.13em"
spacing:
  base: "4px"
  scale: "4, 8, 12, 16, 24, 32, 44, 64, 88, 120"
  section-gap: "64px"
  column-gap: "40px"
rounded:
  all: "0px"
measure:
  prose: "64ch"
  standfirst: "58ch"
  caption: "42ch"
  margin-note: "132px"
grid:
  sheet-max: "1040px"
  margin-column: "132px"
  main-column: "640px"
  breakpoint: "820px"
---

# Folio, the design system for The Warm Channel

## Overview

Folio makes the page look like a document rather than a marketing site: warm
paper, a serif set for reading, ruled tables, numbered footnotes, and a margin
that carries apparatus instead of decoration.

It exists because of three facts about this business, not because documents are
fashionable.

1. **There is almost no photography, and the product argues against getting
   more.** The Warm Channel sells discretion, to the point of promising no
   photograph of the table. A system that needs imagery is a system this brand
   cannot fill. Folio needs none, and that is a feature rather than a
   concession.
2. **There is no logo.** Type, space and rules carry the entire identity, so
   the typography has to be good enough to do that alone.
3. **The copy is an argument with citations**, not a list of features. It wants
   a reading surface. Footnotes become a credibility asset instead of clutter.

The system it replaces, Roster, was dark, near monochrome and derived from a
developer tool. Its buyer was an engineer. This one sells to a marketing leader
at an enterprise vendor who is reading an argument about where a large budget
goes, so the page has to look like something worth reading rather than
something worth scrolling past.

**There is no dark mode and one is not coming.** A document does not have one.
Building a second skin would produce a worse version of this one, not a choice.

## Colors

Nine tokens. If a colour is needed that is not here, the answer is almost
always a different weight of `{colors.ink}` or a rule.

| Token | Value | On paper | Use |
|---|---|---|---|
| `{colors.paper}` | `#FBF9F5` | n/a | The page. Warm off white, never `#FFFFFF` |
| `{colors.paper-sunk}` | `#F4F1EB` | n/a | The one recessed surface: form fields, a quoted block |
| `{colors.ink}` | `#14120F` | 17.8:1 | Headings, table headers, the masthead |
| `{colors.body}` | `#3A3733` | 11.3:1 | Body text and table cells |
| `{colors.muted}` | `#6B655C` | 5.5:1 | Margin notes, captions, footnotes, table notes |
| `{colors.rule}` | `#DDD8CF` | 1.3:1 | Hairlines between rows. Decorative only, never text |
| `{colors.rule-strong}` | `#C3BBAE` | 1.9:1 | The rule that closes a table. Never text |
| `{colors.accent}` | `#1F3A5F` | 10.9:1 | Hero figures, the call to action, footnote markers |
| `{colors.flag}` | `#6E2A2A` | 9.8:1 | Reserved. The one colour that says a number is bad |

Every contrast figure above was computed against `{colors.paper}`, not
estimated. The two rule tokens sit far below text contrast on purpose: they are
hairlines, and a rule you notice is a rule that is too dark.

**One accent, and it is load bearing.** `{colors.accent}` marks exactly three
things: the number the reader should leave with, the action they should take,
and the citation markers that prove the page is sourced. Using it for a fourth
thing devalues the first three. `{colors.flag}` appears only when the page has
to tell the reader something is against them, most importantly when the ROI
calculator returns a bad answer.

### Charts

There usually is not one, and that is the correct answer more often than it
feels like it is. Three data points is a hero figure plus a ruled table. A
seven row comparison is a table. Both beat a chart at this size, and both are
already in the system.

When a chart genuinely earns its place:

- Sequential work uses `{colors.accent}` stepped in lightness. One hue.
- Categorical series are capped at three, because there is no validated
  categorical palette here and generating one to fill a slot is how palettes
  break under colour vision deficiency.
- Never a dual axis.
- `{colors.flag}` is a status colour and never a series.
- A hero figure is set in `{typography.sans}` with proportional figures. Never
  the serif, which reads as decoration, and never `tabular-nums`, which gives
  every digit the width of a zero and opens visible gaps at display size.
  Tabular figures belong in table columns and nowhere else.

## Typography

Two families, both derived from OFL releases and both documented in
`brand/fonts/LICENSE-NOTICE.md`. Folio Serif comes from Newsreader, Folio Sans
from Public Sans.

**Folio Serif carries an optical size axis, 6 to 72, and that is why it was
chosen.** A 62px headline and an 18px paragraph are drawn as genuinely
different shapes from one family: the headline tightens, the body opens up.
Leave `font-optical-sizing` at its default of `auto` and this happens for free.
Pinning `opsz` by hand throws away the reason the face is here.

**Folio Sans defaults to weight 100.** It inherits Public Sans's variable
default, so any rule that sets the family without setting a weight renders
hairline. Always set `font-weight`. This has bitten once already.

Folio Sans ships with `ss01` baked into the cmap, so the tailed `l` and the
single storey `g` are the defaults. The tailed `l` is the point: it separates
`l` from `I` and from `1` on pages full of figures, labels and money.

| Role | Family | Size | Weight | Leading | Tracking |
|---|---|---|---|---|---|
| Display | serif | 62px | 400 | 1.04 | -0.021em |
| Section head | serif | 33px | 400 | 1.16 | -0.012em |
| Standfirst | serif | 21px | 400 | 1.52 | 0 |
| Body | serif | 18px | 400 | 1.62 | 0 |
| Pull line | serif italic | 30px | 400 | 1.26 | -0.008em |
| Hero figure | sans | 74px | 600 | 1.0 | -0.025em |
| Table cell | sans | 13.5px | 400 | 1.5 | 0 |
| Table header | sans | 10px | 700 | 1.4 | 0.13em, uppercase |
| Masthead | sans | 10.5px | 600 | 1.4 | 0.16em, uppercase |
| Margin note | sans | 11.5px | 500 | 1.5 | 0.04em |
| Caption, table note | sans | 11px to 12.5px | 400 to 500 | 1.5 | 0 |
| Footnote | sans | 11.5px | 400 | 1.72 | 0 |
| Action | sans | 13px | 600 | 1.0 | 0.03em |

The system ships four sans weights: 400, 500, 600 and 700. There is no 650.
A weight outside that set is a bug.

**Serif for reading, sans for apparatus.** Everything the reader reads as prose
is serif. Everything that labels, measures, cites or acts is sans. The split is
not decorative: it is how the page signals which parts are argument and which
parts are evidence.

## Layout

A two column grid: a narrow margin for apparatus, a wide column for prose.

```
|<-- 132px -->|<-- 40px -->|<----------- 640px ----------->|
   margin          gap              main column
   section no.                      headings, prose,
   margin note                      figures, tables
```

The sheet is capped at `{grid.sheet-max}` and centred, with 56px of side
padding. Prose is capped at `{measure.prose}`, which lands around 65 characters
at the body size. That measure is the single biggest reason the page reads as a
document rather than a landing page, and widening it undoes the effect.

Sections are separated by `{spacing.section-gap}`, not by cards, panels or
background changes.

## Elevation and Depth

**There is none.** No shadows, no gradients, no glass, no glow, no layered
cards, no 3D. Depth in this system is expressed by rules and space, the way it
is in print.

`{colors.paper-sunk}` is the single exception and it is not elevation: it
recesses a form field or a quoted block very slightly, so the reader can see
where to type.

This supersedes an earlier brief for this page that asked for 3D visuals with
motion. That brief is archived and is not in force.

## Shapes

Radius is `0px` on every element, including the call to action. Documents have
square corners. A rounded button on this page reads as an app control that
wandered in.

Rules are 1px. Table headers close with a 1px `{colors.ink}` rule, rows divide
on `{colors.rule}`, and the last row closes on `{colors.rule-strong}`. Tables
have no vertical rules, no zebra striping and no container.

## Components

### `masthead`
A row at the top of the page: the brand name in uppercase sans on the left, a
descriptor on the right, closed by a 1px `{colors.ink}` rule and a second
`{colors.rule}` hairline 3px below it. The double rule is what makes it read as
a publication rather than a nav bar. It is not sticky and it is not a menu.

### `section-marker`
The margin column entry: a section number, set `§ 1`, in uppercase sans over a
one or two line note in `{colors.muted}`. The note is not a subtitle, it is
apparatus, and it says what the section is for in the voice of an editor rather
than a marketer. On mobile it collapses above the section with a hairline over
it.

### `hero-figure`
The one number a section leads with. Sans, 74px, weight 600, `{colors.accent}`,
proportional figures. Directly under it a caption in `{colors.muted}` giving the
figure its meaning and its date, with a footnote marker. **One per section, and
never more than three on the page.**

### `filing-table`
The workhorse. Horizontal rules only. Header in 10px uppercase sans on
`{colors.ink}`, closed by a 1px ink rule. Body cells in 13.5px sans. Numeric
columns are right aligned and use `font-variant-numeric: tabular-nums`, so
digits stack. The row that describes The Warm Channel is set in `{colors.ink}`
at weight 600 with its label in `{colors.accent}`, which is the only emphasis
the table gets.

### `table-note`
An 11px sans paragraph in `{colors.muted}` directly under a table, carrying the
definition, the caveat or the arithmetic the table implies. This is where the
page does its honest work, and it should never be cut for length.

### `pull-line`
A single italic serif line at 30px, capped at roughly 24 characters, carrying
the argument of a section. Not a quotation and never in quote marks. Used at
most twice on the page.

### `icp-rule`
A short sans block in `{colors.muted}` with a 2px `{colors.accent}` rule on its
left edge, naming exactly who the page is for. It appears once, directly under
the standfirst, and it is deliberately the first thing that disqualifies a
reader.

### `footnote-ref` and `footnote-list`
Markers are superscript sans, 9.5px, weight 600, in `{colors.accent}`. The list
sits at the foot of the page under a 1px ink rule, numbered, in 11.5px sans on
`{colors.muted}`. **Every footnote states its evidence grade.** A page that
cites its own weak sources is more credible than one that hides them, and this
brand's claim rules require the grade anyway.

### `action`
A square `{colors.accent}` block with `{colors.on-accent}` text, 13px sans,
weight 600, 13px by 24px padding. One primary action per screenful. No
secondary button styles exist: a secondary action is a text link in
`{colors.accent}`.

### `calculator-form`
The ROI calculator rendered as a form inside the document, not a widget on top
of it. Fields are `{colors.paper-sunk}` with a 1px `{colors.rule}` border and a
sans label above. Results are `hero-figure` and `filing-table`, reusing those
components rather than inventing result cards. When the result is bad for the
reader, the figure turns `{colors.flag}` and the table note says so in words.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Let `font-optical-sizing` stay `auto` | Pin `opsz` to one value for the whole page |
| Set `font-weight` on every Folio Sans rule | Assume the sans default is 400. It is 100 |
| Use `tabular-nums` in table columns | Use `tabular-nums` on a hero figure |
| Set hero figures in the sans | Set a big number in the serif |
| Keep prose at `{measure.prose}` | Let body text run the full sheet width |
| Separate sections with space | Separate sections with cards or panels |
| Cite in the margin and the footnotes | Bury sources in grey parentheses |
| Keep every refusal and caveat visible | Trim the honest parts for polish |
| Use one accent for figure, action, citation | Add a second accent for variety |
| Write ranges with a hyphen | Use an em dash or an en dash, which this brand bans |

## Responsive Behavior

One breakpoint, at `{grid.breakpoint}`.

Below it the grid collapses to a single column and the margin apparatus becomes
a standfirst above its section, with a hairline over it and the section number
inline. Display drops 62px to 40px, section heads 33px to 26px, hero figures
74px to 56px. Side padding drops 56px to 20px.

**Tables scroll rather than shrink.** They are wrapped in an overflow container
with a 440px minimum width. A filing table squeezed into 350px stops being
readable, and the numbers are the argument.

## Iteration Guide

- The accent is one token. Swapping `{colors.accent}` to `{colors.flag}` turns
  the whole page oxblood, and both pass contrast.
- The typefaces are rebuilt by `python3 tools/build_fonts.py` from
  `brand/fonts/_src/`. Everything in `brand/fonts/` is generated.
- `brand/reference-page.html` is the reference implementation. It is real copy
  in real components, and it is the thing to check a change against.
- Adding a component means adding it here first. A page that grows components
  the system does not name is a page that has stopped being a system.

## Known Gaps

Stated rather than papered over.

1. **No logo.** Logo work was stopped by the founder. The masthead is currently
   a wordmark set in the system's own sans. It works, but a mark would sit at
   the left of that rule when one exists.
2. **No validated categorical chart palette.** Deliberate, because the page has
   no chart. If one is ever needed, the palette has to be built and run through
   a colour vision deficiency validator before use, not picked by eye.
3. **No photography treatment.** The brand has a handful of usable images and a
   consent problem with the rest. The system currently assumes none. A plate
   style, small, captioned, ruled, should be specified before the first image
   goes on the page.
4. **Print stylesheet.** A system this document-like should print well and
   currently has no print rules.
5. **The reference page covers four sections of the landing page**, not all of
   it. The rest is specified in `landing-page/PAGE-STRUCTURE.md` but not yet
   built.
