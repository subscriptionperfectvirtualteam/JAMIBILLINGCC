#!/bin/bash

echo "JamiBilling - Installing Playwright"
echo "=================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH!"
    echo "Please install Python 3.8 or later and make sure it's in your PATH."
    exit 1
fi

echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Using existing virtual environment."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing pip requirements..."
pip install -r requirements_playwright.txt

echo "Installing Playwright browsers..."
python -m playwright install chromium

echo
echo "Creating required directories..."
mkdir -p static/exports
mkdir -p flask_session
mkdir -p debug

echo
echo "Installation complete!"
echo
echo "You can now run the application with: python app_playwright.py"
echo