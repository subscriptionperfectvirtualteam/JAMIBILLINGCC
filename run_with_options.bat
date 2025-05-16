@echo off
echo JamiBilling - Run with Options
echo ==============================
echo.

rem Check for Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or later and make sure it's in your PATH.
    pause
    exit /b 1
)

echo Choose how you want to run the browser:
echo 1. Show browser windows (default)
echo 2. Minimize browser windows
echo 3. Try to hide browser windows (may not work with all setups)
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="2" (
    echo Running with minimized browser windows...
    set JAMI_MINIMIZE_BROWSER=true
) else if "%choice%"=="3" (
    echo Running with hidden browser windows...
    set JAMI_MINIMIZE_BROWSER=true
    rem This tries to use a virtual display if available
    set JAMI_HIDE_BROWSER=true
) else (
    echo Running with visible browser windows...
    set JAMI_MINIMIZE_BROWSER=false
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
