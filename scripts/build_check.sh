#!/usr/bin/env bash
# build_check.sh
# Runs the Python-based build check helper. Exits non-zero on failures.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/Scripts/python"

# If project uses src/ layout, include it on PYTHONPATH so imports like `app.*` work
if [ -d "$ROOT_DIR/src" ]; then
  export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH+:$PYTHONPATH}"
  echo "[build_check] PYTHONPATH includes $ROOT_DIR/src"
fi

if [ ! -x "$PYTHON_BIN" ]; then
  echo "[build_check] Python in virtualenv not found at $PYTHON_BIN"
  echo "[build_check] Please run scripts/setup_and_run.sh first to create venv and install requirements"
  exit 2
fi

echo "[build_check] running build_check.py"
"$PYTHON_BIN" "$ROOT_DIR/scripts/build_check.py" "$@"
