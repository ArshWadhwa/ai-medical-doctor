#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Copy manifest.json to static directory
cp manifest.json static/

# Set environment variables if not already set
export PORT=${PORT:-10000} 