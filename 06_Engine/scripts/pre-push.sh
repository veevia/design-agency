#!/usr/bin/env bash
# pre-push — full OS review at the publish boundary (install with 06_Engine/scripts/install-hooks.sh).
# Bypass deliberately with: git push --no-verify
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
PYTHONDONTWRITEBYTECODE=1 "${AGENCY_PYTHON:-python3}" 00_Agentic-OS/agentic-os-review.py
