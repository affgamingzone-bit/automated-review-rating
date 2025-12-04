#!/bin/bash
set -e

echo "Current working directory: $(pwd)"
echo "Listing root directory contents:"
ls -la

echo "Copying model files to backend..."
mkdir -p backend/models

# Copy models from root models directory to backend/models
if [ -d "models" ]; then
  echo "Found models directory, copying files..."
  cp -v models/*.pkl backend/models/ || echo "Warning: Some model files not found"
  ls -la backend/models/
else
  echo "Models directory not found in $(pwd)"
  find . -name "*.pkl" -type f 2>/dev/null || echo "No .pkl files found"
fi

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Running Django migrations..."
python backend/manage.py migrate

echo "Collecting static files..."
python backend/manage.py collectstatic --noinput

echo "Build completed successfully!"
