#!/usr/bin/env python3
"""Build a show-week brief: one private, branded page about a prospect's coming show.

    python3 build_brief.py brief/brief.json brand/brand.json --out build/acme_cloudsec_brief.html
    python3 build_brief.py brief/brief.json brand/brand.json --out build/acme_cloudsec_brief.html --pdf build/acme_cloudsec_brief.pdf

The page holds: the prospect's presence at the show and its audience, the week day by
day (what they fund, the organiser's programme, the sessions their buyers will attend,
what competitors have announced, and the slots still open), the question the week is
asking, one suggestion with its arithmetic and its honest timing, what only they know,
one call to action, the sources, and the method.

It is one static file: no script, no network request, fonts and the logo embedded. It
prints to two Letter or A4 pages (brief.json "paper"). Brand loading, the three inline
marks (**bold**, [n] for a source, {TBD}) and the copy checks come from the
prospect-deck-builder skill, so the brief and the deck read and check the same way.

Run validate_brief.py before, and brief_check.py after. No third-party dependencies.
Exit status: 0 built, 1 build error, 2 bad usage.
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import _family  # noqa: F401  (puts the sibling skills' scripts on the path)
import build_deck as bd

SHELL = _family.SKILL / "assets" / "brief-shell.html"
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen"]
PARTS = ["breakfast", "morning", "lunch", "afternoon", "evening", "late"]
PART_LABEL = {"breakfast": "Breakfast", "morning": "Morning", "lunch": "Lunch", "afternoon": "Afternoon",
              "evening": "Evening", "late": "Late"}
KINDS = {"yours": "Yours", "open": "Open", "session": "Session", "official": "Official",
         "competitor": "Competitor", "side": "Side event", "partner": "Partner"}
CLEARED_RATES = {0.70: ("invite-only executive dinner", "11"), 0.86: ("VIP or sport hospitality", "12"),
                 0.19: ("vendor-owned conference", "12")}


def d(s):
    return dt.date.fromisoformat(s)


def day_label(x):
    return f"{x.day} {x.strftime('%B')} {x.year}"


def span(a, b):
    if a == b:
        return day_label(a)
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.day} to {b.day} {b.strftime('%B')} {b.year}"
    if a.year == b.year:
        return f"{a.day} {a.strftime('%B')} to {b.day} {b.strftime('%B')} {b.year}"
    return f"{day_label(a)} to {day_label(b)}"


def words(n):
    return WORDS[n] if 0 <= n < len(WORDS) else str(n)


def need(obj, key, where):
    v = (obj or {}).get(key)
    if v in (None, "", [], {}):
        raise bd.BuildError(f"{where}.{key} is required")
    return v


def body(brief, logo_img):
    f = bd.fmt
    p, show = brief["prospect"], brief["show"]
    company = need(p, "company", "prospect")
    date = d(need(brief, "date", "brief"))
    start, end = d(need(show, "start", "show")), d(need(show, "end", "show"))
    weeks = round((start - date).days / 7)
    out = (f'<header class="mast"><div class="who">{logo_img}<span>{f("Prepared for " + company)}</span></div>'
           f'<div>Show-week brief, version {bd.esc(brief.get("version", "v1").lstrip("v"))}, {day_label(date)}</div></header>')
    out += (f'<p class="kicker">{f(brief.get("kicker") or ("Show-week brief, " + show["name"]))}</p>'
            f'<h1>{f(need(brief, "headline", "brief"), "headline")}</h1>'
            f'<p class="stand">{f(brief.get("standfirst"), "standfirst")}</p>')
    out += ('<div class="facts">'
            f'<div><span>Your presence</span><p>{f(need(show, "presence", "show"), "show.presence")}</p></div>'
            f'<div><span>The audience</span><p>{f(show.get("audience") or "{TBD}", "show.audience")}</p></div>'
            f'<div><span>The week</span><p>{bd.esc(show["name"])}, {span(start, end)}. '
            f'About {words(weeks)} weeks from {day_label(date)}.</p></div></div>')

    days = need(brief, "days", "brief")
    out += f'<section><h2>The week, day by day</h2><div class="week" style="--days:{len(days)}">'
    for k, day in enumerate(days):
        slots = sorted(day.get("slots") or [], key=lambda s: (PARTS.index(s.get("part", "evening")), s.get("time", "")))
        out += f'<div class="day"><h3>{bd.esc(day.get("label") or d(day["date"]).strftime("%a %d %b"))}</h3>'
        out += f'<span class="dn">{f(day.get("note", ""), f"days[{k}].note")}</span>'
        for s in slots:
            kind = s.get("kind")
            if kind not in KINDS:
                raise bd.BuildError(f"days[{k}]: slot kind {kind!r} is not one of {', '.join(KINDS)}")
            if s.get("part") not in PARTS:
                raise bd.BuildError(f"days[{k}]: slot part {s.get('part')!r} is not one of {', '.join(PARTS)}")
            when = PART_LABEL[s["part"]] + (f" {bd.esc(s['time'])}" if s.get("time") else "")
            out += (f'<div class="slot k-{kind}"><span class="t">{when}, {KINDS[kind]}</span>'
                    f'{f(s.get("title"), f"days[{k}].slot")}</div>')
        out += '</div>'
    as_of = brief.get("open_as_of") or day_label(date)
    out += ('</div><p class="legend"><span><b>Yours</b>: what you already fund</span>'
            f'<span><b>Open</b>: nothing announced on public pages as of {bd.esc(as_of)}</span>'
            '<span><b>Session</b>: on your buyers\' agenda</span><span><b>Official</b>: run by the organiser</span>'
            '<span><b>Competitor</b>: announced by a competitor</span></p></section>')

    out += '<div class="two" style="margin-top:40px"><section><h2>Where your buyers will be</h2><ul class="list">'
    for s in brief.get("buyer_sessions") or []:
        out += f'<li><b>{f(s["title"])}</b><span>{f(s.get("when", ""))}. {f(s.get("why", ""))}</span></li>'
    out += '</ul></section><section><h2>What already competes for their evenings</h2><ul class="list">'
    for c in brief.get("competing_evenings") or []:
        out += f'<li><b>{f(c["host"])}, {f(c["when"])}</b><span>{f(c.get("what", ""))}</span></li>'
    for o in brief.get("open_slots") or []:
        out += f'<li><b>Still open: {f(o["when"])}</b><span>{f(o.get("why", ""))}</span></li>'
    out += '</ul></section></div>'

    q = brief.get("question")
    if q:
        out += (f'<section class="question"><h2>The question the week is asking</h2>'
                f'<blockquote>{f(q["question"], "question")}</blockquote><p>{f(q.get("why", ""), "question.why")}</p></section>')

    sg = need(brief, "suggestion", "brief")
    seats = int(need(sg, "seats", "suggestion"))
    rate = round(float(need(sg, "rate", "suggestion")), 2)
    if rate not in CLEARED_RATES:
        raise bd.BuildError(f"suggestion.rate {rate} is not a cleared attendance rate: {', '.join(str(r) for r in CLEARED_RATES)}")
    conf = int(seats / rate + 0.5)
    ref = f" [{int(sg['source_n'])}]" if sg.get("source_n") else ""
    out += (f'<section class="suggest"><h2>One suggestion: {f(need(sg, "title", "suggestion"))}</h2>'
            f'<p>{f(need(sg, "body", "suggestion"), "suggestion.body")}</p>'
            f'<div class="arith"><div><b>{seats}</b><span>people at the table</span></div>'
            f'<div><b>{conf}</b><span>{f(f"confirmations, roughly, at the {round(rate * 100)}% {CLEARED_RATES[rate][0]} benchmark{ref}")}</span></div></div>'
            f'<p class="when">{f(sg.get("timing", ""), "suggestion.timing")}</p>'
            f'<p class="status">{f(sg.get("status", ""), "suggestion.status")}</p></section>')

    if brief.get("unknowns"):
        out += '<section><h2>What only you know</h2><ul class="unknowns">'
        out += "".join(f"<li>{f(u, 'unknowns')}</li>" for u in brief["unknowns"])
        out += '</ul></section>'

    nx, cta = brief.get("next_step") or {}, need(brief, "cta", "brief")
    out += (f'<section class="next"><h2>{f(nx.get("headline", "The next step"))}</h2><p>{f(nx.get("body", ""), "next_step.body")}</p>'
            f'<a class="btn" href="{bd.esc(need(cta, "href", "cta"))}" data-print="{bd.esc(cta["href"].replace("mailto:", "").split("?")[0])}" '
            f'rel="noopener noreferrer">{bd.esc(need(cta, "label", "cta"))}</a></section>')

    out += '<section class="small"><div class="two">'
    out += f'<div><h2>How this was made</h2><p>{f(brief.get("method", ""), "method")}</p></div>'
    out += '<div><h2>Sources</h2><ol>'
    for s in brief.get("sources") or []:
        bd.check_text(s.get("text"), "sources")
        link = f' <a href="{bd.esc(s["url"])}" rel="noopener noreferrer" target="_blank">Link</a>' if s.get("url") else ""
        kind = f' ({bd.esc(s["kind"])})' if s.get("kind") else ""
        out += f'<li id="src-{int(s["n"])}" value="{int(s["n"])}">{bd.esc(s["text"])}{kind}{link}</li>'
    out += '</ol></div></div></section>'
    out += (f'<footer><span>Prepared by The Warm Channel for {bd.esc(company)}, {day_label(date)}.</span>'
            f'<span>Prepared privately for {bd.esc(company)}. Not for distribution.</span>'
            '<span>This page makes no network request.</span></footer>')
    return out


def build(brief, brand, brief_path, brand_path):
    if brief.get("schema") != "twc.show-week-brief/1":
        raise bd.BuildError(f"schema is {brief.get('schema')!r}, expected twc.show-week-brief/1")
    tokens, faces, logo_img = bd.load_brand(brand, brand_path.parent)
    html_body = body(brief, logo_img)
    paper = {"letter": "Letter", "a4": "A4"}.get(str(brief.get("paper", "letter")).lower(), "Letter")
    digest = hashlib.sha256(brief_path.read_bytes() + brand_path.read_bytes()).hexdigest()[:12]
    show = brief["show"]
    info = (f"<!-- Show-week brief. Built {dt.date.today().isoformat()} by prospect-show-week-brief. Audience: send. "
            f"Version: {bd.esc(brief.get('version', 'v1'))}. Source digest: {digest}. -->")
    repl = {
        "<!--@LANG@-->": bd.esc(brief["prospect"].get("lang", "en-CA")),
        "<!--@TITLE@-->": bd.esc(f"{show['name']} week, prepared for {brief['prospect']['company']}"),
        "<!--@BUILDINFO@-->": info,
        "/*@FONTFACES@*/": faces,
        "/*@TOKENS@*/": tokens,
        "/*@PAGE@*/": f"@page{{size:{paper};margin:11mm}}",
        "<!--@BODY@-->": html_body,
    }
    shell = SHELL.read_text(encoding="utf-8")
    for k, v in repl.items():
        if k not in shell:
            raise bd.BuildError(f"shell is missing slot {k}")
        shell = shell.replace(k, v)
    return shell


def print_pdf(html_path, pdf_path):
    import screenshot as ss
    chrome = ss.find_chrome(None)
    if not chrome:
        print("  Chrome not found: open the page and print to PDF from the browser", file=sys.stderr)
        return 1
    cmd = ss.chrome_cmd(chrome, [f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer"], Path(html_path).resolve().as_uri(),
                        1280, 900, 800)
    code, err = ss.run(cmd, timeout=120)
    if code or not Path(pdf_path).exists():
        print(f"  PDF failed: {err}", file=sys.stderr)
        return 1
    print(f"PDF: {pdf_path} ({Path(pdf_path).stat().st_size / 1024:.0f} KB). Two pages is the target.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brief")
    ap.add_argument("brand")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pdf")
    a = ap.parse_args()
    bp, kp = Path(a.brief).resolve(), Path(a.brand).resolve()
    try:
        brief = json.loads(bp.read_text(encoding="utf-8"))
        brand = json.loads(kp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Cannot read input: {e}", file=sys.stderr)
        return 2
    try:
        html_out = build(brief, brand, bp, kp)
    except (bd.BuildError, KeyError, ValueError) as e:
        print(f"BUILD ERROR: {e}", file=sys.stderr)
        return 1
    op = Path(a.out)
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(html_out, encoding="utf-8")
    print(f"Built {op} ({op.stat().st_size / 1024:.0f} KB).")
    for w in bd.warnings:
        print(f"  WARN {w}")
    if a.pdf:
        Path(a.pdf).parent.mkdir(parents=True, exist_ok=True)
        return print_pdf(op, Path(a.pdf).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
