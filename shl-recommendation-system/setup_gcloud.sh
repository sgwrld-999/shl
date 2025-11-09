#!/bin/bash

# SHL Assessment Recommendation System - Google Cloud Setup Script
# This script helps set up the project for deployment on Google Cloud

set -e

echo "=================================================="
echo "SHL Assessment Recommendation System - GCP Setup"
echo "=================================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✓ gcloud CLI found"

# Get project ID from .env or prompt
PROJECT_ID="shl-recommender-477516"
LOCATION="us-central1"
BUCKET_NAME="shl-agent-staging"

echo ""
echo "Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Location: $LOCATION"
echo "  Bucket: gs://$BUCKET_NAME"
echo ""

read -p "Is this configuration correct? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
    read -p "Enter location (default: us-central1): " LOCATION
    LOCATION=${LOCATION:-us-central1}
    read -p "Enter bucket name (without gs://): " BUCKET_NAME
fi

echo ""
echo "Step 1: Authenticating with Google Cloud..."
gcloud auth login

echo ""
echo "Step 2: Setting default project..."
gcloud config set project $PROJECT_ID

echo ""
echo "Step 3: Enabling required APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
echo "✓ APIs enabled"

echo ""
echo "Step 4: Creating Cloud Storage bucket..."
if gsutil ls gs://$BUCKET_NAME &> /dev/null; then
    echo "✓ Bucket already exists: gs://$BUCKET_NAME"
else
    gsutil mb -l $LOCATION gs://$BUCKET_NAME
    echo "✓ Bucket created: gs://$BUCKET_NAME"
fi

echo ""
echo "Step 5: Setting up application default credentials..."
gcloud auth application-default login

echo ""
echo "Step 6: Updating .env file..."
cat > app/.env << EOF
# Environment Configuration for SHL Recommendation System

# Enable Google Vertex AI for Generative AI
GOOGLE_GENAI_USE_VERTEXAI=TRUE

# Vertex backend config
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=$LOCATION
GOOGLE_CLOUD_STAGING_BUCKET=gs://$BUCKET_NAME

# Google API Key (required for Gemini model)
GEMINI_API_KEY=AIzaSyCqMxXXHLGbG-eRx7YLOXBwWPwZq4dnLOw

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Data Configuration
DATA_PATH=../data/individual-assessment.json

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
GEMINI_MODEL=gemini-2.0-flash-exp

# Search Configuration
DEFAULT_MAX_RESULTS=10
EOF
echo "✓ .env file updated"

echo ""
echo "Step 7: Installing Poetry (if not installed)..."
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    echo "✓ Poetry installed"
else
    echo "✓ Poetry already installed"
fi

echo ""
echo "Step 8: Installing project dependencies..."
poetry install
echo "✓ Dependencies installed"

echo ""
echo "=================================================="
echo "✓ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   poetry shell"
echo ""
echo "2. Test locally:"
echo "   poetry run deploy-local"
echo ""
echo "3. Deploy to Google Cloud:"
echo "   poetry run deploy-remote --create"
echo ""
echo "For more information, see DEPLOYMENT.md"
echo ""
