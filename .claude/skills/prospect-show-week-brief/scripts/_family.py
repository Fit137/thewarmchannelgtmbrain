"""Locate the two sibling skills this one builds on, and make their scripts importable.

The show-week brief reuses, rather than copies, the family's machinery:
  prospect-channel-strategy  gate.py, claim_envelope.py, validate_strategy.py, the register template
  prospect-deck-builder      build_deck.py (brand loading, text marks), deck_check.py, screenshot.py,
                             brand_extract.py, contrast.py, fetch_font.py

All three skills are installed side by side, for example in the brain's .claude/skills/.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent


def sibling(name):
    for root in [SKILL.parent] + ([Path(os.environ["TWC_SKILLS"])] if os.environ.get("TWC_SKILLS") else []):
        p = root / name
        if (p / "SKILL.md").is_file():
            return p
    sys.exit(f"The {name} skill was not found beside {SKILL.name}. Install the three prospect skills "
             f"side by side, or set TWC_SKILLS to the folder that holds them.")


STRATEGY = sibling("prospect-channel-strategy")
DECK = sibling("prospect-deck-builder")
for p in (STRATEGY / "scripts", DECK / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
