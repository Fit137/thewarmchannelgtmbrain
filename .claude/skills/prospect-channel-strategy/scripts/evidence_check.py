#!/usr/bin/env python3
"""Check a prospect's evidence register, and every citation the strategy makes to it.

    python3 evidence_check.py evidence/evidence-register.md
    python3 evidence_check.py evidence/evidence-register.md --strategy strategy/ --mode BUILD

The register is the closed set of facts a strategy may state. Every row is checked:

  shape     unique IDs (E01, E02 ...), a known kind, a claim, a source, a capture date
  kinds     P0 is prospect-supplied and only exists in UPGRADE mode. P1 and P2 need a
            public address. P3 needs its basis written out, starting "Inference", and
            never carries a percentage or a money figure. M-A and M-B must cite a ledger
            row that exists, sits in the cleared section, and carries the same numbers.
            M-C and NEW rows may be recorded but never used in the deck. NEW rows must
            say they were logged to the brain's signal log.
  age       a capture older than --max-age days (default 90) is re-verified before use
  people    no email address, phone number or personal profile address. Roles, not people
  citations with --strategy, every [E##] in the strategy's markdown exists here, every
            row is cited somewhere or listed as unused, and every sentence carrying a
            percentage or a money figure carries a citation in the same paragraph

ERROR blocks the handoff. WARN is for a person. Exit status 1 on any ERROR.
No third-party dependencies. Python 3.8 or later.
"""
import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

KINDS = {"P0", "P1", "P2", "P3", "M-A", "M-B", "M-C", "NEW"}
PCT_MONEY = re.compile(r"(?:(?:CA|US|C|A)?[$€£]\s?\d[\d,.]*)|(?<![\w.])\d[\d,]*(?:\.\d+)?\s?%")
NUMS = re.compile(r"(?:(?:CA|US|C|A)?[$€£]\s?)?\d[\d,]*(?:\.\d+)?\s?%?")
PEOPLE = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "an email address"),
          (re.compile(r"(?<![\d-])(?:\+\d{1,3}[\s.-]?)?(?:\(\d{3}\)\s?|\d{3}[\s.-])\d{3}[\s.-]\d{4}(?![\d-])"
                      r"|\+\d{1,3}(?:[\s.-]\d{2,5}){2,4}(?!\d)"), "a phone number"),
          (re.compile(r"linkedin\.com/in/", re.I), "a personal LinkedIn profile")]


def find_brain(arg):
    cands = [Path(arg)] if arg else []
    if os.environ.get("TWC_BRAIN"):
        cands.append(Path(os.environ["TWC_BRAIN"]))
    cands += list(Path(__file__).resolve().parents) + [Path.cwd() / ".." / "thewarmchannelgtmbrain"]
    for c in cands:
        if (c / "rules" / "evidence-ledger.md").is_file():
            return c.resolve()
    return None


def ledger_rows(brain):
    rows, section = {}, ""
    for line in (brain / "rules" / "evidence-ledger.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("|") and not re.match(r"^\|\s*(-|#\s*\|)", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3:
                for rid in re.split(r",\s*", cells[0]):
                    rows[rid.strip()] = {"figure": cells[1], "grade": cells[-1].replace("*", ""), "section": section}
    return rows


def parse(path):
    rows, header, problems = [], None, []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|") or re.match(r"^\|\s*:?-", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        low = [c.lower() for c in cells]
        if "id" in low and "kind" in low:
            header = low
            continue
        if not header or not re.match(r"^[EX]\d+$", cells[0]):
            continue
        if len(cells) != len(header):
            problems.append((n, f"row {cells[0]} has {len(cells)} cells, the header has {len(header)}"))
            continue
        row = dict(zip(header, cells))
        row["_line"] = n
        row["_unused_table"] = "why it is out" in header
        rows.append(row)
    return rows, problems


def nums(text):
    return {re.sub(r"[\s,]", "", m.group(0)) for m in NUMS.finditer(text or "") if re.search(r"\d", m.group(0))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("register")
    ap.add_argument("--strategy", help="the strategy folder, for citation checks")
    ap.add_argument("--mode", choices=["BUILD", "UPGRADE", "REFRESH"], default=None)
    ap.add_argument("--max-age", type=int, default=90)
    ap.add_argument("--brain")
    a = ap.parse_args()
    reg = Path(a.register)
    if not reg.is_file():
        print(f"not found: {reg}", file=sys.stderr)
        return 2
    errors, warns = [], []
    rows, problems = parse(reg)
    for n, msg in problems:
        errors.append(f"line {n}: {msg}")
    if not rows:
        errors.append("no evidence rows. The header must name ID and Kind, and rows start E01")
    brain = find_brain(a.brain)
    ledger = ledger_rows(brain) if brain else {}
    if not brain:
        warns.append("brain not found: M-A and M-B rows are not checked against the ledger")
    mode = a.mode
    if not mode and a.strategy:
        sj = Path(a.strategy) / "strategy.json"
        if sj.exists():
            m = re.search(r'"mode"\s*:\s*"(\w+)"', sj.read_text(encoding="utf-8"))
            mode = m.group(1) if m else None
    today = dt.date.today()
    seen = set()
    for r in rows:
        rid, kind = r.get("id", ""), r.get("kind", "").upper().replace(" ", "")
        where = f"{rid} (line {r['_line']})"
        if r["_unused_table"]:
            if kind in ("M-C", "NEW") or rid.startswith("X"):
                continue
        if rid in seen:
            errors.append(f"{where}: duplicate ID")
        seen.add(rid)
        claim = r.get("claim or figure", "")
        src = r.get("source", "")
        basis = r.get("basis or grade", "")
        used = r.get("used in", "")
        if kind not in KINDS:
            errors.append(f"{where}: kind {kind!r} is not one of {', '.join(sorted(KINDS))}")
            continue
        if not claim:
            errors.append(f"{where}: no claim")
        if not src:
            errors.append(f"{where}: no source")
        cap = r.get("captured", "")
        try:
            d = dt.date.fromisoformat(cap)
            if (today - d).days > a.max_age:
                warns.append(f"{where}: captured {cap}, over {a.max_age} days ago. Re-verify before it is used")
        except ValueError:
            errors.append(f"{where}: captured date {cap!r} is not YYYY-MM-DD")
        if kind in ("P1", "P2") and not re.search(r"https?://", src):
            errors.append(f"{where}: {kind} needs the public address it was read at")
        if kind == "P0":
            if mode == "BUILD":
                errors.append(f"{where}: P0 is prospect-supplied, and BUILD mode is public information only")
            if not re.search(r"call|document|email|meeting", src, re.I):
                warns.append(f"{where}: P0 should say how it was supplied: on a call, in a document, with the date")
        if kind == "P3":
            if not basis.lower().startswith("inference"):
                errors.append(f"{where}: P3 needs its basis written out, starting 'Inference'")
            if PCT_MONEY.search(claim):
                errors.append(f"{where}: P3 is an inference and never carries a percentage or a money figure")
        if kind in ("M-A", "M-B", "M-C"):
            m = re.search(r"ledger row\s+([\w]+(?:\s*,\s*\w+)*)", src + " " + basis, re.I)
            if not m:
                errors.append(f"{where}: {kind} must cite 'ledger row N'")
            elif ledger:
                ids = [x.strip() for x in m.group(1).split(",")]
                for lid in ids:
                    lr = ledger.get(lid)
                    if not lr:
                        errors.append(f"{where}: ledger row {lid} does not exist in the brain's evidence ledger")
                        continue
                    cleared = lr["section"].lower().startswith("cleared")
                    if kind in ("M-A", "M-B") and not cleared:
                        errors.append(f"{where}: ledger row {lid} is in '{lr['section']}', not cleared for client assets")
                    missing = nums(claim) - nums(" ".join(ledger[x]["figure"] for x in ids if x in ledger))
                    missing = {x for x in missing if len(re.sub(r"\D", "", x)) > 1}
                    if missing and kind in ("M-A", "M-B"):
                        errors.append(f"{where}: {', '.join(sorted(missing))} not in ledger row {', '.join(ids)}")
                    break
        if kind in ("M-C", "NEW") and re.search(r"\b[A-F]\d\b", used):
            errors.append(f"{where}: {kind} is listed as used in a slide ({used}). It never enters a deck")
        if kind == "NEW" and "signal" not in (basis + " " + used).lower():
            warns.append(f"{where}: NEW figures are logged to the brain's ops/signal-log.md for grading. Say so")
        for pat, what in PEOPLE:
            if pat.search(" | ".join((claim, src, basis))):
                errors.append(f"{where}: {what}. The register records the company, never a person's contact details")
    if a.strategy:
        sdir = Path(a.strategy)
        cited = {}
        for md in sorted(sdir.glob("*.md")):
            text = md.read_text(encoding="utf-8")
            for m in re.finditer(r"\[(E\d+)\]", text):
                cited.setdefault(m.group(1), set()).add(md.name)
            for para in re.split(r"\n\s*\n", text):
                if para.lstrip().startswith(("|", "#", "```", ">")):
                    continue
                for sent in re.split(r"(?<=[.!?])\s+", para):
                    if PCT_MONEY.search(sent) and not re.search(r"\[E\d+\]", para) and "{TBD}" not in sent:
                        warns.append(f"{md.name}: a figure without a citation in its paragraph: {sent.strip()[:110]}")
        for e in sorted(cited):
            if e not in seen:
                errors.append(f"[{e}] is cited in {', '.join(sorted(cited[e]))} and is not in the register")
        unused = sorted(seen - set(cited), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)
        if unused:
            warns.append(f"rows never cited in the strategy files: {', '.join(unused)}. Cite them or move them to the unused table")
    print(f"evidence_check {reg.name}: {len(rows)} rows, mode {mode or 'unknown'}")
    for e in errors:
        print(f"  ERROR {e}")
    for w in warns:
        print(f"  WARN  {w}")
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
