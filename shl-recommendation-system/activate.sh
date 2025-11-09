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

# Activate virtual environment
source /Users/siddhantgond/Desktop/shl/vir_env/bin/activate
export PATH="/Users/siddhantgond/.local/bin:$PATH"
cd /Users/siddhantgond/Desktop/shl/shl-recommendation-system

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo -e "${GREEN}✓ Poetry added to PATH${NC}"
echo -e "${GREEN}✓ Changed to project directory${NC}"
echo ""
echo "You can now run:"
echo "  poetry run python deployment/local.py          # Test locally"
echo "  poetry run python deployment/remote.py --create # Deploy to cloud"
echo ""
echo "For more commands, see SETUP_COMPLETE.md"
echo ""
