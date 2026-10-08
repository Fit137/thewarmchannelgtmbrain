# Build guide

Load for: editing deck.json or brand.json by hand, adding a slide, building, and debugging a build.

```bash
source ./paths.env
python3 "$DECK_SKILL/scripts/build_deck.py" deck/deck.json deck/brand.json --out build/[slug]_strategy_v1_send.html
python3 "$DECK_SKILL/scripts/build_deck.py" deck/deck.json deck/brand.json --out build/[slug]_strategy_v1_present.html --audience present
```

The build refuses, with the reason, on: an em or en dash anywhere, an internal evidence ID such as `[E07]` in copy, an unfilled `{{` placeholder, a missing required field, a deck that does not open on a cover or end on a close, an unknown layout, a points slide outside two to four, a table row of the wrong width, a calculator without its four required inputs, prefilled calculator values without a note, custom HTML with script or network loads, and brand roles that are not hex colours. It warns on a deck over nine slides, a missing presenter note in the present build, a `[WRITE ...]` scaffold marker, a crowded timeline and a file over 8 MB.

## deck.json, schema twc.prospect-deck/1

### Top level

| Field | Required | Notes |
|---|---|---|
| `schema` | yes | `twc.prospect-deck/1` |
| `fictional` | no | Worked examples only |
| `meta` | yes | See below |
| `motif` | no | `count` (36), `seed`, `lit_every` (3) |
| `home` | yes | See below |
| `sources` | no | `n`, `text`, `kind`, `url`. `[n]` in copy links to them |
| `design_global` | for the spec | `register`, `easing`, `rig`, `interaction`, `motif`, `constraints`, `accessibility` |
| `before_you_send` | for the spec | `verified`, `needs_settling`, `designed_not_supplied` |
| `number_provenance` | no | `{ "figure as written": "basis" }`, for a figure that is neither in the ledger nor the register, such as a P0 number in an UPGRADE |
| `brief` | no | `audience`, `ask`, for File 1's opening |
| `short_path` | no | Slide references for the ten-minute path, for example `["A1", "A3", "C5"]` |
| `custom_css` | no | Extra CSS. No network loads |
| `decks` | yes | One to nine. Each: `key` (one lower-case letter), `name`, `minutes`, `source`, `slides` |

### meta

`company`, `title`, `carrying_line` and `cta` (`label`, `href`) are required. Also `prepared_by`, `version`, `version_label`, `date_label`, `confidential`, `lang` (en-CA).

### home

`kicker`, `headline` (required), `standfirst`, `chapters` (one per deck: `deck`, `claim`, `so_what`, `evidence`, `carry`, required for every deck), `next_step` (`headline`, `body`), `method`, `signature`.

### Every slide

| Field | Notes |
|---|---|
| `layout` | One of the seventeen below |
| `title` | Required on every slide, even where it is visually hidden. A claim |
| `kicker` | Small capitals above the title. Covers get "Deck A of F, [name]" automatically |
| `foot` | A line at the foot of the slide |
| `notes`, `seconds` | Presenter notes, present build only, and their speaking time |
| `audience` | `both` (default), `send` or `present` |
| `centrepiece` | true for the four to six slides where motion is the claim |
| `still` | true for the deliberately still slide |
| `design` | `stage`, `hero`, `entry`, `ambient`, `interaction`, `restraint`, `reduced` |
| `css` | Slide-scoped CSS. `#this` is replaced with the slide's id |

Copy fields accept three inline marks: `**bold**`, `[n]` for a source, and `{TBD}`. Paragraphs split on a blank line.

### Layouts

| Layout | Fields | Use |
|---|---|---|
| `cover` | `subtitle`, `motif` (a state, static) | Slide 1 of every deck |
| `statement` | `body` | One claim, alone. The still slide |
| `points` | `points` (2 to 4: `label`, `line`), `body` | A set: roles, formats, questions |
| `figure` | `figures` (1 or 2: `value`, `caption`, `muted`), `body` | A benchmark, counted up on arrival |
| `table` | `columns`, `rows`, `numeric_columns`, `highlight_row`, `note` | Decisions, tiers, measures |
| `quadrant` | `points` (`label`, `x`, `y`, `anchor`, `label_pos`), `quadrants` (top right, top left, bottom left, bottom right), `range`, `x_label`, `y_label`, `aria`, `note` | Density against access |
| `timeline` | `items` (`label`, `month`, `week`, `kind` existing or proposed), `start_month`, `window_weeks`, `dim_existing`, `legend_existing`, `legend_proposed`, `legend_window`, `note` | Their year, and the rebuilt year |
| `arithmetic` | `steps` (`value`, `label`), `interactive` (`seats`, `min`, `max`, `ref`, `formats` with `label` and `rate`, `slider_label`, `select_label`), `note` | The confirmation arithmetic, the cost per scan |
| `comparison` | `columns`, `rows` (`label`, `cells`), `highlight_col`, `note` | Three ways to spend, three ways to run it |
| `steps` | `steps` (`label`, `line`, `status`, `result`), `note` | The six weeks, what we would do |
| `journey` | `stages` (`name`, `line`), `note` | A sequence along one line |
| `words` | `quote`, `attribution`, `body` | Their own published words, verbatim, attributed |
| `invitation` | `subject`, `body`, `note` | The sample guest invitation. Guest copy |
| `motif` | `state`, `body` | The named-account ring beside text |
| `calculator` | `inputs`, `labels`, `currency`, `intro`, `copy`, `prefill`, `prefill_note`, `calc_id` | The calculator on their numbers |
| `custom` | `html`, `show_title` | Anything else. No script, no handlers, no network |
| `close` | `body` | The last slide of every deck. The engine adds the two actions |

Calculator inputs: `deal`, `close`, `investment`, `conversations` (all four required), `cac`, `meeting` (optional). `labels` overrides a label and help line as `[label, help]`. `copy` overrides the result lines `good`, `bad`, `cheaper`, `dearer`, `wait`, `privacy`.

Quadrant points read -20 to 20 on both axes unless `range` says otherwise. Timeline items take a month (1 to 12) and a week (1 to 4). The engine packs labels into rows so nothing overlaps, and warns when it cannot.

## brand.json, schema twc.prospect-brand/1

| Field | Notes |
|---|---|
| `company`, `note`, `captured` | Who, any caveat, and when it was captured |
| `skin` | `prospect` (roles required) or `neutral` (the shell's own palette) |
| `sources` | `element`, `from`, `url`: where each part came from, and every contrast change |
| `guidelines` | `url`, `constraints`: their public brand rules |
| `roles` | All twelve, as `#rrggbb`: surface, surface_2, ink, body, muted, rule, accent, accent_ink, on_accent, positive, caution, flag |
| `fonts.display`, `fonts.text` | `family`, `weight`, `fallback`, `licence`, `substitute_for`, `files` (`path`, `weight`, `style`), paths relative to brand.json |
| `radius` | Corner radius for buttons, for example `6px` |
| `logo` | `path` (SVG, PNG, WebP or JPEG), `alt`, `usage` |
| `twc_signature` | "Prepared by The Warm Channel" |

## Adding a slide

1. Pick the layout that carries the claim. If none does, `custom`, and say so in its design block.
2. Write the title as a claim, the on-screen copy in two sentences at most, and the notes.
3. If it is a centrepiece, write all seven design fields.
4. Rebuild, then `deck_check.py --deck deck.json`.

## Custom slides

`custom` takes raw HTML inside the slide's inner frame. It may use the shell's classes and the role variables (`var(--c-accent)` and so on) and a slide-scoped `css` field. It may not carry `<script>`, `on...=` handlers, `javascript:` links, or anything that loads from the network. Behaviour belongs in the shell, where it is tested.

## Troubleshooting

| Symptom | Cause |
|---|---|
| A slide is blank in a screenshot | Taken with motion on before the entry finished. Use the default `?still` |
| The quadrant crowds its note | Too many points near one edge. Move a label with `label_pos` |
| A timeline label overlaps | Over three moments in one band and month. Shorten labels or split the slide |
| The calculator shows nothing | By design, until the four required fields hold numbers |
| Fonts fall back | A font path in brand.json is wrong, or the file is not WOFF2, WOFF, TTF or OTF |
| The PDF has only the home pages | The print was taken with screen media. Print from the browser or with screenshot.py --pdf |
