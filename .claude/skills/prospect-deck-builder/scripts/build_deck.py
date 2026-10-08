#!/usr/bin/env python3
"""Build a private, single-file prospect strategy deck.

    python3 build_deck.py deck.json brand.json --out build/acme_strategy_v1_send.html
    python3 build_deck.py deck.json brand.json --out build/acme_strategy_v1_present.html --audience present

deck.json carries every word and the structure. brand.json maps the prospect's
brand onto semantic roles, and names the font files and the logo. The output is
one HTML file with no network requests: fonts and the logo are embedded, the
engine is inline, and nothing typed into the calculator leaves the page.

Two audiences, built from the same source:
  send     the copy the prospect receives. Presenter notes are stripped.
  present  the founder's copy for a live walkthrough. Press N for notes.

No third-party dependencies. Python 3.8 or later.
Exit status: 0 built, 1 build error, 2 bad usage.
"""
import argparse
import base64
import datetime as dt
import hashlib
import html
import json
import math
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHELL = HERE.parent / "assets" / "deck-shell.html"

ROLE_VARS = {
    "surface": "--c-surface", "surface_2": "--c-surface-2", "ink": "--c-ink",
    "body": "--c-body", "muted": "--c-muted", "rule": "--c-rule",
    "accent": "--c-accent", "accent_ink": "--c-accent-ink", "on_accent": "--c-on-accent",
    "positive": "--c-positive", "caution": "--c-caution", "flag": "--c-flag",
}
LAYOUTS = ("cover", "statement", "points", "figure", "table", "quadrant", "timeline",
           "arithmetic", "comparison", "steps", "journey", "words", "invitation",
           "motif", "calculator", "custom", "close")

CALC_LABELS = {
    "deal": ("Average first-year contract value", "For a typical new customer in the segment this programme targets.", "money"),
    "close": ("Close rate from a qualified first conversation", "Of ten qualified conversations, how many become customers?", "percent"),
    "investment": ("Programme investment", "Any number you want to test, for example what one trade show costs you today.", "money"),
    "conversations": ("Qualified conversations", "How many you would want the programme to produce.", "count"),
    "cac": ("Your current cost to acquire a customer", "Total sales and marketing spend divided by new customers won.", "money"),
    "meeting": ("Your current cost per senior meeting", "From your own outbound or SDR numbers, if you track it.", "money"),
}
CALC_REQUIRED = ("deal", "close", "investment", "conversations")
CALC_COPY = {
    "good": "At your numbers, each {cur}1 invested returns {per_dollar} of expected first-year revenue, at your close rate of {close}%.",
    "bad": "At your numbers, the programme does not pay back in its first year. Either the investment is too high for your deal size, or the programme is too small.",
    "cheaper": "{amount} less",
    "dearer": "{amount} more",
    "wait": "Fill the four numbers on the left to see the arithmetic. Every number is yours, and nothing you type leaves this page.",
    "privacy": "This calculator runs entirely in your browser. Nothing you type is sent anywhere.",
}
NEUTRAL_ROLES = {
    "surface": "#FBF9F5", "surface_2": "#F2EEE7", "ink": "#14120F", "body": "#3A3733",
    "muted": "#6B655C", "rule": "#DDD8CF", "accent": "#1F3A5F", "accent_ink": "#162B46",
    "on_accent": "#FBF9F5", "positive": "#2E6B4A", "caution": "#8A5A00", "flag": "#6E2A2A",
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class BuildError(Exception):
    pass


warnings = []


def warn(msg):
    warnings.append(msg)


# ---------------------------------------------------------------------------
# Text handling. Every string is escaped. Three inline marks are allowed:
# **bold**, [n] for a source reference, and {TBD} for an unknown.
# ---------------------------------------------------------------------------
REF_RE = re.compile(r"\s*\[(\d{1,2})\]")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
BANNED_CHARS = {"\u2014": "em dash", "\u2013": "en dash"}
EVIDENCE_RE = re.compile(r"\[E\d+\]")


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def check_text(s, where):
    if s is None:
        return
    s = str(s)
    for ch, name in BANNED_CHARS.items():
        if ch in s:
            raise BuildError(f"{name} in {where}: {s[:80]!r}. Use a comma or restructure.")
    if EVIDENCE_RE.search(s):
        raise BuildError(f"internal evidence reference in {where}: {s[:80]!r}. Evidence IDs never ship.")
    if "{{" in s:
        raise BuildError(f"unfilled placeholder in {where}: {s[:80]!r}")
    if "[WRITE" in s:
        warn(f"unwritten scaffold marker in {where}: {s[:80]!r}. deck_check.py fails until it is replaced")


def fmt(s, where="text"):
    check_text(s, where)
    if s is None:
        return ""
    t = esc(s)
    t = BOLD_RE.sub(r"<strong>\1</strong>", t)
    t = REF_RE.sub(lambda m: (f'<sup class="ref"><a href="#src-{m.group(1)}" data-ref="{m.group(1)}">'
                              f'{m.group(1)}</a></sup>'), t)
    t = t.replace("{TBD}", '<span class="tbd">{TBD}</span>')
    return t


def paras(s, cls, where):
    if not s:
        return ""
    parts = [p.strip() for p in str(s).split("\n\n") if p.strip()]
    return "".join(f'<p class="{cls}">{fmt(p, where)}</p>' for p in parts)


def ent(d, kind="", extra=""):
    k = f" e-{kind}" if kind else ""
    cls = f"enter{k}" + (f" {extra}" if extra else "")
    return f'class="{cls}" style="--d:{int(d)}ms"'


# ---------------------------------------------------------------------------
# The motif: the named-account ring. Deterministic, never labelled.
# States: scattered, ringed, lit, connected.
# ---------------------------------------------------------------------------
def motif_html(state, cfg, ambient=True, tilt=False, static=False):
    if state not in ("scattered", "ringed", "lit", "connected"):
        raise BuildError(f"unknown motif state {state!r}")
    n = int(cfg.get("count", 36))
    seed = int(cfg.get("seed", 7))
    every = max(2, int(cfg.get("lit_every", 3)))
    rng = random.Random(seed)
    radius = 300
    marks, lines = [], []
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        x, y = radius * math.cos(a), radius * math.sin(a)
        sx, sy = rng.uniform(-340, 340), rng.uniform(-340, 340)
        lit = (i % every == 0)
        lit_attr = " data-lit" if lit else ""
        marks.append(f'<span class="mm"{lit_attr} style="--x:{x:.1f}px;--y:{y:.1f}px;'
                     f'--sx:{sx:.1f}px;--sy:{sy:.1f}px;--i:{i}"></span>')
        if lit:
            lines.append(f'<span class="m-line" style="--a:{math.degrees(a):.2f}deg;--len:{radius}px;--i:{i}"></span>')
    classes = ["motif"]
    if not static:
        classes.append("rig")
    if ambient and state != "scattered" and not static:
        classes.append("ambient")
    if static:
        classes.append("motif-static")
    tilt_attr = " data-tilt" if tilt else ""
    return (f'<div class="{" ".join(classes)}" data-state="{state}" aria-hidden="true">'
            f'<div class="m-plane"{tilt_attr}><div class="m-spin">'
            f'{"".join(lines)}<span class="m-center"></span>{"".join(marks)}'
            f'</div></div></div>')


# ---------------------------------------------------------------------------
# Layouts. Each returns the inner HTML of one slide.
# ---------------------------------------------------------------------------
def head(sl, where, title_cls="s-title", d0=0):
    out = ""
    if sl.get("kicker"):
        out += f'<div {ent(d0)}><span class="s-kicker">{fmt(sl["kicker"], where + ".kicker")}</span></div>'
    out += f'<h2 {ent(d0 + 80)}><span class="{title_cls}">{fmt(sl["title"], where + ".title")}</span></h2>'
    return out


def foot(sl, where):
    if not sl.get("foot"):
        return ""
    return f'<div class="s-foot"><span>{fmt(sl["foot"], where + ".foot")}</span></div>'


def L_cover(sl, ctx, where):
    deck = ctx["deck"]
    kicker = sl.get("kicker") or f'Deck {deck["key"].upper()} of {ctx["deck_count_letter"]}, {deck["name"]}'
    out = f'<div {ent(0)}><span class="s-kicker">{fmt(kicker, where + ".kicker")}</span></div>'
    out += f'<h2 {ent(120)}><span class="s-title">{fmt(sl["title"], where + ".title")}</span></h2>'
    out += f'<div {ent(260)}>{paras(sl.get("subtitle"), "s-sub", where + ".subtitle")}</div>'
    logo = ctx["logo_img"]
    out += f'<div class="cover-for">{logo}<span>{fmt("Prepared for " + ctx["company"], where)}</span></div>'
    if sl.get("motif"):
        out += motif_html(sl["motif"], ctx["motif_cfg"], ambient=False, static=True)
    return out


def L_statement(sl, ctx, where):
    out = head(sl, where)
    out += f'<div {ent(260)}>{paras(sl.get("body"), "s-body", where + ".body")}</div>'
    return out


def L_points(sl, ctx, where):
    pts = sl.get("points") or []
    if not 2 <= len(pts) <= 4:
        raise BuildError(f"{where}: points needs 2 to 4 items, has {len(pts)}")
    cols = 2 if len(pts) in (2, 4) else 3
    out = head(sl, where)
    out += f'<div class="points" style="--cols:{cols}">'
    for k, p in enumerate(pts):
        out += (f'<div {ent(260 + 110 * k, extra="point")}><b>{fmt(p.get("label"), where)}</b>'
                f'<span>{fmt(p.get("line"), where)}</span></div>')
    out += "</div>" + paras(sl.get("body"), "s-note", where + ".body")
    return out


NUM_RE = re.compile(r"^(?P<pre>[^\d\-]*)(?P<num>-?\d[\d,]*(?:\.\d+)?)(?P<suf>.*)$")


def figure_value(v, delay):
    v = str(v)
    m = NUM_RE.match(v)
    if not m or "{TBD}" in v:
        return f'<span class="fig-value">{fmt(v)}</span>'
    num = m.group("num").replace(",", "")
    dec = len(num.split(".")[1]) if "." in num else 0
    return (f'<span class="fig-value" data-count="{esc(num)}" data-dec="{dec}" data-pre="{esc(m.group("pre"))}" '
            f'data-suf="{esc(m.group("suf"))}" data-delay="{delay}">{fmt(v)}</span>')


def L_figure(sl, ctx, where):
    figs = sl.get("figures") or []
    if not 1 <= len(figs) <= 2:
        raise BuildError(f"{where}: figure needs 1 or 2 figures")
    out = head(sl, where)
    out += '<div class="figs">'
    for k, f in enumerate(figs):
        cls = "fig muted" if f.get("muted") else "fig"
        out += (f'<div {ent(240 + 220 * k, "scale", extra=cls)}>{figure_value(f["value"], 300 + 220 * k)}'
                f'<span class="fig-cap">{fmt(f.get("caption"), where + ".caption")}</span></div>')
    out += "</div>" + paras(sl.get("body"), "s-note", where + ".body")
    return out


def L_table(sl, ctx, where):
    cols = sl.get("columns") or []
    rows = sl.get("rows") or []
    num_cols = set(sl.get("numeric_columns") or [])
    hl = sl.get("highlight_row")
    out = head(sl, where)
    out += f'<div {ent(220, extra="tbl-wrap")}><table class="t"><thead><tr>'
    for c, h in enumerate(cols):
        out += f'<th class="{"num" if c in num_cols else ""}">{fmt(h, where)}</th>'
    out += "</tr></thead><tbody>"
    for r, row in enumerate(rows):
        if len(row) != len(cols):
            raise BuildError(f"{where}: row {r + 1} has {len(row)} cells, expected {len(cols)}")
        out += f'<tr class="{"hl" if hl == r else ""}">'
        for c, cell in enumerate(row):
            out += f'<td class="{"num" if c in num_cols else ""}">{fmt(cell, where)}</td>'
        out += "</tr>"
    out += "</tbody></table></div>"
    out += paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_quadrant(sl, ctx, where):
    W, H, pad = 1344, 470, 30
    pts = sl.get("points") or []
    names = sl.get("quadrants") or ["", "", "", ""]
    if len(names) != 4:
        raise BuildError(f"{where}: quadrants needs four names, top right first, then top left, bottom left, bottom right")
    lo, hi = sl.get("range", [-20, 20])

    def px(v):
        return pad + (float(v) - lo) / (hi - lo) * (W - 2 * pad)

    def py(v):
        return H - pad - (float(v) - lo) / (hi - lo) * (H - 2 * pad)

    cx, cy = px(0), py(0)
    aria = sl.get("aria") or f'Quadrant chart. {sl.get("x_label", "")} across, {sl.get("y_label", "")} up.'
    svg = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(aria)}">']
    svg.append(f'<line class="q-grid" x1="{pad}" y1="{pad}" x2="{W - pad}" y2="{pad}"/>')
    svg.append(f'<line class="q-grid" x1="{pad}" y1="{H - pad}" x2="{W - pad}" y2="{H - pad}"/>')
    svg.append(f'<line class="q-axis" x1="{pad}" y1="{cy:.1f}" x2="{W - pad}" y2="{cy:.1f}"/>')
    svg.append(f'<line class="q-axis" x1="{cx:.1f}" y1="{pad}" x2="{cx:.1f}" y2="{H - pad}"/>')
    tr, tl, bl, br = names
    svg.append(f'<text class="q-name" x="{W - pad - 8}" y="{pad + 30}" text-anchor="end">{esc(tr)}</text>')
    svg.append(f'<text class="q-name" x="{pad + 8}" y="{pad + 30}">{esc(tl)}</text>')
    svg.append(f'<text class="q-name" x="{pad + 8}" y="{H - pad - 14}">{esc(bl)}</text>')
    svg.append(f'<text class="q-name" x="{W - pad - 8}" y="{H - pad - 14}" text-anchor="end">{esc(br)}</text>')
    svg.append(f'<text class="q-lab" x="{W - pad}" y="{cy - 12:.1f}" text-anchor="end">{esc(sl.get("x_label", ""))}</text>')
    svg.append(f'<text class="q-lab" x="{cx + 12:.1f}" y="{pad + 64}">{esc(sl.get("y_label", ""))}</text>')
    for k, p in enumerate(pts):
        check_text(p.get("label"), where)
        x, y = px(p["x"]), py(p["y"])
        anchor = " anchor" if p.get("anchor") else ""
        pos = p.get("label_pos", "right")
        off = 40 if p.get("anchor") else 22
        dx, dy, ta = {"right": (off, 8, "start"), "left": (-off, 8, "end"),
                      "up": (0, -off, "middle"), "down": (0, off + 14, "middle")}.get(pos, (off, 8, "start"))
        halo = f'<circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="28"/>' if anchor else ""
        svg.append(f'<g class="q-pt{anchor}" style="--d:{320 + 140 * k}ms">{halo}'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13"/>'
                   f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{ta}">{esc(p["label"])}</text></g>')
    svg.append("</svg>")
    out = head(sl, where)
    out += f'<div class="quad">{"".join(svg)}</div>'
    out += paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_timeline(sl, ctx, where):
    """Twelve-month strip. Items are packed into rows so that no label, dot or
    outreach window overlaps another. Existing moments sit in the upper band,
    proposed ones in the lower band, each band holding up to three rows."""
    items = sl.get("items") or []
    start = int(sl.get("start_month", 1))
    win_weeks = float(sl.get("window_weeks", 6))
    months = [MONTHS[(start - 1 + k) % 12] for k in range(12)]
    char_pct = 0.80          # 20px label text on a 1344px track
    row_tops = {"existing": [52, 104, 156], "proposed": [220, 272, 324]}

    def pos(it):
        m = int(it["month"])
        if not 1 <= m <= 12:
            raise BuildError(f"{where}: month must be 1 to 12")
        w = float(it.get("week", 2))
        return (((m - start) % 12) + (w - 0.5) / 4.0) / 12.0 * 100.0

    rows = {"existing": [[], [], []], "proposed": [[], [], []]}
    placed = []
    for n, it in enumerate(sorted(items, key=pos)):
        check_text(it.get("label"), where)
        kind = it.get("kind", "existing")
        if kind not in row_tops:
            raise BuildError(f"{where}: timeline item kind must be existing or proposed")
        p = pos(it)
        lw = len(str(it["label"])) * char_pct + 3.0
        left_lbl = p + lw > 99.0
        lo, hi = (p - lw, p + 1.5) if left_lbl else (p - 1.5, p + lw)
        wl = None
        if kind == "proposed" and win_weeks > 0:
            wl = max(0.0, p - win_weeks / 52.0 * 100.0)
            lo = min(lo, wl)
        row = None
        for r in range(3):
            if all(hi + 1.0 <= a or lo >= b2 + 1.0 for a, b2 in rows[kind][r]):
                row = r
                break
        if row is None:
            row = min(range(3), key=lambda r: len(rows[kind][r]))
            warn(f"{where}: timeline is crowded, {it['label']!r} may overlap. Shorten labels or split the slide")
        rows[kind][row].append((lo, hi))
        placed.append((n, it, kind, p, row, left_lbl, wl))

    out_items = []
    kinds = set()
    for n, it, kind, p, row, left_lbl, wl in placed:
        kinds.add(kind)
        top = row_tops[kind][row]
        dim = " dim" if kind == "existing" and sl.get("dim_existing") else ""
        cls = f"tl-item {kind}" + (" lbl-left" if left_lbl else "") + dim
        side = (f"right:{100 - p:.2f}%;margin-right:-11px" if left_lbl else f"left:{p:.2f}%;margin-left:-11px")
        if wl is not None:
            out_items.append(f'<span class="tl-win enter e-draw" style="--d:{500 + 120 * n}ms;left:{wl:.2f}%;'
                             f'width:{p - wl:.2f}%;top:{top + 20}px"></span>')
        out_items.append(f'<div class="{cls} enter" style="--d:{300 + 120 * n}ms;top:{top}px;{side}">'
                         f'<span class="tl-dot"></span><span class="tl-label">{esc(it["label"])}</span></div>')
    legend = '<div class="tl-legend">'
    if "existing" in kinds:
        legend += f'<span><i></i>{esc(sl.get("legend_existing", "What you fund today"))}</span>'
    if "proposed" in kinds:
        legend += f'<span><i class="p"></i>{esc(sl.get("legend_proposed", "Proposed"))}</span>'
        if win_weeks > 0:
            legend += f'<span><i class="w"></i>{esc(sl.get("legend_window", "Outreach window"))}</span>'
    legend += "</div>"
    out = head(sl, where)
    month_html = "".join(f"<span>{m}</span>" for m in months)
    out += f'<div class="tl"><div class="tl-months">{month_html}</div>{"".join(out_items)}{legend}</div>'
    out += paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_arithmetic(sl, ctx, where):
    steps = sl.get("steps") or []
    inter = sl.get("interactive")
    out = head(sl, where)
    if inter:
        formats = inter.get("formats") or [{"label": "Invite-only executive dinner", "rate": 0.70}]
        seats = int(inter.get("seats", 12))
        rate = float(formats[0]["rate"])
        conf = int(seats / rate + 0.5)
        ref = f' [{inter["ref"]}]' if inter.get("ref") else ""
        labels = inter.get("labels") or ["people in the room",
                                         "confirmations, roughly, at the format's attendance rate" + ref]
        chain = [{"value": str(seats), "label": labels[0], "k": "seats"},
                 {"value": str(conf), "label": labels[1], "k": "conf"}] + list(steps)
        out += f'<div class="arith" data-interactive data-rate="{rate}">'
        for k, st in enumerate(chain):
            kk = f' data-arith="{st["k"]}"' if st.get("k") else ""
            lng = " long" if len(str(st["value"])) > 6 else ""
            out += (f'<div {ent(240 + 160 * k, extra="arith-step")}><span class="arith-value{lng}"{kk}>{fmt(st["value"], where)}</span>'
                    f'<span class="arith-label">{fmt(st.get("label"), where)}</span></div>')
        out += "</div>"
        opts = "".join(f'<option value="{float(f["rate"])}">{esc(f["label"])}, {round(float(f["rate"]) * 100)}%</option>'
                       for f in formats)
        for f in formats:
            check_text(f.get("label"), where)
        out += (f'<div class="arith-ctl enter" style="--d:900ms"><label>{esc(inter.get("slider_label", "People in the room"))}'
                f'<input type="range" min="{int(inter.get("min", 6))}" max="{int(inter.get("max", 40))}" value="{seats}" '
                f'aria-label="{esc(inter.get("slider_label", "People in the room"))}"></label>'
                f'<label>{esc(inter.get("select_label", "Format"))}<select aria-label="Format">{opts}</select></label></div>')
    else:
        out += '<div class="arith">'
        for k, st in enumerate(steps):
            lng = " long" if len(str(st["value"])) > 6 else ""
            out += (f'<div {ent(240 + 160 * k, extra="arith-step")}><span class="arith-value{lng}">{fmt(st["value"], where)}</span>'
                    f'<span class="arith-label">{fmt(st.get("label"), where)}</span></div>')
        out += "</div>"
    out += paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_comparison(sl, ctx, where):
    cols = sl.get("columns") or []
    rows = sl.get("rows") or []
    hl = sl.get("highlight_col")
    n = len(cols)
    out = head(sl, where)
    out += f'<div class="cmp enter" style="--n:{n};--d:220ms"><div class="ch"></div>'
    for c, h in enumerate(cols):
        out += f'<div class="ch{" hl" if hl == c else ""}">{fmt(h, where)}</div>'
    for row in rows:
        cells = row.get("cells") or []
        if len(cells) != n:
            raise BuildError(f"{where}: comparison row {row.get('label')!r} has {len(cells)} cells, expected {n}")
        out += f'<div class="rl">{fmt(row.get("label"), where)}</div>'
        for c, cell in enumerate(cells):
            out += f'<div class="{"hl" if hl == c else ""}">{fmt(cell, where)}</div>'
    out += "</div>" + paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_steps(sl, ctx, where):
    steps = sl.get("steps") or []
    out = head(sl, where)
    out += f'<div class="steps" style="--n:{len(steps)}">'
    for k, st in enumerate(steps):
        status = f'<span class="st">{esc(st["status"])}</span>' if st.get("status") else ""
        check_text(st.get("status"), where)
        res = f'<div class="res">{fmt(st["result"], where)}</div>' if st.get("result") else ""
        out += (f'<div {ent(240 + 160 * k, extra="step")}><div class="sn">{k + 1}</div>'
                f'<b>{fmt(st.get("label"), where)}{status}</b><p>{fmt(st.get("line"), where)}</p>{res}</div>')
    out += "</div>" + paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_journey(sl, ctx, where):
    st = sl.get("stages") or []
    out = head(sl, where)
    out += f'<div class="jr" style="--n:{len(st)}">'
    for k, s in enumerate(st):
        out += (f'<div {ent(240 + 120 * k, extra="jr-st")}><i></i><b>{fmt(s.get("name"), where)}</b>'
                f'<span>{fmt(s.get("line"), where)}</span></div>')
    out += "</div>" + paras(sl.get("note"), "s-note", where + ".note")
    return out


def L_words(sl, ctx, where):
    out = ""
    if sl.get("kicker"):
        out += f'<div {ent(0)}><span class="s-kicker">{fmt(sl["kicker"], where)}</span></div>'
    out += f'<blockquote {ent(140, extra="words-q")}>{fmt(sl.get("quote"), where + ".quote")}</blockquote>'
    out += f'<div {ent(420, extra="words-a")}>{fmt(sl.get("attribution"), where)}</div>'
    out += f'<h2 class="sr">{fmt(sl["title"], where)}</h2>'
    out += paras(sl.get("body"), "s-note", where + ".body")
    return out


def L_invitation(sl, ctx, where):
    out = head(sl, where)
    body = "".join(f"<p>{fmt(p.strip(), where + '.guest')}</p>" for p in str(sl.get("body", "")).split("\n\n") if p.strip())
    out += ('<div class="inv">'
            f'<div {ent(240, extra="inv-card")} data-audience="guest"><div class="subj">{fmt(sl.get("subject"), where)}</div>{body}</div>'
            f'<div {ent(420, extra="inv-side")}>{fmt(sl.get("note"), where + ".note")}</div></div>')
    return out


def L_motif(sl, ctx, where):
    state = sl.get("state", "ringed")
    txt = head(sl, where) + f'<div {ent(260)}>{paras(sl.get("body"), "s-body", where + ".body")}</div>'
    return (f'<div class="with-motif"><div class="txt">{txt}</div>'
            f'{motif_html(state, ctx["motif_cfg"], ambient=not sl.get("still"), tilt=bool(sl.get("centrepiece")))}</div>')


def L_calculator(sl, ctx, where):
    cid = sl.get("calc_id", "roi")
    keys = sl.get("inputs") or ["deal", "close", "investment", "conversations", "cac"]
    labels = sl.get("labels") or {}
    prefill = sl.get("prefill") or {}
    cur = sl.get("currency", "$")
    for k in CALC_REQUIRED:
        if k not in keys:
            raise BuildError(f"{where}: calculator must ask for {k}")
    for k in keys:
        if k not in CALC_LABELS:
            raise BuildError(f"{where}: unknown calculator input {k!r}")
    if prefill and not sl.get("prefill_note"):
        raise BuildError(f"{where}: prefilled values need prefill_note naming who supplied them and when")
    copy = dict(CALC_COPY)
    copy.update(sl.get("copy") or {})
    for k2, v in copy.items():
        check_text(v, where + ".copy." + k2)
    ctx["calculators"][cid] = {"currency": cur, "copy": copy}
    out = head(sl, where)
    if sl.get("intro"):
        out += paras(sl["intro"], "s-note", where + ".intro")
    ins = ""
    for k in keys:
        lb, hp, kind = CALC_LABELS[k]
        if isinstance(labels.get(k), (list, tuple)) and len(labels[k]) == 2:
            lb, hp = labels[k]
        check_text(lb, where)
        check_text(hp, where)
        opt = " opt" if k not in CALC_REQUIRED else ""
        pre = f"<span>{esc(cur)}</span>" if kind == "money" else ""
        suf = "<span>%</span>" if kind == "percent" else ""
        val = prefill.get(k)
        vattr = f' value="{esc(val)}"' if val is not None else ""
        ins += (f'<label class="{opt.strip()}"><span class="lb">{esc(lb)}</span><span class="hp">{esc(hp)}</span>'
                f'<span class="field">{pre}<input type="text" inputmode="decimal" autocomplete="off" data-k="{k}" '
                f'data-kind="{kind}"{vattr} aria-label="{esc(lb)}">{suf}</span></label>')
    rows = (f'<dt>Cost per qualified conversation</dt><dd data-o="cpc"></dd>'
            f'<dt>Expected new customers</dt><dd data-o="cust"></dd>'
            f'<dt>Expected first-year revenue</dt><dd data-o="rev"></dd>'
            f'<dt>Cost to acquire a customer through this channel</dt><dd data-o="ccac"></dd>')
    if "cac" in keys:
        rows += '<div data-row="cac" hidden><dt>Against your current cost to acquire</dt><dd></dd></div>'
    if "meeting" in keys:
        rows += '<div data-row="meeting" hidden><dt>Cost per conversation against your cost per senior meeting</dt><dd></dd></div>'
    note = f'<p class="calc-privacy">{esc(sl["prefill_note"])}</p>' if prefill else ""
    formulas = ("Cost per qualified conversation = programme investment divided by qualified conversations.",
                "Expected new customers = qualified conversations multiplied by your close rate.",
                "Expected first-year revenue = expected new customers multiplied by your average first-year contract value.",
                "Return = expected first-year revenue divided by programme investment.")
    out += (f'<div class="calc" data-calc="{esc(cid)}"><div class="calc-in">{ins}'
            f'<p class="calc-privacy">{esc(copy["privacy"])}</p>{note}</div>'
            f'<div><p class="calc-wait">{esc(copy["wait"])}</p>'
            f'<div class="calc-out" hidden><span class="big">0x</span><p class="lead"></p><dl>{rows}</dl></div>'
            f'<ul class="calc-formulas">{"".join(f"<li>{esc(x)}</li>" for x in formulas)}</ul></div></div>')
    return out


def L_custom(sl, ctx, where):
    raw = sl.get("html") or ""
    for ch, name in BANNED_CHARS.items():
        if ch in raw:
            raise BuildError(f"{name} in {where}.html")
    if re.search(r"<script|\bon\w+\s*=|javascript:", raw, re.I):
        raise BuildError(f"{where}: custom HTML may not carry script or event handlers. Put behaviour in the shell")
    if re.search(r"""(?:src|href)\s*=\s*["']?(?:https?:)?//""", raw, re.I) or "@import" in raw:
        raise BuildError(f"{where}: custom HTML may not load anything from the network")
    out = head(sl, where) if sl.get("show_title", True) else f'<h2 class="sr">{fmt(sl["title"], where)}</h2>'
    out += raw
    return out


def L_close(sl, ctx, where):
    out = head(sl, where)
    out += f'<div {ent(260)}>{paras(sl.get("body"), "s-body", where + ".body")}</div>'
    nxt = ctx["next_deck"]
    acts = '<a class="btn ghost" href="#/" data-go="home">Back to the overview</a>'
    if nxt:
        acts += (f'<a class="btn" href="#/{esc(nxt["key"])}/1" data-go="deck:{esc(nxt["key"])}">'
                 f'Next: {esc(nxt["name"])}</a>')
    else:
        cta = ctx["cta"]
        acts += f'<a class="btn" href="{esc(cta["href"])}" rel="noopener noreferrer">{esc(cta["label"])}</a>'
    out += f'<div {ent(420, extra="close-actions")}>{acts}</div>'
    return out


RENDER = {name: globals()["L_" + name] for name in LAYOUTS}


# ---------------------------------------------------------------------------
# Brand, fonts, logo
# ---------------------------------------------------------------------------
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
FONT_MIME = {".woff2": ("font/woff2", "woff2"), ".woff": ("font/woff", "woff"),
             ".ttf": ("font/ttf", "truetype"), ".otf": ("font/otf", "opentype")}


def load_brand(brand, base):
    skin = brand.get("skin", "prospect")
    roles = dict(NEUTRAL_ROLES)
    if skin == "prospect":
        missing = [r for r in ROLE_VARS if r not in (brand.get("roles") or {})]
        if missing:
            raise BuildError(f"brand.json roles missing: {', '.join(missing)}. Use skin 'neutral' if the brand could not be captured")
        roles.update(brand["roles"])
    for r, v in roles.items():
        if not HEX_RE.match(str(v)):
            raise BuildError(f"brand role {r} is {v!r}, expected #rrggbb")
    tokens = ":root{" + "".join(f"{ROLE_VARS[r]}:{v};" for r, v in roles.items() if r in ROLE_VARS)
    faces = []
    fonts = brand.get("fonts") or {}
    for slot, var in (("display", "--f-display"), ("text", "--f-text")):
        f = fonts.get(slot)
        if not f:
            continue
        fam = f.get("family")
        fallback = f.get("fallback", "system-ui, sans-serif")
        files = f.get("files") or []
        for fi in files:
            p = (base / fi["path"]).resolve()
            if not p.exists():
                raise BuildError(f"font file not found: {p}")
            mime, fmtname = FONT_MIME.get(p.suffix.lower(), (None, None))
            if not mime:
                raise BuildError(f"unsupported font format: {p.name}")
            b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            faces.append(f'@font-face{{font-family:"{fam}";src:url(data:{mime};base64,{b64}) format("{fmtname}");'
                         f'font-weight:{fi.get("weight", 400)};font-style:{fi.get("style", "normal")};font-display:swap}}')
        family_part = ('"' + fam + '", ') if (fam and files) else ""
        tokens += var + ":" + family_part + fallback + ";"
        if slot == "display" and f.get("weight"):
            tokens += f'--w-display:{int(f["weight"])};'
    if brand.get("radius") is not None:
        tokens += f'--radius:{brand["radius"]};'
    tokens += "}"
    logo_img = ""
    logo = brand.get("logo") or {}
    if logo.get("path"):
        p = (base / logo["path"]).resolve()
        if not p.exists():
            raise BuildError(f"logo not found: {p}")
        mime = {".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg"}.get(p.suffix.lower())
        if not mime:
            raise BuildError(f"unsupported logo format: {p.name}")
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        logo_img = f'<img src="data:{mime};base64,{b64}" alt="{esc(logo.get("alt", brand.get("company", "")))}">'
    return tokens, "\n".join(faces), logo_img


# ---------------------------------------------------------------------------
# Home layer
# ---------------------------------------------------------------------------
def render_home(deck, ctx):
    meta, home = deck["meta"], deck["home"]
    decks = deck["decks"]
    where = "home"
    out = (f'<header class="h-mast"><div class="who">{ctx["logo_img"]}<span>{fmt("Prepared for " + meta["company"], where)}</span></div>'
           f'<div>{fmt(meta.get("version_label", ""), where)}</div></header>')
    out += (f'<section class="h-hero"><div class="h-kicker">{fmt(home.get("kicker"), where)}</div>'
            f'<h1>{fmt(home["headline"], where + ".headline")}</h1>'
            f'{paras(home.get("standfirst"), "h-stand", where + ".standfirst")}'
            f'<p class="h-line">{fmt(meta["carrying_line"], "meta.carrying_line")}</p>'
            f'<div class="h-start"><a class="btn" href="#/{esc(decks[0]["key"])}/1" data-go="deck:{esc(decks[0]["key"])}">'
            f'Start with {esc(decks[0]["key"].upper())}, {esc(decks[0]["name"])}</a>'
            f'<span class="h-hint" style="color:var(--c-muted);font-size:15px">Or open any chapter below. Press ? for keys.</span></div></section>')
    out += '<nav class="h-register" aria-label="Decks in this file"><ol>'
    for d in decks:
        n = len(ctx["slide_counts"][d["key"]])
        out += (f'<li><span class="k">{esc(d["key"].upper())}</span><a href="#/{esc(d["key"])}/1" data-go="deck:{esc(d["key"])}">'
                f'{esc(d["name"])}</a><span class="m">{n} slides, about {int(d.get("minutes", max(1, round(n * 0.5))))} min</span></li>')
    out += "</ol></nav>"
    chapters = {c["deck"]: c for c in home.get("chapters", [])}
    for d in decks:
        c = chapters.get(d["key"])
        if not c:
            raise BuildError(f"home has no chapter for deck {d['key']}. The home layer must stand alone")
        w = f"home.chapter.{d['key']}"
        ev = "".join(f"<li>{fmt(e, w)}</li>" for e in c.get("evidence", []))
        n = len(ctx["slide_counts"][d["key"]])
        out += (f'<section class="h-chapter" id="ch-{esc(d["key"])}"><div class="num">{esc(d["key"].upper())}</div><div>'
                f'<h2>{fmt(c["claim"], w + ".claim")}</h2><p class="so">{fmt(c.get("so_what"), w)}</p>'
                f'<ul>{ev}</ul><p class="carry">{fmt(c.get("carry"), w)}</p>'
                f'<a class="btn ghost" href="#/{esc(d["key"])}/1" data-go="deck:{esc(d["key"])}">'
                f'Open {esc(d["key"].upper())}, {n} slides</a></div></section>')
    nx = home.get("next_step") or {}
    cta = ctx["cta"]
    out += (f'<section class="h-next"><h2>{fmt(nx.get("headline", "The next step"), "home.next")}</h2>'
            f'{paras(nx.get("body"), "", "home.next.body")}'
            f'<a class="btn" href="{esc(cta["href"])}" rel="noopener noreferrer">{esc(cta["label"])}</a></section>')
    if home.get("method"):
        out += f'<section class="h-method"><h3>How this was made</h3>{paras(home["method"], "", "home.method")}</section>'
    srcs = deck.get("sources") or []
    if srcs:
        out += '<section class="h-sources"><h3>Sources</h3><ol>'
        for s in srcs:
            check_text(s.get("text"), "sources")
            link = f' <a href="{esc(s["url"])}" rel="noopener noreferrer" target="_blank">Link</a>' if s.get("url") else ""
            kind = f' ({esc(s["kind"])})' if s.get("kind") else ""
            out += f'<li id="src-{int(s["n"])}" value="{int(s["n"])}">{esc(s["text"])}{kind}{link}</li>'
        out += "</ol></section>"
    sig = home.get("signature") or f'Prepared by {meta.get("prepared_by", "The Warm Channel")} for {meta["company"]}.'
    out += (f'<footer class="h-foot"><span>{fmt(sig, "home.signature")} {fmt(meta.get("date_label", ""), where)}</span>'
            f'<span>{fmt(meta.get("confidential", ""), where)}</span>'
            f'<span>This page runs entirely in your browser. Nothing you type leaves it.</span></footer>')
    return out


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------
def build(deck, brand, deck_path, brand_path, audience):
    for k in ("meta", "home", "decks"):
        if k not in deck:
            raise BuildError(f"deck.json is missing {k}")
    meta = deck["meta"]
    for k in ("company", "title", "carrying_line", "cta"):
        if not meta.get(k):
            raise BuildError(f"deck.json meta.{k} is required")
    cta = meta["cta"]
    if not cta.get("label") or not cta.get("href"):
        raise BuildError("meta.cta needs label and href. One call to action for the whole file")
    if "{TBD}" in cta["href"]:
        warn("meta.cta.href is {TBD}. Settle it before sending")
    tokens, faces, logo_img = load_brand(brand, brand_path.parent)
    decks = deck["decks"]
    if not 1 <= len(decks) <= 9:
        raise BuildError("between 1 and 9 decks")
    keys = [d["key"] for d in decks]
    if len(set(keys)) != len(keys) or not all(re.fullmatch(r"[a-z]", k) for k in keys):
        raise BuildError("deck keys must be unique single lowercase letters")
    ctx = {"company": meta["company"], "logo_img": logo_img, "motif_cfg": deck.get("motif") or {},
           "calculators": {}, "cta": cta, "slide_counts": {}, "date_label": meta.get("date_label", ""),
           "deck_count_letter": keys[-1].upper()}
    custom_css = [deck.get("custom_css", "")]
    decks_html = []
    register = []
    for di, d in enumerate(decks):
        slides = [s for s in d.get("slides", []) if s.get("audience", "both") in ("both", audience)]
        if len(slides) < 2:
            raise BuildError(f"deck {d['key']} needs at least a cover and a close")
        if slides[0].get("layout") != "cover":
            raise BuildError(f"deck {d['key']}: slide 1 must be a cover")
        if slides[-1].get("layout") != "close":
            raise BuildError(f"deck {d['key']}: the last slide must be a close, which carries the two actions")
        if len(slides) > 9:
            warn(f"deck {d['key']} has {len(slides)} slides. Over 9 usually means two decks")
        ctx["slide_counts"][d["key"]] = slides
        ctx["deck"] = d
        ctx["next_deck"] = decks[di + 1] if di + 1 < len(decks) else None
        art = []
        for si, sl in enumerate(slides):
            where = f"deck {d['key']} slide {si + 1}"
            lay = sl.get("layout")
            if lay not in RENDER:
                raise BuildError(f"{where}: unknown layout {lay!r}. Known: {', '.join(LAYOUTS)}")
            if not sl.get("title"):
                raise BuildError(f"{where}: every slide needs a title, even when it is visually hidden")
            inner = RENDER[lay](sl, ctx, where)
            classes = [f"slide layout-{lay}"]
            if sl.get("still"):
                classes.append("still")
            if sl.get("centrepiece"):
                classes.append("centrepiece")
            if lay == "cover" and sl.get("motif"):
                classes.append("has-motif")
            notes = ""
            if audience == "present":
                if sl.get("notes"):
                    check_text(sl["notes"], where + ".notes")
                    notes = (f'<aside class="notes" data-seconds="{int(sl.get("seconds", 30))}">'
                             f'{paras(sl["notes"], "", where + ".notes")}</aside>')
                else:
                    warn(f"{where}: no presenter notes")
            sid = f"s-{d['key']}-{si + 1}"
            if sl.get("css"):
                custom_css.append(sl["css"].replace("#this", "#" + sid))
            art.append(f'<article class="{" ".join(classes)}" id="{sid}" data-title="{esc(re.sub(r"[*{}]", "", sl["title"]))}" '
                       f'aria-roledescription="slide" aria-label="{si + 1} of {len(slides)}">'
                       f'<div class="slide-inner">{inner}</div>{foot(sl, where)}{notes}</article>')
        decks_html.append(f'<section class="deck" data-deck="{esc(d["key"])}" data-name="{esc(d["name"])}" '
                          f'aria-label="Deck {esc(d["key"].upper())}, {esc(d["name"])}" hidden>'
                          f'<div class="frame">{"".join(art)}</div></section>')
        register.append({"key": d["key"], "name": d["name"], "slides": len(slides)})
    home_html = render_home(deck, ctx)
    for css in custom_css:
        if css and (re.search(r"url\(\s*['\"]?(?:https?:)?//", css) or "@import" in css):
            raise BuildError("custom CSS may not load anything from the network")
    data = {"sources": deck.get("sources") or [], "calculators": ctx["calculators"], "decks": register,
            "meta": {"company": meta["company"], "version": meta.get("version", "")}}
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    shell = SHELL.read_text(encoding="utf-8")
    digest = hashlib.sha256(deck_path.read_bytes() + brand_path.read_bytes()).hexdigest()[:12]
    info = (f"<!-- Prospect strategy deck. Built {dt.date.today().isoformat()} by prospect-deck-builder. "
            f"Audience: {audience}. Version: {esc(meta.get('version', ''))}. Source digest: {digest}. -->")
    chrome_for = esc(f"Prepared for {meta['company']}")
    chrome_logo = logo_img.replace("<img ", '<img aria-hidden="true" ') if logo_img else ""
    repl = {
        "<!--@LANG@-->": esc(meta.get("lang", "en")),
        "<!--@TITLE@-->": esc(meta["title"]),
        "<!--@BUILDINFO@-->": info,
        "/*@FONTFACES@*/": faces,
        "/*@TOKENS@*/": tokens,
        "/*@CUSTOMCSS@*/": "\n".join(c for c in custom_css if c),
        "<!--@HOME@-->": home_html,
        "<!--@DECKS@-->": "\n".join(decks_html),
        "<!--@CHROME_LOGO@-->": chrome_logo,
        "<!--@CHROME_FOR@-->": chrome_for,
        "/*@DATA@*/": data_json,
    }
    for k, v in repl.items():
        if k not in shell:
            raise BuildError(f"shell template is missing slot {k}")
        shell = shell.replace(k, v)
    if audience == "present":
        shell = shell.replace('<body class="view-home">', '<body class="view-home aud-present">', 1)
    return shell


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("brand")
    ap.add_argument("--out", required=True)
    ap.add_argument("--audience", choices=["send", "present"], default="send")
    a = ap.parse_args()
    deck_path, brand_path = Path(a.deck).resolve(), Path(a.brand).resolve()
    try:
        deck = json.loads(deck_path.read_text(encoding="utf-8"))
        brand = json.loads(brand_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Cannot read input: {e}", file=sys.stderr)
        return 2
    try:
        out = build(deck, brand, deck_path, brand_path, a.audience)
    except BuildError as e:
        print(f"BUILD ERROR: {e}", file=sys.stderr)
        return 1
    op = Path(a.out)
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(out, encoding="utf-8")
    size = op.stat().st_size
    print(f"Built {op} ({size / 1024:.0f} KB, audience {a.audience}).")
    for w in warnings:
        print(f"  WARN {w}")
    if size > 8 * 1024 * 1024:
        print("  WARN file is over 8 MB. Check embedded fonts and images")
    return 0


if __name__ == "__main__":
    sys.exit(main())
