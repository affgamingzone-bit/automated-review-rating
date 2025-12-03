#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Running Django migrations..."
python backend/manage.py migrate

echo "Collecting static files..."
python backend/manage.py collectstatic --noinput

echo "Build completed successfully!"
