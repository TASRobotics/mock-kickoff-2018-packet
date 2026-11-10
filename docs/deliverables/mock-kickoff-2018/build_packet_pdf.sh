#!/usr/bin/env bash
# Build mock-kickoff PDF with figures embedded (must run from this directory).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

MD=mock-kickoff-2018-packet.md
CSS=mock-kickoff-2018-packet.css
HTML=mock-packet.html
PDF=mock-kickoff-2018-packet.pdf

echo "build cwd=$ROOT"
pandoc "$MD" \
  -f markdown+raw_html \
  -t html5 \
  -s \
  --resource-path="$ROOT:$ROOT/figures:$ROOT/figures/official:$ROOT/figures/tagged" \
  -o "$HTML"

python3 -m weasyprint "$HTML" "$PDF" -s "$CSS"
ls -la "$PDF"
python3 "$ROOT/verify_packet_pdf.py" "$PDF"
