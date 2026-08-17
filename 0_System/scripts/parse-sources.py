#!/usr/bin/env python3
"""
parse-sources.py — Tiered raw → processed converter for Founder OS.

Walks ``5_Library/sources/raw/`` recursively and converts each file into clean
markdown/CSV under ``5_Library/sources/processed/``, **mirroring the raw/
subfolder layout** and adding a YAML frontmatter block. There is no index file —
the ``processed/`` tree itself is what the pipeline browses.

Engine tiers — best installed wins, per file
--------------------------------------------
  Text (.md/.txt/…) and tables (.csv/.tsv)
      → handled with the Python standard library; no engine needed.
  Office / PDF / images (.pdf/.docx/.pptx/.xlsx/.html/…)
      1. Docling     — if importable (highest fidelity: OCR, scanned PDFs, tables)
      2. MarkItDown  — if importable (fast, offline office + digital PDF)
      3. otherwise   → a stub that recommends the right install — and notes the
                       agent can read PDFs/images itself ("Tier 0").
  Audio / video (.mp3/.wav/.mp4/…)
      → always a stub: bring a transcript, or transcribe locally (faster-whisper).

This script auto-detects what is installed and uses the best available engine.
It NEVER pip-installs or upgrades anything — when it cannot convert a file it
leaves a stub with the exact command for the founder to run themselves.

Usage
-----
  python3 0_System/scripts/parse-sources.py            # convert raw/ → processed/
  python3 0_System/scripts/parse-sources.py --plan     # dry run: what each file
                                                        # WOULD do + what to install
  python3 0_System/scripts/parse-sources.py --force    # reconvert even if up to date
  python3 0_System/scripts/parse-sources.py -h|--help

Idempotent: a processed file is rebuilt only when its raw source is newer, when
the existing output is a stub (so it upgrades once an engine is installed), or
with --force.

Privacy boundary
----------------
  raw/       is gitignored — raw founder data never leaves the machine via the repo.
  processed/ is tracked    — the standardized layer the pipeline reads.
  All conversion runs locally; no file is sent to any external service.
"""

import os
import sys
import datetime
import importlib.util
import re

# ---------------------------------------------------------------------------
# Paths (resolved relative to this script, same approach as scan-skills.py)
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(REPO_ROOT, "5_Library", "sources", "raw")
PROCESSED_DIR = os.path.join(REPO_ROOT, "5_Library", "sources", "processed")

# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

TEXT_EXTENSIONS = {".md", ".txt", ".text", ".markdown", ".rst", ".log"}
CSV_EXTENSIONS = {".csv", ".tsv"}

# Office / document / image formats an installed engine can turn into markdown.
ENGINE_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".epub", ".odt", ".rtf",
    ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp",
}

# Formats the agent itself can read in-session (Tier 0) when no engine is present.
AGENT_READABLE_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp",
}

# Audio / video — never converted locally by default (offline, no-cloud guarantee).
AUDIO_VIDEO_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma",
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
}

# Engines in fidelity order — best first. Detection only; never imported to detect.
ENGINE_PRIORITY = ("docling", "markitdown")

TODAY = datetime.date.today().isoformat()


# ---------------------------------------------------------------------------
# Engine detection + conversion (lazy, memoized, never auto-installs)
# ---------------------------------------------------------------------------


def detect_engines():
    """Return installed engines, best-first. Detection only — no import, no install."""
    return [name for name in ENGINE_PRIORITY if importlib.util.find_spec(name) is not None]


_MARKITDOWN = None
_DOCLING = None


def _markitdown_to_md(path):
    global _MARKITDOWN
    from markitdown import MarkItDown  # lazy: only when actually converting
    if _MARKITDOWN is None:
        _MARKITDOWN = MarkItDown()
    return _MARKITDOWN.convert(path).text_content


def _docling_to_md(path):
    global _DOCLING
    from docling.document_converter import DocumentConverter  # lazy + heavy
    if _DOCLING is None:
        _DOCLING = DocumentConverter()
    return _DOCLING.convert(path).document.export_to_markdown()


_ENGINE_FUNCS = {"markitdown": _markitdown_to_md, "docling": _docling_to_md}


def convert_with_engines(path, engines):
    """
    Try each engine best-first. Return (markdown, engine_name) on success, or
    (None, None) if no engine is installed or every one failed on this file
    (e.g. a missing optional extra) — the caller then writes a stub.
    """
    for name in engines:
        try:
            text = _ENGINE_FUNCS[name](path)
        except Exception:
            continue  # missing extra / unsupported / parse error → try the next engine
        if text and text.strip():
            return text, name
    return None, None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mtime_iso(path):
    try:
        ts = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(ts).date().isoformat()
    except OSError:
        return TODAY


def _rel(path, base):
    return os.path.relpath(path, base).replace(os.sep, "/")


def _safe_stem(filename):
    stem, _ = os.path.splitext(filename)
    return re.sub(r"[^\w\-.]", "-", stem.lower())


def _subdir_for(raw_abs):
    """Relative subdirectory of a raw file from RAW_DIR ('' at top level)."""
    rel = os.path.relpath(os.path.dirname(raw_abs), RAW_DIR)
    return "" if rel == "." else rel.replace(os.sep, "/")


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _read_text(path):
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, OSError):
            continue
    return ""


def _is_binary(path):
    """Heuristic: a null byte in the first 8 KB means binary."""
    try:
        with open(path, "rb") as f:
            return b"\x00" in f.read(8192)
    except OSError:
        return False


def _frontmatter(file_type, source_rel, date, engine=None, status=None):
    lines = ["---", f"type: {file_type}", f"source: {source_rel}",
             f"date: {date}", f"processed: {TODAY}"]
    if engine:
        lines.append(f"engine: {engine}")
    if status:
        lines.append(f"status: {status}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _strip_frontmatter(text):
    return re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)


def _is_stub(path):
    """True if an existing processed file is a converter stub (so we re-attempt it)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return "status: stub" in f.read(400)
    except OSError:
        return False


def _up_to_date(out_path, raw_abs):
    """A real (non-stub) output that is at least as new as its source can be skipped."""
    if not os.path.exists(out_path):
        return False
    try:
        if os.path.getmtime(out_path) < os.path.getmtime(raw_abs):
            return False
    except OSError:
        return False
    return not _is_stub(out_path)


def classify(ext):
    if ext in CSV_EXTENSIONS:
        return "csv"
    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in AUDIO_VIDEO_EXTENSIONS:
        return "audio"
    if ext in ENGINE_EXTENSIONS:
        return "engine"
    return "unknown"


def install_hint(ext):
    """One-line, copy-pasteable guidance for a file we cannot convert as-is."""
    if ext in AUDIO_VIDEO_EXTENSIONS:
        return ("audio/video — bring a transcript (Zoom/Otter/Granola export) into raw/, "
                "or transcribe locally with faster-whisper (`pip install faster-whisper`).")
    if ext == ".pdf":
        return ('PDF — `pip install "markitdown[pdf]"` (digital) or `pip install docling` '
                "(scanned/complex). Or let your agent read the PDF directly (Tier 0).")
    if ext in {".docx", ".doc", ".odt", ".rtf", ".pptx", ".ppt", ".xlsx", ".xls"}:
        return ('Office doc — `pip install "markitdown[docx,pptx,xlsx]"` '
                "(or `pip install docling`).")
    if ext in {".html", ".htm", ".epub"}:
        return "`pip install markitdown` (or `pip install docling`)."
    if ext in AGENT_READABLE_EXTENSIONS:  # images
        return ("image — `pip install docling` for OCR, or let your agent read it directly "
                "(Tier 0).")
    return ("unrecognized format — convert it manually and drop the markdown/text into raw/, "
            "or `pip install docling`.")


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------


def _write(out_path, content):
    _ensure_dir(os.path.dirname(out_path))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)


def write_text_md(raw_abs, source_rel, out_path, date, file_type):
    content = _strip_frontmatter(_read_text(raw_abs))
    _write(out_path, _frontmatter(file_type, source_rel, date) + content.lstrip("\n"))


def write_csv(raw_abs, source_rel, out_csv, out_sidecar, date):
    try:
        with open(raw_abs, "rb") as f:
            raw_bytes = f.read()
    except OSError:
        raw_bytes = b""
    _ensure_dir(os.path.dirname(out_csv))
    with open(out_csv, "wb") as f:
        f.write(raw_bytes)
    name = os.path.basename(out_csv)
    sidecar = _frontmatter("csv", source_rel, date)
    sidecar += f"CSV data file. See `{name}` in the same folder.\n"
    _write(out_sidecar, sidecar)


def write_engine_md(source_rel, out_path, md_text, engine, date, file_type):
    body = _strip_frontmatter(md_text).lstrip("\n")
    _write(out_path, _frontmatter(file_type, source_rel, date, engine=engine) + body)


def write_stub(raw_abs, source_rel, out_path, date, file_type, ext):
    stub = _frontmatter(file_type, source_rel, date, status="stub")
    stub += f"# {os.path.basename(raw_abs)}\n\n"
    stub += (
        "> **Not converted — no installed engine can handle this file yet.**\n"
        f"> Source: `{source_rel}`\n"
        ">\n"
        f"> To convert it: {install_hint(ext)}\n"
        ">\n"
        "> This script never installs anything for you. Once the converter is\n"
        "> installed, re-run `python3 0_System/scripts/parse-sources.py` and this\n"
        "> stub is replaced automatically. Or paste the content below this block.\n"
    )
    _write(out_path, stub)


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------


def _row(source_rel, file_type, date, out_rel, status, engine):
    return {"source": source_rel, "type": file_type, "date": date,
            "output": out_rel, "status": status, "engine": engine}


def process_file(raw_abs, engines, force):
    filename = os.path.basename(raw_abs)
    ext = os.path.splitext(filename)[1].lower()
    source_rel = _rel(raw_abs, RAW_DIR)
    subdir = _subdir_for(raw_abs)
    out_dir = os.path.join(PROCESSED_DIR, subdir) if subdir else PROCESSED_DIR
    stem = _safe_stem(filename)
    date = _mtime_iso(raw_abs)
    file_type = ext.lstrip(".") or "text"
    category = classify(ext)

    # CSV keeps its own extension plus a markdown sidecar.
    if category == "csv":
        out_csv = os.path.join(out_dir, stem + ext)
        out_sidecar = os.path.join(out_dir, stem + ".md")
        # CSV writes two files; only skip when BOTH are present and current, so an
        # interrupted run can't leave the .md sidecar permanently missing.
        if not force and _up_to_date(out_csv, raw_abs) and os.path.exists(out_sidecar):
            return _row(source_rel, file_type, date, _rel(out_csv, REPO_ROOT), "current", "stdlib")
        write_csv(raw_abs, source_rel, out_csv, out_sidecar, date)
        return _row(source_rel, file_type, date, _rel(out_csv, REPO_ROOT), "converted", "stdlib")

    out_path = os.path.join(out_dir, stem + ".md")
    if not force and _up_to_date(out_path, raw_abs):
        return _row(source_rel, file_type, date, _rel(out_path, REPO_ROOT), "current", None)

    out_rel = _rel(out_path, REPO_ROOT)

    if category == "text":
        write_text_md(raw_abs, source_rel, out_path, date, file_type)
        return _row(source_rel, file_type, date, out_rel, "converted", "stdlib")

    if category == "audio":
        write_stub(raw_abs, source_rel, out_path, date, file_type, ext)
        return _row(source_rel, file_type, date, out_rel, "stub", None)

    if category == "engine" or (category == "unknown" and _is_binary(raw_abs)):
        if engines:
            md, used = convert_with_engines(raw_abs, engines)
            if md:
                write_engine_md(source_rel, out_path, md, used, date, file_type)
                return _row(source_rel, file_type, date, out_rel, "converted", used)
        write_stub(raw_abs, source_rel, out_path, date, file_type, ext)
        return _row(source_rel, file_type, date, out_rel, "stub", None)

    # unknown + not binary → treat as text (best-effort decode)
    write_text_md(raw_abs, source_rel, out_path, date, file_type)
    return _row(source_rel, file_type, date, out_rel, "converted", "stdlib")


# ---------------------------------------------------------------------------
# Walk + planning
# ---------------------------------------------------------------------------


def iter_raw_files():
    if not os.path.isdir(RAW_DIR):
        return
    for dirpath, dirnames, filenames in os.walk(RAW_DIR):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for filename in sorted(filenames):
            if filename.startswith(".") or filename == ".gitkeep":
                continue
            yield os.path.join(dirpath, filename)


def plan_action(raw_abs, engines):
    """(action, engine_or_None, ext) for --plan — decides nothing on disk."""
    ext = os.path.splitext(raw_abs)[1].lower()
    category = classify(ext)
    if category in ("text", "csv"):
        return "convert", "stdlib", ext
    if category == "audio":
        return "stub", None, ext
    if category == "engine" or (category == "unknown" and _is_binary(raw_abs)):
        return ("convert", engines[0], ext) if engines else ("stub", None, ext)
    return "convert", "stdlib", ext


def recommendations(stub_exts, engines):
    """Consolidated install guidance for the formats we had to stub."""
    recs = []
    office = stub_exts & {".pdf", ".docx", ".doc", ".odt", ".rtf", ".pptx", ".ppt",
                          ".xlsx", ".xls", ".html", ".htm", ".epub"}
    images = stub_exts & {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp"}
    audio = stub_exts & AUDIO_VIDEO_EXTENSIONS
    if office:
        if not engines:
            recs.append('Install a converter for office/PDF files: '
                        '`pip install "markitdown[pdf,docx,pptx,xlsx]"` '
                        '(fast, offline) — or `pip install docling` (scanned PDFs, OCR).')
        else:
            recs.append("Some office/PDF files need higher-fidelity conversion. "
                        "Install Docling for OCR: `pip install docling`.")
    if images and "docling" not in engines:
        recs.append("Images need OCR (`pip install docling`) — or let your agent read "
                    "them directly in-session (Tier 0).")
    if audio:
        recs.append("Audio/video isn't converted locally. Bring a transcript into raw/, or "
                    "`pip install faster-whisper` to transcribe locally.")
    return recs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run_plan(engines):
    print("\nparse-sources.py --plan (dry run -- nothing written)\n")
    print(f"  Installed engines: {', '.join(engines) if engines else 'none (text/CSV only)'}")
    if engines:
        print("  (engine shown is the best installed; the real run tries it first and falls")
        print("   through to the next if it fails on a given file.)")
    print()
    files = list(iter_raw_files())
    if not files:
        print("  raw/ is empty -- drop files into 5_Library/sources/raw/ and re-run.\n")
        return
    stub_exts = set()
    stub_count = 0
    for raw_abs in files:
        action, engine, ext = plan_action(raw_abs, engines)
        source_rel = _rel(raw_abs, RAW_DIR)
        if action == "stub":
            stub_exts.add(ext)
            stub_count += 1
            print(f"  !  {source_rel}  ->  stub  ({install_hint(ext)})")
        else:
            print(f"  ok  {source_rel}  ->  convert  [{engine or 'stdlib'}]")
    print(f"\n  {len(files)} file(s); {stub_count} would be stubbed with what's installed.")
    recs = recommendations(stub_exts, engines)
    if recs:
        print("\n  To convert everything (run the install yourself -- this script won't):")
        for r in recs:
            print(f"    - {r}")
    print()


def run_convert(engines, force):
    print(f"\nparse-sources.py -- scanning {_rel(RAW_DIR, REPO_ROOT)}/")
    print(f"  Engines: {', '.join(engines) if engines else 'none (text/CSV only)'}\n")
    _ensure_dir(PROCESSED_DIR)

    rows = []
    stub_exts = set()
    for raw_abs in iter_raw_files():
        row = process_file(raw_abs, engines, force)
        rows.append(row)
        if row["status"] == "stub":
            stub_exts.add(os.path.splitext(raw_abs)[1].lower())
        icon = {"converted": "✓", "current": "·", "stub": "!"}.get(row["status"], "?")
        tag = row["status"] if not row["engine"] else f"{row['status']}:{row['engine']}"
        print(f"  {icon}  {row['source']}  ->  {row['output']}  [{tag}]")

    if not rows:
        print("  raw/ is empty -- drop files into 5_Library/sources/raw/ and re-run.\n")
        return

    converted = sum(1 for r in rows if r["status"] == "converted")
    current = sum(1 for r in rows if r["status"] == "current")
    stubs = sum(1 for r in rows if r["status"] == "stub")
    print(f"\n  {len(rows)} file(s)  |  {converted} converted  |  "
          f"{current} unchanged  |  {stubs} stub(s) needing a converter\n")

    recs = recommendations(stub_exts, engines)
    if recs:
        print("  Some files couldn't be converted with what's installed. To finish them")
        print("  (install it yourself -- this script never installs anything):")
        for r in recs:
            print(f"    - {r}")
        print()


def main():
    args = set(sys.argv[1:])
    if args & {"-h", "--help"}:
        print(__doc__)
        return
    engines = detect_engines()
    if "--plan" in args:
        run_plan(engines)
    else:
        run_convert(engines, force="--force" in args)


if __name__ == "__main__":
    main()
