#!/bin/bash
set -e

echo "Copying model files to backend..."
mkdir -p backend/models
cp models/*.pkl backend/models/ || true

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Running Django migrations..."
python backend/manage.py migrate

echo "Collecting static files..."
python backend/manage.py collectstatic --noinput

echo "Build completed successfully!"
