#!/usr/bin/env bash
set -e

echo "=========================================="
echo "    BODMAS Engine CI/CD Pipeline Mock     "
echo "=========================================="

echo "-> [Step 1] Dependency Checks..."
if [ ! -f requirements.txt ]; then
    echo "ERROR: requirements.txt missing!"
    exit 1
fi
echo "Dependencies found."

echo "-> [Step 2] Static Analysis / Linting (Simulated)..."
# In a real scenario we might run flake8 src/ tests/
echo "Linting passed."

echo "-> [Step 3] Test Execution..."
./scripts/test_all.sh
if [ $? -ne 0 ]; then
    echo "ERROR: Test suite failed."
    exit 1
fi
echo "Tests passed."

echo "=========================================="
echo "          PIPELINE SUCCESSFUL             "
echo "=========================================="
