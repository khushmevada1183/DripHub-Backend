#!/usr/bin/env bash
# setup_and_run.sh
# Creates a Python venv (if missing), installs requirements, runs DB prep if present, and starts the FastAPI app with uvicorn.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/Scripts/python"
PIP_BIN="$VENV_DIR/Scripts/pip"

# If project uses src/ layout (e.g. src/app/), make sure PYTHONPATH points at src
if [ -d "$ROOT_DIR/src" ]; then
  export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH+:$PYTHONPATH}"
  echo "[setup_and_run] PYTHONPATH includes $ROOT_DIR/src"
fi

echo "[setup_and_run] project root: $ROOT_DIR"

if [ ! -f "$ROOT_DIR/requirements.txt" ]; then
  echo "[setup_and_run] ERROR: requirements.txt not found in project root ($ROOT_DIR)"
  exit 2
fi

create_venv() {
  if [ ! -d "$VENV_DIR" ]; then
    echo "[setup_and_run] creating virtualenv at $VENV_DIR"
    python -m venv "$VENV_DIR"
  else
    echo "[setup_and_run] virtualenv already exists at $VENV_DIR"
  fi
}

install_requirements() {
  echo "[setup_and_run] installing requirements"
  "$PIP_BIN" install --upgrade pip setuptools wheel
  # Use --upgrade-strategy only-if-needed for faster idempotent installs
  "$PIP_BIN" install -r "$ROOT_DIR/requirements.txt"
}

run_db_migrations_if_any() {
  # Optional: if alembic or similar is present, run migrations.
  if [ -f "$ROOT_DIR/alembic.ini" ]; then
    echo "[setup_and_run] alembic.ini found, running alembic upgrade head"
    "$PYTHON_BIN" -m alembic upgrade head
  fi
}

start_uvicorn() {
  # Allow overriding the app module to run (e.g. APP_MODULE="app.main:app")
  APP_MODULE="${APP_MODULE:-app.main:app}"
  HOST=${HOST:-0.0.0.0}
  PORT=${PORT:-8000}
  WORKERS=${WORKERS:-1}

  # If project uses src/ layout, pass --app-dir src so uvicorn can import `app` from root
  UVICORN_APP_DIR_FLAG=""
  UVICORN_APP_DIR_VALUE=""
  if [ -d "$ROOT_DIR/src" ]; then
    # store flag and value separately so we can append as two argv elements
    UVICORN_APP_DIR_FLAG="--app-dir"
    UVICORN_APP_DIR_VALUE="src"
    echo "[setup_and_run] detected src/ layout, will start uvicorn with --app-dir src"
  fi

  # Allow passing extra uvicorn args via UVICORN_EXTRA_ARGS (quoted string)
  UVICORN_EXTRA_ARGS=${UVICORN_EXTRA_ARGS:-""}

  echo "[setup_and_run] Starting uvicorn on ${HOST}:${PORT} (workers=${WORKERS})"
  CMD=("$PYTHON_BIN" -m uvicorn "$APP_MODULE")
  if [ -n "$UVICORN_APP_DIR_FLAG" ]; then
    if [ -n "$UVICORN_APP_DIR_VALUE" ]; then
      CMD+=("$UVICORN_APP_DIR_FLAG" "$UVICORN_APP_DIR_VALUE")
    else
      CMD+=("$UVICORN_APP_DIR_FLAG")
    fi
  fi
  CMD+=(--host "$HOST" --port "$PORT" --workers "$WORKERS" --reload)

  # Expand UVICORN_EXTRA_ARGS into the CMD safely (using eval when non-empty)
  if [ -n "$UVICORN_EXTRA_ARGS" ]; then
    echo "[setup_and_run] adding extra uvicorn args: $UVICORN_EXTRA_ARGS"
    # Use eval to split quoted args correctly into the command
    eval 'set -- '"$UVICORN_EXTRA_ARGS"
    for a in "$@"; do
      CMD+=("$a")
    done
  fi

  echo "[setup_and_run] exec: ${CMD[*]}"
  exec "${CMD[@]}"
}

main() {
  create_venv
  install_requirements
  run_db_migrations_if_any
  start_uvicorn
}

main
