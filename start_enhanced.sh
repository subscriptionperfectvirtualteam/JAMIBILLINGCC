#!/bin/bash

echo "JamiBilling RDN Fee Scraper (Enhanced Version)"
echo "=============================================="
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
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
echo "This may take a few minutes..."

# Install individual packages with error handling to avoid build errors
pip install Flask==2.2.3
pip install Flask-Session==0.4.0
pip install selenium==4.8.2
pip install beautifulsoup4==4.11.2
pip install pypyodbc==1.3.6
pip install xlsxwriter==3.0.9
pip install openpyxl==3.1.2
pip install Werkzeug==2.2.3
pip install Jinja2==3.1.2
pip install requests==2.28.2

echo
echo "Creating required directories..."
mkdir -p static/exports
mkdir -p flask_session
mkdir -p debug
mkdir -p drivers

# Ask about browser visibility
echo "How would you like to run the browser?"
echo "1. Show browser windows (default)"
echo "2. Minimize browser windows"
echo "3. Try to hide browser windows (may not work with all setups)"
echo
read -p "Enter your choice (1-3): " browser_choice

if [ "$browser_choice" == "2" ]; then
    echo "Running with minimized browser windows..."
    export JAMI_MINIMIZE_BROWSER=true
elif [ "$browser_choice" == "3" ]; then
    echo "Running with hidden browser windows..."
    export JAMI_MINIMIZE_BROWSER=true
    export JAMI_HIDE_BROWSER=true
else
    echo "Running with visible browser windows..."
    export JAMI_MINIMIZE_BROWSER=false
fi

echo
echo "Starting JamiBilling Enhanced application..."
echo
echo "Access the application at: http://localhost:5000"
echo "Debug logs will be saved to jami_billing.log and debug/ directory"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 app_enhanced.py