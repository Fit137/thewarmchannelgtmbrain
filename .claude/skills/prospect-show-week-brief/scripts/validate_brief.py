#!/usr/bin/env python3
"""Validate a show-week brief before it is built and sent.

    python3 validate_brief.py brief/brief.json --register evidence/evidence-register.md

Checks brief.json, schema twc.show-week-brief/1:

  Gate      the prospect passed the gate as GO or HOLD, with event spend at 2 or more
            and no disqualifier. A NO-GO gets nothing.
  One gift  the workspace log shows no earlier strategy, brief or deck sent without a
            reply. One approach per prospect: a second gift only after they answer.
  Timing    the show starts 3 to 12 weeks after the brief's date. Under 3 weeks there is
            nothing left to act on. Under 7, the suggestion must say plainly what the
            time allows. At 8 or more on a GO, the full strategy is the other option:
            choose one.
  The week  every day sits around the show's dates, every slot has a known part and
            kind, every slot but an open one cites the register, every open slot is
            backed by a register row recording where we looked, and open_as_of is set
            and recent, because an open evening fills.
  People    roles, never people: no speaker field, no name of an individual.
  Copy      no em or en dash, no banned word, no placeholder, no evidence ID or scaffold
            marker in copy, no frozen line, every [n] in sources, and every percentage
            or money figure traced to a cleared ledger row or a P0, P1 or P2 register row.
  The ask   one suggestion at a cleared attendance rate, its status said where it
            describes our work, and one real call to action.

ERROR blocks the build. WARN is for a person. Exit status 1 on any ERROR.
No third-party dependencies. Python 3.8 or later.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import _family  # noqa: F401
import validate_strategy as vs

PARTS = {"breakfast", "morning", "lunch", "afternoon", "evening", "late"}
KINDS = {"yours", "open", "session", "official", "competitor", "side", "partner"}
CLEARED_RATES = {0.70, 0.86, 0.19}
NOT_COPY = {"schema", "slug", "website", "url", "href", "ledger", "envelope", "gate", "path", "lang", "version",
            "date", "start", "end", "part", "kind", "evidence", "presence_evidence", "audience_evidence", "paper",
            "rate", "seats", "source_n", "id", "fictional", "basis", "before_you_send", "sources"}


def copy_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in NOT_COPY:
                continue
            yield from copy_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from copy_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def all_keys(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from all_keys(v)
    elif isinstance(o, list):
        for v in o:
            yield from all_keys(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brief")
    ap.add_argument("--register")
    ap.add_argument("--brain")
    ap.add_argument("--today", help="YYYY-MM-DD, for testing the freshness checks")
    a = ap.parse_args()
    E, W, I = [], [], []
    bp = Path(a.brief).resolve()
    b = json.loads(bp.read_text(encoding="utf-8"))
    brain = vs.find_brain(a.brain)
    if not vs.load_lists(brain):
        W.append("brain lint lists not loaded, using built-in copies")
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()

    def need(obj, keys, where):
        for k in keys:
            if (obj or {}).get(k) in (None, "", [], {}):
                E.append(f"{where}.{k} is missing")

    if b.get("schema") != "twc.show-week-brief/1":
        E.append(f"schema is {b.get('schema')!r}, expected twc.show-week-brief/1")
    need(b, ("prospect", "version", "date", "basis", "gate", "show", "headline", "days", "buyer_sessions",
             "suggestion", "cta", "sources", "before_you_send", "method"), "brief")
    need(b.get("prospect"), ("id", "company", "slug"), "prospect")
    need(b.get("show"), ("name", "start", "end", "presence", "presence_evidence"), "show")

    g = b.get("gate") or {}
    sc = g.get("scores") or {}
    if g.get("verdict") not in ("GO", "HOLD"):
        E.append(f"gate verdict is {g.get('verdict')!r}. A brief goes to a GO or a HOLD, never a NO-GO")
    if int(sc.get("event_spend", 0)) < 2:
        E.append("gate event_spend is under 2. A brief needs public evidence they are at the show")
    if g.get("disqualifiers"):
        E.append(f"gate disqualifiers present: {', '.join(g['disqualifiers'])}")

    log = bp.parent.parent / "log.md"
    if log.is_file():
        steps = [l for l in log.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
        sent = [l for l in steps if re.search(r"\bsent\b", l, re.I)]
        replied = [l for l in steps if re.search(r"\breplied\b", l, re.I)]
        if sent and not replied:
            E.append(f"the workspace log shows a gift already sent ({sent[-1].strip()[:80]}) and no reply. "
                     "One approach per prospect: a second gift only after they answer")

    try:
        date = dt.date.fromisoformat(b.get("date", ""))
        start = dt.date.fromisoformat((b.get("show") or {}).get("start", ""))
        end = dt.date.fromisoformat((b.get("show") or {}).get("end", ""))
    except ValueError:
        E.append("date, show.start and show.end must be YYYY-MM-DD")
        date = start = end = None
    sg = b.get("suggestion") or {}
    if date and start and end:
        weeks = (start - date).days / 7
        if end < start:
            E.append("show.end is before show.start")
        if weeks < 3:
            E.append(f"the show starts {weeks:.1f} weeks after the brief. Under 3 there is nothing left to act on: "
                     "log it and note the next edition instead")
        elif weeks < 7 and not sg.get("timing"):
            E.append(f"the show is {weeks:.1f} weeks away and suggestion.timing is empty. Say plainly what the time allows: "
                     "a full table takes about six weeks of individual approaches")
        if weeks > 12:
            W.append(f"the show is {weeks:.1f} weeks away. A brief this early goes stale: the open slots will change")
        if weeks >= 8 and g.get("verdict") == "GO":
            I.append("the show is 8 or more weeks away on a GO, so the full strategy is also possible. "
                     "One gift per prospect: choose one")
        if (today - date).days > 14:
            W.append(f"the brief is dated {date}, over two weeks ago. Re-read the week before sending")
        days = b.get("days") or []
        if len(days) < 2:
            E.append("days needs at least two days: the show's days, and the evening before where it matters")
        prev = None
        for i, day in enumerate(days):
            try:
                dd = dt.date.fromisoformat(day.get("date", ""))
            except ValueError:
                E.append(f"days[{i}].date must be YYYY-MM-DD")
                continue
            if not (start - dt.timedelta(days=3) <= dd <= end + dt.timedelta(days=2)):
                E.append(f"days[{i}] {dd} is outside the show week")
            if prev and dd <= prev:
                E.append(f"days[{i}] is out of order")
            prev = dd
            for j, s in enumerate(day.get("slots") or []):
                w = f"days[{i}].slots[{j}]"
                if s.get("part") not in PARTS:
                    E.append(f"{w}.part must be one of {', '.join(sorted(PARTS))}")
                if s.get("kind") not in KINDS:
                    E.append(f"{w}.kind must be one of {', '.join(sorted(KINDS))}")
                if not s.get("evidence"):
                    E.append(f"{w} has no evidence. Every slot, open ones included, cites where it was read")
                if not s.get("title"):
                    E.append(f"{w}.title is missing")
    if not b.get("open_slots"):
        W.append("no open slots. Say so plainly on the page: a week with nothing open changes the suggestion")
    as_of = b.get("open_as_of")
    if b.get("open_slots") and not as_of:
        E.append("open_as_of is missing. Open means nothing announced on public pages as of a date")
    if as_of:
        try:
            ad = dt.datetime.strptime(as_of, "%d %B %Y").date()
            if (today - ad).days > 7:
                W.append(f"open slots were read on {as_of}. Re-check them within a week of sending")
        except ValueError:
            E.append("open_as_of must read like 7 October 2026")
    rate = round(float(sg.get("rate", 0) or 0), 2)
    if rate not in CLEARED_RATES:
        E.append(f"suggestion.rate {rate} is not a cleared attendance rate (0.70, 0.86, 0.19)")
    if not 6 <= int(sg.get("seats", 0) or 0) <= 40:
        E.append("suggestion.seats must be 6 to 40")
    need(sg, ("title", "body", "source_n"), "suggestion")
    if re.search(r"\b(we|us|our)\b", (sg.get("body", "") + " " + sg.get("status", "")), re.I) and not sg.get("status"):
        E.append("suggestion.status is empty. Wherever our work is described, its status travels with it")
    if sg.get("status") and re.search(r"\bapproach", sg["status"], re.I) and not re.search(r"\bonce|until|opens\b", sg["status"], re.I):
        E.append("suggestion.status describes approaching guests without its status: it opens once our privacy position is written, D5")
    cta = b.get("cta") or {}
    if not cta.get("href") or "{TBD}" in cta.get("href", ""):
        E.append("cta.href is not set")
    elif ".example" in cta["href"]:
        W.append("cta.href uses a placeholder domain. Settle the real address before sending")
    for k in all_keys(b):
        if k in ("speaker", "speakers", "person", "name_of_person", "contact"):
            E.append(f"a {k!r} field. Roles, never people: name the session, never its speaker")

    reg = vs.register(Path(a.register)) if a.register else {}
    if a.register and not reg:
        E.append(f"no rows parsed from {a.register}")

    def walk_ids(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("evidence", "presence_evidence", "audience_evidence") and isinstance(v, list):
                    for e in v:
                        if reg and e not in reg:
                            E.append(f"{path}.{k} cites {e}, which is not in the register")
                        elif reg and reg[e]["kind"] in ("M-C", "NEW", "P3") and k != "evidence":
                            E.append(f"{path}.{k} cites {e}, a {reg[e]['kind']} row, which cannot carry a fact on the page")
                else:
                    walk_ids(v, f"{path}.{k}" if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk_ids(v, f"{path}[{i}]")
    walk_ids(b)

    srcs = {int(s["n"]) for s in b.get("sources") or [] if "n" in s}
    if sg.get("source_n") and int(sg["source_n"]) not in srcs:
        E.append(f"suggestion.source_n {sg['source_n']} has no entry in sources")
    ok = vs.cleared_tokens(brain) if brain else set()
    for r in reg.values():
        if r["kind"] in ("P0", "P1", "P2", "M-A", "M-B"):
            ok |= {(k, v) for k, v, _ in vs.tok(r["text"])}
    for path, s in copy_strings(b):
        for ch, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch in s:
                E.append(f"{path}: {name}")
        for w in vs.BANNED_WORDS:
            if re.search(r"\b" + re.escape(w), s, re.I):
                E.append(f"{path}: banned word '{w}'")
        if "{{" in s or re.search(r"\[WRITE", s):
            E.append(f"{path}: unfilled placeholder")
        if re.search(r"\[E\d+\]", s):
            E.append(f"{path}: an evidence ID inside copy")
        for m in re.finditer(r"\[(\d{1,2})\]", s):
            if int(m.group(1)) not in srcs:
                E.append(f"{path}: source reference [{m.group(1)}] has no entry in sources")
        for pat, why in vs.FROZEN:
            if re.search(pat, s, re.I if "The (List" not in pat else 0):
                if why.startswith("a guarantee") and re.search(r"\bno guarantee", s, re.I):
                    continue
                E.append(f"{path}: {why}: {s[:100]}")
        if re.search(r"\breply rates?\b", s, re.I):
            E.append(f"{path}: a reply rate, in a page that uses the 70% attendance benchmark")
        for kind, v, raw in vs.tok(s):
            if ok and (kind, v) not in ok:
                E.append(f"{path}: {raw} traces to no cleared ledger row and no P0, P1 or P2 register row")

    print(f"validate_brief {bp.name}: {len(reg)} register rows, brain {'found' if brain else 'NOT FOUND'}")
    for e in E:
        print(f"  ERROR {e}")
    for w in W:
        print(f"  WARN  {w}")
    for i in I:
        print(f"  INFO  {i}")
    print(f"\n{len(E)} error(s), {len(W)} warning(s)." + ("" if E else " Ready for build_brief.py."))
    return 1 if E else 0


if __name__ == "__main__":
    sys.exit(main())
