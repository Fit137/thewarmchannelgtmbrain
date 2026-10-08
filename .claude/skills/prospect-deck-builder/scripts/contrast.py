#!/usr/bin/env python3
"""Check a brand kit's colour roles for legible contrast, and propose the smallest fix.

    python3 contrast.py brand.json
    python3 contrast.py brand.json --fix brand.fixed.json

Every pair below is a real use in the deck shell. Text pairs need 4.5 to 1 (WCAG AA
for normal text, and the deck's small captions and kickers are normal text). Non-text
pairs need 3 to 1. A projector washes contrast out, so a pair that only just passes on
a laptop is reported as TIGHT.

A failing role is fixed by moving its lightness, keeping its hue and saturation, until
the pair passes. For button text the fix tries the kit's own surface and ink first.
--fix writes a copy of the kit with the adjusted roles and a line in "sources" for each
change, so the brand kit file says what was altered and why. The prospect's logo is
never recoloured: these roles only colour the deck around it.

No third-party dependencies. Exit status 1 when any pair fails, 2 on bad usage.
"""
import argparse
import colorsys
import json
import sys
from pathlib import Path

TEXT, NONTEXT = 4.5, 3.0
TIGHT_MARGIN = 0.6   # within this of the minimum reads as TIGHT on a projector

# (foreground role, background role, minimum, where the pair appears in the shell)
PAIRS = [
    ("ink", "surface", TEXT, "titles, headings, strong text"),
    ("body", "surface", TEXT, "body copy, table cells"),
    ("muted", "surface", TEXT, "kickers, captions, notes, footers"),
    ("accent", "surface", TEXT, "links, chapter letters, source references, hero figures"),
    ("accent_ink", "surface", TEXT, "link and button hover"),
    ("caution", "surface", TEXT, "{TBD} marks and step status tags"),
    ("flag", "surface", TEXT, "the calculator result when it does not pay back"),
    ("on_accent", "accent", TEXT, "button text"),
    ("on_accent", "accent_ink", TEXT, "button text on hover"),
    ("ink", "surface_2", TEXT, "headings in the next-step block and highlighted cells"),
    ("body", "surface_2", TEXT, "the invitation card, highlighted table rows and columns"),
    ("muted", "surface_2", TEXT, "captions inside highlighted blocks"),
    ("caution", "surface_2", TEXT, "{TBD} inside a highlighted row"),
    ("accent", "surface_2", TEXT, "links and accent text inside highlighted blocks"),
    ("positive", "surface", NONTEXT, "reserved for positive marks and large figures"),
]
INFO_PAIRS = [("rule", "surface", 1.3, "hairlines and table rules, decorative")]


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: #{h}")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in rgb)


def luminance(h):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def nudge(fg, bg, target):
    """Move fg's lightness away from bg until the pair reaches target. None if impossible."""
    r, g, b = hex_to_rgb(fg)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    darker = luminance(bg) > 0.18
    for step in range(0, 101):
        nl = l - step / 100.0 if darker else l + step / 100.0
        if not 0.0 <= nl <= 1.0:
            break
        cand = rgb_to_hex(colorsys.hls_to_rgb(h, nl, s))
        if ratio(cand, bg) >= target:
            return cand
    return None


def evaluate(roles):
    rows = []
    for fg, bg, need, use in PAIRS:
        if fg not in roles or bg not in roles:
            rows.append({"fg": fg, "bg": bg, "need": need, "use": use, "ratio": None, "status": "MISSING"})
            continue
        r = ratio(roles[fg], roles[bg])
        status = "FAIL" if r < need else ("TIGHT" if r < need + TIGHT_MARGIN else "PASS")
        rows.append({"fg": fg, "bg": bg, "need": need, "use": use, "ratio": round(r, 2), "status": status})
    for fg, bg, need, use in INFO_PAIRS:
        if fg in roles and bg in roles:
            r = ratio(roles[fg], roles[bg])
            rows.append({"fg": fg, "bg": bg, "need": need, "use": use, "ratio": round(r, 2),
                         "status": "INFO" if r >= need else "FAINT"})
    return rows


def propose(roles):
    """Return {role: new_hex} for the smallest set of changes that makes every pair pass."""
    fixed = dict(roles)
    changes = {}
    for _ in range(3):  # a change can affect a later pair, so settle in a few passes
        moved = False
        for fg, bg, need, _use in PAIRS:
            if fg not in fixed or bg not in fixed or ratio(fixed[fg], fixed[bg]) >= need:
                continue
            if fg == "on_accent":
                for cand in (fixed.get("surface"), fixed.get("ink"), "#FFFFFF", "#000000"):
                    if cand and ratio(cand, fixed[bg]) >= need and (bg != "accent" or ratio(cand, fixed.get("accent_ink", cand)) >= need):
                        fixed[fg] = cand
                        changes[fg] = cand
                        moved = True
                        break
                else:
                    new = nudge(fixed[bg], fixed[fg], need)
                    if new:
                        fixed[bg] = changes[bg] = new
                        moved = True
                continue
            new = nudge(fixed[fg], fixed[bg], need)
            if new and new != fixed[fg]:
                fixed[fg] = changes[fg] = new
                moved = True
        if not moved:
            break
    return changes, fixed


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brand")
    ap.add_argument("--fix", help="write a copy of the brand kit with the proposed roles")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        brand = json.loads(Path(a.brand).read_text(encoding="utf-8"))
        roles = {k: v for k, v in (brand.get("roles") or {}).items()}
        for k, v in roles.items():
            hex_to_rgb(v)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"cannot read the brand kit: {e}", file=sys.stderr)
        return 2
    if brand.get("skin") == "neutral" and not roles:
        print("skin is neutral, the shell's neutral roles are used and already pass.")
        return 0
    rows = evaluate(roles)
    changes, fixed = propose(roles)
    if a.json:
        print(json.dumps({"pairs": rows, "proposed": changes}, indent=2))
    else:
        print(f"Contrast for {brand.get('company', a.brand)}\n")
        print(f"  {'pair':32} {'ratio':>6}  {'need':>4}  status  where")
        for r in rows:
            pair = f"{r['fg']} on {r['bg']}"
            rt = f"{r['ratio']:.2f}" if r["ratio"] is not None else "  -"
            print(f"  {pair:32} {rt:>6}  {r['need']:>4}  {r['status']:6}  {r['use']}")
        if changes:
            print("\nProposed, hue and saturation kept, lightness moved:")
            for role, new in changes.items():
                print(f"  {role:12} {roles.get(role, '?')} -> {new}")
            print("\nThe logo keeps its own colours. Only the deck's roles change.")
    if a.fix:
        out = dict(brand)
        out["roles"] = fixed
        srcs = list(out.get("sources") or [])
        for role, new in changes.items():
            srcs.append({"element": f"role {role}",
                         "from": f"Adjusted for contrast by contrast.py, {roles.get(role)} to {new}", "url": None})
        out["sources"] = srcs
        Path(a.fix).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nWrote {a.fix}")
    failed = any(r["status"] in ("FAIL", "MISSING") for r in rows)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
