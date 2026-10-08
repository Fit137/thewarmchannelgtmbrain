#!/usr/bin/env python3
"""Fetch an OFL font family as WOFF2 files, with its licence, for embedding in a deck.

    python3 fetch_font.py "Public Sans" --weights 400,600 --out deck/fonts
    python3 fetch_font.py "Source Serif 4" --weights 400,600 --subset latin --out deck/fonts

Files come from the Fontsource packages on the jsDelivr CDN, which republish the Google
Fonts library under each family's own licence. The licence file is saved beside the
fonts as <family>-LICENSE.txt, and the script prints the "files" block to paste into
brand.json.

Only families published under the SIL Open Font Licence may be embedded in a file that
is sent to someone. The script refuses a family that is not on its OFL list unless you
pass --licence-checked after reading the family's licence yourself. A brand's own
proprietary face is never fetched, embedded or redistributed: pick a substitute.

--base-url points at a mirror with the same layout, for offline use or testing.
No third-party dependencies. Python 3.8 or later.
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    from brand_extract import OFL  # the same list the extractor uses
except Exception:  # pragma: no cover
    OFL = set()

DEFAULT_BASE = "https://cdn.jsdelivr.net/npm/@fontsource"


def family_id(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "fetch_font/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("family")
    ap.add_argument("--weights", default="400,600")
    ap.add_argument("--styles", default="normal", help="normal, italic, or normal,italic")
    ap.add_argument("--subset", default="latin")
    ap.add_argument("--version", default="5", help="Fontsource major version")
    ap.add_argument("--out", required=True)
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--licence-checked", action="store_true",
                    help="you have read the family's licence and it permits embedding")
    a = ap.parse_args()
    if a.family.lower() not in OFL and not a.licence_checked:
        print(f"{a.family!r} is not on the OFL list. Read its licence, then pass --licence-checked, "
              "or choose an OFL substitute. A brand's own face is never embedded.", file=sys.stderr)
        return 2
    fid = family_id(a.family)
    root = f"{a.base_url.rstrip('/')}/{fid}@{a.version}"
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for weight in [w.strip() for w in a.weights.split(",") if w.strip()]:
        for style in [s.strip() for s in a.styles.split(",") if s.strip()]:
            name = f"{fid}-{a.subset}-{weight}-{style}.woff2"
            try:
                data = get(f"{root}/files/{name}")
            except Exception as e:
                print(f"  could not fetch {name}: {e}", file=sys.stderr)
                return 1
            if data[:4] != b"wOF2":
                print(f"  {name} is not a WOFF2 file. Refusing to save it.", file=sys.stderr)
                return 1
            (out / name).write_bytes(data)
            files.append({"path": f"{out.name}/{name}", "weight": int(weight), "style": style})
            print(f"  saved {out / name} ({len(data) / 1024:.0f} KB)")
    lic_name = f"{fid}-LICENSE.txt"
    for candidate in ("LICENSE", "LICENSE.txt", "OFL.txt"):
        try:
            text = get(f"{root}/{candidate}")
            (out / lic_name).write_bytes(text)
            print(f"  saved {out / lic_name}")
            break
        except Exception:
            continue
    else:
        print("  licence file not found on the mirror. Save the OFL text beside the fonts by hand before sending.",
              file=sys.stderr)
    print("\nPaste into brand.json, under fonts.display or fonts.text, with paths relative to brand.json:")
    print(json.dumps({"family": a.family, "licence": f"OFL 1.1, see {out.name}/{lic_name}", "files": files}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
