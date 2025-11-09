#!/bin/bash

# Activate virtual environment and run the SHL Recommendation System

echo "🚀 Starting SHL Assessment Recommendation System"
echo "================================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find virtual environment (look in parent directories)
VENV_PATH="${VENV_PATH:-$(find "$SCRIPT_DIR/../.." -maxdepth 2 -name "vir_env" -o -name "venv" -o -name ".venv" | head -1)}"

# Activate virtual environment if found
if [ -n "$VENV_PATH" ] && [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✓ Virtual environment activated: $VENV_PATH"
else
    echo "ℹ Using current Python environment"
fi

# Navigate to app directory
cd "$SCRIPT_DIR"

echo "✓ Starting server on http://localhost:8000"
echo ""

# Detect Poetry or use python directly
if command -v poetry &> /dev/null; then
    poetry run python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fi
