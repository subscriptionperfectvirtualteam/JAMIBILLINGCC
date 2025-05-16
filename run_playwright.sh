#!/bin/bash

echo "JamiBilling - RDN Fee Scraper (Playwright Version)"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH!"
    echo "Please install Python 3.8 or later and make sure it's in your PATH."
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found!"
    echo "Please run install_playwright.sh first."
    exit 1
fi

# Create required directories
mkdir -p debug
mkdir -p static/exports
mkdir -p flask_session

# Ask about browser visibility
echo "How would you like to run the browser?"
echo "1. Show browser windows (default)"
echo "2. Try to hide browser windows"
echo
read -p "Enter your choice (1-2): " browser_choice

if [ "$browser_choice" == "2" ]; then
    echo "Running with hidden browser windows..."
    export JAMI_HIDE_BROWSER=true
else
    echo "Running with visible browser windows..."
    export JAMI_HIDE_BROWSER=false
fi

echo
echo "Starting JamiBilling with Playwright..."
echo
echo "Access the application at: http://localhost:5000"
echo "Debug logs will be saved to jami_billing.log and debug/ directory"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 app_playwright.py