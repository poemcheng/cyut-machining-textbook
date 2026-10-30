#!/bin/sh
set -eu
cd "$(dirname "$0")"
printf '%s\n' 'Open http://localhost:8000 in your browser. Press Ctrl+C to stop.'
exec python3 -m http.server 8000 --bind 127.0.0.1
