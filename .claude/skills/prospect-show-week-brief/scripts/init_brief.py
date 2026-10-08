#!/usr/bin/env python3
"""Start a show-week brief for one prospect, in its workspace outside the brain.

    python3 init_brief.py "Acme Example Co." --id PX-0007 --show "CloudSec Expo" --start 2026-11-24 --end 2026-11-26
    python3 init_brief.py "Acme Example Co." --id PX-0007 --show "CloudSec Expo" --start 2026-11-24 --end 2026-11-26 --root ~/twc-prospects

If the prospect already has a workspace (from the strategy skill), the brief is added
to it as brief/, and the shared register, brand kit, log and envelope are reused. If
not, a light workspace is created: README, log, paths.env, the evidence register, the
claim envelope, and brief/, brand/ and build/ folders. Never inside the brain, never
over an existing brief.

Writes brief/brief.json from the skeleton with the prospect and the show filled in, and
brief/research.md, the working notes for the week. Then: score the gate with the strategy
skill's gate.py, written into brief/brief.json.

No third-party dependencies. Python 3.8 or later.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

import _family
import init_workspace as iw  # the strategy skill's workspace helpers

TEMPLATES = _family.SKILL / "templates"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("company")
    ap.add_argument("--id", required=True)
    ap.add_argument("--show", required=True, help="the show's name")
    ap.add_argument("--start", required=True, help="first day, YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="last day, YYYY-MM-DD")
    ap.add_argument("--website", default="")
    ap.add_argument("--slug")
    ap.add_argument("--short-name")
    ap.add_argument("--root")
    ap.add_argument("--brain")
    a = ap.parse_args()
    if not re.fullmatch(r"PX-\d{4}", a.id):
        ap.error("--id must look like PX-0007")
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    today = dt.date.today()
    weeks = (start - today).days / 7
    if weeks < 3:
        print(f"The show starts {weeks:.1f} weeks from today. Under 3 there is nothing left to act on. "
              "Note the next edition in the workspace log instead.", file=sys.stderr)
        return 2
    brain = iw.find_brain(a.brain)
    if not brain:
        print("The brain was not found. Pass --brain.", file=sys.stderr)
        return 2
    root = Path(a.root).expanduser().resolve() if a.root else (brain.parent / "twc-prospects").resolve()
    if root == brain or brain in root.parents:
        print(f"Refusing: {root} is inside the brain. Prospect data never lives in the brain repository.", file=sys.stderr)
        return 2
    slug = a.slug or iw.slugify(a.company)
    ws = root / slug
    if (ws / "brief" / "brief.json").exists():
        print(f"Refusing: {ws / 'brief' / 'brief.json'} exists. A brief is never overwritten.", file=sys.stderr)
        return 2
    fresh = not ws.exists()
    today_s = today.isoformat()
    for sub in ("brief", "evidence/raw", "brand", "build"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
    if fresh:
        reg_t = _family.STRATEGY / "templates" / "evidence-register.md"
        (ws / "evidence" / "evidence-register.md").write_text(iw.fill(reg_t.read_text(encoding="utf-8"), a.company, a.id, today_s),
                                                            encoding="utf-8")
        (ws / "README.md").write_text(
            f"# {a.id}, {a.company}\n\nA private prospect workspace, outside the brain on purpose: the brain holds only IDs.\n\n"
            f"created: {today_s}\nstatus: show-week brief, gate pending\n\n"
            "- Never commit this folder into the brain. The brain's pipeline gets one row by ID.\n"
            "- Public information only. Roles, never people.\n"
            "- One gift per prospect. A second only after they reply.\n\n"
            "| Path | What |\n|---|---|\n| `paths.env` | Paths to the brain and the skills |\n| `log.md` | Every step, dated |\n"
            "| `brief/` | brief.json and research.md |\n| `evidence/` | The register, the envelope, captures in raw/ |\n"
            "| `brand/` | The brand kit |\n| `build/` | The built page and its PDF |\n", encoding="utf-8")
        (ws / "log.md").write_text(f"# Log, {a.id}\n\nEvery step, dated. IDs and roles only.\n\n| Date | Step | Note |\n|---|---|---|\n",
                                   encoding="utf-8")
    env = ws / "paths.env"
    lines = env.read_text(encoding="utf-8").splitlines() if env.exists() else []
    want = {"BRAIN": str(brain), "STRATEGY_SKILL": str(_family.STRATEGY), "DECK_SKILL": str(_family.DECK),
            "BRIEF_SKILL": str(_family.SKILL), "PROSPECT_ID": a.id}
    have = {l.split("=", 1)[0] for l in lines if "=" in l}
    lines += [f'{k}="{v}"' for k, v in want.items() if k not in have]
    env.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with open(ws / "log.md", "a", encoding="utf-8") as f:
        f.write(f"| {today_s} | show-week brief started | {a.show}, {a.start} to {a.end}, {weeks:.1f} weeks out |\n")

    b = json.loads((TEMPLATES / "brief.skeleton.json").read_text(encoding="utf-8"))
    b["prospect"].update({"id": a.id, "company": a.company, "short_name": a.short_name or a.company.split()[0],
                          "slug": slug, "website": a.website})
    b["date"] = today_s
    b["show"].update({"name": a.show, "start": a.start, "end": a.end})
    d = start - dt.timedelta(days=1)
    b["days"] = [{"date": (d + dt.timedelta(days=i)).isoformat(),
                  "label": (d + dt.timedelta(days=i)).strftime("%a ") + str((d + dt.timedelta(days=i)).day) +
                  (d + dt.timedelta(days=i)).strftime(" %b"),
                  "note": "The day before" if i == 0 else f"Day {i}", "slots": []}
                 for i in range((end - d).days + 1)]
    b["kicker"] = f"Show-week brief, {a.show}"
    env_md, env_json = ws / "evidence" / "envelope.md", ws / "evidence" / "envelope.json"
    r = subprocess.run([sys.executable, str(_family.STRATEGY / "scripts" / "claim_envelope.py"), "--brain", str(brain),
                        "--out", str(env_md), "--json", str(env_json), "--prospect", a.id], capture_output=True, text=True)
    if r.returncode == 0 and env_json.exists():
        e = json.loads(env_json.read_text(encoding="utf-8"))
        b["envelope"] = {"generated": e["generated"], "brain_commit": e["brain_commit"], "path": "evidence/envelope.md"}
    else:
        print("  WARN the claim envelope was not written: " + (r.stderr or r.stdout).strip(), file=sys.stderr)
    (ws / "brief" / "brief.json").write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    research = (TEMPLATES / "brief-research.md").read_text(encoding="utf-8")
    research = research.replace("[Company]", a.company).replace("[Prospect ID]", a.id).replace("[Show]", a.show)
    research = research.replace("date: [YYYY-MM-DD]", f"date: {today_s}")
    (ws / "brief" / "research.md").write_text(research, encoding="utf-8")
    print(f"{'Workspace created' if fresh else 'Brief added to the existing workspace'}: {ws}")
    print(f"  The show starts {weeks:.1f} weeks from today." +
          ("" if weeks >= 7 else " Under 7: the suggestion must say plainly what the time allows."))
    print("Next:")
    print(f"  cd {ws} && source ./paths.env")
    if fresh or not (ws / "strategy" / "strategy.json").exists():
        print('  1. Score the gate: python3 "$STRATEGY_SKILL/scripts/gate.py" --acv n --event-spend n --unreachable n '
              "--warm n --converts n --owner n --write brief/brief.json")
    else:
        print("  1. The gate was scored for the strategy: copy it into brief/brief.json, or re-score it with --write brief/brief.json")
    print("  2. Read the week into brief/research.md, recording every source in evidence/evidence-register.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
