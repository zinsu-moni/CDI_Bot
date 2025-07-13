#!/bin/bash
# CDI Backend Startup Script for Linux/Mac
# This script starts the FastAPI backend with environment variable support

echo "====================================="
echo "CDI Backend Startup Script"
echo "====================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys."
    exit 1
fi

echo ".env file found, loading configuration..."

# Install requirements if needed
echo "Checking Python dependencies..."
pip install -q python-dotenv fastapi uvicorn pillow requests openai

# Start the FastAPI server
echo "Starting CDI Backend API server..."
python main_fastapi.py
