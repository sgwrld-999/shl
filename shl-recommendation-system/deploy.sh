#!/bin/bash

# Simple deployment script for Cloud Run
set -e

echo "🚀 Deploying SHL Recommendation System to Cloud Run..."

# Load environment variables
source .env

# Set defaults
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-shl-recommender-477516}"
REGION="${LOCATION:-us-central1}"
SERVICE_NAME="shl-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "📦 Project: ${PROJECT_ID}"
echo "📍 Region: ${REGION}"
echo "🏷️  Image: ${IMAGE_NAME}"

# Set the project
gcloud config set project ${PROJECT_ID}

# Build the container image
echo "🔨 Building container image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "☁️  Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 600 \
  --max-instances 10 \
  --min-instances 0 \
  --port 8080 \
  --no-cpu-throttling \
  --set-env-vars GEMINI_API_KEY="${GEMINI_API_KEY}"

# Get the service URL
echo ""
echo "✅ Deployment complete!"
echo ""
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format='value(status.url)')
echo "🌐 Your API is live at: ${SERVICE_URL}"
echo ""
echo "Test endpoints:"
echo "  Health check: ${SERVICE_URL}/health"
echo "  Recommend: ${SERVICE_URL}/recommend"
echo ""
