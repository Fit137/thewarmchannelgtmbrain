# Brand kit method

Load for: making brand.json for a prospect, or changing one.

The deck is dressed in the prospect's colours so it feels like theirs from the first screen. That courtesy has limits, and the limits are the method: their mark identifies who the deck is for, never who made it; their colours are mapped to roles, never invented; their typefaces are honoured by a free substitute when the originals may not be redistributed.

## 1. Draft it from their site

```bash
source ./paths.env
python3 "$DECK_SKILL/scripts/brand_extract.py" https://www.[their site] --company "[Company]" --out brand/
```

It reads the home page and its stylesheets, proposes all twelve roles from what the site paints its background, text, headings, links and buttons with, finds the font families, and saves logo candidates to `brand/raw/`. It writes `brand/brand.draft.json` and `brand/brand-report.md`.

Without network access, save the page with its stylesheets from a browser and pass `--saved brand/raw/index.html`.

Where Node and Playwright are available, read the rendered page too. Computed styles beat stylesheet guessing:

```bash
node "$DECK_SKILL/scripts/brand_probe.js" https://www.[their site] brand/probe.json
python3 "$DECK_SKILL/scripts/brand_extract.py" https://www.[their site] --probe brand/probe.json --out brand/
```

## 2. Confirm every role by eye

Open the site beside the report. For each role:

| Role | Take it from | Watch for |
|---|---|---|
| surface | Their page background | Usually white or near white. A dark site still gets a light deck unless the brand is dark everywhere |
| ink, body | Their heading and running text colours | Pure black is rare. Their near-black is part of the look |
| accent | Their primary button or link colour, their brand primary | A campaign colour that appears on one page is not the brand |
| accent ink | A darker tone of the accent, often their hover state | |
| surface 2 | Their light section band | Must keep body text at 4.5 to 1 |
| muted, rule | Their secondary text and borders | Muted often fails contrast on their own site. Fix it here |
| positive, caution, flag | Their success, warning and error colours | The defaults are fine if they publish none |

Search for public brand guidelines ("[Company] brand guidelines", a press or media kit page). Where they exist, they outrank the site: copy their logo rules into `guidelines.constraints`, and record the address.

## 3. Contrast

```bash
python3 "$DECK_SKILL/scripts/contrast.py" brand/brand.json
python3 "$DECK_SKILL/scripts/contrast.py" brand/brand.json --fix brand/brand.fixed.json
```

Text pairs need 4.5 to 1, non-text 3 to 1. TIGHT means it passes on a laptop and may not on a projector. `--fix` moves only lightness, keeping hue and saturation, and records every change in `sources`.

**A light brand accent** (yellow, lime, cyan) cannot carry small text on white. Darkening it far enough changes the brand's feel. Better: use the brand's own dark secondary as the accent, and keep the bright colour out of the deck, or for the lit marks only through a slide's custom CSS.

## 4. Type

| The brand's face is | Do |
|---|---|
| On the OFL list | Fetch it and embed it: `fetch_font.py "[Family]" --weights 400,600 --out deck/fonts` |
| Proprietary, or its licence is unknown | A free substitute from the report's suggestions, judged by eye, fetched the same way. Record `substitute_for` |
| Served from a font service | Never called from the deck: the deck makes no network request. Embed an OFL file instead |
| Not worth matching | System fonts, nothing embedded |

The licence file sits beside the fonts. A proprietary face is never downloaded, embedded or redistributed, however easy it would be to fetch from their site.

## 5. The mark

- **Choose:** the full logo, not the favicon, as SVG where they publish one. Ranked candidates are in the report: header marks first, logo walls of other companies flagged.
- **Use:** only to identify the recipient, in the "Prepared for" line on the home layer and covers, and in the top bar.
- **Never:** recoloured, redrawn, stretched, cropped, animated, placed on a busy background, put in a lockup with The Warm Channel's name, or used as a watermark. If their mark only works reversed out, use their reversed version on a surface it was designed for, or leave the mark out and keep the name.
- **Alt text:** their company name.

## 6. Provenance

`sources` lists where every element came from: the palette from which pages and selectors, the mark from which address, the type and its substitute, and every contrast adjustment. The brand kit file (`04-brand-kit.md`, rendered by render_spec.py) prints it, so anyone can see what was taken and what was changed.

## 7. When the brand cannot be captured

Use `"skin": "neutral"`: the shell's warm neutral palette, no roles needed, their name in text and their mark only if a clean one exists. A neutral deck that is accurate beats a branded one that is wrong.

## What the brand kit never does

- Make the deck look as if it came from the prospect. "Prepared by The Warm Channel" stays in the footer and the build comment.
- Borrow a typeface it may not use, or a photograph from their site.
- Use their customers' logos, or anything from their case studies, as decoration.
- Get published. A prospect-branded file is delivered privately, never as a public page.
