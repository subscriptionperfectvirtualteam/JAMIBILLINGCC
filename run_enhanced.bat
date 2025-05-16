@echo off
echo JamiBilling - RDN Fee Scraper (Enhanced Version)
echo ================================================
echo.

rem Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or later and make sure it's in your PATH.
    pause
    exit /b 1
)

echo This script runs JamiBilling with enhanced debugging and error handling.
echo It will create detailed logs and screenshots to help diagnose issues.
echo.

rem Create required directories
if not exist "debug" mkdir debug
if not exist "static\exports" mkdir static\exports
if not exist "flask_session" mkdir flask_session
if not exist "drivers" mkdir drivers

rem Check if virtual environment exists
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found!
    echo Please run install_dependencies.bat first.
    pause
    exit /b 1
)

rem Ask about browser visibility
echo How would you like to run the browser?
echo 1. Show browser windows (default)
echo 2. Minimize browser windows
echo 3. Try to hide browser windows (may not work with all setups)
echo.
set /p browser_choice="Enter your choice (1-3): "

if "%browser_choice%"=="2" (
    echo Running with minimized browser windows...
    set JAMI_MINIMIZE_BROWSER=true
) else if "%browser_choice%"=="3" (
    echo Running with hidden browser windows...
    set JAMI_MINIMIZE_BROWSER=true
    set JAMI_HIDE_BROWSER=true
) else (
    echo Running with visible browser windows...
    set JAMI_MINIMIZE_BROWSER=false
)

echo.
echo Starting JamiBilling Enhanced application...
echo.
echo Access the application at: http://localhost:5000
echo Debug logs will be saved to jami_billing.log and debug/ directory
echo.
echo Press Ctrl+C to stop the server
echo.

python app_enhanced.py

pause
