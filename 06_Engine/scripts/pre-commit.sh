#!/usr/bin/env bash
# pre-commit — credential scan + fast OS review (incl. the privacy gate) of exactly what is staged.
# Install with 06_Engine/scripts/install-hooks.sh. Bypass deliberately with: git commit --no-verify
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
PY="${AGENCY_PYTHON:-python3}"
# The local privacy denylist is never committed, so the exported index cannot see it: pass it explicitly.
if [ -f "$ROOT/.agency/denylist.txt" ]; then
  export AGENCY_DENYLIST="$ROOT/.agency/denylist.txt${AGENCY_DENYLIST:+:$AGENCY_DENYLIST}"
fi

# 1. Credentials in the lines this commit adds.
bash "$ROOT/06_Engine/scripts/scan-staged-credentials.sh"

# 2. Review the staged tree, not the working tree: export the index to a scratch folder.
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/agency-precommit.XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT
TREE="$SCRATCH/tree"
if git checkout-index --all --prefix="$TREE/" 2>/dev/null; then
  (
    cd "$TREE"
    git init -q
    git -c core.autocrlf=false add -A >/dev/null 2>&1
    # Plug-in mounts are gitlinks: keep them pinned in the scratch index and expose the checked-out copy.
    git -C "$ROOT" ls-files -s | awk -F'\t' '$1 ~ /^160000 / {split($1, meta, " "); print meta[2] "\t" $2}' |
      while IFS=$'\t' read -r sha mount; do
        if [ -d "$ROOT/$mount" ]; then
          rm -rf "${TREE:?}/$mount"; mkdir -p "$(dirname "$TREE/$mount")"; ln -s "$ROOT/$mount" "$TREE/$mount"
        fi
        git update-index --add --cacheinfo "160000,$sha,$mount"
      done
  )
  PYTHONDONTWRITEBYTECODE=1 "$PY" "$TREE/00_Agentic-OS/agentic-os-review.py" --fast
else
  echo "pre-commit: could not export the index; reviewing the working tree instead" >&2
  PYTHONDONTWRITEBYTECODE=1 "$PY" 00_Agentic-OS/agentic-os-review.py --fast
fi
