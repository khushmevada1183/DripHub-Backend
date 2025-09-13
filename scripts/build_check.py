#!/usr/bin/env python3
"""
build_check.py
Comprehensive pre-deploy build checker.

Checks performed (best-effort, non-invasive):
- import-only verification for key modules
- run unit tests (pytest) if available
- run ruff/flake8/mypy if installed in the environment
- simple runtime smoke: import FastAPI app and ensure ASGI app callable exists

Usage: python scripts/build_check.py [--fast]
"""
import argparse
import importlib
import importlib.util
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# If the repo uses a src/ layout (e.g. src/app/), prefer that on sys.path so imports like `app.*` continue to work.
SRC_DIR = ROOT / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))
else:
    sys.path.insert(0, str(ROOT))

MODULES_TO_IMPORT = [
    "app.main",
    "app.api.api_v1.api",
    "app.api.api_v1.routers.cart",
    "app.api.api_v1.routers.wishlist",
    "app.models.schemas.product",
    "app.models.schemas.cart",
]


def run(cmd, check=True, capture=False, env=None):
    if isinstance(cmd, list):
        proc = subprocess.run(cmd, check=check, stdout=(subprocess.PIPE if capture else None), stderr=(subprocess.PIPE if capture else None), env=env)
    else:
        proc = subprocess.run(cmd, shell=True, check=check, stdout=(subprocess.PIPE if capture else None), stderr=(subprocess.PIPE if capture else None), env=env)
    return proc


def import_check(modules):
    results = {}
    for m in modules:
        try:
            importlib.import_module(m)
            results[m] = {"ok": True}
        except Exception as e:
            results[m] = {"ok": False, "error": repr(e)}
    return results


def run_linters():
    results = {}
    # ruff
    if importlib.util.find_spec("ruff") is not None:
        try:
            proc = run([sys.executable, "-m", "ruff", "--select", "E,F,W,D", str(ROOT)], check=False, capture=True)
            out = proc.stdout.decode(errors="replace") if proc.stdout else ""
            results["ruff"] = {"ok": proc.returncode == 0, "output": out}
        except subprocess.CalledProcessError as e:
            results["ruff"] = {"ok": False, "output": getattr(e, 'output', str(e))}
    else:
        results["ruff"] = {"ok": None, "output": "not-installed"}

    # mypy
    if importlib.util.find_spec("mypy") is not None:
        try:
            proc = run([sys.executable, "-m", "mypy", str(ROOT)], check=False, capture=True)
            out = (proc.stdout.decode(errors="replace") if proc.stdout else "") + (proc.stderr.decode(errors="replace") if proc.stderr else "")
            results["mypy"] = {"ok": proc.returncode == 0, "output": out}
        except subprocess.CalledProcessError as e:
            results["mypy"] = {"ok": False, "output": getattr(e, 'output', str(e))}
    else:
        results["mypy"] = {"ok": None, "output": "not-installed"}

    # pytest
    if importlib.util.find_spec("pytest") is not None:
        try:
            proc = run([sys.executable, "-m", "pytest", "-q"], check=False, capture=True)
            out = proc.stdout.decode(errors="replace") if proc.stdout else ""
            # If pytest reports "no tests ran" treat that as OK (no tests present)
            lowered = out.strip().lower()
            if "no tests ran" in lowered or "collected 0 items" in lowered:
                results["pytest"] = {"ok": True, "output": out, "note": "no-tests"}
            else:
                results["pytest"] = {"ok": proc.returncode == 0, "output": out}
        except subprocess.CalledProcessError as e:
            results["pytest"] = {"ok": False, "output": getattr(e, 'output', str(e))}
    else:
        results["pytest"] = {"ok": None, "output": "not-installed"}

    return results


def runtime_smoke():
    res = {}
    try:
        m = importlib.import_module("app.main")
        app = getattr(m, "app", None)
        res["fastapi_app_present"] = bool(app)
    except Exception as e:
        res["fastapi_app_present"] = False
        res["error"] = repr(e)
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true", help="Only run import checks and a quick smoke test")
    args = parser.parse_args()

    summary = {"import_check": {}, "linters": {}, "runtime": {}, "ok": True}

    print("[build_check] running import checks for modules:", MODULES_TO_IMPORT)
    imp = import_check(MODULES_TO_IMPORT)
    summary["import_check"] = imp
    if any(not v.get("ok") for v in imp.values()):
        summary["ok"] = False

    if not args.fast:
        print("[build_check] running linters, mypy and tests (if installed)")
        lin = run_linters()
        summary["linters"] = lin
        if any(v.get("ok") is False for v in lin.values()):
            summary["ok"] = False

    print("[build_check] running runtime smoke checks")
    rt = runtime_smoke()
    summary["runtime"] = rt
    if not rt.get("fastapi_app_present"):
        summary["ok"] = False

    print(json.dumps(summary, indent=2))

    if not summary["ok"]:
        print("[build_check] FAILURE: one or more checks failed")
        sys.exit(3)
    else:
        print("[build_check] SUCCESS: all checks passed (where available)")


if __name__ == "__main__":
    main()
