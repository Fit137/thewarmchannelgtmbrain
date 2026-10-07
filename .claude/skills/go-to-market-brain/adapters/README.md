# Adapters

Pointer files that make GTM Brain load in agent tools other than Claude Code.

Nothing here is content. Each file is a few lines that tell one tool where to look and
when to look there. The method stays in `SKILL.md` and the brain stays in its own repo,
so there is one copy of the truth and many doors into it.

Two families:

| Folder | Points at | Rendered by |
|---|---|---|
| `skill/` | This skill, so a tool can run BUILD, UPDATE, and OPERATE | `install.sh --codex --cursor --windsurf --copilot --gemini` , or by hand |
| `brain/` | A built brain, so a tool loads its control layer before writing | Phase 7 of a build, see `reference/portability.md` |

## Placeholders

`skill/` files use:

| Token | Means | Typical value |
|---|---|---|
| `{{SKILLS_DIR}}` | Where the skills were installed | `.claude/skills` |
| `{{SKILL_PATH}}` | This skill's directory | `.claude/skills/go-to-market-brain` |
| `{{SKILL_ABS}}` | The same directory, absolute | `/home/you/project/.claude/skills/go-to-market-brain` |

Use `{{SKILL_ABS}}` in any file that lands outside the project, such as the Codex prompt
directory, where a project-relative path would resolve against whatever directory the tool
happens to be started in.

`brain/` files use `{{PROJECT}}`, `{{BRAIN_PATH}}`, `{{PRIMARY_CHANNEL}}`, `{{AUDIENCE_LIST}}`,
and `{{NON_NEGOTIABLES}}`, filled from the brain being built.

Render one by substitution:

```bash
sed -e 's|{{SKILL_PATH}}|.claude/skills/go-to-market-brain|g' \
    -e 's|{{SKILLS_DIR}}|.claude/skills|g' \
    adapters/skill/cursor.mdc > .cursor/rules/go-to-market-brain.mdc
```

A file left with an unfilled `{{TOKEN}}` in it is a bug. `scripts/audit_brain.py` fails a
brain that ships one.

## Block markers

Files named `*.block.md` are meant to be merged into a file the project already has, not to
replace it. They carry markers:

```
<!-- gtm-brain:begin -->
...
<!-- gtm-brain:end -->
```

Replace whatever sits between the markers on an update, and append the block if the markers
are absent. `install.sh` does this. Do the same by hand and re-running stays safe.

## Adding a tool

Copy the closest file, change the path convention and the frontmatter, keep it under about
twenty lines, and open a pull request. The recipe belongs in `PORTING.md` at the repo root
in the same change, so the human-facing guide and the template ship together.
