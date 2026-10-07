---
name: go-to-market-brain
description: Turn a go-to-market into a Go-to-Market Brain, a governed context repository that any AI agent or human operator loads as the single source of truth for strategy, messaging, claims, and voice. Use this skill when the user has GTM dashboards, strategy decks, positioning docs, ICP research, competitive analysis, value proposition frameworks, customer journey maps, or a campaign plan and wants them turned into a repo, a context repo, a GTM brain, a command center, a brand or messaging source of truth, or agent guardrails. Also use it to operate an existing brain: logging a signal from a lead, prospect, customer call, churn reason, review, or competitor move and deciding whether it changes positioning, ICP, messaging, or the claim ledger; capturing a periodic snapshot; updating a feature or claim status; or auditing a brain for staleness and broken guardrails. Also use it to wire a brain, or this procedure, into another agent tool: Codex, Cursor, Windsurf, Copilot, Gemini, Grok, a custom GPT, or a chat window with no file access. Triggers include "GTM brain", "go-to-market repo", "context repo", "single source of truth for our messaging", "turn these dashboards into a repo", "rules so the AI stops overclaiming", "did this change our positioning", "log this customer signal", "make this work in Codex", "port the brain to another agent".
---

# Go-to-Market Brain

A Go-to-Market Brain is a plain-text repository that holds one company's entire go-to-market in a form an AI agent can load and execute against without re-deriving anything, and that a human operator can use as a command center for decisions. It is content and context, not application code.

It solves four problems at once. Strategy stops living in one person's head and in scattered files. Every asset inherits the same positioning and voice. Agents stop overclaiming, because what may be said is written down and checked. And the whole thing compounds: every lead conversation, customer signal, and periodic snapshot feeds back into the ledgers, so the brain gets sharper with use instead of going stale.

## Route first

Three modes. Decide which one you are in before doing anything.

| The user has | Mode | Go to |
|---|---|---|
| Source material and no brain yet | **BUILD** | Phases 1 to 9 below |
| A brain, plus new input: a call note, an objection, a churn reason, a competitor move, a shipped feature, a metrics snapshot | **UPDATE** | `reference/compounding.md` |
| A brain, and wants an asset produced, reviewed, or shipped | **OPERATE** | `reference/operating.md` |

If a brain exists, never write customer-facing output without loading its entry file and control layer first. That is the point of the brain.

## The three-layer architecture

Everything in the build serves one of three layers. Keep them distinct.

1. **Control layer.** Small, authoritative, checked on every task: the entry files, the rules, the QA checklist. This is what governs output. Keep it short enough that loading it costs nothing.
2. **Reference layer.** Large, authoritative, loaded on demand: the master context and one file per source artifact. This is the brain's memory.
3. **Execution layer.** Templates, examples, prompts, finished pages. This is how work gets produced fast and on-voice.

Under all three sits the **state layer** (`ops/` and `snapshots/`), which records what was decided, what language is approved, what has been heard from the market, and when each ledger was last reviewed. The state layer is what makes the brain compound.

Full file map, purposes, and size budgets: `reference/blueprint.md`.

## BUILD: nine phases

Work in order. Do not skip Phase 2, and do not start Phase 4 before Phase 3 is drafted.

### Phase 1. Inventory the sources
Run `scripts/extract_sources.py <source_dir> <out_dir>` to convert XLSX, DOCX, PPTX, PDF, and CSV into readable Markdown. Read every extract. Then write a source manifest: for each artifact, its name, type, what decision it settles, and its date. Flag any two artifacts that disagree, and resolve the conflict explicitly with the user rather than silently picking one.

Method and the source-to-file mapping table: `reference/extraction.md`.

### Phase 2. Interview for gaps
The sources will not carry everything. Ask only for what is missing, in one batched round, and prefer questions whose answers change the build. The standing gap list is in `reference/extraction.md`. The four that are almost always missing: the channel mix and which channels are forbidden, the exact permissioned proof points, feature or delivery status by capability, and the words this brand refuses to use.

If the user cannot answer something, record it as an open question in `ops/decisions.md` under "Open, owned elsewhere" rather than inventing an answer. An invented answer becomes a rule, and a wrong rule propagates into every asset.

### Phase 3. Draft the master context
One file, `context/<Project>_GTM_Master_Context.md`, that distills every source into a single read. Numbered sections, YAML frontmatter carrying version, last updated, and status notes, and Section 0 written as operating instructions to the agent reading it.

Target 300 to 500 lines. If it runs longer, you are transcribing instead of distilling. Section order and the frontmatter contract: `reference/blueprint.md`. Skeleton: `assets/context/master-context.md`.

### Phase 4. Derive the control layer
Lift the governing parts of the master context out into standalone files under `rules/`. This duplication is deliberate: the master is the reference brain, the rules are the layer that gets checked on every single task. The master stays authoritative when they diverge, and both get updated together.

Derive in this order, because each depends on the last:
1. `rules/glossary.md`, the canonical vocabulary. Names first, since every other rule refers to things by name.
2. `rules/feature-status.md`, what is shipped versus in build versus roadmap. Rename it to fit the business: a services firm ships capabilities, not features.
3. `rules/do-not-say.md`, the claim hygiene spine. Two columns: forbidden or risky on the left, the safe replacement on the right. Never a bare prohibition without a replacement.
4. `rules/writing-rules.md`, mechanics, tone, channel discipline, and the approved signature lines.
5. `ops/QA-checklist.md`, which is the mechanical, tickable mirror of the four files above. If a rule cannot be checked, it is not a rule yet.

Derivation method, including how to turn a competitive claim into a scoped safe form: `reference/ledgers.md`.

### Phase 5. Build the reference layer
One short file in `reference/` per source artifact, each opening with a line naming the source it distills and what to load it for. Then add the synthesized files the sources imply but do not contain, typically battlecards, objection handling, and a channel engine for whatever the primary channel is.

Each file earns its place by answering a question an operator actually asks. Sixty lines is usually enough. If a reference file is only a restatement of the master context, cut it.

### Phase 6. Build the execution layer
Instantiate a template per channel in the mix, and only those. A template the business will never use is noise that dilutes retrieval. Start from `assets/templates/`, then rewrite each one in the project's own vocabulary and guardrails.

Write at least one gold-standard example per major asset type into `examples/`. Examples are the few-shot voice reference and they do more work than any amount of tone description. If no approved asset exists yet, write one and get it approved before the brain is declared built.

Fill `prompts/common-tasks.md` with a filled, ready-to-run prompt per recurring job.

### Phase 7. Build the routers, and the doors for other tools
Three entry files, all small, all pointing at the same load order, all restating the non-negotiables in short form: `CLAUDE.md`, `AGENTS.md` (for Codex, Cursor, Zed, opencode, and the rest of the tools that read AGENTS.md), and `llms.txt` (a linked index of every file). Add `README.md` for humans: what this is, how it is organized, what it is for, and the maintenance rule.

Keep each router under about sixty lines. The always-loaded layer must stay small and authoritative. Everything else is pulled in on demand.

Then ask which tools the team actually runs, and write one pointer file per tool into `adapters/`, from the templates in `adapters/brain/`. A guardrail that loads in one tool and not the others is not a guardrail: the person on the tool you skipped ships copy nothing checked. For anyone working in a chat window with no file access, render the dated portable control layer. Method, the tool table, and how to keep adapters from drifting: `reference/portability.md`.

### Phase 8. Install the compounding loop
This is what separates a brain from a folder of documents. Create `ops/signal-log.md`, `ops/decisions.md`, `ops/copy-bank.md`, `ops/asset-index.md`, `ops/review-cadence.md`, and the `snapshots/` directory. Seed the decision log with every strategic call the sources already settled, each with its date, verdict, and rationale, so settled strategy is never relitigated.

Set the review cadence and the corroboration thresholds with the user. Full protocol: `reference/compounding.md`.

### Phase 9. Audit and hand off
Run `scripts/audit_brain.py <brain_dir>`. It checks required files, broken relative links, files missing from the index, size budgets, banned words and forbidden mechanics inside the brain's own prose, and ledger staleness.

Then run a live test: produce one real asset using only the brain, and run it through `ops/QA-checklist.md`. If the asset needed a fact that is not in the brain, the brain is not finished. Fix it, then hand off.

## Invariants

These hold for every brain, regardless of company, category, or channel mix.

- **Ledgers before copy, always.** When status changes, update the ledger, then let copy follow. Never the other way around.
- **Every capability carries a status flag.** Shipped, partial, in build, or roadmap. No claim about an unshipped capability without the flag attached.
- **Every prohibition carries a replacement.** A do-not-say entry without a "say instead" gets ignored under deadline pressure.
- **Audience before writing.** If the business has more than one audience, they get separate value propositions and are never blended in one asset. Pick first.
- **Proof points are a closed set.** Only real, permissioned, sourced facts. The brain names them explicitly, and anything not on the list is fabrication.
- **Scope every superlative.** "Only," "first," "best," and "never" get checked against the claim ledger and narrowed to the form that survives scrutiny.
- **Name the mode when a claim is conditional.** If a claim is true in one configuration and false in another, the mode is part of the claim.
- **Channel discipline is a rule, not a preference.** If the GTM excludes a channel, the brain refuses to produce for it and says so.
- **The always-loaded layer stays small.** Routers and rules are short. Depth lives in files loaded on demand.
- **The brain is tool-neutral.** It is Markdown. Any agent that can read a file can be pointed at it, and the guardrails reach every tool the team runs, not just the one that built the brain.
- **Decisions are dated and never relitigated.** Including an explicit note of what the decision did not change.

## Files in this skill

| File | Load it when |
|---|---|
| `reference/blueprint.md` | Building or extending the file structure. Full map, purposes, load policy, size budgets. |
| `reference/extraction.md` | Phase 1 and 2. Reading source material, mapping artifacts to files, the gap interview. |
| `reference/ledgers.md` | Phase 4. Deriving glossary, status ledger, claim ledger, writing rules, QA checklist. |
| `reference/compounding.md` | UPDATE mode. Signal intake, triage, routing, snapshots, review cadence. |
| `reference/operating.md` | OPERATE mode. Producing, checking, and shipping an asset against a built brain. |
| `reference/portability.md` | Phase 7. Making the brain load in every tool the team runs, not only this one. |
| `reference/worked-example.md` | Any phase, for a real instance of the blueprint end to end. |
| `assets/` | Phase 3 to 8. Skeletons to copy and rewrite in the project's own terms. |
| `adapters/` | Phase 7. Pointer templates per tool, for the brain and for this skill. |
| `scripts/extract_sources.py` | Phase 1. Converts XLSX, DOCX, PPTX, PDF, CSV to Markdown. |
| `scripts/audit_brain.py` | Phase 9 and every review cycle. Lints a built brain. |
| `scripts/bundle_skill.py` | When a tool cannot read files. Flattens this skill into one pasteable document. |

## If you are not running in Claude Code

Nothing here is Claude-specific. You are reading Markdown, and every path above is relative to this skill's own directory, so the procedure works wherever these files landed. Two adjustments:

- **You cannot open a file.** Everything you need is in the bundle you were given. Where the text says to open `reference/x.md`, look for that path as a section heading in the same document. Where it names a script, do the work the script describes by hand and say that you did.
- **Someone wants this wired into their tool.** Use the pointer templates in `adapters/skill/`, substituting the real install path for `{{SKILL_PATH}}` and `{{SKILLS_DIR}}`. The per-tool recipes, and the five-prompt check that proves the wiring works, are in `PORTING.md` at the root of the GTM Brain repository.

Templates are starting points, never final output. A brain that reads like a filled-in template is a brain nobody trusts. Rewrite every line in the project's own vocabulary, and delete every section the project does not need.
