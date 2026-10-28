#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  exec python3 scripts/serve.py
elif command -v python >/dev/null 2>&1 && python --version 2>&1 | grep -qE 'Python 3\.'; then
  exec python scripts/serve.py
else
  echo "Python 3 was not found. Install Python 3 and run this launcher again." >&2
  echo "Download: https://www.python.org/downloads/" >&2
  exit 1
fi
