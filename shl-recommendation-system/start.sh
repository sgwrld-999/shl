#!/bin/bash

# SHL Recommender - Quick Start Script

echo "========================================"
echo "🚀 SHL Assessment Recommender"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"
    echo "   Activating: /Users/siddhantgond/Desktop/shl/vir_env"
    source /Users/siddhantgond/Desktop/shl/vir_env/bin/activate || {
        echo "❌ Failed to activate virtual environment"
        exit 1
    }
    echo "✅ Virtual environment activated"
    echo ""
fi

# Install required packages
echo "📦 Installing dependencies..."
pip install -q fastapi uvicorn pyngrok pydantic || {
    echo "❌ Failed to install dependencies"
    exit 1
}
echo "✅ Dependencies installed"

echo ""
echo "Choose an option:"
echo "1) Start with PUBLIC URL (recommended for SHL submission)"
echo "2) Start LOCALLY only (localhost:8000)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🌐 Starting with public URL..."
        echo ""
        python start_public.py
        ;;
    2)
        echo ""
        echo "🏠 Starting locally..."
        echo ""
        python server.py
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
