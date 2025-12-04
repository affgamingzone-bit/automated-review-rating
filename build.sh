#!/bin/bash
set -e

echo "Current working directory: $(pwd)"
echo ""

echo "=== Installing Python dependencies ==="
pip install -r backend/requirements.txt

echo ""
echo "=== Downloading ML Model Files ==="
mkdir -p backend/models
cd backend/models

# These URLs point to GitHub Releases
# Replace with your actual release URL once you upload the files
MODEL_URL="https://github.com/affgamingzone-bit/automated-review-rating/releases/download/v1.0/best_ml_model.pkl"
VECTORIZER_URL="https://github.com/affgamingzone-bit/automated-review-rating/releases/download/v1.0/best_ml_vectorizer.pkl"
SVD_URL="https://github.com/affgamingzone-bit/automated-review-rating/releases/download/v1.0/best_ml_svd.pkl"

download_file() {
  local url=$1
  local output=$2
  echo "Attempting to download $output..."
  if curl -L -f --connect-timeout 30 -o "$output" "$url" 2>&1; then
    if [ -s "$output" ]; then
      echo "✅ Successfully downloaded $output ($(ls -lh $output | awk '{print $5}'))"
      return 0
    else
      echo "⚠️  File is empty: $output"
      return 1
    fi
  else
    echo "⚠️  Could not download $output"
    return 1
  fi
}

echo "Downloading model files from GitHub Releases..."
download_file "$MODEL_URL" "best_ml_model.pkl" || echo "Model download failed - will try local fallback"
download_file "$VECTORIZER_URL" "best_ml_vectorizer.pkl" || echo "Vectorizer download failed"
download_file "$SVD_URL" "best_ml_svd.pkl" || echo "SVD download failed"

echo ""
echo "Files in backend/models:"
ls -lh

cd ../..

echo ""
echo "=== Running Django migrations ==="
python backend/manage.py migrate

echo ""
echo "=== Collecting static files ==="
python backend/manage.py collectstatic --noinput || echo "Static files collection had issues but continuing..."

echo ""
echo "✅ Build completed successfully!"
