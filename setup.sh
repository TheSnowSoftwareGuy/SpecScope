#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r backend/requirements.txt

mkdir -p data/storage
python - <<'PY'
from backend.app.config import sqlite_conn, init_sqlite_schema
init_sqlite_schema(sqlite_conn)
print("SQLite initialized at data/specscope.db")
PY

echo "Setup complete."