#!/usr/bin/env python3
"""Write the claim envelope for a prospect strategy: what may and may not be said today.

    python3 claim_envelope.py --out ../twc-prospects/acme/evidence/envelope.md
    python3 claim_envelope.py --brain ../thewarmchannelgtmbrain --out envelope.md --json envelope.json

The envelope is a dated snapshot of the brain's control layer, read at the moment a
strategy is written, so the strategy can be checked against the rules that were in
force when it was made, and re-checked when the brain moves on. It holds:

  1. Every open decision, what it blocks, its default, and what it means for a
     prospect strategy and deck.
  2. Every decided entry, by title, newest first.
  3. Every capability's service status, with the non-READY ones called out.
  4. The figures cleared for client assets, with their grades, and the rules that
     travel with the numbers.
  5. The hard bans, and the banned words.

It reads ops/decisions.md, rules/service-status.md, rules/evidence-ledger.md,
rules/do-not-say.md and scripts/lint_claims.py from the brain. The brain is found from
--brain, then $TWC_BRAIN, then by walking up from this script, then
../thewarmchannelgtmbrain from the working directory.

Re-run it before sending anything. If the brain's commit has changed since the
envelope was written, the strategy is re-checked against the new envelope first.
No third-party dependencies. Python 3.8 or later.
"""
import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# What each open decision means for a prospect strategy and its deck. A decision not
# listed here is reported with "read the entry", never guessed at.
MEANING = {
    "D1": "No legal entity. No scope, contract, invoice or business number in any material. The founder is the sender.",
    "D2": "No price, fee, discount or tier anywhere, including the calculator's investment field, which stays empty.",
    "D3": "The founder's two commissioned rooms are not proof. Never cited as results, never called successful.",
    "D4": "No promise, floor or remedy. No guaranteed attendance, meetings, leads or pipeline, in copy or notes.",
    "D5": "Approaching guests is not offered yet. Wherever outreach is described as ours, its status travels in the same sentence.",
    "D7": "Founder attendance is not promised. Default is to attend the first three, which is a default, not an offer.",
    "D8": "The concentration segment is open, default enterprise cybersecurity. A prospect outside it needs a stated reason.",
    "D9": "The unit of value's name is open. 'Qualified conversation' is the working name, never a counted promise.",
    "D10": "The value metric is open. No per-arrival, per-lead or per-conversation pricing language.",
    "D11": "Post-event conversion and the guest promise are frozen. Describe what happens after the evening only as continuing with guests who choose it, designed with the client, not offered until settled. Never describe a hand-over mechanism.",
    "D12": "The brand name on guest surfaces is open. Sample invitations are signed by the founder by name, with the host named.",
    "D13": "Founding client terms are open. No founding discount or offer named.",
    "D14": "The guest ICP is open. Describe guests by role and organisation type only.",
    "D15": "The partner set is open. No partner named as a route to guests.",
    "D16": "The landing page is unpublished. Never link to it from a prospect deck.",
    "D17": "The channel economics stay at their ledger grades. Grade C plus figures never enter a deck.",
}

DECISION = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s+(?:(D\d+)(?:\s+amended)?\.?\s+)?(.*?)\s*\((OPEN|DECIDED)([^)]*)\)\s*$")


def find_brain(arg):
    cands = []
    if arg:
        cands.append(Path(arg))
    if os.environ.get("TWC_BRAIN"):
        cands.append(Path(os.environ["TWC_BRAIN"]))
    cands.extend(Path(__file__).resolve().parents)
    cands += [Path.cwd() / ".." / "thewarmchannelgtmbrain", Path.cwd() / "thewarmchannelgtmbrain"]
    for c in cands:
        if (c / "ops" / "decisions.md").is_file() and (c / "rules").is_dir():
            return c.resolve()
    return None


def brain_commit(brain):
    try:
        r = subprocess.run(["git", "-C", str(brain), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", str(brain), "status", "--porcelain", "--", "rules", "ops", "context"],
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return r.stdout.strip() + (" with uncommitted rule changes" if dirty else "") if r.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def table_rows(text, after_heading):
    """Rows of the first markdown table after a heading that starts with after_heading."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("#") and after_heading.lower() in l.lower()), None)
    if start is None:
        return []
    rows, in_table = [], False
    for l in lines[start + 1:]:
        if l.startswith("|"):
            in_table = True
            if re.match(r"^\|\s*:?-", l):
                continue
            rows.append([c.strip() for c in l.strip().strip("|").split("|")])
        elif in_table:
            break
        elif l.startswith("#"):
            break
    return rows[1:] if rows else []


def decisions(brain):
    text = (brain / "ops" / "decisions.md").read_text(encoding="utf-8")
    glance = {}
    for r in table_rows(text, "Open decisions at a glance"):
        if len(r) >= 5 and re.match(r"D\d+", r[0]):
            glance[r[0]] = {"decision": r[1], "blocks": r[2], "default": r[3], "owner": r[4]}
    entries = []
    for line in text.splitlines():
        m = DECISION.match(line)
        if m:
            date, did, title, status, rest = m.groups()
            entries.append({"date": date, "id": did, "title": title.strip(), "status": status,
                            "note": rest.strip(" ,")})
    open_ids = []
    for e in entries:
        if e["status"] == "OPEN" and e["id"] and e["id"] not in open_ids:
            open_ids.append(e["id"])
    for k in glance:
        if k not in open_ids:
            open_ids.append(k)
    open_ids.sort(key=lambda x: int(x[1:]))
    return entries, open_ids, glance


def statuses(brain):
    out, section = [], ""
    for line in (brain / "rules" / "service-status.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        m = re.match(r"^-\s+(.+?):\s+(DELIVERED|READY|IN BUILD|BLOCKED|ROADMAP|EXCLUDED|NONE|NOT HELD|NOT BUILT|DECIDED)\b(.*)$", line)
        if m and section not in ("Legend",):
            out.append({"section": section, "capability": m.group(1).strip(), "status": m.group(2),
                        "detail": m.group(3).strip(" .,")})
    return out


def ledger(brain):
    text = (brain / "rules" / "evidence-ledger.md").read_text(encoding="utf-8")
    cleared = [r for r in table_rows(text, "Cleared for client assets") if len(r) >= 4]
    rules = []
    lines = text.splitlines()
    i = next((k for k, l in enumerate(lines) if l.startswith("## Rules that come with the numbers")), None)
    if i is not None:
        for l in lines[i + 1:]:
            if l.startswith("## "):
                break
            if re.match(r"^\d+\.\s", l):
                rules.append(l.strip())
    return cleared, rules


def bans(brain):
    text = (brain / "rules" / "do-not-say.md").read_text(encoding="utf-8")
    return [r for r in table_rows(text, "Hard bans") if len(r) >= 2]


def banned_words(brain):
    lint = brain / "scripts" / "lint_claims.py"
    try:
        spec = importlib.util.spec_from_file_location("twc_lint_claims", str(lint))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return list(mod.BANNED_WORDS)
    except Exception:
        return ["leverage", "unlock", "seamless", "robust", "streamline", "cutting-edge", "empower"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brain")
    ap.add_argument("--out", required=True, help="where to write envelope.md")
    ap.add_argument("--json", help="also write the envelope as JSON")
    ap.add_argument("--prospect", default="", help="prospect ID, for the header")
    a = ap.parse_args()
    brain = find_brain(a.brain)
    if not brain:
        print("The brain was not found. Pass --brain, or paste adapters/portable-control-layer.md and stop: "
              "a prospect strategy is never written without the envelope.", file=sys.stderr)
        return 2
    today = dt.date.today().isoformat()
    commit = brain_commit(brain)
    entries, open_ids, glance = decisions(brain)
    st = statuses(brain)
    cleared, num_rules = ledger(brain)
    hard = bans(brain)
    words = banned_words(brain)
    reviewed = {}
    for f in ("service-status.md", "evidence-ledger.md", "do-not-say.md", "two-vocabularies.md", "writing-rules.md"):
        p = brain / "rules" / f
        if p.exists():
            m = re.search(r"last_reviewed:\s*(\S+)", p.read_text(encoding="utf-8"))
            reviewed[f] = m.group(1) if m else "not stated"

    L = [f"# Claim envelope{', ' + a.prospect if a.prospect else ''}\n",
         f"generated: {today}  ",
         f"brain: {brain}  ",
         f"brain commit: {commit}\n",
         "What may and may not be said in this prospect's strategy and deck, as the brain stood on the date above. "
         "Re-run `claim_envelope.py` before sending. If the commit differs, re-check the strategy against the new envelope.\n",
         "Rules files reviewed: " + ", ".join(f"{k} {v}" for k, v in reviewed.items()) + ".\n",
         "## 1. Open decisions, and what each means here\n",
         "| # | Decision | Blocks | Default until decided | For this strategy and deck |", "|---|---|---|---|---|"]
    titles = {e["id"]: e["title"] for e in entries if e["id"]}
    for d in open_ids:
        g = glance.get(d, {})
        L.append(f"| {d} | {g.get('decision') or titles.get(d, '')} | {g.get('blocks', '')} | {g.get('default', '')} | "
                 f"{MEANING.get(d, 'Read the entry in ops/decisions.md before writing anything it touches.')} |")
    L.append("\n## 2. Decided, newest first\n")
    for e in entries:
        if e["status"] == "DECIDED":
            L.append(f"- {e['date']} {e['id'] + '. ' if e['id'] else ''}{e['title']}" + (f" ({e['note']})" if e["note"] else ""))
    L.append("\n## 3. Service status\n")
    L.append("Nothing BLOCKED, IN BUILD or ROADMAP is described as a thing the prospect can buy today. "
             "If it must be mentioned, its status travels in the same sentence.\n")
    L.append("| Area | Capability | Status | Detail |\n|---|---|---|---|")
    for s in st:
        mark = "" if s["status"] == "READY" else "**"
        L.append(f"| {s['section']} | {s['capability']} | {mark}{s['status']}{mark} | {s['detail']} |")
    L.append("\n## 4. Figures cleared for client assets\n")
    L.append("The only market numbers a strategy or deck may use. Grade C never enters a deck. "
             "None of these is The Warm Channel's performance.\n")
    L.append("| Ledger row | Figure | Source | Grade |\n|---|---|---|---|")
    for r in cleared:
        L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    if num_rules:
        L.append("\nRules that travel with the numbers:\n")
        L += num_rules
    L.append("\n## 5. Hard bans\n")
    L.append("| Never | Say instead |\n|---|---|")
    for r in hard:
        L.append(f"| {r[0]} | {r[1]} |")
    L.append("\nBanned words, never used: " + ", ".join(words) + ". No em dash and no en dash, anywhere.\n")
    L.append("## 6. Always true for a prospect strategy\n")
    L += ["- The proof set is empty. No client, count, logo, testimonial, case study or result.",
          "- Every number about the prospect's business is theirs to supply, written `{TBD}` until they do.",
          "- Positions, scores and placements are our reading of public information, and are labelled so.",
          "- Guests are described by role and organisation type, never by name. No personal data in the brain.",
          "- The strategy is client copy. Any guest copy inside it (a sample invitation) uses guest words only.",
          "- One call to action. One researched approach to one named person. No sequence, no follow-up to a non-reply."]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {out}. Brain commit {commit}. {len(open_ids)} open decisions, "
          f"{sum(1 for s in st if s['status'] != 'READY')} capabilities not READY, {len(cleared)} cleared figures.")
    if a.json:
        Path(a.json).write_text(json.dumps({
            "generated": today, "brain": str(brain), "brain_commit": commit, "open_decisions": open_ids,
            "not_ready": [s for s in st if s["status"] != "READY"], "cleared_rows": [r[0] for r in cleared],
            "banned_words": words}, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
