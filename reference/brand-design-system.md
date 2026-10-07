# Brand and design system, Folio

Load for: any visual asset, page build, deck styling or design tool prompt. Distils `brand/DESIGN.md` (Folio 1.0.0, 2026-09-22) and the Claude Design handoff. The full system is in `sources/raw/warmchannelgtmbuild/brand/DESIGN.md`. Fonts and the reference page live in the build repository, see `ops/asset-index.md`.

## Why Folio

The page looks like a document, not a marketing site: warm paper, a serif set for reading, ruled tables, numbered footnotes, and a margin that carries apparatus instead of decoration. Three facts drive it. There is almost no photography and the brand promises none of the table. There is no logo, so type, space and rules carry the identity. The copy is an argument with citations, so footnotes are a credibility asset.

**Folio replaces Roster.** Roster was dark, near monochrome and derived from a developer tool. It is retired and archived. Never merge the two: no dark canvas, no `#0A0B0C` surfaces, no amber `#E8A33D`, no monospace face, no `seat-chip`, `roster-band`, `evidence-cite`, `concession-row` or `exclusion-block`. **Light only. No dark mode, and one is not coming.**

## Colour, nine tokens

| Token | Value | Use |
|---|---|---|
| paper | `#FBF9F5` | The page. Never pure white |
| paper-sunk | `#F4F1EB` | The one recessed surface: form fields, a quoted block |
| ink | `#14120F` | Headings, table headers, the masthead |
| body | `#3A3733` | Body text and table cells |
| muted | `#6B655C` | Margin notes, captions, footnotes |
| rule | `#DDD8CF` | Hairlines between rows, never text |
| rule-strong | `#C3BBAE` | The rule that closes a table, never text |
| accent | `#1F3A5F` | Exactly three things: the hero figure, the call to action, footnote markers |
| flag | `#6E2A2A` | Reserved. The one colour that says a number is bad, as when the calculator returns a bad answer |

One accent. A fourth use devalues the first three. `on-accent` is `#FBF9F5`, `accent-ink` is `#162B46`.

## Type

Folio Serif, from Newsreader, with an optical size axis from 6 to 72, which is why it was chosen. Leave `font-optical-sizing` at `auto`. Folio Sans, from Public Sans, with `ss01` baked in for the tailed `l`. **Folio Sans defaults to weight 100: always set `font-weight`.** Weights are 400, 500, 600 and 700 only.

| Role | Family | Size | Weight |
|---|---|---|---|
| Display | serif | 62px, 40px mobile | 400 |
| Section head | serif | 33px, 26px mobile | 400 |
| Standfirst | serif | 21px | 400 |
| Body | serif | 18px, leading 1.62 | 400 |
| Pull line | serif italic | 30px | 400 |
| Hero figure | sans, proportional figures, never tabular | 74px, 56px mobile | 600 |
| Table cell | sans, tabular figures in numeric columns | 13.5px | 400 |
| Table header, masthead | sans uppercase, tracked | 10 to 10.5px | 600 to 700 |
| Action | sans | 13px | 600 |

Serif for reading, sans for apparatus: what the reader reads as argument is serif, what labels, measures, cites or acts is sans.

## Layout and shape

A 132px margin column for section numbers and notes, a 40px gap, a 640px main column, a 1040px sheet. Prose capped at 64ch, about 65 characters. Sections separated by 64px of space, never by cards or panels. One breakpoint at 820px, below which the margin collapses above its section. Tables scroll inside their container with a 440px minimum width rather than shrinking. **Radius 0px everywhere, including the call to action. No shadows, gradients, glass, glow or 3D.**

## Components

`masthead` with a double rule, never sticky. `section-marker` in the margin, set "§ 1". `hero-figure`, one per section and never more than three on the page. `filing-table`, horizontal rules only, The Warm Channel row in ink at 600. `table-note`, where the honest caveat lives, never cut for length. `pull-line`, at most twice. `icp-rule`, once, under the standfirst. `footnote-ref` and `footnote-list`, **every footnote states its evidence grade**. `action`, one primary per screenful, no secondary button style. `calculator-form`, a form inside the document, results reuse hero figures and tables.

## Motion

Allowed: rules drawing in on first view at 240ms, calculator figures counting at 400ms, the action darkening on hover, visible focus rings. Not allowed: parallax, reveals, 3D, tilt, glow, particles, scroll-jacking, anything sticky. Respect `prefers-reduced-motion`.

## Known gaps

No logo, by founder decision. No validated categorical chart palette, and the page has no chart. No photography treatment, because consent tiers are unsettled. No print stylesheet. The reference page covers four sections of the landing page, the rest is specified but not built.
