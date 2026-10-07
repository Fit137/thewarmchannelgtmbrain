# {{PROJECT}} GTM, agent entry point

Cross-tool entry file. Codex, Cursor, Zed, opencode, and most newer agents read `AGENTS.md`, so this is the widest door into this brain. Kept identical in intent to `CLAUDE.md`. If the two differ, `CLAUDE.md` wins.

Working in a tool that reads neither, or in a chat window with no file access? See `adapters/`.

## Start here
1. `context/{{PROJECT}}_GTM_Master_Context.md`, the full go-to-market. Source of truth.
2. `rules/writing-rules.md`, house writing rules.
3. `rules/do-not-say.md`, claim hygiene and safe replacements.
4. `rules/feature-status.md`, shipped versus in build.
5. `reference/{{CHANNEL_ENGINE_FILE}}`, load this for any {{PRIMARY_CHANNEL}} task.

## Channel discipline
{{CHANNELS_IN_SENTENCE}} {{CHANNELS_OUT_SENTENCE}}

## Audiences, never blended
{{AUDIENCE_LIST}}

## Non-negotiables
{{NON_NEGOTIABLES}}

## Before shipping
Run `ops/QA-checklist.md`.

## Compounding
New market input goes to `ops/signal-log.md`. Rule changes follow the amendment procedure: ledger, master context, decision log, then copy.
