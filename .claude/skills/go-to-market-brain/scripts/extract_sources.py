#!/usr/bin/env python3
"""
Extract GTM source material into readable Markdown.

Phase 1 of the Go-to-Market Brain build. Walks a directory of source
artifacts (XLSX, DOCX, PPTX, PDF, CSV, MD, TXT) and writes one Markdown
file per source, plus a manifest stub to fill in.

    python3 extract_sources.py <source_dir> <out_dir>

Optional dependencies, installed only as needed:
    pip install openpyxl python-docx python-pptx pypdf
"""

import csv
import os
import re
import sys
from pathlib import Path

MAX_ROWS = 3000
MAX_COL_CHARS = 300


def slug(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s or "source"


def missing(dep: str, pkg: str) -> str:
    return f"_Could not read this file: `{dep}` is not installed. Run `pip install {pkg}`._\n"


def cell(value) -> str:
    if value is None:
        return ""
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > MAX_COL_CHARS:
        text = text[: MAX_COL_CHARS - 3] + "..."
    return text


def read_xlsx(path: Path) -> str:
    try:
        import openpyxl
    except ImportError:
        return missing("openpyxl", "openpyxl")

    out = []
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    for ws in wb.worksheets:
        out.append(f"\n## Sheet: {ws.title}\n")
        count = 0
        for row in ws.iter_rows(values_only=True):
            cells = [cell(c) for c in row]
            while cells and not cells[-1]:
                cells.pop()
            if not any(cells):
                continue
            out.append("| " + " | ".join(cells) + " |")
            count += 1
            if count >= MAX_ROWS:
                out.append(f"\n_Truncated at {MAX_ROWS} rows._")
                break
        if count == 0:
            out.append("_Empty sheet._")
    wb.close()
    return "\n".join(out) + "\n"


def read_docx(path: Path) -> str:
    try:
        import docx
    except ImportError:
        return missing("python-docx", "python-docx")

    document = docx.Document(str(path))
    out = []
    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style_obj = getattr(para, "style", None)
        style = (getattr(style_obj, "name", "") or "").lower()
        if style.startswith("heading"):
            level = "".join(ch for ch in style if ch.isdigit()) or "2"
            out.append("\n" + "#" * min(int(level) + 1, 6) + f" {text}\n")
        elif style.startswith("title"):
            out.append(f"\n## {text}\n")
        elif style.startswith("list"):
            out.append(f"- {text}")
        else:
            out.append(text + "\n")

    for i, table in enumerate(document.tables, 1):
        out.append(f"\n### Table {i}\n")
        for row in table.rows:
            out.append("| " + " | ".join(cell(c.text) for c in row.cells) + " |")
    return "\n".join(out) + "\n"


def read_pptx(path: Path) -> str:
    try:
        from pptx import Presentation
    except ImportError:
        return missing("python-pptx", "python-pptx")

    prs = Presentation(str(path))
    out = []
    for i, slide in enumerate(prs.slides, 1):
        out.append(f"\n## Slide {i}\n")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = "".join(run.text for run in para.runs).strip()
                    if text:
                        out.append(text)
            if getattr(shape, "has_table", False):
                for row in shape.table.rows:
                    out.append("| " + " | ".join(cell(c.text) for c in row.cells) + " |")
    return "\n".join(out) + "\n"


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return missing("pypdf", "pypdf")

    reader = PdfReader(str(path))
    out = []
    for i, page in enumerate(reader.pages, 1):
        out.append(f"\n## Page {i}\n")
        out.append((page.extract_text() or "").strip())
    return "\n".join(out) + "\n"


def read_csv(path: Path) -> str:
    out = []
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        for i, row in enumerate(csv.reader(fh)):
            out.append("| " + " | ".join(cell(c) for c in row) + " |")
            if i >= MAX_ROWS:
                out.append(f"\n_Truncated at {MAX_ROWS} rows._")
                break
    return "\n".join(out) + "\n"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


READERS = {
    ".xlsx": read_xlsx,
    ".xlsm": read_xlsx,
    ".docx": read_docx,
    ".pptx": read_pptx,
    ".pdf": read_pdf,
    ".csv": read_csv,
    ".md": read_text,
    ".txt": read_text,
}


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    src = Path(sys.argv[1]).expanduser()
    out = Path(sys.argv[2]).expanduser()
    if not src.is_dir():
        print(f"Not a directory: {src}")
        return 2
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    skipped = []

    for path in sorted(src.rglob("*")):
        if not path.is_file() or path.name.startswith((".", "~$")):
            continue
        reader = READERS.get(path.suffix.lower())
        if reader is None:
            skipped.append(path.name)
            continue

        print(f"reading {path.name}")
        try:
            body = reader(path)
        except Exception as exc:  # a bad source should not stop the run
            body = f"_Extraction failed: {exc}_\n"

        target = out / f"{slug(path.stem)}.md"
        header = (
            f"# Source: {path.name}\n\n"
            f"Original path: `{path}`\n"
            f"Type: {path.suffix.lower().lstrip('.')}\n"
            f"Size: {path.stat().st_size:,} bytes\n"
        )
        target.write_text(header + body, encoding="utf-8")
        manifest.append((path.name, path.suffix.lower().lstrip("."), target.name))

    lines = [
        "# Source manifest",
        "",
        "Fill the two empty columns before distilling anything. An artifact that",
        "settles nothing is background reading, not a source. If two artifacts settle",
        "the same question differently, resolve it with the owner before continuing.",
        "",
        "| Artifact | Type | Extract | What it settles | Dated |",
        "|---|---|---|---|---|",
    ]
    for name, kind, extract in manifest:
        lines.append(f"| {name} | {kind} | [{extract}]({extract}) |  |  |")
    if skipped:
        lines += ["", "## Skipped (unsupported type)", ""]
        lines += [f"- {n}" for n in skipped]
    (out / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n{len(manifest)} sources extracted to {out}")
    if skipped:
        print(f"{len(skipped)} skipped: {', '.join(skipped)}")
    print(f"Fill in {out / 'INDEX.md'} before distilling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
