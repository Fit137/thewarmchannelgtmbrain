#!/usr/bin/env python3
"""Score the qualification gate for a free prospect strategy: GO, HOLD or NO-GO.

    python3 gate.py --acv 2 --event-spend 3 --unreachable 2 --warm 2 --converts 1 --owner 2
    python3 gate.py --from strategy/gate.json --write strategy/strategy.json
    python3 gate.py --acv 3 --event-spend 3 --unreachable 2 --warm 2 --converts 1 --owner 2 \
        --disqualifier healthcare_conflict

A free strategy costs founder days. It is earned by a prospect that matches the brain's
client ICP (reference/icp-client.md), on public evidence, before any research is spent.

Six criteria, each scored 0 to 3 on the same evidence scale:
  3  direct public evidence that it holds (an evidence register row of kind P1 or P2)
  2  indirect evidence, or an inference with its basis written down (kind P3)
  1  no evidence either way. Normal for characteristic 5 from outside
  0  evidence that it fails

  acv          characteristic 1, six-figure average contract value and up
  event_spend  characteristic 2, already spends materially on events
  unreachable  characteristic 3, the buyer is structurally unreachable cold
  warm         characteristic 4, already distinguishes warm from cold
  converts     characteristic 5, current event spend converts badly, the wedge
  owner        the qualifiers: a named account list exists, and someone owns events
               and is measured on pipeline

Verdict:
  NO-GO  any disqualifier, or acv or event_spend scored 0, or a total under 9
  GO     a total of 12 or more, acv and event_spend at 2 or more, and no zero
  HOLD   everything else. Research one more signal, or wait for one, then re-score

Disqualifiers, each a hard stop:
  low_acv              evidence the ACV is below six figures, or self-serve pricing
  no_named_accounts    a volume or self-serve motion with no account list to build from
  agency_request       they want a booth, a venue or a production crew
  needs_guarantee      they need a guaranteed count of meetings or leads to report upward
  events_sceptic       they want convincing that events work at all
  single_test_event    one event, run once, to see if it works (refuse or reprice)
  healthcare_conflict  inside the founder's separate healthcare business, D6
  active_conflict      a conflict with an active engagement or a partner commitment

Exit status: 0 for GO, 3 for HOLD, 4 for NO-GO, 2 on bad usage.
No third-party dependencies. Python 3.8 or later.
"""
import argparse
import json
import sys
from pathlib import Path

CRITERIA = [
    ("acv", "Six-figure ACV and up", "Characteristic 1. Below it the arithmetic does not work at any fee"),
    ("event_spend", "Already spends materially on events", "Characteristic 2. The budget line and the belief exist"),
    ("unreachable", "Buyer unreachable cold", "Characteristic 3. If a sequence reaches them, the cheapest channel wins"),
    ("warm", "Distinguishes warm from cold", "Characteristic 4. No education required"),
    ("converts", "Event spend converts badly", "Characteristic 5. The wedge. Usually unknown from outside"),
    ("owner", "Named list, and an owner measured on pipeline", "The qualifiers. Without a list there is nothing to build from"),
]
DISQUALIFIERS = {
    "low_acv": "ACV below six figures. 'The arithmetic does not work at a fee that supports the delivery.'",
    "no_named_accounts": "No named account list. 'There is nothing to build from yet. Come back with the list.'",
    "agency_request": "Wants a booth, a venue or a production crew. 'That is an events agency. We are not one.'",
    "needs_guarantee": "Needs a guaranteed count to report upward. 'We will not promise that. An agency that will is the better fit.'",
    "events_sceptic": "Wants convincing that events work at all. Characteristic 4 fails, the education cost exceeds the deal.",
    "single_test_event": "One event, run once, to see if it works. Refused or repriced, decided 2026-09-22.",
    "healthcare_conflict": "Inside the founder's separate healthcare business. A consent boundary, D6. Stop.",
    "active_conflict": "Conflicts with an active engagement or a partner commitment. Stop and tell the founder.",
}


def verdict(scores, dq):
    total = sum(scores.values())
    if dq or scores["acv"] == 0 or scores["event_spend"] == 0 or total < 9:
        return "NO-GO", total
    if total >= 12 and scores["acv"] >= 2 and scores["event_spend"] >= 2 and 0 not in scores.values():
        return "GO", total
    return "HOLD", total


def reasons(scores, dq, v):
    out = []
    for k in dq:
        out.append(DISQUALIFIERS.get(k, k))
    for k, label, _ in CRITERIA:
        if scores[k] == 0:
            out.append(f"{label} scored 0: there is evidence it fails.")
    if v == "HOLD":
        low = [label for k, label, _ in CRITERIA if scores[k] <= 1 and k != "converts"]
        if scores["acv"] < 2 or scores["event_spend"] < 2:
            out.append("ACV and event spend both need at least indirect evidence before research is spent.")
        if low:
            out.append("Find one more public signal for: " + ", ".join(low) + ".")
    if v == "GO" and scores["converts"] <= 1:
        out.append("Characteristic 5 is unknown from outside, which is normal. The calculator lets them answer it.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k, label, _ in CRITERIA:
        ap.add_argument("--" + k.replace("_", "-"), type=int, choices=[0, 1, 2, 3], help=label)
    ap.add_argument("--from", dest="src", help="a JSON file with scores and disqualifiers")
    ap.add_argument("--disqualifier", action="append", default=[], choices=sorted(DISQUALIFIERS))
    ap.add_argument("--write", help="write the gate into this strategy.json")
    ap.add_argument("--notes", default="", help="one or two sentences on the evidence behind the scores")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    scores, dq, notes = {}, list(a.disqualifier), a.notes
    if a.src:
        g = json.loads(Path(a.src).read_text(encoding="utf-8"))
        g = g.get("gate", g)
        scores.update({k: int(v) for k, v in (g.get("scores") or {}).items()})
        dq += [d for d in g.get("disqualifiers") or [] if d not in dq]
        notes = notes or g.get("notes", "")
    for k, _, _ in CRITERIA:
        v = getattr(a, k)
        if v is not None:
            scores[k] = v
    missing = [k for k, _, _ in CRITERIA if k not in scores]
    if missing:
        ap.error("score every criterion: missing " + ", ".join(missing))
    bad = [d for d in dq if d not in DISQUALIFIERS]
    if bad:
        ap.error("unknown disqualifier: " + ", ".join(bad))
    v, total = verdict(scores, dq)
    why = reasons(scores, dq, v)
    result = {"verdict": v, "total": total, "scores": scores, "disqualifiers": dq, "notes": notes, "reasons": why}
    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Gate: {v}, {total} of 18\n")
        for k, label, why_k in CRITERIA:
            print(f"  {scores[k]}  {label:48} {why_k}")
        for d in dq:
            print(f"  DISQUALIFIER {d}: {DISQUALIFIERS[d]}")
        if why:
            print()
            for r in why:
                print(f"  - {r}")
        print({"GO": "\nResearch is earned. Initialise the workspace and start phase 1.",
               "HOLD": "\nNo research yet. Record the HOLD in the workspace log with what would change it.",
               "NO-GO": "\nStop. Record the NO-GO by prospect ID and do not approach this company with a strategy."}[v])
    if a.write:
        p = Path(a.write)
        st = json.loads(p.read_text(encoding="utf-8"))
        st["gate"] = {k: result[k] for k in ("verdict", "total", "scores", "disqualifiers", "notes")}
        p.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote the gate into {p}")
    return {"GO": 0, "HOLD": 3, "NO-GO": 4}[v]


if __name__ == "__main__":
    sys.exit(main())
