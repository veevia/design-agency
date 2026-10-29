#!/usr/bin/env bash
# render.sh — thin launcher around `npx remotion render` (and `still`).
# Produces the real .mp4 (or a one-frame .png with --still). PATH-safe for fnm/nvm/Homebrew.
#
# Usage:
#   render.sh <composition-id> <out.mp4> [project-dir] [-- extra remotion args...]
#   render.sh --still <composition-id> <out.png> [project-dir] [--frame=N]
#
# Examples:
#   render.sh MyComp out/video.mp4
#   render.sh MyComp out/video.mp4 path/to/my-video -- --props=data.json
#   render.sh --still MyComp out/frame.png . --frame=30
set -euo pipefail

ensure_node() {
  if command -v node >/dev/null 2>&1; then return 0; fi
  if command -v fnm >/dev/null 2>&1; then eval "$(fnm env 2>/dev/null)" || true; fi
  if [ -s "$HOME/.nvm/nvm.sh" ]; then
    # shellcheck disable=SC1091
    . "$HOME/.nvm/nvm.sh"; nvm use --silent default 2>/dev/null || true
  fi
  for d in "$HOME/.local/share/fnm/node-versions"/*/installation/bin; do
    [ -d "$d" ] && case ":$PATH:" in *":$d:"*) ;; *) PATH="$d:$PATH";; esac
  done
  for d in /opt/homebrew/bin /usr/local/bin; do
    [ -x "$d/node" ] && case ":$PATH:" in *":$d:"*) ;; *) PATH="$d:$PATH";; esac
  done
  export PATH
  command -v node >/dev/null 2>&1 || { echo "ERROR: node not found (install Node 18+ or fnm/nvm)"; exit 1; }
}

mode="render"
if [ "${1:-}" = "--still" ]; then mode="still"; shift; fi

id="${1:?usage: render.sh [--still] <composition-id> <out> [project-dir] [-- extra args]}"
out="${2:?missing output path}"
proj="${3:-.}"
shift || true; shift || true; shift || true
# drop a leading `--` separator if present
[ "${1:-}" = "--" ] && shift || true
extra=("$@")

ensure_node
cd "$proj"
[ -f package.json ] || { echo "ERROR: no package.json in $(pwd) — is this a Remotion project?"; exit 1; }
mkdir -p "$(dirname "$out")"
echo "node: $(node -v)  ·  $mode '$id' → $out  (in $(pwd))"
if [ "$mode" = "still" ]; then
  exec npx remotion still "$id" "$out" "${extra[@]}"
else
  exec npx remotion render "$id" "$out" "${extra[@]}"
fi
