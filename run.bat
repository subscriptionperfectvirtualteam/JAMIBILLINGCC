@echo off
echo JamiBilling - RDN Fee Scraper
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

rem Check for virtual environment
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found!
    echo Please run install_dependencies.bat first.
    pause
    exit /b 1
)

echo.
echo Starting JamiBilling application...
echo.
echo Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
