# Portability, making a brain every agent can read

Load this in Phase 7, and again whenever someone on the team shows up running a different tool.

A brain outlives the tool that built it. The operator who commissions it runs Claude Code, the
engineer who edits the product strings runs Codex, the founder rewrites the landing page in a
chat window with Grok or ChatGPT open, and the agency uses Cursor. If the guardrails only load
in one of those, the other three ship copy the brain would have refused. That is the failure this
file prevents.

## The rule that keeps it sane

**One copy of the truth, many doors into it.** The brain is the truth. Everything a tool reads is
a pointer file of about twenty lines that says where to look and when. No adapter ever restates
strategy, a claim, or a status. The moment an adapter carries content, it starts drifting, and a
stale guardrail is worse than none because it still carries authority.

The one deliberate exception is the portable control layer, below. It carries content because a
chat model cannot follow a pointer, and it is dated and regenerated for exactly that reason.

## What every brain ships

Three routers plus the index, built in Phase 7 and non-negotiable:

- `CLAUDE.md`, for Claude Code and the Claude apps.
- `AGENTS.md`, read by Codex, Cursor, Zed, Jules, opencode, and most newer tools. Widest reach of
  the three, so keep it complete rather than thin.
- `llms.txt`, the linked index. An agent reads it to decide what to open without opening anything.
- `README.md`, for people.

`CLAUDE.md` wins if the routers ever disagree, and `AGENTS.md` says so in a line.

## Adapters, one per tool in use

Add these only for tools someone actually runs. An adapter for a tool nobody uses is a file that
goes stale unnoticed. Templates are in `adapters/brain/`, and each takes `{{PROJECT}}`,
`{{BRAIN_PATH}}`, `{{PRIMARY_CHANNEL}}`, `{{AUDIENCE_LIST}}`, and `{{NON_NEGOTIABLES}}`.

| Tool | Write | From |
|---|---|---|
| Codex, Zed, Jules, opencode | `AGENTS.md` in the consuming repo | `adapters/brain/AGENTS.block.md` |
| Cursor | `.cursor/rules/<project>-gtm.mdc` | `adapters/brain/cursor.mdc` |
| Windsurf | `.windsurf/rules/<project>-gtm.md` | `adapters/brain/windsurf.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `adapters/brain/copilot-instructions.block.md` |
| Gemini CLI | `GEMINI.md` | `adapters/brain/GEMINI.block.md` |
| Any chat model, no file access | `adapters/portable-control-layer.md` | `adapters/brain/system-prompt.md` |

The brain repository holds the rendered adapters in its own `adapters/` folder. A consuming
repository, the product codebase for instance, gets the pointer file copied into it, aimed at
wherever the brain is checked out.

Files ending `.block.md` merge into a file the project already has. Keep the markers:

```
<!-- gtm-brain:begin -->
<!-- gtm-brain:end -->
```

Replace what sits between them on an update, append the block when they are absent, and never
edit inside them by hand.

## The portable control layer

For anyone working in a chat window, render `adapters/brain/system-prompt.md` into a filled file
under `adapters/`. It carries the audiences, positioning, status summary, proof points, the
do-not-say table, the channel list, and the writing rules. That is enough to keep a draft inside
the guardrails without any file access.

It carries content, so it decays. Three rules keep it honest:

1. It is dated in its own header.
2. It regenerates whenever a ledger changes, as the last step of the amendment procedure, after
   the ledger, the master context, and the decision log.
3. It is listed in `ops/asset-index.md` and named in `ops/review-cadence.md`, so a review catches
   it when nobody remembered to regenerate it.

## Wiring it in

Add to `ops/asset-index.md`: every adapter, where it is installed, and who runs that tool. Add to
`ops/review-cadence.md`: a line that adapters are checked on the same cycle as the ledgers. Add to
`llms.txt`: one line per adapter, so the set stays visible.

The amendment procedure gains a final step. Ledger, then master context, then decision log, then
copy, then the portable control layer. Adapters that are pointers need nothing, which is the point
of keeping them pointers.

## Retrofitting the skill itself

Someone will want to run BUILD or UPDATE from a tool that has no skill system. That is a separate
question from the brain being readable, and the full set of recipes lives in `PORTING.md` at the
root of the GTM Brain repository, covering Codex, Cursor, Windsurf, Copilot, Gemini, Grok, custom
GPTs, agent frameworks, and plain chat. The short version: install the skill files anywhere, write
the pointer file that tool reads, and where there is no file access at all, generate a bundle with
`scripts/bundle_skill.py` and paste it in.

## Check it works

Do not assume an adapter loaded. In each tool someone runs, open a fresh session and ask for
something the brain forbids: copy for an excluded channel, a claim about a capability that is in
build, a metric that is not a proof point. Then ask for something it allows.

A tool that is wired in refuses the first, names the rule and the file it came from, and produces
the second in voice. A tool that produces both is not loading the brain, and the person using it
has been shipping unchecked copy. Fix the adapter, then check what already shipped.
