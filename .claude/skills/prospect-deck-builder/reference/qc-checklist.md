# QC checklist

Load for: the check phase, every time, before anything is sent. Run it on the **send** build.

A script can prove the file is contained, consistent and clean. It cannot tell you whether a claim is true, whether a slide lands, or whether the prospect will feel respected. Both halves are required.

## 1. Automated

```bash
source ./paths.env
python3 "$DECK_SKILL/scripts/deck_check.py" build/[slug]_strategy_v1_send.html --deck deck/deck.json \
  --register evidence/evidence-register.md --design spec/02-design-concepts.md --brand deck/brand.json
python3 "$DECK_SKILL/scripts/contrast.py" deck/brand.json
python3 "$DECK_SKILL/scripts/screenshot.py" build/[slug]_strategy_v1_send.html --out build/shots --pdf build/[slug]_strategy_v1.pdf
```

| Check | Pass |
|---|---|
| deck_check.py | 0 errors. Every warning read, and either fixed or answered in writing in the log |
| contrast.py | Every pair passes. TIGHT pairs reviewed on the dimmest screen available |
| screenshot.py | Every slide shot exists, the PDF's page count is the home pages plus one per slide |
| The brain's `scripts/lint_claims.py` on the spec folder | 0 errors |
| The strategy's `validate_strategy.py` | Ran clean at the handoff, and nothing in strategy.json changed since |

What deck_check.py covers: no network load, no tracking parameter, no form or frame, a noindex tag; no dash, banned word, placeholder, evidence ID or scaffold marker; retired scope names, network, proof and price claims, frozen D11 lines, unscoped superlatives, Commonwealth spelling; client words in guest copy; the 70% and reply-rate collision; every percentage and money figure traced to the cleared ledger, the register or declared provenance, with the sentence sharing words with its source; capabilities that are not READY carrying their status; covers, closes with two actions, titles, alt text, chart names, paragraph length; notes absent from the send build and timed in the present build; centrepieces, the still slide and motif count; and no hex value or typeface name in the design concepts file.

## 2. By eye, on the screenshots

- [ ] The contact sheet reads as one file: the same register, the same roles, nothing that looks borrowed.
- [ ] Every slide's hero is the thing the eye lands on first.
- [ ] No text touches an edge, overlaps another element, or wraps a single word onto a line of its own.
- [ ] Every `{TBD}` is visible and reads as an invitation to fill in, not as an error.
- [ ] The quadrant's positions match the strategy's scores, and the anchor is where the title says.
- [ ] The rebuilt year keeps every moment the plan keeps.
- [ ] The prospect's mark appears only in the Prepared for line and the top bar, unaltered.

## 3. By hand, in a browser

- [ ] **Keyboard only:** open the file, Tab to Start, walk every deck with the arrows, use 1 to 9, Esc home, S, M, ?, and reach the call to action. Nothing needs a mouse.
- [ ] **The end of every deck** shows two actions, and both work.
- [ ] **Back:** enter a deck, move three slides, press the browser's Back: it leaves the deck.
- [ ] **Deep link:** paste `#/c/5` into a fresh tab: it opens there.
- [ ] **The arithmetic:** move the slider and switch the format: confirmations change instantly, rounded.
- [ ] **The calculator:** nothing shows until four fields hold numbers; a bad case says so in words and turns to the flag role; typing never turns the slide.
- [ ] **Reduced motion:** with the system setting on, or M, every slide arrives resolved.
- [ ] **Phone:** the home layer reads alone at phone width with no sideways scroll; a deck asks to be turned sideways and works when it is.
- [ ] **Print preview:** the home layer, then one slide per page, nothing cut off.
- [ ] **Screen reader smoke test:** the live region announces the deck, slide and title on each change.
- [ ] **Offline:** with the network off, the file still opens with its fonts and its mark.

## 4. The content, against the brain

- [ ] The brain's `ops/QA-checklist.md`, client asset blocks, run against File 1 of the spec.
- [ ] Every market figure in the deck is in the claim envelope's cleared table, with its source on the slide or in the notes.
- [ ] No reply rate anywhere, screen or notes, because the 70% figure is in the deck.
- [ ] Every capability that is not READY carries its status in the same sentence or on its step.
- [ ] After the evening appears only in the consent framing, with no mechanism.
- [ ] No price, no guarantee, no network, no client, no result, no founder attendance promised.
- [ ] Before you present names things individually, and the founder has read it.

## 5. The file you send

- [ ] It is the send build: its build comment says "Audience: send", and N says the copy has no notes.
- [ ] The call to action address is real, and carries no tracking parameter.
- [ ] The filename says the company, "strategy", the version and nothing internal: `[slug]_strategy_v1.html` or `.pdf`.
