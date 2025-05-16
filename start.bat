@echo off
echo JamiBilling RDN Fee Scraper
echo ==============================
echo.

rem Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or later and make sure it's in your PATH.
    pause
    exit /b 1
)

echo Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
echo This may take a few minutes...

rem Install individual packages with error handling to avoid build errors
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

echo.
echo Creating required directories...
if not exist "static\exports" mkdir static\exports
if not exist "flask_session" mkdir flask_session
if not exist "drivers" mkdir drivers

echo.
echo Starting JamiBilling application...
echo.
echo Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
