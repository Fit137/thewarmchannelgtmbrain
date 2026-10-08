#!/usr/bin/env python3
"""Create a private workspace for one prospect's strategy and deck, outside the brain.

    python3 init_workspace.py "Acme Example Co." --id PX-0007 --website https://acme.example
    python3 init_workspace.py "Acme Example Co." --id PX-0007 --root ~/twc-prospects

The workspace goes in --root (default: a twc-prospects folder beside the brain
repository), as <root>/<slug>/. It is never created inside the brain: the brain holds
no data about prospects, only IDs. The script refuses a root inside the brain, and
refuses to overwrite an existing workspace.

It creates the folders, copies the eleven phase templates with the company and ID
filled in, starts the evidence register, the research log and the activity log, writes
strategy.json from the skeleton, writes paths.env so every command can find the brain
and both skills, and writes the claim envelope as the brain stands today.

No third-party dependencies. Python 3.8 or later.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
TEMPLATES = SKILL / "templates"
PHASES = ["00-gate", "01-account", "02-footprint", "03-buyers", "04-landscape", "05-channel", "06-questions",
          "07-operating", "08-economics", "09-engagement", "10-handoff"]


def find_brain(arg):
    cands = [Path(arg)] if arg else []
    cands += list(HERE.parents) + [Path.cwd() / ".." / "thewarmchannelgtmbrain", Path.cwd()]
    for c in cands:
        if (c / "ops" / "decisions.md").is_file() and (c / "rules").is_dir():
            return c.resolve()
    return None


def slugify(name):
    s = re.sub(r"\b(inc|incorporated|ltd|limited|llc|corp|corporation|co|company|plc|gmbh|sa|ag)\b\.?", "", name, flags=re.I)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "prospect"


def fill(text, company, pid, today):
    text = text.replace("[Company]", company).replace("[Prospect ID]", pid)
    return re.sub(r"^(date|created|captured): \[YYYY-MM-DD\]", lambda m: f"{m.group(1)}: {today}", text, flags=re.M)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("company")
    ap.add_argument("--id", required=True, help="pipeline ID, PX-0000 format")
    ap.add_argument("--website", default="")
    ap.add_argument("--slug")
    ap.add_argument("--short-name", help="what the copy calls them, for example Acme")
    ap.add_argument("--root")
    ap.add_argument("--brain")
    a = ap.parse_args()
    if not re.fullmatch(r"PX-\d{4}", a.id):
        ap.error("--id must look like PX-0007. The pipeline holds IDs")
    brain = find_brain(a.brain)
    if not brain:
        print("The brain was not found. Pass --brain. A strategy is never started without it.", file=sys.stderr)
        return 2
    root = Path(a.root).expanduser().resolve() if a.root else (brain.parent / "twc-prospects").resolve()
    if root == brain or brain in root.parents:
        print(f"Refusing: {root} is inside the brain. Prospect data never lives in the brain repository.", file=sys.stderr)
        return 2
    slug = a.slug or slugify(a.company)
    ws = root / slug
    if ws.exists():
        print(f"Refusing: {ws} already exists. A workspace is never overwritten. Use REFRESH or UPGRADE inside it.", file=sys.stderr)
        return 2
    today = dt.date.today().isoformat()
    for sub in ("strategy", "evidence/raw", "brand", "deck/fonts", "spec", "build"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
    for ph in PHASES:
        src = TEMPLATES / f"{ph}.md"
        (ws / "strategy" / f"{ph}.md").write_text(fill(src.read_text(encoding="utf-8"), a.company, a.id, today), encoding="utf-8")
    for name in ("evidence-register.md", "research-log.md"):
        (ws / "evidence" / name).write_text(fill((TEMPLATES / name).read_text(encoding="utf-8"), a.company, a.id, today),
                                            encoding="utf-8")
    (ws / "README.md").write_text(fill((TEMPLATES / "workspace-README.md").read_text(encoding="utf-8"), a.company, a.id, today),
                                  encoding="utf-8")
    (ws / "log.md").write_text(f"# Log, {a.id}\n\nEvery step, dated. IDs and roles only.\n\n| Date | Step | Note |\n|---|---|---|\n"
                               f"| {today} | workspace created | gate pending |\n", encoding="utf-8")
    deck_skill = SKILL.parent / "prospect-deck-builder"
    (ws / "paths.env").write_text(
        f'BRAIN="{brain}"\nSTRATEGY_SKILL="{SKILL}"\nDECK_SKILL="{deck_skill}"\nPROSPECT_ID="{a.id}"\n', encoding="utf-8")
    st = json.loads((TEMPLATES / "strategy.skeleton.json").read_text(encoding="utf-8"))
    st["prospect"].update({"id": a.id, "company": a.company, "short_name": a.short_name or a.company.split()[0],
                           "slug": slug, "website": a.website})
    st["date"] = today
    st["basis"] = "Public information only. No CRM, budget or account list seen."
    env_md, env_json = ws / "evidence" / "envelope.md", ws / "evidence" / "envelope.json"
    r = subprocess.run([sys.executable, str(HERE / "claim_envelope.py"), "--brain", str(brain), "--out", str(env_md),
                        "--json", str(env_json), "--prospect", a.id], capture_output=True, text=True)
    if r.returncode == 0 and env_json.exists():
        env = json.loads(env_json.read_text(encoding="utf-8"))
        st["envelope"] = {"generated": env["generated"], "brain_commit": env["brain_commit"],
                          "path": "evidence/envelope.md", "open_decisions": env["open_decisions"]}
    else:
        print("  WARN the claim envelope was not written: " + (r.stderr or r.stdout).strip(), file=sys.stderr)
    (ws / "strategy" / "strategy.json").write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Workspace: {ws}")
    print(f"  {len(PHASES)} phase files in strategy/, register and research log in evidence/, envelope written.")
    print("Next:")
    print(f"  cd {ws} && source ./paths.env")
    print("  1. Fill strategy/00-gate.md from public evidence, starting the register as you go.")
    print('  2. python3 "$STRATEGY_SKILL/scripts/gate.py" --acv n --event-spend n --unreachable n --warm n --converts n --owner n '
          "--write strategy/strategy.json")
    print("  3. Only on GO: phases 01 to 10.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
