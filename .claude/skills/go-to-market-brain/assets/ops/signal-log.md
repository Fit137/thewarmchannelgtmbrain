# Signal log

Raw market input, captured before judgment. Every signal from a lead, prospect, customer, competitor, or channel lands here first, whatever it turns out to mean. Newest at the top.

Capture is cheap on purpose. A signal that gets debated before it gets written down does not get written down.

**Keep the verbatim.** Do not paraphrase a customer into house vocabulary. The language a real buyer used before we taught them ours is the most valuable thing a signal carries, and it cannot be recovered later.

## How to use this file

**Types:** OBJECTION, LANGUAGE, PROOF, STATUS, COMPETITIVE, SEGMENT, CHANNEL, LOSS, RISK.

**Dispositions:**
- `NOISE`, one instance, no pattern, no action. Logged and closed.
- `WATCH (n/N)`, a plausible pattern awaiting corroboration. Increment as instances arrive.
- `PATCH`, changes copy but not strategy. Route it, edit, done. No decision entry.
- `AMEND`, changes a ledger, a position, or a rule. Follow the full amendment procedure and write a `decisions.md` entry.

**Corroboration thresholds** (agreed {{DATE}}, see `review-cadence.md`):

| Signal class | Threshold to act |
|---|---|
| Opinion, preference, language, objection | {{3}} independent instances within {{60}} days |
| Verifiable fact: status, proof, competitive, risk | 1 verified instance, act immediately |
| Loss reason | {{2}} instances, or 1 if the deal was in the core ICP |
| Channel performance | A full measurement cycle, never a single week |

Default disposition is NOISE. A brain that amends on every input has no memory, and one that flip-flops on the last conversation is worse than a static document.

Triage runs {{weekly, day}}. A WATCH item that has not incremented in two cycles expires to NOISE, and the expiry is written in the log.

---

## Entries

### {{YYYY-MM-DD}} | {{TYPE}} | {{source: sales call, support ticket, review, community thread, competitor site, analytics}}
**Verbatim:** "{{what was actually said or observed, in their words}}"
**Context:** {{who, which funnel stage, which segment, which channel}}
**Disposition:** {{NOISE | WATCH (1/3) | PATCH | AMEND}}
**Routed to:** {{file changed, or "none"}}

---

*Seed this file on day one. An empty signal log after a month of selling means the loop is not running.*
