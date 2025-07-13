@echo off
REM CDI Backend Startup Script for Windows
REM This script starts the FastAPI backend with environment variable support

echo =====================================
echo CDI Backend Startup Script
echo =====================================

REM Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and configure your API keys.
    pause
    exit /b 1
)

echo .env file found, loading configuration...

REM Install requirements if needed
echo Checking Python dependencies...
pip install -q python-dotenv fastapi uvicorn pillow requests openai

REM Start the FastAPI server
echo Starting CDI Backend API server...
python main_fastapi.py

pause
