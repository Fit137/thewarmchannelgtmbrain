#!/usr/bin/env python3
"""Check The Warm Channel brain against its own claim and vocabulary rules.

Adapted from tools/lint_claims.py in Fit137/warmchannelgtmbuild. It adds the
check that rule cannot be broken quietly: client vocabulary inside guest copy.

ERROR, fails the run:
  - an em dash or an en dash anywhere
  - a banned word, outside a line that states the ban
  - a client word inside a guest-copy block, meaning between
    <!-- guest-copy:begin --> and <!-- guest-copy:end -->
  - an unfilled {{PLACEHOLDER}}

WARN, for a person to read:
  - a line that reads near a banned claim. A pattern cannot tell an assertion
    from a report of one, and the rules files name banned claims in order to
    forbid them, so these never fail the run.

Neither severity can tell you whether a claim is true. That is what
ops/QA-checklist.md is for.

Usage: python3 scripts/lint_claims.py [brain_dir]
Exit status is 1 on any ERROR, so it can gate a commit or a CI run.
"""
import os
import re
import sys

SKIP_DIRS = {".git", "sources", ".claude", ".github", "node_modules", "__pycache__"}
EXTENSIONS = (".md", ".txt", ".mdc")

BANNED_WORDS = ["leverage", "unlock", "seamless", "robust", "streamline",
                "cutting-edge", "cutting edge", "empower"]

# A line that states a ban necessarily contains the banned words.
DECLARING = re.compile(
    r"banned words?|do not say|never say|say instead|do not use|forbidden|"
    r"none of the|banned word",
    re.I)

BANNED_CLAIMS = [
    (r"\b70\s*%\s*(positive\s*)?reply", "the unaudited 70% reply rate, D3"),
    (r"\bMiro\b", "a client named without written permission"),
    (r"raised a \$30 ?(million|M)\b", "sole causation on the Series A"),
    (r"resulted in more than \$1 ?(million|M)", "pipeline causation"),
    (r"\bguarantee[sd]?\s+(a |any |you )?(meeting|meetings|pipeline|lead|leads|introduction)",
     "an outcome guarantee"),
    (r"no other channel", "an unscoped superlative"),
    (r"\bour (network|community) of\b", "a claim of an existing network"),
    (r"composed attendance", "the retired category"),
]

# Words that never reach a guest. rules/two-vocabularies.md is the source.
GUEST_BANNED = [
    r"\blead generation\b", r"\bleads?\b", r"\bsales-qualified\b", r"\bSQLs?\b",
    r"\bMQLs?\b", r"\bpipeline\b", r"\bfunnel\b", r"\bconver(t|ts|ted|sion|sions)\b",
    r"\bclose rate\b", r"\bdeals?\b", r"\bprospects?\b", r"\btarget accounts?\b",
    r"\bnamed accounts?\b", r"\baccount list\b", r"\bin-ICP\b", r"\bICP\b",
    r"\bcomposed attendance\b", r"\baccess\b", r"\binventory\b", r"\bcoverage\b",
    r"\bshow rate\b", r"\battendance floor\b", r"\bchannel\b", r"\bclients?\b",
    r"\breply rates?\b",
]

PLACEHOLDER = re.compile(r"\{\{[^}]{1,80}\}\}")
GUEST_BEGIN = "<!-- guest-copy:begin -->"
GUEST_END = "<!-- guest-copy:end -->"


def targets(root):
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        parts = [] if rel_dir == "." else rel_dir.split(os.sep)
        if any(part in SKIP_DIRS for part in parts):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.endswith(EXTENSIONS):
                yield os.path.join(dirpath, name)


def check(path, root):
    rel = os.path.relpath(path, root)
    lines = open(path, encoding="utf-8").read().splitlines()
    errors, warnings = [], []
    in_guest = False

    for n, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped == GUEST_BEGIN:
            in_guest = True
            continue
        if stripped == GUEST_END:
            in_guest = False
            continue

        if "—" in line:
            errors.append((n, "em dash, use a comma or restructure"))
        if "–" in line:
            errors.append((n, "en dash, use a comma or 'to'"))

        if not DECLARING.search(line):
            for word in BANNED_WORDS:
                if re.search(r"\b" + re.escape(word), line, re.I):
                    errors.append((n, "banned word: %s" % word))

        for hit in PLACEHOLDER.findall(line):
            errors.append((n, "unfilled placeholder %s" % hit))

        if in_guest:
            for pattern in GUEST_BANNED:
                match = re.search(pattern, line, re.I)
                if match:
                    errors.append((n, "client word in guest copy: '%s'"
                                   % match.group(0)))

        for pattern, why in BANNED_CLAIMS:
            if re.search(pattern, line, re.I):
                warnings.append((n, why))

    if in_guest:
        errors.append((len(lines), "guest-copy block opened and never closed"))
    return rel, errors, warnings


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                           os.path.join(os.path.dirname(__file__), os.pardir))
    failed = warned = checked = 0

    for path in targets(root):
        checked += 1
        rel, errors, warnings = check(path, root)
        if errors:
            failed += 1
            print("ERROR %s" % rel)
            for n, why in errors:
                print("  line %d: %s" % (n, why))
        if warnings:
            warned += 1
            print("WARN  %s" % rel)
            for n, why in warnings:
                print("  line %d: reads near a banned claim, %s" % (n, why))

    print("\n%d file(s) checked. %d with errors, %d with warnings."
          % (checked, failed, warned))
    if warned and not failed:
        print("Warnings are for a person to read. Naming a claim in order to "
              "forbid it, or quoting a competitor, is allowed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
