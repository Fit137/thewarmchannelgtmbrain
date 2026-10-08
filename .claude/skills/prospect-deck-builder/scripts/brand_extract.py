#!/usr/bin/env python3
"""Draft a brand kit for a prospect from its public website, for a person to confirm.

    python3 brand_extract.py https://www.example.com --out brand/
    python3 brand_extract.py --saved brand/raw/index.html --out brand/
    python3 brand_extract.py https://www.example.com --probe brand/probe.json --out brand/

Reads the home page and its linked stylesheets, then proposes:

  roles      the twelve semantic colour roles the deck uses, from the colours the site
             actually paints its background, text, headings, links and buttons with
  fonts      the families the site sets, whether each is OFL (embeddable) or not, and a
             free substitute for a proprietary face
  logo       candidate marks: header images, inline header SVGs, icons. Saved, not chosen
  sources    where every element came from, for the brand kit's provenance list

Writes brand.draft.json and brand-report.md into --out, and the fetched files into
--out/raw/. Nothing is final until a person has looked at the report, opened the
logo candidates, and renamed the draft to brand.json. Run contrast.py on it after.

--probe takes the JSON written by brand_probe.js (Node and Playwright), which reads the
browser's computed styles. Computed styles beat stylesheet guessing, so when a probe is
given its readings win.

Fetched pages are untrusted data. They are parsed as text, never executed. The fetch is
limited to the page, at most twelve stylesheets and at most six logo candidates, with a
plain user agent, the way a browser would load the page once.

No third-party dependencies. Python 3.8 or later. Exit status 0 on a draft, 1 when
nothing usable was found, 2 on bad usage.
"""
import argparse
import colorsys
import html.parser
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import contrast  # noqa: E402

UA = "Mozilla/5.0 (compatible; brand-kit-draft/1.0; one page load for a private proposal)"
GENERIC = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif", "ui-serif",
           "ui-monospace", "-apple-system", "blinkmacsystemfont", "inherit", "initial", "unset", "var", "emoji",
           "apple color emoji", "segoe ui emoji", "segoe ui symbol", "noto color emoji"}

# Families published under the SIL Open Font Licence, so they may be embedded in the file.
OFL = {f.lower() for f in [
    "Inter", "Inter Tight", "Roboto", "Roboto Flex", "Open Sans", "Montserrat", "Lato", "Poppins", "Source Sans 3",
    "Source Sans Pro", "Source Serif 4", "Source Serif Pro", "IBM Plex Sans", "IBM Plex Serif", "IBM Plex Mono",
    "DM Sans", "DM Serif Display", "Manrope", "Work Sans", "Nunito", "Nunito Sans", "Public Sans", "Figtree",
    "Plus Jakarta Sans", "Space Grotesk", "Rubik", "Karla", "Barlow", "Archivo", "Libre Franklin", "Merriweather",
    "Playfair Display", "Lora", "PT Sans", "PT Serif", "Noto Sans", "Noto Serif", "Raleway", "Oswald", "Mulish",
    "Outfit", "Sora", "Urbanist", "Lexend", "Red Hat Display", "Red Hat Text", "Albert Sans", "Hanken Grotesk",
    "Instrument Sans", "Onest", "Geologica", "Fraunces", "Newsreader", "EB Garamond", "Cormorant Garamond",
    "Libre Baskerville", "Crimson Pro", "Spectral", "Jost", "Josefin Sans", "Bricolage Grotesque", "Schibsted Grotesk",
    "Be Vietnam Pro", "Epilogue", "Syne", "Space Mono", "JetBrains Mono", "Fira Sans", "Fira Code", "Cabin", "Heebo",
    "Assistant", "Hind", "Mukta", "Overpass", "Titillium Web", "Exo 2", "Kanit", "Prompt", "Quicksand", "Comfortaa",
    "Bitter", "Zilla Slab", "Roboto Slab", "Roboto Serif", "Roboto Condensed", "Barlow Condensed", "Archivo Narrow",
    "Geist", "Geist Mono", "Atkinson Hyperlegible", "Golos Text", "Wix Madefor Display", "Wix Madefor Text"]}

# Common proprietary faces and the free families that sit closest. Judge by eye.
SUBSTITUTES = {
    "helvetica": ["Inter", "Public Sans"], "helvetica neue": ["Inter", "Public Sans"], "neue haas": ["Inter"],
    "arial": ["Inter", "Public Sans"], "gotham": ["Montserrat"], "proxima nova": ["Figtree", "Montserrat"],
    "avenir": ["Nunito Sans", "Figtree"], "avenir next": ["Nunito Sans", "Figtree"], "futura": ["Jost"],
    "circular": ["DM Sans", "Plus Jakarta Sans"], "graphik": ["Inter", "Hanken Grotesk"],
    "gt america": ["Inter", "Public Sans"], "gt walsheim": ["DM Sans", "Albert Sans"], "söhne": ["Inter"],
    "sohne": ["Inter"], "akzidenz": ["Archivo", "Inter"], "univers": ["Public Sans"], "frutiger": ["Hind", "Mukta"],
    "gill sans": ["Lato"], "founders grotesk": ["Hanken Grotesk"], "calibre": ["Hanken Grotesk", "Inter"],
    "brandon grotesque": ["Josefin Sans", "Raleway"], "din": ["Barlow", "Barlow Condensed"],
    "tiempos": ["Source Serif 4", "Newsreader"], "canela": ["Fraunces"], "freight": ["Source Serif 4"],
    "lyon": ["Source Serif 4"], "publico": ["Source Serif 4", "Newsreader"], "segoe ui": ["Inter", "Open Sans"],
    "sf pro": ["Inter"], "san francisco": ["Inter"], "aeonik": ["Manrope", "Albert Sans"], "basis grotesque": ["Hanken Grotesk"],
    "neue montreal": ["Inter", "Hanken Grotesk"], "suisse": ["Inter"], "aktiv grotesk": ["Inter", "Public Sans"],
    "museo sans": ["Nunito Sans"], "effra": ["Rubik"], "ff meta": ["Fira Sans"], "verdana": ["Public Sans"],
}

DEFAULT_STATUS = {"positive": "#17803D", "caution": "#8A5A00", "flag": "#B42318"}
HEX = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RGB = re.compile(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})(?:[\s,/]+([\d.]+%?))?\s*\)", re.I)


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
def norm_hex(h):
    h = h.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    elif len(h) == 8:
        h = h[:6]
    return "#" + h.upper()


def parse_colour(tok):
    """A solid colour as #RRGGBB, or None for a translucent one, which is not a brand role."""
    tok = tok.strip()
    m = HEX.fullmatch(tok)
    if m:
        digits = tok[1:]
        if len(digits) in (4, 8):
            a = digits[-1] * 2 if len(digits) == 4 else digits[-2:]
            if int(a, 16) / 255.0 < 0.85:
                return None
        return norm_hex(tok)
    m = RGB.fullmatch(tok)
    if m:
        a = m.group(4)
        if a:
            av = float(a[:-1]) / 100 if a.endswith("%") else float(a)
            if av < 0.85:
                return None
        r, g, b = (max(0, min(255, int(m.group(i)))) for i in (1, 2, 3))
        return f"#{r:02X}{g:02X}{b:02X}"
    return None


def colours_in(text):
    out = []
    for m in HEX.finditer(text):
        c = parse_colour(m.group(0))
        if c:
            out.append(c)
    for m in RGB.finditer(text):
        c = parse_colour(m.group(0))
        if c:
            out.append(c)
    return out


def hls(h):
    r, g, b = contrast.hex_to_rgb(h)
    return colorsys.rgb_to_hls(r, g, b)


def is_neutral(h):
    _, l, s = hls(h)
    return s < 0.14 or l < 0.08 or l > 0.97


def shade(h, dl):
    hh, l, s = hls(h)
    return contrast.rgb_to_hex(colorsys.hls_to_rgb(hh, max(0.0, min(1.0, l + dl)), s))


def mix(a, b, t):
    ra, rb = contrast.hex_to_rgb(a), contrast.hex_to_rgb(b)
    return contrast.rgb_to_hex(tuple(x * (1 - t) + y * t for x, y in zip(ra, rb)))


# ---------------------------------------------------------------------------
# Fetching and parsing
# ---------------------------------------------------------------------------
def fetch(url, max_bytes=3_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = r.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"{url} is larger than {max_bytes} bytes")
        ctype = r.headers.get("Content-Type", "")
        return data, ctype, r.geturl()


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.styles, self.inline, self.sheets, self.imgs, self.icons = [], [], [], [], []
        self.meta, self.fontlinks = {}, []
        self.svgs = []           # (in_header, attrs, markup)
        self._stack = []
        self._svg_depth = 0
        self._svg_buf = []
        self._in_style = False
        self._title = []
        self._in_title = False

    def in_header(self):
        return any(t in ("header", "nav") or "header" in a.get("class", "") or "navbar" in a.get("class", "")
                   for t, a in self._stack)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if self._svg_depth:
            self._svg_depth += 1
            self._svg_buf.append(self.get_starttag_text() or "")
            return
        if tag == "svg":
            self._svg_depth = 1
            self._svg_buf = [self.get_starttag_text() or "<svg>"]
            self._svg_attrs = (self.in_header(), a)
            return
        if tag not in ("img", "link", "meta", "br", "input", "source", "hr"):
            self._stack.append((tag, a))
        if tag == "style":
            self._in_style = True
        if tag == "title":
            self._in_title = True
        if "style" in a:
            self.inline.append(a["style"])
        if tag == "link":
            rel = a.get("rel", "").lower()
            href = a.get("href", "")
            if "stylesheet" in rel and href:
                self.sheets.append(href)
                if "fonts.googleapis.com" in href or "typekit" in href or "fonts.adobe" in href:
                    self.fontlinks.append(href)
            if any(x in rel for x in ("icon", "apple-touch-icon", "mask-icon")) and href:
                self.icons.append({"href": href, "rel": rel, "color": a.get("color", "")})
        if tag == "meta":
            k = (a.get("name") or a.get("property") or "").lower()
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "img":
            hint = " ".join([a.get("src", ""), a.get("alt", ""), a.get("class", ""), a.get("id", "")]).lower()
            self.imgs.append({"src": a.get("src") or a.get("data-src", ""), "alt": a.get("alt", ""),
                              "logo": "logo" in hint or "brand" in hint, "header": self.in_header()})

    def handle_endtag(self, tag):
        if self._svg_depth:
            self._svg_buf.append(f"</{tag}>")
            self._svg_depth -= 1
            if self._svg_depth == 0:
                in_head, a = self._svg_attrs
                markup = "".join(self._svg_buf)
                self.svgs.append((in_head, a, markup))
            return
        if tag == "style":
            self._in_style = False
        if tag == "title":
            self._in_title = False
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_startendtag(self, tag, attrs):
        if self._svg_depth:
            self._svg_buf.append(self.get_starttag_text() or "")
            return
        self.handle_starttag(tag, attrs)
        if self._stack and self._stack[-1][0] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._svg_depth:
            self._svg_buf.append(data)
        elif self._in_style:
            self.styles.append(data)
        elif self._in_title:
            self._title.append(data)


RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
DECL = re.compile(r"([-\w]+)\s*:\s*([^;]+)")


def css_rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for m in RULE.finditer(css):
        sel = m.group(1).strip()
        if sel.startswith("@"):
            sel = sel.split("{")[-1]
        for d in DECL.finditer(m.group(2)):
            yield sel, d.group(1).strip().lower(), d.group(2).strip()


def resolve_vars(css):
    vars_ = {}
    for sel, prop, val in css_rules(css):
        if prop.startswith("--"):
            vars_.setdefault(prop, val)
    return vars_


def deref(val, vars_, depth=0):
    if depth > 5:
        return val
    return re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)",
                  lambda m: deref(vars_.get(m.group(1), m.group(2) or ""), vars_, depth + 1), val)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
def score_colours(css, page, probe):
    vars_ = resolve_vars(css)
    votes = {k: Counter() for k in ("surface", "ink", "body", "accent", "rule", "surface_2", "positive", "caution", "flag")}
    seen = Counter()
    where = defaultdict(list)

    def vote(role, colour, w, why):
        if colour:
            votes[role][colour] += w
            where[colour].append(why)

    for name, val in vars_.items():
        for c in colours_in(deref(val, vars_)):
            n = name.lower()
            if re.search(r"primary|brand|accent|cta|highlight", n):
                vote("accent", c, 6, f"CSS variable {name}")
            if re.search(r"success|positive|green", n):
                vote("positive", c, 4, f"CSS variable {name}")
            if re.search(r"warn|caution|amber|yellow", n):
                vote("caution", c, 4, f"CSS variable {name}")
            if re.search(r"danger|error|critical|red\b", n):
                vote("flag", c, 4, f"CSS variable {name}")
            if re.search(r"background|bg|surface|canvas|base", n) and is_neutral(c):
                vote("surface", c, 2, f"CSS variable {name}")
            if re.search(r"text|foreground|fg|body", n):
                vote("body", c, 2, f"CSS variable {name}")
            if re.search(r"heading|title|ink|dark", n):
                vote("ink", c, 2, f"CSS variable {name}")
            if re.search(r"border|divider|rule|line|stroke", n):
                vote("rule", c, 2, f"CSS variable {name}")
    for sel, prop, val in css_rules(css):
        v = deref(val, vars_)
        cs = colours_in(v)
        if not cs:
            continue
        s = sel.lower()
        for c in cs:
            seen[c] += 1
        c = cs[0]
        is_bg = prop in ("background", "background-color")
        if re.search(r"(^|[\s,])(html|body)\b", s):
            if is_bg:
                vote("surface", c, 8, f"{sel} {prop}")
            elif prop == "color":
                vote("body", c, 8, f"{sel} color")
        if re.search(r"\bh1\b|\bh2\b|\bh3\b|heading|title", s) and prop == "color":
            vote("ink", c, 5, f"{sel} color")
        if re.search(r"(^|[\s,>])a\b|link", s) and prop == "color" and not is_neutral(c):
            vote("accent", c, 3, f"{sel} color")
        if re.search(r"btn|button|cta|primary", s) and is_bg and not is_neutral(c):
            vote("accent", c, 5, f"{sel} {prop}")
        if prop.startswith("border") and is_neutral(c):
            vote("rule", c, 1, f"{sel} {prop}")
        if is_bg and is_neutral(c) and re.search(r"section|card|panel|band|alt|muted|light|grey|gray", s):
            vote("surface_2", c, 2, f"{sel} {prop}")
    tc = page.meta.get("theme-color") if page else None
    if tc and parse_colour(tc):
        c = parse_colour(tc)
        vote("accent" if not is_neutral(c) else "ink", c, 4, "meta theme-color")
    for ic in (page.icons if page else []):
        if ic.get("color") and parse_colour(ic["color"]):
            vote("accent", parse_colour(ic["color"]), 3, "mask-icon color")
    if probe:
        cs = probe.get("computed") or {}
        pc = {k: parse_colour(v) for k, v in cs.items() if isinstance(v, str)}
        vote("surface", pc.get("body_bg"), 20, "computed body background")
        vote("body", pc.get("body_color"), 20, "computed body text")
        vote("ink", pc.get("h1_color") or pc.get("h2_color"), 18, "computed heading colour")
        if pc.get("button_bg") and not is_neutral(pc["button_bg"]):
            vote("accent", pc["button_bg"], 20, "computed primary button background")
        if pc.get("link_color") and not is_neutral(pc["link_color"]):
            vote("accent", pc["link_color"], 10, "computed link colour")
    return votes, seen, where


def pick(votes, role):
    return votes[role].most_common(1)[0][0] if votes[role] else None


def propose_roles(votes, seen):
    surface = pick(votes, "surface")
    if not surface or not is_neutral(surface) or hls(surface)[1] < 0.85:
        lights = [c for c, _ in seen.most_common() if is_neutral(c) and hls(c)[1] >= 0.94]
        surface = surface if surface and hls(surface)[1] >= 0.85 else (lights[0] if lights else "#FFFFFF")
    neutrals_dark = [c for c, _ in seen.most_common() if is_neutral(c) and hls(c)[1] <= 0.3]
    ink = pick(votes, "ink") or (min(neutrals_dark, key=lambda c: hls(c)[1]) if neutrals_dark else "#111111")
    if contrast.ratio(ink, surface) < 7:
        ink = "#111111" if contrast.luminance(surface) > 0.4 else "#FFFFFF"
    body = pick(votes, "body") or ink
    if contrast.ratio(body, surface) < 4.5:
        body = ink
    chroma = [c for c, _ in votes["accent"].most_common() if not is_neutral(c)]
    if not chroma:
        chroma = [c for c, _ in seen.most_common() if not is_neutral(c)]
    accent = chroma[0] if chroma else ink
    accent_ink = shade(accent, -0.10)
    on_accent = max((surface, "#FFFFFF", ink), key=lambda c: contrast.ratio(c, accent))
    muted = mix(body, surface, 0.35)
    if contrast.ratio(muted, surface) < 5.2:  # margin over 4.5, because a projector washes contrast out
        muted = contrast.nudge(muted, surface, 5.2) or body
    rule = pick(votes, "rule") or mix(ink, surface, 0.85)
    if contrast.ratio(rule, surface) > 2.2 or contrast.ratio(rule, surface) < 1.15:
        rule = mix(ink, surface, 0.85)
    s2 = pick(votes, "surface_2")
    if not s2 or contrast.ratio(s2, surface) > 1.25 or contrast.ratio(body, s2) < 4.5:
        s2 = mix(surface, accent, 0.05) if contrast.luminance(surface) > 0.4 else shade(surface, 0.06)
    roles = {"surface": surface, "surface_2": s2, "ink": ink, "body": body, "muted": muted, "rule": rule,
             "accent": accent, "accent_ink": accent_ink, "on_accent": on_accent}
    for k, dflt in DEFAULT_STATUS.items():
        c = pick(votes, k)
        roles[k] = c if c and not is_neutral(c) else dflt
    changes, fixed = contrast.propose(roles)
    return roles, changes, fixed


def fonts_from(css, page, probe):
    """Families the site sets, ranked. Returns (fonts, services, body_family, heading_family)."""
    fams = Counter()
    faces = defaultdict(list)
    body_family = heading_family = None
    vars_ = resolve_vars(css)
    for sel, prop, val in css_rules(css):
        if prop == "font-family" or (prop == "font" and "," in val):
            val = deref(val, vars_)
            first = [f.strip().strip("'\"") for f in val.split(",")]
            for f in first:
                f = f.split()[-1] if prop == "font" and " " in f and f[0].isdigit() else f
                if f and f.lower() not in GENERIC and not f.lower().startswith("var("):
                    heading = re.search(r"\bh1\b|\bh2\b|heading|title|display", sel.lower())
                    fams[f] += 3 if heading else 1
                    if re.search(r"(^|[\s,])(html|body)\b", sel.lower()) and not body_family:
                        body_family = f
                    if heading and not heading_family:
                        heading_family = f
                    break
    for m in re.finditer(r"@font-face\s*\{([^}]*)\}", css, re.I):
        body = m.group(1)
        fam = re.search(r"font-family\s*:\s*['\"]?([^;'\"]+)", body)
        src = re.findall(r"url\(\s*['\"]?([^)'\"]+)", body)
        if fam:
            faces[fam.group(1).strip()].extend(src[:2])
    if probe:
        for k in ("body_font", "h1_font"):
            v = (probe.get("computed") or {}).get(k)
            if v:
                f = v.split(",")[0].strip().strip("'\"")
                if f.lower() not in GENERIC:
                    fams[f] += 20
                    if k == "body_font":
                        body_family = f
                    else:
                        heading_family = f
    out = []
    for f, n in fams.most_common(6):
        low = f.lower()
        ofl = low in OFL
        subs = []
        if not ofl:
            for key, s in SUBSTITUTES.items():
                if key in low:
                    subs = s
                    break
        out.append({"family": f, "weight_of_evidence": n, "ofl": ofl, "faces": faces.get(f, [])[:2],
                    "substitutes": subs})
    services = list(page.fontlinks if page else [])
    return out, services, body_family, heading_family


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?", help="the prospect's home page")
    ap.add_argument("--saved", help="a saved copy of the page instead of fetching it. Linked .css files are read from beside it")
    ap.add_argument("--css", nargs="*", default=[], help="extra stylesheet files to read")
    ap.add_argument("--probe", help="probe.json written by brand_probe.js")
    ap.add_argument("--company", help="the company name, for the draft")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-fetch-assets", action="store_true", help="read the page only, no stylesheets or logos")
    a = ap.parse_args()
    if not a.url and not a.saved and not a.probe:
        ap.error("give a URL, --saved or --probe")
    out = Path(a.out)
    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    sources, css_parts, notes = [], [], []
    page = Page()
    base_url = a.url
    try:
        if a.saved:
            sp = Path(a.saved)
            html_text = sp.read_text(encoding="utf-8", errors="replace")
            base_url = a.url or sp.resolve().as_uri()
            sources.append({"element": "page", "from": f"saved copy {sp.name}", "url": a.url})
        elif a.url:
            data, ctype, final = fetch(a.url)
            html_text = data.decode("utf-8", errors="replace")
            (raw / "index.html").write_text(html_text, encoding="utf-8")
            base_url = final
            sources.append({"element": "page", "from": "home page, fetched once", "url": final})
        else:
            html_text = ""
    except Exception as e:
        print(f"could not read the page: {e}", file=sys.stderr)
        return 1
    page.feed(html_text)
    css_parts.extend(page.styles)
    css_parts.extend(page.inline and ["x{" + ";".join(page.inline) + "}"] or [])
    for i, href in enumerate(page.sheets[:12]):
        if "fonts.googleapis.com" in href or "typekit" in href:
            continue
        url = urllib.parse.urljoin(base_url, href)
        try:
            if url.startswith("file:"):
                p = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path))
                css_parts.append(p.read_text(encoding="utf-8", errors="replace"))
            elif not a.no_fetch_assets:
                data, _, _ = fetch(url, 2_000_000)
                txt = data.decode("utf-8", errors="replace")
                (raw / f"sheet-{i + 1}.css").write_text(txt, encoding="utf-8")
                css_parts.append(txt)
            sources.append({"element": "stylesheet", "from": f"linked stylesheet {i + 1}", "url": url})
        except Exception as e:
            notes.append(f"stylesheet not read: {url} ({e})")
    for c in a.css:
        css_parts.append(Path(c).read_text(encoding="utf-8", errors="replace"))
        sources.append({"element": "stylesheet", "from": f"file {Path(c).name}", "url": None})
    css = "\n".join(css_parts)
    probe = json.loads(Path(a.probe).read_text(encoding="utf-8")) if a.probe else None
    if probe:
        sources.append({"element": "computed styles", "from": "brand_probe.js, read from the rendered page", "url": probe.get("url")})

    votes, seen, where = score_colours(css, page, probe)
    if not seen and not probe:
        print("no colours found. Save the page with its stylesheets, or run brand_probe.js", file=sys.stderr)
    roles, changes, fixed = propose_roles(votes, seen)
    fonts, services, body_family, heading_family = fonts_from(css, page, probe)

    # Logo candidates: header images first, then any image named logo, then inline header SVGs, then icons.
    cands = []
    for im in page.imgs:
        if (im["logo"] or im["header"]) and im["src"]:
            wall = bool(re.search(r"customer|client|partner|logos\b|trusted|press", (im["src"] + " " + im["alt"]).lower()))
            cands.append({"kind": "image", "src": urllib.parse.urljoin(base_url or "", im["src"]), "alt": im["alt"],
                          "why": ("probably a wall of other companies' logos, not theirs" if wall else
                                  "header image" if im["header"] else "image named logo"),
                          "rank": (0 if im["header"] else 1) + (5 if wall else 0)})
    for k, (in_head, attrs, markup) in enumerate(page.svgs):
        hint = " ".join(attrs.get(x, "") for x in ("class", "id", "aria-label", "role")).lower()
        if in_head or "logo" in hint or "brand" in hint:
            p = raw / f"logo-candidate-svg-{k + 1}.svg"
            if "xmlns" not in markup[:200]:
                markup = markup.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            p.write_text(markup, encoding="utf-8")
            cands.append({"kind": "inline svg", "src": str(p), "alt": attrs.get("aria-label", ""),
                          "why": "inline SVG in the header" if in_head else "inline SVG named logo",
                          "rank": 0 if in_head else 1})
    for ic in page.icons:
        cands.append({"kind": "icon", "src": urllib.parse.urljoin(base_url or "", ic["href"]), "alt": "",
                      "why": f"link rel {ic['rel']}, a small mark, last resort", "rank": 4})
    cands.sort(key=lambda c: c["rank"])
    if probe and probe.get("logo_png"):
        cands.insert(0, {"kind": "rendered", "src": probe["logo_png"], "alt": "", "why": "screenshot of the header mark, from brand_probe.js"})
    saved = 0
    for c in cands:
        if c["kind"] in ("image", "icon") and c["src"].startswith("http") and not a.no_fetch_assets and saved < 6:
            try:
                data, ctype, _ = fetch(c["src"], 2_000_000)
                ext = {"image/svg+xml": ".svg", "image/png": ".png", "image/webp": ".webp", "image/jpeg": ".jpg",
                       "image/x-icon": ".ico", "image/vnd.microsoft.icon": ".ico"}.get(ctype.split(";")[0].strip(), "")
                ext = ext or Path(urllib.parse.urlparse(c["src"]).path).suffix or ".bin"
                p = raw / f"logo-candidate-{saved + 1}{ext}"
                p.write_bytes(data)
                c["saved"] = str(p)
                saved += 1
            except Exception as e:
                c["error"] = str(e)
        elif c["kind"] in ("image", "icon") and c["src"].startswith("file:"):
            c["saved"] = urllib.parse.unquote(urllib.parse.urlparse(c["src"]).path)

    company = a.company or (page._title and re.split(r"\s[|:\u2013\u2014-]\s", "".join(page._title).strip())[0]) or "{TBD}"
    by_name = {f["family"]: f for f in fonts}
    display = by_name.get(heading_family) or next((f for f in fonts if f["weight_of_evidence"] >= 3), fonts[0] if fonts else None)
    text_f = by_name.get(body_family) or (fonts[-1] if fonts else None)

    def font_slot(f, weight):
        if not f:
            return {"family": "System", "fallback": "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif",
                    "licence": "system fonts, nothing embedded", "files": []}
        if f["ofl"]:
            return {"family": f["family"], "weight": weight, "fallback": "system-ui, sans-serif",
                    "licence": "OFL 1.1. Fetch with fetch_font.py and keep the licence file", "files": [],
                    "substitute_for": None}
        sub = (f["substitutes"] or ["Public Sans"])[0]
        return {"family": f"{sub}", "weight": weight, "fallback": "system-ui, sans-serif",
                "licence": "OFL 1.1. Fetch with fetch_font.py and keep the licence file", "files": [],
                "substitute_for": f"{f['family']}, the brand's own face, which may not be redistributed"}

    draft = {
        "schema": "twc.prospect-brand/1",
        "company": company,
        "note": "DRAFT from brand_extract.py. Confirm every role, the type and the logo against the live site and any public brand guidelines, then save as brand.json.",
        "skin": "prospect",
        "captured": __import__("datetime").date.today().isoformat(),
        "sources": sources + [{"element": f"role {r}", "from": "; ".join(dict.fromkeys(where.get(v, ["derived from the other roles"])))[:200], "url": None}
                              for r, v in fixed.items()],
        "guidelines": {"url": None, "constraints": [
            "Logo used only to identify the recipient, in the Prepared for line and the top bar",
            "Logo never recoloured, stretched, animated or placed in a lockup with another mark"]},
        "roles": fixed,
        "fonts": {"display": font_slot(display, 600), "text": font_slot(text_f, 400)},
        "radius": "6px",
        "logo": {"path": None, "alt": company, "usage": "prepared-for only"},
        "twc_signature": "Prepared by The Warm Channel",
    }
    (out / "brand.draft.json").write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    R = [f"# Brand kit draft, {company}\n",
         "Read this, open every logo candidate, then edit brand.draft.json and save it as brand.json. Nothing here is final.\n",
         "## Proposed roles\n", "| Role | Proposed | Before contrast fix | Evidence |", "|---|---|---|---|"]
    for r in ["surface", "surface_2", "ink", "body", "muted", "rule", "accent", "accent_ink", "on_accent", "positive", "caution", "flag"]:
        before = roles.get(r)
        ev = "; ".join(dict.fromkeys(where.get(before, ["derived"])))[:140]
        R.append(f"| {r} | `{fixed[r]}` | `{before}` | {ev} |")
    R.append("\n## Contrast after the proposal\n")
    R.append("| Pair | Ratio | Needs | Status |\n|---|---|---|---|")
    for row in contrast.evaluate(fixed):
        rt = f"{row['ratio']:.2f}" if row["ratio"] is not None else "-"
        R.append(f"| {row['fg']} on {row['bg']} | {rt} | {row['need']} | {row['status']} |")
    R.append("\n## Most used colours on the site\n")
    for c, n in seen.most_common(14):
        R.append(f"- `{c}` used {n} times" + (" (neutral)" if is_neutral(c) else ""))
    R.append("\n## Type\n")
    for f in fonts:
        verdict = "OFL, can be embedded" if f["ofl"] else ("proprietary or unknown licence. Substitute: " + ", ".join(f["substitutes"] or ["Public Sans, or judge by eye"]))
        R.append(f"- **{f['family']}**, evidence weight {f['weight_of_evidence']}. {verdict}.")
    for s in services:
        R.append(f"- Font service linked: {s}. A web font service is never called from the deck: embed an OFL file instead.")
    R.append("\n## Logo candidates\n")
    if not cands:
        R.append("- None found. Save the mark from the site by hand, SVG if they publish one, and record where it came from.")
    for c in cands:
        R.append(f"- {c['kind']}: {c.get('saved') or c['src']} ({c['why']})" + (f", alt '{c['alt']}'" if c.get("alt") else "") +
                 (f". Not saved: {c['error']}" if c.get("error") else ""))
    R.append("\n## Before this becomes brand.json\n")
    R += ["- [ ] Each role checked against the live site. The accent is the brand's own primary, not a one-off campaign colour",
          "- [ ] Public brand guidelines searched for, and their logo rules copied into guidelines.constraints",
          "- [ ] The mark chosen: the full logo, not the favicon, SVG where one exists, never redrawn or recoloured",
          "- [ ] Proprietary faces replaced by an OFL substitute, fetched with fetch_font.py, licence file kept beside it",
          "- [ ] `contrast.py brand.json` passes",
          "- [ ] The sources list says where every element came from"]
    if notes:
        R.append("\n## Notes\n")
        R += [f"- {n}" for n in notes]
    (out / "brand-report.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    print(f"Wrote {out / 'brand.draft.json'} and {out / 'brand-report.md'}")
    print(f"  accent {fixed['accent']}, ink {fixed['ink']}, surface {fixed['surface']}. {len(cands)} logo candidate(s). "
          f"{len(fonts)} font family(ies) found.")
    if changes:
        print(f"  contrast.py moved: {', '.join(changes)}")
    return 0 if (seen or probe) else 1


if __name__ == "__main__":
    sys.exit(main())
