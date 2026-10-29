#!/usr/bin/env bash
# install-hooks — install pre-commit and pre-push wrappers that run the active worktree's gates.
# Honours core.hooksPath; an existing foreign hook is kept as <hook>.bak.<timestamp>. Remove a wrapper to disable it.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "install-hooks: not inside a git repository" >&2; exit 1; }
cd "$ROOT"
HOOKS_DIR="$(git config --get core.hooksPath || true)"
if [ -z "$HOOKS_DIR" ]; then
  HOOKS_DIR="$(git rev-parse --git-common-dir)/hooks"
elif [ "${HOOKS_DIR#/}" = "$HOOKS_DIR" ]; then
  HOOKS_DIR="$ROOT/$HOOKS_DIR"
fi
mkdir -p "$HOOKS_DIR"
MARK="# design-agency-os hook wrapper"
for hook in pre-commit pre-push; do
  target="$HOOKS_DIR/$hook"
  if [ -e "$target" ] || [ -L "$target" ]; then
    if grep -q "$MARK" "$target" 2>/dev/null; then
      :  # our wrapper: refresh in place
    else
      backup="$target.bak.$(date +%Y%m%d%H%M%S)"
      mv "$target" "$backup"
      echo "install-hooks: kept the previous $hook as $(basename "$backup")"
    fi
  fi
  cat > "$target" <<WRAPPER
#!/usr/bin/env bash
$MARK — runs the script of whichever worktree is committing.
exec bash "\$(git rev-parse --show-toplevel)/06_Engine/scripts/$hook.sh" "\$@"
WRAPPER
  chmod +x "$target"
  echo "install-hooks: installed $hook"
done
