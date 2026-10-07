# Decision log

What was decided, when, and why, so settled strategy is never relitigated, and what is still open, with an owner and a default. Newest first. Seeded on 2026-10-07 from every call the sources had already settled.

**Numbering.** D1 to D7 keep the numbers from `GTM-BRIEF.md` Section 4 so the history stays traceable. D8 onward were opened by the 2026-09-22 repositioning or found during the brain build.

**Amendment procedure, all steps or none.** Update the `rules/` ledger and its `last_reviewed`. Update the master context section, bump `version` and `last_updated`, revise `status_notes`. Write the entry here, including what it does not change and the downstream list. Grep the repo for the old phrasing and update `ops/copy-bank.md`, templates and references. List affected live surfaces from `ops/asset-index.md`. Regenerate `adapters/portable-control-layer.md`.

**Authority.** Only the founder decides. An agent may prepare a brief with `templates/decision-brief.md`, and never marks an entry DECIDED on its own.

## Open decisions at a glance, in the order to settle them

| # | Decision | Blocks | Default until decided | Owner |
|---|---|---|---|---|
| D1 | Register a business name and tax number | Invoicing, every compliant email, the scope, referral fees | Register before the first proposal | Founder |
| D5 | Written CASL and PIPEDA position, re-scoped | Guest outreach, the demonstration event, conversion contact | Send the re-scoped brief now. Partnership route only | Founder, counsel |
| D11 | Guest promise against post-event conversion | The hero component, half the landing page, the note afterwards | Consented continuation, recommended. Both contested promises frozen | Founder, counsel |
| D3 | Reconstruct the two commissioned rooms | The only proof the business could have | Do it this week, it needs nobody else | Founder |
| D8 | Concentration segment | Guest ICP, partners, research, scorecard wording | Enterprise cybersecurity | Founder |
| D4 | The promise, floor and remedy | The scope, the strongest copy, any per-unit price | Nothing promised | Founder |
| D9 | Unit of value name | Pricing, the scope, the report | "Qualified conversation" | Founder |
| D10 | Value metric | Pricing | Engagement fee shape, per-arrival and per-lead both open | Founder |
| D2 | Price | Every number | `{TBD}` everywhere | Founder |
| D13 | Founding client terms | Landing page block 12 | Wording approved, numbers `{TBD}` | Founder |
| D16 | Landing page pre-ship claim fixes | Publishing the page | Draft stays unpublished | Founder |
| D12 | Brand name on guest surfaces | Guest sender identity | Founder writes by name, host named | Founder |
| D14 | Guest ICP for the segment | Any guest approach | Follows D8 | Founder |
| D15 | Partner set for the segment | The only open guest route | Research R10, then founder | Founder |
| D7 | Founder attends and facilitates | Delivery cost, holding the no-pitch line | Attend the first three | Founder |
| D17 | Founder's own cost per lead and meeting history | Grade of the landing page economics | Grade C plus stays, attributed | Founder |

---

## 2026-10-07 The brain is the source of truth (DECIDED)
This repository is the go-to-market command center from 2026-10-07. The `warmchannelgtmbuild` repository becomes the workshop and archive: its markdown is copied verbatim into `sources/raw/` at commit 1aac76e and its rendered files stay there. New work starts here.
**What this does not change:** any decision below. The build repository's files remain valid evidence of what was researched.
**Downstream:** a pointer in the build repository's `CLAUDE.md` and `AGENTS.md`, done the same day.

## 2026-10-07 Build interpretations applied where sources conflicted (DECIDED, founder may overturn)
Each was resolved by the documented hierarchy, `POSITIONING.md` of 2026-09-22 governing, and is listed so none is silent.
1. Where `GTM-BRIEF.md` (09-16 to 09-18) and `POSITIONING.md` (09-22) disagree, POSITIONING wins, as its own text and every reconcile banner say.
2. The no-format rule covers client headlines and the website. A guest invitation describes its own evening honestly, including size.
3. "Institution" became "organisation" in guest copy, and one line gained "like yours", for segment neutrality. A PATCH.
4. The List, The Room and The Channel are retired as client-facing names until packaging is rebuilt.
5. Direct approach to client prospects stays open at low volume, as the 09-18 plan set it, and joins the D5 re-scope.
6. A six-flag status legend for a pre-launch services business: DELIVERED, READY, IN BUILD, BLOCKED, ROADMAP, EXCLUDED.
7. Post-event conversion is BLOCKED until D11, rather than published on the landing page as drafted.
8. Promise Discipline is not led with until D4 and D10 decide what is promised, because the 09-18 vector was built on refusing outcomes the channel now sells toward.
9. Four client drill lines and one guest line written for the brain are marked PROPOSED, never approved, in the value proposition files.
10. No guest or prospect personal data in this repository, even though it is private. Trackers use IDs.
**What this does not change:** any DECIDED entry from the sources.

## 2026-10-07 D11. The guest promise against post-event conversion (OPEN, highest priority)
The 2026-09-22 positioning makes post-event conversion the hero: conversations "qualified and handed over to your sellers with the context of what was actually said". Run B promises guests the opposite: "No contact details go to anyone, including the host", "No follow-up sequence", "Nothing follows", and a room where what is said stays in the room. POSITIONING said Run B "largely survives" without reconciling this. Both cannot ship. The guest promise is what wins the second acceptance, and the conversion step is what makes the channel a channel.
**Options.** (a) Consented continuation: each guest chooses, at or after the evening, whether to continue a conversation with the host, and conversion work is done only with those who opt in. Keeps guest trust, narrows the funnel, and needs counsel on the consent mechanics. This was candidate item 7, "consented introductions", in the 09-16 brief. (b) Guest copy changes to disclose that the host may follow up. Honest, and it likely lowers acceptance among the anchors the whole cohort depends on. (c) Conversion stays inside The Warm Channel: we follow up on the host's behalf without passing details. Still contradicts "nothing follows".
**Recommended:** (a). **Default until decided:** both contested promises frozen. "No attendee list circulated" stays approved. Nothing about any guest passes to a client without the guest's choice.
**What this does not change:** the two-vocabulary rule, guest list retention, the list-circulation refusal, the no-pitch rule.
**Downstream:** `rules/service-status.md`, `reference/value-proposition-guest.md`, `reference/engagement-playbook.md`, landing page blocks 7 and 8, `templates/guest-invitation.md`, the scope, the D5 brief question 4.

## 2026-10-07 D5 amended. The counsel brief must be re-scoped before it is sent (OPEN)
The 09-18 brief covered Canadian financial services guests and a Toronto room. The repositioning makes the ICP geography-free and the default segment security leaders, adds post-event conversion contact, and client-side prospecting was never asked. Add: which regime applies to recipients outside Canada, the segment's population, client prospecting, consented continuation, and the cross-client standing list. Detail: `reference/compliance-and-consent.md`.
**Default:** send the re-scoped brief now. Only the partnership route and inbound activity run until a written position exists.

## 2026-10-07 D12. The brand name on guest surfaces (OPEN)
"The Warm Channel" now means a lead generation channel whose output is warm. A guest who reads it as the sender can infer what they are to the host. CASL requires the sender to be identified. **Default:** the founder writes by name and names the host, and identifies the sender wherever the law requires it. Options for the founder: a separate guest-facing name, the founder's name only, or accept the risk.

## 2026-10-07 D14. Guest ICP for the chosen segment (OPEN)
The 09-18 guest ICP followed the old client ICP, bank and insurer executives. Re-derive it from D8. Anchors first, three functions at least, practitioners only.

## 2026-10-07 D15. Partner set for the chosen segment (OPEN)
CBA, CCUA, Advocis and Payments Canada served banking. Re-source through research R10 and verify each before contact. List ownership is agreed before the first conversation.

## 2026-10-07 D16. Landing page pre-ship claim fixes (OPEN)
Nineteen findings in `pages/landing-page.md`, from "highest-quality pipeline" and "no other channel" to an omitted cost row and calculator defaults that display a 5.0x result built from our numbers. The founder approves or rejects each safe form. **Default:** the page stays unpublished.

## 2026-10-07 D17. Cross-check the channel economics against the founder's own numbers (OPEN)
Most landing page economics are grade C plus. The founder's own historical cost per lead and per meeting outranks every aggregator. One hour.

## 2026-09-22 The product is a lead generation channel, not a room (DECIDED)
A done-for-you B2B lead generation channel built on in-person events. Format never in the headline. ICP by five characteristics, no geography on the page. Components configured on the call, never website sections. The website sells the outcome.
Rationale: attendance undersold the whole and invited comparison on the cheapest step, a room-centric offer excluded every buyer planning a different format, and a city-bound ICP served the operator, not the buyer. Detail: `reference/positioning-verdict.md`.
**What this does not change:** the two-vocabulary rule, the empty proof set, credential rules, the healthcare boundary, the channel exclusions, guest list retention, the client supplying conversion inputs, Folio.
**Downstream:** Run A Phases 1, 3, 4 rebuilt 09-22. Phases 5 to 9 reconciled in this brain on 10-07. Landing page rewritten 09-22.

## 2026-09-22 Folio replaces Roster (DECIDED)
Light-only, document-like design system, Newsreader and Public Sans derivatives, one accent, no logo, no photography. Roster, dark and derived from a developer tool, is archived and never merged.
**What this does not change:** any copy.

## 2026-09-22 The landing page is a conversion page with one action (DECIDED)
The 14-block anatomy. One call to action, "Book a call", three times. No FAQ, no refusals block, no navigation, no second offer.
**What this does not change:** the exclusions themselves, which live in the scope document and the call.

## 2026-09-22 Single test events are refused or repriced (DECIDED)
A buyer who wants one event to see if it works is judged on the day, while the output comes from weeks of conversion work.

## 2026-09-22 D8. Concentration segment (OPEN)
Cybersecurity scores highest on the criteria. Healthcare is the only segment with founder operating history. Fintech was the 09-16 choice. Phase 4 selected cybersecurity because the criteria were the instruction, and POSITIONING lists the choice as undecided. The 09-16 brief had rejected cybersecurity as saturated, and had left healthcare to the founder's separate business. **Default:** cybersecurity, with the rule to switch if the first ten conversations fail on credibility. Run research R1 first.

## 2026-09-22 D9. The unit of value's name (OPEN)
"Attendee" is a downsell and "lead" is what the buyer wants. The name has to exist because the price attaches to it. **Default:** "qualified conversation", the landing page's working term.

## 2026-09-22 D10. The value metric (OPEN)
Pay-per-arrival is format-agnostic and honest, and prices a step rather than the outcome. Pay-per-qualified-lead matches the promise and puts delivery risk on a business with no show-rate history, and it depends on D11. Per meeting and per pipeline dollar stay rejected. Detail: `reference/pricing-and-packaging.md`.

## 2026-09-22 D13. Founding client terms (OPEN)
The page offers a reduced fee, a free coverage read, founder delivery and a written scope. The fee, the read's scope and turnaround, and the number of founding slots need deciding. Follows D2.

## 2026-09-20 The landing page argues on channel economics, with attributed grade C plus figures (DECIDED)
The founder asked for a page argued on lead generation economics, and those figures exist only at grade C plus. Every one is attributed on the page, which is the mitigation, not a fix. Figure 32, the 30% to 50% dinner conversion and 300% to 500% ROI, never appears as a headline or as ours.
**What this does not change:** grade C is still banned in proposals, scopes, contracts, decks and emails.

## 2026-09-18 The channel mix is replaced (DECIDED)
No paid ads, no volume cold email, no LinkedIn automation. Client side: founder-led organic and low-volume direct approach, the demonstration event, partnerships. Guest side: nomination, founder direct approach, institutional partnership. Never advertising or sequences on the guest side.
Rationale: a business arguing that cold digital channels are decaying cannot run them at volume, paid against an unproven offer buys expensive evidence, and anti-spam law governs the core activity.

## 2026-09-18 The client supplies every conversion input (DECIDED)
We never supply a close rate, deal size or lead count, including as an illustration. Pricing on meetings or pipeline dollars is rejected absolutely.
**What this does not change:** D10 may still price per qualified lead, which is not the client's pipeline.

## 2026-09-18 The Warm Channel retains the guest list (DECIDED)
The client receives the event, the host position, the reporting and the qualified conversations. A client that requires the list is buying work for hire, priced materially higher or declined. The method is copyable in a weekend and the list is not.

## 2026-09-18 The founder's record is a credential, not a proof point (DECIDED)
Permitted wording only, four claims gated. Detail: `reference/founder-credentials.md`.

## 2026-09-18 The proof set is empty and closed (DECIDED)
No client, engagement, testimonial, reference or outcome exists. Unknown numbers are `{TBD}` and never invented. Proof fields are filled with method, never with claims.

## 2026-09-18 D6. The healthcare guest list is never ported (DECIDED, applied)
Guests who consented to invitations from a healthcare convening business did not consent to invitations from this one. Consent grounds first, brand second. Guest inventory starts at zero. Holds even if D8 picks healthcare.

## 2026-09-16 Two audiences, two vocabularies, never blended (DECIDED)
The two audiences share the room and one is sold to the other. Client vocabulary never reaches a guest surface. Detail: `rules/two-vocabularies.md`.

## 2026-09-16 No venue, no catering, no production (DECIDED)
A founder constraint. It removes venue liability, insurance exposure and catering float, and makes this a services engagement. It turned out to be the position: the client keeps the host position.

## 2026-09-16 D1. Register a business name and tax number (OPEN)
Accounts payable will not process an invoice without a tax number, so the funnel fails at the last stage after every earlier stage worked. Every commercial email also needs a mailing address. **Default:** register before the first proposal goes out. The only item with no strategic content, gating two unrelated things.

## 2026-09-16 D2. Price (OPEN)
The 09-16 bands were an analyst proposal, not a founder decision. Settle last, after D1, D11, D4 and D10. A price set before the promise is a guess wearing a number.

## 2026-09-16 D3. Reconstruct the two commissioned rooms into an auditable funnel table (OPEN)
The cheapest unblocking action in the business: an afternoon with send records moves the proof set from empty to non-empty. Define "reply" precisely. Once reconstructed, never say it in the same conversation as the Clutch 70% attendance benchmark.

## 2026-09-16 D4. The promise, its floor and its remedy (OPEN)
Originally an attendance floor with a named remedy, modelled on the worst show rate actually produced, never a meeting or pipeline guarantee. The repositioning asks what is promised now. Set any floor against confirmations, not invitations. At 70%, twelve needs about seventeen confirmations. The 09-18 recommendation: conservative for the first three, a re-run rather than a credit.

## 2026-09-16 D7. Does the founder attend and facilitate (OPEN)
The format survives a paying client only if someone in the room stops a pitch from the floor. **Default:** attend the first three, absorbed as a delivery cost, never billed separately.

---

## Open, owned elsewhere

| Question | Owner | Where the answer comes from |
|---|---|---|
| The legal basis for every outreach type | Counsel | The re-scoped D5 brief |
| Competitor weaknesses, booth costs, site reads, slot 1 coverage, job postings, universe size | Researcher | `reference/research-gaps.md` |
| Burn and runway | Founder | Not recorded anywhere yet. Phases 8 and 9 assumed a business that cannot buy evidence |
| Which tools the team runs, for adapters | Founder | `ops/gap-interview.md` |
| Domain name | Founder | Not chosen |
