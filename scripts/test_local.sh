#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate || true

pytest -q --maxfail=1 --disable-warnings --cov=backend --cov-report=term-missing backend/tests
