#!/usr/bin/env python3
"""demo-master deck linter — static, deterministic quality gate.

Scans a *built* deck .html against references/design-tokens.json and reports the
deterministic rubric rows as `severity | rule | file:line | message`.

This is the STATIC tier. It does NOT (and cannot) cover the runtime rows —
console errors, stage overflow, transition-cleared-before-loop, focal-motion
count — those belong to scripts/check_runtime.py (headless Chrome). It also does
NOT judge taste rows (narrative fit, metaphor, "feels physical"); those are the
agent-evaluated prose rubric.

Stdlib only. Exit code is non-zero if any ERROR-severity finding is present, so it
can gate a build.

Usage:
    python3 lint_deck.py <deck.html> [--tokens design-tokens.json] [--json]
"""
from __future__ import annotations
import argparse
import colorsys
import json
import re
import sys
from pathlib import Path

ERROR, WARN, INFO = "error", "warn", "info"

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
FONT_RE = re.compile(r"font-size:\s*([0-9.]+)px")
EXTERNAL_RE = re.compile(r"<(?:script|link)\b[^>]*\b(?:src|href)\s*=\s*[\"']https?://", re.I)
# true emoji / pictographs / dingbats (NOT arrows U+2190-21FF or punctuation)
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0000FE0F]")


def norm_hex(h: str):
    """'#rgb' / '#rrggbb' / '#rrggbbaa' -> (r, g, b) ints, dropping alpha."""
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def sat_light(rgb):
    r, g, b = (c / 255 for c in rgb)
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    return s, l


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def load_tokens(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def allowed_palette(tokens: dict):
    out = []
    for src in ("color_roles", "semantic_palette"):
        for name, hx in tokens.get(src, {}).items():
            out.append((name, norm_hex(hx)))
    return out


def in_type_scale(px: float, tokens: dict) -> bool:
    tol = tokens.get("type_tolerance_px", 1.0)
    return any(abs(px - v) <= tol for v in tokens["type_scale_px"].values())


def lint(deck: Path, tokens: dict):
    findings = []  # (severity, rule, line_no, message)
    palette = allowed_palette(tokens)
    tol = tokens.get("color_distance_tolerance", 46)
    min_sat = tokens.get("color_min_saturation", 0.35)
    lo_l, hi_l = tokens.get("color_lightness_bounds", [0.12, 0.9])
    fake = [t.lower() for t in tokens["lint"]["fake_data_tokens"]]
    slop = [t.lower() for t in tokens["lint"]["slop_hexes"]]
    capture_tokens = [t.lower() for t in tokens["lint"]["capture_mode_tokens"]]
    type_min = tokens.get("type_check_min_px", 30)

    text = deck.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    low_all = text.lower()

    # ---- whole-file rule: capture-safe (STILL) mode present ----
    if not any(tok in low_all for tok in capture_tokens):
        findings.append((WARN, "no-capture-mode", 0,
                         "no STILL/freeze capture param found — deck may not be capture-safe (blank MP4 frames, hard to verify)"))

    seen_offpal = set()
    for i, line in enumerate(lines, 1):
        low = line.lower()

        # R4 self-contained (external build dep)
        if EXTERNAL_RE.search(line):
            findings.append((ERROR, "not-self-contained", i,
                             "external http(s) <script>/<link> — breaks offline file:// open; inline it"))

        # R2 fake / placeholder data
        for t in fake:
            if t in low:
                findings.append((ERROR, "fake-data", i, f"placeholder/fake token '{t}' — ground every value in real content"))

        # R3 known AI-slop hues
        for sx in slop:
            if sx in low:
                findings.append((WARN, "slop-color", i, f"AI-slop hue {sx} — use the semantic palette, not generic purple/pink"))

        # R1 off-palette saturated color
        for m in HEX_RE.findall(line):
            key = (i, m.lower())
            if key in seen_offpal:
                continue
            rgb = norm_hex(m)
            s, l = sat_light(rgb)
            if s < min_sat or not (lo_l < l < hi_l):
                continue  # grey / near-white / near-black — fine as neutral
            if min((dist(rgb, p) for _, p in palette), default=999) > tol:
                seen_offpal.add(key)
                findings.append((WARN, "off-palette-color", i,
                                 f"saturated {m} is off-token — reserve color for the semantic palette (color = meaning)"))

        # R7 heading font-size off the type scale
        for fm in FONT_RE.findall(line):
            px = float(fm)
            if px >= type_min and not in_type_scale(px, tokens):
                findings.append((INFO, "off-type-scale", i,
                                 f"heading font-size {px}px is off the type scale — snap to a scale step"))

        # R9 emoji-as-icon
        if EMOJI_RE.search(line) and "<!--" not in low:
            findings.append((WARN, "emoji-as-icon", i,
                             "emoji in markup — use SVG/typographic marks, not emoji-as-icons"))

    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Static quality gate for a built demo-master deck.")
    ap.add_argument("deck", help="path to the built .html deck")
    ap.add_argument("--tokens", default=None, help="path to design-tokens.json (default: ../references/design-tokens.json)")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = ap.parse_args(argv)

    deck = Path(args.deck)
    if not deck.is_file():
        print(f"error: deck not found: {deck}", file=sys.stderr)
        return 2
    tokens_path = Path(args.tokens) if args.tokens else Path(__file__).resolve().parent.parent / "references" / "design-tokens.json"
    if not tokens_path.is_file():
        print(f"error: tokens not found: {tokens_path}", file=sys.stderr)
        return 2

    tokens = load_tokens(tokens_path)
    findings = lint(deck, tokens)
    order = {ERROR: 0, WARN: 1, INFO: 2}
    findings.sort(key=lambda f: (order[f[0]], f[2]))
    n_err = sum(1 for f in findings if f[0] == ERROR)
    n_warn = sum(1 for f in findings if f[0] == WARN)
    n_info = sum(1 for f in findings if f[0] == INFO)

    if args.json:
        print(json.dumps({
            "deck": str(deck), "errors": n_err, "warnings": n_warn, "info": n_info,
            "findings": [{"severity": s, "rule": r, "line": ln, "message": msg} for s, r, ln, msg in findings],
        }, indent=2))
    else:
        rel = deck.name
        for s, r, ln, msg in findings:
            loc = f"{rel}:{ln}" if ln else rel
            print(f"{s:5} | {r:20} | {loc:32} | {msg}")
        print(f"\nlint_deck: {n_err} error(s), {n_warn} warning(s), {n_info} info  —  "
              + ("FAIL (errors gate)" if n_err else "PASS (no errors)"))
        print("note: runtime rows (console / overflow / loop-cleared / focal-motion) are check_runtime.py's job.")

    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
