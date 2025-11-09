#!/bin/bash
# Quick activation script for SHL Recommendation System

# Colors for output
GREEN='\033[0.32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}SHL Recommendation System${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Get script directory for dynamic path resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use environment variables or detect paths dynamically
VENV_PATH="${VENV_PATH:-$(find "$SCRIPT_DIR/.." -maxdepth 2 -name "vir_env" -o -name "venv" -o -name ".venv" | head -1)}"
PROJECT_PATH="${PROJECT_PATH:-$SCRIPT_DIR}"
POETRY_PATH="${POETRY_PATH:-$HOME/.local/bin}"

# Fallback if detection fails
if [ -z "$VENV_PATH" ] || [ ! -d "$VENV_PATH" ]; then
    echo -e "${BLUE}Note: Virtual environment not found. Using current Python environment.${NC}"
else
    source "$VENV_PATH/bin/activate"
    echo -e "${GREEN}✓ Virtual environment activated: $VENV_PATH${NC}"
fi

export PATH="$POETRY_PATH:$PATH"
cd "$PROJECT_PATH"

echo -e "${GREEN}✓ Poetry added to PATH: $POETRY_PATH${NC}"
echo -e "${GREEN}✓ Project directory: $PROJECT_PATH${NC}"
echo ""
echo "You can now run:"
echo "  poetry run python deployment/local.py          # Test locally"
echo "  poetry run python deployment/remote.py --create # Deploy to cloud"
echo ""
echo "For more commands, see SETUP_COMPLETE.md"
echo ""
