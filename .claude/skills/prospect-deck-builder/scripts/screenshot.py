#!/usr/bin/env python3
"""Screenshot every slide of a built deck with headless Chrome, for review before sending.

    python3 screenshot.py build/acme_strategy_v1_send.html --out build/shots
    python3 screenshot.py build/acme_strategy_v1_send.html --out build/shots --only c/5 --motion
    python3 screenshot.py build/acme_strategy_v1_send.html --pdf build/acme_strategy_v1.pdf

Each slide is opened at its own deep link (#/c/5) in a fresh headless Chrome at the
1600 x 900 design size. By default the deck is opened with ?still, which ships the
resolved end state of every animation, so the picture is what the slide finally says.
--motion captures mid-flight instead, after --wait milliseconds of virtual time.

Outputs, in --out:
  a-01.png ... f-05.png   one per slide
  home.png                the home layer, at --home-width by --home-height
  sheet.png               a contact sheet, when Pillow is installed
  index.html              a local gallery of the shots, always

--pdf prints the leave-behind PDF through Chrome's own print path, one slide per
1600 x 900 page after the home layer. Open the PDF and check the page count.

Chrome is found from --chrome, then $CHROME, then the usual names on PATH, then the
usual install paths on macOS, Windows and Linux, then Playwright's browser cache.
No third-party dependencies. Pillow is optional, for the contact sheet.
"""
import argparse
import concurrent.futures as cf
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]
INSTALL_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome(arg):
    if arg:
        return arg
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for name in CANDIDATES:
        p = shutil.which(name)
        if p:
            return p
    for p in INSTALL_PATHS:
        if os.path.exists(p):
            return p
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), os.path.expanduser("~/.cache/ms-playwright"),
             os.path.expanduser("~/Library/Caches/ms-playwright"), "/opt/pw-browsers"]
    for root in roots:
        if not root:
            continue
        hits = sorted(glob.glob(os.path.join(root, "chromium-*", "chrome-linux", "chrome")) +
                      glob.glob(os.path.join(root, "chromium-*", "chrome-mac", "Chromium.app", "Contents", "MacOS", "Chromium")) +
                      glob.glob(os.path.join(root, "chromium-*", "chrome-win", "chrome.exe")))
        if hits:
            return hits[-1]
    return None


def chrome_cmd(chrome, extra, url, width, height, wait):
    cmd = [chrome, "--headless=new", "--hide-scrollbars", "--mute-audio", "--disable-gpu",
           "--no-first-run", "--no-default-browser-check", "--disable-extensions",
           "--force-device-scale-factor=1", f"--window-size={width},{height}",
           f"--virtual-time-budget={wait}", "--run-all-compositor-stages-before-draw"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        cmd.append("--no-sandbox")
    return cmd + extra + [url]


def run(cmd, timeout=90):
    prof = tempfile.mkdtemp(prefix="deckshot-")
    try:
        r = subprocess.run(cmd[:1] + [f"--user-data-dir={prof}"] + cmd[1:], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout)
        return r.returncode, r.stderr.decode("utf-8", "replace")[-400:]
    except subprocess.TimeoutExpired:
        return 124, "timed out"
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def deck_data(path):
    raw = Path(path).read_text(encoding="utf-8")
    m = re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)
    if not m:
        raise SystemExit("no deck-data block found. Is this a file built by build_deck.py?")
    return json.loads(m.group(1).replace("<\\/", "</"))


def contact_sheet(files, out, cols=6, thumb=(400, 225)):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False
    rows = (len(files) + cols - 1) // cols
    pad, lab = 10, 22
    sheet = Image.new("RGB", (cols * (thumb[0] + pad) + pad, rows * (thumb[1] + pad + lab) + pad), (120, 120, 120))
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        im.thumbnail(thumb)
        x = pad + (i % cols) * (thumb[0] + pad)
        y = pad + (i // cols) * (thumb[1] + pad + lab)
        sheet.paste(im, (x, y + lab))
        draw.text((x, y + 4), Path(f).stem, fill=(255, 255, 255))
    sheet.save(out)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out", default=None, help="folder for the screenshots")
    ap.add_argument("--chrome")
    ap.add_argument("--only", action="append", help="one slide as deck/n, for example c/5. Repeatable")
    ap.add_argument("--motion", action="store_true", help="capture with motion on, instead of the resolved still state")
    ap.add_argument("--wait", type=int, default=2500, help="virtual milliseconds to let a slide settle")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--home-width", type=int, default=1280)
    ap.add_argument("--home-height", type=int, default=5200)
    ap.add_argument("--no-home", action="store_true")
    ap.add_argument("--pdf", help="also print the leave-behind PDF to this path")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    chrome = find_chrome(a.chrome)
    if not chrome:
        print("Chrome or Chromium not found. Pass --chrome /path/to/chrome or set CHROME.", file=sys.stderr)
        return 2
    src = Path(a.html).resolve()
    data = deck_data(src)
    base = src.as_uri() + ("" if a.motion else "?still")
    jobs = []
    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        wanted = None
        if a.only:
            wanted = {tuple(x.split("/")) for x in a.only}
        for d in data["decks"]:
            for n in range(1, int(d["slides"]) + 1):
                if wanted and (d["key"], str(n)) not in wanted:
                    continue
                png = out / f"{d['key']}-{n:02d}.png"
                jobs.append((png, chrome_cmd(chrome, [f"--screenshot={png}"], f"{base}#/{d['key']}/{n}",
                                             a.width, a.height, a.wait)))
        if not a.no_home and not a.only:
            png = out / "home.png"
            jobs.append((png, chrome_cmd(chrome, [f"--screenshot={png}"], base + "#/", a.home_width, a.home_height, 800)))
    failures = []
    with cf.ThreadPoolExecutor(max_workers=max(1, a.workers)) as ex:
        futs = {ex.submit(run, cmd): png for png, cmd in jobs}
        for f in cf.as_completed(futs):
            png = futs[f]
            code, err = f.result()
            if code != 0 or not png.exists():
                failures.append((png.name, code, err.strip().splitlines()[-1:] if err else ""))
    shots = sorted(p for p, _ in jobs if p.exists() and p.name != "home.png")
    if a.out:
        out = Path(a.out)
        cards = "".join(f'<figure><a href="{html.escape(p.name)}"><img src="{html.escape(p.name)}" loading="lazy" '
                        f'alt="{html.escape(p.stem)}"></a><figcaption>{html.escape(p.stem)}</figcaption></figure>' for p in shots)
        (out / "index.html").write_text(
            "<!doctype html><meta charset=utf-8><title>Slide review</title><style>body{font:14px system-ui;margin:16px;"
            "background:#444;color:#eee}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}"
            "img{width:100%;display:block;background:#fff}figure{margin:0}</style><main>" + cards + "</main>", encoding="utf-8")
        if shots and contact_sheet(shots, out / "sheet.png"):
            print(f"Contact sheet: {out / 'sheet.png'}")
        print(f"{len(shots)} slide screenshot(s) in {out}. Gallery: {out / 'index.html'}")
    if a.pdf:
        pdf = Path(a.pdf).resolve()
        pdf.parent.mkdir(parents=True, exist_ok=True)
        cmd = chrome_cmd(chrome, [f"--print-to-pdf={pdf}", "--no-pdf-header-footer", "--print-to-pdf-no-header"],
                         src.as_uri() + "#/", a.width, a.height, 1500)
        code, err = run(cmd, timeout=180)
        if code != 0 or not pdf.exists():
            failures.append((pdf.name, code, err))
        else:
            print(f"PDF: {pdf} ({pdf.stat().st_size / 1024:.0f} KB). Check the page count: home pages, then one page per slide.")
    for name, code, err in failures:
        print(f"  FAILED {name} (exit {code}) {err}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
