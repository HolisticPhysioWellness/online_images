#!/usr/bin/env bash
# Rebuild the handout PDF. Needs python3 and Node with Playwright (Chromium).
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
node pdf.js handout.html ../road-to-your-first-pull-up-2026-09.pdf
rm -f handout.html
