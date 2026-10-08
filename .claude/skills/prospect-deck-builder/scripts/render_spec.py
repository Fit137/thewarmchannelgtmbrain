#!/usr/bin/env python3
"""Render the written spec of a prospect deck from deck.json and brand.json.

    python3 render_spec.py deck.json brand.json --out spec/

Writes five markdown files. The first three follow the reusable walkthrough brief
exactly, so the same spec can drive build_deck.py or a Claude Design build:

  01-content.md          File 1. Every word on screen and in the notes, the hierarchy,
                         the navigation table, the deck register, Before you present.
  02-design-concepts.md  File 2. What is designed on every slide, in semantic roles
                         only: no hex value, no typeface name, no font stack.
  03-build-handoff.md    File 3. The paste-ready handoff block for Claude Design, and
                         the Claude Code build path through build_deck.py.
  04-brand-kit.md        The prospect's palette mapped to the roles, with contrast,
                         type substitutes, logo rules and where each element came from.
                         The only file with hex values in it.
  05-before-you-send.md  The sending checklist for this deck.

Slides without a "design" block get the engine's defaults for their layout, so
File 2 always describes what the engine actually does. Run deck_check.py --design
on File 2 afterwards: it must contain no hex value and no typeface name.

No third-party dependencies. Python 3.8 or later.
"""
import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    import contrast  # noqa: E402  (same folder)
except ImportError:  # pragma: no cover
    contrast = None

ROLE_NAMES = ["surface", "surface_2", "ink", "body", "muted", "rule", "accent", "accent_ink", "on_accent",
              "positive", "caution", "flag"]
FIELDS = [("stage", "Stage"), ("hero", "Hero object"), ("entry", "Entry motion"), ("ambient", "Ambient"),
          ("interaction", "Interaction"), ("restraint", "Restraint"), ("reduced", "Reduced motion")]

# What the engine does for each layout when a slide carries no design block. Kept in
# step with build_deck.py and assets/deck-shell.html. Timings are delays from arrival.
DEFAULT_DESIGN = {
    "cover": {
        "stage": "Kicker, title and subtitle stacked left on the surface role. The Prepared for line, with the recipient's mark, at the foot. {motif_note}",
        "hero": "The title.",
        "entry": "Kicker rises 18px and fades in at 0ms, title at 120ms, subtitle at 260ms, each over 560ms on the file's curve.",
        "ambient": "None. A cover motif is static.",
        "interaction": "None.",
        "restraint": "The motif on a cover never turns, tilts or moves. The cover introduces the shape, it does not perform it.",
        "reduced": "Everything present on arrival.",
    },
    "statement": {
        "stage": "One claim and at most two short paragraphs, left aligned on the surface role, with the lower third left empty.",
        "hero": "The title, read as a sentence.",
        "entry": "Title rises and fades in at 80ms, body at 260ms, 560ms each.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "No illustration. If a picture adds nothing, the slide stays text, and says so by its emptiness.",
        "reduced": "Everything present on arrival.",
    },
    "points": {
        "stage": "Title, then two to four points in a grid, two columns for two or four points and three for three. Each point is topped by an ink rule, with a bold label and one line.",
        "hero": "The points, read as a set.",
        "entry": "Points rise and fade in 110ms apart from 260ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "No icons. A label and a line carry the point, an icon would only decorate it.",
        "reduced": "All points present on arrival.",
    },
    "figure": {
        "stage": "Title, then one or two large figures in the accent role, each with a caption beneath. A comparison figure sits in the muted role.",
        "hero": "The figure.",
        "entry": "Each figure scales from 0.94 and fades in, 220ms apart from 240ms, and counts up from zero over 900ms in tabular figures.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "The count runs once on arrival. An unknown never counts: it shows the unknown mark in the caution role.",
        "reduced": "Final values present, no count.",
    },
    "table": {
        "stage": "Title, then a table with an ink rule under the header and hairlines in the rule role between rows. A highlighted row sits on the surface 2 role.",
        "hero": "The highlighted row, or the column the argument rests on.",
        "entry": "The table rises and fades in as one object at 220ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "Rows never arrive one by one. A table is read, not performed.",
        "reduced": "Present on arrival.",
    },
    "quadrant": {
        "stage": "A full-width two-axis chart. Axes in the ink role, frame lines in the rule role, quadrant names in the muted role at the corners, every point labelled in print. The anchor point in the accent role with a halo.",
        "hero": "The anchor point.",
        "entry": "Axes present on arrival. Points scale from 0.4 and fade in, 140ms apart from 320ms, anchor last so the eye lands on it.",
        "ambient": "None. A chart that moves at rest asks to be read again.",
        "interaction": "None. Nothing hides behind a hover.",
        "restraint": "No 3D tilt. Perspective would distort position, and position is the claim.",
        "reduced": "Points present at full size on arrival.",
    },
    "timeline": {
        "stage": "A twelve-month strip with month rules in the rule role. Existing moments in the upper band, proposed moments in the lower band, each proposed moment led by its hatched outreach window.",
        "hero": "The proposed moments in the accent role.",
        "entry": "Items rise and fade in 120ms apart from 300ms in calendar order. Outreach windows draw left to right over 900ms, 120ms apart from 500ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "Existing moments may dim but never disappear. The plan keeps them, and erasing them would contradict the slide.",
        "reduced": "Everything present, windows fully drawn.",
    },
    "arithmetic": {
        "stage": "Blocks in a row, each a large value over a short label and topped by an ink rule, the last block by an accent rule.",
        "hero": "The result block.",
        "entry": "Blocks rise and fade in left to right, 160ms apart from 240ms. Controls, when present, arrive last at 900ms.",
        "ambient": "None.",
        "interaction": "{interactive_note}",
        "restraint": "No count-up on recompute. A number that spins while someone drags reads as a slot machine.",
        "reduced": "Identical, recompute is already instant.",
    },
    "comparison": {
        "stage": "A grid: row labels on the left, one column per option, the recommended column on the surface 2 role under an accent header.",
        "hero": "The recommended column.",
        "entry": "The grid rises and fades in as one object at 220ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "No ticks or crosses. Words carry the difference, a tick would turn it into a scorecard.",
        "reduced": "Present on arrival.",
    },
    "steps": {
        "stage": "Numbered steps in a row divided by hairlines. Each has a number in the accent role, a label, an optional status tag in the caution role on its own line, one line of description and a result under a rule.",
        "hero": "The step whose status matters most to the argument.",
        "entry": "Steps rise and fade in 160ms apart from 240ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "A status is always words, never colour alone, so it survives print and colour blindness.",
        "reduced": "All steps present.",
    },
    "journey": {
        "stage": "Stages along one horizontal line, each a marker, a name and one line.",
        "hero": "The stage the argument turns on.",
        "entry": "Stages rise and fade in 120ms apart from 240ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "No travelling dot along the line. The order is the point, not the movement.",
        "reduced": "All stages present.",
    },
    "words": {
        "stage": "A quotation set large in the ink role, the attribution beneath in the muted role.",
        "hero": "The quotation.",
        "entry": "Quotation fades in at 140ms, attribution at 420ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "Only words the source said or published, verbatim and attributed. Never a paraphrase in quotation marks.",
        "reduced": "Present on arrival.",
    },
    "invitation": {
        "stage": "A card on the surface 2 role under an ink rule, holding the sample invitation in guest vocabulary. A side note to its right.",
        "hero": "The card, read as the guest would read it.",
        "entry": "Card rises at 240ms, the side note at 420ms.",
        "ambient": "None.",
        "interaction": "None.",
        "restraint": "The card is guest copy and carries no client word. Nothing on it is annotated, underlined or highlighted in client language.",
        "reduced": "Present on arrival.",
    },
    "motif": {
        "stage": "Text on the left. The named-account ring on the right, on its tilted plane, in the {state} state.",
        "hero": "The ring in its {state} state.",
        "entry": "Text rises at 80ms and 260ms. The marks move into the {state} state as specified in the motif part.",
        "ambient": "{ambient_note}",
        "interaction": "{tilt_note}",
        "restraint": "The ring is never labelled, counted or explained on screen.",
        "reduced": "The {state} state present on arrival, no turn, no tilt.",
    },
    "calculator": {
        "stage": "Input fields in two columns on the left, results on the right. Until the four required fields hold numbers, a waiting line stands where the results will be.",
        "hero": "The return figure, in the accent role when it pays back and the flag role when it does not.",
        "entry": "Fields rise and fade in. Results stay hidden until the required inputs are complete.",
        "ambient": "None. People are typing.",
        "interaction": "Results recompute on every keystroke. Money fields take separators when the field loses focus. Typing never moves the slide.",
        "restraint": "No defaults, no example values, no count-up. A result built from our numbers would be a claim we cannot support.",
        "reduced": "Identical.",
    },
    "custom": {
        "stage": "Specified in deck.json for this slide.",
        "hero": "Specified in deck.json.",
        "entry": "Specified in deck.json.",
        "ambient": "Specified in deck.json.",
        "interaction": "Specified in deck.json.",
        "restraint": "Specified in deck.json.",
        "reduced": "Specified in deck.json.",
    },
    "close": {
        "stage": "A closing line that returns to the deck's cover, a short body, and exactly two actions: back to the overview, and onward.",
        "hero": "The closing line.",
        "entry": "Title at 80ms, body at 260ms, the two actions at 420ms.",
        "ambient": "None.",
        "interaction": "The two actions.",
        "restraint": "Two actions, never more. A third choice at the end of a deck is a reason to stop.",
        "reduced": "Present on arrival.",
    },
}

NAV_ROWS = [
    ("Open the file", "The overview (home layer). It stands alone: someone who never opens a deck still gets the argument."),
    ("Overview to a deck", "Start button, any chapter's Open button, the register link, or keys 1 to 9."),
    ("Next and previous slide", "Right arrow, Space, Page Down. Left arrow, Shift Space, Page Up. On-screen arrows. Swipe on touch."),
    ("First or last slide of a deck", "Home and End."),
    ("Jump within a deck", "Keys 1 to 9, or the slide rail at the foot."),
    ("End of a deck", "Two visible actions: Back to the overview, and Next: the following deck. The last deck offers the call to action instead."),
    ("Past the last slide", "Right arrow continues into the next deck's cover."),
    ("Before the first slide", "Left arrow from the first deck's cover returns to the overview."),
    ("Back to the overview", "Esc, the top bar's back link, or the browser's Back button after a deck change."),
    ("Deep links", "#/ is the overview. #/c/5 is deck C, slide 5. Every slide has its own address and survives a reload."),
    ("Browser history", "Changing deck adds a history entry. Moving between slides replaces it, so Back leaves the deck instead of stepping through every slide."),
    ("Sources", "S, or any superscript reference, opens the sources panel. On the overview, references jump to the numbered list."),
    ("Presenter notes", "N, in the present build only. The send build carries no notes and says so."),
    ("Motion", "M toggles motion. The visitor's reduced-motion setting is respected without asking."),
    ("Full screen and print", "F for full screen. P prints the overview and then every slide, one per page."),
    ("Help", "? opens the key map."),
]

MOTIF_STATES = {
    "scattered": "Marks scattered across the field, no ring, no centre. The cold channels.",
    "ringed": "Marks gathered into an even ring around an empty centre. The named list.",
    "lit": "One mark in three lifted toward the viewer and turned to the accent role, the plane tilted back like a table. The accounts in the room.",
    "connected": "The lit state, with thin accent lines drawing from the centre to the lit marks only. The conversation that continues, with those who choose it.",
}


def words(s):
    return len([w for w in (s or "").replace("\n", " ").split(" ") if w.strip()])


def q(s):
    """Blockquote a possibly multi-paragraph string."""
    s = str(s or "").strip()
    return "\n>\n".join("> " + p.replace("\n", " ") for p in s.split("\n\n") if p.strip())


def ref(dk, i):
    return f"{dk['key'].upper()}{i}"


def onscreen(sl, ctx):
    """Labelled on-screen elements of one slide, as markdown lines."""
    lay = sl.get("layout")
    out = []
    if sl.get("kicker") or lay == "cover":
        kick = sl.get("kicker") or f"Deck {ctx['deck']['key'].upper()} of {ctx['last_key'].upper()}, {ctx['deck']['name']}"
        out.append(("Kicker", kick))
    if lay == "words":
        out.append(("Title (visually hidden, read by screen readers)", sl["title"]))
    else:
        out.append(("Title", sl["title"]))
    if lay == "cover":
        if sl.get("subtitle"):
            out.append(("Subtitle", sl["subtitle"]))
        out.append(("Foot", f"The recipient's mark, then: Prepared for {ctx['company']}"))
        if sl.get("motif"):
            out.append(("Visual", f"the named-account ring at rest, {sl['motif']} state, never labelled"))
    elif lay in ("statement", "close"):
        if sl.get("body"):
            out.append(("Body", sl["body"]))
        if lay == "close":
            nxt = ctx.get("next")
            onward = f"Next: {nxt['name']}" if nxt else ctx["cta"]["label"]
            out.append(("Actions", f"Back to the overview | {onward}"))
    elif lay == "points":
        for k, p in enumerate(sl.get("points") or [], 1):
            out.append((f"Point {k}", f"**{p.get('label', '')}** {p.get('line', '')}"))
        if sl.get("body"):
            out.append(("Note", sl["body"]))
    elif lay == "figure":
        for k, f in enumerate(sl.get("figures") or [], 1):
            out.append((f"Figure {k}" + (" (muted)" if f.get("muted") else ""), f"**{f['value']}** {f.get('caption', '')}"))
        if sl.get("body"):
            out.append(("Note", sl["body"]))
    elif lay == "table":
        cols = sl.get("columns") or []
        rows = sl.get("rows") or []
        t = "| " + " | ".join(cols) + " |\n> |" + "---|" * len(cols)
        for r, row in enumerate(rows):
            mark = " (highlighted)" if sl.get("highlight_row") == r else ""
            t += "\n> | " + " | ".join(str(c) for c in row) + " |" + mark
        out.append(("Table", "\n>\n> " + t))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "quadrant":
        out.append(("Axes", f"{sl.get('x_label', '')} across, {sl.get('y_label', '')} up"))
        names = sl.get("quadrants") or []
        if names:
            out.append(("Quadrants", f"top right {names[0]}, top left {names[1]}, bottom left {names[2]}, bottom right {names[3]}"))
        for p in sl.get("points") or []:
            out.append(("Point" + (" (anchor)" if p.get("anchor") else ""), f"{p['label']} at ({p['x']}, {p['y']})"))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "timeline":
        for it in sl.get("items") or []:
            out.append(("Proposed" if it.get("kind") == "proposed" else "Existing",
                        f"{it['label']}, month {it['month']}, week {it.get('week', 2)}"))
        leg = [sl.get("legend_existing", "What you fund today")]
        if any(it.get("kind") == "proposed" for it in sl.get("items") or []):
            leg += [sl.get("legend_proposed", "Proposed"), sl.get("legend_window", "Outreach window")]
        out.append(("Legend", " | ".join(leg)))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "arithmetic":
        inter = sl.get("interactive")
        if inter:
            fm = inter.get("formats") or []
            seats = int(inter.get("seats", 12))
            rate = float(fm[0]["rate"]) if fm else 0.7
            out.append(("Block 1", f"**{seats}** people in the room"))
            out.append(("Block 2", f"**{int(seats / rate + 0.5)}** confirmations, roughly, at the format's attendance rate"))
            opts = ", ".join(f"{f['label']} {round(float(f['rate']) * 100)}%" for f in fm)
            out.append(("Controls", f"{inter.get('slider_label', 'People in the room')} slider, {inter.get('min', 6)} to "
                                    f"{inter.get('max', 40)}. {inter.get('select_label', 'Format')} select: {opts}"))
        for k, st in enumerate(sl.get("steps") or [], 1):
            out.append((f"Block {k + (2 if inter else 0)}", f"**{st['value']}** {st.get('label', '')}"))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "comparison":
        cols = sl.get("columns") or []
        hl = sl.get("highlight_col")
        head = [c + (" (recommended)" if hl == i else "") for i, c in enumerate(cols)]
        t = "| | " + " | ".join(head) + " |\n> |---|" + "---|" * len(cols)
        for row in sl.get("rows") or []:
            t += "\n> | " + row.get("label", "") + " | " + " | ".join(row.get("cells") or []) + " |"
        out.append(("Comparison", "\n>\n> " + t))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "steps":
        for k, st in enumerate(sl.get("steps") or [], 1):
            status = f" [status: {st['status']}]" if st.get("status") else ""
            res = f" Result: {st['result']}" if st.get("result") else ""
            out.append((f"Step {k}", f"**{st.get('label', '')}**{status} {st.get('line', '')}{res}"))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "journey":
        for k, s in enumerate(sl.get("stages") or [], 1):
            out.append((f"Stage {k}", f"**{s.get('name', '')}** {s.get('line', '')}"))
        if sl.get("note"):
            out.append(("Note", sl["note"]))
    elif lay == "words":
        out.append(("Quotation", sl.get("quote", "")))
        out.append(("Attribution", sl.get("attribution", "")))
        if sl.get("body"):
            out.append(("Note", sl["body"]))
    elif lay == "invitation":
        out.append(("Card, guest copy, guest vocabulary only", ""))
        out.append(("Subject", sl.get("subject", "")))
        out.append(("Card body", sl.get("body", "")))
        if sl.get("note"):
            out.append(("Side note", sl["note"]))
    elif lay == "motif":
        if sl.get("body"):
            out.append(("Body", sl["body"]))
        out.append(("Visual", f"the named-account ring, {sl.get('state', 'ringed')} state, never labelled"))
    elif lay == "calculator":
        if sl.get("intro"):
            out.append(("Intro", sl["intro"]))
        try:
            from build_deck import CALC_LABELS, CALC_REQUIRED, CALC_COPY
        except ImportError:
            CALC_LABELS, CALC_REQUIRED, CALC_COPY = {}, (), {}
        labels = sl.get("labels") or {}
        for k in sl.get("inputs") or []:
            lb, hp, _kind = CALC_LABELS.get(k, (k, "", ""))
            if isinstance(labels.get(k), list) and len(labels[k]) == 2:
                lb, hp = labels[k]
            req = "" if k in CALC_REQUIRED else " (optional)"
            out.append((f"Field{req}", f"**{lb}** {hp}"))
        copy = dict(CALC_COPY)
        copy.update(sl.get("copy") or {})
        out.append(("Before input", copy.get("wait", "")))
        out.append(("Results", "Cost per qualified conversation | Expected new customers | Expected first-year revenue | "
                               "Cost to acquire a customer through this channel | the comparison rows for the optional fields"))
        out.append(("Result line, pays back", copy.get("good", "")))
        out.append(("Result line, does not", copy.get("bad", "")))
        out.append(("Privacy", copy.get("privacy", "")))
    elif lay == "custom":
        out.append(("Custom", "bespoke HTML, see the slide's html field in deck.json"))
    if sl.get("foot"):
        out.append(("Foot", sl["foot"]))
    return out


def file1(deck, ctx):
    meta, home = deck["meta"], deck["home"]
    decks = deck["decks"]
    total_slides = sum(len(d["slides"]) for d in decks)
    talk = sum(int(s.get("seconds") or 0) for d in decks for s in d["slides"])
    read = sum(int(d.get("minutes") or 0) for d in decks)
    centre = [(d, i, s) for d in decks for i, s in enumerate(d["slides"], 1) if s.get("centrepiece")]
    brief = deck.get("brief") or {}
    L = []
    L.append(f"# {meta['title']}\n")
    L.append("File 1 of 3, content. Every word in the walkthrough, and the structure that carries it. "
             "File 2 says how each slide is designed. File 3 is the build handoff.\n")
    if deck.get("fictional"):
        L.append(f"> **Fictional example.** {deck['fictional']}\n")
    L.append("## Audience, runtime, ask, deliverable\n")
    L.append(f"- **Audience:** {brief.get('audience', 'the person at ' + meta['company'] + ' who owns events and is measured on pipeline')}. Client vocabulary throughout, except the guest copy on any invitation slide.")
    L.append(f"- **Runtime:** about {math.ceil(talk / 60)} minutes presented, from the speaker notes. About {read} minutes self-guided, from the deck register.")
    L.append(f"- **Ask:** {brief.get('ask', home.get('next_step', {}).get('headline', meta['cta']['label']))}. One call to action in the whole file: {meta['cta']['label']}.")
    L.append("- **Deliverable:** one self-contained HTML file in two builds, send (no notes) and present (notes on N), plus a PDF leave-behind printed from the same file.\n")
    L.append("## Spec at a glance\n")
    L.append("| | |\n|---|---|")
    L.append(f"| Format | Single-file interactive walkthrough: a home layer and {len(decks)} sub-decks of horizontal slides at 1600 by 900 |")
    L.append(f"| Sections and slides | {len(decks)} decks, {total_slides} slides, {len(centre)} centrepieces |")
    L.append(f"| Register | {(deck.get('design_global') or {}).get('register', '')} |")
    L.append(f"| Spine | {' > '.join(d['name'] for d in decks)} |")
    arc = [c.get("claim", "") for c in home.get("chapters", [])]
    L.append(f"| Arc | {' Then: '.join(arc)} |")
    L.append(f"| The line that carries it | {meta['carrying_line']} |")
    short = deck.get("short_path") or ([f"{decks[0]['key'].upper()}1"] + [ref(d, i) for d, i, _ in centre] +
                                        [f"{decks[-1]['key'].upper()}{len(decks[-1]['slides'])}"])
    L.append(f"| Short cut path | The overview, then {', '.join(short)}. Use it when the walkthrough has ten minutes, not twenty |\n")

    L.append("## Hierarchy, pages and navigation\n")
    L.append("This part matters more than any slide. The file is opened by people with no presenter and no instructions.\n")
    L.append("### The three levels\n")
    L.append(f"1. **Home layer, the overview.** A scrolling page: masthead with the recipient's mark and Prepared for {meta['company']}, "
             "the hero (kicker, headline, standfirst, the carrying line, a start button), the deck register, one chapter per deck, "
             "the next step with the one call to action, how this was made, the numbered sources, and the footer.")
    L.append("2. **Deck layer.** Each deck is a horizontal sequence of slides that opens on a cover and ends on a close with two actions. "
             "Persistent chrome: a top bar (back to the overview, the recipient's mark, the deck letter and name, the slide count), "
             "a slide rail at the foot, previous and next arrows at the edges.")
    L.append("3. **Slide.** A 1600 by 900 stage, scaled to fit any screen, with presenter notes attached in the present build only.\n")
    L.append("The repeating skeleton of a home chapter:\n")
    L.append("```\n[Deck letter]\n[Claim, as the headline]\n[So what, one line tying it to the ask]\n"
             "- [Evidence, with its source number]\n- [Evidence]\n[Carry forward, one line into the next chapter]\n"
             "[Open [letter], [n] slides]\n```\n")
    L.append("### Navigation table\n")
    L.append("| Route, key or gesture | What happens |\n|---|---|")
    for a, b in NAV_ROWS:
        L.append(f"| {a} | {b} |")
    L.append("")
    L.append("### Deck register\n")
    L.append("| Key | Name | Slides | Minutes, self-guided | Source in the strategy |\n|---|---|---|---|---|")
    for d in decks:
        L.append(f"| {d['key'].upper()} | {d['name']} | {len(d['slides'])} | {d.get('minutes', '')} | {d.get('source', '')} |")
    L.append("")

    L.append("## Home layer\n")
    hero = [("Masthead", f"the recipient's mark, Prepared for {meta['company']}, and {meta.get('version_label', '')}"),
            ("Kicker", home.get("kicker", "")), ("Headline", home.get("headline", "")),
            ("Standfirst", home.get("standfirst", "")), ("Carrying line", meta["carrying_line"]),
            ("Start", f"Start with {decks[0]['key'].upper()}, {decks[0]['name']}")]
    L.append("**Hero**\n")
    for lb, tx in hero:
        L.append(f"> **{lb}:** {tx}".replace("\n\n", " "))
    L.append("")
    chapters = {c["deck"]: c for c in home.get("chapters", [])}
    for d in decks:
        c = chapters.get(d["key"], {})
        L.append(f"### {d['key'].upper()}. {c.get('claim', '')}\n")
        L.append(f"> **So what:** {c.get('so_what', '')}")
        for e in c.get("evidence", []):
            L.append(f"> - {e}")
        L.append(f"> **Carry forward:** {c.get('carry', '')}\n")
    nx = home.get("next_step") or {}
    L.append("### The next step\n")
    L.append(f"> **Headline:** {nx.get('headline', '')}\n> **Body:** {nx.get('body', '')}\n> **Action:** {meta['cta']['label']} ({meta['cta']['href']})\n")
    if home.get("method"):
        L.append("### How this was made\n")
        L.append(q(home["method"]) + "\n")
    if deck.get("sources"):
        L.append("### Sources\n")
        for s in deck["sources"]:
            L.append(f"{s['n']}. {s['text']}" + (f" ({s['kind']})" if s.get("kind") else "") + (f", {s['url']}" if s.get("url") else ""))
        L.append("")

    L.append("## Sub-decks\n")
    L.append("Every slide: **On screen** is literal final copy. **Say it** is the presenter's argument, first person, "
             "sayable at speed, about 2.5 words a second. The two share no sentence.\n")
    for di, d in enumerate(decks):
        ctx["deck"] = d
        ctx["next"] = decks[di + 1] if di + 1 < len(decks) else None
        L.append(f"### Deck {d['key'].upper()}, {d['name']}\n")
        for i, s in enumerate(d["slides"], 1):
            tags = [s.get("layout")]
            if s.get("centrepiece"):
                tags.append("centrepiece")
            if s.get("still"):
                tags.append("still")
            if s.get("audience", "both") != "both":
                tags.append(f"{s['audience']} build only")
            L.append(f"#### {ref(d, i)}. {s['title']} ({', '.join(tags)})\n")
            L.append("**On screen**\n")
            for lb, tx in onscreen(s, ctx):
                L.append(f"> **{lb}:** {tx}".rstrip())
            L.append("")
            if s.get("notes"):
                L.append(f"**Say it (~{s.get('seconds', '?')} s, {words(s['notes'])} words)**\n")
                L.append(s["notes"] + "\n")
            else:
                L.append("**Say it:** none written. Every slide needs notes before the present build.\n")
    bys = deck.get("before_you_send") or {}
    L.append("## Before you present\n")
    L.append("The highest-trust part of this document. Nothing here is softened.\n")
    for key, head in (("verified", "Verified, and where it traces to"),
                      ("needs_settling", "Needs settling, and what breaks if it goes the other way"),
                      ("designed_not_supplied", "Designed, not supplied, and the cost of committing to it")):
        L.append(f"### {head}\n")
        items = bys.get(key) or []
        L.extend(f"- {x}" for x in items) if items else L.append("- Nothing listed. That is itself a finding: say why.")
        L.append("")
    return "\n".join(L)


def design_for(sl, ctx):
    lay = sl.get("layout")
    base = dict(DEFAULT_DESIGN.get(lay, DEFAULT_DESIGN["statement"]))
    fill = {
        "motif_note": (f"The motif sits at rest to the right in its {sl['motif']} state, faded far back behind the type."
                       if sl.get("motif") else "No motif."),
        "state": sl.get("state", "ringed"),
        "ambient_note": ("None. This slide is deliberately still." if sl.get("still") else
                         "The plane turns one revolution every 140 seconds. Alive at rest, never busy."),
        "tilt_note": ("The plane tilts up to 4 degrees with the pointer." if sl.get("centrepiece") else "None."),
        "interactive_note": ("A slider sets the people in the room and a select switches the format. The second block "
                             "recomputes instantly as people divided by the attendance rate, rounded to the nearest whole person."
                             if sl.get("interactive") else "None."),
    }
    out = {k: v.format(**fill) for k, v in base.items()}
    explicit = sl.get("design") or {}
    out.update({k: v for k, v in explicit.items() if v})
    return out, bool(explicit)


def file2(deck, ctx):
    g = deck.get("design_global") or {}
    decks = deck["decks"]
    L = [f"# {deck['meta']['title']}: design concepts\n",
         "File 2 of 3. What gets designed on every slide to carry its argument.\n",
         "> **No design system is specified here.** No hex values, no typeface names, no font stacks. Colour appears only as a "
         "semantic role: surface, surface 2, ink, body, muted, rule, accent, accent ink, on accent, positive, caution, flag. "
         "The builder maps each role once and holds it. Size appears only as relative hierarchy. Geometry, timing and motion "
         "are exact: milliseconds, pixels at the 1600 by 900 design size, degrees, order.\n",
         "## Global\n"]
    for key, head in (("register", "Register, and how objects move because of it"), ("easing", "Motion vocabulary"),
                      ("rig", "The 3D construction rig"), ("interaction", "Interaction contract"),
                      ("constraints", "Build constraints"), ("accessibility", "Accessibility")):
        L.append(f"### {head}\n\n{g.get(key, 'Not specified. Specify it before building.')}\n")
    L.append("## The recurring motif\n")
    L.append(g.get("motif", "The named-account ring.") + "\n")
    cfg = deck.get("motif") or {}
    L.append(f"Geometry: {cfg.get('count', 36)} marks on a ring of radius 300px around an empty centre, every "
             f"{cfg.get('lit_every', 3)}rd mark lit in the lit and connected states. Scatter positions are seeded "
             f"({cfg.get('seed', 7)}) so every build places them identically. The plane tilts back 52 degrees under a "
             "1700px perspective. Marks travel to the ring 22ms apart. The mark count is not data and is never stated.\n")
    L.append("| Slide | State | What the state says |\n|---|---|---|")
    for d in decks:
        for i, s in enumerate(d["slides"], 1):
            st = s.get("state") if s.get("layout") == "motif" else (s.get("motif") if s.get("layout") == "cover" else None)
            if st:
                L.append(f"| {ref(d, i)} | {st} | {MOTIF_STATES.get(st, '')} |")
    L.append("\nNever labelled, never counted, never explained on screen. By its third appearance it reads without a legend.\n")
    L.append("## Centrepieces\n")
    L.append("| Slide | Title | Why the motion is the claim |\n|---|---|---|")
    for d in decks:
        for i, s in enumerate(d["slides"], 1):
            if s.get("centrepiece"):
                why = (s.get("design") or {}).get("hero") or "The motion carries the argument."
                L.append(f"| {ref(d, i)} | {s['title']} | {why} |")
    still = [ref(d, i) for d in decks for i, s in enumerate(d["slides"], 1) if s.get("still")]
    L.append(f"\nDeliberately still: {', '.join(still) if still else 'none, which is a fault: add one before the biggest moment'}.\n")
    L.append("## Slide by slide\n")
    L.append("Slides marked *engine default* carry the layout's standard treatment, stated in full so nothing is left to guess.\n")
    restraints = []
    for di, d in enumerate(decks):
        L.append(f"### Deck {d['key'].upper()}, {d['name']}\n")
        for i, s in enumerate(d["slides"], 1):
            des, explicit = design_for(s, ctx)
            tag = "" if explicit else " *engine default*"
            L.append(f"#### {ref(d, i)}. {s['title']}{tag}\n")
            for k, head in FIELDS:
                L.append(f"- **{head}:** {des.get(k, '')}")
            L.append("")
            if des.get("restraint"):
                restraints.append((ref(d, i), des["restraint"]))
    L.append("## Restraint register\n")
    L.append("Every place not to animate, and why. Several exist because the obvious animation would contradict the slide.\n")
    L.append("| Where | Do not | Why |\n|---|---|---|")
    L.append("| Every chart and table | animate at rest | A chart that moves at rest asks to be read again |")
    L.append("| Every number | count up on recompute or revisit | It reads as a slot machine, and a number that performs is doubted |")
    L.append("| The motif | label, count or explain it | The shape is the argument, a legend turns it into decoration |")
    for where, r in restraints:
        first, _, rest = r.partition(". ")
        L.append(f"| {where} | {first.rstrip('.')} | {rest or 'See the slide.'} |")
    L.append("")
    L.append("## Reduced motion and print\n")
    L.append("**Reduced motion.** The visitor's setting is honoured on arrival and M toggles it. Every animation ships its "
             "resolved end state: entries present, counts at their final value, windows drawn, motif states settled, no turn, "
             "no tilt. Every information-revealing interaction still works as an instant swap: the arithmetic slider and "
             "select, the calculator, the sources panel, the rail.\n")
    L.append("**Print.** P, or the browser's print, produces the overview first and then every slide, one per 1600 by 900 page, "
             "every slide in its resolved state. Nothing in the file is hover-only, so nothing needs printing inline. The "
             "calculator prints its formulas in place of results, because a printed page cannot hold someone's typed numbers. "
             "Interactive controls, the chrome and the two end-of-deck actions do not print.\n")
    return "\n".join(L)


def file3(deck, ctx):
    meta = deck["meta"]
    decks = deck["decks"]
    g = deck.get("design_global") or {}
    centre = [(d, i, s) for d in decks for i, s in enumerate(d["slides"], 1) if s.get("centrepiece")]
    L = [f"# {meta['title']}: build handoff\n",
         "File 3 of 3. Two build paths from the same three files.\n",
         "## Path 1, Claude Code, the default\n",
         "```bash\n"
         "python3 scripts/build_deck.py deck.json brand.json --out build/" + ctx["slug"] + "_send.html\n"
         "python3 scripts/build_deck.py deck.json brand.json --out build/" + ctx["slug"] + "_present.html --audience present\n"
         "python3 scripts/deck_check.py build/" + ctx["slug"] + "_send.html --deck deck.json --register evidence-register.md --design spec/02-design-concepts.md --brand brand.json\n"
         "python3 scripts/screenshot.py build/" + ctx["slug"] + "_send.html --out build/shots --pdf build/" + ctx["slug"] + ".pdf\n"
         "```\n",
         "The engine already implements everything below: the shell, the chrome, the navigation contract, reduced motion, "
         "print, the motif and every layout. Content changes go in deck.json, brand changes in brand.json, and the file is rebuilt.\n",
         "## Path 2, Claude Design\n",
         "Use this when a bespoke build is wanted. Paste the block below with File 1, File 2 and the brand kit attached.\n",
         "```"]
    centre_rows = "\n".join(f"  {ref(d, i)}  {s['title']}  ({(s.get('design') or {}).get('hero', 'the motion carries the claim')})"
                            for d, i, s in centre)
    L.append(f"""Build an interactive HTML walkthrough for {meta['company']}: {meta['title']}.
It is a private strategy, prepared from public information, for the person who owns
events and pipeline. It must persuade by its arithmetic and its restraint.

USE YOUR NATIVE DESIGN SYSTEM for components, spacing and the type scale. Colour comes
ONLY from the semantic roles in File 2, mapped onto the prospect's palette in the brand
kit. Map each role once, hold it everywhere, and invent no colour. Use the substitute
typefaces the brand kit names. The prospect's mark appears only in the Prepared for
line and the top bar, never recoloured, stretched or animated.

STRUCTURE, three levels:
  1. Home layer: a scrolling overview that stands alone.
  2. Deck layer: {len(decks)} decks of horizontal slides, {', '.join(d['key'].upper() + ' ' + d['name'] for d in decks)}.
  3. Slide: a 1600 by 900 stage scaled to the viewport.

BUILD ORDER, and do not change it:
  1. The shell and the full navigation, against placeholder decks.
  2. One complete vertical slice, deck {decks[0]['key'].upper()}, as the pattern.
  3. The remaining decks.
  4. The home layer.
  5. Print and reduced motion, checked on every slide.
Retrofitting routing into finished slides is the expensive path.

NAVIGATION CONTRACT, in full:
""" + "\n".join(f"  {a}: {b}" for a, b in NAV_ROWS) + f"""

NON-NEGOTIABLES:
  - Real 3D with no libraries, on the motif only.
  - One self-contained file. No CDN, no web font service, no analytics, no request of any kind.
  - Alive at rest only where File 2 says so. Illustrative, never decorative.
  - One easing curve for the whole file. {g.get('easing', '')}
  - Tabular figures on every numeral.
  - Reduced motion is first class: resolved end states, every interaction still works.
  - The print path is mandatory: overview, then one slide per page.
  - Projector safe: text contrast at least 4.5 to 1, running text never under 20px at the design size.
  - The calculator opens empty. No default, no example value, no result before the reader types.
  - Every unknown stays the literal {{TBD}} mark in the caution role. Never replace it with a plausible number.

THE MOTIF: {g.get('motif', 'The named-account ring.')}
THE REGISTER: {g.get('register', '')}

CENTREPIECES, built with the most care:
{centre_rows}

HOOKS, so the build can be checked by deck_check.py: a robots noindex meta tag;
<section class="deck" data-deck="a" data-name="..."> per deck; <article class="slide
layout-cover"> on slide 1 and layout-close on the last; a <div class="close-actions"> with
exactly two links on every close; <aside class="notes" data-seconds="n"> in the present
build only; data-audience="guest" on the invitation card; <sup class="ref"> on source
references; and a build comment naming the audience, send or present.

SCAFFOLD FIRST. Before writing any slide content, return for approval: the shell, the
overlay chrome, the working navigation against placeholder decks, and your semantic role
mapping. Every slide inherits that mapping, and changing it later is a large revision.""")
    L.append("```\n")
    L.append("### Note to whoever runs the handoff\n")
    L.append("- **Attach:** File 1, File 2, the brand kit, the font files and the logo file. Nothing else: no other deck, no "
             "other company's material, no brain file.")
    L.append("- **Approve first:** the role mapping and the navigation, on placeholder decks. Then the deck "
             f"{decks[0]['key'].upper()} slice.")
    L.append("- **Most likely to get lost:** the two actions at the end of every deck, the send build without notes, the empty "
             "calculator, the {TBD} marks, and the print path. Check each by hand, then run deck_check.py on the result.")
    return "\n".join(L)


def file4(brand):
    L = [f"# Brand kit, {brand.get('company', '')}\n"]
    if brand.get("note"):
        L.append(f"> {brand['note']}\n")
    L.append(f"Skin: **{brand.get('skin', 'prospect')}**. Captured {brand.get('captured', '{TBD}')}. "
             "This is the only spec file that holds hex values.\n")
    L.append("## Roles\n")
    L.append("| Role | Value | Used for |\n|---|---|---|")
    uses = {"surface": "page and slide background", "surface_2": "highlighted blocks, rows and columns",
            "ink": "titles, headings, axes", "body": "running text", "muted": "kickers, captions, notes",
            "rule": "hairlines", "accent": "links, figures, buttons, the lit motif", "accent_ink": "hover states",
            "on_accent": "text on buttons", "positive": "reserved", "caution": "{TBD} marks and status tags",
            "flag": "a result that does not pay back"}
    roles = brand.get("roles") or {}
    for r in ROLE_NAMES:
        L.append(f"| {r} | `{roles.get(r, 'neutral default')}` | {uses[r]} |")
    L.append("")
    if contrast and roles:
        L.append("## Contrast\n")
        L.append("| Pair | Ratio | Needs | Status |\n|---|---|---|---|")
        for row in contrast.evaluate(roles):
            rt = f"{row['ratio']:.2f}" if row["ratio"] is not None else "-"
            L.append(f"| {row['fg']} on {row['bg']} | {rt} | {row['need']} | {row['status']} |")
        L.append("")
    L.append("## Type\n")
    for slot, f in (brand.get("fonts") or {}).items():
        files = ", ".join(x["path"] for x in f.get("files") or [])
        L.append(f"- **{slot}:** {f.get('family', '')}, weight {f.get('weight', 'per file')}. Files: {files or 'none, system fallback'}. "
                 f"Licence: {f.get('licence', '{TBD}')}. Stands in for: {f.get('substitute_for', 'the brand face itself')}.")
    L.append("")
    lg = brand.get("logo") or {}
    L.append("## Mark\n")
    L.append(f"- File: {lg.get('path', 'none')}. Alt text: {lg.get('alt', '')}. Usage: {lg.get('usage', 'prepared-for only')}.")
    for c in (brand.get("guidelines") or {}).get("constraints") or []:
        L.append(f"- {c}")
    if (brand.get("guidelines") or {}).get("url"):
        L.append(f"- Guidelines read at {brand['guidelines']['url']}.")
    L.append("")
    L.append("## Where each element came from\n")
    for s in brand.get("sources") or []:
        L.append(f"- **{s.get('element')}:** {s.get('from')}" + (f", {s['url']}" if s.get("url") else ""))
    L.append(f"\nSignature on the file: {brand.get('twc_signature', 'Prepared by The Warm Channel')}.\n")
    return "\n".join(L)


def file5(deck, ctx):
    bys = deck.get("before_you_send") or {}
    slug = ctx["slug"]
    L = [f"# Before you send, {deck['meta']['company']}\n",
         "Every box is ticked by a person. A script cannot tell you whether a claim is true.\n",
         "## Run\n",
         f"- [ ] `deck_check.py build/{slug}_send.html --deck deck.json --register evidence-register.md --design spec/02-design-concepts.md --brand brand.json` is clean, and every warning has been read",
         f"- [ ] `contrast.py brand.json` passes",
         f"- [ ] `screenshot.py build/{slug}_send.html --out build/shots --pdf build/{slug}.pdf`, and every shot has been looked at",
         "- [ ] The brain's `ops/QA-checklist.md` blocks for a client asset, run against File 1",
         "- [ ] Opened on a phone, on a laptop and in print preview. The overview reads alone on a phone",
         "",
         "## Content\n"]
    for x in bys.get("verified") or []:
        L.append(f"- [ ] Verified: {x}")
    for x in bys.get("needs_settling") or []:
        L.append(f"- [ ] Settled: {x}")
    for x in bys.get("designed_not_supplied") or []:
        L.append(f"- [ ] Labelled as designed: {x}")
    L.append("- [ ] Every {TBD} is a number only the prospect can supply, and the copy says so")
    L.append("- [ ] No client, count, testimonial, result, guarantee, price or network claim, anywhere, including the notes")
    L.append("- [ ] Every capability that is not READY carries its status in the same sentence")
    L.append("")
    L.append("## Delivery\n")
    L += ["- [ ] Sent as the **send** build, never the present build",
          "- [ ] As a private, unlisted, noindex link or a PDF. Never an HTML attachment, which mail filters treat as phishing",
          "- [ ] No tracking: no pixel, no link shortener, no UTM parameter, no read receipt",
          "- [ ] One researched approach from the founder, to one named person. No sequence, no follow-up to a non-reply",
          "- [ ] Logged in the pipeline by prospect ID only, with the date sent and the version",
          "- [ ] Never published, never reused for another company, never shown as a case study",
          ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("brand")
    ap.add_argument("--out", required=True)
    ap.add_argument("--slug", help="file stem for the build paths, defaults to the company name")
    a = ap.parse_args()
    deck = json.loads(Path(a.deck).read_text(encoding="utf-8"))
    brand = json.loads(Path(a.brand).read_text(encoding="utf-8"))
    company = deck["meta"]["company"]
    slug = a.slug or "".join(ch.lower() if ch.isalnum() else "_" for ch in company).strip("_").replace("__", "_")
    slug = f"{slug}_strategy_{deck['meta'].get('version', 'v1')}"
    ctx = {"company": company, "cta": deck["meta"]["cta"], "last_key": deck["decks"][-1]["key"], "slug": slug}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "01-content.md": file1(deck, dict(ctx)),
        "02-design-concepts.md": file2(deck, dict(ctx)),
        "03-build-handoff.md": file3(deck, dict(ctx)),
        "04-brand-kit.md": file4(brand),
        "05-before-you-send.md": file5(deck, dict(ctx)),
    }
    for name, text in files.items():
        (out / name).write_text(text.rstrip() + "\n", encoding="utf-8")
        print(f"wrote {out / name} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
