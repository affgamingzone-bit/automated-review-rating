#!/bin/bash
set -e

echo "Current working directory: $(pwd)"
echo "Listing root directory contents:"
ls -la

echo ""
echo "=== Copying model files to backend ==="
mkdir -p backend/models

# The repository root is at /opt/render/project/src
# We need to copy from /opt/render/project/src/models to /opt/render/project/src/backend/models
REPO_ROOT=$(pwd)
SOURCE_MODELS="$REPO_ROOT/models"
DEST_MODELS="$REPO_ROOT/backend/models"

echo "Source: $SOURCE_MODELS"
echo "Destination: $DEST_MODELS"

if [ -d "$SOURCE_MODELS" ]; then
  echo "✅ Found models directory"
  echo "Contents:"
  ls -la "$SOURCE_MODELS"
  echo ""
  echo "Copying files..."
  cp -v "$SOURCE_MODELS"/*.pkl "$DEST_MODELS/" || echo "⚠️  Warning: Copy failed"
  echo "Copied files:"
  ls -la "$DEST_MODELS"
else
  echo "❌ Models directory not found at $SOURCE_MODELS"
  find "$REPO_ROOT" -name "*.pkl" -type f 2>/dev/null | head -20 || echo "No .pkl files found"
fi

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
