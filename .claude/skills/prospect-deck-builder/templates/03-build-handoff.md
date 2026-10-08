# [Deck title], build handoff

File 3 of 3. Two build paths from the same files. `render_spec.py` writes this file, with the paste block filled in from deck.json.

## Path 1, Claude Code, the default

```bash
source ./paths.env
python3 "$DECK_SKILL/scripts/build_deck.py" deck/deck.json deck/brand.json --out build/[slug]_strategy_v1_send.html
python3 "$DECK_SKILL/scripts/build_deck.py" deck/deck.json deck/brand.json --out build/[slug]_strategy_v1_present.html --audience present
python3 "$DECK_SKILL/scripts/deck_check.py" build/[slug]_strategy_v1_send.html --deck deck/deck.json --register evidence/evidence-register.md --design spec/02-design-concepts.md --brand deck/brand.json
python3 "$DECK_SKILL/scripts/screenshot.py" build/[slug]_strategy_v1_send.html --out build/shots --pdf build/[slug]_strategy_v1.pdf
```

## Path 2, Claude Design

Paste the block below with File 1, File 2, the brand kit, the font files and the logo attached.

```
Build an interactive HTML walkthrough for [Company]: [title].
[Two sentences: what it is and for whom.]

USE YOUR NATIVE DESIGN SYSTEM for components, spacing and the type scale. Colour comes
ONLY from the semantic roles in File 2, mapped onto the prospect's palette in the brand
kit. Map each role once and hold it. Use the substitute typefaces the brand kit names.
The prospect's mark appears only in the Prepared for line and the top bar.

STRUCTURE, three levels: [home layer, decks, slide].

BUILD ORDER: shell and navigation against placeholder decks, one vertical slice (deck A),
the remaining decks, the home layer, then print and reduced motion.

NAVIGATION CONTRACT, in full: [from reference/navigation-contract.md]

NON-NEGOTIABLES: real 3D with no libraries, on the motif only; one self-contained file,
no request of any kind; alive at rest only where File 2 says; one easing curve; tabular
figures; reduced motion first class; print path mandatory; projector safe; the calculator
opens empty; every {TBD} stays {TBD}.

THE MOTIF: [one line]
THE REGISTER: [one line]
CENTREPIECES: [table]
HOOKS, so the build can be checked by deck_check.py: [from reference/claude-design-handoff.md]

SCAFFOLD FIRST: return the shell, the chrome, the working navigation and your role
mapping for approval before any slide content.
```

### Note to whoever runs the handoff

- **Attach:** File 1, File 2, the brand kit, the fonts and the logo. Nothing else.
- **Approve first:** the role mapping and the navigation, then the deck A slice.
- **Most likely to get lost:** the two actions at the end of every deck, the send build without notes, the empty calculator, the {TBD} marks, the print path, and any network request.
