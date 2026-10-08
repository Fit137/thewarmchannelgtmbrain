# Evidence register, PX-0000, Acme Example Co.

FICTIONAL. Acme Example Co. does not exist. Every P row below is invented to show the shape of a real register, and every source address uses the reserved `.example` domain. The M rows are real and copied from the brain's evidence ledger.

Every claim in the strategy and every figure in the deck traces to one row here. Kinds:

- **P0**, supplied by the prospect, on a call or in a document they sent. UPGRADE mode only. Shown back only to them.
- **P1**, the prospect's own public statement: their site, case studies, press releases, job posts, event pages.
- **P2**, a third party's public record about the prospect: an exhibitor list, a sponsor page, an agenda, press coverage.
- **P3**, our inference from P1 and P2, with its basis written out. Never a number, never stated as fact on screen.
- **M-A, M-B**, a market figure from the brain's ledger, cleared for client assets. Cite the ledger row.
- **M-C**, a grade C market figure. Internal planning only. Never in the deck.
- **NEW**, a market figure found during research that is not in the ledger. Goes to the brain's `ops/signal-log.md` for grading. Never used until the ledger carries it.

captured: 2026-10-07

| ID | Kind | Claim or figure | Source | Captured | Basis or grade | Used in |
|---|---|---|---|---|---|---|
| E01 | P1 | Acme sells identity security software to large regulated enterprises | https://acme.example/about | 2026-10-05 | Their own description | 01, B |
| E02 | P1 | Acme's case studies name the CISO and the head of identity as the people who chose it | https://acme.example/customers | 2026-10-05 | Four of five case studies | 03, B2 |
| E03 | P2 | Acme exhibits at SecureCon, fourth week of April | https://securecon.example/exhibitors | 2026-10-05 | Exhibitor list, 2026 edition | 02, A2, A3, C2 |
| E04 | P2 | Acme sponsors Identity Summit, second week of June | https://identitysummit.example/sponsors | 2026-10-05 | Sponsor page | 02, A2, C2 |
| E05 | P1 | Acme Connect, Acme's own customer conference, second week of October | https://acme.example/connect | 2026-10-05 | Event page | 02, A2, C2 |
| E06 | P2 | Acme sponsors two Security Forum breakfasts, February and November | https://securityforum.example/events | 2026-10-05 | Sponsor credits on two event pages | 02, A2, C2 |
| E07 | P1 | A partner roadshow in September, co-hosted with resellers | https://acme.example/partners/roadshow | 2026-10-05 | Partner page | 02, A2 |
| E08 | P1 | A field marketing role is measured on pipeline from named accounts | https://acme.example/careers/field-marketing | 2026-10-05 | Job post wording: "pipeline from our named accounts" | 00, 01 |
| E09 | P3 | Acme's deals are six figures | https://acme.example/customers | 2026-10-05 | Inference: case studies describe enterprise-wide rollouts across tens of thousands of identities, and the pricing page offers contact-sales tiers only. Confirm on the call | 00, 01 |
| E10 | P3 | Tier 1 accounts cluster in three metros, and architects and risk leads sit on the buying committee | https://acme.example/customers | 2026-10-05 | Inference: named customers' headquarters concentrate in three metros, and two case studies quote an architect and a risk lead | 03, 05, B2, C3 |
| E11 | P1 | Machine identity governance is Acme's current public priority | https://acme.example/blog | 2026-10-05 | Last four blog posts | 01, 06 |
| E12 | P2 | Competitor A runs an annual customer conference and a SecureCon booth | https://securecon.example/exhibitors | 2026-10-05 | Exhibitor list, fictional | 04 |
| E13 | P2 | Competitor B hosts a sponsored reception at Identity Summit | https://identitysummit.example/sponsors | 2026-10-05 | Sponsor page, fictional | 04 |
| E14 | P2 | Identity Summit 2026 lists three sessions on machine identity governance | https://identitysummit.example/agenda | 2026-10-05 | The question is live in the sector | 06, C6 |
| E15 | P2 | Incident recovery recurs as a session theme in the sector's 2026 conference programmes | https://securecon.example/agenda | 2026-10-05 | Two programmes, fictional | 06, C6 |
| E16 | M-B | Invite-only executive dinners attend at 70% of registered. 13,155 registrations, 191 events | Clutch Events, ledger row 11 | 2026-10-07 | B plus | 07, A4, D2 |
| E17 | M-B | VIP and sport events 86%, vendor-owned conferences 19% | Clutch Events, ledger row 12 | 2026-10-07 | B plus | 07, A4, D2 |
| E18 | M-B | Trade show exhibiting is 40.8% of exhibitor marketing budgets | CEIR 2026, ledger row new | 2026-10-07 | B | 08, E2 |
| E19 | M-B | Trade show cost per lead $112 to $300 per badge scan | CEIR, ledger row 5 | 2026-10-07 | B | 08, E3 |

## Not used, and why

| ID | Kind | Claim or figure | Why it is out |
|---|---|---|---|
| X01 | M-C | Dinner attendees convert to opportunities at 30% to 50% | Grade C, ledger row 32. Never as ours, never in a deck |
| X02 | NEW | A vendor survey putting identity budgets up a fifth year on year | Not in the ledger. Logged to the brain's signal log for grading, not used |
