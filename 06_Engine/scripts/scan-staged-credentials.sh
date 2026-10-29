#!/usr/bin/env bash
# scan-staged-credentials — fail when a line the next commit ADDS looks like a credential.
# Removed lines are ignored (removing a secret must never be blocked). Matched values are never printed.
set -euo pipefail
added="$(git diff --cached -U0 --no-color --no-ext-diff | grep -E '^\+' | grep -v -E '^\+\+\+ ' || true)"
# A here-string, not a pipe into `grep -q`: an early match can never be lost to SIGPIPE under pipefail.
if grep -E -q -e '-----BEGIN [A-Z ]*PRIVATE KEY-----' -e '(ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}' \
     -e 'sk-[A-Za-z0-9_-]{20,}' -e 'xox[abp]-[A-Za-z0-9-]{10,}' -e 'AKIA[0-9A-Z]{16}' <<<"$added"; then
  echo "credential scan: a staged line looks like a credential. Remove it (and rotate it) before committing." >&2
  exit 1
fi
