#!/usr/bin/env bash
# scaffold.sh — thin launcher around `npx create-video@latest`.
# Scaffolds a fresh Remotion project (blank, no Tailwind). PATH-safe for fnm/nvm/Homebrew
# (agent and cron shells often don't have `node` on PATH).
#
# Usage:  scaffold.sh <project-name> [parent-dir]
#   project-name : the folder/name for the new project (required)
#   parent-dir   : where to create it (default: current dir)
#
# Where it goes: project work in the hub phase folder that owns it, e.g.
#   scaffold.sh my-video 01_Project-Hubs/<hub>/03_build
# and personal learning projects in a folder you own outside any work repository.
# Licensing: organizations of 4+ people need a Remotion Company License — see references/licensing.md.
# The blank template's only composition (MyComp) renders nothing; copy templates/Scene.tsx and
# templates/Root.tsx into <project>/src/ for a working first scene (MyScene).
set -euo pipefail

ensure_node() {
  if command -v node >/dev/null 2>&1; then return 0; fi
  # fnm
  if command -v fnm >/dev/null 2>&1; then eval "$(fnm env 2>/dev/null)" || true; fi
  # nvm
  if [ -z "${_NODE_OK:-}" ] && [ -s "$HOME/.nvm/nvm.sh" ]; then
    # shellcheck disable=SC1091
    . "$HOME/.nvm/nvm.sh"; nvm use --silent default 2>/dev/null || true
  fi
  # fnm default install dir on macOS
  for d in "$HOME/.local/share/fnm/node-versions"/*/installation/bin; do
    [ -d "$d" ] && case ":$PATH:" in *":$d:"*) ;; *) PATH="$d:$PATH";; esac
  done
  # Homebrew
  for d in /opt/homebrew/bin /usr/local/bin; do
    [ -x "$d/node" ] && case ":$PATH:" in *":$d:"*) ;; *) PATH="$d:$PATH";; esac
  done
  export PATH
  command -v node >/dev/null 2>&1 || { echo "ERROR: node not found (install Node 18+ or fnm/nvm)"; exit 1; }
}

name="${1:?usage: scaffold.sh <project-name> [parent-dir]}"
parent="${2:-.}"
ensure_node
echo "node: $(node -v)  npx: $(command -v npx)"
mkdir -p "$parent"
cd "$parent"
echo "Scaffolding Remotion project '$name' in $(pwd) ..."
npx create-video@latest --yes --blank --no-tailwind "$name"
echo "Done. Next:  cd $parent/$name && npx remotion studio"
