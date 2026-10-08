# The deliverable

Load for: writing strategy.json, the handoff in phase 10, and anyone building on this skill's output.

A strategy is three things: eleven markdown files a person can read, a register that every claim traces to, and one structured file, `strategy.json`, that the deck builder reads. The markdown is where the thinking happens. The JSON is the contract.

## The workspace

```
<root>/<slug>/
  README.md, log.md, paths.env
  strategy/00-gate.md ... 10-handoff.md
  strategy/strategy.json
  evidence/evidence-register.md, research-log.md, envelope.md, envelope.json, raw/
  brand/   deck/   spec/   build/
```

`<root>` defaults to a `twc-prospects` folder beside the brain repository. Never inside it.

## strategy.json, schema twc.prospect-strategy/1

Required for both deck profiles unless marked full only. Every `evidence` array holds register IDs (`E01`), never prose. Every other string is copy and is checked as copy: no dash, no banned word, no evidence ID, no scaffold marker, and every percentage or money figure traceable.

### Top level

| Field | Type | Notes |
|---|---|---|
| `schema` | string | `twc.prospect-strategy/1` |
| `fictional` | string, optional | Present only on worked examples |
| `version` | string | `v1` for BUILD, `v2` after UPGRADE |
| `mode` | string | `BUILD`, `UPGRADE` or `REFRESH` |
| `date` | string | YYYY-MM-DD, the day the strategy was finished |
| `basis` | string | "Public information only. No CRM, budget or account list seen." in BUILD |
| `envelope` | object | `generated`, `brain_commit`, `path`, `open_decisions` |
| `gate` | object | Written by gate.py: `verdict`, `total`, `scores`, `disqualifiers`, `notes` |
| `method` | string | The home layer's "How this was made" paragraph |
| `sources` | array | `n`, `text`, `kind`, `url`, `ledger`. Numbered from 1 in the order the deck cites them |
| `before_you_send` | object | `verified`, `needs_settling`, `designed_not_supplied`, each a list of single items |

### prospect

`id` (PX-0000), `company`, `short_name` (what the copy calls them), `slug`, `website`, `what_they_sell`, `who_they_sell_to`, `acv_band`, `segment`, `home_market`, `lang` (en-CA by default), `currency`, `evidence`.

### thesis

`kicker`, `headline` (the home layer's claim), `standfirst`, `carrying_line` (three sentences at most: keep, add, follow through), `one_paragraph` (the whole strategy in a paragraph, for the founder's own use).

### account

`summary`, `facts` (text, evidence), `priorities`, `priorities_evidence`. Feeds the method paragraph and the notes, not a slide.

### footprint

| Field | Notes |
|---|---|
| `window`, `start_month` | The twelve months mapped, and the month the strip starts on |
| `moments[]` | `id` (M1), `name`, `kind`, `role`, `month` 1 to 12, `week` 1 to 4, `today` (one or two words), `density` and `access` (-20 to 20, one decimal), `evidence`, `anchor` (exactly one true), `map_label`, `label_pos` (right, left, up, down), `same_as` (a repeat of another moment) |
| `quadrant` | `title` (a claim), `x_label`, `y_label`, `names` (top right, top left, bottom left, bottom right), `range`, `basis` |
| `timeline_title` | A claim about their year |
| `anchor_line`, `anchor_body` | The anchor statement slide |
| `chapter` | See chapters, below |

### buyers (full only)

`committee[]` (role, line, evidence), `committee_title`, `tiers[]` (tier, who, accounts, room_for), `list_note`, `chapter`.

### landscape (optional)

`summary`, `rows[]` (who, in_person, evidence), `white_space`, `use_in_deck` (false by default).

### channel

`choices[]` (moment id, today, recommendation, anchor first), `formats[]` (name, line, fits, evidence), `calendar[]` (label, month, week, around), `keep_on_calendar` (moment ids), `window_weeks`, `calendar_note`, `timeline_title`, `chapter`.

### questions and invitation (full only)

`questions[]` (label, question, for, why_live, evidence), `questions_note`, `invitation` (subject, body with paragraphs split by a blank line, note). The invitation is guest copy and is checked against the guest word list.

### operating

`arithmetic` (seats, formats[] with label and rate as a fraction, source_n, approached, approached_label, note), `arithmetic_title` (optional, written from the numbers otherwise), `six_weeks[]` (full only), `after` (title, body, in the consent framing), `measures[]` and `measures_note` (full only), `chapter` (full only).

### economics

`budget_line` (value, caption, source_n, ledger), `scan_cost` (theirs_label, benchmark, benchmark_label, source_n, ledger, cost_label, note), `options` (columns, highlight, rows of label and cells), `calculator` (inputs, currency, intro, and in UPGRADE only prefill with prefill_note), `chapter`.

### engagement

`options` (columns, highlight, rows), `steps[]` (label, line, status for anything not READY, result), `honesty_line`, `next_step` (headline, body, slide_title, slide_body), `cta` (label, href), `chapter`.

### Chapters

Every phase that feeds a deck carries one: `cover_title`, `cover_subtitle`, `claim`, `so_what`, `evidence` (two lines of copy for the home layer, with [n] source references), `carry`, `close_title`, `close_body`. The chapter is how the home layer stands alone: someone who never opens a deck reads the claim, the so-what, the evidence and the carry for every deck, in order, and has the argument.

## What the deck builder does with it

`new_deck.py` maps the strategy onto decks. Every settled word is carried across verbatim.

| Strategy | Full profile | Lite profile |
|---|---|---|
| thesis | Home: kicker, headline, standfirst, carrying line | Same |
| footprint | Deck A: cover with the ringed motif, the year as a timeline, the quadrant (centrepiece), the attendance benchmark figure, the anchor statement, the close | Deck A, same |
| buyers | Deck B: cover, committee points, cold channels (motif scattered), the named list (motif ringed), the tiers table, the close | Not used |
| channel, questions | Deck C: cover, choices table, formats, the carrying line (the still slide), the rebuilt year (centrepiece), the questions, the close | Deck B: cover with the lit motif, choices, the still slide, the rebuilt year, the arithmetic and the after-the-evening motif, the close |
| operating, invitation | Deck D: cover, the interactive arithmetic (centrepiece), the six weeks, the invitation, after the evening (motif connected, centrepiece), the measures, the close | Folded into deck B |
| economics | Deck E: cover, the budget line, the cost per scan, three ways to spend, the calculator (centrepiece), the close | Deck C: cover, the budget line, the calculator, the close |
| engagement | Deck F: cover, three ways to run it, what we would do and what is not set up, the next step, the close | Deck D: cover, the steps, the next step, the close |
| sources, before_you_send, method | Carried across | Same |

Presenter notes are never generated. They are written by hand in the deck builder, at about 2.5 words a second, sharing no sentence with the screen.

## Versioning

- `v1`: BUILD, public information only.
- `v2`: UPGRADE, with the prospect's own numbers and list. The v1 deck is kept, never overwritten.
- A REFRESH keeps the version, moves the date, and logs what changed.
