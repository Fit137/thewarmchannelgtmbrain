#!/usr/bin/env python3
"""Check the GTM output against GTM-BRIEF.md Section 5.

Two severities, because the two kinds of rule are not alike.

ERROR is the mechanics: no em dash, no en dash, and seven banned words. These
are purely lexical, so a match is always a violation, and they fail the run.

WARN is the banned claims. A pattern cannot tell an assertion from a report of
one, and these documents legitimately quote a competitor's guarantee and name
the claims they forbid. So hits are printed for a person to read and do not
fail the run. Treating them as errors would only teach the reader to ignore
the output, which is worse than not checking.

Neither severity can tell you whether a claim is true.

Exit status is 1 only on an ERROR, so this can gate a commit.

Usage: python3 tools/lint_claims.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BANNED_WORDS = [
    "leverage", "unlock", "seamless", "robust",
    "streamline", "cutting-edge", "cutting edge", "empower",
]

# Claims GTM-BRIEF.md Section 5 bans outright, as patterns rather than wording,
# so a paraphrase is caught too.
BANNED_CLAIMS = [
    (r"\b70\s*%\s*(positive\s*)?reply", "unaudited 70% reply rate, open decision 3"),
    (r"resulted in more than \$1 ?million", "pipeline causation claim"),
    (r"\bMiro\b", "client named without written permission"),
    (r"I raised a \$30 ?million", "sole causation on the Series A"),
    (r"guarantee[sd]? (a |any )?(meeting|pipeline|introduction)",
     "outcome guarantee beyond attendance"),
]

# These two must name the banned words to do their job: the audit reports on
# them, and the handover passes the rule to whoever works on this next.
BANNED_WORD_EXEMPT = {"CLAIM-AUDIT.md", "HANDOVER.md"}


def targets():
    paths = []
    for pattern in ("research/*.md", "run-a-client/*.md",
                    "run-b-guest/*.md", "handover/*.md",
                    "landing-page/*.md"):
        paths += glob.glob(os.path.join(ROOT, pattern))
    for name in ("CLAIM-AUDIT.md", "RUN-LOG.md"):
        path = os.path.join(ROOT, name)
        if os.path.exists(path):
            paths.append(path)
    return sorted(paths)


def check(path):
    """Return (relative path, errors, warnings)."""
    rel = os.path.relpath(path, ROOT)
    text = open(path, encoding="utf-8").read()
    errors, warnings = [], []

    for line_no, line in enumerate(text.splitlines(), start=1):
        if "—" in line:
            errors.append((line_no, "em dash, use a comma"))
        if "–" in line:
            errors.append((line_no, "en dash, use a comma"))
        if os.path.basename(rel) not in BANNED_WORD_EXEMPT:
            for word in BANNED_WORDS:
                if re.search(r"\b" + re.escape(word), line, re.I):
                    errors.append((line_no, "banned word: %s" % word))
        for pattern, why in BANNED_CLAIMS:
            if re.search(pattern, line, re.I):
                warnings.append((line_no, why))
    return rel, errors, warnings


def main():
    paths = targets()
    failed, warned = 0, 0

    for path in paths:
        rel, errors, warnings = check(path)
        if errors:
            failed += 1
            print("ERROR %s" % rel)
            for line_no, why in errors:
                print("  line %d: %s" % (line_no, why))
        if warnings:
            warned += 1
            print("WARN  %s" % rel)
            for line_no, why in warnings:
                print("  line %d: reads near a banned claim, %s" % (line_no, why))

    print("\n%d file(s) checked. %d with errors, %d with warnings."
          % (len(paths), failed, warned))
    if warned and not failed:
        print("Warnings are for a person to read. Quoting a competitor's "
              "guarantee, or naming a claim in order to forbid it, is allowed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
