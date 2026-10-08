# Research playbook

Load for: phases 0 to 6, and any REFRESH.

The strategy is built from public information only, until the prospect chooses to give us its own. That is a constraint and a selling point at once: everything in the deck is something [the prospect] could check, and the parts only they know are left for them to fill in.

## Principles

1. **Public only.** A page anyone can read without an account, a password or a pretext. Nothing received informally, nothing from a paid data broker, nothing from behind a login.
2. **Roles, never people.** The register records the company. A person appears only as a role ("the head of identity"), even when their name is on the page.
3. **Capture as you go.** Every fact becomes a register row the moment it is read: the claim as the source states it, the address, the date, what on the page supports it. Save the relevant excerpt to `evidence/raw/E##-short-name.md`, headed with the address and the capture date.
4. **Date everything.** Event calendars change every year. Use the current or next edition, and say which.
5. **"Nothing found" is a finding.** Log it in the research log. It is often the reason a score is 1.
6. **Conflicting sources are flagged, never silently resolved.** Record both rows, and say which the strategy relies on and why.
7. **Time-boxed.** The research log tracks minutes per phase. Running far over budget usually means the footprint is thin, which is a reason for the Lite profile, not for more hours.

## Tools in Claude Code

- **Web search and web fetch**, where the session has them. Search, then fetch the page, then capture the excerpt.
- **Without web tools**, this is an external research step, the way gtm-builder marks one: write the research scope (the pages and searches below, filled in for the prospect), hand it to the founder, and continue when the pages or excerpts come back. Never fill a gap from memory: a remembered fact has no address and no date.
- **A browser capture** of a page that renders with scripts: save the visible text, not the markup.

Never automate crawling beyond a handful of pages per site, never ignore a site's terms, and never submit a form to get content.

## Where to look, by phase

### Gate and account (phases 0 and 1)

| Source | What it gives |
|---|---|
| Their home, about and product pages | What they sell and to whom, in their words |
| Customers and case study pages | Buyer titles, deployment scale (an ACV signal), segments, sometimes metros |
| Pricing page | Contact-sales only, enterprise tiers, or self-serve prices |
| Careers page and job posts | Who owns events, whether they say "named accounts", "ABM", "pipeline", "prove event ROI" |
| Newsroom and press releases | Launches, expansions, partnerships, leadership roles (not names) |
| Investor relations, if public | Priorities, sometimes marketing spend lines |
| Trust or security pages | Regulated buyers, procurement friction (a sales cycle signal) |
| Their company page on a professional network | Size band, events tab, recent posts |
| Public review sites | The category they are listed in, reviewer titles |

### Footprint and landscape (phases 2 and 4)

| Source | What it gives |
|---|---|
| Their events page and blog | Own conference, roadshows, hosted moments |
| The segment's main shows: exhibitor lists, sponsor pages | Booths and sponsorship tiers, by edition |
| Show agendas and speaker lists | Speaking slots, the topics that are live |
| Sponsorship prospectuses | The organiser's audience profile: titles, seniority, numbers. The best density evidence there is |
| Partner and alliance pages | Co-hosted events |
| Announcements of dinners or receptions | Private formats already in use, theirs and competitors' |

Search patterns, adapted per prospect:

```
"[Company]" exhibitor [year]
"[Company]" sponsor [show] [year]
site:[show domain] "[Company]"
"[Company]" roadshow OR "user conference" OR summit [year]
"[Company]" dinner OR roundtable OR reception [show]
[segment] conference [year] agenda
[show] sponsorship prospectus [year] attendees
```

### Buyers and questions (phases 3 and 6)

| Source | What it gives |
|---|---|
| Case study quotes, webinar co-presenters | Who sits on the committee, by title |
| Job posts on the buyer side, at their customers' kind of organisation | What the buyer is accountable for this year |
| Conference agendas, this year's edition | Which questions get sessions |
| Regulators and standards bodies | Changes that force a question onto the buyer's desk |
| Incident reporting in the trade press | The problems that keep recurring |
| Practitioner communities, public threads | How the buyer talks about the problem, in their words |
| Analyst notes, public summaries | Category shifts |

## What never happens in research

- Contacting an employee of the prospect, or of its customers, to "ask a quick question".
- A pretext: posing as a candidate, a journalist, a buyer or a student.
- Buying, scraping or downloading personal data, including contact lists from event platforms.
- Recording a person's name, email, phone number or profile address in the register or anywhere in the workspace.
- Using anything learned under confidentiality elsewhere, including from the founder's past roles.
- Anything from the founder's separate healthcare business, D6.

## A new market figure

Research turns up statistics. A figure that is not in the brain's evidence ledger does not exist for this strategy. Record it as a NEW row in the register's unused table, add it to the brain's `ops/signal-log.md` verbatim with its source for grading, and carry on without it.

## The research scope, for a founder doing it by hand

```
RESEARCH SCOPE, [Prospect ID]

1. Events, last twelve months and next twelve:
   - [Company] events page: [address]
   - Exhibitor and sponsor lists: [show 1], [show 2], [show 3]
   - Their own conference or roadshow pages
   Return: name, month, their role, and the page address for each.

2. Buyers:
   - Three case studies: the titles quoted
   - Two job posts on their careers page that mention events, ABM or named accounts
   Return: the titles and the exact phrases, with addresses.

3. Questions:
   - The agendas of [show 1] and [show 2] for this year: session titles on [topic area]
   Return: titles and addresses.

Nothing behind a login. No names of people, only titles.
```
