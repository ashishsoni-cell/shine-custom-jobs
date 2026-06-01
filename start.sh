#!/bin/bash
set -e
python3 -m pip install --user google-search-results -q || true
cd "$(dirname "$0")"
python3 backend/server.py
