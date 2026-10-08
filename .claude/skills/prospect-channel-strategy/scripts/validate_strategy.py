#!/usr/bin/env python3
"""Validate a prospect strategy before it is handed to the deck builder.

    python3 validate_strategy.py strategy/strategy.json --register evidence/evidence-register.md
    python3 validate_strategy.py strategy/strategy.json --register evidence/evidence-register.md --profile lite

Checks strategy.json, schema twc.prospect-strategy/1, on four levels:

  Shape      every field the chosen deck profile needs is present and well formed:
             the prospect, the gate, the thesis, the footprint with one anchor, the
             committee, the channel, the questions, the invitation, the operating model,
             the economics, the engagement path, sources and before_you_send. Every
             phase that feeds a deck carries a full chapter: cover title and subtitle,
             claim, so-what, evidence, carry-forward, close title and body.
  Evidence   every evidence ID in the file exists in the register. Every [n] source
             reference in copy exists in sources. Every percentage and money figure in
             copy traces to a cleared ledger row or a P0, P1 or P2 register row.
  Copy       no em or en dash, no banned word, no unfilled placeholder, no evidence ID
             or scaffold marker inside copy, guest words only in the invitation, and the
             lines frozen by open decisions held in their safe form.
  Readiness  the gate says GO, the call to action is real, the questions are verified,
             and before_you_send names things individually.

ERROR blocks the handoff. WARN is for a person. Exit status 1 on any ERROR.
No third-party dependencies. Python 3.8 or later.
"""
import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

CHAPTER_KEYS = ("cover_title", "cover_subtitle", "claim", "so_what", "evidence", "carry", "close_title", "close_body")
BANNED_WORDS = ["leverage", "unlock", "seamless", "robust", "streamline", "cutting-edge", "cutting edge", "empower"]
GUEST_BANNED = [r"\blead generation\b", r"\bleads?\b", r"\bsales-qualified\b", r"\bSQLs?\b", r"\bMQLs?\b",
                r"\bpipeline\b", r"\bfunnel\b", r"\bconver(t|ts|ted|sion|sions)\b", r"\bclose rate\b", r"\bdeals?\b",
                r"\bprospects?\b", r"\btarget accounts?\b", r"\bnamed accounts?\b", r"\baccount list\b", r"\bin-ICP\b",
                r"\bICP\b", r"\bcomposed attendance\b", r"\baccess\b", r"\binventory\b", r"\bcoverage\b",
                r"\bshow rate\b", r"\battendance floor\b", r"\bchannel\b", r"\bclients?\b", r"\breply rates?\b"]
FROZEN = [
    (r"\bhand(ed|s|ing)? (it )?(over|off) to (your|the) (sellers|sales|reps?|team)\b|context of what was (actually )?said",
     "a hand-over mechanism, frozen until D11"),
    (r"\b(your|their|guest'?s?) details go to no one\b|\bnothing follows\b", "the frozen guest promise, D11"),
    (r"\bguarantee[sd]?\b(?! nothing)", "a guarantee, none until D4 and D10"),
    (r"\bwe charge\b|\bour (fee|fees|price|pricing|retainer)\b", "a price, none until D2"),
    (r"\bour (network|community|guest list|executives)\b", "a network claim"),
    (r"\bThe (List|Room|Channel)\b", "a retired scope name"),
    (r"\b(clients?|customers?) (include|like|such as)\b|\btrusted by\b", "a proof claim, the proof set is empty"),
    (r"\bfounder[- ](led|delivered|hosted|facilitated)\b", "founder attendance, open at D7"),
]
TOKEN = re.compile(r"(?P<money>(?:CA|US|C|A)?[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:k|K|M|million|billion)\b)?)"
                   r"|(?P<pct>(?<![\w.])\d[\d,]*(?:\.\d+)?\s?%)")


def find_brain(arg):
    cands = [Path(arg)] if arg else []
    if os.environ.get("TWC_BRAIN"):
        cands.append(Path(os.environ["TWC_BRAIN"]))
    cands += list(Path(__file__).resolve().parents) + [Path.cwd() / ".." / "thewarmchannelgtmbrain"]
    for c in cands:
        if (c / "rules" / "evidence-ledger.md").is_file():
            return c.resolve()
    return None


def load_lists(brain):
    global BANNED_WORDS, GUEST_BANNED
    lint = brain / "scripts" / "lint_claims.py" if brain else None
    if lint and lint.is_file():
        try:
            spec = importlib.util.spec_from_file_location("twc_lint_claims", str(lint))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            BANNED_WORDS, GUEST_BANNED = list(mod.BANNED_WORDS), list(mod.GUEST_BANNED)
            return True
        except Exception:
            return False
    return False


def tok(text):
    out = set()
    for m in TOKEN.finditer(text or ""):
        raw = m.group(0)
        v = float(re.search(r"\d[\d,]*(?:\.\d+)?", raw).group(0).replace(",", ""))
        if m.lastgroup == "money" and re.search(r"(k|K)\b", raw):
            v *= 1e3
        if m.lastgroup == "money" and re.search(r"(M|million)\b", raw):
            v *= 1e6
        out.add((m.lastgroup, round(v, 6), raw.strip()))
    return out


def cleared_tokens(brain):
    toks, section = set(), ""
    for line in (brain / "rules" / "evidence-ledger.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:]
        elif line.startswith("|") and section.lower().startswith("cleared"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and re.search(r"\b[AB]\b", cells[-1]):
                toks |= {(k, v) for k, v, _ in tok(cells[1])}
    return toks


def register(path):
    rows, header = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*:?-", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        low = [c.lower() for c in cells]
        if "id" in low and "kind" in low:
            header = low
            continue
        if header and re.match(r"^E\d+$", cells[0]) and "why it is out" not in header:
            r = dict(zip(header, cells))
            rows[cells[0]] = {"kind": r.get("kind", "").upper().replace(" ", ""), "text": " ".join(cells[1:])}
    return rows


def strings(o, path=""):
    """Every copy string in the strategy, with its path. Evidence arrays and ids are not copy."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("evidence", "priorities_evidence") and isinstance(v, list) and all(re.match(r"^E\d+$", str(x)) for x in v):
                continue  # evidence IDs, not copy. A chapter's evidence lines are copy and are checked
            if k in ("priorities_evidence", "id", "moment", "around", "fits", "same_as", "keep_on_calendar",
                     "schema", "slug", "website", "url", "href", "ledger", "envelope", "gate", "path", "kind", "role",
                     "date", "mode", "version", "lang", "currency", "brain_commit", "label_pos"):
                continue
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("strategy")
    ap.add_argument("--register")
    ap.add_argument("--profile", choices=["full", "lite"], default="full")
    ap.add_argument("--brain")
    a = ap.parse_args()
    E, W = [], []
    st = json.loads(Path(a.strategy).read_text(encoding="utf-8"))
    brain = find_brain(a.brain)
    if not load_lists(brain):
        W.append("brain lint lists not loaded, using built-in copies")
    lite = a.profile == "lite"

    def need(obj, keys, where):
        for k in keys:
            v = (obj or {}).get(k)
            if v in (None, "", [], {}):
                E.append(f"{where}.{k} is missing")

    if st.get("schema") != "twc.prospect-strategy/1":
        E.append(f"schema is {st.get('schema')!r}, expected twc.prospect-strategy/1")
    need(st, ("prospect", "version", "mode", "date", "basis", "gate", "thesis", "footprint", "channel", "economics",
              "engagement", "sources", "before_you_send"), "strategy")
    need(st.get("prospect"), ("id", "company", "slug", "website", "what_they_sell", "who_they_sell_to"), "prospect")
    if st.get("mode") not in ("BUILD", "UPGRADE", "REFRESH"):
        E.append(f"mode {st.get('mode')!r} is not BUILD, UPGRADE or REFRESH")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(st.get("date", ""))):
        E.append("date must be YYYY-MM-DD")
    if not re.match(r"^PX-\d{4}$", str((st.get("prospect") or {}).get("id", ""))):
        W.append("prospect.id should be a pipeline ID like PX-0007. The pipeline holds IDs, never names of people")
    g = st.get("gate") or {}
    if g.get("verdict") != "GO":
        E.append(f"gate verdict is {g.get('verdict')!r}. A strategy is only handed to the deck builder on GO")
    need(st.get("thesis"), ("headline", "standfirst", "carrying_line"), "thesis")

    phases = ["footprint", "channel", "economics", "engagement"] + ([] if lite else ["buyers", "operating"])
    for ph in phases:
        need(st.get(ph), ("chapter",), ph)
        ch = (st.get(ph) or {}).get("chapter") or {}
        need(ch, CHAPTER_KEYS, f"{ph}.chapter")
        if ch.get("evidence") and not isinstance(ch["evidence"], list):
            E.append(f"{ph}.chapter.evidence must be a list of lines")

    fp = st.get("footprint") or {}
    ms = fp.get("moments") or []
    if len(ms) < 2:
        E.append("footprint.moments needs at least two moments. A thin footprint is a HOLD, not a deck")
    ids = [m.get("id") for m in ms]
    if len(set(ids)) != len(ids):
        E.append("footprint.moments ids are not unique")
    anchors = [m for m in ms if m.get("anchor")]
    if len(anchors) != 1:
        E.append(f"footprint needs exactly one anchor moment, has {len(anchors)}")
    for m in ms:
        w = f"footprint.moments[{m.get('id')}]"
        need(m, ("id", "name", "kind", "month", "today"), w)
        if not 1 <= int(m.get("month", 0)) <= 12:
            E.append(f"{w}.month must be 1 to 12")
        if not 1 <= int(m.get("week", 2)) <= 4:
            E.append(f"{w}.week must be 1 to 4")
        for axis in ("density", "access"):
            v = m.get(axis)
            if v is not None and not -20 <= float(v) <= 20:
                E.append(f"{w}.{axis} must sit between -20 and 20")
        if m.get("density") is not None and float(m["density"]) == int(float(m["density"])) and not m.get("same_as"):
            W.append(f"{w}: scores are read to one decimal, for example 7.3, not round numbers")
        if not m.get("evidence") and not m.get("same_as"):
            E.append(f"{w} has no evidence. Every moment on the calendar is a public record")
    q = fp.get("quadrant") or {}
    need(q, ("title", "names", "x_label", "y_label", "basis"), "footprint.quadrant")
    if q.get("names") and len(q["names"]) != 4:
        E.append("footprint.quadrant.names needs four names: top right, top left, bottom left, bottom right")
    mids = set(ids)
    ch = st.get("channel") or {}
    for c in ch.get("choices") or []:
        if c.get("moment") not in mids:
            E.append(f"channel.choices names moment {c.get('moment')!r}, which is not in the footprint")
    decided = {c.get("moment") for c in ch.get("choices") or []}
    for m in ms:
        if not m.get("same_as") and m.get("id") not in decided:
            W.append(f"moment {m.get('id')} ({m.get('name')}) has no decision in channel.choices. Every moment gets one")
    for k in ch.get("keep_on_calendar") or []:
        if k not in mids:
            E.append(f"channel.keep_on_calendar names {k!r}, which is not in the footprint")
    if not ch.get("calendar"):
        E.append("channel.calendar is empty. The plan needs proposed moments")
    if not lite:
        b = st.get("buyers") or {}
        if not 2 <= len(b.get("committee") or []) <= 4:
            E.append("buyers.committee needs two to four roles")
        for r in b.get("committee") or []:
            if re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", r.get("role", "")) and not r.get("role", "").startswith("The "):
                W.append(f"buyers.committee role {r.get('role')!r} looks like a person's name. Roles, never people")
        qs = st.get("questions") or []
        if len(qs) < 2:
            E.append("questions needs at least two candidate questions")
        for x in qs:
            if not x.get("evidence"):
                W.append(f"question {x.get('label')!r} is not verified as live. Verify it or cut it before sending")
        need(st.get("invitation"), ("subject", "body"), "invitation")
        op = st.get("operating") or {}
        need(op, ("arithmetic", "six_weeks", "after", "measures"), "operating")
    op = st.get("operating") or {}
    ar = op.get("arithmetic") or {}
    for f in ar.get("formats") or []:
        if not 0 < float(f.get("rate", 0)) <= 1:
            E.append(f"operating.arithmetic format {f.get('label')!r}: rate must be a fraction, 0.70 not 70")
    after = " ".join(str(v) for v in (op.get("after") or {}).values())
    if after and not re.search(r"\bchoose|chose|consent", after, re.I):
        E.append("operating.after must carry the consent framing: the conversation continues only with guests who choose it")
    if after and not re.search(r"designed with you|not offered|until", after, re.I):
        E.append("operating.after must say the step is designed with the client and not offered until settled, D11")
    eco = st.get("economics") or {}
    calc = eco.get("calculator") or {}
    for k in ("deal", "close", "investment", "conversations"):
        if k not in (calc.get("inputs") or ["deal", "close", "investment", "conversations"]):
            E.append(f"economics.calculator must ask for {k}")
    if calc.get("prefill"):
        if st.get("mode") == "BUILD":
            E.append("economics.calculator carries prefilled values. BUILD mode never supplies a number for the prospect")
        elif not calc.get("prefill_note"):
            E.append("economics.calculator.prefill needs prefill_note: who supplied the numbers, by role, and when")
    eng = st.get("engagement") or {}
    need(eng, ("steps", "next_step", "cta"), "engagement")
    cta = eng.get("cta") or {}
    if not cta.get("href") or "{TBD}" in cta.get("href", ""):
        E.append("engagement.cta.href is not set")
    elif ".example" in cta.get("href", ""):
        W.append("engagement.cta.href uses a placeholder domain. Settle the real address before sending")
    for s in eng.get("steps") or []:
        lab = (s.get("label", "") + " " + s.get("line", "")).lower()
        if re.search(r"fill|approach|outreach|follow", lab) and not s.get("status"):
            E.append(f"engagement step {s.get('label')!r} describes a capability that is not READY and carries no status")

    srcs = {int(s["n"]) for s in st.get("sources") or [] if "n" in s}
    for s in st.get("sources") or []:
        if not s.get("url") and not s.get("ledger"):
            W.append(f"source {s.get('n')} has neither an address nor a ledger row")
    reg = register(Path(a.register)) if a.register else {}
    if a.register and not reg:
        E.append(f"no rows parsed from {a.register}")
    ok_tokens = cleared_tokens(brain) if brain else set()
    for r in reg.values():
        if r["kind"] in ("P0", "P1", "P2", "M-A", "M-B"):
            ok_tokens |= {(k, v) for k, v, _ in tok(r["text"])}

    def walk_ids(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("evidence", "priorities_evidence") and isinstance(v, list) and all(re.match(r"^E\d+$", str(x)) for x in v):
                    for e in v:
                        if reg and e not in reg:
                            E.append(f"{path}.{k} cites {e}, which is not in the register")
                        elif reg and reg[e]["kind"] in ("M-C", "NEW"):
                            E.append(f"{path}.{k} cites {e}, a {reg[e]['kind']} row, which never supports a claim")
                else:
                    walk_ids(v, f"{path}.{k}" if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk_ids(v, f"{path}[{i}]")
    walk_ids(st)

    for path, s in strings(st):
        for ch_, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch_ in s:
                E.append(f"{path}: {name}")
        for w in BANNED_WORDS:
            if re.search(r"\b" + re.escape(w), s, re.I):
                E.append(f"{path}: banned word '{w}'")
        if "{{" in s:
            E.append(f"{path}: unfilled placeholder")
        if re.search(r"\[E\d+\]", s):
            E.append(f"{path}: an evidence ID inside copy. IDs go in evidence arrays, never in words the prospect reads")
        if re.search(r"\[WRITE", s):
            E.append(f"{path}: unwritten scaffold marker")
        for m in re.finditer(r"\[(\d{1,2})\]", s):
            if int(m.group(1)) not in srcs:
                E.append(f"{path}: source reference [{m.group(1)}] has no entry in sources")
        for pat, why in FROZEN:
            if re.search(pat, s, re.I if "The (List" not in pat else 0):
                if why.startswith("a guarantee") and re.search(r"\bno guarantee", s, re.I):
                    continue
                E.append(f"{path}: {why}: {s[:100]}")
        if path.startswith(("sources", "before_you_send", "fictional", "basis", "gate", "landscape", "account")):
            continue
        for kind, v, raw in tok(s):
            if ok_tokens and (kind, v) not in ok_tokens:
                E.append(f"{path}: {raw} traces to no cleared ledger row and no P0, P1 or P2 register row")
    inv = st.get("invitation") or {}
    for k in ("subject", "body"):
        for pat in GUEST_BANNED:
            m = re.search(pat, inv.get(k, ""), re.I)
            if m:
                E.append(f"invitation.{k}: client word '{m.group(0)}' in guest copy")
    bys = st.get("before_you_send") or {}
    for k in ("verified", "needs_settling", "designed_not_supplied"):
        if not bys.get(k):
            E.append(f"before_you_send.{k} is empty. Name things individually")
    print(f"validate_strategy {Path(a.strategy).name}: profile {a.profile}, {len(reg)} register rows, "
          f"brain {'found' if brain else 'NOT FOUND'}")
    for e in E:
        print(f"  ERROR {e}")
    for w in W:
        print(f"  WARN  {w}")
    print(f"\n{len(E)} error(s), {len(W)} warning(s)." + ("" if E else " Ready for new_deck.py."))
    return 1 if E else 0


if __name__ == "__main__":
    sys.exit(main())
