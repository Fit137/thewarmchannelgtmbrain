#!/usr/bin/env python3
"""
Audit a Go-to-Market Brain.

Checks structure, links, size budgets, the brain's own writing rules,
unfilled placeholders, ledger staleness, open downstream debt, and whether
the brain still loads in the tools the team runs.

    python3 audit_brain.py <brain_dir> [--max-age-days 90] [--quiet]

Exit codes: 0 clean or warnings only, 1 errors found, 2 bad usage.
No third-party dependencies.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REQUIRED = [
    "CLAUDE.md",
    "llms.txt",
    "README.md",
    "rules/writing-rules.md",
    "rules/do-not-say.md",
    "rules/glossary.md",
    "ops/QA-checklist.md",
    "ops/decisions.md",
    "ops/signal-log.md",
    "ops/copy-bank.md",
]

RECOMMENDED = [
    "AGENTS.md",
    "rules/feature-status.md",
    "ops/asset-index.md",
    "ops/review-cadence.md",
    "prompts/common-tasks.md",
]

# Layer -> (glob, soft line budget)
BUDGETS = [
    ("CLAUDE.md", 70),
    ("AGENTS.md", 70),
    ("rules/*.md", 90),
    ("reference/*.md", 80),
    ("templates/*.md", 60),
]

DEFAULT_BANNED = [
    "leverage", "unlock", "seamless", "robust",
    "streamline", "cutting-edge", "empower",
]

SKIP_DIRS = {".git", "node_modules", "sources", "snapshots", ".venv", "__pycache__"}

findings = {"error": [], "warn": [], "info": []}


def add(level, msg):
    findings[level].append(msg)


def md_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix in (".md", ".txt", ".mdc"):
            if not any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                yield path


def check_required(root: Path):
    for rel in REQUIRED:
        if not (root / rel).exists():
            add("error", f"missing required file: {rel}")
    for rel in RECOMMENDED:
        if not (root / rel).exists():
            add("warn", f"missing recommended file: {rel}")
    if not list(root.glob("context/*.md")):
        add("error", "no master context file in context/")
    if not (root / "snapshots").is_dir():
        add("warn", "no snapshots/ directory, the compounding loop has no periodic capture")
    examples = root / "examples"
    if not examples.is_dir() or not list(examples.glob("*.md")):
        add("warn", "no files in examples/, agents have no voice reference to match")


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")


def check_links(root: Path):
    for path in md_files(root):
        for target in LINK_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "<")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel = path.relative_to(root)
                add("error", f"broken link in {rel}: {target}")


def check_index(root: Path):
    index = root / "llms.txt"
    if not index.exists():
        return
    text = index.read_text(encoding="utf-8", errors="replace")
    for path in md_files(root):
        rel = path.relative_to(root)
        if rel.parts[0] in {"ops", "prompts", "examples", "templates", "adapters"}:
            continue  # indexed as groups, not always file by file
        if rel.name in {"README.md", "CLAUDE.md", "AGENTS.md", "llms.txt"}:
            continue
        if str(rel) not in text and rel.name not in text:
            add("warn", f"not indexed in llms.txt: {rel}")


def check_budgets(root: Path):
    for pattern, budget in BUDGETS:
        for path in sorted(root.glob(pattern)):
            lines = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
            if lines > budget:
                add("warn", f"{path.relative_to(root)} is {lines} lines, budget {budget}")
    for path in sorted(root.glob("context/*.md")):
        lines = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if lines > 550:
            add("warn", f"{path.relative_to(root)} is {lines} lines, over 500 suggests transcription not distillation")
        elif lines < 120:
            add("warn", f"{path.relative_to(root)} is only {lines} lines, likely under-distilled")


def parse_banned(root: Path):
    """Read the banned-word list out of the brain's own writing rules."""
    rules = root / "rules" / "writing-rules.md"
    if not rules.exists():
        return DEFAULT_BANNED, True
    text = rules.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"[Bb]anned words:\s*([^\n.]+)", text)
    if not match:
        return DEFAULT_BANNED, True
    words = [w.strip(" `*_").lower() for w in re.split(r"[,;]", match.group(1))]
    words = [w for w in words if w and " " not in w and not w.startswith("{{")]
    return (words or DEFAULT_BANNED), False


def check_prose(root: Path):
    banned, defaulted = parse_banned(root)
    if defaulted:
        add("info", "no banned-word list found in rules/writing-rules.md, using defaults")

    rules_text = ""
    rules = root / "rules" / "writing-rules.md"
    if rules.exists():
        rules_text = rules.read_text(encoding="utf-8", errors="replace").lower()
    ban_em_dash = "no em dash" in rules_text or not rules_text

    patterns = {w: re.compile(rf"\b{re.escape(w)}\w*", re.I) for w in banned}
    # A line that states the ban necessarily contains the banned words.
    declaring = re.compile(
        r"banned words?|do not say|never say|say instead|do not use|forbidden|none of the",
        re.I,
    )

    for path in md_files(root):
        rel = path.relative_to(root)
        # The rules files quote the banned words in order to ban them.
        if rel.parts[0] == "rules" or rel.name == "QA-checklist.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            if ban_em_dash and "—" in line:
                add("error", f"em dash in {rel}:{i}")
            if declaring.search(line):
                continue
            hits = [w for w, pattern in patterns.items() if pattern.search(line)]
            if hits:
                add("error", f"banned word(s) {', '.join(hits)} in {rel}:{i}")


PLACEHOLDER_RE = re.compile(r"\{\{[^}]{1,80}\}\}")


def check_placeholders(root: Path):
    for path in md_files(root):
        rel = path.relative_to(root)
        hits = PLACEHOLDER_RE.findall(path.read_text(encoding="utf-8", errors="replace"))
        if hits:
            add("error", f"{len(hits)} unfilled placeholder(s) in {rel}, first: {hits[0]}")


DATE_RE = re.compile(r"(?:last_reviewed|last_updated)\s*:\s*(\d{4}-\d{2}-\d{2})")


def check_staleness(root: Path, max_age: int):
    today = dt.date.today()
    tracked = list((root / "rules").glob("*.md")) + list((root / "context").glob("*.md"))
    for path in sorted(tracked):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8", errors="replace")
        match = DATE_RE.search(text)
        if not match:
            add("warn", f"{rel} has no last_reviewed or last_updated date")
            continue
        try:
            when = dt.date.fromisoformat(match.group(1))
        except ValueError:
            add("warn", f"{rel} has an unreadable date: {match.group(1)}")
            continue
        age = (today - when).days
        if age > max_age:
            add("warn", f"{rel} last reviewed {age} days ago, threshold {max_age}")


ADAPTER_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def check_adapters(root: Path, max_age: int):
    """A guardrail that loads in one tool and not the others is not a guardrail."""
    adapters = root / "adapters"
    files = sorted(adapters.glob("*")) if adapters.is_dir() else []
    files = [p for p in files if p.is_file()]
    if not files:
        add("info", "no adapters/, so the brain loads in Claude Code and in tools that read "
                    "AGENTS.md, and nowhere else. Fine if that is the whole team.")
        return

    add("info", f"{len(files)} adapter(s): {', '.join(p.name for p in files)}")

    # The portable copy carries content rather than a pointer, so it decays.
    portable = adapters / "portable-control-layer.md"
    if portable.exists():
        head = "\n".join(portable.read_text(encoding="utf-8", errors="replace").splitlines()[:20])
        match = ADAPTER_DATE_RE.search(head)
        if not match:
            add("warn", "adapters/portable-control-layer.md carries no date in its first 20 lines, "
                        "so nobody can tell whether it matches the ledgers")
        else:
            age = (dt.date.today() - dt.date.fromisoformat(match.group(1))).days
            if age > max_age:
                add("error", f"adapters/portable-control-layer.md was generated {age} days ago, "
                             f"threshold {max_age}. It carries claims, so a stale copy is a live risk.")


def check_state(root: Path):
    log = root / "ops" / "signal-log.md"
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
        entries = len(re.findall(r"^###\s+\d{4}-\d{2}-\d{2}", text, re.M))
        if entries == 0:
            add("warn", "ops/signal-log.md has no dated entries, the compounding loop is not running")
        else:
            add("info", f"signal log holds {entries} dated entries")
            watches = re.findall(r"WATCH\s*\((\d+)/(\d+)\)", text)
            open_watches = sum(1 for n, total in watches if int(n) < int(total))
            if open_watches:
                add("info", f"{open_watches} open WATCH item(s) awaiting corroboration")

    decisions = root / "ops" / "decisions.md"
    if decisions.exists():
        text = decisions.read_text(encoding="utf-8", errors="replace")
        entries = len(re.findall(r"^##\s+\d{4}", text, re.M))
        if entries == 0:
            add("warn", "ops/decisions.md has no dated entries, settled strategy is not recorded")
        else:
            add("info", f"decision log holds {entries} dated entries")

    snaps = sorted((root / "snapshots").glob("*.md")) if (root / "snapshots").is_dir() else []
    dated = [m.group(1) for m in (re.match(r"(\d{4}-\d{2}-\d{2})", p.name) for p in snaps) if m]
    if dated:
        age = (dt.date.today() - dt.date.fromisoformat(max(dated))).days
        add("info", f"{len(dated)} snapshot(s), most recent {age} days ago")
        if age > 120:
            add("warn", f"most recent snapshot is {age} days old")
    elif snaps:
        add("warn", "snapshots/ holds files but none are named YYYY-MM-DD-<label>.md")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("brain_dir")
    parser.add_argument("--max-age-days", type=int, default=90)
    parser.add_argument("--quiet", action="store_true", help="errors and warnings only")
    args = parser.parse_args()

    root = Path(args.brain_dir).expanduser().resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}")
        return 2

    check_required(root)
    check_links(root)
    check_index(root)
    check_budgets(root)
    check_prose(root)
    check_placeholders(root)
    check_staleness(root, args.max_age_days)
    check_adapters(root, args.max_age_days)
    check_state(root)

    print(f"Go-to-Market Brain audit: {root}\n")
    for level, label in (("error", "ERROR"), ("warn", "WARN"), ("info", "INFO")):
        if level == "info" and args.quiet:
            continue
        for msg in findings[level]:
            print(f"  [{label}] {msg}")

    n_err, n_warn = len(findings["error"]), len(findings["warn"])
    print(f"\n{n_err} error(s), {n_warn} warning(s).")
    if n_err == 0 and n_warn == 0:
        print("Clean. Now run the live test: produce one real asset using only the brain.")
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
