#!/usr/bin/env python3
"""demo-master deck runtime check — headless Chrome, zero extra deps.

Loads every beat of a built deck in headless Chrome (STILL mode) and asserts the
runtime rubric rows the static linter can't see. v1 covers the highest-value one:

    * 0 console / JS errors on every beat   (the thing we verify by hand each round)

It auto-detects the beat count from the deck's console banner ("... N beats ...")
and excludes the benign favicon 404. Uses a Google Chrome or Chromium already on the
machine (same dependency as scripts/render_mp4.sh) — no Playwright, no pip install.
Chrome is found via --chrome, then $CHROME, then the usual install locations, then PATH.

Overflow / transition-cleared / focal-motion checks need DOM geometry and are the
next increment (they want CDP/Playwright); this file is structured so they slot in.

Usage:
    python3 check_runtime.py <url-or-file> [--beats N] [--chrome PATH] [--json]

  <url-or-file>  a served URL (e.g. http://127.0.0.1:8170/.../deck.html) or a
                 path to a self-contained deck (opened via file://).
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Usual install locations, then command names looked up on PATH.
CHROME_LOCATIONS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)
CHROME_COMMANDS = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")

# a stderr line is a real page JS error if it mentions the console AND a JS fault
ERR_SIGNALS = re.compile(
    r"(Uncaught|ReferenceError|TypeError|SyntaxError|RangeError|is not defined|"
    r"Cannot read|Cannot access|is not a function|Unexpected token)", re.I)
CONSOLE_LINE = re.compile(r"CONSOLE|Uncaught|ERROR:", re.I)
BANNER_BEATS = re.compile(r"(\d+)\s*(?:beats|steps)\b", re.I)  # engine.html logs "N steps", reference-deck "N beats"
BENIGN = re.compile(r"favicon|Failed to load resource.*favicon|GPU|gpu_|Voltage|sandbox", re.I)


def beat_url(base: str, k: int) -> str:
    # `start` drives decks built from templates/engine.html; `b` drives reference-deck-style decks.
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}still=1&start={k}&b={k}&cb={k}"


def run_chrome(chrome: str, url: str, profile: Path, budget_ms: int = 1800) -> str:
    """Load url in headless Chrome, return combined stderr (console log)."""
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-sandbox",
        "--hide-scrollbars", "--mute-audio", "--disable-extensions",
        "--enable-logging=stderr", "--v=1", f"--user-data-dir={profile}",
        "--dump-dom", url,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        return p.stderr or ""
    except subprocess.TimeoutExpired as e:
        return (e.stderr.decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")) + "\n[check_runtime] chrome timed out"


def page_errors(stderr: str) -> list[str]:
    out = []
    for line in stderr.splitlines():
        if not CONSOLE_LINE.search(line):
            continue
        if BENIGN.search(line):
            continue
        if ERR_SIGNALS.search(line):
            out.append(line.strip()[:240])
    return out


def to_url(target: str) -> str:
    if target.startswith("http://") or target.startswith("https://") or target.startswith("file://"):
        return target
    return Path(target).resolve().as_uri()


def find_chrome() -> str | None:
    """$CHROME first, then the usual install locations, then PATH."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for location in CHROME_LOCATIONS:
        if Path(location).exists():
            return location
    for name in CHROME_COMMANDS:
        found = shutil.which(name)
        if found:
            return found
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Headless-Chrome runtime gate for a built deck (0 console errors / beat).")
    ap.add_argument("target", help="served URL or path to a self-contained deck")
    ap.add_argument("--beats", type=int, default=None, help="beat count (default: auto-detect from console banner)")
    ap.add_argument("--chrome", default=None, help="path to Google Chrome or Chromium (default: $CHROME, usual locations, PATH)")
    ap.add_argument("--max", type=int, default=40, help="safety cap on beats to probe")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    chrome = args.chrome or find_chrome()
    if not chrome or not Path(chrome).exists():
        print(f"error: Chrome not found{f' at {chrome}' if chrome else ''} (pass --chrome or set CHROME)", file=sys.stderr)
        return 2
    args.chrome = chrome

    url = to_url(args.target)
    with tempfile.TemporaryDirectory(prefix="deckcheck-") as tmp:
        profile = Path(tmp)

        # beat 0 → detect beat count from the deck's console banner
        first = run_chrome(args.chrome, beat_url(url, 0), profile)
        beats = args.beats
        if beats is None:
            m = BANNER_BEATS.search(first)
            beats = int(m.group(1)) if m else 1
            if not m:
                print("warn: no '... N beats' banner found; checking beat 0 only (pass --beats N)", file=sys.stderr)
        beats = min(beats, args.max)

        results = []  # (beat, [errors])
        results.append((0, page_errors(first)))
        for k in range(1, beats):
            errs = page_errors(run_chrome(args.chrome, beat_url(url, k), profile))
            results.append((k, errs))

    total = sum(len(e) for _, e in results)
    bad = [(k, e) for k, e in results if e]

    if args.json:
        print(json.dumps({
            "url": url, "beats_checked": len(results), "total_errors": total,
            "beats_with_errors": [{"beat": k, "errors": e} for k, e in bad],
        }, indent=2))
    else:
        for k, e in bad:
            for msg in e:
                print(f"error | console | beat {k:02} | {msg}")
        verdict = "PASS (0 console errors)" if total == 0 else f"FAIL ({total} console error(s))"
        print(f"\ncheck_runtime: {len(results)} beats checked — {verdict}")

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
