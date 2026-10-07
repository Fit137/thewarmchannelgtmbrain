# Two vocabularies, the governing sensitivity

Checked on every asset before a word is written. Pick the audience first, then load its column.
last_reviewed: 2026-10-07

## Why this file exists

The two audiences occupy the same room and one of them is being sold to the other. The client buys a lead generation channel. The guest accepts an invitation to an evening with peers. A guest who reads client-facing language learns they were inventory, and returning guests are the only asset this business compounds. This rule held through the 2026-09-22 repositioning unchanged, and the repositioning made it sharper: the client is now promised leads, and every guest is one.

## The rule

1. Every asset has exactly one audience, declared before drafting: client or guest.
2. Client vocabulary never appears on a guest surface. Not in an invitation, a reconfirmation, a note afterwards, a summary, a partner-routed invitation, a public post a guest might read, or a slide shown in the room.
3. The two are never merged into one document that leaves the building. Internal analysis may use either set of words. Outbound copy may not.
4. Copy is never borrowed from one side to the other. Structure may be.
5. Guest copy in a template or example sits between `<!-- guest-copy:begin -->` and `<!-- guest-copy:end -->`, and `scripts/lint_claims.py` fails the run if a client word appears inside those markers.

## Words that never reach a guest

| Never on a guest surface | Why |
|---|---|
| lead, leads, lead generation, sales-qualified, SQL, MQL | Tells the guest what they are to the host |
| pipeline, funnel, conversion, convert, close rate, deal | The same |
| prospect, target account, named account, account list, ICP, in-ICP | Describes the guest as a target |
| composed attendance, access, inventory, coverage, show rate, attendance floor | The pre-2026-09-22 client vocabulary, banned from guests since the first run |
| channel, as in a lead generation channel | The product the client bought |
| client, as a description of the host | The guest meets a host |
| Anything about trust in digital channels declining, the cost of reaching a buyer, or reply rates | Tells the guest their presence is a workaround for someone else's marketing problem |
| Anything describing the guest's presence as something the host bought | Self-evident |

## Words for the guest

| Use | Meaning |
|---|---|
| The question | The one live problem the evening is built on, named in the first line |
| The evening, the table, the room | The event, described honestly, including its size and format |
| Peers, people dealing with the same problem | Who else is there, by role and organisation type, never by name before acceptance |
| The host | The named organisation paying for the evening, which did not choose the question and does not present |
| The summary | The written account, offered afterwards, attributing nothing to a named person without their permission |
| Nomination | One peer who should have been there. Never a list |

## Words for the client

Lead generation channel, sales-qualified lead, qualified conversation, named account list, coverage read, pipeline, channel strategy, post-event conversion, the arithmetic, capacity. Never "attendance" as the product, never "composed attendance", never a format in a headline. Full list in `rules/glossary.md`.

## Arguments that belong to one side only

| Argument | Side | Never |
|---|---|---|
| Trust scarcity, reply-rate decline, AI volume in inboxes | Client | Run at a guest |
| Badge scans, budget share, finance acceptance | Client | Run at a guest |
| No pitching, nothing circulated, a known end time | Guest | Sold to a client as a feature of their purchase. To a client say "your guests are treated as guests" |
| Who else is in the room | Guest | Promised to a client as a named list before guests accept |

## Edge cases

- **The brand name.** "The Warm Channel" describes a lead generation channel whose output is warm. Whether it appears as the sender on guest surfaces is D12. Until then, guest invitations come from the founder by name and name the host. Identify the sender wherever the law requires it, and flag the draft for D12.
- **A public LinkedIn post.** Assume guests read it. Client-side argument posts are allowed, but never describe guests, an evening or a named organisation as inventory or targets.
- **The demonstration room.** Observers are disclosed to guests in advance in guest words: "Two people from organisations considering hosting an evening like this will be present. They will not present or pitch." Observers do not pitch, per the 2026-09-18 plan.
- **Partner-routed invitations.** The partner's consent basis governs, and the guest vocabulary governs too.
