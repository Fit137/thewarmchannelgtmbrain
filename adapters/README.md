# Adapters

Doors into the brain for tools other than Claude Code. One copy of the truth, many doors. Nothing here restates strategy except the portable control layer, which carries content on purpose because a chat model cannot follow a pointer.

| File | For | How to use | Kept current by |
|---|---|---|---|
| `portable-control-layer.md` | Any tool with no file access: Gamma, Claude Design, ChatGPT, custom GPTs, API system prompts | Paste everything below its rule | Regenerated as the last step of every amendment. Dated. The audit fails it after 90 days |
| `AGENTS.block.md` | Any repository that holds customer-facing text, such as `warmchannelgtmbuild` or a future website repository | Merge between the `gtm-brain` markers into that repository's `AGENTS.md` or `CLAUDE.md`. Replace what sits between the markers on update, never edit inside them by hand | A pointer. Needs no regeneration unless a path changes |

`CLAUDE.md` and `AGENTS.md` at this repository's root serve Claude Code, Codex, Cursor, Zed, Jules and opencode directly.

## Adding a tool

Only add a door for a tool someone actually runs, Q7 in `ops/gap-interview.md`. An adapter for a tool nobody uses goes stale unnoticed. Templates for Cursor, Windsurf, Copilot and Gemini are in `.claude/skills/go-to-market-brain/adapters/brain/`. Render one by replacing the BRAIN_PATH token, written in double braces, with the brain's path from that repository, fill the audience list and non-negotiables from `CLAUDE.md`, and list the new door in `ops/asset-index.md`.

## Check that a door works

In a fresh session in the tool, ask for something the brain forbids: a paid ad, a guarantee of meetings, a testimonial, a guest invitation that mentions leads. Then ask for something it allows. A wired tool refuses the first, names the rule and the file, and produces the second in voice. A tool that produces both is not loading the brain.
