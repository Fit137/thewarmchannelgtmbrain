#!/usr/bin/env python3
"""Quality gate for a built show-week brief. Run it on the file you will send.

    python3 brief_check.py build/acme_cloudsec_brief.html --brief brief/brief.json \
        --register evidence/evidence-register.md --pdf build/acme_cloudsec_brief.pdf

The same checks as the deck builder's deck_check.py, from the same code, applied to one
page: nothing loads from the network, no tracking parameter, a noindex tag; no dash,
banned word, placeholder, evidence ID or scaffold marker; no retired scope name, network,
proof or price claim, no frozen D11 line; no reply rate beside the 70% benchmark;
capabilities that are not READY carry their status; every percentage, money figure and
count of 100 or more traces to the cleared ledger, a P0, P1 or P2 register row, or
declared provenance, with the sentence sharing words with its source.

Then the brief's own shape: one call to action, one headline, every source reference
present in the sources list, alt text on the mark, no presenter notes, and, with --pdf,
two printed pages at most.

Exit status 1 on any ERROR, or on any WARN with --strict.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import _family  # noqa: F401
import deck_check as dc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--brief", help="brief.json, for number_provenance")
    ap.add_argument("--register", help="the prospect's evidence-register.md")
    ap.add_argument("--pdf", help="the printed PDF, to check its page count")
    ap.add_argument("--brain")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    rep = dc.Report()
    hp = Path(a.html)
    raw = hp.read_text(encoding="utf-8")
    brain = dc.find_brain(a.brain)
    dc.load_brain_lists(brain, rep)
    if "Show-week brief. Built" not in raw:
        rep.add("WARN", "build", "no build comment found. Was this file built by build_brief.py?")
    size = hp.stat().st_size
    rep.add("WARN" if size > 3 * 1024 * 1024 else "INFO", "size", f"{size / 1024:.0f} KB")

    ex = dc.Extract()
    ex.feed(raw)
    ex.close()
    groups = dc.collect(ex)
    if ("home", "screen") not in groups:
        rep.add("ERROR", "structure", "no page body found inside id=home. Is this a built brief?")
    dc.check_containment(ex, raw, rep)
    dc.check_copy(groups, rep)
    dc.check_collision(groups, rep)
    dc.check_status(groups, rep)
    ledger = dc.parse_ledger(brain / "rules" / "evidence-ledger.md") if brain else []
    register = dc.parse_register(Path(a.register)) if a.register else []
    declared = {}
    if a.brief:
        b = json.loads(Path(a.brief).read_text(encoding="utf-8"))
        for k, basis in (b.get("number_provenance") or {}).items():
            for kind, val, _ in dc.tokens(k):
                declared[(kind, val)] = basis
    dc.check_numbers(groups, ledger, register, declared, rep)

    btns = re.findall(r'<a class="btn"', raw)
    if len(btns) != 1:
        rep.add("ERROR", "structure", f"{len(btns)} calls to action. A brief carries exactly one")
    if len(re.findall(r"<h1\b", raw)) != 1:
        rep.add("ERROR", "structure", "a brief has exactly one headline")
    if ex.articles or re.search(r'<aside class="notes"', raw):
        rep.add("ERROR", "structure", "presenter notes or slides found in a brief")
    for img in ex.imgs:
        if not img.get("alt", "").strip():
            rep.add("ERROR", "accessibility", "an image has no alt text")
    refs = set(re.findall(r'data-ref="(\d+)"', raw))
    ids = set(re.findall(r'id="src-(\d+)"', raw))
    for r in sorted(refs - ids):
        rep.add("ERROR", "sources", f"reference [{r}] has no entry in the sources list")
    if a.pdf:
        data = Path(a.pdf).read_bytes()
        pages = len(re.findall(rb"/Type\s*/Page(?![s\w])", data))
        rep.add("ERROR" if pages > 2 else "INFO", "print", f"the PDF has {pages} page(s). Two at most")
    tbd = groups.get(("home", "screen"), {}).get("text", "").count("{TBD}")
    if tbd:
        rep.add("INFO", "unknowns", f"{tbd} {{TBD}} marks. Each is something only the prospect knows")

    print(f"brief_check {hp.name}  brain={'found' if brain else 'NOT FOUND'}")
    for sev in ("ERROR", "WARN", "INFO"):
        if a.quiet and sev == "INFO":
            continue
        for it in rep.items:
            if it["severity"] == sev:
                print(f"  {sev:5} [{it['where']}] {it['message']}")
    print(f"\n{rep.count('ERROR')} error(s), {rep.count('WARN')} warning(s).", end=" ")
    print("Do not send." if rep.count("ERROR") else
          ("A person reads every warning before this is sent." if rep.count("WARN") else
           "Clean. The QA checklist still applies: no script can tell you whether a claim is true."))
    return 1 if rep.count("ERROR") or (a.strict and rep.count("WARN")) else 0


if __name__ == "__main__":
    sys.exit(main())
