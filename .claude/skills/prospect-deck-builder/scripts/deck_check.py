#!/usr/bin/env python3
"""Quality gate for a built prospect strategy deck. Run it before anything is sent.

    python3 deck_check.py build/acme_strategy_v1_send.html
    python3 deck_check.py build/acme_strategy_v1_send.html --deck deck.json \
        --register ../strategy/evidence-register.md --design spec/02-design-concepts.md

What it checks, on the built file, because the built file is what the prospect opens:

  Containment   nothing loads from the network, no tracking parameter, no form,
                no frame, no beacon. Links out are allowed, loads are not.
  Copy rules    em and en dashes, banned words, unfilled placeholders, internal
                evidence IDs, retired scope names, claims that read near a ban,
                lines frozen until D11, Commonwealth spelling.
  Guest copy    client vocabulary inside any element marked data-audience="guest".
  Numbers      every percentage and money figure on screen or in the notes must
                trace to the brain's evidence ledger (cleared, grade A or B), to a
                P1 or P2 row in the prospect's evidence register, or to a declared
                entry in deck.json number_provenance. Grade C is an error.
  Structure     every deck opens on a cover and ends with two visible actions,
                every slide has a title, every image has alt text, every chart an
                accessible name.
  Notes         the send build carries no presenter notes. The present build has
                notes on every slide, at about 2.5 words a second.
  Spec          with --deck: notes and screen share no sentence, centrepieces carry
                all seven design fields, one slide is deliberately still, the motif
                appears three to six times. With --design: no hex value, no colour
                function and no typeface name in the design concepts file.

Severities: ERROR blocks sending. WARN is for a person to read and decide. INFO is
context. Exit status 1 on any ERROR, or on any WARN with --strict. 2 on bad usage.

The brain is found from --brain, then the TWC_BRAIN environment variable, then by
walking up from this script, then ../thewarmchannelgtmbrain from the working
directory. When it is found, the banned word, claim and guest lists are loaded
from its scripts/lint_claims.py, so the brain stays the single source.

No third-party dependencies. Python 3.8 or later.
"""
import argparse
import html.parser
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Rule lists. These are fallbacks: when the brain is found, its lint_claims.py
# supplies BANNED_WORDS, DECLARING, BANNED_CLAIMS and GUEST_BANNED instead.
# ---------------------------------------------------------------------------
BANNED_WORDS = ["leverage", "unlock", "seamless", "robust", "streamline",
                "cutting-edge", "cutting edge", "empower"]
DECLARING = re.compile(r"banned words?|do not say|never say|say instead|do not use|forbidden|none of the", re.I)
BANNED_CLAIMS = [
    (r"\b70\s*%\s*(positive\s*)?reply", "the unaudited 70% reply rate, D3"),
    (r"\bguarantee[sd]?\s+(a |any |you )?(meeting|meetings|pipeline|lead|leads|introduction)", "an outcome guarantee"),
    (r"no other channel", "an unscoped superlative"),
    (r"\bour (network|community) of\b", "a claim of an existing network"),
    (r"composed attendance", "the retired category"),
]
GUEST_BANNED = [
    r"\blead generation\b", r"\bleads?\b", r"\bsales-qualified\b", r"\bSQLs?\b",
    r"\bMQLs?\b", r"\bpipeline\b", r"\bfunnel\b", r"\bconver(t|ts|ted|sion|sions)\b",
    r"\bclose rate\b", r"\bdeals?\b", r"\bprospects?\b", r"\btarget accounts?\b",
    r"\bnamed accounts?\b", r"\baccount list\b", r"\bin-ICP\b", r"\bICP\b",
    r"\bcomposed attendance\b", r"\baccess\b", r"\binventory\b", r"\bcoverage\b",
    r"\bshow rate\b", r"\battendance floor\b", r"\bchannel\b", r"\bclients?\b",
    r"\breply rates?\b",
]

# Deck-specific rules, on top of the brain's lint. (pattern, why, severity, flags)
DECK_RULES = [
    (r"\bThe (List|Room|Channel)\b", "a retired scope name, banned until D10", "ERROR", 0),
    (r"\bour (network|community|guest list|executives|members|database|rolodex|relationships)\b",
     "a claim of an existing network or guest list", "ERROR", re.I),
    (r"\b(executives|CISOs?|buyers|leaders) we know\b", "a claim of an existing network", "ERROR", re.I),
    (r"\bwe know (the|every|your|most) (CISOs?|buyers|executives|leaders)\b", "a claim of an existing network", "ERROR", re.I),
    (r"\b(clients?|customers?) (include|including|like|such as)\b", "a client claim. The proof set is empty", "ERROR", re.I),
    (r"\btrusted by\b", "a proof claim. The proof set is empty", "ERROR", re.I),
    (r"\b(we have|we've) (hosted|run|delivered|filled|convened) \d", "a count of our own work. The proof set is empty", "ERROR", re.I),
    (r"\bwe charge\b|\bour (fee|fees|price|prices|pricing|rate card|retainer)\b|\bpricing (starts|from)\b",
     "a price or fee. No price until D2 and D10", "ERROR", re.I),
    (r"\bcase stud(y|ies)\b", "a case study mention. Fine only as the approved 'No case study yet' line", "WARN", re.I),
    (r"\bguarantee", "a guarantee word. None until D4 and D10", "WARN", re.I),
    (r"\bpromise", "a promise word. Check it is not an outcome promise", "WARN", re.I),
    (r"\bwe will (deliver|produce|generate|bring|fill)\b|\byou will (get|receive|see) \d",
     "reads as an outcome commitment", "WARN", re.I),
    (r"\bhand(ed|s|ing)? (it )?(over|off) to your (sellers|sales|reps?|team)\b",
     "post-event hand-over mechanics. Frozen until D11, describe it as designed with the client", "WARN", re.I),
    (r"\bcontext of what was (actually )?said\b", "the frozen hand-over line, D11", "ERROR", re.I),
    (r"\b(your|their|guest'?s?|nobody'?s) details (go|travel|are shared|pass)", "the frozen guest promise, D11", "WARN", re.I),
    (r"\bnothing follows\b", "the frozen guest promise, D11", "ERROR", re.I),
    (r"\b(only|no other) (we|channel|firm|agency|company)\b|\bhighest[- ]quality\b|\bbest[- ]in[- ]class\b|#1\b",
     "an unscoped superlative", "WARN", re.I),
    (r"\bwe bring (you )?(attendees|executives|buyers|guests|CISOs?)\b|\battendees from your ICP\b",
     "attendance as the product, or a network claim", "ERROR", re.I),
    (r"\bpay[- ]on[- ]attendance\b", "pay-on-attendance is never our differentiator, and it implies a price", "WARN", re.I),
    (r"\bMiro\b|\bAimedis\b", "a named client or employer. Gated, never in a prospect deck", "ERROR", 0),
    (r"\bhealthcare (guest|guests|list|business)\b|\bhospital (buyers|guests)\b", "the healthcare business, D6", "ERROR", re.I),
    (r"\$30 ?(million|M)\b|\bSeries A\b", "the founder's credential outside its permitted wording", "WARN", re.I),
]

US_SPELLINGS = [
    (r"\bprogram(s|med|ming)?\b", "programme"), (r"\borganiz(e|es|ed|ing|ation|ations|er|ers)\b", "organis..."),
    (r"\bcolor(s|ed|ful)?\b", "colour"), (r"\bbehavior(s|al)?\b", "behaviour"), (r"\bcenter(s|ed)?\b", "centre"),
    (r"\bfavor(s|ed|ite|able)?\b", "favour"), (r"\banalyz(e|es|ed|ing)\b", "analyse"), (r"\bprioritiz(e|es|ed|ing)\b", "prioritise"),
    (r"\boptimiz(e|es|ed|ing|ation)\b", "optimise"), (r"\bcatalog(s)?\b", "catalogue"), (r"\blabor\b", "labour"),
    (r"\bhonor(s|ed)?\b", "honour"), (r"\bdefense\b", "defence"), (r"\btraveled|traveling\b", "travelled"),
    (r"\bmodeling\b", "modelling"), (r"\brecogniz(e|es|ed|ing)\b", "recognise"), (r"\bsummariz(e|es|ed|ing)\b", "summarise"),
    (r"\bminimiz(e|es|ed|ing)\b", "minimise"), (r"\bmaximiz(e|es|ed|ing)\b", "maximise"),
]

TYPEFACE_NAMES = [
    "Inter", "Helvetica", "Helvetica Neue", "Arial", "Roboto", "Open Sans", "Lato", "Montserrat", "Poppins",
    "Source Sans", "Source Serif", "IBM Plex", "Public Sans", "Work Sans", "DM Sans", "Manrope", "Nunito",
    "Raleway", "Playfair", "Merriweather", "Georgia", "Times New Roman", "Garamond", "EB Garamond", "Futura",
    "Gotham", "Proxima Nova", "Avenir", "Circular", "Graphik", "GT America", "GT Walsheim", "Sohne", "Söhne",
    "Akzidenz", "Univers", "Frutiger", "Gill Sans", "Neue Haas", "Founders Grotesk", "Calibre", "Brandon Grotesque",
    "Tiempos", "Canela", "Freight", "Lyon", "Publico", "Segoe UI", "SF Pro", "San Francisco", "Noto Sans",
    "Noto Serif", "Fira Sans", "Barlow", "Archivo", "Space Grotesk", "Plus Jakarta", "Figtree", "Outfit", "Jost",
    "Fraunces", "Newsreader", "Libre Franklin", "Libre Baskerville", "Crimson", "Spectral", "Karla", "Rubik",
    "Mulish", "Quicksand", "Oswald", "Bebas", "Verdana", "Tahoma", "Trebuchet", "Courier", "Consolas", "Menlo",
    "JetBrains Mono", "system-ui", "sans-serif", "serif", "monospace", "Folio Sans",
]

TRACKING_PARAMS = re.compile(r"[?&](utm_[a-z]+|fbclid|gclid|msclkid|mc_eid|mc_cid|_hsenc|_hsmi|mkt_tok|ref_src|trk|li_fat_id)=", re.I)
NETWORK_JS = re.compile(r"\bfetch\s*\(|XMLHttpRequest|sendBeacon|new\s+WebSocket|new\s+EventSource|new\s+Image\s*\(|\bimport\s*\(|navigator\.connection", re.I)

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
INLINE_JOIN = {"strong", "b", "em", "i", "a", "sup", "sub", "small", "abbr", "code", "mark", "u", "s"}
WORDS_PER_SECOND = 2.5


class Report:
    def __init__(self):
        self.items = []

    def add(self, sev, where, msg):
        self.items.append({"severity": sev, "where": where, "message": msg})

    def count(self, sev):
        return sum(1 for i in self.items if i["severity"] == sev)


# ---------------------------------------------------------------------------
# Brain discovery and rule loading
# ---------------------------------------------------------------------------
def find_brain(arg):
    cands = []
    if arg:
        cands.append(Path(arg))
    if os.environ.get("TWC_BRAIN"):
        cands.append(Path(os.environ["TWC_BRAIN"]))
    here = Path(__file__).resolve()
    cands.extend(here.parents)
    cands.append(Path.cwd() / ".." / "thewarmchannelgtmbrain")
    cands.append(Path.cwd() / "thewarmchannelgtmbrain")
    for c in cands:
        try:
            if (c / "rules" / "evidence-ledger.md").is_file():
                return c.resolve()
        except OSError:
            continue
    return None


def load_brain_lists(brain, rep):
    global BANNED_WORDS, DECLARING, BANNED_CLAIMS, GUEST_BANNED
    if not brain:
        rep.add("WARN", "setup", "Brain not found. Using built-in rule lists, and numbers are not checked against the ledger. Pass --brain")
        return
    lint = brain / "scripts" / "lint_claims.py"
    if not lint.is_file():
        rep.add("WARN", "setup", f"{lint} not found. Using built-in rule lists")
        return
    try:
        spec = importlib.util.spec_from_file_location("twc_lint_claims", str(lint))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        BANNED_WORDS = list(mod.BANNED_WORDS)
        DECLARING = mod.DECLARING
        BANNED_CLAIMS = list(mod.BANNED_CLAIMS)
        GUEST_BANNED = list(mod.GUEST_BANNED)
        rep.add("INFO", "setup", f"Rule lists loaded from {lint}")
    except Exception as e:  # a broken brain script must not silently pass a deck
        rep.add("WARN", "setup", f"Could not load {lint} ({e}). Using built-in rule lists")


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------
NUM_TOKEN = re.compile(r"""
    (?P<money>(?:CA|US|C|A|NZ|AU)?[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:k|K|M|bn|million|billion|thousand)\b)?)
  | (?P<pct>(?<![\w.])\d[\d,]*(?:\.\d+)?\s?%)
  | (?P<mult>(?<![\w.])\d+(?:\.\d+)?x\b)
  | (?P<count>(?<![\w.$€£])\d{1,3}(?:,\d{3})+(?![\d%])|(?<![\w.,$€£])\d{3,}(?![\d,%x]))
""", re.X)
SCALE = {"k": 1e3, "K": 1e3, "thousand": 1e3, "M": 1e6, "million": 1e6, "bn": 1e9, "billion": 1e9}


def tokens(text):
    out = []
    for m in NUM_TOKEN.finditer(text or ""):
        kind = m.lastgroup
        raw = m.group(kind)
        if kind == "money":
            num = re.search(r"\d[\d,]*(?:\.\d+)?", raw).group(0).replace(",", "")
            sc = re.search(r"(k|K|M|bn|million|billion|thousand)\s*$", raw)
            val = float(num) * (SCALE[sc.group(1)] if sc else 1)
        elif kind == "pct":
            val = float(raw.replace("%", "").replace(",", "").strip())
        elif kind == "mult":
            val = float(raw[:-1])
        else:
            val = float(raw.replace(",", ""))
            if 1900 <= val <= 2099 and "," not in raw:
                continue  # a year
        out.append((kind, round(val, 6), raw.strip()))
    return out


def parse_ledger(path):
    rows, section = [], ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("|") or re.match(r"^\|\s*-", line) or re.match(r"^\|\s*#\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        grade = cells[-1].replace("*", "").strip()
        letter = re.search(r"\b([ABC])\b", grade)
        cleared = section.lower().startswith("cleared")
        rows.append({"id": cells[0], "figure": cells[1], "source": cells[2] if len(cells) >= 4 else "",
                     "grade": grade, "section": section,
                     "usable": bool(cleared and letter and letter.group(1) in "AB"),
                     "tokens": {(k, v) for k, v, _ in tokens(cells[1])}})
    return rows


def parse_register(path):
    """The prospect's evidence register: a markdown table whose header names ID and Kind."""
    rows, header = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*:?-", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        low = [c.lower() for c in cells]
        if "id" in low and "kind" in low:
            header = low
            continue
        if not header or not re.match(r"^E\d+$", cells[0]):
            continue
        row = dict(zip(header, cells))
        text = " ".join(cells[1:])
        rows.append({"id": cells[0], "kind": row.get("kind", "").upper().replace(" ", ""), "text": text,
                     "tokens": {(k, v) for k, v, _ in tokens(text)}})
    return rows


# ---------------------------------------------------------------------------
# HTML extraction
# ---------------------------------------------------------------------------
class Extract(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.segments = []          # (text, ctx) where ctx is a dict snapshot
        self.paras = []             # (slide, text) for <p> on slides
        self.imgs, self.svgs, self.urls, self.forms = [], [], [], []
        self.scripts, self.styles, self.inline_styles = [], [], []
        self.articles = []          # dicts per slide
        self.decks = []             # dicts per deck
        self.meta_robots = None
        self._buf_p = None
        self._in_script = self._in_style = False
        self._script_type = None

    def ctx(self):
        c = {"slide": None, "deck": None, "notes": False, "guest": False, "ref": False, "calc": False,
             "chrome": False, "home": False, "hidden_title": False}
        for tag, a in self.stack:
            cls = a.get("class", "")
            if tag == "section" and "deck" in cls.split():
                c["deck"] = a.get("data-deck")
            if tag == "article" and "slide" in cls.split():
                c["slide"] = a.get("id")
            if tag == "aside" and "notes" in cls.split():
                c["notes"] = True
            if a.get("data-audience") == "guest":
                c["guest"] = True
            if tag == "sup" and "ref" in cls.split():
                c["ref"] = True
            if "calc" in cls.split():
                c["calc"] = True
            if "chrome" in cls.split() or a.get("id") in ("toast", "help", "notesPanel", "srcPanel", "live"):
                c["chrome"] = True
            if a.get("id") == "home":
                c["home"] = True
        return c

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.meta_robots = a.get("content", "")
        for att in ("src", "href", "action", "data", "poster", "srcset", "formaction"):
            if att in a:
                self.urls.append((tag, att, a[att], a.get("rel", "")))
        if "style" in a:
            self.inline_styles.append(a["style"])
        if tag in ("iframe", "object", "embed", "form", "frame", "frameset", "portal"):
            self.forms.append(tag)
        if tag == "img":
            self.imgs.append(a)
        if tag == "svg":
            self.svgs.append(a)
        if tag == "script":
            self._in_script = True
            self._script_type = a.get("type", "")
            if a.get("src"):
                self.urls.append((tag, "src", a["src"], ""))
        if tag == "style":
            self._in_style = True
        if tag == "section" and "deck" in a.get("class", "").split():
            self.decks.append({"key": a.get("data-deck"), "name": a.get("data-name"), "slides": []})
        if tag == "article" and "slide" in a.get("class", "").split():
            art = {"id": a.get("id"), "title": a.get("data-title", ""), "aria": a.get("aria-label", ""),
                   "classes": a.get("class", "").split(), "close_links": 0, "notes_words": 0,
                   "notes_seconds": None, "has_notes": False, "deck": self.decks[-1]["key"] if self.decks else None}
            self.articles.append(art)
            if self.decks:
                self.decks[-1]["slides"].append(art)
        if tag == "aside" and "notes" in a.get("class", "").split() and self.articles:
            self.articles[-1]["has_notes"] = True
            try:
                self.articles[-1]["notes_seconds"] = int(a.get("data-seconds") or 0) or None
            except ValueError:
                pass
        if tag == "a" and self.articles and any("close-actions" in x.get("class", "").split() for _, x in self.stack):
            self.articles[-1]["close_links"] += 1
        if tag not in INLINE_JOIN:
            self.segments.append((" ", self.ctx()))
        if tag == "p" and self.ctx()["slide"] and not self.ctx()["notes"]:
            self._buf_p = []
        if tag not in VOID:
            self.stack.append((tag, a))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_script = False
        if tag == "style":
            self._in_style = False
        if tag == "p" and self._buf_p is not None:
            self.paras.append((self.ctx()["slide"], "".join(self._buf_p).strip()))
            self._buf_p = None
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag not in INLINE_JOIN:
            self.segments.append((" ", self.ctx()))

    def handle_data(self, data):
        if self._in_script:
            self.scripts.append((self._script_type, data))
            return
        if self._in_style:
            self.styles.append(data)
            return
        c = self.ctx()
        self.segments.append((data, c))
        if self._buf_p is not None and not c["ref"]:
            self._buf_p.append(data)
        if c["notes"] and self.articles:
            self.articles[-1]["notes_words"] += len(re.findall(r"[A-Za-z0-9'’]+", data))


def collect(ex):
    """Group visible text by container: each slide (screen and notes apart), home, guest blocks."""
    groups = {}
    for text, c in ex.segments:
        if c["chrome"]:
            key = ("chrome", None)
        elif c["slide"]:
            key = (c["slide"], "notes" if c["notes"] else ("guest" if c["guest"] else "screen"))
        elif c["home"]:
            key = ("home", "guest" if c["guest"] else "screen")
        else:
            key = ("other", None)
        g = groups.setdefault(key, {"text": [], "noref": []})
        g["text"].append(text)
        if not c["ref"] and not c["calc"]:
            g["noref"].append(text)
    for g in groups.values():
        g["text"] = re.sub(r"\s+", " ", "".join(g["text"])).strip()
        g["noref"] = re.sub(r"\s+", " ", "".join(g["noref"])).strip()
    return groups


def snippet(text, m, width=60):
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    return ("..." if a else "") + text[a:b] + ("..." if b < len(text) else "")


def label(key):
    slide, part = key
    if slide == "home":
        return "home" + (" (guest block)" if part == "guest" else "")
    if slide == "chrome":
        return "chrome"
    m = re.match(r"s-([a-z])-(\d+)", slide or "")
    where = f"deck {m.group(1).upper()} slide {m.group(2)}" if m else str(slide)
    return where + {"notes": " notes", "guest": " (guest block)", "screen": ""}.get(part, "")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def check_containment(ex, raw, rep):
    for tag, att, url, rel in ex.urls:
        u = url.strip()
        if not u or u.startswith(("#", "data:", "mailto:", "tel:")):
            if u.startswith("mailto:") and TRACKING_PARAMS.search(u):
                rep.add("ERROR", "links", f"tracking parameter in {u[:90]}")
            continue
        is_remote = bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//", u, re.I)) or u.lower().startswith("http")
        if tag == "a" and att == "href":
            if TRACKING_PARAMS.search(u):
                rep.add("ERROR", "links", f"tracking parameter in link {u[:90]}. No tracking, ever")
            continue
        if is_remote:
            rep.add("ERROR", "containment", f"<{tag} {att}> loads {u[:90]}. The file must make no network request")
        elif tag in ("img", "script", "link", "source", "video", "audio", "iframe"):
            rep.add("ERROR", "containment", f"<{tag} {att}> points at a separate file {u[:90]}. Embed it, the deck is one file")
    for t in ex.forms:
        rep.add("ERROR", "containment", f"<{t}> found. No forms, frames or embeds in a prospect deck")
    css = "\n".join(ex.styles + ex.inline_styles)
    for m in re.finditer(r"url\(\s*['\"]?(?!data:|#)([^)'\"]+)", css):
        rep.add("ERROR", "containment", f"CSS url() loads {m.group(1)[:90]}")
    if "@import" in css:
        rep.add("ERROR", "containment", "CSS @import found")
    for typ, code in ex.scripts:
        if typ == "application/json":
            continue
        m = NETWORK_JS.search(code)
        if m:
            rep.add("ERROR", "containment", f"script contains {m.group(0)!r}. The engine never talks to a network")
    if ex.meta_robots is None or "noindex" not in ex.meta_robots.lower():
        rep.add("WARN", "head", 'no <meta name="robots" content="noindex">. A private link must never be indexed')


def check_copy(groups, rep):
    for key, g in groups.items():
        if key[0] in ("other",):
            continue
        text = g["text"]
        where = label(key)
        for ch, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch in text:
                i = text.index(ch)
                rep.add("ERROR", where, f"{name}: ...{text[max(0, i - 50):i + 50]}...")
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if DECLARING.search(sentence):
                continue
            for w in BANNED_WORDS:
                m = re.search(r"\b" + re.escape(w), sentence, re.I)
                if m:
                    rep.add("ERROR", where, f"banned word '{m.group(0)}': {sentence[:140]}")
        for m in re.finditer(r"\{\{[^}]{0,80}\}\}", text):
            rep.add("ERROR", where, f"unfilled placeholder {m.group(0)}")
        for m in re.finditer(r"\[WRITE[^\]]*\]", text):
            rep.add("ERROR", where, f"unwritten scaffold marker {m.group(0)[:90]}")
        for m in re.finditer(r"\[E\d+\]", text):
            rep.add("ERROR", where, f"internal evidence ID {m.group(0)} shipped. Evidence IDs never reach the prospect")
        for m in re.finditer(r"\[(?:[A-Z][A-Za-z]*)(?: [A-Za-z]+){0,5}\]", text):
            rep.add("ERROR", where, f"unfilled template slot {m.group(0)}")
        for pat, why in BANNED_CLAIMS:
            m = re.search(pat, text, re.I)
            if m:
                rep.add("WARN", where, f"reads near a banned claim, {why}: {snippet(text, m)}")
        for pat, why, sev, flags in DECK_RULES:
            for m in re.finditer(pat, text, flags):
                ctx = snippet(text, m)
                if "case stud" in m.group(0).lower() and re.search(r"\bno case stud", ctx, re.I):
                    continue
                if m.group(0).lower().startswith("guarantee") and re.search(r"\bno guarantee", ctx, re.I):
                    rep.add("INFO", where, f"'no guarantee' line: {ctx}")
                    continue
                rep.add(sev, where, f"{why}: {ctx}")
        for pat, uk in US_SPELLINGS:
            m = re.search(pat, text)
            if m:
                rep.add("WARN", where, f"US spelling '{m.group(0)}', the brain writes {uk}. Keep it only inside a proper name")
        if key[1] == "guest":
            for pat in GUEST_BANNED:
                m = re.search(pat, text, re.I)
                if m:
                    rep.add("ERROR", where, f"client word in guest copy: '{m.group(0)}' in {snippet(text, m, 40)}")


# Capabilities whose status is not READY in rules/service-status.md. Wherever one is
# described as ours, its status must travel in the same sentence (the demo and
# description rule). Scope "ours" fires only on a sentence about us (we, our, us,
# The Warm Channel). Scope "any" fires on every sentence. Post-event lines pass
# when they carry the consent framing, because the client's own follow-through
# with guests who choose to continue is a recommendation, not our capability.
STATUS_TRIGGERS = [
    (r"\b(outreach|approach(es|ing)? (the )?(people|executives|guests|named)|invitations? (go|goes|are sent))\b",
     "outreach to named executives is BLOCKED on D5", "ours"),
    (r"\b(post-event|follow[- ]through|follow[- ]up|hand[- ]?over|hand(ed)? (over|off)|"
     r"continue[sd]? (the|a) conversation|after the evening, (your|the) (sellers|team))\b",
     "post-event conversion is BLOCKED on D11 and D5", "any"),
    (r"\b(composition report|confirmation report|attribution|report(ing)? (format|it|upward|back)|we report)\b",
     "measurement and reporting are IN BUILD", "ours"),
    (r"\b(demonstration (room|evening|event))\b", "the demonstration room is BLOCKED on D5", "ours"),
    (r"\b(founder[- ](led|delivered|hosted|facilitated)|the founder (attends|hosts|facilitates|runs|leads))\b",
     "founder attendance is open, D7", "any"),
    (r"\b(guest (network|universe)|returning guests|our cohort|our guests)\b",
     "a standing guest network is ROADMAP, never implied", "any"),
]
STATUS_MARKERS = re.compile(r"\b(in development|not yet|once|until|designed with you|not offered|being set up|blocked|"
                            r"opens|when (our|the)|after (our|we)|still|settled|agreed in writing|we have not|isn't|is not)\b", re.I)
CONSENT_MARKERS = re.compile(r"\b(choose|chose|chooses|choosing) to (continue|share)|\bconsent(ing|ed)?\b|\bwho want(s|ed)? (it|to)\b", re.I)
OURS = re.compile(r"\b(we|we'll|we're|we've|our|ours|us|The Warm Channel)\b", re.I)


def check_status(groups, rep):
    for key, g in groups.items():
        if key[0] in ("chrome", "other"):
            continue
        for sent in re.split(r"(?<=[.!?])\s+", g["text"]):
            for pat, why, scope in STATUS_TRIGGERS:
                m = re.search(pat, sent, re.I)
                if not m or STATUS_MARKERS.search(sent):
                    continue
                if scope == "ours" and not OURS.search(sent):
                    continue
                if "post-event" in why and CONSENT_MARKERS.search(sent):
                    continue
                rep.add("WARN", label(key), f"mentions '{m.group(0)}' with no status in the sentence: {why}. "
                                            f"Status travels in the same sentence: {sent[:120]}")


def check_collision(groups, rep):
    """Do-not-say, speech: whenever the 70% attendance benchmark is used, never mention a reply rate in the
    same conversation. A deck is one conversation, so the rule holds across the whole file, notes included."""
    has70 = [label(k) for k, g in groups.items() if re.search(r"\b70\s*%|\bseventy percent", g["text"], re.I)]
    reply = [label(k) for k, g in groups.items() if re.search(r"\breply rates?\b|\bresponse rates?\b", g["text"], re.I)]
    if has70 and reply:
        rep.add("ERROR", "file", f"the 70% attendance benchmark ({', '.join(has70[:3])}) and a reply rate "
                                 f"({', '.join(reply[:3])}) in one file. A deck is one conversation: drop the reply rate. "
                                 "Do-not-say speech rule and ledger rule 3")


STOP = set("""that this with from have your their which about into than more less same dataset percent figure
figures also only were when what where them they there these those will would could should being been other each
every over under after before between across against most many much such some just like then here near""".split())


def keywords(text):
    return {w[:-1] if w.endswith("s") and len(w) > 4 else w
            for w in re.findall(r"[a-z][a-z\-]{3,}", (text or "").lower())} - STOP


def check_numbers(groups, ledger, register, declared, rep):
    """Every percentage and money figure needs a source, and the sentence it sits in must
    share words with that source. A value that matches an unrelated row is not traced."""
    seen = {}
    for key, g in groups.items():
        if key[0] in ("chrome", "other"):
            continue
        for sent in re.split(r"(?<=[.!?])\s+", g["noref"]):
            for kind, val, raw in tokens(sent):
                seen.setdefault((kind, val, raw), []).append((label(key), sent))
    if not seen:
        rep.add("INFO", "numbers", "no percentage, money figure, multiplier or count of 100 or more on any surface")
        return
    for (kind, val, raw), occ in sorted(seen.items(), key=lambda x: (x[0][0], x[0][1])):
        wheres = sorted({w for w, _ in occ})
        where = ", ".join(wheres[:4]) + (" and more" if len(wheres) > 4 else "")
        hits = [r for r in ledger if (kind, val) in r["tokens"]]
        usable = [r for r in hits if r["usable"]]
        reg = [r for r in register if (kind, val) in r["tokens"]]
        reg_ok = [r for r in reg if r["kind"] in ("P1", "P2", "M-A", "M-B", "MA", "MB")]
        dec = declared.get((kind, val))
        if dec:
            rep.add("INFO", "numbers", f"{raw} declared in deck.json number_provenance: {dec}. Seen in {where}")
            continue
        if usable or reg_ok:
            src_words = [keywords(r["figure"] + " " + r["source"]) for r in usable] + [keywords(r["text"]) for r in reg_ok]
            loose = [(w, snt) for w, snt in occ if not any(keywords(snt) & sw for sw in src_words)]
            ids = ", ".join([f"ledger #{r['id']} ({r['grade']})" for r in usable] + [f"register {r['id']} {r['kind']}" for r in reg_ok])
            if loose:
                w0, s0 = loose[0]
                rep.add("ERROR" if kind in ("pct", "money") else "WARN", "numbers",
                        f"{raw} matches {ids} by value only. In {w0} the sentence shares no words with that source, so it is "
                        f"probably a different claim: '{s0[:110]}'. Trace it or cut it")
            else:
                rep.add("INFO", "numbers", f"{raw} traces to {ids}. Seen in {where}")
            continue
        if hits:
            ids = ", ".join(f"#{r['id']} {r['grade']} ({r['section']})" for r in hits)
            rep.add("ERROR", "numbers", f"{raw} matches only ledger rows not cleared for a deck: {ids}. Seen in {where}. "
                                        "Grade C never enters a deck. Use the grade B figure or cut it")
            continue
        if reg:
            ids = ", ".join(f"{r['id']} {r['kind']}" for r in reg)
            rep.add("ERROR" if kind in ("pct", "money") else "WARN", "numbers",
                    f"{raw} matches register rows {ids}, which are not cleared for the deck (P3 is an inference, "
                    f"NEW and M-C are not usable). Seen in {where}")
            continue
        sev = "ERROR" if kind in ("pct", "money") else "WARN"
        rep.add(sev, "numbers", f"{raw} has no source: not in the ledger, the register or number_provenance. "
                                f"Seen in {where}. A figure without a source does not exist. Write {{TBD}} or cite it")


def check_structure(ex, audience, rep):
    if not ex.decks:
        rep.add("ERROR", "structure", "no decks found. Is this a built deck file?")
    for d in ex.decks:
        sl = d["slides"]
        tag = f"deck {str(d['key']).upper()}"
        if not sl:
            rep.add("ERROR", tag, "deck has no slides")
            continue
        if "layout-cover" not in sl[0]["classes"]:
            rep.add("ERROR", tag, "slide 1 is not a cover")
        if sl[-1]["close_links"] != 2:
            rep.add("ERROR", tag, f"last slide has {sl[-1]['close_links']} actions. It needs exactly two: back to the overview, and onward")
        if len(sl) > 9:
            rep.add("WARN", tag, f"{len(sl)} slides. Over nine usually means two decks")
        for i, a in enumerate(sl, 1):
            if not a["title"].strip():
                rep.add("ERROR", f"{tag} slide {i}", "no title")
            elif len(a["title"].split()) < 4 and "layout-close" not in a["classes"]:
                rep.add("WARN", f"{tag} slide {i}", f"title '{a['title']}' reads as a label. Headlines are claims")
            if audience == "send" and a["has_notes"]:
                rep.add("ERROR", f"{tag} slide {i}", "presenter notes in the send build. Rebuild with --audience send")
            if audience == "present":
                if not a["has_notes"]:
                    rep.add("WARN", f"{tag} slide {i}", "no presenter notes")
                elif a["notes_seconds"]:
                    target = a["notes_seconds"] * WORDS_PER_SECOND
                    if abs(a["notes_words"] - target) > max(12, 0.35 * target):
                        rep.add("WARN", f"{tag} slide {i}", f"notes are {a['notes_words']} words for {a['notes_seconds']}s. "
                                                            f"About {int(target)} words is sayable at speed")
    for img in ex.imgs:
        if img.get("aria-hidden") == "true":
            continue
        if not img.get("alt", "").strip():
            rep.add("ERROR", "accessibility", "an image has no alt text")
    for s in ex.svgs:
        if s.get("role") == "img" and not s.get("aria-label", "").strip():
            rep.add("ERROR", "accessibility", "a chart (svg role=img) has no accessible name")
    for slide, p in ex.paras:
        n = len([x for x in re.split(r"(?<=[.!?])\s+", p) if x.strip()])
        if n > 2:
            rep.add("WARN", label((slide, "screen")), f"an on-screen paragraph runs {n} sentences. Two at most: {p[:100]}")


def check_spec(deck, rep):
    """Checks that need deck.json: notes against screen copy, design fields, motif usage."""
    fields = ("stage", "hero", "entry", "ambient", "interaction", "restraint", "reduced")
    centre, still, motif_uses = 0, 0, 0
    for d in deck.get("decks", []):
        for i, sl in enumerate(d.get("slides", []), 1):
            where = f"deck {d['key'].upper()} slide {i}"
            if sl.get("centrepiece"):
                centre += 1
                miss = [f for f in fields if not (sl.get("design") or {}).get(f)]
                if miss:
                    rep.add("WARN", where, f"centrepiece without design fields: {', '.join(miss)}")
            if sl.get("still"):
                still += 1
            if sl.get("layout") == "motif" or (sl.get("layout") == "cover" and sl.get("motif")):
                motif_uses += 1
            notes = sl.get("notes") or ""
            if not notes.strip():
                rep.add("WARN", where, "no presenter notes in deck.json. Every slide gets Say it notes before the walkthrough")
            if notes and sl.get("seconds"):
                words = len(re.findall(r"[A-Za-z0-9'’]+", notes))
                target = int(sl["seconds"]) * WORDS_PER_SECOND
                if abs(words - target) > max(12, 0.35 * target):
                    rep.add("WARN", where, f"notes are {words} words for {sl['seconds']}s, aim for about {int(target)}")
            screen = json.dumps({k: v for k, v in sl.items() if k not in ("notes", "design", "seconds")}, ensure_ascii=False)
            for sent in re.split(r"(?<=[.!?])\s+", notes):
                s = sent.strip().rstrip(".!?")
                if len(s.split()) >= 5 and s.lower() in screen.lower():
                    rep.add("WARN", where, f"notes repeat on-screen copy: '{s[:90]}'. Screen and notes share no sentence")
    if not 4 <= centre <= 6:
        rep.add("WARN", "spec", f"{centre} centrepieces. The method asks for four to six")
    if still < 1:
        rep.add("WARN", "spec", "no slide marked still. Put one immediately before the biggest moment")
    if not 3 <= motif_uses <= 6:
        rep.add("WARN", "spec", f"the motif appears {motif_uses} times. Three to six, in different states")
    bys = deck.get("before_you_send") or {}
    for k in ("verified", "needs_settling", "designed_not_supplied"):
        if not bys.get(k):
            rep.add("WARN", "spec", f"before_you_send.{k} is empty. Name things individually, never soften it")


def check_design_doc(path, brand, rep):
    text = path.read_text(encoding="utf-8")
    for n, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", line):
            rep.add("ERROR", f"{path.name}:{n}", f"hex value {m.group(0)}. Colour appears only as a semantic role")
        if re.search(r"\b(rgb|rgba|hsl|hsla|oklch|oklab)\(", line, re.I):
            rep.add("ERROR", f"{path.name}:{n}", "a colour function. Colour appears only as a semantic role")
        if re.search(r"font-size|font-family|\b\d+\s?pt\b", line, re.I):
            rep.add("WARN", f"{path.name}:{n}", "an absolute type size or a font property. Size is relative hierarchy only")
    names = list(TYPEFACE_NAMES)
    for slot in ((brand or {}).get("fonts") or {}).values():
        for k in ("family", "substitute_for"):
            v = (slot or {}).get(k)
            if v and k == "family":
                names.append(v)
    for nm in sorted(set(names), key=len, reverse=True):
        pat = r"(?<![\w-])" + re.escape(nm) + r"(?![\w-])"
        flags = 0 if nm[0].isupper() else re.I
        for n, line in enumerate(text.splitlines(), 1):
            if re.search(pat, line, flags):
                rep.add("ERROR", f"{path.name}:{n}", f"typeface name '{nm}'. The design concepts file names no typeface")


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", help="the built deck file")
    ap.add_argument("--deck", help="deck.json, for spec checks and number_provenance")
    ap.add_argument("--brand", help="brand.json, so the design doc check knows the brand's font names")
    ap.add_argument("--design", help="the design concepts markdown file, checked for hex values and typeface names")
    ap.add_argument("--register", help="the prospect's evidence-register.md")
    ap.add_argument("--brain", help="path to the brain repository")
    ap.add_argument("--strict", action="store_true", help="fail on warnings too")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--quiet", action="store_true", help="hide INFO lines")
    a = ap.parse_args()

    rep = Report()
    hp = Path(a.html)
    if not hp.is_file():
        print(f"not found: {hp}", file=sys.stderr)
        return 2
    raw = hp.read_text(encoding="utf-8")
    brain = find_brain(a.brain)
    load_brain_lists(brain, rep)
    m = re.search(r"Audience: (send|present)\.", raw)
    audience = m.group(1) if m else "unknown"
    if audience == "present":
        rep.add("WARN", "build", "this is the PRESENT build, with presenter notes. Never send it. Send the send build")
    elif audience == "unknown":
        rep.add("WARN", "build", "no build comment found. Was this file built by build_deck.py?")
    size = hp.stat().st_size
    if size > 15 * 1024 * 1024:
        rep.add("ERROR", "size", f"{size / 1048576:.1f} MB. Too large to host or open comfortably. Subset fonts, compress images")
    elif size > 5 * 1024 * 1024:
        rep.add("WARN", "size", f"{size / 1048576:.1f} MB. Check embedded fonts and images")
    else:
        rep.add("INFO", "size", f"{size / 1024:.0f} KB")

    ex = Extract()
    ex.feed(raw)
    ex.close()
    groups = collect(ex)

    check_containment(ex, raw, rep)
    check_copy(groups, rep)
    check_collision(groups, rep)
    check_status(groups, rep)
    ledger = parse_ledger(brain / "rules" / "evidence-ledger.md") if brain else []
    register = parse_register(Path(a.register)) if a.register else []
    if a.register and not register:
        rep.add("WARN", "numbers", f"no evidence rows parsed from {a.register}. Header must name ID and Kind")
    deck = None
    declared = {}
    if a.deck:
        deck = json.loads(Path(a.deck).read_text(encoding="utf-8"))
        for k, basis in (deck.get("number_provenance") or {}).items():
            for kind, val, _ in tokens(k):
                declared[(kind, val)] = basis
    check_numbers(groups, ledger, register, declared, rep)
    check_structure(ex, audience, rep)
    if deck:
        check_spec(deck, rep)
    if a.design:
        brand = json.loads(Path(a.brand).read_text(encoding="utf-8")) if a.brand else None
        check_design_doc(Path(a.design), brand, rep)

    tbd = sum(g["text"].count("{TBD}") for k, g in groups.items() if k[1] != "notes")
    if tbd:
        rep.add("INFO", "unknowns", f"{tbd} {{TBD}} marks on screen. Each must be a number only the prospect can supply")

    if a.json:
        print(json.dumps({"file": str(hp), "audience": audience, "brain": str(brain) if brain else None,
                          "errors": rep.count("ERROR"), "warnings": rep.count("WARN"), "items": rep.items}, indent=2))
    else:
        print(f"deck_check {hp.name}  audience={audience}  brain={'found' if brain else 'NOT FOUND'}")
        for sev in ("ERROR", "WARN", "INFO"):
            if a.quiet and sev == "INFO":
                continue
            for it in rep.items:
                if it["severity"] == sev:
                    print(f"  {sev:5} [{it['where']}] {it['message']}")
        print(f"\n{rep.count('ERROR')} error(s), {rep.count('WARN')} warning(s).", end=" ")
        if rep.count("ERROR"):
            print("Do not send.")
        elif rep.count("WARN"):
            print("A person reads every warning before this is sent.")
        else:
            print("Clean. The QA checklist still applies: no script can tell you whether a claim is true.")
    if rep.count("ERROR") or (a.strict and rep.count("WARN")):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
