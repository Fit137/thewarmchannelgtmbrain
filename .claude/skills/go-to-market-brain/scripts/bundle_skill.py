#!/usr/bin/env python3
"""
Bundle a skill into one file, for any model that cannot read a directory.

Chat interfaces, custom GPTs, Grok, an API call's system parameter, and most agent
frameworks take text, not a file tree. This flattens the skill into a single document
with the load order preserved and the frontmatter stripped.

    python3 bundle_skill.py                            # compact bundle to stdout
    python3 bundle_skill.py --mode system-prompt       # trimmed, for a system parameter
    python3 bundle_skill.py --mode full --out gtm.md   # everything, for a large context
    python3 bundle_skill.py --list                     # what each mode would include

Modes, by what they cost and what they carry:

  system-prompt   SKILL.md plus the portable rules. Smallest. Use when the model has one
                  shot at the whole method and a modest context window.
  compact         system-prompt plus the reference files. The default. Fits comfortably in
                  a 100k window and carries the real procedure.
  full            Everything including asset skeletons and the worked example. Use with a
                  long context window, or when the model will be asked to build.

Exit codes: 0 ok, 2 bad usage. No third-party dependencies.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

try:  # so `bundle_skill.py --list | head` closes quietly instead of tracing back
    from signal import SIG_DFL, SIGPIPE, signal
    signal(SIGPIPE, SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

HERE = Path(__file__).resolve().parent
DEFAULT_SKILL = HERE.parent

# Order matters. An agent reading top to bottom should meet the procedure before the detail.
LAYERS = {
    "system-prompt": [
        "SKILL.md",
        "adapters/skill/system-prompt.md",
    ],
    "compact": [
        "SKILL.md",
        "reference/blueprint.md",
        "reference/extraction.md",
        "reference/ledgers.md",
        "reference/compounding.md",
        "reference/operating.md",
        "reference/portability.md",
        "adapters/skill/system-prompt.md",
    ],
    "full": [
        "SKILL.md",
        "reference/*.md",
        "adapters/skill/system-prompt.md",
        "adapters/**/*.md",
        "assets/**/*.md",
        "assets/entry/llms.txt",
    ],
}

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)

# A file may carry a header that only makes sense when it is read on its own. Everything
# before this marker is dropped when the file is bundled.
BUNDLE_START = "<!-- bundle:start -->"



def expand(skill: Path, patterns) -> list:
    """Resolve the pattern list to real files, in order, without repeats."""
    seen, out = set(), []
    for pattern in patterns:
        matches = sorted(skill.glob(pattern)) if any(c in pattern for c in "*?[") else [skill / pattern]
        for path in matches:
            if path.is_file() and path not in seen:
                seen.add(path)
                out.append(path)
    return out


def strip_frontmatter(text: str) -> tuple:
    """Return (body, description) with any YAML frontmatter removed."""
    match = FRONTMATTER.match(text)
    if not match:
        return text, ""
    block = match.group(0)
    desc = ""
    found = re.search(r"^description:\s*(.+?)(?=\n[a-z_]+:|\n---)", block, re.S | re.M)
    if found:
        desc = " ".join(found.group(1).split())
    return text[match.end():], desc


def preamble(name: str, mode: str, files: list) -> str:
    today = dt.date.today().isoformat()
    lines = [
        f"# {name}, single-file bundle",
        "",
        f"Generated {today} in `{mode}` mode from the {name} skill.",
        "",
        "You are reading a directory flattened into one document because the tool you are running "
        "in cannot open files. Each section below was a separate file. The section headed "
        "`SKILL.md` is the procedure and everything after it is the detail that procedure names. "
        "Read the procedure, decide which mode you are in, then read only the section it points at.",
        "",
        "Where the text says to open a file, look for that path as a section heading here instead. "
        "Where it names a script you cannot run, do the work the script describes by hand and say "
        "that you did.",
        "",
        "Contents:",
        "",
    ]
    lines += [f"- `{p}`" for p in files]
    lines += ["", "---", ""]
    return "\n".join(lines)


def build(skill: Path, mode: str) -> str:
    paths = expand(skill, LAYERS[mode])
    missing = [p for p in paths if not p.exists()]
    for path in missing:
        print(f"warning: skipping missing file {path}", file=sys.stderr)
    paths = [p for p in paths if p.exists()]
    rels = [str(p.relative_to(skill)) for p in paths]

    chunks = [preamble(skill.name, mode, rels)]
    for path, rel in zip(paths, rels):
        body, desc = strip_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        if BUNDLE_START in body:
            body = body.split(BUNDLE_START, 1)[1]
        chunks.append(f"## {rel}\n")
        if desc:
            chunks.append(f"*When to use this: {desc}*\n")
        chunks.append(body.strip())
        chunks.append("\n---\n")
    chunks.append(
        "End of bundle. Nothing above this line is optional context: the rules are the point of "
        "the tool. If a request cannot be met inside them, say which rule blocks it and offer the "
        "nearest thing that is allowed."
    )
    return "\n".join(chunks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("skill_dir", nargs="?", default=str(DEFAULT_SKILL),
                        help="skill directory to bundle (default: the skill this script ships in)")
    parser.add_argument("--mode", choices=list(LAYERS), default="compact")
    parser.add_argument("--out", help="write here instead of stdout")
    parser.add_argument("--list", action="store_true", help="list the files each mode includes, write nothing")
    args = parser.parse_args()

    skill = Path(args.skill_dir).expanduser().resolve()
    if not (skill / "SKILL.md").exists():
        print(f"No SKILL.md in {skill}", file=sys.stderr)
        return 2

    if args.list:
        for mode in LAYERS:
            files = [p for p in expand(skill, LAYERS[mode]) if p.exists()]
            words = sum(len(p.read_text(encoding="utf-8", errors="replace").split()) for p in files)
            marker = "  <- default" if mode == "compact" else ""
            print(f"\n{mode}: {len(files)} file(s), about {words * 4 // 3} tokens{marker}")
            for path in files:
                print(f"  {path.relative_to(skill)}")
        return 0

    text = build(skill, args.mode)
    if args.out:
        out = Path(args.out).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out} ({len(text.split())} words, about {len(text.split()) * 4 // 3} tokens)",
              file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
