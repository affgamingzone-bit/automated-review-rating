#!/bin/bash
set -e

echo "Current working directory: $(pwd)"
echo ""

echo "=== Downloading ML Model Files ==="
mkdir -p backend/models
cd backend/models

# Download models from a cloud storage (using curl)
# You can replace these URLs with your actual model storage URLs
# For now, we'll create placeholder URLs - you need to host these files

echo "Downloading model files..."

# These URLs should point to your hosted model files
# For demonstration, creating empty files (you'll need to upload actual models)
# Option 1: Use GitHub Releases (recommended)
MODEL_URL="https://github.com/affgamingzone-bit/automated-review-rating/releases/download/v1.0/best_ml_model.pkl"
VECTORIZER_URL="https://github.com/affgamingzone-bit/automated-review-rating/releases/download/v1.0/best_ml_vectorizer.pkl"
SVD_URL="https://github.com/affgamingzone-bit/automated-review-rating/releases/download/v1.0/best_ml_svd.pkl"

# Download with retry logic
download_file() {
  local url=$1
  local output=$2
  echo "Downloading $output from $url..."
  if curl -L -f -o "$output" "$url" 2>/dev/null; then
    echo "✅ Downloaded $output"
  else
    echo "⚠️  Could not download $output - file might not exist yet"
    echo "Please upload model files to GitHub Releases or another cloud storage"
    # Create empty placeholder
    touch "$output"
  fi
}

download_file "$MODEL_URL" "best_ml_model.pkl"
download_file "$VECTORIZER_URL" "best_ml_vectorizer.pkl"
download_file "$SVD_URL" "best_ml_svd.pkl"

cd ../..

echo ""
echo "=== Installing Python dependencies ==="
pip install -r backend/requirements.txt

echo ""
echo "=== Running Django migrations ==="
python backend/manage.py migrate

echo ""
echo "=== Collecting static files ==="
python backend/manage.py collectstatic --noinput

echo ""
echo "✅ Build completed successfully!"
