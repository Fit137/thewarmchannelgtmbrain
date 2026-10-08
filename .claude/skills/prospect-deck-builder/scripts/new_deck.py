#!/usr/bin/env python3
"""Scaffold deck.json from a finished prospect strategy (strategy.json).

    python3 new_deck.py ../strategy/strategy.json --out deck.json
    python3 new_deck.py ../strategy/strategy.json --profile lite --out deck.json

Two profiles:
  full   the home layer and six decks, A to F, about 37 slides. The default for a
         priority prospect who passed the gate with a clear GO.
  lite   the home layer and four decks, A, C, E and a short F, about 20 slides. For a
         HOLD that became a GO, or when the footprint is thin.

Every word that the strategy already settled is carried across verbatim. Market
slides that every deck shares (the attendance benchmark, the arithmetic, the budget
line) are written from the strategy's ledger-backed figures. Anything the scaffold
cannot know is written as a [WRITE ...] marker: build_deck.py builds with it and warns,
and deck_check.py fails until every marker is replaced. Presenter notes are left
empty on purpose: they are written by hand, at about 2.5 words a second, sharing no
sentence with the screen.

Refuses to overwrite an existing deck.json unless --force, because a deck.json is
edited by hand after the scaffold.

No third-party dependencies. Python 3.8 or later.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
         "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

DESIGN_GLOBAL = {
    "register": "A calm, exact briefing for an accountable marketing leader. Objects move like documents being laid on a table: they arrive, settle and stop. Nothing loops except the motif's slow turn, which is the one thing alive at rest.",
    "easing": "One curve for the whole file, a decelerating ease out. Entry motion 560ms, slide change 520ms, line draws 900ms. Stagger 110ms to 160ms between siblings.",
    "rig": "Real 3D only on the motif: a plane tilted 52 degrees back, marks lifted 30px toward the viewer when lit, perspective 1700px from slightly above. No 3D on charts or tables.",
    "interaction": "Four interactions in the whole file: the motif tilts a few degrees with the pointer on centrepieces, the arithmetic slider and format select, the calculator fields, and the slide rail. Every interaction has a keyboard path.",
    "motif": "The named-account ring. A ring of small marks, one per account, around an empty centre. Four states: scattered (cold channels), ringed (the named list), lit (the accounts in the room, lifted and in the accent role, the plane tilted like a table), connected (thin lines from the centre to the lit marks). Never labelled, never counted, never explained on screen.",
    "constraints": "Single self-contained file. No network requests, no libraries. Tabular figures on every numeral. Reduced motion ships the resolved end state. Print path stacks the home layer and every slide.",
    "accessibility": "Text contrast at least 4.5 to 1 against its surface. Every chart carries an accessible name. The live region announces deck, slide and title on every change.",
}


def design_quadrant(anchor):
    return {
        "stage": "Full-width chart on the surface role, axes in the ink role, quadrant names in the muted role.",
        "hero": f"The {anchor} point, in the accent role with a halo.",
        "entry": f"Axes are present on arrival. Points scale from 0.4 to 1 and fade in, 140ms apart, {anchor} last so the eye lands on it.",
        "ambient": "None. A chart that moves at rest asks to be re-read.",
        "interaction": "None. Every label is printed, nothing hides behind a hover.",
        "restraint": "No 3D tilt. Perspective would distort position, and position is the claim.",
        "reduced": "Points present at full size on arrival.",
    }


DESIGN_STILL = {
    "stage": "The line alone on the surface role, nothing else on the slide.",
    "hero": "The sentence.",
    "entry": "The sentence fades in once, 560ms. Nothing follows it.",
    "ambient": "None. This is the deliberately still slide before the biggest moment.",
    "interaction": "None.",
    "restraint": "No motif, no figure, no motion after arrival. Stillness is what makes the next slide land.",
    "reduced": "Identical.",
}
DESIGN_TIMELINE = {
    "stage": "Twelve-month strip on the surface role, month rules in the rule role.",
    "hero": "The proposed tables in the accent role, each with its hatched outreach window.",
    "entry": "Existing moments present on arrival, then dim to the muted role after 900ms. Outreach windows draw left to right, 900ms each, 120ms apart. Proposed tables pop in as each window completes.",
    "ambient": "None.",
    "interaction": "None.",
    "restraint": "Existing moments dim but never disappear: the plan keeps them, and erasing them would contradict the slide.",
    "reduced": "Everything present, existing moments already dimmed, windows fully drawn.",
}
DESIGN_ARITH = {
    "stage": "Blocks in a row on the surface role, each topped with an ink rule, the last with an accent rule.",
    "hero": "The confirmations figure, which changes as the slider moves.",
    "entry": "Blocks fade up left to right, 160ms apart. The controls arrive last at 900ms.",
    "ambient": "None.",
    "interaction": "The slider sets people in the room from 6 to 40. The select switches the format. Confirmations recompute instantly as people divided by the attendance rate, rounded to the nearest whole person.",
    "restraint": "No count-up on recompute. A number that animates while someone drags reads as a slot machine.",
    "reduced": "Identical, the recompute is already instant.",
}
DESIGN_CONNECTED = {
    "stage": "Text left, the motif right on its tilted plane.",
    "hero": "Thin accent lines drawing from the empty centre to the lit marks.",
    "entry": "Marks travel from scattered to the ring, 22ms apart, then the lit marks lift and turn to the accent role at 900ms, the centre appears at 1200ms, and the lines draw at 1500ms, 40ms apart.",
    "ambient": "The plane turns one revolution every 140 seconds. Alive at rest, never busy.",
    "interaction": "The plane tilts up to 4 degrees with the pointer.",
    "restraint": "Lines run only to lit marks. Drawing a line to every mark would claim that every guest continues, which is the opposite of the slide.",
    "reduced": "Ring, lit marks, centre and lines all present, no turn, no tilt.",
}
DESIGN_CALC = {
    "stage": "Fields left on the surface role, results right.",
    "hero": "The return figure, in the accent role when it pays back and the flag role when it does not.",
    "entry": "Fields fade up 110ms apart. Results stay hidden until the four required fields hold numbers.",
    "ambient": "None. People are typing.",
    "interaction": "Results recompute on every keystroke. Money fields format with separators when the field loses focus.",
    "restraint": "No defaults, no example values, no count-up. A result built from our numbers would be a claim we cannot support.",
    "reduced": "Identical.",
}

todo = []


def w(n, cap=False):
    s = WORDS[n] if 0 <= n < len(WORDS) else str(n)
    return s[0].upper() + s[1:] if cap else s


def need(value, what):
    """Carry a settled value across, or leave a marker the check will catch."""
    if value:
        return value
    todo.append(what)
    return f"[WRITE {what}]"


def src_n(strategy, ledger_row):
    for s in strategy.get("sources") or []:
        rows = [x.strip() for x in str(s.get("ledger", "")).split(",")]
        if ledger_row in rows:
            return int(s["n"])
    todo.append(f"a source entry for ledger row {ledger_row}")
    return None


def refmark(n):
    return f" [{n}]" if n else ""


def cover(ch, motif=None):
    s = {"layout": "cover", "title": need(ch.get("cover_title"), "cover title"),
         "subtitle": need(ch.get("cover_subtitle"), "cover subtitle"), "notes": "", "seconds": 0}
    if motif:
        s["motif"] = motif
    return s


def close(ch):
    return {"layout": "close", "title": need(ch.get("close_title"), "close title, returning to the cover"),
            "body": need(ch.get("close_body"), "close body, one line into the next deck"), "notes": "", "seconds": 0}


def moment_map(st):
    return {m["id"]: m for m in (st.get("footprint") or {}).get("moments", [])}


def deck_a(st, short):
    fp = st.get("footprint") or {}
    ch = fp.get("chapter") or {}
    moments = fp.get("moments") or []
    distinct = {m.get("same_as") or m["id"] for m in moments}
    items = [{"label": m["name"], "month": int(m["month"]), "week": int(m.get("week", 2)), "kind": "existing"} for m in moments]
    pts, seen = [], set()
    anchor_name = None
    for m in moments:
        key = m.get("same_as") or m["id"]
        if key in seen or m.get("density") is None or m.get("access") is None:
            continue
        seen.add(key)
        p = {"label": m.get("map_label") or m["name"], "x": float(m["density"]), "y": float(m["access"])}
        if m.get("anchor"):
            p["anchor"] = True
            anchor_name = p["label"]
        if m.get("label_pos"):
            p["label_pos"] = m["label_pos"]
        pts.append(p)
    pts.sort(key=lambda p: 1 if p.get("anchor") else 0)  # anchor drawn last, so the eye lands on it
    q = fp.get("quadrant") or {}
    clutch = src_n(st, "11")
    slides = [
        cover(ch, "ringed"),
        {"layout": "timeline", "title": need(fp.get("timeline_title"), f"timeline claim, for example: {w(len(distinct), True)} moments a year put {short} in the same building as its buyers"),
         "start_month": int(fp.get("start_month", 1)), "window_weeks": 0, "items": items,
         "legend_existing": f"Public moments in {short}'s year",
         "note": "Read from public pages only. Your internal calendar will have more.", "notes": "", "seconds": 0},
        {"layout": "quadrant", "title": need(q.get("title"), "quadrant claim, read from where the anchor sits"),
         "centrepiece": True, "x_label": q.get("x_label", "New buyers in the room"), "y_label": q.get("y_label", "Time across a table"),
         "quadrants": q.get("names") or ["Build on", "Keep for customers", "Reconsider", "Wrap with a private programme"],
         "range": q.get("range", [-20, 20]), "points": pts,
         "note": q.get("basis") or "Positions are our reading of public information, not measurement.",
         "design": design_quadrant(anchor_name or "anchor"), "notes": "", "seconds": 0},
        {"layout": "figure", "title": "What a registration is worth depends on the format",
         "figures": [{"value": "19%", "caption": f"of registrants attend vendor-owned conferences{refmark(clutch)}", "muted": True},
                     {"value": "70%", "caption": f"of registrants attend invite-only executive dinners{refmark(clutch)}"}],
         "body": "Both are free to attend and aimed at senior B2B buyers. The format decides who turns up.", "notes": "", "seconds": 0},
        {"layout": "statement", "title": need(fp.get("anchor_line"), "anchor line: where the buyers are, and why the current format does not reach them"),
         "body": need(fp.get("anchor_body"), "anchor body, one or two sentences"), "notes": "", "seconds": 0},
        close(ch),
    ]
    if not anchor_name:
        todo.append("an anchor moment in the footprint (one moment with anchor: true)")
    return {"key": "a", "name": "What you already fund", "source": "Strategy phases 1 and 2", "slides": slides}, ch


def deck_b(st, short):
    b = st.get("buyers") or {}
    ch = b.get("chapter") or {}
    comm = b.get("committee") or []
    if len(comm) > 4:
        todo.append("the committee has more than four roles: the slide shows the first four, cut or merge")
    pts = [{"label": c["role"], "line": c.get("line", "")} for c in comm[:4]]
    if len(pts) < 2:
        todo.append("at least two committee roles")
    tiers = b.get("tiers") or []
    slides = [
        cover(ch),
        {"layout": "points", "title": b.get("committee_title") or "The committee you sell to, and why each one would come",
         "points": pts, "notes": "", "seconds": 0},
        {"layout": "motif", "title": "Cold channels reach your buyers one at a time", "state": "scattered",
         "body": "Each approach lands alone, in an inbox every other vendor is also writing to. A table puts one question in front of several of them at once.",
         "notes": "", "seconds": 0},
        {"layout": "motif", "title": "Your named accounts are the list. The channel starts from it, not from a rented audience.", "state": "ringed",
         "body": "Every name in the room starts as a name on your account list. You see who will be approached before anyone is contacted.",
         "notes": "", "seconds": 0},
        {"layout": "table", "title": f"{w(len(tiers), True)} tiers of accounts, and the number only your list can tell us",
         "columns": ["Tier", "Who", "Accounts", "What the room is for"],
         "rows": [[t["tier"], t.get("who", ""), t.get("accounts", "{TBD}"), t.get("room_for", "")] for t in tiers],
         "highlight_row": 0, "note": b.get("list_note") or "Account counts are left blank on purpose. A full coverage read on your named list fills them in.",
         "notes": "", "seconds": 0},
        close(ch),
    ]
    return {"key": "b", "name": "Who has to be in the room", "source": "Strategy phase 3", "slides": slides}, ch


def deck_c(st, short, lite=False):
    c = st.get("channel") or {}
    ch = c.get("chapter") or {}
    mm = moment_map(st)
    choices = c.get("choices") or []
    rows = [[mm.get(x["moment"], {}).get("map_label") or mm.get(x["moment"], {}).get("name", x["moment"]),
             x.get("today") or mm.get(x["moment"], {}).get("today", ""), x.get("recommendation", "")] for x in choices]
    existing = [{"label": mm[i]["name"], "month": int(mm[i]["month"]), "week": int(mm[i].get("week", 2)), "kind": "existing"}
                for i in c.get("keep_on_calendar") or [] if i in mm]
    proposed = [{"label": x["label"], "month": int(x["month"]), "week": int(x.get("week", 2)), "kind": "proposed"}
                for x in c.get("calendar") or []]
    formats = c.get("formats") or []
    qs = st.get("questions") or []
    slides = [
        cover(ch, "lit" if lite else None),
        {"layout": "table", "title": f"{w(len(rows), True)} choices, one per moment you already fund",
         "columns": ["Moment", "Today", "Recommendation"], "rows": rows, "highlight_row": 0, "notes": "", "seconds": 0},
    ]
    if not lite:
        slides.append({"layout": "points", "title": f"{w(len(formats), True)} kinds of table, chosen from what each moment can carry",
                       "points": [{"label": f["name"], "line": f.get("line", "")} for f in formats[:4]], "notes": "", "seconds": 0})
    slides += [
        {"layout": "statement", "title": st.get("thesis", {}).get("carrying_line") or need(None, "the carrying line"),
         "still": True, "design": dict(DESIGN_STILL), "notes": "", "seconds": 0},
        {"layout": "timeline", "title": c.get("timeline_title") or "Your year, rebuilt around the moments you already fund",
         "centrepiece": True, "dim_existing": True, "start_month": int((st.get("footprint") or {}).get("start_month", 1)),
         "window_weeks": int(c.get("window_weeks", 6)), "items": existing + proposed,
         "legend_existing": "What you fund today", "legend_proposed": "Proposed tables",
         "legend_window": f"{w(int(c.get('window_weeks', 6)), True)}-week outreach window",
         "note": c.get("calendar_note") or "Placements are a proposal.", "design": dict(DESIGN_TIMELINE), "notes": "", "seconds": 0},
    ]
    if not lite and qs:
        slides.append({"layout": "points", "title": f"{w(len(qs[:4]), True)} questions your buyers would give up an evening for",
                       "points": [{"label": x["label"], "line": x["question"]} for x in qs[:4]],
                       "body": st.get("questions_note") or "Each question would be verified as live before any invitation goes out. The host never chooses the question.",
                       "notes": "", "seconds": 0})
        unverified = [x["label"] for x in qs if not x.get("evidence")]
        if unverified:
            todo.append(f"verify these questions as live before sending, or cut them: {', '.join(unverified)}")
    if lite:
        slides += deck_d_core(st, lite=True)
    slides.append(close(ch))
    return {"key": "c", "name": "Run it as a channel", "source": "Strategy phases 5 and 6", "slides": slides}, ch


def arith_title(op):
    ar = op.get("arithmetic") or {}
    seats = int(ar.get("seats", 12))
    fm = ar.get("formats") or [{"rate": 0.70}]
    conf = int(seats / float(fm[0]["rate"]) + 0.5)
    return f"{w(seats, True)} seats needs about {w(conf)} confirmations. The format sets the arithmetic."


def deck_d_core(st, lite=False):
    op = st.get("operating") or {}
    ar = op.get("arithmetic") or {}
    after = op.get("after") or {}
    slides = [
        {"layout": "arithmetic", "title": op.get("arithmetic_title") or arith_title(op), "centrepiece": True,
         "interactive": {"seats": int(ar.get("seats", 12)), "min": 6, "max": 40, "ref": ar.get("source_n") or src_n(st, "11"),
                         "formats": [{"label": f["label"], "rate": float(f["rate"])} for f in ar.get("formats") or []],
                         "slider_label": "People in the room", "select_label": "Format"},
         "steps": [{"value": ar.get("approached", "{TBD}"), "label": ar.get("approached_label", "people approached, set by the coverage read on your list")}],
         "note": ar.get("note") or "Attendance rates are the Clutch Events category benchmark, not our performance.",
         "design": dict(DESIGN_ARITH), "notes": "", "seconds": 0},
        {"layout": "motif", "title": need(after.get("title"), "the after-the-evening claim, in the consent framing"),
         "state": "connected", "centrepiece": True,
         "body": need(after.get("body"), "the after-the-evening body: only guests who choose it, designed with the client, not offered until settled"),
         "design": dict(DESIGN_CONNECTED), "notes": "", "seconds": 0},
    ]
    return slides


def deck_d(st, short):
    op = st.get("operating") or {}
    ch = op.get("chapter") or {}
    inv = st.get("invitation") or {}
    core = deck_d_core(st)
    ww = int((st.get("channel") or {}).get("window_weeks", 6))
    slides = [
        cover(ch),
        core[0],
        {"layout": "steps", "title": f"{w(ww, True)} weeks of individual work stand behind every table",
         "steps": [{k: v for k, v in s.items() if v} for s in op.get("six_weeks") or []], "notes": "", "seconds": 0},
        {"layout": "invitation", "title": "How your guests would hear about it",
         "subject": need(inv.get("subject"), "invitation subject, guest vocabulary"),
         "body": need(inv.get("body"), "invitation body, guest vocabulary only"),
         "note": inv.get("note") or "A sample in the language your guests would read. It never describes them as a target.",
         "notes": "", "seconds": 0},
        core[1],
        {"layout": "table", "title": op.get("measures_title") or "Report it the way finance reads it",
         "columns": ["Measure", "What it counts", "Target"],
         "rows": [[m["measure"], m.get("counts", ""), m.get("target", "{TBD}")] for m in op.get("measures") or []],
         "note": op.get("measures_note") or "The report format is in development. Targets are set with you, from your own numbers.",
         "notes": "", "seconds": 0},
        close(ch),
    ]
    return {"key": "d", "name": "How a room fills, and what happens after", "source": "Strategy phases 6 and 7", "slides": slides}, ch


def deck_e(st, short, lite=False):
    e = st.get("economics") or {}
    ch = e.get("chapter") or {}
    bl = e.get("budget_line") or {}
    sc = e.get("scan_cost") or {}
    opt = e.get("options") or {}
    calc = e.get("calculator") or {}
    n_bl = bl.get("source_n") or src_n(st, "new")
    n_sc = sc.get("source_n") or src_n(st, "5")
    slides = [
        cover(ch),
        {"layout": "figure", "title": "The trade show line is the largest in the exhibitor budget",
         "figures": [{"value": bl.get("value", "40.8%"),
                      "caption": (bl.get("caption") or "of exhibitor marketing budgets goes to trade show exhibiting, the largest single line") + refmark(n_bl)}],
         "notes": "", "seconds": 0},
    ]
    if not lite:
        slides += [
            {"layout": "arithmetic", "title": "Your cost per badge scan is a number you already have",
             "steps": [{"value": "{TBD}", "label": sc.get("theirs_label", "badge scans from your last show")},
                       {"value": sc.get("benchmark", "$112 to $300"), "label": sc.get("benchmark_label", "cost per scan, the industry benchmark") + refmark(n_sc)},
                       {"value": "{TBD}", "label": sc.get("cost_label", "what those scans cost you, from your own budget")}],
             "note": sc.get("note") or "We do not estimate your spend. Your own number outranks any benchmark.", "notes": "", "seconds": 0},
            {"layout": "comparison", "title": opt.get("title") or "Three ways to spend the same budget",
             "columns": opt.get("columns") or [], "highlight_col": opt.get("highlight", 2), "rows": opt.get("rows") or [],
             "notes": "", "seconds": 0},
        ]
    slides += [
        {"layout": "calculator", "title": "Run the arithmetic on your own numbers", "centrepiece": True, "calc_id": "roi",
         "inputs": calc.get("inputs") or ["deal", "close", "investment", "conversations", "cac"],
         "currency": calc.get("currency") or (st.get("prospect") or {}).get("currency", "$"),
         "intro": calc.get("intro") or "Every number is yours. We do not supply a close rate, because we do not know yours.",
         **({"prefill": calc["prefill"], "prefill_note": calc.get("prefill_note") or need(None, "prefill_note naming who supplied the numbers and when")}
            if calc.get("prefill") and st.get("mode") != "BUILD" else {}),
         "design": dict(DESIGN_CALC), "notes": "", "seconds": 0},
        close(ch),
    ]
    return {"key": "e", "name": "The economics", "source": "Strategy phase 8", "slides": slides}, ch


def deck_f(st, short, lite=False):
    g = st.get("engagement") or {}
    ch = g.get("chapter") or {}
    opt = g.get("options") or {}
    nx = g.get("next_step") or {}
    slides = [cover(ch)]
    if not lite:
        slides.append({"layout": "comparison", "title": opt.get("title") or "Who carries the six weeks is the real decision",
                       "columns": opt.get("columns") or [], "highlight_col": opt.get("highlight", 1), "rows": opt.get("rows") or [],
                       "notes": "", "seconds": 0})
    slides += [
        {"layout": "steps", "title": g.get("steps_title") or "What we would do, and what is not set up yet",
         "steps": [{k: v for k, v in s.items() if v} for s in g.get("steps") or []],
         "note": g.get("honesty_line") or "We are new. No case study yet, and we are not going to dress that up.",
         "notes": "", "seconds": 0},
        {"layout": "statement", "title": need(nx.get("slide_title"), "the next step as a claim"),
         "body": need(nx.get("slide_body"), "the next step body"), "notes": "", "seconds": 0},
        close(ch),
    ]
    return {"key": "f", "name": "How to run it", "source": "Strategy phase 9", "slides": slides}, ch


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("strategy")
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", choices=["full", "lite"], default="full")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists() and not a.force:
        print(f"{out} exists and is edited by hand. Pass --force to overwrite it.", file=sys.stderr)
        return 2
    st = json.loads(Path(a.strategy).read_text(encoding="utf-8"))
    if st.get("schema") != "twc.prospect-strategy/1":
        print(f"not a prospect strategy: schema is {st.get('schema')!r}", file=sys.stderr)
        return 2
    if (st.get("gate") or {}).get("verdict") != "GO":
        print(f"the gate verdict is {(st.get('gate') or {}).get('verdict')!r}. A deck is only built for a GO.", file=sys.stderr)
        return 1
    pr = st.get("prospect") or {}
    company = pr["company"]
    short = pr.get("short_name") or company.split()[0]
    lite = a.profile == "lite"
    builders = [deck_a, deck_c, deck_e, deck_f] if lite else [deck_a, deck_b, deck_c, deck_d, deck_e, deck_f]
    decks, chapters = [], []
    for fn in builders:
        if fn in (deck_c, deck_e, deck_f):
            d, ch = fn(st, short, lite=lite)
        else:
            d, ch = fn(st, short)
        decks.append(d)
        chapters.append((d, ch))
    if lite:  # rekey a, b, c, d so number keys and deck letters stay contiguous
        for k, d in zip("abcd", decks):
            d["key"] = k
    for d in decks:
        d["minutes"] = max(1, math.ceil(len(d["slides"]) * 0.5))
    th = st.get("thesis") or {}
    g = st.get("engagement") or {}
    ver = st.get("version", "v1")
    seed = int(hashlib.sha256(company.encode("utf-8")).hexdigest()[:6], 16) % 97 + 1
    home_chapters = []
    for d, ch in chapters:
        home_chapters.append({"deck": d["key"], "claim": need(ch.get("claim"), f"deck {d['key']} chapter claim"),
                              "so_what": need(ch.get("so_what"), f"deck {d['key']} so-what line"),
                              "evidence": ch.get("evidence") or [need(None, f"deck {d['key']} chapter evidence")],
                              "carry": need(ch.get("carry"), f"deck {d['key']} carry-forward line")})
    deck = {
        "schema": "twc.prospect-deck/1",
        "meta": {
            "company": company,
            "title": f"In-person channel strategy for {company}",
            "prepared_by": "The Warm Channel",
            "version": ver,
            "version_label": f"Version {ver.lstrip('v')}, " + ("public information only" if st.get("mode", "BUILD") == "BUILD" else "with your numbers"),
            "date_label": st.get("date_label") or need(None, "date label, for example 7 October 2026"),
            "confidential": f"Prepared privately for {company}. Not for distribution.",
            "lang": pr.get("lang", "en-CA"),
            "carrying_line": need(th.get("carrying_line"), "the carrying line"),
            "cta": g.get("cta") or {"label": "Book a call", "href": need(None, "the call to action address")},
        },
        "motif": {"count": 36, "seed": seed, "lit_every": 3},
        "home": {
            "kicker": th.get("kicker") or f"In-person channel strategy, version {ver.lstrip('v')}",
            "headline": need(th.get("headline"), "home headline, a claim"),
            "standfirst": need(th.get("standfirst"), "home standfirst"),
            "chapters": home_chapters,
            "next_step": {"headline": (g.get("next_step") or {}).get("headline") or "The next step is one call",
                          "body": need((g.get("next_step") or {}).get("body"), "next step body")},
            "method": st.get("method") or need(None, "how this was made, naming that it is public information only"),
        },
        "sources": [{k: v for k, v in s.items() if k in ("n", "text", "kind", "url")} for s in st.get("sources") or []],
        "design_global": dict(DESIGN_GLOBAL),
        "before_you_send": st.get("before_you_send") or {"verified": [], "needs_settling": [], "designed_not_supplied": []},
        "decks": decks,
    }
    if st.get("fictional"):
        deck = {"schema": deck["schema"], "fictional": st["fictional"], **{k: v for k, v in deck.items() if k != "schema"}}
    if st.get("date") and not st.get("date_label"):
        try:
            import datetime as dt
            dd = dt.date.fromisoformat(st["date"])
            deck["meta"]["date_label"] = f"{dd.day} {dd.strftime('%B')} {dd.year}"
            todo[:] = [t for t in todo if not t.startswith("date label")]
        except ValueError:
            pass
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n = sum(len(d["slides"]) for d in decks)
    print(f"Wrote {out}: {len(decks)} decks, {n} slides, profile {a.profile}.")
    print("Next: write presenter notes on every slide, at about 2.5 words a second, sharing no sentence with the screen.")
    for t in todo:
        print(f"  TODO {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
