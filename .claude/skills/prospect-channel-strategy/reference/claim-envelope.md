# The claim envelope

Load for: starting a strategy, any line that touches a promise, a price, a capability, a figure or the guest side, and the last check before sending.

A prospect strategy is client copy. It is written for a company that has not asked for it, about its own business, and it will be read more carefully than anything on the website. Everything in the brain's control layer applies to it, and a few things apply harder, because a prospect who finds one invented number stops believing the rest.

The envelope is the brain's control layer, written into the workspace on the day the strategy is made, so the strategy can be checked against the rules that were in force, and re-checked when the brain moves on.

## Generate it

```bash
source ./paths.env
python3 "$STRATEGY_SKILL/scripts/claim_envelope.py" --out evidence/envelope.md --json evidence/envelope.json --prospect "$PROSPECT_ID"
```

`init_workspace.py` writes it once at the start. Write it again:

- before the handoff in phase 10,
- before sending, every time,
- whenever the brain's commit has changed since `strategy.json` recorded it (`envelope.brain_commit`),
- at the start of a REFRESH or an UPGRADE.

When the commit has changed, diff `rules/` and `ops/decisions.md` between the two commits, and re-read every strategy line the change touches. The envelope wins every disagreement with the strategy. A strategy never changes the brain: new market input goes to the brain's `ops/signal-log.md` and follows the amendment procedure there.

## What it contains, and how each part constrains the strategy

### 1. Open decisions

Each open decision closes a door in the copy. The envelope prints the brain's own table and adds what it means here. The lines that come up in nearly every strategy:

| Decision | Unsafe in a strategy | Safe |
|---|---|---|
| D2 price | "From [amount] per table", a fee in the calculator's investment field | "Written scope agreed before anything starts." The investment field is empty, labelled as any number they want to test |
| D4 promise | "We will fill twelve seats", "guaranteed attendance" | "You know what this channel can deliver against your real list before you spend." Seat counts are labelled as designed to show the arithmetic |
| D5 outreach | "We approach your guests" as a present-tense offer | "We do, once our privacy position is written." Status in the same sentence |
| D7 founder | "Founder-led", "the founder hosts every table" | Nothing, or the default stated as a default |
| D11 after the evening | "Handed to your sellers with the context of what was said", "your sellers follow up within days with what each guest shared" | "After the evening, the conversation continues only with guests who choose it, and nobody is chased. How that step works is designed with you, and it is not offered until that design is settled." |
| D11 guest promise | "Your details go to no one, including the host. Nothing follows." | "No attendee list is circulated, before or after." |
| D10 value metric | "Per qualified conversation", "per arrival" pricing language | Describe the work and the measures, never a unit price |
| D16 landing page | A link to the landing page draft | No link. The deck is the only surface |

### 2. Decided entries

Settled strategy is never relitigated inside a prospect file. The ones that shape every strategy: the product is a lead generation channel, not a room. Single test events are refused or repriced. The client supplies every conversion input. The proof set is empty and closed. The founder's record is a credential, not proof. Two audiences, two vocabularies. No venue, no catering, no production. The healthcare guest list is never ported.

### 3. Service status

The status words are law. READY is described in the present tense of the offer ("we plan"). IN BUILD is "in development". BLOCKED is mentioned only with its dependency, never with a date. ROADMAP is never implied. EXCLUDED is said plainly and said to be deliberate. A slide that describes a BLOCKED capability carries its status on the slide, in the same sentence or on a status tag beside it.

| What a strategy usually describes | Status | How it reads |
|---|---|---|
| The channel strategy itself | READY | "We plan the channel around your account list" |
| The coverage read on their named list | READY | "A full coverage read on your named list fills these in" |
| Identifying the named individuals | READY | "You see who will be approached before anyone is contacted" |
| Approaching them | BLOCKED, D5 | "Opens once our privacy position is written" |
| Conversation design for the evening | READY | "One question, set from what is live at the guests' organisations" |
| After the evening | BLOCKED, D11 and D5 | "Designed with you, not offered until that design is settled" |
| Reporting | IN BUILD | "The report format is in development" |
| Venue, catering, production | EXCLUDED | "You contract those directly. We supply none of them, by design" |

### 4. Cleared figures

The only market numbers that exist. A and B grades, attributed in the copy, with the source on the slide or in the notes. The rules that travel with them:

- **The 70% collision.** A deck is one conversation. When the 70% invite-only dinner benchmark appears anywhere, no reply rate appears anywhere, screen or notes. Almost every strategy uses the 70%, so almost no strategy cites a reply rate.
- **Figure 11 over figure 6.** For an invite-only executive event, use the Clutch Events 70%. The Pheedloop 40% to 60% loss applies only to "payment predicts attendance".
- **The arithmetic.** At 70%, twelve in the room needs about seventeen confirmations. Floors are set against confirmations, never invitations, and no floor is promised while D4 is open.
- **None of them is our performance.** Say "the category benchmark", never "what we see".

### 5. Hard bans and banned words

Printed in full in the envelope. The ones a strategy is most tempted by: a client count or name, an "illustrative" conversion figure, a network of executives, a price, the retired scope names, a format or city in a headline about The Warm Channel itself. The no-format rule governs our own headlines and website. A prospect's plan is about formats and cities, and names them freely.

## Answering a prospect who asks about an open decision

The strategy will provoke questions on the call. The answers come from the brain's `reference/objection-handling.md`. The short forms:

- **"What does it cost?"** "Written scope agreed before anything starts. I will not put a number on it until the scope says what it covers."
- **"Can you guarantee the room?"** "No. You will know what this channel can deliver against your real list before you spend, from the coverage read."
- **"Who have you done this for?"** "We are new. No case study yet, and we are not going to dress that up."
- **"What happens to the guests after?"** "The conversation continues only with the ones who choose it. How that works is the one thing we design with you before anything starts."
