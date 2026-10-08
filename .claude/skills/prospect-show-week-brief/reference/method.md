# Method

Load for: reading a show week, deciding what goes on the page, and the rules that make it safe to send.

A show-week brief is the smallest useful thing The Warm Channel can give a prospect before a conversation: one page, in their colours, about a week they are already committed to. It works because it is specific, timely and finished. The reader learns something about their own week they did not have time to find, and can act on it without us.

## When a brief is the right gift

| Situation | Gift |
|---|---|
| GO, the anchor show eight weeks or more away | The full strategy and deck, or this brief. One, never both. The strategy when there is time to use it |
| GO, the show 3 to 8 weeks away | This brief |
| HOLD, with event spend scored 2 or more, and a show 3 to 12 weeks away | This brief. It costs half a day, so it is the right size for a HOLD |
| The show is under 3 weeks away | Nothing now. Note the next edition in the log |
| NO-GO, or any disqualifier | Nothing |
| A gift already sent and no reply | Nothing. One approach per prospect. A second gift only after they answer |

The gate is the strategy skill's `gate.py`, written into `brief/brief.json` with `--write`.

## Reading the week

About half a day, public pages only, nothing behind a login, and no person's name recorded. Work in this order, writing each finding into `brief/research.md` and the register as you go.

1. **The show itself.** The organiser's site: dates, opening and closing times, the agenda, the exhibitor list, the sponsor page, and the sponsorship prospectus, which is the best public evidence of who attends.
2. **Their presence.** Their stand on the exhibitor list, their sponsorship on the sponsor page, any speaking slot on the agenda, any event on their own events page.
3. **Their buyers' sessions.** Read the agenda for the roles the strategy skill's committee names: the tracks and sessions those roles will sit in. Record the session's title and track, never its speaker.
4. **What competes for the evenings.** The organiser's official receptions. Each competitor's events page. Associations' calendars. Public event listings for the city and the dates. Record what each one announced, as announced.
5. **The open slots.** A slot is open when nothing is announced against it on any of the pages above, on the day they were read. Record where you looked, as one register row, and set `open_as_of` to that day.
6. **The question.** The live question the agenda shows, ideally verified by the strategy skill's three-signal test, at least one session on it this year.

### Search patterns

```
[show] [year] agenda
[show] [year] exhibitors "[company]"
[show] [year] sponsorship prospectus
"[show]" dinner OR reception OR breakfast [month] [year]
[competitor] events [show]
site:[association domain] [show] [year]
```

## What open means, and how it is said

Open never means "nothing will happen". It means nothing was announced on the public pages read, on the date read. The legend on the page says exactly that, and `validate_brief.py` warns when `open_as_of` is more than seven days old: evenings in a show week fill, and a brief that recommends a slot somebody took last week is worse than no brief.

## Competitors on the page

Competitors appear only as public announcements, attributed: "Competitor A, an invitation-only dinner, announced on their events page". Never a judgement of their event, a guess at their guest list, their results, their spend or their intentions. Never a sentence that invites the reader to compare us with them.

## The page

| Part | Holds | Rule |
|---|---|---|
| Masthead | Their mark, "Prepared for [Company]", the version and date | The mark identifies the reader, never the author |
| Kicker, headline, standfirst | The show and dates, one claim about the week, what the page is | The headline is a claim the page supports |
| Three facts | Their presence, the audience as published, the week and how far away it is | Every figure cites the register |
| The week, day by day | Every slot read, by part and kind | Kinds are words, never colour alone |
| Where their buyers will be | Two to four sessions | Titles and tracks, never speakers |
| What competes for their evenings | Announced events, then the open slots | Public facts only |
| The question | One live question | In their buyers' words |
| One suggestion | One idea, its arithmetic, its timing, its status | One, never a menu. See `suggestion-menu.md` |
| What only you know | `{TBD}` lines | Things only their team can answer |
| The next step | One call, one button | No price, nothing changes hands |
| How this was made, sources | The method, numbered sources | Open means as of the date |

It is client copy throughout. No guest copy appears on a brief.

## The numbers that may appear

- The attendance benchmark behind the suggestion, from the cleared ledger rows only: 70% for invite-only executive dinners, 86% for VIP and sport hospitality, 19% for vendor-owned conferences (Clutch Events, B plus).
- What the organiser publishes about the show (an attendee count, a share of senior titles), as a P2 register row, attributed to the organiser.
- Their stand number, dates and times, as P2 rows.
- Nothing about their budget, their meetings, their pipeline or their results. Those are `{TBD}`.
- No reply rate, ever, on a page that uses the 70% figure.

## Build, check, send

```bash
source ./paths.env
python3 "$BRIEF_SKILL/scripts/validate_brief.py" brief/brief.json --register evidence/evidence-register.md
python3 "$BRIEF_SKILL/scripts/build_brief.py" brief/brief.json brand/brand.json --out build/[slug]_[show]_brief.html --pdf build/[slug]_[show]_brief.pdf
python3 "$BRIEF_SKILL/scripts/brief_check.py" build/[slug]_[show]_brief.html --brief brief/brief.json --register evidence/evidence-register.md --pdf build/[slug]_[show]_brief.pdf
```

The brand kit is made exactly as for a deck, with the deck builder's `brand_extract.py`, `contrast.py` and `fetch_font.py` and its `reference/brand-kit-method.md`. If the prospect already has a deck workspace, reuse its brand.json.

Delivery follows the deck builder's `reference/delivery.md`: the built file as a private, noindex link with a random path, or the two-page PDF; never an HTML attachment; no tracking; one approach; logged by ID; taken down after the show.
