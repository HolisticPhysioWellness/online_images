#!/usr/bin/env bash
# Rebuild drawings + handout PDF. Needs python3 and Node with Playwright (Chromium).
set -euo pipefail
cd "$(dirname "$0")"
rm -rf svg svg_cropped png
python3 exercises.py > /dev/null
node crop.js svg svg_cropped png
python3 build.py
node pdf.js handout.html ../Road-to-Your-First-Pull-Up.pdf
rm -rf ../images/svg ../images/png && mv svg_cropped ../images/svg && mv png ../images/png
rm -rf svg sheet.html handout.html
