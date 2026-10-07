# Handoff to Claude Design

What to upload, in what order, and what to watch for. The prompt itself is a
separate file, `brand/CLAUDE-DESIGN-PROMPT.md`, so it can be pasted without
being edited around.

**Read this first.** I still do not have documentation for Claude Design's
upload specification and I am not going to invent one. What follows is ordered
by what a design tool generally needs, and anything marked **inferred** is a
best read rather than a known requirement. Verify those as you go. The part
that is not a guess is the content: the tokens, the type scale, the components
and the page structure are all exact, and they are all verified against a
rendered page rather than described from imagination.

## The single most important instruction

**This replaces a system, it does not extend one.** If a previous Warm Channel
system called Roster exists in the workspace, it is dark, near monochrome and
wrong for this audience. Merging the two produces a muddle: a dark canvas with
a paper accent, or a light page carrying a developer tool's amber. The prompt
says this explicitly at the top, in capitals, because it is the failure this
handoff is most likely to hit.

## Upload order

| # | File | Why it goes in this position |
|---|---|---|
| 1 | `brand/DESIGN.md` | The system of record. Everything else is an instance of it |
| 2 | `brand/fonts/` static TTFs | Uploaded before anything renders, or the preview falls back to a system serif and the whole thing looks wrong |
| 3 | `brand/reference-page.html` | The reference implementation. Real copy, real components |
| 4 | `brand/reference-page.png` | The rendered target, so there is something to compare against |
| 5 | `landing-page/PAGE-STRUCTURE.md` | The build order for the full page |
| 6 | `landing-page/TheWarmChannel_Landing_Page.md` | The copy, which is settled and not to be rewritten |
| 7 | `landing-page/roi-calculator.html` | The current calculator, which needs restyling into the system |

## Which font files

`brand/fonts/` holds 48 files: 16 faces in three formats each. Do not upload
all of them.

**Upload these eight static TTFs**, which is the most broadly accepted format
and covers every weight the system uses:

```
FolioSerifText-Regular.ttf      FolioSerifText-Italic.ttf
FolioSerifDisplay-Regular.ttf   FolioSerifDisplay-Italic.ttf
FolioSans-Regular.ttf           FolioSans-Medium.ttf
FolioSans-Semibold.ttf          FolioSans-Bold.ttf
```

**Inferred:** that Claude Design prefers static TTF over variable. If it
accepts variable fonts, prefer `FolioSerif-Regular-Variable.ttf` and
`FolioSans-Regular-Variable.ttf` instead, because the serif's optical size axis
is the reason that face was chosen and static cuts only approximate it at two
sizes.

For the eventual web build, use the `.woff2` files and `brand/fonts/fonts.css`,
which is already written and carries both traps as comments.

## The two traps, repeated because they will bite

1. **Folio Sans defaults to weight 100.** It inherits Public Sans's variable
   default. Any rule that sets the family without setting a weight renders
   hairline. This has already happened once during the build.
2. **Folio Serif has an optical size axis.** Leave `font-optical-sizing` at
   `auto`. Pinning `opsz` to a single value for the page discards the reason
   the face was chosen, and a 62px headline set at text optical size looks
   slack.

## What to check before accepting the result

A checklist, because these are the things that go wrong and each is visible in
a screenshot.

- [ ] Background is `#FBF9F5`, not white. Hold a white window next to it
- [ ] Nothing has a rounded corner, including the call to action
- [ ] No shadow, gradient, glass or glow anywhere
- [ ] Table columns of numbers align on their right edge exactly
- [ ] The hero figure is set in the sans, not the serif
- [ ] The hero figure does not use tabular figures. Check the gap after a comma
- [ ] Prose is around 65 characters a line, not full width
- [ ] Footnote markers and the call to action are the same blue
- [ ] Ranges use hyphens. No em dash or en dash appears anywhere
- [ ] At 390px wide there is no horizontal page scroll, and tables scroll
      inside their own container

## Where this is likely to go wrong

1. **It will want to add a hero image.** There is none and there is not going
   to be one. The brand promises no photograph of the table.
2. **It will want to make the tables into charts.** They are already the right
   form. The dataviz form heuristic says a seven row comparison is a table.
3. **It will want to round the corners and add a shadow to the calculator.**
   The calculator is a form inside a document.
4. **It will want to soften the refusals and the pre-launch answer.** Those are
   the proof substitute for a business with no case study, and they carry the
   page.
5. **It will want a navigation bar.** One page, one action.

## After it builds

The output goes back into this repo, not into a separate place. Replace
`brand/reference-page.html`, and add the full page beside it. Re-run
`python3 tools/lint_claims.py` if any copy changed, which it should not have.
