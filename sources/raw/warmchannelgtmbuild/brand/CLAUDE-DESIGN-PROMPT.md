# The Claude Design prompt

Everything below the rule is the prompt. Copy it whole. It is written to stand
on its own, because Claude Design has none of the context this repo has.

Attach these files alongside it: `brand/DESIGN.md`, the eight static TTFs named
in `brand/CLAUDE-DESIGN-BRIEF.md`, `brand/reference-page.html`,
`brand/reference-page.png`, `landing-page/PAGE-STRUCTURE.md`, and
`landing-page/TheWarmChannel_Landing_Page.md`.

---

## REPLACE, DO NOT EXTEND

If a design system for The Warm Channel already exists in this workspace, it is
called **Roster**. It is dark, near monochrome, derived from a developer tool,
and it is **retired**. Do not merge it with what follows. Do not keep its dark
canvas, its `#0A0B0C` surfaces, its amber `#E8A33D` accent, its monospace face,
or any component named `seat-chip`, `roster-band`, `evidence-cite`,
`concession-row` or `exclusion-block`.

Delete or archive Roster and build the system below from scratch. A hybrid of
the two, a dark page with paper accents or a light page carrying amber, is the
specific failure to avoid. If you find yourself preserving one Roster value
because it "still works," stop: it does not.

## What the business is

The Warm Channel runs in-person as a **B2B lead generation channel**, end to
end. Pre-launch, one founder, no delivered engagement and no case study.

A client names the companies it wants as customers. The Warm Channel plans the
channel, gets the right people from those companies into the room, and works
the conversations afterwards until the client's sellers have sales-qualified
leads. Strategy, execution, the people, and the follow-through.

**The channel is in person, which spans many formats: a table of ten, a summit
of two hundred, a programme around a trade show the client already exhibits
at.** The format is a delivery detail.

### Three things that will wreck this page if you get them wrong

1. **Never name a format or an event size.** Writing "a room of twelve" or
   "an executive dinner" tells every buyer planning something else that they
   are not the customer. This exact mistake is why the previous version of this
   page was thrown away.
2. **Never name a city or a country.** The service is deliverable anywhere.
3. **Never sell attendance.** Attendance is one step of four, and leading with
   it undersells the product. The unit of value is a **qualified conversation**
   that becomes a sales-qualified lead. The word "attendee" does not appear as
   the thing being bought.

The founder configures four components on a sales call: strategy, convening,
running the programme, and post-event conversion. **On the page these appear
once, as four steps of one engagement.** Never as four things that can be
bought separately: a buyer offered four components buys the cheapest one and
then judges the whole channel on it.

The buyer is a marketing or demand generation leader at an enterprise vendor
with six-figure contract values, whose buyers will not answer a cold approach,
who already spends heavily on events, and who already knows that spend is
converting badly. The concentration is enterprise security vendors, but the
characteristics matter more than the vertical.

Three facts drive every design decision:

1. **There is almost no photography, and the product argues against getting
   more.** The service promises discretion. A design that needs imagery cannot
   be filled.
2. **There is no logo.** Type, space and rules carry the identity alone.
3. **The copy is an argument with citations**, not a feature list. It needs a
   reading surface.

## The system: Folio

The page should look like a **serious printed document**: a research note, a
prospectus, a filing. Warm paper, a serif set for reading, ruled tables,
numbered footnotes, and a margin carrying apparatus rather than decoration.

Not a marketing site. Not a SaaS landing page. Not a dashboard.

**Light only. There is no dark mode and one is not wanted.** A document does
not have one.

### Colour

```
paper         #FBF9F5   the page, warm off white, never #FFFFFF
paper-sunk    #F4F1EB   the only recessed surface: form fields, quoted blocks
ink           #14120F   headings, table headers, masthead
body          #3A3733   body text, table cells
muted         #6B655C   margin notes, captions, footnotes, table notes
rule          #DDD8CF   hairlines between rows, never text
rule-strong   #C3BBAE   the rule closing a table, never text
accent        #1F3A5F   hero figures, the call to action, footnote markers
flag          #6E2A2A   reserved: the colour that says a number is bad
```

Contrast against paper, computed not estimated: ink 17.8:1, body 11.3:1, muted
5.5:1, accent 10.9:1, flag 9.8:1. The two rule tokens sit near 1.3:1 and 1.9:1
because they are hairlines. A rule you notice is too dark.

**One accent, and it is load bearing.** `accent` marks exactly three things:
the number the reader should leave with, the action they should take, and the
citation markers that prove the page is sourced. Do not introduce a second
accent, a tint ramp, or a "secondary brand colour." `flag` appears only when
the page must tell the reader something is against them.

### Typography

Two families, both supplied as files:

- **Folio Serif**, for everything the reader reads as prose.
- **Folio Sans**, for everything that labels, measures, cites or acts.

That split is not decorative. It is how the page signals which parts are
argument and which parts are evidence.

**Two traps that will break the build if ignored:**

1. **Folio Sans defaults to weight 100.** Any rule that sets the family without
   setting a weight renders hairline. Always set `font-weight` explicitly.
2. **Folio Serif carries an optical size axis, 6 to 72.** Leave
   `font-optical-sizing: auto`. Do not pin `opsz` to one value for the page: a
   62px headline drawn at text optical size looks slack, and the axis is the
   whole reason this face was chosen.

Scale:

| Role | Family | Size | Weight | Leading | Tracking |
|---|---|---|---|---|---|
| Display | serif | 62px | 400 | 1.04 | -0.021em |
| Section head | serif | 33px | 400 | 1.16 | -0.012em |
| Standfirst | serif | 21px | 400 | 1.52 | 0 |
| Body | serif | 18px | 400 | 1.62 | 0 |
| Pull line | serif italic | 30px | 400 | 1.26 | -0.008em |
| Hero figure | sans | 74px | 600 | 1.0 | -0.025em |
| Table cell | sans | 13.5px | 400 | 1.5 | 0 |
| Table header | sans | 10px | 700 | 1.4 | 0.13em uppercase |
| Masthead | sans | 10.5px | 600 | 1.4 | 0.16em uppercase |
| Margin note | sans | 11.5px | 500 | 1.5 | 0.04em |
| Caption, table note | sans | 11 to 12.5px | 400 to 500 | 1.5 | 0 |
| Footnote | sans | 11.5px | 400 | 1.72 | 0 |
| Action | sans | 13px | 600 | 1.0 | 0.03em |

Four sans weights exist: 400, 500, 600, 700. Any other weight is a bug.

**Numerals.** Table columns use `font-variant-numeric: tabular-nums` so digits
stack and right edges align exactly. Hero figures and any large standalone
number use the default **proportional** figures: tabular figures give every
digit the width of a zero, which opens a visible gap after a comma at display
size. Never set a hero figure in the serif; it reads as decoration.

### Layout

A two column grid: a narrow margin for apparatus, a wide column for prose.

```
|<-- 132px -->|<-- 40px -->|<----------- 640px ----------->|
   margin          gap              main column
   section no.                      headings, prose,
   margin note                      figures, tables
```

Sheet capped at 1040px, centred, 56px side padding. **Prose capped at about 65
characters a line.** That measure is the single biggest reason the page reads
as a document, and widening it undoes the effect entirely.

Sections separated by 64px of space. Not by cards, panels, borders or
background changes.

### Depth

**There is none.** No shadows, no gradients, no glass, no glow, no layered
cards, no 3D, no illustration. Depth is expressed by rules and space, as in
print. `paper-sunk` is the one exception and it is not elevation: it recesses a
form field slightly so the reader can see where to type.

**Radius is 0px on every element, including the call to action.** Documents
have square corners. A rounded button here reads as an app control that
wandered in.

Rules are 1px. Table headers close with a 1px `ink` rule, rows divide on
`rule`, the last row closes on `rule-strong`. **Tables have no vertical rules,
no zebra striping and no container.**

### Components

Build these, named as given:

- **`masthead`** Brand name uppercase sans left, descriptor right, closed by a
  1px ink rule with a `rule` hairline 3px below. The double rule is what makes
  it read as a publication. Not sticky, and there is no navigation.
- **`section-marker`** The margin entry: a section number set `§ 1` in
  uppercase sans over a one or two line note in `muted`, written in the voice
  of an editor rather than a marketer.
- **`hero-figure`** The number a section leads with. Sans, 74px, weight 600,
  `accent`, proportional figures, with a caption under it giving the figure its
  meaning, its date and a footnote marker. One per section, at most three on
  the page.
- **`filing-table`** Horizontal rules only. Numeric columns right aligned and
  tabular. The Warm Channel's own row set in `ink` at weight 600 with its label
  in `accent`, which is the only emphasis the table gets.
- **`table-note`** An 11px sans paragraph in `muted` under a table, carrying
  the definition, the caveat or the arithmetic. Never cut this for length; it
  is where the page does its honest work.
- **`pull-line`** One italic serif line at 30px, about 24 characters, carrying
  a section's argument. Not a quotation, no quote marks. At most twice.
- **`icp-rule`** A short sans block in `muted` with a 2px `accent` rule on its
  left edge, naming exactly who the page is for.
- **`footnote-ref`** and **`footnote-list`** Superscript sans markers at 9.5px
  weight 600 in `accent`. The list under a 1px ink rule, numbered, 11.5px sans
  in `muted`. **Every footnote states its evidence grade.**
- **`action`** A square `accent` block, `paper` text, 13px sans weight 600,
  13px by 24px padding. One per screenful. No secondary button style exists: a
  secondary action is a text link in `accent`.
- **`calculator-form`** The ROI calculator as a form inside the document, not a
  widget on top of it. Fields `paper-sunk` with a 1px `rule` border and a sans
  label above. Results reuse `hero-figure` and `filing-table` rather than
  inventing result cards.

### Responsive

One breakpoint, 820px. Below it the grid collapses to one column and the margin
apparatus becomes a standfirst above its section, with a hairline over it and
the section number inline. Display drops to 40px, section heads to 26px, hero
figures to 56px, side padding to 20px.

**Tables scroll rather than shrink.** Wrap them in an overflow container with a
440px minimum width. A squeezed table stops being readable, and the numbers are
the argument.

### Motion

Almost none, and only what a document does: rules drawing in on first scroll
into view at 240ms, calculator figures counting to their value at 400ms, the
action darkening on hover, and always visible focus rings.

**No parallax, no section reveals, no fades, no slides, no 3D, no tilt, no
glow, no particles, no scroll jacking, no sticky anything.** All motion
respects `prefers-reduced-motion: reduce` by not animating at all.

## The page

Build in this order. The copy is settled and must not be rewritten: if a
section will not fit the layout, change the layout.

| # | Block | Lead component |
|---|---|---|
| 0 | Masthead | `masthead` |
| 1 | Hero: transformation headline, framing, built-for line, CTA | display |
| 2 | What your pipeline desperately needs, three needs | subheads, prose |
| 3 | What you're already doing right, four validations | subheads, short prose |
| 4 | But you're still, five pains | `hero-figure` 40.8% and 1%, `filing-table` |
| 5 | Crescendo transition, **no heading** | body prose |
| 6 | The solution | `pull-line` |
| 7 | The big promise, checkmarks, CTA | display, `action` |
| 8 | How it works in 3 steps | numbered `filing-table` |
| 9 | Beyond the 3 steps, measurement | short prose |
| 10 | vs the alternatives, cost table, calculator, CTA | `filing-table`, `calculator-form` |
| 11 | Transform closing, old way against new way | two-column `filing-table` |
| 12 | Founding client CTA | `action` |
| 13 | Footer | `masthead` styling |

This page runs a conversion formula, not an argument. **Blocks 2 to 5 are a
single mechanism and must not be reordered:** need, then validation, then pain,
then crescendo. The pain in block 4 only lands because block 3 told the reader
they had been doing the right things. Block 5 has no heading because it is a
transition, and its capitalised phrases carry the emotional weight and are not
to be sentence-cased for tidiness.

Exactly two `hero-figure` instances, both in block 4. Three is the system
ceiling.

**There is no FAQ and no refusals block, and neither is to be added.** Both
invite the reader into a discussion. **Every call to action on this page is the
same one: book a call.** No secondary CTA, no scorecard, no newsletter, no
pricing table. A second option is a way of not taking the first one.

Three blocks carry unusual weight and must not be softened:

- **Block 4's first pain is the wedge.** It says the client already spends more
  on in-person than on anything else and gets roughly 1% conversion back, so
  this is a reallocation of budget they already hold rather than a request for
  new budget. Do not shorten it.
- **Block 3 is not filler and must not be trimmed for length.** It is the
  validation that earns the right to deliver block 4's pain. Cutting it turns
  the pain section into an accusation.
- **Block 12 admits the business is new**, in the CTA block, and that stays.
  It is framed as founding client terms rather than as a confession, and it is
  the last thing read before the button.

The calculator's scope input is **qualified conversations you need**, ranging
from 1 to 200, so a ten person table and a two hundred person summit both
compute. It must be able to return a **bad** answer: at a low close rate and a
high fee it returns under 1x, the hero figure turns `flag`, and the note says
in words that the channel does not pay for itself. A calculator that can only
return good news is read as marketing and discounted.

## Do not

1. Name a format, an event size, a city or a country anywhere on the page.
2. Present the four components as separately purchasable, or use "attendance"
   or "attendee" as the thing being bought.
3. Add an FAQ, an objections section, a refusals table, or any second call to
   action. Reorder blocks 2 to 5.
4. Add a hero image, a stock photograph, an illustration or a 3D render. There
   is no imagery and there is not going to be any.
5. Turn any table into a chart. A three point series is a hero figure plus a
   table; a seven row comparison is a table. Both are already the right form.
6. Round any corner, or add a shadow, gradient or glass effect to anything,
   including the calculator.
7. Widen the prose column past about 65 characters.
8. Add a navigation bar. One page, one action.
9. Introduce a second accent colour or a tint ramp.
10. Soften, shorten or hide the refusals, the exclusions, or the pre-launch
   answer.
11. Use an em dash or an en dash anywhere. This brand bans both. Ranges take a
   hyphen.
12. Rewrite the copy.

## Accept only if

- [ ] Background is `#FBF9F5`, verifiably not white
- [ ] No rounded corners anywhere, including the action
- [ ] No shadow, gradient, glass or glow
- [ ] Numeric table columns align exactly on their right edge
- [ ] The hero figure is sans, and shows no gap after its comma
- [ ] Prose runs about 65 characters a line
- [ ] Footnote markers and the action are the same blue
- [ ] No em dash or en dash appears anywhere on the page
- [ ] At 390px there is no horizontal page scroll, and tables scroll inside
      their own container
- [ ] Every footnote states an evidence grade
