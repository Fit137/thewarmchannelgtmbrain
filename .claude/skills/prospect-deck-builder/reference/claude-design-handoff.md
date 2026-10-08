# The Claude Design handoff

Load for: building a deck by hand in Claude Design instead of with build_deck.py.

The default build path is the engine: `build_deck.py` turns deck.json and brand.json into a tested, contained file in seconds, and every check in this skill is written against it. Use Claude Design only when a prospect warrants something the engine cannot do: a bespoke visual for one argument, a layout the seventeen do not cover, or a different hand for a very large account. The content, the design concepts and the rules stay exactly the same. Only the builder changes.

## What to hand over

`render_spec.py` writes all of it from deck.json and brand.json:

| File | Attach |
|---|---|
| `spec/01-content.md` | Yes. Every word, the hierarchy, the navigation table, the register, Before you present |
| `spec/02-design-concepts.md` | Yes. Semantic roles only, every slide's design block, the motif, centrepieces, restraint |
| `spec/03-build-handoff.md` | The paste block, pasted as the instruction |
| `spec/04-brand-kit.md` | Yes, with the font files and the logo file |
| Anything else | No. No other deck, no other company's material, no brain file |

## The order, and what to approve

1. **Scaffold first.** Before any slide content, Claude Design returns the shell, the overlay chrome, the working navigation against placeholder decks, and its mapping of the twelve roles onto the brand kit. Approve the mapping and the navigation here. Every slide inherits the mapping, and changing it later is a large revision.
2. **One vertical slice.** Deck A, complete, as the pattern for the rest.
3. **The remaining decks.**
4. **The home layer.**
5. **Print and reduced motion,** checked on every slide.

## Hooks, so the checker can verify a bespoke build

Ask the builder to keep the engine's structural hooks. With them, `deck_check.py` runs on the bespoke file exactly as on an engine build:

| Hook | Where |
|---|---|
| `<meta name="robots" content="noindex, nofollow, noarchive">` | The head |
| `<section class="deck" data-deck="a" data-name="...">` | Each deck |
| `<article class="slide layout-cover">` on slide 1, `layout-close` on the last | Each slide |
| `<div class="close-actions">` holding exactly two links | Each close |
| `<aside class="notes" data-seconds="20">` | Present build only |
| `data-audience="guest"` | The invitation card |
| `<sup class="ref">` | Source references |
| `<!-- ... Audience: send. ... -->` | A build comment naming the audience |

## What is most likely to get lost

| Lost | Check |
|---|---|
| A web font service link, a CDN library, an analytics snippet | deck_check.py containment. The file must make no request at all |
| The two actions at the end of every deck | deck_check.py structure, and by hand |
| Notes left in the send build | deck_check.py notes check, and N in the browser |
| A prefilled or example calculator | By hand: nothing shows until four fields are typed |
| `{TBD}` replaced with a plausible number | deck_check.py numbers, and by eye. A replaced unknown is an invented figure and comes out |
| Hover-only labels | By hand, and in print preview |
| The print path | Print preview: the home layer, then one slide per page |
| Reduced motion | With the system setting on, every slide resolved |
| A colour that is not one of the roles | By eye against the brand kit |

After the build, run the full `qc-checklist.md` on the exported file. A Claude Design build is held to the same bar as an engine build, with no exceptions for being bespoke.
