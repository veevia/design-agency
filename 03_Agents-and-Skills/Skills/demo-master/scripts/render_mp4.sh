#!/usr/bin/env bash
# render_mp4.sh — compose a demo-master deck (.html) into a shareable MP4.
#
# THE GAP THIS CLOSES: demo-master produces a click-through .html (great for presenting live,
# but you can't *send* it as a video). This is the composition step that closes the agent → final-video
# loop, under three constraints:
#   • one openable artifact (an .mp4 you can drop into a team chat or email), not "live at localhost"
#   • real frames, not a redraw — headless Chrome screenshots the actual deck
#   • capture-safe: drives the engine's ?still=1 mode so keyframe animations settle (no blank frames)
#
# Usage:
#   ./render_mp4.sh <deck.html> <total_beats> [out.mp4] [seconds_per_beat]
#   ./render_mp4.sh my-demo.html 14 my-demo.mp4 2.5
#
# Requires: headless Chrome (Google Chrome / Chromium; set CHROME=<path> to override) + ffmpeg. Both checked below.
set -euo pipefail

DECK="${1:?usage: render_mp4.sh <deck.html> <total_beats> [out.mp4] [sec_per_beat]}"
BEATS="${2:?need total beat count (the number of click-steps in the deck)}"
OUT="${3:-${DECK%.html}.mp4}"
SPB="${4:-2.5}"   # seconds per beat

# --- resolve an absolute file:// path (Chrome needs absolute) ---
DECK_ABS="$(cd "$(dirname "$DECK")" && pwd)/$(basename "$DECK")"
[ -f "$DECK_ABS" ] || { echo "render_mp4: deck not found: $DECK_ABS" >&2; exit 1; }

# --- find a Chrome binary: $CHROME wins, then the usual install locations, then PATH ---
CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "$(command -v google-chrome 2>/dev/null || true)" \
    "$(command -v google-chrome-stable 2>/dev/null || true)" \
    "$(command -v chromium 2>/dev/null || true)" \
    "$(command -v chromium-browser 2>/dev/null || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && { CHROME="$c"; break; }
  done
fi
[ -n "$CHROME" ] && [ -x "$CHROME" ] || { echo "render_mp4: no Chrome/Chromium found (install one, or set CHROME=<path>)." >&2; exit 2; }
command -v ffmpeg >/dev/null 2>&1 || { echo "render_mp4: ffmpeg not on PATH (install ffmpeg)." >&2; exit 2; }

TMP="$(mktemp -d -t demomaster-render-XXXX)"
trap 'rm -rf "$TMP"' EXIT
echo "render_mp4: deck=$DECK_ABS · beats=$BEATS · $SPB s/beat · chrome=$(basename "$CHROME")"

# --- 1. capture one settled frame per beat (?start=N&b=N&still=1 — engine and reference-deck styles) ---
for i in $(seq 0 $((BEATS - 1))); do
  printf -v FN "%s/frame_%03d.png" "$TMP" "$i"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=1280,720 \
    --virtual-time-budget=2600 \
    --screenshot="$FN" \
    "file://${DECK_ABS}?start=${i}&b=${i}&still=1" >/dev/null 2>&1
  [ -s "$FN" ] || { echo "render_mp4: blank/empty frame at beat $i — aborting." >&2; exit 3; }
  echo "  ✓ beat $i → $(basename "$FN")"
done

# --- 2. stitch to MP4 at fixed seconds-per-beat (concat demuxer = exact per-frame duration) ---
LIST="$TMP/frames.txt"
: > "$LIST"
for i in $(seq 0 $((BEATS - 1))); do
  printf "file '%s/frame_%03d.png'\nduration %s\n" "$TMP" "$i" "$SPB" >> "$LIST"
done
# concat demuxer needs the last frame repeated (no trailing duration) to hold it
printf "file '%s/frame_%03d.png'\n" "$TMP" "$((BEATS - 1))" >> "$LIST"

ffmpeg -y -f concat -safe 0 -i "$LIST" \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
  -c:v libx264 -preset medium -movflags +faststart "$OUT" >/dev/null 2>&1

[ -s "$OUT" ] || { echo "render_mp4: ffmpeg produced no output." >&2; exit 4; }
SIZE=$(du -h "$OUT" | cut -f1)
echo "render_mp4: ✅ $OUT ($SIZE, ${BEATS} beats × ${SPB}s)"
