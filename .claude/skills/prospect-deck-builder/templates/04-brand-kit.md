# Brand kit, [Company]

The prospect's palette mapped to the deck's roles, with contrast, type and the mark, and where each element came from. The only spec file that holds hex values. `render_spec.py` writes it from brand.json. Method: `reference/brand-kit-method.md`.

Skin: [prospect or neutral]. Captured [YYYY-MM-DD].

## Roles

| Role | Value | Used for | Taken from |
|---|---|---|---|
| surface | `[#RRGGBB]` | page and slide background | [their page background] |
| surface_2 | `[#RRGGBB]` | highlighted blocks, rows and columns | [their light section band] |
| ink | `[#RRGGBB]` | titles, headings, axes | [their heading colour] |
| body | `[#RRGGBB]` | running text | [their text colour] |
| muted | `[#RRGGBB]` | kickers, captions, notes | [their secondary text, adjusted if it failed contrast] |
| rule | `[#RRGGBB]` | hairlines | [their borders] |
| accent | `[#RRGGBB]` | links, figures, buttons, the lit motif | [their primary button or brand primary] |
| accent_ink | `[#RRGGBB]` | hover states | [their hover colour, or a darker accent] |
| on_accent | `[#RRGGBB]` | text on buttons | [their button text] |
| positive | `[#RRGGBB]` | reserved | [their success colour, or the default] |
| caution | `[#RRGGBB]` | {TBD} marks and status tags | [their warning colour, or the default] |
| flag | `[#RRGGBB]` | a result that does not pay back | [their error colour, or the default] |

## Contrast

Paste `contrast.py brand.json` output. Every text pair at 4.5 to 1 or better, every TIGHT pair reviewed on a dim screen.

## Type

| Slot | Family | Weight | Files | Licence | Stands in for |
|---|---|---|---|---|---|
| display | [family] | [600] | [fonts/...woff2] | [OFL 1.1, see fonts/...LICENSE.txt] | [the brand's face, or itself] |
| text | [family] | [400] | [fonts/...woff2] | [OFL 1.1] | [the brand's face, or itself] |

## Mark

- File: [logo.svg]. Alt text: [Company].
- Usage: the Prepared for line and the top bar only.
- Never recoloured, redrawn, stretched, cropped, animated, or put in a lockup with another mark.
- Their published rules: [constraints from their brand guidelines, with the address, or none found].

## Where each element came from

- **palette:** [pages and selectors]
- **mark:** [address]
- **type:** [what the site sets, and the substitute chosen]
- **contrast changes:** [role, from, to]

Signature on the file: Prepared by The Warm Channel.
