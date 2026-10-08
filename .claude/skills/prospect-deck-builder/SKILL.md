---
name: prospect-deck-builder
description: Package a finished prospect strategy as an interactive single-file HTML deck in the prospect's own branding, showing a high-value lead the value, the return on their own numbers, the strategy and why to consider an in-person channel, then check it and send it privately. Scaffolds deck.json from the strategy.json of prospect-channel-strategy, drafts a brand kit from the prospect's site, writes notes and design concepts, renders the three-file walkthrough spec plus a brand kit and a sending checklist, builds send and present versions (deep links, keyboard and touch navigation, notes, print to PDF, reduced motion, a 3D motif, an ROI calculator the prospect fills in), and runs containment, claims, numbers and contrast checks with screenshots of every slide. Use when the user wants a prospect's strategy turned into a branded or interactive deck, deck specs for a lead, a deck rebuilt after a call or re-skinned, or a built deck checked before sending.
---

# Prospect Deck Builder

## Skill overview

The strategy is the gift. The deck is how it is handed over. It arrives in the prospect's own colours with their mark on the cover, opens on a page that makes the whole argument in one scroll, lets a curious reader go deeper in any order, lets them run the economics on their own numbers, and prints into a PDF their CFO can read without us in the room.

**It has four jobs, and every deck in the file serves one:**

| Job | Where the deck does it |
|---|---|
| **The value** | The whole file is theirs to keep, in their brand, built on their public year. Deck A shows we read their calendar more carefully than anyone selling to them. Deck F says the plan is theirs either way |
| **The return** | Deck E: the budget already spent, the cost per scan on their numbers, three ways to spend the same money, and a calculator that runs on their deal size and close rate and says so when it does not pay |
| **The strategy** | Decks B, C and D: who must be in the room, one decision per moment, the rebuilt year, the arithmetic of a full room, what happens after the evening |
| **Why this channel** | Deck A's attendance benchmark (70% for invite-only dinners against 19% for vendor-owned conferences), deck B's cold channels, deck E's three ways to spend, and the honesty of deck F |

**Inputs:** `strategy/strategy.json` from the **prospect-channel-strategy** skill, the prospect's public site, and the brain.
**Outputs, in the prospect's workspace:** `deck/deck.json`, `deck/brand.json`, five spec files in `spec/`, the send and present builds in `build/`, screenshots, a contact sheet and the PDF.

**What governs it.** The Warm Channel's go-to-market brain. Load its `CLAUDE.md` and control layer before writing any word: `rules/two-vocabularies.md`, `rules/glossary.md`, `rules/service-status.md`, `rules/do-not-say.md`, `rules/evidence-ledger.md`, `rules/writing-rules.md`. The deck is client copy, and the present build's notes are a conversation with the prospect: the same rules apply to both.

## Route first

| The situation | Mode | Do |
|---|---|---|
| A validated strategy.json, no deck yet | **BUILD** | Phases 1 to 8 |
| The deck needs a bespoke hand for one argument or one account | **HANDOFF** | Phases 1 to 4, then `reference/claude-design-handoff.md` instead of phase 5 |
| The strategy was upgraded to v2 after a call | **UPGRADE** | Scaffold a new deck.json from v2 (keep v1 as sent), carry over notes and design blocks that still hold, phases 3 to 8 |
| The brand kit was wrong, or the deck must go out neutral | **REBRAND** | Phase 2 only, then 5 to 6. Content untouched |
| A built deck file needs checking | **REVIEW** | Phase 6 only |

## Non-negotiables, as they apply to a deck

- **The proof set is empty.** No client, count, logo, testimonial, case study or result, on screen or in the notes.
- **Every number about the prospect is theirs:** `{TBD}` until they supply it. The calculator opens empty in a v1 deck.
- **Every percentage and money figure traces** to the brain's cleared ledger rows, the prospect's register, or declared provenance, with its source on the slide. Grade C never.
- **The 70% collision:** no reply rate anywhere in a deck that uses the 70% benchmark.
- **No guarantee, no price, no network claim. Nothing frozen by D11:** after the evening only in the consent framing, never a mechanism. **Status travels** with every capability that is not READY.
- **Their brand identifies the reader, never the author.** Their mark only in "Prepared for" and the top bar, never altered. "Prepared by The Warm Channel" stays.
- **Contained:** one file, no network request of any kind, no tracking, noindex.
- **Never published.** Sent once, privately, as the send build: a private link or a PDF, never an HTML attachment, never a public page.
- **No em dash, no en dash. Banned words:** leverage, unlock, seamless, robust, streamline, cutting-edge, empower. Commonwealth spelling.

## Required inputs

```
□ strategy/strategy.json, passing validate_strategy.py, gate verdict GO
□ evidence/evidence-register.md, passing evidence_check.py
□ The prospect's website address, for the brand kit
□ The brain, reachable from paths.env
□ Chrome or Chromium for screenshots and the PDF (found automatically)
□ Optional: Node and Playwright, for brand_probe.js
```

## The engine

`assets/deck-shell.html` with `scripts/build_deck.py`: one self-contained file, no libraries, no network.

- **Three levels:** a scrolling home layer that stands alone, decks of 1600 by 900 slides scaled to any screen, notes per slide.
- **Navigation:** hash routes and deep links (`#/c/5`), history that pushes on deck changes and replaces within a deck, arrows, Space, Page keys, Home, End, 1 to 9, Esc, swipe, on-screen arrows, a slide rail, two actions at the end of every deck. Full contract: `reference/navigation-contract.md`.
- **Seventeen layouts:** cover, statement, points, figure, table, quadrant, timeline, arithmetic, comparison, steps, journey, words, invitation, motif, calculator, custom, close.
- **Interaction:** the arithmetic slider and format select, the calculator, the motif's pointer tilt on centrepieces, the sources panel, the help panel.
- **The motif:** the named-account ring, real CSS 3D, four states, never labelled.
- **Builds:** send (no notes) and present (N for notes), from one source.
- **Print:** the home layer, then every slide, one per page. **Reduced motion:** resolved states, honoured automatically, toggled with M.
- **Brand:** twelve colour roles, embedded fonts, the embedded logo, a radius.

## Workspace

The prospect's workspace from the strategy skill, with `source ./paths.env` for `$DECK_SKILL`, `$STRATEGY_SKILL` and `$BRAIN`:

```
deck/deck.json, deck/brand.json, deck/logo.svg, deck/fonts/
brand/   brand_extract.py output: brand.draft.json, brand-report.md, raw/
spec/    01-content.md to 05-before-you-send.md
build/   [slug]_strategy_v1_send.html, _present.html, shots/, [slug]_strategy_v1.pdf
```

---

# PHASE 1: SCAFFOLD

## Step 1.1: Check the strategy is ready

**DO:**
```
python3 "$STRATEGY_SKILL/scripts/validate_strategy.py" strategy/strategy.json --register evidence/evidence-register.md
A deck is only built from a GO strategy that validates. If it fails, fix the strategy, not the deck.
```

## Step 1.2: Scaffold deck.json

**DO:**
```
python3 "$DECK_SKILL/scripts/new_deck.py" strategy/strategy.json --profile full --out deck/deck.json

Full: home and decks A to F, about 37 slides. Lite: home and four decks, about 20.
Every settled word is carried across verbatim. Read the TODO list it prints: each
[WRITE ...] marker is a line the strategy did not settle, and deck_check.py fails until
it is written. Notes are left empty on purpose.
```

**OUTPUT:** `deck/deck.json`. Architecture: `reference/deck-architecture.md`.

---

# PHASE 2: BRAND KIT

Method: `reference/brand-kit-method.md`.

## Step 2.1: Draft from their site

**DO:**
```
python3 "$DECK_SKILL/scripts/brand_extract.py" https://[their site] --company "[Company]" --out brand/
Optional, more accurate where Node and Playwright exist:
node "$DECK_SKILL/scripts/brand_probe.js" https://[their site] brand/probe.json
python3 "$DECK_SKILL/scripts/brand_extract.py" https://[their site] --probe brand/probe.json --out brand/
Offline: save the page with its stylesheets and pass --saved brand/raw/index.html.
```

## Step 2.2: Confirm, substitute, contrast

**DO:**
```
1. Open the site beside brand/brand-report.md and confirm every role by eye. Search for
   public brand guidelines and copy their logo rules into guidelines.constraints.
2. Choose the mark: the full logo, SVG where published, never the favicon, never altered.
   Copy it to deck/.
3. Type: an OFL family is fetched and embedded; a proprietary face gets an OFL substitute:
   python3 "$DECK_SKILL/scripts/fetch_font.py" "[Family]" --weights 400,600 --out deck/fonts
4. Save as deck/brand.json and check:
   python3 "$DECK_SKILL/scripts/contrast.py" deck/brand.json
   Fix failures with --fix, which moves lightness only and records the change.
5. If the brand cannot be captured cleanly, use "skin": "neutral".
```

**OUTPUT:** `deck/brand.json`, the mark, the fonts with their licence files.

---

# PHASE 3: CONTENT

Rules: `reference/content-rules.md`. Schema: `reference/build-guide.md`.

## Step 3.1: Write every unsettled line

**DO:**
```
Replace every [WRITE ...] marker. Headlines are claims. No on-screen paragraph over two
sentences. Their words, from the strategy's phase 1 glossary, not ours. Every figure with
its [n] source. Every unknown stays {TBD}.
```

## Step 3.2: Write the notes

**DO:**
```
Every slide gets "Say it" notes: first person, contractions, sayable at speed, about
2.5 words a second, with "seconds" set to their speaking time. The notes carry the argument
the slide only shows, and share no sentence with the screen. Say the Clutch Events source
aloud wherever the 70% figure is used. Notes obey every rule the screen does.
```

## Step 3.3: The home layer and before you send

**DO:**
```
Read the home layer alone, top to bottom, as someone who will never open a deck. It must
make the whole argument. Then fill before_you_send with single items, never softened.
```

**OUTPUT:** deck.json with every word final.

---

# PHASE 4: DESIGN CONCEPTS

Language: `reference/design-language.md`.

## Step 4.1: Design blocks for the slides that carry the argument

**DO:**
```
Every centrepiece (four to six) carries all seven fields: stage, hero, entry, ambient,
interaction, restraint, reduced, in executable terms: milliseconds, pixels, degrees, order.
The still slide sits immediately before the biggest moment. The motif appears three to
six times in different states. Colour only as roles. Any slide without a block gets the
engine's default treatment, written out in full by render_spec.py.
```

## Step 4.2: Render and check the spec

**DO:**
```
python3 "$DECK_SKILL/scripts/render_spec.py" deck/deck.json deck/brand.json --out spec/
Writes 01-content.md, 02-design-concepts.md, 03-build-handoff.md, 04-brand-kit.md and
05-before-you-send.md. File 2 must hold no hex value and no typeface name: deck_check.py
--design verifies it in phase 6.
```

**OUTPUT:** five spec files. HANDOFF mode continues in `reference/claude-design-handoff.md`.

---

# PHASE 5: BUILD

## Step 5.1: Both builds

**DO:**
```
python3 "$DECK_SKILL/scripts/build_deck.py" deck/deck.json deck/brand.json --out build/[slug]_strategy_v1_send.html
python3 "$DECK_SKILL/scripts/build_deck.py" deck/deck.json deck/brand.json --out build/[slug]_strategy_v1_present.html --audience present
A build error names the field and the reason. Fix deck.json or brand.json, never the built file.
```

---

# PHASE 6: CHECK

Checklist: `reference/qc-checklist.md`.

## Step 6.1: Automated

**DO:**
```
python3 "$DECK_SKILL/scripts/deck_check.py" build/[slug]_strategy_v1_send.html --deck deck/deck.json \
  --register evidence/evidence-register.md --design spec/02-design-concepts.md --brand deck/brand.json
python3 "$DECK_SKILL/scripts/deck_check.py" build/[slug]_strategy_v1_present.html --deck deck/deck.json --quiet
python3 "$DECK_SKILL/scripts/screenshot.py" build/[slug]_strategy_v1_send.html --out build/shots --pdf build/[slug]_strategy_v1.pdf
0 errors. Every warning read, and fixed or answered in writing in log.md.
```

## Step 6.2: By eye and by hand

**DO:**
```
Look at every screenshot and the contact sheet. Then in a browser: keyboard only through
every deck, the two actions at every close, Back after a deck change, a deep link in a fresh
tab, the slider, the calculator (empty, then a bad case, then a good one), reduced motion,
a phone at portrait and landscape, print preview, and the network off.
Run the brain's ops/QA-checklist.md client blocks against spec/01-content.md.
```

**OUTPUT:** a clean send build, checked shots, the PDF, the checks logged.

---

# PHASE 7: DELIVER

Procedure: `reference/delivery.md`. The message: the strategy skill's `reference/approach.md`.

## Step 7.1: Send once, privately

**DO:**
```
The send build only. A private, unlisted, noindex link on a random path, or the PDF, or
both. Never an HTML attachment, never a public page, never a tracking pixel, shortener,
UTM parameter or read receipt. One researched approach from the founder to one named person.
No follow-up to a non-reply.
```

---

# PHASE 8: LOG AND CLOSE

**DO:**
```
log.md: the date sent, version, format, the link's path, the take-down date.
The brain's ops/pipeline.md: the stage and date, by ID, never a person.
Take the link down at the first of: the anchor moment passed without a reply, a decline,
ninety days, or a new version sent. A reply goes to the brain's templates/discovery-call.md,
and numbers shared on the call start an UPGRADE in the strategy skill.
```

---

# SCRIPTS

| Script | Does |
|---|---|
| `scripts/new_deck.py` | Scaffolds deck.json from strategy.json, full or lite |
| `scripts/brand_extract.py` | Drafts brand.json and a report from the prospect's site, a saved page, or a probe |
| `scripts/brand_probe.js` | Optional, Node and Playwright: computed styles and a capture of the header mark |
| `scripts/fetch_font.py` | Fetches an OFL family as WOFF2 with its licence, refuses anything else |
| `scripts/contrast.py` | Checks every colour pair the shell uses, proposes the smallest fix |
| `scripts/render_spec.py` | Writes the five spec files from deck.json and brand.json |
| `scripts/build_deck.py` | Builds the send or present file |
| `scripts/deck_check.py` | The pre-send gate: containment, claims, guest copy, numbers, status, structure, notes, spec |
| `scripts/screenshot.py` | Headless Chrome: every slide, the home layer, a contact sheet, a gallery, the PDF |

Standard library Python, 3.8 or later, except brand_probe.js. Every script takes `--help`.

# REFERENCES

| File | Load for |
|---|---|
| `reference/deck-architecture.md` | The three levels, the decks, the profiles, the two builds, the PDF |
| `reference/navigation-contract.md` | Routes, history, keys, touch, chrome, the end of a deck, print, scaling |
| `reference/design-language.md` | Roles, type, motion, the 3D rig, the motif, design blocks, restraint |
| `reference/brand-kit-method.md` | Making brand.json: extraction, roles, contrast, type, the mark, provenance |
| `reference/content-rules.md` | Every word: on screen, the notes, frozen lines, style, the home layer |
| `reference/build-guide.md` | deck.json and brand.json field by field, every layout, troubleshooting |
| `reference/qc-checklist.md` | The full pre-send check, automated and by hand |
| `reference/delivery.md` | Sending, hosting, the PDF, take-down |
| `reference/claude-design-handoff.md` | The bespoke build path and the hooks that keep it checkable |

# TEMPLATES

`templates/01-content.md`, `02-design-concepts.md`, `03-build-handoff.md`, `04-brand-kit.md`, `05-before-you-send.md`: the five spec files, for drafting by hand before deck.json exists. `render_spec.py` writes the same files from deck.json.

# EXAMPLE

`assets/example/`: a complete fictional deck for Acme Example Co., built from the strategy skill's example. `deck.json` (6 decks, 37 slides, notes and design blocks), `brand.json` with an OFL font and a fictional mark.

```bash
python3 scripts/build_deck.py assets/example/deck.json assets/example/brand.json --out /tmp/acme_send.html
python3 scripts/deck_check.py /tmp/acme_send.html --deck assets/example/deck.json
```

---

# EXECUTION CHECKLIST

```
PROSPECT DECK PROGRESS, [Prospect ID]

□ PHASE 1: Scaffold
  □ 1.1 validate_strategy.py clean, gate GO
  □ 1.2 new_deck.py, profile chosen, TODO list read
□ PHASE 2: Brand kit
  ⚠️ 2.1 brand_extract.py from their site (WEB, or a saved page)
  □ 2.2 Roles confirmed, mark chosen, type substituted, contrast.py passes
□ PHASE 3: Content
  □ 3.1 Every [WRITE] marker replaced, in their words
  □ 3.2 Notes on every slide, timed, no shared sentence
  □ 3.3 Home layer read alone, before_you_send filled
□ PHASE 4: Design concepts
  □ 4.1 Centrepieces with all seven fields, the still slide, the motif placed
  □ 4.2 render_spec.py, five files
□ PHASE 5: Build
  □ 5.1 Send and present builds
□ PHASE 6: Check
  □ 6.1 deck_check.py 0 errors, screenshots and PDF
  □ 6.2 By eye, by hand, the brain's QA blocks
□ PHASE 7: Deliver
  □ 7.1 Send build, privately, one approach
□ PHASE 8: Log and close
  □ Logged, take-down date set
→ OUTPUT: build/[slug]_strategy_v1_send.html and build/[slug]_strategy_v1.pdf, checked and sent
```

# QUICK START

When the user wants a strategy turned into a deck, open with:

```
I'll package [Company]'s strategy as an interactive deck in their own branding: a home page
that makes the whole argument in one scroll, six short decks (what you already fund, who
has to be in the room, the plan, how a room fills, the economics on your numbers, how to
run it), a calculator they fill in themselves, and a PDF that reads without us.

I'll need:
1. The workspace with the validated strategy (or I'll check it now)
2. Their website, for the brand kit. I'll show you the palette, type and mark before building
3. Full or lite: full for a clear GO, lite for a thin footprint

Then: scaffold, brand kit, notes and design concepts, the five spec files, the send and
present builds, every check and every screenshot. Nothing is sent until you have looked
at the shots and the before-you-send list.
```

# SKILL METADATA

- **Version:** 1.0
- **Last updated:** October 2026
- **Phases:** 8
- **Modes:** BUILD, HANDOFF, UPGRADE, REBRAND, REVIEW
- **Profiles:** full (home and 6 decks, about 37 slides), lite (home and 4 decks, about 20)
- **Engine:** one self-contained HTML file, 17 layouts, send and present builds, print and reduced motion
- **Spec outputs:** 5 markdown files: content, design concepts, build handoff, brand kit, before you send
- **Scripts:** 9
- **Pairs with:** prospect-channel-strategy, which produces strategy.json
- **Governed by:** The Warm Channel go-to-market brain
