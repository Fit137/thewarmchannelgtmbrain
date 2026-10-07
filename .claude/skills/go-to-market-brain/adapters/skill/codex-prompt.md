Run the Go-to-Market Brain procedure.

Read `{{SKILL_ABS}}/SKILL.md` and follow it exactly. If that path does not exist on this machine,
look for `go-to-market-brain/SKILL.md` under `.claude/skills`, `.agents/skills`, or whatever this
repository's `AGENTS.md` points at, and read that instead.

Route first: BUILD if there is source material and no brain, UPDATE if a brain exists and there is
new market input, OPERATE if a brain exists and an asset is wanted. Open the reference file
SKILL.md names for that mode when you reach it, not before.

The request: $ARGUMENTS

If the request is empty, look for GTM source material in this directory, say which mode you would
run and why, and ask for the one thing you most need before starting.
