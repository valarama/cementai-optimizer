#!/bin/bash

set -e

PROJECT_ID="cementai-optimiser"
REGION="us-central1"

echo "🚀 CementAI Optimizer - One-Command Deploy"
echo "=========================================="
echo ""

# Deploy Backend
echo "📦 Step 1/2: Deploying Backend API..."
cd backend
gcloud run deploy cementai-backend \
  --source . \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars PROJECT_ID=$PROJECT_ID

BACKEND_URL=$(gcloud run services describe cementai-backend \
  --region $REGION \
  --project $PROJECT_ID \
  --format="value(status.url)")

echo "✅ Backend deployed: $BACKEND_URL"
echo ""

# Deploy Frontend
echo "📦 Step 2/2: Deploying Frontend..."
cd ../frontend
gcloud run deploy cementai-optimizer \
  --source . \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --memory 2Gi \
  --set-env-vars NEXT_PUBLIC_API_URL=$BACKEND_URL

FRONTEND_URL=$(gcloud run services describe cementai-optimizer \
  --region $REGION \
  --project $PROJECT_ID \
  --format="value(status.url)")

echo ""
echo "🎉 Deployment Complete!"
echo "=========================================="
echo "Frontend URL: $FRONTEND_URL"
echo "Backend URL:  $BACKEND_URL"
echo ""
echo "✅ Your CementAI Optimizer is now live!"
