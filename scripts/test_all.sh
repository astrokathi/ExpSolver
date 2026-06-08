#!/usr/bin/env bash
set -e

echo "[TEST RUNNER] Disabling Langfuse telemetry for test suite..."
export LANGFUSE_PUBLIC_KEY=""
export LANGFUSE_SECRET_KEY=""
export LANGFUSE_HOST=""

echo "[TEST RUNNER] Executing pytest..."
python -m pytest tests/ -v --tb=short
