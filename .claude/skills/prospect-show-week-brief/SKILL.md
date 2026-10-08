---
name: prospect-show-week-brief
description: Build a free, one-page show-week brief for a qualified prospect with a trade show or conference coming up in 3 to 12 weeks, from public information only, in the prospect's own branding, as The Warm Channel's lightest value-first gift to a lead. Reads the week day by day (what they already fund, the organiser's programme, the sessions their buyers will attend, what competitors have announced for the evenings, and the slots still open as of a date), finds the question the week is asking, makes one suggestion with its confirmation arithmetic, honest timing and service status, then builds a static page and a two-page PDF and checks claims, numbers, containment and print. Reuses the gate and claim envelope from prospect-channel-strategy and the brand kit and checks from prospect-deck-builder. Use when the user wants a show-week brief, a brief on a prospect's upcoming show, a quick gift for a lead before an event, or the week around a conference read for a prospect.
---

# Prospect Show-Week Brief

## Skill overview

A prospect is about to spend real money on a show: a booth, a sponsorship, a breakfast. The week around it is crowded, and nobody on their team has time to read it whole. The brief does that, from public pages, on one page in their colours: where their buyers will be, what already competes for those buyers' evenings, what is still open, the question the week is asking, and one thing they could do with it. It is theirs to use whether or not they ever speak to us.

It is the smallest gift in the family, about half a day of work, and the one that fits when time is short:

| Skill | Gift | Cost | When |
|---|---|---|---|
| prospect-channel-strategy, prospect-deck-builder | The full in-person strategy, as an interactive deck | Two to four founder days | GO, with the anchor show eight weeks or more away |
| **prospect-show-week-brief** | **One page about one week** | **About half a day** | **GO or HOLD, with a show 3 to 12 weeks away** |

**One gift per prospect.** A brief and a strategy are never both sent unprompted. A second gift only after they reply.

**Built on the family.** The three skills sit side by side in the brain's `.claude/skills/`. This one reuses the strategy skill's gate, workspace helpers, claim envelope and register, and the deck builder's brand kit tools, brand loader and checker, so the brief looks and checks exactly like a deck. If the siblings live elsewhere, set `TWC_SKILLS` to their folder.

**What governs it.** The Warm Channel's go-to-market brain. Load its `CLAUDE.md` and control layer before writing: `rules/two-vocabularies.md`, `rules/glossary.md`, `rules/service-status.md`, `rules/do-not-say.md`, `rules/evidence-ledger.md`, `rules/writing-rules.md`. The brief is client copy.

## Non-negotiables, as they apply to a brief

- **Public information only,** read on a stated date. Nothing behind a login. Roles, never people: sessions by title, never by speaker.
- **Open means "nothing announced on public pages as of [date]",** never "nothing will happen". Re-checked within a week of sending.
- **Competitors appear only as public announcements,** attributed. Never their results, spend, guests or intentions.
- **Every figure traces:** the cleared ledger for the attendance benchmark, the organiser's published numbers as register rows. Everything about the prospect's plans is `{TBD}`. No reply rate on a page that uses the 70% figure.
- **One suggestion,** with its arithmetic, its timing said plainly, and its status wherever our work is mentioned. It always works without us.
- **No price, no guarantee, no network claim, no client, no result.** Nothing frozen by D11.
- **One page, one call to action, sent once,** privately, as a noindex link or the PDF. Never an HTML attachment, never tracked, never published, never reused.
- **No em dash, no en dash. Banned words:** leverage, unlock, seamless, robust, streamline, cutting-edge, empower. Commonwealth spelling.

## Required inputs

```
□ The company, its website, and a pipeline ID (PX-0000)
□ The show: its name and its first and last day, 3 to 12 weeks away
□ The brain, and the two sibling skills beside this one
□ Web search and fetch in this session, or a founder who will read the pages by hand
```

---

# PHASE 0: GATE, TIMING AND THE ONE-GIFT CHECK

**DO:**
```
source ./paths.env   (after step 1 below creates the workspace)
1. python3 scripts/init_brief.py "[Company]" --id PX-0000 --show "[Show]" --start YYYY-MM-DD --end YYYY-MM-DD
   Adds brief/ to an existing prospect workspace, or creates a light one outside the brain.
   Refuses a show under 3 weeks away.
2. If no gate exists yet, score it from public evidence with the strategy skill's rubric:
   python3 "$STRATEGY_SKILL/scripts/gate.py" --acv n --event-spend n --unreachable n --warm n \
     --converts n --owner n --write brief/brief.json
   A brief needs GO or HOLD, event spend at 2 or more, and no disqualifier.
3. Read log.md. If any gift was sent and there is no reply, stop.
4. On a GO with 8 weeks or more, decide brief or full strategy. One, never both.
```

# PHASE 1: THE SHOW AND THEIR PRESENCE

**DO:**
```
From the organiser's site: dates, opening and closing times, the agenda, the exhibitor
list, the sponsor page and the sponsorship prospectus. Record their stand, sponsorship and
any speaking slot, and the organiser's published audience line, each as a register row.
```

# PHASE 2: THE WEEK, SLOT BY SLOT

Method: `reference/method.md`. Template: `templates/brief-research.md`.

**DO:**
```
For the evening before the show and every show day, read every part of the day:
breakfast, morning, lunch, afternoon, evening, late. Record each announced thing with its
kind (yours, session, official, competitor, side, partner) and its register row.
Search the organiser's agenda and sponsor page, every competitor's events page, the
associations' calendars and public event listings for the city and dates. Where nothing
is announced, record the slot as open, with one register row naming the pages read and
the date. That date is open_as_of.
```

# PHASE 3: BUYERS, COMPETITION, THE QUESTION

**DO:**
```
1. Two to four sessions their buyer roles will sit in: title, day, time, track, and why,
   in their words. Never a speaker's name.
2. What already competes for their buyers' evenings, as announced, attributed.
3. The open slots that matter to them, and why each one does.
4. The question the week is asking: at least one session on it this year, ideally three
   signals by the strategy skill's test.
```

# PHASE 4: ONE SUGGESTION

Menu: `reference/suggestion-menu.md`.

**DO:**
```
Choose one idea from what the week shows. Write its title and two or three sentences.
Set the format and its cleared rate (0.70 dinners, 0.86 VIP and sport, 0.19 vendor
conferences) and the seats: the page computes the confirmations, rounded.
Say the timing plainly for the weeks left: a full table needs about six weeks of
individual approaches. Add the status line wherever our work appears, and make sure it
works without us: "You can run it with your own team."
```

# PHASE 5: COPY, BRAND, BUILD

**DO:**
```
1. Write the headline (a claim the page supports), the standfirst, the unknowns ({TBD}),
   the next step and the call to action into brief/brief.json. Fill before_you_send.
2. Brand kit: reuse the deck workspace's brand.json, or make one with the deck builder:
   python3 "$DECK_SKILL/scripts/brand_extract.py" https://[their site] --company "[Company]" --out brand/
   then confirm, substitute fonts with fetch_font.py, and pass contrast.py.
3. python3 "$BRIEF_SKILL/scripts/validate_brief.py" brief/brief.json --register evidence/evidence-register.md
4. python3 "$BRIEF_SKILL/scripts/build_brief.py" brief/brief.json brand/brand.json \
     --out build/[slug]_[show]_brief.html --pdf build/[slug]_[show]_brief.pdf
```

# PHASE 6: CHECK

**DO:**
```
python3 "$BRIEF_SKILL/scripts/brief_check.py" build/[slug]_[show]_brief.html --brief brief/brief.json \
  --register evidence/evidence-register.md --pdf build/[slug]_[show]_brief.pdf
0 errors, two pages. Then read it on a phone and in print, and run the brain's
ops/QA-checklist.md client blocks against the page.
```

# PHASE 7: SEND ONCE, LOG, TAKE DOWN

**DO:**
```
Re-check the open slots if more than a week has passed. Send with
templates/approach-message.md, once, to one person, as a private noindex link or the PDF.
Log in log.md: "| date | brief v1 sent | format, link path, take-down date |", and one row
in the brain's ops/pipeline.md by ID. Take the link down after the show. A reply goes to
the brain's templates/discovery-call.md, and next year's full strategy can follow it.
```

---

# SCRIPTS

| Script | Does |
|---|---|
| `scripts/init_brief.py` | Adds brief/ to a prospect workspace, or creates a light one, with the skeleton, research notes, register and envelope |
| `scripts/validate_brief.py` | Gate, one gift, timing, the week's shape, people, copy, numbers, the suggestion and the call to action |
| `scripts/build_brief.py` | Builds the static branded page, and the two-page PDF with `--pdf` |
| `scripts/brief_check.py` | The pre-send gate on the built page, from the deck builder's checker, plus the brief's own shape and page count |
| `scripts/_family.py` | Finds the two sibling skills and makes their scripts importable |

Standard library Python, 3.8 or later. Chrome or Chromium for the PDF, found automatically.

# REFERENCES AND TEMPLATES

| File | Use |
|---|---|
| `reference/method.md` | When a brief is the gift, reading the week, what open means, competitors, the page, the numbers, build and send |
| `reference/suggestion-menu.md` | Choosing the one suggestion, its arithmetic, its timing and its status |
| `reference/worked-example.md` | The fictional Acme at CloudSec Expo, start to finish |
| `templates/brief-research.md` | The working notes, written into the workspace by init_brief.py |
| `templates/brief.skeleton.json` | The empty brief.json |
| `templates/approach-message.md` | The message that carries the brief |
| `assets/brief-shell.html` | The page: static, phone-first, two printed pages |
| `assets/example/` | The fictional brief and its register |

# EXECUTION CHECKLIST

```
SHOW-WEEK BRIEF, [Prospect ID], [Show]

□ PHASE 0  init_brief.py, gate GO or HOLD, no gift outstanding, 3 to 12 weeks
⚠️ PHASE 1  The show and their presence (WEB RESEARCH)
⚠️ PHASE 2  The week, slot by slot, open_as_of set (WEB RESEARCH)
⚠️ PHASE 3  Buyers' sessions, competing evenings, open slots, the question (WEB RESEARCH)
□ PHASE 4  One suggestion: arithmetic, timing, status
□ PHASE 5  Copy, brand kit, validate_brief.py, build_brief.py --pdf
□ PHASE 6  brief_check.py clean, two pages, phone and print read, QA blocks
□ PHASE 7  Sent once, logged, take-down date set
→ OUTPUT: build/[slug]_[show]_brief.html and .pdf
```

# QUICK START

```
I'll read [Company]'s week at [Show] from public pages and put it on one page in their
colours: where their buyers will be, what already competes for their evenings, what is
still open, and one thing they could do with it. About half a day.

I need: the company and its site, the show and its dates, and a pipeline ID.
I'll check the gate and that nothing has been sent to them already before reading a page.
```

# SKILL METADATA

- **Version:** 1.0
- **Last updated:** October 2026
- **Phases:** 8, from the gate to the take-down
- **Output:** one static page and a two-page PDF
- **Scripts:** 4, plus the family helper
- **Estimated effort:** about half a day per brief
- **Depends on:** prospect-channel-strategy and prospect-deck-builder, installed beside it
- **Governed by:** The Warm Channel go-to-market brain
