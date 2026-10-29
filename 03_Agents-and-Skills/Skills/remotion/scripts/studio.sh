#!/usr/bin/env bash
# studio.sh — thin launcher around `npx remotion studio` (the live preview editor).
# PATH-safe for fnm/nvm/Homebrew.
#
# Usage:  studio.sh [project-dir]
#   project-dir : the Remotion project root (default: current dir)
#
# Studio runs a local dev server. NOTE: when an agent starts it, the agent's browser session is not
# yours — open the printed URL in your own browser to actually see it.
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

proj="${1:-.}"
ensure_node
cd "$proj"
[ -f package.json ] || { echo "ERROR: no package.json in $(pwd) — is this a Remotion project?"; exit 1; }
echo "node: $(node -v)  ·  starting Remotion Studio in $(pwd)"
exec npx remotion studio
