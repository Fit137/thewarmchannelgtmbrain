# Landing page structure

Build order for `TheWarmChannel_Landing_Page.md` in Folio components from
`brand/DESIGN.md`. Rebuilt 2026-09-22 on the `landing-page-copywriter`
14-section anatomy.

## What changed, and why it matters to the build

Earlier versions of this page were written as an essay: a sequence of arguments
in document order, with a refusals table and a six question FAQ. That is not a
conversion page. The page now runs a conversion formula, and the build has to
respect the emotional sequence rather than rearranging it for visual balance.

**Two sections of the formula are deliberately omitted.** There is no FAQ and
no "what we refuse to do" block. Both invite the reader into a discussion. The
page has one job.

**Every call to action on this page is the same call to action: book a call.**
There is no secondary CTA, no scorecard offer, no newsletter, no pricing table
to compare. A second option is a way to not do the first one.

## The sequence, and why each block is where it is

| # | Block | Job | Lead component |
|---|---|---|---|
| 0 | Masthead | Establish seriousness | `masthead` |
| 1 | Hero | Stop the scroll, name the transformation, identify the reader, first CTA | display, `standfirst`, `icp-rule`, `action` |
| 2 | What your pipeline desperately needs | Frame the problem at the level of deeper needs, three of them | three subheads, prose |
| 3 | What you're already doing right | Validate the reader, earn the right to deliver pain next, four of them | four subheads, short prose |
| 4 | But you're still | Pain, each one mirroring a block 3 behaviour, five of them | subheads, `hero-figure`, `filing-table` |
| 5 | Crescendo | One high-emotion transition into the solution | body prose, **no heading** |
| 6 | The solution | Crisp positioning before the mechanics | `pull-line` for the disambiguation |
| 7 | The big promise | The single line the rest of the page proves, then CTA | display, checkmark list, `action` |
| 8 | How it works in 3 steps | Make the mechanism feel achievable | numbered `filing-table` |
| 9 | Beyond the 3 steps | The measurement capability | short prose |
| 10 | vs the alternatives | Comparison, cost benchmarks, calculator, CTA | two `filing-table`, `calculator-form`, `action` |
| 11 | Transform closing | Sharpen the decision with side by side contrast | two-column `filing-table` |
| 12 | Founding client CTA | Scarcity framing, final CTA | `action` |
| 13 | Footer | Close | `masthead` styling |

**Blocks 3 and 4 are a pair and must stay adjacent.** Block 3 tells the reader
they have been doing the right things. Block 4 shows that doing the right
things has not been enough. Separating them, or reordering them for layout,
destroys the mechanism: the pain only lands because the validation came first.

**Block 5 has no heading.** It is a transition, not a section. A heading there
breaks the run from pain into solution. The capitalised phrases in it carry the
emotional weight and are not to be sentence-cased for tidiness.

## Where the figures go

Three `hero-figure` instances is the system ceiling. Two are used, both in
block 4, where the pain needs numbers:

- **40.8%**, the exhibitor budget share, under "Collecting badge scans instead
  of buyers". This is the wedge: the reader already spends more here than
  anywhere else.
- **1%**, the reported in-person conversion, directly beneath it.

The cold email decline is a three row `filing-table`, not a chart and not a
hero figure. Three points over seven years does not earn a chart.

## Component notes by block

**Block 1.** Category label above the headline in `masthead` styling. The
`icp-rule` is the "built for" line and it does the qualifying work. No image.

**Block 4.** Each pain is a subhead plus one or two short paragraphs. Keep them
short: the design system's prose measure applies, but a pain that runs four
lines stops being a punch.

**Block 7.** The checkmark list uses `{colors.accent}` marks and `{colors.ink}`
text. It is capability, never performance: nothing in it claims a conversion
rate, a lead count or a revenue figure.

**Block 10.** The first table is a four column comparison against the
alternatives, with The Warm Channel column set in `{colors.ink}`. The second is
the cost benchmark table. The calculator sits directly after them, because the
reader has just been given the comparison and the calculator lets them run it
on their own numbers.

**Block 11.** Old Way rows use the failure mark in `{colors.flag}`. New Way
rows use the accent mark. This is the one place two mark colours appear
together and it is intentional.

## Motion

| Allowed | Not allowed |
|---|---|
| Rules drawing in on first scroll into view, 240ms | Parallax of any kind |
| Calculator figures counting to their value, 400ms | Section reveals, fades, slides |
| The action darkening on hover | 3D, tilt, glow, particles |
| Focus rings, always visible | Scroll jacking, sticky anything |

All of it respects `prefers-reduced-motion: reduce` by not animating.

## What the build must not do

1. **Do not reorder blocks 2 to 5.** The formula is need, validation, pain,
   crescendo. It only works in that order.
2. **Do not add an FAQ, an objections block, or a refusals table.** They were
   removed on purpose. The page sells, it does not debate.
3. **Do not add a second call to action of any kind.** Every action on the page
   is book a call.
4. **Do not name a format, an event size, a city or a country.** The product is
   a channel. Naming a format tells every buyer planning a different one that
   they are not the customer.
5. **Do not use the word attendance, or attendee, as the product.** The unit is
   a qualified conversation.
6. **Do not add photography** until consent tiers are settled.
7. **Do not add a navigation bar.** One page, one action.
8. **Do not convert any table into a chart.**
9. **Do not introduce a second accent.** Block 11's failure mark is `flag`,
   which is a reserved status colour, not a second accent.
10. **Do not soften the capitalised lines in block 5.**

## Known gap

The calculator's money inputs are `type=number`, which cannot display thousands
separators, so a deal size reads `120000` while being typed. Worth fixing with
a text input that formats on blur and parses on input. Left alone because the
calculation logic behind it is stress tested.
