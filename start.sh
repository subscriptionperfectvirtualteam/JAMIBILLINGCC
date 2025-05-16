#!/bin/bash

echo "JamiBilling RDN Fee Scraper"
echo "=============================="
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

echo
echo "Starting JamiBilling application..."
echo
echo "Access the application at: http://localhost:5000"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 app.py
